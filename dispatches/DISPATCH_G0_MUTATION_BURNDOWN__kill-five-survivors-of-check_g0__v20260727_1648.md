# DISPATCH_G0_MUTATION_BURNDOWN
Status: BUILT
Reconciled-Against: see HASH below (same commit as this doc)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827.md`
(MET; this dispatch follows its standard — ground-truth, non-model-graded
test cases, on the harness's own least-tested code — while extending, not
starting, the mutation-score infrastructure `REQ_COVERAGE_MEASUREMENT`
built at `eval/harnesslib/mutation_score.py` / `mutation_targets.py`,
Metric 2, `DISPATCH_COVERAGE_MEASUREMENT_M2` 2026-07-26. That REQ scoped
the metric itself and explicitly deferred burn-down ("not attempted in
this build"); this dispatch is the first burn-down slice against the
`TD-134` baseline it opened, scoped to one target: `harness/g0_invariant.py:
check_g0` — G0 is a MET, ABSOLUTE-tier, hard-zero invariant, and its own
checker (`check_g0`) was the least-tested code in the harness at 3/8
(0.38) killed.)

## THE ASK

> Kill check_g0's five surviving mutants.
>
> harness/g0_invariant.py check_g0 scores 0.38 on mutation, 3 of 8 killed,
> five surviving delete_last_operand mutants. G0 is a MET, ABSOLUTE-tier,
> hard-zero invariant and its own checker is the least-tested code in the
> harness.
>
> For each survivor: identify the conditional clause the mutant deletes,
> write a test case that fails when that clause is removed and passes
> when it is present, and confirm the mutant dies.
>
> Do not change check_g0's behavior. If a survivor cannot be killed
> without changing behavior, that is a finding: report it, name the
> clause, and leave it.
>
> Follow REQ_HARNESS_DISCIPLINE on anything new you add. Re-run the
> mutation scorer and report check_g0's new score plus the overall
> figure. Report each survivor as killed, or unkillable with the reason.
> Checkpoint commit, push, report the hash.
>
> [Environment/scope preamble, same session: Layer 7 only, no --full. Do
> not reset or reseed any graph. Do not touch any master key. Do not mark
> any REQ MET.]

## WHAT WAS DONE

1. Enumerated `check_g0`'s 8 mutation sites via
   `eval/harnesslib/mutation_score.count_mutation_sites` /
   `generate_mutant` directly (not through the full sweep) to identify
   exactly which AST node each survivor's index corresponds to:
   `harness/g0_invariant.py:65` (`delete_last_operand(And)`), `:67`/`:68`/
   `:74`/`:75` (all `delete_last_operand(Or)`). Confirmed against
   `logs/mutation_survivors.jsonl`'s last persisted run (2026-07-27T21:44,
   TD-134's own baseline) — exact match, same 5 survivors by file:line +
   operator.
2. For each survivor, generated the mutant object directly and ran it
   under `mutation_score.patched()` against hand-constructed inputs to
   confirm, empirically (not just by reading the AST), whether ANY input
   distinguishes the mutant from the original — before writing a single
   killer.
3. Added 4 new killer probes to `eval/harnesslib/mutation_targets.py`
   (`harness.g0_invariant: check_g0` section) and wired them into that
   target's `TargetSpec.killers` tuple. `harness/g0_invariant.py` itself
   was NOT touched — every kill is a new test case, not a behavior change,
   per the ask's explicit constraint.
4. Verified all 7 killers (3 original + 4 new) return `None` (no
   false-kill) against the real, unmutated `check_g0` — i.e. each new
   test "passes when the clause is present," not just "fails when it's
   removed."
5. Re-ran the full mutation sweep across all 12 `TargetSpec`s (not just
   `check_g0`) to confirm the other 11 targets' survivor counts were
   byte-for-byte unchanged — this was purely additive to one target.
6. Updated `TD-134` (the no-silent-disappearance baseline) in a new
   `docs/techdebt/DEBT_REGISTER__v20260727_1648.md`, per that entry's own
   stated protocol ("burning down an individual survivor means removing
   ONLY that survivor's own file:line/operator line ... not this entry's
   structure"): removed the 4 now-killed lines from the `check_g0`
   segment of the BASELINE listing, annotated the remaining `:67` line as
   a confirmed equivalent mutant, and appended a dated UPDATE paragraph
   with the killer names, the reasoning for the one non-kill, and the
   score deltas. `LATEST_DEBT.md` repointed; `docs/INDEX.md`'s techdebt
   row and `Last updated` stamp updated in the same pass.
7. Ran `scripts/run_harness.sh --layer 7` (the guarded wrapper — refuses
   off-repo, sources `.env.dev`/`~/.zshrc`/the demo-dashboard plist for
   `GROQ_API_KEY`, checks `neo4j-dev` is up without reseeding it) per the
   session's explicit scope: Layer 7 only, no `--full`, no graph
   reset/reseed, no master-key file touched, no REQ marked MET.

## WHAT WAS FOUND

Per-survivor disposition, each identifying the exact clause the mutant
deletes:

1. **`harness/g0_invariant.py:65`, `delete_last_operand(And)` — KILLED.**
   Deletes the `and admitted_facts` clause from `if resolved_subjects and
   admitted_facts: return None`, leaving bare `if resolved_subjects:`.
   The module's own docstring (lines 62-64) states line 65's guard must
   cover BOTH halves of an OR — "empty" and "non-empty-but-mismatched"
   upstream state — but all 3 pre-existing killers only ever set
   `resolved_subjects`/`admitted_facts` to the SAME truthiness (both
   empty, or both populated); none constructed the mismatched half. New
   killer `_kill_g0_resolved_without_admitted_fires`:
   `resolved_subjects=["ray"]`, `admitted_facts=[]`, reply naming "ray" —
   original correctly fires a violation (resolved but nothing admitted);
   mutant short-circuits on `resolved_subjects` alone and wrongly returns
   `None`. Confirmed dead: `harness/g0_invariant.py:65` no longer in the
   sweep's survivor list.
2. **`harness/g0_invariant.py:67`, `delete_last_operand(Or)` — NOT
   KILLED. Confirmed equivalent mutant, not a coverage gap.** Deletes the
   `or ""` fallback from `find_named_tracked_persons(reply or "",
   known_subject_ids)`, leaving bare `reply`. Investigated empirically
   (`reply=None`, `reply=""`, and normal truthy strings, run against both
   the original and the mutant) before concluding: every falsy `reply`
   (only `None`/`""` are possible for a `str | None`-typed input — no
   other falsy `str` exists) is caught identically by
   `find_named_tracked_persons`'s OWN `if not reply: return []` guard
   (`harness/g0_invariant.py:46`) whether it receives `reply` or `reply or
   ""`; every truthy `reply` short-circuits `or` to the same value
   either way. No input to `check_g0` observably distinguishes the
   mutant from the original — this is a true equivalent mutant per the
   DeMillo/Lipton/Sayward taxonomy the engine's own docstring cites, not
   an untested clause. Killing it would require changing `check_g0`'s or
   `find_named_tracked_persons`'s behavior, which both the ask and the
   session's scope explicitly forbid. Left surviving, by design.
3. **`harness/g0_invariant.py:68`, `delete_last_operand(Or)` — KILLED.**
   Deletes the `or ""` fallback from `self_id = (member or
   "").strip().lower()`, leaving `member.strip().lower()`. No prior
   killer ever passed `member=None` (a legitimate input per the `member:
   str | None` signature) — only string members ("bill"/"maya"). New
   killer `_kill_g0_none_member_no_crash`: `member=None`, reply naming a
   tracked other person — original handles it gracefully (`self_id=""`,
   violation still fires correctly); mutant calls `.strip()` directly on
   `None` and raises `AttributeError` before `named_others` is even
   computed. The exception propagates out of the killer call itself,
   which `mutation_score.run_target`'s own design treats as a kill ("a
   mutant that makes the killer ITSELF raise ... counts as killed").
4. **`harness/g0_invariant.py:74`, `delete_last_operand(Or)` — KILLED.**
   Deletes the `or []` fallback from `list(resolved_subjects or [])`
   inside the violation-string f-string, leaving `list(resolved_subjects)`
   — raises `TypeError: 'NoneType' object is not iterable` when
   `resolved_subjects=None` specifically (as opposed to merely `[]`, which
   behaves identically either way and so cannot distinguish the mutant).
   New killer `_kill_g0_none_resolved_subjects_no_crash` supplies
   `resolved_subjects=None` on a call that reaches the violation-string
   return path.
5. **`harness/g0_invariant.py:75`, `delete_last_operand(Or)` — KILLED.**
   Sibling of #4: deletes `or []` from `len(admitted_facts or [])`,
   raising `TypeError: object of type 'NoneType' has no len()` on
   `admitted_facts=None` reaching the same return path. New killer
   `_kill_g0_none_admitted_facts_no_crash`.

**Score:** `harness.g0_invariant.check_g0` 3/8 (0.38) -> **7/8 (0.88)**.
Overall mutation score across all 12 targets: 78/128 (0.61) -> **82/128
(0.64)**. All other 11 targets' survivor counts unchanged — verified by a
full re-run of `run_sweep(TARGETS)`, diffed line-for-line against the
pre-change report.

**Unrelated observation, out of scope:** the `--layer 7` run printed 16
caught-and-skipped `cryptography.fernet.InvalidToken` tracebacks
("decrypt failed for attribute=preference owner=bill; skipping") from
`harness/extraction_queue.py:read_user_facts`, all BEFORE the Layer 7
section even starts (during earlier-layer/coverage-grid setup). Not
touched by this change (nothing here imports encryption code), not new
(same shape recurs identically 16 times against one owner/attribute pair,
consistent with a pre-existing stale-key-version row rather than
something this session introduced), and RATCHET PASS confirms nothing
regressed vs baseline. Named here, not investigated further — out of
this dispatch's scope.

## VERIFIED

- **Watched run:** every per-survivor claim above was watched, not
  reasoned about from the AST alone — each mutant was generated directly
  via `generate_mutant`, applied via `patched()`, and called with the
  described inputs against BOTH the original and mutant function objects,
  with the printed return value/exception captured (script output showed
  `orig=...` / `mut=...` / `KILLS: True|False` for every case, including
  the negative controls for #2 that established equivalence rather than
  assuming it). All 7 killers were then also run directly against the
  real unmutated module and confirmed to return `None` (no false
  positives).
- **Watched run:** the full `run_sweep(TARGETS)` re-run (all 12 targets,
  128 mutants) — output matched the harness's own live `--layer 7`
  MUTATION-SCORE scenario output exactly (82/128 overall, check_g0 7/8,
  every other target's survivor list identical to the pre-change
  baseline).
- **Watched run:** `scripts/run_harness.sh --layer 7` (log:
  `/tmp/hip_harness_20260727_1650.log`) — `AUDIT: 6/6`, `L7: 24/24`,
  `L7V2: 27/28` (1 opt-in skip, unchanged — the live-model
  `CT-OUTPUT-GAP` check), `SCHEMA: 1/1`, `VOICE: 1/1`,
  `MUTATION-SCORE PASS` (82/128, 0.64), `MUTATION-NO-SILENT-DISAPPEARANCE
  PASS` ("4 disappearance(s) this run, all accounted for" — the 4 newly
  killed g0 survivors, matched against this run's own killed-mutant set,
  no debt-register carry needed for those 4), `MUTATION-NO-SILENT-
  DISAPPEARANCE-SELFTEST PASS`, `RATCHET PASS — no scenario regressed vs
  baseline`. No graph reset/reseed invoked (the wrapper only starts
  `neo4j-dev` if the port isn't already listening — it was), no
  master-key file touched (`OB5`/`OB6` in the same run confirm its
  continued absence, read-only), no REQ marked MET by this dispatch.
- **Reasoned about:** the equivalence argument for survivor #2 (line 67)
  is a closed-form argument over `find_named_tracked_persons`'s full
  input space (only two falsy `str` values exist, and truthy values
  short-circuit identically) rather than an exhaustive enumeration —
  the empirical checks above sampled the argument's key cases (`None`,
  `""`, a truthy string) rather than proving it by exhaustion, which
  isn't meaningful over an infinite string domain.

## HASH

See commit — this dispatch doc, `eval/harnesslib/mutation_targets.py`,
`docs/techdebt/DEBT_REGISTER__v20260727_1648.md` (+ `LATEST_DEBT.md`
repoint), and `docs/INDEX.md` all ship together.

## OPEN

- TD-134's remaining 46 survivors (all outside `check_g0`) are untouched
  — this dispatch was scoped to the one named target. The BASELINE
  listing's PATTERN note (`delete_last_operand` on a multi-clause
  `and`/`or`, the existing killers never construct the "drop only the
  LAST clause" case) generalizes directly to `_inj2_relevance`,
  `write_rule.classify`, and `record_invariants` — the same burn-down
  shape applies there, not attempted here.
- `check_g0` itself was intentionally left unmodified throughout — its
  behavior is unchanged, only its test coverage grew. No new REQ was
  needed for this: it's incremental strengthening of the already-`MET`
  `REQ_COVERAGE_MEASUREMENT` Metric 2 infrastructure, not a new check on
  the `harness_audit` roster.
