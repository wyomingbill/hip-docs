# REQ_VOICE_INTO_KERNEL
Status: PLAN
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ `4167184` (NC 12 verified).
Filed by NC 13 **before the first code edit**.

**DELTA REQUIREMENT (R-NC1-1).** The kernel, the typed request, the two rulings and the
`TurnResult` are proven (NC 9, NC 11) and are **referenced, not restated**. Only the voice
delta is required here.

---

## THE REQUIREMENT — Bill's words, 2026-08-14, verbatim

> **OBJECTIVE: the live Pipecat voice path enters the ONE kernel. After this capability there
> is no second governance-bearing decision path on voice.**
>
> **1. Pipecat's _on_user_text produces a TurnRequest and invokes the same deterministic
> pre-generation dispatcher as typed/HTTP voice — speaker identity, confirmation, disclosure,
> memory-write decisions all in the kernel; streaming may diverge only after those decisions.**
>
> **2. F2's contract holds here: any exception in the governed stage fails closed — never
> forwards the transcript to a model. (HA-86 fixed the handler; prove the migrated path
> inherits it.)**
>
> **3. Behavioral equivalence: same transcript+principal through text and migrated voice match
> on every governance-bearing field; structural refusal on voice = server refusal, NO LLM call,
> TTS renders; must hold with all answering models down.**
>
> **4. Latency before/after recorded (M-0 baseline exists); grounding non-regression actually
> exercised, not vacuous.**
>
> **5. DECOMMISSION the second decision path after proof — the parallel _on_user_text
> governance code is removed or reduced to a thin adapter, measured (NC 9's branch-count
> method).**

**Standing rulings that bind:** option C; **A1-7 stands and this IS A1b**; **M-0's latency
measurement discharges R-1's ordering**.

**EXCLUDED BY RULING:** `/ws/voice` — TD-V-023, `demo_dashboard`, and the deliberately-red C8
surface stay out of scope.

**KEEPER TABLE (carried in-dispatch per HA-92's limit):** the five canonical HTTP duplicates
keep `voice_https_orch` — `text-query`, `facts`, `members`, `routing`, `reset`. **Surface dedup
is NOT this capability; no route is retired here.**

---

## THE ACCEPTANCE TEST

- **V1** `_on_user_text` builds a **`TurnRequest`** and calls the **kernel's** deterministic
  pre-generation decision. No governance-bearing decision is taken by voice code before it.
- **V2 FAIL CLOSED (F2).** Any exception raised inside the governed stage results in a
  refusal and **the transcript is never forwarded to a model**. Proven by injecting an
  exception and observing the model boundary.
- **V3 EQUIVALENCE.** The same transcript + principal through the text path and through the
  migrated voice path **match on every governance-bearing field** — outcome, member, refusal
  reason, and whether a model was called.
- **V4 STRUCTURAL REFUSAL ON VOICE.** A refusal is a **server** refusal: **no LLM call**, and
  **TTS still renders** the refusal. **Must hold with all answering models down.**
- **V5 LATENCY** before and after, recorded against M-0's baseline.
- **V6 GROUNDING NON-REGRESSION**, actually exercised — a grounded turn still reaches its
  facts. A test that cannot fail does not count.
- **V7 DECOMMISSION**, measured by **NC 9's branch-count method**: `_on_user_text`'s
  governance-bearing control-flow count before and after, with the delta attributed.

---

## WHAT'S ALREADY DONE — REFERENCED, NOT REBUILT

`harness/kernel.py` (`governed_turn`, `TurnResult`, both rulings), `harness/turn_request.py`
(`spoken_request`, `ClaimMismatch`), `harness/model_calls.py` (observed `model_called`, NC 11),
and the egress gateway. **None is reimplemented.**

## WHAT'S KNOWN BROKEN

`_on_user_text` is **689 lines with 55 control-flow nodes** and carries its own speaker
resolution, control-flow classification, decide/route and refusal handling — **a second
governance-bearing decision path on voice**, which is precisely what this capability ends.

## CONSTRAINTS

- **`~/hip-vo` untouched**; work in `~/hip-nc2` @ `nc-b0`. No graph writes, no service started.
- **`/ws/voice` and the demo dashboard are out of scope** and must not be edited.
- **No route retired** (keeper table above).
- **The streaming path may diverge only AFTER the governed decisions** — never before.
- **A refusal must never become softer.** If the migrated path answers where the old one
  refused, that is a regression.

## OPEN — NOT DECIDED BY THIS REQ

**How much of the 689 lines can be decommissioned safely in one dispatch is an empirical
question, and the answer must be MEASURED and reported, not asserted.** Removing governance
code that the kernel does not yet own would be a regression dressed as cleanup.

---

# AMENDMENT 1 — SINGLE-DECISION MIGRATIONS (NC 14, 2026-08-14)

**AMENDED, NOT REPLACED.** NC 13 landed the pre-generation gate (V1-V6) and reported V7
unearned with the branch count measured going **up** by one. This amendment carries Bill's
ruling on what happens next.

## THE REQUIREMENT — Bill's words, verbatim

> **continue single-decision; "gate is sufficient" REJECTED — it would prove the perimeter
> while allowing semantic differences inside it.**
>
> **Migrate in THIS order, one decision boundary per segment, each with its own equivalence
> twin and measured branch-count drop BEFORE the next begins: S1 speaker identity, S2
> confirmation, S3 disclosure, S4 memory-write.**
>
> **Per segment: the decision moves into the kernel; the Pipecat path's copy is removed or
> reduced to a thin adapter (branch count measured); equivalence twin proves same transcript+
> principal matches on every governance-bearing field; fail-closed inherited (exception never
> forwards the transcript).**

**Expanded — why the rejection is the load-bearing half.** NC 13 proved that *nothing reaches
a model without crossing the kernel*. That is a **perimeter** property. It says nothing about
whether the decision taken inside the perimeter is the same one the typed path would take, and
two implementations of "who is speaking" can agree on *whether* to answer while disagreeing on
*for whom*. **A perimeter that admits semantic divergence inside it is the shape this whole
capability exists to end.**

## THE ACCEPTANCE TEST — per segment, and the order is part of it

For **each** of S1-S4, in order, and **completed before the next begins**:

- **Sn.1** the decision is taken in `harness/kernel.py` and nowhere else on the voice path.
- **Sn.2** the Pipecat copy is **removed, or reduced to a thin adapter** — and the
  `_on_user_text` control-flow count is **measured before and after**, with the drop reported.
  **A segment whose count does not drop has not migrated a decision**; it has added one.
- **Sn.3** an **equivalence twin**: the same transcript + principal through the typed path and
  the voice path **match on every governance-bearing field**.
- **Sn.4** **fail-closed inherited**: an exception inside that decision refuses and **never
  forwards the transcript to a model**, observed at the model counter.

- **X1** `/ws/voice` remains out of scope and untouched.
- **X2** zero new suite failures, by failure-**set** comparison.
- **X3** **STOP between segments only on contradiction**, per the standing amendment — not on
  difficulty, and not on scope discomfort.

## CONSTRAINTS ADDED

- **A segment is not complete until its branch drop is measured.** Reporting a migration
  without the count is the failure mode NC 13 avoided by measuring; it is now forbidden.
- **No segment may make a refusal softer.** If the migrated decision answers where the copy
  refused, that is a regression regardless of what the twin says.

---

# AMENDMENT 2 — ONE DECISION POINT PER MODALITY (NC 24, 2026-08-15)

**AMENDED, NOT REPLACED.** This amendment is filed **before the first code edit**, against
`~/hip-nc2` @ `nc-b0` @ `0c7b6ee` (NC 22's Conversation Episode, landed 06:53 today).

## THE REQUIREMENT — Bill's words, 2026-08-15, verbatim

> **F5 — the typed path enters governed_decision(). NC 21 measured: governed_decision has
> exactly ONE production call site (voice_orch.py:1637); the typed HTTPS endpoint reaches the
> kernel by a route that never passes B1, so spoken "that one" clarifies while typed "that
> one" misroutes to a store-down refusal. Fix: the typed adapter calls the SAME decision point
> before the turn proceeds — one call site per modality, same order, no copy. Equivalence
> twin: the same dependency phrasing spoken and typed lands in the SAME class with the SAME
> reply shape.**

## WHY THIS IS AN AMENDMENT AND NOT A NEW REQUIREMENT

**This REQ's own objective already said it, and the code never made it true.** Bill's
requirement 1 above reads *"Pipecat's `_on_user_text` … invokes the same deterministic
pre-generation dispatcher **as typed/HTTP voice**"* — a clause that presupposes the typed side
already crossed the dispatcher. **It did not, and V3 EQUIVALENCE has therefore never been
satisfiable**: NC 21 measured the same utterance landing in two different classes by modality.
`governed_decision`'s own docstring states *"The live Pipecat path calls THIS, and so does the
typed path"* — the one sentence in the file that was false. **Amendment 2 makes the REQ's
existing V3 reachable; it does not widen the capability.**

## THE DESIGN, PINNED BEFORE THE EDIT

- **A2.1 — the typed adapter's ONE call site is `harness/kernel.py::governed_turn`,
  as its FIRST action.** `governed_turn` is the single typed funnel (`text_turn` → `text_reply`
  → both `/api/text-query` routes, Tier L, and the eval harnesses). One call there is one call
  per typed turn, and no route file is edited — the same "no caller edit" property NC 20
  claimed for voice.
- **A2.2 — SAME ORDER means B1 decides before store-down, on both modalities.** The spoken
  order is episode → B1 → store-down. `governed_decision` running first reproduces it exactly,
  which is what repairs the measured symptom: a dependency phrasing with the store down must
  land in the DEPENDENCY class, not the store-down class. **A modality-specific order would be
  a second policy wearing one function's name.**
- **A2.3 — NO COPY: `governed_turn`'s own store-down block is REMOVED**, because
  `governed_decision` already contains it. Two store-down gates in one turn is precisely the
  duplication this capability exists to end, and the second one is what currently answers first.
- **A2.4 — `governed_decision` gains an optional `store_probe`, passed through to
  `store_reachable`.** Additive, defaulted, and the spoken call site is **not touched** — the
  seam that lets both rulings be twinned in both directions without a graph must survive the
  move, or A2.3 would trade a duplicated gate for an untestable one.
- **A2.5 — `TurnResult` carries `notice`.** NC 22's `TurnDecision.notice` states *"Callers must
  deliver this whether the turn proceeds or not"*; after A2.1 `governed_turn` IS a caller, so
  the field must survive the boundary. **Rendering it into a typed HTTP response body is NOT in
  this amendment** — see the residuals.

## THE ACCEPTANCE TEST

Executing consumer-path twins, through the real public entries, both modalities:

- **E1 EQUIVALENCE (Bill's twin).** The same dependency phrasing through the typed adapter and
  through the spoken decision point lands in the **same class** with the **byte-identical**
  reply.
- **E2 ONE CALL SITE PER MODALITY.** A typed turn reaches `governed_decision` **exactly once**,
  counted at the function; the spoken path keeps **exactly one** production call site.
- **E3 ORDER.** With the store down, a household-dependent **dependency** phrasing refuses as
  `REFUSED_UNRESOLVED_REFERENCE`, not `REFUSED_STORE_DOWN` — the F5 symptom, measured at the
  outcome.
- **E4 NO SOFTER REFUSAL.** A household-dependent **non-dependency** utterance with the store
  down still refuses `REFUSED_STORE_DOWN`, and the `store_probe` seam still decides it.
- **E5 NO MODEL CALL** on the B1 refusal through the typed path, observed at
  `harness/model_calls.py`.
- **E6 THE WINDOW REACHES TYPED.** With a live Episode carrying the prior turn, the same typed
  dependency phrasing **proceeds** — the typed path inherits NC 22's window at the same line.
- **E7 ZERO NEW SUITE FAILURES**, by failure-**set** comparison at the same service state
  (this lane has no graph on 7693 — store-down is the standing condition, not a fault).

## CONSTRAINTS ADDED

- **No voice edit.** The spoken call site is untouched; if the spoken path changes at all, the
  change is wrong.
- **No route file edited.** `server/voice_https_orch.py` and `server/voice_orch.py` are outside
  this amendment's scope.
- **A refusal must never become softer** (this REQ's standing constraint) — E4 is its gate.

## RESIDUALS THIS AMENDMENT DOES NOT CLOSE, NAMED SO THEY ARE NOT MISTAKEN FOR DONE

1. **`server/voice_https_orch.py:469` is a SECOND spoken entry that bypasses the kernel funnel
   entirely** — it calls `voice_orch.process_governed_turn` directly, so it crosses neither
   `governed_turn`'s gates nor `governed_decision`. A2.1 does not reach it. Closing it means
   routing that endpoint through the kernel adapter, which edits a route file and cannot be
   executed in this lane (NC 21: import fail-closed in the bare env). **Filed, not fixed.**
2. **No typed route renders `notice`.** A2.5 carries it to the boundary; delivering it to a
   member on a typed surface is a route-level, user-visible decision and is Bill's to make.
3. **F3-interim is NOT built and this amendment does not specify it.** NC 22's landed code
   supplies B1's window at `harness/kernel.py:365-366` — the exact line F3-interim targeted —
   and retires `voice_orch._trim_context`, the window F3-interim was to plumb. **Building it
   would add a caller-supplied mechanism contradicting `TurnRequest.episode`'s stated
   kernel-resolved rule.** Cancellation is Bill's ruling, not this amendment's.
