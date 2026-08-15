# WP / NDA Diligence Review -- Punch List
Status: BUILT
Reconciled-Against: HIP_WhitePaper_Confidential__v20260712_1602.docx, HIP_EcosystemAnalysis_NDA__v20260712_1602.docx
Produced: 2026-07-12 17:42 MT (read-only review -- no edits made)
Reviewer: Sonnet 4.6

---

## Scope

Review of two documents:
- `HIP_WhitePaper_Confidential__v20260712_1602.docx` (Parts I-XIV, References)
- `HIP_EcosystemAnalysis_NDA__v20260712_1602.docx` (Sections 1-12, 40-firm map)

Checking: (1) strategy consistency, (2) honesty discipline, (3) WP-vs-NDA alignment, (4) diligence readiness. Read-only.

---

## 1. Strategy Consistency

### SOLID

**Multi-member thesis.** Both documents are built around it end to end. WP Part I defines the four-layer architecture as household-scoped by design. NDA Section 1 opens with "the household operating system." Consistent throughout.

**Dyad beachhead -- 63.7% cited and sourced.** WP Part III cites "63.7 percent of US households are one- or two-person households: 38.5 million living alone and 45.7 million in two-person households, out of 132.2 million total. (Source: Census CPS ASEC Historical Households Tables HH-4.)" The figure is specific, attributed, and matches the Census series it cites. NDA Section 1 and Layer 0 size the market against the same household topology. Consistent.

**Eldercare wedge and CMS GUIDE.** WP Part IX cites GUIDE Model correctly: "CMS launched the GUIDE Model in July 2024, an eight-year national dementia care coordination program paying providers approximately 4,000 to 6,000 dollars per enrolled beneficiary per year." NDA Section 2.3 sizes the eldercare vertical with the GUIDE reimbursed path as a distinct upside scenario. Both state explicitly that GUIDE is policy-dependent upside, not banked revenue. Consistent and appropriately scoped.

**Operator-blind/model-neutral/multi-principal moat.** WP Part XII (nine-layer sort) explicitly separates: (1) routing cascade as margin, (2) injection contract as context moat, (3) operator-blind architecture as liability moat, (4) governance harness as compliance moat. NDA Section 6 states the competitive separation on the same axis for all five identified competitors. Consistent.

**OP-1 through OP-5 as expansion roadmap.** WP Part XII and NDA Section 11 both enumerate the five open problems with identical framing (what it is, why hard, why deferral is safe, line of attack). The five problems (minors/consent, relational facts, competence-aware disclosure, dynamic sensitivity, coercion) are presented as research assets with safe-failure proofs, not product gaps. Consistent and strong diligence position.

### STALE

**Voice governance -- WP Part II caveat is no longer accurate.** WP Part II trust boundary section states: "Voice-path hardening to run that same enforcement chain end to end is open engineering work, tracked in the debt register as Code Review Finding 4." BUILD-1 (commit fbcd372) closed this finding. It routed OrchestratorGate._on_user_text through assemble_governed_context at all three sites and is gated by the VOICE conformance suite (VOICE-GOV-001..004, ratcheted PASS). The WP is describing a resolved gap as open. This will confuse a technical diligence reviewer who reads the WP and then runs the harness. The WP caveat should be updated to state that voice-path governance is implemented and gated, with BUILD-1 cited.

---

## 2. Honesty Discipline

### CRITICAL -- FIX BEFORE DILIGENCE

**SIA classification quality: WP says 90.2%, actual is 85.7%.** WP Part II trust boundary section states: "Overall classification quality across the full 133-entry corpus is 90.2 percent." The verified current figure, documented in SIA_SHIP_BAR__two-gate-conformance__v20260711_0842.md and confirmed against harness_baseline.json, is 85.7% (114/133 entries, Gate B, which requires >= 90%). Gate B is red -- below the 90% UX quality target. The 90.2% figure was accurate at an earlier point in development and was left in the WP without being updated after the Gate B failure was documented. Any engineer running the harness during diligence will see 85.7% (or slightly improved post-b0ba39d, but still below 90%) and the WP's claim will fail on contact. This is the single highest-priority honesty fix: update WP Part II to state the current verified figure, label Gate A separately (26/26 governance-critical entries, 100% PASS) and Gate B (133 total, 85.7% as of v20260712, below the 90% UX target with Phase B cutover deferred).

### ACCURATE -- GOOD HONESTY PRACTICE

**Household-held key recovery: correctly disclosed as not yet built.** WP Part III (privacy force field note section) states: "A household-held recovery design that would end operator sole custody is specified in the architecture research but not yet built, and the platform makes no claim of household key control today." This is a precise, honest disclosure. It pre-empts a common diligence question without overclaiming.

**GLM-5.2 capability characterization: precise and honest.** WP Part IV states: "On the hardest software-engineering benchmarks it still trails materially. The claim to make is therefore precise: open-weight models now reach near-frontier performance on a wide range of coding and agentic tasks, at a fraction of the cost, while still trailing on the most demanding work." This is the accurate characterization. The document explicitly flags the honest version and explains why it is stronger than an inflated claim.

**Lease-back bridge risk case: explicitly stated.** WP Part VIII states all five risk factors with source attribution: spot rate collapse up to 88%, token compression ~600x, ~6-year depreciation, customer internalization, no exact precedent. The document then explains why each risk is survivable given the bridge is a transition mechanism, not a standing business. This is diligence-friendly structuring.

**Confidential computing enclave: no claim of current ship.** WP Part XII adopts the enclave layer as "partner co-build" and tags it as an enabling layer, not a shipped feature. This is accurate to the current state.

### REVIEW -- VERIFY BEFORE EXTERNAL USE

**"$1.01 trillion in unpaid labor annually" (NDA Section 2.3).** Attributed to AARP and the National Alliance for Caregiving, Caregiving in the US 2025. Prior AARP publications have cited similar figures ($17,600/caregiver/year in 2019 at 53M caregivers). At 59M caregivers, $1.01T implies roughly $17,100/caregiver/year, which is plausible. Verify the 2025 report cites this figure explicitly before external use -- previous NDA versions cited a 2019 report and this appears updated to the 2025 version but should be confirmed.

**~80% framing: not found in current versions.** No unlabeled or refuted ~80% household stat appears in either document. The household topology figures are the 63.7% Census figure (sourced) and the McPherson et al. 2006 "mean number of core confidants" decline (cited to American Sociological Review). If a prior WP version had an ~80% problem, the current v20260712_1602 versions do not carry it. No action needed unless a prior draft circulated externally.

**NDA Section 2.3 -- eldercare coordination spend: $40/mo, 35% adoption.** These are the model's soft inputs and the NDA correctly labels them as such: "The adoption rate, price, and capture share are the soft inputs the pilot replaces." A diligence reviewer will note these are assumptions, not observed data. The honest labeling is correct; just confirm the assumptions are not presented as market data in any verbal presentation.

---

## 3. WP-vs-NDA Alignment

### ALIGNED

**Pricing structure.** WP Part XI discloses Standard at $9.99/mo, Data-Sharing at $4.99/mo, Premium Data at $19.99/mo, blended ARPU approximately $10.63. NDA Layer 0 uses $10/mo as the reference midpoint for the operator revenue line sizing. Consistent.

**OP-1..5 descriptions.** WP Part XII and NDA Section 11 use the same five-item list with the same framing, the same "why deferral is safe" structure, and the same "line of attack" format. Consistent and clearly generated from the same underlying spec (GOVERNANCE_SCOPE_v1, fc5721a).

**Competitive separation on operator-edge custody.** WP Part XII (owned layers) and NDA Section 6 (five competitors) both converge on the same separating claim: operator-edge deployment, enclave-grade custody, institutional integration at a regulated-operator trust level. Competitors are described consistently across both documents.

**Layer 0 operator base counts.** WP Part VII cites Comcast ~200 edge locations, Charter 1,000+, Cox ~30. NDA Layer 0 cites Comcast approximately 31M subscribers, Charter approximately 36M (post-Cox acquisition). These are different fields (facilities vs subscribers) and are consistent -- neither conflicts with the other.

### MISALIGNMENT / GAP

**SIA 90.2% appears only in WP, not NDA.** The 90.2% figure appears in WP Part II. NDA Section 1 and the technical description in Section 11 do not cite this figure. The NDA therefore does not inherit the error, but both documents must state the same verified current figure after the WP correction. After the WP is updated to reflect the actual 85.7% Gate B / 100% Gate A two-gate picture, verify NDA does not contain a stale figure from an earlier sync.

**Voice governance BUILD-1 closure not reflected in either document.** Both WP Part II and neither the NDA explicitly addresses the voice governance state post-BUILD-1. The WP needs the correction (noted above in Strategy Consistency -- STALE). The NDA's Section 11 OP descriptions do not mention voice governance and need no change on this point.

**Cohort throttling cap: WP Part XI describes the mechanism but gives no numerical ceiling.** WP Part XI.2 says the ceiling is "set per operator" but gives no reference range. NDA Section 9 references the 17.5% take rate but does not address the Data-Sharing tier mechanics. A sophisticated investor reading the WP will ask: what is the operator-level cohort cap, and how does it translate to a ceiling on Data-Sharing tier revenue? The NDA does not answer this. Not a contradiction, but a gap that will surface in Q&A.

---

## 4. Diligence Readiness

### WILL BE FOUND HOUR ONE

**SIA Gate B discrepancy (90.2% claimed vs 85.7% actual).** Any engineer given access to the repository and the WP will run the SIA conformance suite and get 85.7% (or marginally better post-b0ba39d). The WP's 90.2% claim will fail on first contact. This is not a subtle gap -- it is a headline technical claim in the trust boundary section that is contradicted by the test suite the WP itself advertises. Fix the WP before any external distribution. The corrected language should: (a) present Gate A (26/26 governance-critical entries, 100% PASS) and Gate B (133 total, 85.7% as of v20260712, below the 90% UX quality target) separately; (b) note that Phase B cutover is gated on Gate B reaching 90% and that cutover is Bill's call; (c) cite the SIA_SHIP_BAR document if the diligence package includes it.

**TD-101b: /api/decrypt is unauthenticated.** Any engineer reviewing the codebase will find /api/decrypt at demo_dashboard.py:187-199 within the first hour. This endpoint is documented in the HIP_DebtRegister_NDA_Appendix as the highest-severity open item. The NDA appendix is the correct place for it, and including that appendix in the diligence package is the right disclosure posture. Confirm the appendix is in every diligence package. The WP itself does not mention /api/decrypt, which is appropriate -- a forward-looking WP is not a vulnerability disclosure log. Just ensure the appendix is included.

**PKG-7: HIP_DebtRegister_NDA_Appendix is untracked and unregistered.** Per the reconciliation report (RECONCILIATION__v20260712_1347.md), HIP_DebtRegister_NDA_Appendix__v20260711_2312.md is not committed to git and not registered in MANIFEST Section B. It is an orphaned artifact by MANIFEST governance rules. Until it is committed and registered, it cannot be reliably included in a diligence package. This is a packaging gap, not a content gap.

### INVESTOR / ENGINEER CHALLENGES

**No paying subscribers, no signed operator.** Both documents are explicit that HIP v1 is built but not deployed commercially. The moat argument depends on "begin accumulating context first" -- a diligence reviewer will ask: what is the pilot plan, who is the first operator, and what is the signed commitment? Neither document answers this. The WP's "why now" argument (Part IX) is structural; the investor will want a tactical answer about the path to first dollar. This is not a document deficiency -- it is a stage-appropriate gap. Have a one-page pilot plan ready for the follow-on meeting.

**Lease-back bridge has no signed offtake.** WP Part VIII correctly states: "The realistic contract structure is reserved or committed offtake rather than pure on-demand, because both sides want certainty." Then it cites no signed agreement. An investor will ask for a term sheet, LOI, or even a conversation log with a neocloud buyer. Not a WP deficiency -- the document is honest about this -- but prepare a response. "We can have a signed LOI within 30 days of operator deployment commitment" is the right answer structure.

**Data-Sharing tier cohort cap: what is the number?** WP Part XI.2 describes the throttling mechanism clearly but gives no reference cap figure. An investor will model the revenue sensitivity of the Data-Sharing tier and need a bounding assumption. Prepare a one-line answer: e.g., "Cohort cap is set at X% of subscribers per operator deployment, adjustable by the operator." The document does not need to name it; the Q&A should be ready.

**Voice governance: BUILD-1 closed, but voice is not yet on /demo.** After the WP is updated to reflect BUILD-1 closure, a diligence reviewer will ask to see voice governance in action. The demo currently shows no epistemic record for voice turns (FLAG-8, by design -- silent panes are correct until D-1 ships). Be prepared to explain that the governance enforcement is running and gated (VOICE-GOV-001..004), but the demo visualization is a pending work item (D-1 dependent). This is honest and defensible.

### SOLID -- NO ACTION NEEDED

**Lease-back risk case.** WP Part VIII states every risk factor, the sourced evidence for each, and why each is survivable given the bridge is temporary. An investor who reads Part VIII cannot claim they were not told the downside. Strong diligence posture.

**OP-1..5 named open problems.** Both documents present these proactively with safe-failure proofs. NDA Section 11 closes with: "a diligence reviewer who finds an unnamed gap is more concerned than one who finds a named problem with a safe-failure proof and a line of attack." This is the correct frame. Guardianship (OP-1) and competence-aware disclosure (OP-3) are correctly identified as the hardest problems and presented as frontier research assets.

**Memory hierarchy argument.** WP Part V sourced figures are specific (TrendForce, DRAMeXchange, Micron Q3 FY2026, Orennia). The HBM vs NAND spread claim is stated accurately: "The strong claim is about levels, not trajectory." The near-term NAND price trajectory caveat is included. An analyst checking these against public sources will find them accurate.

**Cable facility sourcing.** WP Part VII cites operator-attributed figures (Charter <10ms, Comcast "milliseconds") with the attribution explicit: "operator-attributed claims and are presented as such." CableLabs figures are specifically cited. The honest limit (cooling and power constraints for high-density racks) is stated and then resolved: HIP's target hardware is workstation-class and does not need liquid cooling. The operator attribution + honest limit + resolution is a model for how to handle edge-case technical claims.

**Builder section (WP Part X).** Bill's bio is accurate, specific, and relevant: NOC build at Comcast, X1 business case, Canoe Ventures (35M households, 50M set-top boxes, MRC accreditation), Mentis BSS/OSS delivery. The argument that this is the same operational shape as HIP is stated, not asserted as a credential dump.

---

## 5. Priority Fix List

In order of urgency before any external distribution:

| Priority | Item | Location | Action |
|----------|------|----------|--------|
| P0 | SIA Gate B 90.2% vs 85.7% | WP Part II | Update to two-gate picture: Gate A 100%, Gate B 85.7%, Phase B deferred |
| P0 | PKG-7: DebtRegister untracked | Backlog | Commit + MANIFEST register + include in diligence package |
| P1 | Voice governance BUILD-1 closure | WP Part II | Update caveat: Code Review Finding 4 closed by BUILD-1 (fbcd372), voice now gated |
| P2 | Cohort cap not specified | WP Part XI.2 | Prepare Q&A answer; optionally add a range to the document |
| P3 | "$1.01T unpaid labor" source check | NDA Section 2.3 | Verify 2025 AARP report cites this figure explicitly |
| P3 | NDA sync after WP P0 fix | NDA Section cross-refs | Confirm NDA does not carry 90.2% figure anywhere |

---

## 6. What Is Solid

The following claims are well-sourced, honestly framed, and diligence-ready as written:

- 63.7% household topology (Census, specific table cited)
- CMS GUIDE Model (July 2024, $4K-$6K per beneficiary, 8-year program)
- Open-weight model capability gap (Epoch AI, GLM-5.2 benchmarks, DeepSeek-R1 distilled)
- Memory cost hierarchy (TrendForce, Micron earnings, Orennia)
- Cable facility inventory (operator-attributed, Charter / Comcast announcements, CableLabs)
- NVIDIA AI Grid deployment (Comcast field trial, Charter announcement -- named and live)
- Lease-back bridge economics (Lambda/Runpod/Together/Crusoe rates, Micron SCA structure)
- OP-1..5 open problems (named, safe-failure proofs, lines of attack)
- Household-held key: "not yet built" disclosure
- Builder credentials (Comcast NOC, X1, Canoe, Mentis -- accurate and specific)
- Competitive separation (all five NDA competitors separated on operator-edge custody, not on features)
