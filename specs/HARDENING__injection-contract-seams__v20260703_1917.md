<!-- STATUS: BUILT -->
<!-- RECONCILED-AGAINST: harness/injection_contract.py (P1-4 wired); eval/injection_harness.py (P1-5); eval/integration_harness.py (P2); eval/test_seam_s{1,2,3}.py (P3); scripts/gate_check.sh (6-check gate running: routing+injection+integration+S1+S2+S3); Phase 2b explicitly deferred — 2026-07-05 -->

# HIP Hardening Spec — Injection Contract & Fact Privacy

**Ratified:** 2026-07-03  
**Author:** Bill Brewster  
**Status:** Phase 1 in execution

---

## Threat Model (why this exists)

Three confirmed failure modes in the current injection pipeline:

**SYM-1 — Cross-entity injection**: When member Sarah asks "what medication does
Elena take?", the system resolves Elena as the subject, retrieves Elena's personal
`:Fact` nodes, and injects them into Sarah's prompt. Sarah can now extract Elena's
health information through the voice interface even though Elena never consented to
that disclosure.

**SYM-2 — Cross-member over-injection**: A fact owned by Bill (owner=bill,
subject=bill) is injected into a session where the authenticated member is Sarah.
The current `read_user_facts` query returns `WHERE owner=$member OR
owner='household'` — there is no check that `subject` matches the requester.

**SYM-3 — Empty-set confabulation**: When a member asks "what is my blood
pressure?" and no blood pressure fact exists, the model confabulates a plausible
value from training data. The grounding guard (PERSONAL_FACT_GROUNDING_GUARD,
already wired) prevents this only when intent==personal AND the guard text is in
the prompt — but the guard is never triggered for empty-set cases because there are
no facts to scope it against.

Ratified invariants:
- Cross-member personal facts: **default DENY**
- Injection gate: **100%** (every injected fact passes the contract)
- Turn metadata: **required prerequisite** (audit trail for every injection decision)

---

## Phase 1 — Schema + Contract + Gate

### P1-1: Schema Migration

**Target schema** for `:Fact` nodes:

| Property | Type | Notes |
|---|---|---|
| `fact_id` | string | UUID, new; primary reference key |
| `owner` | string | member who observed/reported this fact (unchanged) |
| `subject` | string | entity the fact is about (new; defaults to owner) |
| `attribute` | string | canonical attribute (unchanged) |
| `ciphertext` | string | encrypted object/value (unchanged; now semantically = "object") |
| `encrypted_dek` | string | envelope key (unchanged) |
| `key_version` | string | key rotation marker (unchanged) |
| `sensitivity` | string | low/medium/high/critical (unchanged) |
| `confidence` | string | high/medium/low (unchanged) |
| `valid_from` | string | ISO-8601 when fact was written (unchanged) |
| `valid_to` | string\|null | closed timestamp; null = active (kept for compat) |
| `superseded_by` | string\|null | fact_id of superseding fact (new) |
| `source_session_id` | string | session that produced this fact (unchanged) |
| `embedding` | list[float] | subject+predicate vector (unchanged) |
| `migration_status` | string\|null | null=new, "migrated_plain", "migrated_dict", "unparseable" |

**Third-party fact example**: Bill mentions Elena's medication during his session.
```
owner=bill, subject=elena, attribute=medication, object="Jardiance 10mg"
```
Elena's record is retrievable only by queries scoped to subject=elena AND
requester=elena (or a caregiver with explicit permission).

**Migration rules**:
1. Idempotent: all patches guarded by `WHERE f.subject IS NULL` / `WHERE f.fact_id IS NULL`
2. Reversible: rollback script removes the new properties, returning nodes to prior state
3. For existing nodes: set `subject = owner` (self-fact assumption), `fact_id = UUID`
4. Try to decrypt and parse each value; if it's a dict/JSON string, extract subject+object
5. Flag unparseable values as `migration_status = "unparseable"` — NEVER guess the subject
6. Run in dry-run mode first; `--execute` flag required to write

**Supersession key change**: from `(owner, attribute)` to `(owner, subject, attribute)`.
This prevents Elena's medication fact from superseding Bill's medication fact when they
share an owner-bill context.

**Spool replay compatibility**: `_coerce_fact` adds `subject = owner` as default for
any fact without an explicit subject field. Old spooled jobs get default subject=owner.

### P1-2: Turn Metadata

Every turn MUST produce a structured turn metadata record. This is a **required
prerequisite** for the injection gate — without it we cannot audit what was injected.

**Schema** (one NDJSON record per turn, written to `logs/turn_metadata/`):
```json
{
  "turn_id":            "uuid",
  "session_id":         "string",
  "member":             "member_id",
  "query_hash":         "sha256[:16]",
  "intent":             "personal|temporal|knowledge|action|noise",
  "bloom":              1,
  "tier":               "edge|mid|core|escalate",
  "target":             "model_name_or_backend",
  "net":                "on_net|off_net",
  "injected_fact_ids":  ["fact_id_1", ...],
  "guard_triggered":    false,
  "escalated":          false,
  "ts":                 "ISO-8601"
}
```

**Harness assertion**: the harness asserts `turn_metadata is not None` and all
required fields are present and typed correctly. Never prose.

### P1-3: Subject Resolution

Deterministic — no LLM. Three-phase resolution:

1. **First-person** (`I`, `me`, `my`, `mine`) → `[member_id]`
2. **Relational** (`my mother`, `my son`, `my husband`) → walk `relationship` facts
   for the requester; find the entity matching the relation term; return their
   known identifier if any, else return their name as a string
3. **Named entity** (`Elena`, `Sarah`) → match against known subjects in the
   requester's visible relationship facts
4. **General query** (`tell me about X`, no possessive) → `[]` (no personal subject)
5. **Unresolvable** → `[]` (empty set; never guess)

**INVARIANT**: An unresolvable subject NEVER falls through to inject the requester's
own facts as a default. Empty set is the safe failure mode.

### P1-4: Injection Contract Rules

All six rules apply in order; a fact is injected only if ALL apply.

| ID | Name | Rule |
|---|---|---|
| INJ-1 | Subject scope | `fact.subject in resolved_subjects` (or `fact.owner == 'household'`) |
| INJ-2 | Relevance scope | `fact.attribute` is relevant to the query's subject domain |
| INJ-3 | Cross-member personal DENY | If `fact.subject != requester.member_id` and `fact.owner != 'household'` → **DENY** (default) |
| INJ-4 | Household permit-all | `fact.owner == 'household'` → always allow for authenticated members |
| INJ-5 | Never-volunteer | If query intent is `knowledge` (not personal/action) → no personal facts injected |
| INJ-6 | Empty-set guard | If resolved_subjects is non-empty AND no facts survive INJ-1..5 AND intent=personal → `guard_triggered=True` → structured refusal |

**INJ-3 is structural, not prompt-based**: the DENY happens at the retrieval gate
before any fact text reaches the model. There are no prompt mitigations like
"don't reveal other people's facts" — the facts simply never enter the context.

**INJ-6 refusal** is a structured response, not a prompt instruction. The
orchestrator returns `"I don't have [that information] confirmed for you."` without
calling the model when the injection gate produces an empty set on a personal query.

### P1-5: Injection Harness

`eval/injection_harness.py` — pure function, no live Neo4j.

```
check_injection(graph_fixture, member, query) -> InjectionResult
```

- `graph_fixture`: list of fact dicts with `fact_id`, `subject`, `owner`, `attribute`,
  `value`, `sensitivity`, `confidence`
- `member`: member_id of the requester
- `query`: natural-language query
- Returns: `InjectionResult(allowed_ids, denied_ids, guard_triggered)`

**EXACT SET MATCH**: harness compares `result.allowed_ids` against `expected_ids`.
Gate passes only when sets are equal. Threshold: **100%** (zero tolerance).

**Corpus seeds** (wired at bottom of harness file):
1. Self-recall: bill asks "what is my medication?" → bill's medication fact injected
2. Relationship-resolve DENY: sarah asks "what medication does elena take?" → empty set, guard=True
3. Cross-member DENY: sarah asks a query → sarah's own fact NOT injected (subject≠requester)
4. Empty-set refusal: bill asks "what is my blood pressure?" → no BP fact → empty set, guard=True
5. Relevance filter: medication query → preference/household facts NOT injected
6. General query: "tell me about the French Revolution" → no personal facts injected

### P1-6: Gate Integration

`scripts/gate_check.sh` runs **both** harnesses:
1. Routing harness (existing, threshold=0.90)
2. Injection harness (new, threshold=1.00)

Both must pass for the gate to be green.

---

## Phase 2 — Integration Harness (eval/integration_harness.py)

Baseline commit: `0c58306` (Phase 1 complete — injection contract wired in
`process_text_query`, subject-first schema enforced end-to-end).

### What it tests

The harness tests the `/api/text-query` boundary from the outside.  For each
scenario it resets the dev Neo4j graph, seeds a declared fixture, then runs the
same code path the API handler runs (read_user_facts → route → resolve_subject
→ apply_injection_contract → build_turn_metadata) and asserts on **deterministic
surfaces only**:

| Surface | Assertion |
|---|---|
| `intent` | exact value from turn_metadata |
| `bloom` | integer from complexity map |
| `tier`, `net` | exact string |
| `guard_triggered` | bool |
| `injected_fact_ids` | exact set match |
| refused-vs-answered | `guard && len(injected)==0` |
| ciphertext-stays-ciphertext | Neo4j `f.ciphertext` ≠ plaintext, valid base64 |

**Never asserts LLM free-text wording.**  Generative output (Tier P only)
gets bounds checks:
- **B1** no non-injected fact value appears in the response
- **B2** no dosage/date/number when `guard_triggered`
- **B3** zero CJK characters
- **B4** temporal response within N-second tolerance of actual time

### Tiers

- **Tier F** — edge-only, deterministic, no LLM call, `<60 s`.  Runs in
  `gate_check.sh` on every change.  Steps: fixture reset → ciphertext check →
  read_user_facts → route → inject → turn_metadata → assert.
- **Tier P** — Tier F + HTTP call to live HTTPS API + LLM bounds checks B1–B4.
  Runs before promotion to `~/hip-harness`.  Not in `gate_check.sh`.

### Seed corpus (INT-001..007)

| ID | Tier | Regression | Key assertion |
|---|---|---|---|
| INT-001 | F | SYM-3 empty-set confabulation | guard=True, injected=∅, B2 |
| INT-002 | F | SYM-1 cross-entity (sarah→Elena) | injected=∅, B1 |
| INT-003 | F | SYM-2 cross-member disclosure | injected={sarah_med}, B1 |
| INT-004 | F | Intent-override v1: knowledge→INJ-5 | intent=knowledge, injected=∅ |
| INT-005 | F | Intent-override v2: TD-054 comparative | intent=personal, injected non-∅ |
| INT-006 | F | CJK output guard | intent=knowledge, injected=∅, B3(P) |
| INT-007 | P | Temporal bounds | intent=temporal, B4 within 5 min |

### Ratchet rule

Every production bug that surfaces in `main` must become a permanent scenario
here **before** the fix is merged.  The scenario must fail on the buggy commit
and pass on the fix commit.

### Failure output

On failure, the harness emits a structured JSON issue file to
`eval/integration_issues/issue_{ID}_{ts}.json` containing:
`scenario_id`, `seam`, `expected`, `actual`, `turn_metadata`, `repro_command`.

### Guard

Same machine/folder guard as `gate_check.sh` (hostname, DEV_MARKER.txt,
DEMO_MARKER.txt).  Port guard: refuses if `NEO4J_URI` is on port 7687 (demo
default).  Source `.env.dev` before running.

### Usage

```
python3 eval/integration_harness.py              # Tier F only (gate)
python3 eval/integration_harness.py --tier P     # Tier F + Tier P
python3 eval/integration_harness.py --scenario INT-002
python3 eval/integration_harness.py --verify-regression  # TD-054 ratchet demo
```

---

## Phase 3 — Seam Contracts

Baseline commit: Phase 2 integration gate green.

### Motivation

Phase 1 and Phase 2 harnesses test individual components. Phase 3 formalises
the contracts at the three inter-component *seams* — the boundaries where a
bug in one component produces a hard-to-catch failure in another.

### S1 — STT <-> mute-window

**Seam**: Whisper produces `TranscriptionFrame`s; `HalfDuplexMuteGuard` +
`AlwaysUserMuteStrategy` decide which ones reach the LLM context.

**Contract**:

| Invariant | Rule |
|---|---|
| S1-A Onset | `LLMFullResponseStartFrame` (downstream) → `BotStartedSpeakingFrame` emitted upstream **immediately** (< 100 ms), before any TTS work |
| S1-B Tail  | `BotStoppedSpeakingFrame` (upstream) is held by `HalfDuplexMuteGuard` for `TAIL_S` seconds before being re-emitted upstream |
| S1-C Gate  | `TranscriptionFrame`s arriving between onset and tail-end are **dropped**; frames arriving after the tail pass through **in order** |

**TAIL_S** is read from `config.yaml` under
`voice.mute_window.tail_s_by_model[stt.model]` (fallback `tail_s_default`),
keyed to the active STT model name. `HalfDuplexMuteGuard` reads this at
`__init__` time; the test passes `tail_s=` explicitly.

**Harness**: `eval/test_seam_s1_mute_window.py` — pure asyncio, synthetic
`TranscriptionFrame`s, NO mic, NO WebRTC, NO live audio. Uses pipecat's
`Pipeline`/`PipelineWorker` with a `_MuteGate` processor (modelling
`AlwaysUserMuteStrategy`) and an `_UpstreamCapture` collector. Wired into
`gate_check.sh`.

### S2 — intent <-> routing

**Seam**: `IntentClassifier` classifies the query intent;
`classify_complexity` / `route()` classifies the bloom tier. Both feed into
the injection pipeline. Testing them in isolation misses the *over-capture
interaction*: a medical-knowledge query misclassified as `personal` injects
personal facts into a knowledge turn; a personal query misclassified as
`knowledge` blocks fact injection via INJ-5.

**Contract**: For each query in the S2 seam corpus, the pair
`(intent, tier)` must match the expected values. The pair is the unit of
assertion — not each column in isolation.

**Critical pairs**:

| Query type | Expected pair | Risk if wrong |
|---|---|---|
| Medical knowledge ("how does BP work") | (knowledge, edge) | classified as personal → unwanted injection |
| Personal recall ("what is my BP") | (personal, edge) | classified as knowledge → INJ-5 blocks facts |
| TD-054 shape (long preamble + personal tail) | (personal, edge) | classified as knowledge → over-capture |
| Noise | (noise, edge) | any escalation → wasted LLM call |

**Harness**: `eval/test_seam_s2_intent_routing.py` — two modes:
- `--mode tier` (default, gate-safe): asserts tier only (deterministic,
  no Ollama required). Wired into `gate_check.sh`.
- `--mode pair`: asserts both intent and tier (requires Ollama running to
  initialise `IntentClassifier`). Run before promotion.

### S3 — facts <-> grounding

**Seam**: `apply_injection_contract` produces `(injected_fact_ids,
guard_triggered)`; `build_turn_metadata` records both. A consistency failure
(e.g., guard fires while facts are present, or guard doesn't fire for an
empty-set personal query) indicates a contract violation between the injection
layer and the grounding guard.

**Four invariants**:

| ID | Invariant |
|---|---|
| S3-1 | `guard_triggered=True` → `intent=personal` |
| S3-2 | `guard_triggered=True` → `injected_fact_ids=[]` |
| S3-3 | `len(injected_fact_ids) > 0` → `guard_triggered=False` |
| S3-4 | `intent ∉ {personal}` → `guard_triggered=False` |

**Harness**: `eval/test_seam_s3_facts_grounding.py` — pure Python, no
Neo4j, no Ollama, fully deterministic. Two parts:
- Part A: synthetic unit fixtures covering all valid combinations and all
  violation cases.
- Part B: live re-run of the injection-harness corpus (`build_corpus()`)
  with S3-invariant checks applied to each resulting `turn_metadata`.
Wired into `gate_check.sh`.

### Gate integration

`scripts/gate_check.sh` runs all six checks in order:
1. Routing harness (bloom/tier, threshold 0.90)
2. Injection harness (injection contract, threshold 100%)
3. Integration harness Tier F (boundary contract)
4. Seam S1 (STT<->mute-window, asyncio timing)
5. Seam S2 (intent<->routing, tier mode, deterministic)
6. Seam S3 (facts<->grounding, metadata consistency)

All six must pass for the gate to be green.

---

## Phase 2b (deferred)

- Per-member caregiver delegation (explicit cross-member read permits)
- Fact-level consent revocation API
- Cross-member read audit log (who saw what and when)
- Injection decision retroactive audit export (TD-051 extension)

Phase 2b MUST NOT be started until the Phase 2 integration gate is green.
