# TD-121 Fix — extraction input variance + write-confirmation reply gate
Status: BUILT
Reconciled-Against: Layer 2 RATCHET PASS twice consecutively (T04/T05 un-quarantined) + Tier L 11/11 RATCHET PASS, Mini, 2026-07-09

## Symptom
Layer 2 three_zone_demo.T04: "Ray switched from metformin to Jardiance 10mg
last week." sometimes never landed in the graph while the ack claimed the
change. Quarantined `_known_flaky` at Phase 1 build; register candidates were
temperature/seed pinning, retry-on-empty-change, ack-gated-on-write-confirm.

## Diagnosis (live-verified)
1. **Not sampling noise.** `_call_groq` already ran at temperature 0.0.
   Replaying the exact T04 extraction prompt 12x: 12/12 byte-identical
   correct output. Groq is stable per input.
2. **The input varied.** Call sites passed the turn's retrieval output as the
   detector's facts block. With the target fact absent from the block, Groq
   returns `changes: []` **7/8** (measured) — a silent no-write.
3. **Why retrieval membership varied:** NOTHING in the demo graph carries an
   embedding — `memory_engine/store.encode()` writes `embedding: None`
   (Phase A), and both `scripts/demo_seed.py` and the fact-change path route
   through encode(). `search_facts_by_embedding` therefore always returns []
   and every retrieval silently falls back to `read_user_facts`
   (timestamp DESC, limit 8) — a recency window with timestamp-tie ordering
   variance. Logged as **TD-122**.
4. **Second defect exposed by the first fix:** the facts block rendered
   `attribute: value` with no subject channel. With a fuller block, Groq read
   Ray's medication line as Maya's own fact and the T04 update superseded
   **(maya, maya) lisinopril** instead of (maya, ray) metformin —
   graph-verified. This is the mechanical reproduction of the TD-115
   misattribution class on the write side.

## Fix
- **F1 (fact_change.detect_and_apply):** the detector reads the full active
  owner+household set itself (`read_user_facts`, limit 50, no embedding
  dependence); the caller's facts are only a fallback if the read fails.
  Enforced at the single point instead of trusted from call sites.
- **F1b (facts block subject channel):** fact lines carry `(about <subject>)`
  when subject != owner, and the detector system prompt instructs that such
  facts keep that subject on update. Probe on the exact failing block: 10/10
  `subject=ray`.
- **F3 (voice_orch write-confirmation gate):** a supersede-phrased declarative
  (`_SUPERSEDE_PHRASE_RE`) whose detection cycle produced 0 mutations AND 0
  idempotent no-ops gets a fixed reply: "I heard that as an update, but I was
  unable to save it to the household record just now. Nothing was changed —
  please state it again." No silent retry, by decision — visible failure.
  mutations==0 with noops>0 is NOT gated (value already current; ack
  truthful). Plumbing: `_apply_changes` returns (mutations, noops);
  per-session outcome store + `take_detection_outcome()`.

## Gate evidence
- Layer 2, T04/T05 removed from `_known_flaky`: RATCHET PASS twice
  consecutively. T04 graph assert (jardiance active under (maya,ray)) ok both
  runs; T05 reads Jardiance.
- Tier L: 11/11 RATCHET PASS, incl. all 7 T119 paraphrase legs.
- three_zone_demo.T01 remains the accepted TD-115 ack-wording failure
  ("You take…" to Maya about Ray) — reply-side, unchanged by this fix.

## Left open
- **TD-122** (new): encode() embedding:None — all retrieval silently on the
  recency-window fallback. TD-030-safe fix pattern exists in
  `extraction_queue.write_facts` (embed subject+predicate only).
- TD-115 reply-side ack misattribution.
- TD-120 D2 relational bridge (separate bounded task).
