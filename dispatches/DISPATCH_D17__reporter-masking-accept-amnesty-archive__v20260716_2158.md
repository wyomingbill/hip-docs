# DISPATCH_D17
Status: BUILT
Reconciled-Against: (see commit for hash)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_D17__reporter-masking-accept-amnesty-archive__v20260716_2158.md`

## THE ASK

Bill's dispatch, verbatim:

> "D-17. Fix it.
>
> REQ doc first, per CLAUDE.md. Dispatch doc per the register at 16426b0.
>
> THE DEFECT (from your own analysis, registered as D-17): the reporter
> masks regressions behind brand-new failures. A scenario that was passing
> and now fails gets hidden if a different scenario fails for the first
> time in the same run.
>
> WHY THIS IS FIRST: every green result from the last two days is suspect,
> including the three fixes verified today. ORTH-1 sat red in the baseline
> for a full day announcing nothing, and this is how. A gate that can hide
> a regression is not a gate.
>
> You flagged the cost yourself: it alters ratchet exit-code semantics. So:
>
> 1. Report exactly what the exit codes change TO, before you change them.
> 2. Find everything that reads them — scripts/, dev.sh, CI, anything. List
>    it. If something breaks, I want to know before it does.
> 3. Then fix it.
> 4. Then run --full on main and report whether anything WAS being masked.
>    That number matters more than the fix: if nothing was hidden, the last
>    two days of results stand. If something was, every result needs
>    re-reading.
>
> Also in scope, same defect class, from the risk memo §7:
>    - `--accept` grants permanent amnesty with one string. Known failures
>      carry no expiry and no linked defect ID. Nothing distinguishes
>      "accepted with justification" from "forgotten." Require an expiry or
>      a defect ID.
>    - harness.py:226 truncates harness_run.jsonl at the next run's
>      startup, destroying the previous run's gate evidence. Archive
>      harness_run.<ts>_<commit>.jsonl before truncating.
>
> Verify before reporting. Push, report the hash."

## WHAT WAS DONE

1. Filed `REQ_D17` before any code, per CLAUDE.md item 8.
2. **Reported the exit-code change before writing it** (Bill's step 1):
   traced `apply_baseline`'s exact current control flow, determined the
   ONLY behavior change would be the regression+brand-new-simultaneous
   case (2→1, gains a second printed line), every other case byte-identical
   — written into the REQ before touching `reporter.py`.
3. **Enumerated every exit-code consumer** (Bill's step 2): grepped
   `scripts/`, `dev.sh`, checked for CI config (none exists), checked
   `eval/integration_live.py`'s separate ratchet for the same bug class.
   Found: `scripts/auto-gate.sh` (checks `==0` only, unaffected),
   `scripts/run-harness.sh` (blind SSH forward, unaffected),
   `scripts/gate_check.sh` (doesn't call `eval.harness` at all, not a
   consumer), `dev.sh` (not a consumer). No CI. `integration_live.py` has
   no `brand_new` concept, structurally cannot share this bug.
4. Fixed `eval/harnesslib/reporter.py::apply_baseline`: `regressions`
   checked before `brand_new`; both printed when both present; regression
   wins the exit code (1).
5. Fixed the `--accept` amnesty gap: added `_ACCEPT_ID_RE`/`_ACCEPT_EXPIRY_RE`,
   refuse `--update-baseline --accept "<bare string>"` the same way an
   unjustified update is already refused.
6. Fixed `eval/harness.py:226`'s unconditional truncation: archive
   `harness_run.jsonl` to `harness_run.<ts>_<commit>.jsonl` before
   truncating, only when the file has content.
7. **Ran `python -m eval.harness --full` live on `main`** (Bill's step 4) —
   found and root-caused 5 real regressions the old code would have hidden
   behind `L6:record-invariants`'s brand-new status. Registered D-19
   through D-22. Did NOT fix them (out of this REQ's scope) and did NOT
   update the baseline to accept them away.
8. Registered D-17 as FIXED with the full live-run evidence; updated
   MANIFEST, INDEX, ORDER section (D-20/D-22 promoted ahead of the
   pre-existing priority list — they're live-wrong on `main` right now).

## WHAT WAS FOUND

- `eval/harnesslib/reporter.py:130-190` (pre-fix): `brand_new` checked and
  `return 2`'d before `regressions` was ever printed or read.
- `eval/harnesslib/reporter.py:154-159` (pre-fix): `_accepted` stored any
  non-empty string, no format requirement.
- `eval/harness.py:226` (pre-fix): `_harness_run_log.write_text("")`,
  unconditional, no archive.
- **The big one**: `eval/harness_baseline.json` has NO `L6:*` entries at
  all — every L6 scenario has been "brand new" on every single run since
  Layer 6 was added, meaning the masking condition has been LIVE and
  reachable continuously, not a one-time historical fluke. Confirmed by
  `grep -n "L6" eval/harness_baseline.json` returning nothing.
- D-19/D-20/D-21/D-22: see `HIP_DefectRegister__v20260715_1930.md` for
  full file:line detail on each; not restated here.

## VERIFIED

**Watched run:**
- Synthetic unit-level Reporter tests (regression+brand-new together, pure
  regression, pure brand-new, clean) — all four exit codes/print behaviors
  confirmed directly against the real `Reporter.apply_baseline`.
- `--accept` refusal and acceptance, both live, both against the real
  `apply_baseline`, baseline file read back to confirm byte-state.
- Archive logic, directly against a scratch file with real multi-line
  content, read back to confirm byte-identical archived content.
- **`python -m eval.harness --full`, run live and in full on `main`** — not
  simulated, not inferred. Full stdout captured; `L1:P10`'s specific
  failing check re-run in isolation (`--layer 1`) to get the exact
  sub-assertion detail truncated out of the first run's tail-piped output.
  `is_declarative_utterance` re-run directly against the exact
  `routing_showcase.T02`/`T03` query strings to confirm the D-20 root
  cause rather than infer it from the symptom alone.

**Reasoned about:**
- The precise numeric exit code of the live `--full` run itself was not
  captured (the command was piped through `tail -150` for output-length
  management, which discards the upstream exit code in a plain pipeline).
  Not re-run purely to capture the integer — the printed `RATCHET FAIL` +
  `NEW FAILURES` text pair is unambiguous given the just-verified,
  unit-tested code path: regressions non-empty → return 1. This is a
  deterministic consequence of code already directly observed working,
  not a guess about unobserved behavior.
- D-21's claim that the temp=0.2 retry ran and still failed is inferred
  from the reply text and TD-125's documented mechanism, not from reading
  a per-attempt log line for this specific turn (the retry's own attempt
  log would need `harness/fact_change.py`'s log output, not captured
  separately here).

## HASH

(filled in after commit — see commit message and `git log`)

## OPEN

- D-19, D-20, D-21, D-22 are registered, root-caused, and explicitly NOT
  fixed. Each needs its own REQ before any code changes, per CLAUDE.md
  item 8 — same discipline this dispatch itself followed.
- The baseline (`eval/harness_baseline.json`) was deliberately left
  unchanged. Every `--full` run on `main` until D-20/D-22 are fixed will
  continue to show `RATCHET FAIL` — this is intentional, not an oversight.
- `L6:*` scenarios have never been added to the baseline at all (separate
  from D-17, arguably its own small gap — REQ_HARNESS's own Phase 1
  scope). Until they are, every run's L6 result reads as brand-new,
  which is harmless now that regressions print alongside it, but is still
  worth closing so L6 has a real baseline instead of permanently novel
  status.
- Whether `eval/integration_live.py`'s separate ratchet has OTHER defects
  of its own was not investigated beyond confirming it doesn't share D-17's
  specific bug — out of scope for this dispatch.
- The precise numeric exit code for the live `--full` run itself was not
  captured directly (see VERIFIED); if that specific number matters for a
  future audit, re-run without piping through `tail`.
