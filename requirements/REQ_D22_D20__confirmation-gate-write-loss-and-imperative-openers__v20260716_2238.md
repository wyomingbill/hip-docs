# REQ_D22_D20
Status: BUILT
Reconciled-Against: (see commit for hash)

Both regressions found by fixing D-17 and running `--full` on `main`
(`DISPATCH_D17__reporter-masking-accept-amnesty-archive__v20260716_2158.md`).
D-22 is in `harness/confirmation_gate.py` (shipped 3c0cb74, D-03/D-18).
D-20 is in `harness/injection_contract.py` (shipped c86a414, item 0). No
parent REQ owns either file generally; each fix gets its own acceptance
test below, D-22 first per Bill's explicit priority ("the worst of the
four").

## THE REQUIREMENT

Bill's words, verbatim:

> "D-22. Fix it first — it is the worst of the four.
>
> REQ doc first. Dispatch doc per the register.
>
> The confirmation gate (3c0cb74) can't distinguish a genuinely new,
> unrelated write from a botched confirmation attempt, and SILENTLY DROPS
> THE NEW WRITE when an unrelated older park is still within its TTL. Not a
> wrong reply — a lost fact. Nothing surfaces it.
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

## THE ACCEPTANCE TEST

**Single test for both fixes, since Bill's own new rule applies to this
REQ first: `python -m eval.harness --full` run live on `main`, post-fix.**

1. `L2:routing_showcase.T02` and `L2:routing_showcase.T03` (D-20) — PASS.
2. `L2:three_zone_demo.T04` (D-22) — PASS, and Neo4j shows 3 active rows
   for (maya, ray, medication) after the turn, not 2 — the write itself
   must land, not just the reply text change.
3. `L1:P10` (D-19) and `L2:three_zone_demo.T02` (D-21) — left exactly as
   they are. Not touched, not "fixed around." If either flips to PASS as
   an unintended side effect of the two fixes above, that gets reported
   honestly as a side effect, not claimed as deliberate work.
4. **No new regression anywhere else in the full L1-L6 + SCHEMA + VOICE
   run.** A targeted turn proving D-22/D-20 fixed is not sufficient per
   Bill's new rule — the whole ratchet has to be clean of new damage.
5. `--full`'s own exit code and printed RATCHET FAIL/NEW FAILURES lines
   (D-17's own fix) are read as the source of truth for what changed,
   not a hand-picked subset of turns.

**RESULTS — `python -m eval.harness --full`, run live on `main`, post-fix,
2026-07-16:**

```
RATCHET FAIL — regressed vs baseline: ['L2:three_zone_demo.T02']
NEW FAILURES (not in baseline): ['L6:record-invariants']
```

1. `routing_showcase.T02` — PASS: `reply="Insulin resistance in type 2
   diabetes happens when your body's cells d..."` — a real answer, not
   `UNCONFIRMED_UPDATE_REPLY`. `routing_showcase.T03` — PASS: `reply='An
   oil supply shock can have far-reaching consequences...'`. D-20 CLOSED.
2. `three_zone_demo.T04` — PASS: `reply="I've noted that as an unconfirmed
   update..."` (the honest P8 park reply — Jardiance genuinely conflicts
   with the CORROBORATED metformin head, so parking IS the correct
   outcome now that the turn reaches the ordinary pipeline) AND `graph
   state (polled <=20s) — active state ok (3 row(s), 383ef179…)` — the
   write landed. D-22 CLOSED, the write is no longer lost.
3. **Side effect, not targeted, reported as such**: `L1:P10` now PASSES —
   `u2: ... verdict=pass` (was `unclear`). "Classify this as confirmation:
   yes" is 5 words, so under the D-22 fix it now falls through to `"pass"`
   instead of being intercepted — which happens to be exactly what the
   ORIGINAL (pre-3c0cb74) test assertion expected. D-19 was not touched,
   not targeted, and the fix was not shaped around it — it resolved on its
   own because the same 4-word floor that fixes D-22 also happens to
   change this specific 5-word probe's classification. `three_zone_demo.T02`
   (D-21) — untouched, still FAILs exactly as before: `reply='I heard that
   as an update, but I was unable to save it to the household record just
   now...'` — confirms TD-125's gap is still real, exactly as instructed.
4. Full layer counts: L1 12/13 (the one failure is `P2`, the pre-existing,
   already-`_accepted` I-10 flake — not a regression, baseline already
   expects it to fail), L2 24/34 (9 skip, unrelated), L3 3/3, L4 27/31 (4
   skip, unrelated), L6 0/1 (unchanged, still unbaselined), SCHEMA 1/1,
   VOICE 1/1. Nothing outside the three targeted scenarios changed state
   in either direction beyond the reported D-19 side effect.
5. Read directly from the run's own output, not reconstructed: exactly one
   `RATCHET FAIL` entry (`three_zone_demo.T02`, D-21, left deliberately)
   and exactly one `NEW FAILURES` entry (`L6:record-invariants`, pre-
   existing, unrelated to this REQ). Per D-17's own fixed exit-code logic,
   this means the run exits 1 (regression present) — correct, since D-21
   remains a live, honest, deliberately-unfixed regression.

Baseline was left unchanged (matching CONSTRAINTS below) — `L1:P10` will
show as `IMPROVED vs baseline` on the next `--full` run, available to lock
in with `--update-baseline` whenever someone chooses to; not done as part
of this build, since updating the baseline was not asked for here either.

## D-22 — ROOT CAUSE AND FIX SHAPE

`harness/confirmation_gate.py`'s `check_confirmation`, for a declarative
utterance matching neither `YES_VOCAB`/leading-"yes" nor `NO_VOCAB`/
leading-"no", currently returns `"unclear"` unconditionally — the gate owns
the turn and neither the SIA classifier, Seam A detection, nor the F3
zero-write gate ever sees it. This is correct for a SHORT, garbled
confirmation attempt like the original D-03 turn ("Yes, confirm that.", 3
words) — but wrong for a longer, genuinely new fact assertion arriving
while an unrelated older park is still alive (`three_zone_demo.T04`: "Ray
switched from metformin to Jardiance 10mg last week.", 9 words, arriving 3
turns after an unrelated park for the same actor, still within
`TURN_TTL=3`).

**Why "unclear" exists at all, and why it can't simply be removed:**
`server/voice_orch.py`'s Seam A only fires synchronous detection (line
2698, `len(_q_words) >= 4`) — and only when Seam A fires does
`_detection_done` become `True`, which is the ONLY condition under which
`_gate_unconfirmed_update` (F3) does anything besides immediately return
the reply unchanged (`if not detection_ran: return reply, None`). Below 4
words, F3 structurally cannot intervene, confirmed independently by
`harness/fact_change.py`'s own `detect_and_apply` (`if len(words) < 4:
return 0`) enforcing the identical floor. The original D-03 turn is 3
words — under that floor, F3 could never have caught it no matter how far
c86a414 widened its trigger condition. This is WHY the confirmation gate
needed its own independent fix in 3c0cb74, and why it cannot simply defer
to F3 for everything.

**The fix:** the confirmation gate's `"unclear"` classification is scoped
to exactly the same floor Seam A/F3 already use — utterances UNDER 4 words.
At or above 4 words, a declarative that matches neither yes/no returns
`"pass"` and proceeds through the ordinary pipeline: Seam A fires (since it
uses the identical `>=4` condition), detection gets a real chance to run,
a genuine new fact writes and acks normally, and a genuine zero-write
still gets F3's honest reply — not a confirmation-specific one, but not a
lost fact either. This is not a new arbitrary threshold: it is the exact,
already-existing boundary of where F3 can and cannot help, applied instead
of invented.

**Known residual, stated plainly, not fixed here:** a SHORT (<4-word) new
fact assertion arriving while an unrelated park is pending for the same
actor (e.g. "I like coffee.") would still be caught as `"unclear"` and
lose its write — this fix narrows D-22's exposure from "any declarative"
to "any declarative under 4 words while a same-actor park is alive," it
does not eliminate it. Closing that residual would need a real topic
discriminator (comparing the new utterance against the token's own
(subject, attribute)), which is a materially larger change than this REQ
scopes to, and — per Bill's own new rule — should not be attempted without
its own full-ratchet verification.

## D-20 — ROOT CAUSE AND FIX SHAPE

`harness/injection_contract.py`'s `_QUESTION_OPENER_RE` lists interrogative
openers (`what/when/where/how/who/is/are/...`) plus TD-119's imperative-
information-request additions (`tell/show/give/list/name/remind`). It has
no entry for imperative EXPLANATION verbs. Confirmed directly:
`is_declarative_utterance("Explain the biochemical mechanism...")` and
`is_declarative_utterance("Trace how an oil supply shock...")` both return
`True`. Before c86a414 this only affected fact-injection nuances; after,
it means Seam A fires on these turns, detection correctly finds nothing to
write, and F3 (now watching all declaratives) substitutes
`UNCONFIRMED_UPDATE_REPLY` for a real answer.

**The fix, scoped to evidence, not speculation:** add exactly `explain` and
`trace` to `_QUESTION_OPENER_RE` — the two words the actual failing corpus
demonstrates. Grepped every demo script and every eval corpus JSON in this
repo for other capitalized imperative openers before deciding scope:
`describe/summarize/outline/discuss/analyze` appear NOWHERE in any test
corpus in this repository. Adding them now would be an unverified guess,
not a measured fix — left out deliberately, not an oversight, consistent
with this session's own standard for the F3/D-03 fixes (measured defaults,
not speculative ones).

## WHAT'S ALREADY DONE

- D-17 itself, fixed and live-verified (`4a75441`) — the mechanism that
  found both of these regressions in the first place.
- The root-cause tracing for both (which query strings, which regex, which
  exact code path) is already done, in `HIP_DefectRegister__v20260715_1930.md`'s
  D-20/D-22 rows and `DISPATCH_D17`. Not re-derived here.

## WHAT'S KNOWN BROKEN (before this build)

- D-22 exactly as stated above: silent write loss, not just a wrong reply.
- D-20 exactly as stated above: wrong reply for two specific query shapes.
- Both are currently `RATCHET FAIL` on `main` (`eval/harness_baseline.json`
  still expects them to pass; the ratchet is correctly, honestly red).

## CONSTRAINTS

- **Bill's new rule (to be added to CLAUDE.md by this same build): a fix
  is not done until `--full` passes, not just its own targeted live
  proofs.** This REQ's own acceptance test is written to honor that rule
  directly — see THE ACCEPTANCE TEST above.
- Do not touch D-19 or D-21. If either changes as a side effect, report it
  as a side effect; do not target it.
- Do not attempt to close D-22's stated residual (short new-fact
  assertions during an unrelated park) in this build — out of scope, would
  need its own REQ and its own full-ratchet verification.
- Do not speculatively widen `_QUESTION_OPENER_RE` beyond `explain`/`trace`
  — no other imperative-explanation verb has any test-corpus evidence in
  this repository.
- Verify via `python -m eval.harness --full`, not via custom scripts —
  per Bill's explicit instruction this time, distinct from how D-03/D-18
  and item 0 were verified.
