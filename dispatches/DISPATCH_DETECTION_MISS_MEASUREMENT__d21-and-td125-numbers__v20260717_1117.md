# DISPATCH_DETECTION_MISS_MEASUREMENT
Status: BUILT
Reconciled-Against: 28597b5 (measurement only, no code changed)

**TYPE:** MEASUREMENT

**REQ:** NONE. No code, no prompt, no behavior changed — Bill's own framing
("No fixes. No prompt changes. Numbers only.") makes this a measurement
dispatch per CLAUDE.md item 10, which may have REQ: NONE and must say why.
The measurement script written for this dispatch
(`detection_miss_measurement_script__v20260717_1117.py`, filed alongside
this doc) reproduces `detect_and_apply`'s exact prompt construction
read-only, against a frozen fact snapshot, and never calls `_apply_changes`
— nothing in the graph or the product was touched.

## THE ASK

Bill's dispatch, verbatim:

> "MEASURE THE DETECTION MISS. No fixes. No prompt changes. Numbers only.
> Dispatch doc per the register. Blocks D-21 and TD-123 both.
>
> TD-125 says outright: "retry cost/recovery-rate not yet measured." D-21
> is n=1 evidence the retry does not recover. Nobody has counted the
> population.
>
> What exists and why neither number is usable:
>   ~1%  — DIAG p2-i019 §10. One landed=False in 100 iterations, ONE seed.
>          The doc itself says "likely <= 10%" and that i020-i099 was never
>          counted. Per-ITERATION.
>   ~91% — harness_trend.jsonl, 10 of 11 --full runs failing. Per-RUN. A run
>          fails if ANY iteration misses, so a low per-write rate produces a
>          high per-run rate automatically. Different denominator, not a
>          conflict.
>
> MEASURE THREE NUMBERS:
>
> 1. MISS RATE AT temp=0.0. Run the fact-change detector across a corpus of
>    declarative utterances. Count how many return zero changes when a
>    change was present. Report the count AND the denominator.
>
> 2. RETRY RECOVERY RATE. For every miss in #1, run the temp=0.2 retry
>    (harness/fact_change.py, TD-125's mitigation, shipped c86a414). Count
>    how many the retry recovers. This is the number TD-125 says does not
>    exist and it decides whether yesterday's fix does anything.
>
> 3. NET MISS RATE. After retry. That is the number that matters for the
>    demo.
>
> CORPUS: build it, file it, say what is in it and why. It must include:
>    - "Dad had a fall last week. He's okay but we're watching it." — D-21's
>      utterance. Run it 20 times. If it misses 20/20 at both temps, it is
>      deterministic and no retry fixes it. That is a different defect than
>      a stochastic miss and it changes what TD-123 has to do.
>    - The three coffee declaratives (they landed, delta non-empty — controls)
>    - "I take atorvastatin 20mg every morning." — the G1 case
>    - Enough others to make the rate mean something. Say how many.
>
> Report per utterance and in aggregate. Do not average away a
> deterministic miss inside a stochastic rate.
>
> If "Dad had a fall" misses deterministically, say so plainly and stop.
> That is the whole finding and it is worse than a rate."

## THE FINDING, STATED PLAINLY, FIRST

**"Dad had a fall last week. He's okay but we're watching it." misses
deterministically. 20/20 at temp=0.0. 20/20 still miss after the temp=0.2
retry. The retry has a measured 0% recovery rate on this utterance.
Stopping here to say so before the numbers, per the instruction.**

It is not a population-level detection problem. Every one of the 24 other
declaratives in the aggregate corpus — spanning all 11 canonical
attributes, three members, direct/narrative/cross-principal phrasings,
including a same-utterance reproduction attempt of the exact DIAG p2-i019
scenario — landed on the first attempt. Zero misses, zero retries needed,
across the entire rest of the corpus.

**Working hypothesis, stated as a hypothesis, not measured directly:** the
seed data itself stores this fact under the attribute `incident` (and a
sibling fact under `medication_status`) — `scripts/demo_seed.py:76-77,84-85`.
Neither `incident` nor `medication_status` exists in
`harness/extraction_queue.py`'s `CANONICAL_ATTRIBUTES`, and the Groq
detector's own structured-output schema (`harness/fact_change.py`'s
`_CHANGES_SCHEMA`) enum-locks the `attribute` field to exactly that list —
`medication, allergy, health_condition, dietary, preference, schedule,
appointment, employer, relationship, household, financial`. There is no
`incident`/event category the model is even ALLOWED to emit. "Dad had a
fall" doesn't map cleanly onto any of the 11 (the closest is
`health_condition`, and a fall is an event, not "a diagnosed or reported
condition" in the sense the other health_condition entries in this
corpus — e.g. "I've been diagnosed with mild hypertension" — represent).
**If this hypothesis is right, temperature cannot fix it at any value,
because the constraint is the achievable output space, not model
uncertainty.** This was not independently confirmed (Groq doesn't explain
its own `changes: []`), so it is reported as the leading structural
explanation for a 20/20-both-temps result, not as a proven mechanism.

## WHAT WAS DONE

1. Read `harness/fact_change.py`'s `detect_and_apply` in full to reproduce
   its EXACT prompt construction (`_fact_line`, `_USER_TEMPLATE`,
   `_SYSTEM_PROMPT`) without calling it directly — calling the real
   function would re-read the live graph on every trial and let any
   successful write change the context for the NEXT trial, breaking a
   clean repeated-measurement design. Instead: read each owner's facts
   ONCE, hold them frozen for every trial, call the same `_call_groq` the
   production code calls, with the same system prompt and the same
   temperature values (0.0, then 0.2 on a miss) — read-only, no
   `_apply_changes`, nothing written.
2. Checked `eval/fact_change_golden.json` (TD-124's existing 24-case
   golden set) before building a new corpus, per CLAUDE.md item 11's
   spirit. Not reused directly: that set validates field-level accuracy
   across semantic classes (correction-vs-supersession, negation,
   coreference) against isolated synthetic fact lists; this measurement
   needed the CURRENT, real, live household context (to reproduce D-21 and
   the DIAG p2-i019 scenario as they actually run today) and the
   retry-recovery question specifically, which the golden set doesn't
   track. Different purpose, not a duplicate — noted here rather than
   silently ignored.
3. Built a 24-utterance aggregate corpus (below) plus a dedicated 20-trial
   determinism test for D-21's own utterance, run separately per Bill's
   explicit instruction not to average one into the other.
4. Ran both live, real Groq calls, real detection logic, real (frozen)
   household context. Filed the corpus, the full raw per-trial JSON
   output, and the measurement script alongside this doc.
5. Updated `HIP_DefectRegister__v20260715_1930.md`'s D-21 entry and
   `docs/BACKLOG.md`'s D-21/TD-123 rows with the measured numbers and the
   schema-mismatch hypothesis — documentation only, no code.

## THE CORPUS — WHAT'S IN IT AND WHY (24 entries + 1 dedicated 20x repeat)

Filed at `docs/dispatches/detection_miss_measurement_results__v20260717_1117.json`
(full corpus + every raw per-trial result) and
`docs/dispatches/detection_miss_measurement_script__v20260717_1117.py`
(the exact reproduction, runnable again against whatever the live graph
looks like at the time).

**Dedicated (excluded from the aggregate rate, per instruction):**
- sam: "Dad had a fall last week. He's okay but we're watching it." — D-21's
  own utterance, x20. The whole point of running it separately is stated
  in THE FINDING above: a 100%-both-temps result would be hidden inside
  any aggregate average, and it needs to stand alone to be legible.

**Aggregate corpus (24, one trial each), by why each is in it:**
- 3 controls (bill): "I like black coffee.", "Sometimes I like it frothed
  with milk.", "You know, I like having coffee in the morning." — D-15's
  own cited turns, already known (post-D-15-fix) to land.
- 1 G1 case (sam): "I take atorvastatin 20mg every morning." — I-10's
  cited evidence turn.
- 1 known-good cross-principal case (maya): "Ray switched from metformin
  to Jardiance 10mg last week." — already independently verified landing
  in `three_zone_demo.T04` during the D-22 fix's `--full` run.
- 2 same-utterance DIAG p2-i019 reproduction (maya, sam): "I'm eating
  vegetarian meals on weekdays now." — the exact historical i016(landed)/
  i019(missed) pair, re-run against TODAY's live context (not the original
  seed=1 run — a different context, so a non-reproduction here is itself
  informative, see RESULTS).
- 17 more spanning every one of the 11 `CANONICAL_ATTRIBUTES` at least
  once (medication x4 incl. above, allergy x3, dietary/preference x2+4,
  appointment x5, schedule x1, household x1, employer x1, relationship x1,
  financial x1, health_condition x1), across all three members, mixing
  direct/narrative/cross-principal phrasing — chosen for coverage breadth,
  not cherry-picked for a particular outcome. Full list with exact
  utterance text and result in the filed JSON.

**Why 24, not more or fewer:** large enough that a single miss would be
legible as ~4% (not lost in rounding), small enough to run and report in
one sitting with real API calls per entry. Not a statistically powered
sample size for a rare-event rate — stated as a scoping choice, not a
claim of precision beyond what 24 trials can support.

## THE THREE NUMBERS

**1. Miss rate at temperature=0.0, aggregate corpus:** 0 / 24 (0%). Every
utterance produced at least the expected fact-change on the first attempt.
No entry required a retry.

**1b. Miss rate at temperature=0.0, D-21's utterance alone (n=20,
reported separately, not folded into the above per instruction):** 20 / 20
(100%).

**2. Retry recovery rate:** undefined for the aggregate corpus — there
were no misses in 24 trials to retry. For D-21's utterance: 0 / 20 (0%).
The temp=0.2 retry recovered nothing on any of the 20 trials.

**3. Net miss rate after retry:** aggregate corpus 0 / 24 (0%, unchanged —
nothing needed retrying). D-21's utterance: 20 / 20 (100%, unchanged by
the retry).

**Do not average these into one number.** A single combined rate (e.g.
20 misses out of 44 total trials = ~45%) would misrepresent both halves:
it would overstate the risk for the 24-utterance population (whose real
rate is 0%) and understate the certainty of D-21's own failure (which is
not "45% risky," it is 100% guaranteed, twice, at every temperature tried).

## WHAT THIS MEANS FOR THE TWO EXISTING NUMBERS

- **~1% (DIAG p2-i019, per-iteration, one seed):** unaffected by this
  measurement — a different utterance ("vegetarian meals on weekdays" for
  sam, iteration i019 of a specific seed=1 run), a different failure
  instance. Re-running the SAME utterance today, against today's live
  context, did NOT reproduce a miss (see corpus results) — consistent with
  the DIAG doc's own finding that this class is context-composition
  sensitive, not with a claim that the original i019 miss didn't happen.
- **~91% (harness_trend.jsonl, per-run):** this measurement makes that
  number much easier to explain, not harder. If `three_zone_demo.T02`
  (D-21's exact turn) is a 100%-deterministic miss, then ANY `--full` run
  that includes `three_zone_demo` in its scope will ALWAYS show at least
  one L2 failure from this single scenario — which is sufficient by itself
  to explain a high per-run failure rate, independent of any broader
  population-level detection unreliability. The ~91% figure does not need
  a stochastic population-level explanation; one deterministically-red
  scenario recurring in every run's corpus is sufficient on its own.

## VERIFIED

**Watched run:** every number above is read directly from
`detection_miss_measurement_results__v20260717_1117.json`, the actual
per-trial output of live Groq calls against the real, current household
context (`bill`/`maya`/`sam`, read once via `read_user_facts`, frozen for
the duration of the measurement). Not simulated, not estimated.

**Reasoned about:** the schema-mismatch explanation for WHY D-21's
utterance misses deterministically (`incident`/`medication_status` absent
from `CANONICAL_ATTRIBUTES`) is inference from reading the code's own enum
constraint, not a confirmed causal mechanism — Groq's `changes: []`
response carries no explanation field, so this cannot be directly
verified from the model's own output, only argued from the schema it was
constrained to. Flagged as a hypothesis in THE FINDING section, not
asserted as proven.

## HASH

NONE for the measurement itself (no code changed). The documentation
updates this dispatch makes (defect register, BACKLOG.md, INDEX) will
carry whatever commit hash results from filing this dispatch — see commit
message.

## OPEN

- The schema-mismatch hypothesis is not confirmed. If it's right, TD-123's
  current framing (prompt hardening for dietary/preference disambiguation
  and subject-typing) does not touch D-21's failure mode at all — a
  different fix (adding an event/incident category to
  `CANONICAL_ATTRIBUTES`) would be needed, which is a schema change, not a
  prompt change. This measurement does not decide that; it hands the
  question to whoever writes `REQ_TD123`, per `docs/BACKLOG.md`'s own
  rule that TD-123 needs a REQ before any fix attempt.
- 24 trials at 0% miss is not proof the population rate is truly 0% — it
  bounds it well below what D-21's own rate is, but a rare, low-single-
  digit-percent stochastic miss elsewhere in the attribute/phrasing space
  could exist undetected at this sample size. Not claimed as ruled out.
- The DIAG p2-i019 "vegetarian meals" pair not reproducing today's miss is
  itself a finding worth someone's attention: it suggests the original
  i019 failure was sensitive to the EXACT context composition of that
  historical seed=1 run, not a stable property of "sam" or "vegetarian" in
  general — consistent with, not contradicting, the original DIAG doc.
- No REQ was written for TD-123 as part of this dispatch, deliberately —
  that was explicitly out of scope ("No fixes. No prompt changes.").
