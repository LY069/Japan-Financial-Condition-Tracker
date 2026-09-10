# Japan's Monetary & Liquidity Conditions — Assessment Report

**Framework:** Monetary conditions (rates, money & credit, exchange rate, balance sheet) and liquidity conditions (central-bank, funding, market layers), read as the upstream companion to the BoJ two-stage financial-conditions assessment
**Research basis:** Team literature review, *Japan Monetary & Liquidity Conditions: Literature and Indicator Review* (`report/research/monetary_liquidity_literature_review.md`, 10 September 2026) and indicator shortlist (`report/research/indicator_shortlist.csv`)
**Data:** Japan Monetary & Liquidity Conditions Tracker (`web/data_ml.json`), snapshot **2026-09-30**, generated 2026-09-10 — **LIVE + SEED mode** (FRED mirrors of BoJ/BIS/MoF series live; BoJ-only money-market and market-functioning series illustrative seed anchored to recent verified observations)
**Policy context:** BoJ policy rate **1.00%** (16 June 2026, highest since 1995); JGB-purchase taper running to ~¥2tn/month by FY2027; record ¥15.4tn yen intervention July–August 2026 (per the literature review)
**Companion report:** `report/Japan_Financial_Conditions_Assessment.md` (FCI **+1.08**, real policy rate −0.98% vs natural-rate band −0.94% / −0.36% / +0.53%)
**Prepared for:** investment professionals and policymakers

> **Labelling caveat.** The Monetary Conditions Index (MCI), Liquidity Conditions Index (LCI) and their average (MLCI) are *analytical syntheses* assembled by this tracker — z-score composites, signed so that **positive = easier / more liquid**. They are not official BoJ indices. Each indicator is scored against its **longest available history**; "direction" is the trailing 6-month change in the score (▲ easing / ▼ tightening / → stable). Several liquidity series are **seed** rather than live (see §10) and the confidence attached to them is correspondingly lower.

---

## 1. Executive summary

- **Monetary conditions are mildly accommodative; liquidity conditions are mildly restrictive; the combined read is neutral.** MCI **+0.27** (→ stable, −0.03 over six months), LCI **−0.17** (▲ easing, +0.11), MLCI **+0.05**. The neutral headline is an *average of opposites*, not a description of any single channel.

- **The quantity of central-bank money is contracting at a pace last seen at the 2006 QE exit.** Monetary base **−13.1% y/y**, BoJ current-account balances **−14.5% y/y**, BoJ total assets **−8.2% y/y**. The central-bank-liquidity axis scores **−1.33** and the balance-sheet-stance axis **−1.26** — the two most restrictive readings in the framework, and the only two in "restrictive" territory.

- **The price of money, credit and the yen remain easy.** The ex-post real policy rate is **−0.53%** and the real 1Y rate **−0.59%** (real-rate axis **+0.33**, ▼ tightening); bank lending is growing **+5.7% y/y** (score +1.67) even though M2 (**+2.2%**) and M3 (**+1.7%**) are subdued; the BIS real effective exchange rate is **63.6** (2020=100), within ~2 points of its 2024 record low, and USD/JPY is **~159** (FX axis **+1.79**, the easiest axis in the tracker).

- **Funding liquidity is orderly.** TONA sits **1.4bp** from target, 3m TIBOR–OIS is **0.19pp** (its 2005+ average is 0.21pp), and the 3m USD/JPY basis is **−30bp** against a 2005+ average of −58bp. Funding axis **+0.42**; rate control has survived the first two years of QT intact.

- **JGB market liquidity is repairing, but from a very low base.** The Bond Market Survey functioning DI has climbed from **−64 (Mar-2023)** to **−14**; the 10Y bid-ask proxy is back near 2015 levels; realized 10Y volatility has eased from **13.7bp (Mar-2026)** to **10.2bp**; the 10s30s slope has flattened from **1.47pp (Oct-2025)** to **1.09pp**. The market axis is **+0.40** (▲ easing, +0.40 over six months) — the strongest improvement of any axis — but the BoJ still holds **48.9%** of outstanding JGBs and the DI remains negative in absolute terms.

- **Long-end yields are term-premium-driven, not stance-driven.** The 10Y JGB is **2.95%** and the 30Y **4.04%** with the policy rate at 1.00%; the literature review (IMF April 2026 GFSR) attributes the rise to fiscal-risk term premia. The tracker's realized-volatility and 10s30s series were added precisely to capture this.

- **Money growth is not an inflation signal today.** On the regime-dependent "money view" (Borio, Hofmann & Zakrajšek 2023), M2 at +2.2% is *disinflationary* relative to nominal GDP; the inflation impulse is coming from the yen and energy, not from money.

- **Verdict in one line:** *Neutral on average, divergent underneath — quantity tightening hard, price still easy; the divergence is sustainable only while market functioning keeps improving.*

---

## 2. Definitions: monetary, liquidity and financial conditions

The existing tracker measures **financial conditions** — what the economy faces in the price and availability of finance. This tracker measures two concepts upstream of that. In the literature review's framing: **monetary conditions** ask *what the central bank has set* (and how much money and credit it generates); **liquidity conditions** ask *whether the plumbing works, and at what price*; financial conditions ask *what the economy faces*. The three sit on a transmission chain:

> **Money & instruments** (policy rate, balance sheet, FX) → **Liquidity** (reserves → funding markets → securities markets) → **Financial conditions** (lending rates, availability, asset prices, volumes) → **Activity & prices**

A liquidity shock — a repo squeeze, a JGB seizure, a dollar-basis blow-out — can tighten financial conditions with no change in the monetary stance, which is why the trackers are kept distinct but read together.

| | **Monetary conditions (MCI)** | **Liquidity conditions (LCI)** | **Financial conditions (FCI)** |
|---|---|---|---|
| **Question** | Is policy easy or tight relative to neutral, and how much money/credit is it generating? | Is the implementation machinery working, and at what price can institutions fund and trade? | How cheap, easy and plentiful is finance for firms and households? |
| **Canonical lineage** | Bank of Canada / RBNZ MCI (Freedman 1995); critique in Ericsson, Jansen, Kerbeshian & Nymoen (1998); money view (Borio et al. 2023) | Reserve-demand curve (Afonso, Giannone, La Spada & Williams 2022/25; Shiratsuka 2025); funding (Borio, McCauley, McGuire & Sushko 2016); JGB microstructure (Kurosaki et al. 2015; Sakiyama & Kobayashi 2018) | BoJ Review 2026-E-4 two-stage assessment |
| **Layers / axes here** | Real short-rate stance; money & credit aggregates; exchange rate; BoJ balance-sheet stance | Central-bank liquidity; funding liquidity; market liquidity | Stage 1 real rates; Stage 2 funding costs, availability, asset prices, volumes |
| **Horizon of signal** | Money → inflation 12–24 months (BIS evidence); FX → import prices within months | Funding spreads → lending spreads within weeks; market liquidity near-contemporaneous with policy reaction | Contemporaneous to 2–4 quarters |
| **Overlaps** | Policy rate and FX shared with FCI; bank lending shared with FCI volumes | BoJ JGB share also a balance-sheet stance gauge | — |
| **Current read** | **+0.27** mildly accommodative | **−0.17** mildly restrictive | **+1.08** accommodative |

The three liquidity layers are themselves chained (review §2.3): abundant reserves pin TONA to the floor (base → funding); dealers' repo access sets their warehousing capacity (funding → market); and market functioning feeds back on how fast the BoJ can shrink base liquidity, since the taper is conditioned on "developments in and functioning of the JGB markets" (market → base).

---

## 3. Key indicators

Polarity is stated in the tracker's convention: the sign applied so that **+ = easier / more liquid**. "Live" = fetched from an official or mirrored source; "seed" = illustrative series anchored to recent verified observations, pending BoJ-CSV ingestion (`meta.source_note`).

### 3.1 Monetary conditions

| Indicator (`series` key) | Axis / weight | What it measures | Source & frequency | History in tracker | Polarity / reading | Status |
|---|---|---|---|---|---|---|
| Real policy rate, ex-post (`real_policy_rate_xp`) | Real short-rate / 1.0 | Policy rate minus realized core CPI — the price of money | Computed (BoJ rate, e-Stat CPI); monthly | 2004– | Lower = easier (−1) | Live |
| Real 1Y rate, ex-post (`real_1y_xp`) | Real short-rate / 1.0 | 1Y JGB minus realized core CPI | Computed (MoF, e-Stat); monthly | **1974–** | Lower = easier (−1) | Live |
| M2 y/y (`m2_yoy`) | Money & credit / 1.0 | Broad money growth; "money view" inflation signal | BoJ Money Stock via FRED; monthly | 2005– | Faster = easier (+1) | Live |
| M3 y/y (`m3_yoy`) | Money & credit / 0.5 | Broadest aggregate; secondary to M2 | BoJ via FRED (OECD MEI); monthly | 2005– | Faster = easier (+1) | Live |
| Bank lending y/y (`bank_lending_yoy`) | Money & credit / 1.0 | Credit counterpart of money | BoJ Loans & Discounts; monthly | 2005– | Faster = easier (+1) | BoJ-CSV (seed pending) |
| BIS REER, 2020=100 (`reer`) | FX / 1.0 | Real effective yen — the classic MCI second leg | BIS via FRED; monthly | 2005– | Higher (stronger yen) = tighter (−1) | Live |
| USD/JPY (`usdjpy`) | FX / 0.5 | Bilateral rate; intervention regime | BoJ/FRED mirror; monthly | 2004– | Higher (weaker yen) = easier (+1) | Live |
| BoJ total assets y/y (`boj_assets_yoy`) | Balance sheet / 1.0 | QQE expansion vs post-2024 contraction | BoJ Accounts via FRED; monthly | 2005– | Growth = easier (+1) | Live |

### 3.2 Liquidity conditions, by layer

| Layer | Indicator (`series` key) | Weight | What it measures | Source & frequency | History | Polarity / reading | Status |
|---|---|---|---|---|---|---|---|
| Central-bank | Monetary base y/y (`monetary_base_yoy`) | 1.0 | Quantity of base money created or withdrawn | BoJ MD01; monthly | 2005– | Growth = more liquid (+1) | Seed (BoJ-CSV pending) |
| Central-bank | BoJ current-account balances y/y (`boj_ca_yoy`) | 1.0 | Reserves (mostly excess) held at the BoJ | BoJ MD06/08; monthly | 2005– | Growth = more liquid (+1) | Seed |
| Funding | Call rate − policy target (`call_policy_spread`) | 1.0 | Rate control / reserve scarcity: TONA trading above target = scarcity | BoJ FM01; monthly | 2005– | Wider = tighter (−1) | Seed |
| Funding | 3m TIBOR − OIS (`tibor_ois_3m`) | 1.0 | Bank unsecured term-funding premium | JBA TIBOR / FRED; monthly | 2005– | Wider = tighter (−1) | Seed |
| Funding | 3m USD/JPY basis (`jpy_basis_3m`) | 0.75 | Dollar-funding cost for Japanese banks | Licensed / BoJ FSR proxy; monthly | 2005– | Less negative = easier (+1) | Seed |
| Market | Bond Market Survey functioning DI (`jgb_market_functioning_di`) | 1.0 | Participants' read of JGB market functioning (high − low) | BoJ, quarterly (Feb/May/Aug/Nov) | 2015– | Higher = more liquid (+1) | Seed (hand-entry) |
| Market | 10Y JGB bid-ask, normalized (`jgb_bid_ask`) | 0.75 | Tightness, in the style of the BoJ *Liquidity Indicators* | BoJ; monthly | 2005– | Wider = less liquid (−1) | Seed |
| Market | BoJ share of outstanding JGBs (`boj_jgb_share`) | 0.75 | Free float absorbed by the central bank | BoJ Flow of Funds / MoF; quarterly | 2005– | Higher = thinner float (−1) | Seed |
| Market | **Realized 10Y JGB volatility**, 12m std of monthly changes, bp (`jgb_10y_vol`) | 0.75 | Impaired liquidity / term-premium stress; the 2025 taper-slowdown trigger | **Computed from MoF yields**; monthly | **1987–** | Higher = less liquid (−1) | **Live** |
| Market | **10s30s slope**, 30Y − 10Y, pp (`jgb_10s30s`) | 0.5 | Super-long term-premium / fiscal-risk gauge | **Computed from MoF yields**; monthly | **1999–** | Steeper = more stress (−1) | **Live** |
| Market | Nikkei Volatility Index (`nikkei_vi`) | 0.5 | Implied equity volatility; spikes coincide with liquidity withdrawal | Nikkei; monthly | 2005– | Higher = less liquid (−1) | Seed |

**Relation to the review's shortlist.** Of the fourteen phase-1 items in `indicator_shortlist.csv`, the tracker implements eleven. Not yet implemented: the **GC repo − IOER spread** (#9), the **BoJ hard microstructure indicators** — futures bid-ask, price impact, turnover (#12) — and the **excess-reserves-to-bank-assets "ampleness ratio"** (#7, the Afonso et al. metric Shiratsuka 2025 applies to Japan). Phase-2 candidates — the **BIS credit-to-GDP gap** (Drehmann & Tsatsaronis 2014), a **Divisia / M1-share proxy** (Barnett et al. 2024), a **Japan proxy policy rate** on the SF Fed template (Choi, Doh, Foerster & Martinez 2022), and the **foreign share of JGB cash trading** — are not in the tracker. The ampleness ratio and repo−IOER spread are the omissions that matter most for the QT question (§7).

---

## 4. What's new in the research (2022–2026)

The literature review isolates five developments that change how monetary and liquidity conditions should be measured in Japan. Each has a direct design consequence for this tracker.

**4.1 The QT end-date and balance-sheet path are now known.** The BoJ's *Review of Monetary Policy from a Broad Perspective* (December 2024) closed the QQE era analytically — large-scale easing lifted real GDP by roughly +1.3 to +1.8% and inflation by about +0.6–0.7pp, and its yield-curve effect worked through the **stock** of holdings rather than the flow of purchases (Nakazawa & Osada, BoJ WP 24-E-10, 2024). The June 2025 interim assessment slowed the taper to −¥200bn/quarter from April 2026; the June 2026 assessment set a guideline of **~¥2tn/month from April 2027**, i.e. tapering ends in FY2027 (Tamura dissenting for Q1 2028). Total assets fell ¥67.6tn (−9.3%) in FY2025; JGB holdings fell from 91% of GDP to about 80% (IMF 2026 Article IV). The review flags the June 2026 current-account figure (¥407tn, −16.4% y/y) as **secondary-sourced — verify against BoJ MD08**. *Implication:* read the balance-sheet axis as a known, decelerating path; the stock effect means holdings of 49% of outstanding matter for term premia even after the flow stabilizes.

**4.2 Market functioning — not reserve scarcity — is the binding constraint on QT.** Shiratsuka (2025, *Toward a Guidepost for Quantitative Tightening: The Case of the Bank of Japan*, HIAS-E-146 / *Japanese Economic Review*) estimates Japan's reserve-demand curve on daily data to August 2025 and finds demand at IOER-eligible institutions satiated: current-account balances do not move the call rate, and when shrinkage would bite carries "considerable uncertainty." The Fed-side framework (Afonso, Giannone, La Spada & Williams, NY Fed SR 1019, 2022 rev. 2025) puts the abundant/ample threshold at roughly 12–13% of bank assets. The BoJ's *Market Operations in Fiscal 2025* (August 2026) reports TONA "extremely stable" just below IOER and GC repo rising toward it — a first mild sign of easing collateral scarcity. BoJ Review 2026-E-10 (August 2026, *Impact of the Bank of Japan's Reductions in JGB Purchases on the JGB Markets*) finds functioning "steadily improving" but the medium-to-long zone still tight. *Implication:* `call_policy_spread` is the regime switch — while it stays a few bp from target, falling reserves are *intended* QT progress; a drift through zero would reclassify the same series as stress. The missing ampleness ratio and repo−IOER spread are the priority additions.

**4.3 The "money view" is back, but regime-dependent.** Borio, Hofmann & Zakrajšek (2023, *Does money growth help explain the recent inflation surge?*, BIS Bulletin 67; updated in Borio's January 2024 speech) find the money–inflation link close to one-for-one when inflation is high and essentially absent when it is low. Berger, Karlsson & Österholm (2023, IMF WP 2023/137) is the caution: the relation is unstable and the post-pandemic episode largely reflects conventional shocks. Sokic (2025, *Bulletin of Economic Research*) reconciles them — strong at low frequencies, weak at business-cycle frequencies: money is a *medium-run* signal. Japan is the low-inflation regime par excellence (M2 +9–10% in 2020–21, modest lagged pass-through). *Implication:* with core CPI near 2%, money growth is *regaining* signal value, and +2.2% M2 is a disinflationary signal, not a monetary-overhang one.

**4.4 Long yields are being driven by term premia, not the expected policy path.** The IMF April 2026 *Global Financial Stability Report* (Ch. 1) attributes the rise in JGB yields to fiscal-risk term premia and flags spillovers through Japan's large net international investment position. The IMF 2026 Article IV notes foreign investors are now ~65% of monthly cash trading (12% in 2009) — better turnover, more news-sensitivity — and urges readiness for "exceptional targeted interventions." Cross-country evidence (Du, Forbes & Luzzetti, NBER WP 32321, 2024): QT raises yields and steepens curves, "more than paint drying, far less than reversing QE." *Implication — and why two series were added:* realized 10Y volatility (the variable that triggered the June 2025 taper slowdown after the 30-year spiked ~100bp to 3.2%) and the 10s30s slope are computed from the MoF curve, giving the market axis a live, long-history component independent of hand-entered survey data.

**4.5 The yen is an explicit monetary-conditions variable.** The classic MCI (Freedman 1995) always included the exchange rate; the Ericsson et al. (1998) critique — model-dependent weights, and an index that conflates shocks needing opposite responses — is why the review recommends showing the MCI as a range. What is new is practice: the July–August 2026 record ¥15.4tn intervention, with unusual US participation, treats the yen as a stance variable in its own right. *Implication:* the FX axis is scored separately rather than folded into the real-rate leg with fixed weights; a stronger yen after intervention tightens the MCI with rates unchanged.

Two cross-cutting points shape the reading throughout: **horizons differ by group** (money leads inflation by 12–24 months; funding spreads lead financial conditions by weeks; market liquidity is near-contemporaneous with policy reaction), and **the sign of "good news" is not uniform** — falling excess reserves are intended progress until the reserve-demand curve steepens.

---

## 5. Time series of the key indicators

The composites run from 1974 (MCI) and 1987 (LCI), but the full seven-axis framework is populated only from 2005; pre-2005 readings are single-axis context, not comparable composite values.

**Pre-QQE and the 2006 exit (2005–2012).** The tracker's QE-exit precedent is 2006: monetary base −20.5% y/y and current accounts −40.2% at the June 2006 trough, central-bank-liquidity axis **−1.80** and balance-sheet axis **−1.84** (March 2006) — still the most restrictive quantity readings in the series; today's are the second-most. The GFC shows what a *funding* crisis looks like: October 2008 saw TIBOR–OIS at **0.57pp** (peak 0.60pp, Dec-2008), the call–target spread at **0.15pp** (series maximum), the dollar basis at **−109bp**, Nikkei VI at **70.6**; funding axis **−2.99**, LCI **−1.37**, MLCI **−0.74**. Monetary conditions were meanwhile *tight* on the yen: REER **120.7** (October 2011), USD/JPY **76.6**, FX axis **−1.50** (December 2012), the tightest in its history.

**QQE (April 2013) and the peak of quantity easing.** QQE is the largest event in the liquidity series. Monetary base growth went from +20% (Dec-2012) to **+46.4% y/y** (Dec-2013, series maximum), current-account balances **+100%**, BoJ assets +37.5% (peaking at +45.2% in June 2014). The central-bank-liquidity axis hit **+2.98** and the LCI **+1.29** in December 2013 — both maxima — and the MLCI its all-time high of **+1.07**. The yen moved from 84 to 103 and the REER from 112 to 86 over 2013, taking the FX axis from −1.50 to −0.05 and on to +0.49 by end-2014. Realized 10Y volatility spiked to **11.6bp** in December 2013 before subsiding. The consumption-tax pass-through pushed the ex-post real policy rate to **−2.52%** (Dec-2013) and the real-rate axis to +1.54, then back to −0.11 a year later — ex-post real rates are noisy around tax events.

**NIRP and YCC (2016) to the pandemic.** After the January 2016 move to −0.1%, the call–target spread went negative (**−2.4bp**, May 2016, series minimum). YCC made the quantity flow irrelevant while the stock kept rising: base growth fell from +28% (Jan-2016) to +5% (Dec-2019) and the balance-sheet axis from +1.44 to −0.05, but the BoJ's JGB share climbed from 34% to 43%. The Bond Market Survey DI, **+1** at its March 2015 start, fell steadily to **−27** by end-2019 — functioning deteriorating under YCC even in calm conditions (Fukuma et al., BoJ WP 24-E-9). Realized volatility hit its all-time low of **2.4bp** (September 2018). Funding was the weak spot: the dollar basis widened to **−129bp** (Dec-2019) and **−138bp** (Mar-2020, series minimum), taking the funding axis to −0.87 and the LCI to −0.42. The pandemic briefly re-expanded quantity (base +17.8%, M2 **+9.2%** — its maximum — money & credit axis **+2.55**, Dec-2020); the money surge then faded with only modest inflation pass-through, as the BIS regime model predicts for a low-inflation economy.

**The 2022–23 YCC stress — the market-liquidity trough.** Defending the 10Y cap against rising global yields pushed the BoJ share of outstanding JGBs to its maximum of **53.1%** (June 2023), the functioning DI to **−64** (March 2023), the bid-ask proxy to **2.57** (February 2023) and the market axis to **−1.17**; the LCI reached −0.43. Monetary conditions were simultaneously at their *easiest* on the price of money: core CPI at 3.2% against a −0.1% policy rate gave an ex-post real policy rate of **−3.90%** (January 2023, series minimum), a real-rate axis of **+1.84** (June 2023) and, with the REER at 67 and USD/JPY at 141, an FX axis of +1.36; the MCI at **+0.66** is the post-2013 high. This is when the §7 divergence first opened: rates and the yen maximally easy, liquidity impaired by the instrument used to keep them so.

**Exit and taper (March 2024–).** NIRP and YCC ended in March 2024; purchase reduction began August 2024. Base growth turned negative in mid-2024, reached −4.4% by March 2025, **−9.95%** by December 2025 and **−13.1%** now; current accounts followed (−3.9% → −5.9% → −10.6% → −14.5%). BoJ assets went from +1.0% (Mar-2024) to −7.2% (Dec-2025) and **−8.2%** (Sep-2026), consistent with the −9.3% FY2025 decline in the BoJ Accounts. The quantity axes fell almost linearly: central-bank liquidity −0.62 → −1.14 → **−1.33**; balance sheet −0.64 → −1.19 → **−1.26**. Market functioning improved in step: DI −29 (Mar-2024) → −18 (Mar-2025); BoJ share 53.1% → 51.0%. The real-rate axis stayed near +1.5 through 2024–25 because core CPI (2.6–3.6%) ran far above a 0.25–0.5% policy rate.

**The 2025–26 super-long sell-off, the December and June hikes, and intervention.** The super-long zone is where the taper met fiscal-risk term premia. The 10s30s slope, 1.02pp in March 2025, widened to **1.39pp** by June 2025 (the taper-slowdown trigger) and a series maximum of **1.47pp** in October 2025; realized volatility rose from 9.7bp to 11.6bp. The DI slipped from −18 back to **−26 (Mar-2026)** — taper and sell-off pulling in opposite directions. The 10Y rose from 1.49% (Mar-2025) to 2.06% (Dec-2025), 2.67% (Jun-2026) and **2.95%** (Sep-2026), the highest since 1996; the 30Y is 4.04%. The December 2025 hike to 0.75% coincided with a temporary collapse in core CPI to 0.45%: the ex-post real policy rate briefly turned positive (+0.30%) and the real-rate axis printed **−0.19**, its only restrictive reading since 2021, before CPI recovered to 1.5–1.8%. The June 2026 hike to 1.00% put the ex-post real policy rate at **−0.53%** and the axis at +0.28–0.33. USD/JPY hit its series maximum of **162.3** in July 2026 and fell back to **158.8** in August on the ¥15.4tn intervention; the REER, 61.6 at its June 2024 trough, is 63.6. Over the last six months the market axis has swung from 0.00 to **+0.40** — DI −26 → −14, volatility 13.7 → 10.2bp, 10s30s 1.13 → 1.09pp, Nikkei VI 27.7 → 20.6 — and the LCI has risen from −0.28 to **−0.17**.

**Seed vs live, and what it means for confidence.** Money (M2/M3), BoJ assets, REER, USD/JPY, the JGB curve and the two computed market-stress series are live. The monetary base, current accounts, bank lending, money-market spreads, functioning DI, bid-ask, BoJ share and Nikkei VI are seed: their *recent* values are anchored to verified observations (the review's June 2026 base −13.7% and May 2026 DI of −16 are within a point or two of the tracker's −13.1% and −14) but their **historical shapes are illustrative** — correct in sign and approximate magnitude at the QQE, GFC and YCC turning points, not quotable to two decimals. The live series carry the market-functioning conclusion largely on their own: realized volatility and the 10s30s slope both show the 2025–26 stress peaking in Q4 2025 and easing since.

---

## 6. Current assessment by axis

### 6.1 Scorecard

| Axis | Index | Score | Assessment | Direction | Evidence (latest) |
|---|---|---:|---|---|---|
| Real short-rate stance | MCI | **+0.33** | Mildly accommodative | ▼ tightening (−0.19) | Real policy rate −0.53% (Jun), real 1Y −0.59% (Jul); core CPI 1.79% |
| Money & credit aggregates | MCI | **+0.23** | Mildly accommodative | → stable (+0.02) | M2 +2.18% (−0.67), M3 +1.73% (−0.85), bank lending +5.72% (+1.67) |
| Exchange rate (MCI) | MCI | **+1.79** | Accommodative | → stable (−0.02) | REER 63.6 (2020=100; +1.57), USD/JPY 158.8 (+2.22) |
| BoJ balance-sheet stance | MCI | **−1.26** | Restrictive | → stable (+0.06) | Total assets −8.24% y/y |
| Central-bank liquidity | LCI | **−1.33** | Restrictive | → stable (−0.06) | Monetary base −13.08% (−1.51), current accounts −14.53% (−1.15) |
| Funding liquidity | LCI | **+0.42** | Mildly accommodative | → stable (−0.02) | Call − target 1.4bp (+0.18), TIBOR–OIS 0.19pp (+0.13), basis −29.7bp (+1.13) |
| Market liquidity | LCI | **+0.40** | Mildly accommodative | ▲ easing (+0.40) | DI −14 (+0.98), bid-ask 1.29 (+1.24), BoJ share 48.9% (−1.12), 10Y vol 10.2bp (+0.30), 10s30s 1.09pp (−0.94), Nikkei VI 20.6 (+1.73) |
| **MCI** | — | **+0.27** | **Mildly accommodative** | → stable (−0.03) | Equal-weight mean of four axes |
| **LCI** | — | **−0.17** | **Mildly restrictive** | ▲ easing (+0.11) | Equal-weight mean of three axes |
| **MLCI** | — | **+0.05** | **Broadly neutral** | → stable (+0.04) | Average of MCI and LCI |

### 6.2 Axis commentary

**Real short-rate stance (+0.33, ▼).** The ex-post real policy rate (−0.53%) and real 1Y rate (−0.59%) are negative and score accommodative against a 1974-based history whose mean is +0.67%. But the direction is unambiguous: the axis has fallen from +1.84 (June 2023) and +1.41 (September 2025) as five hikes lifted the nominal rate from −0.1% to 1.00% while core CPI slipped from 3.6% (May 2025) to 1.8%. This is the one monetary axis where policy is visibly doing its work. Two caveats: ex-post real rates are noisy around tax and subsidy events (December 2025); and on a 2005+ window the real 1Y rate reads broadly neutral (z ≈ 0), on 2013+ mildly restrictive (≈ −0.5) — the deflation-era-baseline effect set out in the companion report. The long-history read is the fair one: *still mildly easy, tightening*.

**Money & credit aggregates (+0.23, →).** A composite of opposites. M2 (+2.2%) and M3 (+1.7%) score restrictive — M2 is below its 2005+ mean of 3.1% and the ~3–4% nominal GDP growth the review cites — while bank lending at +5.7% is the fastest sustained pace since the 2020 surge (maximum 6.3%, June 2020) and scores +1.67. The review's diagnosis: deposit creation is being offset by portfolio shifts into investment trusts and by QT, so weak M2 means money is being *diverted*, not that credit demand is weak. On the BIS regime reading this is a disinflationary signal; there is no monetary-overhang case for Japanese inflation. The Divisia caveat cuts the same way: with time deposits repricing toward 1%, simple-sum M2 overstates transactions money.

**Exchange rate (+1.79, →).** The easiest axis, and the one most exposed to the Ericsson et al. critique. The REER at 63.6 is within two points of its June 2024 record low (61.6) and 1.6 standard deviations below its 2005+ mean of 88; USD/JPY at 158.8 is 2.2 standard deviations above its mean. The yen is providing more stimulus than at any point in the QQE era, when the FX axis never exceeded +0.5. The review's judgement that the yen has been the single most important swing factor in the 2022–26 inflation episode turns this into a policy variable: the ¥15.4tn July–August intervention pulled USD/JPY from 162.3 to 158.8 but barely dented the axis (+1.83 → +1.79). Weight it as the review advises: a stimulus the BoJ does not control and that reverses on global-rate and risk shocks.

**BoJ balance-sheet stance (−1.26, →).** Total assets −8.2% y/y is the second-deepest contraction in the series after 2006 (−19.8%). Direction is stable because the y/y rate has plateaued at −8 to −9% since March 2026; the taper path implies it stays negative but decelerates as purchases approach ~¥2tn/month. The stock effect (Nakazawa & Osada 2024) means term-premium suppression keeps unwinding even at a stable flow: holdings of 49% of outstanding remain far above any pre-2013 level (8% in 2005, 11% in March 2013).

**Central-bank liquidity (−1.33, →).** The most restrictive axis. Monetary base −13.1% and current accounts −14.5% are each more than one standard deviation below their means and the second-most negative readings after 2006. Per §4.2 this is *intended* — QT is supposed to look like this — and the axis is restrictive only in the quantity sense; whether it becomes restrictive in the *price* sense is the funding axis's question, and so far the answer is no. The tracker does not yet compute the ampleness ratio that would say how far the system is from the steep part of the reserve-demand curve.

**Funding liquidity (+0.42, →).** Orderly. TONA is 1.4bp from target (the spread's ▼ direction reflects a drift from ~1bp — within noise, but worth noting); 3m TIBOR–OIS at 0.19pp is at its 2005+ mean (0.21pp) and under a third of its GFC peak; the dollar basis at −30bp is well inside its −58bp average and its −138bp March 2020 extreme. This matches the review's reading of *Market Operations in FY2025* — regional banks arbitraging IOER in an active call market, GC repo drifting toward IOER as collateral scarcity eases. The caveat: all three members are seed, so the axis says "no stress in the anchoring observations," not "no stress in a verified daily history."

**Market liquidity (+0.40, ▲).** The most improved axis (+0.40 over six months) and the most internally divided. The functioning DI at −14 scores +0.98 — but only because its 2015+ history averages −27; in absolute terms a negative DI still means more respondents see functioning as "low" than "high." The bid-ask proxy (1.29, near 2015 levels), Nikkei VI (20.6, near its minimum of 18.3) and realized volatility (10.2bp) score accommodative; the BoJ share (48.9%, −1.12) and the 10s30s slope (1.09pp vs a 0.88pp long-run mean, −0.94) score restrictive — the float is still thin and the super-long premium elevated. Realized volatility carries a baseline caveat: +0.30 is against a 1987-based history that includes the 40–55bp months of 1987–90; on 2005+ the same 10.2bp reads −0.61, on 2013+ −0.97. *Volatility is still high by post-2005 standards but falling fast* — direction is the more reliable signal than level.

---

## 7. Implications for growth, inflation and policy conduct

### 7.1 The central argument: quantity is tightening, price is easy

The headline MLCI of +0.05 hides the framework's most important message. The two axes that measure the **quantity** of central-bank money — balance sheet (−1.26) and central-bank liquidity (−1.33) — are both restrictive, at their second-most negative readings in two decades, and moving in step with a pre-announced QT path. The axes that measure the **price** of money and its counterparts — real short rate (+0.33), credit (+1.67 within the money & credit axis), the yen (+1.79) — remain easy, and funding liquidity (+0.42) shows the quantity withdrawal has not yet raised the price of reserves or bank funding at all.

Why can both be true? Because, per Shiratsuka (2025) and Afonso et al., reserves are still satiated: the BoJ can withdraw base money without the call rate moving, so the *quantity* contraction has no *price* consequence in money markets. Its price consequences show up further out the curve — via the stock effect on term premia (Nakazawa & Osada 2024), the mechanism behind a 10Y at 2.95% and a 30Y at 4.04% with the policy rate at 1.00%. That is a tightening of long-term *financial* conditions, not of the money-market *monetary* stance, and the companion report duly shows funding costs as the FCI's only restrictive axis.

The divergence is sustainable while three things hold: (i) the call–target spread stays pinned (reserves satiated); (ii) market functioning keeps improving as the BoJ hands float back (the DI trend); and (iii) the yen and credit continue to offset the quantity withdrawal in aggregate demand terms. It becomes a problem if any breaks — a repo or call-rate drift would mean QT has hit the steep part of the demand curve; a renewed super-long sell-off would mean the market cannot absorb the float; a sharp yen appreciation would remove the largest single source of accommodation in the MCI.

### 7.2 Implications matrix

| Condition group (axis) | Growth | Inflation | Monetary-policy conduct |
|---|---|---|---|
| **Real short-rate stance** (+0.33 ▼) | Real short rates still negative; on the companion tracker the real policy rate is 0.62pp below the r\* midpoint, so demand support persists. Each 25bp hike closes roughly a quarter of the gap. | The stance is not yet disinflationary in level terms; the *change* since 2025 is. | Supports continued gradual hikes (markets price 1.25% for 17–18 Sep 2026 per the review); the ex-post real rate's noise around subsidies argues for reading it alongside the ex-ante measure. |
| **Money & credit** (+0.23 →) | Lending at +5.7% signals firm capex and real-estate demand; weak M2 reflects diversion into investment trusts, not weak demand. | BIS regime message: with inflation near 2%, money regains signal value, and +2.2% M2 is a *disinflationary* signal. A re-acceleration above ~4% would be an upside-risk flag. | No monetary-overhang case for faster hikes; credit gap near zero (review, unverified latest value) gives no macroprudential reason either. |
| **Exchange rate** (+1.79 →) | Weak REER supports exporters and profits; the largest single stimulus in the MCI. | The fastest inflation channel — import prices; the 2026 oil shock plus a weak yen is why the BoJ's Outlook projects core CPI "clearly above" 2% (tracker: 1.8% realized). | The MCI separates what the yen has already done from what rates must do; intervention (¥15.4tn Jul–Aug) is being used as a stance instrument alongside hikes. Yen strength tightens the MCI without a hike. |
| **BoJ balance sheet** (−1.26 →) | Stock-effect literature implies the ~¥100tn/yr run-off adds to term premia gradually; Du–Forbes–Luzzetti: modest, front-loaded yield effect. | Little direct inflation effect once rates are positive; indirect via the yen if higher term premia attract inflows. | QT path is known to FY2027; the tracker should show the "hold-to-run-off gap." The review reads the Broad Review as ruling out a return of NIRP/YCC/ETFs — the reversal instrument would be a QT pause. |
| **Central-bank liquidity** (−1.33 →) | None directly while reserves are satiated. | None directly. | Restrictive in quantity, not price. The binding constraint on QT pace is market functioning, not reserves (Shiratsuka; BoJ 2026-E-10). The missing ampleness ratio is the guidepost. |
| **Funding liquidity** (+0.42 →) | Funding stress transmits to lending spreads within weeks; currently negligible. | Indirect. | Rate control (IOER floor) is working. A drift in call−target or repo−IOER toward zero would argue for slower QT or a new floor design; a wider year-end 2026 dollar basis (the $550bn US–Japan investment deal is expected to widen the 5–10Y basis) would test USD swap-line readiness. |
| **Market liquidity** (+0.40 ▲) | Super-long stress raises long-term borrowing costs for insurers/pensions and, via the curve, mortgage and corporate rates. | Term-premium yield rises are not a demand-management tightening but do tighten financial conditions; the BoJ treats them as partly fundamental. | The group the BoJ ties explicitly to its purchase plan. On the 2025 precedent, a DI back below ~−30 or a realized-volatility spike would trigger taper flexibility or targeted purchases, as the IMF recommends. Financial-stability relevance: foreign share of trading (~65%) makes the market more news-sensitive. |

### 7.3 Policy-conduct synthesis

*Rate path.* The price-side monetary axes (real rate +0.33, FX +1.79) are consistent with further gradual normalization; money & credit is consistent with, but does not demand, it. Nothing here argues for a faster pace than the companion report's "one or two further 25bp steps."

*QT pace and rate control.* Nothing argues for slowing QT *today*: funding is orderly, market liquidity improving, the IOER floor functioning, and Shiratsuka's satiation result says reserves are not close to scarce. The tracker cannot yet say *how far* from scarce — hence the priority on the ampleness ratio and repo−IOER spread. The case for *ending* tapering in FY2027 rather than 2028 (Tamura's dissent) rests on a BoJ share still at 49% and a 10s30s slope still restrictive.

*FX intervention.* Working at the margin (USD/JPY 162 → 159) but not changing the stance (FX axis +1.83 → +1.79); only a narrowing rate differential moves the axis durably.

*Financial stability.* The stress points are the super-long zone and the market's dependence on foreign liquidity providers, not bank funding; tripwires in §9.

---

## 8. Interaction with the Financial Conditions tracker

The two trackers should agree on sign and disagree on magnitude, and they do.

| Lens | Read | What it captures |
|---|---|---|
| Natural-rate (companion) | Real policy rate (ex-ante) −0.98% vs r\* band −0.94% / −0.36% / +0.53%; 0.62pp below the midpoint → **accommodative** | Where the short rate sits relative to neutral |
| Financial conditions (companion) | FCI **+1.08** (▲ easing); Stage 1 +0.41; funding costs −0.82 restrictive; availability +1.07; asset prices +2.87; volumes +1.20 | What firms and households face |
| Monetary conditions (this tracker) | MCI **+0.27** → stable; rates +0.33, money & credit +0.23, FX +1.79, balance sheet −1.26 | What the BoJ has set, and the money/credit it generates |
| Liquidity conditions (this tracker) | LCI **−0.17** ▲ easing; CB liquidity −1.33, funding +0.42, market +0.40 | Whether the plumbing works, and at what price |

**Reconciliation.** The FCI is far easier (+1.08) than the MCI (+0.27) because its Stage 2 is dominated by asset prices (+2.87) and volumes (+1.20) — the *outcomes* of easy money and a weak yen — while the MCI nets those same inputs against a restrictive balance sheet. Strip the balance-sheet axis out and the remaining three MCI axes average +0.78. The trackers share bank lending (+5.7% y/y; +1.67 here, the core of the FCI's volumes axis) and USD/JPY (+2.22 here, +2.16 there); they differ on the 1Y ex-post real rate, which the ML build scores +0.53 and the FC build −0.01 for the same −0.59% value — a scoring-vintage discrepancy to reconcile in the next ETL cycle, and a reminder that the *sign* of the real-rate read is robust while the magnitude is not.

**Why the FCI's funding-cost axis is restrictive when the LCI's funding axis is easy.** They measure different things: the FCI's funding costs are lending and CP *rates* (1.17%, 1.11%) — the risk-free base repricing; the LCI's funding liquidity is *spreads* over that base (TIBOR–OIS 0.19pp, basis −30bp), which are calm. Higher rates with calm spreads is what orderly normalization looks like; the companion's 0.31% corporate-bond spread confirms it from the credit side.

**Where the lenses meet.** The natural-rate lens says the short rate is 0.62pp below neutral; the money & credit axis says credit is strong but money weak; the FX axis says the yen is doing more of the accommodating than the rate. The FCI's +1.08 is the outcome; the MCI's +0.27 and LCI's −0.17 explain how it is produced and where the stress sits — a BoJ normalizing the *rate* into an economy whose *credit* and *yen* are still easy and whose *long yields* are set by term premia it no longer controls.

---

## 9. Risks & watchlist

| Watch | Tracker indicator(s) | Current | Trigger to worry | Why (literature) |
|---|---|---|---|---|
| Reserve scarcity / loss of rate control | `call_policy_spread`; (add) GC repo − IOER, excess reserves / bank assets | +1.4bp; repo just below IOER (review) | Call−target rising through **+5bp** and holding; repo−IOER turning positive; ampleness ratio approaching **12–13%** of bank assets | Afonso et al. (2022/25); Shiratsuka (2025) — the switch from "intended QT" to "stress" |
| Super-long sell-off resumes | `jgb_10s30s`, `jgb_10y_vol`, `jgb_market_functioning_di` | 1.09pp; 10.2bp; −14 | 10s30s back above **1.4pp** (Oct-2025 max 1.47); 12m realized vol above **13bp**; DI falling back below **−30** | June 2025 precedent (taper slowdown); IMF Art. IV "exceptional targeted interventions"; BoJ 2026-E-10 |
| Term-premium spillover to financial conditions | `jgb_10y` (2.95%), 30Y (4.04%), companion `real_10y_xp` | 10Y highest since 1996 | 10Y through **3.25%** with 10s30s widening rather than flattening (term premium, not expectations) | IMF GFSR Apr-2026; Du, Forbes & Luzzetti (2024) |
| Dollar-funding stress | `jpy_basis_3m`; (add) BoJ USD-ops take-up | −30bp | Basis wider than **−60bp** (its 2005+ mean) outside year-end; BoJ USD operations drawn | Borio et al. (2016); FSR Apr-2026; $550bn deal widening 5–10Y basis |
| Bank term-funding stress | `tibor_ois_3m` | 0.19pp | Above **0.35pp** (≈ +1σ) | GFC peak 0.60pp |
| Yen reversal removes the largest stimulus | `reer`, `usdjpy` | 63.6; 158.8 | REER above **72** / USD/JPY below **140** would take the FX axis from +1.8 toward +1.0 — a material MCI tightening with no hike | Ericsson et al. (1998): FX shocks need different responses depending on source |
| Money re-acceleration (inflation upside) | `m2_yoy`, `m3_yoy` | +2.2%; +1.7% | M2 above **~4%** with core CPI above 2% — the regime in which money regains signal value | Borio, Hofmann & Zakrajšek (2023) |
| Credit overheating | `bank_lending_yoy`; (add) BIS credit-to-GDP gap | +5.7% | Lending above **6.5%** (past the 2020 peak) with the credit gap turning positive | Drehmann & Tsatsaronis (2014); FSR heat map |
| Real-rate stance flips restrictive | `real_policy_rate_xp`, `real_1y_xp` | −0.53%; −0.59% | Ex-post real policy rate sustainably **above 0** while core CPI is at/below 2% — the axis would read restrictive on all baselines | Companion report §4.1; BoJ Review 2026-E-4 |
| Seed-data risk | All BoJ-only series | — | Ingested BoJ CSVs diverging materially from seed anchors (e.g. CAB −16.4% vs tracker −14.5%) | Review §7 verification notes |

---

## 10. Methodology & data note

**The tracker.** Official-source and mirrored time series are assembled into seven axes under two indices in the same ETL/SQLite pipeline as the financial-conditions tracker; `web/data_ml.json` is its published snapshot (`meta.latest_date` 2026-09-30; generated 2026-09-10T07:25 UTC).

**Scoring.** Each indicator → accommodation score = z-score × polarity, so **+ = easier / more liquid**. Axis = `ml_weight`-weighted mean of members. MCI = equal-weight mean of its four axes; LCI = equal-weight mean of its three; MLCI = average of MCI and LCI. Direction = trailing 6-month change in score, labelled ▲/▼/→ (thresholds as in the companion tracker). Labels: |score| < 0.2 broadly neutral; 0.2–0.5 mildly; 0.5–1.0 accommodative/restrictive; the largest magnitudes (FX +1.79, CB liquidity −1.33) are "accommodative"/"restrictive" without qualifier.

**Weights (`series[*].ml_weight`).** Real policy rate 1.0, real 1Y 1.0 · M2 1.0, M3 0.5, bank lending 1.0 · REER 1.0, USD/JPY 0.5 · BoJ assets 1.0 · monetary base 1.0, current accounts 1.0 · call−target 1.0, TIBOR–OIS 1.0, basis 0.75 · functioning DI 1.0, bid-ask 0.75, BoJ share 0.75, 10Y realized vol 0.75, 10s30s 0.5, Nikkei VI 0.5. Weights reflect the review's ranking: official/primary gauges at 1.0, proxies and globally driven series lower.

**Baseline: longest available history, and why.** Every indicator is z-scored over its **full available history** (`series[*].history_start`): real 1Y from 1974, realized volatility from 1987, 10s30s from 1999, real policy rate and USD/JPY from 2004, most others from 2005, functioning DI from 2015 — following the companion report's finding that a 2005+ (ZIRP/NIRP-dominated) window biases real-rate reads toward "restrictive." The cost is heterogeneity: a 1987-based volatility baseline makes today's 10bp look mild (2005+ and 2013+ alternatives: −0.61, −0.97); a 2015-based DI baseline averaging −27 makes a still-negative −14 look accommodative. Where the baseline changes the verdict this report says so; direction of travel is baseline-invariant and the more reliable signal. The MCI is the real-rate axis alone before 2004 and the LCI realized volatility alone before 2005; pre-2005 composite values are context only.

**Live vs seed status (`meta.source_note`).** *Live:* M2, M3, BoJ total assets, REER (FRED mirrors), policy rate, USD/JPY, JGB yields (MoF), core CPI (e-Stat), and the two series computed from MoF yields (10Y realized volatility, 10s30s). *Seed (illustrative, anchored to recent verified observations):* monetary base, current-account balances, bank lending, call−target spread, TIBOR–OIS, USD/JPY basis, functioning DI, bid-ask, BoJ JGB share, Nikkei VI — BoJ-only or licensed series awaiting ingestion via the BoJ Time-Series Data Search API. The review flags as **unverified at source**: the May 2026 survey DI (−16), the June 2026 current-account balance (¥407tn, −16.4% y/y) and the FRED IDs `RBJPBIS`, `MANMM101JPM189S`, `QJPPAM770A`; the August 2026 Bond Market Survey (released 1 September) should be hand-entered.

**Known gaps and next steps.** (1) Excess reserves / bank assets (ampleness ratio) and GC repo − IOER — the QT guideposts. (2) BoJ hard microstructure series (futures bid-ask, price impact, turnover). (3) Phase-2: BIS credit-to-GDP gap, M1/M2 Divisia proxy, Japan proxy policy rate, foreign trading share. (4) Reconcile the 1Y ex-post real-rate score between the two trackers. (5) Show the MCI's FX/rate weighting as a range, per Ericsson et al.

**Research basis (full citations).** Team literature review, *Japan Monetary & Liquidity Conditions: Literature and Indicator Review*, 10 September 2026. Key references: Freedman (1995), *Bank of Canada Review*; Ericsson, Jansen, Kerbeshian & Nymoen (1998), BIS Conference Papers 6; Borio, Hofmann & Zakrajšek (2023), BIS Bulletin 67; Berger, Karlsson & Österholm (2023), IMF WP 2023/137; Sokic (2025), *Bulletin of Economic Research*; Bank of Japan (2024), *Review of Monetary Policy from a Broad Perspective*; Nakazawa & Osada (2024), BoJ WP 24-E-10; Fukuma, Kitamura, Maehashi, Matsuda, Takemura & Watanabe (2024), BoJ WP 24-E-9; Bank of Japan (2026), BoJ Review 2026-E-10; Bank of Japan (2026), *Market Operations in Fiscal 2025*; Bank of Japan (2026), *Financial System Report*, April; Afonso, Giannone, La Spada & Williams (2022, rev. 2025), NY Fed Staff Report 1019; Shiratsuka (2025), HIAS-E-146 / *Japanese Economic Review*; Borio, McCauley, McGuire & Sushko (2016), BIS Quarterly Review; Aldasoro & Ehlers (2018), BIS Quarterly Review; IMF (2026), *Global Financial Stability Report*, April, Ch. 1; IMF (2026), Japan Article IV, Country Report 26/75; Du, Forbes & Luzzetti (2024), NBER WP 32321; Choi, Doh, Foerster & Martinez (2022), FRBSF Economic Letter 2022-30; Drehmann & Tsatsaronis (2014), BIS Quarterly Review; Kurosaki, Kumano, Okabe & Nagano (2015), BoJ WP 15-E-2; Sakiyama & Kobayashi (2018), BoJ Research Paper; Barnett, Chauvet, Leiva-Leon & Su (2024), *JMCB*; Carriere-Swallow, Kindberg-Hanlon & Smirnov (2025), IMF WP 2025/227. Companion framework: Bank of Japan (2026), BoJ Review 2026-E-4.

---

## Bottom-line verdict

**Japan's monetary and liquidity conditions are neutral on average and divergent underneath. Monetary conditions are mildly accommodative (MCI +0.27) because the price of money is still easy — an ex-post real policy rate of −0.53%, bank lending growing 5.7%, and a real effective yen near a record low (REER 63.6) that is supplying more stimulus than QQE ever did through this channel — even as the BoJ's balance sheet contracts 8% a year. Liquidity conditions are mildly restrictive (LCI −0.17) for one reason only: the quantity of central-bank money is being withdrawn at a pace (monetary base −13.1%, current accounts −14.5%) exceeded only at the 2006 exit. That withdrawal has not touched the price of reserves or bank funding — TONA is pinned, TIBOR–OIS and the dollar basis are calm — and JGB market functioning is repairing faster than at any point since YCC ended (DI −64 → −14; realized volatility and the 10s30s slope both off their late-2025 peaks). The divergence is what a well-sequenced exit should look like, and it is sustainable while reserves remain satiated, the market keeps absorbing the float, and the yen stays weak. Its fault lines are visible in the tracker: a BoJ share still at 49%, a super-long slope still restrictive, a market now reliant on foreign liquidity, and seed-status money-market data that cannot yet say how far the system is from the steep part of the reserve-demand curve. Read with the companion tracker, the picture is of a central bank normalizing the rate into an economy whose credit and currency are still easy, whose long yields are set by term premia it no longer controls, and whose liquidity plumbing is — so far — holding.**
