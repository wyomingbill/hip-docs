# TD-114 Fix — write-then-can't-read root cause (HITL F-1/F-2)
Status: BUILT
Reconciled-Against: Tier L 9/9 (E1-E8 + G2), two consecutive green runs, baseline locked 2026-07-08

## Summary

HITL Phase 4 found that a fact asserted and acknowledged in one turn was not
retrievable by its own owner in the next turn (F-1), and that the epistemic
pane showed the just-written fact in a closed/struck state (F-2). Reproduced
live against the dev graph with direct Neo4j inspection. **Two independent
write-path defects produced the same symptom**, one per HITL reproduction:

## Defect 1 — retract closes the just-written head (Elena leg, F-2 proper)

Fingerprint: the Jardiance fact for (owner=bill, subject=elena, medication)
was created and then closed **25ms later** with `closed_by='retracted'`,
`closed_reason=None`, `superseded_by=None`, and no successor row.

Chain: for "switched **from metformin** to Jardiance" Groq emits BOTH an
`update` (Jardiance) and a `retract` (metformin no longer true). The update's
supersede correctly closed the old row and opened the new head. The retract
then called `retract_fact(owner, attribute)` — **unscoped by subject and with
no value check** — closing every active medication fact for the owner,
including the head written moments earlier in the same batch.

Fix (harness/fact_change.py):
- Any (owner, attribute) targeted by an update/add in the current change
  batch is off-limits to a retract in the same batch, regardless of the
  update's apply outcome (a retract after a rejected or idempotent-no-op
  update would destroy the head the update meant to keep).
- Standalone retracts are now subject-scoped: Groq's subject when present,
  else the speaker's own row. The attribute-level nuke remains available only
  to callers that pass no subject (voice_orch manual retract) — not from
  utterance-level change detection.

## Defect 2 — literal "null" subject string (Sam leg, F-1 first reproduction)

Groq emits `"subject": "null"` as a **string**, which survives
`(subject or owner)` truthiness; Sam's penicillin allergy was written under
`subject='null'` — active in the graph but unreachable by subject-scoped
retrieval, so INJ-6b fired the empty-set refusal on the owner's own fact.

Fix: `_clean_subject()` treats "", "null", "none" as absent; applied to both
the update and retract branches.

## Third defect found while closing G2 — NOT fixed, logged as TD-119

With the fix in, G2's Elena read still failed on the phrasing "What
medication does Elena take?" while "What medication is Elena on now?"
answers correctly — **prompt-identical A/B confirmed** (the contract admits
the fact and the rendered prompt carries "(about Elena) Jardiance 10mg" in
both cases). Deterministic edge-model (qwen2.5:7b) phrase sensitivity under
PERSONAL_FACT_GROUNDING_GUARD. The guard exists against verified
confabulation and was not touched. G2 uses the answered phrasing; TD-119
tracks the robustness gap with a phrasing-matrix scenario required before
any guard wording change.

## Gate

- G2 added to eval/integration_live.py per the harness gap spec
  (docs/testing/LATEST_HARNESS_GAP_SPEC.md): owner asserts, owner reads back
  next turn; two legs (Sam/allergy, Bill re Elena/medication) — one per
  defect above.
- RED confirmed on pre-fix code: 8/9, G2 failing with the exact predicted
  fingerprints (leg 1 write landed but unreadable; leg 2 head closed
  in-turn).
- GREEN on fixed code: 9/9, twice consecutively; baseline updated to include
  G2=true (ratchet now guards both defects).
- No E1-E8 regression in any run.

## Verification pipeline note (for future read-path triage)

Stage-by-stage instrumentation used to isolate the third defect, reusable
for any "fact exists but reply refuses" triage:
retrieval (read_user_facts) → resolve_subject → apply_injection_contract →
subject annotation (voice_orch) → local_system_prompt render → model. In
this case every stage upstream of the model was correct and identical
between the working and failing phrasings.
