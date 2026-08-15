# DISPATCH_TD140_RULING
Status: BUILT
Reconciled-Against: 2026-08-02 (D-111; parent 9c7b749 at dispatch time)

**TYPE:** PROCESS (a ruling enacted: requirement amendment + register closure;
one comment-only code edit; no behaviour change anywhere)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2112.md`
— this dispatch CREATES that version, enacting Bill's 2026-08-02 ruling on
TD-140. The ruling is Bill's, quoted verbatim below; nothing here is
self-ruled.

## THE ASK

> RULING, Bill, 2026-08-02, on TD-140: INVALIDATE-ONLY BECOMES THE
> REQUIREMENT. R18's recompute clause is REMOVED, not deferred. Amend R18's
> text so it requires what the system does and can do: when a source fact is
> retracted, its derived children are invalidated.
> RECORD THE REASON, in the requirement itself, not a footnote:
> - D-104 proved the original derivation is a live Groq call, so "recompute
>   from surviving parents" is a SECOND NON-DETERMINISTIC MODEL CALL, not a
>   re-derivation from stored data. There is no stored recipe to re-run.
> - A rule describing an operation the system cannot perform reads as a
>   commitment and is not one.
> - Invalidate-only errs toward FORGETTING MORE than the original clause
>   required, never less. The failure mode is lost inference, not retained
>   inference.
> - Recompute-as-fresh-inference is NOT foreclosed. If it is ever wanted it
>   comes back as its own requirement, through the inference-permit
>   machinery, with the non-determinism handled openly. Say so, so a later
>   reader does not read this as the door closing.
> TD-140 is RESOLVED by this ruling — closed by requirement change, not by a
> build. Mark it so in the register, with that distinction stated.
> R18's remaining gaps were TD-139 (resolved, D-105), TD-140 (resolved
> here), TD-141 (resolved, D-107). Report whether R18 now has any open gap.
> DO NOT RULE R18 MET — report the evidence and let Bill rule.

## WHAT WAS DONE

1. Machine gate passed; cutover lane's WIP present again (three dispatch
   docs + three INDEX rows, uncommitted) — committed AROUND with explicit
   pathspecs + surgical INDEX stage. `.hip-lock` free → taken → released.
2. Every reference to R18's two-branch rule enumerated BEFORE editing:
   the REQ (requirement text :648-654, A18 acceptance row :934, section 16
   ruling), `harness/derivation_cascade.py:7-8` (verbatim docstring quote),
   and nothing else in code (grep); no mutation-target coordinates touch
   derivation_cascade.
3. REQ amended as a NEW VERSION v20260802_2112 (Naming Law — never
   overwrite): R18's operative rule is now invalidate-only with the four
   reasons recorded IN the requirement; A18's row reworded ("invalidates
   every dependent child" — what the passing battery always asserted); a
   new section-16 block records the amendment and deliberately does NOT
   re-rule MET; the 2026-08-01 NOT MET ruling is kept as history, marked
   historical. Header status/version updated. LATEST symlink repointed.
4. `harness/derivation_cascade.py` docstring updated to quote the amended
   rule and point at the new REQ version — comment-only; the
   `cascade_recompute_eligible`/`cascade_recompute_from` breadcrumbs stay
   written-and-unread per the ruling's door-open clause.
5. Register v20260802_2115: TD-140 → RESOLVED with the closed-by-
   requirement-change-not-build distinction stated in the entry itself;
   header note; LATEST_DEBT repointed.
6. Full evidence run (step 4 of the ask) — below.

## WHAT WAS FOUND — R18's open-gap report (step 3; NOT a MET ruling)

**The three named debt gaps:** TD-139 partially closed (D-105 — 4 of 11
fields implemented fail-closed, 4 present under existing names), TD-140
resolved here by requirement change, TD-141 resolved (D-107 — the seed
writes real lineage through the creator; live cascade proof). **No OPEN
debt item now names R18.**

**What remains, reported for Bill — the honest both-ways evidence, also
recorded in the REQ's section 16:**
- *Toward MET:* the amended operative rule is built and live-proven (D-81
  cascade to fixpoint in-transaction; A18 LIVE and passing with its fault
  twin; D-107's live retraction closed the seeded derived child,
  `closed_by='lineage_cascade'`). The lineage gate refuses derived writes
  missing the implemented block; the seed exercises the same gate.
- *Toward caution:* three of R18's eleven minimum-metadata fields
  (`purpose_id`, `retention_deadline`, `policy_version`) are DELIBERATELY
  ABSENT — they cannot be populated honestly until R23's purpose
  vocabulary, R21's retention mechanism, and a real policy version exist;
  a standing test asserts the absence. "Erase it according to its storage
  class" holds only in the weak closed-from-retrieval sense for the same
  reason. The 12 pre-lineage facts carry no block and no ruling exists for
  pre-lineage artifacts on a durable (non-reseeded) graph.
- **Whether R18 is MET with those absences recorded, or stays NOT MET
  until R21/R23 land, is exactly the call left to Bill.**

**Flagged, not silently changed:** TD-139's register STATUS COLUMN still
reads "OPEN -- schema change, needs its own REQ" while its entry text
says PARTIALLY CLOSED (D-105) and this dispatch's ask calls it "resolved,
D-105". The column was left as-is — reconciling it is a one-line register
edit that should carry Bill's word for it (the 3 absent fields are the
reason the column stayed OPEN at D-105).

## VERIFIED

**Watched run (evidence read individually from the logs):**
- Batteries: **297 passed / 1 skipped / 8 xfailed** (identical to D-107's
  counts; the derivation-cascade + lineage batteries also run standalone:
  39 passed / 2 xfailed).
- **AUDIT 8/8 · DISC 1/1 · L7 27/27 · L7V2 27/28** (the 1 skip is
  CT-OUTPUT-GAP, opt-in live-model check — the standing shape) · SCHEMA
  1/1 · VOICE 1/1 · **RATCHET PASS** · COVERAGE-GRID-RATCHET PASS · **0
  scenario FAILs**.
- ABSOLUTE, individually: **OB6 · G0 · PSA1 · CTX-STRIP · LI1 — all
  PASS.**
- **Mutation self-test finds its mutant at `injection_contract.py:664`**,
  both directions (killed with killers, survives without).
- **Memory harness: 15/17, failing exactly {MEM-115, MEM-116}** — inside
  the D-109 pin (13-15/17, failures ⊂ {115,116,117,118}), at the
  structural ceiling D-110 predicted (115 permanent-red per TD-146, 116
  permanent-red per TD-145, live variation only {117,118}). NOT 16/17 —
  the STOP shape did not occur.

**Reasoned about:** that no other code or doc quotes the removed
two-branch rule — from the grep enumeration in step 2, not from reading
every file.

## HASH

Committed this session on `roadmap` (D-111); parent 9c7b749.

## OPEN

- **R18's MET ruling — Bill's, on the section-16 evidence.** The one
  decision this dispatch deliberately does not make.
- TD-139's status-column/entry-text discrepancy (flagged above).
- The breadcrumb fields (`cascade_recompute_eligible`/`_from`): written,
  consumed by nothing, kept per the door-open clause — if
  recompute-as-fresh-inference is ever REQ'd, they are its starting
  inventory; if it never is, a future cleanup ruling could drop them.
- Historical docs quoting the two-branch rule (D-104's dispatch, older
  register versions, the 2026-08-01 ruling text) stay as history.
