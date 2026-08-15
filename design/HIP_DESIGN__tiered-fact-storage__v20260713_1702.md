# HIP Design Note — Tiered Fact Storage (Access Heat)

Version: v20260713_1702 (Mountain Time)
Status: DESIGN — not built. Spec for a future build pass.
Author context: captured from meeting-driven architecture discussion, 2026-07-13.

## Summary

Every fact in HIP carries THREE orthogonal dimensions. Two are governance
(built). The third is operational (this note, not yet built):

1. Validity (temporal truth) — is it true now? open / closed
   (superseded / corrected). About the world. BUILT.
2. Trust (epistemic weight) — how much do we believe it? Derived / Asserted /
   Unconfirmed (live) climbing to Corroborated / Confirmed (consolidation).
   About our confidence. BUILT (entry levels).
3. Storage tier (access heat) — how fast do we need to reach it?
   Hot / Warm / Cold. About operations and cost. NOT BUILT — this note.

The core insight: these three axes do NOT correlate. A fact can be current,
relevant, and true, yet cold (a standing allergy nobody has queried in months).
Heat is about access pattern, not truth, trust, or relevance.

## Why a third axis is needed

At scale a household accumulates thousands of facts over years, across millions
of households. Keeping every fact instantly accessible is neither necessary nor
affordable. Tiered storage is the standard answer: keep frequently accessed data
fast and expensive, move rarely accessed data to slow and cheap, promote on
access. This is the same pattern as CDN edge caching (hot content near the user,
cold content in deep storage) — which is native operator competency, not a lab
one. Framing HIP memory as tiered storage speaks the operator's language.

## The heat model

Heat is driven by ACCESS and moves independently of the other two axes.

- Promote on access: a cold fact queried today becomes hot immediately.
  (A months-untouched allergy promotes to hot the instant the ER asks.)
- Decay on neglect: a hot fact untouched for a defined interval cools to warm,
  then cold. Never deleted — demoted to cheaper, slower storage.
- Independent of validity: a closed (superseded) fact can be hot (actively being
  reviewed) or cold (untouched for a year). Closing a fact does not cool it;
  not accessing it does.
- Independent of trust: a Confirmed fact can be cold; an Unconfirmed fact can be
  hot. Confidence and access frequency are unrelated.

## THE INVARIANT (non-negotiable)

Storage heat optimizes cost and latency ONLY. It must NEVER influence a
governance decision.

- A cold fact still clears the disclosure gates and reaches the model if it is
  valid, in-scope, relevant, and trusted. Cold means SLOWER TO FETCH (cache
  miss, promote-on-access), never WITHHELD.
- The moment "it was in cold storage" becomes a reason a fact was not disclosed,
  the governance guarantee is broken. Example of the catastrophic failure this
  prevents: never "we did not surface your shellfish allergy because it was
  cold."
- Disclosure is decided by validity + trust + the disclosure contract. Heat is
  INVISIBLE to that decision. Heat only affects how fast an already-admitted
  fact arrives.

This orthogonality is the whole point. Two governance axes decide WHAT is
disclosed; the third operational axis decides only WHERE it is stored and HOW
FAST it is reached.

## What must be specified before build

1. Access tracking: how last-access and access-frequency are recorded per fact
   without themselves becoming a hot-path cost.
2. Promotion / demotion policy: the interval and access thresholds that move a
   fact between hot / warm / cold. Promote-on-access is immediate; decay is
   time-based.
3. Tier boundaries: physical vs logical tiering. Hot = in-memory / fast store;
   warm = primary graph; cold = cheap deep store or compressed. (Current build:
   everything in Neo4j at one access speed — no tiering exists yet.)
4. The disclosure-blindness guarantee: prove, in the harness, that a cold fact
   is disclosed identically to a hot one (only latency differs). A conformance
   test that fetches a deliberately-cold valid fact and asserts it is admitted.
5. Cold-fetch latency budget: an admitted cold fact must still return within an
   acceptable window (promote-on-access must be fast enough not to feel broken).

## Relationship to the demo (dashboard-clarity work)

The three axes become three lenses on the same fact set in the dashboard:
- Validity/time — the scrubbable timeline (what was true when).
- Trust — color-coded rungs (how trusted).
- Heat — a hot/warm/cold view (how it is stored) — the operational lens a cable
  operator leans into.

Showing all three simultaneously on the same facts is "absolute clarity": one
fact set, three orthogonal governance/ops dimensions, visible at once. The heat
lens is also a moat argument — governed AND cost-optimized storage. Labs do not
tier governed context because they do not govern context; it is a flat pile.

## Priority placement

DESIGN item, not the next build. Committed dev sequence stays:
baseline lock -> NDA cascade -> dashboard-clarity demo.
Tiered storage is the NEXT architecture build after the demo lands, because:
- it is a genuine scaling necessity (thousands of facts/household x millions of
  households — tiering is mandatory, not optional);
- it is the operator-native framing (tiered storage = the operator's world);
- it strengthens the moat (governed + cost-optimized, which labs cannot show).

Build only after a proper spec pass that fixes the promotion/demotion policy and,
above all, PROVES the disclosure-blindness invariant in the harness.
