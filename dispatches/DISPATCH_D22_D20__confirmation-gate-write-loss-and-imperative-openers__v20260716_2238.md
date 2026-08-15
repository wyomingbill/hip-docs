# DISPATCH_D22_D20
Status: BUILT
Reconciled-Against: (see commit for hash)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_D22_D20__confirmation-gate-write-loss-and-imperative-openers__v20260716_2238.md`

## THE ASK

Bill's dispatch, verbatim:

> "D-22. Fix it first — it is the worst of the four.
>
> REQ doc first. Dispatch doc per the register.
>
> The confirmation gate (3c0cb74) can't distinguish a genuinely new,
> unrelated write from a botched confirmation attempt, and SILENTLY DROPS
> THE NEW WRITE when an unrelated older park is still within its TTL. Not
> a wrong reply — a lost fact. Nothing surfaces it.
>
> Then D-20 (c86a414): is_declarative_utterance doesn't treat "Explain..."
> / "Trace..." as questions, so general-knowledge queries get the F3
> gate's "unable to save" reply instead of an answer.
>
> Both are mine from today. Both shipped with live proofs that passed on
> the turns they tested and missed these.
>
> NEW RULE, add to CLAUDE.md: a fix is not done until the FULL RATCHET
> passes, not just its own live proofs. "Prove it live" was in all three of
> today's dispatches and it was not enough — narrow proofs pass while the
> fix breaks something adjacent.
>
> Leave D-19 and D-21 failing. D-19 is a stale assertion. D-21 confirms
> TD-125's risk is real — the temp=0.2 retry didn't recover that detection
> miss. Both are telling the truth.
>
> Verify with --full, not with targeted turns. Push, report the hash."

## WHAT WAS DONE

1. Filed `REQ_D22_D20` before any code, per CLAUDE.md item 8.
2. Added CLAUDE.md item 12 (Bill's new rule): a fix is not done until
   `--full` passes, not just its own live proofs.
3. Traced WHY `"unclear"` exists at all and why it can't just defer to F3:
   `voice_orch.py`'s Seam A only fires synchronous detection at `>= 4`
   words, and only then can F3 (`_gate_unconfirmed_update`) do anything —
   below that floor it unconditionally returns the reply unchanged.
   `harness/fact_change.py`'s `detect_and_apply` enforces the identical
   floor independently. The original D-03 turn ("Yes, confirm that.") is 3
   words — under the floor, so F3 could never have caught it regardless of
   how far it was widened. This is why the confirmation gate needed its
   own fix in 3c0cb74, and why D-22's fix cannot simply remove `"unclear"`.
4. Fixed D-22: `harness/confirmation_gate.py`'s `check_confirmation` now
   scopes `"unclear"` to utterances under 4 words. At or above 4 words, a
   declarative matching neither yes/no returns `"pass"` and proceeds
   through the ordinary pipeline (Seam A fires, since it uses the
   identical `>=4` condition).
5. Fixed D-20: grepped every demo script and eval corpus JSON in the repo
   for other imperative-explanation-verb openers before deciding scope —
   found none beyond the two already failing. Added exactly `explain`/
   `trace` to `_QUESTION_OPENER_RE`.
6. Unit-verified both fixes directly against the real functions (not
   simulated) before running the full harness.
7. **Ran `python -m eval.harness --full` live on `main`** — not targeted
   turns, per Bill's explicit instruction and new rule. Confirmed:
   `routing_showcase.T02`/`T03` (D-20) PASS with real answers;
   `three_zone_demo.T04` (D-22) PASS with the write landed in Neo4j (3
   active rows, not 2); `L1:P10` (D-19) PASSES as an unplanned side effect;
   `three_zone_demo.T02` (D-21) still FAILS, untouched, exactly as
   instructed; no new regression anywhere else in the run.
8. Registered D-22 and D-20 as FIXED, D-19 as RESOLVED (side effect, not
   targeted), D-21 left exactly as it was, in the defect register.
   Updated MANIFEST, INDEX, and the ORDER section's priority-0 note.

## WHAT WAS FOUND

- `server/voice_orch.py:2696-2699` (Seam A): `len(_q_words) >= 4` is the
  exact, pre-existing boundary that determines whether the F3 zero-write
  gate can ever see a turn at all. `harness/fact_change.py`'s
  `detect_and_apply` (`if len(words) < 4: return 0`) enforces the same
  floor independently, confirming it is not an accident of one code path.
- Grepped `demo_scripts/*.json` and every `eval/*.json`/`eval/**/*.json`
  corpus for capitalized query openers: only `Explain` and `Trace` appear
  as imperative-explanation-style openers anywhere in this repository.
  `describe`/`summarize`/`outline`/`discuss`/`analyze` appear nowhere —
  confirmed absent, not assumed absent.
- `harness/confirmation_gate.py`'s `check_confirmation`, post-fix, unit
  tested directly: short garbled ("Sure whatever", 2 words) still returns
  `"unclear"`; the D-22 turn itself (9 words) returns `"pass"`; the P10 u2
  injection probe (5 words) also returns `"pass"` — the last one an
  anticipated, not targeted, side effect.

## VERIFIED

**Watched run:**
- Both fixes, unit-level, directly against the real
  `is_declarative_utterance`/`check_confirmation` functions — not
  simulated.
- **`python -m eval.harness --full`, run live and in full on `main`.**
  Read directly from the run's own printed output: exactly one
  `RATCHET FAIL` entry (`three_zone_demo.T02`), exactly one
  `NEW FAILURES` entry (`L6:record-invariants`, pre-existing, unrelated).
  `routing_showcase.T02`/`T03` reply text read directly from the log
  (real explanations, not the unconfirmed-update string).
  `three_zone_demo.T04`'s Neo4j state read directly from the log's own
  polled graph-state assertion (`active state ok (3 row(s)...)`) — not
  re-queried separately, the harness's own check IS the verification.
  `L1:P10`'s `u2` line read directly (`verdict=pass`).
- Full layer pass/fail counts read directly from the run
  (L1 12/13, L2 24/34, L3 3/3, L4 27/31, L6 0/1, SCHEMA 1/1, VOICE 1/1) and
  the single L1 failure (`P2`) identified as the pre-existing, already-
  `_accepted` I-10 flake, not a new problem — confirmed by checking
  `eval/harness_baseline.json`'s `_accepted` entry for `L1:P2` predates
  this session.
- `tests/test_injection_declarative.py` re-run post-fix (16 passed) as a
  nearby-suite regression check on the `_QUESTION_OPENER_RE` change.
- Dev Neo4j/registry state restored to a clean baseline
  (`demo_reset.py` + `demo_seed.py`) after the verification run.

**Reasoned about:**
- That `L1:P10`'s side-effect resolution is causally the SAME 4-word-floor
  change as D-22's fix, not a coincidence — inferred from the exact word
  count of the P10 probe string (5) crossing the same threshold, not from
  tracing the interpreter's control flow line-by-line for that specific
  call in the full run (the unit-level test in WHAT WAS FOUND establishes
  this directly, so it is watched, not purely reasoned — noted here for
  completeness since the full-run log alone doesn't show the "why").
- The stated residual (a short new-fact assertion during an unrelated park
  still lost) was not exercised by any turn in the actual `--full` corpus
  — reasoned to still exist from the code's own logic, not contradicted or
  confirmed by this specific run, since no test scenario happens to hit it.

## HASH

(filled in after commit — see commit message and `git log`)

## OPEN

- D-22's stated residual: a SHORT (<4-word) new fact assertion arriving
  while an unrelated park is alive for the same actor would still be
  caught `"unclear"` and lose its write. Narrower than before (was "any
  declarative"), not eliminated. Needs a real (subject, attribute)
  discriminator to close fully — explicitly out of this REQ's scope.
- `L1:P10` (D-19) now passes but the baseline was not updated to lock that
  in (`--update-baseline` was not run, per CONSTRAINTS — updating the
  baseline wasn't asked for). The next `--full` run will show it as
  `IMPROVED vs baseline`, available to lock in whenever someone chooses.
- D-21 remains open by design, per instruction. TD-123's prompt-hardening
  track is still the correct fix path, not attempted here.
- CLAUDE.md's new item 12 (full-ratchet-before-done) is now written down;
  whether it actually gets followed by future sessions under time pressure
  is a process risk, not something this dispatch can guarantee.
