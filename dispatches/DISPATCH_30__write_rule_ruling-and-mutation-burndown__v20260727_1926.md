# DISPATCH_30
Status: BUILT
Reconciled-Against: see HASH below (same commit as this doc)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_COVERAGE_MEASUREMENT__coverage-metric-and-mutation-score__v20260726_1224.md`
and `docs/requirements/REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md`
(both edited in place, per instruction — corrections and an explicit
narrow-vs-widen rule, not new scope); extends the already-MET mutation-score
infrastructure (REQ_COVERAGE_MEASUREMENT Metric 2) with a `write_rule.classify`
burn-down slice, same shape as the prior `check_g0` and TD-133 ITEM-5 slices.

## THE ASK

> RULING on the discrepancy the coverage-grid work found: the REQ's
> illustrative example is wrong, the code is right. Do NOT change
> write_rule.classify().
>
> The reasoning, to be written into the REQ: a directive that NARROWS
> scope, such as a household-attribute fact directed to the care team, is
> safe and permitted. The constraint that matters is on WIDENING, and it
> is already ratified. Level-2 author widening to household-shared is
> allowed only for facts about the author or generic household facts.
> Widening a fact about another person beyond its level-3 default
> requires that person's standing policy. The mandatory subject-is-
> caregiver rule stays a hard non-overridable constraint.
>
> 1. Correct the illustrative example in REQ_COVERAGE_MEASUREMENT. Add a
>    dated note recording what it previously said and why it was wrong;
>    do not silently rewrite it.
> 2. Add the narrow-versus-widen rule explicitly to REQ_PARTITION_CUSTODY,
>    stated as above. If it is already there in substance, cite the line
>    rather than duplicating it.
> 3. Re-derive the coverage grid's validity map against the corrected
>    understanding and report whether the valid-cell count changes from
>    2170.
> 4. Run the write_rule.py mutation burn-down. Kill as many survivors as
>    you can with new tests only; do not change classify() behavior. Any
>    survivor that cannot be killed without a behavior change is a
>    finding: name the clause and leave it.
>
> Report the new write_rule score and the overall figure. Layer 7 green,
> RATCHET PASS. Do not touch docs/INDEX.md or MANIFEST.md; another
> session may hold those. Commit, push, report the hash. Do not mark any
> REQ MET.

## WHAT WAS DONE

**Item 1.** Found the illustrative example at
`REQ_COVERAGE_MEASUREMENT__coverage-metric-and-mutation-score__v20260726_1224.md:47`
("e.g. a care-team scope on a household attribute") — already flagged as
disputed by a prior session's own build notes further down the same file
("FLAGGED, not silently reconciled... does NOT hold against the real
classifier"), but never corrected at its source location, and no ruling
had been recorded. Corrected the parenthetical in place to name the
ACTUAL invalid combination (pair-private + household/coordination
attributes, matching the validity derivation's own empirical finding),
with an inline pointer to a new dated note. Appended a **RULING
2026-07-27** paragraph immediately after the existing FLAGGED paragraph:
preserves the original wrong text verbatim, states why it was wrong
(conflated narrowing with widening), and cites `REQ_PARTITION_CUSTODY:95-96`
for the actual ratified constraint. Original FLAGGED paragraph left
untouched — this is a resolution appended to it, not a rewrite.

**Item 2.** Read `REQ_PARTITION_CUSTODY` in full. Found the "Household-circle
widening restriction" sentence at line 95 already states the widening
half of Bill's ruling near-verbatim — ratified 2026-07-21, six days before
this dispatch: "an author may use a level-2 directive to widen to
household-circle-shared only for facts about the author themself or
generic household facts; widening a fact whose subject is another person
requires that person's standing policy (level 1)". The mandatory
subject-exclusion rule at line 96 ("a HARD, non-overridable constraint")
is the generalized form of the "mandatory subject-is-caregiver rule" (the
2026-07-21 role-separation widening, per line 118's own note). Cited both,
did not duplicate. What was genuinely missing: an explicit statement that
NARROWING is unrestricted — grepped the file for "narrow", found only an
unrelated usage (line 120, a different "narrow" describing a residual
risk) and one about sensitivity (line 124, level 4, not level 2). Added
one new sentence immediately after the existing widening-restriction
sentence, dated 2026-07-27, making the asymmetry explicit and naming this
dispatch as its source.

**Item 3.** Read `eval/harnesslib/coverage_grid.py` in full. Its own module
docstring already recorded the SAME discrepancy and the SAME correct rule
(`is_valid_cell`: invalid iff `scope == CLASS_DYAD and (attribute ==
"household" or attribute in COORDINATION_ATTRIBUTES)`) — the code was
never wrong; only the REQ's prose illustrative example was. Re-derived
live: `valid_cells()`/`invalid_cells()` re-run against the current
codebase, fresh, not read from a comment. Also independently re-verified
the underlying `classify()` behavior the validity map depends on — see
VERIFIED below for what was live-checked vs. reasoned from source, since
the `care_team_keys` roster is currently empty in this dev graph (no
`care_teams` rows at all) and could not be used for a live positive-case
probe of the narrowing path without seeding data, which was out of scope.

**Item 4.** Ran the mutation sweep fresh (not from memory) to get today's
true baseline: `write_rule.classify` 15/34 (0.44), 19 survivors, unchanged
from the last time this suite ran. Mapped each survivor to its exact
source clause by reading `harness/write_rule.py` in full. Designed and
live-verified each test case directly (calling `classify()` standalone,
not through the mutation harness) before writing it as a killer, exactly
as the two prior mutation-burndown dispatches did. Discovered mid-work
that 12 of the 19 survivors are structurally undetectable without real
`harness.care_team_keys` registry state — both "check the inner condition
and fail" and "skip the outer gate and never check" converge to the same
fallthrough behavior when no recipient/caregiver data exists, so a
positive fixture is required, not optional. Built one using the SAME raw
SQL insert/delete-in-finally pattern this codebase's DK1/DK4/P1
fault-injections already established, deliberately bypassing the public
`add_caregiver`/`ensure_care_team` API (which emits an append-only HEL
`care_team.grant` event with no erasure path for a synthetic row) —
SQLite-only, the Neo4j graph is never touched. Ten new killers added,
covering all 19 survivors; wired into `mutation_targets.py`'s existing
`classify` `TargetSpec`. `harness/write_rule.py` itself was not edited —
confirmed by `git diff` before committing.

## WHAT WAS FOUND

**Item 3 answer: the valid-cell count does NOT change from 2170.**
Fresh re-derivation: `total=2380, valid=2170, invalid=210`. The invalid
set, deduped by (scope, attribute): exactly `pair-private` paired with
`household`, `appointment`, `care_plan`, `incident`, `medication_status`,
`vitals` — 6 pairs × 7 roles × 5 intents = 210, matching the figure
already on record. The ruling confirms the CODE (and the code-derived
validity map) were always right; only the REQ's prose illustrative
example was wrong. Nothing about `is_valid_cell()` or the grid changes.

**Item 4 — the new write_rule score: 34/34 (1.00), up from 15/34 (0.44).
Zero survivors remain. No findings** — every one of the 19 was killable
without touching `classify()`'s behavior, unlike the `check_g0` slice
(which had one confirmed-equivalent mutant left standing). The 10 new
killers, mapped to what they close:

- `_kill_classify_none_subject_resolves_via_first_person` — :146, both
  `delete_last_operand(Or)` sites on `subj = (subject or "").strip()
  .lower() or None`. One test (`subject=None`, a first-person utterance)
  kills both: Or #1's mutant crashes outright (`None.strip()`,
  auto-killed via exception); Or #2's mutant skips `resolve_subject_
  for_write` entirely, so "I" never resolves to the author.
- `_kill_classify_coordination_attribute_blocks_narrowing` — :216,
  `delete_last_operand(And)`. A coordination attribute with no dyad/care
  team must fall through ALL the way to level 5, never land in 3c
  (3c is explicitly not coordination-attribute territory — that's 3b's).
- `_kill_classify_share_household_widens_self` /
  `_blocks_other_subject` — :166's four mutants, the household-circle
  widening restriction itself: self-facts widen, other-subject facts do
  not.
- `_kill_classify_share_care_team_positive` / `_requires_enrollment` —
  :170/:174/:178. Positive fixture (real active caregiver) kills the
  outer gate and the empty-exclude-set `in`/`not in` asymmetry in one
  call; a second fixture (recipient exists, nobody enrolled) isolates
  the AND-chain's enrollment requirement specifically.
- `_kill_classify_flag_safety_positive` / `_requires_enrollment` —
  :181/:184, same shape as share_care_team.
- `_kill_classify_coordination_default_positive` /
  `_requires_enrollment` — :200/:205, level 3b's own AND-chain and its
  subject-visibility ternary.

**Overall mutation score: 82/128 (0.64) → 101/128 (0.79).** All other 11
targets' survivor counts confirmed unchanged by the same full re-sweep
(`_inj1` 4/5, `_inj2` 10/20, `_inj3` 9/15, `_inj4` 1/1, `_inj5` 4/4,
`apply_injection_contract` 8/9, `check_g0` 7/8, `g1` 9/12, `g2` 2/5, `g3`
4/5, `g4` 9/10 — byte-for-byte identical to the pre-this-session sweep).

## VERIFIED

- **Watched run:** every one of the 10 new killer test cases was run
  standalone against the real, unmutated `classify()` and its printed
  `visibility`/`rule`/`subject_visibility`/`subject` output inspected
  directly, before being written into `mutation_targets.py` — not
  designed from reading the source alone. All 14 killers (4 pre-existing
  + 10 new) then re-confirmed to return `None` against real code as a
  group.
- **Watched run:** the full mutation sweep, both before (34/34→wait,
  15/34 baseline) and after (34/34) this session's edits, via direct
  invocation of `run_target`/`run_sweep` — not assumed from the debt
  register's prior text.
- **Watched run:** `coverage_grid.valid_cells()`/`invalid_cells()`
  re-executed fresh this session; 2170/210 reproduced live, not read
  from a comment.
- **Watched run:** `classify(owner="maya", attribute="household",
  subject="ray", ...)` with a "share with the care team" utterance —
  attempted live to reproduce the exact narrowing case, but
  `care_team_keys.is_recipient("ray")` returned `False` (the SQLite
  `care_teams` table is currently empty — zero rows — in this dev
  graph's state; a prior session's own recorded probe of this same case
  presumably ran against a since-diverged seed state). Per the no-reset/
  no-reseed constraint, did not seed this data to force a live
  reproduction of that SPECIFIC household/ray/maya case. Substituted a
  synthetic, self-contained, cleaned-up fixture (`zzz_mut_*` recipient
  refs) to prove the SAME code path live instead — confirmed a household-
  attribute fact directed to a real, actively-enrolled synthetic care
  team via "share with the care team" lands `care-team-private`, not
  the illustrative example's claimed-impossible outcome, exactly the
  general shape the ruling describes, just not against ray/maya
  specifically.
- **Reasoned about, not live-verified:** that the narrowing path is
  reachable in principle for ANY real recipient/caregiver pair, argued
  from direct reading of `write_rule.py:170-193`'s return-early ordering
  (level 2's `share_care_team` branch is checked, and returns, BEFORE
  level 3a's household-attribute check) rather than from a live call
  against real household data. The synthetic-fixture live proof above
  corroborates this reading; it does not by itself prove the exact
  ray/maya case still behaves identically today, only that no reset/
  reseed was used to force that specific proof.
- `python -m eval.harness --layer 7`: see the harness log referenced in
  the commit message. `RATCHET PASS`, `L7V2:MUTATION-SCORE` reports
  101/128 by name, `MUTATION-NO-SILENT-DISAPPEARANCE` PASS (19
  disappearances this run, all accounted for as killed — no debt-register
  edit was even required for that check to pass, though TD-134 was
  updated anyway, for the same reason the two prior mutation-burndown
  dispatches did: honesty of the persistent record, not a hard
  requirement of the mechanism itself).
- `git diff` confirmed zero changes to `harness/write_rule.py` this
  entire session — the "kill with new tests only" constraint holds by
  construction.

## HASH

See commit — this dispatch doc, the two REQ doc edits, `docs/techdebt/
DEBT_REGISTER__v20260727_1926.md` (+ `LATEST_DEBT.md` repoint), and
`eval/harnesslib/mutation_targets.py` all ship together. `docs/INDEX.md`
and `docs/deliverables/MANIFEST.md` deliberately NOT touched, per
instruction — another session holds them.

## OPEN

- TD-134 now has 27 survivors remaining (from the original 50), spanning
  `injection_contract`'s three predicates, `apply_injection_contract`
  itself, `check_g0`'s one confirmed-equivalent mutant, and
  `record_invariants`' four functions. `write_rule.classify` and
  (from the prior session) `harness/g0_invariant.py` are now the two
  fully-closed-or-resolved modules in the mutation-score family.
- The `care_team_keys` registry being completely empty in this dev
  graph's live state (not just for ray — zero rows in `care_teams`) is
  worth a separate look outside this dispatch's scope: either a stale/
  reset seed state, or a fixture this checkout never had. Named, not
  investigated further here.
- No REQ was marked MET by this dispatch, per instruction. Both edited
  REQs (`REQ_COVERAGE_MEASUREMENT`, `REQ_PARTITION_CUSTODY`) keep
  whatever `Status:` header they already carried.
