<!-- STATUS: BUILT -->
<!-- RECONCILED-AGAINST: scripts/gate_check.sh (machine/folder guard, routing harness threshold 0.90 enforced); hip-dev/hip-harness split is the live workflow; scripts/generate_corpus.py, scripts/adjudicate.py present — 2026-07-05 -->

# Dev -> Demo Promotion (TD-049 routing/classifier changes)

`~/hip-dev` (this checkout, `main`, port 7863) is where all classifier work
happens. `~/hip-harness` (`demo-stable`, port 7860) is the frozen demo
checkout — it is never edited directly; it only receives promoted commits.
`scripts/routing_harness.py`, run via `scripts/gate_check.sh`, is the gate
between the two. A classifier change cannot be promoted to demo unless the
gate passes **on both sides** of the promotion.

## The promotion sequence

1. **Fix in dev.** Make the classifier change in `~/hip-dev`
   (`harness/complexity_features.py`, or whatever it touches) and commit it
   to `main` here, same as any other change.

2. **Generate boundary cases.**
   ```
   scripts/improve_cycle.sh
   ```
   Generates fresh candidate queries targeting the classifier's known fuzzy
   edges (see "The iteration loop" below), reports how many auto-accepted
   into the corpus and how many landed in the review queue. This exercises
   the fix against cases it hasn't seen yet, not just the cases that
   motivated it.

3. **Adjudicate the review queue.**
   ```
   .venv/bin/python scripts/adjudicate.py
   ```
   Walks `data/test_corpus/review_queue.jsonl` one entry at a time. Resolve
   every conflict the generator and labeler couldn't agree on (or explicitly
   skip ones you're not ready to call — they stay in the queue, they don't
   block anything by sitting there). See "The iteration loop" for what you're
   actually deciding here.

4. **`scripts/gate_check.sh` must pass.**
   ```
   scripts/gate_check.sh          # threshold 0.90 by default
   ```
   This is the actual gate. It refuses to run anywhere except this machine
   and this checkout (see the guard at the top of the script — fails loudly
   rather than silently checking the wrong thing), then runs
   `routing_harness.py --threshold 0.90` against
   `data/test_corpus/test_corpus.jsonl` and prints the agreement rate, both
   confusion matrices, and the category-drift breakdown. **Nonzero exit ==
   do not promote.** Go back to step 1 (or step 3, if the failures are
   adjudication-queue items you skipped) and try again.

5. **Only then, cherry-pick into `~/hip-harness`.**
   ```
   cd ~/hip-harness
   git cherry-pick <commit-from-hip-dev>
   ```
   Restart the demo server, then **re-run the gate on the demo side**:
   ```
   cd ~/hip-harness
   .venv/bin/python scripts/routing_harness.py --corpus data/test_corpus/test_corpus.jsonl --threshold 0.90
   ```
   (`~/hip-harness` doesn't have `scripts/gate_check.sh`'s machine/folder
   guard — that guard is specifically written to refuse running outside
   `~/hip-dev`, since its whole point is catching a dev-side mistake. On the
   demo side, run `routing_harness.py` directly with the same
   `--corpus`/`--threshold` flags gate_check.sh uses.) If the corpus file
   itself changed as part of the promotion (new seed/generated/adjudicated
   rows), cherry-pick that too, or the demo side is grading against a stale
   corpus and the numbers won't mean anything.

**Bootstrapping note (current state as of this writing):** the harness
infrastructure itself (`scripts/routing_harness.py`,
`data/test_corpus/test_corpus.jsonl`, `scripts/generate_corpus.py`,
`scripts/adjudicate.py`) exists only in `~/hip-dev` right now — it has never
been promoted to `~/hip-harness`. Step 5 above (re-run the gate on the demo
side) only works once that first promotion has happened. Until then, treat
the first promotion that carries this infrastructure over as its own special
case: cherry-pick (or otherwise bring over) `scripts/routing_harness.py` and
`data/test_corpus/test_corpus.jsonl` alongside whatever classifier commit
you're promoting, so `routing_harness.py` exists on the demo side to re-run
at all.

Every promotion is gated by the harness on both sides: once before you
cherry-pick (dev, confirms the fix is good), once after (demo, confirms the
cherry-pick actually landed what you think it landed).

## The iteration loop

This is what steps 2-3 above are actually doing, and it's designed to run
repeatedly — each cycle should leave the corpus a little stronger and the
review queue a little smaller (or the same size, if you were thorough and
generation just found nothing new; growing over time is the sign to stop).

```
generate boundary queries
        |
        v
  three-signal agreement check
    (generator label / independent labeler label / actual classifier output)
        |
   agree? ----yes----> auto-accept into test_corpus.jsonl
        |                (source=generated, adjudicated_by=auto-3way)
        no
        |
        v
  review_queue.jsonl
  (all three labels + both models' rationales, adjudicated_by=null)
        |
        v
  Bill adjudicates ONLY the conflicts
  (scripts/adjudicate.py — bloom, tier, one-line rationale)
        |
        v
  resolved entry moves into test_corpus.jsonl (adjudicated_by=bill)
        |
        v
  re-run scripts/gate_check.sh
        |
        v
   (back to the top for the next cycle)
```

Two things matter about this loop:

- **Bill only ever adjudicates disagreements, never the whole batch.** The
  three-signal design (`scripts/generate_corpus.py`: one model generates and
  proposes a label, a genuinely different model independently labels the
  same query blind, the real classifier scores it — nobody sees anybody
  else's answer before committing to their own) means agreement is a real
  signal, not two passes of the same model rubber-stamping itself. When all
  three land on the same bloom level, that's about as strong a "this label
  is correct" signal as an automated pipeline can produce without a human in
  the loop, so it auto-accepts. When they don't agree, that disagreement
  itself is the useful output — it's pointing at exactly the kind of
  boundary case worth a human ruling, which is why generation is
  boundary-focused (Bloom 4-vs-5, trivial-vs-institutional "should", buried
  analytical verbs after long preambles, analysis/analyst noun-vs-verb
  homographs, etc. — see `BOUNDARY_SPECS` in `generate_corpus.py`) rather
  than evenly sampling easy cases that would just auto-accept and add noise.

- **The rationale Bill writes during adjudication IS the escalation rule for
  that case, not a comment about it.** `scripts/routing_harness.py` reads
  every corpus row's `rationale` field and prints it next to any future MISS
  involving that row. There's no separate design doc that says "here's how
  we decided trivial 'should I' stays at mid and institutional 'should we'
  escalates to core" — that decision lives as the `rationale` string on the
  corpus rows that test it, adjudicated in the specific case where the
  automated pipeline couldn't tell on its own. The corpus rationales
  collectively ARE the rulebook. A future classifier change that breaks one
  of these rows shows up as a MISS with the exact rule it violated printed
  right there — read the rationale before touching the pattern that used to
  satisfy it.

Run the cycle again after any classifier change, and periodically even
without one (drift in the generator/labeler models themselves, or just to
keep expanding boundary coverage). Each cycle should shrink the queue
(everything genuinely ambiguous gets adjudicated once and then the corpus
remembers the answer) — if a cycle instead grows it, that's worth noticing:
either the classifier has a real, not-yet-understood gap at a boundary, or
generation needs a new spec because it found an edge nobody's described yet.
