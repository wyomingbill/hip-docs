# HIP NDA Package -- Tier-1 Diligence

Status: BUILT
Reconciled-Against: main da9db91 (2026-07-14); MANIFEST as of 2026-07-14
Supersedes: v20260713_1314
Changes from prior version:
- Governance proof artifact added as formal diligence deliverable (Stage 1 item 10, Stage 2 Item 7)
- Financial Annex xlsx reference updated to v20260713_2010 (current post-B38-fix version)
- Secure-site publish note added (Section: Package Completeness Gaps)

Audience: Technologist-investor under NDA + non-compete. Not a competitor. Evaluating the opportunity and the architecture. Deep implementation IP (injection contract internals, D-1 engine, specific acquisition-target intelligence) stays Tier-2 and is not in this package.

This document is the reader's guide and index for the Tier-1 diligence package. It covers: (1) Stage 1 inventory and consistency audit, (2) Stage 2 reading order and document index, (3) cross-reference discipline notes.

---

## Stage 1: Inventory and Consistency Audit

### 1. Confidential White Paper

File: `HIP_WhitePaper_Confidential__v20260712_1852.docx`
MANIFEST status: CURRENT
Last updated: 2026-07-12 (Round 3 -- P0/P1 diligence fixes)

Consistency checks:
- SIA two-gate framing: PASS. Gate A (26/26 governance-critical, 100%) and Gate B (85.7%, Phase B deferred) presented separately. No stale 90.2% figure.
- Voice governance closure: PASS. BUILD-1 (fbcd372) reflected. "Open engineering work, Code Review Finding 4" sentence removed. Voice path now stated as governed through the injection contract.
- 63.7% / 84.2M household dyad figure: PASS (63.7% present and cited).
- 28.7M Comcast SOM: PASS.
- Refuted ~80% framing: PASS -- absent.
- CMS GUIDE Model (July 2024): PASS -- present in Part IX.
- OP-1..5 expansion roadmap: PRESENT (Part II, trust boundary section references deferred scope).
- Operator-blind / model-neutral / multi-principal moat: PASS -- well covered in Part II.
- Cited-vs-modeled discipline: PASS -- modeled figures labeled throughout.
- Em/en dashes: PASS -- none.

**Assessment: HANDABLE. No refresh required before distribution.**

---

### 2. Ecosystem Analysis NDA

File: `HIP_EcosystemAnalysis_NDA__v20260712_1602.docx`
MANIFEST status: CURRENT
Last updated: 2026-07-12

Consistency checks:
- 28.7M Comcast SOM: PASS (operator base section).
- CMS GUIDE Model / eldercare reimbursed path: PASS (Section 2.3, sized in detail).
- Injection contract (INJ-1 through INJ-7): PASS (Section 11 governance boundary).
- OP-1..5 expansion roadmap: PASS (Section 11 v2+ scope).
- 63.7% / 84.2M dyad figure: FAIL -- ABSENT. The market-sizing section references the 80M cable-broadband base and the eldercare demographic, but the 63.7% household composition figure from the verified market research (CPS HH-4) does not appear. The Confidential WP and HIP_STRATEGY both cite it; the ecosystem analysis does not. A reviewer who reads the WP first will notice the missing anchor.
- SIA / Gate A / Gate B: ABSENT. The ecosystem analysis does not discuss the SIA classification layer or two-gate conformance. This is acceptable for a market document; the technical depth is appropriate for the NDA_OpenProblems doc. No stale 90.2% is present.
- Voice governance (BUILD-1): ABSENT. No stale caveat either -- the governance section (Section 11) references the injection contract accurately. This omission is acceptable in a market/partner analysis; it becomes stale only if the doc makes a specific voice claim.
- Governance proof (new): ABSENT -- the ecosystem analysis has no reason to reference the audited transcript; no consistency issue.
- Refuted ~80% framing: PASS -- absent.
- Modeled figures discipline: PASS -- adoption assumptions, TAM layers, and marketplace upside are labeled as assumptions and softest inputs throughout.
- Em/en dashes: PASS -- absent.

**Assessment: MOSTLY HANDABLE with one gap. Gap: 63.7% dyad figure missing from the household market framing. This is the cited structural anchor in both the WP and the strategy doc; its absence in the ecosystem analysis is an inconsistency a careful technologist will catch. Refresh recommendation: one sentence in Section 1 or Section 2 adding "1-2 person households are 63.7% of all US households (US Census CPS ASEC HH-4, 2024), the structural foundation of the trust-dyad segment HIP is built to serve." Single sentence addition, no rebuild of the analysis required. Flag to Bill; do not auto-add without Bill's approval of placement.**

---

### 3. Financial Annex

Files:
- `HIP_FinancialAnnex__v20260713_2010.xlsx` (CURRENT -- live model, v10 with B38 breakeven fix)
- `HIP_FinancialAnnex__v20260702_1913.docx` (STALE -- formatted version, not rebuilt since July 2)

MANIFEST status: xlsx CURRENT; docx STALE

Consistency checks:
- The xlsx model (v20260713_2010) is the current model incorporating all v10 corrections: op_rev_share variable, churn monthly 1.5%/mo mode, exit multiple 3/6/15x with conditional growth adjustment, penetration double-count removed, ecosystem/partner modes reduced, supply-chain capex correlation 25%, reg-shock exit compression 15%, ANNUAL_PL B38 breakeven fixed.
- The methodology and parameter-defense paper (HIP_FinMethodology__parameter-defense__v20260713_1708.md) documents all parameter choices and investor challenges.
- The review memo (HIP_FinModel_ReviewMemo__v20260713_2017.md) confirms cell-level verification of all v10 fixes.
- The docx formatted version (v20260702_1913) predates the SIA spec, harness Phase 2, and all v10 model corrections. MANIFEST explicitly flags it as STALE and warns not to distribute without reconciling against current xlsx.
- No SIA, Gate A/B, or voice governance content -- this is a financial model, not an architecture doc, so that is appropriate.

**Assessment: xlsx is HANDABLE as-is; docx is NOT HANDABLE without a rebuild. For this package, reference the xlsx. Do not include the v20260702_1913.docx as a standalone deliverable until rebuilt. The WP Part VIII narrative covers the financial framing in prose for readers who want text before numbers.**

---

### 4. Market Research (Household Trust-Circle Segment Sizing)

Files:
- `docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-verified__v20260712_1331.md` (CURRENT -- adversarially verified, 26 sources, 24/25 claims confirmed 3-0)
- `docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-external__v20260712_1331.md` (CURRENT -- external analysis, modeled estimates)

MANIFEST status: not individually registered in MANIFEST Section B (they are research artifacts supporting deliverables, not standalone deliverables). Not orphaned; they are cited sources.

Consistency checks:
- 63.7% / 84.2M: PASS (source of truth for this figure; verified against CPS HH-4).
- Cited vs modeled discipline: PASS -- [V], [E], [D] markers throughout.
- Refuted ~80% older-adults-in-1-2-person-HH framing: the verified doc does not use this framing; it presents the raw size distribution correctly.
- Consistent with WP Part III and HIP_STRATEGY Section 4: PASS.
- Governance proof: no intersection -- research artifact, no consistency issue.

**Assessment: HANDABLE as supporting reference material. Verified doc is strong standalone evidence for the dyad beachhead thesis. External doc provides additional modeled estimates with appropriate labeling. Both are appropriate Tier-1 inclusions for a diligence reviewer who wants to trace the 63.7% citation.**

---

### 5. NDA Open Problems / Expansion Roadmap

File: `docs/deliverables/NDA_OpenProblems__expansion-roadmap__v20260713_1100.md`
MANIFEST status: CURRENT

Consistency checks:
- SIA two-gate framing: PASS. Gate A (26/26, 100%), Gate B (85.7%, Phase B deferred pending 90% threshold). Matches WP v20260712_1852.
- Voice governance (BUILD-1): PASS. "The prior caveat ('voice-path hardening is open engineering work') is superseded by this build closure."
- OP-1..5 in detail: PASS -- fully fleshed out with safe-failure proofs and v2+ positions.
- P8 write monotonicity + P10 confirmation gate references: PASS -- these are correct harness Layer 1 scenario IDs, consistent with the governance-proof artifact's scope note (P7-P10 govern internal mechanics, out of scope for the disclosure conformance summary, but correctly cited in this operational context).
- Cited-vs-modeled: not a market doc; no figures requiring the discipline.
- Em/en dashes: PASS -- absent.

**Assessment: HANDABLE. This is the primary architecture depth document for Tier-1. Strong diligence posture.**

---

### 6. Debt Register NDA Appendix

File: `docs/deliverables/HIP_DebtRegister_NDA_Appendix__v20260713_1100.md`
MANIFEST status: CURRENT

Consistency checks:
- BUILD-1 voice closure: PASS -- updated to reflect closure.
- SIA two-gate (Gate A 100%, Gate B 85.7%): PASS -- updated to reflect current state.
- Open items (TD-101b unauthenticated decrypt, TD-108 consent ledger, TD-109 biometric consent): PASS -- present and honestly stated.
- Governance proof: no intersection -- debt register covers open engineering items, not the disclosure conformance summary.
- Consistent with BACKLOG__v20260713_1115.md: PASS.

**Assessment: HANDABLE. Honest open-items disclosure is a strong diligence position. A reviewer who finds a STALE debt register is more concerned than one who finds current honest tracking.**

---

### 7. Technical Annex

File: `HIP_TechnicalAnnex__v20260702_1155.docx`
MANIFEST status: STALE

Consistency checks:
- SIA / CandidateIntent / Gate A / Gate B: FAIL -- all ABSENT. Predates the SIA architecture entirely.
- Four-layer L0/L1/L2/L3 terminology: FAIL -- uses "Layer 1/2/3" in a different sense (4-tier inference cascade, not the current governance layer model).
- INJ-7, injection contract by name: FAIL -- absent.
- Voice governance / BUILD-1: FAIL -- absent.
- Two-gate conformance: FAIL -- absent.

**Assessment: DO NOT INCLUDE in Tier-1 package. STALE against current architecture. A technologist who reads the WP's CandidateIntent / four-layer / SIA framing and then reads this annex will find a document that describes a different architecture. The inconsistency is worse than the gap. Rebuild required before any distribution.**

**Tier-2 note: The TechnicalAnnex also contains implementation-level details (model selections, quantization, Groq API specifics, enclave hardware BOM) that may be Tier-2 even after a rebuild. Flag for Bill on scope decision before rebuilding.**

---

### 8. Prototype Evidence

File: `HIP_PrototypeEvidence__v20260702_1615.docx`
MANIFEST status: STALE

Not checked in detail. MANIFEST note: "last updated before the SIA spec, harness Phase 2, and voice research corpus existed."

**Assessment: DO NOT INCLUDE. STALE. The harness conformance suite and the SIA two-gate conformance results (Gate A 26/26) are the current prototype evidence and are described in the WP and the NDA_OpenProblems doc. The v0702 prototype evidence predates both.**

---

### 9. Architecture Design-Level Material

MANIFEST status: MISSING as a standalone Tier-1 deliverable

The user brief calls for "the governance diagrams, module specs at what-it-does level." Current state:
- DIAGRAM_SPEC__architecture-visuals (da5b84b): SVG content spec for all 7 WP/NDA diagrams (D1 CandidateIntent flow, D2 decision/data plane, D3 trust ladder + P8, D4 proof harness, D5 orthogonal contracts, D6 four-layer arch, D7 P10 confirmation gate) -- SPEC DONE, SVGs NOT BUILT (PKG-3b backlog item, NOT-STARTED).
- GOVERNANCE_SCOPE_v1__LOCKED__v20260712_1245.md (docs/general/): covers what the governance layer does, all four behaviors, the principal taxonomy, and safe-failure proofs -- but it is an internal scope fence, not a polished NDA deliverable.
- HIP_Interaction_Layer_Architecture_and_Roadmap (docs/research-technical/): four-layer model, what changes vs what does not -- internal research doc.

**Assessment: GAP. No standalone Tier-1 architecture overview document exists that is current (SIA-era), polished for a NDA-audience, and suitable as a deliverable. The NDA_OpenProblems doc partially fills this for the governance layer. The Confidential WP Part II fills it for the moat argument. A purpose-built "Architecture for Diligence" doc (what-it-does-level, no implementation code, four-layer model, CandidateIntent pattern, SIA two-gate) would close this gap. This is a Tier-1 content gap -- not a showstopper if the reviewer starts with the WP, but named here for the bill-of-materials.**

---

### 10. Governance Proof -- Audited Transcript and Conformance Summary

File: `docs/deliverables/HIP_GovernanceProof__audited-transcript__v20260714_1345.md`
MANIFEST status: CURRENT
Commit: da9db91 (2026-07-14)

What it is: A human-readable, turn-by-turn audit of a real reveal_demo run (7 turns, 14 engine + shadow records, timestamp 2026-07-14T11:28 UTC) plus a conformance summary covering the six disclosure governance invariants P1-P6. Every disclosure decision is traced to the injection contract clause that produced it. Every withheld fact names the specific INJ rule and gives a plain-English reason. Guard events (INJ-6b empty-set, INJ-7 access-boundary) are documented with timing evidence showing no model call was made.

Consistency checks against other Tier-1 documents:

- **vs. Confidential WP Part II (moat section):** PASS. WP claims "CandidateIntent: every classification is a proposal; the policy envelope is deterministic." The governance proof demonstrates this claim turn-by-turn -- the model is never consulted for access decisions in R06 or R07. No tension.
- **vs. NDA_OpenProblems (P8/P10 references):** PASS. NDA_OpenProblems correctly references "P8 write monotonicity" and "P10 confirmation gate" as harness Layer 1 scenario IDs. The governance proof's scope note explicitly acknowledges P7-P10 as valid harness invariants governing internal mechanics, and states that those external references are correct and require no correction. Consistent.
- **vs. Ecosystem Analysis (Section 11 governance boundary):** PASS. Ecosystem analysis describes the injection contract (INJ-1 through INJ-7) in Section 11. The governance proof is a live-run demonstration of the same contract. No contradiction; the governance proof is the deepest layer of evidence for the Section 11 claims.
- **vs. Debt Register NDA Appendix:** PASS. The debt register discloses TD-101b (unauthenticated /api/decrypt endpoint). The governance proof covers the disclosure path only (process_text_query injection contract), not the decrypt endpoint. No intersection; the debt register's open item is out of scope for the governance proof and is correctly described elsewhere.
- **Honest gap noted in governance proof:** INJ-6b (attr-targeted empty-set, the seam that fired in R06) is marked "asserted, not proven-by-test" -- no dedicated L2 harness fixture exists yet. The fixture spec for this seam is being written as a companion PLAN doc (HARNESS_SPEC__inj6b-attr-empty-set-fixture, same commit). This is an honest, internally consistent position.

**Assessment: HANDABLE. This is the deepest technical evidence layer in the Tier-1 package -- the actual rule-by-rule trace of a live run. It is not required reading for an investor, but it is exactly what a technologist-skeptic will want when evaluating the "rule of law, not rule of the model" claim. It also functions as a demonstration artifact: the reading order (governance proof before or after NDA_OpenProblems) gives the reviewer both the behavioral proof and the architectural context.**

---

### 11. Orphan Check

Files in docs/deliverables/ not in the package or already registered:
- `WP_PartII_TrustBoundary_DRAFT__v20260711_1730.md` and `WP_PartII_TrustBoundary_DRAFT__v20260711_1800.md`: MANIFEST status INTEGRATED. These were working drafts integrated into v20260711_1830 WP. They are correctly not in the Tier-1 package.
- `HIP_GovernanceProof__audited-transcript__v20260714_1330.md`: MANIFEST status SUPERSEDED (by v1345). Correctly not in the active package.

No additional orphans found.

---

## Stage 1 Summary Table

| Doc | Exists | MANIFEST | Consistent | Handable | Action |
|-----|--------|----------|------------|----------|--------|
| Confidential WP v20260712_1852 | YES | CURRENT | YES | YES | Include |
| Ecosystem Analysis v20260712_1602 | YES | CURRENT | MOSTLY | YES (minor gap) | Include; flag 63.7% gap to Bill |
| Financial Annex xlsx v20260713_2010 | YES | CURRENT | YES | YES | Include as xlsx |
| Financial Annex docx v20260702_1913 | YES | STALE | NO | NO | Exclude; rebuild before sending |
| Market Research verified v20260712_1331 | YES | (research artifact) | YES | YES | Include as citation support |
| Market Research external v20260712_1331 | YES | (research artifact) | YES | YES | Include as citation support |
| NDA Open Problems / Expansion Roadmap | YES | CURRENT | YES | YES | Include |
| Debt Register NDA Appendix | YES | CURRENT | YES | YES | Include |
| Governance Proof v20260714_1345 | YES | CURRENT | YES | YES | Include; primary live-run evidence |
| Technical Annex v20260702_1155 | YES | STALE | NO | NO | Exclude; rebuild + scope decision |
| Prototype Evidence v20260702_1615 | YES | STALE | NO | NO | Exclude |
| Architecture overview (Tier-1) | NO | MISSING | -- | -- | Gap; WP fills partially |
| Confidential strategy doc (polished) | PARTIAL | NOT REG. | YES | PARTIAL | Bill's call on format |

---

## Stage 2: Package Index and Reading Order

### What Is in This Package

Eight items constitute the Tier-1 diligence package. Two additional items (Technical Annex, Prototype Evidence) are excluded pending rebuild. One gap (architecture overview) is noted. Reading order below is optimized for a technologist-investor: architecture and moat first, then live proof, then market and economics, then honest open items.

---

### Item 1 -- Confidential White Paper (Start Here)

File: `HIP_WhitePaper_Confidential__v20260712_1852.docx`
Version: v20260712_1852
Format: docx
Audience fit: Both. The technologist reads for Parts I-II (architecture, CandidateIntent pattern, moat, SIA two-gate). The investor reads for Parts III, VII-IX (market forces, cable economics, why now).

What it covers:
- Part I: HIP platform -- the four-tier inference cascade, the governed context layer, what the architecture is and why.
- Part II: The moat -- why multi-principal governance is not closeable with a release; CandidateIntent pattern; Gate A 26/26 governance-critical 100% PASS; Gate B 85.7% quality target and deferred cutover; voice governance closed (BUILD-1); honest speaker-verifier attack surface.
- Part III: Household forces -- 63.7% / 84.2M 1-2 person households [CITED]; 63M caregivers; caregiver remote monitoring 13% to 25% adoption (2020-2025) [CITED]; the care crisis, AI backlash, privacy reactivation.
- Parts IV-VII: Intelligence commoditizes; memory costs; compute location; cable owns the location.
- Part VIII: Economics -- incremental deployment cost, bonus depreciation, lease-back bridge, financial model conservative case.
- Part IX: Why now -- incumbent concessions (Amazon PIN, Apple proximity, Google Voice Match); CMS GUIDE Model (July 2024) reimbursed eldercare path; window defined by moat-building, not market maturation.
- Part X: The builder.

Cross-references: Financial detail traces to the xlsx annex (Item 3). SIA architecture depth and OP-1..5 expansion trace to Item 2. Live governance proof traces to Item 7. Market research citations trace to Item 6.

---

### Item 2 -- NDA Open Problems / Expansion Roadmap (Architecture Depth)

File: `docs/deliverables/NDA_OpenProblems__expansion-roadmap__v20260713_1100.md`
Version: v20260713_1100
Format: md
Audience fit: Primarily technologist. Investor reads Section 1 (technical context) and OP-1..5 summaries.

What it covers:
- Technical context: four governance behaviors (Admit, Refuse with reason, Park, Encrypt per member) and their current harness status. SIA two-gate: Gate A 100%, Gate B 85.7%. Voice governance: BUILD-1 closure restated.
- P8 write monotonicity and P10 confirmation gate: referenced as harness Layer 1 scenario IDs for the Park behavior. Consistent with governance proof's scope note.
- OP-1 through OP-5: each open problem with (what it is, why deferral is safe, why it is defensible IP, v2+ position). These are the expansion roadmap. Naming them is a stronger diligence posture than a quietly narrowed product.
- OP-1 Minors and consent gradients; OP-2 Relational facts / co-ownership; OP-3 Recipient-competence-aware disclosure; OP-4 Contextually variable sensitivity; OP-5 Coercion and duress detection.

Cross-references: Consistent with Confidential WP Part II. Governance behaviors traceable to WP Part I. Live-run demonstration in Item 7 (Governance Proof).

---

### Item 3 -- Financial Annex (Unit Economics)

File: `HIP_FinancialAnnex__v20260713_2010.xlsx`
Version: v20260713_2010
Format: xlsx
Audience fit: Investor primarily. Technologist reads to validate that the economic model is grounded in real operator subscriber counts.

What it covers: op_rev_share (40% mode, triangular draw), 7.5% paid penetration Y4 at Comcast (2.15M subs), exit multiple 3/6/15x with conditional growth adjustment, churn 1.5%/mo mode, ecosystem/partner revenue with zero-inflation ramp, supply-chain capex correlation, reg-shock exit compression, ANNUAL_PL deterministic waterfall Y1-Y7, 10,000-row Monte Carlo SIMULATIONS sheet. Numbers are built bottom-up from public operator subscriber counts.

Companion documents:
- `HIP_FinMethodology__parameter-defense__v20260713_1708.md`: parameter sourcing and investor challenge Q&A.
- `HIP_FinModel_ReviewMemo__v20260713_2017.md`: cell-level verification that all v10 fixes landed; 5 investor attack numbers with defense prep; 6 items requiring Bill's input.

Note: The formatted docx version (v20260702_1913) is STALE and excluded. Bill should rebuild the docx from the xlsx before a formal diligence package delivery if a formatted narrative version is required.

Cross-references: WP Part VIII summarizes the financial framing in prose. The Ecosystem Analysis Section 2 references this model as the base for its Layer 0/1 sizing.

---

### Item 4 -- Ecosystem Analysis NDA (Market, Partners, Competitive Map)

File: `HIP_EcosystemAnalysis_NDA__v20260712_1602.docx`
Version: v20260712_1602
Format: docx
Audience fit: Both. Technologist reads for the four-category firm analysis (tenants, partners, competitors, acquisition targets) and Section 11 governance boundary. Investor reads for the TAM four-layer stack and the 40-firm demand validation.

What it covers:
- Section 1: The substrate thesis -- 40 funded firms each own a slice; HIP owns the layer beneath the slice.
- Section 2: Opportunity sized in four layers: Layer 0 (operator subscription base, $9.6B TAM at $10/mo); Layer 1 (marketplace floor, HIP take); Layer 2 (eldercare anchor vertical, $30B category by 2030, CMS GUIDE reimbursed path); Layer 3 (platform economy, nine-category mesh); Layer 4 (robotics adjacency, emergent modeled).
- Sections 3-10: 40-firm analysis by category (family coordination, eldercare, health data, household finance, smart home, family safety, education, insurance, emerging AI). Each firm: what they wall against, the HIP unlock, strategic classification (tenant / partner / competitor / acquisition target).
- Section 11: v1 scope and v2+ roadmap (consistent with NDA_OpenProblems doc).

Gap flagged: The 63.7% / 84.2M household composition figure does not appear. This is the WP's primary cited anchor for the trust-dyad segment. A careful reviewer will notice the gap between the WP and this document. Recommend adding one sentence in Section 1 or Section 2 before distribution.

Cross-references: Ecosystem Analysis is not a substitute for the Confidential WP. It is the market-and-partner layer that sits on top of the WP's architecture and thesis.

---

### Item 5 -- Debt Register NDA Appendix (Honest Open Items)

File: `docs/deliverables/HIP_DebtRegister_NDA_Appendix__v20260713_1100.md`
Version: v20260713_1100
Format: md
Audience fit: Technologist primarily. Investor reads the summary-level entries (SEC and GATE severity items).

What it covers: Active tech debt with severity classification (SEC, GATE, ENG, OPS). Most significant open items for a Tier-1 reviewer:
- TD-101b: /api/decrypt endpoint currently unauthenticated. DEFERRED -- not validation-critical; must close before external code review. Honest statement.
- TD-108: Per-fact consent-and-routing ledger not yet built. OPEN -- primary liability-severity reducer; ship pre-scale. Honest scope statement.
- TD-109: Biometric consent-and-retention controls for speaker recognition. OPEN build requirement. No public consent claim is accurate until this ships.

Framing note: Proactive honest disclosure of GATE and SEC items is the correct diligence posture. A reviewer who finds undisclosed SEC items during code review is far more concerned than one who finds them pre-disclosed here. This document is a trust signal, not a risk list.

---

### Item 6 -- Market Research (Citation Support)

Files:
- `docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-verified__v20260712_1331.md`
- `docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-external__v20260712_1331.md`

Version: v20260712_1331 (both)
Format: md
Audience fit: Investor primarily. Technologist reads to verify cited methodology.

What it covers:
- Verified doc: 26 sources, 24/25 claims confirmed at 3-0 adversarial vote. Source of the 63.7% / 84.2M figure, the 29.2M couple-only base, the 15.2M 65+ solo households, the 63M caregiver count, the remote monitoring adoption doubling. All [V] flags indicate the primary source was downloaded and checked.
- External doc: Modeled estimates for the 45-55% core addressable segment and 78-85% functionally multi-principal framing. These are labeled [D] throughout; a reviewer who asks "where does the 45-55% come from?" gets this document as the honest answer.

Cited-vs-modeled discipline: verified doc uses [V]/[E]/[D] throughout; every modeled figure is distinguished from every cited figure.

**Note: The REFUTED ~80% older-adults-in-1-2-person-HH framing does not appear in either document. The refuted framing must not be introduced in any summary or verbal presentation.**

---

### Item 7 -- Governance Proof (Live-Run Evidence)

File: `docs/deliverables/HIP_GovernanceProof__audited-transcript__v20260714_1345.md`
Version: v20260714_1345
Format: md
Audience fit: Technologist primarily. An investor can read Section 1 summary table and the Section 2 conformance summary first paragraph for the high-level claim.

What it covers:
- Section 1: Turn-by-turn audit of the reveal_demo run (7 turns, R01-R07, real engine records from 2026-07-14T11:28 UTC). For each turn: member, query, reply, routing/inference timing, every admitted fact with trust rung (CONFIRMED/CORROBORATED/ASSERTED/UNCONFIRMED/DERIVED), every withheld fact with the specific INJ clause and plain-English reason, guard events with timing.
- Key evidence points: R06 (guard_empty_set, 56 ms routing, inference=null -- model not called, rule fires deterministically); R07 (guard_inj7, 82 ms routing, inference=null, withheld=[] per existence-invariant FLAG-1 -- Sam cannot determine whether Maya has any facts).
- Section 2: Conformance summary for P1-P6 (the six disclosure governance invariants), each with harness citation and turn reference. Honest gap: INJ-6b (attr-targeted empty-set, the seam that fired in R06) is marked "asserted, not proven-by-test" -- the fixture spec is in progress (companion PLAN doc same commit).
- Scope note: P7-P10 (SIO integrity, write monotonicity, confidence-ladder severing, confirmation gate independence) are valid harness Layer 1 invariants governing internal mechanics; they are outside the scope of this disclosure-conformance document and are correctly referenced in NDA_OpenProblems.

Why this matters for diligence: The WP states "rule of law, not rule of the model." The governance proof is the evidence layer. A technologist who wants to verify the claim does not need to read source code -- they can read a faithful turn-by-turn trace of a real run and verify that each decision is rule-driven.

Cross-references: Consistent with WP Part II (CandidateIntent pattern, Gate A 26/26). Consistent with NDA_OpenProblems (P8/P10 usage is correct harness numbering). Consistent with Debt Register (TD-101b is out of scope for this document).

---

### Suggested Reading Order

For a technologist-investor reviewing over one or two sessions:

**Session 1 -- Architecture, moat, and live proof (3-5 hours)**
1. Confidential WP Parts I and II (architecture, moat, SIA, CandidateIntent, Gate A/B, voice governance, speaker verifier).
2. NDA Open Problems / Expansion Roadmap (OP-1..5 depth; safe-failure proofs; v2+ lines of attack; P8/P10 behavioral context).
3. Governance Proof (turn-by-turn live-run trace; P1-P6 conformance evidence; guard timing; honest gap flagged).

**Session 2 -- Market, economics, and open items (2-3 hours)**
4. Confidential WP Parts III, VII, VIII, IX (market forces, cable economics, unit economics, why now).
5. Ecosystem Analysis NDA (40-firm map, TAM layers, partnership taxonomy, eldercare anchor).
6. Financial Annex xlsx (model detail; unit economics behind Part VIII).
7. Debt Register NDA Appendix (honest open items; contextualize against WP and architecture).
8. Market Research verified doc (trace 63.7% and caregiver figures to primary sources).

---

## Cross-Reference Discipline Notes

### Cited-vs-modeled discipline
The following figures are CITED (Census, AARP primary sources) and may be stated without qualification:
- 63.7% / 84.2M of 132.2M US households are 1-2 person (2024 CPS ASEC HH-4).
- 29.2M couple-only households (CPS 2023 Table H1, lower bound).
- 15.2M households with a 65+ adult living alone (ACS-derived).
- 63M family caregivers (AARP/NAC 2025).
- Caregiver remote monitoring: 13% (2020) to 25% (2025) (AARP/NAC 2025).

The following figures are MODELED (analyst derivations, no direct Census source) and must be labeled every time:
- 45-55% core near-term addressable segment (60-73M HH): [MODELED, external analysis].
- 78-85% functionally multi-principal: [MODELED, session deep-research synthesis].
- 20-33M eldercare wedge: [MODELED, involvement rates applied to 65+ solo HH base].

The following framing is REFUTED and must NEVER appear in any summary, verbal presentation, or document:
- "~80% of older adults live in 1-2 person households": REFUTED. The correct figure is 63.7% of ALL households. The ~80% framing conflates household SIZE composition with an age-segment percentage that does not hold under primary-source review.

### Package completeness gaps (for Bill's decision)

**Gap 1 -- Architecture overview doc (Tier-1):** No standalone, polished, SIA-era architecture-for-diligence document exists. The Confidential WP fills this partially; the NDA Open Problems doc fills the governance depth; the Governance Proof fills the live-evidence layer. The STALE Technical Annex describes an older architecture and is excluded. A purpose-built "HIP Architecture for Diligence" (what-it-does level, four-layer model, CandidateIntent pattern, no implementation code) would close this gap. This is PKG-3b territory (diagrams) plus a prose companion. Not a showstopper for the current reviewer if the WP and NDA_OpenProblems docs are read in order.

**Gap 2 -- Ecosystem analysis 63.7% figure:** One sentence addition to Section 1 or Section 2 of the ecosystem analysis closes this. Recommend adding before distribution. Requires Bill's approval of placement and a new docx version per naming law and MANIFEST update.

**Gap 3 -- Financial Annex formatted deliverable:** The xlsx is current; the docx formatted version is STALE. If a formatted financial narrative is required for distribution, rebuild the docx from the xlsx. No prose changes needed; it is a formatting rebuild.

**Gap 4 -- Confidential strategy doc (polished deliverable):** The HIP_STRATEGY doc contains complete, current strategy content. It is not registered as a NDA deliverable and reads as a working reference doc. Bill should decide whether to package it. Recommendation: for a first send, rely on the Confidential WP, which covers the thesis, moat, beachhead, and wedge in polished form. The strategy doc becomes relevant if the reviewer wants more depth on the operator partnership thesis or the co-founding argument.

**Secure-site publish note (action NOT taken here -- Bill's call):** If a secure diligence data room (e.g. Firmex, Intralinks, or a purpose-built secure site) is used for package delivery, the governance proof should be included as a formal upload alongside NDA_OpenProblems and the Debt Register Appendix. It is not a marketing document -- it belongs in the architecture-and-evidence tier, not the cover-letter tier. The secure-site publish manifest (if one exists) should add `HIP_GovernanceProof__audited-transcript__v20260714_1345.md` with audience tag "technologist" and reading-order position after NDA_OpenProblems. This note is for Bill's action; no publish action has been taken here.

---

## MANIFEST Update Required

This index document must be registered in MANIFEST Section B as an NDA-tier deliverable. Registration in same commit as this file.

Docs not requiring MANIFEST updates from this audit:
- Market research docs (research artifacts, not deliverables).
- Strategy doc (internal, not registered).
- GOVERNANCE_SCOPE_v1 (internal scope fence, not registered).
