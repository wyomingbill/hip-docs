<!-- STATUS: BUILT — Seam A wired and verified on the live path 2026-07-06; Tier L baseline ratcheted to 7/8 -->
<!-- RECONCILED-AGAINST: working tree on main 22ec924; Tier L run 3× identical; full 10-check gate green; memory 17/17; truth 6/6 -->

# Phase 3, Seam A — Post-Write Grounding for Declarative Turns (E1/E2)

Baseline finding (docs/testing/INTEGRATION_LIVE__e1-e8-baseline__v20260706_1310.md): a
declarative statement wrote correctly (metformin superseded → Jardiance ASSERTED head)
but the grounding guard + injection contract evaluated the PRE-write fact snapshot, so
the CORRECTION-RULE ack never fired (E1) and a next-turn recall refused instead of
naming the new head (E2).

## The fix (three parts, all on the text path the demo/browser uses)

1. **Order — write before disclosure** (`server/voice_orch.py`,
   `process_text_query`): a potentially-mutating declarative turn (mirrors
   `detect_and_apply`'s own gates: declarative, ≥4 words, no question opener) now runs
   fact-change detection SYNCHRONOUSLY before the injection contract, waits on the
   detection event (12s bound), re-retrieves the fact state, and lets grounding +
   injection evaluate the POST-write head. The end-of-turn async detection is skipped
   when this ran (`_detection_done`) — still exactly one detection per turn (E8 held).
   Question turns are untouched.

2. **Guard scope — statements are acks, not answers** (`harness/orchestrator.py`,
   `local_system_prompt(declarative_turn=...)`): the TD-052 grounding guard governs
   ANSWERING questions about specific details; on a statement turn it forced
   "I don't have that confirmed yet" instead of the CORRECTION-RULE ack even with the
   just-written fact in the bullets (the statement's other details — the old value,
   "last week" — are not bullets). Statement turns now skip the guard; question turns
   keep it exactly as before. Measured 3/3 stable acks post-change.

3. **Disclosure integrity — prompt carries the contract's output only**
   (`local_system_prompt(known_facts=...)` + call site): the "Things you know" section
   did its own `read_user_facts` retrieval, filtered by permissions only — a channel
   AROUND the injection contract. Harmless-looking while replies were blanket
   refusals; the moment Seam A made replies engage, it leaked Maya's own medication on
   a Ray query (E5 regressed mid-fix). The text path now passes `known_facts=[]` so
   the prompt carries exactly the contract-admitted set, once. This does not weaken
   the contract for other-subject queries — it closes the path that bypassed it.
   Additionally, contract-admitted facts about a subject OTHER than the requester are
   rendered subject-explicit (`(about Ray) Jardiance 10mg`, copies only), so a recall
   about that person can use the fact instead of refusing.

**Scope discipline:** INJ-1..6 rules untouched. E6 (structural refusal) untouched and
still FAIL as expected. E3's leak channel was the same contract-bypass closed in (3),
so E3 flipped PASS as a side effect — the underlying subject-attribution RENDERING
seam (second-person framing) is NOT implemented; E2's correct "Ray is on Jardiance
10mg." comes from the explicit `(about Ray)` annotation on admitted facts. Voice path
(`_on_user_text`) not changed — it does not run the injection contract at all (DIV-2)
and is a separate wiring phase; Tier L measures the text path.

## Tier L after Seam A (3 identical runs; baseline ratcheted)

| id | scenario | before | after | evidence |
|---|---|---|---|---|
| E1 | statement writes ONE supersede + acknowledges | FAIL | **PASS** | graph unchanged-correct (1 supersede, ASSERTED); reply now `"Got it, Ray switched from metformin to Jardiance 10mg last week…"` |
| E2 | recall retrieves the new value | FAIL | **PASS** | `"Ray is on Jardiance 10mg."` — correct value AND correct subject attribution |
| E3 | simple personal → EDGE + correct answer | FAIL | **PASS** (side effect) | `"You take lisinopril each morning."` — Jardiance leak gone because the contract-bypass channel is closed |
| E4 | complex personal → CORE | PASS | **PASS** | tier=core, bloom 6; answer now actually uses Ray's medication |
| E5 | cross-subject privacy (own facts withheld) | PASS | **PASS** | no lisinopril / cardiology leak (regressed mid-fix via the bypass channel; green after (3)) |
| E6 | empty-set → structural refusal | FAIL | **FAIL** (untouched seam) | `guard_triggered=False`; refusal remains model-behavioral |
| E7 | fact_history single clean chain | PASS | **PASS** | 2 nodes, 1 head, distinct values |
| E8 | idempotency (replay = no-op) | PASS | **PASS** | same head fact_id, node count unchanged — sync detection kept single-fire |

**New ratcheted baseline** (`eval/integration_live_baseline.json`): 7/8 —
`{"E1": true, "E2": true, "E3": true, "E4": true, "E5": true, "E6": false, "E7": true, "E8": true}`

## Regression battery (all green)

- Full 10-check gate: PASS (routing ≥0.90, injection 11/11, Tier F 17/17, S1/S2/S3,
  DEMO-005 4/4, trust agreement 11/11, E7/E8 idempotency, Tier L ratchet)
- `eval/memory_harness.py`: 17/17 (incl. MEM-100)
- `eval/truth_harness.py`: 6/6

## Carried forward

- **E6** — INJ-6 unreachable for this query shape (admitted set non-empty after
  INJ-2); separate seam.
- **Subject-attribution rendering** — the `(about <subject>)` annotation is a
  caller-side data tweak; a principled subject-aware renderer (and the voice path's
  missing contract, DIV-2) remain Phase 3 follow-ups.
- **Latency note** — declarative turns now block on one Groq detection round
  (~1-3s typical, 12s bound) before generation; question turns unaffected.
