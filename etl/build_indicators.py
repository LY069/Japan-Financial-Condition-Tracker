"""Compute derived indicators for the BoJ financial-conditions framework.

Outputs (all written to the `indicators` table):
  scope='series'    : per-series accommodation z-score (+ = accommodative vs own history)
  scope='axis'      : the framework axes
                      (real_rate, funding_costs, availability, asset_prices, funding_volumes)
  scope='stage'     : stage1 (interest rates) / stage2 (funding environment) composites
  scope='composite' : 'fci' overall index, and 'rate_gap' (real policy rate - natural rate)

Also derives the real interest rates (real_1y / real_3y / real_10y), the real
policy rate, and writes them back into `observations` (source COMPUTED).

Sign convention: a positive score means *more accommodative* than the series'
own 2005+ history. Polarity in the catalog flips cost/rate series so that, e.g.,
a lower real rate scores positive (accommodative).
"""
from __future__ import annotations

import statistics
from datetime import date

from db import connect, init_db, load_catalog, get_series, upsert_observations, catalog_rows, set_meta

AXES = ["real_rate", "funding_costs", "availability", "asset_prices", "funding_volumes"]
AXIS_LABEL = {
    "real_rate": "Real interest rates (Stage 1)",
    "funding_costs": "Funding costs",
    "availability": "Availability of funds",
    "asset_prices": "Asset prices",
    "funding_volumes": "Funding volumes",
}


def month_grid(start="2005-01", end=None):
    sy, sm = int(start[:4]), int(start[5:7])
    if end is None:
        t = date.today()
        ey, em = t.year, t.month
    else:
        ey, em = int(end[:4]), int(end[5:7])
    out = []
    y, m = sy, sm
    while (y, m) <= (ey, em):
        if m == 12:
            last = date(y, 12, 31)
        else:
            last = date.fromordinal(date(y, m + 1, 1).toordinal() - 1)
        out.append(last.isoformat())
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


def to_monthly(rows, grid):
    """Map (date,value) rows onto a monthly grid by month key, forward-filling."""
    by_month = {}
    for d, v in rows:
        by_month[d[:7]] = v
    out, last = {}, None
    for g in grid:
        k = g[:7]
        if k in by_month:
            last = by_month[k]
        out[g] = last
    return out


def zscores(monthly):
    vals = [v for v in monthly.values() if v is not None]
    if len(vals) < 8:
        return {d: None for d in monthly}
    mu = statistics.fmean(vals)
    sd = statistics.pstdev(vals) or 1.0
    return {d: (None if v is None else (v - mu) / sd) for d, v in monthly.items()}


def main():
    conn = connect()
    init_db(conn)
    load_catalog(conn)
    grid = month_grid(end=None)

    raw = {}
    for r in catalog_rows(conn):
        raw[r["series_id"]] = to_monthly(get_series(conn, r["series_id"]), grid)

    def g(sid, d):
        return raw.get(sid, {}).get(d)

    # ---- Derive real interest rates ----
    real_1y, real_3y, real_10y, real_pol = [], [], [], []
    for d in grid:
        j1, j2, j5, j10 = g("jgb_1y", d), g("jgb_2y", d), g("jgb_5y", d), g("jgb_10y", d)
        e1, e3, e10 = g("infexp_1y", d), g("infexp_3y", d), g("infexp_10y", d)
        pol = g("policy_rate", d)
        if j1 is not None and e1 is not None:
            real_1y.append((d, j1 - e1))
        if j2 is not None and j5 is not None and e3 is not None:
            jgb_3y = j2 + (j5 - j2) * (3 - 2) / (5 - 2)  # linear interp 2y->5y
            real_3y.append((d, jgb_3y - e3))
        if j10 is not None and e10 is not None:
            real_10y.append((d, j10 - e10))
        if pol is not None and e1 is not None:
            real_pol.append((d, pol - e1))

    upsert_observations(conn, "real_1y", real_1y, "COMPUTED")
    upsert_observations(conn, "real_3y", real_3y, "COMPUTED")
    upsert_observations(conn, "real_10y", real_10y, "COMPUTED")
    upsert_observations(conn, "real_policy_rate", real_pol, "COMPUTED")

    # Ex-post real rates over the FULL available history (nominal - realized core
    # CPI), used for long-horizon baseline analysis since expected-inflation data
    # only starts in 2005. Computed directly from observations (not the 2005 grid).
    def obs_map(sid):
        return {d[:7]: v for d, v in get_series(conn, sid)}
    nj1, nj2, nj5, nj10 = obs_map("jgb_1y"), obs_map("jgb_2y"), obs_map("jgb_5y"), obs_map("jgb_10y")
    ncpi = obs_map("core_cpi_yoy")

    def month_end_of(ym):
        y, m = int(ym[:4]), int(ym[5:7])
        return (date(y, 12, 31) if m == 12
                else date.fromordinal(date(y, m + 1, 1).toordinal() - 1)).isoformat()

    xp1 = [(month_end_of(m), nj1[m] - ncpi[m]) for m in sorted(nj1) if m in ncpi]
    xp10 = [(month_end_of(m), nj10[m] - ncpi[m]) for m in sorted(nj10) if m in ncpi]
    xp3 = [(month_end_of(m), (nj2[m] + (nj5[m] - nj2[m]) / 3.0) - ncpi[m])
           for m in sorted(nj2) if m in nj5 and m in ncpi]
    upsert_observations(conn, "real_1y_xp", xp1, "COMPUTED")
    upsert_observations(conn, "real_3y_xp", xp3, "COMPUTED")
    upsert_observations(conn, "real_10y_xp", xp10, "COMPUTED")
    for sid in ("real_1y", "real_3y", "real_10y"):
        raw[sid] = to_monthly(get_series(conn, sid), grid)

    # ---- Per-series accommodation scores ----
    conn.execute("DELETE FROM indicators")
    cat = {r["series_id"]: r for r in catalog_rows(conn)}
    series_scores = {}      # sid -> {date: score}
    for r in catalog_rows(conn):
        sid = r["series_id"]
        if r["weight"] <= 0 or r["polarity"] == 0:
            continue
        z = zscores(raw.get(sid, {}))
        signed = {d: (None if v is None else v * r["polarity"]) for d, v in z.items()}
        series_scores[sid] = signed
        payload = [("series", sid, d, s, raw[sid].get(d))
                   for d, s in signed.items() if s is not None]
        conn.executemany(
            "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES(?,?,?,?,?)",
            payload)

    # ---- Axis aggregation (weighted mean of member series scores) ----
    axis_scores = {a: {} for a in AXES}
    for a in AXES:
        # The catalog 'category' equals the axis name for every scored series.
        members = [(sid, cat[sid]["weight"]) for sid in series_scores if cat[sid]["category"] == a]
        for d in grid:
            num = den = 0.0
            for sid, w in members:
                s = series_scores[sid].get(d)
                if s is not None:
                    num += w * s
                    den += w
            if den > 0:
                axis_scores[a][d] = num / den
        payload = [("axis", a, d, s, None) for d, s in axis_scores[a].items()]
        conn.executemany(
            "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES(?,?,?,?,?)",
            payload)

    # ---- Stage composites ----
    stage_map = {"stage1": ["real_rate"],
                 "stage2": ["funding_costs", "availability", "asset_prices", "funding_volumes"]}
    for stage, axes in stage_map.items():
        for d in grid:
            vals = [axis_scores[a][d] for a in axes if d in axis_scores[a]]
            if vals:
                conn.execute(
                    "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES(?,?,?,?,?)",
                    ("stage", stage, d, statistics.fmean(vals), None))

    # ---- Composite FCI: equal-weight mean across the five axes ----
    for d in grid:
        vals = [axis_scores[a][d] for a in AXES if d in axis_scores[a]]
        if vals:
            conn.execute(
                "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES(?,?,?,?,?)",
                ("composite", "fci", d, statistics.fmean(vals), None))

    # ---- Real policy rate vs natural-rate gap (policy lens) ----
    rp_monthly = to_monthly(get_series(conn, "real_policy_rate"), grid)
    for d in grid:
        rp = rp_monthly.get(d)
        rstar = g("natural_rate_mid", d)
        if rp is not None and rstar is not None:
            conn.execute(
                "INSERT OR REPLACE INTO indicators(scope,key,date,score,value) VALUES(?,?,?,?,?)",
                ("composite", "rate_gap", d, rp - rstar, rp))
    conn.commit()

    latest = grid[-1]
    fci = conn.execute("SELECT score FROM indicators WHERE scope='composite' AND key='fci' "
                       "AND date<=? ORDER BY date DESC LIMIT 1", (latest,)).fetchone()
    set_meta(conn, "last_built", date.today().isoformat())
    print(f"Indicators built through {latest}. Latest composite FCI score = "
          f"{fci['score']:.2f}" if fci else "Indicators built.")


if __name__ == "__main__":
    main()
