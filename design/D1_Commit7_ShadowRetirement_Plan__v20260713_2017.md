# D-1 Commit 7: Shadow Retirement Plan

Status: PLAN
Reconciled-Against: D1_RECORD_SPEC__epistemic-record-contract__v20260712_1138.md + scripts/text_demo.py + eval/harness_baseline.json at HEAD (Mini [REDACTED-USER]@[REDACTED-TAILNET-ADDRESS]:~/hip-dev, 82cc45f)

---

## What commit 7 is and is not

Commit 7 is the text_demo side only. The engine side -- `harness/epistemic_record.py`, all 9 emit sites in `process_text_query`, GAP-1 through GAP-5 -- is already built and landed. Confirmed: `L1:HARNESS1.1` through `L1:HARNESS1.4` are all `true` in `eval/harness_baseline.json`, meaning the four Part B probes (admitted, INJ-7, P8-park, P10-confirm) are wired and green on Mini.

Commit 7 has zero engine changes. Its single job: make `text_demo.py` read the record the engine already emitted instead of computing one itself. It is the acceptance proof that the epistemic record is complete and the shadow is no longer needed.

---

## What gets deleted

### 1. `_deny_reason()` -- lines 42-71, full deletion

A 30-line hand-maintained copy of the INJ rule evaluation order. Imports and calls `_inj5_never_volunteer`, `_inj3_cross_member_deny`, `_inj1_subject_scope`, `_inj2_relevance` as private functions from `injection_contract.py`. Two confirmed staleness defects named in D1_RECORD_SPEC section 0:

- No INJ-7 branch: a cross-member refusal replays as `deny_default_cross_member` per-fact, losing the structural `access_denied` semantics of `injection_contract.py:364-365`.
- No INJ-2 declarative-bypass branch (`inj2_declarative_override`, `injection_contract.py:204`).

GAP-1 (built in earlier commits) placed the per-fact deny reason at each of the four `result.denied.append()` sites in the engine. The consume-style `text_demo.py` reads `record["withheld"][i]["deny_reason"]` from the engine-emitted record. It never calls a predicate function.

Deletion also removes the four private predicate imports from `injection_contract`. These are the only callers of those private symbols outside the engine.

### 2. `_epistemic()` -- lines 88-124, full deletion

Creates a fake `TurnOrchestrator` with `_NoopStore / _NoopModel / _NoopSpeech`, calls `orch.decide(query)`, then calls `apply_injection_contract()` directly. This is the second contract pass -- the shadow. Its `allowed` and `denied` lists are what current `admitted` and `withheld` arrays are built from.

Deletion also removes all of its imports: `_NoopStore`, `_NoopModel`, `_NoopSpeech`, `_get_text_query_router`, `TurnOrchestrator`, `apply_injection_contract`, `resolve_subject`.

### 3. `_trust_for()` -- lines 76-83, full deletion

Currently called per fact to produce `{level, basis}` via `truth_layer.queries.trust()`. In consume mode, trust comes from the engine record's `admitted[].trust` field (populated from `classify_trust_props()` at the injection site, per D1_RECORD_SPEC section 1.3). No remaining callers after deletion.

### 4. `_append_demo_log()` -- lines 207-210, full deletion

The engine now writes to `logs/turns_demo.jsonl` inside `process_text_query` via `log_epistemic_record()`. `text_demo.py` must not write a second record to the same file. The `DEMO_LOG` path constant at line 33 should be imported from `harness/epistemic_record.py` (where the engine owns it) rather than redefined here.

---

## What `_run_one()` becomes

**Current shape (lines 129-204):**

1. Call `process_text_query(query, member)` -- real reply
2. Concurrently: `wait_for_detection(session_id, 4.0)` + `_epistemic()` task
3. Assemble `admitted`/`withheld` from the shadow's `inj.allowed` / `inj.denied`
4. Call `_deny_reason()` for each withheld fact
5. Call `_trust_for()` for each admitted and withheld fact
6. Return assembled dict, write to log, print summary

**Consume-style shape:**

1. Note the current line count (or byte offset) of `turns_demo.jsonl` before the call
2. Call `process_text_query(query, member)` -- engine emits the record to the log inside this call
3. Read the last record appended to `turns_demo.jsonl` (the one just written)
4. Return that record directly; do NOT write to the log (the engine already did)
5. Print summary from the engine record's fields

`_run_one` becomes structurally thin: call, read, return. No fact iteration, no predicate calls, no trust queries. The `detection_wait` + `epistemic_task` concurrent pattern disappears entirely.

---

## Schema delta: shadow vs engine record

The engine-emitted record follows D1_RECORD_SPEC section 1.3. Several fields differ from what `text_demo.py` currently writes. All differences are deliberate. The byte-compat check must treat these as known schema evolution, not regressions.

| Field | Shadow (current text_demo) | Engine record (consume) | Classification |
|---|---|---|---|
| `admitted[].claim` | `"attribute: value"` composite string | not present | TD-030: values never in log |
| `admitted[].level` | from `truth_layer.queries.trust().level` | not present | replaced by `admitted[].trust` |
| `admitted[].basis` | from `truth_layer.queries.trust().basis` | not present | replaced by `admitted[].trust` |
| `admitted[].trust` | not present | single rung string (CONFIRMED / CORROBORATED / ASSERTED / UNCONFIRMED / DERIVED) | addition |
| `admitted[].visibility` | `fact.get("sensitivity", "")` | not in spec schema | dropped |
| `admitted[].reason` | hardcoded `"allowed"` | not in spec schema | dropped |
| `withheld[].claim` | `"attribute: value"` | not present | TD-030 |
| `withheld[].level` / `.basis` | same as admitted | replaced by `.trust` | field rename |
| `withheld[].visibility` | `fact.sensitivity` | not in spec schema | dropped |
| `net` | `"off" if tier not in ("escalate","frontier") else "on"` | `"off" iff tier == TIER_ESCALATE` | shadow logic appears inverted; engine is correct |
| `writes_pending` | absent (shadow waits 4s for detection) | `true` if detection not yet landed | behavioral change (see Risk 1) |
| `path` | absent | 9-value enum per D1_RECORD_SPEC section 3 | addition |
| `guard` block | absent | `{kind, subject}` per section 1.3 | addition |
| `record_version` | absent | `"d1.1"` | addition |
| `session_id` | absent | `"text-{member}"` | addition |

---

## The byte-compat check (D1_RECORD_SPEC section 6, step 5)

The spec language: "Do not delete the file until an L2 script run through the new path produces byte-compatible admitted/withheld fields for the pinned expected files."

### What the check is

Not a full JSON byte-for-byte diff -- the schema intentionally changes. It is a structural equivalence check on the semantically critical fields for each turn in a demo script run:

- Same set of `fact_id` values in `admitted[]` for each turn
- Same set of `fact_id` values in `withheld[]` for each turn
- Same `deny_reason` per withheld `fact_id` (engine GAP-1 label must equal what `_deny_reason()` returned for the four reason codes: `deny_never_volunteer`, `deny_default_cross_member`, `deny_subject_scope`, `deny_relevance`)
- Same trust rung per admitted `fact_id` (engine `classify_trust_props()` rung must equal shadow `truth_layer.queries.trust().level`)

The comparison deliberately excludes: `claim` (TD-030 schema change), `visibility`, `level`/`basis` (replaced by `trust`), `reason: "allowed"`.

### What "pinned expected files" means

The L2 expected files in `demo_scripts/*_expected.json` check reply content and refusal classification -- they do not contain admitted/withheld structure. The byte-compat reference must therefore be a separate baseline: a `turns_demo.jsonl` capture from the OLD shadow path for at least one full demo script run (reveal_demo or care_coordination are the natural choices given their admitted/withheld coverage). This baseline must be captured ON MINI running the current (pre-commit-7) code before the commit lands.

### The comparison procedure

1. Capture shadow-path `turns_demo.jsonl` for the chosen script (pre-commit, on Mini)
2. Run the same script through the new consume-path text_demo
3. For each turn, extract `admitted[].fact_id` set and `withheld[]` as `{fact_id, deny_reason}` pairs
4. Diff: zero mismatches required (except the known INJ-7 deny_reason divergence -- see Risk 2)
5. Trust rung comparison: map shadow `level` string to engine rung vocabulary; flag any mismatch

---

## Four risks

### Risk 1 -- `writes_pending` changes CLI demo behavior (medium)

Currently `_run_one` calls `wait_for_detection(session_id, 4.0)` before assembling the record, so writes from a declarative utterance land in the SAME record's `delta[]` array and appear in the one-line CLI summary. In consume mode the engine emits the record BEFORE async detection completes (`writes_pending: true`); the delta arrives in a subsequent record (FLAG-5 design per D1_RECORD_SPEC section 7).

`_print_turn_summary` currently reads `record["delta"]` -- this will be empty on write turns in the new path.

This is architecturally correct. But two harness tests depend on the current behavior:
- `eval/test_demo_smoke.py` checks that `turns_demo.jsonl` has a delta record with a supersede chain
- `eval/memory_harness.py` MEM-118 asserts new records in `turns_demo.jsonl` containing `delta`

Both tests currently pass because text_demo waits and includes deltas synchronously. After consume conversion, those assertions need to look for the FOLLOW-UP record (turn N+1 or the async-completion record) carrying the delta rather than the same record. These are harness updates, not engine changes. Bill must decide: are they in commit 7 scope, or is this a separate cleanup commit?

### Risk 2 -- INJ-7 `deny_reason` will differ for cross-member turns (low, known, engine is correct)

`_deny_reason()` has no INJ-7 branch. For a cross-member query it falls through to `deny_default_cross_member` at the INJ-3 check. The engine record (GAP-1) labels withheld facts with the correct `access_denied` semantics from `injection_contract.py:364-365`.

The byte-compat comparison for INJ-7 turns will therefore show a MISMATCH between shadow and engine labels. This is a known divergence -- it is the reason the spec calls the shadow stale. The engine is right, the shadow is wrong. The byte-compat check must document this as an accepted discrepancy on `path="guard_inj7"` turns and treat the engine label as authoritative.

### Risk 3 -- `DEMO_LOG` path constant duplication (low)

Currently text_demo defines `DEMO_LOG = ROOT / "logs" / "turns_demo.jsonl"` (line 33). `server/demo_dashboard.py:27` defines the same path. After the commit, `harness/epistemic_record.py` owns the path as a third definition. Consume-style text_demo still needs the path to READ the last record. The constant should be imported from `epistemic_record.py` rather than defined a third time. The `demo_dashboard.py` copy is a separate cleanup.

### Risk 4 -- `net` field logic is inverted in the shadow (low, engine is correct)

`text_demo.py` line 199: `"off" if decision.tier not in ("escalate", "frontier") else "on"`. This is backward -- most turns are not escalate-tier and would be labeled `"off"`. D1_RECORD_SPEC section 1.2 says `net: "off" iff tier == TIER_ESCALATE`. The engine-emitted record has the correct logic. The byte-compat comparison will expose this as a difference on every non-escalate turn. This is a pre-existing bug in the shadow being corrected, not a regression. Flag it explicitly in the commit description so it is not mistaken for a byte-compat failure.

---

## Three pre-flight items for Bill before commit 7 can gate

**PF-1 -- Capture the shadow-path baseline on Mini before commit 7 lands.**

Run at least one full demo script (recommend `reveal_demo.txt` or `care_coordination.txt`) through the CURRENT (shadow) text_demo on Mini and save the resulting `turns_demo.jsonl` segment as a named baseline file. This is the reference for the byte-compat comparison. If this capture does not exist before the commit, there is no reference to compare against.

**PF-2 -- Decide whether the `writes_pending` harness updates are in commit 7 scope.**

`eval/test_demo_smoke.py` and `eval/memory_harness.py` MEM-118 will need updates if the delta-in-same-record assumption is removed. Either include those harness updates in commit 7 (clean single commit, wider diff) or commit text_demo first and treat the harness fix as immediate follow-on commit 8. The gate must pass before merge either way: a commit 7 that breaks `--quick` on the harness is not mergeable.

**PF-3 -- Document the INJ-7 deny_reason mismatch as an accepted delta in the byte-compat check.**

Add a comment or assertion exclusion in the byte-compat comparison procedure that explicitly names `path="guard_inj7"` turns as the one class where shadow and engine deny_reason labels are expected to differ (shadow: `deny_default_cross_member`; engine: access_denied semantics). Without this documentation, a reviewer running the comparison will see the mismatch and not know whether it is a bug or a known correction.

---

## Merge gate

The commit merges only when:

1. `--quick` (L2 + L3) green on Mini after the text_demo changes
2. HARNESS-1 Part A still passes: ORTH-1 39/39 with the per-fact deny_reason assertions
3. HARNESS-1 Part B still green: `L1:HARNESS1.1` through `L1:HARNESS1.4` all true in baseline
4. Byte-compat check passes (zero fact_id mismatches, zero deny_reason mismatches except the documented INJ-7 exception, trust rungs match)
5. `text_demo.py` contains no `_deny_reason`, no `_epistemic`, no second `apply_injection_contract` call
6. `/epistemic` renders live during a LOAD/NEXT demo session with zero text_demo involvement

Acceptance criteria per D1_RECORD_SPEC section 8: one record per `process_text_query` call, all 9 paths, never-raise; every schema field maps to the engine source cited in section 1; no field computed by replay; text_demo contains no contract replay.
