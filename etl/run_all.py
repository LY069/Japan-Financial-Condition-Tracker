"""One-command pipeline: (seed if empty) -> fetch -> indicators -> exports.

    python etl/run_all.py            # full refresh (live fetch if keys present)
    python etl/run_all.py --seed     # force reseed before building (offline demo)
    python etl/run_all.py --no-fetch # skip the live fetch step

This is the single entry point used locally and by the GitHub Action.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def run(mod, *a):
    print(f"\n=== {mod} {' '.join(a)} ===")
    r = subprocess.run([sys.executable, os.path.join(HERE, mod), *a])
    if r.returncode != 0:
        sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", action="store_true", help="(kept for compatibility; seeding is now always attempted and is guarded)")
    ap.add_argument("--no-fetch", action="store_true", help="skip the live fetch step")
    args = ap.parse_args()

    # seed_data is per-series guarded (a series with live observations is never
    # reseeded), so it runs every time: that lets corrected/extended seed anchors
    # reach series that still have no live connector, instead of only at first build.
    run("seed_data.py")
    if not args.no_fetch:
        run("fetch.py")
    run("seed_data_ml.py")     # Monetary & Liquidity series (guarded: never overwrites live data)
    run("dedupe_monthly.py")   # one row per series-month (month-end); guards chart alignment
    run("build_indicators.py")
    run("build_indicators_ml.py")
    run("export_web.py")
    run("export_web_ml.py")
    run("export_excel.py")
    run("export_excel_ml.py")
    print("\nPipeline complete: data/jfct.db, web/data*.json, Japan_FCI_Tracker.xlsx, Japan_ML_Tracker.xlsx are up to date.")


if __name__ == "__main__":
    main()
