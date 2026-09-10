
---

# Companion: Japan Monetary & Liquidity Conditions Tracker

A second tracker in the same repository/database that looks *upstream* of financial
conditions — at the **stance and quantity of money** and the **availability of funds** in
the system. 🌐 Live: https://ly069.github.io/Japan-Financial-Condition-Tracker/monetary.html

## Definitions
- **Monetary conditions** — how loose or tight the central bank's instruments are, as transmitted
  through the *price* of money (real short rates), the *exchange rate* (the classic Monetary
  Conditions Index channel), the *quantity* of money and credit (M2/M3, bank lending), and the
  *BoJ balance-sheet stance* (QQE expansion vs the post-2024 taper).
- **Liquidity conditions** — the availability of funds and ease of trading, in three layers:
  **central-bank liquidity** (monetary base, BoJ current-account balances), **funding liquidity**
  (TONA vs target, 3m TIBOR–OIS, USD/JPY cross-currency basis) and **market liquidity** (BoJ Bond
  Market Survey functioning DI, JGB bid-ask, BoJ share of outstanding JGBs, Nikkei VI).
- *Financial conditions* (the first tracker) are the downstream **transmission outcomes** — funding
  costs, availability, asset prices, volumes — that these upstream conditions produce.

## Axes and indicators
| Stage | Axis | Members (weight) | Live source |
|---|---|---|---|
| Monetary | Real short-rate stance | real policy rate ex-post (1.0), real 1Y ex-post (1.0) | computed (FRED/MoF/e-Stat) |
| Monetary | Money & credit aggregates | M2 y/y (1.0), M3 y/y (0.5), bank lending y/y (1.0) | FRED `MYAGM2JPM189N`, `MABMM301JPM189S` |
| Monetary | Exchange rate (MCI) | BIS REER (1.0), USD/JPY (0.5) | FRED `RBJPBIS`, `EXJPUS` |
| Monetary | BoJ balance-sheet stance | BoJ total assets y/y (1.0) | FRED `JPNASSETS` |
| Liquidity | Central-bank liquidity | monetary base y/y (1.0), BoJ current-account balances y/y (1.0) | BoJ CSV |
| Liquidity | Funding liquidity | call–policy spread (1.0), 3m TIBOR–OIS (1.0), USD/JPY 3m basis (0.75) | BoJ CSV |
| Liquidity | Market liquidity | JGB market-functioning DI (1.0), JGB bid-ask (0.75), BoJ JGB share (0.75), Nikkei VI (0.5) | BoJ CSV |

**Scoring.** Every indicator is z-scored over its **longest available history** and polarity-signed so
**+ = easier / more liquid**; axes are weighted means; **MCI** (monetary) and **LCI** (liquidity) are
equal-weight means of their axes; **MLCI** averages the two. Direction = trailing 6-month change.

## Files
- `etl/ml_framework.py` (axes/members), `etl/seed_data_ml.py`, `etl/build_indicators_ml.py`,
  `etl/export_web_ml.py`, `etl/export_excel_ml.py` — all run by `etl/run_all.py`.
- `web/monetary.html` + `web/app_ml.js` (dashboard; `web/data_ml.json` / `data_ml.js`).
- `Japan_ML_Tracker.xlsx` (workbook), `report/Japan_Monetary_Liquidity_Conditions_Assessment.md`
  (assessment) and `report/research/` (literature review).

> BoJ-only money-market and market-functioning series are illustrative seed anchored to recent
> observations until BoJ Time-Series / Bond Market Survey CSVs are ingested via
> `python etl/fetch.py --boj-dir ./boj_exports` (file stems = series ids).
