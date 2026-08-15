# DISPATCH_CEILING_ACCEPTANCE_AUDIT
Status: BUILT
Reconciled-Against: ae87034 (HEAD at dispatch start)
REQ: `docs/requirements/REQ_CEILING_ACCEPTANCE__testing-plan-for-the-ceiling-sprint__v20260801_0617.md` (authority resolved via INDEX + LATEST symlink) and `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` R7
Dispatch: D-86, 2026-08-01
**Status proposed: NONE. No requirement ruled MET. No tier reassigned.**

## What was asked, and what happened

Audit all 30 ceiling acceptance rows, then wire the 5 LIVE and 7 STRICT XFAIL rows in
order, **stopping at the first ambiguity**. The audit ran. **A7 was wired. A11 — the
second row in the wiring order — is a stop condition, so nothing after it was written.**

Bill is away; per the dispatch, I stopped and wrote the report rather than waiting or
guessing.

## The audit — 3 of 30

Full table: `/tmp/d86_ceiling_acceptance_audit.md` and §6 of the acceptance REQ.

**Three rows had an executable check: A18, A29, A30.** The five runner files the plan names
(`test_ceiling_representation.py`, `test_ceiling_audience.py`, `test_ceiling_solicitation.py`,
`test_ceiling_inference.py`, `test_ceiling_retention.py`) — **none existed.** A18's absence
was found at D-81 and A10's at D-84; D-86 establishes the pattern was universal, not
two isolated misses.

**In fairness: the plan never claimed they were wired** — *"This is a plan, not a ruling…
12 of 30 rows CAN be wired now."* The gap is in the system. The one genuinely stale entry
is A18.

### A methodological correction made before counting

A naive `grep "\bA[0-9]+\b" eval/` reports A1–A5 hits in three unrelated files. **Four
independent A-numbering schemes collide here:** ceiling A1–A30; care-coordination A1–A4
(`eval/care_coord_run.py:26`); demo-smoke A1–A4 (`eval/test_demo_smoke.py:132`); and L5
red-team A1–A5 (`eval/harness.py:9`). Counting any of them would have overstated coverage
by four rows. Same hazard family as the standing caution against source regexes: a name
match is not a semantic match.

### Claim verification

Every factual claim the plan makes about *why* a row is red or vacuous was re-verified at
HEAD rather than inherited. **All held except A11.** Verified: A7 (no reasoning-trace
persistence), A1 (`DERIVABLE_ATTRIBUTES` absent), A19 (retraction clears no embedding),
A20 (`check_training_example` exists; no export/evaluation gate), A21 (no retention
mechanism), A26 (`apply_decline` exists; non-response unmodelled), A27 (no objective keyed
on acceptance), A10 (`encode()` performs none of R10's four checks).

## STOP-1 — A11

**The plan's rationale and fixture are falsified at HEAD.**

It says A11 *"passes because no promotion path exists"* and specifies an *"import-graph scan
proving no code path rewrites a member-owned fact's `owner`/scope to `household` or a
care-team scope."*

Promotion paths exist and are ratified: `share_household` → `CLASS_HOUSEHOLD` with owner
rewritten to `"household"` (`harness/write_rule.py:160-168`); `share_care_team` (`:170-179`);
`flag_safety` (`:181+`); and the attribute default (`:191`, `harness/fact_change.py:693`).

**R11 is still satisfied — by a CONTROL, not by absence.** The household-circle widening
restriction ratified 2026-07-21 (`write_rule.py:161-167`) permits widening only when
`subj is None or subj == author`, otherwise falling through without widening; care-team
paths additionally require `is_recipient` **and** `is_active_caregiver`; plus mandatory
subject-exclusion.

**Why it blocked the row.** Writing the specified fixture produces a check that is red on
arrival against correct behavior, whose only green path is deleting a ratified feature.
Writing the *right* check — a behavioral assertion that a third-party claim does not widen
while a self-claim does — is a different assertion than the plan authorizes. **Bill rules;
I did not substitute.**

Recommendation recorded for that ruling: re-specify A11 behaviorally. It would be one of
very few ceiling rows asserting a control that **actually exists**. And A11 is **not**
"vacuously true today" — that holds for A7 and A27, not for A11.

## What was wired — A7 only

`eval/test_ceiling_representation.py`, 10 cases, green; registered in `scripts/run_harness.sh`.

Written as a **regression tripwire and labelled as one in its own docstring** — it holds by
ABSENCE (nothing refuses a reasoning-trace write; nothing ever attempted one), so its value
is catching the commit that introduces one, not present assurance.

House discipline: **AST, never a source regex**, with
`test_a7_scanner_ignores_comments_and_docstrings` asserting the D-75 defect directly (that
dispatch's first A29 guard fired on its own explanatory comment). Four-part discipline —
fault twin **executed** (red-on-command demonstrated, not asserted); hand-authored fixture;
runner entry; metamorphic variants covering renames and aliased imports. Plus
`test_a7_scan_actually_covered_the_packages`, guarding the vacuous pass where a scan walking
zero files reports no offenders.

**Verified, not rebuilt** (per instruction): A29/A30 (D-75) and A18 (D-81).

## Two findings recorded for Bill

1. **A18's tier is stale** — classified STRICT XFAIL, actually LIVE and passing since D-81.
   Not silently re-tiered. R18 remains **NOT MET** (TD-139/140/141): a passing row does not
   carry its requirement, exactly as already recorded for A30.
2. **A29/A30 have a fault-twin gap.** The plan calls the AST guard "the twin"; by
   `REQ_HARNESS_DISCIPLINE`'s definition — *"the specific mutation that turns the check
   red"* — it is a guard, not a twin, because no mutated consumer is executed. A18's and
   A7's twins both are. A gap in those rows' coverage, not a defect in the registry.

## Harness

```
standing batteries (7 files): 103 passed, 2 xfailed
== AUDIT:  8/8   (0 flaked, 0 skipped)
== DISC:   1/1
== L7:     27/27 (0 flaked, 0 skipped)
== L7V2:   27/28 (0 flaked, 1 skipped — CT-OUTPUT-GAP, opt-in by design)
== SCHEMA: 1/1   == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.
```

**No ABSOLUTE-tier check red. 0 scenario FAILs.** `--full` was not attempted; the TD-129
memory guard refused it at D-81 on this same machine state and the dispatch asked for
`--layer 7`.

## Files changed

| File | Change |
|---|---|
| `eval/test_ceiling_representation.py` | NEW — A7, 10 cases, twin + metamorphic + anti-vacuity |
| `scripts/run_harness.sh` | A7 battery registered (7 batteries now) |
| `REQ_CEILING_ACCEPTANCE__…v20260801_0617.md` | §6 appended — execution state only; §§1-5 untouched |

## Not done, deliberately

A11 (stopped), A27 and the seven STRICT XFAIL rows (downstream of the stop, per the
dispatch's ordering), A12/A16 and the 16 UNWRITABLE rows (out of scope by instruction).
`~/hip-vo`, `~/hip-dev`, `~/hip-harness` untouched.
