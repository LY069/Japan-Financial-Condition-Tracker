# Japan Monetary & Liquidity Conditions: Literature and Indicator Review

*Companion research note for the Japan Monetary & Liquidity Conditions Tracker (sister to the Japan Financial Conditions Tracker built on BoJ Review 2026-E-4).*
*Prepared 10 September 2026. Sources are cited inline; a consolidated reference list is at the end. Items that could not be verified directly (the BoJ, BIS, IMF and FRED sites were unreachable from the research environment, so primary PDFs were read through search-engine extracts and secondary mirrors) are flagged explicitly.*

---

## 1. Purpose and scope

The existing tracker measures **financial conditions** — the transmission channel from policy to the real economy, following the two-stage framework in BoJ Review 2026-E-4 (*Developments in the Natural Rate of Interest and the Assessment of the Degree of Monetary Accommodation*, March 2026, https://www.boj.or.jp/en/research/wps_rev/rev_2026/rev26e04.htm). This note reviews the literature and indicator set for two adjacent concepts that the FCI deliberately does not cover: **monetary conditions** (the stance and quantity of money) and **liquidity conditions** (the plumbing through which the stance is implemented and through which stress propagates). The aim is to specify what to measure, why, how to read it, and where to get it.

The policy backdrop is unusually live. Between March 2024 and September 2026 the Bank of Japan ended negative rates and yield-curve control, raised the policy rate in five steps to 1.0% (June 2026), shrank its balance sheet by roughly 9% in FY2025 alone, and is tapering JGB purchases to ~¥2 trillion per month by early 2027 — the first sustained quantitative tightening in Japan's history. Every indicator discussed below is being re-priced by that regime change.

---

## 2. Definitions and taxonomy

### 2.1 Three overlapping concepts

| Concept | What it measures | Canonical instruments | Primary use |
|---|---|---|---|
| **Monetary conditions** | The *stance* of monetary policy and the *quantity* of money/credit it generates | Real short rate vs. natural rate; exchange rate; money (M2/M3, Divisia) and credit aggregates; central-bank balance-sheet size and composition; shadow/proxy policy rates | Judging whether policy is easy or tight relative to neutral; medium-run inflation signal |
| **Liquidity conditions** | The *ease of transacting and funding* at three layers (central bank, funding markets, securities markets) | Reserves/current-account balances; TONA–IOER and GC-repo spreads; TIBOR–OIS; JPY cross-currency basis; JGB bid-ask, depth, turnover, volatility | Judging implementation control, funding stress, and the constraint that market functioning places on balance-sheet normalisation |
| **Financial conditions** (existing tracker) | The *price and availability of finance to the real economy* | Lending rates and spreads, credit availability DIs, equity prices, FX, lending volumes | Judging the degree of accommodation reaching firms and households |

The three overlap at the edges — the policy rate and the exchange rate belong to both monetary and financial conditions; bank lending volumes sit in both money and financial conditions — but they answer different questions. Monetary conditions ask *what the central bank has set*; liquidity conditions ask *whether the machinery is working and at what price*; financial conditions ask *what the economy faces*. A liquidity shock (e.g. a repo-rate spike or a JGB market seizure) can tighten financial conditions with no change in the monetary stance, which is exactly why the two trackers should be kept distinct but read together.

### 2.2 Monetary conditions: the MCI lineage and its critique

The **Monetary Conditions Index** (MCI) — a weighted sum of changes in the real short rate and the real exchange rate, with weights reflecting their relative effect on output — was pioneered by the Bank of Canada and later used by the RBNZ as an operational guide (Freedman, C., "The Role of Monetary Conditions and the Monetary Conditions Index in the Conduct of Policy," *Bank of Canada Review*, Autumn 1995; Freedman 1994 in IMF, *Frameworks for Monetary Stability*, https://www.elibrary.imf.org/display/book/9781557754196/ch018.xml). The definitive critique is Ericsson, Jansen, Kerbeshian and Nymoen (1998), "Interpreting a Monetary Conditions Index in Economic Policy," *BIS Conference Papers* Vol. 6 (https://www.bis.org/publ/confp06i.pdf): MCI weights are model-dependent, parameter uncertainty is large, and the index conflates shocks that require opposite policy responses (an exchange-rate move driven by a terms-of-trade shock vs. one driven by capital flows). Freedman himself concluded the MCI is "a useful concept and practical tool but must be used with care."

**Implication for Japan.** An MCI is still worth computing — Japan's exchange rate has been the single most important swing factor in the 2022–26 inflation episode, and the July–August 2026 record ¥15.4 trillion intervention (with unusual US participation) shows the authorities treat the yen as a monetary-conditions variable in practice (https://www.omfif.org/2026/08/japans-yen-intervention-and-the-us-unusual-support/). But it should be shown as a *range* under alternative weights, and the real-rate leg should reference the BoJ's natural-rate band (≈ −1% to +0.5%) from BoJ Review 2026-E-4 rather than an unconditional zero.

### 2.3 Liquidity conditions: three layers

| Layer | Concept | Japan-specific instruments | Key references |
|---|---|---|---|
| **Central-bank (base) liquidity** | Reserves the central bank has created; the quantity side of the balance sheet | Monetary base; BoJ current-account balances (CAB) and excess reserves; BoJ JGB holdings and share of outstanding; total assets | Shiratsuka (2025); BoJ Broad Perspective Review (2024); Afonso et al. (2022/25) |
| **Funding liquidity** | Ease with which institutions borrow against or without collateral, in yen and dollars | TONA vs. policy target (IOER); GC repo (Tokyo Repo Rate) vs. IOER; TIBOR–OIS; JPY/USD cross-currency basis; BoJ USD funds-supplying operations | BoJ "Market Operations in FY2025" (Aug 2026); BoJ (Nov 2024) money-market paper; Borio et al. (2016); Aldasoro & Ehlers (2018) |
| **Market liquidity** | Ease of transacting in size without moving price, in the JGB market above all | BoJ *Liquidity Indicators in the JGB Markets* (bid-ask, depth, price impact, turnover); *Bond Market Survey* functioning DI; realised yield volatility; term premium | Kurosaki et al. (2015); Sakiyama & Kobayashi (2018); BoJ WP 24-E-9; BoJ Review 2026-E-10; IMF Article IV 2026 |

The layers are causally chained: base liquidity anchors funding liquidity (abundant reserves pin TONA to the floor); funding liquidity underwrites market liquidity (dealers' repo access determines warehousing capacity); and market liquidity feeds back on the central bank's ability to shrink base liquidity (the BoJ's taper is explicitly conditioned on "developments in and functioning of the JGB markets"). A tracker that displays them as a single stack makes that chain visible.

---

## 3. What is new, 2022–2026

### 3.1 The "money view" revival

The post-2021 inflation surge rehabilitated money growth as an inflation signal. **Borio, Hofmann and Zakrajšek (2023)**, "Does money growth help explain the recent inflation surge?", *BIS Bulletin* No. 67 (https://www.bis.org/publ/bisbull67.pdf), find the money–inflation link is regime-dependent: close to one-for-one when inflation is high, essentially absent when it is low; an upsurge in money growth preceded the flare-up, countries with stronger money growth saw markedly higher inflation, and adding money growth would have materially improved 2021–22 forecasts. Borio updated the evidence in January 2024 ("Money growth and the post-pandemic inflation surge: updating the evidence," https://www.bis.org/speeches/sp240124.htm; VoxEU version at https://cepr.org/voxeu/columns/money-growth-and-post-pandemic-inflation-surge-updating-evidence), showing the subsequent money-growth collapse was consistent with the disinflation.

The counter-view is **Berger, Karlsson and Österholm (2023)**, "A Note of Caution on the Relation Between Money Growth and Inflation," IMF WP 2023/137, also *Scottish Journal of Political Economy* 70(5) (https://www.imf.org/en/Publications/WP/Issues/2023/06/30/A-Note-of-Caution-on-the-Relation-Between-Money-Growth-and-Inflation-534322): using time-varying-parameter BVARs they find the relation is unstable, and that the post-pandemic episode is largely explained by conventional demand and supply shocks. A 2025 wavelet study (Sokic, *Bulletin of Economic Research*, https://onlinelibrary.wiley.com/doi/10.1111/boer.70072) finds the link is strong at low frequencies and weak at business-cycle frequencies — which reconciles the two camps: money is a *medium-run* signal, not a quarterly one.

**Japan's evidence.** Japan is the low-inflation regime par excellence in the BIS sample: M2 grew 9–10% y/y in 2020–21 with only a lagged, modest pass-through, and growth is now back to 2.2% y/y (July 2026, ¥1,297 trillion) with M3 at 1.4% (https://www.mql5.com/en/economic-calendar/japan/m2-money-stock-yy; BoJ Money Stock statistics https://www.boj.or.jp/en/statistics/money/ms/index.htm). By contrast **bank lending** has accelerated to 5.4–6.3% y/y in mid-2026, the fastest since 2020 (https://www.japantimes.co.jp/business/2026/07/08/economy/japan-bank-lending-rise/). The divergence — credit strong, money weak, monetary base contracting at −13.7% y/y (June 2026) — is itself informative: deposit creation is being offset by portfolio shifts into investment trusts and by QT.

*Measurement implication.* Track **M2/M3 growth, real M2 growth (deflated by core CPI), the M2–nominal-GDP gap, and bank lending growth** side by side, and display the BIS regime message: the inflation-signal value of money rises when inflation is already above 2%, which is Japan's situation in H2 FY2026 (the BoJ's July 2026 Outlook expects core CPI "clearly above" 2%, https://www.cnbc.com/2026/07/31/boj-rates-yen-intervention-inflation-japan.html).

### 3.2 The BoJ's exit and the JGB-purchase taper

The **Review of Monetary Policy from a Broad Perspective** (BoJ, 19 December 2024, https://www.boj.or.jp/en/mopo/outline/bpreview/index.htm; full report https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2024/k241219b.pdf) is the reference document. Its quantitative findings: large-scale easing since 2013 raised the level of real GDP by roughly +1.3 to +1.8% (Q-JEM) or +0.9 to +1.3% (alternative models) and CPI inflation by about +0.6 to +0.7 pp on average; the yield-curve effect operated through the **stock** of holdings rather than the flow of purchases (Nakazawa & Osada, BoJ WP 24-E-10, https://www.boj.or.jp/en/research/wps_rev/wps_2024/wp24e10.htm); and QQE/YCC measurably impaired JGB market functioning (Fukuma et al., BoJ WP 24-E-9, https://www.boj.or.jp/en/research/wps_rev/wps_2024/wp24e09.htm, panel evidence across JGB issues). The Review's forward lesson, as read by Nomura's Kiuchi (https://www.nri.com/en/media/journal/kiuchi/20250110.html), is that NIRP, YCC and ETF purchases are unlikely to return; if unconventional support is needed again, the BoJ would pause QT and resume JGB purchases.

**Chronology of the exit (verified against BoJ statements and contemporaneous reporting):**

| Date | Decision | Source |
|---|---|---|
| Mar 2024 | NIRP and YCC ended; policy rate 0–0.1% | Broad Review |
| 31 Jul 2024 | Rate to 0.25%; JGB purchase-reduction plan: −¥400bn per quarter to ~¥3tn/month by Q1 2026 | https://www.boj.or.jp/en/mopo/mpmdeci/state_2024/k240731a.htm |
| Jan 2025 | Rate to 0.5% | — |
| 17 Jun 2025 | Interim assessment: taper slowed to −¥200bn/quarter from Apr 2026, reaching ~¥2tn/month in Jan–Mar 2027; super-long (>25y) purchases held flat after the April–May 2025 30-year yield spike (+100bp to 3.2%) | https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2025/k250617b.pdf; https://www.nri.com/en/media/journal/kiuchi/20250711.html |
| Dec 2025 | Rate to 0.75% | https://www.cnbc.com/2026/04/28/bank-of-japan-keeps-policy-rate-steady-cpi-iran-war-gdp.html |
| Jan/Mar/Apr 2026 | Holds at 0.75%; April Outlook raises core-CPI forecast to 2.8% on the Middle East oil shock | same |
| 16 Jun 2026 | Rate to **1.0%** (7–1), highest since 1995; interim assessment keeps taper (¥2.7tn Apr–Jun 2026 → ¥2.1tn Jan–Mar 2027) and sets guideline of **~¥2tn/month from April 2027** — i.e. tapering ends in FY2027; Tamura dissents, proposing continued −¥200bn/quarter to Q1 2028 | https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260616a.pdf; https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260616b.pdf; https://www.oxfordeconomics.com/resource/the-boj-hiked-a-policy-rate-and-will-end-the-tapering-of-jgb-purchases-in-fy2027/ |
| 31 Jul 2026 | Hold at 1.0% (8–1, Takata for 1.25%); Ueda: "if we fail… we could be forced to raise rates rapidly" | https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260731a.pdf; https://www.cnbc.com/2026/07/31/boj-rates-yen-intervention-inflation-japan.html |
| 17–18 Sep 2026 | Markets price a hike to 1.25% | https://www.japantimes.co.jp/business/2026/08/28/economy/tokyo-cpi-august/ |

Balance-sheet outcomes: total assets ¥662.1tn at end-March 2026, down ¥67.6tn (−9.3%) in FY2025 (BoJ Accounts, https://www.boj.or.jp/en/statistics/boj/other/acmai/release/2026/ac260331.htm); JGB holdings down from 91% of GDP (June 2024) to about 80% (January 2026) per the IMF 2026 Article IV (https://www.imf.org/en/news/articles/2026/04/02/pr-26105-japan-imf-executive-board-concludes-2026-article-iv-consult); current-account balances ¥407tn at end-June 2026, −16.4% y/y (https://ai-market-station.jp/japan/jul-monetary-policy-tightening-en/ — secondary source, verify against BoJ MD08).

### 3.3 Effect of the taper on JGB market functioning

The BoJ's own assessment is **BoJ Review 2026-E-10**, *Impact of the Bank of Japan's Reductions in JGB Purchases on the JGB Markets* (August 2026, https://www.boj.or.jp/en/research/wps_rev/rev_2026/rev26e10.htm): functioning "has been steadily improving as the Bank makes progress in reducing its JGB purchases," long rates are "formed more freely," but the medium-to-long zone still shows tight supply-demand from the BoJ's high holdings share; recent yield increases are attributed "to a certain extent" to fundamentals (higher underlying inflation) rather than to the taper alone; and domestic banks and households have been absorbing supply only gradually. The April 2026 *Financial System Report* (https://www.boj.or.jp/en/research/brp/fsr/fsr260421.htm) records that cash-market transaction volume is on an increasing trend and the bond-market functioning DI improved through H2 FY2025. The quarterly *Liquidity Indicators in the JGB Markets* (latest 29 June 2026, https://www.boj.or.jp/en/paym/bond/ryudo.pdf) is the underlying data.

The **Bond Market Survey** DI for the degree of functioning was −16 in the May 2026 survey (from −26 in February; 3-month-change DI +12), still negative but far above the −64 trough of February 2023 under YCC. *(The August 2026 survey, released 1 September 2026 with 75 respondents — https://www.boj.or.jp/en/paym/bond/bond_list/bond2608.pdf — could not be read directly; the headline DI should be entered by hand.)*

Two qualifications from outside the BoJ. First, the **IMF 2026 Article IV** notes that foreign investors — now about 65% of monthly cash trading volume vs. 12% in 2009 (https://www.morningstar.com/markets/how-japans-bond-selloff-impacts-banks-insurers) — improve turnover but make the market more sensitive to fiscal and global news, and it urges the BoJ to be ready for "exceptional targeted interventions" if volatility undermines liquidity. Second, the **IMF April 2026 GFSR** (Ch. 1, https://www.imf.org/-/media/files/publications/gfsr/2026/april/english/ch1.pdf) attributes the rise in JGB yields to term premia driven by fiscal-risk perceptions, and flags spillovers through Japan's large NIIP (Box: "Rising Japanese Government Bond Yields Could Affect Global Asset Allocation"). The 10-year yield reached 2.93% in August 2026, the highest since 1996; the 30-year reached 3.89% in January 2026 (https://www.euronews.com/business/2026/08/17/japans-10-year-bond-yield-hits-a-30-year-high-as-growth-data-disappoints). Cross-country QT evidence (Du, Forbes & Luzzetti, NBER WP 32321, 2024, https://www.nber.org/papers/w32321) is that QT announcements raise yields and steepen curves, active QT more than passive, but with effects "more than paint drying, far less than reversing QE."

*Measurement implication.* Market liquidity must be tracked with **both** hard microstructure data (bid-ask, depth, price impact, turnover) **and** the survey DI, plus a realised-volatility series that the tracker can compute daily from the MoF yield-curve file. Volatility is what actually triggered the June 2025 taper slowdown.

### 3.4 Reserves: abundance, scarcity, and rate control

The Fed literature now frames reserve regimes by the slope of the reserve-demand curve: **Afonso, Giannone, La Spada and Williams**, "Scarce, Abundant, or Ample? A Time-Varying Model of the Reserve Demand Curve," NY Fed Staff Report 1019 (2022, rev. 2025, https://www.newyorkfed.org/research/staff_reports/sr1019), estimate that reserves become "abundant" (demand satiated) above roughly 12–13% of bank assets; the NY Fed publishes a monthly Reserve Demand Elasticity. Applied to Japan, **Shiratsuka (2025)**, "Toward a Guidepost for Quantitative Tightening: The Case of the Bank of Japan," HIAS-E-146 and *Japanese Economic Review* (https://hias.hit-u.ac.jp/wp-content/uploads/2025/09/HIAS-E-146.pdf; https://link.springer.com/article/10.1007/s42973-025-00232-6), estimates the reserve-demand curve on daily data from 2009 to August 2025, finds that IOER-eligible institutions' reserve demand is currently satiated so CAB does not move the call rate, simulates JGB-holding paths to 2027–28, and proposes "extended banknote rules" for the long-run balance-sheet size — while stressing "considerable uncertainty" about when shrinkage would start to bite on the call rate.

Implementation evidence is reassuring so far. The BoJ's *Market Operations in Fiscal 2025* (August 2026, https://www.boj.or.jp/en/research/brp/mor/mor260812.htm) reports TONA "extremely stable at a level slightly below" IOER (TONA ~0.977% against a 1.0% target in September 2026), with regional banks and other CDF-eligible institutions borrowing actively in the call market to arbitrage IOER; the GC repo rate rose during H2 FY2025 from slightly below IOER to close to it as bond supply-demand eased — a first, mild sign that collateral is becoming less scarce as the BoJ hands JGBs back to the market. The Broad Perspective Review's money-market paper (BoJ, November 2024, https://www.boj.or.jp/en/research/brp/ron_2024/ron241106a.htm) sets out why this matters: with TONA now the benchmark for the entire yen derivatives complex after LIBOR, a call market with diverse participants and real volume is a policy objective in itself.

*Measurement implication.* Track **excess reserves as a share of bank assets** (the Afonso et al. metric), the **TONA–IOER spread** and **GC repo–IOER spread** as the early-warning gauges for the transition from abundance to ample-ness. Today both spreads are a few basis points and negative; a *rise* toward zero and above would be the tell that the QT path is reaching the steep part of the demand curve.

### 3.5 Dollar funding and the yen basis

Japanese banks are the largest non-US dollar lenders and rely on FX swaps and cross-currency swaps to fund a structural dollar gap. The canonical references remain Borio, McCauley, McGuire and Sushko (2016), "Covered interest parity lost: understanding the cross-currency basis," *BIS Quarterly Review* September 2016 (https://www.bis.org/publ/qtrpdf/r_qt1609e.htm), and Aldasoro and Ehlers (2018), "The geography of dollar funding of non-US banks," *BIS Quarterly Review* December 2018 (https://www.bis.org/publ/qtrpdf/r_qt1812b.htm), with Aldasoro, Ehlers & Eren (2018), BIS WP 708 on business models. The BoJ's 2021 Review on the cross-currency swap market through OTC-derivatives data (https://www.boj.or.jp/en/research/wps_rev/rev_2021/data/rev21e01.pdf) and BoJ Review 2025-E-8 on G-SIBs' foreign-currency deposit stickiness (https://www.boj.or.jp/en/research/wps_rev/rev_2025/data/rev25e08.pdf) are the Japan-specific supervisory literature. The April 2026 FSR reports dollar funding premia "generally at low levels," widening temporarily at year-end and on the Middle East shock. New in 2026 is the expectation that the US–Japan $550bn investment agreement will push the 5–10-year dollar-yen basis wider (https://www.globalcapital.com/article/2fy4f1pkz253xi11mtfy8/people-and-markets/leader/japans-550bn-us-trade-deal-set-to-drive-cross-currency-basis), and the BIS global liquidity indicators show yen credit outside Japan contracting (−4% y/y at end-Q3 2025, https://www.bis.org/statistics/gli2601.htm).

*Measurement implication.* The 3-month JPY/USD basis is the single best funding-stress gauge but is **not freely available**; the tracker should either license it or proxy it from the FSR charts and BoJ USD-operations usage, and should present BIS yen-credit growth as the slow-moving structural backdrop.

### 3.6 Shadow rates and effective-stance measures

Under the ZLB the stance was summarised by shadow short rates — Krippner (2013/2015), Wu & Xia (2016), and for Japan Ichiue & Ueno (BoJ WP 13-E-8; *JJIE* 2015). Krippner's LJK Ltd still publishes a Japan SSR, "Effective Monetary Stimulus" and expected-time-to-liftoff series (https://www.ljkmfa.com/). With the policy rate at 1.0% these collapse onto the observed rate, but the balance-sheet stock effect on term premia persists (Nakazawa & Osada 2024), so an "effective stance" measure is still needed. The cleanest template is the SF Fed **proxy funds rate** (Choi, Doh, Foerster & Martinez 2022; https://www.frbsf.org/research-and-insights/data-and-indicators/proxy-funds-rate/), which extracts principal components from a dozen market rates and spreads and maps them to a policy-rate equivalent; in 2022 it showed US policy behaving as if the funds rate were ~2pp higher than actual. Anderl & Caporale (2023, *Scottish JPE*, https://onlinelibrary.wiley.com/doi/10.1111/sjpe.12343) is the caveat: shadow-rate estimates are model-sensitive and should be displayed as ranges.

*Measurement implication.* Build a **Japan proxy policy rate** from the tracker's own yield-curve, TIBOR, repo and swap data rather than importing a shadow rate; use the LJK SSR only for pre-2024 history.

### 3.7 Divisia money

Divisia aggregates weight components by their user cost so that near-money earning market rates is not counted as transactions money. Barnett and co-authors have shown improved nowcasting of nominal GDP and inflation with Divisia (Barnett, Chauvet & Leiva-Leon 2016; Barnett & Park, *J. Forecasting* 2023; Barnett et al., *JMCB* 2024, https://onlinelibrary.wiley.com/doi/10.1111/jmcb.13088). For Japan, the literature is thin and old: Ishida (1984, BoJ *Monetary and Economic Studies*) found Divisia mattered for broad money but not M1, and the BoJ does not publish a Divisia index (https://www.boj.or.jp/en/statistics/outline/exp/data/exms01.pdf). The case for a Japanese Divisia is stronger now than at any time since the 1990s: with deposit rates finally dispersing (time deposits repriced toward 1%), simple-sum M2 overstates transactions money.

*Measurement implication.* A proper Divisia is a phase-2 project (needs component rates); as an interim, show **M1 vs. M2 growth** and the **currency + demand-deposit share of M2**, which move in the same direction as a Divisia adjustment.

### 3.8 Credit-to-GDP gaps

The BIS credit-to-GDP gap (HP-filtered deviation of private non-financial credit/GDP from trend) remains the best single early-warning indicator of banking distress (Drehmann & Tsatsaronis 2014, *BIS QR* March 2014, https://www.bis.org/publ/qtrpdf/r_qt1403g.htm; Aldasoro, Borio & Drehmann 2018, *BIS QR* March 2018, https://www.bis.org/publ/qtrpdf/r_qt1803e.htm, which adds household-debt and debt-service ratios). Japan's gap swung positive in 2020–21 on pandemic lending and has since narrowed; the April 2026 FSR's heat map shows no overheating but warns that structural loan-demand decline can produce either contraction or "excessive search for yield." The gap is downloadable from the BIS Data Portal (https://data.bis.org/topics/CREDIT_GAPS) — *(latest Japanese value not verified here; the portal was unreachable).*

### 3.9 New official indicators worth adopting

- BoJ *Liquidity Indicators in the JGB Markets*: quarterly since 2015, expanded March 2018 to cover volume, tightness, depth and resiliency in the cash market (Sakiyama & Kobayashi 2018, https://www.boj.or.jp/en/research/brp/ron_2018/data/ron180329a.pdf; Kurosaki, Kumano, Okabe & Nagano 2015, BoJ WP 15-E-2).
- BoJ *Bond Market Survey* (quarterly, Feb/May/Aug/Nov): functioning DI, bid-ask and depth DIs.
- BoJ *Tokyo Money Market Survey* (annual, August; 2026 results to be presented at the 14 October 2026 Meeting on Market Operations, https://www.boj.or.jp/en/paym/market/mkt260903a.pdf).
- NY Fed *Reserve Demand Elasticity* as a methodological template for Japan.
- BIS *global liquidity indicators* (quarterly) for yen and dollar credit.

---

## 4. Indicator recommendations for Japan

Polarity convention: **↑ = easier/more liquid** unless stated. "Auto" = retrievable programmatically from FRED, BIS, MoF or JSDA; "BoJ-CSV" = BoJ Time-Series Data Search (API available, https://www.stat-search.boj.or.jp/info/api_manual_en.pdf); "Manual" = PDF/survey hand-entry. BoJ codes marked † are the series-family codes confirmed from the BoJ site map; exact sub-series must be looked up in stat-search.

| # | Indicator | Layer | Source / URL | Freq. | History | Access | Polarity | Why it matters |
|---|---|---|---|---|---|---|---|---|
| 1 | Policy rate (uncollateralized O/N call target) & TONA | Monetary / Funding | BoJ FM01† (daily TONA); FRED `IRSTCI01JPM156N` (monthly avg) | D / M | 1985– | BoJ-CSV / Auto | ↑ tighter | Anchor of the stance; TONA–target gap is the control gauge |
| 2 | Real policy rate (TONA − core CPI ex fresh food & energy, and − 1y inflation expectations) vs. natural-rate band | Monetary | Computed; r* band from BoJ Review 2026-E-4 | M | 2005– | Computed | ↑ tighter | Stage-1 stance measure; ties to existing tracker |
| 3 | Real effective exchange rate (BIS REER) and USD/JPY | Monetary | BIS EER dataset; FRED `RBJPBIS` (verify), `DEXJPUS` | M / D | 1994– / 1971– | Auto | ↑ (yen stronger) tighter | Second MCI leg; 2026 intervention regime |
| 4 | MCI (0.75×Δreal rate + 0.25×Δlog REER, weight range 3:1 to 2:1) | Monetary | Computed | M | 2005– | Computed | ↑ tighter | Classic composite; show as band |
| 5 | M2, M3 growth (y/y) and real M2 growth | Monetary | BoJ MD02†; FRED `MABMM301JPM189S` (M3), `MYAGM2JPM189N` (M2, ends 2017) | M | 1967– (M2), 2003– (M3) | BoJ-CSV / Auto | ↑ easier | Money-view inflation signal (BIS Bulletin 67) |
| 6 | M1 growth and M1/M2 share (Divisia proxy) | Monetary | BoJ MD02†; FRED `MANMM101JPM189S` (verify) | M | 2003– | BoJ-CSV / Auto | ↑ easier | Approximates liquidity-weighted money as deposit rates disperse |
| 7 | Bank lending growth (y/y, total & ex-shinkin) | Monetary | BoJ Loans and Bills Discounted (stat-search "Loans and Discounts"); Reuters/JT monthly | M | 1991– | BoJ-CSV | ↑ easier | Credit leg; 5–6% y/y in 2026 is the strongest since 2020 |
| 8 | Credit-to-GDP gap (BIS) and private credit/GDP | Monetary | BIS Data Portal WS_CREDIT_GAP, WS_TC; FRED `QJPPAM770A` (verify) | Q | 1965– | Auto | ↑ easier / risk | Early-warning indicator (Drehmann–Tsatsaronis) |
| 9 | Monetary base (y/y) | CB liquidity | BoJ MD01† | M | 1970– | BoJ-CSV | ↑ easier | Quantity of base money; −13.7% y/y June 2026 |
| 10 | BoJ current-account balances & excess reserves; excess reserves / bank assets | CB liquidity | BoJ MD06†/MD07†/MD08† (CAB by sector); bank assets from BoJ Assets & Liabilities of Domestically Licensed Banks | D / M | 2001– | BoJ-CSV | ↑ easier | Afonso et al. ampleness metric; Shiratsuka QT guidepost |
| 11 | BoJ total assets, JGB holdings, and share of outstanding JGBs | CB liquidity | FRED `JPNASSETS` (monthly); BoJ Accounts (10-day); MoF holdings breakdown (Q) https://www.mof.go.jp/english/policy/jgbs/reference/Others/holdings01.pdf | M / Q | 1998– | Auto / Manual | ↑ easier | Stock effect on term premium (Nakazawa–Osada); taper progress |
| 12 | BoJ monthly JGB purchase amount vs. plan | CB liquidity | BoJ purchase schedule (Financial Markets Dept.) | M | 2013– | Manual | ↑ easier | Flow of QT; deviation from plan = policy signal |
| 13 | TONA − IOER spread; GC repo (Tokyo Repo Rate) − IOER | Funding | BoJ FM01†; JSDA Tokyo Repo Rate https://www.jsda.or.jp/en/statistics/bonds/trr/ | D | 2008– / 2012– | BoJ-CSV / Auto (scrape) | ↑ (toward zero/positive) tighter/scarcer | Transition from abundant to ample reserves; collateral scarcity |
| 14 | 3m TIBOR − OIS (or TIBOR − TONA 3m compounded) | Funding | JBA TIBOR https://www.jbatibor.or.jp/english/rate/historical_data.html; FRED `IR3TIB01JPM156N` | D / M | 2014– / 1986– | Auto | ↑ tighter | Bank term-funding stress |
| 15 | 3m JPY/USD cross-currency basis; BoJ USD ops usage | Funding | Bloomberg/LSEG (licensed); BoJ FSR charts; BoJ USD funds-supplying operation results | D | 2008– | Manual / licensed | More negative = tighter | Dollar funding cost of Japanese banks (Borio et al. 2016) |
| 16 | JGB market functioning DI (Bond Market Survey) | Market | https://www.boj.or.jp/en/paym/bond/bond_list/index.htm | Q | 2015– | Manual | ↑ more liquid | Official participant read; taper conditioned on it |
| 17 | JGB liquidity indicators: futures bid-ask, depth (best-ask volume), price impact, cash turnover, SC repo fee | Market | https://www.boj.or.jp/en/paym/bond/index.htm ("Liquidity Indicators in the JGB Markets") | Q (monthly data) | 2012– | Manual | Spread/impact ↑ = less liquid; turnover ↑ = more liquid | Microstructure core (Kurosaki et al. 2015) |
| 18 | Realised volatility of 10y and 30y JGB yields (20-day) and 10s30s slope | Market | MoF daily yield CSV https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/jgbcme.csv; FRED `IRLTLT01JPM156N` | D | 1974– | Auto | ↑ less liquid | Volatility triggered the 2025 taper slowdown; super-long stress |
| 19 | 10y term premium (ACM-style or 10y − 3m TONA futures/OIS) | Market / Monetary | Computed from MoF curve; JPX 3m TONA futures | D | 1990s– | Computed | ↑ tighter | GFSR 2026: fiscal-risk term premium is the new driver |
| 20 | Foreign share of JGB cash trading; BIS yen credit outside Japan | Market / Funding | JSDA trading by investor type; BIS GLI https://www.bis.org/statistics/gli2601.htm | M / Q | 2004– | Auto (scrape) / Auto | Ambiguous | Structural liquidity providers vs. fragility (IMF Art. IV 2026) |

---

## 5. Implications for growth, inflation and policy conduct

| Indicator group | Growth | Inflation | Policy conduct |
|---|---|---|---|
| **Stance & MCI (1–4)** | Real short rate still below the r* band ⇒ conditions accommodative; each 25bp hike closes ~a quarter of the gap. Yen strength after intervention tightens the MCI even with rates unchanged. | Yen is the fastest inflation channel (import prices); the 2026 oil shock plus a weak yen is why the BoJ expects core CPI "clearly above" 2%. | Markets price 1.25% in September 2026 and the BoJ has hinted at a faster-than-semi-annual pace; the MCI helps separate what the yen has already done from what rates must do. |
| **Money & credit (5–8)** | Lending at 5–6% y/y signals firm capex and real-estate demand; M2 at ~2% says deposit creation is being diverted, not that demand is weak. | BIS regime message: with inflation above 2%, money growth regains signal value; currently M2 growth is *disinflationary* relative to nominal GDP growth (~3–4%). A re-acceleration of M2 above ~4% would be an upside-risk flag. | Low money growth argues against the "monetary overhang" view of Japanese inflation; the credit gap being near zero gives no macroprudential reason to accelerate hikes. |
| **CB liquidity (9–12)** | Stock-effect literature implies the ~¥100tn/yr run-off adds to term premia gradually; Du–Forbes–Luzzetti suggest a modest, front-loaded yield effect. | Balance-sheet shrinkage has little direct inflation effect once rates are positive; its inflation relevance is through the yen if higher term premia attract inflows. | The binding constraint on QT pace is market functioning, not reserves (Shiratsuka; BoJ 2026-E-10). The April-2027 floor of ~¥2tn/month means holdings keep falling but at a slower pace — the tracker should show the "hold-to-run-off gap." |
| **Funding liquidity (13–15)** | Funding stress transmits to lending spreads within weeks; currently negligible. | Indirect. | TONA–IOER and repo–IOER creeping up would signal the start of reserve ample-ness and would argue for a slower QT or a new floor system; a wider dollar basis at year-end 2026 would test the BoJ's USD swap-line readiness. |
| **Market liquidity (16–20)** | Super-long stress raises long-term borrowing costs for insurers/pensions and, via the curve, mortgage and corporate rates. | Term-premium-driven yield rises are not a monetary tightening in the demand-management sense but they do tighten financial conditions; the BoJ treats them as partly fundamental. | This is the group the BoJ has explicitly tied to its purchase plan ("may modify the plan… after reviewing developments in and functioning of the JGB markets"). A functioning DI falling back below ~−30 or a 30y realised-vol spike would, on the 2025 precedent, trigger taper flexibility or targeted purchases, as the IMF recommends. |

Two cross-cutting points. First, the lead-lag structure differs by group: money growth leads inflation by 12–24 months in the BIS evidence; funding spreads lead financial conditions by weeks; market-liquidity deterioration is near-contemporaneous with policy reaction. The tracker should label each panel with its horizon. Second, the sign of "good news" is not uniform: falling excess reserves are *intended* QT progress until the reserve-demand curve steepens, at which point the same series becomes a stress signal. The TONA–IOER spread is the switch that tells the user which regime applies.

---

## 6. Recommended shortlist for first implementation

1. **Policy rate & TONA (daily)** — the anchor; the TONA–target gap is the implementation gauge. *Auto.*
2. **Real policy rate vs. r\* band** — direct link to the existing tracker's Stage 1 and the natural-rate lens. *Computed.*
3. **BIS REER / USD-JPY and a banded MCI** — the yen is the dominant 2026 monetary-conditions variable. *Auto.*
4. **M2 and M3 growth, nominal and real** — the money-view inflation signal, with the BIS regime caveat displayed. *Auto (FRED M3) + BoJ-CSV (M2).*
5. **Bank lending growth** — the credit counterpart, currently diverging from money. *BoJ-CSV.*
6. **Monetary base and BoJ current-account balances (y/y and level)** — the quantity of base liquidity being withdrawn. *BoJ-CSV.*
7. **Excess reserves / bank assets** — the Afonso-et-al. ampleness ratio; the QT guidepost. *BoJ-CSV.*
8. **BoJ total assets and JGB holdings (level, % GDP, % of outstanding)** — the stock effect and taper progress. *Auto (FRED JPNASSETS) + Manual (MoF share).*
9. **TONA − IOER and GC repo − IOER spreads** — the earliest warning of reserve scarcity and collateral tightness. *BoJ-CSV + JSDA scrape.*
10. **3m TIBOR − OIS/TONA spread** — bank term-funding stress. *Auto.*
11. **JGB market functioning DI (Bond Market Survey)** — the official participant read the BoJ conditions its taper on. *Manual, quarterly.*
12. **JGB liquidity indicators: futures bid-ask and price impact, cash turnover** — hard microstructure evidence. *Manual, quarterly.*
13. **Realised 10y/30y JGB yield volatility and 10s30s slope** — computable daily from MoF, the trigger variable in 2025. *Auto.*
14. **3m JPY/USD cross-currency basis** — dollar-funding stress; include if a licensed feed exists, otherwise proxy from FSR and BoJ USD-operation take-up. *Licensed/Manual.*

Deferred to phase 2: Divisia M2 (needs component rates), a Japan proxy policy rate (needs the phase-1 series as inputs), credit-to-GDP gap (quarterly BIS pull is easy but low-frequency), and foreign trading share (JSDA scrape).

---

## 7. Verification notes and caveats

- The 2026 rate chronology conflicts across secondary sources; the sequence used here (0.75% Dec-2025 → 1.0% Jun-2026 → hold Jul-2026) is corroborated by CNBC, Bloomberg, Focus Economics and Oxford Economics and by the BoJ statement URLs cited. One search-engine summary of the July 2026 statement claimed a 1.25% guideline; this is contradicted by all contemporaneous reporting and is treated as an extraction error.
- The May 2026 Bond Market Survey DI values (−16 current, +12 change) come from a search extract of the BoJ PDF and should be confirmed against https://www.boj.or.jp/en/paym/bond/bond_list/bond2605.pdf; the August 2026 values were not readable.
- The June 2026 current-account-balance figure (¥407tn, −16.4% y/y) is from a secondary site and should be replaced by BoJ MD08 data.
- FRED IDs marked "verify" (`RBJPBIS`, `MANMM101JPM189S`, `QJPPAM770A`) follow FRED's OECD/BIS naming convention but were not opened during this review.
- No BoJ Working Paper on a Japanese reserve-demand curve was found for 2025–26; Shiratsuka (2025) is the only estimate located. Whether the BoJ has an internal ampleness threshold is unknown.

---

## References

- Afonso, G., D. Giannone, G. La Spada and J. C. Williams (2022, rev. 2025). "Scarce, Abundant, or Ample? A Time-Varying Model of the Reserve Demand Curve." NY Fed Staff Report 1019. https://www.newyorkfed.org/research/staff_reports/sr1019
- Aldasoro, I. and T. Ehlers (2018). "The geography of dollar funding of non-US banks." *BIS Quarterly Review*, December. https://www.bis.org/publ/qtrpdf/r_qt1812b.htm
- Aldasoro, I., C. Borio and M. Drehmann (2018). "Early warning indicators of banking crises: expanding the family." *BIS Quarterly Review*, March. https://www.bis.org/publ/qtrpdf/r_qt1803e.htm
- Anderl, C. and G. M. Caporale (2023). "Shadow rates as a measure of the monetary policy stance: Some international evidence." *Scottish Journal of Political Economy*. https://onlinelibrary.wiley.com/doi/10.1111/sjpe.12343
- Bank of Japan (2024). *Review of Monetary Policy from a Broad Perspective*, 19 December. https://www.boj.or.jp/en/mopo/outline/bpreview/index.htm
- Bank of Japan (2024). "Developments in the Japanese Money Markets and their Functioning with Excess Reserves." Broad-Perspective Review Series, November. https://www.boj.or.jp/en/research/brp/ron_2024/ron241106a.htm
- Bank of Japan (2026). *Financial System Report*, April. https://www.boj.or.jp/en/research/brp/fsr/fsr260421.htm
- Bank of Japan (2026). "Market Operations in Fiscal 2025," August. https://www.boj.or.jp/en/research/brp/mor/mor260812.htm
- Bank of Japan (2026). "Impact of the Bank of Japan's Reductions in JGB Purchases on the JGB Markets." BoJ Review 2026-E-10, August. https://www.boj.or.jp/en/research/wps_rev/rev_2026/rev26e10.htm
- Bank of Japan (2026). "Developments in the Natural Rate of Interest and the Assessment of the Degree of Monetary Accommodation." BoJ Review 2026-E-4, March. https://www.boj.or.jp/en/research/wps_rev/rev_2026/rev26e04.htm
- Bank of Japan (2026). Statements on Monetary Policy, 16 June and 31 July. https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260616a.pdf; https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260616b.pdf; https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260731a.pdf
- Bank of Japan, *Bond Market Survey* and *Liquidity Indicators in the JGB Markets*. https://www.boj.or.jp/en/paym/bond/index.htm
- Barnett, W. A., M. Chauvet, D. Leiva-Leon and L. Su (2024). "The Credit-Card-Services Augmented Divisia Monetary Aggregates." *JMCB*. https://onlinelibrary.wiley.com/doi/10.1111/jmcb.13088
- Berger, H., S. Karlsson and P. Österholm (2023). "A Note of Caution on the Relation Between Money Growth and Inflation." IMF WP 2023/137; *Scottish JPE* 70(5). https://www.imf.org/en/Publications/WP/Issues/2023/06/30/A-Note-of-Caution-on-the-Relation-Between-Money-Growth-and-Inflation-534322
- Borio, C., B. Hofmann and E. Zakrajšek (2023). "Does money growth help explain the recent inflation surge?" *BIS Bulletin* 67. https://www.bis.org/publ/bisbull67.pdf
- Borio, C. (2024). "Money growth and the post-pandemic inflation surge: updating the evidence." BIS speech, 24 January. https://www.bis.org/speeches/sp240124.htm
- Borio, C., R. McCauley, P. McGuire and V. Sushko (2016). "Covered interest parity lost: understanding the cross-currency basis." *BIS Quarterly Review*, September. https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- Carriere-Swallow, Y., G. Kindberg-Hanlon and D. Smirnov (2025). "Macroeconomic Effects and Spillovers from Bank of Japan Unconventional Monetary Policy." IMF WP 2025/227. https://www.elibrary.imf.org/view/journals/001/2025/227/article-A001-en.xml
- Choi, J., T. Doh, A. Foerster and Z. Martinez (2022). "Monetary Policy Stance Is Tighter than Federal Funds Rate." *FRBSF Economic Letter* 2022-30. https://www.frbsf.org/research-and-insights/publications/economic-letter/2022/11/monetary-policy-stance-is-tighter-than-federal-funds-rate/
- Drehmann, M. and K. Tsatsaronis (2014). "The credit-to-GDP gap and countercyclical capital buffers: questions and answers." *BIS Quarterly Review*, March. https://www.bis.org/publ/qtrpdf/r_qt1403g.htm
- Du, W., K. Forbes and M. Luzzetti (2024). "Quantitative Tightening Around the Globe: What Have We Learned?" NBER WP 32321. https://www.nber.org/papers/w32321
- Ericsson, N., E. Jansen, N. Kerbeshian and R. Nymoen (1998). "Interpreting a Monetary Conditions Index in Economic Policy." *BIS Conference Papers* 6. https://www.bis.org/publ/confp06i.pdf
- Freedman, C. (1995). "The Role of Monetary Conditions and the Monetary Conditions Index in the Conduct of Policy." *Bank of Canada Review*, Autumn.
- Fukuma, N., T. Kitamura, K. Maehashi, N. Matsuda, K. Takemura and K. Watanabe (2024). "The Impact of QQE and YCC on the Functioning of the JGB Market." BoJ WP 24-E-9. https://www.boj.or.jp/en/research/wps_rev/wps_2024/wp24e09.htm
- IMF (2026). *Japan: 2026 Article IV Consultation*, Country Report 26/75. https://www.imf.org/en/publications/cr/issues/2026/04/02/japan-2026-article-iv-consultation-press-release-staff-report-and-statement-by-the-575112
- IMF (2026). *Global Financial Stability Report*, April, Chapter 1. https://www.imf.org/-/media/files/publications/gfsr/2026/april/english/ch1.pdf
- Kumhof, M. and M. Salgado-Moreno (2024). "Quantitative easing and quantitative tightening: the money channel." BoE Staff WP 1090. https://www.bankofengland.co.uk/working-paper/2024/quantitative-easing-and-quantitative-tightening-the-money-channel
- Kurosaki, T., Y. Kumano, K. Okabe and T. Nagano (2015). "Liquidity in JGB Markets: An Evaluation from Transaction Data." BoJ WP 15-E-2. https://www.boj.or.jp/en/research/wps_rev/wps_2015/wp15e02.htm
- Nakazawa, T. and M. Osada (2024). "The Bank of Japan's Large-Scale Government Bond Purchases and the Formation of Long-Term Interest Rates." BoJ WP 24-E-10. https://www.boj.or.jp/en/research/wps_rev/wps_2024/wp24e10.htm
- Sakiyama, T. and S. Kobayashi (2018). "Liquidity in the JGB Cash Market: An Evaluation from Detailed Transaction Data." BoJ Research Paper, March. https://www.boj.or.jp/en/research/brp/ron_2018/data/ron180329a.pdf
- Shiratsuka, S. (2025). "Toward a Guidepost for Quantitative Tightening: The Case of the Bank of Japan." HIAS-E-146; *Japanese Economic Review*. https://hias.hit-u.ac.jp/wp-content/uploads/2025/09/HIAS-E-146.pdf
- Sokic, A. (2025). "Revisiting the Money Growth and Inflation Nexus in the United States: New Evidence From a Wavelet Approach." *Bulletin of Economic Research*. https://onlinelibrary.wiley.com/doi/10.1111/boer.70072
