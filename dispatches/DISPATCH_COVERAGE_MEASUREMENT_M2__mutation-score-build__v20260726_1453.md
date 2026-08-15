# DISPATCH_COVERAGE_MEASUREMENT_M2
Status: BUILT
Reconciled-Against: this commit

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_COVERAGE_MEASUREMENT__coverage-metric-and-mutation-score__v20260726_1224.md` (830ec2f) — Metric 2 (mutation score) only. Metric 1 (coverage-grid) is out of scope for this dispatch; the REQ stays Status: NOT MET.

## THE ASK

Bill's words, verbatim:

> Build to REQ_COVERAGE_MEASUREMENT (830ec2f, LATEST) — Metric 2, the
> MUTATION SCORE, first (Metric 1 coverage-grid can follow). Commit WIP
> checkpoints. Do not touch fact_change.py or the care_coordination path
> (LOWER/Fable is diagnosing T01/T02 there).
> 1. Build the mutation-score metric per the REQ: mutate a gate predicate IN
>    MEMORY (never on disk), run the checks, a check going red = mutant
>    killed, survival = untested gate logic. Target predicates:
>    injection_contract INJ-1..7, write_rule.classify, check_g0,
>    record_invariants g1-g4.
> 2. For each mutant that SURVIVES (no check killed it), report file:line —
>    that's untested logic. Feed survivors into a TD-133-style burn-down
>    with a no-silent-disappearance rule.
> 3. The metric's own fault-twin (per REQ acceptance): a seeded known-
>    killable mutant (negating the INJ-7 refusal condition, killed by
>    FF1/FF4/MT2) MUST be killed, AND must survive when its killers are
>    excluded — proves the metric actually detects both.
> 4. Verify: mutation run completes, survivors listed, --layer 7 stays green
>    (in-memory, no residue), post-destruction law respected (no v1/master-
>    key resurrection).
> Report the mutation score (killed/total), the survivor list with
> file:line, the fault-twin result, WIP hashes. Do NOT mark REQ MET until
> both metrics are built — this is Metric 2 only.

## WHAT WAS DONE

1. Read the full REQ (830ec2f) to extract Metric 2's exact acceptance
   criteria (items 5-8) and constraints (post-destruction law, hard-zero
   semantics, deterministic/offline, no regression).
2. Read `harness/injection_contract.py` (the five separable INJ predicates
   plus the inlined INJ-7 boundary block), `harness/write_rule.py`,
   `harness/g0_invariant.py`, `eval/oracle/record_invariants.py` to confirm
   all named targets are pure functions over passed-in data — no Neo4j/
   model dependency, safe offline mutation targets.
3. Prototyped the core AST-mutation approach directly (a `NodeTransformer`
   walking a fresh parse per mutant, matched by deterministic traversal-
   order index rather than object identity — identity does not survive
   `copy.deepcopy`).
4. Built `eval/harnesslib/mutation_score.py` — the generic engine:
   `_SiteWalker` (four operators: `swap_compare`, `delete_last_operand`,
   `negate_if_test`, `flip_bool_const`), `count_mutation_sites`,
   `generate_mutant`, `patched` (context manager, unconditional restore),
   `Survivor`/`ModuleScore` dataclasses, `run_target` (with
   `exclude_killers`), `run_sweep`, `format_report`.
5. Found and fixed a bug: `count_mutation_sites` did not call `ast.
   increment_lineno` before applying a `lineno_range` filter (unlike
   `generate_mutant`, which does), so a scoped sweep compared relative
   (function-local) line numbers against absolute file line numbers and
   silently found zero sites. Fixed by adding the same `increment_lineno`
   call — confirmed via a before/after re-run (`apply_injection_contract`'s
   INJ-7-scoped sweep went from 0/0 to 8/9 killed).
6. Built `eval/harnesslib/mutation_targets.py` — 12 `TargetSpec` entries,
   ~30 killer probes, one `fault_twin_self_test()` function.
7. Ran the full sweep standalone, then wired both the sweep report and the
   fault-twin self-test into `eval/harnesslib/layer7_crypto_v2.py` as two
   new scenarios (`L7V2:MUTATION-SCORE`, `L7V2:MUTATION-SCORE-SELFTEST`),
   always-on (not opt-in — the sweep takes ~0.4s, cheap enough that
   acceptance item 5's opt-in-or-scheduled clause doesn't apply).
8. Registered both new scenarios in `eval/harnesslib/check_registry.py`
   with real twin/fixture/coverage/metamorphic entries (no debt), then ran
   `harness_audit.run()` standalone to confirm the roster picked them up
   cleanly (rows=53, missing=0).
9. Ran `python -m eval.harness --layer 7` end to end (dev graph, `.env.dev`
   sourced) — both new scenarios PASS, `L7V2: 25/26 (1 skipped)`, `RATCHET
   PASS`.
10. Filed `TD-134` in a new debt-register cut (`DEBT_REGISTER__v20260726_1453.md`)
    listing all 50 survivors by file:line + operator, framed explicitly as
    the no-silent-disappearance baseline; repointed `LATEST_DEBT.md`;
    updated `docs/INDEX.md`'s tech-debt row.
11. Added an UPDATE section to the REQ doc documenting Metric 2 as built,
    Metric 1 as still open, Status left at NOT MET.

## WHAT WAS FOUND

Overall mutation score: **78/128 killed (0.61)**. Per module:

- `harness/injection_contract.py:_inj1_subject_scope` — 4/5 killed.
  Survivor: `:413` `delete_last_operand(Or)`.
- `harness/injection_contract.py:_inj2_relevance` — 10/20 killed.
  Survivors: `:443` `delete_last_operand(Or)`; `:447` `flip_bool_const`;
  `:450` `delete_last_operand(Or)`; `:450` `swap_compare Eq->NotEq`; `:450`
  `delete_last_operand(And)`; `:451` `swap_compare IsNot->Is`; `:452`
  `swap_compare In->NotIn`; `:453` `flip_bool_const`; `:460` `swap_compare
  In->NotIn`; `:471` `flip_bool_const`.
- `harness/injection_contract.py:_inj3_cross_member_deny` — 9/15 killed.
  Survivors: `:505` `flip_bool_const`; `:508` `delete_last_operand(Or)`;
  `:510` `delete_last_operand(Or)`; `:514` `negate_if_test`; `:517`
  `negate_if_test`; `:518` `flip_bool_const`.
- `harness/injection_contract.py:_inj4_household` — 1/1 killed (100%).
- `harness/injection_contract.py:_inj5_never_volunteer` — 4/4 killed (100%).
- `harness/injection_contract.py:apply_injection_contract` (INJ-7 block,
  `lineno_range=(611,629)`) — 8/9 killed. Survivor: `:619` `delete_last_
  operand(And)` (drops the `intent in _PERSONAL_INTENTS` clause).
- `harness/write_rule.py:classify` — 15/34 killed (weakest module).
  19 survivors across `:146,166,170,174,178,181,184,200,205,216` — full
  list in `docs/techdebt/DEBT_REGISTER__v20260726_1453.md` TD-134.
- `harness/g0_invariant.py:check_g0` — 3/8 killed. Survivors: `:65,67,68,74,75`,
  all `delete_last_operand`.
- `eval/oracle/record_invariants.py` g1-g4 — g1 9/12 (survivors `:62,76,78`),
  g2 2/5 (survivors `:95,96,97`), g3 4/5 (survivor `:117`), g4 9/10
  (survivor `:171`).

Dominant pattern: `delete_last_operand` dropping the LAST clause of a
multi-clause `and`/`or`. Every named module's killer probes exercise each
clause's true/false state individually, but none constructs the specific
case where dropping the trailing clause (as opposed to any other) changes
the outcome — that gap is structural across the whole target set, not one
module's oversight.

Fault-twin self-test (acceptance item 6): seeded mutant = `negate_if_test`
at `harness/injection_contract.py:619` (the INJ-7 refusal condition:
`member_ids is not None and not is_declarative and intent in
_PERSONAL_INTENTS`). Bill's dispatch named this mutant as "killed by
FF1/FF4/MT2" (the harness's crypto-layer scenario names); the concrete
killer probes built for it in `mutation_targets.py` are
`_kill_inj7_cross_member_denied`, `_kill_inj7_self_query_not_denied`,
`_kill_inj7_declarative_exempt` — functionally the same boundary those
scenarios exercise, expressed as offline predicate-level probes rather than
full end-to-end crypto scenarios (this metric mutates the predicate, not
the crypto layer, so it needed its own probes at that level).

## VERIFIED

- **Watched run:** `python3 -c "from eval.harnesslib.mutation_score import
  run_target; ..."` — printed `FULL KILLER SET -> ... negate_if_test@619
  survived=False` and `EXCLUDED KILLERS -> ... negate_if_test@619
  survived=True`, both directions confirmed live, not reasoned about.
  `python -m eval.harness --layer 7` (dev graph, `.env.dev` sourced) run to
  completion: `L7V2: 25/26 (0 flaked, 1 skipped)`, `MUTATION-SCORE PASS`,
  `MUTATION-SCORE-SELFTEST PASS`, `RATCHET PASS — no scenario regressed vs
  baseline.` `harness_audit.run(verbose=False)` run standalone: `rows=53,
  missing=[], debt_flags=46, gate_pass=True` — both new checks present in
  `aud.rows` with `twin`/`fixture`/`coverage`/`metamorphic` all `ok`/`n/a`,
  none `missing`.
- **Reasoned about:** that no code path in `mutation_score.py`/
  `mutation_targets.py` imports `harness.encryption` or touches master-key/
  v1 machinery — confirmed by grep (`grep -rn "harness.encryption"
  eval/harnesslib/mutation_score.py eval/harnesslib/mutation_targets.py`
  returns nothing), not by a dedicated negative-proof run.

## HASH

WIP commits (this dispatch): see below — `mutation_score.py`/
`mutation_targets.py` committed, then the wiring/registry/debt/REQ-update
changes committed. Final hash reported after commit below.

## OPEN

- Metric 1 (coverage-grid, declared-vs-measured state-space enumeration)
  is unbuilt — separate dispatch, per Bill's explicit sequencing.
- TD-134's 50 survivors are not burned down in this dispatch — Bill's
  ask was to build and verify the metric, not close what it found. The
  dominant `delete_last_operand`-on-last-clause pattern suggests the
  burn-down is mechanical (one boundary-clause probe per site) but that
  work has not started.
- The REQ's acceptance item 7 also requires a MECHANICAL check (not just a
  register entry) that a future run's survivor list only shrinks with
  accounting — i.e. a diff against the previous run's survivor list stored
  in the trend file (`harness_trend.jsonl`). This dispatch created the
  human-readable baseline (TD-134) but did not build that mechanical trend-
  diff enforcement; left for when Metric 1 lands and the REQ closes.
