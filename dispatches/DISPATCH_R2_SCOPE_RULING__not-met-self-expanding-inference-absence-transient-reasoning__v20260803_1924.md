# DISPATCH_R2_SCOPE_RULING
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (docs-only: a ruling recorded, a read-only survey, two INDEX residuals fixed —
no production code changed, per the dispatch's own preamble)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
R2 (typed inference permit), with direct bearing on R5, R6, R7, R10.

## THE ASK

Dispatch text, verbatim:

```
=== D-143 | ~/hip-roadmap | R2 RULED NOT MET — record the ruling, establish the
    remaining scope ===
STANDARD PREAMBLE. Docs + read-only survey. No production code changes.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R2.

1. RECORD THE RULING in §16, Bill's words verbatim:
   "R2's text is broader than what got built. The requirement also carries the
   no-self-expanding-inference rule, the no-inference-from-absence rule, and the
   transient-reasoning rule. The build delivered the permit object and its
   enforcement point. Whether the rest is covered elsewhere or simply unbuilt isn't
   established in the report."
   State explicitly that this is a SCOPE finding, not a rejection of D-130's build —
   the permit object and its enforcement at create_fact_node stand.

2. THEN ESTABLISH WHAT THE REPORT DIDN'T. Read-only, report before proposing anything.
   For each of R2's three unaddressed clauses — no self-expanding inference, no
   inference from absence without a validated sensing contract, transient reasoning
   creates no durable authority — answer: covered by existing code (name the call
   site), held vacuously by absence (name what would have to exist to break it), or
   genuinely unbuilt. Cite evidence per clause. Do NOT guess; UNKNOWN is an
   acceptable answer with what would determine it named.

3. NOTE for the record: A2 is now WRITABLE (D-130 closed the reason it wasn't) and
   has never been written or run. R2 has no executed acceptance. State this in §16
   alongside the ruling.

4. R10 STAYS NOT MET — one of its four checks rests on an unproven requirement.
   Record that reason. A10 stays xfail(strict=True), untouched. Do not re-tier.

5. INDEX RESIDUALS owed from D-130: its own dispatch doc and TD-151's debt-register
   version bump were never registered (committing around the cutover lane's dirty
   INDEX). Add both rows.

6. Rule nothing else. Report LONG to a dispatch doc.
```

## WHAT WAS DONE

1. Gate checked (`bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` /
   `roadmap`) — matched. Tree state confirmed `ahead 0 / behind 0`.
2. Lock read first (absent), taken noclobber: `holder: D-143 (R2 RULED NOT MET — record
   ruling, establish remaining scope)`.
3. Re-read R2's full text (`:225-247`) plus its neighbors R3-R7 (`:249-364`) in full — the
   three clauses Bill's ruling names (`no self-expanding inference`, `no inference from
   absence`, `transient reasoning`) turned out to be R5, R6, R7 respectively: separate,
   separately-headed requirements in the same file, not sub-clauses inside R2's own text
   block. Recorded as found, not silently corrected in the ruling's own quoted words (which
   are reproduced verbatim regardless of this).
4. Surveyed R5 (self-expanding inference): traced every consumer of `derived=True` across the
   tree (`trust.py`, `injection_contract.py`, `api.py`'s render hints, `curator_shadow.py`'s
   fixed feature key), and specifically checked whether `_escalate_pass` (the must-confirm
   queue mechanism) could touch a derived fact — it cannot, structurally (query scoped to
   `write_state='unresolved'`; derived facts are always `write_state='augment'` per
   `_write_derived_node`).
5. Surveyed R6 (inference from absence): full-tree grep for sensing-contract/inactivity/
   last-seen vocabulary (zero hits); read the real `GroqInterpreter.abstract()` prompt
   (`memory_engine/interpreter.py:368-416`) directly to confirm its input shape (a list of
   facts that exist) structurally cannot represent an absent signal.
6. Surveyed R7 (transient reasoning): identified `eval/test_ceiling_representation.py` as R7's
   own existing, wired-in acceptance battery (A7) — already known to this session from a
   naming-collision check during D-140 — read its docstring in full to confirm what it proves
   and does not prove.
7. Confirmed A2's non-execution: full-tree grep for `inference_permit`/`ABSTRACTION_PERMIT`
   across `eval/` — zero hits.
8. Recorded R2's NOT MET ruling in §16, verbatim, with the SCOPE-not-rejection statement, the
   three-clause survey, the A2 finding, and the R10 interaction — as a new dated entry, with
   the prior D-130 "reported, not ruled" entry annotated historical rather than rewritten.
9. Corrected R10's existing D-100 entry, which factually says `representation`/`permit` are
   "unbuildable today" — no longer true since D-130/D-140. Annotated with a dated correction
   (pre-authorized ruling class: "correct a status-vs-authoritative-section contradiction by
   annotation, never silent patch") rather than editing the original wording.
10. Registered the two INDEX residuals using the surgical technique (STANDARD PREAMBLE item
    2): saved the dirty union copy, reset `docs/INDEX.md` to HEAD, applied both edits to the
    clean base, `git add`, restored the union copy to the working tree — verified the staged
    diff contains only my 2 edits (`2 insertions, 1 deletion`, matching one new row + one
    modified pointer-row exactly) and the working-tree diff against the index contains only
    the cutover lane's original 4 rows, unchanged.
11. Wrote this dispatch doc.
12. Staged by explicit pathspec, committed, pushed, released the lock.

## WHAT WAS FOUND

### R5 — no self-expanding inference: HELD VACUOUSLY BY ABSENCE, unmonitored

R5's text (`:306-317`): a "sensitive hypothesis" (a derived fact) may trigger only a pause, a
neutral human-review suggestion, a predefined authorized workflow, or an emergency response —
never more questions in its own domain, a new/widened permit, a wider audience, or extended
retention.

Every place `derived`/`derived=True` is read was enumerated:
`memory_engine/trust.py:84` (confidence cap — narrows, does not expand),
`harness/injection_contract.py:514,530` (excludes derived facts from a read path — narrows),
`memory_engine/api.py:294-318` (render-hint text only — no side effect),
`harness/curator_shadow.py:128` (one of the shadow scorer's ten FIXED, ABSOLUTE-tier-pinned
feature keys — a retrieval-prioritization signal, considered and distinguished from
evidence-gathering authority, not conflated with it), and the R18 cascade (closes children on
a parent's retraction — narrows).

The one mechanism that COULD look like self-expansion — `_escalate_pass`'s must-confirm
queue (`memory_engine/consolidate.py:722-779`, R5's own explicitly-permitted "neutral
suggestion that human review may help") — is structurally excluded from derived facts:
its query is `WHERE f.write_state = 'unresolved'`, and `_write_derived_node`
(`:502-549`) always stamps `write_state="augment"`. Verified by reading both functions
directly, not inferred.

**What would break this:** any future code that reacts to `derived=True` (or specifically
`attribute='risk_pattern'`) by triggering additional targeted extraction/questions, a
new/widened `inference_permit`, a broader `audience_policy`/`recipient_ref` than
`classify_write` assigned, or a longer retention window. Nothing today watches for this
addition — the vacuous holding is real but unmonitored, unlike R7 below.

### R6 — no inference from absence: HELD VACUOUSLY BY ABSENCE, unmonitored

R6's text (`:319-337`): deriving a fact from a signal's absence requires a validated sensing
contract (six named properties); named prohibited examples include "no medication confirmation
→ medication not taken" and "no reply → confusion or incapacity."

Full-tree grep for `sensing_contract`, `inactivity`, `days_since`, `last_seen`, `no_signal`:
zero hits in production code. The real abstraction prompt
(`memory_engine/interpreter.py::GroqInterpreter.abstract`, `:368-416`) receives `episodes` — a
list of facts that DO exist, built from positively-stated attribute/confidence pairs
(`_abstract_pass`'s subject-grouped candidate query, `consolidate.py:430-500`). It never
receives a representation of what's missing. The live fact-change path
(`harness/fact_change.py`) is the same shape: its input is an uttered statement, inherently
presence-only. This is a structural absence of the INPUT SHAPE absence-reasoning would need,
not merely an unexercised instruction.

**What would break this:** any future feature computing an absence/inactivity signal and
feeding it into `abstract()` or `classify_write()`. No sensing-contract mechanism (the
six-property gate R6 requires before absence-inference is ever permitted) exists anywhere to
catch it if that happened.

### R7 — transient reasoning creates no durable authority: COVERED, by an active regression tripwire

Distinguished deliberately from R5/R6 above: `eval/test_ceiling_representation.py` is R7's own
acceptance row (A7), already built, already wired into `scripts/run_harness.sh`. It AST-scans
every production module for reasoning/scratchpad/chain-of-thought-shaped fields on any durable
write, with its own fault twin (a synthetic module proven to be flagged) and a metamorphic
renaming check. Its own docstring states precisely what it proves: **"A7 passes today because
nothing in the codebase persists model reasoning traces at all — it holds by ABSENCE, not by
CONTROL... this must never be cited as though it were [a refusal demonstration]."** The
underlying property is the same SHAPE as R5/R6 (true today because nothing tries), but R7 has
an ACTIVE MONITOR that R5/R6 do not — a future violation turns this battery red on the commit
that introduces it; a future R5/R6 violation would land silently.

### A2: WRITABLE, never executed

D-130 built `harness/inference_permit.py::ABSTRACTION_PERMIT` and its enforcement at
`create_fact_node`, closing the reason A2 was UNWRITABLE. No test named `A2` exists, and no
test anywhere imports `harness.inference_permit` or `ABSTRACTION_PERMIT` — a full `eval/` grep
returned zero hits for both. **R2 has no executed acceptance of any kind**, independent of the
scope gap above.

### R10: stays NOT MET, reason recorded and R10's own §16 entry corrected

R10's four `create_fact_node` revalidations (origin, registry, representation, permit) were
verified at D-140 to all fire structurally: `found == {"origin", "registry", "representation",
"permit"}`. This does not flip R10 to MET. `permit` implements R2, now RULED NOT MET by this
dispatch; `representation` implements R8, still "reported, not ruled" (D-140) — neither
requirement is settled, so a correctly-executing check does not make its governing requirement
proven. `A10` stays `xfail(strict=True)`, `_a10_enforced_at_creator()` untouched, not re-tiered
— per explicit instruction, the same as both D-130 and D-140 held.

R10's existing §16 entry (D-100, `:1375-1396`) states `representation`/`permit` are
"unbuildable today" — factually stale since D-130/D-140 and left silently wrong would mislead
a future reader into thinking the checks still don't exist. Annotated with a dated correction
(not rewritten) explaining exactly what changed and why the NOT MET verdict itself is still
correct despite the stale sub-reasoning.

### INDEX residuals

Confirmed via grep (`D-130`, `TD-151`) that neither was registered anywhere in `docs/INDEX.md`
before this dispatch. Two rows added: D-130's own dispatch doc, in the
`requirements/`-section chronological log next to its sibling D-131 (the established, if
informally chronological, precedent for REQ_STRUCTURAL_CEILING-lineage dispatches); and the
`techdebt/` section's single pointer row, updated to the current versioned file
(`DEBT_REGISTER__v20260803_1455.md`) with a prepended `UPDATED` note describing TD-151, matching
the existing chain-of-updates convention in that cell.

## VERIFIED

**Watched run:** every code claim above was read directly from the file cited, not recalled —
`_escalate_pass`'s query and `_write_derived_node`'s `write_state` stamp were both read in
full; the abstraction prompt was read in full; the full-tree greps for R5/R6-relevant
vocabulary were executed and returned the stated (zero or enumerated) results; the A2 grep was
executed and returned zero hits; the INDEX grep for D-130/TD-151 was executed and returned zero
hits before this dispatch's edits. The surgical INDEX edit's isolation was verified directly:
staged diff = exactly 2 insertions/1 deletion (one new row, one modified pointer row);
unstaged diff (working tree vs index) = exactly the cutover lane's original 4-row addition,
byte-for-byte unchanged from prior dispatches' own captures of it.

**Reasoned about:** that R5/R6's vacuous holdings are "unmonitored" (as opposed to R7's active
monitor) is a structural inference from the absence of any equivalent scanning battery for
either — confirmed by absence of a matching file/test name, not by an exhaustive claim that no
such battery could exist anywhere unnoticed. The R10 "downstream, rests on an unproven
requirement" framing is this session's own synthesis of D-140's live probe result plus D-143's
own R2 ruling, not something read from a single source.

## HASH

Staged for commit alongside this doc: `docs/requirements/REQ_STRUCTURAL_CEILING__
dimensioned-collection-limit__v20260802_2205.md` (§16: R2 NOT MET ruling, R10 correction) and
`docs/INDEX.md` (two residual rows, surgically isolated from the cutover lane's untouched WIP).

## OPEN

- **R5 and R6 have no standing regression tripwire.** Both are true today by absence alone,
  matching R7's own shape, but unlike R7 neither has an equivalent AST-scanning battery. A
  future dispatch could close this gap the same way A7 already models — not attempted here
  (read-only survey, no code changes, per the preamble).
- **The three clauses' true status could still shift** if a future build adds any of the
  named breaking mechanisms (self-expansion trigger on a derived fact, an absence-signal input
  to `abstract()`/`classify_write()`, a durable write from transient reasoning). This report
  is a snapshot, not a permanent guarantee — the vacuous-by-absence framing is explicit about
  that fragility, matching A7's own documented caution.
- **R2 is NOT MET; A2 has never run.** Whether R2 should be considered MET once R5/R6/R7's
  coverage is formalized (tripwires built) and A2 is written/executed, or whether R2's scope
  should be narrowed instead (leaving R5/R6/R7 as fully independent, separately-ruled
  requirements with no bearing on R2's own MET status), is Bill's call — not decided here.
- **R8 remains "reported, not ruled."** R10's second unproven leg. Not this dispatch's scope.
- **Nothing else ruled**, per instruction.
