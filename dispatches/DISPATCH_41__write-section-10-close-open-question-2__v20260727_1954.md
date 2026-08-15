# DISPATCH_41
Status: BUILT
Reconciled-Against: see HASH below (same commit as this doc)

**TYPE:** BUILD (docs only, ratifies stated positioning into the diligence
deliverable; no code, no REQ acceptance test)

**REQ:** none named. This dispatch writes ratified positioning into
`docs/deliverables/HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md`,
a diligence deliverable, not a REQ doc — no build starts against it, so
Requirements Discipline item 8's gate does not apply the way it does to a
code-changing dispatch.

## THE ASK

> Rewrite HIP_ArchitectureForDiligence Section 10 (Long vision) from
> Bill's ratified positioning, and close Open Question 2.
>
> THE THESIS, verbatim: Vertical depth, world modeling, and multi-modal
> input are not separate bets; each is the same governed substrate
> extended — new input classes in, predictive structure over it, domain
> context packs on top. The models involved commoditize; the substrate
> does not.
>
> THREE POSITIONS, ratified 2026-07-27: [1. multi-modal input is
> perception, cross-referencing REQ_PARTITION_CUSTODY's observation-
> custody positions; 2. world model means the graph made predictive,
> positioned as the destination the context manager's later generations
> point toward; 3. verticality lives in governed context, not in
> domain-specific models.]
>
> ORDERING, stated plainly: perception inputs enter when the custody
> positions ratify; the predictive layer enters after the learning
> substrate exists; vertical context packs can begin at any time, because
> they are rules and taxonomy, not models.
>
> Keep it in the document's voice: flat declarative sentences, fact then
> reason, no em dashes, no rule-of-three. Mark Section 10 ratified with
> today's date. Remove Open Question 2 and update the count.
>
> Commit, push, report the hash and the remaining Open Questions.

(Full text of the three positions given in the dispatch is reproduced
verbatim in the section itself, not abbreviated here.)

## WHAT WAS DONE

1. Confirmed the document's current state fresh before editing — this
   file has been actively edited in place by other sessions today
   (DISPATCH 35, 36, 38, 38a, 40 all touch it per its own changelog
   line). Read Section 10 and "Open questions for Bill" in full,
   current, before writing anything.
2. Marked the Section 10 header `(positioning ratified 2026-07-27,
   DISPATCH 41)` and added one lead sentence scoping exactly what is
   ratified: the thesis and the three positions. Stated explicitly, in
   the same sentence, what is NOT ratified by this: the six-generation
   roadmap itself (already marked proposed, unchanged) and the
   observation-and-perception custody positions position 1
   cross-references (tracked separately in REQ_PARTITION_CUSTODY,
   themselves still awaiting ratification per DISPATCH_39).
3. Kept the six-generation list byte-for-byte unchanged — out of this
   dispatch's scope, and Generation 6 ("predictive context assembly") is
   cited by name from the new world-model position rather than rewritten.
4. Replaced the old paragraph naming this as an open, unpositioned
   question, and the old observation-custody paragraph, with the thesis,
   the three positions, and the ordering statement. Folded the
   observation-custody paragraph's substance into position 1 rather than
   keeping both — REQ_PARTITION_CUSTODY (DISPATCH_39) now carries the
   full detail; Section 10 needed one cross-reference, not two
   overlapping ones.
5. Twice during this edit the file changed under me from a concurrent
   session (DISPATCH 38a's Open-Questions restoration landing live, then
   a further edit). Re-read the current state fresh before each
   subsequent edit rather than trusting the version last read — the tool
   itself flagged both instances, and both were treated as a stop-and-
   recheck, not an ignore-and-proceed.
6. Removed Open Question 2 (vertical/world-model/multi-modal
   positioning) from "Open questions for Bill," added a dated
   `FURTHER UPDATE 2026-07-27 (DISPATCH 41)` paragraph matching the
   existing DISPATCH 38 / 38a changelog convention, and renumbered the
   remaining items (old 3/4/5/6 to new 2/3/4/5). Left the `Item 7 —`
   / `Item 8 —` labels on the former items 5/6 untouched — those are
   historical identifiers from the original eleven-item numbering, not
   list-position numbers, and renumbering the list position does not
   change what they refer to.
7. Appended a matching dated note to the top-of-file `Reconciled-Against`
   changelog line, the same append-only convention every prior dispatch
   touching this document has used.
8. Checked the new prose against the style constraint directly: grepped
   my own additions for `—` (none), and re-read for rhetorical
   three-part constructions. The one three-item list retained (`sealed
   to the right audience, process-and-discard..., and corroborate-never-
   confirm...`) is substantive, three named REQ_PARTITION_CUSTODY
   positions, not a decorative triad, and mirrors the dispatch's own
   phrasing rather than inventing new structure.

## WHAT WAS FOUND

The document's own top-of-file changelog line claims, ahead of DISPATCH
40, that Open Question 1 (multi-tenancy platform posture) was
"reclosed." The "Open questions for Bill" list body, read fresh
immediately before this dispatch's own edits, still carries item 1 as
open ("REOPENED 2026-07-27"), unresolved in the list itself. This is the
same shape of gap DISPATCH 38a found and fixed for items 7/8 (a
changelog claim landing before the corresponding body edit) and it is
still present for item 1 as of this dispatch. Not this dispatch's to
fix — named here so it is not silently missed, matching the register-
discrepancy convention every other dispatch in this session has followed.
The list itself, after this dispatch's edit, still shows item 1
unresolved, unaffected by this dispatch's own item-2 closure.

## VERIFIED

- **Watched, direct read:** the full current Section 10 and Open
  Questions text, twice, re-read fresh after each concurrent-edit
  interruption, not assumed from an earlier read.
- **Watched:** `git diff` after each edit, confirming only the intended
  hunks landed and no concurrent session's own uncommitted content was
  overwritten or reverted by mine.
- **Reasoned about, not independently re-derived:** the substance of the
  thesis and the three positions is Bill's own ratified content, taken
  as given. This dispatch's own work was placement, cross-referencing,
  voice, and the open-question bookkeeping around it, not evaluating
  whether the positioning itself is correct.
- `git status` immediately before commit confirmed exactly one file
  changed by this dispatch: the architecture deliverable itself.
  `docs/INDEX.md` and `docs/deliverables/MANIFEST.md` were both, and
  remain, modified by a concurrent session — not touched here, same
  caution the three prior dispatches in this session applied.

## HASH

See commit — this dispatch doc and the architecture-deliverable edit
ship together.

## OPEN

- Item 1 (multi-tenancy platform posture) reads as still-open in the
  Open Questions list despite the top-of-file changelog's claim that
  DISPATCH 40 reclosed it. Named under WHAT WAS FOUND; not resolved by
  this dispatch.
- Five items remain in "Open questions for Bill" after this dispatch:
  1. Multi-tenancy platform posture (reopened 2026-07-27; see the OPEN
     note above on its changelog-vs-body discrepancy).
  2. Observation-and-perception custody (positions on record in Section
     10 and in REQ_PARTITION_CUSTODY, ratification itself still open,
     plus the two sub-questions named there).
  3. The four-tier deployment hierarchy.
  4. Training-data record (restored as a gated-moat item, DISPATCH 38a).
  5. Federated learning (restored as a gated-moat item, DISPATCH 38a).
- `docs/INDEX.md` does not yet register this dispatch doc, per instruction
  not to touch it — whichever session next holds that file should add it,
  same as DISPATCH_39's own OPEN note.
