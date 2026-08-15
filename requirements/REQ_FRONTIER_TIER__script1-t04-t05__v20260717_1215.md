# REQ_FRONTIER_TIER
Status: BUILT — the real Anthropic round trip completed
(`DISPATCH_FRONTIER_TIER_LIVE__real-anthropic-roundtrip__v20260717_1530.md`,
2026-07-17): T04 gate, T04b real-key approve, return-path write at
ASSERTED, and T05 summary all live-verified end to end; boundary_and_consent
T04/T05 landed 5/5 on fresh reset+seed. Questions 10/11 were not explicitly
answered — treated as resolved-by-implication (see ANSWERS below) rather
than re-blocking the build, since Bill's own script and BUILD instruction
directly settle what they were asking.
Reconciled-Against: eb2e274

## ANSWERS (Bill, 2026-07-17, DISPATCH FRONTIER_TIER_BUILD)

1. BUILD NOW.
2. NO — do not reuse confirmation_gate.py. Disclosure consent is a
   separate mechanism (`harness/disclosure.py`), not a reuse of either
   confirmation_gate.py or control_flow.py's codeword-gated mechanism
   (the latter requires a spoken codeword, incompatible with "Maya
   approves" — not reused, left untouched).
3. Provider: Anthropic.
4. Key: one key in `~/.env.dev` (`ANTHROPIC_API_KEY`), same convention as
   GROQ_API_KEY/OPENAI_API_KEY. Per-member key storage logged as TD-128.
5. Web search: ON, frontier searches on its own — not disabled.
6. Return path: through the normal write path (`memory_engine.store.encode()`,
   the same function every other fact write uses) — not a special-cased
   Neo4j write. Resolves this REQ's own Question 6 sub-clause about a new
   CANONICAL_ATTRIBUTES entry: NOT needed — the return fact reuses
   attribute="zone_district" (augments, coexists with D11).
7. Email: no real sending code. Narration only.
8. D10/D11: do NOT migrate to `household` (confirms the collision found
   live under REQ_D21_D23 was real, not a transient bug) — `address` and
   `zone_district` are their own CANONICAL_ATTRIBUTES values instead.
9. D11's real value: R-1-18, confirmed from Jefferson County records —
   seeded, no longer a placeholder.
10. (Not explicitly answered.) Treated as: yes, correct the prep doc's
    stale "phone or hold" T05 text — done in this build's dispatch doc,
    not the prep doc itself (out of scope for a BUILD dispatch to edit a
    prep doc; flagged as still open).
11. (Not explicitly answered.) Treated as: the three prep-doc verification
    items (live web access for the April 2026 repeal, setback numbers vs.
    actual Title 17, NET display truthfulness) block PRESENTING, not
    BUILDING — Bill's BUILD dispatch proceeds straight to code against a
    real, confirmed D11 value (R-1-18) and doesn't re-raise them, so
    presentation-time verification remains open, tracked, not re-asked.

Parent context: `docs/BACKLOG.md` BILL-1 ("Frontier tier: build or defer
Script 1... Multi-day build decision. No REQ exists or should be written
until Bill says go"). This dispatch is Bill saying go on the DRAFT only —
not on the build. See BACKLOG UPDATE at the end of this doc for what
changed there.

## THE REQUIREMENT

Bill's words, verbatim:

> "THE FRONTIER TIER is script 1's T04/T05. It is the top demo item, it is
> UNGOVERNED, and it is not on BACKLOG.md — no defect ID, in none of the
> four registers. It exists only in
> docs/demo_prep/HIP_DemoScript01_BoundaryAndConsent__prep__v20260715_1000.md.
> Add it to the backlog as #1.
>
> BILL'S DESIGN, from the prep doc:
>   T04: zoning question — setback rules at his address and what it takes
>        to get a variance. GATE first, then FRONTIER on approval.
>   PAYLOAD: D10 (address) + D11 (zone_district), both CONFIRMED, built BY
>        CODE from fact rows, never model-composed. Owner and members
>        redacted. The code-built payload IS the governance claim — say so
>        in the REQ.
>   THE BEAT: without D11 the frontier says "go look it up." With it, it
>        answers definitively. That is the whole script: raw intelligence
>        commoditizes, context compounds.
>   RETURN RUNG: ASSERTED (settled).
>   T05: HIP summarizes on EDGE and says it will EMAIL the details. Bill
>        changed this 2026-07-17 — no phone, no second device. The long
>        answer is never read aloud. The email does not have to send. The
>        ASSERTED row is the point; the email is the disposition.
>
> NOTE: D10/D11's attribute is changing to `household` per the schema
> decision. Confirm the payload builder reads fact rows, not attribute
> strings, or this breaks.
>
> D11's VALUE is still TBD — Bill has to pull the real zone district from
> Lakewood's map. Build against a placeholder and flag it. The beat works
> with any value; the real one matters for truthfulness on stage, not for
> the build.
>
> Draft the acceptance test from the above. Then list your questions, one
> line each."

**Second correction, said plainly rather than silently carried forward:**
the household-migration NOTE above is no longer an accurate description of
the current state, even as "decided but not yet landed." `REQ_D21_D23`
(`docs/requirements/REQ_D21_D23__canonical-attribute-enum-expansion-and-seed-schema-validation__v20260717_1200.md`,
filed 15 minutes before this REQ, Status IN_PROGRESS, uncommitted working
changes as of this reconciliation) shows Bill's four-part schema call
included exactly this migration (item 3: "FIX D10/D11 as a SEED BUG... the
seed just used different literal strings. Change the seed to use
`household`"). It was tried, live, this session — and **reverted**.
`scripts/demo_seed.py`'s working diff carries a dated comment on D10/D11:
setting both to `attribute="household"` collides with D7, which already
owns the triple `(household, household, household)`;
`eval/harnesslib/fixture.py`'s `verify_seed` asserts exactly one active
fact per `(owner, subject, attribute)` triple, so three facts sharing one
triple broke immediately on reset (D7's expected value read back as
D10/D11's instead — confirmed live). D10 and D11 are back on their
original literal strings (`address`, `zone_district`), now carrying a
`HOLD` comment and a temporary spot on `_ENUM_EXEMPT_LABELS`, pending
Bill's decision on how to disambiguate multiple household-owned facts
sharing one attribute. **The migration is not "not yet landed" — it is
attempted and blocked.** This REQ's CONSTRAINTS and Question 8 below are
corrected accordingly: building the payload keyed on `fact_id`, never on
the attribute string, is now not just a hedge against a future migration
but the only design that survives the migration being stuck exactly where
it is.

**Correction, said plainly rather than silently acted on:** this is NOT
"not on BACKLOG.md." As of `1bd4500` it appears in three places — row #47
("Frontier tier build (if BILL-1 approves)"), the `BILL-1` NEEDS-BILL row,
and the MISSING REQ DOCS table (`REQ_SCRIPT01_FRONTIER`, with the exact
question "build it for the next meeting, or defer Script 1 and present
2-of-3 scripts?"). It was on the list, just at the bottom, ungoverned, and
waiting on this exact confirmation. Consolidated to the top per the actual
instruction (elevate priority, not "it was absent") — see BACKLOG UPDATE.

## THE ACCEPTANCE TEST — DRAFTED FROM THE ABOVE

**T04 — gate then frontier.**
1. Maya asks the zoning/variance question. HIP does not contact any
   external model yet. It renders a PROPOSED DISCLOSURE payload built BY
   CODE, not by a model, directly from Neo4j fact rows.
2. Every clause in the payload cites its `fact_id` and its rung. A clause
   with no `fact_id` is not possible to construct — verify this
   structurally (the builder has no code path that emits an un-sourced
   clause), not just "none happened to appear in one test run."
3. `owner` and `members` are redacted in the rendered payload. The address
   itself is NOT redacted — per Bill's own framing, a zoning question
   cannot be asked without the address, so the honest claim is "the
   question goes, the questioner doesn't," not "everything identifying is
   stripped."
4. Maya must explicitly approve before anything leaves the network. A
   turn that does not approve must result in nothing sent and no fact
   written.
5. On approval: the frontier tier fires (BYOK, Maya's key, one provider —
   which provider is OPEN, see questions). `log_frontier_authorized_event`
   (or an equivalent invariant, see questions on whether this reuses
   `harness/control_flow.py`) records the crossing before dispatch.
6. The frontier's response lands in the graph as a NEW fact at
   **ASSERTED**, sourced `frontier`.
7. **The beat, run both ways, per Bill's own instruction — this is the
   test that actually matters:** with D11 REMOVED from the payload, the
   frontier's answer must be a hedge (cannot confirm the zone district,
   offers both/several tables, tells the user to look it up). With D11 IN
   the payload, the frontier's answer must be definitive (the specific
   setback numbers, cites the specific code section, states the variance
   path). Both runs must be observed live, not asserted from one run with
   the fact present.

**T05 — disposition (Bill's 2026-07-17 design, supersedes the prep doc's
"phone or hold" text, which is now stale on this point).**
1. HIP summarizes the frontier's long answer ON EDGE — the local model
   talks, the frontier already did the thinking. Verify: this turn's
   `tier` is edge, not core/escalate.
2. The long-form answer (~1000 words with tables, per the prep doc) is
   NEVER read aloud in full, at any point in T04 or T05.
3. HIP tells Maya it will email the details. No phone number is asked
   for, no second device is invoked.
4. **The email does not have to actually send for this acceptance test to
   pass.** What must be true: the ASSERTED fact from T04 step 6 exists in
   the graph BEFORE T05 resolves — the write is the substance, the email
   offer is narration on top of it. If a real send is wired at all (open
   question below), its success/failure must not gate whether T05 is
   considered to have passed.

**Cross-cutting, not turn-specific:**
- The payload builder must not silently regress if D10/D11's `attribute`
  field is later migrated from `address`/`zone_district` to `household` —
  that migration was attempted and reverted this session (see corrections
  above) and remains unresolved, not merely future — see CONSTRAINTS.
- This must never be presented live while D11's value is the "TBD"
  placeholder. The beat works mechanically either way; the CONTENT is
  false on stage until Bill supplies the real number.

## WHAT'S ALREADY DONE

- **T01-T03 built and working** — confirmed directly:
  `demo_scripts/boundary_and_consent__v20260715_1158.json` exists, and its
  own `description` field already states plainly: *"T01-T03 built; T04-T05
  omitted (blocked on PROPOSED DISCLOSURE pane, frontier tier, payload
  builder, return path, T05 disposition...)"* — the JSON file is honest
  about its own gap, not silently incomplete.
- **D10 (address) and D11 (zone_district) are seeded**, CONFIRMED rung,
  per `scripts/demo_seed.py:122-140`. D11's value is the literal string
  `"TBD"` today. Attribute strings remain `address`/`zone_district` (the
  `household` migration was attempted and reverted — see second correction
  above); both are now on a temporary `_ENUM_EXEMPT_LABELS` list alongside
  D8, pending Bill's disambiguation decision.
- **The schema decision this REQ was waiting on has since been made and is
  in progress**: `REQ_D21_D23` (filed 1200, IN_PROGRESS, uncommitted) adds
  `incident`/`medication_status` to `CANONICAL_ATTRIBUTES` (13 values now)
  and adds an enum check to `demo_seed.py`'s `_seed_one` (raises on an
  unexempted out-of-enum attribute). Neither change touches D10/D11's
  attribute strings — that part is the blocked item above, not this part.
- **A confirmation-gate mechanism exists and was hardened today**
  (`harness/confirmation_gate.py`, D-03/D-18/D-22, commits `3c0cb74`/
  `28597b5`) — exact yes/no vocabulary, leading-word matching, a `<4`-word
  floor for ambiguous declaratives. Whether T04's "Maya approves" gate
  should reuse this mechanism is an open question below, not assumed.
- **A DIFFERENT frontier-crossing mechanism already exists and is not
  mentioned in the prep doc at all**: `harness/control_flow.py`'s
  `handle_frontier_request`, gated by a codeword
  (`HIP_FRONTIER_CODEWORD`), with its own invariants (INV-2: an
  authorization event must be logged before any frontier dispatch; INV-3:
  a single legal call site for the actual cross). This shipped
  2026-07-03/07-05 (`e35dcd4`, `60069f8`), before the prep doc was written
  (`d5104ff`, 2026-07-15). **It is a generically-shaped, codeword-gated
  escalation, not a visual disclosure-pane/payload-builder/redaction
  system** — `docs/specs/CONTROL_FLOW__reconsider-frontier-sm__v20260703_1126.md`
  has no mention of zoning, disclosure panes, or a payload builder. The
  prep doc's "Nothing here exists except the routing" is therefore not
  quite accurate: something adjacent exists, shaped for a different UX.
  **This is the single most important open question below** — building
  T04 without first deciding whether it extends this mechanism or
  replaces it risks building the wrong shape twice.

## WHAT'S KNOWN BROKEN / NOT YET BUILT

Per the prep doc's own BUILD LIST (`HIP_DemoScript01_BoundaryAndConsent__prep`,
lines 141-152), nothing on this list exists yet:
1. PROPOSED DISCLOSURE pane — outbound payload rendering, one row per
   fact, fact_id + rung, approve/deny.
2. Frontier tier wired — BYOK, one provider, Maya's key. (Credential
   storage for "Maya's key" does not appear to exist anywhere in this
   codebase — see questions; this may be its own sub-build, not a detail.)
3. Payload builder — code, not model-composed, reading fact rows.
4. Return path — frontier response lands as a fact at ASSERTED.
5. T05 disposition — summary on EDGE, then the email-offer prompt (NEW
   design, 2026-07-17 — the prep doc's own T05 text, "phone or hold," is
   now stale and should be corrected there too, not attempted in this
   dispatch).
6. `narration` field in the demo-script turn schema.
7. The T04/T05 turns themselves in
   `demo_scripts/boundary_and_consent__v20260715_1158.json` — not written.

Additionally, unresolved in the prep doc itself and carried forward here
because they bear directly on "demo that is true" (Goal 1), not because
this dispatch resolves them:
- Whether the frontier model needs live web access to know about the
  April 2026 Lakewood zoning repeal — if it searches, T04 lights two
  tiers, not one, and the routing-pane story in the voiceover changes.
- The setback numbers (section citations, distances) are NOT yet verified
  against actual Title 17 — only the repeal itself has been checked.
- What `NET` prints on a Groq call generally (MID/CORE are Groq, which is
  external) — if it shows `NET ON`, that is a false claim on screen,
  already flagged in the prep doc for T02/T03 and equally relevant here.

## CONSTRAINTS

- **The payload builder must key off `fact_id` (or another stable,
  non-attribute-string identifier), never off `attribute="address"` or
  `attribute="zone_district"` literal matches.** This is no longer a hedge
  against a hypothetical future migration — `REQ_D21_D23` shows the
  `household` migration for D10/D11 was actually attempted and **reverted**
  live this session (collision with D7's existing
  `(household, household, household)` triple under `verify_seed`'s
  one-active-fact-per-triple rule; see second correction above). D10/D11
  are back on `address`/`zone_district` today, on a temporary exemption
  list, with the disambiguation question still open. A builder keyed on
  the literal attribute string would need to change again the moment that
  question resolves, however it resolves — `fact_id`-keying is the only
  version of this that survives the migration being stuck.
- **Never present this live with D11's value as `"TBD"`.** The mechanism
  works with any string in that slot; the demo is dishonest with a
  placeholder in it.
- **Do not conflate this with `harness/control_flow.py`'s existing
  frontier mechanism without a decision** (see WHAT'S ALREADY DONE and
  questions below) — building a second, parallel frontier-crossing
  concept without reconciling it against the first risks two
  inconsistent audit/authorization stories for "left the network," which
  is exactly the credibility claim this script exists to make.
- Must not regress T01-T03, already built and working in the same script
  file.
- Per CLAUDE.md item 8: no code changes proceed from this REQ, on any part
  of it, until the questions below are answered — this includes the
  disclosure-pane UI, the frontier wiring, the payload builder, and the
  narration field, individually, not just "the big design questions."

## NEEDS BILL CONFIRMATION — ONE QUESTION PER LINE

1. Build now, for a specific next meeting, or defer Script 1 and present
   2-of-3 scripts — the exact question BACKLOG's own missing-REQ line
   already had on file. Answer this one first; everything else is moot
   until it's a "build."
2. Does T04's "Maya approves" gate reuse `harness/confirmation_gate.py`
   (today's hardened yes/no/leading-word logic), reuse
   `harness/control_flow.py`'s existing codeword-gated
   `handle_frontier_request`, or is it a third, new mechanism?
3. Which frontier provider (BYOK)? The design says "one provider, Maya's
   key" but names none.
4. Where does "Maya's key" live? No per-member API-key storage mechanism
   currently exists in this codebase, as far as this REQ found. Is that
   its own sub-build, and if so, what's the security model for it
   (encrypted at rest? who can view/rotate it?)?
5. Is the frontier call permitted live web access, or must it answer from
   training data alone? This changes whether the routing pane shows one
   external hop or two, and the voiceover's own claims about what's
   happening.
6. Does the return-path write (frontier answer → ASSERTED fact) go
   through the existing Groq detect_and_apply/enum-constrained pipeline,
   or is it a direct, code-driven write (like `demo_seed.py`'s `encode()`
   calls)? If it goes through detection, does the new fact's attribute
   (something like "zoning ruling" or "variance status") also need a
   CANONICAL_ATTRIBUTES entry that doesn't exist yet — the same D-23 class
   of problem, on a brand-new fact type this feature would introduce?
7. Does ANY real email-sending code need to exist for this build, or is
   "I'll email you the details" pure narration with nothing behind it
   (per "the email does not have to send")? If real, what's the
   recipient, and what happens on send failure mid-demo?
8. The `household`-attribute migration for D10/D11 was attempted and
   reverted this session (collision with D7 under `verify_seed`'s
   one-fact-per-triple rule — see corrections above). How does Bill want
   to disambiguate multiple household-owned facts sharing one attribute —
   a compound/qualified attribute value, a different key entirely for
   `verify_seed`'s uniqueness check, or something else? Until that's
   decided, should this build proceed now against the current
   `address`/`zone_district` strings behind the fact_id-keyed builder (see
   CONSTRAINTS), treating the eventual migration as a non-event for this
   feature specifically?
9. When will the real D11 zone-district value be available (Bill pulling
   it from Lakewood's map)? Does the build proceed now against the "TBD"
   placeholder regardless, per the instruction, with presentation blocked
   separately on the real value landing?
10. Should this dispatch also correct the prep doc's now-stale T05 text
    ("phone or hold") to match the 2026-07-17 email design, or leave that
    for whoever actually builds T05?
11. Do the three unresolved prep-doc items (live web access needed for
    the April 2026 repeal, setback numbers unverified against real Title
    17, `NET` display truthfulness on Groq calls) block THIS build, or
    only block PRESENTING it — i.e., can the code be written now and the
    verification happen right before the demo, or does verification need
    to happen before anyone starts building against numbers that might be
    wrong?

## BACKLOG UPDATE

`docs/BACKLOG.md` updated in the same commit as this REQ:
- New item **#0** (ordered ahead of #1, non-disruptive insertion —
  renumbering all 47 existing rows and every cross-reference between them
  was judged a larger, separate piece of churn than this dispatch's actual
  scope) consolidates the frontier tier at the top of the ordered list,
  superseding the old #47 entry (which now points up to #0).
- `BILL-1` updated: a draft REQ now exists
  (`REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`), status PLAN,
  pending the 11 questions above — not "no REQ should be written until
  Bill says go" anymore, since this dispatch IS Bill saying go on the
  draft specifically.
- `REQ_SCRIPT01_FRONTIER` removed from the MISSING REQ DOCS table (it is
  no longer missing — it exists, in draft, right here).
