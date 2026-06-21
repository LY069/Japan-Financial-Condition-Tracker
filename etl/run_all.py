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


def has_observations():
    sys.path.insert(0, HERE)
    from db import connect, init_db
    conn = connect(); init_db(conn)
    n = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    return n > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", action="store_true", help="force reseed before building")
    ap.add_argument("--no-fetch", action="store_true", help="skip the live fetch step")
    args = ap.parse_args()

    if args.seed or not has_observations():
        run("seed_data.py")
    if not args.no_fetch:
        run("fetch.py")
    run("dedupe_monthly.py")   # one row per series-month (month-end); guards chart alignment
    run("build_indicators.py")
    run("export_web.py")
    run("export_excel.py")
    print("\nPipeline complete: data/jfct.db, web/data.json, Japan_FCI_Tracker.xlsx are up to date.")


if __name__ == "__main__":
    main()
