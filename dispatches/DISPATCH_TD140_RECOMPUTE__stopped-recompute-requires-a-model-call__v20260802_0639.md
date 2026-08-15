# DISPATCH_TD140_RECOMPUTE
Status: BUILT (as an analysis — the survey ran and stopped by design; no code was built)
Reconciled-Against: 827190a (roadmap HEAD at dispatch start)

**TYPE:** ANALYSIS

**REQ:** NONE. This is a survey required to happen *before* any REQ could be written for
TD-140's recompute branch — its own governing dispatch text says so explicitly ("SURVEY
FIRST, before changing anything... STOP AND REPORT if (b) shows recompute requires a fresh
model call. That is a different requirement than the one filed and it needs Bill's ruling,
not an implementation."). The survey below shows exactly that. No REQ is filed here because
writing one now would be guessing at a requirement Bill has not yet ruled on.

## THE ASK

> === D-104 | ~/hip-roadmap, roadmap | the recompute gap (TD-140) ===
>
> 1. AUTHORITY: REQ_STRUCTURAL_CEILING R18, ruled NOT MET 2026-08-01. TD-140 is the
> requirement gap: R18 is a two-branch rule and only the else branch exists. Nothing
> consumes cascade_recompute_eligible, so this is the ABSENCE of recompute, not a partial
> one. The built half forgets MORE than R18 requires, so today's behavior errs safe.
> ALSO READ: docs/design/DESIGN_EARNED_CALIBRATION. Its scope line binds this dispatch —
> any confidence measure may gate INFERENTIAL RECOVERY only, never collection depth.
>
> 2. SURVEY FIRST, before changing anything. Report:
> a. Where cascade_recompute_eligible is set, and everything it would need to be consumed.
> b. What "recompute from surviving parents" actually requires: does the derived fact
> retain enough to be re-evaluated, or was the original derivation an unrepeatable
> model call? If it cannot be recomputed without calling a model again, say so — that
> changes the shape of the fix entirely.
> c. The evidence floor: consolidate requires >= 2 source facts. What happens when a
> retraction leaves exactly one surviving parent — is that an invalidate, or a
> recompute that then fails its own floor?
> d. Whether a recomputed fact keeps its original trust level, or re-derives it.
> STOP AND REPORT if (b) shows recompute requires a fresh model call. That is a different
> requirement than the one filed and it needs Bill's ruling, not an implementation.
>
> 3. THEN IMPLEMENT recompute-then-invalidate per R18, if the survey is clean.
> [...]
>
> 4. TD-139 and TD-141 are NOT in scope. Report whether this changes either.
>
> 5. Run --layer 7 plus RATCHET plus the memory harness. [...]
>
> 6. Rule nothing MET. A18 passes today and R18 is NOT MET; that stays true until Bill rules.
>
> 7. Lock — check held-and-alive first. Release, commit with explicit pathspecs, push, print
> the full report to the terminal.

Gate passed clean at start: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @
`827190a` (D-103's HEAD — A12 re-tiered LIVE, R12 MET, in a parallel session; unrelated to
this dispatch, noted not investigated). Repo `.env.dev` sourced, not `~/.env.dev`.

## WHAT WAS DONE

Read `docs/design/DESIGN_EARNED_CALIBRATION__validated-correctness-not-usage__v20260801_1214.md`
in full (item 1). Traced `cascade_recompute_eligible` to its one write site
(`harness/derivation_cascade.py::cascade_from_parents`) and read the whole module. Traced the
original derivation path it would need to repeat: `memory_engine/consolidate.py::_abstract_pass`
→ `Interpreter.abstract()` → `memory_engine/interpreter.py`'s `GroqInterpreter.abstract()`, the
real production implementation. Confirmed the evidence floor (`MIN_PARENTS_FOR_RECOMPUTE = 2`)
is the same constant `_abstract_pass` itself uses (`len(episodes) < 2: continue`). Stopped at
item 2(b) per the dispatch's own explicit instruction — no code was written, no confidence
measure was designed, `--layer 7`/RATCHET/memory-harness were not re-run because nothing
changed to verify against.

## WHAT WAS FOUND

**(a) Where `cascade_recompute_eligible` is set, and everything it would need to be consumed.**
Written in exactly one place: `harness/derivation_cascade.py:130-131`, inside
`cascade_from_parents()`, on the CLOSED child node, alongside `cascade_recompute_from` (the
list of surviving parent fact_ids). `eligible = len(alive) >= MIN_PARENTS_FOR_RECOMPUTE`
(`derivation_cascade.py:123`). Nothing reads either field today (confirmed by grep — zero
other hits across the repo). To be consumed, something would need: (1) a query for closed
`:Fact` nodes with `cascade_recompute_eligible = true` (a later consolidation pass, per the
module's own docstring at `derivation_cascade.py:24-31`, which already names this shape:
"recompute eligibility is recorded on the closed node for a later consolidation pass to
act on"); (2) a call into the SAME abstraction path that produced the original derived fact,
now scoped to `cascade_recompute_from`'s surviving-parent subset; (3) on success, a new
`:Fact` node via the same `create_fact_node` single materialization point (D-96), with fresh
lineage; (4) on failure or a zero-fact return, no action — the child is already invalidated,
which is the correct terminal state either way (this is why the module's docstring insists
invalidation happens synchronously and first: "a still-active child whose recompute failed
is not" correct).

**(b) STOP CONDITION FIRED.** The original derivation is not repeatable from stored data — it
is a live model call. `memory_engine/consolidate.py::_abstract_pass` (lines ~459-464 at HEAD)
groups an owner's non-derived facts by subject and calls `interpreter.abstract(episodes)` —
"MODEL judgment; CODE writes result," per its own comment. The real, production interpreter is
`memory_engine/interpreter.py::GroqInterpreter`, which calls out to Groq (Llama 4 Scout) to
produce zero or more `DerivedFact` objects — `Interpreter.abstract()`'s own docstring: "Returns
zero or more DerivedFact objects; code writes them to Neo4j." `harness/derivation_cascade.py`'s
own module docstring already says this in different words, written at D-81 before this
dispatch existed: **"Recompute is not attempted synchronously. Re-deriving a consolidated fact
requires an LLM abstraction call... If that call were made inside the retraction path, a
timeout or a refusal would leave the child ACTIVE."** This dispatch's survey confirms that
sentence is not a caution about timing — it is a statement that **"recompute" as R18 names it
cannot be built as a pure function of stored data at all.** Any implementation calls a model
again, with no guarantee it returns the same fact (or any fact) the second time. **That is a
different requirement than "recompute child and replace lineage" reads on its face** — R18's
text describes a mechanical operation; what would actually have to be built is a second,
independent derivation attempt that may or may not agree with the first. Per the dispatch's
own instruction, this needs Bill's ruling, not an implementation, and none was attempted.

**(c) The evidence floor and the one-surviving-parent case.** `MIN_PARENTS_FOR_RECOMPUTE = 2`
(`derivation_cascade.py:49`) is the exact same constant `_abstract_pass` enforces
(`len(episodes) < 2: continue  # not enough for an abstraction`, `consolidate.py:460`) — the
two floors are not independently chosen, they are the same number read in two places. When a
retraction leaves exactly one surviving parent: `eligible = len(alive) >= 2` evaluates `1 >= 2`
= **False**. **This is a plain invalidate, never a recompute attempt that then fails its own
floor.** The eligibility check gates entry to recompute BEFORE any recompute would be
attempted — there is no code path today where recompute is tried and then fails the evidence
floor; the floor is checked first, structurally, and only a genuinely-eligible child (≥2
surviving parents) would ever reach a hypothetical recompute step.

**(d) Trust level of a recomputed fact.** Not preserved, because there is nothing to preserve
from in the current design: `_abstract_pass` unconditionally clamps every newly-derived fact
to `confidence = "low"` (`consolidate.py:468`, "Clamp confidence to 'low'") regardless of how
many episodes fed it or how confident those episodes were. A recomputed fact, if built, would
go through the identical path and receive the identical clamp — there is no mechanism today
for a fact to inherit or re-derive a "trust level" from the derivation it replaces, because the
abstraction pass does not read or propagate one from its inputs in the first place. This
matches R18's own text ("recompute child and replace lineage") read literally: replacement, not
inheritance.

## VERIFIED

- **Watched run:** none required for the survey itself — every claim above is a direct code
  citation, not a live execution. The one thing worth being explicit about not having run: no
  live Groq call was made to confirm `GroqInterpreter.abstract()` behaves as documented: this
  finding rests on reading its docstring, its caller's comment ("MODEL judgment; CODE writes
  result"), and the cascade module's own pre-existing docstring, three independent statements
  agreeing with each other, not on watching a call execute.
- **Reasoned about:** (a)'s "everything it would need to be consumed" list (items 1-4) is a
  design inference from the existing code's shape and the module's own docstring, not a
  description of code that exists — nothing consumes the field today, by direct grep (zero
  hits).
- `--layer 7`, RATCHET, and the memory harness were **not run**. No code changed; there is
  nothing to verify a delta against, and running them would confirm only that nothing moved,
  which the git diff already shows directly (this dispatch is docs-only).

## HASH

Committed as a docs-only dispatch (this doc + INDEX registration + a TD-140 addendum in the
debt register). No production or test code changed. See the commit for the hash.

## TD-139 / TD-141 — explicitly out of scope, and unaffected

**TD-139** (the lineage block is 2 of R18's required 11 fields) is untouched by this survey —
it concerns what gets *recorded* about a derivation, not whether recompute can be attempted,
and nothing here changes that gap's shape or size.

**TD-141** (the live graph's one derived fact has an empty `derived_from`, so the cascade is
correct but currently inert against real data) is also untouched — it is a data-state finding
about what exists in the graph today, independent of whether a recompute mechanism is ever
built. Neither TD is resolved, narrowed, or widened by this dispatch.

## Nothing ruled MET.

A18 passes today (the invalidate-only cascade); R18 is NOT MET (ruled 2026-08-01, unchanged).
That gap stands exactly as it did before this dispatch — this survey does not close it, and
does not attempt to.

## OPEN

**The actual open question, unresolved by design:** is "recompute" as R18 names it even the
requirement Bill wants built, given that a real implementation is a second, independent model
call rather than a mechanical re-derivation from stored data? Concretely, three shapes a ruling
could take, named here so the next session does not have to re-derive them:

1. **Rule R18's text amended** to describe what recompute actually is (a fresh derivation
   attempt over the surviving evidence, which may disagree with or fail to reproduce the
   original) rather than the mechanical "recompute child and replace lineage" it currently
   reads as.
2. **Build it as specified anyway**, accepting that "recompute" means "ask the model again and
   accept whatever it returns, including nothing" — with the non-determinism and the DESIGN_
   EARNED_CALIBRATION collision (a confidence gate on WHETHER to even attempt this, scoped
   strictly to inferential recovery per that design's own scope line) as a live open question
   about whether every eligible child gets a recompute attempt unconditionally, or whether that
   too needs gating.
3. **Leave TD-140 open and R18 NOT MET indefinitely**, on the basis that the built half (invalidate-only) already errs toward the safe direction and a model-call-dependent recompute is a
   large enough behavior change to deserve its own REQ and acceptance criteria before any code
   is written — which is what CLAUDE.md's own gate would require regardless of this dispatch's
   finding.

This dispatch does not recommend one of the three. It exists so whichever the next dispatch
picks, it is picking with this finding already on the table rather than rediscovering it.
