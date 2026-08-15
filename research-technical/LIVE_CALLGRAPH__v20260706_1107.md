<!-- STATUS: BUILT — traced from live code, read-only, 2026-07-06 -->
<!-- RECONCILED-AGAINST: main @ 2213512 (working tree clean for cited files), logs/ evidence 2026-07-06 -->

# HIP Live Integration Map — Call Graph, Seam Inventory, Idempotency Root Cause

The ACTUAL ordered function calls for one statement turn and one question turn —
utterance-in → response-out → graph-write — through the live orchestrator
(`harness/orchestrator.py` + `server/voice_orch.py`), plus the seam-by-seam
live-vs-governed inventory and the pinned trigger for the Jardiance→Jardiance
supersede loop. Companion to `LATEST_EPISTEMIC_PROCESS.md` (divergence analysis;
DIV numbers referenced below), `LATEST_SYSTEM_UNIVERSE.md`, `LATEST_FACT_LIFECYCLE.md`.

**Live entry points** (server `server/voice_https_orch.py`, port 7860):
- **Text** (Track A demo surface): `POST /api/text-query` (`voice_https_orch.py:94`)
  → `process_text_query()` (`voice_orch.py:2098`). Also driven by
  `scripts/demo_run.py:143,233` (script runner / presentation `fire_next_turn`),
  `scripts/text_demo.py:145`, `scripts/demo_player.py:149`, `POST /api/voice-query`
  (`voice_https_orch.py:315`).
- **Voice**: WebRTC frames → `OrchestratorGate.process_frame()` (`voice_orch.py:1074`)
  → `_flush_utterance()` (`:1132`) → `_on_user_text()` (`:1256`).

`TurnOrchestrator.handle_turn()` (`orchestrator.py:411`) remains the canonical compose
but is NOT wired into either live path (`orchestrator.py:29`); both live handlers use
only `decide()` + `local_system_prompt()` and re-implement the rest differently.

---

## Trace A — Statement turn (text path)

Utterance: `bill: "My mother Elena was switched from metformin to Jardiance, ten
milligrams, starting this week."` (care_coordination.json T01 — the demo turn that
produces the supersede loop; transcript evidence in §Idempotency).

```
 1. hip_api_text_query()                       voice_https_orch.py:94
    ├─ get_member_by_id("bill")                voice_https_orch.py:115 (member_registry)
    ├─ _log_line_count() ×2 (router/meta snapshot)  voice_https_orch.py:126-127
    └─ process_text_query(query, "bill")       voice_https_orch.py:130 → voice_orch.py:2098
 2. is_local_now_query(query)                  voice_orch.py:2119 (temporal.py:123) → False
 3. session_store.get_or_create("text-bill")   voice_orch.py:2132   ← session_id is CONSTANT per member
 4. classify_control(query)                    voice_orch.py:2133 (control_classifier.py:97) → "NONE"
 5. _get_text_query_router()                   voice_orch.py:2190 (lazy singleton Router, :2082)
 6. TurnOrchestrator(_NoopStore(), …, user_id="bill")   voice_orch.py:2191-2194 (orchestrator.py:171)
 7. orch.decide(query)                         voice_orch.py:2196 → orchestrator.py:397
    ├─ retrieve(query)                         orchestrator.py:402 → :213
    │   ├─ keyword_domains(query)              orchestrator.py:220 → :131  ("medication" → health, :105)
    │   │   └─ (ambiguous fallback) _NoopStore.infer_domains → []   orchestrator.py:223 / voice_orch.py:616
    │   ├─ search_facts_by_embedding(query, "bill", top_k) orchestrator.py:236 → extraction_queue.py:680
    │   │   ├─ embed_text(query)               extraction_queue.py:701 → :328 (local Ollama embed)
    │   │   └─ Neo4j: valid_to IS NULL AND owner∈(bill,household) AND embedding NOT NULL; cosine in Python
    │   └─ (fallback if []) read_user_facts("bill")     orchestrator.py:237 → extraction_queue.py:624
    ├─ max_sensitivity(facts)                  orchestrator.py:404 → :145
    └─ router.dispatch(query, sensitivity_tag) orchestrator.py:405 → router.py:816
        └─ on TIER_ESCALATE this ALREADY fires the SerpAPI backend as a side effect
 8. log_routing_decision(...)                  voice_orch.py:2206 (routing_telemetry.py:23)
 9. resolve_subject(query, "bill", facts)      voice_orch.py:2220 (subject_resolution.py:171) → ["elena", …]
10. apply_injection_contract(facts, …)         voice_orch.py:2221-2225 (injection_contract.py:229)
    └─ is_declarative_utterance(query)         voice_orch.py:2224 (injection_contract.py:90) → True (INJ-2 bypass)
11. guard NOT triggered → _candidate_facts = d["facts"] (pre-contract, FULL set)  voice_orch.py:2260
    facts = _inj.allowed                       voice_orch.py:2261
12. orch.local_system_prompt(facts, owner="bill", requester, query, intent)  voice_orch.py:2263 → orchestrator.py:242
    ├─ filter_facts(facts, requester)          orchestrator.py:306 (permissions.py)
    ├─ enrich_time_context / enrich_facts      orchestrator.py:301,307 (temporal.py)
    ├─ SECOND retrieval — "Things you know":   orchestrator.py:326-331
    │   search_facts_by_embedding(query, owner) or read_user_facts(owner)   ← retrieval runs TWICE per turn
    └─ intent=="personal" → PERSONAL_FACT_GROUNDING_GUARD appended  orchestrator.py:343-344 (:72)
13. Generation:                                 voice_orch.py:2320-2357
    ├─ complexity mid/core + GROQ_API_KEY → Groq chat (:2328), else
    └─ local Ollama qwen2.5:7b via AsyncOpenAI  voice_orch.py:2346  → reply
14. _write_routing_log(...)                    voice_orch.py:2335 or :2357 (→ logs/router.jsonl)
15. _write_trace_log(...)                      voice_orch.py:2362 (→ logs/trace/…)
16. write_transcript_turn(user), (hip)         voice_orch.py:2370-2376 (transcript_log.py:79)
    ── response is now final; returned via JSONResponse at voice_https_orch.py:157 ──
17. detect_and_apply_async(utterance=query, facts=_candidate_facts, owner="bill", …)
                                               voice_orch.py:2382 → fact_change.py:445
    └─ daemon thread → detect_and_apply()      fact_change.py:459-461 → :406
        ├─ gates: <4 words / ends "?" / question opener → no-op   fact_change.py:413-419 (statement passes)
        ├─ _call_groq(Llama-4-Scout, temp 0)   fact_change.py:431 → :235   ← S-INT: bare Groq, 3-action vocab
        └─ _apply_changes(changes, "bill", "text-bill")   fact_change.py:439 → :267
            for each change:                                       ← N changes → N writes (no dedupe)
            ├─ attribute ∈ CANONICAL_ATTRIBUTES check     fact_change.py:276
            ├─ log_fact_lifecycle_event("change_detect")  fact_change.py:284
            ├─ passes_sensitivity_filter(attr, value)     fact_change.py:303 (extraction_queue.py:105)
            ├─ subject: Groq subject | _resolve_subject_by_old_value | owner   fact_change.py:315-330 (:194)
            ├─ _snapshot_prior_fact(driver, owner, subj, attr)   fact_change.py:335 → :127
            ├─ WriteDecision(state="supersede", target=None, confidence=0.75)  ← HARDCODED, fact_change.py:344-349
            ├─ encode(driver, wd, …)            fact_change.py:352-363 → store.py:297
            │   ├─ code overrides §5.1          store.py:325-347 (MULTI_VALUED→augment live; θ_WRITE/correct DEAD at 0.75)
            │   ├─ encrypt_fact_value ×2        store.py:350-353
            │   ├─ _tx_supersede (target=None → key-based)   store.py:392-403 → :226
            │   │   ├─ close ALL active rows (attr, owner, subject): valid_to, closed_reason='superseded', superseded_by   store.py:245-257
            │   │   └─ CREATE new :Fact (write_state, confidence_log, tier='hot', embedding=None)  store.py:259 (:201)
            │   └─ _append_audit(...)           store.py:421-435 → :83 (logs/memory_engine/encode_audit.jsonl)
            ├─ _store_delta(...)                fact_change.py:378 (prior value decrypted at :374 → :183 — used ONLY for the delta record, never to gate the write)
            └─ log_fact_lifecycle_event("enrichment"|"assertion")   fact_change.py:392
18. update_turn_state(...)                      voice_orch.py:2387 (control_flow) → return reply
```

**Graph-write summary (statement):** exactly ONE `detect_and_apply_async` call per turn
execution; each Groq-proposed change becomes one `encode()` supersede; `retract` bypasses
encode via `retract_fact()` (`fact_change.py:290` → `extraction_queue.py:544`). A second,
ungoverned writer fires at session end / speaker change: `enqueue_session_end`
(`voice_orch.py:2436`, `:1229`) → `process_session` → `write_facts` → `_write_one`
(`extraction_queue.py:460`) — raw nodes, no write_state/audit (DIV-4).

## Trace B — Question turn (text path)

Utterance: `bill: "What did I tell you about my mother's medication?"`

```
 1-9.  identical to Trace A steps 1-9 (decide → retrieve ×1 → route; intent="personal")
10. apply_injection_contract(...)              voice_orch.py:2221 — INJ-1..6 evaluate for subject "elena"
11a. GUARD PATH (empty approved set + personal):   voice_orch.py:2226-2255
     ├─ empty_set_refusal(query, resolved)     voice_orch.py:2228 (injection_contract.py:317) — reply built, NO model call
     ├─ build_turn_metadata / log_turn_metadata voice_orch.py:2231-2239
     ├─ write_transcript_turn ×2               voice_orch.py:2240-2246
     ├─ detect_and_apply_async(...)            voice_orch.py:2248  ← STILL FIRES on question turns…
     │   └─ …but no-ops at the cheap gates: ends "?" (fact_change.py:417) / opener "what" (:418). ZERO Groq calls, ZERO writes.
     └─ update_turn_state → return refusal     voice_orch.py:2253-2255
11b. ALLOWED PATH (facts admitted): steps 12-16 of Trace A —
     local_system_prompt + PERSONAL_FACT_GROUNDING_GUARD (orchestrator.py:343) → Groq/Ollama → logs → transcript
     └─ detect_and_apply_async at voice_orch.py:2382 — same question gates → no write.
```

**Graph-write summary (question):** none. The question gates live INSIDE
`detect_and_apply` (`fact_change.py:413-419`), not at the call sites — every routed text
turn fires the thread; questions die at the gate before the Groq call.

## Voice-path deltas (same seams, different wiring)

| # | Voice behavior | Where |
|---|---|---|
| V1 | TD-046 settle: TranscriptionFrames buffered; one merged utterance flushed after `VAD["user_speech_timeout"]` | `voice_orch.py:1117-1129`, `:1132-1178` |
| V2 | Per-turn speaker re-verification against all members; speaker change flushes context + enqueues departing member's extraction | `:1317-1355`, `:1203-1254` |
| V3 | `_decide()` wraps `orch.decide()`; guests get sensitivity="high", no retrieval | `:1959-1978` |
| V4 | `detect_and_apply_async` fires at `:1502` — only if `self._last_facts` non-empty AND member verified (DIV-8: first-ever facts never captured per-turn), with `owner_name=None` |
| V5 | **No injection contract on voice** — `local_system_prompt` + `filter_facts` only (DIV-2) | `:1730-1733` |
| V6 | Retrieval scope: `orch.user_id` is fixed `"bill"` at build (`:2021-2023`); `decide()` retrieves as bill regardless of verified speaker (DIV-7) |
| V7 | Local replies stream via pipecat `OLLamaLLMService` (`:2055`); reply text recovered from `self._ctx._messages` for transcript/satisfaction (`:1038-1042`, `:1264-1270`) |
| V8 | Session-end extraction (ungoverned Path B writer) on disconnect (`:2431-2437`) |

---

## Seam Inventory — runs now vs governed design

| seam | runs now (live, cited) | should run (governed design, cited) | divergence | risk |
|---|---|---|---|---|
| **S-INT** interpretation | `fact_change.py` bare Groq: 3-action prompt (`:46-69`), `_call_groq` (`:235`), then **hardcoded** `WriteDecision("supersede", target=None, 0.75)` for BOTH update and add (`fact_change.py:344-349`). Fired once per routed turn: voice `voice_orch.py:1502`; text `:2248`/`:2305`/`:2382` (mutually exclusive) | `GroqInterpreter.classify_write()` — 4 write-states, real confidence, real target selection (`interpreter.py:196-246`); θ_WRITE + overrides then meaningful (`store.py:47,325-347`) | Governed classifier called from nowhere in `harness/`/`server/`. CORRECT & UNRESOLVED unreachable; θ_WRITE gate dead at 0.75; "add" of an existing value becomes a key-based supersede → **self-supersede loop** (§below); Groq's literal `subject:"null"` string accepted as a subject (`:315`; audit row 2026-07-06T13:44:20, owner=maya subject="null") | **HIGH** — correctness of the write ledger; the demo's visible churn |
| **S-WRITE** write | Per-turn path DOES use `memory_engine/store.encode()` with overrides + `_append_audit` (`fact_change.py:352` → `store.py:297,421`) — but fed the constant decision above. Second writer at session end bypasses encode entirely: `_write_one` (`extraction_queue.py:460-504`), no write_state/confidence_log/audit, closes with `closed_by` not `closed_reason`. Retract also bypasses (`extraction_queue.py:544`) | ALL mutations through `encode()` so every node carries write_state + confidence_log and every write is audited (spec §5.1; `store.py:1-22`) | Governed writer, ungoverned decision (Path A); ungoverned writer (Path B). Same fact lands ASSERTED per-turn but UNCONFIRMED via session end; `encode()` has **no value-equality no-op** — identical value re-writes churn the lineage | **MED-HIGH** |
| **S-CLS** classify | `trust()` (`truth_layer/queries.py:638`) runs **never** in a live turn — callers are demo dashboard (`demo_dashboard.py:452`), demo logging (`scripts/text_demo.py:80`), evals. Inline mirror `_classify_trust` (`fact_change.py:146`) labels delta records only (predicates unified by `4fadca2`) | Trust computed at disclosure; UNRESOLVED/derived/retired hedged via `render_fact_hint`/`render_system_note` (`api.py:248,269`) | Model sees a flat `attribute: value` list (`orchestrator.py:311,340-342`) — confirmed and unconfirmed facts indistinguishable (DIV-5) | **MED** |
| **S-RET** retrieval | `search_facts_by_embedding \|\| read_user_facts` — twice per turn: `orchestrator.py:236-237` (decide) and `:326-331` (prompt build). Filter is only `valid_to IS NULL AND owner∈(member,household)` (`extraction_queue.py:647,710`) — no tier, no temporality, no annotations | `memory_engine.api.candidate_facts()` (`api.py:155`) — tier-aware CQL (`:110,131`), temporality fail-closed via interpreter (`:169-180`), annotation keys; cold structurally excluded (MEM-107) | Built, tested, unwired ("pipeline diff is one import line", `api.py:16-18`). No historical retrieval; cold exclusion NOT structural on live path (a cold-tier fact with `valid_to` null WOULD be injected); engine-written nodes have `embedding=None` (`store.py:195`) so they're invisible to the semantic path and surface only via the `read_user_facts` fallback (DIV-1) | **HIGH** (disclosure scope) |
| **S-CONS** consolidation | `run_consolidation()` has **zero production callers** — evals only (`memory_e2e.py:412`, `memory_harness.py:871,951,1028`); dashboard only reads its report file (`memory_dashboard.py:48`); no launchd job (`launchd/` has voice, dashboard, exemplar-refinement only). Header self-declares offline (`consolidate.py:2-5`) | Nightly REM: RECONCILE → ABSTRACT → PROMOTE → DEMOTE → ESCALATE (`consolidate.py:1-24`) | Never runs → no reconcile harden entries → CORROBORATED unreachable in production (`queries.py:707-709`); UNRESOLVED never resolved; tiers frozen at 'hot'; must-confirm queue producer-less (DIV-6) | **MED** |

---

## Idempotency — the Jardiance→Jardiance supersede loop, root-caused

### Observed (logs, 2026-07-06)

`logs/memory_engine/encode_audit.jsonl` — four supersede writes for
`(owner=bill, subject=elena, attribute=medication)`, each closing the node the previous
one created:

```
14:47:43Z  requested=supersede actual=supersede  prior_closed=-         session=text-bill
14:48:34Z  requested=supersede actual=supersede  prior_closed=7f7972bf  session=text-bill
15:56:05Z  requested=supersede actual=supersede  prior_closed=3f951a93  session=text-bill
16:22:00Z  requested=supersede actual=supersede  prior_closed=a5ba0e57  session=text-bill
```

`logs/fact_lifecycle/fact_lifecycle_text-bill__v20260706_*.jsonl` shows each was Groq
`proposed action=add`. `logs/transcript/transcript_text-bill__*.jsonl` shows the cause:
the **identical scripted statement** (care_coordination.json T01, "My mother Elena was
switched from metformin to Jardiance…") was fired at 14:47:41, 14:48:33, 15:56:04 and
16:21:57 — four demo (re)runs. After the first write, every replay is a
Jardiance→Jardiance self-supersede: close the identical fact, create an identical fact.
Same pattern for maya/ray at 13:44-14:17 (three_zone_demo T01/T04 reruns), including one
stray node written with **subject = literal string "null"** at 13:44:20.

### The trigger, pinned

**`detect_and_apply_async` is NOT called more than once per turn execution.** The call
sites are single and mutually exclusive per path — voice `voice_orch.py:1502` (one call
inside `_on_user_text`, which runs once per merged TD-046 utterance); text
`voice_orch.py:2248` (guard return) / `:2305` (temporal-placeholder return) / `:2382`
(normal end) — each path returns immediately after its call. The logs confirm one
`change_detect` per statement turn.

The N writes come from **re-processing the same logical turn**, and nothing at any layer
makes re-processing a no-op:

1. **Replay is routine.** Demo scripts re-run (`demo_run.run_script`/`fire_next_turn`
   via `scripts/demo_run.py:143,233`, client script strip `hip_client.html:1044`,
   `run_demo_script.py:221`, `text_demo.py:145`) and `session_id` is the constant
   `f"text-{member}"` (`voice_orch.py:2114`), so every replay re-enters the same
   session and re-fires detection with the same utterance.
2. **Detector re-proposes.** The Groq prompt (`fact_change.py:46-69`) has no
   "no change if the value is already current" rule — and "If the statement adds detail
   to an existing fact, that is an update" actively invites a re-write on restatement.
   Here it returns `add` each time (old value metformin is no longer in the facts list).
3. **Mapping erases the distinction.** `_apply_changes` maps BOTH `add` and `update` to
   the hardcoded `WriteDecision(state="supersede", target_fact_id=None, confidence=0.75)`
   (`fact_change.py:344-349`) — an "add" of an already-present value becomes a key-based
   supersede.
4. **Writer never compares values.** `encode()` → `_tx_supersede` with `target=None`
   unconditionally closes ALL active rows for `(attribute, owner, subject)` and creates
   the new node (`store.py:245-259`). The prior value IS decrypted right there in the
   caller (`fact_change.py:374` → `_decrypt_prior_value:183`) — but only to build the
   Phase-3 delta record, never to gate the write.

**Secondary multipliers (structural, cited, not the observed cause):**
- One detection returning multiple entries in `changes[]` loops through
  `_apply_changes` (`fact_change.py:269`) with no dedupe — two changes for the same
  `(attribute, subject)` in one turn would produce two supersedes, the second closing
  the first's node.
- Voice only: a mid-utterance pause longer than `VAD["user_speech_timeout"]` splits one
  spoken statement into two routed turns (`voice_orch.py:1126-1128` — a fragment arriving
  after the settle window means the earlier flush already ran a full turn), each firing
  detection once.

**Fix shape (NOT applied in this read-only pass):** value-equality no-op in
`_apply_changes` — after `_snapshot_prior_fact`, decrypt the prior value and skip the
`encode()` when the normalized new value equals the current active value for
`(owner, subject, attribute)`; plus dedupe of identical changes within one detection
cycle. One turn writes once; re-processing becomes a no-op. This is deterministic code
below the model seam and does not touch S-INT/S-RET wiring or the frozen pipeline.
