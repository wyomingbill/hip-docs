# DISPATCH_D36 — verify Fable's three Curator findings

Status: BUILT
REQ: NONE — analysis/verification dispatch. It reproduces claims made by an
external reviewer against committed code and changes nothing. Per Requirements
Discipline item 10, an ANALYSIS dispatch may carry REQ: NONE and must say why;
this is that statement. The FIXES arising from it are dispatched separately
(D-37) and carry their own REQ, as item 8 requires.
Branch: roadmap
Reconciled-Against: f30ecd5 (2026-07-30); gate under test
harness/learner_isolation.py unchanged since 82e86a9 (D-30); live registry
read from data/registry.db (read-only URI)

Gate: PASSED (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap).
Lock: graph+harness, taken and released. **No code changed. No REQ assessed.**
Run twice, ~15 minutes apart, with identical results both times; the second
run re-confirmed HEAD, tree cleanliness, and that the gate file had not moved
before re-executing.

## What this dispatch was

D-35 captured two independent Fable reviews
(`docs/reviews/FABLE_CuratorReview__test-model-and-gate-code-review__v20260730_0801.md`)
and filed them explicitly UNVERIFIED. This dispatch verifies three of their
findings — the two both reviewers converged on plus the one schema claim —
by reproduction rather than by re-reading. Everything below is a measurement
taken this session, not a restatement of the review.

## Result: 3 of 3 CONFIRMED

### (a) EMPTY-AUDIENCE BYPASS — CONFIRMED (7th hole)

Reproduced live against the committed gate with an injected fixture resolver,
the same call shape `eval/test_learner_isolation_adversarial.py` uses.

| case | target audience | verdict |
|---|---|---|
| CONTROL member-private(alice) | `{alice,bob,mary}` | **VIOLATION** (correct — battery case c1) |
| ATTACK member-private(alice) | `frozenset()` | **ADMISSIBLE** ← the crossing is admitted |
| SWEEP household-circle | `frozenset()` | **ADMISSIBLE** |
| CONTRAST member-private(alice) | `None` | **VIOLATION** (fail-closed fires) |

EVIDENCE LINE — `harness/learner_isolation.py:286`:

    if ex_aud is None or tgt_aud is None:

The branch tests identity with `None`. An empty `frozenset()` is not `None`,
so it skips fail-closed and reaches `:292`:

    unauthorized = frozenset(tgt_aud) - frozenset(ex_aud)

`frozenset() - anything == frozenset()` → no unauthorized readers → admit.
One declared field admits every scope in the household, member-private
included. The `None` contrast case is what proves this is specifically an
empty-vs-None defect and not a broken containment check.

**Root cause, and why it is a 7th hole rather than a variant of the first
six:** D-30 authenticated the EXAMPLE side of the comparison (household and
audience derived from an un-forgeable `fact_id`) and left the TARGET side
exactly as D-25 found the example side — caller-supplied, never derived,
never validated. `target["household_id"]`, `target["audience"]`, and
`target["model_id"]` are read straight from the caller's dict at `:260` and
`:285`. The 23-case battery contains no target-forgery case at all: all five
targets are hand-written module constants whose audiences are true by
construction.

### (b) BATTERY WIRED INTO NOTHING — CONFIRMED

`eval/test_learner_isolation_adversarial.py` — the 23 cases that encode the
six D-25 holes — is executed by no runner.

EVIDENCE LINES:
- Repo-wide grep for the module name returns exactly two hits, both inside
  that file's OWN docstring (lines 9-10, the "two ways to run" note). Nothing
  else in the repository references it.
- `scripts/run_harness.sh:77` is the sole executor and runs
  `"$HIP_DEV_PYTHON" eval/harness.py "$@"` — no pytest, ever.
- `harness_audit._SCENARIO_FILES` is `("eval/harnesslib/layer7_crypto.py",
  "eval/harnesslib/layer7_crypto_v2.py")` only; `enumerate_roster`
  additionally imports `record_invariants.CHECKS`. The battery is in neither,
  so it cannot appear in `AUDIT:four-part-roster`.
- No entry in `eval/harnesslib/check_registry.py`.
- No Makefile, no `.github/`, no `.gitlab-ci.yml`, no `.circleci`, and no
  `pytest.ini` / `setup.cfg` / `pyproject.toml` / `tox.ini`.

Consequence: the 23 expectations — including the 6 that encode the closed
holes — can regress to green-by-deletion without any run turning red. The
project institutionalized the fix and left the finding mechanism unenforced.

### (c) DYAD AUDIENCE BRANCH READS COLUMNS THAT DO NOT EXIST — CONFIRMED

Verified against the LIVE database, not only the DDL.

`PRAGMA table_info(dyads)` on `data/registry.db` (read-only URI) returns
exactly six columns:

    dyad_id | recipient_ref | household_id | dyad_pubkey | status | created_at

`harness/learner_isolation.py:184-187` reads:

    members = {d.get("member_a"), d.get("member_b"),
               d.get("caregiver"), d.get("recipient")}

INTERSECTION OF THE TWO SETS: **[]** — zero of the four exist. Note the
near-miss: the table has `recipient_ref`; the code asks for `recipient`.
The actual custodians live in a different table entirely, `dyad_members`
(`custodian_member_id`, `role`, `added_at`, `removed_at`), which this branch
never reads.

RUNTIME PROOF, using a real row read from the live DB:

    _audience_of(dyad fact) -> frozenset()
    is None (fail-closed)?  False        <- empty, so fail-closed does NOT fire

CURRENCY, same branch: `get_dyad` is `SELECT * FROM dyads WHERE dyad_id = ?`
with no status filter, and an exited dyad still resolves — there is a real
`status='exited'` row in the table today. Its two siblings in the same module
both filter (`get_active_dyad_for` requires ACTIVE; `get_dyad_for_recipient`
requires `status='active'`), and the other two audience branches both bind to
live tables with `removed_at IS NULL`. This branch filters on nothing.

## COMPOSITION FINDING — (a) + (c), stated by neither review

The two defects compose into something worse than either alone, and this was
found by verification rather than by review:

- (c) makes every dyad-private fact derive `audience == frozenset()`.
- (a) makes an empty TARGET audience admit everything.

Verified directly: an empty derived source audience against an empty target
audience yields `unauthorized = NONE → ADMISSIBLE`. Dyad-private data — the
most tightly partitioned class in the system under REQ_PARTITION_CUSTODY — is
admissible for training.

The other direction is a correctness problem rather than a security one:
against a normal non-empty target, the same branch blocks with a violation
string asserting `live source audience []`, which is a fabricated roster, not
a derived one. The error message actively misleads whoever reads it.

## What this dispatch did NOT do

No fix, no test added to the battery, no REQ assessed, nothing committed
beyond this record. The lock was taken and released. The working tree was
verified clean before and after both runs.

## Disposition (carried into D-37)

- (a) and (b) → security fix + wiring, under a REQ, D-37.
- (c) → separate REQ/defect: different root cause (a schema-drift coding
  error in an untested branch), different acceptance. Deliberately not
  bundled with the security fix.
