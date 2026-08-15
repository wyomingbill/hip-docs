# DISPATCH_BACKLOG_GOVERNANCE
Status: BUILT
Reconciled-Against: main 33049a4, 2026-07-17

**TYPE:** ANALYSIS

**REQ:** NONE. This dispatch tags governance status on an existing backlog
and proposes REQ docs that don't exist yet. It touches no code and writes
no REQ doc itself — writing one without Bill's answer to its question would
repeat the SIA mistake this dispatch exists to flag.

## THE ASK

Bill's words, verbatim:

> "ADDENDUM to Task 3. The backlog must say which items are GOVERNED and
> which are not. That is the point, not a footnote.
>
> Four REQ docs exist. Two carry Bill's verbatim words (REQ_VOICE_DEMO,
> REQ_HARNESS). Two were filed correctly before code (REQ_D03_D18,
> REQ_TD126_REMEDIATION).
>
> Per item in the backlog, one of:
>   - GOVERNED — names its REQ doc
>   - DEFECT — has an ID, no REQ needed, fix and close
>   - UNGOVERNED — needs a REQ before any code. Say so.
>
> The SIA track is the case in point. You searched and found nothing Bill
> said. It came from a chat session's theory, then a Fable review, then
> Bill saying "adopting it." That is an adopted analysis. It shipped code
> twice (c86a414, 3c0cb74) and both carried regressions the ratchet caught
> later. Mark every SIA item UNGOVERNED.
>
> The frontier tier is UNGOVERNED too and it is the top demo item. It needs
> a REQ before anyone writes code.
>
> Then propose, do not build: what REQ docs are missing, and for each, what
> question Bill has to answer to write it. One line each. He will answer
> them."

## WHAT WAS DONE

1. Read the full text of `REQ_HARNESS`, `REQ_atorvastatin-false-ack`, and
   `REQ_D22_D20` (not previously read in full during Task 3) to check each
   REQ's own stated scope boundary, not just its INDEX one-liner.
2. Cross-checked `REQ_HARNESS`'s own text against every HarnessPlan phase
   it might plausibly cover — found it explicitly self-limits: *"This task
   is Phase 1 only. Do not restate the plan; reference it."* Everything
   past Phase 1 is therefore outside REQ_HARNESS's authorization by its own
   words, not by an inference this dispatch made.
3. Cross-checked `REQ_HARNESS`'s own CONSTRAINTS against BILL-4 (the I-10/H-06
   flake decision) — found it explicitly states *"G1 and G4 must gate at
   HARD ZERO — --accept refused for these checks,"* which directly
   contradicts one of I-10's own three on-file options (moving G1 to the
   ratchet). Flagged that specific option as requiring an explicit
   amendment, not a silent one, if chosen.
4. Went through all 47 backlog items plus the 6 BILL-decision items and
   assigned GOVERNED / DEFECT / UNGOVERNED to each, using blast radius and
   provenance (not severity) as the dividing line — see the backlog's own
   GOVERNANCE KEY section for the rule and the reasoning on the closest
   calls (D-01, D-02, TD-101, TD-108, TD-123, TD-110, TD-115/120/122).
5. Rewrote `docs/BACKLOG.md` in place (same file, redeployed — see that
   doc's own exemption from the Naming Law) adding a Gov column to the
   ordered table, a Governance Key section, and re-tagged the BILL-*
   decisions with their own governance status.
6. Built the MISSING REQ DOCS table: one line per proposed REQ, one
   question each, derived directly from what's actually contested or
   undecided in the source registers — not invented.
7. Did NOT write any of the 13 proposed REQ docs. Did NOT change any code.

## WHAT WAS FOUND

- **REQ_HARNESS's own text already draws two of the boundaries Bill asked
  for**, independent of any new reasoning this dispatch did: (1) it scopes
  itself to Phase 1 only, meaning Phases 0(residual)/2/3/4/5/6/7 are
  UNGOVERNED by REQ_HARNESS's own admission, not by this dispatch's
  inference; (2) it names I-10 as *"scoped OUTSIDE this REQ_HARNESS's own
  target... but it shares the same gate"* — REQ_HARNESS itself disclaims
  authority over the fix BILL-4 is stuck on.
- **`REQ_SIA_PHASEB` contains its own admission that undercuts its
  authority claim.** Its own RECONCILE THE PLANS §2 text says building
  G0/item 0b is authorized "via REQ_VOICE_DEMO" — but the same doc's own
  earlier paragraph says that connection is *"this doc's inference, not a
  quote."* An analysis session's inference about its own authorization is
  not the same as Bill's authorization. This is why G0 is tagged UNGOVERNED
  here even though `REQ_SIA_PHASEB` argues otherwise — the argument comes
  from the same lineage under scrutiny.
- **D-01 and D-02 are defect-register entries with pinned file:line root
  causes, which would normally read as DEFECT** under the letter of Bill's
  rule ("has an ID, no REQ needed"). Tagged UNGOVERNED anyway because of
  blast radius: the register's own words are "fixing D-01 collapses D-02,
  D-03, and D-04" — a foundational default-behavior change, not a local
  patch. Flagging this explicitly rather than mechanically applying "has an
  ID → DEFECT," since that mechanical reading is exactly the kind of
  under-scrutinized call that produced c86a414/3c0cb74's regressions.
- **TD-123 has a documented history of five prior fix attempts, each of
  which patched one layer and broke another** (`DEBT_REGISTER` TD-123 row).
  That history, not severity, is why it's tagged UNGOVERNED rather than
  DEFECT — a sixth ad hoc patch without a REQ and an acceptance test
  repeats a pattern already proven to fail five times.
- **TD-108's HEL Phase 2 has a full spec doc under `docs/specs/` but no REQ
  under `docs/requirements/`.** CLAUDE.md's gate (item 8) names the folder
  specifically. A thorough spec is not a substitute for the REQ doc the
  gate requires — flagged as UNGOVERNED despite the spec's quality, not
  because the spec is thin.
- **13 REQ docs proposed, none built.** Each question was pulled from an
  actual documented fork, tension, or open design call already on file
  (e.g. BILL-4's ratchet-vs-hard-zero conflict with REQ_HARNESS's own
  constraint; TD-110's two named forks; the SIA memo's own 85.7%-is-not-
  accuracy argument) — none were invented for this dispatch.
- **One item's classification is genuinely borderline and flagged as
  such rather than silently resolved:** D-10/TD-101b (unauthenticated
  `/api/decrypt`) is tagged DEFECT (single endpoint, add an auth check) but
  its severity (SEC) argues for more caution than a typical DEFECT gets.
  Left as DEFECT per the letter of Bill's rule, noted here so it isn't
  read as an oversight if someone later wants it upgraded to UNGOVERNED.

## VERIFIED

- **Watched run:** none — this is a documentation reconciliation, no code
  executed.
- **Reasoned about:** every governance tag in `docs/BACKLOG.md`, read
  directly from `REQ_HARNESS`, `REQ_atorvastatin-false-ack`, `REQ_D22_D20`,
  `REQ_D03_D18` (read in the prior dispatch), `REQ_SIA_PHASEB`, and
  `REQ_VOICE_DEMO`'s own text — not inferred from their INDEX one-liners.
  Where a tag required a judgment call beyond what the source text states
  outright (D-01, D-02, TD-108, TD-123, TD-101, TD-110, TD-115/120/122),
  the reasoning is stated inline in the backlog's GOVERNANCE KEY section
  and in WHAT WAS FOUND above, so it can be checked and overturned rather
  than taken on faith.

## HASH

NONE. Doc-only: `docs/BACKLOG.md` (rewritten in place), this dispatch doc
(new), `docs/INDEX.md` (registered).

## OPEN

- **13 REQ docs are proposed and none are written.** Per Bill's own
  instruction ("propose, do not build... He will answer them"), the next
  step is his answers, not more analysis.
- **The DEFECT/UNGOVERNED line for D-10/TD-101b, TD-115, TD-120, and
  TD-122 is a judgment call this dispatch made, not something the source
  registers state explicitly.** If Bill's intent for "blast radius" is
  narrower or wider than applied here, several of these could move.
  Flagged rather than silently assumed settled.
- **BILL-4's option (b) (move G1 to the ratchet) directly contradicts a
  written constraint in `REQ_HARNESS` itself.** This dispatch flagged that
  conflict but did not resolve it — resolving it requires Bill choosing an
  option AND, if it's (b), explicitly authorizing an amendment to
  `REQ_HARNESS`'s own CONSTRAINTS section, not just a note in a new doc.
- **This governance tagging will go stale the same way the original
  backlog would have** — the moment any of the 13 proposed REQs gets
  written and answered, or any UNGOVERNED item ships code without one, this
  doc's tags need a fresh pass. Nothing currently watches for that either.
