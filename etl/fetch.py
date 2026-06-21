"""Orchestrate live data refresh from official sources into the DB.

Usage
-----
    export FRED_API_KEY=xxxx        # https://fred.stlouisfed.org/docs/api/api_key.html
    export ESTAT_APP_ID=yyyy        # https://www.e-stat.go.jp/api/ (free)
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
    cd_cat = os.environ.get("ESTAT_CPI_CAT")        # ex-fresh-food item code (table-specific)
    cd_area = os.environ.get("ESTAT_CPI_AREA", "00000")   # national

    # The default table is the full 2020-base CPI database (many items). Narrow it
    # to the genuine 'ex-fresh-food total', national series via metadata lookup.
    if not cd_cat:
        try:
            codes = S.estat_meta_find(stats_id, app, ["生鮮食品を除く総合"])
            cat_codes = {k: v for k, v in codes.items() if k.startswith("cat")}
            if cat_codes:
                cd_cat = next(iter(cat_codes.values()))
                area = S.estat_meta_find(stats_id, app, ["全国"])
                if any(k == "area" for k in area):
                    cd_area = area["area"]
                print(f"  [ESTAT] resolved ex-fresh-food code={cd_cat}, area={cd_area}")
        except Exception as e:
            print(f"  [ESTAT] metadata lookup failed ({e}); querying without item narrowing")
    try:
        levels = S.fetch_estat(stats_id, app, cd_cat=cd_cat, cd_area=cd_area, limit=2000)
        rows = S.to_yoy(levels)
        if rows:
            n += upsert_observations(conn, sid, rows, "ESTAT")
            print(f"  [ESTAT] {sid}: {len(rows)} obs (id={stats_id}, cat={cd_cat}, area={cd_area})")
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
                levels = S.fetch_estat(cid, app, cd_area=cd_area, limit=2000)
                rows = S.to_yoy(levels)
                if rows:
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
