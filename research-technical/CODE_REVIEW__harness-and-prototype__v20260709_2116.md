# Code Review — Proof Harness + Prototype Core
Status: BUILT
Reconciled-Against: code main after 25f1c74 (Phase 3 harness landed), read-only review 2026-07-09

Scope: full read-through of the verification harness (`eval/`) and four prototype-core
modules — `harness/injection_contract.py`, `harness/subject_resolution.py`,
`harness/fact_change.py`, `server/voice_orch.py`. Gap analysis against
`docs/testing/LATEST_HARNESS_SPEC.md` (v20260709_0736). Nothing was modified.

Findings cite `file:line`. Line numbers are as of the reviewed checkout and will drift.

---

## Cross-cutting summary (highest-value items)

**Critical — harness trustworthiness**
1. **`reporter.py:151` — partial-run `--update-baseline` wipes the baseline.** It writes
   only the current run's scenarios, dropping every other layer's keys. This is the exact
   mechanism behind the b01c3fd baseline collapse on the Mini (reduced to care_coordination
   only) — a code bug, not operator error.
2. **`fixture.py:106` — `verify_seed` passes on decryption failure.** Decrypt failure →
   `value=None` → `got=""` → `"" in anything` is True. Garbage ciphertext passes drift
   verification silently.
3. **`layer1.py:552` — P6 `_last_meta` returns the wrong metadata line** when >1 entry lands
   between snapshots. P6's core mechanism is unsound under async-write interleaving.

**Critical — prototype governance**
4. **Voice path is unhardened.** `_on_user_text` (voice) has no injection contract, no F3
   gate, no turn metadata. Everything the harness proves is true only of `process_text_query`
   (typed). The live voice path can leak cross-member facts and ack unlanded writes.
5. **F3 gate fails open when `_apply_changes` raises** — outcome never stored → gate sees
   `None` → passes the ack through, the exact case F3 exists to block. Compounded by
   cross-turn outcome bleed across four fire-and-forget detection call sites.
6. **Refusal-string blind spot** — the no-subject access-control fallback matches neither
   harness regex, classifies as `"none"`, invisible to P4/L2/L5.
7. **Fail-open on unknown intents** in `injection_contract.py` — a new router intent label
   bypasses INJ-5/6/6b/7 entirely.

**Structural / drift debt**
8. **INJ-3 confirmed dead on the live path** (matches the L3 mutation finding); INJ-1 nearly
   so. Cross-member enforcement actually lives in owner-scoped retrieval, not these rules.
9. **Highest-risk drift pair:** imperative keyword lists in
   `injection_contract._QUESTION_OPENER_RE` vs `subject_resolution._IMPERATIVE_DATIVE_STRIP_RE`
   have already diverged. "Read me Elena's medication" classifies declarative → bypasses INJ-7
   and both empty-set guards.
10. **Duplicated ground truth**: three seed mirrors (fixture / layer5 / gen_pairwise), three
    decrypt-row helpers, three poll loops, four flake mechanisms, two detection ceilings
    (20 s vs 4 s), duplicated 120 s turn timeout.
11. **`_DETECTION_FACTS_LIMIT = 50`** recreates TD-121 F1 at scale — oldest facts fall out of
    the detection prompt on graphs > 50 active facts.

**Spec gaps (Phase 3 exit surface):** baseline commit-hash-vs-HEAD refusal (§7), INJ-1/INJ-2
mutation + boundary mutations (§4), fixture variants high-density/single-member-only (§1),
per-iteration flake seed replay (§2), P5 confidence logging (§2), L5 refusal-type assertion +
full before/after graph snapshot (§6), in-proc/subprocess divergence check (§4),
changed-guards-only quick gate (§7), default iteration count 50 vs 20.

---

# Part A — Prototype Core

## A1. `harness/injection_contract.py`

**Summary.** Pre-context injection contract: `apply_injection_contract()` (282–424) takes
candidate facts plus requester/query/resolved-subjects/intent and applies INJ-7 (cross-member
access refusal, checked first and short-circuiting, 335–344), then per-fact INJ-4 household
short-circuit, INJ-5 never-volunteer, INJ-3 cross-member deny, INJ-1 subject scope, INJ-2
keyword relevance with a declarative value-match bypass, and finally INJ-6/INJ-6b empty-set
guards (395–422). Relevance is enumerative regex per attribute (`_ATTR_KEYWORDS`, 57–100). The
module also supplies the two structural refusal strings (429–453) and
`is_declarative_utterance()` (136–145).

**Dead code.**
- `empty_set_refusal()` — `if who == who:` (451) is always true; `who` (450) and the `query`
  parameter (443) are unused; the function reduces to a constant string.
- `_inj2_relevance()` params `intent` and `requester_member_id` (222–223) never used — an
  intent-based relevance path that was never implemented.
- Household re-checks in `_inj5_never_volunteer` (275), `_inj3_cross_member_deny` (255),
  `_inj1_subject_scope` (208) are unreachable: INJ-4 short-circuits every household fact at 348
  first. `attribute == "household"` in `_inj2_relevance` (230) likely dead for the same reason.
- **Live-path dead rule (INJ-3 class):** if retrieval is owner-scoped (per the INJ-7 comment at
  313–315), every fact reaching this function has `owner == requester`, so
  `_inj3_cross_member_deny` returns True at 259 for every fact — INJ-3 can never deny on the
  live path, matching the Layer-3 mutation finding. INJ-1 (368) is near-dead by the same logic.

**Redundant logic.**
- `_inj4_household()` (265–267) is a trivial one-line wrapper, one call site.
- INJ-6b `candidate_hit` (417–420) is effectively redundant live: with owner-scoped retrieval,
  another member's facts never appear in `facts`, and registered-member subjects are intercepted
  by INJ-7 at 335 anyway.
- INJ-7 early return (344) leaves `denied` empty and all audit counters zero — facts silently
  vanish from the audit trail.

**Inconsistencies (keyword drift / TD-120 class).**
- **Opener-list drift:** `_QUESTION_OPENER_RE` (124–133) lists `tell|show|give|list|name|remind`;
  `subject_resolution._IMPERATIVE_DATIVE_STRIP_RE` (42–45) lists
  `tell|show|give|remind|read|get|list|bring`. "Read me Elena's medication" / "Bring me…" are
  not question openers → classified **declarative** → exempt from INJ-7 (336) and both empty-set
  guards (411). Two lists covering the same imperative class have diverged — a direct TD-119
  regression surface, and the single highest-risk drift pair in the codebase.
- **INJ-6b "precise pattern" claim vs actual patterns:** `_TARGETED_ATTRS` (109–112) is
  rationalized (102–108) as precise-only, but `medication` includes bare `take|taking` (67) and
  `dietary` includes bare `eat|foods?` (75). "Does Elena take sugar in her coffee?" marks
  `medication` as asked; a structural refusal can fire on an ordinary turn.
- **`schedule` vs `appointment` overlap** (80–89): near-identical keyword sets; any drift changes
  which attribute matches.
- **PW023 class still open-ended:** `_inj2_relevance` returns False when
  `_ATTR_KEYWORDS.get(attribute) is None` (235–237). Any newly seeded attribute without a pattern
  is undisclosable to its own owner except via the general-personal regex or declarative bypass —
  the PW023-25 failure mode recurs for every future attribute; nothing couples the seed list to
  the keyword map.
- **Docstring vs code:** header says "Six rules" (3) but the file implements INJ-1..INJ-7 + 6b.
- `_declarative_value_match` docstring says "5+ characters" (164) but gates the value at
  `len(value) < 4` (168) — a 4-char value passes the gate yet can never yield a 5-char word; the
  value gate is effectively dead.

**Bugs / fragile spots.**
- **Substring value match (173):** `word in utterance_lower` is not word-bounded; "cardio"
  matches "cardiologist" etc. Should be `\b`-bounded.
- **`is_declarative_utterance` `"?" in t` (143):** any embedded question mark forces question
  classification; "I told you X. Right?" flips the whole turn.
- **INJ-7 subject naming (429–440):** `access_denied_subject` is lowercased (343) then re-cased
  with `.title()`; ids that aren't display names (`bill_b` → "Bill_B") leak raw into user-facing
  text.
- **Fail-open on unknown intent:** an intent outside both `_PERSONAL_INTENTS` (115) and
  `_KNOWLEDGE_INTENTS` (117) passes INJ-5 (277), receives personal facts, and is exempt from
  INJ-6/6b/INJ-7 (397, 410, 337). Unknown intents are treated **more** permissively than
  `personal` — fail-open.
- Declarative-bypass admitted facts are counted only in `inj2_declarative_override`, not
  distinguishable in `injected_fact_ids` for audit.

**Interactions.**
- INJ-3 is confirmed dead live, INJ-1 nearly so, INJ-6b's `candidate_hit` clause dead live. The
  rules doing live work are INJ-7, INJ-4, INJ-5, INJ-2, INJ-6. INJ-3 survives only as
  defense-in-depth against a future retrieval widening — worth stating in the module docstring so
  a mutation run isn't re-flagged as a mystery.
- INJ-7 correctness depends entirely on subject_resolution adding member_ids to `known`
  (subject_resolution 249–250); the declarative-classification drift above is the live bypass.

## A2. `harness/subject_resolution.py`

**Summary.** `resolve_subject()` (187–263) deterministically resolves who a query is about:
Phase 1 first-person regex (after stripping relational possessives and imperative datives)
appends the requester; Phase 2 maps relational terms through relationship facts
(`_resolve_via_relationship_facts`/`_extract_name_from_relationship`); Phase 3 unconditionally
unions capitalized named entities matched against subjects from visible facts plus registered
`member_ids` (the INJ-7 hook). A relational term resolving to nobody with no other signal returns
`[]` (empty-set-safe invariant, 259–260).

**Dead code.**
- `_FIRST_PERSON_RE` (22–26): the alternatives (`i'm|i've|i take|…`) are all subsumed by `i\b`
  — 17 alternatives can never be the deciding match.
- `_extract_name_from_relationship` (117–130): caller lowercases input (104), so the "starts with
  uppercase" check (126) is never true — dead branch; every result comes from the fallback
  (128–129), whose `else None` is also unreachable given `if cleaned:`.
- `_RELATION_TERMS` "husband" entry (68): `spouse` also appears in the "wife" entry (67), checked
  first, so `my spouse` always canonicalizes to "wife".
- `_LEADING_NAME_RE` / `_TRAILING_NAME_RE` (113–114) defined but never used.

**Redundant logic.**
- `_known_subjects` (169–182) re-derives relationship-value names with a `\b[A-Z][a-z]+\b`
  findall on the raw value while `_resolve_via_relationship_facts` extracts the same names via a
  different algorithm on the lowered value — two extraction paths that can disagree.
- Lines 128–129 redundant conditional.

**Inconsistencies.**
- **Docstring:** "Three-phase resolution" followed by five numbered items (6–11).
- **Relational-term drift (TD-120 class):** `_RELATION_TERMS` accepts `gran` (73) / `granddad`
  (74), but `_RELATIONAL_STRIP_RE` (30–35) lists only `grandmother|grandma|grandfather|grandpa`.
  "What does my gran take?" → "my gran" not stripped → `my` fires first-person → requester wrongly
  added as subject.
- **Canonical-term mismatch:** `nurse|doctor` canonicalize to `caregiver` (78), but
  `_resolve_via_relationship_facts` matches by substring `relation_lower in value` (104) — a fact
  "Rosa is my nurse" contains "nurse", not "caregiver", so "my nurse" never resolves. The
  canonicalization defeats its own lookup.
- **Case-sensitivity split:** `_known_subjects` uses an uppercase-anchored regex (180) while
  everything else lowercases; lowercase-stored relationship values are invisible to Phase 3.
- `resolve_subject()` Args docstring (199–204) omits the `member_ids` parameter added for INJ-7.

**Bugs / fragile spots.**
- **Sentence-initial capitalization:** `_extract_named_entities` (152–166) treats any capitalized
  token not in `_COMMON_WORDS` as an entity. Bounded by the Phase 3 intersection with `known`, but
  member names colliding with English words ("Mark the calendar" → member `mark`) are a real
  false-positive surface.
- **Possessive strip only handles `'s`** (161): ASCII apostrophe only; curly `Elena's` works only
  by luck of the token regex splitting.
- **Substring relation match (104):** `"son" in value` matches "Jackson is my grandson" for
  relation `son` — wrong-person resolution risk; should be word-bounded.

**Interactions.**
- **Owner-scoped-retrieval dependency:** `_known_subjects` is built from `visible_facts`, scoped
  to the requester's own facts. A non-member subject is resolvable only if the requester stored
  facts naming them; this confirms INJ-3 and INJ-1's cross-member arms are enforced by retrieval
  scoping, not these modules, on every live path.
- The additive Phase 3 union (247–253) + INJ-7's "any resolved member ≠ requester" loop means a
  self+other query ("Do I take the same meds as Maya?") hard-refuses with Maya's access string even
  though the requester's own half is answerable — documented as intended, but a UX cliff.
- The two imperative keyword lists (dative strip here, question openers in injection_contract)
  enforce one linguistic concept in two files with no shared constant — the highest-risk drift pair.

## A3. `harness/fact_change.py`

**Summary.** Real-time fact-change detection: `detect_and_apply` (552) gates trivially-non-
declarative utterances, re-reads the full active owner+household fact set (572, TD-121 F1),
prompts Groq Llama 4 Scout with a numbered facts block + utterance (597), and applies the returned
`changes` via `_apply_changes` (349) — retracts through `retract_fact`, update/adds through
`memory_engine.store.encode` with a synthetic `WriteDecision(state="supersede", confidence=0.75)`
(490). Public surface: `detect_and_apply`, `detect_and_apply_async` (daemon thread + per-session
Event, 616), `wait_for_detection` (121), `take_detection_outcome` (F3 gate, 158),
`take_session_deltas` (110, only text_demo.py). Includes an idempotency guard, TD-114 same-batch
retract suppression, and null-subject resolution via old-value matching.

**Dead code.**
- `Any` import unused (33). `MULTI_VALUED` import unused (38, referenced only in comments).
- `take_session_deltas` unused on the server path (only caller scripts/text_demo.py:153).

**Redundant logic.**
- **Duplicated gating between caller and callee.** voice_orch.py:2271-2273 re-implements
  `detect_and_apply`'s own gates before calling it; the callee runs them again (559-564). The
  duplicates have drifted (voice_orch uses `_q_words[0].lower()`, fact_change uses
  `.lower().rstrip("?")`, and voice_orch omits `endswith("?")`). "Switched to Jardiance?" can pass
  the Seam A pre-gate, set `_detection_done=True`, then be rejected inside `detect_and_apply` →
  `take_detection_outcome` returns None for a turn voice_orch believes ran detection.
- **Two back-to-back reads of the same active rows** — `_active_values` (462) and
  `_snapshot_prior_fact` (481) each query the identical key. One query could serve both.
- `updated_attrs` includes non-canonical attributes (368-374, built before the skip at 382).
- `_CONF_ORDER`/`_classify_trust` are acknowledged duplicates of `truth_layer.queries` (46-48,
  186-197), justified by a circular-import constraint but with no equivalence test — drift risk on
  comment discipline alone.

**Inconsistencies.**
- **`_QUESTION_WORDS` (53) vs `_SUPERSEDE_PHRASE_RE` (voice_orch.py:2115-2118) asymmetry.** The F3
  gate only fires on the supersede-phrase regex. A phrase-free declarative ("My medication is
  Jardiance now") runs detection, stores an outcome, but the outcome is never popped (only popped
  inside the regex-gated branch, voice_orch.py:2130). TD-119's phrase-invariant goal is half met:
  recall is phrase-invariant, but the unlanded-write protection is not; the stale outcome leaks
  into a later turn.
- `CANONICAL_ATTRIBUTES` (extraction_queue.py:124) is the write vocabulary; injection_contract's
  `_ATTR_KEYWORDS` is keyed by the same names with no mechanical link — a new canonical attribute
  becomes writable while INJ-2 silently treats it as non-relevant.
- **Retract subject-scoping default differs from update's.** Retract falls back to
  `effective_owner` without attempting `_resolve_subject_by_old_value` (411), while updates do
  (443). "Ray no longer takes metformin" with a null subject retracts the *speaker's* row.

**Bugs / fragile spots.**
- **Event race in `_get_or_create_event`/`wait_for_detection`.** `_get_or_create_event` calls
  `ev.clear()` on a shared per-session event (106); overlapping cycles can erase a completed
  cycle's signal → waiter blocks the full 12 s. `wait_for_detection` pops the event (133) even
  when a newer in-flight detection uses that object.
- **Cross-turn outcome bleed.** Four call sites fire `detect_and_apply_async` with no matching
  `wait_for_detection`/`take_detection_outcome` (voice_orch.py:1508, 2351, 2445, 2551). A straggler
  thread from turn N can `_store_outcome` after turn N+1's synchronous detection stored its
  outcome, so the F3 gate judges N+1's ack against N's result.
- **Outcome never stored if `_apply_changes` raises.** Only `encode` is wrapped (497-513). An
  exception from `retract_fact`/`log_fact_lifecycle_event`, or a malformed change dict (Groq
  returns a list of strings → `change.get` raises at 376) escapes, kills the worker after
  `ev.set()`, and skips `_store_outcome`. The F3 gate then sees `outcome is None` and **passes the
  ack through** (voice_orch.py:2131-2132) — the exact "ack asserts an unlanded write" case F3
  exists to block.
- **No shape validation of Groq JSON** (603): tolerates missing/None but not wrong types.
- **`owner_name=None` at voice_orch.py:1512** → `_USER_TEMPLATE.format(name=None)` → "Current facts
  for None:".
- **Idempotency guard fails open:** `_active_values` returns `[]` on any driver/decrypt failure
  (260-262), letting a duplicate self-supersede through — deserves an explicit log tying the
  failure to guard bypass.
- **`_DETECTION_FACTS_LIMIT = 50`** recreates TD-121 F1 at scale: `read_user_facts` orders
  `timestamp DESC LIMIT $limit`, so on >50 active facts the oldest drop out and Groq flips to
  `changes: []` for them — now with a comment asserting it can't happen (55-57).
- **`utterance=""` passed to encode** (507): provenance/utterance field is empty for every fact
  written through this path.

**Bitemporal / append-only model.**
- No hard deletes (confirmed); closure via `valid_to` is the sanctioned mechanism.
- **Retract produces closure with no successor node** (extraction_queue.py:560-563): the only
  record is mutated properties on the closed node + the lifecycle log. Retraction is the one state
  change recorded purely by in-place property writes — worth an explicit design sign-off.
- **Valid-time only, no transaction-time.** `ts = _now_iso()` (477) serves both when-true and
  when-known; "Ray switched last month" is written valid-from=now. If "bitemporal" is a live claim,
  this write path is effectively mono-temporal.

## A4. `server/voice_orch.py`

**Summary.** Phase-2 orchestrator-driven voice server (port 7862): wires a pipecat pipeline whose
brain is `OrchestratorGate._on_user_text` (1262) — per-turn config hot-reload, speaker
verification/session segmentation, enrollment, control flow (RECONSIDER/FRONTIER), temporal
short-circuits, tiered routing, telemetry, session-end fact extraction. A second, pipeline-free
entry point, `process_text_query` (2142), serves typed demo/harness turns and additionally carries
Seam A synchronous write detection, the INJ-1..7 injection contract, the TD-121 F3 gate, and
per-turn metadata logging. `bot()` (2562) is the pipecat runner entry; `voice_https_orch.py`
imports `bot` and `process_text_query`.

**Dead code.**
- `INFER_MODEL` (135) defined, never referenced. `TIER_EDGE` import (113) never used.
- `HOT_NAME`, `HOT_PREFS` (389, 391) defined, never read; the "demo hot-cache" comment (388) is
  stale — the path is a no-op (`_NoopStore.hot_context`, 625).
- `_Turn.decision`/`_Turn.user_text` (742-743) written at 1532-1533, never read.
- `_NoopStore.set_hot_cache`/`a_add` (628, 631) have no callers left after TD-035.
- Five inline `from openai import AsyncOpenAI` (1617, 1683, 1791, 2463, 2481).

**Redundant logic / voice-vs-text divergence (the big one).** The two paths share the
decide→route→generate skeleton but have drifted materially:

| Concern | `_on_user_text` (voice) | `process_text_query` (text) |
|---|---|---|
| Injection contract (INJ-1..7) | **absent** — facts straight into prompt (1736) | applied (2295) |
| Seam A sync write + re-read | **absent** — fire-and-forget only (1508) | sync, 12 s wait + re-retrieve (2272-2285) |
| TD-121 F3 gate | **absent** | applied (2517) |
| Turn metadata logging | **never logged** | every routed turn (2535) |
| Escalate non-temporal grounding | web-grounded (1576-1651) | skipped except temporal (2417) — documented |
| Local model temp | 0.3 (1992) | 0.0 (TD-119, 2491) |
| Owner name for detection | `None` (1512) | registry-resolved (2277) |
| Empty-set / access-control refusals | model free-generates | structural strings |

Net: everything the harness measures (contract refusals, F3, metadata) is true only of the typed
path. The live voice path can leak cross-member facts (no INJ-7), ack unlanded writes (no F3), and
produces no turn metadata. Either extract the guards into a shared per-turn function both paths
call, or the docs must state the voice path is unhardened.

Smaller duplications that will drift: control-flow blocks (1432-1500 vs 2175-2232); local-now
short-circuit (1417-1430 vs 2163-2173); temporal city-clock fallback (1663-1676 vs 2420-2428);
`_bloom_map` literal three times (2307, 2331, 2534); repeated `detect_and_apply_async` exit-path
calls with different `facts` arguments (2349/2443/2549 — fragile ordering dependency); Groq call
block (1769-1832 vs 2459-2477).

**Cross-module inconsistencies.**
- **Supersede detection asymmetry:** `_SUPERSEDE_PHRASE_RE` (2115-2118) exists only here;
  `fact_change.detect_and_apply` gates on word count / question shape and lets Groq detect any
  change. "Ray takes Jardiance now" can land a write without the F3 gate ever inspecting the
  outcome (silently returns raw reply at 2128).
- **Redundant alternation in the regex** (2116): `not any ?more|any ?more` — second branch
  subsumes first; bare `any ?more` over-triggers on "do you want any more details".
- **Refusal-string fingerprints vs harness** (eval/harnesslib/server.py:22-25):
  `ACCESS_CONTROL_RE = "I can only share it with"` matches injection_contract.py:438 but **not**
  the no-subject fallback at :440 ("That's someone else's private information — I can't share
  it.") → classifies as `"none"`, and `EMPTY_SET_RE` misses it too. A real F-4 refusal invisible
  to the harness.
- `UNCONFIRMED_UPDATE_REPLY` (2120-2123) matches neither harness regex.
- `EMPTY_SET_RE` over-match: `escalation_placeholder()` "I don't have that information yet."
  (orchestrator.py:422) matches it, so escalation placeholders are indistinguishable from
  structural INJ-6 refusals.
- **Question-opener regexes diverge three ways:** voice_orch.py:485-489 (no tell/show/give/…),
  injection_contract.py:124-133 (includes them), fact_change `_QUESTION_WORDS` (53, six wh-words).

**Bugs / fragile spots.**
- **Global mutable state:** `_TRACE_FILE_CACHE` (248) grows unboundedly. `_text_query_router`
  (2085) is built with a frozen config (`load_routing_config()` once, 2093) — typed queries never
  see config.yaml edits, unlike the voice path's per-turn `_hot_reload` (1062).
- **Text-query session entries never removed** (`session_id=f"text-{member}"`, 2158): no
  session-end, control_state accumulates forever; two concurrent typed turns for the same member
  share the id and `take_detection_outcome` pops non-atomically → outcome theft.
- **Exception swallowing that hides 500 causes:** `_flush_utterance` demotes all `_on_user_text`
  exceptions to a warning + local answer (1174-1178); the final local fallback returns "Sorry, I
  couldn't process that." (2497-2499) so the HTTP caller can't distinguish infra failure from a
  model reply — harness failures show as content regressions, not errors. Bare `except: pass` in
  verification loops (713, 1340).
- **`self._ctx._messages` private-attribute surgery** throughout (1046, 1252-1254, 1274, 1292,
  1757, 1811) — a pipecat rename breaks ~8 sites silently inside try blocks.
- **`datetime.utcnow()`** (213, 323, 359) deprecated naive-UTC, mixed with tz-aware
  `datetime.now(timezone.utc)` at 2314.
- **New `AsyncOpenAI` client per call**, never closed — leaks httpx resources under load.
- Guest-upgrade writes the trigger utterance into the session before verification (1386) →
  fact-pipeline pollution.

**Module-level side effects (import cost).**
- **Model warmup HTTP POST at import** (179-190): a synchronous `requests.post` to Ollama with
  `timeout=60` runs the moment `voice_orch` is imported. `voice_https_orch.py:27` imports
  `process_text_query`, so every harness subprocess pays this on startup — up to 60 s if Ollama is
  cold, and it pointlessly loads the voice model for pure-text harness use. Recommend moving warmup
  into `bot()`/an explicit `warmup()` gated on `HIP_SKIP_WARMUP`.

---

# Part B — Verification Harness (`eval/`)

## B1. `eval/harness.py`

**Summary.** Single CLI entry. Enforces machine guards (dev marker, port 7688, GROQ key),
resolves run mode (quick/full/pre-demo/single-layer/all) into a layer set + per-invariant
iteration counts, boots a subprocess `HarnessServer` for L1/L2/L4/L5 (and `--record-expected`),
runs L3 afterward on an in-process server, prints summary, writes results, appends trend, applies
the baseline ratchet for the exit code.

**Dead code.** `p1_n/p2_n/p3_n/p5_n` assigned in the `--quick` branch but unused (108).
`run_p4(..., 0)` and `run_p6(..., 0)` pass an ignored iterations arg (166, 170).

**Redundant logic.** The three non-quick branches (111-132) differ only in the layer set and two
constants; a table would remove the triplication.

**Inconsistencies.** Help says "Layer 1 iterations per invariant" (77) but a single
`--iterations N` overrides P1/P2/P3/P5 identically, contradicting the per-mode defaults. Docstring
(24) says exit "1 regression / 2 new failure" but `apply_baseline` also returns 1 for "no
baseline" and refused `--update-baseline`.

**Bugs / fragile spots.** `--record-expected` returns 0 with no summary/results file and ignores
`run_layers` (150-154); `--quick --record-expected` silently records rather than gating. No
validation of `--port` against `INPROC_PORT` (7997 vs 7998 collision).

**Gaps vs spec.** No baseline commit-hash-vs-HEAD refusal (§7). `--quick` runs all three guards
unconditionally, not "changed guards only" (§7). Default 20 iterations vs spec §2's 50. Nightly
mode unimplemented.

## B2. `harnesslib/fixture.py`

**Summary.** Fixture manager: hard-coded mirror of `scripts/demo_seed.py` D1–D9 (`SEED_FACTS`,
`LEAK_NEEDLES`), `reset()` (stdout-suppressed demo_reset/demo_seed), `verify_seed()` drift check,
`assert_fact_state()`/`active_count()` graph assertions, `_key_facts()` decrypt. Exposes
`get_driver()`.

**Redundant logic.** `_key_facts` decrypt loop (144-159) is duplicated in layer1.py:372-387
(`_all_rows`) and 390-407 (`_value_active`) — three copies. layer1.run_p6 (448) and
layer5._read_owned_value (179) reach into private `fixture._key_facts` instead of a public
accessor.

**Inconsistencies.** `assert_fact_state` param order (112) differs from the spec signature;
`expected_write_state` not implemented, replaced by `expect_active`.

**Bugs / fragile spots.**
- **`verify_seed` can pass on decryption failure** (105-106): decrypt throws → `value=None` →
  `got=""`, and `"" in sf.value.lower()` is always True. Garbage ciphertext passes drift
  verification. Require non-empty `got`.
- Decrypt exceptions swallowed to `None` with no note (155-158). `redirect_stdout` hides a
  partially-failed seed that doesn't raise (83).

**Gaps vs spec.** Fixture variants `high-density` and `single-member-only` are `NotImplementedError`
(91); only `standard` and `empty` exist, and `empty` is unused. No cross-scenario state tracking
(§1).

## B3. `harnesslib/reporter.py`

**Summary.** `Scenario` (check/flake/skip) + `Reporter`: per-layer summary, JSON results,
append-only trend with git commit, baseline ratchet (`apply_baseline`) with exit codes 0/1/2 and
`_known_flaky`/`_accepted` sidecars.

**Redundant logic.** Identical by-layer grouping loop in `print_summary` (65-67) and
`append_trend` (100-102).

**Inconsistencies.** Baseline filename `harness_baseline.json` (20) vs spec §7 `baseline.json`.
FLAKE counts in "npass" (69) and passes the ratchet (137) while the docstring/print say "NOT
green" (79) — a permanently flaky scenario is green for exit-code purposes; spec §2 says flakes
are not green. Exit code contradicts the printout.

**Bugs / fragile spots.**
- **Partial-run `--update-baseline` destroys the baseline** (137-160): `actuals` holds only this
  run's scenarios; `out = dict(sorted(actuals.items()))` writes only those. `--layer 2
  --update-baseline` drops every other layer's entry, so later failures report exit-2 "brand new"
  instead of exit-1 regressions. Update must merge into the existing baseline. **This is the
  mechanism behind the b01c3fd collapse.**
- Corrupt baseline JSON swallowed → misleading "NO BASELINE" inviting an overwrite (126-128).
- `--accept` stamps the justification onto **every** currently-failing scenario, not a named one
  (156-157).

**Gaps vs spec.** Baseline commit-hash refusal absent (§7). Flake diffs vs baseline not reported
(§1).

## B4. `harnesslib/server.py`

**Summary.** Subprocess server lifecycle (`server.voice_https_orch` on 7997, log to
`harness_server.log`, readiness poll on `/api/members`, terminate/kill teardown) + the harness-wide
refusal classifier (`classify_refusal`, ACCESS_CONTROL before EMPTY_SET). `post_turn` raises
enriched `HTTPError`s.

**Redundant logic.** `post_turn`/`members`/`_wait_ready` re-implemented in inproc.py:60-85 with
different behavior.

**Inconsistencies.** `TURN_TIMEOUT_S = 120.0` (19) vs inproc.py:77 hard-coded `120.0` — not
shared. `_wait_ready(timeout=120.0)` (68) vs inproc.py:60 `60.0`, poll 1.0 s vs 0.5 s. server
`post_turn` extracts error detail; inproc `post_turn` just `raise_for_status()` — L3 loses the
detail L2 gets.

**Bugs / fragile spots.**
- `log_fh = open(SERVER_LOG, "w")` (50) never closed — parent handle leaks for the whole run.
- Refusal regexes (22-25) are single-point string couplings to the server's exact wording;
  `EMPTY_SET_RE` is broad (`"not have"` matches "do not have permission"), `ACCESS_CONTROL_RE` is
  one exact phrase. Any copy edit flips L1/L2/L3/L4 classifications; no test asserts the server
  still emits these verbatim.

## B5. `harnesslib/inproc.py`

**Summary.** L3 support: `InProcServer` runs uvicorn in a daemon thread on 7998 against the same
app object (plain HTTP); `mutate_guard(guard, mode)` monkeypatches INJ-3 (module attr swap) or
wraps `apply_injection_contract` for INJ-7/INJ-6b disable/overtrigger, always reverting.

**Dead code.** `InProcServer.members()` (81-85) never called.

**Bugs / fragile spots.**
- `_wait_ready` (60-71) has no liveness check: if the uvicorn thread dies (port bound), it spins
  the full 60 s. Should check `self._thread.is_alive()` (HarnessServer checks `proc.poll()`).
- `__exit__` joins with `timeout=10` and ignores a failed join (54-58); a wedged thread persists,
  colliding on the port for a second in-process run.
- `_wrap_contract` hard-codes the real contract's full signature (95-97); a new parameter crashes
  **only under mutation** (L3). Use `*args, **kwargs`.
- Imports private `_PERSONAL_INTENTS` and re-implements the INJ-6 firing condition (118-121); any
  change to INJ-6's real condition desyncs the INJ-6b disable mutation.

**Gaps vs spec.** Only INJ-3/6b/7 mutable (`_GUARDS`, 90) — INJ-1/INJ-2 have no mutation coverage
(§4). Boundary mutation (§4 step 3) entirely unbuilt. No in-proc/subprocess divergence check (§4).

## B6. `harnesslib/layer1.py`

**Summary.** Governance invariants P1–P6 (see per-invariant behavior in the module). Shared
polling/decrypt helpers at the bottom.

**Dead code.** `iterations` param unused in `run_p4`/`run_p6` (270, 438); `seed` unused in
`run_p6` (439). `_P5_SWITCH_TEMPLATES["allergy"]` unreachable — run_p5 hard-codes `attr="medication"`
(316). `_wait_detection_settle`'s `expect_at_most` effectively fixed at 1; return value unused
(361-369).

**Redundant logic.** `_all_rows`/`_value_active` (372-407) duplicate `_key_facts`.
`_DETECTION_CEILING_S = 20.0` defined in layer1 (40) and layer4 (26), hard-coded inline in
layer2.py:162; layer5 uses 4.0. Three bespoke poll loops (layer1 165-178, layer4 95-104, layer2
162-170).

**Bugs / fragile spots.**
- **`_last_meta` ignores which line is new** (539-553): checks `len(lines) <= before` then returns
  `lines[-1]`. If the async pipeline writes two entries, the wrong turn's `injected_fact_ids` are
  asserted — P6's core mechanism. Return `lines[before]` or match on a turn id.
- P1 flake path discards the first failing reply (the actual evidence, 99).
- P2 convoluted retry control flow (184-195); can't distinguish "passed on retry" from "value
  present but empty-refusal classified".
- P2 never resets between iterations (158-163); context carryover can satisfy `answered>=1` from a
  prior iteration's value rather than graph retrieval.
- P5 idempotency check waits up to 8 s for a violation; a duplicate landing at 10-20 s (within the
  stated ceiling) passes falsely (243).

**Gaps vs spec.** No per-iteration seed replay (§2). P1 only probes existing facts — the not-exists
cross-member case lives only in P4's static cells (§2). P3 never inspects write_state, only active
count (§2). P5 has no confidence assertion/logging (§2). P4 requires the regex to match, rejecting
"a natural 'I don't know'" the spec allows (§2). Default 50 vs 20.

## B7. `harnesslib/layer2.py`

**Summary.** Demo regression: per script, verify paired expected file exists + SHA-256 matches,
reset, fire each turn, sleep `pause_ms`, assert required/forbidden needles + refusal type + tier,
optionally poll a graph assertion (≤20 s), apply `_known_flaky`. `record()` writes review-gated
skeletons.

**Redundant logic.** Needle/refusal block (126-139) duplicates layer4 `_assert_row` semantics.
Poll loop (162-170) is the third copy.

**Inconsistencies.** Turn-id fallback `f"turn{index}"` (86) vs real `T01` ids; `record()` has no
fallback (186) — an unnamed turn records under `null` which run()'s fallback never finds.
Hash-mismatch/missing-expected failures use sid `sc_name` (70, 77) while per-turn results use
`sc_name.tid` — a script flapping between states churns baseline keys.

**Bugs / fragile spots.** `list.index(turn)` (86) returns the first equal turn — two identical
unnamed turns collide on one id. `turn["text"]`/`turn["member"]` KeyErrors are caught by the
`post_turn` handler (104) and misreported as "HTTP error". `pause_ms + 20 s` per turn has no budget
guard for the <60 s quick-gate promise.

**Gaps vs spec.** No epistemic-timeline/display assertion (§3); "or no change" negative assertion
only via `active: false`, not "nothing was written".

## B8. `harnesslib/layer3.py`

**Summary.** Guard-integrity mutation for INJ-7/INJ-6b/INJ-3: pin unmutated baseline on a blocked
and an allowed probe, assert the behavioral delta under disable/overtrigger; INJ-3's no-op under
disable is emitted as an explicit `[FINDING]`. One reset, question-only probes, in-process server.

**Dead code.** `_turn` returns `routing` discarded by `_inj7`/`_inj3` (`text, _ =`); only `_inj6b`
uses it (45-48).

**Redundant logic.** The three `_injX` functions share a pin/mutate/assert skeleton; a driver over
a probe table would remove the triplication and make INJ-1/2 cheap.

**Inconsistencies.** No retry/flake handling at all — a single nondeterministic reply reds the
whole guard scenario, yet L3 is in the pre-commit quick gate: the most flake-exposed layer with the
least tolerance.

**Gaps vs spec.** INJ-1/INJ-2 untested; boundary mutation absent. The intentional INJ-3 inversion
(no-leak + FINDING vs the spec's `assert "lisinopril" in result.text`) is well-reasoned but an
undocumented deviation from the spec text — amend the spec or cross-reference.

## B9. `harnesslib/layer4.py`

**Summary.** Consumes `pairwise_matrix.json`: after one reset, run read-only rows (one retry →
FLAKE), group graph-mutating rows by setup utterance, fire each write once, poll ≤20 s, assert each
row via `_assert_row`, all inside a single `L4:pairwise` scenario.

**Redundant logic.** `_foreign_needles` recomputed per call (29-34). Throwaway `Scenario("_","_","_")`
probe (79-81) hacks around `check()` mutating state.

**Inconsistencies.** Read-only rows get one retry (76); mutating-group rows get none (109-112) — the
rows most exposed to async timing have the least tolerance. Skipped rows become `[SKIP-ROW]` notes
(70), invisible to reporter skip counts and the baseline.

**Bugs / fragile spots.**
- **One Scenario for the whole matrix** (63): baseline key `L4:pairwise` — one row regression and
  fifty are indistinguishable to the ratchet, one known-bad row poisons the signal for all others.
  Rows have stable `PW###` ids and should each be a scenario (spec §7).
- Flake note reuses `probe.notes[-1]` as the label (84) → double-bracketed garbled output.
- Landed-check uses `grp[0]` subject/attribute for the whole group (98-100); correct only because
  utterances are attribute-unique — an unasserted invariant.
- Mutating groups can perturb later reads (89-112); safe today only by accident of matrix content
  (the Ray metformin→empagliflozin supersede at gen_pairwise.py:124 changes D9).

**Gaps vs spec.** Resets once for the layer, relying on read-before-write ordering; no fixture
isolation between mutating groups (§5). `pronoun` and `mixed` dimension values absent (§5).

## B10. `harnesslib/layer5.py`

**Summary.** Curated red-team A1–A5 as a static `_Attack` table. Each fires as the attacker and
asserts no forbidden cross-member needles in the reply; A5 sleeps 4 s and asserts Maya's medication
fact still contains "lisinopril".

**Dead code.** `_clean_maya_med` (138) is captured "as a baseline to compare against" but only
interpolated into a failure string (167); no comparison is ever made — the cascade-detection
rationale is not implemented.

**Redundant logic.** `_MAYA_PERSONAL`/`_SAM_PERSONAL` (43-44) hand-duplicate LEAK_NEEDLES +
is_member_personal. `_read_owned_value` (176-183) is another `_key_facts` reach-in.

**Inconsistencies.** `_A5_SETTLE_S = 4.0` (128) vs the 20 s ceiling everywhere else — an async
corrupting write landing between 4 s and 20 s passes A5 falsely. Poll to the same ceiling
(inverted: poll for corruption, assert none by deadline). No retry/flake handling.

**Bugs / fragile spots.**
- A5 graph check inspects only (maya, maya, medication) (159-167). A5.3 ("Delete all of Maya's
  health records") could delete D1 appointment and the check still passes. Spec §6 assertion 4
  requires a full before/after snapshot diff.
- Forbidden-needle string match is the only reply assertion (153-156); A4 (inferential leakage) is
  the category where verbatim needles are least likely to appear — A4 scenarios are nearly
  assertion-free as written.

**Gaps vs spec.** §6 assertion 5 (refusal-type correctness) — `classify_refusal` never called.
§6 seeding mentions "Sam has penicillin allergy" — no such seed exists (A4.1's penicillin probe has
no ground truth). A5.4 softened from "change it to X" to "needs to be corrected" — weaker than
specified.

## B11. `eval/gen_pairwise.py`

**Summary.** Generates `pairwise_matrix.json`: defines the five dimensions, prunes invalid combos
via `_valid` (documented exclusions), runs a greedy all-pairs cover, `_concretize`s each abstract
row into asker/subject/query/setup/expected, marks `retracted-this-session` as runtime-skips.

**Dead code.** `dims = [...]` (172) assigned, never used. The by-relation exists-and-owned
`_NONMEM_OWNED` lookup path (114) is unreachable given `_valid`'s exclusions.

**Redundant logic.** `_SELF_OWNED`/`_NONMEM_OWNED` (36-41) re-mirror `fixture.SEED_FACTS` by hand —
a third copy of seed ground truth. Could import from fixture (no heavy import-time deps).

**Inconsistencies.** Plural query builder (139-143) has a stray space before `}` in the medication
template only → `"What medications does Maya  take?"` double spaces, asserted verbatim against an
LLM path. `_meta.excluded` (206-208) says retracted rows are runtime-SKIPped without the
cross-member carve-out that actually runs them.

**Bugs / fragile spots.** The non-member just-written setup ("Ray switched from metformin to
empagliflozin", 124) supersedes seeded D9 — a hidden ordering dependency the generator neither
documents nor guards (layer4 read-first ordering saves it today). `id=f"PW{i:03d}"` over
`sorted(chosen)` (194) renumbers every row when a dimension value is added, churning any per-row
baseline keys.

**Gaps vs spec.** No test asserting "every achievable pair covered" post-generation (the loop can
`break` with `uncovered` non-empty and nothing fails). "(non-member, any) → defined behavior (TBD
per registry design)" is hard-committed to empty_set/no_leak without a spec amendment.

---

## Recommended sequencing (not scope for this review — for planning)

1. **Fix before next `--update-baseline` on any machine:** reporter.py:151 merge-not-replace;
   fixture.py:106 non-empty `got`; layer1.py:552 correct metadata line. These three undermine the
   harness's own trustworthiness.
2. **Governance correctness:** injection_contract fail-open on unknown intent; fact_change F3
   fails-open on `_apply_changes` raise + cross-turn outcome bleed; the no-subject access-control
   refusal string the harness can't classify.
3. **Decide the voice-path question:** extract a shared per-turn guard function, or explicitly
   document the voice path as unhardened. Today the harness green light does not cover it.
4. **Drift consolidation:** one imperative-keyword constant shared by injection_contract and
   subject_resolution; one seed-ground-truth source; one decrypt-rows helper; one detection
   ceiling; one refusal-fingerprint contract test.
5. **Spec-gap backlog:** baseline commit-hash check, INJ-1/2 + boundary mutations, L5 refusal-type
   + full snapshot, per-row L4 scenarios, fixture variants, per-iteration seed replay.
