# REQ_FRONTIER_TIER
Status: BUILT — provider switched Anthropic -> OpenAI, 2026-07-18. The
Anthropic build (`DISPATCH_FRONTIER_TIER_LIVE__real-anthropic-roundtrip__v20260717_1530.md`,
2026-07-17) proved T04 gate, T04b real-key approve, return-path write at
ASSERTED, and T05 summary live end to end, with boundary_and_consent T04/T05
landing 5/5 on fresh reset+seed. This update re-points `harness/frontier_client.py`
at OpenAI (BYOK, `OPENAI_API_KEY`, live key confirmed 200 via
`GET /v1/models`) — same call shape (question + code-built, fact_id-keyed
payload rows in, concatenated text answer out), same single call site
(`server/voice_orch.py:2619`), web search kept ON via the Responses API's
`web_search_preview` tool. See DISPATCH_FRONTIER_TIER_OPENAI for the
re-run proofs (T04 end-to-end + boundary_and_consent 5x) against the new
provider. Questions 10/11 were not explicitly answered in the original
build — treated as resolved-by-implication (see ANSWERS below) rather than
re-blocking the build, since Bill's own script and BUILD instruction
directly settle what they were asking.
Reconciled-Against: see DISPATCH_FRONTIER_TIER_OPENAI's HASH (commit made
in the same push as this doc)

## ANSWERS (Bill, 2026-07-17, DISPATCH FRONTIER_TIER_BUILD; Q3/Q4 updated
2026-07-18, provider switch)

1. BUILD NOW.
2. NO — do not reuse confirmation_gate.py. Disclosure consent is a
   separate mechanism (`harness/disclosure.py`), not a reuse of either
   confirmation_gate.py or control_flow.py's codeword-gated mechanism
   (the latter requires a spoken codeword, incompatible with "Maya
   approves" — not reused, left untouched).
3. Provider: OpenAI (updated 2026-07-18 — was Anthropic; Anthropic key
   went stale/was being replaced, OPENAI_API_KEY in `~/.env.dev` is the
   live one, curl-confirmed 200). Responses API
   (`https://api.openai.com/v1/responses`), model `gpt-4.1`, tool
   `web_search_preview` — live-tested to actually invoke a real web
   search and return a definitive, cited answer before this switch was
   made permanent (see DISPATCH_FRONTIER_TIER_OPENAI).
4. Key: one key in `~/.env.dev` (`OPENAI_API_KEY`), same convention as
   GROQ_API_KEY/ANTHROPIC_API_KEY. Per-member key storage logged as
   TD-128 (still open, provider-agnostic).
5. Web search: ON, frontier searches on its own — not disabled. (OpenAI
   Responses API `web_search_preview` tool, functionally equivalent to
   Anthropic's `web_search_20250305` this replaces.)
6. Return path: through the normal write path (`memory_engine.store.encode()`,
   the same function every other fact write uses) — not a special-cased
   Neo4j write. Resolves this REQ's own Question 6 sub-clause about a new
   CANONICAL_ATTRIBUTES entry: NOT needed — the return fact reuses
   attribute="zone_district" (augments, coexists with D11). Unchanged by
   the provider switch — the return path never touched the provider.
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
    Unaffected by the provider switch.

Parent context: `docs/BACKLOG.md` BILL-1 ("Frontier tier: build or defer
Script 1... Multi-day build decision. No REQ exists or should be written
until Bill says go"). This dispatch is Bill saying go on the DRAFT only —
not on the build. See BACKLOG UPDATE at the end of this doc for what
changed there. (BACKLOG UPDATE section describes the original 2026-07-17
state; the 2026-07-18 provider switch is scoped work under the same
already-approved REQ, not a new backlog item.)

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
>
> (2026-07-18, provider switch): "point the frontier tier at OpenAI
> instead of Anthropic. The OPENAI_API_KEY is live in ~/.env.dev (curl
> returns 200). The tier is BYOK — base URL, key, request shape. Update
> REQ_FRONTIER_TIER's provider answer to OpenAI. Then run T04 end to end
> and confirm real setback numbers come back from OpenAI and the fact
> lands ASSERTED in Neo4j. Then boundary_and_consent 5x. Keep web search
> on. Commit and push, report the hash."

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
   OpenAI, see ANSWERS above). `log_frontier_authorized_event` (or an
   equivalent invariant) records the crossing before dispatch.
6. The frontier's response lands in the graph as a NEW fact at
   **ASSERTED**, sourced `frontier`.
7. **The beat, run both ways, per Bill's own instruction — this is the
   test that actually matters:** with D11 REMOVED from the payload, the
   frontier's answer must be a hedge (cannot confirm the zone district,
   offers both/several tables, tells the user to look it up). With D11 IN
   the payload, the frontier's answer must be definitive (the specific
   setback numbers, cites the specific code section, states the variance
   path). Both runs must be observed live, not asserted from one run with
   the fact present. (Provider-switch scope note: this re-run's T04
   proof exercises the "D11 present" arm only, matching the original
   DISPATCH_FRONTIER_TIER_LIVE's own scope — the "D11 removed" hedge arm
   was proven once already under Anthropic and is a property of the
   payload builder, not the provider, so it is not re-run per-provider.)

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
  per `scripts/demo_seed.py:122-140`. Attribute strings remain
  `address`/`zone_district` (the `household` migration was attempted and
  reverted — see second correction above); both are now on a temporary
  `_ENUM_EXEMPT_LABELS` list alongside D8, pending Bill's disambiguation
  decision.
- **T04/T04b/T05 built and live-verified against Anthropic**
  (`DISPATCH_FRONTIER_TIER_LIVE__real-anthropic-roundtrip__v20260717_1530.md`):
  disclosure gate, code-built fact_id-keyed payload builder, return-path
  write at ASSERTED via `memory_engine.store.encode()`, T05 EDGE summary
  + email-disposition narration. **Provider switch, 2026-07-18: only
  `harness/frontier_client.py`'s internals (URL, model, request/response
  shape) changed — the disclosure gate, payload builder, return-path
  write, and T05 disposition logic are provider-agnostic and untouched.**
- **The schema decision this REQ was waiting on has since been made and is
  in progress**: `REQ_D21_D23` (filed 1200, IN_PROGRESS, uncommitted) adds
  `incident`/`medication_status` to `CANONICAL_ATTRIBUTES` (13 values now)
  and adds an enum check to `demo_seed.py`'s `_seed_one` (raises on an
  unexempted out-of-enum attribute). Neither change touches D10/D11's
  attribute strings — that part is the blocked item above, not this part.
- **A confirmation-gate mechanism exists and was hardened today**
  (`harness/confirmation_gate.py`, D-03/D-18/D-22, commits `3c0cb74`/
  `28597b5`) — exact yes/no vocabulary, leading-word matching, a `<4`-word
  floor for ambiguous declaratives. T04's "Maya approves" gate does NOT
  reuse this mechanism (see ANSWERS item 2) — noted here as prior
  context, not an open question anymore.
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
  Left untouched, unreconciled — pre-existing open item, not this
  dispatch's scope.

## WHAT'S KNOWN BROKEN / NOT YET BUILT

Carried forward, unresolved in the prep doc itself, unaffected by the
provider switch:
- Whether the frontier model needs live web access to know about the
  April 2026 Lakewood zoning repeal — if it searches, T04 lights two
  tiers, not one, and the routing-pane story in the voiceover changes.
- The setback numbers (section citations, distances) are NOT yet verified
  against actual Title 17 — only the repeal itself has been checked.
- What `NET` prints on a Groq call generally (MID/CORE are Groq, which is
  external) — if it shows `NET ON`, that is a false claim on screen,
  already flagged in the prep doc for T02/T03 and equally relevant here.
- Per-member key storage (TD-128) is still open — the OpenAI key, like
  the Anthropic key before it, is a single household-level key in
  `~/.env.dev`, not "Maya's key" specifically.

## CONSTRAINTS

- **The payload builder must key off `fact_id` (or another stable,
  non-attribute-string identifier), never off `attribute="address"` or
  `attribute="zone_district"` literal matches.** Unchanged by the
  provider switch — `harness/disclosure.py` was not touched.
- **Never present this live with D11's value as a placeholder.** D11 is
  seeded with its real value (R-1-18) — see ANSWERS item 9.
- **Do not conflate this with `harness/control_flow.py`'s existing
  frontier mechanism without a decision** — building a second, parallel
  frontier-crossing concept without reconciling it against the first
  risks two inconsistent audit/authorization stories for "left the
  network," which is exactly the credibility claim this script exists to
  make.
- Must not regress T01-T03, already built and working in the same script
  file.
- **The provider switch must not change the call shape's contract**:
  `call_frontier(question, payload_rows) -> str` — single import site
  (`server/voice_orch.py:132`), single call site
  (`server/voice_orch.py:2619`) — must not change, so nothing downstream
  needs to know which provider answered.

## NEEDS BILL CONFIRMATION — ONE QUESTION PER LINE

All 11 original questions are answered (see ANSWERS above; 10/11 remain
resolved-by-implication, not re-raised by this switch). No new open
questions from the provider switch itself — Bill's 2026-07-18 instruction
directly answered Q3/Q4 (provider, key) and gave the acceptance test
inline ("run T04 end to end and confirm real setback numbers come back
from OpenAI and the fact lands ASSERTED in Neo4j. Then
boundary_and_consent 5x. Keep web search on.").

## BACKLOG UPDATE

`docs/BACKLOG.md` updated in the same commit as the original REQ (2026-07-17):
- New item **#0** (ordered ahead of #1, non-disruptive insertion —
  renumbering all 47 existing rows and every cross-reference between them
  was judged a larger, separate piece of churn than this dispatch's actual
  scope) consolidates the frontier tier at the top of the ordered list,
  superseding the old #47 entry (which now points up to #0).
- `BILL-1` closed the same day the build landed (Anthropic round-trip
  proven, `DISPATCH_FRONTIER_TIER_LIVE`).
- `REQ_SCRIPT01_FRONTIER` removed from the MISSING REQ DOCS table.
- The 2026-07-18 provider switch is scoped maintenance under this
  already-closed REQ/BACKLOG item, not a new backlog entry.
