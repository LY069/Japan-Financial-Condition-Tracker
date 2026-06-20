"""Seed the tracker DB with realistic illustrative series.

These series are anchored to (a) real, recently observed values gathered for
June 2026 and (b) the qualitative paths described in BoJ Review 2026-E-4
(charts 3-9). They are *illustrative approximations* so the database, web app
and Excel workbook are fully populated and the pipeline is demonstrable end to
end. Running `etl/fetch.py` with network access overwrites every series with
authoritative values from the official sources listed in series_catalog.csv.

Generation is deterministic (fixed seed) so rebuilds are reproducible.
"""
from __future__ import annotations

import math
import random
from datetime import date

from db import connect, init_db, load_catalog, upsert_observations, set_meta

random.seed(20260620)

START = date(2005, 1, 1)
END = date(2026, 6, 1)


def month_ends(start: date = START, end: date = END):
    """Yield period-end ISO dates (month end approximated as 28th->last)."""
    y, m = start.year, start.month
    out = []
    while (y, m) <= (end.year, end.month):
        # last day of month
        if m == 12:
            nd = date(y + 1, 1, 1)
        else:
            nd = date(y, m + 1, 1)
        last = (nd.toordinal() - 1)
        out.append(date.fromordinal(last).isoformat())
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def quarter_ends(start: date = START, end: date = END):
    out = []
    for d in month_ends(start, end):
        mm = int(d[5:7])
        if mm in (3, 6, 9, 12):
            out.append(d)
    return out


def interp(anchors, dates, noise=0.0):
    """Piecewise-linear interpolation of (iso_date,value) anchors onto `dates`.

    Anchors must be sorted. Values before/after the range are held flat.
    """
    ax = [date.fromisoformat(d).toordinal() for d, _ in anchors]
    ay = [v for _, v in anchors]
    out = []
    for d in dates:
        x = date.fromisoformat(d).toordinal()
        if x <= ax[0]:
            y = ay[0]
        elif x >= ax[-1]:
            y = ay[-1]
        else:
            i = 0
            while ax[i + 1] < x:
                i += 1
            t = (x - ax[i]) / (ax[i + 1] - ax[i])
            y = ay[i] + t * (ay[i + 1] - ay[i])
        if noise:
            y += random.uniform(-noise, noise)
        out.append((d, round(y, 4)))
    return out


def step(anchors, dates):
    """Step function: value holds until the next anchor date (for policy rate)."""
    ax = [date.fromisoformat(d).toordinal() for d, _ in anchors]
    ay = [v for _, v in anchors]
    out = []
    for d in dates:
        x = date.fromisoformat(d).toordinal()
        y = ay[0]
        for i, xi in enumerate(ax):
            if x >= xi:
                y = ay[i]
        out.append((d, round(y, 4)))
    return out


def build():
    mdates = month_ends()
    qdates = quarter_ends()

    series = {}

    # ---- Stage 1: policy rate (step function through the hiking cycle) ----
    series["policy_rate"] = step([
        ("2005-01-31", 0.0), ("2006-07-31", 0.25), ("2007-02-28", 0.50),
        ("2008-10-31", 0.30), ("2008-12-31", 0.10), ("2010-10-31", 0.05),
        ("2013-04-30", 0.10), ("2016-02-29", -0.10), ("2024-03-31", 0.05),
        ("2024-07-31", 0.25), ("2025-01-31", 0.50), ("2025-12-31", 0.75),
        ("2026-06-30", 1.00),
    ], mdates)

    # ---- JGB nominal curve ----
    series["jgb_1y"] = interp([
        ("2005-01-31", 0.02), ("2006-12-31", 0.55), ("2008-06-30", 0.75),
        ("2009-06-30", 0.30), ("2013-01-31", 0.08), ("2016-06-30", -0.30),
        ("2022-12-31", -0.07), ("2024-03-31", 0.05), ("2025-01-31", 0.45),
        ("2025-12-31", 0.78), ("2026-06-30", 0.95),
    ], mdates, noise=0.02)
    series["jgb_2y"] = interp([
        ("2005-01-31", 0.08), ("2006-12-31", 0.80), ("2008-06-30", 0.95),
        ("2013-01-31", 0.10), ("2016-06-30", -0.28), ("2022-12-31", 0.02),
        ("2024-03-31", 0.18), ("2025-01-31", 0.65), ("2025-12-31", 1.05),
        ("2026-06-30", 1.30),
    ], mdates, noise=0.02)
    series["jgb_5y"] = interp([
        ("2005-01-31", 0.55), ("2006-12-31", 1.30), ("2008-06-30", 1.55),
        ("2013-01-31", 0.18), ("2016-06-30", -0.20), ("2020-06-30", -0.10),
        ("2022-12-31", 0.25), ("2024-03-31", 0.45), ("2025-01-31", 0.95),
        ("2025-12-31", 1.45), ("2026-06-30", 1.85),
    ], mdates, noise=0.03)
    series["jgb_10y"] = interp([
        ("2005-01-31", 1.40), ("2006-12-31", 1.68), ("2008-06-30", 1.75),
        ("2010-09-30", 1.00), ("2013-01-31", 0.78), ("2016-07-31", -0.10),
        ("2019-08-31", -0.25), ("2021-12-31", 0.07), ("2022-12-31", 0.42),
        ("2023-10-31", 0.90), ("2024-06-30", 1.05), ("2025-01-31", 1.25),
        ("2025-09-30", 1.65), ("2025-12-31", 2.05), ("2026-03-31", 2.35),
        ("2026-06-30", 2.65),
    ], mdates, noise=0.03)
    series["jgb_30y"] = interp([
        ("2005-01-31", 2.20), ("2008-06-30", 2.65), ("2013-01-31", 1.95),
        ("2016-07-31", 0.30), ("2019-08-31", 0.20), ("2022-12-31", 1.55),
        ("2024-06-30", 2.05), ("2025-09-30", 2.70), ("2025-12-31", 3.05),
        ("2026-06-30", 3.35),
    ], mdates, noise=0.03)

    # ---- Inflation expectations (composite, by horizon) ----
    series["infexp_1y"] = interp([
        ("2005-01-31", -0.2), ("2008-09-30", 1.2), ("2009-06-30", -0.6),
        ("2014-04-30", 1.4), ("2016-06-30", 0.4), ("2020-06-30", 0.2),
        ("2022-12-31", 1.6), ("2023-06-30", 2.2), ("2024-06-30", 2.1),
        ("2025-06-30", 2.0), ("2026-06-30", 2.0),
    ], mdates, noise=0.05)
    series["infexp_3y"] = interp([
        ("2005-01-31", 0.0), ("2008-09-30", 0.9), ("2009-06-30", -0.1),
        ("2014-04-30", 1.1), ("2016-06-30", 0.5), ("2020-06-30", 0.4),
        ("2022-12-31", 1.3), ("2023-06-30", 1.7), ("2024-06-30", 1.9),
        ("2025-06-30", 1.9), ("2026-06-30", 1.9),
    ], mdates, noise=0.04)
    series["infexp_10y"] = interp([
        ("2005-01-31", 0.3), ("2009-06-30", 0.3), ("2014-04-30", 1.0),
        ("2016-06-30", 0.6), ("2020-06-30", 0.5), ("2022-12-31", 1.1),
        ("2023-06-30", 1.4), ("2024-06-30", 1.6), ("2025-06-30", 1.7),
        ("2026-06-30", 1.8),
    ], mdates, noise=0.03)

    # ---- Stage 2: funding costs ----
    series["lending_rate"] = interp([
        ("2005-01-31", 1.55), ("2008-06-30", 1.70), ("2010-06-30", 1.35),
        ("2013-06-30", 1.05), ("2016-06-30", 0.80), ("2020-06-30", 0.68),
        ("2024-03-31", 0.72), ("2025-01-31", 0.90), ("2025-12-31", 1.05),
        ("2026-06-30", 1.18),
    ], mdates, noise=0.02)
    series["cp_rate"] = interp([
        ("2005-01-31", 0.05), ("2007-06-30", 0.70), ("2009-06-30", 0.30),
        ("2013-06-30", 0.10), ("2016-06-30", 0.00), ("2024-03-31", 0.10),
        ("2025-01-31", 0.55), ("2025-12-31", 0.85), ("2026-06-30", 1.10),
    ], mdates, noise=0.02)
    series["corp_bond_spread"] = interp([
        ("2005-01-31", 0.30), ("2008-12-31", 0.85), ("2010-06-30", 0.45),
        ("2013-06-30", 0.35), ("2016-06-30", 0.28), ("2020-05-31", 0.55),
        ("2022-06-30", 0.30), ("2025-01-31", 0.26), ("2026-06-30", 0.30),
    ], mdates, noise=0.02)

    # ---- Stage 2: availability (Tankan DIs, quarterly) ----
    series["tankan_lend_large"] = interp([
        ("2005-03-31", 12), ("2007-06-30", 18), ("2008-12-31", -8),
        ("2009-06-30", -18), ("2011-03-31", 6), ("2013-06-30", 14),
        ("2016-06-30", 22), ("2019-06-30", 22), ("2020-06-30", 8),
        ("2022-06-30", 20), ("2024-06-30", 25), ("2025-12-31", 24),
        ("2026-03-31", 23),
    ], qdates, noise=1.0)
    series["tankan_lend_small"] = interp([
        ("2005-03-31", 2), ("2007-06-30", 8), ("2008-12-31", -18),
        ("2009-06-30", -24), ("2011-03-31", -4), ("2013-06-30", 4),
        ("2016-06-30", 14), ("2019-06-30", 16), ("2020-06-30", -2),
        ("2022-06-30", 12), ("2024-06-30", 18), ("2025-12-31", 18),
        ("2026-03-31", 17),
    ], qdates, noise=1.0)
    series["tankan_finpos_large"] = interp([
        ("2005-03-31", 8), ("2007-06-30", 14), ("2008-12-31", -6),
        ("2009-06-30", -14), ("2011-03-31", 6), ("2013-06-30", 12),
        ("2016-06-30", 18), ("2019-06-30", 20), ("2020-06-30", 6),
        ("2022-06-30", 18), ("2024-06-30", 22), ("2025-12-31", 21),
        ("2026-03-31", 21),
    ], qdates, noise=1.0)
    series["tankan_finpos_small"] = interp([
        ("2005-03-31", 0), ("2007-06-30", 4), ("2008-12-31", -16),
        ("2009-06-30", -21), ("2011-03-31", -2), ("2013-06-30", 4),
        ("2016-06-30", 10), ("2019-06-30", 12), ("2020-06-30", -8),
        ("2022-06-30", 8), ("2024-06-30", 14), ("2025-12-31", 14),
        ("2026-03-31", 13),
    ], qdates, noise=1.0)

    # ---- Stage 2: asset prices ----
    series["topix"] = interp([
        ("2005-01-31", 1150), ("2007-06-30", 1750), ("2009-02-28", 750),
        ("2012-11-30", 760), ("2015-06-30", 1630), ("2018-09-30", 1820),
        ("2020-03-31", 1300), ("2021-09-30", 2090), ("2023-06-30", 2290),
        ("2024-07-31", 2870), ("2025-06-30", 3250), ("2026-03-31", 3700),
        ("2026-06-30", 3950),
    ], mdates, noise=18)
    series["nikkei225"] = interp([
        ("2005-01-31", 11400), ("2007-06-30", 18100), ("2009-02-28", 7600),
        ("2012-11-30", 9000), ("2015-06-30", 20500), ("2018-09-30", 24100),
        ("2020-03-31", 18900), ("2021-09-30", 29800), ("2023-06-30", 33200),
        ("2024-07-31", 41000), ("2025-06-30", 44500), ("2026-03-31", 51000),
        ("2026-06-30", 54500),
    ], mdates, noise=220)
    series["usdjpy"] = interp([
        ("2005-01-31", 103), ("2007-06-30", 122), ("2011-10-31", 76),
        ("2013-05-31", 101), ("2015-06-30", 123), ("2016-08-31", 101),
        ("2020-03-31", 108), ("2022-10-31", 148), ("2023-11-30", 150),
        ("2024-07-31", 158), ("2025-06-30", 157), ("2026-06-30", 161),
    ], mdates, noise=1.2)

    # ---- Stage 2: funding volumes (y/y %) ----
    series["bank_lending_yoy"] = interp([
        ("2005-01-31", -1.8), ("2007-06-30", 0.8), ("2008-12-31", 3.6),
        ("2010-06-30", -1.9), ("2013-06-30", 2.3), ("2016-06-30", 2.4),
        ("2020-06-30", 6.2), ("2021-06-30", 0.8), ("2023-06-30", 3.1),
        ("2025-06-30", 3.4), ("2026-06-30", 3.2),
    ], mdates, noise=0.15)
    series["cp_corpbond_yoy"] = interp([
        ("2005-01-31", 1.0), ("2008-12-31", 8.0), ("2010-06-30", -2.0),
        ("2013-06-30", 2.0), ("2016-06-30", 4.5), ("2020-06-30", 12.0),
        ("2021-06-30", 3.0), ("2023-06-30", 5.0), ("2025-06-30", 6.5),
        ("2026-06-30", 6.0),
    ], mdates, noise=0.4)

    # ---- Context ----
    series["core_cpi_yoy"] = interp([
        ("2005-01-31", -0.3), ("2008-09-30", 2.4), ("2009-08-31", -2.4),
        ("2014-05-31", 1.5), ("2016-06-30", 0.0), ("2020-06-30", -0.5),
        ("2022-12-31", 4.0), ("2023-06-30", 3.3), ("2024-06-30", 2.6),
        ("2025-06-30", 2.4), ("2026-03-31", 1.6), ("2026-06-30", 1.5),
    ], mdates, noise=0.06)
    series["potential_growth"] = interp([
        ("2005-03-31", 1.4), ("2008-06-30", 1.2), ("2009-09-30", 0.2),
        ("2012-06-30", 0.7), ("2016-06-30", 0.5), ("2019-06-30", 0.8),
        ("2020-09-30", 0.05), ("2022-06-30", 0.45), ("2024-06-30", 0.6),
        ("2026-03-31", 0.7),
    ], qdates, noise=0.03)
    # Natural rate band (six-model range), recently edging up.
    series["natural_rate_low"] = interp([
        ("2005-03-31", -1.0), ("2013-06-30", -1.3), ("2020-06-30", -1.2),
        ("2023-03-31", -1.0), ("2025-09-30", -0.9), ("2026-03-31", -0.85),
    ], qdates, noise=0.0)
    series["natural_rate_mid"] = interp([
        ("2005-03-31", -0.1), ("2013-06-30", -0.5), ("2020-06-30", -0.45),
        ("2023-03-31", -0.25), ("2025-09-30", -0.20), ("2026-03-31", -0.15),
    ], qdates, noise=0.0)
    series["natural_rate_high"] = interp([
        ("2005-03-31", 0.8), ("2013-06-30", 0.3), ("2020-06-30", 0.35),
        ("2023-03-31", 0.5), ("2025-09-30", 0.5), ("2026-03-31", 0.55),
    ], qdates, noise=0.0)

    return series


def main():
    conn = connect()
    init_db(conn)
    load_catalog(conn)
    series = build()
    total = 0
    for sid, rows in series.items():
        total += upsert_observations(conn, sid, rows, source="SEED")
    set_meta(conn, "seeded", "true")
    set_meta(conn, "data_mode", "SEED (illustrative; run etl/fetch.py for live data)")
    print(f"Seeded {len(series)} series, {total} observations into the DB.")


if __name__ == "__main__":
    main()
