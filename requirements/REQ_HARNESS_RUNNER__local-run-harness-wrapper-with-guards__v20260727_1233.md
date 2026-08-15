# REQ_HARNESS_RUNNER
Status: MET — **AMENDED HA-25, 2026-08-10** (§'THE EXIT-CODE RULE'): records Bill's
2026-08-09 exit-code ruling built at HA-24. Acceptance unchanged; status unchanged.
Reconciled-Against: main 5f95c13 (2026-07-27, local, unpushed at the time --
now on origin/roadmap, confirmed 2026-07-28); MET per DISPATCH_44 below

## VERIFICATION (2026-07-27, same session)

scripts/run_harness.sh written, chmod +x, and tested three ways as specified:

1. Normal `--layer 7` run from `~/hip-roadmap`: sourced `.env.dev` +
   `~/.zshrc`, `GROQ_API_KEY`/`NEO4J_PASSWORD` both resolved from the shell
   env (already set by `~/.zshrc`; the plist fallback path exists but
   wasn't exercised live since it wasn't needed this run), port 7688 was
   already listening so the neo4j-dev-start path wasn't exercised live
   either, invoked `$HIP_DEV_PYTHON eval/harness.py --layer 7`, teed to
   `/tmp/hip_harness_20260727_1238.log`, printed that path. Result: AUDIT
   3/3, DISC 1/1, L7 24/24, L7V2 25/26 (1 expected opt-in skip,
   CT-OUTPUT-GAP), SCHEMA 1/1, VOICE 1/1, **RATCHET PASS — no scenario
   regressed vs baseline.**
2. Run from `/tmp` (not a git repo) and from `~/hip-vo` (a real, different
   repo): both refused before sourcing anything, exit 1, correctly named
   the actual toplevel found (`<not a git repo: /tmp>` and
   `[REDACTED-USER-PATH]/hip-vo` respectively).
3. `--full` attempt: free memory on this box was genuinely under 2GB at
   test time (real condition, not simulated — 0.53GB free per `vm_stat`),
   so the refusal was proven against real conditions. Refused before
   `eval/harness.py` was ever invoked, named TD-129 by ID, printed the
   measured figure (0.53GB). No real `--full` run occurred, per the
   standing FORBIDDEN list.

One build-time bug found and fixed: the script was first written with a
bash shebang; `~/.zshrc` uses zsh-only builtins (`setopt`) and sourcing it
under bash failed outright (exit 127) before reaching any guard. Switched
to `#!/usr/bin/env zsh`; all three tests above are from the corrected
version.

Two-line usage note added to
`docs/deliverables/HIP_OperationsRunbook__how-to-run__v20260726_1606.md`
under "Running the gate", MANIFEST updated in the same commit per the
Document Governance Rule.

This reports readiness. Per the standing FORBIDDEN list, this REQ is not
being marked MET -- that is Bill's call.

## THE REQUIREMENT

Bill's own words, verbatim, from the environment block and Item 1 of a
five-item sprint instruction (2026-07-27):

> Environment: cd ~/hip-roadmap && source .env.dev && source ~/.zshrc;
> GROQ_API_KEY from ~/Library/LaunchAgents/com.hip.demo.dashboard.plist via
> PlistBuddy; run under $HIP_DEV_PYTHON. If 7688 is not listening:
> NEO4J_HOME=$HOME/neo4j-dev NEO4J_CONF=$HOME/neo4j-dev/conf
> /opt/homebrew/opt/neo4j/bin/neo4j start

> Write scripts/run_harness.sh, executable, committed, registered.
> It must: refuse unless the git toplevel is [REDACTED-USER-PATH]/hip-roadmap,
> naming where it actually is; source .env.dev and ~/.zshrc; pull
> GROQ_API_KEY from the demo dashboard plist; refuse by name if
> NEO4J_PASSWORD or GROQ_API_KEY is still empty; check 7688 is listening
> and start ~/neo4j-dev if not, polling until it accepts connections or
> timing out with a clear message; refuse --full when free memory is
> under 2GB, naming TD-129 and printing the figure; pass all arguments
> through to eval/harness.py under $HIP_DEV_PYTHON; tee to
> /tmp/hip_harness_$(date +%Y%m%d_%H%M).log and print the path.
>
> Test three ways before committing: a normal --layer 7 run, a run from
> the wrong directory (must refuse), a --full attempt under the memory
> threshold (must refuse). Report what each did.
>
> Add a two-line usage note to docs/deliverables/HIP_OperationsRunbook.
> Report the hash.

## AMENDMENT — THE EXIT-CODE RULE (HA-25 rider, 2026-08-10)

**Added by HA-25's one-line rider, recording the contract HA-24 built.** Bill's ruling,
2026-08-09, verbatim:

> **"Binding tests all pass -> exit 0. Live-model reds -> loud warning and log, not a
> failing exit. Any binding failure -> non-zero."**

**BINDING:** the standing pytest batteries, plus `L7`, `L7V2`, `AUDIT`, `DISC`, `SCHEMA`,
`VOICE`, and the ratchet over them. **LIVE-MODEL:** `L1`, `L2`, `L3`, `L4`, `L6` — reported,
never gating, until a reproducibility rule is set from collected data (CLAUDE.md
Requirements Discipline item 12, as amended 2026-08-09 at HA-20).

When live reds coexist with a green binding set, the runner prints exactly:

```
BINDING TESTS PASS. LIVE-MODEL TESTS HAVE FAILURES — SEE RUN LOG.
```

**Why this amendment exists at all.** This REQ's original scope is the runner's
PRECONDITIONS AND REFUSALS — git toplevel, env vars, the memory threshold. It said nothing
about what the runner's exit status *means*, so when item 12 was amended the exit code kept
failing on non-gating layers and two dispatches (HA-20, HA-22) had to tell readers *"read
the layer lines, not the exit code."* **HA-24's build is recorded here so the runner's exit
contract has a REQ home rather than living only in a dispatch doc.**

**Implementation note, so the next reader does not look in the wrong file:** the
binding/live classification lives in `eval/harnesslib/reporter.py`, where a scenario's layer
is known. `scripts/run_harness.sh` documents the contract and propagates the status via
`pipefail`. Proven three ways at HA-24 — binding green + live red → exit 0 with the line;
a broken binding test → non-zero with the line absent; all green → exit 0, no line.

**Status is unchanged: MET.** This records a ruled behaviour of the same script; it does not
reopen the acceptance above.

Standing constraints from the same instruction, quoted in full because they
bound how this must be built and tested:

> FORBIDDEN, no exceptions, Bill is away:
> - No --full. Layer 7 only.
> - No demo_preflight.sh, no demo_reset, no demo_seed, no graph reset or
>   reseed. Graph 7688 holds the 11 v2 facts that ARE the operator-blind
>   proof. Destroying them destroys the evidence.
> - No touching any .master_key, no key destruction, no force-push, no
>   history rewrite, no git branch deletion.
> - No marking any REQ MET. Report readiness; Bill decides.
> - If Layer 7 regresses any existing scenario, STOP and report rather
>   than adjusting the scenario.

Amended in a later message the same day:

> Revised gate: proceed when `git status --short` is clean. Ignore HEAD
> versus origin entirely.
>
> ONE ADDITION TO THE STANDING RULES: DO NOT PUSH. Commit each step as
> instructed, but push nothing. This tree holds an unpushed commit Bill
> has not reviewed, and any push from here carries it along. Bill pushes
> when he is back.

Expanded: this is docs/deliverables/, business/, and scripts/-adjacent
tooling work (a new operations script), not a change to governed product
code, but it is still a code change under Requirements Discipline item 8 and
gets a REQ. No REQ existed for this specific ask when the five-item sprint
message arrived; this document is written first, from the words above,
before any script code is touched, to close that gap rather than bypass it.

## THE ACCEPTANCE TEST

1. From `[REDACTED-USER-PATH]/hip-roadmap`, running `scripts/run_harness.sh
   --layer 7`: sources `.env.dev` and `~/.zshrc`; if `GROQ_API_KEY` is
   still empty after that, resolves it from
   `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` via `PlistBuddy`;
   refuses by name (printing which variable(s)) if `NEO4J_PASSWORD` or
   `GROQ_API_KEY` is still empty after that; confirms port 7688 is
   listening, starting `~/neo4j-dev` and polling for it if not; invokes
   `"$HIP_DEV_PYTHON" eval/harness.py --layer 7`; tees combined output to
   `/tmp/hip_harness_<YYYYMMDD_HHMM>.log`; prints that log path.
2. Running `scripts/run_harness.sh` (any arguments) from any directory
   whose `git rev-parse --show-toplevel` is not exactly
   `[REDACTED-USER-PATH]/hip-roadmap` exits non-zero before sourcing any
   environment file or touching Neo4j, and prints the toplevel it actually
   found (or that none exists).
3. Running `scripts/run_harness.sh --full` when free memory is (real or
   simulated) under 2GB exits non-zero before `eval/harness.py` is
   invoked, names TD-129 by ID, and prints the measured free-memory
   figure. Per the standing FORBIDDEN list, this build's own testing may
   only exercise this refusal path — a real `--full` run is never allowed
   to execute during this REQ's verification, regardless of actual free
   memory on this box at test time.
4. `docs/deliverables/HIP_OperationsRunbook` (current version) gains a
   two-line usage note for the script, committed in the same or a
   following checkpoint.
5. The script is executable (`chmod +x`), committed, and registered in
   `docs/INDEX.md` per this repo's doc-registration convention.
6. All of the above is verified by direct invocation and output
   inspection, not by reading the script and asserting it should work.

## WHAT'S ALREADY DONE

- `eval/harness.py` and `eval/harnesslib/` exist and are the real
  invocation target; not being rebuilt here.
- `.env.dev` exists at repo root and defines `HIP_DEV_PYTHON` (verified:
  `export HIP_DEV_PYTHON="$HOME/hip-dev/.venv/bin/python"`).
- `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` exists.
- `scripts/run-harness.sh` (hyphenated, pre-existing, 155 bytes) already
  exists but SSHes to a remote box (`[REDACTED-USER]@[REDACTED-TAILNET-ADDRESS]`) and runs
  `eval.harness` there against a different checkout (`~/hip-dev` on that
  host) with a hardcoded `NEO4J_URI`. It does not do any of the local
  guard work this REQ asks for and is not being modified, replaced, or
  reused by this build -- left exactly as found.
- `docs/deliverables/HIP_OperationsRunbook__how-to-run__v20260726_1606.md`
  exists as the current runbook version to append the usage note to.

## WHAT'S KNOWN BROKEN

No local, self-contained harness runner exists that enforces the
guardrails Bill specified. Running `eval/harness.py` directly today
requires a human to remember to source `.env.dev` and `.zshrc`, manually
resolve `GROQ_API_KEY` from the plist if the shell doesn't already have it,
manually confirm Neo4j is up on 7688, and manually avoid running `--full`
under memory pressure (the resource-contention condition TD-129
describes: two `ollama` daemons plus harness load competing for the same
box). There is no refusal path today if any of those preconditions are
missing; a harness invocation just fails partway through or, worse,
proceeds against unintended state.

## CONSTRAINTS

- No `--full` execution, real or accidental, during this build or its
  verification. Layer 7 only. The `--full` refusal path must be provable
  without ever letting a real `--full` run reach `eval/harness.py`.
- No touching `demo_preflight.sh`, `demo_reset`, `demo_seed`, or any graph
  reset/reseed path. Graph 7688 holds the 11 v2 facts that are the
  operator-blind proof; this build must not write to, reset, or reseed
  that graph.
- No touching any `.master_key`, no key destruction, no force-push, no
  history rewrite, no git branch deletion.
- **No pushing.** Commit each checkpoint locally only. The tree carries an
  unpushed commit (`5f95c13`) Bill has not reviewed; nothing from this
  build may push and carry it along.
- No marking this REQ, or any REQ, MET. This document reports readiness;
  Bill decides.
- If running the harness under this script regresses any existing Layer 7
  scenario, stop and report rather than adjusting the scenario.

## UPDATE 2026-07-28: MET, per DISPATCH_44

The "Bill is away" FORBIDDEN list this REQ was built under (no push, no
marking MET) has since lifted: `5f95c13` is now on `origin/roadmap`
(`git merge-base --is-ancestor 5f95c13 origin/roadmap` confirms it), and
`HEAD`/`origin/roadmap` are in sync (0 ahead, 0 behind) as of this update
— pushing has resumed as normal practice across several dispatches since.
Marking MET here is a direct exercise of "Bill decides," per
`docs/dispatches/DISPATCH_44__four-req-met-assessment-against-full-run__v20260728_1023.md`'s
own explicit instruction to do exactly that.

All 6 acceptance items hold:

1. Normal `--layer 7` run via `scripts/run_harness.sh` — live-verified in
   the VERIFICATION section above (2026-07-27); today's
   `/tmp/hip_harness_20260728_0514.log` matches the script's exact tee
   naming convention, corroborating it's still what produces this log.
2. Wrong-directory refusal (from `/tmp` and `~/hip-vo`) — live-verified
   2026-07-27; script unchanged since (`git log -- scripts/run_harness.sh`
   shows only `e13646e`, Jul 27 12:37).
3. `--full` refusal under real 2GB-free pressure (0.53GB measured), naming
   TD-129 — live-verified 2026-07-27.
4. Runbook two-line usage note — confirmed present today,
   `docs/deliverables/HIP_OperationsRunbook__how-to-run__v20260726_1606.md:34`.
5. Executable, committed, registered — confirmed: `-rwxr-xr-x`, commit
   `e13646e`, `docs/INDEX.md`.
6. Verified by direct invocation and output inspection, not just read —
   confirmed per the VERIFICATION section's three live tests.

Items 2-3's evidence is dated 2026-07-27, not re-exercised by today's
normal run (a wrong-directory or low-memory refusal isn't triggered by a
successful full/layer-7 run); named explicitly rather than implied as
re-proven today.
