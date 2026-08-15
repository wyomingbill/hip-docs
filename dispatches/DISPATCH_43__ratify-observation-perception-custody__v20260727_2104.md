# DISPATCH_43
Status: BUILT
Reconciled-Against: see HASH below (same commit as this doc)

**TYPE:** BUILD (docs only, records a policy ratification; no code, no
change to the REQ's MET criteria or acceptance table)

**REQ:** `docs/requirements/REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md`
(edited in place; `Status: NOT MET` unchanged, per instruction — this is a
policy ratification within one section, not a status change on the REQ)

## THE ASK

> Bill has ratified the observation-and-perception custody positions.
> Change their status in REQ_PARTITION_CUSTODY (current version via the
> LATEST symlink) from POSITIONS AWAITING RATIFICATION to RATIFIED, dated
> 2026-07-27, EXCEPT where noted below. Then update
> HIP_ArchitectureForDiligence Section 10 / Open Question and its Open
> Questions count to match.
>
> RATIFIED as written: position 1 (caregiver-subject sealing), WITH A
> STATED CAVEAT — provisional, revisits when the care-model and legal
> review land. Position 3 (process-and-discard), with the at-inference
> limit named in the same breath. Position 4 (corroborate-never-confirm).
>
> RATIFIED IN AMENDED FORM, position 2: replace the flat non-member rule
> with a three-way split — bare presence (household-scoped event),
> identity resolution against a non-enrolled person (refused), enrolled
> member or existing subject (existing scopes). The boundary is presence
> versus naming, not presence versus nothing. FLAGGED: this line itself
> is a position pending legal and care-model review, same posture as
> position 1's caveat.
>
> STILL OPEN, kept as sub-questions: standing policy extending from
> disclosure to collection, surviving incapacity; how a system-observed
> fact classifies with no author for the mandatory subject rule.
>
> Do not touch the REQ's MET criteria or acceptance table. Date the
> section. Cross-reference the scope doc. Commit, push, report the hash
> and confirm the scope doc's Open Questions count dropped by one.

## WHAT WAS DONE

1. Re-read both target documents fresh, current, before editing —
   `REQ_PARTITION_CUSTODY`'s observation-and-perception custody section
   (landed DISPATCH_39, untouched since) and the scope doc's Section 10
   and Open Questions list. The scope doc had moved since DISPATCH_41:
   DISPATCH 40/42 closed the old item 1 (multi-tenancy) and added a new
   item 5 (edge-node concurrency), so observation-and-perception custody
   is item 1 today, not item 2 or item 3 as in earlier dispatches. Worked
   against the current numbering, not a remembered one.
2. Rewrote the REQ section's header and opening framing from `NOT
   RATIFIED` to `RATIFIED, WITH NAMED EXCEPTIONS`, stating in the same
   paragraph exactly which positions carry a caveat (1, 2) and which do
   not (3, 4), and that the two sub-questions stay open, not ratified.
3. Position 1: added the ratified marker and Bill's caveat verbatim —
   provisional, revisits when the care-model and legal review land.
4. Position 2: replaced the flat rule with the three-way split (bare
   presence, identity-resolution-refused, enrolled-member-existing-
   scopes), stated the presence-versus-naming line explicitly, and
   flagged that line itself as pending legal and care-model review, in
   the same words used for position 1's caveat.
5. Position 3: kept the process-and-discard position and added the
   at-inference limit in the same breath, as instructed. Grounded it in
   an existing, already-ratified precedent rather than inventing new
   language: `REQ_CRYPTO_P2_PARTITION_SEALED`'s own CONSTRAINT ("the
   model seeing plaintext is not the same as the server being able to
   derive it," verified directly at `:82` of that file before citing it)
   states the identical shape for a fact value; position 3 restates it
   for a frame.
6. Position 4: marked ratified, kept its existing precedent citations
   (`REQ_CONFIDENCE_DISCIPLINE`, `server/voice_orch.py:1405-1471`,
   `memory_engine/trust.py:27-34`) unchanged from DISPATCH_39 — nothing
   about position 4 needed rewriting, only marking ratified.
7. Sub-questions: kept both, not ratified. Folded in Bill's concrete
   framing for the first ("no observation in my bedroom") without
   changing its substance.
8. Cross-reference: named the scope doc's Open Questions item by
   subject ("Observation-and-perception custody"), not by number.
   Followed a precedent the scope doc's own DISPATCH 42 had just set for
   exactly this reason: its Open Questions list had already been
   renumbered twice in one day by the time this dispatch started, and a
   bare numeric cross-reference goes stale the same way DISPATCH 42
   found and fixed for Section 6's own cross-reference into that list.
9. Scope doc: updated Section 10's own framing sentence (the custody
   positions "are themselves also ratified as of 2026-07-27... with
   named exceptions" rather than "remain not yet ratified") and the
   position-1 paragraph's cross-reference (dropped the now-stale
   "POSITIONS AWAITING RATIFICATION" section-name quote and the future-
   conditional "when those positions ratify" framing, since they now
   have).
10. Removed Open Questions item 1 (observation-and-perception custody),
    renumbered items 2-5 to 1-4, added a dated `FURTHER UPDATE 2026-07-27
    (DISPATCH 43)` paragraph summarizing the ratification and its named
    exceptions, updated the count to "Four items remain." Did not restate
    the two sub-questions as their own list item — REQ_PARTITION_CUSTODY
    is now their canonical record, and duplicating them here would be the
    same two-places-say-the-same-thing problem DISPATCH_41 already
    avoided by folding the old paragraph into position 1.
11. Appended a matching dated note to the top-of-file `Reconciled-Against`
    changelog line, the same append-only convention every prior dispatch
    touching this document has used.

## WHAT WAS FOUND

Nothing contradicted the ask. One thing worth naming: position 2's
amendment is substantive, not editorial — the original flat rule ("never
stored without enrollment") would have refused bare-presence household
events outright; the ratified three-way split now permits them
unidentified. This is exactly what the dispatch asked for, stated here so
the size of the change is visible, not just its mechanics.

## VERIFIED

- **Watched, direct read:** both documents' current, live state,
  re-checked via `git status`/fresh reads before each edit — the scope
  doc in particular had moved since this session's own DISPATCH_41,
  confirmed by direct comparison before touching it, not assumed
  unchanged.
- **Watched, direct grep + read:**
  `REQ_CRYPTO_P2_PARTITION_SEALED__stage4-phase2__v20260719_0840.md:82`
  opened and confirmed to contain the exact plaintext-at-inference
  sentence cited in position 3, before citing it.
- **Watched:** `git status` immediately before commit, confirming
  exactly two files changed: the REQ and the scope doc. No concurrent
  session's uncommitted content present at commit time.
- **Reasoned about, not independently evaluated:** whether the
  ratified positions themselves are the right call — that is Bill's
  decision, taken as given per this dispatch's instruction. This
  session's own work was landing the ratification accurately, with its
  stated caveats intact, cross-referenced, and dated.

## HASH

See commit — this dispatch doc and both document edits ship together.

## OPEN

- The two sub-questions (standing-policy-to-collection,
  no-author classification) remain open, unratified, recorded only in
  REQ_PARTITION_CUSTODY now.
- Positions 1 and 2 are explicitly provisional, pending legal and
  care-model review named in the ratification itself — not a gap this
  dispatch introduced, the caveat Bill stated.
- **Confirmed: the scope doc's Open Questions count dropped by one**,
  from five to four, by removing the observation-and-perception custody
  item now that REQ_PARTITION_CUSTODY carries its ratified (and
  provisional-caveated) content in full.
- `docs/INDEX.md` was not checked or touched this dispatch — not
  mentioned in this dispatch's own instructions, and, matching the
  caution of DISPATCH_39/41/30 in this same session, left alone in case
  another session holds it.
