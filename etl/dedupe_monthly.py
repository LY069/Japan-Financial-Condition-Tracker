"""Collapse observations to one row per (series, month), snapping every date to
month-end. Fixes mixed date conventions (FRED returns month-start, other sources
month-end) that created duplicate monthly points and zig-zag chart lines.

On collision, keep the most authoritative source (MoF/BoJ/e-Stat > FRED >
COMPUTED > SEED), breaking ties by latest vintage. Idempotent; safe to re-run.
"""
from __future__ import annotations

from datetime import date
from db import connect

PRIO = {"MOF": 5, "BOJ": 5, "ESTAT": 5, "FRED": 3, "COMPUTED": 2, "SEED": 1}


def month_end(d: str) -> str:
    y, m = int(d[:4]), int(d[5:7])
    nd = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
    return date.fromordinal(nd.toordinal() - 1).isoformat()


def main():
    conn = connect()
    rows = conn.execute(
        "SELECT series_id, date, value, source, vintage FROM observations").fetchall()
    best = {}
    for r in rows:
        key = (r["series_id"], month_end(r["date"]))
        rank = (PRIO.get(r["source"], 0), r["vintage"] or "")
        cur = best.get(key)
        if cur is None or rank > cur[0]:
            best[key] = (rank, r["value"], r["source"], r["vintage"])
    conn.execute("DELETE FROM observations")
    conn.executemany(
        "INSERT INTO observations(series_id, date, value, source, vintage) VALUES(?,?,?,?,?)",
        [(sid, d, v[1], v[2], v[3]) for (sid, d), v in best.items()])
    conn.commit()
    print(f"Deduped {len(rows)} -> {len(best)} observations (one per series-month, month-end).")


if __name__ == "__main__":
    main()
