<!-- STATUS: BUILT — dialogue-driven reveal live on dashboard 7871, verified 2026-07-06; full 10-check gate + Tier L 8/8 green after -->
<!-- RECONCILED-AGAINST: main a35c933 + this change; verification transcript below is from the live tailnet dashboard -->

# Demo Console — Empty Start, Dialogue-Driven Reveal

Fix for the pre-loaded-state problem: the `/demo` console showed the seeded vault
(Sam/Maya records, encrypted) and epistemic chains BEFORE any conversation. Now every
pane opens empty and a fact renders ONLY once a dialogue turn actually touches it —
the graph stays fully seeded underneath for retrieval.

## What was leaking, and the mechanism now

| pane | before | now |
|---|---|---|
| Vault (`VaultPanel`) | polled `/api/facts` unconditionally — every seeded record visible on page load | gated on session load + `/api/facts?touched_since=<session_start>`; empty sections say "waiting — records appear when dialogue touches them" |
| Epistemic timeline | `/api/fact_history?since=` — TIMESTAMP filter; seeds leaked whenever seed `valid_from` ≥ session_start (reset-after-load) | `?touched_since=` — a chain renders only when a turn touched one of its facts; a supersede reveals the WHOLE chain (seed → new head) at that moment |
| Routing / conversation | already gated on `since=` + `loadedInThisSession` | unchanged |

**"Touched" is defined by the pipeline, not the clock**: the union of
(a) `injected_fact_ids` from per-turn metadata — facts the turn actually placed in
model context, and (b) fact ids written/closed by the turn (`encode_audit.jsonl`
`new_fact_id`/`prior_closed_fact_id`). Computed by `_touched_fact_ids(since)` in
`server/demo_dashboard.py`; inspectable at `GET /api/demo/touched?since=`.

**Reveal plumbing (telemetry only, seams untouched):** `process_text_query` now logs
turn metadata for EVERY routed text turn, not only guard turns (this is also the P1-2
"logged every turn" spec alignment — the text path was guard-only). No routing,
injection, grounding, or write behavior changed; the endpoints' routing-metadata
readers check router.jsonl first, so guard detection is unaffected. Endpoints keep
old behavior when the new params are absent (the dev console `/` still shows
everything).

## Verification (live tailnet dashboard, 2026-07-06)

Reset → load `reveal_demo.json` (`session_start=2026-07-06T22:15:13Z`):

```
=== LOAD STATE ===                     === AFTER TURN 1 ("What's the capital of France?") ===
vault facts:     0 rows                routing rows:  1  [(query, 'edge')]
timeline chains: 0 chains              transcript:    2  (user + "The capital of France is Paris.")
routing rows:    0 rows                vault:         3  household context rows ONLY
transcript:      0 turns                              (maya/sam PERSONAL sections still "waiting")
graph underneath: 9 seeded rows        timeline:      the same 3 household chains
```

Incremental build-up confirmed turn by turn: T2 ("What medication do I take?") added
exactly `maya/medication`; T4 (Jardiance statement) revealed the full supersede chain
`metformin (CORROBORATED, closed) → Jardiance 10mg (ASSERTED, ACTIVE)`.

**Honesty note:** household facts appear after turn 1 because INJ-4 injects household
context into every routed turn, knowledge questions included — the reveal shows
exactly what reached the model. Hiding them would misrepresent the pipeline; the
script narration now owns that beat. Personal records never appear before a turn
touches them.

## Proposed script — one capability per turn (`demo_scripts/reveal_demo.json`)

The existing three_zone/care scripts mix capabilities per turn (T01 writes AND
supersedes a seed). New ADDITIVE script, one beat each — existing scripts untouched:

| turn | member | utterance | the ONE thing it reveals |
|---|---|---|---|
| R01 | maya | "What's the capital of France?" | Routing row (edge); INJ-5 keeps personal vault empty; household context appears |
| R02 | maya | "What medication do I take?" | First PERSONAL record — appears encrypted, decrypts on screen |
| R03 | sam | "I'm allergic to penicillin, by the way." | Fact WRITE (allergy = multi-valued → clean add, no supersede noise) |
| R04 | maya | "Ray switched from metformin to Jardiance 10mg last week." | SUPERSEDE chain beat + Seam A ack |
| R05 | maya | "What medication is Ray on now?" | Post-update recall — new head, correct subject |
| R06 | maya | "What allergies do I have?" | STRUCTURAL refusal (INJ-6b, guard_triggered=true, no model call) |
| R07 | sam | "What medications does Maya take?" | Cross-member privacy — the beat is that NOTHING new appears |

## Findings surfaced by the reveal (pre-existing, logged not fixed)

- **S-INT `subject:"null"`**: R03's allergy write rendered as `sam allergy re null` —
  the known detector bug (Groq's literal `"null"` subject string accepted at
  `fact_change.py` subject fallback; first seen in encode_audit 2026-07-06T13:44:20).
  Invisible before; the reveal makes it audience-visible. Ratchet a scenario before
  fixing (seam S-INT, not display).

## Regression (all green after)

Full 10-check gate PASS — routing ≥0.90, injection 11/11, Tier F 17/17, S1-S3,
DEMO-005 4/4, trust agreement, E7/E8 idempotency, **Tier L 8/8 ratchet** (the
turn-metadata telemetry was the only pipeline-adjacent change; verified harmless).
Graph reseeded clean (D1-D9) after verification so the console is ready for HITL.
