# DISPATCH_39
Status: BUILT
Reconciled-Against: see HASH below (same commit as this doc)

**TYPE:** BUILD (docs only — lands stated positions into the canonical
REQ; performs no ratification and changes no code)

**REQ:** `docs/requirements/REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md`
(edited in place, per this REQ's own established pattern of dated,
in-place sections — status stays NOT MET, unchanged by this dispatch)

## THE ASK

> Bill's stated positions on observation-and-perception custody, carried
> since 2026-07-21, were never written into the canonical REQ. Land them
> now as POSITIONS AWAITING RATIFICATION, clearly marked as such, in
> docs/requirements/REQ_PARTITION_CUSTODY (current version, follow the
> LATEST symlink):
>
> 1. A system-observed fact whose subject is a caregiver seals to that
>    caregiver and the recipient only.
> 2. Non-members captured by sensors are never stored without enrollment.
> 3. Perception is process-and-discard: frames are never retained, only
>    derived sealed facts. Operator-blind-at-rest survives; the
>    at-inference limit is restated for continuous video.
> 4. Observation may CORROBORATE a fact but may never CONFIRM one, the
>    same principle as speaker ID and repetition-never-raises-status: a
>    model with an error rate cannot mint CONFIRMED.
>
> Still genuinely open within the same item, list as sub-questions:
> whether recipient standing policy extends from disclosure to
> collection, surviving incapacity via the recognized authority; and how
> a system-observed fact classifies when no author exists for the
> mandatory subject-is-caregiver rule to key on.
>
> Date the section, cite the scope doc's Section 10 and Open Question 3
> as cross-references. Do not mark anything ratified; these are
> positions on record.
>
> Commit, push, report the hash.

## WHAT WAS DONE

1. Confirmed `docs/requirements/LATEST_REQ_PARTITION_CUSTODY.md` still
   resolves to `REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md`
   (the same file this session's DISPATCH_30 edited two dispatches ago;
   `git log` confirms no other session touched it since).
2. Located the scope doc: `docs/deliverables/HIP_ArchitectureForDiligence__
   scope-borders-testing-and-target__v20260727_1606.md`. Read Section 10
   ("Long vision," the observation-and-perception paragraph) and "Open
   questions for Bill" item 3 in full, verbatim, before writing anything.
3. Added a new, clearly-labeled section — "Observation-and-perception
   custody — POSITIONS AWAITING RATIFICATION (dated 2026-07-27, DISPATCH
   39)" — positioned after the existing "Custody consent, revocation, and
   abuse resistance" section and before "DECISIONS FOR BILL," so it reads
   as adjacent future-scoped material without being folded into the
   section whose own header says "the REQ is MET when these are
   answered." Opens with **NOT RATIFIED** in bold, states plainly that
   nothing in it changes this REQ's MET criteria or acceptance table, and
   that it should not be built against.
4. Cited the scope doc by exact section/item name and quoted its own
   framing sentence back ("Ratifying these positions means writing them
   in; until then they are stated positions awaiting that step, not
   settled requirement text") so a reader can verify the cross-reference
   independently.
5. Landed all 4 positions and both sub-questions in Bill's own words from
   this dispatch, not paraphrased from the scope doc — see WHAT WAS FOUND
   for the one place they genuinely differ.
6. For position 4's "same principle as speaker ID and repetition-never-
   raises-status," did not leave that as a bare assertion — traced and
   cited the actual ratified precedent: `REQ_CONFIDENCE_DISCIPLINE__
   truth-track__v20260721_0945.md` demotes voiceprint match from gate to
   hint (`server/voice_orch.py:1405-1471`) and states repetition alone
   never raises trust level (`memory_engine/trust.py:27-34`'s ordinal
   ladder). Both line ranges spot-checked directly against the live
   source files, not assumed from the REQ's own citation.
7. `Status: NOT MET` header confirmed unchanged before and after the
   edit — this dispatch does not ratify, and does not touch the REQ's
   existing ratified content (D1-D3, the four-level write rule, etc.).

## WHAT WAS FOUND

The scope doc's own Open Question 3 frames "whether observation may
raise a fact's trust rung" as one of TWO still-open items (alongside the
standing-policy-collection question) — it does not resolve it, and does
not separately name the no-author-for-mandatory-exclusion question at
all. Bill's dispatch text settles the trust-rung question as position 4
(corroborate yes, confirm never) and names a DIFFERENT second open
question (no-author classification) in its place. This is not a
contradiction to silently reconcile — the scope doc was written by a
different session on 2026-07-27, before this dispatch, and Bill's own
words here are the more precise, final formulation for landing in the
canonical REQ. Noted explicitly in the new section's cross-reference
paragraph, not smoothed over: "position 4 below settles that question...
the second genuinely open item in its place is the no-author
classification question... which the scope doc did not separately name."

## VERIFIED

- **Watched, direct read:** the scope doc's Section 10 and Open Question
  3 paragraphs, in full, before drafting — not summarized from memory or
  from this dispatch's own framing alone.
- **Watched, direct read:** `REQ_PARTITION_CUSTODY`'s current full text
  (215 lines) before inserting, to place the new section correctly
  relative to "Custody consent..." and "DECISIONS FOR BILL," and to
  confirm the `Status:` header's exact current value.
- **Watched, direct grep + read:** `server/voice_orch.py:1405-1471` (the
  speaker-verification gate section) and `memory_engine/trust.py:27-34`
  (the `TRUST_RANK` ordinal dict) — both cited in position 4, both
  opened and confirmed to contain what `REQ_CONFIDENCE_DISCIPLINE`
  already claims of them, not trusted from that REQ's own citation alone.
- **Reasoned about, not independently re-derived:** the substance of
  positions 1-4 and the two sub-questions themselves are Bill's own
  words, taken as given per this dispatch's instruction — this session
  did not evaluate whether they are the RIGHT positions, only landed
  them accurately, dated, and cross-referenced, exactly as asked.
- `git diff` confirms the only file changed is `REQ_PARTITION_CUSTODY`'s
  own markdown text — no code, no other REQ, no `docs/INDEX.md`.

## HASH

See commit — this dispatch doc and the REQ_PARTITION_CUSTODY edit ship
together. `docs/INDEX.md` not touched (not requested this dispatch, and
another session has held it in adjacent recent work this same day —
same caution as the prior two dispatches in this session).

## OPEN

- The two sub-questions landed here (standing-policy disclosure-vs-
  collection, and no-author classification) are unanswered by design —
  this dispatch's job was to record them, not resolve them.
- Ratification itself (turning these 4 positions into REQ text that
  actually governs `write_rule.classify()` or a future perception
  module) is a separate, not-yet-scoped piece of work — no acceptance
  test, no code, no fixture exists for any of this yet.
- `docs/INDEX.md` does not yet register this dispatch doc — whichever
  session next holds that file should add it.
