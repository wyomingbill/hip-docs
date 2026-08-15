Status: BUILT
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Reconciled-Against: 2026-08-03 (date-tested — read at filing, not remembered)

THE PROMPT BOTH EVAL REVIEWS ANSWERED. Sent to ChatGPT and Fable separately, asking for
evaluation methodology for an access-controlled conversational system — not attack
material. Their answers are banked at reviews/CHATGPT_EvalMethodology__evaluation-
methodology-review__v20260803_1527.md and reviews/FABLE_EvalMethodology__evaluation-
methodology-review__v20260803_1527.md.
Source file: HIP_EvalMethodology_ReviewPrompt.md (~/Downloads), banked verbatim, unedited
below this line.

---

# Prompt — evaluation methodology for an access-controlled conversational system

Send this to ChatGPT and to Fable separately. It asks for testing methodology, not for
attack material. Run it in both and compare.

---

I build a household assistant that holds records for several people who share it, and
enforces which person may see which record. I own the system and I am testing my own
enforcement. I am asking about **evaluation methodology** — how to design a test suite for
this class of system. I am not asking for attack techniques, exploit payloads, or ways to
bypass anything.

Where you can, cite established practice — software testing, safety-critical evaluation,
access-control verification, ML evaluation, or human-subject dialogue evaluation. Where
there is no established practice, say so plainly rather than inventing one. I would rather
hear "this is unsolved" than a confident answer I can't check.

## The system, briefly

Every turn, before any language model is invoked, a deterministic policy layer decides
which stored records may enter the prompt. Records that aren't authorized are not in the
prompt at all, so the model cannot disclose them — it never receives them. Each turn writes
a structured record of what was authorized, what was withheld and why, and whether a model
was invoked at all.

Two categories of failure matter to me:

- **Over-permissive**: something was disclosed that policy should have withheld.
- **Over-restrictive**: something was withheld that policy permitted, or the system gave a
  useless answer where a useful one was available.

## What I have today, honestly

- A combinatorial generator that produces test utterances from templates and asserts
  outcomes. It passes.
- A monotonic gate: a metric may never get worse than its recorded baseline.
- Per-turn structured records that state what was authorized.

## The problems I have found, and want methodology for

**1. My generator can't produce the inputs that break it.**
Every template interpolates the topic word — so it emits "What is PersonB's medication?"
and the system handles that correctly. A real user said something equivalent without the
topic word, and the system failed. The generator is structurally incapable of producing
that phrasing, because the phrasing is what makes it hard.

How do practitioners generate evaluation inputs that fall *outside* the distribution the
system was built and tuned on? Is there an accepted way to measure how far a test corpus
sits from the system's training or tuning distribution, and to deliberately sample the tail?

**2. Every gate I have rewards refusing.**
My baseline metric only moves in the restrictive direction. A system that refuses every
request would score perfectly. I know I need a second measure that fails when the system
withholds something it should have released — but I don't know the standard construction.
What does a two-sided evaluation look like in practice, and how do people avoid the two
sides being gamed against each other?

**3. My expected outcomes are derived from the implementation, not from the policy.**
Some of my assertions were written by reading the code, so a disagreement between test and
system just means someone changed the code. What is the accepted way to derive expected
outcomes from a written policy independently of the implementation, so that a disagreement
is informative? Is there a practical middle ground short of full formal specification?

**4. My tests grade the output text; the guarantee is in the mechanism.**
A refusal produced because the model was never invoked, and a refusal produced because the
model was instructed to decline, are word-for-word identical on screen and are not the same
guarantee. The distinction is visible only in the execution record. How do people write
assertions against internal execution evidence rather than output text, without coupling
every test to implementation detail so tightly that refactoring breaks them?

**5. Half my test inputs change stored state.**
Statements try to update records; questions only read. Run a hundred statements in sequence
and the fixture no longer matches what the expected outcomes were written against. What is
standard practice for state discipline in a suite where most cases mutate — reseed cadence,
isolation, ordering, detecting when a test failed because an earlier one moved the state?

**6. Some conditions I cannot measure with what I have.**
I have one real human speaker available. I can measure how often the system wrongly rejects
that person. I cannot measure how often it wrongly accepts a *different* human, because I
have no second human. How should an evaluation report a measurement it structurally cannot
take? Is there a convention for recording an unmeasurable dimension so it stays visible
rather than quietly absent?

**7. Fixed suite or regenerated per run?**
A fixed 400-item suite will eventually be tuned against and stop measuring anything. A
suite regenerated per run has no stable baseline. What do practitioners actually do, and
how do they keep a trend line when the population changes underneath it?

## Two more, if you have grounded views

**8.** Ambiguity is a governance-relevant input dimension. When a reference cannot be
resolved, the correct behavior is to say so — and the incorrect behavior is a confident
answer to a different question. Is there established practice for evaluating that class of
failure? It seems distinct from both accuracy and refusal.

**9.** Any adaptive behavior — clarification wording, response latency, whether a model was
invoked — can differ depending on whether protected content exists. Is that treated as a
side channel in evaluation practice, and if so, how is it tested?

## What I want back

For each numbered item: what the accepted practice is, where it comes from, what it costs
to implement, and where it is known to fail. Then — if you were designing this evaluation
from scratch and could build only three things this quarter, which three, and why those.

Please flag anything where you are extrapolating rather than citing. I am more interested
in a short, well-grounded answer than a complete one.
