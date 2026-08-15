<!-- STATUS: BUILT — full test plan executed 2026-07-06 and reconciled against docs/research/LATEST_LIVE_CALLGRAPH.md -->
<!-- RECONCILED-AGAINST: main b3a95a4 + idempotency fix working tree; dev Neo4j 7688; Ollama up; Groq live -->

# Test-Plan Run + Reconciliation Against the Live Call Graph

Every runnable suite was executed on 2026-07-06 (dev machine, dev Neo4j 7688) and its
coverage reconciled against the traced live call graph
(`docs/research/LATEST_LIVE_CALLGRAPH.md`). Includes the E7/E8 idempotency gate added
this session (red pre-fix → green post-fix) per the pinned self-supersede trigger.

## 1. Results

| suite | scope | result | notes |
|---|---|---|---|
| `scripts/routing_harness.py` (gate 1) | Bloom/complexity classifier | **PASS** 63/69 = 91.3% ≥ 90% | 6 adjudicated MISS rows, all pre-known shapes |
| `eval/injection_harness.py` (gate 2) | INJ-1..6 contract | **PASS** 11/11 | text-path contract only (see R3) |
| `eval/integration_harness.py --tier F` (gate 3) | INT-001..014 + SV-001..004 boundary | **PASS** 17/17 | via env shim — see ENV-1 |
| `eval/test_seam_s1_mute_window.py` (gate 4) | STT↔mute window | **PASS** | |
| `eval/test_seam_s2_intent_routing.py` (gate 5) | intent↔tier | **PASS** 18/18 | |
| `eval/test_seam_s3_facts_grounding.py` (gate 6) | guard/injected consistency | **PASS** 11/11 + 11/11 | |
| `eval/test_demo_smoke.py` DEMO-005 (gate 7) | E2E: reset+seed, 6 turns, live Groq detection | **PASS** 4/4 (34s) | A1 confirms real supersede still detected post-fix |
| `eval/test_trust_classifier_agreement.py` (gate 8) | `_classify_trust` == `trust()` | **PASS** 11/11 | |
| `eval/test_idempotency_e7_e8.py` (gate 9, **NEW**) | one turn writes once; replay no-op | **FAIL pre-fix** (2 writes/cycle; replay churned lineage) → **PASS post-fix** | ratcheted into gate_check.sh |
| `eval/memory_harness.py` (engine track) | MEM-100..118 (17 scenarios) | **PASS** 17/17 | re-run post-fix: still 17/17 |
| `eval/truth_harness.py` (engine track) | TRUTH-101..106 | **PASS** 6/6 | |

**ENV-1 (environmental, not code):** `integration_harness._machine_guard()` uses
`socket.getfqdn()`, which on this machine currently reverse-resolves `::1` to
`…ip6.arpa` instead of `[REDACTED-MACHINE-NAME]` (DNS state changed since the
2026-07-05 green run; `socket.gethostname()` and `hostname` are correct). The harness
was run through a one-line runner shim (`socket.getfqdn = gethostname`) after verifying
the machine three independent ways. Left unfixed per scope discipline; the one-line
robustness fix (`gethostname() or getfqdn()`) is noted for a future session. Until then
`gate_check.sh` step 3 fails on this DNS state even though all 17 scenarios pass.

## 2. Reconciliation — suite coverage vs what the call graph shows actually runs

| # | call-graph finding (seam) | tested today by | reconciliation verdict |
|---|---|---|---|
| R1 | **S-INT**: live interpretation is bare-Groq 3-action + hardcoded `WriteDecision(supersede, None, 0.75)` (`fact_change.py`); governed `classify_write()` unwired | DEMO-005 A1 (live Groq detect); E7/E8 (mapping+writer, deterministic); MEM-116/117/118 | Detector/mapping/writer now covered incl. idempotency. **No suite exercises `GroqInterpreter.classify_write` in a pipeline context** — correct: it is unwired; tests would assert dead wiring |
| R2 | **S-WRITE**: per-turn writes via `encode()` (audited); session-end Path B via `_write_one` bypasses engine (no write_state/audit; `closed_by` vs `closed_reason`) | MEM-101..104, MEM-117, TRUTH-106 cover `encode()` | **GAP-1: Path B untested** — no scenario asserts `_write_one` node shape or its trust outcome (permanently UNCONFIRMED). If Path B is ever governed, a MEM scenario must ratchet first |
| R3 | **DIV-2**: injection contract runs on TEXT path only; voice path has permissions filter + guest lockout only | injection_harness + INT-001..006 drive `apply_injection_contract` / `process_text_query` | **GAP-2: the passing contract suites prove the TEXT boundary only.** No suite drives `_on_user_text` end-to-end asserting INJ behavior — and it would fail today (contract absent on voice). Gate green ≠ voice governed |
| R4 | **S-CLS**: `trust()` never runs in a live turn; only dashboard/demo-log/evals | TRUTH-104 (predicates), gate 8 (classifier agreement) | Classification logic is well tested; **no test asserts trust reaches disclosure** — correct: it doesn't (governed gap, not test gap) |
| R5 | **S-RET**: live retrieval is `search_facts_by_embedding \|\| read_user_facts` (×2 per turn), no tier/temporality; `candidate_facts()` unwired | MEM-105/106/107 test **`candidate_facts()`** — the unwired path | **GAP-3: cold-exclusion / temporality invariants are only proven on the path the pipeline doesn't use.** `read_user_facts`/`search_facts_by_embedding` have no dedicated eval; a cold-tier fact with `valid_to=null` would inject live and no gate would catch it |
| R6 | **S-CONS**: `run_consolidation` has zero production callers | MEM-108/109/110/113 exercise it offline | Consistent: engine-track tests match offline-only reality. Nothing to reconcile until a scheduler exists |
| R7 | **Idempotency** (pinned trigger): demo-turn re-processing re-writes an already-current value; no no-op at detector/mapping/writer | **Nothing pre-existing** — DEMO-005 resets the graph each run, so replay churn was structurally invisible to the gate | **Closed this session**: E7/E8 written first (red), fix applied, green, ratcheted as gate 9 |
| R8 | Question turns fire `detect_and_apply_async` but die at cheap gates (`fact_change.py` <4 words / "?" / opener) | E7/E8 indirectly (constructed changes bypass gates); DEMO-005 T03/T05/T06 question turns produce no deltas | Adequate; gates are inside `detect_and_apply`, single place |

## 3. E7/E8 evidence (red → green)

Pre-fix (`eval/test_idempotency_e7_e8.py` against dev graph, throwaway owner):
```
E7: expected 1 mutation, got 2          (duplicate changes in one cycle → 2 writes)
E8: expected 0 mutations, got 1         (replay closed the identical fact, new fact_id)
```
Post-fix:
```
[E7]  PASS — duplicate changes in one cycle → 1 write (mutations=1, nodes=1)
[E8]  PASS — re-processing same value → 0 mutations, same fact_id active, no new node
[E8b] PASS — new value still supersedes (old closed) — no over-suppression
```
Fix (scoped to the pinned trigger only): value-equality idempotency guard in
`fact_change._apply_changes` — new helper `_active_values()` decrypts ALL active values
for the `(owner, subject, attribute)` supersession key (covers MULTI_VALUED augment
duplicates too); a case-insensitive exact match logs a `change_detect` lifecycle no-op
and skips `encode()`. No seam rewiring; detector prompt, mapping, `encode()`, and the
frozen pipeline untouched. Post-fix regression: gate checks 1-2,4-9 PASS; gate 3 PASS
via ENV-1 shim (17/17); memory_harness 17/17; truth_harness 6/6; DEMO-005 4/4 with the
genuine metformin→Jardiance supersede still detected (A1).

## 4. Open gaps carried forward (do NOT fix unattended — ratchet first)

1. **GAP-1** Path B (`_write_one`) has no node-shape/trust scenario.
2. **GAP-2** Voice path has no injection-contract coverage (and would fail — DIV-2).
3. **GAP-3** Live retrieval functions have no tier/cold-exclusion eval; MEM-107's
   invariant does not protect the wired path.
4. **ENV-1** `getfqdn()` machine guard is DNS-fragile; gate step 3 red on this machine
   until the guard reads `gethostname()` first.
