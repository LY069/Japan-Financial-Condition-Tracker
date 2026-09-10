"""Indicator engine for the Monetary & Liquidity Conditions tracker.

Writes to the shared `indicators` table with 'ml::'-prefixed keys so it never
collides with the FCI tracker:
  scope='series'    key='ml::<sid>'       per-series accommodation score (+ = easier)
  scope='axis'      key='ml::<axis>'      weighted mean of members
  scope='stage'     key='ml_monetary' / 'ml_liquidity'
  scope='composite' key='mci' / 'lci' / 'mlci'  (monetary / liquidity / overall)

Every ML series is z-scored over its LONGEST available history (not 2005+),
signed by catalog polarity. Also derives real_policy_rate_xp.
"""
from __future__ import annotations

import statistics
from datetime import date

from db import connect, init_db, load_catalog, get_series, upsert_observations, catalog_rows, set_meta
from build_indicators import month_grid, to_monthly
from ml_framework import ML_AXES, ML_AXIS_ORDER, ML_STAGES, COMPOSITES


def month_end_of(ym):
    y, m = int(ym[:4]), int(ym[5:7])
    nd = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
    return date.fromordinal(nd.toordinal() - 1).isoformat()


def main():
    conn = connect()
    init_db(conn)
    load_catalog(conn)
    cat = {r["series_id"]: r for r in catalog_rows(conn)}

    # ---- derived: ex-post real policy rate (policy - realized core CPI) ----
    pol = {d[:7]: v for d, v in get_series(conn, "policy_rate")}
    cpi = {d[:7]: v for d, v in get_series(conn, "core_cpi_yoy")}
    rp_xp = [(month_end_of(m), pol[m] - cpi[m]) for m in sorted(pol) if m in cpi]
    upsert_observations(conn, "real_policy_rate_xp", rp_xp, "COMPUTED")

    # ---- derived market-liquidity gauges from the MoF curve (real, automatable) ----
    j10 = {d[:7]: v for d, v in get_series(conn, "jgb_10y")}
    j30 = {d[:7]: v for d, v in get_series(conn, "jgb_30y")}
    ms = sorted(j10)
    vol = []
    for i in range(12, len(ms)):
        window = [(j10[ms[k]] - j10[ms[k - 1]]) * 100.0 for k in range(i - 11, i + 1)]  # bp changes
        vol.append((month_end_of(ms[i]), statistics.pstdev(window)))
    upsert_observations(conn, "jgb_10y_vol", vol, "COMPUTED")
    upsert_observations(conn, "jgb_10s30s",
                        [(month_end_of(m), j30[m] - j10[m]) for m in ms if m in j30], "COMPUTED")

    # ---- per-series scores over full history ----
    members = sorted({sid for a in ML_AXES.values() for sid in a["members"]})
    conn.execute("DELETE FROM indicators WHERE key LIKE 'ml::%' OR key IN ('ml_monetary','ml_liquidity','mci','lci','mlci')")
    earliest = None
    raw, scores = {}, {}
    for sid in members:
        obs = get_series(conn, sid)
        if not obs:
            print(f"  (no data for {sid})")
            continue
        earliest = min(earliest, obs[0][0]) if earliest else obs[0][0]
        raw[sid] = obs
    grid = month_grid(start=(earliest or "2005-01")[:7], end=None)
    for sid, obs in raw.items():
        mo = to_monthly(obs, grid)
        vals = [v for v in mo.values() if v is not None]
        if len(vals) < 8:
            continue
        mu, sd = statistics.fmean(vals), (statistics.pstdev(vals) or 1.0)
        pol_sign = cat[sid]["polarity"] or 1
        scores[sid] = {d: (None if v is None else pol_sign * (v - mu) / sd) for d, v in mo.items()}
        conn.executemany(
            "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES('series',?,?,?,?)",
            [(f"ml::{sid}", d, s, mo[d]) for d, s in scores[sid].items() if s is not None])

    # ---- axes ----
    axis_scores = {}
    for a in ML_AXIS_ORDER:
        mem = ML_AXES[a]["members"]
        axis_scores[a] = {}
        for d in grid:
            num = den = 0.0
            for sid, w in mem.items():
                s = scores.get(sid, {}).get(d)
                if s is not None:
                    num += w * s
                    den += w
            if den > 0:
                axis_scores[a][d] = num / den
        conn.executemany(
            "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES('axis',?,?,?,NULL)",
            [(f"ml::{a}", d, s) for d, s in axis_scores[a].items()])

    # ---- stages & composites ----
    stage_vals = {}
    for st in ML_STAGES:
        axes = [a for a in ML_AXIS_ORDER if ML_AXES[a]["stage"] == st]
        stage_vals[st] = {}
        for d in grid:
            vals = [axis_scores[a][d] for a in axes if d in axis_scores[a]]
            if vals:
                stage_vals[st][d] = statistics.fmean(vals)
        conn.executemany(
            "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES('stage',?,?,?,NULL)",
            [(st, d, s) for d, s in stage_vals[st].items()])
    for ck, st in COMPOSITES.items():
        conn.executemany(
            "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES('composite',?,?,?,NULL)",
            [(ck, d, s) for d, s in stage_vals[st].items()])
    for d in grid:
        vals = [stage_vals[st][d] for st in ML_STAGES if d in stage_vals[st]]
        if len(vals) == 2:
            conn.execute("INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES('composite','mlci',?,?,NULL)",
                         (d, statistics.fmean(vals)))
    conn.commit()
    set_meta(conn, "ml_last_built", date.today().isoformat())
    latest = grid[-1]
    for ck in ("mci", "lci", "mlci"):
        r = conn.execute("SELECT score FROM indicators WHERE scope='composite' AND key=? ORDER BY date DESC LIMIT 1", (ck,)).fetchone()
        print(f"  {ck}: {r['score']:+.2f}" if r else f"  {ck}: n/a")
    print(f"M&L indicators built through {latest} (baseline from {grid[0][:7]}).")


if __name__ == "__main__":
    main()
