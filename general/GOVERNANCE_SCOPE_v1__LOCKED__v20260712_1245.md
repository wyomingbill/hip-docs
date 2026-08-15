# GOVERNANCE SCOPE v1 -- LOCKED
Status: BUILT
Reconciled-Against: main c87669b (2026-07-12); harness --full RATCHET PASS

**This document is LOCKED.** It is the scope fence for all v1 build work. No session
extends v1 scope to a deferred item without Bill unlocking it. Reference this doc in
HIP_STATE cold-resume and the canonical backlog.

---

## Purpose

HIP v1 governs a bounded set of principals and fact types operating inside a household
context. The architecture is multi-principal by design: every layer -- the identity
envelope, the injection contract, the trust ladder, the confirmation gate -- was built
to handle distinct actors with distinct access rights to distinct facts. The bound
described below is a product and scope decision, not an architectural limit. Crucially,
every deferred case fails closed: the system refuses or parks rather than guessing or
leaking, so deferral is safe without any change to the enforcement path.

---

## In Scope for v1 (Built, Gated, Green)

### Principals and identity

**Competent adults as full members.** A full member holds an identity envelope (voice
principal at L0, session credential at the interaction surface), owns facts under their
principal key, and is subject to per-member encryption (Fernet/HKDF-SHA256, one key per
member). The injection contract enforces isolation invariant P1 (zero cross-member read
failures in the full harness suite) and the SIA classifier resolves the active speaker
before any SIO field is evaluated.

**Care recipients as non-credentialed subjects under declared caregiver grants.** A care
recipient (e.g. Elena, Ray) is a subject in the fact store, not an authenticated
principal. A full member with a caregiver grant may read or write facts about a
recipient under their own session. The grant is an explicit declaration, not inferred
from utterance.

### Governance behaviors (all four demonstrated and harness-gated)

1. **Admit** -- inject allowed facts into the context window; injected_fact_ids recorded
   in telemetry. Invariant P2 (owner retrieval) and P6 (epistemic non-fabrication: fact
   referenced in reply must be in the injected set) both green at L1 and L2.

2. **Refuse with reason** -- two distinct refusal kinds enforced deterministically:
   - *access_control* (INJ-7): cross-member personal query; existence-invariant (the
     system emits the same refusal regardless of whether the target member's fact exists;
     the denied list is never surfaced in any record or reply). Gated at L3, L4, L5; A5
     adversarial suite 4/4.
   - *empty_set* (INJ-6b): subject resolved, zero facts approved. Gated at L2 (T119),
     L4 (PW010, PW013-015), L5. Distinguishable from access_control refusal per P4.

3. **Park pending confirmation** -- cross-member lower-rank write parks as UNCONFIRMED
   alongside the higher-trust head (P8 write monotonicity, store.py:397-415). P10
   confirmation gate resolves the park on a bound-actor closed-vocab utterance; no model
   in the confirmation path. Gated at L1 P8/P10 and L3.

4. **Encrypt per member** -- facts stored and retrieved through member-scoped encryption.
   TD-030 (fact values never in any record or log) enforced at the epistemic record
   layer. Decrypt path is a separate vault call, never triggered by the injection
   contract.

### Fact types governed

- Personal health facts (medication, allergy, appointment) -- primary demonstration
  surface; seeded and pairwise-tested at L4 (PW000-PW030)
- Preference and schedule facts
- Household/shared facts accessible to all members without isolation restriction
- Write-path fact lifecycle: ASSERTED -> CORROBORATED -> CONFIRMED (trust ladder);
  supersede and augment write kinds gated at L1 P3/P5

---

## Out of Scope for v1 -- Named Open Problems

Each item below is deferred, not dismissed. Per the deep review (recommendation 9):
named open problems presented proactively are a stronger diligence position than a
quietly narrowed product. These items are research assets in the NDA.

---

### OP-1: Minors and Consent Gradients

**What it is.** A minor household member is neither a full credentialed member nor a
passive care recipient. They occupy a third category: a principal with evolving consent
capacity, whose access rights and data ownership may change continuously with age,
parental delegation, and jurisdiction.

**Why it is hard.** Consent regimes for minors vary by jurisdiction and by fact type
(health vs educational vs location). No single "minor" principal type is correct; the
governance rules are themselves context-dependent. Writing a wrong rule is worse than
writing no rule.

**Why deferral is safe.** There is no minor principal type in v1. A minor's facts are
either held under an adult member's key (caregiver pattern) or the query falls to the
access_control refusal path. The system does not guess at minor-consent rules; it parks
or refuses.

**Line of attack.** Model minor as a principal-with-delegation-chain: a guardian holds
write authority with automatic expiry tied to an age-threshold trigger. Consent surface
is explicit grant, not inferred. Separate harness invariant: a minor's own facts may not
be read by any adult member without an explicit per-fact grant from the guardian.

---

### OP-2: Facts Owned by a Third Party About a Relationship Between Two Members

**What it is.** Some facts are inherently relational: a shared calendar entry, a care
plan co-signed by two members, a conflict log owned by neither party alone. The current
one-owner model (every fact has exactly one owner: (owner, attribute, subject) triple)
cannot represent co-ownership or shared provenance.

**Why it is hard.** Enforcing isolation on a jointly-owned fact requires a policy
decision: does the fact follow the more restrictive member's rules, the less restrictive,
or a separately-declared joint-grant rule? Each choice has failure modes.

**Why deferral is safe.** Any cross-member read today hits the access_control or
empty_set refusal paths. No relational fact type exists. The store enforces one-owner
invariant P3 (exactly one active head per (owner, attribute, subject) triple). If a
relational fact were inserted manually, it would route to one owner and be invisible to
the other, which is conservative.

**Line of attack.** Introduce a joint-fact type with a two-member grant tuple and a
merge policy enum (union / intersection / explicit-consent-per-member). Gate at a new
L1 invariant: joint-fact reads require both members' grant to be active.

---

### OP-3: Recipient-Competence-Aware Disclosure

**What it is.** A care recipient's capacity to understand, act on, or consent to
disclosure of their own facts may vary: a precocious child, a cognitively-atypical adult,
a member whose capacity changes over time. The question is whether the system should
modulate what it discloses to the recipient themselves based on an assessed competence
level.

**Why it is hard.** Any system that models a person's competence to receive information
about themselves is making a paternalistic judgment. The ethical hazard is severe: a
competent adult's access to their own information must never be reduced by the system's
assessment of their competence. Getting this wrong in either direction is a patient-safety
and civil-rights failure.

**Why deferral is safe.** HIP v1 governs access between members, not the competence of
a principal to hold their own facts. A subject's own facts are disclosed to their
owning member per the normal injection rules; there is no competence gate on
self-directed queries.

**Line of attack.** Only implementable as an opt-in, externally-supplied, time-bounded
grant with explicit human review. The system may never infer competence from utterance
or interaction history. Any implementation requires ethics review before development
begins.

---

### OP-4: Contextually Variable Sensitivity

**What it is.** The sensitivity of a fact is not a fixed property of its attribute type;
it is a function of (fact, asker, context). Maya's medication is high-sensitivity when
the asker is Sam, low-sensitivity when the asker is Maya, and medium-sensitivity when
the asker is Maya's cardiologist under a delegation. The current model assigns
sensitivity statically per attribute.

**Why it is hard.** Dynamic sensitivity requires a policy language with at least three
axes (fact, asker, context), a runtime evaluator, and a harness that can test
combinatorial policy outcomes. The risk of misconfiguration is high and the failure mode
(over-disclosure) is silent.

**Why deferral is safe.** Static per-attribute sensitivity is conservative: if anything,
it over-restricts. The asker-context axes are not yet modeled, so cross-member queries
fail to the access_control refusal path regardless of context. No fact leaks because the
context was misread.

**Line of attack.** Introduce a sensitivity policy DSL with a three-axis evaluator, gated
by a new harness invariant: sensitivity must be monotonically non-decreasing when the
asker is a non-owner. Audit trail required per policy evaluation (TD-108 dependency).

---

### OP-5: Coercion and Duress Detection

**What it is.** A member may be compelled to query or disclose facts under coercion. The
question is whether the system can detect duress and modify its behavior (refuse, alert,
log-only without disclosure).

**Why it is hard.** Reliable coercion detection from speech or text is not a solved
problem. False positives (system refuses a legitimate query because it pattern-matched a
duress signal) are a denial-of-service against the member. False negatives leave the
coercion undetected. Any duress signal would also need an out-of-band escalation path
that does not exist in v1.

**Why deferral is safe.** HIP governs disclosures between system and principals; it does
not surveil the physical or social context of the principal. Coercion is out of scope
entirely, not parked. The system makes no claims about detecting it.

**Line of attack.** This requires a separate research track and is not a near-term build
item. The honest position is that no access control system (digital or physical) is
coercion-proof; the bank does not detect that you are being robbed when you make a
withdrawal.

---

## The Architectural Boundary

HIP governs the system's disclosures: access and disclosure between principals, enforced
deterministically by the injection contract, the trust ladder, and the confirmation gate.
It does NOT govern what an authorized human does with a fact after receiving it.

This is not a weakness. It is the honest and correct scope of what any access and
disclosure system does. A bank enforces who may withdraw funds; it does not control what
the account holder does after the withdrawal. A medical records system enforces who may
view a chart; it does not control what a clinician does after reading it. HIP enforces
which facts are disclosed to which principals under which conditions; it does not control
what a household member does with a fact after the system has delivered it.

Naming this boundary explicitly is a stronger position than eliding it. Auditors,
diligence reviewers, and ethics boards will ask where the system's authority ends. The
honest answer is: at the point of disclosure to an authorized principal.

---

## Strategic Note

The five deferred items above are research assets, not product gaps. Per the deep review
(research-technical/ANALYSIS__candidate-intent-deep-review__v20260711_0501.md,
recommendation 9): proactively naming open problems is a stronger diligence position than
a quietly narrowed product. Guardianship and capacity (OP-1, OP-3) are HIP's hardest
and most valuable open problems -- they represent the frontier of governed AI memory in
high-stakes household contexts. No competitor has solved them. Naming them as deferred
research assets, with a clear line of attack and a safe-failure explanation, demonstrates
that the architecture was designed by people who understand the problem space.

---

## References

- Enforcement invariants P1-P9: general/HIP_STATE__cold-resume__v20260711_1700.md
- Injection contract + INJ-1..INJ-7: server/voice_orch.py, harness/injection_contract.py
- Trust ladder: memory_engine/trust.py:27-32
- P8 write monotonicity + P10 confirmation gate: store.py:397-415, confirmation_gate.py
- Adversarial test suite (A1-A5): harness/eval.py, five-layer harness
- Deep review + recommendation 9: research-technical/ANALYSIS__candidate-intent-deep-review__v20260711_0501.md
- SIA two-gate conformance model: research-technical/SIA_SHIP_BAR__two-gate-conformance__v20260711_0842.md
- Harness architecture and invariants: research-technical/TEST_HARNESS__architecture-and-invariants__v20260711_1900.md
- Tech debt register: techdebt/DEBT_REGISTER__v20260709_0855.md (TD-101, TD-108, TD-110)
