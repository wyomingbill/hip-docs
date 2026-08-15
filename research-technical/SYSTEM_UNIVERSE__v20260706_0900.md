<!-- STATUS: BUILT — extracted from live code 2026-07-06 -->
<!-- RECONCILED-AGAINST: main branch, read-only 2026-07-06 -->

# HIP System Universe — Authoritative Pipeline Map

Seven subsystems, each section: **Implemented** / **Spec intent** / **Divergences**.
All file:line citations are to `[REDACTED-USER-PATH]/hip-dev/` source tree.
Severity tags: `[CORRECTNESS]` `[GOVERNANCE]` `[COMPLETENESS]` `[LATENT]`

---

## 1. INGESTION

### Implemented

Two input paths; both converge at `process_text_query()` in `server/voice_orch.py`.

**Voice path (Pipecat WebRTC, port 7860):**

Entry: `server/voice_https_orch.py` — HTTPS/TLS server. Imports and re-exports `bot` and `process_text_query` from `server/voice_orch.py` (`voice_https_orch.py:27`). Pipecat VAD/STT pipeline defined in `voice_orch.py`'s `bot()` coroutine.

- **VAD**: `SpeechTimeoutUserTurnStopStrategy` via Pipecat; raw WebRTC audio frames.
- **STT**: `WhisperSTTService` (Pipecat wrapper) around `faster-whisper` (`speech.py:62-84`). Model config: `config.yaml`→`voice.stt.*`. `language="en"`, `beam_size=1`, with optional `initial_prompt` (`speech.py:81`). Emits `TranscriptionFrame`.
- **Speaker ID**: `SpeakerVerifier` (`speaker_id.py:285-353`) runs on each turn's audio. Uses **Resemblyzer GE2E** (`_resemblyzer_encoder()` at `speaker_id.py:84-92`), NOT the config comment "speechbrain/spkrec-ecapa-voxceleb". Cosine similarity against enrolled L2-normalized voiceprint. Thresholds: high ≥ 0.75, medium ≥ 0.50 (`speaker_id.py:326-329`). High-confidence turns adapt the stored print via decayed running average (`speaker_id.py:372-380`). Voiceprints stored encrypted (Fernet under `~/hip-harness/data/voiceprints/{user}.npz`).
- **Convergence**: Identified speaker → `process_text_query(transcribed_text, member_id)` in `voice_orch.py`. Unrecognized voice → guest refusal (no personal facts, no routing) (`voice_https_orch.py:325-339`).

**Text path (REST, port 7860):**

`POST /api/text-query` → `hip_api_text_query()` in `voice_https_orch.py:94-157` → `await process_text_query(query, member)` in `voice_orch.py`.
`POST /api/voice-query` → `get_member_by_voice(audio_bytes, min_tier="medium")` → same `process_text_query()` (`voice_https_orch.py:261-339`).

**Canonical entry function**: `process_text_query(query: str, member_id: str)` in `server/voice_orch.py`. Both paths call this.

**Fact extraction (write side)**: `harness/fact_change.py:detect_and_apply_async` is called each turn (`voice_orch.py:123-124`). Session-end extraction via `harness/extraction_queue.enqueue_session_end` (`voice_orch.py:122`). Facts reach Neo4j through the extraction queue, NOT the Pipecat audio path.

**Utterance encryption**: The driving utterance is envelope-encrypted at write time via `encrypt_fact_value()` (`store.py:352-355`) and stored as `driving_utterance_ct`/`driving_utterance_dek` on the `:Fact` node.

### Spec intent

Spec (MEMORY_ENGINE §0, §2): voice and text paths both feed the same pipeline. Speaker identity gates member_id resolution; unrecognized voice gets session-only access with no persistent facts. Utterances stored encrypted so provenance can be audited without exposing plaintext (TRUTH_LAYER §3.1).

### Divergences

- **[LATENT]** `speaker_id.py:65` `_DEFAULTS` names model `"speechbrain/spkrec-ecapa-voxceleb"`, but `speaker_id.py:84-92` loads `resemblyzer.VoiceEncoder` (GE2E). Config value is dead — any YAML override targeting ECAPA would be silently ignored.
- **[COMPLETENESS]** `harness/orchestrator.py` `TurnOrchestrator` is the compositional unit referenced in spec but is NOT wired into the 7860 Pipecat pipeline as the primary turn handler. `voice_orch.py:107` imports it, but Pipecat's `OllamaLLMService`/`GroqLLMService` do streaming generation independently; the orchestrator's `handle_turn()` is the standalone/test path.

---

## 2. ROUTING

### Implemented

Entry: `Router.dispatch(query, sensitivity_tag)` → `router.py:816-825`. Calls pure `route(query)` then, if TIER_ESCALATE, invokes the escalation backend stub.

**`route()` pipeline** (`router.py:680-795`) — five stages, pure, no I/O:

**Stage 0 — Noise filter** (`router.py:705-706`): `_is_noise(q)` from `intent_classifier.py:154-165`. Short filler-only utterances or repeat tokens → `TIER_DROP`.

**Stage 1 — Intent classification** (`router.py:710`): `intent_classifier.classify(q)` — embedding cosine similarity against 5 routes × N exemplars (`intent_classifier.py:175-212`). Routes: `personal / temporal / knowledge / action / noise`. Threshold: `CONFIDENCE_THRESHOLD = 0.30` (`intent_classifier.py:144`); below threshold → defaults to `"knowledge"`. Uses `embed_text()` from `harness/extraction_queue.py` (Ollama `nomic-embed-text`).

- `temporal` → TIER_ESCALATE (this is the freshness axis; no separate `_classify_freshness` call exists — `router.py:724-746`).
- `action` → TIER_LOCAL (`router.py:747-751`).
- `personal` → **falls through to Stage 2** (`router.py:723-724` comment). Previously returned TIER_EDGE early; removed. All on-net tiers are within the operator's enclave so tier is a capability decision, not a privacy boundary (`router.py:713-716`). `intent` field is preserved in `RouteDecision` for injection gating downstream.
- `knowledge` (or below-threshold) → falls through to Stage 2.

**Stage 2 — Complexity / Bloom** (`router.py:757-758`): `classify_complexity(q)` → `router.py:522-564`. Two-stage:
1. Feature classifier (`complexity_features.py`: `extract_features()` → `classify_by_features()`). Bloom's taxonomy level 1-6; hard mapping: 1-2 → edge, 3-4 → mid, 5-6 → core. Returns `(tier, bloom)`.
2. Fallback: exemplar embedding router (`_ExemplarRouter`, top-5 nearest-neighbor vote on `data/tier_exemplars.txt`) if feature classifier raises.
3. Rules fallback (`_classify_complexity_rules`): token count + `_COMPLEX_VERB_RE` / `_ATTACHED_CONTENT_RE` / `_MULTI_PART_RE` heuristics (`router.py:266-286`).

**Stage 3 — Master escalation toggle** (`router.py:761-765`): `cfg.escalation_enabled` from config; if off → on-net complexity tier, no off-net.

**Stage 4 — Capability axis** (`router.py:767-783`, config-gated): `_classify_capability(q)` checks code/math/tool-use cues. If fires and sensitivity does NOT block → TIER_ESCALATE; if sensitivity blocks → on-net complexity tier.

**Sensitivity gate** (`_classify_sensitivity`, `router.py:197-207`): two-tier: (1) fact-level tag `>= force_local_at` threshold (default "high"); (2) query-level `_PII_RE` (any framing) or `_SENSITIVE_TOPIC_RE` with `_PERSONAL_RE` first-person marker. Blocks off-net escalation; does NOT lower on-net tier.

**Escalation backend** (`LoggingEscalationStub`, `router.py:616-661`): logs query hash + routing fields to `logs/router.jsonl`. Returns `handled=False`. **Does NOT call any external API.**

**Personal-intent early-return (router.py:722-726)**: The lines at 722-726 are a comment block (`# Personal intent: fall through to Stage 2`) followed by the temporal block. There is NO personal-intent early return in the current code — it was removed. The removal is architecturally correct given the enclave model: all edge/mid/core tiers run on-device inside the operator enclave; routing personal queries exclusively to edge was overly conservative and limited model capability for complex personal questions.

### Spec intent

Spec (interfaces.py, router.py header): the router is the "moat" above the commodity seams. Freshness (temporal), capability, sensitivity, complexity are the four axes. Sensitivity gates off-net only; on-net tier is purely complexity-driven. Frontier model (`claude`, `config.yaml`) answers escalated turns.

### Divergences

- **[COMPLETENESS]** Escalation backend is `LoggingEscalationStub` only — logs and returns `handled=False` (`router.py:616-661`). Frontier model is never called. `TIER_ESCALATE` turns get a placeholder reply: `"I don't have that information yet."` (`orchestrator.py:374`). This is Phase 1 behavior explicitly; Phase 2 frontier wiring is NOT BUILT.
- **[CORRECTNESS]** Freshness axis has no dedicated classifier. The freshness axis described in the router header comment is implemented entirely via `intent == "temporal"` in Stage 1 (`router.py:725-746`). There is no `_classify_freshness()` call. Queries that need real-time data but don't read as "temporal" via the intent embeddings will not escalate.
- **[COMPLETENESS]** Capability axis is config-gated and off by default (`cfg.capability_enabled`). It is present in code but not active in the standard pipeline configuration.

---

## 3. RETRIEVAL + DISCLOSURE

### Implemented

**Retrieval — live pipeline:**

`harness/orchestrator.py:TurnOrchestrator.retrieve()` (`orchestrator.py:213-239`):
1. Domain classification: keyword classifier (`keyword_domains()`, `orchestrator.py:131-142`) → Ollama `infer_domains` fallback if empty.
2. Fact fetch: `search_facts_by_embedding(query, user_id, top_k=max_facts)` OR `read_user_facts(user_id, limit=max_facts)` from `harness/extraction_queue.py` (`orchestrator.py:236-237`). Both use `WHERE f.valid_to IS NULL` (active facts only). **No tier filter.** Cold facts are NOT excluded by this query.

**Subject resolution** (`harness/subject_resolution.py:resolve_subject()`, `subject_resolution.py:171-224`):
- Phase 1: first-person markers → `[member_id]` (`subject_resolution.py:198-199`).
- Phase 2: relational terms ("my mother") → walk `attribute="relationship"` facts for named match (`subject_resolution.py:200-213`). Unresolvable relational → `[]` (safe empty set).
- Phase 3: named entities → match against known subjects in facts (`subject_resolution.py:214-221`).
- Empty set = safe failure mode invariant (`subject_resolution.py:14`).

**Injection contract** (`harness/injection_contract.py:apply_injection_contract()`, `injection_contract.py:167-236`):

Six rules applied in order; a fact passes ALL or is denied:

| Rule | Logic | Code |
|---|---|---|
| INJ-4 | `owner == 'household'` → short-circuit ALLOW | `injection_contract.py:191-196` |
| INJ-5 | `intent IN {knowledge,temporal,noise}` → DENY personal facts | `injection_contract.py:199-202` |
| INJ-3 | `owner == requester OR subject == requester` → ALLOW; else DENY | `injection_contract.py:205-208` |
| INJ-1 | `subject IN resolved_subjects` → ALLOW | `injection_contract.py:211-214` |
| INJ-2 | `attribute`-keyword match OR general personal query → ALLOW | `injection_contract.py:217-220` |
| INJ-6 | `resolved_subjects non-empty AND allowed=[] AND intent=personal` → `guard_triggered=True` | `injection_contract.py:229-234` |

INJ-4 fires first (before INJ-3) — household facts bypass cross-member deny entirely.
INJ-6 guard fires structural refusal: `empty_set_refusal()` returns `"I don't have that confirmed yet."` without calling the model (`injection_contract.py:241-251`, `orchestrator.py:437`).

**Owner/household visibility**: `read_user_facts(owner)` retrieves `WHERE f.owner = $owner OR f.owner = 'household'`. INJ-3 then separately enforces that a non-owner requester cannot see facts owned by someone else. Cross-member: Sarah cannot read Bill's facts even if Elena (a known subject) is resolved.

**Empty-set guard**: `injection_contract.py:229-234`. Triggers only when `intent in _PERSONAL_INTENTS` (personal, action) AND resolved subjects exist AND no facts survive. Knowledge/temporal intents never trigger the guard (they would get an empty context silently).

### Spec intent

Spec (HARDENING §P1-3, §P1-4): subject resolution is deterministic (no LLM). INJ-1..6 are a structural deny-default boundary. The contract is frozen; the memory engine shapes candidates behind it without touching the rules. INJ-6 is a structural refusal, not a prompt instruction.

MEMORY_ENGINE §1: the live pipeline should call `memory_engine/api.py:candidate_facts()` as the drop-in replacement for `read_user_facts()`, adding tier-aware retrieval, temporality classification, and annotation keys (unresolved hedging, derived flagging, warm/historical facts).

### Divergences

- **[GOVERNANCE]** `memory_engine/api.py:candidate_facts()` is NOT called from `harness/orchestrator.py`. The live pipeline calls `harness/extraction_queue.read_user_facts()` directly (`orchestrator.py:43, 237`). The spec swap-in is NOT DONE. Consequences: (a) warm-tier facts never surface on historical queries; (b) UNRESOLVED facts are not hedged in the response ("may have…"); (c) derived facts are not annotated; (d) temporality classification (Groq call at retrieval time) never runs.
- **[GOVERNANCE]** `read_user_facts()` uses `WHERE f.valid_to IS NULL` with no tier filter. Cold facts with `valid_to IS NULL` (e.g., recently demotion-pending) can appear in the injection set. The spec says cold facts are structurally excluded.
- **[COMPLETENESS]** INJ-2 relevance map (`_ATTR_KEYWORDS`, `injection_contract.py:35-64`) covers only 9 named attribute types. Any attribute written to the store with an unrecognized name fails INJ-2 silently (`injection_contract.py:120-123`), never reaching the model regardless of subject/ownership.

---

## 4. INTERPRETATION

### Implemented

**Write-state classification** — live pipeline path via `harness/fact_change.py:detect_and_apply_async()`. This module calls Groq API using prompts to detect whether an utterance implies a fact change, then calls `extraction_queue` to write. It has its own system prompt and its own CORROBORATED predicate (see §5 / FACT_LIFECYCLE doc).

**Memory engine interpreter** (`memory_engine/interpreter.py:GroqInterpreter`) — used by `memory_engine/store.py:encode()` only (NOT the live pipeline). Separate class, same Groq API endpoint (`GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"`, `interpreter.py:31`), model `meta-llama/llama-4-scout-17b-16e-instruct` (`interpreter.py:33`).

**WriteDecision dataclass** (`interpreter.py:64-72`):
- `state`: `"supersede" | "augment" | "correct" | "unresolved"`
- `target_fact_id`: prior fact to supersede/correct, or None
- `confidence`: 0.0–1.0 (classifier certainty in the write decision, NOT fact truth)
- `rationale`: ≤ 25 words

**Signal mapping** (`_CLASSIFY_SYSTEM_PROMPT`, `interpreter.py:34-59`):
- `supersede`: "switched to", "not anymore, now", "instead of", value replacement signal
- `augment`: "also", "added", listing a new item, multi-valued attributes
- `correct`: "actually", "I misspoke", "that's wrong, it's", "never was" — belief was wrong from the start
- `unresolved`: ambiguous; or model call fails → `unresolved, confidence=0.0`

**Code overrides applied in `store.py:encode()`** before the transaction (`store.py:325-347`):
1. `MULTI_VALUED` attribute + state=SUPERSEDE → AUGMENT (`store.py:329-332`)
2. state=CORRECT + `target_fact_id is None` → UNRESOLVED (`store.py:334-337`)
3. `write_confidence < θ_WRITE (0.6)` → UNRESOLVED regardless of requested state (`store.py:339-347`)

`classify_query_temporality()` (`interpreter.py:248-305`): classifies whether a query asks about current vs. historical state. Fail-closed to `historical=False` (current) on any error — user sees fewer facts, never stale ones framed as current.

### Spec intent

Spec (MEMORY_ENGINE §2): ALL model judgment is behind the `Interpreter` protocol. Write-state classification is probabilistic (model), execution is deterministic (code). The model classifies; code applies, audits, and can override. `θ_WRITE=0.6` is the confidence floor below which code forces UNRESOLVED regardless of model intent.

### Divergences

- **[LATENT]** The live pipeline uses `harness/fact_change.py` for fact detection, NOT `memory_engine/interpreter.py:GroqInterpreter`. These are two separate Groq callers with separate system prompts. The `memory_engine` interpreter is exercised only by `memory_engine/store.py:encode()`, which is not called from `harness/orchestrator.py`. The live fact-change path is entirely outside the memory engine's write discipline (no `encode()` → no audit trail, no override guarantees, no `θ_WRITE` check).
- **[COMPLETENESS]** `Interpreter.abstract()` (derives higher-order facts from episode clusters, `interpreter.py:368-416`) and `Interpreter.reconcile()` (`interpreter.py:307-366`) are built and tested but never called from the live pipeline. They are offline-only via `consolidate.py`.

---

## 5. FACT LIFECYCLE

The trust-level state machine is fully extracted in dedicated documents. This section references them and summarizes the live behavior.

**Authoritative sources:**
- State diagram source: `docs/research/FACT_LIFECYCLE__state-diagram-source__v20260706_0735.md`
- Mermaid diagram: `docs/research/FACT_LIFECYCLE_DIAGRAM__v20260706_0800.mermaid`

**Summary of implemented behavior:**

Five trust levels computed by `trust()` (`truth_layer/queries.py:638-734`), first-match-wins: DERIVED → CONFIRMED → CORROBORATED → ASSERTED → UNCONFIRMED. Four write-states drive initial placement: SUPERSEDE/AUGMENT/CORRECT (with overrides) → ASSERTED; UNRESOLVED → UNCONFIRMED. DERIVED is permanent — `derived=true` is checked before CONFIRMED, making confirmed derived facts unreachable at CONFIRMED by the predicate ordering (`queries.py:698`).

**What is live vs. offline:**
- Write-state assignment (SUPERSEDE/AUGMENT/CORRECT/UNRESOLVED): live, via `harness/fact_change.py`.
- ASSERTED→CORROBORATED (harden via reconcile): OFFLINE ONLY — `consolidate.py` not called from `orchestrator.py`.
- CORROBORATED→CONFIRMED (human sets confirmed_by): NOT WIRED — no live code path sets `confirmed_by`.
- Fluid confirmation (`confirm_when_relevant=true` → clarifying question): NOT BUILT — flag written (`store.py:364`), never read in `harness/orchestrator.py`.
- `must_confirm_queue` consumption: NOT BUILT — queue appended by `_escalate_pass`, never consumed.

**Two divergent CORROBORATED predicates** (noted in FACT_LIFECYCLE doc):
- `queries.py:607-621`: numeric rise `_CONF_ORDER[to] > _CONF_ORDER[from]`
- `harness/fact_change.py:142-167`: any reconcile entry where `to IN ("medium","high")` — can disagree on the same fact.

---

## 6. CONSOLIDATION

### Implemented

`memory_engine/consolidate.py:run_consolidation(owner, *, driver, interpreter, dry_run=True)` (`consolidate.py:731-773`).

Five sub-passes in order:

**RECONCILE** (`_reconcile_pass`, `consolidate.py:220-348`): finds `(subject, attribute)` pairs with UNRESOLVED facts in hot/warm tier → fetches full lineage → calls `Interpreter.reconcile()` (model judgment) → applies one of: harden (confidence one step up, adds `confidence_log` entry with source="reconcile"), loosen (one step down), resolve (retro-applies supersede/correct/augment to the UNRESOLVED row via `_apply_resolve()`), leave, escalate. One step at a time only.

**ABSTRACT** (`_abstract_pass`, `consolidate.py:423-485`): fetches non-derived facts grouped by subject → for subjects with ≥2 facts → calls `Interpreter.abstract()` → writes `DerivedFact` nodes (confidence clamped to "low", `derived=True`, `migration_status="engine_phase_c"`, `write_state="augment"`). Encrypted via `encrypt_fact_value()` (`consolidate.py:490`).

**PROMOTE** (`_promote_pass`, `consolidate.py:520-563`, Phase D): cold facts with `access_count >= COLD_PROMOTE_MIN_ACCESS (1)` → promoted to warm tier. Runs BEFORE DEMOTE so a recalled fact cannot be immediately re-demoted.

**DEMOTE** (`_demote_pass`, `consolidate.py:568-664`): hot→warm: `valid_to` set AND age since `valid_to >= HOT_TO_WARM_DAYS (30)`; warm→cold: `access_count == 0` AND age `>= HOT_TO_WARM_DAYS + WARM_TO_COLD_DAYS (120 total days)`.

**ESCALATE** (`_escalate_pass`, `consolidate.py:669-726`): UNRESOLVED facts in hot/warm with `salience >= θ_INTENTIONAL (0.75)` → appended to `logs/memory_engine/must_confirm_queue.jsonl`. Salience formula: `0.4·stakes + 0.4·query_likelihood + 0.2·age_factor` where stakes=1.0 for high-stakes attributes (`consolidate.py:62-92`).

**Reversal**: `reverse_consolidation_pass(report_id, *, driver)` (`consolidate.py:778-896`). LIFO, no DELETE — uses inverse tier moves and confidence steps. Derived facts moved to cold (unreachable), not deleted.

**Wiring check** (`memory_engine/api.py`): the api.py module does NOT export `consolidate_owner()`. Consolidation is invoked only via the CLI: `python memory_engine/consolidate.py <owner> --execute`. No call from `harness/orchestrator.py` or any server module. `dry_run=True` is the default to prevent accidental writes.

### Spec intent

Spec (MEMORY_ENGINE §5): consolidation is the "REM pass" — offline nightly run. RECONCILE hardens ASSERTED → CORROBORATED. ABSTRACT creates derived facts. DEMOTE and PROMOTE manage tier movement. ESCALATE feeds the must-confirm queue which triggers HIP-initiated confirmation sessions.

### Divergences

- **[COMPLETENESS]** `run_consolidation()` is NOT called from the live pipeline. `memory_engine/api.py` does not expose a `consolidate_owner()` function; the spec-referenced call site does not exist. Consolidation is **offline-only**, CLI-invoked only.
- **[COMPLETENESS]** `must_confirm_queue` is appended by `_escalate_pass` (`consolidate.py:707-720`) but no live code reads or acts on it — no HIP-initiated confirmation sessions are triggered. Queue grows unboundedly.
- **[COMPLETENESS]** ABSTRACT-created derived facts (`derived=True`) are written to Neo4j but since `candidate_facts()` is not wired into the live pipeline, derived facts are not annotated or hedged in responses.

---

## 7. STORAGE

### Implemented

**Substrate**: Neo4j graph database. All facts are `:Fact` nodes. No Neo4j relationship edges for fact connections — lineage is tracked via scalar pointers (`superseded_by` field on the node). Port 7688 (dev); production port from env.

**Bitemporal model** (`store.py:140-198`, `truth_layer/queries.py:299-374`):

| Field | Axis | Meaning |
|---|---|---|
| `valid_from` | Valid time | When the fact became true in the world |
| `valid_to` | Valid time | When it stopped being true (NULL = still active) |
| `recorded_at` | Transaction time | When the system first recorded this belief |
| `record_closed_at` | Transaction time | When the system recognized the belief as wrong (CORRECT only) |

SUPERSEDE sets `valid_to` but NOT `record_closed_at` (world changed; belief was valid at the time). CORRECT sets both `valid_to` AND `record_closed_at` (belief was wrong from the start). This distinction enables `correction_history()` vs. `lineage()` to tell them apart (`truth_layer/queries.py:377-428`).

**Encryption at rest** (`harness/encryption.py`) — envelope scheme:

1. **Master key**: 32 random bytes at `~/hip-harness/data/encryption/.master_key` (mode 0600, gitignored). Overridable via `$HIP_MASTER_KEY` (`encryption.py:52-55`). Created O_EXCL so concurrent first-writers don't clobber each other (`encryption.py:69-76`).
2. **Owner key**: `HKDF-SHA256(master, info="hip-fact-envelope:v1:<owner>")` → Fernet key, derived on demand, never stored. `owner` is `member_id` or `"household"` (`encryption.py:79-92`).
3. **DEK**: fresh random Fernet key per fact. Encrypts the value. The DEK itself is wrapped with the owner key. Neo4j stores `ciphertext` (value) + `encrypted_dek` (wrapped DEK) + `key_version` (`encryption.py:105-114`).

Rotating the master key requires re-wrapping DEKs (not re-encrypting values). `KEY_VERSION = 1` stamps every node for future rotation detection (`encryption.py:39`).

**Lineage and walkability** (`truth_layer/queries.py:431-600`): `lineage()` is a BFS over `superseded_by` pointer (forward), facts pointing TO the target via `superseded_by` (backward), and `derived_from` lists (derived links). Cycle-safe (visited set). All closed facts (including CLOSED_SUPERSEDED and CLOSED_CORRECTED) are walkable. The live injection query (`WHERE f.valid_to IS NULL`) excludes them — they are historical only.

**What is persisted vs. not:**
- `embedding`: NULL — not populated in Phase A (`store.py:196`). `search_facts_by_embedding()` falls back to `read_user_facts()` when embeddings are absent.
- `driving_utterance_ct`/`driving_utterance_dek`: encrypted driving utterance stored on each node (`store.py:352-355`). Decrypted on demand by `truth_layer/queries.py:provenance()`.
- `confidence_log`: list of JSON strings, one entry per confidence change event, append-only (`store.py:360`, `consolidate.py:207-215`).
- No DELETE issued anywhere in reviewed code paths. Reversal of derived facts moves them to cold tier, not deletion (`consolidate.py:864-877`).

**Audit trail**: `logs/memory_engine/encode_audit.jsonl` — one NDJSON record per `encode()` call (`store.py:83-121`). Fields: `new_fact_id, owner, attribute, subject, session_id, requested_state, actual_state, override_reason, write_confidence, model_id, prompt_hash, prior_closed_fact_id`. Append-only, never overwritten.

### Spec intent

Spec (MEMORY_ENGINE §3): bitemporal store with full valid-time and transaction-time axes. Envelope encryption so the master key never touches fact values directly. Tier ladder (hot/warm/cold) gates retrieval by recency. No fact ever deleted — immutable append-only history. Embeddings populated for query-aware retrieval.

### Divergences

- **[COMPLETENESS]** `embedding` field is NULL on all Phase A nodes (`store.py:196`). `search_facts_by_embedding()` returns empty → `read_user_facts()` fallback (`orchestrator.py:236-237`). Query-aware semantic retrieval is NOT live.
- **[GOVERNANCE]** `voice_https_orch.py:/api/decrypt` endpoint (`voice_https_orch.py:427-473`) decrypts and returns plaintext fact values for any `?member=` parameter. No authentication check. Any caller on the local network can decrypt Bill's facts by querying `GET /api/decrypt?member=bill`. Noted as open in SECURITY_AUDIT (TD-030 status).
- **[CORRECTNESS]** Schema migration (`store.py:449-538`): pre-Phase-A nodes have `write_state = null` set by the migration (line 519). `trust()` in `queries.py:711` checks `write_state IN {"supersede","augment","correct"}` — null write_state always falls to UNCONFIRMED. Migrated nodes are permanently UNCONFIRMED regardless of their semantic trust level before migration.

---

## SYSTEM-WIDE DIVERGENCES

All divergences across all seven subsystems, ranked by severity.

| # | Subsystem | Description | Severity | File:line | Impact |
|---|---|---|---|---|---|
| 1 | RETRIEVAL | `memory_engine/api.py:candidate_facts()` not wired — live pipeline calls `read_user_facts()` directly; no tier filter, no UNRESOLVED hedging, no historical-query warm-tier access | GOVERNANCE | `orchestrator.py:43,237` | Historical facts can appear without "was" framing; UNRESOLVED facts stated confidently; warm-tier facts never surface |
| 2 | RETRIEVAL | `read_user_facts()` has no cold-tier exclusion — uses only `WHERE valid_to IS NULL`, cold facts with null `valid_to` reachable | GOVERNANCE | `extraction_queue.py` (read_user_facts) | Cold facts can appear in injection set contrary to spec |
| 3 | ROUTING | Escalation backend is stub only — frontier model (`claude`) never called; TIER_ESCALATE returns placeholder | COMPLETENESS | `router.py:616-661` | All temporal/freshness queries get "I don't have that information yet." regardless of model capability |
| 4 | INTERPRETATION | Live fact detection uses `harness/fact_change.py` (separate Groq caller), NOT `memory_engine/interpreter.py:GroqInterpreter` — no `encode()` call, no `θ_WRITE` gate, no audit trail, no code overrides | LATENT | `voice_orch.py:123`, `fact_change.py` | Write discipline (overrides, audit, confidence threshold) not applied to live fact writes |
| 5 | CONSOLIDATION | `run_consolidation()` not called from live pipeline — ASSERTED→CORROBORATED trust promotion, derived-fact abstraction, tier demotions never happen in live sessions | COMPLETENESS | `consolidate.py:731`, `api.py` (no `consolidate_owner`) | Trust levels frozen at ASSERTED; no derived facts; tiers never age |
| 6 | FACT LIFECYCLE | Two divergent CORROBORATED predicates: `queries.py:607-621` uses numeric rise; `fact_change.py:142-167` uses `to IN (medium,high)` | CORRECTNESS | `queries.py:607`, `fact_change.py:142` | Same fact can be CORROBORATED in one classifier and not the other — inconsistent trust classification depending on caller |
| 7 | FACT LIFECYCLE | DERIVED always wins over CONFIRMED in `trust()` predicate order — confirmed derived facts unreachable at CONFIRMED level | CORRECTNESS | `queries.py:698-703` | Spec §3.4 claim that DERIVED can reach CONFIRMED is false in code |
| 8 | FACT LIFECYCLE | `confirm_when_relevant=true` flag written on UNRESOLVED facts (`store.py:364`) but never read in `harness/orchestrator.py` | COMPLETENESS | `store.py:364` | Fluid confirmation (woven clarifying questions) never happens; UNRESOLVED facts persist silently |
| 9 | CONSOLIDATION | `must_confirm_queue` appended by `_escalate_pass` (`consolidate.py:707-720`) but no live code reads or acts on it | COMPLETENESS | `consolidate.py:712`, queue path | High-salience unresolved facts never trigger HIP-initiated confirmation |
| 10 | STORAGE | `embedding` field NULL in Phase A — semantic search falls back to `read_user_facts()` | COMPLETENESS | `store.py:196`, `orchestrator.py:236-237` | Query-aware fact retrieval (top-K relevant) not live; all facts for owner returned regardless of query relevance |
| 11 | STORAGE | `/api/decrypt` is unauthenticated — decrypts and returns plaintext facts for any member parameter | GOVERNANCE | `voice_https_orch.py:427-473` | Any LAN caller can exfiltrate all decrypted personal facts |
| 12 | STORAGE | Pre-Phase-A migrated nodes get `write_state = null` (migration, `store.py:519`); `trust()` maps null write_state to UNCONFIRMED | CORRECTNESS | `store.py:519`, `queries.py:711` | All pre-migration facts are permanently UNCONFIRMED regardless of their original trust level |
| 13 | RETRIEVAL | INJ-2 relevance map covers only 9 named attribute types; unknown attributes fail silently at `injection_contract.py:120-123` | COMPLETENESS | `injection_contract.py:35-64` | New attribute types added to the store without updating `_ATTR_KEYWORDS` are never injected into model context |
| 14 | INGESTION | `speaker_id.py:_DEFAULTS` names `"speechbrain/spkrec-ecapa-voxceleb"` but code loads `resemblyzer.VoiceEncoder` (GE2E) | LATENT | `speaker_id.py:65,84-92` | Config-based model override targeting ECAPA would silently have no effect |
| 15 | ROUTING | Freshness axis has no dedicated classifier — implemented entirely via `intent == "temporal"` embedding similarity | CORRECTNESS | `router.py:725` | Post-cutoff queries that don't read as "temporal" (e.g. "who runs OpenAI now?") stay on-net and get stale local-model answers |
| 16 | RETRIEVAL | `truth_layer/queries.py` (trust, lineage, provenance, correction_history, believed_state) built and tested but never called from `harness/orchestrator.py` | COMPLETENESS | `truth_layer/queries.py` | Truth audit layer is offline-only; no turn-time provenance or trust classification in live pipeline |
| 17 | STORAGE | `Provenance.rationale` is always None in Phase T-A (`queries.py:288`) — rationale_hash stored but not the text | COMPLETENESS | `queries.py:281-288` | Cannot audit WHY the model chose a write-state; only a hash of the rationale is available |
