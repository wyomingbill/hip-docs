# DISPATCH_FRONTIER_TIER_REQ
Status: BUILT
Reconciled-Against: 1bd4500

**TYPE:** PROCESS

**REQ:** `docs/requirements/REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`
— this dispatch's own output IS that REQ; there is no separate parent REQ
because the ask was to draft one, not to build against an existing one.

## THE ASK

> "DISPATCH: REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215
> TYPE: PROCESS (REQ drafting, no code)
> GOAL: 1 — demo that is true
> BACKLOG: #1 (add it — it is not on the list)
>
> Draft docs/requirements/REQ_FRONTIER_TIER__<slug>__v<stamp>.md. Do not
> write code. Mark it NEEDS BILL CONFIRMATION and list every question you
> need answered.
>
> THE FRONTIER TIER is script 1's T04/T05... [full design: T04 zoning/
> variance question, GATE then FRONTIER; payload = D10 (address) + D11
> (zone_district), CONFIRMED, built BY CODE from fact rows, owner/members
> redacted; the beat — without D11 the frontier hedges, with D11 it answers
> definitively; return rung ASSERTED; T05 — HIP summarizes on EDGE and
> offers to EMAIL details, no phone, no second device, long answer never
> read aloud, email need not actually send.
>
> NOTE: D10/D11's attribute is changing to `household` per the schema
> decision. Confirm the payload builder reads fact rows, not attribute
> strings, or this breaks.
>
> D11's VALUE is still TBD... Build against a placeholder and flag it.
>
> Draft the acceptance test from the above. Then list your questions, one
> line each."
>
> "Push, report the hash."

## WHAT WAS DONE

1. Read `docs/demo_prep/HIP_DemoScript01_BoundaryAndConsent__prep__v20260715_1000.md`
   in full (T04/T05 design, BUILD LIST, SEEDS REQUIRED, VERIFY BEFORE
   PRESENTING tables) and `demo_scripts/boundary_and_consent__v20260715_1158.json`
   (confirmed T01-T03 built, T04-T05 explicitly omitted per the file's own
   `description` field).
2. Checked the dispatch's claim that the frontier tier is "not on
   BACKLOG.md" against the actual file — found it already present at row
   #47, in `BILL-1`, and in the MISSING REQ DOCS table. Reported this
   directly in the REQ rather than silently adding a duplicate row.
3. Grepped `harness/control_flow.py` for `frontier` — found a pre-existing,
   differently-shaped, codeword-gated frontier-crossing mechanism
   (`handle_frontier_request`, `HIP_FRONTIER_CODEWORD`, INV-2/INV-3/INV-4/
   INV-5), shipped 2026-07-03/05, predating the Script 1 prep doc
   (2026-07-15). Grepped `docs/specs/CONTROL_FLOW__reconsider-frontier-sm__v20260703_1126.md`
   for zoning/disclosure-pane/payload-builder language — none found,
   confirming the two mechanisms are unrelated in current design.
4. Drafted `docs/requirements/REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`:
   THE REQUIREMENT (verbatim), the BACKLOG correction, THE ACCEPTANCE TEST
   (T04 gate-then-frontier incl. the with/without-D11 beat test; T05
   edge-summary + email disposition incl. "email need not send"), WHAT'S
   ALREADY DONE, WHAT'S KNOWN BROKEN (the prep doc's own 7-item BUILD LIST
   plus 3 carried-forward verification items), CONSTRAINTS, and 11 NEEDS
   BILL CONFIRMATION questions.
5. Mid-task, found `docs/requirements/REQ_D21_D23__canonical-attribute-enum-expansion-and-seed-schema-validation__v20260717_1200.md`
   (filed 15 minutes before this REQ, IN_PROGRESS, uncommitted working
   changes) and read it in full, along with the live diffs of
   `harness/extraction_queue.py`, `harness/injection_contract.py`,
   `scripts/demo_seed.py`, and `eval/oracle/disclosure_oracle.py`. This
   directly bears on the REQ's own NOTE about a `household` migration for
   D10/D11 — see WHAT WAS FOUND.
6. Corrected the REQ draft in five places (the NOTE section, WHAT'S
   ALREADY DONE, CONSTRAINTS, the cross-cutting acceptance-test note, and
   Question 8) rather than leaving a now-inaccurate claim standing.
7. Applied the REQ's own "BACKLOG UPDATE" section as actual edits to
   `docs/BACKLOG.md`: new item **#0** (frontier tier, non-disruptive
   insertion ahead of #1, avoiding a 47-row renumber), `BILL-1` updated to
   reflect the draft REQ now exists, row #47 marked superseded pointing to
   #0, `REQ_SCRIPT01_FRONTIER` removed from the MISSING REQ DOCS table (a
   draft now exists, so it is no longer missing).
8. Registered the REQ in `docs/INDEX.md` (requirements/ section), created
   `docs/requirements/LATEST_REQ_FRONTIER_TIER.md` symlink.

## WHAT WAS FOUND

- The frontier tier's design (`HIP_DemoScript01_BoundaryAndConsent__prep`)
  has nothing built yet except routing — confirmed against the prep doc's
  own BUILD LIST (lines 141-152) and the script JSON's own `description`
  field.
- A second, pre-existing frontier-crossing mechanism exists in
  `harness/control_flow.py` (`handle_frontier_request`, shipped `e35dcd4`/
  `60069f8`, 2026-07-03/05) that the prep doc does not mention and whose
  UX shape (generic codeword escalation) differs from Script 1's
  (visual disclosure-pane, code-built redacted payload). Not reconciled;
  flagged as the single most important open question in the REQ.
- **The REQ's own NOTE — "D10/D11's attribute is changing to `household`
  per the schema decision" — is stale.** `REQ_D21_D23`'s four-part schema
  decision did include this migration (item 3), and it was attempted live
  this session. It **collided with D7**, which already owns the triple
  `(household, household, household)`; `eval/harnesslib/fixture.py`'s
  `verify_seed` asserts exactly one active fact per `(owner, subject,
  attribute)` triple, so three facts under one triple broke immediately on
  reset (D7's expected value read back as D10/D11's instead — this is
  documented as confirmed live in `scripts/demo_seed.py`'s own working
  diff, not something I re-ran myself). D10/D11 are back on their original
  `address`/`zone_district` strings, now on a temporary
  `_ENUM_EXEMPT_LABELS` list alongside D8, pending Bill's decision on how
  to disambiguate multiple household-owned facts sharing one attribute.
  The migration is attempted-and-blocked, not landed and not merely
  future — the REQ is corrected to say this in five places rather than
  carrying the stale framing forward.
- The unrelated part of `REQ_D21_D23` (adding `incident`/
  `medication_status` to `CANONICAL_ATTRIBUTES`, and an enum check on
  `demo_seed.py`'s `_seed_one`) does not touch D10/D11 at all — it is a
  different part of the same REQ, orthogonal to the frontier-tier draft.

## VERIFIED

- **Watched run:** none — this dispatch is PROCESS type, no code changed,
  nothing to run. The `_seed_one`/D7-collision claim above is NOT something
  I ran; it is read directly from `scripts/demo_seed.py`'s own in-progress,
  uncommitted working diff, which documents it as "confirmed live" in its
  own comment. I am reporting what that diff says, not independently
  reproducing it — flagged as reasoned-about, not watched, per this
  template's own discipline.
- **Reasoned about:** the BACKLOG "not on the list" correction (direct file
  read of `docs/BACKLOG.md` at rows #47/BILL-1/MISSING REQ DOCS); the
  control_flow.py frontier-mechanism finding (direct grep + spec read); the
  REQ_D21_D23 staleness correction (direct read of that REQ doc and the
  four modified files' diffs).

## HASH

`3f8e0f9` — REQ, this dispatch, BACKLOG.md edits, and INDEX.md
registration, all in one commit. Pushed to `origin/main`.

## OPEN

- All 11 NEEDS BILL CONFIRMATION questions in the REQ itself — none
  answered, no code authorized.
- The D10/D11 disambiguation question (Question 8, corrected) is now a
  concrete, live-tested blocker, not a hypothetical — it belongs to
  `REQ_D21_D23`'s scope, not this REQ's, but this REQ's payload-builder
  design depends on how it resolves.
- `REQ_D21_D23` itself is IN_PROGRESS and uncommitted as of this dispatch —
  not this dispatch's work to finish, but its eventual commit will change
  `CANONICAL_ATTRIBUTES`'s value count (11 to 13) cited in this REQ's own
  WHAT'S ALREADY DONE section; whoever finishes that REQ should confirm
  this REQ's citations still match after it lands.
- Whether the control_flow.py frontier mechanism and Script 1's design get
  reconciled, extended, or built as two separate systems — unresolved,
  named as the most important open question in the REQ itself.
