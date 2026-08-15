<!-- STATUS: STALE -->
<!-- RECONCILED-AGAINST: point-in-time transfer 2026-06-27; harness/injection_contract.py (injection contract not yet built on this date — now BUILT); harness/member_registry.py (multi-member now live); harness/zep_store.py (Zep not active; Neo4j is the store); roadmap items (multi-member, speaker gate, encryption) are now partially or fully built — 2026-07-05 -->

# HIP Development Transfer — June 27, 2026

**Date:** 2026-06-27
**Branch:** main
**Author:** Bill Brewster / Claude Sonnet 4.6

---

## Architecture Summary

HIP (Household Intelligence Platform) is a privacy-preserving voice assistant prototype running on a single Mac. Audio capture, STT, TTS, and the primary LLM all run locally. Memory persists in Neo4j via a canonical fact schema. Escalation to Groq (fact-change detection) is the only off-device call, and it receives facts only after stripping personal identifiers when `groq_is_onnet: false`.

### Changes since June 24 transfer doc

- **Canonical attribute schema** replaces free-form subject+predicate+object triples. 10 fixed attributes; supersession now keys on `attribute+owner` instead of a string match.
- **Groq async fact-change detector** (`harness/fact_change.py`) fires on every utterance, replacing the hand-coded contradiction keyword detector.
- **Temporal enrichment** injects a computed time context block (today's date, day of week, days until each scheduled event) into the system prompt at retrieval time.
- **Two-stage intent routing** (`harness/router.py`) uses an embedding-based semantic router to classify intent before the local model sees the turn.
- **HIP-branded voice client** (`server/static/voice_client.html`) with split-pane layout, scrollable conversation panel, and RTVI bot text display.
- **Dashboard auto-start** added to `scripts/restart.sh` (port 7870).
- **launchd plist rewritten** — RunAtLoad=false, KeepAlive=false; managed via restart.sh.
- **household owner bug fixed** — `_apply_changes` now uses `owner='household'` for household-attribute facts so supersession queries match the stored node.

---

## Model Hierarchy

| Layer | Model | Where | Purpose |
|-------|-------|--------|---------|
| Edge / voice | qwen2.5:7b | Ollama (local) | Real-time spoken replies (<800ms) |
| Extraction | qwen2.5:32b | Ollama (local) | Session-end fact extraction from transcript |
| Fact-change | Llama 4 Scout 17B | Groq cloud | Async utterance-level fact update/retract/add |
| Embedding | nomic-embed-text | Ollama (local) | Fact vector storage and semantic retrieval |

`config.yaml` keys: `models.local`, `models.extraction`, `models.frontier`.

---

## Canonical Attributes

Defined in `harness/extraction_queue.py:CANONICAL_ATTRIBUTES`. The 10 attributes:

| Attribute | Description |
|-----------|-------------|
| `medication` | Prescription or OTC medications |
| `allergy` | Known allergens (food, drug, environmental) |
| `health_condition` | Diagnosed or reported health conditions |
| `dietary` | Dietary restrictions or preferences |
| `preference` | Personal likes, dislikes, or habits |
| `schedule` | Recurring events, appointments, routines |
| `employer` | Current or past employer / job role |
| `relationship` | Named people and their relationship to the owner |
| `household` | Household-level facts (address, trash day, shared routines) |
| `financial` | Financial facts (accounts, subscriptions, budget goals) |

**Multi-valued attributes** (facts accumulate, no supersession): `allergy`, `relationship`, `schedule`.

**Household scoping:** facts with `attribute='household'` are stored with `owner='household'` and are visible to all members via `read_user_facts` (which queries `owner=$member OR owner='household'`).

**Known gap (FACT-001):** `preference` is single-valued but users may have many simultaneous preferences (coffee AND tea). Candidate for MULTI_VALUED.

---

## Groq Async Fact-Change Detector

**File:** `harness/fact_change.py`

**How it works:**

1. `detect_and_apply_async()` is called from `voice_https_orch.py` on every user utterance (daemon thread — never blocks the voice response path).
2. It builds a prompt with the user's current :Fact nodes and the raw utterance.
3. Groq Llama 4 Scout returns `{"changes": [{"action": "update|retract|add", "attribute": "<canonical>", "new_value": "..."}]}`.
4. `_apply_changes()` processes each change:
   - **update**: calls `retract_fact(effective_owner, attribute)` then `write_facts(...)`.
   - **retract**: calls `retract_fact(effective_owner, attribute)`.
   - **add**: calls `write_facts(...)` directly (supersession in `_write_one` handles dedup).
5. `effective_owner = 'household'` when `attribute == 'household'`; otherwise the member's owner ID.

**Latency:** Groq Scout is ~150-300ms. The daemon thread means the voice turn completes before the fact write.

**System prompt guard:** Utterances < 4 words or ending with `?` or starting with a question word are skipped (no changes on questions or greetings).

**API key:** `GROQ_API_KEY` env var (required; set in launchd plist and .zshrc).

---

## Temporal Enrichment

**File:** `server/voice_https_orch.py` (inline in `local_system_prompt()`), computed from `harness/extraction_queue.py` schedule facts.

**How it works:**

At retrieval time, the system prompt includes a precomputed block:

```
Today is Friday, June 27, 2026.
Scheduled events and days until next occurrence:
  - trash pickup every Tuesday morning → next Tuesday is 2026-07-01 (4 days)
```

This lets qwen2.5:7b answer temporal questions ("when is my next trash pickup?") by reading precomputed values instead of doing date arithmetic — mitigating the 7B model's temporal reasoning weakness (LLM-001).

Schedule facts are parsed from active `:Fact` nodes with `attribute='schedule'`. The pattern matcher looks for day-of-week keywords and computes the next occurrence from `datetime.date.today()`.

---

## Intent-Based Routing

**File:** `harness/router.py`

**Two-stage pipeline:**

1. **Semantic intent classifier** — embeds the utterance with `nomic-embed-text` and computes cosine similarity against per-domain anchor embeddings. Fast (local embedding); replaces keyword matching.
2. **Complexity gate** — for capability-axis escalation (currently disabled in config).

**Routing axes** (config `routing.axes`):
- `sensitivity` (enabled) — high-sensitivity turns pinned local.
- `freshness` (enabled) — post-cutoff-year questions escalated to SerpAPI.
- `capability` (disabled) — heavy compute escalation not yet wired.

**Intent routing result** is logged to `router.jsonl` for each turn (query_hash, not plaintext — TD-009).

---

## Key Commits (This Session)

```
9219db3 docs: update KNOWN_ISSUES.md with current state
505988b ops: rewrite launchd plist for reliable service management
b98c3ab fix(ui): split-pane layout, scrollable conversation, bot text display
01ea6c8 ops: auto-start dashboard in restart script
8fb8870 fix(fact-change): ensure household updates supersede old values
03d2e67 fix(ui): show bot text, scrollable conversation panel
11fe85b fix(ui): show bot text, scrollable conversation panel
d144e6c feat(ui): HIP branded voice client matching dashboard design
c488cad feat(ui): HIP branded voice client with conversation panel
4568cf4 fix(prompt): cleanup for qwen2.5:7b, add temporal awareness instruction
06a42a6 refactor(dashboard): canonical attribute schema
36aa356 feat(temporal): compute-at-retrieval time context and schedule enrichment
0b73a9b feat(router): two-stage intent + complexity routing
b7e0371 ops: restart script + launchd fix
85713ad fix(voice-orch): handle noise drop, remove permission-asking, prevent confabulation
99e5610 ops: one-command restart script
4489dd9 config: local model qwen2.5:14b -> qwen2.5:7b
46c8197 perf: pre-load edge model at startup, keep_alive 24h on all Ollama calls
0508eb4 refactor(voice_orch): replace hardcoded contradiction detection with detect_and_apply_async
afc386a refactor(orchestrator): remove suppressed_facts from local_system_prompt
```

---

## Current config.yaml State

```yaml
models:
  local: qwen2.5:7b          # edge voice model
  extraction: qwen2.5:32b    # session-end fact extraction
  frontier: claude            # wired Phase 2 (not active)
  embedding: (auto-detect nomic-embed-text)

routing:
  groq_is_onnet: false        # strip personal facts before Groq calls
  axes:
    sensitivity: enabled=true, force_local_at=high
    freshness:   enabled=true, cutoff_year=2023
    capability:  enabled=false

voice:
  stt: faster-whisper base.en (int8, CPU)
  tts: Kokoro af_heart, American English
  speaker_gate: false         # voiceprint pre-filter off (quiet room mode)
  vad: confidence=0.3, stop_secs=0.8

household:
  location: "Lakewood, Colorado, United States"
```

---

## Known Issues (Summary)

See `KNOWN_ISSUES.md` for full detail. Top items as of June 27:

| ID | Severity | Summary |
|----|----------|---------|
| UI-001 | Low | RTVI bot text display needs live testing |
| UI-002 | Medium | Dashboard iframe breaks from remote browsers |
| STT-001 | Low | Whisper: "T" vs "tea" transcription errors |
| FACT-001 | Medium | `preference` is single-valued (should accumulate) |
| ARCH-001 | Low | Session-end extraction conflicts with Groq writes (correct but chatty) |
| OPS-001 | Medium | launchd unreliable; workaround is restart.sh |
| LLM-001 | Low | 7B temporal reasoning (mitigated by temporal enrichment) |
| BUG-001 | Medium | Grounded escalation speaks raw snippet (Option A wired) |

---

## Next Steps / Roadmap

### Immediate (before next demo)

1. **UI-002 fix** — change dashboard iframe src to use Tailscale hostname instead of localhost.
2. **FACT-001 fix** — add `preference` to `MULTI_VALUED` set (or split attribute).
3. **RTVI bot text e2e test** — verify `BotLlmText` events render in the split-pane client from a remote browser.

### Short term

4. **STT upgrade** — try `small.en` for Whisper to reduce single-word transcription errors.
5. **OPS-001 investigate** — root cause launchd failure mode; maybe switch to a `launchctl start` pattern.
6. **ARCH-001 dedup** — check for Groq-vs-session-end write collision; add a "already written this session" guard or timestamp comparison.

### Milestone 2 (multi-member)

- Per-member containers and fact namespacing.
- Speaker gate (`speaker_gate: true`) with Resemblyzer voiceprint verification.
- Registry-driven voiceprint paths (TD-028).

### Milestone 3 (scale / security)

- Answer-level output scanning.
- Living cost model with real telemetry.
- Durable extraction queue (TD-038 — in-memory queue loses jobs on crash).
- Per-member encryption key rotation (TD-030 envelope encryption is built; key management is not).
