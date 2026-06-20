# Japan Financial Conditions Tracker

An economic tracker for **Japan's financial conditions**, built on the **Bank of Japan's
official two-stage assessment framework** as described in *BoJ Review 2026-E-4,
"Developments in the Natural Rate of Interest and the Assessment of the Degree of Monetary
Accommodation"* (Monetary Affairs Department, March 2026).

It answers two questions the BoJ itself poses:

1. **How accommodative or restrictive are Japan's financial conditions right now?**
2. **Do current conditions — read alongside the natural-rate estimate — support further rate hikes?**

The tracker ships as **four connected artifacts**:

| Artifact | File | What it is |
|---|---|---|
| 📊 **Web dashboard** | `web/index.html` | Interactive single-page app mirroring the BoJ two-stage framework. Open directly in a browser. |
| 🗄️ **Database** | `data/jfct.db` | SQLite single-source-of-truth: catalog, observations, computed indicators. |
| 📒 **Excel workbook** | `Japan_FCI_Tracker.xlsx` | Refreshable workbook (Dashboard + per-stage sheets + wide data + indicators + catalog). |
| 📝 **Assessment report** | `report/Japan_Financial_Conditions_Assessment.md` | Economist's assessment of conditions, hike impact, and the rate-path verdict. |

All four are generated from the same database, so they always agree.

---

## The framework

The BoJ assesses the degree of monetary accommodation through **two stages** (Chart 6 of the paper),
because financial conditions are the *transmission channel* from monetary policy to the real economy:

**Stage 1 — Interest-rate developments**
- Short-term **policy rate** and safe-asset yields (**JGB yield curve**).
- **Real interest rates** (nominal − expected inflation) **by maturity** — short/medium real rates
  matter most for activity.

**Stage 2 — Funding environment**, across four axes:
- **Funding costs** — lending rates, CP/corporate-bond issuance rates (= safe yields + spreads).
- **Availability of funds** — Tankan lending-attitude & financial-position DIs.
- **Asset prices** — equities (TOPIX/Nikkei) and the exchange rate (USD/JPY).
- **Funding volumes** — bank lending and CP/corporate-bond outstanding (y/y).

**The natural-rate lens (cross-check).** Separately, the real policy rate is compared with the
**natural rate of interest** (BoJ's six-model estimate, ≈ −0.9% to +0.5% as of 2025/Q3). A real rate
below the natural rate signals an accommodative stance — but the estimate carries *considerable*
uncertainty ("navigating by the stars under cloudy skies"), so the financial-conditions read is
weighted heavily, especially as the policy rate nears neutral. The tracker reports **both lenses**;
the report explains how they jointly shape the hiking path.

### Composite index
The dashboard/workbook compute a **Financial Conditions Index (FCI)** — an *analytical synthesis*
(z-scored accommodation scores aggregated over the framework's five axes; **+ = accommodative** vs
2005+ history). It is **not** an official BoJ index; it operationalises the paper's multi-axis,
comprehensive-judgment approach into one comparable gauge.

---

## Quick start

```bash
pip install -r requirements.txt          # only openpyxl is required

# Offline demo (uses illustrative seed data anchored to recent observations):
python etl/run_all.py --seed --no-fetch

# Open the dashboard:
open web/index.html                       # or just double-click it
```

`run_all.py` runs the full pipeline: **seed → fetch → indicators → exports**, regenerating
`data/jfct.db`, `web/data.json` (+ `web/data.js`), and `Japan_FCI_Tracker.xlsx`.

---

## Updating with live data

Data flows from official / authoritative sources, BoJ and Japanese government first:

| Source | Provider | Coverage | Auth |
|---|---|---|---|
| **MoF** JGB reference yields | `etl/sources.py: fetch_mof_jgb` | JGB curve (1/2/5/10/30y), daily CSV | none |
| **e-Stat** (MIC) | `fetch_estat` | Core CPI | free `ESTAT_APP_ID` |
| **FRED** (mirrors BoJ/MoF/MIC) | `fetch_fred` | Policy rate, 10y JGB, CPI, USD/JPY, Nikkei | free `FRED_API_KEY` |
| **BoJ** Time-Series Data Search | `load_boj_csv` (via `--boj-dir`) | Tankan DIs, inflation-expectations index, lending/CP volumes, r* | CSV export |

```bash
export FRED_API_KEY=xxxx      # https://fred.stlouisfed.org/docs/api/api_key.html
export ESTAT_APP_ID=yyyy      # https://www.e-stat.go.jp/api/
python etl/run_all.py                       # live refresh; un-fetched series keep prior values
python etl/fetch.py --boj-dir ./boj_exports # ingest BoJ stat-search CSV exports
```

Each source is fetched independently and failures are non-fatal — a missing key or offline run
simply preserves existing values. The **GitHub Action** in `.github/workflows/update.yml` runs the
pipeline on a weekday schedule and commits refreshed artifacts (set `FRED_API_KEY` / `ESTAT_APP_ID`
as repo secrets).

> **Data mode.** Out of the box the tracker is seeded with **illustrative** series anchored to
> recent real observations (June 2026) and the paths described in the paper's charts, so every
> artifact is fully populated. Running the live ETL overwrites these with authoritative values.
> The current mode is shown in the dashboard badge and `meta.data_mode`.

---

## Repository layout

```
data/
  series_catalog.csv     # the framework mapping: every series -> stage/axis/source/polarity/weight
  jfct.db                # SQLite database (built)
etl/
  db.py                  # schema + helpers (single source of truth)
  seed_data.py           # illustrative seed series (offline demo)
  sources.py             # live connectors: MoF / e-Stat / FRED / BoJ-CSV
  fetch.py               # orchestrate live refresh
  build_indicators.py    # real rates, accommodation z-scores, axes, FCI, rate gap
  export_web.py          # -> web/data.json (+ data.js)
  export_excel.py        # -> Japan_FCI_Tracker.xlsx
  run_all.py             # one-command pipeline
web/                     # dashboard (index.html, app.js, styles.css, data.json/js)
report/                  # assessment report
.github/workflows/       # scheduled refresh
```

## Methodology notes
- **Accommodation score** for a series = z-score over its 2005+ monthly history × **polarity**
  (catalog field; +1 = higher is accommodative, −1 = higher is restrictive). So a *lower* real rate
  or *lower* spread scores **positive** (accommodative).
- **Axis score** = weight-weighted mean of member series scores. **FCI** = equal-weight mean of the
  five axes. **Rate gap** = real policy rate − natural-rate midpoint.
- Quarterly series (Tankan, potential growth, r*) are forward-filled to the monthly grid.

## Source
Bank of Japan (2026), *"Developments in the Natural Rate of Interest and the Assessment of the
Degree of Monetary Accommodation,"* **Bank of Japan Review 2026-E-4**, Monetary Affairs Department.
