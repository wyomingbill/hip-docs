# REQ_D17
Status: BUILT
Reconciled-Against: (see commit for hash)

Parent: no single REQ owns the harness itself (`REQ_HARNESS__orthogonal-e2e-
regression-per-push__v20260715_1700.md` covers Phase 1 wiring, not this).
This REQ stands alone, filed before code per CLAUDE.md gate item 8, because
D-17 and the two risk-memo §7 items are gate-integrity fixes to the harness
`eval.harness`/`eval.harnesslib.reporter` module, not new build work under
any existing REQ's scope.

Dispatch doc for this work: `docs/dispatches/` (filed alongside, per the
register at `16426b0`).

## THE REQUIREMENT

Bill's words, verbatim:

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

## THE ACCEPTANCE TEST

1. A run with BOTH a real regression (baseline expected pass, now fails)
   AND a brand-new failure (never in baseline) in the same invocation must
   print BOTH — never one masking the other — and must exit non-zero for
   the reason that actually applies (see EXIT CODE CHANGE below).
2. `python -m eval.harness --full` run on `main`, post-fix, reported
   honestly: did this specific masking bug actually hide anything across
   the runs already on file (`logs/harness_trend.jsonl`), or not. This
   number is the deliverable, not a formality.
3. `--accept "<string with no defect ID and no expiry>"` must be refused,
   the same way an unjustified `--update-baseline` is already refused
   today (non-zero exit, clear message, nothing written).
4. `--accept` with a real defect ID (`D-17`, `TD-124`, etc.) or an explicit
   expiry must continue to work exactly as before.
5. A second `--full` run must archive the FIRST run's `harness_run.jsonl`
   to a distinctly-named file before truncating, and the archived file's
   content must be byte-identical to what was in `harness_run.jsonl`
   immediately before the second run started.

**RESULTS — all five watched live, 2026-07-16:**

1. Unit-level, synthetic: a scenario set with one baseline-regressed key and
   one brand-new key, run through the real `Reporter.apply_baseline`,
   prints `RATCHET FAIL — regressed vs baseline: ['L2:foo']` AND
   `NEW FAILURES (not in baseline): ['L6:new']`, exits **1**. Confirmed the
   three unchanged cases (pure regression, pure brand-new, clean) produce
   exit 1/2/0 respectively, matching pre-fix behavior exactly. PASS.

2. **`python -m eval.harness --full` run live on `main`, post-fix.
   THIS IS THE FINDING THAT MATTERS MOST, per Bill's own framing — reported
   in full below, not summarized away.** The run printed, simultaneously:
   ```
   IMPROVED vs baseline: ['L1:P2'] — update to lock in.

   RATCHET FAIL — regressed vs baseline: ['L1:P10', 'L2:routing_showcase.T02',
   'L2:routing_showcase.T03', 'L2:three_zone_demo.T02', 'L2:three_zone_demo.T04']

   NEW FAILURES (not in baseline): ['L6:record-invariants']
   ```
   **Under the pre-fix code, this exact run would have printed ONLY the
   NEW FAILURES line and exited 2 — all five regressions above would have
   been completely invisible.** This is not hypothetical or retrospective:
   it is what happened, today, on the current state of `main`, the moment
   the fix was in place to actually show it. **Something WAS being masked.
   The number is five, right now, on this run.**

   Each of the five was traced to a specific, confirmed root cause (not
   left as "the harness said so") and registered as its own defect, since
   D-17's own fix is not the place to also fix what it reveals:
   - **D-19** (`L1:P10`) — a stale unit-test assertion in `layer1.py`,
     expecting `check_confirmation(...) == "pass"` for an utterance the
     D-03/D-18 fix (3c0cb74, shipped earlier the same day) now correctly
     classifies `"unclear"`. NOT a security regression — `"unclear"` still
     never confirms/declines anything, the property the test exists to
     guard is intact. The test's specific assertion is simply stale.
   - **D-20** (`L2:routing_showcase.T02`/`T03`) — a REAL regression in
     c86a414 (also shipped earlier the same day, item 0's F3 widening).
     `is_declarative_utterance` has no entry for imperative
     explanation-verbs ("Explain the biochemical mechanism...", "Trace how
     an oil supply shock...") in its interrogative-opener list — confirmed
     directly: `is_declarative_utterance()` returns `True` for both. Before
     c86a414 this gap was cosmetic; after it, these general-knowledge
     queries get `UNCONFIRMED_UPDATE_REPLY` instead of an actual answer.
   - **D-21** (`L2:three_zone_demo.T02`) — a live, confirmed instance of
     TD-125's own stated, already-logged risk: the temperature-0.2 detect
     retry (also shipped in c86a414) does not reach 100% recovery. Sam's
     "Dad had a fall last week..." — a genuine declarative about an
     already-seeded subject — got zero changes from Groq on BOTH the
     temp=0.0 attempt and the temp=0.2 retry, so F3 (now watching every
     declarative) substituted the unconfirmed reply. Not a new problem —
     the first concrete reproduction of one TD-125 already named.
   - **D-22** (`L2:three_zone_demo.T04`) — a REAL, more serious regression
     in 3c0cb74 (D-03/D-18, same day). The confirmation gate's
     `is_declarative_utterance`-based discriminator cannot tell "an old,
     unrelated confirmation token happens to still be pending for this
     actor" apart from "this new declarative is an attempt to resolve it."
     A genuinely new, topically-unrelated write (Jardiance) arriving 3
     turns after an unrelated park (still alive, TURN_TTL=3) got
     `"unclear"` instead of being processed — and because the confirmation
     gate runs BEFORE detection by design, the new fact was never even
     attempted: Neo4j showed 2 active rows where 3 were expected. This is
     not just a wrong reply, it is a silent write failure.

   None of D-19 through D-22 were fixed in this session — fixing them is
   out of REQ_D17's scope (a gate-integrity fix is not the place to also
   rush fixes into the same-day work it just found problems in), and the
   baseline was deliberately left unchanged so the ratchet keeps reporting
   all four as active `RATCHET FAIL`s rather than silently accepting them
   away. **Conclusion for "do the last two days of results stand": partially.
   D-17 itself and the risk-memo §7 items are sound. Item 0 (c86a414) and
   D-03/D-18 (3c0cb74) — both "verified today" per their own REQs' live
   proofs — each have one real regression this run surfaced that their own
   acceptance tests did not catch, because neither session ran the FULL
   harness ratchet against the existing L1/L2 corpus, only their own
   narrow, custom-scripted live turns. Every claim in those two REQs about
   the SPECIFIC turns they tested stands (re-verified, still true); the
   claim that shipping was otherwise safe does not — D-20 and D-22 are live
   on `main` right now.**

3. `--accept "seems flaky, ignore it"` (no defect ID, no expiry) refused
   live: `REFUSING --accept 'seems flaky, ignore it': must reference a
   defect ID...`, exit 1, baseline file byte-unchanged. PASS.

4. `--accept "D-99 known issue, tracked"` (has a defect-ID-shaped token)
   accepted live: baseline written, `_accepted` entry recorded, exit 0.
   PASS.

5. Archive logic tested directly against a scratch file with real content
   (`{"turn": 1}\n{"turn": 2}\n`): archived to
   `harness_run.<ts>_<commit>.jsonl`, content verified byte-identical via
   direct read-back; live `harness_run.jsonl` left empty and ready for the
   next run. PASS.

## EXIT CODE CHANGE — REPORTED BEFORE THE FIX (Bill's step 1)

**Today (`eval/harnesslib/reporter.py:130-190`, `apply_baseline`, non-update
path):**
```
regressions = [...]   # computed
flaky_firing = [...]  # computed and printed if non-empty
brand_new = [...]     # computed
improvements = [...]  # computed and printed if non-empty
if brand_new:
    print("NEW FAILURES...")
    return 2                    # <-- regressions is NEVER printed or read
if regressions:
    print("RATCHET FAIL...")
    return 1
return 0
```
`brand_new` is checked and returned FIRST. If `regressions` is also
non-empty in the same run, it is silently dropped — computed, never
printed, never causing a non-zero-for-that-reason exit. The exit code (2)
and the printed message both report ONLY the brand-new failure. This is
D-17 exactly as registered: reproduced live 2026-07-15/16 with
`L2:three_zone_demo.T03`/`T05` (real regressions) masked behind
`L6:record-invariants` (a brand-new layer's first run).

**After the fix:**
```
if regressions:
    print("RATCHET FAIL — regressed vs baseline: {regressions}")
    if brand_new:
        print("NEW FAILURES (not in baseline): {brand_new}")
    return 1
if brand_new:
    print("NEW FAILURES (not in baseline): {brand_new}")
    return 2
return 0
```
**The only behavior that changes:** a run with BOTH regressions and
brand-new failures. Before: prints only the brand-new message, exits 2.
After: prints BOTH messages, exits **1** (not 2) — because the docstring's
own stated priority (`eval/harness.py:26`, "0 green / 1 regression / 2 new
failure") already ranks regression as the more severe condition, and this
fix makes the code actually honor that ranking instead of silently
inverting it. A run with ONLY brand-new failures (no regressions) is
UNCHANGED: still prints the brand-new message, still exits 2. A run with
ONLY regressions is UNCHANGED: still exits 1. A clean run is UNCHANGED:
still exits 0.

**In one sentence: exit 2 becomes exit 1, and gains a second printed line,
in exactly the one case (regression + brand-new, same run) that was
previously silent about the regression. Every other case is byte-identical
to today.**

## WHO READS THE EXIT CODE — ENUMERATED (Bill's step 2)

Grepped `scripts/`, `dev.sh`, `.github/` (does not exist — no CI config in
this repo), and every `.py`/`.sh` file referencing `eval.harness` or
`apply_baseline`:

- **`scripts/auto-gate.sh:26`** — `[ "$EXIT_CODE" -eq 0 ] && QUICK_PASS="true"`.
  Only checks `== 0` vs. not. Collapses 1 and 2 into the same "not pass"
  bucket already. **Unaffected** — the only case that changes (2→1) still
  reads as "not pass" either way.
- **`scripts/run-harness.sh`** — a bare SSH wrapper (`.venv/bin/python -m
  eval.harness $*`), forwards whatever exit code results as the ssh
  command's own exit status. Nothing in the script branches on 1 vs. 2 —
  a human reads the printed output. **Unaffected.**
- **`scripts/gate_check.sh`** — does NOT call `eval.harness` at all. It
  calls three separate, older scripts (`routing_harness.py`,
  `injection_harness.py`, `integration_harness.py`) that have their own
  independent exit codes and do not go through `reporter.py`.
  **Not a consumer, not affected.**
- **`dev.sh`** — the dev voice-server launcher. No reference to
  `eval.harness` anywhere in it. **Not a consumer.**
- **CI** — no `.github/workflows/` or other CI config exists in this repo.
  **No CI consumer exists to break.**
- **`eval/integration_live.py:551-577`, `_apply_ratchet`** — a SEPARATE,
  parallel ratchet implementation (Tier L / E1-E8), not a caller of
  `eval.harnesslib.reporter`. Checked for the same defect CLASS since it
  computes its own regressions/improvements: it has no `brand_new` concept
  at all (only `regressions`/`improvements` against one baseline dict), so
  it structurally cannot exhibit D-17's specific masking bug. **Not
  affected by this fix; not a bearer of the same bug either** — noted, not
  fixed, since it's a different file with a different (simpler, two-state)
  ratchet that doesn't have the masking failure mode to begin with.
- **A human running `python -m eval.harness --full` interactively** — the
  actual primary consumer today, per every session's own workflow this
  week. Reads the printed lines and the exit code together. This is the
  consumer D-17 actually harmed (a human trusting "NEW FAILURES" was the
  whole story).

**Conclusion: no script, launchd job, or CI config branches on exit code 1
vs. 2 specifically anywhere in this repository.** The only consumer that
cares about the distinction is a human reading the terminal, and (per
D-17's own history) that human was being misled by the current behavior,
not protected by it. Nothing automated will break.

## WHAT'S ALREADY DONE

- D-17 itself is already registered (`HIP_DefectRegister__v20260715_1930.md`),
  found live during REQ_HARNESS Phase 1: "First post-fix harness run:
  L2:three_zone_demo.T03/T05 were real regressions... but the printed
  summary showed only NEW FAILURES... — the T03/T05 regression was
  silent." That finding is the basis for this REQ, not re-derived here.
- `reporter.py`'s `_known_flaky` mechanism (separate from `_accepted`) is
  unaffected by either fix in scope here.

## WHAT'S KNOWN BROKEN (before this build)

1. `apply_baseline`'s early-return on `brand_new` (line 183-185, before
   this fix) drops `regressions` on the floor whenever both occur in the
   same run — the exact bug analyzed above.
2. `apply_baseline`'s `--accept` path (lines 154-159) accepts ANY non-empty
   string as sufficient justification to permanently mark a scenario as a
   known failure — no format requirement, no expiry, no defect-ID
   cross-reference. One existing entry
   (`eval/harness_baseline.json:_accepted."L1:P2"`) happens to mention
   `TD-124` in its prose, but nothing enforces that; a future `--accept
   "seems flaky"` would be accepted exactly as readily.
3. `eval/harness.py:226`, `_harness_run_log.write_text("")` — unconditional
   truncation at the start of every run, before that run's own Layer 6
   evidence is written. The previous run's `harness_run.jsonl` (what Layer
   6 actually evaluated last time) is gone the moment the next run starts,
   with no archive.

## CONSTRAINTS

- Must not change exit-code behavior for any case except regression+brand-
  new-simultaneously, per the EXIT CODE CHANGE section above — verified,
  not assumed, before any consumer is told it's safe.
- `--accept`'s new validation must not retroactively invalidate the one
  existing `_accepted` entry in `eval/harness_baseline.json` (it already
  contains `TD-124`, so it would pass the new check if re-validated, but
  this fix does not re-validate existing entries — only new `--accept`
  calls going forward).
- The archive fix must not change what Layer 6 reads during a normal run —
  only the one-time startup truncation point is touched; mid-run
  read/append behavior in `FixtureManager._flush_to_harness_log` is
  untouched.
- Step 4 (`--full` on main, report whether anything was actually masked)
  is not optional and is not a formality — per Bill's own framing, it
  matters more than the code fix itself.
- Do not touch `eval/integration_live.py`'s separate ratchet — confirmed
  above it doesn't share this bug; changing it is out of scope and
  unjustified by this REQ.
