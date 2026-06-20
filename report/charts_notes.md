# Chart notes — Japan Financial Conditions Assessment

Companion to `Japan_Financial_Conditions_Assessment.md`. Each chart below is specified against series in `web/data.json` so it can be reproduced from the tracker. All figures are from the SEED snapshot (latest_date 2026-06-30); refresh via `etl/fetch.py` before publication. Sign convention: positive = accommodative.

---

## Chart 1 — Composite FCI vs policy rate (the headline)
- **Type:** dual-axis line. Left: `indicator_series.fci`. Right: `series.policy_rate`.
- **Window:** 2023-01 to 2026-06.
- **Annotations:** policy hikes at 2025-01 (0.25→0.50), 2025-12 (0.50→0.75), 2026-06 (0.75→1.00).
- **Story:** FCI drifts down (+1.01 Dec-24 → +0.69 Jun-26) as the rate quadruples, yet stays well above 0 — accommodation narrowing, not gone.

## Chart 2 — The real-rate curve split (most important chart)
- **Type:** line, 3 series: `series.real_1y`, `real_3y`, `real_10y`. Zero line bold.
- **Window:** 2024-01 to 2026-06.
- **Key values (Jun-26):** 1Y −1.03%, 3Y −0.38%, 10Y **+0.87%**.
- **Story:** front/medium real rates still negative (accommodative, high activity weight); long-end real rate has crossed firmly positive (restrictive). Shade the region where 10Y real > 0 (from ~late 2025).

## Chart 3 — JGB curve shift and bear-steepening
- **Type:** curve snapshots (x = maturity 1/2/5/10/30Y) for Jun-2025, Dec-2025, Jun-2026 using `series.jgb_*`.
- **Highlight:** 10Y +1.15pp in 12 months (1.52 → 2.67%), far exceeding the 0.50pp of policy hikes → rising term premium.

## Chart 4 — Axis scorecard (current snapshot)
- **Type:** horizontal diverging bar; one bar per axis from `axes[].score`, colored by sign.
- **Values:** real_rate −0.04, funding_costs −0.89, availability +1.09, asset_prices +2.74, funding_volumes +0.55.
- **Story:** funding costs the lone restrictive axis; asset prices dominate the positive composite.

## Chart 5 — Axis trajectories (what is doing the tightening)
- **Type:** small-multiples lines from `indicator_series.axis::*` plus `stage1`, `stage2`.
- **Window:** 2024-01 to 2026-06.
- **Story:** Stage 1 / real-rate axis (+1.13 → −0.04) and funding-costs axis (+0.25 → −0.89) carry the move; Stage 2 barely shifts (+0.98 → +0.87).

## Chart 6 — Natural-rate band vs real policy rate
- **Type:** shaded band (`series.natural_rate_low`/`_mid`/`_high`) with `series.real_policy_rate` overlaid.
- **Key values (Jun-26):** band −0.85% to +0.55% (mid −0.15%); real policy rate −0.98%; gap ≈ −0.83pp.
- **Story:** real policy rate below the band midpoint → accommodative on the natural-rate lens; band width conveys r\* uncertainty. Show band edging up over 2025–26.

## Chart 7 — Transmission acid test: volumes & availability
- **Type:** combo. Bars: `series.bank_lending_yoy`, `cp_corpbond_yoy`. Lines: `tankan_lend_small`, `tankan_finpos_small`.
- **Story:** volumes still growing (+3.1%, +6.4%), small-firm DIs still positive → hikes not yet biting on funding activity. These are the §7 watchlist tripwires.

## Chart 8 — Funding costs vs credit risk
- **Type:** line. `series.lending_rate`, `cp_rate` (rising) vs `corp_bond_spread` (flat, ~0.31%).
- **Story:** higher funding costs are the safe-rate base repricing, not credit-risk widening — system not fragile.

---

### Data caveat
SEED mode (`meta.data_mode`): illustrative approximations anchored to recent observations. Per `meta.source_note`, run `etl/fetch.py` for authoritative BoJ/MoF/e-Stat/FRED data before any decision or publication use.
