<!-- STATUS: BUILT -->
<!-- RECONCILED-AGAINST: truth_layer/__init__.py (present); truth_layer/queries.py (scaffold with signatures + NotImplementedError bodies, confirmed no live imports); eval/truth_harness.py (T-A + T-B scenarios written) — 2026-07-05 -->

# Truth-Layer Spec — Completion Report

**Commit:** `b1c9cb4` on `main` in `~/hip-dev`
**Date:** 2026-07-05
**Live 6-check gate:** PASS unchanged (routing 91.2% ≥ 90%, injection 11/11,
integration Tier F 17/17, seams S1/S2/S3 all PASS). Injection contract and
live pipeline untouched.

## Deliverables

| File | What |
|---|---|
| `docs/TRUTH_LAYER_SPEC.md` | The architecture spec (plan only, ~350 lines) |
| `truth_layer/__init__.py` | Package namespace |
| `truth_layer/queries.py` | Read-only scaffold: dataclasses + signatures + `NotImplementedError` bodies; verified to import with no Neo4j / live-pipeline / contract imports |

## What the spec pins down

- **§1 Boundaries** — ownership table: memory engine owns storage/tiers/
  retrieval; truth layer owns belief provenance, correction history, trust,
  confirmation authority; frozen injection contract owns disclosure. Three
  hard rules: the layer never stores, never discloses, never decides.
- **§3 Four truth questions as named read-only queries** —
  - `provenance(fact_id)` — driving utterance (encrypted at rest), session,
    write decision (requested + actual + override_reason), model_id,
    rationale.
  - `believed_state(subject, attribute, at)` — the bitemporal record-time
    reconstruction, finally executable instead of a paragraph (engine §7).
  - `correction_history(subject, attribute)` — CORRECT (`closed_reason=
    error`, record-time closed) made queryably distinct from SUPERSEDE
    (world changed).
  - `lineage(fact_id)` — bidirectional supersede/correct/derived chain walk,
    typed links, cycle-safe, surfaces broken links instead of truncating.
  - `trust(fact_id)` — see below.
- **§4 Trust: classification, not score** — explicit decision with
  rationale: a numeric formula would launder categorical inputs
  (`confirmed_by`, `write_state`, `derived`) into false precision. Five
  ordered levels — DERIVED (category, checked first) → CONFIRMED →
  CORROBORATED → ASSERTED → UNCONFIRMED — deterministic first-match
  predicates, `basis` string returned with every classification, age is a
  `stale` flag only (staleness is information, not distrust).
- **§5 Disclosure governance** — the layer is a contract-neutral library;
  every user-facing surface passes results through the real
  `apply_injection_contract` (the `recall_from_cold` pattern, including the
  who/when/why audit log). Trust tagging at disclosure is additive-only,
  applied strictly after the contract call, with TRUTH-100 asserting a
  byte-identical `InjectionResult` with/without annotation (MEM-100 analog).
- **§6 Gaps (the honest list)** — key finding from grounding the spec in
  the code: **the write-decision rationale is persisted hash-only**
  (`rationale_hash` in `confidence_log`, `prompt_hash` in the audit
  record), so provenance can prove a rationale existed but not show it.
  That is G-1 — the only write-path change in the plan (persist encrypted
  `rationale_ct/_dek` at ENCODE, TD-030 applies), deferred to Phase T-D and
  gated like any engine change. G-2 lineage walk, G-3 trust classification,
  G-4 trust tagging, G-5 named bitemporal query are all read-only.
- **§7 Model/code boundary** — model's role at query time is zero; the
  truth layer exists precisely so recorded write-time judgment can be
  audited without re-asking a model (which would replace evidence with a
  fresh opinion).
- **§8 Claims discipline** — permitted claim template: "structurally
  constrained from injecting facts outside the contract, with deterministic
  disclosure controls and auditability" — never "can't leak", never "live"
  until swap-in. Six residual vectors enumerated with mitigation or
  explicit out-of-scope status: misclassification, explicit-search side
  channel, operator/debug access (including the memory dashboard's own
  debug mode), log-metadata exposure, backup exposure, prompt injection.
- **§9 Tests** — TRUTH-100..107 corpus specified for `eval/truth_harness.py`;
  independent engine-track gate; NOT wired into `gate_check.sh` until the
  memory swap-in milestone; ratchet rule inherited (bug → scenario before
  fix merges).
- **§10 Phases** — T-A thin query layer (already answerable today; exposure,
  not construction) → T-B trust classification → T-C trust tagging +
  byte-identity proof → T-D the G-1 rationale persistence (engine track,
  last, everything else works without it).

## Status language (per the spec's own rule)

The memory engine + planned truth layer are **built, tested, and
integration-ready behind the frozen injection contract** — not live. The
live pipeline still runs `read_user_facts()`; swap-in is the engine spec
§10 milestone.
