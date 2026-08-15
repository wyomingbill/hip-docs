# REQ_PROMPT_RECORD_FIDELITY: Fact-ID Set Parity Between the Assembled Prompt and record.admitted[]
Status: MET
Branch: roadmap
Reconciled-Against: 20c0063 (REQ_PROMPT_SUBSET_ADMITTED filed, docs only, no code
touched); REQ_PROMPT_SUBSET_ADMITTED__layer7-prompt-record-fidelity__v20260726_1617.md
(the scoping REQ this doc operationalizes with a concrete, code-traced acceptance test);
79aa95a (docs-only session that assessed this REQ against code, narrowed items 4-6 per
Bill's 2026-07-27 decision, and re-ran the harness — no application code touched by
either the assessment or this update); `/tmp/l7_recheck.log` (this session's re-run)

## UPDATE 2026-07-27 — MET

Assessed item-by-item against current code and a live `--layer 7` run
(evidence below). Items 4-6 as originally drafted described bidirectional
set parity; the built check (`harness/prompt_fidelity_invariant.check_psa1`)
only ever implemented the subset direction. Bill's ruling (see AMENDMENT
under THE ACCEPTANCE TEST below): narrow items 4-6 to the subset invariant
actually built; do not build the reverse direction. With that amendment,
all seven items are MET.

**ACCEPTANCE — all seven, evidence:**

1. MET. `orchestrator.py:393-394` (recent-context block) and `:445-447`
   (confirmed-facts-about-other-people block) both `rendered_fact_ids.extend(...)`
   the fact_ids they rendered, collected from the dicts already in hand —
   never parsed from the formatted string. (A third block, "Things you
   know," is instrumented too at `:421-423`, exceeding this item.)
2. MET. `harness/epistemic_record.py:173` (`prompt_fact_ids` param) →
   `:251` (`"prompt_fact_ids": list(prompt_fact_ids or [])`) — a pure
   passthrough, no regex, no string scanning.
3. MET. `assemble_governed_context` sets `telemetry["prompt_fact_ids"]`
   (`voice_orch.py:2588-2599`) from the exact `local_system_prompt` call
   that produces `sys`; `sys` becomes `messages[0]["content"]` at
   `voice_orch.py:3235` (the true last assembly site, drifted from the
   REQ's original `:3224` citation by doc growth, not a functional change);
   the real generation-path `emit_epistemic_record` (`reply_source="model"`,
   `:3417-3430`) reads `prompt_fact_ids` from that same dict.
4. MET (as amended). `harness/prompt_fidelity_invariant.py:35-45`:
   `check_psa1` computes `leaked = prompt_ids - admitted_ids` and fails
   naming the offending fact_id(s) when non-empty — exactly the amended
   subset invariant.
5. MET. `layer7_crypto.py:1301-1311` — exact-equal case, `[ok]` in
   `/tmp/l7_recheck.log:418`. The proper-subset case also passes
   (`:1313-1327`, `/tmp/l7_recheck.log:419`), consistent with the amended
   item 5.
6. MET (as amended). `layer7_crypto.py:1395-1427` — the real
   `local_system_prompt` fault-injection twin: red on an injected
   `other_subject_facts` leak (`/tmp/l7_recheck.log:422`), green on removal
   (`:423`), naming the exact fact_id both times.
7. MET. `/tmp/l7_recheck.log:580` — `RATCHET PASS — no scenario regressed
   vs baseline.` `== L7: 24/24`, `== AUDIT: 3/3`, `== L7V2: 25/26 (1 skipped,
   opt-in, unrelated)`.

**Harness-discipline four-part, on PSA1 by name** (not just AUDIT 3/3
aggregate) — `eval.harnesslib.harness_audit.run()`, `L7:PSA1` row:
`coverage: ok`, `fixture: ok`, `metamorphic: ok` (`psa1_rewordings`, 27 red +
9 green rewording variants, all correct), `twin: ok`. All four artifacts
verified present, not merely declared.

**The four named gaps in WHAT'S KNOWN BROKEN — voice conversation history,
the `known_facts` bypass (D-27), `hot_context`, and PSA1's synthetic-vs-live
assembly path — are STATED LIMITS OF SCOPE, not unmet acceptance items.**
None of the seven acceptance items above claims to cover any of the four; each
gap is named precisely so a later reader does not mistake a structural
non-goal for open work on this REQ. The reverse-direction (completeness)
question raised by narrowing items 4-6 is filed as `docs/BACKLOG.md` row 50 /
`REQ_PROMPT_COMPLETENESS` (proposed), not decided here.

## THE REQUIREMENT

Bill's own words, verbatim (from today's read-only trace):

> The epistemic record's admitted[] is built from injection_result.allowed
> (epistemic_record.py:184). The prompt is built from a SEPARATELY REBUILT
> local admitted variable (voice_orch.py:2550, 2569-2578) that filters out
> other_subject_facts and, on declarative turns, replaces dicts with
> modified copies. These are two distinct objects by the time each reaches
> its destination. The record therefore attests what the contract allowed,
> not what the model was shown.
>
> 1. local_system_prompt (harness/orchestrator.py:363-375, 408-420) returns
>    the list of fact_ids it actually rendered. The dicts still carry
>    fact_id at render time; it is discarded only at string formatting
>    (orchestrator.py:368, :412).
> 2. A new record field, record.prompt_fact_ids, populated from that return
>    value. Never by parsing prose.
> 3. The check compares record.prompt_fact_ids against record.admitted's
>    fact_ids as SETS. ID equality, not string matching.
> 4. Capture point is the true last assembly site per path:
>    voice_orch.py:3224 for text.

Expanded: today, `_fact_entry` (`epistemic_record.py:75-102`) already stores
`fact_id` (never the value, per the TD-030 comment at `:24-25`/`:76`) —
`record.admitted[]` is ID-bearing. The gap is on the OTHER side: nothing
records which fact_ids actually made it into the string handed to the model.
The fix is to make the prompt side ID-bearing too, at the one point in the
code (`local_system_prompt`) where the fact dict still carries `fact_id`
before formatting drops it, and compare two ID sets — not a string diff
against prose.

## THE ACCEPTANCE TEST

Pass/fail, per item. Any single failure is FAIL; no partial credit.

**AMENDMENT 2026-07-27 (Bill's decision, narrowing items 4-6):** as originally
drafted, items 4 and 6 below described BIDIRECTIONAL set parity — a mismatch
in either direction (a rendered fact_id missing from `admitted`, OR an
admitted fact_id never rendered) was written as a FAIL. The built check
(`harness/prompt_fidelity_invariant.check_psa1`) only ever implemented ONE
direction — `prompt_fact_ids ⊆ admitted_fact_ids` — and an assessment this
session found the two out of step: item 4 as originally written was NOT MET,
and item 6's negative case was NOT MET both on the bidirectional question and
because the actual fault-injection twin (`layer7_crypto.py:1395-1427`)
constructs its leak via a synthetic direct call to
`harness.orchestrator.TurnOrchestrator.local_system_prompt`, not via
`voice_orch.py`'s real declarative-turn rebuild. Bill's ruling: narrow the
acceptance test to the subset invariant that was actually built, do not build
the reverse direction. Reasons, in Bill's words: a record-only fact_id
(admitted but never rendered) is under-disclosure, not a leak — a different
failure class from the one this REQ exists to catch — and enforcing equality
would false-positive on ordinary `max_facts` truncation or the attribute/
value render guard dropping a legitimate entry. Items 4-6 below are rewritten
accordingly; the REQ's title ("Fact-ID Set Parity") and Bill's original
"ID equality, not string matching" quote both survive unedited above — they
were always about comparing by ID rather than by prose, not about requiring
set equality. The reverse direction is filed separately, not decided here:
see WHAT'S KNOWN BROKEN gap 4 and `docs/BACKLOG.md`'s `REQ_PROMPT_COMPLETENESS`
(proposed).

1. `local_system_prompt` (`harness/orchestrator.py:363-375` "Recent context
   about this person", and `:408-420` "Confirmed facts about other people")
   returns (or the caller collects, via the dicts it already receives) the
   list of `fact_id`s actually rendered into those two blocks — not
   reconstructed by parsing the formatted string.
2. `harness/epistemic_record.py` gains a new field, `record.prompt_fact_ids`
   (a set of fact_ids), populated ONLY from that returned/collected list —
   never derived by regexing or scanning the assembled prompt text.
3. The capture point on the text path is the true last assembly site,
   `server/voice_orch.py:3224` (`messages = [...]`, immediately before the
   Groq/Ollama call) — i.e. `prompt_fact_ids` reflects what
   `local_system_prompt` rendered into the SAME `admitted`/
   `other_subject_facts` inputs that produced the string assembled at that
   line, not an earlier or later snapshot.
4. A layer-7 check compares `record.prompt_fact_ids` against
   `record.admitted`'s fact_ids AS SETS (ID/set membership, not
   substring/string matching), and asserts the SUBSET invariant:
   `prompt_fact_ids ⊆ admitted_fact_ids`. Only a PROMPT-ONLY fact_id — one
   present in `prompt_fact_ids` with no corresponding entry in `admitted` —
   is a FAIL, printed by that exact fact_id, not by prose diff. An admitted
   fact_id that was never rendered is NOT, by itself, a failure of this
   check (see AMENDMENT above and WHAT'S KNOWN BROKEN gap 4).
5. POSITIVE CASE (must pass): a turn where the contract admits N facts, all
   N are rendered by `local_system_prompt` into the prompt, with no
   prompt-only fact_id present. `prompt_fact_ids == admitted_fact_ids`.
   PASS. (A proper subset — fewer fact_ids rendered than admitted, e.g. from
   `max_facts` truncation or the attribute/value render guard — is ALSO a
   legitimate PASS under the subset invariant; it is not treated as a
   distinct required case here because it is the ordinary, unremarkable
   shape of the invariant, not an edge case.)
6. NEGATIVE CASE (must fail): a turn where an `other_subject_facts` entry
   renders into the prompt with a fact_id that has no corresponding entry in
   `admitted`/`injection_result.allowed` — the prompt-only leak this check
   exists to catch. The check FAILS on that turn, naming the specific
   fact_id. This is the case the fault-injection twin
   (`layer7_crypto.py:1395-1427`) actually constructs, via a direct
   `local_system_prompt(..., other_subject_facts=[...])` call — see WHAT'S
   KNOWN BROKEN gap 4 for the honest limit of what code path that twin
   exercises.
7. Full RATCHET green before and after wiring — `--full` (not a hand-picked
   subset), any pre-existing failure named as pre-existing, per
   Requirements Discipline item 12.

## WHAT'S ALREADY DONE (do not redo)

- **`record.admitted[]` is already fact_id-bearing.** `_fact_entry`
  (`harness/epistemic_record.py:75-102`) stores `fact_id`/`attribute`/
  `owner`/`subject`/`confidence`/`level` — never the value (TD-030, comment
  at `:24-25`/`:76`). `admitted = [_fact_entry(f) for f in
  injection_result.allowed]` at `epistemic_record.py:184` is confirmed by
  direct code read this session, not inferred from docs.
- **The fact dicts carry `fact_id` all the way to render time.** The dicts
  passed into `local_system_prompt` still have `fact_id` on them when they
  reach `orchestrator.py:368` and `:412` — it is discarded only by the
  `f"{attribute}: {value}"`-style format string at those two lines, not
  earlier. No new plumbing is needed to GET the id to the render site; it
  is already there and thrown away one line too late.
- **The two assembly points are already identified** (this session's
  trace): text path `server/voice_orch.py:3224`; voice/realtime path primed
  at `voice_orch.py:1956-1957`, snapshotted at `:1976-1979`, sent at
  `:1998-2000` (local/Ollama tier returns at `:2059` with no further
  explicit assembly call in this codebase — see EXPLICIT NON-GOAL below).
  This REQ's acceptance test (item 3) targets the text path's
  `voice_orch.py:3224` only, per Bill's own item 4 above.
- **G0's wiring pattern** (ABSOLUTE tier, unconditional in
  `eval/harnesslib/layer7_crypto.py run()`, `--accept` mechanically
  refused) is the mechanism to copy for the layer-7 check in acceptance
  item 4, per REQ_PROMPT_SUBSET_ADMITTED's own WHAT'S ALREADY DONE section.

## WHAT'S KNOWN BROKEN

- **The record and the prompt are built from two distinct objects today.**
  `record.admitted[]` traces to `injection_result.allowed`
  (`epistemic_record.py:184`, passed through as telemetry from
  `voice_orch.py:2548`). The prompt is built from a locally rebuilt
  `admitted` variable (`voice_orch.py:2550, 2569-2578`) that filters out
  `other_subject_facts` and, on declarative turns, replaces dicts with
  value-rewritten copies. By the time each reaches its destination they are
  not the same object and are not asserted equal anywhere. The record
  attests what the contract allowed, not what the model was shown.
- **No fact-id capture exists on the prompt side at all.** Confirmed by
  code read: `local_system_prompt`'s two fact-rendering blocks
  (`orchestrator.py:363-375`, `:408-420`) format straight to a string and
  return nothing about which fact_ids were used.
- **The `known_facts` bypass is a second render path, currently
  neutralized, not removed.** `orchestrator.py:376-402` ("Things you know
  about this person") renders facts independent of the injection contract
  entirely when `known_facts` is non-empty. The text path currently
  suppresses this by always passing `known_facts=[]`
  (`voice_orch.py:2589`). If `known_facts` is ever populated again on any
  path, this REQ's check must cover that render site too — it is a KNOWN,
  NAMED gap in this REQ's coverage as scoped today, not a hidden one.
- **`hot_context` is a fourth fact-bearing render site with no
  `rendered_fact_ids` instrumentation at all — PSA1 covers 3 of 4.**
  `local_system_prompt` renders `hot = self.store.hot_context()`
  (`orchestrator.py:344`) into the "Always-true context" block
  (`orchestrator.py:374-375`) with no `rendered_fact_ids.extend(...)` call
  alongside the three that exist at `orchestrator.py:393-394` (recent
  context), `:421-423` (things you know), and `:445-447` (confirmed facts
  about other people). Verified this session against current code, not
  assumed: `server/voice_orch.py` contains exactly one `store =`
  assignment in the entire file (`:2218`, `store = _NoopStore()`), and
  every `TurnOrchestrator(...)` construction in that file passes either
  that `store` (`:2226-2228`, the realtime pipeline's own orchestrator,
  used only for `.decide()`/routing) or a freshly-constructed
  `_NoopStore()` inline (`:2500-2501` inside `assemble_governed_context`,
  `:2963` inside `process_text_query`) — never a live `ZepStore`.
  `_NoopStore.hot_context()` (`voice_orch.py:710-711`) returns `[]`
  unconditionally. Per the BUILD-1 comment at `voice_orch.py:1707-1711`,
  the voice/realtime path's own governed-prompt assembly now routes
  through the SAME `assemble_governed_context()` the text path calls
  (`voice_orch.py:1722` vs `:3054`), which builds its own `_NoopStore()`
  internally (`:2500-2501`) — so hot_context is inert (renders nothing)
  on BOTH paths as currently wired, not text-only. This corrects
  REQ_PROMPT_SUBSET_ADMITTED's own retained note (that section's
  "voice/live-store path... is live" framing predates this session's
  verification and does not hold against current code). `ZepStore`'s own
  `hot_context()` (`harness/zep_store.py:386-394`) is not a hard no-op —
  it emits real prose from `self._hot` — but it is unreachable in
  production regardless: its populator, `set_hot_cache()`
  (`zep_store.py:375-384`), has exactly one call site repo-wide
  (`voice/test_schema.py:93`, a test), and no production code ever
  constructs a `TurnOrchestrator` with a `ZepStore` instance. Moot
  structurally either way: `ZepStore.hot_context()` returns `list[str]`
  pre-formatted prose (name, household members, preferences), never fact
  dicts — there is no `fact_id` to capture on either implementation. Not
  instrumented by this REQ; recorded here as a known, named gap.
- **PSA1's fault-injection twin is proven against a synthetic assembly
  path, not the live one.** The twin (`eval/harnesslib/layer7_crypto.py:
  1395-1427`) constructs its own `TurnOrchestrator` directly from
  `harness.orchestrator` and calls `local_system_prompt(...,
  other_subject_facts=[{"fact_id": "PSA1-INJECTED-LEAK", ...}])` by hand.
  It never calls `server/voice_orch.py`'s `assemble_governed_context` or
  exercises the real declarative-turn admitted-rebuild (`voice_orch.py:
  2551-2579`, current lines) at all. This proves `check_psa1` correctly
  catches a prompt-only leak WHEN one is constructed, and that the
  wiring described in acceptance item 3 is correct by direct code read
  (verified this session — `assemble_governed_context`'s own
  `telemetry["prompt_fact_ids"]` assignment at `voice_orch.py:2588-2599`
  feeds the same `_ctx_meta` dict the real `emit_epistemic_record` call
  reads at `:3417-3430`) — but no test exercises that real production
  code path end to end through PSA1 itself. A regression introduced
  inside `assemble_governed_context` or the declarative-turn rebuild
  specifically (as opposed to inside `local_system_prompt`) would not be
  caught by this twin. Not fixed by this REQ; recorded as a known, named
  gap in what the twin actually proves.

## CONSTRAINTS

- Do not change any existing check's pass/fail behavior.
- Do not touch the demo on main or graph 7689.
- Layer 7, AUDIT, and full RATCHET stay green — before and after.
- The check is a deterministic set comparison over fact_ids. No new model
  calls, no prose parsing, no regex-against-the-rendered-string — the
  entire point is to stop relying on string matching.
- Hard zero, matching G0/G1/G4/REQ_PROMPT_SUBSET_ADMITTED's own
  never-`--accept`-able set — a build that ships this behind a flag or an
  acceptable baseline has not built this REQ.

## EXPLICIT NON-GOAL

This REQ does NOT cover conversation history on the voice/realtime path
(`voice_orch.py:1976-2011`). A fact disclosed in turn N reappears in turn
N+5's prompt via `self._ctx._messages` as plain assistant text with no
`fact_id` attached — it was flattened into prose long before that later
turn's contract ran, and outside that turn's `admitted[]` entirely.
Instrumenting only the per-turn `local_system_prompt` call (this REQ's
whole scope) misses this completely: a check built to this REQ will report
GREEN on turn N+5 while its prompt still carries a fact disclosed five
turns earlier, because that fact was never in turn N+5's own
`record.admitted[]` or `record.prompt_fact_ids` to begin with — the
mismatch is invisible to a per-turn set comparison by construction, not by
bug. Closing that gap needs a session-level disclosure ledger tracking
which fact_ids have ever been rendered into history, independent of this
REQ's per-turn mechanism, and its own REQ. A BACKLOG entry pointing at this
REQ is filed alongside it (see `docs/BACKLOG.md`, "THE ORDERED BACKLOG" row
37b and "MISSING REQ DOCS", `REQ_VOICE_HISTORY_DISCLOSURE_LEDGER`).

## WHY THIS REQ EXISTS

It operationalizes REQ_PROMPT_SUBSET_ADMITTED (filed 2026-07-26, this REQ's
scoping parent) with a concrete, code-traced acceptance test: the exact
fields, file:lines, and set-comparison mechanism found by tracing the real
text-query generation path this session, rather than a general statement
that the prompt should be a subset of the record. REQ_PROMPT_SUBSET_ADMITTED
remains the broader precondition-(ii)-of-three framing for the
context-architecture learned ranker (HIP_ContextArch_Reconciliation STEP 4);
this REQ is the buildable slice of it.
