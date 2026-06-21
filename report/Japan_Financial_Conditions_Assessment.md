# Japan's Financial Conditions — Assessment Report

**Framework:** Bank of Japan two-stage assessment of financial conditions and the natural rate of interest
**Source paper:** BoJ Review 2026-E-4, *"Developments in the Natural Rate of Interest and the Assessment of the Degree of Monetary Accommodation"*, Monetary Affairs Department, March 2026
**Data:** Japan Financial Conditions Tracker (`web/data.json`), snapshot dated **2026-06-30**, generated 2026-06-20
**Policy context:** BoJ policy rate raised to **1.00%** on 16 June 2026 — the highest since 1995
**Prepared for:** investment professionals and policymakers

> **Important labelling caveat.** The composite Financial Conditions Index (FCI) discussed below is an *analytical synthesis* built on the axes of the BoJ's framework — a z-score composite assembled by this tracker. It is **not** an official BoJ index, and the BoJ publishes no single headline FCI. Where this report quotes "the BoJ's own read," that refers to the qualitative comprehensive judgment in BoJ Review 2026-E-4; where it quotes a numerical score, that is the tracker's synthetic measure. The current data run is in **SEED mode** (illustrative approximations anchored to recent observations); see the Methodology note.

---

## 1. Executive summary

- **Conditions remain accommodative despite three hikes.** After raising the uncollateralized overnight call rate from 0.25% (Dec 2024) to 0.50% (Jan 2025), 0.75% (Dec 2025) and **1.00% (16 June 2026)**, the tracker's composite FCI reads **+0.69**, squarely in *accommodative* territory relative to its 2005-onward history. This mirrors the BoJ's qualitative conclusion that "Japan's financial conditions have remained accommodative even after the policy interest rate hike."

- **Both lenses point the same way — accommodation — but with caveats.** On the **natural-rate lens**, the real policy rate is about **−0.98%**, roughly **0.83pp below** the midpoint of the six-model natural-rate band (midpoint −0.15%; band **−0.85% to +0.55%**). On the **financial-conditions lens**, four of five framework axes read accommodative. The two lenses corroborate each other, which raises confidence in the *direction* of the read even where the *magnitude* is uncertain.

- **The accommodation is narrowing, not vanishing.** The FCI has drifted down steadily — +1.01 (Dec 2024) → +0.88 (Jun 2025) → +0.82 (Dec 2025) → +0.75 (Mar 2026) → **+0.69 (Jun 2026)** — and the synthetic real-rate gap has closed from about −1.61 to **−0.83**. Transmission is working at the margin, but slowly.

- **Funding costs are the one tightening axis; everything else stays easy.** The funding-costs axis is **restrictive (−0.89)** as lending and CP rates climb with the policy rate. But availability (**+1.09**), asset prices (**+2.74**), and funding volumes (**+0.55**) remain clearly accommodative, and the real-rate axis is **broadly neutral (−0.04)**.

- **The key nuance is in the real-rate curve.** Short and medium real rates are still **negative** (1Y real **−1.03%**, 3Y real **−0.38%**) — the maturities that matter most for activity — while the **long-end real rate has turned clearly positive (10Y real +0.87%)** as JGBs sold off. Accommodation is concentrated at the front end, where it bites on spending; the back end is already restrictive.

- **Near-term scope for further gradual hikes exists, but is bounded.** With the real policy rate below the neutral midpoint and conditions still easy, the data are *consistent with* continued, data-dependent normalization toward the **lower end** of the neutral band. The binding constraints are the fast-rising long-end real rate / JGB term premium, a **weak yen (USD/JPY ~161)**, U.S./global spillovers to Japan's r*, SME and high-debt-sector stress, and the wide r* uncertainty itself.

- **Bottom line up front.** Japan's financial conditions are still accommodative at a 1.00% policy rate; the degree of accommodation is shrinking but real and material; further gradual tightening is supportable on the data but must be calibrated with "considerable latitude" given r* uncertainty and the rapidly stiffening long end.

---

## 2. The BoJ framework: comprehensive judgment, not a mechanical r\*

### 2.1 Why the natural rate alone is insufficient

The natural (or neutral) rate of interest, **r\***, is the real short-term rate that is neutral to economic activity and prices — neither stimulating nor restraining. In principle, comparing the prevailing real rate to r\* tells you whether policy is accommodative or restrictive. In practice, the BoJ — like the Federal Reserve, ECB, and Bank of England — declines to use r\* as a mechanical or direct policy trigger, for three reasons set out in BoJ Review 2026-E-4:

1. **Dispersion, estimation error, and revision.** The BoJ estimates r\* with **six models** — two time-series (Del Negro et al. 2017; Goy–Iwasaki 2024) and four structural (Holston–Laubach–Williams 2023; Imakubo–Kojima–Nakajima 2015; Nakajima et al. 2023; Okazaki–Sudo 2018). As of **2025/Q3** the range spanned roughly **−0.9% to +0.5%** (after the December 2025 GDP benchmark revision; it was −1.0% to +0.5% as of 2023/Q1). A band that wide, compounded by real-time-vs-ex-post revisions, cannot pin down a precise trigger.

2. **Open-economy under-capture.** With free capital mobility, overseas — especially U.S. — developments influence Japan's r\*. The models under-capture this, so a domestically-estimated r\* can drift relative to the rate the open economy actually faces.

3. **Deflation/ZLB distortion.** Japan's long deflation and protracted zero-lower-bound (ZLB) period meant financial cycles never fully materialized, biasing time-series r\* estimates **downward**.

The paper's conclusion is that r\* "cannot be pinned down in advance" and must be "viewed with considerable latitude" — Chair Powell's image of "navigating by the stars under cloudy skies." The BoJ therefore makes a **comprehensive judgment**, examining economic activity, prices, **and** financial developments, with financial conditions treated as *the transmission channel* through which policy actually reaches the economy.

Encouragingly, the tracker's r\* inputs are consistent with the paper's "moderately up" narrative: the midpoint estimate has edged up from **−0.245% (mid-2025)** to **−0.15% (mid-2026)**, the upper bound from +0.50% to **+0.55%**, and the lower bound from −0.99% to **−0.85%** — while BoJ-staff potential growth has risen from ~0.64% to **~0.71%**. Rising potential growth and the entrenchment of moderate wage/price increases (which reduce safe-asset demand) are exactly the drivers the paper cites.

### 2.2 The two-stage financial-conditions framework (Chart 6)

| Stage | Focus | What is examined | Key indicators in this tracker |
|---|---|---|---|
| **Stage 1** | **Interest-rate developments** | Short-term policy rate and safe-asset (JGB) yields feed into lending rates and asset prices. Examine **real** rates (nominal − expected inflation) **across maturities**, because real rates drive consumption/investment; short and medium real rates have the greater impact on activity. | Policy rate; JGB 1/2/5/10/30Y; inflation expectations 1/3/10Y; **real rates 1Y, 3Y, 10Y** |
| **Stage 2** | **Funding environment** | (i) **Funding costs** = safe yields + spreads; (ii) **availability of funds** = lending attitudes and firms' financial positions; (iii) **asset prices** via balance-sheet / expected-return channels; (iv) **funding volumes**. If funding demand stays strong after a hike, the change in accommodation may be small; a clear shift in volumes signals the hike is biting. | Lending rate, CP rate, corporate-bond spread; Tankan lending-attitude & financial-position DIs (large/small); TOPIX, Nikkei, USD/JPY; bank-lending y/y, CP & corporate-bond outstanding y/y |

The framework's logic is sequential: Stage-1 interest-rate moves are the *impulse*; Stage-2 funding outcomes are the *response*. A hike that pushes up policy and safe rates (Stage 1) has only bitten if it shows through in higher funding costs **and** tighter availability and slowing volumes (Stage 2). When availability stays easy and volumes keep growing after a hike, the BoJ infers that the change in the degree of accommodation has been small.

---

## 3. The two lenses on the hiking path

The BoJ cross-checks two complementary readings. They are not redundant: the natural-rate lens answers "how far is policy from neutral?"; the financial-conditions lens answers "is policy actually restraining the economy yet?". Near neutral, the second question dominates — because the first cannot be answered precisely, while the second is observable in real-world funding data.

| Dimension | **(A) Natural-rate / neutral-rate lens** | **(B) Financial-conditions lens** |
|---|---|---|
| **Core question** | How far is the real policy rate below (or above) r\*? | Are financial conditions accommodative or restrictive in transmission? |
| **What it says now** | Real policy rate **−0.98%** vs r\* midpoint **−0.15%** → gap **≈ −0.83pp**, i.e. policy still **accommodative**. Even against the band's **upper bound (+0.55%)**, the rate sits ~1.53pp below; against the **lower bound (−0.85%)**, policy is essentially *at* neutral. | Composite FCI **+0.69 (accommodative)**. Stage 1 **broadly neutral (−0.04)**; Stage 2 clearly **accommodative (+0.87)**. Availability easy, asset prices rich, volumes growing; only funding costs restrictive. |
| **Direction of travel** | r\* edging **up** (midpoint −0.245% → −0.15%; potential growth 0.64% → 0.71%), which *widens* room to hike. | Accommodation **narrowing**: FCI 1.01 → 0.69 over 18 months; real-rate gap −1.61 → −0.83. |
| **Strengths** | Anchors policy to fundamentals (growth, demographics, productivity); captures structural shifts in equilibrium. | Observable, timely, model-light; directly measures the transmission the policy is meant to achieve. |
| **Limitations** | Wide six-model band; real-time revisions; under-captures U.S./global spillovers; ZLB/deflation downward bias. "Cannot be pinned down in advance." | Composite weighting is analytical, not official; asset-price axis can dominate; says little about *why* conditions are easy (e.g. global risk appetite vs domestic policy). |
| **Weight near neutral** | Necessary but blunt — a *range*, not a trigger. | Gains relative weight: as the policy rate approaches the neutral range, gauging *actual* accommodation matters more than the imprecise distance to an uncertain star. |

**How the cross-check resolves.** Both lenses currently say *accommodative*, and both say *less so than a year ago*. That agreement is the key analytical result: when an imprecise structural measure (r\*) and an observable transmission measure (FCI) corroborate, the *direction* of the read is robust even though neither pins down the precise neutral rate. The paper's logic — and this tracker's data — therefore support continued, cautious normalization rather than either a pause-on-principle or an aggressive catch-up.

---

## 4. Current assessment by axis

### 4.1 Stage 1 — interest-rate developments

**Policy path and the JGB curve.** The overnight call rate has quadrupled from 0.25% to **1.00%** in eighteen months. The entire JGB curve has shifted up and steepened over the past year:

| Maturity | Jun 2025 | Dec 2025 | Jun 2026 | 12-month change |
|---|---|---|---|---|
| Policy rate | 0.50% | 0.75% | **1.00%** | +0.50pp |
| JGB 1Y | 0.60% | 0.79% | **0.95%** | +0.35pp |
| JGB 2Y | 0.84% | 1.05% | **1.31%** | +0.47pp |
| JGB 5Y | 1.19% | 1.48% | **1.82%** | +0.63pp |
| JGB 10Y | 1.52% | 2.03% | **2.67%** | +1.15pp |
| JGB 30Y | 2.59% | 3.04% | **3.34%** | +0.75pp |

The standout is the **10Y at ~2.67%**, up a striking **1.15pp** in a year — a far larger move than the 0.50pp of policy hikes, signalling a rising **term premium** and a genuine bear-steepening in the belly-to-10Y segment, not merely the mechanical pass-through of front-end hikes.

**Real rates by maturity — the crucial split.** Because real rates (nominal − expected inflation) drive spending, the framework insists on examining them across the curve. Inflation expectations are stable and well-anchored (1Y ~1.98%, 3Y ~1.86%, 10Y ~1.80%), so the real-rate moves are driven by nominal yields:

| Real rate | Jun 2025 | Dec 2025 | Jun 2026 | Reading | Activity weight |
|---|---|---|---|---|---|
| **1Y real** | −1.35% | −1.26% | **−1.03%** | Accommodative | Highest |
| **3Y real** | −0.97% | −0.71% | **−0.38%** | Broadly neutral | High |
| **10Y real** | −0.17% | +0.28% | **+0.87%** | **Restrictive** | Lower |

This is the single most important picture in the report. **Short and medium real rates remain negative** — exactly the maturities the BoJ flags as having the greatest impact on consumption and investment — so the front end is still stimulating activity. But the **long-end real rate has crossed firmly into positive territory (+0.87%)**, having swung ~1.04pp higher in a year. Accommodation is now concentrated at the front of the curve; the long end is already a drag. The aggregate **real-rate axis score is −0.04 ("broadly neutral")**, reflecting this tug-of-war: the front end (weighted heavily, 1.0) pulls accommodative, the long end (weighted 0.5, lower activity relevance) pulls restrictive.

### 4.2 Stage 2 — funding environment

**Funding costs (axis −0.89, restrictive — the one tightening axis).** This is where the hikes show through most clearly. The average contracted lending rate has risen to **1.17%** (from 0.95% a year ago); the CP issuance rate to **1.11%** (from 0.69%). Crucially, however, the **corporate-bond spread is just 0.31%** — barely changed (0.27% a year ago) and scored *accommodative*. The rise in funding costs is therefore almost entirely the safe-rate (policy/JGB) component, **not** a widening of credit risk premia. Credit markets are not signalling stress; they are repricing the risk-free base.

**Availability of funds (axis +1.09, accommodative).** Tankan diffusion indices show lending attitudes and corporate financial positions still firmly easy. Lending-attitude DIs sit at **+23.7 (large)** and **+17.6 (small)** enterprises; financial-position DIs at **+21.5 (large)** and **+13.7 (small)**. Notably, the small-enterprise readings have not deteriorated over the past year — they have nudged *up* — indicating that, in aggregate, SMEs do not yet report a credit squeeze. (See the distributional caveat in §5.)

**Asset prices (axis +2.74, strongly accommodative).** Equities are elevated and rising: **TOPIX ~3,958** (from ~3,248 a year ago, +22%) and **Nikkei 225 ~54,542** (from ~44,565, +22%). The yen is **weak at USD/JPY ~161** (from ~156), which the framework reads as accommodative via the export/expected-return channel. This axis is the largest single contributor to the positive FCI — and the analytical caveat applies: rich equities and a weak yen partly reflect global risk appetite and rate differentials, not solely domestic policy. A weak yen is "accommodative" mechanically, but it is also a *symptom* of policy lagging — see §6.

**Funding volumes (axis +0.55, accommodative).** The transmission acid test: are firms still borrowing? **Bank lending is growing +3.1% y/y** and **CP + corporate-bond outstanding +6.4% y/y**, both only marginally below a year ago (3.3% and 6.5%). Per the framework, sustained volume growth after a hike implies the change in accommodation has been *small*. There is, as yet, **no clear shift in volumes** to signal the hikes are biting hard.

### 4.3 Scorecard

| Axis (framework component) | Stage | Score (z) | Reading | Latest evidence |
|---|---|---:|---|---|
| **Real interest rates** | Stage 1 | **−0.04** | Broadly neutral | 1Y real −1.03% / 3Y −0.38% (accommodative) vs 10Y +0.87% (restrictive) |
| **Funding costs** | Stage 2 | **−0.89** | **Restrictive** | Lending 1.17%, CP 1.11% (rising); corp-bond spread 0.31% (still tight) |
| **Availability of funds** | Stage 2 | **+1.09** | Accommodative | Tankan lending DIs +23.7 / +17.6; financial-position DIs +21.5 / +13.7 |
| **Asset prices** | Stage 2 | **+2.74** | Accommodative | TOPIX 3,958 (+22% y/y); Nikkei 54,542; USD/JPY 161 (weak yen) |
| **Funding volumes** | Stage 2 | **+0.55** | Accommodative | Bank lending +3.1% y/y; CP & corp-bonds +6.4% y/y |
| **Stage 1 composite** | — | **−0.04** | Broadly neutral | Real-rate curve split front/back |
| **Stage 2 composite** | — | **+0.87** | Accommodative | Easy availability, rich assets, growing volumes outweigh higher costs |
| **Composite FCI** | — | **+0.69** | **Accommodative** | Conditions still accommodative at a 1.00% policy rate |

*Sign convention: positive = accommodative, negative = restrictive, expressed as z-scores against 2005-onward history.*

---

## 5. Impact of the BoJ rate hikes (Dec 2025 + June 2026)

**Has transmission been muted?** Partially. The hikes are pulling the right levers but with a long and uneven lag.

- **The working channel is funding costs.** Lending rates (+0.22pp y/y) and CP rates (+0.42pp y/y) are passing through. This is transmission doing its job at Stage 2.
- **But availability is still easy and volumes are still growing.** Tankan DIs have not turned down; bank lending (+3.1%) and bond issuance (+6.4%) continue to expand. By the framework's own test — "if funding demand stays strong after a hike, the change in accommodation may be small" — the hikes have **not yet materially curbed** funding activity.
- **Asset prices have moved the "wrong" way for tightening.** Equities are up 22% y/y and the yen has weakened further, both *adding* accommodation through balance-sheet and expected-return channels and partly offsetting the rate hikes.

**The trajectory confirms a modest, not sharp, withdrawal of accommodation:**

| Measure | Dec 2024 | Jun 2025 | Dec 2025 | Jun 2026 |
|---|---:|---:|---:|---:|
| Composite FCI | +1.01 | +0.88 | +0.82 | **+0.69** |
| Synthetic real-rate gap | −1.61 | −1.25 | −1.12 | **−0.83** |
| Stage 1 (real rates) | +1.13 | +0.75 | +0.43 | **−0.04** |
| Stage 2 (funding env.) | +0.98 | +0.92 | +0.92 | **+0.87** |
| Funding-costs axis | +0.25 | −0.08 | −0.42 | **−0.89** |

The decisive movement is in **Stage 1 / real rates** (from +1.13 to −0.04) and **funding costs** (from +0.25 to −0.89). **Stage 2 as a whole has barely moved** (+0.98 → +0.87) because easy availability, rich assets, and growing volumes have cushioned the rise in costs. The interest-rate impulse is real; the funding-environment response is so far muted.

**Distributional caveat (essential).** Aggregate readings mask heterogeneity, exactly as the paper warns. Rate hikes hit **sooner** for SMEs and high-debt sectors — whose floating-rate borrowing and thinner margins transmit higher costs quickly — and **later (if at all)** for debt-free, high-profit firms that are net savers. The small-enterprise Tankan DIs remaining positive (+17.6 lending-attitude, +13.7 financial-position) is reassuring *in aggregate* but does not preclude pockets of stress among leveraged smaller firms; these DIs should be watched closely for the first turn. On the **household** side, the impact must be judged on **both** the saving side (higher deposit/JGB returns help savers) **and** the borrowing side (variable-rate mortgages raise debt-service), set against **wage** growth that determines real purchasing power. With core CPI now at **1.5% y/y** (down from 2.3% a year ago) and a 1.00% policy rate, the household real-rate calculus is shifting but remains supportive of consumption where wages keep pace.

**Verdict on §5:** the hikes have reduced accommodation **only modestly so far**. The impulse is unambiguous; the bite on activity remains light.

---

## 6. Does the current picture support further rate hikes?

**Reasoned verdict: yes — further *gradual, data-dependent* normalization toward the lower end of the neutral band is supportable — but the room is narrower and more conditional than the headline FCI suggests.**

**The case for continuing:**
- The **real policy rate (−0.98%) is still ~0.83pp below the r\* midpoint** and ~1.53pp below the band's upper bound. Even allowing for r\* uncertainty, policy is more likely accommodative than not.
- **Conditions remain accommodative** (FCI +0.69), led by easy availability, rich asset prices, and growing volumes.
- **r\* is drifting up** (rising potential growth, entrenched moderate wage/price gains), which *widens* the distance to neutral and the room to move.
- Credit-risk premia are benign (**corp-bond spread 0.31%**), so the system is not fragile to a measured further step.

**The constraints that bound the path:**
- **The long end is already restrictive and rising fast.** The 10Y real rate is **+0.87%** and the 10Y nominal yield has jumped **1.15pp** in a year — a steepening term premium that does much of the tightening work without further BoJ action and raises debt-sustainability and financial-stability questions. Additional front-end hikes risk an outsized back-end reaction.
- **The yen is weak (USD/JPY ~161).** A weak currency is "accommodative" in the framework, but it also reflects policy *lagging* and imports inflation pressure; FX is a two-sided constraint on pace and a politically salient one.
- **U.S./global spillovers.** With free capital mobility, Japan's effective r\* is hostage to U.S. rates; a sharp shift abroad could move the neutral rate the models under-capture.
- **Distributional stress.** SMEs and high-debt borrowers feel each hike first; the small-firm Tankan DIs are the early-warning gauge.
- **Data revisions and the wide r\* band.** The neutral rate "cannot be pinned down in advance"; the GDP benchmark revision already shifted the band once. As policy nears neutral, the cost of over-tightening rises asymmetrically.

**Conditional path.** The data are consistent with one or two further **25bp** steps over the coming quarters *if* — wages and underlying inflation hold near or above 2%, Tankan availability DIs stay positive, lending and issuance volumes keep growing, and the long end does not disorderly steepen further. Should the long-end real rate climb materially above ~1%, the yen overshoot, or SME DIs roll over, the appropriate response is to **pause and reassess** rather than press toward the upper band. The destination is the **lower-to-middle** part of the neutral band, approached slowly. Consistent with the paper: *as the policy rate approaches the neutral range, correctly gauging the degree of accommodation becomes more important than ever* — argue for caution in **pace**, not a halt in **direction**.

---

## 7. Risks and what to watch

A watchlist tied to specific tracker indicators. The first column is the signal that would change the assessment; the trigger is a directional turn, not a precise threshold.

| # | Watch indicator (tracker key) | Current | What a worrying turn looks like | Implication |
|---|---|---:|---|---|
| 1 | **Tankan lending-attitude DI, small firms** (`tankan_lend_small`) | +17.6 | Falls toward 0 / negative | Availability tightening → accommodation withdrawn faster than intended; pause signal |
| 2 | **Bank-lending y/y** (`bank_lending_yoy`) | +3.1% | Rolls over toward 0% | Volume test trips → hikes biting; per framework, accommodation change is no longer "small" |
| 3 | **Corporate-bond spread** (`corp_bond_spread`) | 0.31% | Widens above ~0.5–0.6% | Credit-risk repricing (not just safe-rate); financial-stress signal |
| 4 | **1Y real rate** (`real_1y`) | −1.03% | Crosses **above zero** | Front-end (high-activity-weight) accommodation gone → policy at/through neutral |
| 5 | **10Y real rate / 10Y JGB** (`real_10y`, `jgb_10y`) | +0.87% / 2.67% | Long-end real >~1%, disorderly steepening | Term-premium / debt-sustainability risk; back-end overtightening |
| 6 | **USD/JPY** (`usdjpy`) | 161 | Overshoots weaker | Imported inflation, policy-credibility pressure; FX-driven constraint on pace |
| 7 | **Natural-rate band** (`natural_rate_*`) | −0.85% / −0.15% / +0.55% | Revised **down** (revisions, weaker growth) | Room-to-hike shrinks; current stance closer to neutral than thought |
| 8 | **Core CPI y/y** (`core_cpi_yoy`) | +1.5% | Falls sustainably below ~1.5–2% | Weakens the inflation case for further hikes |
| 9 | **Small-firm financial-position DI** (`tankan_finpos_small`) | +13.7 | Deteriorates | Distributional stress materializing among leveraged SMEs |

---

## 8. Methodology and data note

**The tracker.** The Japan Financial Conditions Tracker assembles official-source time series into the BoJ's two-stage framework. Data are sourced from the **Bank of Japan** (policy rate, lending/CP rates, corporate-bond spread, Tankan DIs, equities/FX, lending and issuance volumes, r\* and potential-growth estimates), the **Ministry of Finance** (JGB curve), **e-Stat** (CPI), and **FRED** (international cross-checks), and are stored in a SQLite database populated by an ETL pipeline (`etl/fetch.py`). Each indicator carries a polarity (sign convention), a weight reflecting its activity relevance (e.g. 1Y real rate weight 1.0 vs 10Y real rate 0.5; TOPIX 1.0 vs Nikkei 0.5), and a source URL.

**The composite FCI.** The FCI is a **z-score composite** computed against 2005-onward history, aggregated up the framework's five axes (real rates, funding costs, availability, asset prices, funding volumes) into Stage-1 and Stage-2 scores and a headline index. **It is an analytical synthesis on the BoJ framework's axes — not an official Bank of Japan index.** The BoJ publishes no single headline FCI; BoJ Review 2026-E-4 sets out a *qualitative* comprehensive judgment, and this tracker operationalizes that judgment quantitatively. Read the FCI as a structured summary of direction and degree, not as an official policy gauge. The asset-price axis in particular can be dominated by global factors; users should weight the underlying axes, not just the headline.

**Baseline horizon — the headline real-rate read now uses the longest available history.** The headline real-rate axis is z-scored over each maturity's **full available history** on an **ex-post** basis (nominal − *realized* core CPI), the only real inflation series available far enough back (CPI from 1970; JGB 1Y/3Y from 1974, 10Y from 1986). The **2005+ ex-ante** read (nominal − expected inflation) is retained only as a **reference**. Accommodation = −(z-score), weighted 1.0/1.0/0.5 across 1Y/3Y/10Y:

| Baseline window | Real-rate basis | Axis score | Assessment |
|---|---|---:|---|
| **Full history (1974/86+) — headline** | ex-post (vs realized core CPI) | **+0.19** | **Mildly accommodative** |
| Since 1990 | ex-post | **−0.03** | Broadly neutral |
| Since 1995 | ex-post | **−0.26** | Mildly restrictive |
| Since 2000 | ex-post | **−0.35** | Mildly restrictive |
| Since 2005 (ex-ante) — reference \* | ex-ante (vs expected inflation) | **−0.26** | Mildly restrictive |

> \* **The 2005+ reference is biased toward "restrictive."** Its baseline is dominated by Japan's zero/negative interest-rate policy (ZIRP from the late 1990s, NIRP 2016–2024), so the average real rate over that window is unusually low; a normalizing real rate therefore scores *above* that depressed mean and looks tighter than it is in a longer-run context. It is shown for continuity, not as the headline.

The verdict is **horizon-dependent**: on the headline full-history baseline (which includes the high-real-rate 1970s–80s) the stance is *mildly accommodative* (+0.19); against 1990 it is *broadly neutral*; only on post-1995 baselines is it *mildly restrictive*. Even so, the "restrictive" reading on those shorter windows is **not merely a NIRP artifact** — Japan's deflation episodes (negative CPI in 2009–10 and the mid-2010s) produced *high* ex-post real rates, and the 10Y real rate has now risen to ~its long-run norm (ex-post z ≈ 0). Read alongside the **level-based natural-rate read**, the *policy* stance remains accommodative (real policy rate ~0.83pp below the −0.15% midpoint, below the entire six-model band). Latest ex-post real rates: **1Y −0.4%, 3Y +0.1%, 10Y +1.1%**.

**Seed-data caveat (verbatim from `web/data.json` `meta.source_note`).**
> *"Seed values are illustrative approximations anchored to recent observations; run etl/fetch.py for authoritative data from BoJ/MoF/e-Stat/FRED."*

The snapshot used here is in **SEED mode** (`meta.data_mode = "SEED (illustrative; run etl/fetch.py for live data)"`), generated 2026-06-20, with `latest_date = 2026-06-30`. Numbers are illustrative approximations consistent with the June 2026 policy and market context; they should be refreshed against authoritative sources before any decision use. No values in this report were invented — every figure is drawn directly from `web/data.json`.

**Source paper (full citation).**
Bank of Japan, *"Developments in the Natural Rate of Interest and the Assessment of the Degree of Monetary Accommodation,"* **BoJ Review 2026-E-4**, Monetary Affairs Department, March 2026. Six-model r\* suite: Del Negro et al. (2017); Goy–Iwasaki (2024); Holston–Laubach–Williams (2023); Imakubo–Kojima–Nakajima (2015); Nakajima et al. (2023); Okazaki–Sudo (2018). Two-stage financial-conditions framework per Chart 6.

---

## Bottom-line verdict

**At a 1.00% policy rate, Japan's financial conditions remain genuinely accommodative (FCI +0.69; real policy rate ~0.83pp below the −0.15% neutral midpoint) — but the accommodation is narrowing, front-loaded in still-negative short real rates while the long end has already turned restrictive; further gradual, data-dependent normalization toward the lower end of the neutral band is supportable, provided it is paced with the BoJ's own "considerable latitude" against a fast-steepening curve, a weak yen, and an uncertain, upward-drifting r\*.**
