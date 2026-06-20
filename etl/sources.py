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

UA = "JapanFCITracker/1.0 (research; contact via repo)"
TIMEOUT = 30


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
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
FRED_MAP = {
    "policy_rate": ("IRSTCB01JPM156N", "level"),     # central bank rate, Japan, monthly
    "jgb_10y":     ("IRLTLT01JPM156N", "level"),     # 10y govt bond yield, monthly
    "core_cpi_yoy": ("JPNCPICORMINMEI", "yoy_from_level"),
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
MOF_HIST = "https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/jgbcm_all.csv"
MOF_CUR = "https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/jgbcm.csv"
# column header (years) -> catalog series_id
MOF_COL = {"1": "jgb_1y", "2": "jgb_2y", "5": "jgb_5y", "10": "jgb_10y", "30": "jgb_30y"}


def fetch_mof_jgb():
    """Return {catalog_series_id: [(month_end, yield)]} from MoF reference rates."""
    try:
        raw = _get(MOF_HIST)
    except Exception:
        raw = _get(MOF_CUR)
    text = raw.decode("shift_jis", errors="ignore")
    reader = csv.reader(io.StringIO(text))
    rows = [r for r in reader if r]
    # find header row containing maturity labels like '1','2',... '10'
    hdr_i = next(i for i, r in enumerate(rows) if any(c.strip() in MOF_COL for c in r))
    hdr = [c.strip() for c in rows[hdr_i]]
    col_idx = {hdr[j]: j for j in range(len(hdr))}
    daily = {sid: [] for sid in MOF_COL.values()}
    for r in rows[hdr_i + 1:]:
        d = r[0].strip().replace("/", "-")
        if len(d) < 8:
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
    return {sid: monthly_avg(rows_) for sid, rows_ in daily.items()}


# --------------------------------------------------------------- e-Stat ----
ESTAT_BASE = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"


def fetch_estat(stats_data_id: str, app_id: str, cd_cat=None):
    """Generic e-Stat getStatsData fetch -> [(iso_date, value)] for a CPI-style table."""
    url = f"{ESTAT_BASE}?appId={app_id}&statsDataId={stats_data_id}&metaGetFlg=N&cntGetFlg=N"
    if cd_cat:
        url += f"&cdCat01={cd_cat}"
    data = json.loads(_get(url))
    values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    out = []
    for v in values:
        t = v.get("@time", "")        # e.g. 2026000505 (yyyy00mm) for monthly
        if len(t) >= 8:
            y, m = int(t[:4]), int(t[6:8])
            try:
                out.append((_month_end(y, m), float(v["$"])))
            except (ValueError, KeyError):
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
