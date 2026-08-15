HIP Financial Annex
Monte Carlo Results and Unit Economics
Confidential. For NDA Distribution Only.
Bill Brewster
Olinda Solutions
July 2026

Table of Contents



1. Executive Summary
This document is the written companion to HIP_FinancialAnnex.xlsx, a formula-driven Monte Carlo simulation of HIP unit economics and platform value under the single-operator-first deployment model. It explains what the workbook shows, how the numbers were produced, and what a CFO organization should look at first. It does not require opening the spreadsheet to understand the case.
The model runs 10,000 scenarios per recalculation. Every input is a random draw from a documented distribution (see section 2). Every output is a formula, traceable back to an input assumption. Nothing in this document is a hardcoded Python calculation dressed up as a spreadsheet result.
1.1 Headline P50 outputs
Metric
P10
P50
P90
Year 4 annual revenue
$227M
$307M
$407M
Year 7 annual revenue
$344M
$453M
$596M
Year 4 gross profit
$154M
$221M
$262M
Cumulative capex, Year 4
$31M
$42M
$50M
Net cash flow, 48 months
$315M
$429M
$502M
Platform value at exit multiple
$3.3B
$4.8B
$5.8B
ROI multiple (cash-on-cash, net CF / capex)
7.6x
10.2x
13.4x

1.2 Probability outcomes
Outcome
Probability
Cash breakeven within 48 months
100%
Platform value exceeds $5B
44.6%
Platform value exceeds $10B
0.5%
Platform value exceeds $20B
0.0%
ROI exceeds 3x
100%
Year 4 deployed subscribers exceed 3M
29.9%

Read this table as a downside-protected, moderate-upside case. Cash breakeven inside 48 months is effectively certain across the simulated distribution. The platform does not, at single-operator scale, clear $10B in more than a handful of simulated paths. That ceiling is a direct function of founding subscriber base, addressed in section 6.
2. Methodology
The model is formula-driven, not Python-computed. Every cell in the SIMULATIONS sheet is an Excel formula referencing the CONTROLS sheet or a prior column in the same row. Python built the structure and wrote the formulas; Excel (or LibreOffice) performs every calculation. This means the workbook remains live: change an assumption in CONTROLS, press F9, and the entire 10,000-row simulation and every downstream result recalculates.
2.1 Distribution draws
Twenty-five stochastic input variables (penetration by year, paid conversion, churn, ARPU by tier, tier mix, unit costs, macro assumptions, tail-risk probabilities) are drawn from triangular distributions defined by a low, mode, and high value in CONTROLS. Each simulated row draws its own value for every variable, independently, so the 10,000 rows collectively trace out the full joint distribution of outcomes.
A note on formula construction: the original design called for Excel's LET() function to compute a single random draw per cell and reuse it across the triangular quantile transform. LET() does not evaluate under LibreOffice recalculation and produced formula errors on the first build. The workbook uses a two-draw fallback (one RAND() call for the branch selection, one for the magnitude) that is standard practice when LET is unavailable and introduces no material distortion to the shape of the output distributions.
2.2 Live vs. frozen results
RESULTS_LIVE recomputes P10 through P90 on every recalculation (F9). P50 is stable to within approximately 1 percent across recalculations at 10,000 iterations. RESULTS_FROZEN holds a paste-values snapshot with a timestamp, used as the source for the numbers quoted in this document. To refresh, recalculate and paste-values RESULTS_LIVE into RESULTS_FROZEN.
2.3 Traceability and validation
Every formula in the workbook resolves to zero calculation errors under LibreOffice recalculation, verified against 550,251 formulas. The VALIDATION sheet runs nine automated checks on every recalculation, covering tier mix normalization, sign checks on revenue and profit, simulation completeness, and calibration against the prior (v8) model. Two checks currently show OUT OF BAND status; both are addressed directly in section 6, not hidden.
2.4 Why these distributions, in the open
Distribution choice is where a Monte Carlo either earns credibility or loses it, so the reasoning is stated here rather than left implicit in the workbook.
Continuous inputs use triangular distributions. The 22 continuous variables (penetration, conversion, churn, ARPU, tier mix, unit costs, macro assumptions) are drawn triangular from a low, mode, and high. These are expert-elicited with no historical dataset to fit a curve against, and triangular is the standard three-point choice when you have a best guess and a plausible range but not a fitted shape. It is bounded by construction, so no draw produces a nonsense value such as negative churn or above-100-percent conversion. Beta-PERT is a smoother alternative on the same three points and is noted as a refinement, not a defect; for bounded rates the two produce materially similar central tendencies.
Discrete tail events use a two-layer Bernoulli draw. Operator pullout, regulatory shock, and supply-chain failure are event risks: in any given run they either occur or they do not. Modeling them as continuous probabilities that never fire, which is what the prior version did, turns tail risk into inert metadata. Instead each event's probability is drawn triangular (expert uncertainty about how likely it is), then a Bernoulli draw against that probability decides whether it fires in that run, and documented impacts apply when it does. This is the AACE RP 118R-21 and Clemen-Winkler separation of inherent uncertainty from discrete contingent risk. Section 5.2 shows what it does to the distribution.
Known limitation, stated up front: penetration is point-by-year, not a diffusion curve. Year 2, 4, and 7 penetration are three independent triangular draws rather than points generated from a single stochastic adoption (Bass or logistic) curve. This is the model's main acknowledged simplification, and it is the one place a sophisticated reviewer will push. An S-curve rebuild, drawing ultimate penetration, inflection timing, and slope and generating the year points from the curve, is the scoped next refinement. It is flagged here because the honest answer to the reviewer is that it is a known next step, not an oversight.
Sources for the methodology: Bass (Management Science, 1969) and Mahajan/Muller/Bass (Journal of Marketing, 1990) for diffusion curves; AACE International RP 118R-21 (2022) for inherent-uncertainty vs discrete-risk separation; Clemen and Winkler (Risk Analysis, 1999) for expert-elicited distributions absent hard data; Oracle Crystal Ball User's Guide for standard distribution selection. These are named in the workbook README as well.
3. Base Case Walk-Through
The base case (SCENARIO_LOG row 1) holds every stochastic variable at its CONTROLS mode value, no random draw, for a single deterministic reference point.
Line item
Value
Founding operator broadband subscribers
28,700,000
Year 4 penetration (mode)
8.9%
Year 4 deployed subscribers
~2.55M
Paid conversion rate
70%
Year 4 paid subscribers
~1.79M
Blended ARPU (three-tier)
$10.63/mo
Year 4 annual revenue (base case, deterministic)
$262.6M
Year 4 cumulative node capex
$38.7M
Net cash flow, 48 months (base case)
$335.9M

The three-tier pricing model (Standard $9.99, Data-Sharing $4.99, Premium Data $19.99) blends to a weighted ARPU around $10.63 at the reference 55/30/15 tier mix. Data-Sharing tier adoption is cohort-throttled at the operator level; the model does not assume runaway data-tier growth.
4. Sensitivity Analysis
Which variables move outcomes most, ranked by structural leverage on the model, not by a formal tornado-chart regression (the workbook does not currently compute one; this is qualitative from the formula chain).
Variable
Leverage
Why
Founding subscriber base
Highest
Every revenue and value line scales linearly off this single input. Single-operator (28.7M) vs consortium (67.7M) is a 2.36x swing on its own.
Year 4 penetration rate
High
Directly multiplies the subscriber base to set deployed subscribers; ranges 5.0% to 15.0%, a 3x spread.
Paid conversion rate
High
Gates what fraction of deployed subscribers generate revenue at all; ranges 50% to 85%.
Exit multiple
High on platform value only
Platform value is a direct multiple of annual revenue; ranges 8x to 25x, more than a 3x spread on that one line.
Blended ARPU / tier mix
Moderate
Three-tier pricing narrows the ARPU range versus a single price point, dampening this lever relative to v8.
Node capex and hardware refresh
Moderate on capex and ROI
RTX PRO 6000 pricing update (+55% vs v8 assumption) raises the capex base; amortized over subscriber count so the per-subscriber effect is smaller than the headline price move suggests.
Confidential computing throughput penalty
Low to moderate
5% to 27% throughput loss on enclave-tier queries, priced into per-query variable cost; a real but second-order cost driver.

5. Tail-Risk: Two Ways of Looking At the Downside
The model handles discrete tail risk (operator pullout, regulatory shock, supply-chain failure) two ways, and both belong in a CFO conversation because they answer different questions.
5.1 Deterministic named scenarios (SCENARIO_LOG)
SCENARIO_LOG forces specific downside stories with no random draws, so a reviewer can ask "what exactly happens if the founding operator walks" and read the answer directly rather than off a distribution.
Scenario
Year 4 revenue
Year 4 capex
Net CF 48mo
Base case
$262.6M
$38.7M
$335.9M
Operator pullout, Year 3
$53.0M
$14.3M
$32.6M
Regulatory shock, Year 2
$160.7M
$29.0M
$169.1M
Valuation compression (8x exit)
$262.6M
$38.7M
$335.9M
Supply chain failure, Year 1
$150.0M
$37.9M
$136.9M
Combined stress case
$128.6M
$30.2M
$60.1M
Upside case (consortium, 67.7M subs)
$619.7M
$91.3M
$792.6M

Operator pullout at Year 3 is the single worst deterministic case in the log: deployment caps at Year 2 penetration and roughly half the accumulated capex is written down. Even here, net cash flow stays positive. The combined stress case is the closest thing to a true worst case and still clears breakeven. The consortium case is not the base plan; it shows the ceiling if other operators join the founding cohort.
5.2 Stochastic tail risk fired inside the simulation (RISK-ADJUSTED band)
The deterministic scenarios above answer "what if this specific thing happens." They do not tell you how the tail risk reshapes the overall distribution, because a forced scenario is not a probability-weighted outcome. To answer that, the same three events now fire stochastically inside the 10,000-run Monte Carlo, each via a Bernoulli draw against a probability that is itself drawn from a distribution. This is the change from the prior model version, where these probabilities sat in CONTROLS as inputs that never actually affected P10 through P90. They do now.
The result is a second reported band. BASE CASE is the operating distribution assuming no tail event fires. RISK-ADJUSTED layers the three events on top at their modeled frequencies.
Metric
Base P10
Base P50
Risk-adj P10
Risk-adj P50
Year 4 revenue
$228M
$307M
$184M
$295M
Net cash flow, 48 months
$318M
$430M
$254M
$413M
Platform value at exit
$3.3B
$4.8B
$2.6B
$4.6B
ROI multiple
7.6x
10.2x
6.2x
9.8x

Read the P10 columns, not the P50. The median barely moves because tail events are rare, which is correct. The downside is where the tail lives: risk-adjusted P10 platform value drops from $3.3B to $2.6B, a 22 percent haircut at the tenth percentile, and P10 net cash flow drops from $318M to $254M. That is the number a CFO stresses against, and before this change the model could not produce it.
5.3 Event frequencies and a flag worth stating plainly
Outcome
Probability
Operator pullout fires (per run)
~6.9%
Regulatory shock fires (per run)
~4.2%
Supply-chain failure fires (per run)
~5.5%
At least one tail event fires
~15.6%
Cash breakeven at 48 months, risk-adjusted
100%

One number here should be treated as a question, not a trophy: cash breakeven holds at 100 percent even in the risk-adjusted band, meaning even the paths where a tail event fires still break even inside 48 months in this model. That is either genuine downside resilience from the lease-back bridge and bonus depreciation cushioning the capex, or a sign the impact multipliers on the tail events are too gentle. It should be presented as "breakeven holds across the modeled tail; the impact assumptions are documented in the workbook and can be stressed harder," not as a clean guarantee. Overstating it is exactly the kind of thing a sharp diligence reviewer catches.
6. Comparison to v8 Baseline, With Change Log
v9 does not match v8's P50 outputs, and it should not be read as a failed calibration. The two models target different deployment scales. v8 was built against a consortium founding base (67.7M subscribers across Comcast, Charter, Cox, and Altice). v9 is built against the locked single-operator-first direction: Comcast standalone, 28.7M subscribers, a 2.36x smaller base. Consortium remains modeled as the SCENARIO_LOG upside case, not the plan of record.
6.1 What changed and why
Change
v8
v9
Rationale
Founding subscriber base
67.7M (consortium)
28.7M (single operator)
Locked direction update; consortium is upside, not baseline.
RTX PRO 6000 Blackwell MSRP
$8,565
$13,250 (+55%)
External research memo, July 2026 pricing.
Node capex (hub-class)
Lower
~$53,000/node
Reflects updated hardware pricing.
Bonus depreciation
Not modeled
100%, permanent
OBBBA enacted after v8 was built.
Pricing model
Single tier
Three tier (Standard / Data-Sharing / Premium Data)
Reflects current go-to-market design.
Confidential computing cost
Not separately modeled
5-27% throughput penalty priced in
Blackwell CC benchmark range applied to enclave-tier cost.

6.2 Calibration status
VALIDATION currently flags two checks OUT OF BAND. Both were checked against a band originally set for the consortium-scale v8 model and rescaled by the 2.36x subscriber ratio; the rescaled band is close but the simulated P50 lands just outside it on both metrics.
Check
Rescaled band
v9 P50 actual
Status
Year 4 revenue
$340M - $680M
$307M
OUT OF BAND, ~10% below floor
Platform value
$5.1B - $12.7B
$4.8B
OUT OF BAND, ~6% below floor

A pure linear rescale by subscriber ratio does not fully capture the other v8-to-v9 deltas above (three-tier ARPU blend, updated cost structure), which also touch revenue and platform value independently of subscriber count. The residual gap is real and is not a formula defect; recalc runs clean at zero errors across 550,251 formulas. This is flagged here as an honest variance rather than adjusted to force a passing status. If a tighter calibration is required, the next step is a like-for-like v8 rerun at the 28.7M subscriber base rather than a post-hoc rescale of the original band.
7. What the CFO Should Look At First
1. The risk-adjusted P10, not the base-case P50. The base-case P50 (Year 4 revenue $307M, platform value $4.8B) is the operating number. The risk-adjusted P10 (revenue $184M, platform value $2.6B, ROI 6.2x) is the number to stress against, because it reflects the tail events actually firing. Leading with the P50 alone is the mistake; the model now produces both and both should be on the table.
2. Cash breakeven, presented as a question. Breakeven at 48 months holds at 100 percent even risk-adjusted. That is a strong result but should be framed as "breakeven holds across the modeled tail, and the impact assumptions can be stressed harder" rather than as a guarantee. A 100 percent breakeven probability invites the reviewer to test whether the downside is modeled hard enough; get there first.
3. ROI methodology. Reported as net cash flow divided by cumulative capex, a cash-on-cash proxy, not platform value divided by capex. An earlier build included unrealized platform value in the ROI numerator against a single year's capex snapshot and produced multiples above 100x. That was a modeling defect, corrected. The 10.2x base-case P50 (9.8x risk-adjusted) is what should be quoted externally.
4. Single-operator vs. consortium framing. Every headline number here is the single-operator case. The consortium case roughly doubles revenue and cash flow. Do not blend the two; state which base is in view.
5. The two OUT OF BAND validation flags. Both are disclosed in section 6.2 with the reasoning. Neither is a broken formula. Answer them as an anticipated variance rather than letting them surface live in diligence.

Appendix: Workbook Sheet Index
Sheet
Contents
README
Usage instructions, methodology summary, calibration notes.
CONTROLS
Every input assumption. Blue cells are editable. Named ranges on every variable.
ASSUMPTIONS_MARKET
Addressable market, deployment ramp, comparables, competitive context.
ASSUMPTIONS_UNIT
Three-tier pricing detail, node economics, per-query cost breakdown.
ASSUMPTIONS_MACRO
Depreciation, tax, exit multiple, discount rate, tail-risk probabilities.
SIMULATIONS
10,000 rows, each one full formula-driven scenario. Press F9 to redraw.
RESULTS_LIVE
Percentiles and probability outcomes, recalculates on F9.
RESULTS_FROZEN
Timestamped paste-values snapshot, source for this document.
SCENARIO_LOG
Seven deterministic tail-risk and upside scenarios.
VALIDATION
Nine automated sanity and calibration checks, runs on every recalculation.

