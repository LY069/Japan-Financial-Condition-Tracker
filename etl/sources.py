"""Live data connectors for official / authoritative sources.

Priority order follows the user's mandate: Bank of Japan and other Japanese
government bodies first, with FRED (which *mirrors* many BoJ/MoF/MIC series) as
a reliable automated fallback.

Providers
---------
MOF   : Ministry of Finance JGB reference yields (daily CSV, fully open).      [authoritative, no key]
ESTAT : e-Stat REST API (MIC CPI, etc.). Requires ESTAT_APP_ID.               [authoritative, free key]
FRED  : St. Louis Fed API; mirrors JGB/CPI/FX/policy-rate series. FRED_API_KEY. [fallback, free key]
BOJ   : BoJ Time-Series Data Search has no open REST API; series such as the
        Tankan DIs and the composite inflation-expectations index are ingested
        from CSVs exported from https://www.stat-search.boj.or.jp/ (see
        load_boj_csv). FRED covers the rest automatically.

Every connector returns a list of (iso_date, float_value) tuples, or raises.
Network failures are caught by the orchestrator (fetch.py), which then leaves
the existing (seed or prior) values in place.
"""
from __future__ import annotations

import csv
import io
import json
import os
import urllib.request
from datetime import date

UA = "Mozilla/5.0 (compatible; JapanFCITracker/1.0; research)"
TIMEOUT = 60


def _get(url: str, timeout: int = TIMEOUT) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _month_end(y: int, m: int) -> str:
    nd = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
    return date.fromordinal(nd.toordinal() - 1).isoformat()


def monthly_avg(daily_rows):
    """Collapse (iso_date, value) daily rows to month-end averages."""
    buckets = {}
    for d, v in daily_rows:
        if v is None:
            continue
        buckets.setdefault(d[:7], []).append(v)
    out = []
    for ym, vals in sorted(buckets.items()):
        y, m = int(ym[:4]), int(ym[5:7])
        out.append((_month_end(y, m), sum(vals) / len(vals)))
    return out


def to_yoy(monthly_levels):
    """Convert month-end levels to year-on-year % change."""
    by = {d: v for d, v in monthly_levels}
    out = []
    for d, v in monthly_levels:
        y, m = int(d[:4]), int(d[5:7])
        prev = _month_end(y - 1, m)
        if prev in by and by[prev]:
            out.append((d, (v / by[prev] - 1.0) * 100.0))
    return out


# ---------------------------------------------------------------- FRED -----
FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

# catalog series_id -> (FRED series, transform)  transform in {level, monthly_avg, yoy_from_level}
# Note: core_cpi_yoy here uses FRED's all-items CPI index as a reliable *fallback*
# (headline proxy). When the e-Stat fetch succeeds it overwrites this with the
# proper MIC "ex-fresh-food" core measure (fetch order: FRED then ESTAT).
FRED_MAP = {
    "policy_rate": ("IRSTCB01JPM156N", "level"),     # central bank rate, Japan, monthly
    "jgb_10y":     ("IRLTLT01JPM156N", "level"),     # 10y govt bond yield, monthly
    "core_cpi_yoy": ("JPNCPIALLMINMEI", "yoy_from_level"),  # CPI all items index -> y/y (fallback)
    "usdjpy":      ("EXJPUS", "level"),              # monthly avg JPY per USD
    "nikkei225":   ("NIKKEI225", "monthly_avg"),     # daily index -> month avg
}


def fetch_fred(fred_id: str, api_key: str):
    url = (f"{FRED_BASE}?series_id={fred_id}&api_key={api_key}&file_type=json"
           f"&observation_start=2004-01-01")
    data = json.loads(_get(url))
    out = []
    for o in data.get("observations", []):
        if o["value"] in (".", "", None):
            continue
        out.append((o["date"], float(o["value"])))
    return out


# ----------------------------------------------------------------- MoF -----
# MoF reorganises these paths periodically, so try several known layouts and use
# whatever responds. The historical file (1974~) is preferred for full coverage;
# the current-year file is merged in for the latest fixings.
MOF_BASES = [
    "https://www.mof.go.jp/jgbs/reference/interest_rate/",                  # JP site
    "https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/",   # EN site
]
MOF_FILES = [
    "data/jgbcm_all.csv",          # all years, JP (bare-number headers, parser-friendly)
    "historical/jgbcme_all.csv",   # all years, EN (note trailing 'e')
    "historical/jgbcm_all.csv",    # all years (alt)
    "jgbcm_all.csv",               # all years (alt)
    "jgbcme.csv",                  # current year, EN
    "jgbcm.csv",                   # current year, JP
]
# column header (years) -> catalog series_id
MOF_COL = {"1": "jgb_1y", "2": "jgb_2y", "5": "jgb_5y", "10": "jgb_10y", "30": "jgb_30y"}


def _norm_mat(cell: str) -> str:
    """Normalize a header cell to a bare maturity number ('10Y'->'10', '1年'->'1')."""
    return cell.strip().upper().rstrip("Y").rstrip("年").strip()


def _parse_mof_csv(raw: bytes):
    text = raw.decode("shift_jis", errors="ignore")
    rows = [r for r in csv.reader(io.StringIO(text)) if r]
    # header row contains maturity labels like '1','2','10' or '1Y','10Y'
    hdr_i = next((i for i, r in enumerate(rows)
                  if sum(1 for c in r if _norm_mat(c) in MOF_COL) >= 3), None)
    if hdr_i is None:
        return {}
    hdr = [_norm_mat(c) for c in rows[hdr_i]]
    col_idx = {hdr[j]: j for j in range(len(hdr))}
    daily = {sid: [] for sid in MOF_COL.values()}
    for r in rows[hdr_i + 1:]:
        parts = r[0].strip().replace("/", "-").split("-")
        if len(parts) != 3 or not parts[0].isdigit():
            continue
        try:
            d = date(int(parts[0]), int(parts[1]), int(parts[2])).isoformat()
        except ValueError:
            continue
        for mat, sid in MOF_COL.items():
            j = col_idx.get(mat)
            if j is None or j >= len(r):
                continue
            val = r[j].strip()
            if val in ("", "-", "*****"):
                continue
            try:
                daily[sid].append((d, float(val)))
            except ValueError:
                pass
    return daily


def fetch_mof_jgb():
    """Return {catalog_series_id: [(month_end, yield)]} from MoF reference rates.

    Tries multiple candidate URLs (historical + current, JP + EN) and merges all
    successful pulls, so it survives MoF path changes and always gets latest data.
    """
    merged = {sid: {} for sid in MOF_COL.values()}      # sid -> {iso_date: value}
    got, diag = [], []
    for base in MOF_BASES:
        for fn in MOF_FILES:
            url = base + fn
            try:
                daily = _parse_mof_csv(_get(url))
            except Exception as e:
                diag.append(f"{fn}@{base.split('//')[1].split('/')[0]}: {type(e).__name__} {e}")
                continue
            if any(daily.values()):
                got.append(url)
                for sid, rows_ in daily.items():
                    for d, v in rows_:
                        merged[sid][d] = v
            else:
                diag.append(f"{url}: fetched but no maturity columns parsed")
    if not got:
        raise RuntimeError("all MoF candidate URLs failed -> " + " | ".join(diag))
    return {sid: monthly_avg(sorted(dv.items())) for sid, dv in merged.items()}


# --------------------------------------------------------------- e-Stat ----
ESTAT_BASE = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
ESTAT_LIST = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"
ESTAT_META = "https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo"
ESTAT_CPI_STATSCODE = "00200573"   # MIC "Consumer Price Index" stats provider code


def estat_meta_find(stats_data_id: str, app_id: str, want, timeout: int = TIMEOUT):
    """Return {class_id: code} for the class entries whose name matches all of `want`.

    Used to pin the 'ex-fresh-food total' item code and the national area code so
    the big CPI table can be narrowed to a single clean monthly series.
    """
    url = f"{ESTAT_META}?appId={app_id}&statsDataId={stats_data_id}"
    data = json.loads(_get(url, timeout=timeout))
    objs = (data.get("GET_META_INFO", {}).get("METADATA_INF", {})
            .get("CLASS_INF", {}).get("CLASS_OBJ", []))
    if isinstance(objs, dict):
        objs = [objs]
    found = {}
    for obj in objs:
        cid = obj.get("@id", "")
        classes = obj.get("CLASS", [])
        if isinstance(classes, dict):
            classes = [classes]
        for c in classes:
            name = c.get("@name", "")
            if all(w in name for w in want):
                found[cid] = c.get("@code", "")
                break
    return found


def estat_find_cpi_table(app_id: str, timeout: int = TIMEOUT):
    """Discover a monthly CPI statsDataId via getStatsList (so the ID self-heals).

    Returns a list of (statsDataId, title) candidates, monthly tables first.
    """
    url = (f"{ESTAT_LIST}?appId={app_id}&statsCode={ESTAT_CPI_STATSCODE}"
           f"&searchWord=%E5%93%81%E7%9B%AE%E5%88%A5&limit=100")  # 品目別 (by item)
    data = json.loads(_get(url, timeout=timeout))
    tables = data.get("GET_STATS_LIST", {}).get("DATALIST_INF", {}).get("TABLE_INF", [])
    if isinstance(tables, dict):
        tables = [tables]
    out = []
    for t in tables:
        sid = str(t.get("@id", ""))
        title = (t.get("TITLE", {}) or {})
        title = title.get("$", title) if isinstance(title, dict) else title
        cycle = t.get("SURVEY_DATE", "")
        out.append((sid, str(title), str(cycle)))
    # prefer monthly ("月次"/length-6 survey dates) tables
    out.sort(key=lambda x: (0 if "月" in x[1] or len(x[2]) == 6 else 1))
    return [(s, t) for s, t, _ in out]


def fetch_estat(stats_data_id: str, app_id: str, cd_cat=None, cd_area=None,
                limit=None, timeout: int = TIMEOUT):
    """Generic e-Stat getStatsData fetch -> [(iso_date, value)] for a CPI-style table.

    Narrowing params keep the payload small enough to avoid timeouts:
      cd_cat  : category code (e.g. the 'all items, less fresh food' item code)
      cd_area : area code (national = '00000')
      limit   : max rows to return
    """
    url = f"{ESTAT_BASE}?appId={app_id}&statsDataId={stats_data_id}&metaGetFlg=N&cntGetFlg=N"
    if cd_cat:
        url += f"&cdCat01={cd_cat}"
    if cd_area:
        url += f"&cdArea={cd_area}"
    if limit:
        url += f"&limit={int(limit)}"
    data = json.loads(_get(url, timeout=timeout))
    values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    if isinstance(values, dict):
        values = [values]
    out = []
    for v in values:
        t = v.get("@time", "")        # e.g. 2026000505 (yyyy00mm) for monthly
        if len(t) >= 8:
            y, m = int(t[:4]), int(t[6:8])
            try:
                out.append((_month_end(y, m), float(v["$"])))
            except (ValueError, KeyError, TypeError):
                pass
    out.sort()
    return out


# ----------------------------------------------------------------- BoJ -----
def load_boj_csv(path: str, series_id: str, date_col=0, val_col=1, skip=1):
    """Ingest a CSV exported from BoJ Time-Series Data Search for one series."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    out = []
    for r in rows[skip:]:
        if len(r) <= max(date_col, val_col):
            continue
        d = r[date_col].strip()
        try:
            out.append((_normalize_date(d), float(r[val_col])))
        except ValueError:
            pass
    return out


def _normalize_date(d: str) -> str:
    d = d.strip().replace("/", "-")
    parts = d.split("-")
    if len(parts) == 2:          # yyyy-mm -> month end
        return _month_end(int(parts[0]), int(parts[1]))
    return d
