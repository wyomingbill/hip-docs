<!-- STATUS: BUILT — harness live in eval/integration_live.py, gate check 10; baseline measured 2026-07-06 -->
<!-- RECONCILED-AGAINST: working tree on main 3bf594f + this session's changes; dev Neo4j 7688; Groq + Ollama live -->

# Tier L — Live-Path Integration Harness (E1-E8) and the Honest Baseline

Phase 2 of the integration plan: a harness that MEASURES the path the demo/browser
actually uses, and the recorded pass/fail baseline before any seam is wired (Phase 3).
Note: `docs/testing/LATEST_INTEGRATION_TEST_PLAN.md` did not exist in the checkout when
this phase started; the E1-E8 definitions came from the phase instruction and are now
recorded here — this document is the plan of record for Tier L
(`LATEST_INTEGRATION_TEST_PLAN.md` now points here).

## What "live path" means (and what the harness deliberately avoids)

`eval/integration_live.py` subprocess-launches the REAL server
(`python -m server.voice_https_orch --host 127.0.0.1 --port 7996`) and drives every
turn over HTTPS `POST /api/text-query` — the exact route the browser demo hits
(`voice_https_orch.py:94` → `process_text_query`, `voice_orch.py:2098`). It does NOT
use the in-process text shim (`scripts/text_demo.run_query`, which DEMO-005 uses) and
does NOT touch the unwired `memory_engine.api.candidate_facts()` path. Graph state is
asserted directly on dev Neo4j 7688; trust via `truth_layer.queries.trust()`; history
via a supersession-chain walk.

**Determinism:** fixture reset (`scripts/demo_reset.py --yes` + `scripts/demo_seed.py`,
D1-D9) before the server starts; fixed scenario order; async Groq detection handled by
polling to a 20s ceiling (writes) or a 12s settle (no-op assertions). Two consecutive
full runs produced identical results on every check, including the E3 leak wording.

**Ratchet:** results are compared to `eval/integration_live_baseline.json`. Known seam
gaps stay recorded as expected failures; the gate (check 10 in `scripts/gate_check.sh`)
fails ONLY on a regression below the baseline. Improvements print a notice to update
the baseline (`--update-baseline`).

## PREREQ — ENV-1 fixed

`eval/integration_harness.py:_machine_guard` now tries `socket.gethostname()` before
`socket.getfqdn()` (getfqdn reverse-resolved `::1` to an ip6.arpa name under this
machine's current DNS state, rejecting the real dev box). Gate step 3 runs green
without a shim: 17/17.

## E1-E8 live-path baseline (2026-07-06, two identical runs)

| id | scenario | LIVE result | what passed | what failed (the seam) |
|---|---|---|---|---|
| E1 | statement writes ONE supersede + acknowledges | **FAIL** | Graph side is fully correct: exactly one supersede (2 nodes: seed + new), seed metformin closed with `closed_reason='superseded'` → new head, trust(new)=ASSERTED | Reply is `"I don't have that confirmed yet."` — the TD-052 grounding guard fires against the pre-write fact snapshot, so the CORRECTION RULE ack never happens (S-INT/disclosure: injected facts are retrieved before the async write lands) |
| E2 | recall retrieves the new value | **FAIL** | History unchanged by the question; trust unchanged (ASSERTED) | Reply is the same refusal — Jardiance IS the active graph fact but never reaches the model usefully (S-RET presentation + grounding guard) |
| E3 | simple personal → EDGE + correct answer | **FAIL** | tier=edge, intent=personal; answer names lisinopril; seed trust intact (CONFIRMED); no write from a question | **Cross-subject leak**: reply = `"You take lisinopril each morning and Jardiance 10mg."` — Ray's subject=ray medication presented as Maya's own (INJ admits it as her owned fact; the prompt's second-person framing erases the subject) |
| E4 | complex personal → CORE | **PASS** | tier=core via complexity axis (bloom 6), non-empty answer | (content quality note: reply begins "I don't have information about Ray" — retrieval seam visible but out of scope for E4's routing assertion) |
| E5 | cross-subject privacy: Maya re Ray, own facts withheld | **PASS** | lisinopril not disclosed; cardiology appointment not volunteered; no write | (passes trivially today because the reply is a blanket refusal — will need re-reading once E2 is wired) |
| E6 | empty-set personal → structural refusal | **FAIL** | Refusal WORDING present | `guard_triggered=False` — the INJ-6 structural guard did NOT fire; the refusal came from the model's prompt rule, not the empty-set guard (admitted set was non-empty: medication facts survive INJ-2 for an allergy query) |
| E7 | fact_history single clean chain | **PASS** | 2 nodes, 1 head; values distinct (no Jardiance→Jardiance churn); closed row points at the active head | |
| E8 | idempotency: replay E1 verbatim = no-op | **PASS** | Node count and active fact_id unchanged after replay + 12s settle — this session's `fact_change` idempotency guard holding on the live path | |

**Baseline: 4/8 PASS** — committed as `eval/integration_live_baseline.json`:
`{"E1": false, "E2": false, "E3": false, "E4": true, "E5": true, "E6": false, "E7": true, "E8": true}`

## Reading the failures (Phase 3 targets, in dependency order)

1. **E1/E2 (one seam, two symptoms):** the model answers from a fact snapshot
   retrieved BEFORE the turn's own write (and the write itself is async). Wiring
   post-write context (or the CORRECTION-RULE ack path) fixes E1; making the
   next-turn retrieval surface the new head fixes E2. Graph and trust layers already
   behave correctly — this is purely the disclosure seam.
2. **E3 (new finding, not in the call-graph divergence table):** subject-scoped facts
   (`subject=ray`, `owner=maya`) are injected into "Things you know about this
   person" and rendered second-person, so care-recipient facts read as the owner's
   own. INJ-1 subject scoping admits by owner; the prompt renderer drops the subject.
3. **E6:** INJ-6 can only fire on an EMPTY admitted set; INJ-2 relevance keeps
   same-owner facts alive for an allergy query, so the structural refusal is
   unreachable for this shape — refusal is currently model-behavioral.
4. **E5 caveat:** re-assert after E2 is wired; today's pass is downstream of the
   blanket refusal.

## Gate integration

`scripts/gate_check.sh` check 10 runs `eval/integration_live.py` (no flags) every gate:
fixture reset → real server → E1-E8 → ratchet vs the committed baseline. Full gate
(checks 1-10) verified green after this change — see inline summary in the session
log; Tier L adds ~2-3 min (server warmup + 9 live turns + detection settles).
