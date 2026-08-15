<!-- STATUS: BUILT — traced from live code 2026-07-06 -->
<!-- RECONCILED-AGAINST: main branch, read-only 2026-07-06 -->

# HIP Epistemic Process — Live Path vs Governed Design

How an utterance becomes stored knowledge: the path that ACTUALLY runs, the path the
specs intend, and every point they diverge. Companion to
`LATEST_SYSTEM_UNIVERSE.md` (subsystem map) and `LATEST_FACT_LIFECYCLE.md` (trust states).

**Live entry points.** The live server is `server/voice_https_orch.py` (port 7860, TLS),
which serves two turn handlers from `server/voice_orch.py`:
- **Voice**: WebRTC audio → `OrchestratorGate._on_user_text()` (`voice_orch.py:1256`)
- **Text**: `POST /api/text_query` (`voice_https_orch.py:95`) → `process_text_query()` (`voice_orch.py:2098`)

There is **no single canonical entry function**. `TurnOrchestrator.handle_turn()`
(`orchestrator.py:411`) is the canonical compose — retrieve → contract → answer → metadata —
but its own module header says it "is NOT wired into the 7860/7861 pipelines"
(`orchestrator.py:29`). The two live handlers each re-implement the compose, and they
implement it **differently** (see DIV-2).

---

## Section 1 — Live Path: What Actually Runs

One utterance, traced through the functions that actually execute.

### 1. INTERPRETATION — utterance → WriteDecision

The live path does **NOT** use `memory_engine/interpreter.py`. `GroqInterpreter.classify_write()`
— the governed 4-state classifier with per-utterance confidence and target selection
(`interpreter.py:196-246`) — is called from **nowhere** in `harness/` or `server/`
(only `api.py:100` constructs a GroqInterpreter, for temporality, and `api.py` itself is unwired).

What runs instead is `harness/fact_change.py`:

1. Every routed turn fires `detect_and_apply_async(utterance, facts, owner, …)`
   — voice: `voice_orch.py:1502`; text: `voice_orch.py:2381` (also on the guard path
   `:2247` and temporal-placeholder path `:2304`). Runs in a daemon thread off the audio path.
2. Cheap gates: <4 words, ends with "?", or starts with a question word → no-op
   (`fact_change.py:413-419`).
3. One Groq Llama-4-Scout call (`fact_change.py:235-262`, `_SYSTEM_PROMPT` at `:46-69`)
   classifies the utterance into **`update` / `retract` / `add`** — a 3-action vocabulary,
   NOT the 4 write-states. The model never chooses supersede/augment/correct/unresolved.
4. `_apply_changes()` (`fact_change.py:267-401`) maps actions to writes:
   - `update` / `add` → a **hardcoded** `WriteDecision(state="supersede", target_fact_id=None,
     confidence=0.75)` (`fact_change.py:344-349`). The comment is explicit: "confidence=0.75
     stays above θ_WRITE (0.6) → supersede is applied."
   - `retract` → `retract_fact()` (`extraction_queue.py:544`) — closes rows with
     `closed_by='retracted'`, bypassing `encode()` entirely.

**What determines write_state live:** nothing semantic. Every non-retract mutation
*requests* SUPERSEDE at fixed 0.75 confidence. CORRECT is unreachable. UNRESOLVED is
unreachable (0.75 ≥ θ_WRITE and state is never "correct"-without-target). The only
state variation is the MULTI_VALUED→AUGMENT code override inside `encode()`.

### 2. WRITE — how the decision hits the graph

There are **two** live write paths:

**Path A — per-turn (governed writer, ungoverned decision).** `fact_change._apply_changes`
calls `memory_engine.store.encode()` (`fact_change.py:341-363` → `store.py:297-444`).
This is the real Phase-2 engine writer, so on this path:
- **Code overrides DO apply live** (`store.py:325-347`): MULTI_VALUED SUPERSEDE→AUGMENT
  fires (`:329-332`); CORRECT-no-target→UNRESOLVED (`:334-337`) and
  `write_confidence < θ_WRITE=0.6` →UNRESOLVED (`:339-347`, θ at `store.py:47`) are live
  code but **dead in practice** — the hardcoded 0.75/supersede input can never trip them.
- New node gets `write_state`, `write_confidence`, `confidence_log` seed entry, `tier="hot"`,
  `salience`, encrypted value + driving utterance (`store.py:357-386`).
- Prior row closed with `valid_to`, `closed_reason='superseded'`, `superseded_by`
  (`_tx_supersede`, `store.py:226-260`).
- **Audit trail exists**: `_append_audit()` (`store.py:83`, invoked `:421-435`) records
  requested vs actual state + override reason per write, and
  `log_fact_lifecycle_event()` NDJSON entries fire per proposed/applied change
  (`fact_change.py:284-287, :392-396`).

**Path B — session-end extraction (ungoverned writer).** On client disconnect
(`voice_orch.py:2431-2437`) or mid-session speaker change (`voice_orch.py:1224-1237`),
the session transcript goes to `enqueue_session_end()` → `ExtractionQueue` worker →
`process_session()` (`extraction_queue.py:779`) → LLM fact extraction → `write_facts()`
(`:585`) → `_write_one()` (`:460-504`). This writer predates the engine and **bypasses
`encode()` completely**: nodes carry **no `write_state`, no `confidence_log`, no
`closed_reason`** (it sets a different field, `closed_by`), no tier/salience, no
write audit. Every session-end fact therefore classifies as **UNCONFIRMED** under
`trust()` (null write_state falls to the catch-all, `queries.py:713-718`) — regardless
of how confidently it was stated.

Encryption is identical on both paths (envelope: master key → HKDF-SHA256 per-owner
Fernet key → random per-fact DEK; `encryption.py:9-23`; called at `store.py:350` and
`extraction_queue.py:475`).

### 3. CLASSIFY — when trust() runs

**Never at write. Never at read. Never anywhere in the live turn pipeline.**
`truth_layer.queries.trust()` (`queries.py:637`) derives the level on demand from stored
fields — it is not persisted — and its only callers are the demo dashboard's
`/api/fact_history` endpoint and the eval harnesses. The live pipeline injects facts
without ever computing their trust level; the model sees a flat
`attribute: value` list (`orchestrator.py:336-342`) with no trust framing, no hedging
for UNCONFIRMED, no "derived" prefix.

The one live-adjacent classification is `fact_change._classify_trust()`
(`fact_change.py:146-180`), used **only to label before/after delta records** for the
demo. Note: commit `4fadca2` unified its CORROBORATED predicate with the canonical
`queries.py:608-621` numeric-rise check — **the two-classifier divergence flagged in
SYSTEM_UNIVERSE (2026-07-06 09:00) is FIXED as of this document.**

### 4. RETRIEVE — what pulls facts on the next turn

`orch.decide()` → `orch.retrieve()` (`orchestrator.py:213-239`):

```python
facts = (search_facts_by_embedding(query, self.user_id, top_k=self.max_facts)
         or read_user_facts(self.user_id, limit=self.max_facts))   # orchestrator.py:236-237
```

Both live in `harness/extraction_queue.py` — **not** `memory_engine.api.candidate_facts()`,
which is fully built (tier-aware Cypher, temporality via interpreter, annotation keys;
`api.py:104-140+`) and **NOT WIRED**. The live filters:
- `read_user_facts` (`extraction_queue.py:624-677`): `valid_to IS NULL AND owner IN
  (member, 'household')`, newest 20. **No tier filter, no temporality, no trust/UNRESOLVED
  annotation, no staleness check.**
- `search_facts_by_embedding` (`:680-746`): same, plus `embedding IS NOT NULL` —
  and `encode()` writes `embedding: None` in Phase A (`store.py:195-196`), so
  **engine-written facts are invisible to semantic search** and surface only via the
  `read_user_facts` fallback (which fires only when embedding search returns nothing).

**Disclosure — the two live paths diverge here (this is the largest single finding):**
- **Text path**: full HARDENING-spec governance. `resolve_subject()` (`voice_orch.py:2220`)
  → `apply_injection_contract()` (`:2221`) applying INJ-1 subject-scope, INJ-2 relevance,
  INJ-3 cross-member deny, INJ-4 household, INJ-5 never-volunteer, INJ-6 empty-set guard
  (`injection_contract.py:167-236`), structured refusal without a model call when the
  guard fires (`:2225-2254`).
- **Voice path**: **the injection contract never runs.** `_on_user_text` passes
  `d["facts"]` straight into `local_system_prompt()` (`voice_orch.py:1730-1733`), whose
  only filters are the role/permission `filter_facts()` (`orchestrator.py:306, :332`)
  and the guest override (unverified speaker → no facts at all, `voice_orch.py:1367-1369`,
  `:1726-1728`). No subject scoping, no INJ-2 relevance gating, no INJ-5 never-volunteer,
  no INJ-6 structural refusal on spoken turns. The import at `voice_orch.py:124` is used
  only by the text path.

Additional voice-path quirk: the shared `TurnOrchestrator` is constructed once with
`user_id=SPEAKER_USER="bill"` (`voice_orch.py:128, :2021-2023`), so `decide()`'s
retrieval — the fact set used for sensitivity tagging and fact-change detection — is
**always bill-scoped regardless of who is speaking**. The per-member scoping happens
later, inside `local_system_prompt(owner=self._member_id)` (`orchestrator.py:325-331`),
which re-queries. The text path constructs a fresh orchestrator per request with
`user_id=member` (`voice_orch.py:2191-2194`) and doesn't have this problem.

### 5. CONSOLIDATE — confirmed offline-only

`memory_engine/consolidate.py`'s own header: *"Runs offline (nightly default); NEVER
called from a live turn"* (`consolidate.py:5`). `run_consolidation()` (`consolidate.py:731`)
is invoked only from `eval/memory_harness.py` and `eval/memory_e2e.py` — no call site in
`harness/` or `server/`. Consequences, confirmed as actual live behavior:

- **ASSERTED never climbs to CORROBORATED live.** The harden transition requires a
  `reconcile`-sourced confidence_log entry (`queries.py:608-621`), which only
  `_reconcile_pass` writes.
- **UNRESOLVED never resolves live** — and is in practice never *created* live either
  (see §1). The entire UNRESOLVED disclosure/resolution machinery
  (`confirm_when_relevant`, fluid confirmation, `must_confirm_queue` from
  `_escalate_pass` at `consolidate.py:707-720`) has no live producer or consumer.
- Tier demotion/promotion never runs: every fact stays `tier="hot"` (engine writes) or
  tierless (session-end writes) forever.

**Net live trust ceiling: a fact enters at ASSERTED (per-turn path) or UNCONFIRMED
(session-end path) and can never move up.** The only live trust transition is
*downward/structural*: being superseded or retracted.

---

## Section 2 — Governed Design: What Was Intended

1. **INTERPRETATION** (MEMORY_ENGINE spec §2): every write classified by
   `Interpreter.classify_write()` (`interpreter.py:111`) into the full 4-state vocabulary
   with a real per-utterance confidence, a specific `target_fact_id`, and a rationale —
   model judgment isolated behind a swappable protocol.

2. **WRITE**: all mutations through `encode()` (`store.py:297`) so the θ_WRITE gate and
   the three code overrides actually discriminate — low-confidence claims land as
   UNRESOLVED with `confirm_when_relevant=true`, corrections inherit `valid_from`
   (`_tx_correct`, `store.py:268-287`), and every write is audited requested-vs-actual.
   One writer, no side door.

3. **CLASSIFY**: `trust()` (`queries.py:637`) as the canonical read-side classifier;
   disclosure formatting hedges UNCONFIRMED/UNRESOLVED facts and prefixes DERIVED ones
   (spec §1.4 annotation keys, `api.py:20-27`).

4. **RETRIEVE**: `candidate_facts(member, query)` (`api.py`) — tier-aware
   (`tier IN ('hot','warm')` structural cold exclusion), temporality-classified
   (historical → warm admitted; current → hot only, fail-closed), annotation keys for
   the formatter — then `resolve_subject` + `apply_injection_contract` **unchanged on
   every path** (spec §1.1: the frozen interface).

5. **CONSOLIDATE**: nightly `run_consolidation()` (`consolidate.py:731`) —
   RECONCILE (harden/loosen/resolve) → ABSTRACT (derived facts) → PROMOTE → DEMOTE →
   ESCALATE (salience ≥ 0.75 → `must_confirm_queue` → HIP-initiated confirmation).
   This is what makes trust a *ladder* instead of a stamp.

---

## Section 3 — End-to-End Divergence Map

```
                              UTTERANCE IN
                                   │
              ┌────────────────────┴────────────────────┐
              │ VOICE (WebRTC→VAD→Whisper)               │ TEXT (POST /api/text_query)
              │ voice_orch.py:1074→1132→1256             │ voice_https_orch.py:95→voice_orch.py:2098
              ▼                                          ▼
        [speaker verify]                           [member given explicitly]
        resemblyzer, per-turn, all members         no audio, no verification
        voice_orch.py:1317-1358                    voice_orch.py:2098
        no match → guest: zero facts (M4-04)
              │                                          │
              ▼                                          ▼
   ┌── RETRIEVE ─────────────────────────────────────────────────────────────────┐
   │ LIVE: search_facts_by_embedding() or read_user_facts()                      │
   │       extraction_queue.py:680 / :624 — valid_to IS NULL, owner+household    │
   │       no tier filter · no temporality · no trust annotation                 │
   │       (voice: always user_id="bill" in decide(), voice_orch.py:2021)        │
   │ GOVERNED: candidate_facts(member, query)  api.py — tier-aware hot/warm,     │
   │       temporality fail-closed, annotation keys                NOT WIRED     │
   └─────────────────────────────────────────────────────────────────────────────┘
                         ⚑ DIV-1: RETRIEVAL GOVERNANCE
              │                                          │
              ▼                                          ▼
        [disclosure]                               [disclosure]
        filter_facts() permissions only            resolve_subject voice_orch.py:2220
        NO injection contract                      apply_injection_contract :2221
        voice_orch.py:1730                         INJ-1..6 + empty-set guard :2225
                         ⚑ DIV-2: INJECTION CONTRACT — VOICE PATH SKIPS IT
              │                                          │
              └────────────────────┬─────────────────────┘
                                   ▼
                          [route + answer + speak]
                          (edge qwen / Groq mid/core / web-grounded escalate)
                                   │
                                   ▼
   ┌── INTERPRET (background thread, every routed turn) ─────────────────────────┐
   │ LIVE: fact_change.detect_and_apply_async  voice_orch.py:1502 / :2381        │
   │       Groq classifies {update|retract|add}   fact_change.py:46-69           │
   │       → HARDCODED WriteDecision(supersede, target=None, conf=0.75) :344     │
   │ GOVERNED: GroqInterpreter.classify_write → 4 states, real confidence,       │
   │       real target_fact_id   interpreter.py:196            NEVER CALLED      │
   └─────────────────────────────────────────────────────────────────────────────┘
                         ⚑ DIV-3: WRITE-STATE IS A CONSTANT, NOT A CLASSIFICATION
                                   │
                     ┌─────────────┴──────────────────┐
                     ▼                                ▼
   ┌── WRITE path A: per-turn ──────────┐  ┌── WRITE path B: session end ────────┐
   │ encode()  store.py:297             │  │ disconnect/speaker-change →         │
   │ overrides LIVE: MULTI_VALUED→      │  │ enqueue_session_end                 │
   │   AUGMENT fires (store.py:329)     │  │ voice_orch.py:2431 / :1224          │
   │ θ_WRITE + CORRECT-no-target: live  │  │ → write_facts → _write_one          │
   │   code, dead inputs (0.75 const)   │  │ extraction_queue.py:585/:460        │
   │ write_state+confidence_log+audit ✓ │  │ NO write_state, NO confidence_log,  │
   │ retract → retract_fact() bypasses  │  │ NO closed_reason (closed_by), NO    │
   │   encode  extraction_queue.py:544  │  │ audit → trust() = UNCONFIRMED       │
   └────────────────────────────────────┘  └─────────────────────────────────────┘
                         ⚑ DIV-4: SECOND UNGOVERNED WRITER
                                   │
                                   ▼
   ┌── CLASSIFY ─────────────────────────────────────────────────────────────────┐
   │ LIVE: trust() NEVER runs in the turn pipeline — level derived on read,      │
   │       only by dashboard + fact_change delta labels (fact_change.py:373)     │
   │       model sees flat "attribute: value" list, no hedging, no framing       │
   │ GOVERNED: trust-annotated disclosure; UNRESOLVED hedged; DERIVED prefixed   │
   └─────────────────────────────────────────────────────────────────────────────┘
                         ⚑ DIV-5: TRUST IS COMPUTED FOR NO ONE
                                   │
                                   ▼
   ┌── CONSOLIDATE ──────────────────────────────────────────────────────────────┐
   │ LIVE: nothing. run_consolidation (consolidate.py:731) called only by eval/  │
   │       ASSERTED→CORROBORATED impossible · UNRESOLVED unresolvable (and       │
   │       uncreatable) · must_confirm_queue write-only · tiers frozen at "hot"  │
   │ GOVERNED: nightly RECONCILE→ABSTRACT→PROMOTE→DEMOTE→ESCALATE                │
   └─────────────────────────────────────────────────────────────────────────────┘
                         ⚑ DIV-6: THE TRUST LADDER HAS ONE RUNG
```

**DIV-1 — Retrieval governance.** Live pulls flat owner+household facts with no tier,
temporality, or trust logic (`extraction_queue.py:624,680`); the governed
`candidate_facts()` (`api.py`) exists, is tested, and is unwired (`orchestrator.py:43`
still imports from extraction_queue). Consequence: warm/historical retrieval and
UNRESOLVED hedging can never happen; engine-written facts (embedding=None,
`store.py:195`) are also invisible to semantic search, surfacing only via the fallback.

**DIV-2 — Injection contract skipped on voice.** The text path runs INJ-1..6 + the
empty-set guard (`voice_orch.py:2220-2254`); the live **voice** path never calls
`apply_injection_contract` — its only gates are role permissions and the guest
lockout (`voice_orch.py:1726-1733`). Consequence: on spoken turns, cross-member
subject scoping (INJ-1/3), relevance withholding (INJ-2), never-volunteer (INJ-5) and
the structural refusal (INJ-6) do not execute. The HARDENING spec's "structural DENY
before the model sees facts" holds for typed queries only.

**DIV-3 — Interpretation is a constant.** The governed classifier
(`interpreter.py:196`) is never called; `fact_change.py:344-349` hardcodes
supersede@0.75. Consequence: CORRECT and UNRESOLVED are unreachable live; the
θ_WRITE gate and correct-no-target override are dead branches; corrections
("actually, it was always X") are stored as supersessions, losing the
`record_closed_at`/`closed_reason='error'`/inherited-`valid_from` semantics.

**DIV-4 — Two writers, one governed.** Per-turn writes go through `encode()` with
full metadata + audit; session-end extraction writes raw nodes via `_write_one`
(`extraction_queue.py:460`) with no write_state/confidence_log/closed_reason.
Consequence: the same spoken fact lands ASSERTED if caught per-turn but UNCONFIRMED
if only caught at session end; supersede chains closed by `_write_one` use `closed_by`,
which `trust()`/`lineage()` don't read.

**DIV-5 — Trust computed for no one.** `trust()` is derived-on-read and correct
(`queries.py:637-724`), but no live code reads it. Consequence: disclosure treats a
9-month-old unconfirmed extraction and a human-confirmed fact identically.
(The SYSTEM_UNIVERSE two-predicate divergence is FIXED — commit `4fadca2`.)

**DIV-6 — Consolidation offline-only.** Header-confirmed (`consolidate.py:5`), call-site
confirmed (eval/ only). Consequence: live trust is write-once — ASSERTED or UNCONFIRMED
at birth, immutable until superseded. Every upward transition in the fact-lifecycle
diagram is OFFLINE or NOT-WIRED.

---

## Section 4 — Consequence Table

| DIV | Point | Live behavior | Governed behavior | Consequence | Severity |
|---|---|---|---|---|---|
| 1 | Retrieval | `read_user_facts`/`search_facts_by_embedding` — flat, no tier/temporality/trust (`extraction_queue.py:624,680`); engine facts unembedded (`store.py:195`) | `candidate_facts()` tier-aware + temporality fail-closed (`api.py`) | No historical retrieval, no UNRESOLVED hedging, cold never excluded structurally; engine-written facts invisible to semantic search | GOVERNANCE |
| 2 | Disclosure (voice) | Injection contract never runs on spoken turns; permissions filter only (`voice_orch.py:1730`) | INJ-1..6 + empty-set guard before model sees facts (as text path does, `voice_orch.py:2221`) | Subject-scoping, relevance, never-volunteer, structural refusal absent on the primary (voice) modality | GOVERNANCE |
| 3 | Interpretation | Hardcoded `WriteDecision(supersede, None, 0.75)` (`fact_change.py:344`); Groq picks update/retract/add only | `classify_write()` → 4 states, real confidence, real target (`interpreter.py:196`) | CORRECT/UNRESOLVED unreachable; θ_WRITE gate dead; corrections mislabeled as supersessions | CORRECTNESS |
| 4 | Write | Second writer `_write_one` at session end: no write_state/confidence_log/closed_reason/audit (`extraction_queue.py:460`) | All writes through `encode()` (`store.py:297`) | Session-end facts permanently UNCONFIRMED; lineage fields inconsistent (`closed_by` vs `closed_reason`) | CORRECTNESS |
| 5 | Classify | `trust()` never called in live pipeline; flat fact injection | Trust-annotated disclosure with hedging/prefixes | Model can't distinguish confirmed from unconfirmed facts; states everything with equal confidence | GOVERNANCE |
| 6 | Consolidate | `run_consolidation` eval-only (`consolidate.py:731`); header says never-live (`consolidate.py:5`) | Nightly 5-pass REM cycle | ASSERTED→CORROBORATED impossible; UNRESOLVED machinery producer-less and consumer-less; tiers frozen | COMPLETENESS |
| 7 | Retrieval scope (voice) | `decide()` retrieves as `user_id="bill"` regardless of speaker (`voice_orch.py:2021`); per-member scoping only later in `local_system_prompt` | Per-member retrieval end to end (as text path: `voice_orch.py:2191`) | Sensitivity tag + fact-change context computed from the wrong member's facts when a non-bill member speaks | LATENT |
| 8 | Interpretation trigger (voice) | Fires only when `self._last_facts` non-empty (`voice_orch.py:1501`) | Text path: "Always fire even on empty graph" (`voice_orch.py:2378-2381`) | A new member's first facts are never captured per-turn on voice — only at session end (into the ungoverned Path B) | LATENT |
| 9 | Retraction | `retract_fact` bypasses `encode()`, sets `closed_by='retracted'` (`extraction_queue.py:544`) | All lifecycle mutations audited through the engine | Retractions invisible to `closed_reason`-based queries (`correction_history`, dashboard chains) | COMPLETENESS |
| 10 | Trust predicates | `fact_change._classify_trust` now mirrors `queries.py` numeric-rise (commit `4fadca2`) | Two classifiers must agree | **FIXED** — divergence claimed in SYSTEM_UNIVERSE v20260706_0900 row 6 is stale | — |

**Reading order for remediation:** DIV-2 (voice contract) is the largest governance gap
and is a wiring change, not a build. DIV-3 + DIV-4 together explain why the stored graph's
epistemic metadata is mostly vacuous today. DIV-1/5/6 are the "engine built, not plugged in"
family already tracked in the plan of record.
