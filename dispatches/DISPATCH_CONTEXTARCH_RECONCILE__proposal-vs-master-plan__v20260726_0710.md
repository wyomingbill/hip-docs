# DISPATCH_CONTEXTARCH_RECONCILE — Context & Interaction Architecture Proposal vs Ratified Master Plan
Status: BUILT (analysis complete)
Reconciled-Against: roadmap fe1f021 (working tree carries uncommitted OB5 crypto changes, untouched)
REQ: NONE — analysis dispatch (Requirements Discipline item 10); no code changed, nothing ratified.

## Identity / preflight
`bill-ai` @ `[REDACTED-MACHINE-NAME]`, `[REDACTED-USER-PATH]/hip-roadmap`, branch `roadmap` (up to date
with origin at dispatch start, fe1f021).

## The ask (Bill)
Reconcile the Context & Interaction Architecture proposal against the ratified HIP design. One table,
every proposal and named subsystem, each row in exactly one of four columns (already ratified /
consistent extension / conflicts / new decision). Separately list false/stale current-behavior
assertions with file:line. Explicitly reconcile the governance separation (learner never overrides
authorization). File the diff, register, commit, push. Analysis, not a build. No code.

## What was found (headline)
- Proposal was on NO disk path — filed verbatim this dispatch:
  `docs/design/HIP_ContextArch_Proposal__context-interaction-intelligence__v20260726_0710.md`.
- Deliverable: `docs/deliverables/HIP_ContextArch_Reconciliation__master-plan-diff__v20260726_0710.md`.
- Column counts: ALREADY RATIFIED 10 · CONSISTENT EXTENSION 31 · CONFLICTS 2 · NEW DECISION 7 (50 rows).
- The 2 conflicts: epistemic fit as an inclusion/exclusion ranking dimension (fights the ratified
  hedge-don't-hide rule + T02 amendment), and a fast voice path emitting content outside the DECIDED
  text checkpoint.
- 7 false/stale assertions, each with file:line (stale scope name HOUSEHOLD-SHARED; stale "recipient"
  standing policy; CUSTODIAN mislisted as a per-fact role; a Disclosure Check stage that does not exist
  — G0 unbuilt; no as-of-time retrieval; silence-is-not-positive already built; authorization is a
  registry lookup, not rankable context).
- Governance (highest stakes): separation holds today BY DATAFLOW (owner-scoped candidates → INJ-1..7
  before the model → class-sealed at rest), but it is not a machine-checked property. Adopting a learned
  ranker requires three builds that do not exist: G0 (ratified, unbuilt), a prompt⊆admitted layer-7
  standing invariant (OB4 pattern; no REQ), and learner/training-signal isolation incl. a sealed
  training record (no REQ).
- Code-state note: the write-time classifier REQ's WHAT'S-KNOWN-BROKEN is stale against the tree — the
  classifier is built (`write_rule.py` rewritten, `role_resolution.py`/`compound_split.py`/
  `standing_policy.py`/`care_team_keys.py`/`answer_mode.py` exist). Reconciled against code, not the
  REQ snapshot.
- Housekeeping: HIP_DesignDigest__weekly__v20260725_1400.md was committed this morning without INDEX/
  MANIFEST registration (orphan per the Document Governance Rule) — registered in this commit.

## Method
Read in full: the proposal; plan of record; REQ_PARTITION_CUSTODY; REQ_CRYPTO_P3_OPERATOR_BLIND
(working copy); REQ_CONFIDENCE_DISCIPLINE; REQ_WRITE_TIME_CLASSIFIER; both crypto/dyad design docs;
voice architecture decision memo; interaction-layer architecture doc. Code opened before any claim about
it: write_rule.py, role_resolution.py, fact_change.py (targeted), store.py (targeted),
injection_contract.py, subject_resolution (via role_resolution + REQ trace), router.py, orchestrator.py,
intent_classifier.py, answer_mode.py, trust.py, temporal.py, satisfaction.py, extraction_queue.py
(targeted), complexity_features.py (targeted).
