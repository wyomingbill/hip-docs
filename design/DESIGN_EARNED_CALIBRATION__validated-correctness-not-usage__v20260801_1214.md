# DESIGN_EARNED_CALIBRATION — earned calibration keyed on validated correctness, not usage
Status: PLAN
Reconciled-Against: b88e629 (roadmap HEAD at filing)
Dispatch: D-88, 2026-08-01
Filed against: **TD-140** (the R18 recompute branch never executes)

**THIS IS A DESIGN NOTE, NOT A REQUIREMENT.** It proposes no requirement and no status. It
authorizes no code. CLAUDE.md item 8's gate is not satisfied by this document for any
build. Its purpose is to capture an idea *with its known collision already attached*, so
that whoever picks it up does not rediscover the collision the hard way.

---

## 1. THE IDEA (Bill's)

Early in a household's life with HIP, retracting one source should simply **kill** the
derived fact that depended on it. HIP is new, it has little basis for judgment, and
destroying an inference is the cheap error.

Over time, HIP should be able to **rebuild** a derived fact from its surviving parents
instead of destroying it — R18's `recompute` branch, which is exactly what TD-140 records
as absent.

The transition between those two behaviors should be governed by a **system-level
confidence measure**: something that starts small because HIP is new, and grows as the
household actually uses it. The system earns the latitude to keep an inference alive.

---

## 2. THE COLLISION — stated first, on purpose

**A measure keyed on USAGE re-imports the exact defect the structural ceiling was written
to eliminate.**

`REQ_STRUCTURAL_CEILING`'s control rule:

> Engagement may justify OFFERING a deeper capability; it may never itself AUTHORIZE deeper
> collection.

And the defect that rule exists to close, from the same document's own framing: every depth
control fired only on a *negative* signal — withdrawal, decline, disengagement — and **the
population most at risk of over-collection emits none of them.** The compliant, the lonely,
the deferential, and the cognitively declining member engages *more*. Under "follow
engagement," they earned depth *faster*. The safety mechanism was structurally blind to
precisely the users it existed to protect.

"Grows as the household uses it" is that same signal wearing different clothes. A household
that talks to HIP constantly would accumulate the most system confidence and therefore the
most inferential latitude — and heavy use is not evidence that HIP's inferences are any
good. It is evidence of engagement, which the ceiling ruling already established cannot
authorize anything on its own.

This is not a reason to abandon the idea. It is a reason to key it on something else.

---

## 3. THE DEFENSIBLE VERSION — key it on VALIDATED CORRECTNESS

The measure should track **how often HIP's own inferences turn out to be right**, not how
often the household speaks to it.

Candidate signals, all about HIP's derived output rather than about member behavior:

| Signal | What it measures |
|---|---|
| **Confirm rate on HIP's own derived facts** | how often a derived fact, when surfaced, is affirmed rather than disputed |
| **Correction rate** | how often a derived fact is corrected, retracted, or superseded by a member |
| **Survival through retraction cascades** | how often a derived fact, rebuilt from surviving parents, is subsequently *not* corrected — the direct evidence that recompute would have been right |

**Measured against ground truth HIP does not control.** The signals above are member
corrections and confirmations of HIP's claims — statements about the world that HIP did not
author. That is the property that keeps this from being self-certification.

**The discriminating consequence, and the point of the whole reframing:** a household that
uses HIP constantly but corrects it half the time earns **LESS** latitude, not more. Under
a usage-keyed measure it would earn the most. That inversion is the test of whether a
proposed signal is the right kind.

---

## 4. THE SCOPE LINE THAT MAKES IT BUILDABLE

**The measure MAY gate INFERENTIAL RECOVERY.** That is: whether an *already existing*
derived fact survives — by recompute from still-authorized parents — when one of its
parents is retracted. This sits inside the ceiling, because the recovered fact is the same
fact it already was: same categories, same audience, same retention, all of which continue
to bind. Nothing new is collected and nothing widens. The measure decides only whether HIP
gets to keep something it already had, when the ground under part of it moves.

**The measure SHALL NOT gate COLLECTION DEPTH.** Not new categories, not new subjects, not
new audiences, not longer retention, not more inferential *reach*. The control rule forbids
it, and no confidence measure — however well-keyed — converts into authorization to collect
more.

That line is what makes this buildable at all: recovery is a decision about an existing
governed object, and the ceiling's five axes keep binding it either way.

---

## 5. OPEN QUESTIONS — not answered here

1. **Per-household or per-inference-class?** A single household-wide scalar is simple and
   crude: being reliable about medication schedules would buy latitude on relationship
   inferences, which is not obviously earned. Per-class is better targeted and much
   sparser — a small household may never generate enough corrections in a class for the
   measure to mean anything. Unresolved.
2. **Can it ever DECREASE?** If it can, a run of corrections should claw latitude back —
   which is the honest behavior, and also means a derived fact that survived a cascade last
   month might not survive an identical one today. If it cannot, the measure is a ratchet,
   and a ratchet on inferential latitude is the thing the ceiling exists to prevent.
   Unresolved, and this one is load-bearing.
3. **What prevents it becoming an optimization target?** **The evaluator-is-not-optimizer
   house rule applies in full.** The moment "system confidence" is a number anyone wants to
   go up, there is pressure to surface inferences likely to be confirmed, to avoid
   surfacing ones likely to be corrected, and to define "correction" narrowly. That is
   Goodhart operating on a safety control. Note the direct tension with `A27`/`R27`, which
   forbids any objective that rewards acceptance — a confirm-rate measure is *structurally
   adjacent* to an acceptance-rate objective, and the distinction between them has to be
   made explicit and enforced, not assumed.
4. **Cold start.** With no confirmations, the measure is at its floor and HIP always
   invalidates. That is the correct default and matches the built behavior today — worth
   recording that TD-140's current state *is* the floor of this design, not a departure
   from it.
5. **Whose correction counts?** A correction by the fact's subject, by its author, and by
   an unrelated household member are not equivalent evidence, and treating them as one
   number would let one member's disputes move another's latitude.

---

## 6. RELATION TO WHAT IS BUILT

Today (D-81, `4ae70cc`) the cascade invalidates unconditionally and records
`cascade_recompute_eligible` / `cascade_recompute_from` on the closed child. **Nothing
consumes those fields.**

If this design were ever built, that flag is where it would attach: eligibility is already
computed structurally (≥2 surviving parents), and the measure would supply the second
condition. **Recording that is not a recommendation to build it** — TD-140 stays open, R18
stays NOT MET, and the current unconditional-invalidate behavior remains the safe floor
described in §5.4.

**Cross-references:** TD-140 (the gap this note addresses), TD-139 and TD-141 (the other two
R18 gaps), `REQ_STRUCTURAL_CEILING` R18 and §16's R18 ruling, the control rule and A27/R27,
and `REQ_ARCHITECTURE_BOUNDARY` §4 — a recompute is a model-authored write, so "models
propose, only the core commits" binds anything built here.
