<!-- STATUS: BUILT — Phase 4 human-in-the-loop checklist against the 8/8 live baseline (LATEST_SEAM_B.md) -->
<!-- RECONCILED-AGAINST: main d4a031e + dashboard /hitl + /api/text-query routes; dashboard 7871 restarted on this code 2026-07-06 -->

# HITL Checklist — Phase 4 Human Judgment Pass (against the 8/8 baseline)

What the harness cannot judge: tone, legibility, narrative fit, plausibility, and how
it all *feels* to an evaluator clicking around. Work through this in the browser at
**http://[REDACTED-TAILNET-ADDRESS]:7871/** (tailnet) — this page itself is served at
**/hitl** so you can keep it open in a second tab.

**Before you start:** hit **Reset** (or `POST /api/reset`) so the graph is the clean
D1-D9 fixture — E1's statement must be a genuine update (metformin → Jardiance), not
an idempotent no-op against a leftover Jardiance head. The dashboard was restarted on
the 8/8 code (commit `d4a031e` + this checklist's dashboard routes); the 7860 voice
server still runs the FROZEN ~/hip-harness build — do NOT judge seams there. Anything
you fire from THIS dashboard (`/demo` player, `/api/text-query`) runs the code under
test.

Mark each item PASS / FAIL / NOTE and jot findings in the box under it. A FAIL here is
a demo-quality finding, not a regression — file it; don't fix live.

---

## HITL-1 — Response naturalness (the E1 ack, and all 8 tones)

**(a) Action.** Open `/demo`, load the care-coordination script, and fire the E1 turn
(maya: *"Ray switched from metformin to Jardiance 10mg last week."*). Then fire the
other scenario turns one at a time (or use the unscripted box / `POST /api/text-query`
with the Tier L queries: "What medication is Ray on now?", "What medication do I
take?", "Draft a care plan for Ray…", "What do we know about Ray's medications?",
"What allergies do I have?").

**(b) Look for.** The acknowledgment wording and the follow-up. The harness only
checked "not a refusal" — you're judging whether *"Got it, Ray switched from metformin
to Jardiance 10mg last week. How are you feeling with the new medication?"* reads like
a capable assistant or like a template. Same judgment on all eight replies: length,
warmth, second-person vs third-person consistency (E2 should say "Ray is on…", E3
"You take…").

**(c) PASS:** every reply is 1-3 sentences, addresses the right person, the ack
sounds conversational, and nothing reads as boilerplate or as the model reciting its
instructions. **FAIL:** robotic phrasing ("I have updated the fact"), wrong-person
attribution ("You take Jardiance" on a Ray query), instruction leakage ("as per my
rules…"), or an over-eager follow-up question on every single turn (one is charming,
six is a tic).

> Findings:
>
> _______________________________________________

## HITL-2 — Timeline legibility (the supersede beat)

**(a) Action.** After E1, open `/epistemic` (and the fact-history view for Ray's
medication via the dashboard's fact panel). Look at the metformin → Jardiance chain.

**(b) Look for.** Whether a non-engineer watching the screen groks in ~5 seconds:
old value retired, new value active, trust level shown (ASSERTED head vs the
CORROBORATED seed), exactly one transition. Noise check: no duplicate Jardiance rows
(the old self-supersede churn), no `(about Ray)` annotation artifacts rendered where
they confuse rather than clarify, no raw fact_ids where a value should be.

**(c) PASS:** one clean chain, the arrow of history obvious, trust labels legible
without explanation. **FAIL:** the audience needs you to narrate what they're seeing;
stale rows, cryptic labels (`write_state=supersede` raw), or the timeline ordering
fights the story (newest not visually distinct).

> Findings:
>
> _______________________________________________

## HITL-3 — Demo narration fit (full script, operator-paced)

**(a) Action.** Reset. Load the full script on `/demo` and drive it start-to-finish
with the Next button at your speaking pace — say your actual evaluator narration out
loud as each turn fires.

**(b) Look for.** Screen-vs-words fights: a turn whose on-screen result lands AFTER
your sentence about it (the E1 sync-detect adds ~1-3s before the reply — does the
pause feel like thinking or like a hang?); a reply that contradicts the beat you're
narrating; panels updating out of order (routing row before reply, delta after you've
moved on); the guard refusal appearing where your story promised an answer.

**(c) PASS:** every beat lands on or before your narration; pauses read as thinking;
you never have to say "ignore that". **FAIL:** any turn where you'd have to talk over
the screen, apologize, or re-explain — note WHICH turn and WHAT fought you.

> Findings (turn → what fought the words):
>
> _______________________________________________

## HITL-4 — Routing plausibility (does the tier story hold?)

**(a) Action.** After the script run, review the routing rows on the dashboard
(last-50 panel or `/api/routing`).

**(b) Look for.** Per-row believability, as a skeptical evaluator would read it: is
"What medication do I take?" self-evidently an EDGE (bloom 1) lookup? Is "Draft a
care plan for Ray weighing his fall risk against his medication" genuinely a CORE
(bloom 6) synthesis task — would YOU give that to the big model? Any row where the
tier looks arbitrary, or where two similar queries got different tiers without a
tellable reason. Also check the guard row (E6) reads as a routing event, not an error.

**(c) PASS:** you can defend every row's tier in one sentence to a skeptic.
**FAIL:** any row where the honest answer is "the classifier just does that" — record
the query and the indefensible tier.

> Findings (query → tier → why implausible):
>
> _______________________________________________

## HITL-5 — Empty-set beat (structural refusal must LOOK structural)

**(a) Action.** Ask an unknown-fact personal question — e.g. as maya: *"What
allergies do I have?"* or *"What is Elena's blood type?"* (unscripted box or
`POST /api/text-query`). Watch the reply AND the routing/guard indicators.

**(b) Look for.** The demo's money moment: does the screen make it obvious the SYSTEM
refused (guard fired, no model call, `guard_triggered=true` visible somewhere an
audience can see) — versus the reply just being a vague "I don't have that"? An
evaluator must be able to tell "cannot fabricate, by construction" apart from "the
model happened to demur". Note: blood-type phrasing exercises the original INJ-6 path
only when nothing is admitted; the allergy phrasing exercises the new INJ-6b — try
both and see whether they LOOK different (they shouldn't).

**(c) PASS:** refusal is visibly a guard event (badge/row/metadata) and the wording
is confident, not apologetic mush. **FAIL:** the refusal is indistinguishable from a
model shrug, the guard indicator is buried in a log only you can find, or the two
refusal paths render inconsistently.

> Findings:
>
> _______________________________________________

## HITL-6 — Edge realism (3 unscripted minutes)

**(a) Action.** No script. For 3 minutes, act like a bored evaluator: reload the page
mid-run; hit STOP then START on the demo player; fire two turns fast without waiting;
ask something weird ("What's Ray's favorite dinosaur?"), something long, something
empty-ish ("ok"); switch members mid-conversation; hit Reset while a turn is
in-flight.

**(b) Look for.** Anything that would read as *broken* rather than *limited*: stuck
spinners, a turn that never renders, duplicated rows after reload, the player state
machine wedging (can't fire after STOP), a 500 surfacing raw JSON in the UI, the
weird question producing a confident fabrication (worse than a refusal), or the
in-flight-reset leaving half-written state on screen.

**(c) PASS:** every abuse either works or fails politely and recoverably (one click
back to a working state); weird questions get refusals or graceful generality, never
invented personal facts. **FAIL:** any wedge, any raw error surfaced to the UI, any
fabricated personal fact — write down the exact click sequence so it can be
reproduced.

> Findings (exact sequence → what broke):
>
> _______________________________________________

---

## Sign-off

| item | verdict (PASS/FAIL/NOTE) | one-line finding |
|---|---|---|
| HITL-1 naturalness | | |
| HITL-2 timeline legibility | | |
| HITL-3 narration fit | | |
| HITL-4 routing plausibility | | |
| HITL-5 empty-set beat | | |
| HITL-6 edge realism | | |

Findings that need code go to `docs/debt/LATEST_DEBT.md` or ratchet into a Tier L /
INT scenario before their fix (the standing rule). Do not hot-fix the demo surface
during a HITL pass — the run you're judging must stay the run that's committed.
