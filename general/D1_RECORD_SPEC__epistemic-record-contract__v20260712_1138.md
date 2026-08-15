# D-1 Epistemic Record Contract

**File:** `docs/general/D1_RECORD_SPEC__epistemic-record-contract__v20260712_1138.md`
**Status:** SPEC ONLY. No code written. Every citation verified against the working tree on Mini ([REDACTED-USER]@[REDACTED-TAILNET-ADDRESS]:~/hip-dev) at HEAD 82cc45f, 2026-07-12.
**Companion:** DEMO_SPEC__v20260712T0800.md (decision D-1). This document is the schema authority for the epistemic record (FLAG-5 there / FLAG-5 here differ; see section 7).

---

## 0. The one-sentence contract

`process_text_query()` emits exactly ONE epistemic record per turn, built from the REAL `InjectionResult` produced by the single `apply_injection_contract()` pass inside `assemble_governed_context()` (voice_orch.py:2343-2350), via a never-raise helper `harness/epistemic_record.py` modeled on `harness/turn_metadata.py` (build at :63, log at :114) -- killing the `text_demo.py` shadow.

**Why the shadow must die:** `text_demo.py:_deny_reason` (scripts/text_demo.py:42-71) re-runs `_inj5/_inj3/_inj1/_inj2` predicates in a hand-maintained copy of contract order. It is ALREADY STALE: it has no INJ-7 branch (a cross-member-refused turn replays as `deny_default_cross_member` per-fact, missing the structural `access_denied` semantics of injection_contract.py:364-365), and no INJ-2 declarative-bypass branch (`inj2_declarative_override`, injection_contract.py:204). Every future contract change widens the drift. The record must come from the engine's own result object, never a replay.

---

## 1. Record schema

One JSON object per turn, appended to `logs/turns_demo.jsonl` (path constant: server/demo_dashboard.py:27). Field-for-field, each value maps to a real engine source -- nothing is computed inside the record writer beyond formatting.

### 1.1 Envelope

| Field | Type | Engine source |
|---|---|---|
| `record_version` | `"d1.1"` | literal |
| `turn_id` | str | uuid4 at emit time (as turn_metadata does) |
| `ts` | ISO-8601 UTC | emit time |
| `session_id` | str | `f"text-{member}"` (voice_orch.py:2428) |
| `member` | str | `process_text_query(query, member)` arg (voice_orch.py:2406) |
| `query` | str | the raw utterance arg |
| `reply` | str | the returned reply string of whichever return path fired |
| `path` | enum, section 3 | which of the 9 return paths emitted (e.g. `"generation"`, `"guard_inj7"`, `"confirmation"`) |

### 1.2 Routing block (source: `RouteDecision`)

| Field | Engine source |
|---|---|
| `tier` | `decision.tier` from `d = await orch.decide(_run_query)` (voice_orch.py:2534), post `_force_tier` override (:2541-2543) |
| `complexity` | `decision.complexity` |
| `bloom` | `RouteDecision.bloom` (harness/router.py:120; hard bloom-to-tier mapping :529-541) |
| `tier_target` | resolved model: `GROQ_MODEL_MID`/`GROQ_MODEL_CORE` (voice_orch.py:149-151) or `LOCAL_MODEL` (:90); special values `"confirmation_gate"`, `"system-clock"`, `"control_flow"`, `"access_control_guard"`, `"injection_guard"` on non-generation paths (exactly the tier_target strings already written to transcripts/metadata on those paths) |
| `net` | `"off"` iff tier == TIER_ESCALATE (router.py:72; off-net only via capability/freshness axes, sensitivity blocks the boundary, router.py:669-697), else `"on"` |
| `sensitivity_tag` | `d.get("sensitivity_tag")` (voice_orch.py:2545) |
| `intent` | the `_intent` passed to assemble_governed_context |
| `sio_source` | telemetry field already threaded (voice_orch.py:2360) |

### 1.3 Disclosure block (source: `InjectionResult`, injection_contract.py:183-204)

| Field | Engine source |
|---|---|
| `admitted[]` | one entry per fact in `inj.allowed` (:411): `{fact_id, attribute, owner, subject, trust, write_state}`. `trust` from `classify_trust_props()` (memory_engine/trust.py:56-78) over the fact's properties -- the five rungs CONFIRMED / CORROBORATED / ASSERTED / UNCONFIRMED / DERIVED per TRUST_RANK (trust.py:27-32). **Never the fact value** (TD-030: values render only via the vault's decrypt path, never in a log file). |
| `withheld[]` | one entry per fact in `inj.denied` (:379, 385, 391, 405): `{fact_id, attribute, owner, subject, deny_reason}`. `deny_reason` requires GAP-1 (section 2). Subject to FLAG-1 display scoping (section 7) -- the record CARRIES withheld entries; renderers decide what may be shown. |
| `denied_counts` | `{inj1, inj2, inj3, inj5}` straight from `denied_inj1/2/3/5` (:198-201) -- the cross-check that per-fact labels sum to per-rule counts (HARNESS-1, section 5) |
| `inj2_declarative_override` | `:204` -- count of facts admitted via declarative value-match bypass |
| `guard` | `null`, or `{kind: "empty_set" \| "attr_empty_set" \| "access_control", subject}` -- kinds require GAP-2; `access_control` maps `inj.access_denied` + `access_denied_subject` (:194-195) |
| `resolved_subjects` | telemetry field (voice_orch.py:2358) from `resolve_subject()` (:2341) |
| `injected_fact_ids` | `inj.injected_fact_ids` (:2359) -- kept for turn-metadata parity checks |

### 1.4 Write / state-transition block (source: encode audit + confirmation gate)

| Field | Engine source |
|---|---|
| `delta[]` | per completed write this turn: `{attribute, owner, subject, from_fact_id, to_fact_id, from_trust, to_trust, write_state, cause_utterance}`. Source: the `encode()` result already surfaced through the encode-audit log that `_touched_fact_ids` reads (`new_fact_id`/`prior_closed_fact_id`, demo_dashboard.py:121-136); trust rungs via `classify_trust_props` on the closed and new rows. `from_value`/`to_value` are NOT carried (TD-030); `/epistemic`'s value strip renders via decrypt at read time or displays attribute-only. |
| `park` | `null`, or `{parked_fact_id, head_fact_id, incoming_trust, head_trust}` when encode returns `actual_state == "unresolved"` with `override_reason` starting `"P8 "` (registration point: harness/fact_change.py:497-508; the park itself: memory_engine/store.py:397-415, Override 4) |
| `confirmation` | `null`, or `{verdict: "confirm" \| "decline", parked_fact_id, promoted_to: "ASSERTED" \| null}` from the P10 gate (`check_confirmation` harness/confirmation_gate.py:109-143; `apply_confirm` :148-183 promotes to write_state=supersede/confidence=medium = ASSERTED, deliberately not `confirmed_by`; `apply_decline` :185-201) -- requires GAP-4 |
| `writes_pending` | bool -- `true` when `detect_and_apply_async` was dispatched this turn and its result has not landed (voice_orch.py:2825-2832 dispatch; Seam A synchronous case :2564-2577 sets it `false` because detection completed in-turn). See FLAG-5. |
| `guard_triggered` | bool -- `inj.guard_triggered` verbatim (compat with existing `/epistemic` renderer, epistemic.html:551-556) |

Timing fields (`routing_ms`, `inference_ms`) mirror what `build_turn_metadata` already carries (turn_metadata.py:63) for cheap parity checking.

---

## 2. The five gaps -- engine info discarded today, to BUILD (not fake)

**GAP-1 -- per-fact deny reason.** `InjectionResult` counts denials per rule (`denied_inj1/2/3/5`, injection_contract.py:198-201) but `denied` is a bare fact list -- WHICH rule denied WHICH fact is discarded at each of the four `result.denied.append(fact)` sites (:379 INJ-5, :385 INJ-3, :391 INJ-1, :405 INJ-2). Build: one line at each append site records the reason -- either a parallel `denied_reasons: list[str]` or appending `(fact, reason)` tuples. Reason vocabulary is pinned to the four existing codes (`deny_never_volunteer`, `deny_default_cross_member`, `deny_subject_scope`, `deny_relevance` -- the codes `/epistemic` already renders, epistemic.html:438-443) so the renderer needs no change.

**GAP-2 -- INJ-6 vs INJ-6b collapsed.** Both guards set the same `result.guard_triggered = True` -- INJ-6 empty-set at injection_contract.py:421, INJ-6b attribute-targeted (Seam B) at :445. The record (and HARNESS-1) needs `guard_kind`: add a field set to `"empty_set"` at :421 and `"attr_empty_set"` at :445 (first-writer-wins; INJ-6b's condition already excludes the INJ-6-fired case via `not result.guard_triggered`, :431). `access_control` derives from the existing `access_denied` flag -- no new engine state.

**GAP-3 -- full InjectionResult discarded on success.** On the success path `assemble_governed_context` copies only `resolved_subjects` + `injected_fact_ids` + `sio_source` into the caller's telemetry dict (voice_orch.py:2357-2360) and returns a prompt STRING (:2402-2405 return orch.local_system_prompt(...)); `inj` -- the denied list, per-rule counts, override count -- dies in scope. Build: extend the existing telemetry side-channel (same pattern, zero API break: callers that pass no telemetry see no change) to carry the fields of section 1.3; alternatively return `(prompt, inj)` behind a keyword flag. The telemetry-dict extension is preferred -- it is the established seam and `OrchestratorGate._on_user_text` uses the same one.

**GAP-4 -- confirmation-gate turns emit no metadata.** The P10 branch (voice_orch.py:2430-2445) writes two transcript turns and returns `CONFIRM_REPLY`/`DECLINE_REPLY` -- no `log_turn_metadata`, no record of WHICH parked fact was resolved. `apply_confirm`/`apply_decline` know the parked_fact_id and outcome but return it only to their internal audit trail. Build: capture the gate's result (parked_fact_id, verdict, promoted state) at the call site and emit the record's `confirmation` block on this return path. Same for the park side: `fact_change.py:497-508` registers the park -- the registration already has everything the `park` block needs; it must be surfaced to the emitting turn (Seam A synchronous case) or the follow-up record (async case, `writes_pending` -> landed).

**GAP-5 -- timeline holes: local-now / drop / control-flow.** Three return paths write transcripts but no turn metadata and would emit no epistemic record naively: local-now (:2465), routing `drop` (:2549 -- writes only the user transcript line, not even a reply), control-flow decline/confirm-needed (:2493, :2515). On these paths no facts were retrieved and no contract ran -- and that is exactly what the record must SAY, not skip: emit with `path` set, empty disclosure block, `tier_target` `"system-clock"`/`null`/`"control_flow"`. A timeline with silent holes invites the renderer to interpolate; an explicit `path: "local_now"` card is honest and cheap.

---

## 3. Emit point: one never-raise helper at all 9 return paths

**Correction to the tasking note:** `process_text_query` has NINE return statements, not eight (grep verified at HEAD 82cc45f):

| # | Line | Path enum | Disclosure block | Notes |
|---|---|---|---|---|
| 1 | voice_orch.py:2445 | `confirmation` | empty | + `confirmation` block (GAP-4) |
| 2 | :2465 | `local_now` | empty | GAP-5 |
| 3 | :2493 | `control_decline` | empty | RECONSIDER decline; GAP-5 |
| 4 | :2515 | `control_pending` | empty | FRONTIER confirm-needed/decline; GAP-5 |
| 5 | :2549 | `drop` | empty | reply is `""`; GAP-5 |
| 6 | :2641 | `guard_inj7` | withheld only, `guard.kind="access_control"` | from `DisclosureBlocked` fields (:2350) + GAP-1 for the withheld list |
| 7 | :2672 | `guard_empty_set` | `guard.kind` per GAP-2 | |
| 8 | :2721 | `generation_placeholder` | full (GAP-3) | local placeholder branch; already logs turn metadata (:2699-2704) |
| 9 | :2831 | `generation` | full (GAP-3) | main path; turn metadata at :2805-2820 |

**Design (mirrors turn_metadata.py):** `harness/epistemic_record.py` exposes `build_epistemic_record(...)` (pure dict assembly, like build_turn_metadata :63) and `log_epistemic_record(record)` (append-only JSONL writer, like log_turn_metadata :114). The log function is wrapped so that NO exception escapes -- a failed record write must never fail a user turn (same stance turn_metadata takes). Each return path calls the helper immediately before returning; the two generation paths pass the telemetry-carried InjectionResult fields (GAP-3), the guard paths pass the DisclosureBlocked payload, the rest pass path + envelope only.

**Where NOT to emit, and why:**
- **NOT inside `apply_injection_contract`** -- ORTH-1's disclosure-conformance suite (39 cases, `DISC:conformance` ratcheted true in eval/harness_baseline.json) drives the contract as a pure function offline. A side-effecting writer inside it breaks that purity, entangles the conformance suite with the filesystem, and double-emits on text_demo's second pass while the shadow still exists.
- **NOT in `text_demo.py`** -- that IS the shadow being killed (section 6).
- **NOT in `assemble_governed_context`** -- it is called by three consumers (process_text_query, OrchestratorGate voice, RealtimeAdapter connect); emitting there triples records and voice must NOT emit yet (FLAG-8).

**Free rider:** the demo player (`demo_run.fire_next_turn`, scripts/demo_run.py:192-250; and the autonomous `run_script` :97-159) calls `process_text_query` directly (:231-233) -- once emission lives in the engine, every LOAD/NEXT and auto-run turn produces a record with zero demo_run changes. The `/epistemic` page and the demo Governance Feed both light up from the same file.

---

## 4. Session filtering

Records carry `ts`; `/api/turns` (demo_dashboard.py:420-437) grows a `since=` param mirroring `/api/transcript?since=` (:440-470) so the demo page's `sessionStart` filter (demo.html:1369) applies. `/epistemic`'s existing no-filter behavior is preserved when `since` is absent.

---

## 5. HARNESS-1: two-part fidelity gate

**Part A -- offline, riding ORTH-1.** The disclosure-conformance suite already drives `apply_injection_contract` over 39 pinned cases. Extend each case's assertions:
- per-fact `deny_reason` labels are internally consistent: count of label X == `denied_injN` counter for the matching rule (catches a mislabeled append site forever);
- `guard_kind` is pinned per case group: empty-set cases assert `"empty_set"`, Seam-B cases assert `"attr_empty_set"`, INJ-7 cases assert `access_denied` with no guard_kind conflation;
- `inj2_declarative_override` cases assert the admitted fact carries no deny label.
No live infra, no LLM, runs in `--quick`. This is the ratchet: `DISC:conformance` stays a single boolean gate, now with wider teeth.

**Part B -- live probes, `L1:HARNESS1`.** Four probe turns through the REAL `process_text_query` against seeded state (fixture manager per eval/harnesslib/fixture.py), each asserting three-way agreement -- epistemic record == turn metadata == Neo4j:
1. **admitted** -- personal retrieval turn: record `admitted[].fact_id` set == metadata `injected_fact_ids` == the Neo4j facts whose owner/subject match; every admitted entry's `trust` matches `classify_trust_props` re-run against the live node.
2. **INJ-7** -- cross-member query: record `path="guard_inj7"`, `guard.kind="access_control"`, `admitted == []`; metadata target `access_control_guard` (voice_orch.py:2618-2645); no new Neo4j rows.
3. **P8-park** -- cross-principal lower-rank write: record `park` block populated; Neo4j shows two active rows (retained head + parked `unresolved`); `writes_pending` semantics honored (Seam A sync -> park in same record).
4. **P10-confirm** -- bound-actor "yes": record `path="confirmation"`, `confirmation.verdict="confirm"`, `promoted_to="ASSERTED"`; Neo4j head now the promoted row, old head closed.
Ratchet as `L1:HARNESS1.*` booleans in harness_baseline.json alongside the existing L1 invariants.

---

## 6. Migration: retiring the shadow

Order matters; each step gates before the next:
1. **Build** GAP-1 + GAP-2 (contract fields) -> gate: ORTH-1 39/39 + L3 guard mutation + full P1-P10.
2. **Build** GAP-3 (telemetry extension) + `epistemic_record.py` + all 9 emit sites + GAP-4 + GAP-5 -> gate: full regression + HARNESS-1 Part A.
3. **Wire** HARNESS-1 Part B, ratchet.
4. **Flip consumers.** Readers of the new record: `/epistemic` page (already schema-compatible -- section 1 is a superset of text_demo's record: turn_id, member, query, reply, tier, intent, bloom, net, admitted, withheld, guard_triggered, delta all preserved, text_demo.py:189-204); the demo page's Governance Feed (DEMO_SPEC D-2, new); auto-run (DEMO_SPEC Stage 2 -- free via section 3); voice (Phase 4 ONLY, FLAG-8).
5. **Retire** `text_demo.py`'s second decide() + contract pass (:132-135) and `_deny_reason` (:42-71): it becomes a thin CLI that calls `process_text_query` and reads back the engine-emitted record (Phase-B-consume style). Do not delete the file until an L2 script run through the new path produces byte-compatible admitted/withheld fields for the pinned expected files.
6. `demo_run.py` and `/api/text-query`: no changes (both already call process_text_query).

---

## 7. The eight temptation flags

Each names a demo requirement that will tempt a faked state, and the rule that forbids it.

**FLAG-1 -- INJ-7 withheld panel.** The Governance Feed's withheld column makes it tempting to show WHAT was withheld on a cross-member refusal ("Maya's medication -- denied"). NEVER. On `guard.kind="access_control"` turns the panel renders an EMPTY withheld list plus a membership banner ("access boundary: personal facts of another member"). Fetching another member's fact attributes in order to display them as withheld IS the boundary violation the contract exists to prevent -- and INJ-7 is existence-invariant by design (injection_contract.py:190-195): it fires whether or not facts exist, so any display of real withheld entries leaks existence. The record for these turns carries the guard block, not a fact list (the engine raises DisclosureBlocked before the denied list is populated for the target subject -- do not "enrich" it afterward).

**FLAG-2 -- no second contract pass.** When a pane wants a field the record lacks, the temptation is to re-run `apply_injection_contract` at render time (text_demo's sin). Forbidden: one pass per turn; missing fields are a GAP to build in the engine.

**FLAG-3 -- no deny-reason replay.** Same temptation, smaller: re-deriving deny reasons in the writer or renderer by calling `_inj*` predicates. Forbidden -- that recreates the drift this spec kills. Reasons come from GAP-1's append-site labels only.

**FLAG-4 -- guard records must be complete.** A DisclosureBlocked turn is the demo's money shot; the temptation is to emit a minimal record and let the UI infer the refusal type. Every guard record must carry `guard.kind`, `path`, and (for access_control) the subject -- inferred UI states drift from enforcement.

**FLAG-5 -- never predict a write chip.** A declarative utterance ("Elena switched to Ozempic") tempts the UI to show a "fact written" chip immediately -- but detection is ASYNC (detect_and_apply_async fires post-reply, voice_orch.py:2825-2832) and may not land, may park, or may write something other than the utterance's surface shape. Render `writes_pending` until the record (or a follow-up record on the next turn) carries the real `delta[]`/`park`. Utterance shape is not a write.

**FLAG-6 -- park and confirm are separate events.** The temptation: collapse P8 park + P10 confirm into one "update" delta for a cleaner strip. Forbidden -- the two-active-row parked state IS the demonstrable safety property (P8 monotonicity, store.py:397-415); the record keeps `park` and `confirmation` as distinct blocks on distinct turns.

**FLAG-7 -- the record is not an SIO consumer.** Temptation: enrich the record from SIO fields (attribute guess, subject names) when the contract result looks sparse. The SIO is a proposal with no authority (HIP_STATE section 1.2); the record reports what the CONTRACT and ENCODE did, full stop. `sio_source` is carried for audit; no other SIO field enters the record.

**FLAG-8 -- voice emits nothing until Phase 4.** The voice adapter assembles governed context once at connect (realtime_adapter.py:301-302) and does not run the per-turn governed path -- a per-turn epistemic record for voice turns would be a record WITHOUT enforcement: smoke. Voice turns emit no record until Phase 4 routes each voice turn through `assemble_governed_context` per turn with the same telemetry seam. Silent panes are correct; wrong panes are misleading. (The OrchestratorGate text path :1598 IS governed per turn and may emit when its sites are wired -- explicitly out of scope for the first build.)

---

## 8. Acceptance

1. One record per `process_text_query` call, all 9 paths, never-raise.
2. Every schema field maps to the engine source cited in section 1; no field computed by replay.
3. ORTH-1 39/39 with Part-A assertions; `L1:HARNESS1.*` green; full P1-P10 + L2-L5 + DISC + SCHEMA + VOICE conformance green before each commit (engine-change discipline).
4. text_demo.py contains no contract replay and no `_deny_reason`.
5. `/epistemic` renders live during a LOAD/NEXT demo session with zero text_demo involvement.
6. All eight FLAGs hold under review of the diff -- each has a named reviewer check in the PR description.
