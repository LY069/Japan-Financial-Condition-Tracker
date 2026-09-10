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


def _points(node, out):
    """Collect (date, value) pairs from an arbitrarily shaped JSON response."""
    if isinstance(node, dict):
        d = node.get("time") or node.get("date") or node.get("period")
        v = node.get("value") if "value" in node else node.get("val")
        if d is not None and v not in (None, "", "NA", "ND"):
            try:
                out.append((str(d), float(str(v).replace(",", ""))))
            except ValueError:
                pass
        for x in node.values():
            _points(x, out)
    elif isinstance(node, list):
        for x in node:
            _points(x, out)
    return out


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
    """Fetch one series as [(iso_date, value)], month-end dated."""
    doc = api("getDataCode", db=db, code=code, lang=lang)
    rows = []
    for period, value in _points(doc, []):
        iso = normalize_period(period)
        if iso:
            rows.append((iso, value))
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
    """Print a getDataCode response verbatim, to learn the data-point schema."""
    doc = api("getDataCode", db=db, code=code, lang=lang)
    text = json.dumps(doc, ensure_ascii=False, indent=1)
    print(f"\n  getDataCode db={db} code={code}: {len(text)} chars")
    print("\n".join("    " + ln for ln in text.splitlines()[:60]))


# Databases to look through, with the names we need out of each.
TARGETS = [
    ("CO", ["lending attitude", "financial position", "general prices"]),
    ("IR04", ["new loans", "average contract", "short-term"]),
    ("FM01", ["commercial paper", "cp "]),
    ("FM02", ["commercial paper"]),
    ("FM08", ["commercial paper"]),
    ("MD01", ["commercial paper"]),
    ("MD10", ["commercial paper", "corporate bond"]),
]


def run_targets():
    """One pass over every database/keyword pair we need codes for."""
    for db, keywords in TARGETS:
        print(f"\n=== {db} ===")
        try:
            rows = metadata_rows(db)
        except Exception as e:  # noqa: BLE001
            print(f"  unavailable: {type(e).__name__}: {e}")
            continue
        print(f"  {len(rows)} catalogue rows")
        for kw in keywords:
            discover(db, kw)


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
    if not (args.probe or args.discover or args.series or args.dump or args.targets):
        ap.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
