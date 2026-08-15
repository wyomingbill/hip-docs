# DISPATCH_42
Status: BUILT
Reconciled-Against: see HASH below (same commit as this doc)

**TYPE:** BUILD (docs only, upgrades a ratified interim posture to final and
reconciles a changelog-vs-body gap; no code, no REQ acceptance test)

**REQ:** none named. This dispatch edits
`docs/deliverables/HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md`,
a diligence deliverable, not a REQ doc. No build starts against it, so
Requirements Discipline item 8's gate does not apply the way it does to a
code-changing dispatch.

## THE ASK

> TASK 1: reconcile the changelog-vs-body discrepancy on Open Question 1.
> The doc's top-of-file changelog claims a prior dispatch reclosed the
> multi-tenancy posture, while the Open Questions body still lists it
> open. Read both, determine which is correct against what Section 6
> actually now contains, and make them agree. Same gap-shape DISPATCH 38a
> fixed for items 7 and 8. Report which was wrong.
>
> TASK 2: upgrade Section 6 from interim to final, folding in the
> citation-verified refinements from DISPATCH 40 Phase B: split Case 3
> into 3A (fractional, operator trusted, MIG-backed vGPU on RTX PRO 6000
> Blackwell Server Edition, profiles 1g.24gb/2g.48gb/4g.96gb) and 3B
> (fractional, operator excluded, not available since NVIDIA states MIG
> and vGPU are unsupported in CC mode); state the posture as structurally
> final, a hardware fact not a product-timing bet; replace "disables the
> interconnect" wording with the specific P2P/NCCL/NVLink limits; add
> Case 1.5 (shared base model plus per-tenant LoRA adapters, productized
> in NIM and vLLM, customization not custody); add the USENIX Security
> 2026 "Behind Bars" MIG side-channel finding and use it to state HIP's
> own three-way separation of resource isolation, tenant isolation, and
> cryptographic confidentiality; attach NVIDIA's own CC threat-model
> exclusions verbatim to Case 2. Keep the two-axis spine, cases as
> illustrations. Every vendor claim cited inline. Voice: flat
> declarative, fact then reason, no em dashes, no rule-of-three. Mark
> Section 6 final with today's date. Remove Open Question 1. Update the
> count. Commit, push, report the hash and the remaining Open Questions.

## WHAT WAS DONE

1. Verified environment before touching anything: `bill-ai` /
   `[REDACTED-MACHINE-NAME]`, toplevel `[REDACTED-USER-PATH]/hip-roadmap`,
   branch `roadmap`, HEAD at `fdd9a42` (this session's own prior
   DISPATCH_40 commit). `git status --short` was clean. No concurrent
   session touched this file at any point during this dispatch, unlike
   DISPATCH 40/41/38a's shared-tree collisions earlier the same day.
2. **TASK 1.** Read the top-of-file changelog (line 4) and the full "Open
   questions for Bill" body fresh. The changelog claims DISPATCH 40
   reclosed item 1 (multi-tenancy platform posture). The body, as of
   `fdd9a42`, does not list a multi-tenancy item at all: the numbered
   list runs Observation-and-perception custody, the four-tier hierarchy,
   the training-data record, federated learning, and edge-node
   concurrency, five items, none of them multi-tenancy. Grepped the whole
   document for "multi-tenancy platform posture," "REOPENED," and "Open
   Question 1" to confirm no stray still-open reference survives anywhere
   outside Section 6's own single cross-reference at old line 112. Found:
   the two already agreed. No fix was needed to make them agree, because
   they already did.
3. Traced why DISPATCH 41's own dispatch doc (committed in `b9ed199`,
   read before starting this dispatch) reported the opposite: its own
   "WHAT WAS FOUND" section states the body still showed item 1 open, as
   read at the time DISPATCH 41 checked. DISPATCH 41 ran concurrently
   with DISPATCH 40 in the same shared working tree that day; DISPATCH 40's
   own closing edit to the Open Questions body had not yet landed at the
   moment DISPATCH 41 read the file, but had landed by the time DISPATCH 41
   committed (`b9ed199`, which bundled both sessions' completed edits,
   per DISPATCH_40's own dispatch doc). DISPATCH 41 correctly reported
   what was true when it looked; it was not true of what shipped.
4. **TASK 1 verdict:** the changelog was correct throughout. The
   "still-open" observation was accurate only for an intermediate,
   uncommitted state during concurrent same-file editing, never for a
   committed version of this document. Recorded this finding directly in
   the Open Questions section itself (a new dated paragraph) rather than
   only in this dispatch doc, since a future reader of the deliverable
   should not have to find this dispatch doc to learn the gap was already
   closed.
5. **TASK 2.** Rewrote the "Allocation and economics" subsection of
   Section 6 in full: kept the two-axis framing (axis A, what is shared;
   axis B, who must be unable to see it) as the spine; kept Case 1 and
   Case 2 substantively as DISPATCH 40 left them, rewritten sentence by
   sentence to remove em dashes and match flat declarative voice; inserted
   Case 1.5 (shared base model, per-tenant LoRA adapters, citing vLLM's
   LoRA features page and NVIDIA NIM's PEFT page, explicit that
   customization is not custody); split Case 3 into 3A (citing NVIDIA's
   AI Enterprise vGPU MIG-backed-vGPU page and the Tesla MIG User Guide's
   supported-profiles page) and 3B (citing the confidential-computing
   enterprise reference architecture for self-hosted Kubernetes); replaced
   the old "disables the interconnect" line with the specific P2P/NCCL/
   NVLink limits, citing the MIG User Guide's deployment-considerations
   page; inserted a paragraph between 3A and 3B naming the USENIX Security
   2026 "Behind Bars" paper and using it to state HIP's own three-way
   separation of resource isolation, tenant isolation, and cryptographic
   confidentiality, cross-referenced against AW-04's own accepted limit
   below; attached NVIDIA's own confidential-computing threat-model
   exclusions to Case 2, close to verbatim, sourced from the trust-and-
   threat-model documentation Phase B already quoted; rewrote the closing
   posture paragraph to state the posture as final and structural, not
   interim, with the reasoning restated as a hardware fact that does not
   expire on a driver release.
6. Marked the Section 6 header `(allocation posture ratified final
   2026-07-27, DISPATCH 42)`, the same convention DISPATCH 41 used for
   Section 10's header.
7. Updated the "Open questions for Bill" section: added a dated
   `FURTHER UPDATE 2026-07-27 (DISPATCH 42)` paragraph recording the
   final-not-interim upgrade, the Task 1 finding (no fix needed, both
   already agreed), and the retirement of the stale numeric
   "Open Question 1" cross-reference, in the same spirit as DISPATCH 38a's
   distinction between an item's historical number and its list position
   (this list has been renumbered twice since "1" meant multi-tenancy).
   The numbered list itself was not touched, since the item it would have
   removed was already absent; item count stays five, stated as
   unchanged by this dispatch rather than silently re-asserted.
8. Appended a matching dated note to the top-of-file `Reconciled-Against`
   changelog line, the same append-only convention every prior dispatch
   touching this document has used.
9. Checked the new prose against the style constraint directly: grepped
   every span containing this dispatch's own added text (the header
   addition, the Section 6 rewrite, the Open Questions addition)
   separately for the em-dash character, all three returned zero. Read
   back for decorative three-part constructions; the one explicit triad
   this dispatch introduces, "resource isolation, tenant isolation, and
   cryptographic confidentiality," is the substantive three-way
   separation the ask itself named, not a rhetorical flourish, matching
   the standard DISPATCH 41 applied to its own one retained triad.

## WHAT WAS FOUND

Documented under TASK 1 above: the changelog-vs-body discrepancy DISPATCH
41 flagged was real only in an intermediate, uncommitted state during
concurrent same-file editing earlier the same day, and had already
resolved itself by the time `b9ed199` was committed. Nothing in the
committed document needed correcting to make the two agree; they already
did. This dispatch's actual Task 1 work was investigation and a clarifying
note, not a content fix.

## VERIFIED

- **Watched, direct read:** full current state of Section 6 and "Open
  questions for Bill," read fresh immediately before each edit. No
  concurrent session touched this file during this dispatch, confirmed by
  `git status --short` showing only this dispatch's own change at every
  checkpoint.
- **Watched:** grepped the full document for "multi-tenancy platform
  posture," "REOPENED," and "Open Question 1" before concluding Task 1,
  not just the numbered list itself.
- **Watched:** grepped this dispatch's three added spans (header,
  Section 6, Open Questions) individually for the em-dash character,
  isolating them from the surrounding text's own pre-existing em dashes
  (DISPATCH 38/38a/40's prose, and the deliberate "Item 7 —" / "Item 8 —"
  historical-identifier convention, both left untouched and out of
  scope).
- **Reasoned about, not independently re-derived:** the nine underlying
  vendor claims (MIG-backed vGPU productization, profile sizes, CC's
  exclusion of MIG/vGPU, P2P/NCCL/NVLink limits, LoRA concurrency in NIM
  and vLLM, the Behind Bars paper, NVIDIA's own CC threat-model scope)
  were verified in DISPATCH 40 Phase B, reported to Bill, not re-verified
  here; this dispatch's own work was folding already-confirmed facts into
  final prose with inline citation, not re-checking sources.

## HASH

See commit. This dispatch doc and the architecture-deliverable edit ship
together.

## OPEN

- `docs/INDEX.md` and `docs/deliverables/MANIFEST.md` updated in this
  same commit per the Document Governance Rule, describing this
  dispatch's own delta on top of the already-registered DISPATCH
  38a/40/41 cumulative state.
- No new Open Questions were added or removed by this dispatch beyond
  what DISPATCH 40 already closed; the count stays at five.
