# REQ_HARNESS
Status: IN_PROGRESS
Reconciled-Against: 55bd835

## THE REQUIREMENT

Bill's words, verbatim:

> "This system needs a harness that grows with the system, that conduct a
> regression end-to-end with each push. that has metrics that we can track."

## THE ACCEPTANCE TEST

Branch `acceptance/inj6-revert`. Revert the INJ-6 fix from c75655d in
`harness/injection_contract.py` only. That fix stopped HIP fabricating
about household members when personal subject resolved but only household
facts were admitted.

Run: `python -m eval.harness --full`

Must observe: Layer 6 (record_invariants G1) reports one or more violations.
Harness exits non-zero. No human typed a query by hand.

Restore the fix (return to main). Run: `python -m eval.harness --full`

Must observe: Layer 6 G1 reports zero violations. G2, G3, G4 also pass.
Harness exits 0.

If reverting the fix does not turn the gate red, the harness does not test
the fabrication class and the requirement is not met.

STATUS: PARTIALLY MET — red half PASSES (revert branch: harness-run/G1=4,
including the real fabrication "You have no appointments before 9am today").
Green half: the instrument defects blocking it are fixed, but the literal
bar ("Layer 6 G1 reports zero violations... Harness exits 0") is NOT
reliably met, for a reason outside this test's own target (see I-10 below).

Instrument defects fixed this session:
  - G4 MULTI_VALUED false positives: fixed 7b5a75f (37 -> 2).
  - G4 park-turn false positive (model output discarded, template spoken):
    fixed 546bd52/c5cb104. Two more bugs found tracing it live this session
    and fixed same commit: (1) the gate had no declarative check and was
    intercepting the WRITE turn that creates the park, eating its ack; (2)
    the gate's early return skipped `_write_routing_log`, so `routing.tier`
    came back None on the gated turn — see D-05/D-17 in the defect register.
  - Cross-run contamination: fixed d76be9e (run_start_ts watermark on
    FixtureManager — harness_run.jsonl gates only records stamped at/after
    this run's start).

Three `--full` runs on the Mini this session, same code state (post
routing-log fix): L2/L3/L4/SCHEMA/VOICE clean and stable across all three
(three_zone_demo.T03/T05 and reveal_demo.R05 — previously flaky on the
routing.tier=None gap — now pass every time). L6 (G1-G4): FAIL / PASS /
FAIL. The one clean run is the one reported as "exit 0" evidence that the
D-05 gate itself is fixed. The other two failed on a PRE-EXISTING, UNRELATED
G1 hit — see I-10 (rate corrected this session: ~91% of runs since Layer 6
was added, not the "~1%" the entry originally claimed). Until I-10 is
resolved, "Harness exits 0" on a routine `--full` run is not a realistic bar
regardless of D-05's state — I-10 is scoped OUTSIDE this REQ_HARNESS's own
target (the INJ-6/G1 fabrication class), but it shares the same gate.

--update-baseline attempted once this session and correctly REFUSED by the
tool (a run with 2 unaccepted failures cannot silently become the baseline)
— eval/harness_baseline.json is unchanged from before this session. L6 is
still not locked into the baseline; that requires either a clean run at
--update-baseline time or resolving I-10 first so clean runs are the norm,
not the 1-in-3 case.

New, out-of-scope finding from this session: D-17 — `Reporter.apply_baseline()`
returns on brand-new failures before checking `regressions`, so a real
regression can print as invisible whenever it coincides with any brand-new
failure (as L6's first run masked the T03/T05 regression here). Not fixed;
Bill's call, logged in defect register.

## WHAT'S ALREADY DONE

- `eval/oracle/record_invariants.py` (G1-G4): written and placed by Bill,
  2026-07-15. Not yet wired to harness.
- `eval/oracle/test_disclosure.py` (disclosure case oracle): built at
  da43516, 311 lines. Not yet wired to harness.
- `eval/harnesslib/disclosure_conformance.py`: offline unit test against
  apply_injection_contract() corpus. Already wired (DISC layer in harness).
  This is NOT the same as test_disclosure.py.
- c75655d INJ-6 fix: guards fabrication by requiring at least one admitted
  fact about the resolved subject before generation. THE FIX BEING GUARDED.
- Harness layers L1-L5 + DISC/SCHEMA/VOICE conformance: all built and
  gated. This task adds Layer 6. Layer 7 (test_disclosure.py) is Phase 2.

## WHAT'S KNOWN BROKEN

1. record_invariants.py not wired: `grep oracle eval/harness.py` returns
   nothing. Invariants only ran when someone typed them by hand.

2. G3 defect in record_invariants.py line 105: `if ms:` treats
   inference_ms=0 as no-inference (falsy). Must be
   `if ms is not None and ms > 0:`.

3. turns_demo.jsonl is truncated by fixture.reset() (called by every
   scenario). By the time Layer 6 would run at harness end, only the last
   layer's turns survive. The harness needs its own accumulation log
   (logs/harness_run.jsonl) that survives resets.

4. Phantom records: 1ca921b found OAI sends a duplicate response.done ~85ms
   after the first, producing a d1.1 record with an empty query. One is
   in the current log. Must be counted and skipped, never silently filtered.

## CONSTRAINTS

- One entry point: eval/harness.py. No fork.
- Do not touch gen_pairwise. Phase 2 only.
- Do not delete demo_scripts. They may be wired to layers not in scope.
- G1 and G4 must gate at HARD ZERO — --accept refused for these checks.
- G2 and G3 join the normal ratchet.
- Verify before reporting. Never report a check as passing without
  observing it pass on the Mini stack.

## HOW (Phase 1)

Reference: docs/deliverables/HIP_HarnessPlan__v20260715_1600.md (Bill placing).
This task is Phase 1 only. Do not restate the plan; reference it.

Phase 1 build items:
  2a. Fix G3: `if ms is not None and ms > 0:`
  2b. Add logs/harness_run.jsonl accumulator to FixtureManager.reset()
      so turns survive across resets.
  2c. Add Layer 6 to eval/harness.py: reads harness_run.jsonl + current
      turns_demo.jsonl. G1/G4 hard zero; G2/G3 ratchet.
  2d. Phantom record handling: skip and COUNT records with empty query.
  2e. Wire test_disclosure.py as a layer (Phase 2, requires live stack).

Commit reference: every commit in this build references REQ_HARNESS.
