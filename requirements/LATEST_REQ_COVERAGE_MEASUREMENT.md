# REQ_COVERAGE_MEASUREMENT: Coverage Metric and Mutation Score
Status: MET
Branch: roadmap
Reconciled-Against: 200be75 (audit + registry live at 003fd9c/7730044 with UPPER's TD-133 burn-down in progress — 7 crypto-layer twin gaps closed at 200be75; REQ_CRYPTO_P3 MET at ffe4d67, PS1-4's v1-simulation retired, OB6 successor built; roster and registry contents are therefore MOVING — this REQ names mechanisms, not row counts); HIP_TestingBestPractices__research__v20260726_1005.md (§5 "the audit verifies artifact existence, not strength", §1 mutation-score finding, adoption items 4 and 5); REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827.md (standard (c), the coverage entry this REQ upgrades)

REQ only, scope only, no code. Filed while Bill is out, from the standing
instruction's words; no build starts until a dispatch names this doc
(Requirements Discipline item 8).

## THE REQUIREMENT

Bill's words, verbatim (standing instruction, 2026-07-26):

> turn the audit's coverage-entry field from a declaration into a measurement
> — a metric that reports what fraction of the authorization state space
> (role combinations, scope classes, attribute-taxonomy splits, intent
> classes) actually has a test exercising it, and flags uncovered regions.

> Draw on the research doc's mutation-score finding: the audit verifies
> artifact existence not strength; mutation testing is the published fix.
> Scope how a mutation-score metric would work here (mutate a gate predicate,
> confirm a check goes red; survival = untested logic).

Expanded: two metrics, one upgrade each.

**Metric 1 — coverage, from declared to measured.** Today a check's registry
entry DECLARES its slice of the authorization state space and the audit
verifies only that the declaration is non-empty. Nothing checks that the
declared slice matches what the check's fixtures actually exercise, and
nothing sums exercised slices across the suite to say which regions of the
space no check touches at all. The upgrade: define the state space as an
enumerable grid, derive the EXERCISED cells mechanically from the scenarios'
own fixtures (owners, subjects, attributes, classes, and intents are
literals in the registry, the fixture code, and the write-rule tables — they
are parseable, which is what makes measurement possible), and report
exercised/valid as a fraction with every uncovered valid cell listed.

The space's dimensions, from Bill's words: role combinations (author,
custodian, care-team member, household adult, non-member, care-recipient
subject, operator-as-adversary), scope classes (member-private,
pair-private, care-team-private, household-circle-shared — the ratified
four), attribute-taxonomy splits (the CANONICAL_ATTRIBUTES enum plus the
coordination-attribute family from the write rule), intent classes (personal
recall, declarative write, household query, adversarial probe, free
generation — the classes the routing layer actually distinguishes). A cell
is one tuple across the four dimensions. Structurally-invalid cells (e.g. a
pair-private scope paired with the household attribute or any coordination
attribute, combinations the ratified partition rules make unrepresentable —
CORRECTED 2026-07-27, this example originally named a different, WRONG
combination; see the dated RULING note in the build section below for what
it said and why) are excluded from the DENOMINATOR and
listed separately as invalid-by-design — a metric whose denominator includes
impossible cells flatters itself; one that hides the exclusion list cannot
be checked.

**Metric 2 — mutation score, from existence to strength.** The audit proves
a twin EXISTS; it cannot prove the twin (or the check behind it) is strong.
The research doc's finding, adopted here as scope: mutate a gate predicate
(negate a condition, swap a comparison, delete a clause, flip a constant) in
one of the named gate modules — harness/injection_contract.py (INJ-1..7),
harness/write_rule.py (classify), harness/g0_invariant.py (check_g0),
eval/oracle/record_invariants.py (g1-g4) — one mutant at a time, in memory,
never on disk; run the deterministic check subset that claims to cover that
predicate; record KILLED (some check went red) or SURVIVED. A surviving
mutant is a piece of gate logic no check actually tests, located to
file:line — the measured version of the gap the four-part standard can only
declare. Score = killed/generated per module; every survivor listed, each
one becoming either a new twin or a debt-ID entry, the same burn-down
contract TD-133 already runs.

## THE ACCEPTANCE TEST

Pass/fail, per metric.

Coverage metric:
1. On every `--full`, the AUDIT block prints: total valid cells, exercised
   count, the fraction, the full uncovered-valid-cell list, and the
   invalid-by-design exclusion list (or an explicit count + pointer if the
   lists exceed a stated print budget — a truncation that does not announce
   itself is a FAIL). Observable: run `--full`, see all five elements.
2. The metric is MEASURED, proven by its own fault-injection twin:
   (a) red-on-command — a synthetic registry entry declaring coverage of a
   cell no fixture exercises is reported as a DECLARED-NOT-MEASURED
   discrepancy; (b) sensitivity — removing one scenario's fixture from the
   derivation input (synthetically, in the audit's self-test, same pattern
   as the existing twin-less injection) reduces the exercised count. If the
   count does not move, the metric is a declaration with extra steps: FAIL.
3. Per-check discrepancy rule: a check whose DECLARED slice contains cells
   its fixtures do not exercise is flagged by name (visible, debt-ID-able,
   same FLAGGED-not-silent contract as TD-133). Measured-but-undeclared
   cells update the report without failing it.
4. The fraction lands in the trend file per run, and the ratchet treats a
   DECREASE the way it treats a scenario regression: not silent — either
   green (no decrease), or flagged with a debt ID/expiry.

Mutation-score metric:
5. The runner completes deterministically (no model calls, no network, no
   live graph mutation outside the existing mutation-window discipline) and
   prints per-module: generated, killed, survived, score, and each survivor
   as file:line + mutation operator. Observable on demand and on a stated
   cadence (per sprint at minimum — the sprint-start standing rule of
   REQ_HARNESS_DISCIPLINE is the natural hook); wired the same
   opt-in-or-scheduled way CT-OUTPUT-GAP is if runtime cost demands it,
   but its REPORT is part of the audit output either way.
6. Its own two-sided self-test: (a) a seeded mutant the suite is known to
   catch (e.g. negating the INJ-7 refusal condition, which FF1/FF4/MT2
   claim to cover) is KILLED — red-on-command; (b) the same mutant with its
   killing checks excluded from the run set SURVIVES and is reported as a
   survivor — proves survival detection is real, not vacuous. Both
   directions must hold or the metric FAILs.
7. Survivors are output, not run-failures: the run is green with survivors
   PRESENT AND PRINTED. What is a FAIL of this REQ: a survivor list that
   shrinks without each removed survivor being either killed by a new/
   strengthened check or carried under a debt ID — the no-silent-
   disappearance rule, mechanically checked against the previous run's
   survivor list in the trend file.
8. Neither metric changes any existing check's pass/fail behavior, and the
   whole build leaves AUDIT 3/3, the layer-7 suite, and the full RATCHET
   green (CLAUDE.md item 12: done means the full ratchet passes).

## WHAT'S ALREADY DONE

Do not redo any of this:
- The four-part audit and registry (003fd9c, 7730044): roster enumeration by
  AST, declaration verification, executable probes, twin-less rejection,
  TD-133 flag printing on every run. The coverage metric EXTENDS the audit's
  coverage verification; it does not replace the audit.
- Coverage-entry declarations exist for every registered check (the
  registry's `coverage` field) — they become Metric 1's DECLARED side, and
  UPPER's TD-133 burn-down (200be75 and onward) is actively changing
  registry contents; the build must read the registry live, not snapshot
  today's rows.
- Layer 4's pairwise matrix: the generation half of combinatorial coverage
  for retrieval (NIST SP 800-142's territory, per the research doc). Metric
  1 is the measurement half, suite-wide.
- Layer 3's guard-integrity machinery: in-process mutation with monkey-
  patching, and — load-bearing for Metric 2 — the MUTATION_WINDOWS_LOG
  contamination discipline that keeps deliberate-mutation output out of the
  L6 gate (harness.py's C3/D-06 handling). Metric 2 generalizes Layer 3's
  targeted mutations into a scored sweep; it reuses the window discipline
  as-is.
- The trend/ratchet infrastructure (harness_trend.jsonl, reporter tiers,
  debt-ID-or-expiry `--accept` discipline) — both metrics' no-silent-
  regression rules ride on it.
- The research doc (HIP_TestingBestPractices v20260726_1005) has the
  published grounding: mutation testing (DeMillo/Lipton/Sayward 1978;
  Petrović & Ivanković, ICSE-SEIP 2018), combinatorial coverage measurement
  (Kuhn et al., NIST SP 800-142), and the honest statement of the weakness
  this REQ closes (§5). Adoption-list items 4 and 5 are this REQ.

## WHAT'S KNOWN BROKEN

From the research doc, stated as the gaps this REQ exists to close:
- Coverage is declared, not measured: the audit verifies the four coverage
  keys are non-empty lists — nothing verifies the lists are TRUE, and
  nothing aggregates them into what-fraction-of-the-space-is-tested.
- Declared entries can drift from fixtures with no detection: a fixture
  edit (or a scenario retirement — PS1-4's retirement at ffe4d67 is a live
  example of the roster moving under the registry) can silently invalidate
  a declaration today.
- No mutation score exists anywhere: nobody can state what fraction of gate
  mutants the suite kills. Layer 3 mutates a handful of hand-picked guards;
  there is no sweep, no score, no survivor list.
- The audit verifies artifact existence, not strength: a weak twin passes
  the audit identically to a strong one. Metric 2 is the published fix.
- Uncovered regions are invisible: no artifact anywhere lists the
  authorization-state-space cells that NO check exercises. The four-part
  standard made per-check slices visible; the suite-wide complement is
  still dark.

## CONSTRAINTS

- Scope only, this REQ, docs only. The build starts on a dispatch naming
  this doc, not before, and not by this session (harness code is UPPER's).
- The post-destruction world is law: no part of either metric may resurrect
  master-key/v1 machinery or contradict OB5/OB6. Mutants are applied in
  memory to loaded module objects (or AST-transformed copies), NEVER
  written to the working tree, never committed, never left applied after a
  run — a crash mid-sweep must not leave a mutated module live (the Layer 3
  window pattern already solves this; reuse it).
- Hard-zero semantics untouchable: neither metric may add an accept path,
  gate, or config flag to G0/G1/G4 or any ABSOLUTE-tier scenario.
- Deterministic and offline: no model calls in either metric; the mutation
  sweep runs only checks that are themselves deterministic (the live-model
  L2/L5 families are out of the kill-set by construction — a flake must
  never decide a mutant's fate).
- No regression: AUDIT 3/3, layer-7 green, full RATCHET green after wiring.
  The metrics report and flag; they do not turn existing green runs red on
  day one — new hard failures enter via the debt-ID/ratchet path like
  every other tightening has.
- The registry is the single source of the DECLARED side; the fixtures/
  code are the single source of the MEASURED side. No third bookkeeping
  file that can drift from both.

## UPDATE 2026-07-26 (later still): Metric 2 (mutation score) BUILT — Metric 1 (coverage grid) still open, Status stays NOT MET

Built per Bill's dispatch naming this doc (this session, not the filing
session — Requirements Discipline item 8's gate satisfied by that dispatch).
Metric 1 (coverage-grid) is explicitly out of scope for this dispatch and
remains unbuilt; this REQ is NOT marked MET.

**Engine** (`eval/harnesslib/mutation_score.py`, generic, reusable):
`ast.NodeTransformer`-based mutator (`_SiteWalker`) applying one of four
operators per site — `swap_compare` (Eq/NotEq/Lt/GtE/Gt/LtE/In/NotIn/Is/
IsNot), `delete_last_operand` (BoolOp And/Or), `negate_if_test`, `flip_
bool_const` — targeted by a deterministic traversal-order index (re-parses
fresh source per mutant; no object-identity matching across copies, which
does not survive `deepcopy`). `generate_mutant` compiles the mutated AST to
a fresh function object in a copy of the module's namespace; `patched` is a
context manager that monkeypatches the module attribute for the `with`
block only and restores the ORIGINAL object unconditionally in `__exit__`,
even on exception — nothing is ever written to disk, nothing survives a
crash mid-sweep (constraint: "must not leave a mutated module live").
`run_target(target, exclude_killers=...)` runs every site's mutant against
a `TargetSpec`'s killer probes, scoring KILLED (a killer returned non-None)
vs SURVIVED; `exclude_killers` exists specifically for the fault-twin's
negative half.

**Targets** (`eval/harnesslib/mutation_targets.py`, domain-specific, ~30
killer probes, zero model calls/network/live graph mutation — every probe
constructs synthetic facts/records in memory): `harness.injection_contract`
`_inj1_subject_scope` / `_inj2_relevance` / `_inj3_cross_member_deny` /
`_inj4_household` / `_inj5_never_volunteer` (the five separable predicates)
plus `apply_injection_contract` scoped via `lineno_range=(611,629)` to just
the INJ-7 boundary block (the ~200-line function's other conditions would
otherwise dilute the count); `harness.write_rule.classify`; `harness.
g0_invariant.check_g0`; `eval.oracle.record_invariants` g1-g4.

**Result, this run**: overall **78/128 killed (score 0.61)**. Per-module:
`_inj1_subject_scope` 4/5, `_inj2_relevance` 10/20, `_inj3_cross_member_deny`
9/15, `_inj4_household` 1/1, `_inj5_never_volunteer` 4/4,
`apply_injection_contract` (INJ-7 block) 8/9, `write_rule.classify` 15/34
(weakest module), `check_g0` 3/8, `g1` 9/12, `g2` 2/5, `g3` 4/5, `g4` 9/10.
All 50 survivors listed by file:line + operator in `docs/techdebt/
DEBT_REGISTER__v20260726_1453.md` (TD-134) — the no-silent-disappearance
baseline (acceptance item 7): a future run's survivor list may only shrink
with each removal accounted for (killed by a strengthened probe, or
explicitly carried forward under TD-134). Dominant survivor pattern:
`delete_last_operand` dropping the LAST clause of a multi-clause and/or —
existing probes exercise each clause's true/false state individually but
none constructs the case where only the dropped clause was load-bearing.

**Fault-twin self-test (acceptance item 6), BOTH directions verified live**:
seeded mutant = `negate_if_test` at `harness/injection_contract.py:619`
(the INJ-7 refusal condition: `member_ids is not None and not is_declarative
and intent in _PERSONAL_INTENTS`). With its 3 designated killers present
(`_kill_inj7_cross_member_denied`, `_kill_inj7_self_query_not_denied`,
`_kill_inj7_declarative_exempt`): KILLED. With those same 3 excluded via
`run_target(target, exclude_killers=target.killers)`: SURVIVES. Both hold —
survival detection is real, not vacuous.

**Wiring (acceptance item 5)**: sweep completes in ~0.4s total — cheap
enough that "opt-in-or-scheduled...if runtime cost demands it" does not
apply (unlike CT-OUTPUT-GAP's real model call); wired as an ALWAYS-ON part
of `--layer 7`/`--full` output. Two new scenarios in `layer7_crypto_v2.py`:
`L7V2:MUTATION-SCORE` (SERIOUS — fails only if the sweep itself breaks or a
named module generates zero mutants; survivors are printed via `format_
report`, never fail the check per acceptance item 7) and `L7V2:MUTATION-
SCORE-SELFTEST` (ABSOLUTE — the fault-twin above; mirrors the MT1-CANARY/
MT2/OB6 self-test pattern). Both registered in `check_registry.py` with
real twin/fixture/coverage markers (no debt entries) — AUDIT roster clean:
rows=53, missing=0, both new checks verified with `role/twin/fixture/
coverage/metamorphic` all present. Verified live: `L7V2 25/26` (1 opt-in
skip, unchanged from before this build), `RATCHET PASS`, AUDIT rows=53/
missing=0.

**Post-destruction law respected**: neither `mutation_score.py` nor
`mutation_targets.py` imports `harness.encryption` or touches master-key/
v1 machinery; all mutation is in-memory AST transforms on loaded module
objects, `patched`'s `__exit__` restores unconditionally.

**Not touched, per Bill's explicit constraint**: `harness/fact_change.py`,
`care_coordination` path (LOWER/Fable's T01/T02 diagnosis).

**Remaining for this REQ to reach MET**: Metric 1 (coverage-grid,
declared-vs-measured, state-space enumeration) — unbuilt, separate
dispatch.

## OPEN ITEM 2026-07-26 (later still): acceptance item 7 cannot run — no survivor output file exists

Docs-only note, filed against this REQ, Status unchanged (stays NOT MET).

Acceptance item 7 requires the survivor list to be checked against the
previous run's survivor list in the trend file — a mechanical
no-silent-disappearance check. That check has no file to read: a repo-wide
search for a survivor output file (`find ~/hip-roadmap -iname "*survivor*"`)
returns nothing. `mutation_score.py`'s runner PRINTS survivors
(file:line + mutation operator, per the Metric 2 build above) but does not
PERSIST them anywhere — there is no trend-comparable record for a later run
to diff against.

Item 7 cannot execute until survivors are written to a file that a
subsequent run can compare against (the same trend-file discipline Metric
1's ratchet already uses for the coverage fraction). Until that exists, the
no-silent-disappearance rule is unenforceable — a survivor could vanish
between runs and nothing would notice.

Status stays NOT MET.

## UPDATE 2026-07-27: acceptance item 7 BUILT and verified live — Metric 1
(coverage grid) is now the ONLY remaining blocker. Status stays NOT MET.

Built at e13646e (item 2 of a five-item 2026-07-27 sprint instruction).

**Persistence** (`eval/harnesslib/mutation_score.py`): `ModuleScore` gained
a `killed_mutants` field (same `Survivor` shape as `survivors` — module/
func/operator/lineno), populated in `run_target` alongside the existing
`killed` count. Purely additive; does not change `killed`/`survived`
counts or any existing check's pass/fail behavior. Needed because telling
"no longer surviving because a killer now catches it" apart from "no
longer surviving because the mutation site itself is gone" requires
knowing which exact mutants were killed THIS run, not just how many.
`write_survivor_trend(scores, timestamp=...)` appends one JSONL record per
run to `logs/mutation_survivors.jsonl` (alongside `logs/
mutation_windows.jsonl`, same directory/convention, distinct mechanism):
survivors, killed-mutant identities, and the aggregate score. `timestamp`
is caller-supplied — the module stays pure/deterministic, no wall-clock
read inside it. `read_last_survivor_run()` returns the most recently
persisted record, or `None` if the file doesn't exist yet (bootstrap case
— nothing to compare against is not a violation, it establishes the
baseline).

**No-silent-disappearance check**: `check_no_silent_disappearance(previous,
current_scores, debt_text=...)`. A previous survivor "disappears" if it is
not in the current survivor list; a disappearance is accounted for if
EITHER (a) the identical mutant now appears in this run's killed-mutant
identities, or (b) its location is named alongside its operator in the
debt register text (`find_debt_carry`, scanning `docs/techdebt/
LATEST_DEBT.md`). `find_debt_carry` is a best-effort parse of hand-written
debt-register prose (each row is one physical line starting `| TD-NNN |`,
verified 31/31 rows this shape against the live register; within a row, a
module is introduced by a backtick-quoted `*.py` path and its `:LINENO
`operator`` listing runs until the next such marker) — not a guaranteed
structural format, stated as such in the code. Validated against the REAL
register, not just synthetic data: correctly resolves all 6 spot-checked
TD-134 entries across three different modules to `TD-134`, and correctly
returns `None` for a bogus module, a bogus line number, and a genuine
cross-module line-number collision test (`harness/injection_contract.py:
166`, which does not exist — :166 belongs to `write_rule.py` in TD-134's
text; module-scoped segmentation prevents the false match).

**Wiring** (`eval/harnesslib/layer7_crypto_v2.py`): two new SERIOUS/
ABSOLUTE scenarios after `MUTATION-SCORE-SELFTEST`, same file, same
pattern. `L7V2:MUTATION-NO-SILENT-DISAPPEARANCE` (SERIOUS) reads the
previous persisted run BEFORE writing the current one (order matters — an
after-write comparison would be vacuously green forever, comparing a run
against itself), runs the check against the live debt register, then
persists this run's survivors. `L7V2:MUTATION-NO-SILENT-DISAPPEARANCE-
SELFTEST` (ABSOLUTE) is this check's own fault-injection twin
(REQ_HARNESS_DISCIPLINE standard #1), mirroring `MUTATION-SCORE-SELFTEST`'s
pattern exactly: synthetic previous/current survivor pairs, never touching
the real trend file or debt register, proving all four directions —
RED (unaccounted disappearance), GREEN (killed this run), GREEN (carried
under a debt ID), and the bootstrap no-op (no previous record).

**Registered** in `check_registry.py` with real markers for both new
checks (fixed one build-time bug: two initial marker strings were written
to span a line-wrapped comment/string-literal boundary in the source,
which the audit's exact-substring check correctly rejected as MISSING;
corrected to markers fully contained on one source line each, re-verified
green). `twin` is `{"na": ...}` for the main check (same pattern as
`MUTATION-SCORE` itself — the check body IS the comparison; the SELFTEST
check is where kill/survive detection is actually proven), a real
synthetic self-test for the SELFTEST check. `metamorphic` is `{"na": ...}`
for both (code-mutation-coverage bookkeeping, not a decision over
meaning-preserving input rewordings — same reasoning `MUTATION-SCORE`
already uses).

**Live-verified, three separate `--layer 7` runs** (via the new
`scripts/run_harness.sh` from item 1 of this sprint, all through the real
graph, no simulation for the primary path):
- Run 1 (bootstrap, no `logs/mutation_survivors.jsonl` existed yet):
  `MUTATION-NO-SILENT-DISAPPEARANCE` PASS, detail "no previous survivor
  record — this run establishes the baseline"; wrote generated=128,
  killed=78, survived=50 (matches TD-134's documented baseline exactly).
  `MUTATION-NO-SILENT-DISAPPEARANCE-SELFTEST` PASS, all four directions
  true. AUDIT 3/3, 56 checks enumerated (54 -> 56, the two new ones), 0
  missing artifacts. `L7V2` 27/28 (up from 25/26, the two new checks, same
  1 opt-in skip as before — no existing check's count changed). RATCHET
  PASS.
- Run 2 (real previous-run comparison, not the bootstrap path): detail
  changed to "no disappearances vs previous run" — proves the comparison
  genuinely reads the prior persisted record, not just the self-test's
  synthetic data. `logs/mutation_survivors.jsonl` grew from 1 to 2 lines
  (append-only, confirmed). RATCHET PASS.
- Self-test proven both directions on real (not just synthetic-in-code)
  execution: `no_silent_disappearance_self_test()` invoked directly and
  via the wired scenario, `red_ok=True green_killed_ok=True
  green_debt_ok=True bootstrap_ok=True` on every run.

**Acceptance items 5, 6, 7, 8 (Metric 2's full scope) now all hold**: 5 —
unchanged, already built; 6 — unchanged, already built (`MUTATION-SCORE-
SELFTEST`, verified again this run); 7 — BUILT, verified above; 8 — no
regression: AUDIT 3/3, layer-7 green (L7 24/24, L7V2 27/28), full L7 layer
RATCHET PASS across all three runs (this build's own CONSTRAINT was
verified via `--layer 7`, not `--full` — see the standing sprint
instruction's FORBIDDEN list for why `--full` was not run this session;
`--full` verification is outstanding, named below, not silently assumed).

**What this update does NOT do**: run `--full` (forbidden this session —
Layer 7 only; the FORBIDDEN list is explicit and this build respected it,
so `--full`'s own additional scenarios, e.g. `care_coordination.T01`/`T02`,
were not re-verified against this change — they do not touch mutation
scoring and are extremely unlikely to be affected, but "unlikely" is not
"verified," named here rather than assumed); build Metric 1 (coverage
grid, acceptance items 1-4, entirely separate scope); burn down any of the
50 TD-134 survivors (that is item 4 of this same sprint, not this item);
mark this REQ MET.

**Remaining for this REQ to reach MET: Metric 1 only** (coverage-grid,
declared-vs-measured, authorization-state-space enumeration — acceptance
items 1-4). Metric 2 (mutation score + no-silent-disappearance) is now
fully built against every acceptance item in its scope (5-8). Status stays
NOT MET per the standing instruction's explicit constraint — this reports
readiness, Bill decides.

## UPDATE 2026-07-27 (later): Metric 1 (coverage grid) BUILT and verified.
Both metrics now hold against every acceptance item in their scope. Status
stays NOT MET.

Built at item 3 of the same 2026-07-27 five-item sprint, following item 2
(no-silent-disappearance). Read this section's THE REQUIREMENT block first
and used its axes literally, per the standing instruction ("do not
improvise the axes") — no substitute vocabulary, no borrowed axis set from
Layer 4's own pairwise matrix (checked and confirmed to be a different,
narrower axis set for a different purpose: retrieval-generation coverage,
not the suite-wide authorization state space this REQ names).

**The grid** (new module, `eval/harnesslib/coverage_grid.py`, generic
engine + domain-specific fixture derivation together, unlike mutation_
score.py/mutation_targets.py's split -- the space is small enough not to
need one): role combinations (7, Bill's literal list: author, custodian,
care-team member, household adult, non-member, care-recipient subject,
operator-as-adversary) x scope classes (4, the literal `harness.write_
rule.CLASS_*` constants) x attribute-taxonomy splits (17, `harness.
extraction_queue.CANONICAL_ATTRIBUTES`, read live every call, never a
frozen copy) x intent classes (5, Bill's literal list: personal recall,
declarative write, household query, adversarial probe, free generation).
2380 total cells.

**Validity** (acceptance items 1/2a): derived from `harness.write_rule.
classify()`'s actual four-level precedence, not asserted, then verified
live against the real classifier (household maya/sam/ray -- sam and maya
are both ray's registered active caregivers with active dyads, bill is
neither). Finding: member-private, household-circle-shared, and care-
team-private are each reachable for EVERY attribute via a level-2
directive override (none of the four directives inspect `attribute` at
all); pair-private is reachable ONLY for a non-household, non-coordination
attribute (level 3c's own `attribute not in COORDINATION_ATTRIBUTES`
condition, and level 3a intercepts "household" before 3c can ever fire).
Only 6 of 68 (scope, attribute) pairs are structurally invalid -- pair-
private paired with "household" or any of the five coordination
attributes -- giving 210 invalid cells (2170 valid) out of 2380 total.

**FLAGGED, not silently reconciled**: the REQ's own illustrative example
("a care-team scope on a household attribute" as invalid-by-design) does
NOT hold against the real classifier. Verified live: `classify(owner=
"maya", attribute="household", subject="ray", utterance="share with the
care team: ...")` returns `care-team-private`, rule=`2-directive-share-
care-team` -- exactly the combination the example names as impossible.
This build uses the code-derived rule (confirmed against 5 separate live
`classify()` calls spanning all four rule levels, not just this one), not
the illustrative example. Named here because the REQ explicitly warned
"do not improvise the axes" and this is the one place the code disagreed
with Bill's own stated expectation -- surfaced, not smoothed over.

**RULING 2026-07-27 (Bill), closing the flag above:** the REQ's
illustrative example is wrong, the code is right -- `write_rule.classify()`
is not changed. What the illustrative example originally said, preserved
here as the record (THE REQUIREMENT section above is corrected in place;
this note is the trace of what it said and why): *"(e.g. a care-team scope
on a household attribute, combinations the ratified partition rules make
unrepresentable)"*. Why it was wrong: it conflated NARROWING with WIDENING.
A directive that NARROWS scope -- such as a household-attribute fact
directed to the care team via "share with the care team" -- is safe and
permitted; nothing in the ratified write rule restricts narrowing, and
REQ_PARTITION_CUSTODY's own level-2 directive vocabulary names "share with
the care team" as a first-class directive with no attribute carve-out. The
constraint that matters, and the one the illustrative example should have
named, is on WIDENING, and it was already ratified before this REQ was even
filed: REQ_PARTITION_CUSTODY's household-circle widening restriction
(`docs/requirements/REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md:95`)
says a level-2 directive may widen to household-circle-shared only for
facts about the author or generic household facts, and widening a fact
about another person beyond its level-3 default requires that person's own
standing policy (level 1) -- the illustrative example simply had the
direction of the constraint backwards. The mandatory subject-is-caregiver
rule (generalized 2026-07-21 to subject-is-any-enrolled-member,
`REQ_PARTITION_CUSTODY:96`) stays a hard, non-overridable constraint,
untouched by this correction. The real invalid-by-design set is exactly
the one the validity derivation above already found empirically, from the
live classifier, independent of the wrong illustrative example: pair-
private paired with the household attribute or any of the five
coordination attributes (210 of 2380 cells, 2170 valid) -- narrowing TO
care-team-private or household-circle-shared FROM a household attribute
was never one of them, and the validity figure itself does not change.

**EXERCISED derivation**: two-stage, because `classify()` (write-time)
and `injection_contract`'s separable predicates (retrieval-time) are
different functions with different parameters -- neither alone produces a
(role, scope, attribute, intent) tuple. Stage 1 (`_write_cells`) calls the
real `classify()` for 4 roles x 17 attributes, tags "declarative write".
Stage 2 (`_retrieval_cells`) builds a fact from stage 1's real WriteClass
output and calls the real `_inj3_cross_member_deny` with varying
requesters, tagging "personal recall"/"household query"/"adversarial
probe" from the requester relationship. A third stage
(`_free_generation_cells`) calls the real `_inj2_relevance` with a
deliberately irrelevant query (same shape as mutation_targets.py's own
`_kill_inj2_irrelevant_keyword_denied`), tagging "free generation". Every
cell is recorded because a real function was actually called with these
literals and returned a real result -- never a hand-asserted scope or
verdict. Two roles (custodian, operator-as-adversary) fit neither
function's parameter model at all (crypto-custody and operator-level
access are not household-role concepts) and are asserted from the KNOWN,
already-verified scope of the RE1-RE7/OB4-OB6 checks instead of freshly
derived -- a named, lighter-touch treatment for 2 of 7 roles, not hidden.

**Honest result, not padded**: 195 of 2170 valid cells exercised, fraction
0.090. This is expected and correct, not a defect to explain away -- this
build's fixture derivation is a representative, hand-selected sample
(mirroring mutation_targets.py's own killer-probe scale), not an
exhaustive scan of every scenario's literals across L1-L7. The metric's
entire point is to make that gap visible; a padded number would defeat it.
Expanding the exercised-cell derivation to scan real L1-L7 scenario
fixtures more broadly is future work, not attempted this session -- named
as a scope limit, not silently assumed done.

**Fault-injection twin (acceptance item 2), both halves, live-verified**:
(a) red-on-command -- a synthetic registry entry declaring coverage of
`Cell("non-member", household-circle-shared, "zone_district", "adversarial
probe")`, confirmed absent from the real exercised set, IS reported
DECLARED-NOT-MEASURED. (b) sensitivity -- removing `_retrieval_cells()`
(a real derivation stage) from the input strictly reduces the exercised
count (195 -> 110). Both hold: `red_on_command=True sensitivity=True`.

**Per-check discrepancy rule (acceptance item 3)**: `find_declared_not_
measured()` exact-matches each registered check's declared `coverage`
lists against this grid's own axis vocabulary; a check whose declared
slice (cartesian product of matched values) contains an unexercised cell
is flagged by name. Proven correct via the fault-twin above (a synthetic
entry that DOES match fires red). Run against the REAL registry (56
checks): 0 findings -- honest and expected, since every existing check's
`coverage` prose predates this vocabulary and uses its own free-text
descriptions instead. Not a gap in the mechanism; a gap in adoption,
named as future work (existing checks could migrate their coverage
declarations to this grid's vocabulary over time).

**Trend file + ratchet (acceptance item 4)**: `logs/coverage_trend.jsonl`,
one JSONL record per run (same append-only pattern as item 2's survivor
trend, gitignored the same way). `check_coverage_ratchet()` fails a
fraction DECREASE unless the debt register contains the marker phrase
"coverage decrease accepted" -- same "must be named, not just present"
discipline as the harness's own `--accept` convention, simplified to a
single marker since this is one aggregate number, not a per-cell list.
Its own fault-twin (`coverage_ratchet_self_test`) proves all four
directions: unaccounted decrease RED, debt-flagged decrease GREEN, no-
decrease GREEN, no-previous-record bootstrap GREEN.

**Wired into the AUDIT block** (`eval/harness.py`, not a new file --
acceptance item 1 says "the AUDIT block prints", so this extends that
exact block, right after the existing four-part-roster/probes/fault-
injection scenarios), unconditionally, same placement discipline as
MUTATION-SCORE: `AUDIT:COVERAGE-GRID` (SERIOUS, prints all five required
elements: total valid cells, exercised count, fraction, uncovered-cell
list, invalid-by-design list, each with an announced print budget so a
truncation is never silent), `AUDIT:COVERAGE-GRID-RATCHET` (SERIOUS, the
decrease check), `AUDIT:COVERAGE-GRID-SELFTEST` (ABSOLUTE, both fault-
twins' self-tests). AUDIT-category scenarios are the auditor, not audited
subjects (confirmed: `AUDIT:four-part-roster`/`probes`/`fault-injection`
have no check_registry.py entries either) -- no registry entry needed for
these three.

**Verification, two ways, since `--full` is forbidden this session**:
(1) Direct invocation -- every function called standalone (`derive_
exercised`, `measure`, `format_report` at two different budgets to prove
truncation announces itself, `find_declared_not_measured` against the
real registry, `coverage_fault_twin_self_test`, a real trend-file
bootstrap-then-second-write round trip, `coverage_ratchet_self_test`) --
all pass, reported in full above. (2) `--layer 7` (permitted; AUDIT
already runs unconditionally on every mode, confirmed by reading `eval/
harness.py` before assuming otherwise) via `scripts/run_harness.sh`: the
real harness printed the identical five-element report, `AUDIT` grew from
3/3 to 6/6 (the three new scenarios), all three PASS, `RATCHET PASS -- no
scenario regressed vs baseline`.

**What this update does NOT do**: run `--full` (forbidden -- named as
outstanding, not assumed clean, same as item 2's own note); expand
exercised-cell derivation beyond the representative sample described
above; reconcile the discrepancy with the REQ's own illustrative validity
example beyond flagging it (Bill's call whether the code or the example is
wrong -- this build trusts the code, since the code is the ratified rule
the REQ itself points to); mark this REQ MET.

**This REQ's acceptance items 1-8 are now ALL built and passing**
(Metric 1: 1-4 this update; Metric 2: 5-8, item 2 of this sprint). Status
stays NOT MET -- this reports readiness, Bill decides. Outstanding,
named rather than assumed: `--full` verification (this sprint's FORBIDDEN
list only permitted `--layer 7`); TD-133/TD-134 survivor burn-down (a
separate item in this same sprint, not this REQ's acceptance test at
all); the illustrative-example discrepancy above.

## UPDATE 2026-07-28: MET, per DISPATCH_44

Of the two things named outstanding above, both are now closed:
- The illustrative-example discrepancy was resolved by DISPATCH_30
  (2026-07-27, commit `24948b9`) -- see the RULING paragraph earlier in
  this doc. Re-confirmed live at today's `HEAD` (post-Dispatch 43, which
  touched `REQ_PARTITION_CUSTODY` again after DISPATCH_30 landed):
  `coverage_grid.valid_cells()`/`invalid_cells()` re-executed fresh
  reproduce `total=2380 valid=2170 invalid=210`, same 6 `(scope,
  attribute)` pairs -- unchanged, the ruling still holds.
- The `--full` run named outstanding here is
  `/tmp/hip_harness_20260728_0514.log`, confirmed genuine by its own
  header (`"HIP verification harness — full (L1-L4, 100 iters)"`) --
  `docs/dispatches/DISPATCH_44__four-req-met-assessment-against-full-run__v20260728_1023.md`
  re-verified all 8 acceptance items against it directly:
  - Item 1 (five printed elements on `--full`): `total valid cells: 2170`,
    `exercised: 195`, `fraction: 0.090`, invalid-by-design (210) and
    uncovered (1975) both printed with explicit "exceeds print budget,
    see X" pointers -- announced truncation, not silent.
  - Items 2-4 (fault twin + ratchet): `COVERAGE-GRID-SELFTEST PASS`,
    `twin_red=True twin_sensitivity=True (195->110) ratchet_red=True
    ratchet_green_flagged=True ratchet_green_nodecrease=True
    ratchet_bootstrap=True`; real ratchet `COVERAGE-GRID-RATCHET PASS`,
    `no decrease: 0.090 -> 0.090`.
  - Items 5-7 (mutation-score report, self-test, no-silent-disappearance):
    full per-module dump present (`OVERALL: 101/128 killed (score=0.79)`),
    `MUTATION-SCORE-SELFTEST PASS`, `MUTATION-NO-SILENT-DISAPPEARANCE
    PASS`, `MUTATION-NO-SILENT-DISAPPEARANCE-SELFTEST PASS`.
  - Item 8 (no regression): `RATCHET PASS — no scenario regressed vs
    baseline.` at the end of the log.

Marking MET here exercises "Bill decides" directly, per DISPATCH_44's own
explicit instruction to do exactly that for any REQ whose items all hold.
