# DISPATCH_BACKLOG
Status: BUILT
Reconciled-Against: main 33049a4, 2026-07-17

**TYPE:** ANALYSIS

**REQ:** NONE. This dispatch reconciles four existing tracking documents
into one ordered queue and touches no code. There is nothing to build a
REQ against.

## THE ASK

Bill's words, verbatim:

> "TASK 3 — BUILD THE BACKLOG. One file, one order, no new analysis.
>
> The work is spread across four registers with four numbering schemes:
>   docs/deliverables/HIP_DefectRegister__v20260715_1930.md (D/I/H)
>   docs/deliverables/HIP_HarnessPlan__v20260715_1600.md (8 phases)
>   docs/deliverables/HIP_SIA_PhaseB__risk-memo__v20260716_1624.md (6 items + 0)
>   tech debt (TD-101b, TD-123..TD-127)
>
> Nothing reconciles them, so every session picks priority from whatever
> failed most recently. That is why the plan has not moved since 07-15.
>
> Build docs/BACKLOG.md. Every open item from all four, in ONE ordered list.
> Per item: ID, one line, which of three goals it serves, blocked-by, and
> whether it needs a Bill decision.
>
> The three goals, in this order:
>   1. DEMO THAT IS TRUE — 2 of 3 scripts work. Script 1 needs the frontier
>      tier. The voice acceptance test (9 steps, REQ_VOICE_DEMO) has never
>      been run end to end.
>   2. PRODUCT THAT WORKS — D-01 fail-open is untouched. D-02: 110
>      exemplars, all first-person, and the market is people asking about
>      someone else. Calibration never measured.
>   3. HARNESS THAT CATCHES — 1 of 8 phases.
>
> Rules for the list:
>   - Anything already fixed comes off. Do not carry closed items.
>   - Anything that needs Bill and only Bill goes in its own short section
>     at the top. I know of: I-10 options, SIA Phase B cutover, Spanish
>     support, frontier tier build-or-defer. Find the rest.
>   - Say which items are dead. Phases 2/4/6/7 have not been touched in two
>     days and nobody decided whether they are deferred or abandoned. Ask,
>     do not assume.
>   - Order by what unblocks what, not by severity.
>
> Then add to CLAUDE.md: docs/BACKLOG.md is the single source of order. Work
> top-down. If something jumps the queue, say so and why, in the dispatch
> doc.
>
> No new work. Reconcile what exists. Report what you find that has no
> owner."

## WHAT WAS DONE

1. Read `docs/INDEX.md` (mandatory first read) to confirm current status of
   every doc touched below.
2. Read all four source registers in full: `HIP_DefectRegister__v20260715_1930.md`,
   `HIP_HarnessPlan__v20260715_1600.md`, `HIP_SIA_PhaseB__risk-memo__v20260716_1624.md`,
   `techdebt/DEBT_REGISTER__v20260712_2300.md`.
3. Read the two requirements docs that govern the biggest open threads
   (`REQ_VOICE_DEMO`, `REQ_SIA_PHASEB`) to check whether either had already
   resolved a question this dispatch was about to ask Bill.
4. Read `docs/demo_prep/HIP_DemoScript01_BoundaryAndConsent__prep__v20260715_1000.md`
   to confirm the shape and size of the frontier-tier gap named in Bill's
   goal 1, and `HIP_DemoScript02_SpeakerIsolation__prep__v20260715_1000.md`
   to rule out a TD-127 conflict with Script 2 (there isn't one — Script 2
   as scripted runs text-path, no voiceprint involved).
5. Grepped for "frontier" across `docs/` to confirm no other doc already
   answers the build-or-defer question.
6. Cross-checked `git log --oneline -5` against the newest commit cited by
   any of the four registers (`33049a4`) to confirm no commit has landed
   since the registers were last written that would change any status.
7. Built one ID-to-status table across all four registers by hand, marked
   every FIXED/RESOLVED/side-effect-closed item for removal, and ordered
   the survivors by dependency rather than severity.
8. Wrote `docs/BACKLOG.md` and this dispatch doc together, per CLAUDE.md
   item 9.
9. Appended the CLAUDE.md pointer Bill asked for (below).

## WHAT WAS FOUND

- **47 open items** survive across the four sources after removing closed
  ones. Full detail lives in `docs/BACKLOG.md`; the highlights below are
  what needed judgment calls, not just transcription.
- **I-06 and risk-memo item 0b are the same artifact under two names.**
  `HIP_HarnessPlan__v20260715_1600.md:100-113` (the amendment note under
  §3.3) already states this explicitly — both check "reply names a
  registered member while nothing is admitted about them," one offline
  (gates a push), one runtime (gates a reply). Listed once in the backlog
  (item #2), not twice.
- **I-10 and H-06 are the same design call**, not two open items —
  `HIP_DefectRegister__v20260715_1930.md:82,95` describe the identical
  nondeterministic-detection-step flake behind the G1 hard-zero gate.
  Folded into one Bill-decision entry (BILL-4).
- **Risk-memo items 1-6 are currently ungoverned.** `REQ_SIA_PHASEB__reconcile-plans-and-file-requirement__v20260716_1736.md:218-224`
  states this directly: the REQ authorizes only D-03/D-18 and G0/item 0b,
  not "the rest of the risk memo's §9 (items 1-6, the SIA/Gate-B
  adjudication work)." Per CLAUDE.md item 8, none of items 1-6 (backlog
  #39-44) may proceed as code changes without a REQ doc naming them — this
  is a gate, not just a sequencing note, and the backlog says so per item.
- **Bill-decision items beyond the four named in the ask:** found TD-110
  (cross-member write authority, "decision required" on file since
  2026-07-08, still undecided) and the Phase 2/4/6/7 deferred-vs-abandoned
  question Bill explicitly named. Did not find any other item on file
  phrased as "awaiting Bill" beyond these six (BILL-1 through BILL-6).
- **One stale-but-not-dead item found by cross-reference, not new
  analysis:** D-05's removed confirm/decline invitation
  (`HIP_DefectRegister__v20260715_1930.md:48`, the D-05 row) was pulled
  specifically because D-03 wasn't fixed yet at the time. D-03 fixed later
  the same day (2026-07-16 1806, per `REQ_D03_D18`). Nobody has revisited
  putting the invitation back. Not urgent, not a Bill decision, folded into
  backlog item #2 rather than given a standalone line — flagged here as
  the kind of drift this reconciliation exists to catch.
- **TD-102 is likely stale but unconfirmed.** It was flagged 2026-07-05
  against a truth-layer delivery report; nothing since references it.
  Recommended a quick check-and-close in the backlog (item #32) rather than
  asserting it's dead outright — that would be new analysis, which the ask
  explicitly excluded ("no new work").
- **Doc-defect X-05 duplicates HarnessPlan Phase 2 item 2.3** exactly (the
  oracle-fixture-verify-at-import item). Listed once (backlog item #11),
  cross-referenced, not counted twice against the "47 open items" tally in
  spirit even though it appears as one line.
- **No commit since any of the four registers was written changes their
  status** — `git log --oneline -5` shows `33049a4` as HEAD, matching every
  register's own "Reconciled-Against" line or later. Confirms nothing here
  is already-stale-by-a-commit.

## VERIFIED

- **Watched run:** `git log --oneline -5` (confirms no commit postdates the
  four registers); `grep -rln "frontier tier"` and `grep -n "speaker\|voiceprint\|Resemblyzer"` across `docs/demo_prep/` (confirms Script 2 has no
  TD-127 conflict, and that no other doc pre-answers BILL-1).
- **Reasoned about:** every open-item status, dependency, and goal
  assignment in `docs/BACKLOG.md` — read from the four registers' own text,
  not independently re-tested. This dispatch did not re-run the harness,
  re-verify any live turn, or re-measure anything the source registers
  already measured. Where a register's own claim was itself flagged
  uncertain (I-10's rate, TD-125's recovery rate, TD-102's staleness), the
  backlog carries that uncertainty forward rather than resolving it — this
  dispatch is a reconciliation, not a re-verification pass.

## HASH

NONE. Doc-only: `docs/BACKLOG.md` (new), this dispatch doc (new),
`docs/INDEX.md` (registered), `CLAUDE.md` (one line added per Bill's
instruction — see OPEN).

## OPEN

- **CLAUDE.md line added:** "docs/BACKLOG.md is the single source of order.
  Work top-down. If something jumps the queue, say so and why, in the
  dispatch doc." Filed under the Workflow section, adjacent to the existing
  Plan of Record pointer.
- **BILL-1 through BILL-6 are unresolved by design** — this dispatch's job
  was to surface them accurately, not decide them. Nothing in
  `docs/BACKLOG.md` proceeds past its first blocked-by-Bill item until one
  of those six lands.
- **This reconciliation itself will go stale the next time any one of the
  four source registers gets a new version.** Nothing currently watches for
  that. Whoever next edits `HIP_DefectRegister`, `HIP_HarnessPlan`, the
  risk memo, or the tech-debt register should update `docs/BACKLOG.md` in
  the same session, or file a fresh dispatch that supersedes this one — the
  four-numbering-scheme drift this dispatch exists to fix will otherwise
  just reopen on the next status change.
- **TD-102 and the D-05 invitation restore are flagged, not resolved** — see
  WHAT WAS FOUND. Left as backlog line items rather than acted on, per "no
  new work."
