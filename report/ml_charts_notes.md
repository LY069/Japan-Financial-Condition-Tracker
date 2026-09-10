# Chart notes — Japan Monetary & Liquidity Conditions Assessment

Companion to `Japan_Monetary_Liquidity_Conditions_Assessment.md`. Each chart is specified against series in `web/data_ml.json` (snapshot 2026-09-30, generated 2026-09-10) so it can be reproduced from the tracker. Sign convention: positive = easier / more liquid. Seed-status series are marked (S); treat their pre-2024 shapes as illustrative.

---

## Chart 1 — MCI vs LCI vs MLCI (the headline divergence)
- **Type:** three-line chart from `indicator_series.mci`, `lci`, `mlci`; zero line bold.
- **Window:** 2005-01 to 2026-09 (the full seven-axis period).
- **Key values (Sep-26):** MCI +0.27, LCI −0.17, MLCI +0.05.
- **Annotations:** QQE Apr-2013 (LCI peak +1.29 Dec-2013); YCC stress Mar-2023 (LCI −0.43); taper Aug-2024; hikes Jan-2025 / Dec-2025 / Jun-2026.
- **Story:** the composites diverge from 2022 — MCI holds +0.5–0.7 while LCI turns negative — and converge to neutral only after the 2025–26 hikes.

## Chart 2 — Quantity vs price of money (the central argument)
- **Type:** dual-panel. Top: `axis::mon_balance_sheet` and `axis::liq_cb` (quantity). Bottom: `axis::mon_rates`, `axis::mon_fx`, `axis::liq_funding` (price).
- **Window:** 2013-01 to 2026-09.
- **Key values (Sep-26):** quantity −1.26 / −1.33; price +0.33 / +1.79 / +0.42.
- **Story:** quantity axes fall almost linearly from mid-2024; price axes stay positive. Shade the post-Aug-2024 taper period.

## Chart 3 — Base money withdrawal against the 2006 precedent
- **Type:** line, `series.monetary_base_yoy` (S) and `series.boj_ca_yoy` (S), with `series.boj_assets_yoy` (live) overlaid.
- **Window:** 2005-01 to 2026-09.
- **Highlights:** Jun-2006 trough −20.5% / −40.2%; Dec-2013 peak +46.4% / +100%; Sep-2026 −13.1% / −14.5% (assets −8.2%).
- **Story:** the current withdrawal is second only to the 2006 exit in pace.

## Chart 4 — Money vs credit divergence
- **Type:** line, `series.m2_yoy`, `series.m3_yoy` (live) vs `series.bank_lending_yoy` (S).
- **Window:** 2015-01 to 2026-09.
- **Key values:** M2 +2.18%, M3 +1.73%, lending +5.72%.
- **Story:** the pandemic money surge (M2 +9.2% Dec-2020) faded with modest inflation pass-through; lending now runs ~3.5pp above money — deposits diverted to investment trusts and QT, not weak credit demand.

## Chart 5 — The yen as a monetary-conditions variable
- **Type:** dual-axis. Left: `series.reer` (inverted, so up = easier). Right: `series.usdjpy`. Overlay `axis::mon_fx` as a thin line on a third scale if the charting library allows; otherwise a small multiple.
- **Window:** 2005-01 to 2026-09.
- **Annotations:** REER max 120.7 Oct-2011; REER min 61.6 Jun-2024; USD/JPY max 162.3 Jul-2026; ¥15.4tn intervention Jul–Aug 2026.
- **Story:** the FX axis at +1.79 is the easiest in the framework; intervention moved the level but barely the score.

## Chart 6 — JGB market functioning: survey vs hard data
- **Type:** combo. Bars: `series.jgb_market_functioning_di` (S, quarterly). Lines: `series.jgb_10y_vol` (live, bp) and `series.jgb_10s30s` (live, pp) on a right axis.
- **Window:** 2015-03 to 2026-09.
- **Key values:** DI −64 (Mar-2023) → −14 (Sep-2026); vol 13.7bp (Mar-2026) → 10.2bp; 10s30s 1.47pp (Oct-2025) → 1.09pp.
- **Story:** survey and computed series agree that the 2025–26 super-long stress peaked in Q4 2025 and has eased; the live series carry the conclusion independently of the seed DI.

## Chart 7 — Free float and the BoJ share
- **Type:** area, `series.boj_jgb_share` (S), with `series.jgb_10y` overlaid.
- **Window:** 2005-03 to 2026-09.
- **Highlights:** share 8.1% (Mar-2005) → 53.1% (Jun-2023) → 48.9%; 10Y −0.28% (Aug-2019) → 2.95% (Sep-2026).
- **Story:** the float is being returned slowly; the 10Y is at a 30-year high with the policy rate at 1.00% — the term-premium story.

## Chart 8 — Funding liquidity: no stress
- **Type:** small multiples, `series.call_policy_spread`, `series.tibor_ois_3m`, `series.jpy_basis_3m` (all S), with ±1σ bands from full history.
- **Window:** 2005-01 to 2026-09.
- **Key values:** 1.4bp; 0.19pp; −30bp. GFC extremes for scale: 15bp; 0.60pp; −109bp (basis min −138bp Mar-2020).
- **Story:** the IOER floor holds through two years of QT; this panel is the regime switch for reading Chart 3 (intended progress vs stress).

## Chart 9 — Axis scorecard (current snapshot)
- **Type:** horizontal diverging bar from `axes[].score`, grouped by index, colored by sign; direction arrow from `axes[].direction.label`.
- **Values:** rates +0.33 ▼, money & credit +0.23 →, FX +1.79 →, balance sheet −1.26 →, CB liquidity −1.33 →, funding +0.42 →, market +0.40 ▲.
- **Story:** two restrictive quantity axes vs five easy price/plumbing axes.

## Chart 10 — Baseline sensitivity (methodology panel)
- **Type:** dot plot of the realized-volatility and real-1Y scores under three baselines (full history / 2005+ / 2013+): vol +0.30 / −0.61 / −0.97; real 1Y +0.53 / −0.01 / −0.49.
- **Story:** level verdicts are baseline-dependent; direction is not. Computed offline from `series[*].observations` — not published in `data_ml.json`.

---

### Data caveat
`meta.data_mode` is LIVE + SEED. Series marked (S) are illustrative seed anchored to recent verified observations until BoJ CSVs are ingested (`meta.source_note`); refresh via the ETL before publication use. The two computed market-stress series and all FRED-mirrored series are live.
