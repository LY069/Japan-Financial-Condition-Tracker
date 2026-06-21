"""Orchestrate live data refresh from official sources into the DB.

Usage
-----
    export FRED_API_KEY=xxxx        # https://fred.stlouisfed.org/docs/api/api_key.html
    export ESTAT_APP_ID=yyyy        # https://www.e-stat.go.jp/api/ (free)
    # Optional e-Stat CPI overrides (auto-resolved from getMetaInfo otherwise):
    #   ESTAT_CPI_CORE_ID  CPI table id (default 0003427113)
    #   ESTAT_CPI_CAT      ex-fresh-food item code (e.g. 9205)
    #   ESTAT_CPI_TAB      presentation-tab code for the index (e.g. 01)
    #   ESTAT_CPI_AREA     area code (default 00000 = national)
    python etl/fetch.py             # refresh everything available
    python etl/fetch.py --only mof  # just MoF JGB curve
    python etl/fetch.py --boj-dir ./boj_exports   # ingest BoJ CSV exports

Design: each source is attempted independently. If a source has no key or the
network is unavailable, that source is skipped with a warning and existing
(seed or previously-fetched) values are preserved. Series that have no open
API (Tankan DIs, the composite inflation-expectations index, BoJ natural-rate
estimates) are documented as BoJ-CSV / manual and left untouched unless a
matching CSV is supplied via --boj-dir.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

from db import connect, init_db, load_catalog, upsert_observations, set_meta
import sources as S

# series that come from a BoJ stat-search CSV export, filename stem -> series_id
BOJ_CSV_SERIES = {
    "tankan_lend_large", "tankan_lend_small", "tankan_finpos_large", "tankan_finpos_small",
    "infexp_1y", "infexp_3y", "infexp_10y", "lending_rate", "cp_rate", "corp_bond_spread",
    "topix", "bank_lending_yoy", "cp_corpbond_yoy", "potential_growth",
    "natural_rate_low", "natural_rate_mid", "natural_rate_high",
}


def run_mof(conn):
    n = 0
    try:
        data = S.fetch_mof_jgb()
    except Exception as e:
        print(f"  [MOF] skipped: {e}")
        return 0
    for sid, rows in data.items():
        if rows:
            n += upsert_observations(conn, sid, rows, "MOF")
            print(f"  [MOF] {sid}: {len(rows)} obs")
    return n


def run_fred(conn):
    key = os.environ.get("FRED_API_KEY")
    if not key:
        print("  [FRED] skipped: FRED_API_KEY not set")
        return 0
    n = 0
    for sid, (fid, transform) in S.FRED_MAP.items():
        try:
            rows = S.fetch_fred(fid, key)
            if transform == "monthly_avg":
                rows = S.monthly_avg(rows)
            elif transform == "yoy_from_level":
                rows = S.to_yoy(rows)
            if rows:
                n += upsert_observations(conn, sid, rows, "FRED")
                print(f"  [FRED] {sid} <- {fid}: {len(rows)} obs")
        except Exception as e:
            print(f"  [FRED] {sid} <- {fid} failed: {e}")
    return n


def run_estat(conn):
    app = os.environ.get("ESTAT_APP_ID")
    if not app:
        print("  [ESTAT] skipped: ESTAT_APP_ID not set")
        return 0
    n = 0
    # MIC CPI: core (ex-fresh food), national, monthly. statsDataId is configurable.
    sid = "core_cpi_yoy"
    stats_id = os.environ.get("ESTAT_CPI_CORE_ID", "0003427113")
    # A single national monthly series spans only a few hundred months; if a query
    # returns more, the narrowing didn't bite and the series is contaminated, so we
    # discard it and keep the clean FRED CPI fallback already in the DB.
    MAX_MONTHS = 900

    # Build narrowing filters mapped to the table's ACTUAL class dimensions.
    # The CPI table is split by item (cat01), presentation tab (index vs y/y vs
    # contribution) and area, so pinning all three collapses it to one monthly
    # series. We read the metadata once and resolve each code by name.
    filters = {}
    try:
        meta = S.estat_meta(stats_id, app)
        # Identify dimension ids by their item contents (robust to id naming).
        item_dim = next((cid for cid in meta
                         if S.meta_pick(meta, cid, ["生鮮食品を除く総合"])), None)
        tab_dim = next((cid for cid in meta if S.meta_pick(meta, cid, ["指数"])), None)
        area_dim = next((cid for cid in meta if S.meta_pick(meta, cid, ["全国"])), None)
        if item_dim:
            filters[item_dim] = S.meta_pick(meta, item_dim, ["生鮮食品を除く総合"])
        if tab_dim:
            # index only, excluding y/y change and contribution presentations
            filters[tab_dim] = S.meta_pick(meta, tab_dim, ["指数"],
                                           avoid=["前年", "前月", "寄与"])
        if area_dim:
            filters[area_dim] = S.meta_pick(meta, area_dim, ["全国"])
        # Self-reveal: log the candidate ex-fresh-food item codes for pinning.
        if item_dim:
            cands = [f"{c}={nm}" for c, nm in meta[item_dim]["items"]
                     if ("除く" in nm and "総合" in nm)][:6]
            print(f"  [ESTAT] item dim '{item_dim}' ex-food candidates: {cands}")
            print(f"  [ESTAT] to pin, set ESTAT_CPI_CAT (item) / ESTAT_CPI_TAB / ESTAT_CPI_AREA")
    except Exception as e:
        print(f"  [ESTAT] metadata lookup failed ({e}); will guard on row count")

    # Explicit env overrides win over auto-resolution.
    if os.environ.get("ESTAT_CPI_CAT"):
        filters["cat01"] = os.environ["ESTAT_CPI_CAT"]
    if os.environ.get("ESTAT_CPI_TAB"):
        filters["tab"] = os.environ["ESTAT_CPI_TAB"]
    filters.setdefault("area", os.environ.get("ESTAT_CPI_AREA", "00000"))
    print(f"  [ESTAT] narrowing filters: {filters}")

    try:
        levels = S.fetch_estat(stats_id, app, filters=filters, limit=2000)
        rows = S.to_yoy(levels)
        if rows and len(rows) <= MAX_MONTHS:
            n += upsert_observations(conn, sid, rows, "ESTAT")
            print(f"  [ESTAT] {sid}: {len(rows)} obs (id={stats_id}, filters={filters})")
            return n
        if rows:
            print(f"  [ESTAT] {sid}: {len(rows)} rows > {MAX_MONTHS} -> not narrowed; "
                  f"keeping FRED CPI fallback. Inspect getMetaInfo for {stats_id} and set "
                  f"ESTAT_CPI_CAT to the ex-fresh-food item code.")
            return n
        print(f"  [ESTAT] {sid}: id={stats_id} returned no usable rows; trying discovery")
    except Exception as e:
        print(f"  [ESTAT] {sid} id={stats_id} failed ({e}); trying discovery")

    # Self-heal: discover a monthly CPI table id via getStatsList.
    try:
        candidates = S.estat_find_cpi_table(app)
        print(f"  [ESTAT] discovery found {len(candidates)} CPI tables; trying top 3")
        for cid, title in candidates[:3]:
            try:
                levels = S.fetch_estat(cid, app, filters=filters, limit=2000)
                rows = S.to_yoy(levels)
                if rows and len(rows) <= MAX_MONTHS:
                    n += upsert_observations(conn, sid, rows, "ESTAT")
                    print(f"  [ESTAT] {sid}: {len(rows)} obs via discovered id={cid} ({title[:40]})")
                    print(f"          set ESTAT_CPI_CORE_ID={cid} to lock this in.")
                    break
            except Exception:
                continue
        else:
            print("  [ESTAT] discovery exhausted; FRED CPI fallback retained.")
    except Exception as e:
        print(f"  [ESTAT] discovery failed: {e}; FRED CPI fallback retained.")
    return n


def run_boj_dir(conn, boj_dir):
    n = 0
    for path in glob.glob(os.path.join(boj_dir, "*.csv")):
        stem = os.path.splitext(os.path.basename(path))[0]
        if stem in BOJ_CSV_SERIES:
            try:
                rows = S.load_boj_csv(path, stem)
                if rows:
                    n += upsert_observations(conn, stem, rows, "BOJ")
                    print(f"  [BOJ] {stem}: {len(rows)} obs from {os.path.basename(path)}")
            except Exception as e:
                print(f"  [BOJ] {stem} failed: {e}")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["mof", "fred", "estat", "boj"], default=None)
    ap.add_argument("--boj-dir", default=None)
    args = ap.parse_args()

    conn = connect()
    init_db(conn)
    load_catalog(conn)

    total = 0
    print("Refreshing from official sources...")
    if args.only in (None, "mof"):
        total += run_mof(conn)
    if args.only in (None, "fred"):
        total += run_fred(conn)
    if args.only in (None, "estat"):
        total += run_estat(conn)
    if (args.only in (None, "boj")) and args.boj_dir:
        total += run_boj_dir(conn, args.boj_dir)

    if total == 0:
        print("No live observations fetched (no keys / offline). Seed data preserved.")
        set_meta(conn, "data_mode", "SEED (no live fetch succeeded; run with API keys)")
    else:
        set_meta(conn, "data_mode", "LIVE (official sources) + SEED fallback for un-fetched series")
    print(f"Done. {total} observations upserted.")


if __name__ == "__main__":
    main()
