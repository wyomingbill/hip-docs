# REQ_PROMPT_SUBSET_ADMITTED: Layer-7 Prompt/Record Fidelity
Status: SUPERSEDED BY REQ_PROMPT_RECORD_FIDELITY

**SUPERSEDED 2026-07-27 by REQ_PROMPT_RECORD_FIDELITY__factid-set-parity-prompt-vs-admitted__v20260726_1717.md — the two docs describe one requirement and 1717 carries the concrete, code-traced acceptance test operationalizing this one. Retained here for history, not a live REQ — do not build against this file; build against REQ_PROMPT_RECORD_FIDELITY.**

Branch: roadmap
Reconciled-Against: 6d1abab (docs-only filing, no code touched this session); REQ_G0_OUTPUT_INVARIANT__output-side-fabrication-backstop__v20260726_0735.md (MET — the ABSOLUTE-tier auto-wired-into-run() pattern this REQ copies); REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827.md (MET — the four-part standard items 3-6 of this REQ's acceptance test are drawn from); HIP_ContextArch_Reconciliation__master-plan-diff__v20260726_0710.md STEP 4 (why this REQ exists)

## THE REQUIREMENT

Bill's own words, verbatim:

> Every fact-bearing string that reaches the model in the assembled prompt
> must correspond to an entry in that turn's record.admitted[]. The prompt is
> a subset of what the record says was admitted. Nothing verifies this today:
> every harness assertion in the system asserts against the record, and the
> record is a self-report the prompt is not checked against.

Expanded: today's entire harness verifies the RECORD (resolved_subjects,
admitted[], the G0/G1-G4 invariants, INJ-1..7 discrepancy checks) — all of it
trusts that the assembled prompt handed to the model contains exactly, and
only, what the record claims was admitted. No mechanism reads the actual
prompt string and checks it against admitted[]. A bug that leaks an
unadmitted fact into the prompt (a stale cache, a wrong merge, a Seam-A
splitting error) would be invisible to every existing check, because every
existing check is downstream of the record, not the prompt.

## THE ACCEPTANCE TEST

Pass/fail, per item. Any single failure is FAIL; no partial credit.

1. A layer-7 check, ABSOLUTE tier, hard zero, `--accept` mechanically
   refused via the `layer7_crypto_v2.py` mechanism, wired unconditionally
   into `eval/harnesslib/layer7_crypto.py` `run()` the way G0 is (auto-run
   on every `--layer 7` / `--full`, no hand-run step).
2. The check compares the assembled prompt against `record.admitted[]` for
   every generation turn in the run and fails on any fact-bearing content in
   the prompt with no corresponding admitted entry. Observable: run
   `--layer 7`, see the check execute and report PASS/FAIL per turn.
3. FAULT-INJECTION TWIN: a probe that inserts an unadmitted fact into the
   assembled prompt turns the check red on command, and removing the
   injection turns it green. Both directions must hold or the metric FAILs.
4. GROUND-TRUTH FIXTURE: alice/bob/mary, human-verified expected admitted
   sets — the oracle for what SHOULD be in the prompt is a verified fixture,
   not a model's own self-report.
5. COVERAGE ENTRY: the check declares which slice of the state space it
   covers (which turn types, which admission paths), registered the same
   way `check_registry.py` already tracks every other check's four-part
   declaration.
6. METAMORPHIC WRAPPER: meaning-preserving rewordings of the query do not
   change the check's decision (same pattern as MT1/MT2).
7. RATCHET PASS on `--full` before and after, with any pre-existing
   failures named as pre-existing (Requirements Discipline item 12 — a
   targeted proof alone is not done).

## WHAT'S ALREADY DONE (do not redo)

- **G0 is built and MET** (runtime gate `44e3626`, harness invariant
  `44ff3d3`) and is the wiring pattern to copy: an ABSOLUTE-tier `Scenario`
  inside `eval/harnesslib/layer7_crypto.py`'s `run()`, auto-run on every
  `--layer 7`/`--full`, `--accept` mechanically refused via the same
  `reporter.py` `absolute_new_failures` gate G0 and the ABSOLUTE-tier
  `layer7_crypto_v2.py` bullets already use. Reuse this mechanism; do not
  build a second wiring path.
- **REQ_HARNESS_DISCIPLINE is MET** and its four-part standard — (1)
  fault-injection twin, (2) ground-truth fixture, (3) coverage entry, (4)
  metamorphic wrapper — is exactly where acceptance items 3-6 above come
  from. Do not invent a different quality bar; this REQ's check is required
  to clear the same standard every other reference-implementation check
  clears.
- **`admitted[]` is already computed per turn** and carried in the d1.1
  record (`epistemic_record.py:134`, sourced from
  `injection_result.allowed`). The record side of the comparison already
  exists; this REQ does not touch how `admitted[]` is populated.

## WHAT'S KNOWN BROKEN

- **There is no prompt-side instrumentation today.** The prompt is
  assembled downstream of the record (the Seam A split, `voice_orch.py:
  2405-2418`) from what is effectively a local copy of the admitted facts.
  Nothing reads that assembled prompt string back and diffs it against
  `record.admitted[]`.
- **Every harness assertion in the system today asserts against the
  record, never the prompt.** This means a class of bug — an unadmitted
  fact leaking into the actual model-facing prompt through a stale cache,
  a bad merge, or a Seam-A splitting error — is structurally invisible to
  every check that exists right now, including G0/G1-G4. This REQ closes
  that blind spot; it does not claim the blind spot is already closed by
  any existing mechanism.
- **Voice conversation history is NOT covered, and cannot be by this REQ's
  own per-turn mechanism.** Verified against current `server/voice_orch.py`
  this session (not carried over from an older trace): `_on_user_text` (the
  voice/realtime path) rebuilds `_ctx_snapshot` from `self._ctx._messages[1:]`
  at `:1976-1979`, then appends the current turn's raw query/reply text back
  onto that same list at `:2010-2011`. A fact disclosed in turn N reappears
  in turn N+5's prompt through this history list as plain assistant text,
  with no `fact_id` attached — it was flattened into prose long before turn
  N+5's own contract ran, and is outside turn N+5's own `admitted[]` or
  `prompt_fact_ids` entirely. A per-turn set comparison cannot see this by
  construction, not by bug. Closing it needs a session-level ledger of which
  fact_ids have ever been disclosed into history — its own REQ, not v1 of
  this one (v1 covers the per-turn `local_system_prompt` render on the text
  path only). This is the SAME function TD-131/BILL-7 implicates:
  `strip_context_for_tier`, called immediately after the history rebuild at
  `:1986-1988` (verified today; an earlier note on a different checkout
  cited a different line, and `docs/BACKLOG.md:77` cites line 3240 from an
  older trace — line numbers drift, this is what is true now) — TD-131/
  BILL-7 is about what that call strips (household facts reaching the
  outbound MID/CORE payload unfiltered); this gap is about what reaches the
  call already un-tagged (conversation history with no fact_id). Two
  distinct gaps sharing one call site. TD-131/BILL-7 is not resolved by this
  note and no code here is changed.

  **CITATION REPAIR, 2026-07-27 (DISPATCH 35, `HIP_RegisterReconciliation__cross-branch-id-collisions__v20260727_1930.md`):**
  the `docs/BACKLOG.md:77` / `TD-131`/`BILL-7` references two paragraphs
  above are dangling on `roadmap` and were never resolvable here — `roadmap`
  has no `BILL-7` row in `docs/BACKLOG.md` at all (main's `BILL-7` sits at
  its own line 77; roadmap's line 77 is blank, one row short), and
  `roadmap`'s own `TD-131` (`docs/techdebt/LATEST_DEBT.md`) is an unrelated
  git-worktree-checkout finding, not the Groq-payload one this bullet meant.
  Stated plainly instead of by broken ID: this bullet was pointing at
  **main branch's TD-131** (filed 2026-07-22, commit `4390240`) — the
  finding that `strip_context_for_tier` never fires for MID/CORE tiers, so
  household-shared facts reach Groq's payload unfiltered on those tiers.
  Per the reconciliation plan, main's TD-131 is slated to become
  **TD-136** on `roadmap` — not yet ported as of this note (that porting is
  phase 2, not done here). Until it lands, the correct present-day pointer
  for "household facts reaching Groq's MID/CORE payload unfiltered" is
  **`D-28`** (`HIP_DefectRegister`), the roadmap-native finding of the same
  class, located independently and NOT FIXED as filed (a fix for its
  specific triggering shape has since landed under
  `REQ_STRIP_CONTEXT_COMPLETENESS`; TD-131/TD-136's own broader MID/CORE
  question is explicitly out of that REQ's scope and remains open). This
  bullet's own gap (voice history carrying an un-tagged fact) is unaffected
  by any of this and remains open and separate.
- **`hot_context` carries no `fact_id` on either path, and is neutralized
  outright on text.** `_NoopStore.hot_context` (`server/voice_orch.py:
  710-711`) returns `[]` unconditionally — the text path's hot-cache section
  never renders anything, so `local_system_prompt`'s `rendered_fact_ids`
  correctly reports nothing for it. The voice/live-store path's own
  `hot_context` (`harness/zep_store.py`) is live and returns real strings,
  but even there they are pre-formatted prose (name, household members,
  preferences), never fact dicts — there is no `fact_id` to report on
  either path structurally, not a gap this REQ's mechanism could close by
  extension.

## CONSTRAINTS

- Do not change any existing check's pass/fail behavior.
- Do not touch the demo on main or graph 7689.
- Layer 7, AUDIT, and full RATCHET stay green — before and after, per
  Requirements Discipline item 12.
- Hard zero, never `--accept`-able, matching G0/G1/G4's own never-baseline
  set (REQ_CONFIDENCE_DISCIPLINE Phase G taxonomy) — a build that ships this
  check behind a flag or an acceptable baseline has not built this REQ.
- No new model calls in the check itself: it is a deterministic string/set
  comparison between the assembled prompt and `record.admitted[]`.

## WHY THIS REQ EXISTS

It is precondition (ii) of three for the context-architecture learned
ranker, per `HIP_ContextArch_Reconciliation` STEP 4. G0 is precondition (i)
and is MET. Precondition (iii) — learner/training-signal isolation — has no
REQ filed yet.
