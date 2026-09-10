"""Bank of Japan Time-Series Data Search — API client, flat files and probe.

The Bank launched a public API for BOJ Time-Series Data Search in February 2026
("Launch of API Service for BOJ Time-Series Data Search", notice 2026-02-18).
It is open: no registration, no key. Three endpoints are documented —
``getDataCode``, ``getDataLayer`` and ``getMetadata`` — over
``https://www.stat-search.boj.or.jp/api/v1`` with ``format=json``.

Two fallbacks exist if the API is unavailable or rate-limited:

* **Flat files.** ``/info/dload_en.html`` publishes zipped CSV packages for
  Prices, Flow of Funds, TANKAN, Balance of Payments and BIS-related
  statistics, refreshed by about 10:00 JST on each release day. TANKAN is the
  one that matters here: its flat-file series codes are the Data Search codes
  without the leading ``CO'``.
* **Per-statistic releases.** Each statistics page on ``boj.or.jp`` links the
  month's CSV/XLSX release (loan rates, CP rates, deposits and loans, ...).

This module is written to run in CI, where the Bank's hosts are reachable.
``python etl/boj_api.py --probe`` prints exactly which of the above respond and
what they return, so the series codes can be pinned from evidence rather than
guessed. ``--discover`` walks a database's code layers looking for a keyword.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import date

UA = "Mozilla/5.0 (compatible; JapanFCITracker/1.0; research)"
TIMEOUT = 60
API_BASE = "https://www.stat-search.boj.or.jp/api/v1"
DLOAD_PAGE = "https://www.stat-search.boj.or.jp/info/dload_en.html"

# Statistics index pages that publish the monthly release files directly.
RELEASE_PAGES = {
    "lending_rate": "https://www.boj.or.jp/en/statistics/dl/loan/yaku/index.htm",
    "cp_rate": "https://www.boj.or.jp/en/statistics/market/short/tankirate/index.htm",
    "loans_deposits": "https://www.boj.or.jp/en/statistics/dl/depo/index.htm",
    "output_gap": "https://www.boj.or.jp/en/research/research_data/gap/index.htm",
    "tankan": "https://www.boj.or.jp/en/statistics/tk/index.htm",
}

_LAST_CALL = [0.0]
MIN_INTERVAL = 1.0  # the Bank warns that excessive access frequency is throttled


def _get(url: str, timeout: int = TIMEOUT) -> bytes:
    wait = MIN_INTERVAL - (time.time() - _LAST_CALL[0])
    if wait > 0:
        time.sleep(wait)
    _LAST_CALL[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# ------------------------------------------------------------------ API -----
def api_url(endpoint: str, **params) -> str:
    params.setdefault("format", "json")
    parts = []
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            for item in v:
                parts.append((k, str(item)))
        else:
            parts.append((k, str(v)))
    return f"{API_BASE}/{endpoint}?" + urllib.parse.urlencode(parts)


def api(endpoint: str, **params):
    """Call one API endpoint and return the decoded JSON document."""
    return json.loads(_get(api_url(endpoint, **params)).decode("utf-8", "replace"))


def _walk(node, out, depth=0):
    """Collect (code, name) pairs from an arbitrarily shaped JSON response."""
    if isinstance(node, dict):
        code = node.get("code") or node.get("seriesCode") or node.get("dataCode")
        name = (node.get("name") or node.get("seriesName") or
                node.get("title") or node.get("label"))
        if code and isinstance(code, str):
            out.append((code, str(name or "")))
        for v in node.values():
            _walk(v, out, depth + 1)
    elif isinstance(node, list):
        for v in node:
            _walk(v, out, depth + 1)
    return out


def period_to_month_end(period, frequency: str):
    """BoJ period label -> month-end ISO date.

    Confirmed shapes (probe, 2026-09-10): monthly periods are YYYYMM
    (202607 = July 2026); quarterly ones are YYYYQQ with QQ in 01..04
    (202602 = 2026 Q2), so the same six digits mean different things and the
    series' own FREQUENCY has to decide. Annual periods are YYYY.
    """
    s = str(period).strip()
    freq = (frequency or "").upper()
    if len(s) == 6 and s.isdigit():
        y, n = int(s[:4]), int(s[4:])
        if freq.startswith("Q"):
            return _month_end(y, n * 3) if 1 <= n <= 4 else None
        return _month_end(y, n) if 1 <= n <= 12 else None
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:]}"
    if len(s) == 4 and s.isdigit():
        return f"{s}-12-31"
    return None


def normalize_period(p: str):
    """BoJ period labels -> month-end ISO date. Returns None if unrecognised."""
    p = p.strip()
    m = re.fullmatch(r"(\d{4})[-/]?(\d{2})", p)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            return _month_end(y, mo)
    m = re.fullmatch(r"(\d{4})[-/]?Q([1-4])", p, re.I)
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        return _month_end(y, q * 3)
    m = re.fullmatch(r"(\d{4})[-/](\d{2})[-/](\d{2})", p)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.fullmatch(r"(\d{4})", p)
    if m:
        return f"{m.group(1)}-12-31"
    return None


def _month_end(y: int, m: int) -> str:
    nd = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
    return date.fromordinal(nd.toordinal() - 1).isoformat()


def fetch_series(db: str, code: str, lang: str = "EN"):
    """Fetch one series as [(month_end_iso, float)].

    Response shape (confirmed): RESULTSET[0].VALUES holds two parallel lists,
    SURVEY_DATES and VALUES.
    """
    doc = api("getDataCode", db=db, code=code, lang=lang)
    if doc.get("STATUS") != 200:
        raise RuntimeError(f"{db}/{code}: STATUS {doc.get('STATUS')} {doc.get('MESSAGE')}")
    rows = []
    for entry in doc.get("RESULTSET") or []:
        vals = entry.get("VALUES") or {}
        dates = vals.get("SURVEY_DATES") or []
        values = vals.get("VALUES") or []
        freq = entry.get("FREQUENCY") or ""
        for period, value in zip(dates, values):
            if value in (None, "", "NA", "ND", "-"):
                continue
            try:
                v = float(str(value).replace(",", ""))
            except ValueError:
                continue
            iso = period_to_month_end(period, freq)
            if iso:
                rows.append((iso, v))
    rows.sort()
    return rows


# ----------------------------------------------------------- flat files -----
def scrape_links(page_url: str, exts=(".zip",)):
    """Absolute links on a page whose path ends with one of `exts`."""
    html = _get(page_url).decode("utf-8", "replace")
    out = []
    for href in re.findall(r'href="([^"]+)"', html, re.I):
        low = href.lower().split("?")[0]
        if low.endswith(tuple(e.lower() for e in exts)):
            out.append(urllib.parse.urljoin(page_url, href))
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def read_flat_zip(url: str, max_rows: int = 5):
    """Download a flat-file zip and return (member_names, sample_rows)."""
    blob = _get(url, timeout=180)
    zf = zipfile.ZipFile(io.BytesIO(blob))
    names = zf.namelist()
    sample = []
    if names:
        with zf.open(names[0]) as fh:
            text = io.TextIOWrapper(fh, encoding="cp932", errors="replace")
            for i, line in enumerate(text):
                if i >= max_rows:
                    break
                sample.append(line.rstrip("\n"))
    return names, sample


# ---------------------------------------------------------------- probe -----
# Parameter shapes to try, since the manual is not reachable from every network.
PROBE_CALLS = [
    ("getMetadata", {"db": "CO", "lang": "EN"}),
    ("getMetadata", {"db": "CO", "lang": "JP"}),
    ("getDataLayer", {"db": "CO", "layer1": "*", "lang": "EN"}),
    ("getDataCode", {"db": "CO", "code": "TK99F1000601GCQ01000", "lang": "EN"}),
    ("getDataCode", {"db": "CO", "code": "TK99F1000601GCQ01000", "lang": "JP"}),
    ("getMetadata", {"db": "IR04", "lang": "EN"}),
    ("getDataLayer", {"db": "IR04", "layer1": "*", "lang": "EN"}),
]


def _show(label, fn):
    print(f"\n=== {label} ===")
    try:
        fn()
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} {e.reason}")
        body = e.read()[:400].decode("utf-8", "replace")
        if body.strip():
            print(f"  body: {body}")
    except Exception as e:  # noqa: BLE001 - probe reports every failure verbatim
        print(f"  {type(e).__name__}: {e}")


def probe():
    print("BoJ connectivity probe")
    print(f"  api base   : {API_BASE}")
    print(f"  dload page : {DLOAD_PAGE}")

    for endpoint, params in PROBE_CALLS:
        url = api_url(endpoint, **params)

        def run(u=url):
            doc = json.loads(_get(u).decode("utf-8", "replace"))
            text = json.dumps(doc, ensure_ascii=False)
            print(f"  ok, {len(text)} chars")
            print(f"  top-level keys: {list(doc)[:12] if isinstance(doc, dict) else type(doc).__name__}")
            codes = _walk(doc, [])[:8]
            if codes:
                print("  sample codes:")
                for c, n in codes:
                    print(f"    {c:<26}{n[:70]}")
            pts = _points(doc, [])[:5]
            if pts:
                print(f"  sample points: {pts}")
            print(f"  head: {text[:300]}")
        _show(f"{endpoint} {params}", run)

    def flat():
        links = scrape_links(DLOAD_PAGE, (".zip",))
        print(f"  {len(links)} zip links")
        for u in links:
            print(f"    {u}")
        tankan = [u for u in links if "tankan" in u.lower() or "/co" in u.lower()]
        if tankan:
            names, sample = read_flat_zip(tankan[0])
            print(f"  opened {tankan[0]}")
            print(f"  members: {names[:6]}")
            for line in sample:
                print(f"    {line[:200]}")
    _show("flat files (dload_en.html)", flat)

    for label, page in RELEASE_PAGES.items():
        def rel(p=page):
            links = scrape_links(p, (".csv", ".xlsx", ".xls", ".zip"))
            print(f"  {len(links)} data links")
            for u in links[:12]:
                print(f"    {u}")
        _show(f"release page: {label}", rel)


def metadata_rows(db: str, lang: str = "EN"):
    """All catalogue rows for a database.

    Confirmed response shape (probe, 2026-09-10):
      {STATUS, MESSAGEID, MESSAGE, DATE, DB,
       RESULTSET: [{SERIES_CODE, NAME_OF_TIME_SERIES, UNIT, FREQUENCY,
                    CATEGORY, LAYER1..LAYER4}, ...]}
    Header rows carry an empty SERIES_CODE and name a layer, so they are kept:
    the layer names are what make a bare code readable.
    """
    doc = api("getMetadata", db=db, lang=lang)
    if doc.get("STATUS") != 200:
        raise RuntimeError(f"{db}: STATUS {doc.get('STATUS')} {doc.get('MESSAGE')}")
    return doc.get("RESULTSET") or []


def discover(db: str, keyword: str, lang: str = "EN", limit: int = 40):
    """Print catalogue entries in `db` whose name or category matches `keyword`."""
    kw = keyword.lower()
    try:
        rows = metadata_rows(db, lang)
    except Exception as e:  # noqa: BLE001
        print(f"  {db}: {type(e).__name__}: {e}")
        return []
    hits = []
    for r in rows:
        name = str(r.get("NAME_OF_TIME_SERIES") or "")
        cat = str(r.get("CATEGORY") or "")
        if kw in name.lower() or kw in cat.lower():
            hits.append(r)
    print(f"\n  db={db} '{keyword}': {len(hits)} of {len(rows)} rows match")
    for r in hits[:limit]:
        code = r.get("SERIES_CODE") or ""
        freq = r.get("FREQUENCY") or ""
        unit = r.get("UNIT") or ""
        layers = "/".join(str(r.get(f"LAYER{i}") or "") for i in range(1, 5))
        marker = "  " if code else "> "  # "> " marks a layer heading
        print(f"    {marker}{code:<24}{freq:<3}{str(r.get('NAME_OF_TIME_SERIES'))[:64]:<66}{unit[:14]:<16}{layers}")
    if len(hits) > limit:
        print(f"    ... {len(hits) - limit} more")
    return hits


def dump_series(db: str, code: str, lang: str = "EN"):
    """Print the shape of a getDataCode response: keys, and a slice of each array."""
    doc = api("getDataCode", db=db, code=code, lang=lang)
    print(f"\n  getDataCode db={db} code={code}")
    print(f"  top keys: {list(doc)}")
    for row in (doc.get("RESULTSET") or [])[:2]:
        print("  --- series row ---")
        for k, v in row.items():
            if isinstance(v, dict):
                print(f"    {k}: dict keys={list(v)}")
                for vk, vv in v.items():
                    if isinstance(vv, list):
                        print(f"      {vk}: list[{len(vv)}] head={vv[:6]} tail={vv[-6:]}")
                    else:
                        print(f"      {vk}: {vv!r}")
            elif isinstance(v, list):
                print(f"    {k}: list[{len(v)}] head={v[:6]} tail={v[-6:]}")
            else:
                print(f"    {k}: {v!r}")


def find(db: str, *terms, lang: str = "EN", limit: int = 12):
    """Print catalogue entries whose name contains EVERY term (AND, case-insensitive)."""
    wanted = [x.lower() for x in terms if x]
    try:
        rows = metadata_rows(db, lang)
    except Exception as e:  # noqa: BLE001
        print(f"  {db}: {type(e).__name__}: {e}")
        return []
    hits = []
    for r in rows:
        hay = (str(r.get("NAME_OF_TIME_SERIES") or "") + " " +
               str(r.get("CATEGORY") or "")).lower()
        if all(w in hay for w in wanted):
            hits.append(r)
    print(f"\n  db={db} {list(terms)}: {len(hits)} of {len(rows)} rows match")
    for r in hits[:limit]:
        print(f"    {r.get('SERIES_CODE') or '(heading)':<24}"
              f"{str(r.get('FREQUENCY'))[:9]:<10}"
              f"{str(r.get('NAME_OF_TIME_SERIES'))[:88]:<90}"
              f"{str(r.get('UNIT'))[:12]}")
    if len(hits) > limit:
        print(f"    ... {len(hits) - limit} more")
    return hits


# Series still to pin, as (database, AND-matched terms).
# Already confirmed and wired in sources.BOJ_API_SERIES:
#   IR04 DLLR2CIDBNL1          lending_rate
#   CO   TK99F0000612GCQ01000  tankan_lend_large
#   CO   TK99F0000612GCQ03000  tankan_lend_small
FINDS = [
    ("CO", ["Financial Position", "All industries", "Actual result", "D.I."]),
    ("CO", ["Outlook for General Prices", "All industries", "1 year ahead", "Average of Enterprises"]),
    ("CO", ["Outlook for General Prices", "All industries", "5 years ahead", "Average of Enterprises"]),
    ("IR04", ["Short-term", "Domestically Licensed Banks", "New Loans"]),
]

# getMetadata needs a db; try to learn the valid list from the error it returns.
DB_LIST_PROBE = [("getMetadata", {"lang": "EN"}), ("getMetadata", {"db": "*", "lang": "EN"})]


def run_targets():
    """One pass over every search still outstanding."""
    for db, terms in FINDS:
        try:
            find(db, *terms)
        except Exception as e:  # noqa: BLE001
            print(f"  {db} {terms}: {type(e).__name__}: {e}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--probe", action="store_true", help="report what responds and how")
    ap.add_argument("--discover", nargs=2, metavar=("DB", "KEYWORD"),
                    help="list series codes in DB whose name contains KEYWORD")
    ap.add_argument("--series", nargs=2, metavar=("DB", "CODE"),
                    help="fetch one series and print the last rows")
    ap.add_argument("--dump", nargs=2, metavar=("DB", "CODE"),
                    help="print a raw getDataCode response")
    ap.add_argument("--targets", action="store_true",
                    help="search every database we need codes from")
    ap.add_argument("--find", nargs="+", metavar="DB TERM",
                    help="list codes in DB whose name contains every TERM")
    args = ap.parse_args()
    if args.probe:
        probe()
    if args.discover:
        discover(*args.discover)
    if args.series:
        rows = fetch_series(*args.series)
        print(f"{len(rows)} rows; last 8: {rows[-8:]}")
    if args.dump:
        dump_series(*args.dump)
    if args.targets:
        run_targets()
    if args.find:
        find(args.find[0], *args.find[1:])
    if not (args.probe or args.discover or args.series or args.dump or args.targets or args.find):
        ap.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
