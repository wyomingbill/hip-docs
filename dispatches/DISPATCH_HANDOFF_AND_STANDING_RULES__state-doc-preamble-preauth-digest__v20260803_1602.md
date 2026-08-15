# DISPATCH_HANDOFF_AND_STANDING_RULES
Status: BUILT (docs only; no graph, no harness, no code)
Reconciled-Against: 2026-08-03 (D-137; parent `5a2fbe9` at dispatch time)

**TYPE:** GOVERNANCE / STATE DOCUMENT + FRAMEWORK RULES + DELIVERABLE

**REQ:** NONE — documentation and CLAUDE.md session-conduct rules on Bill's direct
instruction. No code, no build; item 8's gate does not arise.

## SEGMENT 1 — the handoff document

`docs/HIP_HANDOFF.md`, created. A STATE document, not a dispatch log, covering the roadmap
lane D-70 → D-136, with a **CURRENT STATE** block at the top per the D-135 rule it now arms.
Carries: the ceiling REQ per-requirement **from §16 itself** (MET: R1/R12/R18/R29/R30;
**R10 the one NOT MET**, with its four `create_fact_node` checks broken out — origin ✅ and
registry ✅ enforced at D-97, representation ❌ and permit ❌, so **A10 flips when A2 and A8
build**, not on any remaining A10 wiring; R2 built at D-130 and reported-not-ruled); the
three-lane structure and why another concurrent BUILD lane is unsafe until TD-148's lock
exists (both failure directions already observed, plus the contended surfaces enumerated);
the standing baseline (**13–15/17 pin, 15/17 the CEILING because TD-145/TD-146 make two rows
permanently red, 16/17 a STOP**, TD-129's ≥2GB guard, TD-147's deliberately loud L6 red);
the process rules **each with the incident that produced it**; open items **grouped by
blocker** (12 build / 2 fixture / 3 outside person / 4 ruling); and the next dispatches
ordered by unlock value.

Hashes cited were verified with `git log --diff-filter=A`, not recalled — `98dfb7a` (ceiling
REQ filed), `b07ab10`, `829464f`, `872ad0c`, `f840161`.

## SEGMENT 2 — the STANDARD PREAMBLE, defined

New CLAUDE.md section `## The STANDARD PREAMBLE (MANDATORY)`, placed immediately before the
reporting section. Five numbered clauses: machine gate before any action (mismatch is a STOP);
tree-not-clean means report whose edits and commit AROUND them with explicit pathspecs plus
the surgical INDEX method spelled out; repo `.env.dev` only, never `~/.env.dev` (which pins
7689 with `override=True` and silently redirects a run into another lane's graph); lock read
FIRST then noclobber, report the holder, release after push; report per the routing rule.
A dispatch saying STANDARD PREAMBLE invokes all of it.

## SEGMENT 3 — pre-authorized ruling classes

New subsection recording Bill's 2026-08-03 pre-authorization: file any TD whose subject is
test or tool infrastructure (**filing pre-authorized, FIXING still needs a REQ**); correct any
document whose stated status contradicts its own authoritative section (**annotate, never
silently patch**); correct its own prior report when later evidence contradicts it; re-run a
check whose failure it has traced to invocation error (**reporting both attempts**).

And the closed NOT-list, with the sentence that keeps it closed — *"this list does not grow
by inference, analogy, or urgency"*: ruling any REQ MET, re-tiering any acceptance row,
changing any baseline, destructive writes, anything touching the frozen demo.

The QUEUED-SEGMENT convention and the six-line STATUS query were **already landed at D-135**
and were VERIFIED present rather than duplicated (all six labels, all three first-line
strings, exactly once each).

## SEGMENT 4 — reporting route by size

**Already landed at D-136** (`5a2fbe9`). Verified as values rather than re-added: SHORT →
terminal; LONG (any build, any harness run, any per-row evidence) → the dispatch doc with the
terminal getting only the status first-line, the file path, and the commit hash; and the
forbidden route with its reason recorded — `open -e` and TextEdit copy return blank, dragging
works, as the D-63 axes document and the REQ drafts did. Re-adding it would have produced a
duplicate rule that could later disagree with itself.

## SEGMENT 5 — the weekly design digest

`HIP_DesignDigest__weekly__v20260803_1602.md`, cumulative (newest week on top, all prior
weeks retained byte-for-byte — verified), `LATEST_HIP_DesignDigest.md` repointed. The
2026-08-03 section covers the four required subjects: the guard that protected only subjects
the requester could already see (**protection scaled with visibility — backwards, since the
boundary matters most where the requester cannot see**) and the resolution-is-not-disclosure
split that fixed it, including the named residual that subject KNOWNNESS is now observable
while fact-level indistinguishability holds; the model-cooperation finding, its **wrong first
headline**, and what four dispatches cost to establish a width whose decisive fact was that
the scenario that mattered had **zero of thirty-one rows**; classification is not wiring —
an orphaned disclosure oracle referenced by no runner beside a wired sibling, and sixteen
honestly-UNWRITABLE acceptance rows; and the velocity instruments, including the one that
nearly failed (a baseline tool that rewrote its own accepted justifications twice in two
days, both times caught only by a human reading a diff).

**Document Governance Rule satisfied in this same commit:** MANIFEST header updated
(Last-updated + Updated-by, prior attribution preserved), Section B's CURRENT row repointed
to v20260803_1602 with the prior CURRENT demoted to SUPERSEDED carrying its
content-retained-in-successor note. **Section C checked: NO WP section maps to the design
digest, so no row is marked NEEDS-UPDATE — checked, not assumed.**

## FINDINGS

1. **The lock was HELD by another session and was not taken.** `.hip-lock` read first:
   `session=claude-code-banking pid=60474 purpose='Index Bank 2 — file six findings on the
   register' started=2026-08-03T21:55:34Z`. Per TD-148's discipline the noclobber take was
   not attempted against a live holder and the holder was NOT overwritten. This dispatch ran
   entirely in its own worktree (no write to the shared checkout), touched no file that lane
   is working (the tech-debt register), and rebased onto origin before pushing.
2. **The dispatch header says "four segments" and the body defines five.** All five were
   executed; recorded so the count discrepancy is not read later as a dropped segment.
3. **Segments 3 and 4 were partly or wholly already satisfied** (D-135's STATUS query and
   queued convention; D-136's routing rule). Verified rather than duplicated.
4. **D-135's PRECONDITION is discharged.** The live-handoff rule was inert pending a document
   that did not exist; that document is created here, so the bullet is replaced with an
   ARMED note in the same commit. The rule now stands unqualified.

## VERIFIED AS VALUES

- CLAUDE.md: 58 insertions / 3 deletions; every new anchor string present exactly once
  (wrap-tolerant, whitespace-collapsed scan — the single-line-grep false-zero hazard);
  PRECONDITION count 0, ARMED count 1.
- Digest: all four week headings present, prior content retained (18,492 → 26,091 bytes).
- MANIFEST: exactly one CURRENT digest row pointing at the new file; the prior CURRENT
  demoted; 4 insertions / 3 deletions.

## PROCESS NOTES

- Own worktree `~/hip-roadmap-d137` from `origin/roadmap`; temp branch
  `d137/handoff-and-rules` pushed as `d137/handoff-and-rules:roadmap`; worktree and branch
  removed after the push.
- Docs only: no graph, no harness, no code — Lane A owns both and is mid-build on R2.
- The shared checkout's foreign WIP (the demo-cutover lane's four dispatch docs and four
  INDEX rows) was never touched: this dispatch's INDEX edit was made in the worktree against
  a clean HEAD copy, so there was nothing of theirs to stage around.

## OPEN

- TD-148's lock REQ remains the gating item for a fourth lane; the holder-collision this
  dispatch navigated is exactly its subject.
- Nothing ruled; no REQ marked MET.
