# SIA Phase B: risk memo

Version: v20260716_0800 MT
Supersedes: HIP_Theory__turn-type-ontology__v20260715_2230.md
Revised after Fable review, 2026-07-15. Four corrections accepted, all material.

REQ: docs/requirements/REQ_HARNESS__orthogonal-e2e-regression-per-push__v20260715_1700.md
Spec: SIA_SPEC__structured-intent-architecture__v20260710_1614.md
Evidence: docs/deliverables/HIP_Findings__disclosure-pipeline__v20260715_1900.md
Register: docs/deliverables/HIP_DefectRegister__v20260715_1930.md

---

## WHAT THIS IS

The v2230 draft proposed designing a turn-type ontology. That ontology already
exists: SIA, spec'd 2026-07-10, Phase A shadow-running on every turn
(`harness/sio.py`). The draft was written without reading it.

That is worth keeping rather than burying, because it is the strongest evidence
in the document: **two independent derivations of the same type, from opposite
directions, five days apart.** The spec author reasoned forward from design.
The draft reasoned backward from six defects. Both landed on speech-act plus
subject, stateless, fail-closed on low confidence. CORROBORATED, on HIP's own
ladder — and corroboration is the rung the whole product is built to notice.

So this is not a proposal. It is the risk memo for a cutover that is already
specified, already half-built, and gated on a number that is not what it looks
like.

---

## 1. THE DIAGNOSIS THAT SURVIVED

`intent` is a category error. Five values encoding three different kinds of claim:

| value | is a claim about |
|---|---|
| `personal` | the **subject** |
| `action` | the **speech act** |
| `knowledge` | **answerability** |
| `temporal` | **answerability** |
| `noise` | the **speech act** |

The classifier is asked to answer three questions with one label, so it answers
one and discards the rest.

**"What's Ray on?"** is *question / non-member subject / owned by requester*. The
classifier compressed that to one token, picked the answerability axis, guessed
wrong, and the subject axis — the only one that mattered — had no field to be
right in.

**Fail-open is a corollary, not a cause.** This is the argument Fable could not
break and it stands regardless of what ships:

> If a five-valued enum must encode three axes, some values mean several things
> at once, and the fallback value inevitably means the least constrained thing.
> `knowledge` is the residue — what is left when nothing matched. And the residue
> category is the one that disarms INJ-5, both empty-set guards, and the
> grounding instruction. Not by design. **By arithmetic.**

Consequence: adding third-party exemplars helps and does not fix it. The type
still cannot express "question, about a non-member, in the graph." The
information has nowhere to go.

## 2. THE FIX SHAPE — PUBLISH THE DECISION, NEVER RE-DERIVE IT

Fable's answer to "is this a type system or just extract-a-function," and it is
better than the question. Look at which fixes actually held this week:

| Fix | Shape |
|---|---|
| `guard_kind` | the contract **publishes which guard fired**; the L3 wrapper stopped recomputing |
| `park` | the write path **publishes its decision**; G4 stopped guessing |
| `delta` / `inj2_declarative_override` | same, for G1 |

One shape: **a stage publishes its decision as a record field; downstream reads
the decision and never re-derives it.**

The codebase already states this. FLAG-3 in `epistemic_record`: *"a label of the
decision already made, never a re-derivation."* The discipline was applied to the
**record** and not to the **pipeline**. Guards re-derive turn kind instead of
reading a published classification. That is the whole defect family.

## 3. THE COUNTEREXAMPLE THAT KILLS THE WEAK VERSION

`is_declarative` was already a clean, shared, reliable single-axis value.
INJ-6b read it. INJ-6 did not. G1 did not. G4 did not.

**A shared ontology whose consumption is optional reproduces the drift with
better variable names.** Each guard hand-writing `and not is_declarative` into
its own conjunction is the same disease.

So the version that survives:

> Guards do not compose predicates from axes. They are rows in **one decision
> table**, keyed by `(speech_act × subject-relation × admitted-about-subject)`,
> exhaustively enumerated, in one module.

**A table forces every cell to be decided. A hand-written conjunction lets cells
go unconsidered** — which is literally what INJ-6's missing `not is_declarative`
was: an unconsidered cell.

Without this dispatch structure the change is extract-a-function and will fail
the same way. This is the load-bearing correction.

## 4. THE AXIS THAT WAS WRONG

The draft proposed three classifiable axes. The third does not exist.

**`answerable` is not a property of the turn.** "What is Ray's medication?" is
FROM_GRAPH only if a fact exists, which a stateless classifier cannot know — and
SIA's statelessness is LOCKED, correctly, because it is what makes the cache
sound and the golden set complete.

Classified pre-retrieval, `answerable` asks the model to guess graph contents.
**That is a fabrication generator installed at the front of the pipeline** —
the exact defect the whole effort exists to close.

Correct factoring:

- **Turn properties, classifiable:** `speech_act`, `subject`, `attribute`
- **Outcome, computed deterministically after retrieval:** did anything admitted
  match subject+attribute? INJ-6/6b already compute exactly this.

Ray Charles is not an answerability confusion. It is **subject-resolution
confidence** (D-04), and it lives on the subject axis.

## 5. THE THREE DELTAS SIA DOES NOT ALREADY HAVE

Everything above is corroboration or correction. These three are new:

**5.1 `confirmation` is missing from `VALID_TYPES`.**
`VALID_TYPES = {"question", "statement", "command", "noise"}` (sio.py:47). There
is no confirmation speech act. `"Yes, confirm that."` → `noise` → remapped to
`knowledge` (injection_contract.py:370) → park left outstanding. trust_ladder T04
died of this.

Both things are true and neither saves it: the confirmation gate deliberately
runs *before* any model, on exact vocabulary — and a near-miss like "Yes, confirm
that." falls through to the classifier, where the taxonomy has no bucket for it.

Concrete spec amendment. Add `confirmation` to `VALID_TYPES` and to the golden set.

**5.2 Cross-axis contradiction checks.**
`subject=NON_MEMBER ∧ FROM_WORLD` is coherent (Ray Charles).
`subject=NON_MEMBER ∧ FROM_GRAPH` is coherent (Ray's medication).
Today those are byte-identical at the guard and **no stage cross-checks another
stage's output.** `resolved_subjects=['ray']` coexisting with `intent=knowledge`
is a contradiction sitting inside one record, detectable with no new information.
Not in the SIA phase plan.

**5.3 The invariants do not read the type.**
G1 and G4 re-derive turn kind and needed three exemptions between them
(MULTI_VALUED, parks, declaratives). The record already carries `sio_source` and
the shadow fields. The invariants do not read them. Re-keying them to SIO fields
runs **in shadow, before cutover**, and de-risks the cutover by proving the type
is sufficient to express the policy before anything depends on it.

## 6. THE DOCTRINE WORTH KEEPING

`disclosure_oracle.py` says an oracle derived from the implementation tests the
code against itself and goes green forever. True. G1 and G4 were written on that
doctrine and were wrong anyway.

**Independence from the implementation is not independence from the ontology.**

A policy oracle written without the domain's type structure is not policy — it is
a private reconstruction of the domain, and it drifts exactly like everything
else. That is why G1 counted the product's core loop as a fabrication: it did not
know declaratives existed, because the domain's type structure is not in the
policy, it is scattered across nine derivations. There was nothing to read it
from.

**A policy oracle needs a shared ontology to be policy about.** SIA is that
ontology. That is 5.3's real argument.

## 7. THE OTHER ROOT CAUSE — NOT THIS FAMILY, AND MORE DANGEROUS

The draft claimed every defect yesterday was one defect. Over-unified. There are
two, and the second is worse.

**Gate integrity.** ORTH-1's corpus went stale when `c75655d` changed INJ-6's
policy. DISC had been red **since the patch landed**, sitting in the baseline,
announcing nothing. That is not ontology drift — a conformance corpus is
*supposed* to independently restate policy, and going stale on a policy change is
its designed failure mode.

The defect is that **a red gate can sit in the baseline and say nothing.**

- `--accept` grants permanent amnesty with one string
- known failures carry no expiry and no linked debt ID
- nothing distinguishes "accepted with justification" from "forgotten"
- `harness_run.jsonl` is truncated at the next run's startup, destroying the
  previous run's gate evidence

Fable's framing, and it is right: **this is the mechanism by which every other
defect gets to persist.** No turn type fixes it. It needs its own defect ID and
its own fix, and it is arguably ahead of the ontology in priority, because
without it the ontology's own gates can go quietly red too.

## 8. THE GATE IS NOT WHAT IT LOOKS LIKE

**Phase B cutover is Gate B. Bill's call only.** Agreement is at **85.7%**
against a **98%** bar.

Read that number carefully. **It is agreement with the incumbent, not accuracy.**

When SIA and the current stack disagree, either could be right — and yesterday
established that the incumbent is wrong on exactly the class SIA exists for.
`"What's Ray on?"` → `knowledge` is the incumbent being wrong. If SIA says
*question, about ray*, that is **correct**, and it counts against the 85.7%.

So an unknown share of the 14.3% gap is SIA being right and being penalized for it.

The bar is a safety bar: do not cut over to something that behaves differently
until you know why it differs. It is not a correctness bar. **Closing the gap by
tuning SIA toward the incumbent could mean making it wrong more often.**

**The 14.3% needs adjudicating, not shrinking.** For each disagreement: which one
is right, decided from policy, not from what the code currently does. Same
doctrine CC applied to the DISC corpus yesterday. That work is the actual content
of Gate B, and it is where the ontology gets proven or refuted.

## 9. SEQUENCE

Nothing here waits on a rewrite. Nothing gets done twice.

| # | Move | Size | Gate |
|---|------|------|------|
| 1 | **Guards stop reading `intent`.** INJ-5's "never volunteer" is expressible from the two surviving axes: personal facts inject only when `speech_act=question ∧ subject resolves to someone the facts are about`, or `speech_act=statement` (correction rule). `c75655d` already made INJ-6 intent-blind and the world got safer. | small, now | — |
| 2 | **Adjudicate the 14.3%.** Which side is right per disagreement, from policy. This is Gate B's real content. | the work | — |
| 3 | **Re-key invariants and oracle to SIO fields.** Runs in shadow. Proves the type expresses the policy before anything depends on it. | tonight-sized | — |
| 4 | **Add `confirmation` to `VALID_TYPES`** and the golden set. | small | — |
| 5 | **The decision table.** Guards become rows, not conjunctions. | real work | — |
| 6 | **SIO fail-closed goes live** per spec §2.3. | — | **Gate B, Bill only** |

Gate integrity (§7) is orthogonal to all six and should run in parallel. It is
the reason any of the rest can go quietly wrong.

---

## PROVENANCE

Written by a chat session that was wrong six times in one day reading this
codebase — including twice while arguing an instrument was broken when it was
correct, once claiming the record lies when it does not, and once writing a
theory about an ontology that had been running in shadow for five days without
opening the file.

The two arguments that survived adversarial review are §1's arithmetic and §6's
doctrine. Both are independent of whether anything here ships. Everything else in
this memo is either SIA's own spec restated, or Fable's correction of a draft
that did not know SIA existed.
