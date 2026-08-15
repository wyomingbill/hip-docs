# HIP Platform -- Open Problems as Expansion Roadmap
Status: BUILT
Reconciled-Against: main 031cf68 (2026-07-13); GOVERNANCE_SCOPE_v1__LOCKED__v20260712_1245; HIP_STRATEGY__positioning-and-market__v20260712_1541 (1a13028)

This document is an NDA-tier extract of the five named open problems in HIP v1 scope, formatted for sophisticated operator and technical diligence audiences. It is a lightly reformatted extract of GOVERNANCE_SCOPE_v1__LOCKED, Section "Out of Scope for v1 -- Named Open Problems," per the cascade map in HIP_STRATEGY Section 8.2.

Positioning: these are research assets, not product gaps. HIP v1 governs a bounded and fully gated scope. Each deferred item fails closed under the v1 enforcement path. Naming the deferral proactively, with a safe-failure proof and a v2+ position, is the correct diligence posture. A reviewer who finds an unnamed gap is more concerned than one who finds a named problem with a safe-failure proof and a clear line of attack.

---

## Technical Context

The v1 governance layer enforces four behaviors across all deployed principals, all built and harness-gated:

- **Admit:** inject allowed facts into the context window; injected_fact_ids recorded in telemetry. Invariant P2 (owner retrieval) and P6 (epistemic non-fabrication: fact referenced in reply must be in the injected set) both green at L1 and L2.
- **Refuse with reason:** two distinct refusal kinds enforced deterministically. access_control (INJ-7): cross-member personal query; existence-invariant (the system emits the same refusal regardless of whether the target member's fact exists). empty_set (INJ-6b): subject resolved, zero facts approved. Distinguishable per P4.
- **Park pending confirmation:** cross-member lower-rank write parks as UNCONFIRMED alongside the higher-trust head (P8 write monotonicity, store.py:397-415). P10 confirmation gate resolves on a bound-actor closed-vocab utterance with no model in the confirmation path.
- **Encrypt per member:** facts stored and retrieved through member-scoped encryption (Fernet/HKDF-SHA256). TD-030 enforced at the epistemic record layer; fact values never appear in any record or log.

**Classification layer (SIA):** the structured intent architecture replaces seven divergent regex classifiers with a single edge-model call producing a Structured Intent Object. Two-gate conformance model: Gate A (governance-critical 26-entry subset) at 100 percent PASS; Gate B (full 133-entry quality corpus) at 85.7 percent as of v20260712, below the 90 percent UX quality target with Phase B cutover deferred to operator decision. Gate A governs disclosure safety; Gate B governs UX quality. No governance-critical entry has ever been misclassified.

**Voice path:** voice-path governance is implemented and harness-gated. BUILD-1 (commit fbcd372) routed the live voice path through the same assemble_governed_context enforcement chain as the typed path at all three sites. Conformance suite VOICE-GOV-001..004 ratcheted PASS. The prior caveat ("voice-path hardening is open engineering work") is superseded by this build closure; see the companion HIP_DebtRegister_NDA_Appendix (v20260713_1100) for the updated entry.

---

## OP-1 -- Minors and Consent Gradients

**What it is.** A minor household member is neither a full credentialed member nor a passive care recipient. They occupy a third category: a principal with evolving consent capacity, whose access rights and data ownership may change continuously with age, parental delegation, and jurisdiction.

**Why deferral is safe (fail-closed).** There is no minor principal type in v1. A minor's facts are either held under an adult member's key (caregiver pattern) or the query falls to the access_control refusal path. The system does not guess at minor-consent rules; it parks or refuses. Zero leak surface: no code path infers or applies minor-consent rules.

**Why it is defensible IP.** No competitor (Maple, Nori, Ohai, b.well, Life360) has addressed minor consent gradients. Wrong rules are worse than no rules; the regulatory surface (COPPA, state health privacy for minors, jurisdiction-specific age thresholds) is a moat that cannot be closed in a single release cycle. HIP is the only platform whose architecture was designed to add a delegation-chain principal type without rebuilding the enforcement path. The kernel is built once; v2 scope is additive invariants on top of a running harness.

**v2+ position.** Model minor as a principal-with-delegation-chain: a guardian holds write authority with automatic expiry tied to an age-threshold trigger. Consent surface is explicit grant, not inferred. Separate harness invariant: a minor's own facts may not be read by any adult member without an explicit per-fact grant from the guardian. Guardianship and capacity governance (OP-1 and OP-3 jointly) are HIP's hardest and most valuable open problems; they represent the frontier of governed AI memory in high-stakes household contexts.

---

## OP-2 -- Facts Owned by a Third Party About a Relationship Between Two Members

**What it is.** Some facts are inherently relational: a shared calendar entry, a care plan co-signed by two members, a conflict log owned by neither party alone. The current one-owner model (every fact has exactly one owner: (owner, attribute, subject) triple) cannot represent co-ownership or shared provenance.

**Why deferral is safe (fail-closed).** Any cross-member read today hits the access_control or empty_set refusal paths. No relational fact type exists. The store enforces one-owner invariant P3 (exactly one active head per (owner, attribute, subject) triple). If a relational fact were inserted manually, it would route to one owner and be invisible to the other, which is conservative.

**Why it is defensible IP.** Co-ownership policy requires a non-trivial decision: does the fact follow the more restrictive member's rules, the less restrictive, or a separately-declared joint-grant rule? Each choice has distinct failure modes. Getting this right requires a jointly-gated fact type that only an architecture with a per-member enforcement model can implement safely. No existing household platform has a fact model that can represent co-ownership with per-member consent.

**v2+ position.** Introduce a joint-fact type with a two-member grant tuple and a merge policy enum (union / intersection / explicit-consent-per-member). Gate at a new L1 invariant: joint-fact reads require both members' grants to be active. The graph substrate and per-member encryption are both prerequisites that are already present.

---

## OP-3 -- Recipient-Competence-Aware Disclosure

**What it is.** A care recipient's capacity to understand, act on, or consent to disclosure of their own facts may vary: a precocious child, a cognitively-atypical adult, a member whose capacity changes over time. The question is whether the system should modulate what it discloses to the recipient themselves based on an assessed competence level.

**Why deferral is safe (fail-closed).** HIP v1 governs access between members, not the competence of a principal to hold their own facts. A subject's own facts are disclosed to their owning member per the normal injection rules; there is no competence gate on self-directed queries. No paternalistic error is possible because no competence assessment runs.

**Why it is defensible IP.** Any system that models a person's competence to receive information about themselves is making a paternalistic judgment in which a wrong answer in either direction is a patient-safety or civil-rights failure. The ethical hazard is severe and defines a research problem that no commercial household AI platform has approached. HIP's governance architecture is the only deployed platform where a competence-aware disclosure gate could be added without disrupting the enforcement path. Any implementation requires an ethics review before development begins.

**v2+ position.** Only implementable as an opt-in, externally-supplied, time-bounded grant with explicit human review. The system may never infer competence from utterance or interaction history. Ethics board sign-off is a hard prerequisite; this is not a v2 build item but a named research track.

---

## OP-4 -- Contextually Variable Sensitivity

**What it is.** The sensitivity of a fact is not a fixed property of its attribute type; it is a function of (fact, asker, context). Maya's medication is high-sensitivity when the asker is Sam, low-sensitivity when the asker is Maya, and medium-sensitivity when the asker is Maya's cardiologist under a delegation. The current model assigns sensitivity statically per attribute.

A second dimension of the same problem: the same fact disclosed in a shared acoustic space (a living room where multiple people can hear the reply) is a different governance event from the same fact disclosed in a private channel (a phone call, a headset, a text notification to a single recipient). HIP's current architecture governs who may authorize a disclosure; it does not yet model the physical or channel context of delivery. This is a named research direction, not a current feature claim. No competitor has addressed the open-room vs private channel dimension; HIP has named it.

**Why deferral is safe (fail-closed).** Static per-attribute sensitivity is conservative: if anything, it over-restricts. The asker-context and channel axes are not yet modeled, so cross-member queries fail to the access_control refusal path regardless of context. No fact leaks because context was misread.

**Why it is defensible IP.** Dynamic three-axis sensitivity requires a policy language with at least three axes (fact, asker, context), a runtime evaluator, and a harness that can test combinatorial policy outcomes. The failure mode (over-disclosure) is silent, making a harness-first approach essential. HIP is positioned to build this correctly because the enforcement path is already deterministic and the harness architecture already tests combinatorial outcomes at L4 (pairwise matrix). The open-room vs private channel research direction is a named and defensible differentiator: incumbents (Amazon, Apple, Google) have not named it; HIP has.

**v2+ position.** Introduce a sensitivity policy DSL with a three-axis evaluator, gated by a new harness invariant: sensitivity must be monotonically non-decreasing when the asker is a non-owner. Audit trail required per policy evaluation (TD-108 dependency). The open-room vs private channel dimension is a separate research track; no implementation timeline before the three-axis evaluator ships.

---

## OP-5 -- Coercion and Duress Detection

**What it is.** A member may be compelled to query or disclose facts under coercion. The question is whether the system can detect duress and modify its behavior (refuse, alert, log-only without disclosure).

**Why deferral is safe (fail-closed).** HIP governs disclosures between system and principals; it does not surveil the physical or social context of the principal. Coercion is out of scope entirely, not parked. The system makes no claims about detecting it. This is an honest position, not a gap.

**Why it is defensible IP.** The honest position is that no access control system (digital or physical) is coercion-proof. The bank does not detect that you are being robbed when you make a withdrawal. Stating this boundary explicitly is a stronger diligence position than eliding it. If a duress signal is ever added, the kernel architecture does not block it; a separate escalation path and a harness invariant testing false-positive denial-of-service are the prerequisites.

**v2+ position.** A separate research track is required. No false-confidence product feature is introduced. Any implementation requires an out-of-band escalation path that does not exist in v1 and a harness invariant that verifies false-positive denial-of-service does not occur before the feature can ship.

---

## Architectural Boundary

HIP governs the system's disclosures: access and disclosure between principals, enforced deterministically by the injection contract, the trust ladder, and the confirmation gate. It does NOT govern what an authorized human does with a fact after receiving it.

This is not a weakness. It is the honest and correct scope of what any access and disclosure system does. A bank enforces who may withdraw funds; it does not control what the account holder does after the withdrawal. A medical records system enforces who may view a chart; it does not control what a clinician does after reading it. HIP enforces which facts are disclosed to which principals under which conditions; it does not control what a household member does with a fact after the system has delivered it.

Naming this boundary explicitly is a stronger diligence position than eliding it. Auditors, diligence reviewers, and ethics boards will ask where the system's authority ends. The honest answer is: at the point of disclosure to an authorized principal.

---

## Cited vs Modeled Discipline

Any market-sizing figures appearing in NDA narrative sections alongside these open problems must carry their label:

- 63.7 percent of US households are 1-2 person households (84.2M of 132.2M). [CITED: Census CPS ASEC HH-4, 2024]
- 63M family caregivers in 2025, 24 percent of all US adults. [CITED: AARP/NAC 2025]
- Core near-term addressable segment: 45-55 percent of US households, roughly 60-73M. [MODELED: external analysis, no source measures this intersection directly]
- Eldercare wedge: 15-25 percent of US households, roughly 20-33M HH. [MODELED: involvement rates applied to 65+ solo HH base]

The modeled figures must not appear in any external NDA surface without the MODELED qualifier. The approximately-80-percent older-adults-in-1-2-person-HH framing is REFUTED and must not appear in any surface. The 63.7 percent structural figure is the safe citation floor.

---

## References

- GOVERNANCE_SCOPE_v1__LOCKED__v20260712_1245.md (scope fence; all five OPs verbatim source)
- HIP_STRATEGY__positioning-and-market__v20260712_1541.md (Section 8.2, cascade map; Section 7, honest boundary)
- SIA_SHIP_BAR__two-gate-conformance__v20260711_0842.md (Gate A 100%; Gate B 85.7%)
- TEST_HARNESS__architecture-and-invariants__v20260711_1900.md (five-layer harness; VOICE-GOV-001..004)
- ANALYSIS__candidate-intent-deep-review__v20260711_0501.md (recommendation 9: proactive naming is the stronger diligence position)
- HIP_DebtRegister_NDA_Appendix__v20260713_1100.md (companion proactive gaps disclosure; voice-path hardening closed BUILD-1)
