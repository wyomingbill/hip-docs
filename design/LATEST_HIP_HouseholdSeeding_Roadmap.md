# HIP_HouseholdSeeding_Roadmap — Design Roadmap for Household Seeding, Confirmation, and the Boundaries Around Both

Status: DESIGN-DRAFT
Branch: roadmap
Reconciled-Against: `HIP_HouseholdSeeding_Roadmap__v20260730_1936.md` (the
prior version, superseded by this filing), revised per D-57 to fix ONLY what
was false or forbidden in it — four corrections, no design change and no
ruling: (a) the CORROBORATED wiring, withdrawn and aligned with `REQ_ATTESTED`
and D-50 Principle 3, corrected in all THREE places it appeared (Part 1's
trust-ladder wiring, Zone 2's justification, and the seeding-semantics
restatement — the third was not enumerated in the dispatch and is flagged in
place); (b) the justification/trust-ordering claim, bounded by Bill's D-53
"record both, rank neither" ruling; (c) the research-grounding appendix's
opening, which falsely characterized external review as confirmation; (d)
`eligible_confirmers`, named as a CURRENT BLOCKER rather than absorbed into
the durable-pending framing. **Findings 3, 4, 5 and 6 of the D-46 review
(sensitivity encoding, the self-healing/never-re-ask contradiction, the depth
loop and canary blind spot, and the Part 2 items) were deliberately NOT
touched by this revision — those are Bill's calls and remain open.**

**Provenance note from the prior version — RETIRED, gap closed.** That
version flagged that no captured artifact for the research passes it cited
existed in `docs/reviews/`. That is no longer true: D-49 banked
`CHATGPT_research-pass1.txt`,
`CHATGPT_research-pass2-selfcertifying.txt`,
`CHATGPT_research-pass3-trust-axis-evaluation.txt`, and
`FABLE_D46_seeding-critique.md`, and D-54/D-55 banked
`FABLE_D46_critique__household-seeding-parts1-3__v20260731_1258.md`. The
research and review provenance behind this document is now verifiable from
the repo, and the flag is withdrawn rather than carried forward out of habit.

Otherwise unchanged from the prior version: no code exists for any
of the five parts below. Where this roadmap touches already-ratified HIP
architecture — trust ladder (ASSERTED/CONFIRMED/CORROBORATED), the
injection contract, partition custody, the write-rule table — the existing
ratified design controls; this document proposes how a NEW subsystem
(confirmation, seeding, boundaries, safety) sits on top of that ratified
layer, not a replacement for it.

## Why this document exists, and how to read it

Five parts, deliberately ordered by dependency, not by build priority:

1. **Confirmation Subroutine** — the mechanism. Persistent, always-on,
   owns fact confirmation everywhere in the system.
2. **Seeding/Onboarding** — the first, highest-value CALLER of the
   subroutine. Not a special mode; a use case.
3. **Boundary Manager** — governs how much the system may ask for or infer,
   independent of who's asking or why.
4. **Safety Layer** — governs harm. Deliberately separate from the Boundary
   Manager, because "too much" and "dangerous" are different failure
   classes with different remedies.
5. **Cross-Cutting Constraint** — the hardware/custody reality (operator-
   custodial device, no per-member device keys yet) that bounds what Parts
   3 and 4 can actually promise, stated once so it isn't silently assumed
   away in either.

Read order matters: Part 1 is infrastructure; Parts 2-4 are policies built
on it; Part 5 is the ceiling on what any of Parts 3-4 can guarantee today.
A reviewer who reads only Part 2 and skips Part 1 will think seeding is a
wizard with a progress bar. It is a conversation the confirmation
subroutine is quietly instrumenting the whole time.

---

## PART 1 — THE CONFIRMATION SUBROUTINE

### What it is

A **persistent, always-on, path-independent** mechanism that owns every
fact's journey from `UNCONFIRMED` to `CONFIRMED` by its **authorized
confirmer** — the subject themselves for most attributes, a custodian for
a dependent's facts, whichever role the trust-ladder rules already assign.
It is not a feature of seeding. It is not a feature of any single
conversational path. It runs underneath ordinary conversation, corrections,
consolidation passes, and the household-onboarding interview described in
Part 2 alike. Seeding, KYC-style verification, and consolidation are
**callers** of this subroutine, not implementations of it. If the household
never runs a formal onboarding interview at all, the confirmation
subroutine still exists and still does its job — slower, opportunistically,
one confirmed fact at a time, in ordinary conversation.

This is the central design decision this roadmap makes, and it is worth
stating why: every prior sketch of "onboarding" implicitly built
confirmation logic INTO the onboarding flow, which meant every other path
that touches an unconfirmed fact — a correction six weeks later, a
consolidation pass merging two records, a member volunteering information
outside any interview — had to reimplement the same judgment calls (who may
confirm this, what happens if they decline, how long an ASSERTED fact
waits before someone asks about it again). Extracting it into one
subroutine means every caller gets the same answer to "is this fact
confirmed, and if not, whose job is it to confirm it and when should we
ask."

### What it must never do

- **Never force.** No fact reaches `CONFIRMED` by the subroutine insisting.
  Confirmation is something the authorized confirmer does; the subroutine's
  job is to make the opportunity to do so show up at low cost, at the right
  time, to the right person — never to gate functionality on it, never to
  repeat a question the confirmer has already declined to answer, never to
  imply that a household member cannot be helped until they confirm
  something.
- **Never force-resolves; degrades to durable-pending.** A fact that
  cannot currently be confirmed (the confirmer isn't present, isn't a
  customer yet, is a dependent who cannot self-confirm) does not sit
  forever as a silent, untracked gap — but the subroutine does not
  guarantee it eventually resolves either. What it guarantees is a
  **durable-pending** state: re-routed where re-routing is possible (to
  another eligible confirmer, a custodian per the trust ladder's existing
  rules, a later turn, a lower-friction channel), and left honestly pending
  where it is not. "We don't know yet and haven't found the moment to ask"
  is a tracked state, not an untracked one — but "we may never get to ask"
  is also a legitimate, permanent outcome the design must tolerate, not a
  failure the subroutine is expected to eventually eliminate.
- **The stranding case, named as an accepted state, not a failure.** A
  fact whose authorized confirmer is **permanently unavailable** —
  estranged, deceased, never became a customer, a dependent with no
  eligible custodian on record — cannot be re-routed to resolution by any
  amount of subroutine cleverness. This is not a bug to design around; it
  is a real and permanent shape of durable-pending that the subroutine, its
  callers, and anything that reads confirmation state downstream must
  handle as a first-class, expected outcome: the fact stays at its current
  trust rung indefinitely, honestly labeled, never silently upgraded and
  never treated as an error condition requiring resolution.
- **Self-healing.** If a confirmation attempt is interrupted, misfires, hits
  a member who doesn't want to engage right now, or targets someone who
  turns out not to be the right confirmer after all — the subroutine
  recovers on its own on the next opportunity. No stuck states, no
  operator-required unsticking, no doc-only workaround. This is a runtime
  property, not a policy statement: whatever data structure represents "this
  fact is awaiting confirmation from X" must be re-derivable from state that
  already exists (the trust ladder rung, the fact's `confirmed_by`/
  `write_state`, the roster of eligible confirmers) rather than a
  side-channel flag that can itself get stuck.

### The second job: progressive graph-deepening

Confirmation and depth are the same mechanism running in two directions.
A subroutine that decides WHEN to surface "can you confirm X" to a member
is doing the identical work as one that decides WHEN to surface "would you
like to tell me more about Y" — both are picking the next highest-value,
lowest-friction question given everything currently known about this
household's engagement, mood, and history with the system. Treating these
as one mechanism (rather than a confirmation pass plus a separate
depth-seeking pass) is why Part 1 is infrastructure and Parts 2-4 are
policy: the subroutine exposes one decision — "what is the next thing worth
asking, of whom, right now" — and Part 2's onboarding interview, Part 3's
boundary limits, and ordinary steady-state conversation are all just
different callers constraining that decision differently.

### Interfaces this subroutine must expose to its callers

(Named here so Parts 2-4 can be read against them; not a code-level API
spec — this is a design roadmap, not an implementation.)

- **`next_confirmable(household, member?) -> fact | None`** — the next
  fact worth surfacing for confirmation, optionally scoped to a specific
  member's turn. Must respect the boundary manager's depth ceiling (Part 3)
  and must never re-surface a fact the confirmer has already declined
  within some backoff window.
- **`record_confirmation_outcome(fact, confirmer, outcome)`** — confirmed,
  declined, deferred, corrected-in-the-process. Feeds the trust ladder
  (`ASSERTED` → `CONFIRMED` on subject's own confirmation;
  `CONFIRMED` → `CORROBORATED` when a second household member
  independently agrees — see below) and feeds back into `next_confirmable`'s
  backoff logic.
- **`eligible_confirmers(fact) -> [member]`** — derived from the existing
  trust-ladder/custody rules (who may confirm a dependent's fact, whether a
  fact requires self-confirmation or accepts a custodian's), never asserted
  by the caller. This mirrors the isolation-gate design principle already
  ratified elsewhere in this codebase (derive scope from server-
  authoritative state, never trust the caller) and should reuse it rather
  than reinvent a parallel authority model.

  **CURRENT BLOCKER — this derivation returns nothing today, and that is a
  live defect, not a designed state.** Code-verified against the live
  registry: all five `members` rows (`bill`, `maya`, `sam`, `p4smoke_x`,
  `p4smoke_y`) have `household_id = NULL`, and the `dyads` table has no
  member columns at all (`dyad_id, recipient_ref, household_id, dyad_pubkey,
  status, created_at`), so a dyad-modelled custodian is underivable. Applied
  honestly, the derive-from-server-state mandate above therefore yields an
  **empty eligible-confirmer set for essentially every member-owned fact**,
  and every such fact lands in durable-pending **on day one** — not because
  its confirmer is unavailable, but because the system cannot work out who
  the confirmer is.

  This must not be absorbed by the durable-pending framing above. Stranding
  describes a fact whose confirmer is genuinely unreachable; this is a fact
  whose confirmer exists, is present, and is willing — and the derivation is
  broken. Presenting the two as the same state would make a blocking defect
  look like an accepted outcome. **Nothing in Part 1 works end-to-end until
  member enrolment populates `members.household_id` and the dyad schema
  gains its member columns.** (The `household_id` gap is the same D-31b named
  limit the isolation gate already carries; the dyad schema gap is D-36
  finding (c), confirmed against the live DB.)
- **`next_depth_question(household, member?) -> topic | None`** — the
  depth-seeking twin of `next_confirmable`, gated by the Boundary Manager
  (Part 3).

### Trust-ladder wiring (uses the existing ratified ladder; does not invent a new one)

- **Subject confirms their own fact → `CONFIRMED`.** Standard case, no
  change to existing rules.
- **Household agreement → a NEW rung (`ATTESTED`), NOT `CORROBORATED`.**
  Prior versions of this roadmap said a second household member's
  independent affirmation "promotes" a `CONFIRMED` fact to `CORROBORATED`,
  and claimed that did not change what `CORROBORATED` means. **Both halves
  of that were wrong, and the text is withdrawn here rather than softened:**
  - `CORROBORATED`'s ratified meaning is a **reconciliation-hardening**
    event — `memory_engine/trust.py:73` requires `confidence == "high"` plus
    a `confidence_log` entry with `source == "reconcile"` and `to > from`.
    No second person appears in it anywhere. Social agreement is a different
    thing wearing the same name.
  - It was a **demotion, not a promotion**: `TRUST_RANK` has
    `CORROBORATED: 2` below `CONFIRMED: 3`.
  - It was **structurally unreachable**. `classify_trust_props` is
    first-match-wins (`trust.py:70-78`): `confirmed_by is not None` returns
    `CONFIRMED` *before* the corroboration branch is ever evaluated, and a
    fact at `CONFIRMED` has `confirmed_by` set by definition. D-51 proved
    this exhaustively — 144 input combinations, `CORROBORATED` returned 4
    times, **zero** of them with `confirmed_by` set. No input state moves a
    `CONFIRMED` fact to `CORROBORATED`.

  Per Bill's ruling (D-52/D-53), **`CORROBORATED` keeps its
  reconciliation-hardening meaning and social multi-party attestation gets a
  new rung name, `ATTESTED`** — scoped in
  `docs/requirements/REQ_ATTESTED__social-multiparty-attestation-schema__v20260731_0739.md`
  (DESIGN-DRAFT, not authorized for build, dependent on the attributed-claim
  model). Reusing the name would silently reclassify every already-logged
  fact and invalidate two specs that pin the current meaning. This is the
  same conclusion D-50's confirmation model reached independently at its
  Principle 3 ("corroboration is a separate axis, not a rung — a real schema
  change, not a reinterpretation").

  **`ATTESTED` is not specified by this roadmap and must not be built from
  it.** Two costs are recorded in its REQ and matter to anything Part 2
  assumes: `confirmed_by` is a single scalar, so N attestations cannot be
  represented without a schema change; and household members are the least
  independent attesters available, so each attestation must carry provenance
  sufficient to answer "could B have heard this from A?" — including from HIP
  itself, since a member affirming a fact the system just disclosed to them
  is an echo, not evidence.
- **Custodian confirmation of a dependent's fact: deliberate, per-fact, no
  self-exempt shortcut.** A custodian confirming on behalf of a dependent
  (a child, an incapacitated adult, whichever custody relationship the
  ratified custody model already recognizes) must confirm **each fact
  individually** — there is no "confirm everything about this dependent at
  once" shortcut. This is a deliberate friction, not an oversight: a
  custodian who could bulk-confirm a dependent's entire profile in one tap
  is a custodian who never actually reviewed most of it, and the
  Safety Layer (Part 4) depends on custodian confirmation being a genuine
  point of attention, not a formality. The tradeoff this creates — bulk
  confirmation is exactly the low-friction design Part 2 wants for
  everything else — is named explicitly here so it is not "discovered"
  mid-build: dependent-fact confirmation is the one place this roadmap
  chooses friction over ease, on purpose.

### Trust storage model: justifications, not scalar rungs (truth-maintenance-system style)

The trust ladder's rungs (`ASSERTED`/`CONFIRMED`/`CORROBORATED`) are useful
as a **displayed, derived summary** — but the underlying data model this
roadmap specifies should not store trust as a bare scalar. It should store
a **justification**: who said this, who confirmed it (if anyone), and what
else backs it (a corroborating statement, a document, another fact it was
derived from) — the structure a classical truth-maintenance system
(Doyle's TMS; de Kleer's ATMS) or an AGM-style belief-revision model
(Gärdenfors) would keep, rather than a single collapsed number. The rung a
fact currently displays at is then a computed VIEW over its justification,
not the stored fact itself.

This one design decision eases three separate problems this roadmap would
otherwise have to solve independently:

- **Trust-ordering.** Comparing two facts' relative confidence becomes a
  query over their justification structures, not a hand-maintained
  rung-comparison table that has to be extended every time a new
  comparison case comes up. **Bounded by Bill's D-53 ruling, "record both,
  rank neither," which stands:** justifications make the inputs to a
  context-specific judgment *available* to a consumer that has the context
  to weigh them; they do not license the system to compute a
  relative-confidence verdict of its own. The system stores what it knows —
  who asserted, who attested, with what provenance — and declines to collapse
  those into a single ordering. See
  `REQ_TRUST_AXES__record-both-rank-neither__v20260731_0827.md`.
- **Sensitivity encoding.** A fact's justification can carry
  provenance-sensitive detail — WHO confirmed a sensitive fact, for
  instance — that a bare rung cannot represent without a parallel
  side-channel invented just to carry it.
- **The audit trail.** Part 4's Safety Layer, and any future dispute
  resolution, need "why does the system believe this" to be answerable
  from the stored structure itself, not reconstructed after the fact from
  logs that happen to still exist.

Justification-based storage gives all three the same underlying
representation instead of three separately-maintained ones — the same
economy-of-mechanism argument that made Part 1 itself a single subroutine
rather than three separate confirmation implementations.

### Open questions this part does not resolve

- The exact backoff/re-ask cadence for a declined or deferred confirmation
  (hours? days? tied to conversation volume rather than wall-clock time?).
- Whether `next_confirmable` and `next_depth_question` should be one
  unified priority queue or two separately-tunable ones that get merged at
  the last moment before a turn. (This roadmap's position, stated above, is
  that they are the same underlying decision; whether the implementation
  literalizes that as one function or two cooperating ones is open.)
- The exact justification schema (what fields a justification record
  carries beyond who-said-it/who-confirmed-it/what-backs-it, and how deep
  a chain of "what backs it" is retained before summarizing) is left to
  implementation; this roadmap specifies the representational commitment
  (justifications, not scalars), not the schema.

---

## PART 2 — SEEDING / ONBOARDING (a caller of Part 1, not a mechanism of its own)

### Framing

Seeding is the first, richest, highest-value call site for the
confirmation subroutine — not a separate onboarding engine. Everything
below describes how seeding CALLS Part 1's primitives under a specific set
of UX constraints (voice-first, one designated narrator, progressive,
never-shame); it does not re-specify confirmation logic that Part 1 already
owns.

### The Narrator

One household member is **designated as the narrator** and does a
**voice-first bootstrap conversation** — the household's own person telling
HIP about the household, in their own words, rather than a form. This is
deliberately asymmetric: the narrator is not "the account holder" by
necessity and not necessarily the person whose facts get the most
attention; they are simply the person doing the initial telling. Other
members' facts, once mentioned, still route through Part 1's ordinary
confirmation subroutine (self-confirms when present, custodian-confirms
for dependents) — the narrator's telling does not itself confirm anything
about anyone but the narrator.

### Progressive and resumable — explicitly not single-session

There is no requirement that seeding complete in one sitting, one day, or
even one week. The interview is a standing invitation the confirmation
subroutine keeps alive (via `next_confirmable`/`next_depth_question`)
across as many sessions as it takes. A household that seeds in five
two-minute conversations over three weeks has had exactly as valid a
seeding experience as one that does it in one twenty-minute sitting.
Nothing in the design should assume a completion event; there is only
ever-increasing coverage.

### Four-zone interview structure

Research-validated (see RESEARCH-GROUNDING below — this ordering is the
classical funnel technique applied to a household interview); ordered
deliberately, high-value-low-friction first:

1. **Household-with-pride.** Open with what the household is happy to
   describe unprompted: names, who lives here, pets, the shape of daily
   life. This zone exists to establish the conversational register (warm,
   curious, not clinical) and to bank several easy `CONFIRMED` facts before
   any harder ground is touched.
2. **People.** Who's who, relationships, roles. (Prior versions justified
   this zone as "the zone most likely to produce `CORROBORATED` promotions."
   That justification is **withdrawn** — the promotion it named cannot fire;
   see Part 1's trust-ladder wiring. This zone's remaining rationale is the
   ordinary one: relationships and roles are load-bearing for everything
   else, and the narrator can usually describe them at low cost. If the
   `ATTESTED` rung is ever built, this is where multi-party attestation would
   most plausibly arise — but nothing in this roadmap depends on that, and
   the zone must stand or fall on its own merit rather than on a mechanism
   that does not exist.)
3. **Care and how-you-live.** Health conditions, routines, care
   arrangements, the material the rest of HIP is actually built to help
   with. Deliberately placed after the two easier zones, once the
   conversational register is established and some trust has accrued.
4. **Optional.** Anything the narrator wants to add that doesn't fit the
   above — explicitly framed as optional so its absence is never read as a
   gap to chase.

### Design principles governing every zone

- **High-value, low-friction first**, both within a zone and across zones
  — always ask for the thing most useful to the household that costs the
  narrator the least to answer, before anything costlier.
- **Never-shame.** No framing implies the household is behind, incomplete,
  or falling short by not having answered something yet. This is a
  narrower, sharper version of the Boundary Manager's general "never shame
  a gap" principle (Part 3), stated here because seeding is the highest-
  volume place unconfirmed gaps will be visible.
- **Reflect, don't interrogate.** The system's turns in this interview
  paraphrase and reflect back what it heard ("sounds like weekday mornings
  are the busiest part of your day") rather than issuing the next question
  in a checklist voice. This is a conversational-quality requirement, not
  a cosmetic one: an interrogation register measurably increases perceived
  friction even when the actual question load is identical.

### MINIMUM SEED threshold — OPEN

There is a threshold of seeded information below which the system runs in
a named **degraded mode** and at or above which it runs at **full**
capability. **The exact threshold is OPEN** — this roadmap does not set a
number, the same way `REQ_CURATOR_SHADOW_SCORER`'s Gate A trip point was
left as Bill's call rather than guessed at. What this roadmap does specify:

- **Degradation must be legible and invitational, never a silent
  handicap.** If the household is below threshold, the system should be
  able to say, in effect, "I can do more here once I know a bit more about
  X" — not simply perform worse without explanation.
- **Below-threshold is a real, supported operating mode**, not an error
  state or a nag screen. A household that never crosses the threshold
  still gets a working system; it gets a plainly-communicated ceiling on
  a working system.
- **The threshold, whatever its value, is measured on CONFIRMED coverage**,
  not on raw fact count — an unconfirmed dump of a hundred details a
  household member half-remembers is not "more seeded" than ten carefully
  confirmed facts, and MINIMUM SEED should not be gameable by volume.
- **The threshold must be set low enough to avoid an early "the system is
  broken" impression.** The first few real turns after seeding — before
  enough has accumulated to leave degraded mode — are where a household
  forms its first impression of whether HIP works at all. A threshold set
  too high risks that entire early window reading as broken rather than as
  honestly early. This is a substantive argument for erring low by default
  rather than treating the choice as symmetric: setting the number too low
  costs a slightly premature "full" claim; setting it too high costs an
  extended first impression of brokenness, which is the more damaging
  failure of the two. Bill's number should weigh that asymmetry, not split
  the difference blindly.

### When the narrator stalls: re-routing to KYC-style member interviews

If the designated narrator runs out of things to say, disengages, or is
simply the wrong person to know a particular fact (a spouse who doesn't
know a dependent's medical history in the detail a custodian would), the
confirmation subroutine (Part 1) **re-routes the open questions to the
relevant OTHER members directly** — a KYC-style individual interview,
scoped to exactly the gaps the narrator's account left open, not a repeat
of the whole four-zone interview from zero. This re-routing is Part 1's
`next_confirmable`/eligible-confirmer machinery doing exactly what it does
in steady state; seeding just generates an unusually large initial backlog
for it to work through.

### Confirmation semantics specific to seeding (inherits Part 1, adds nothing new)

- Subject-confirmed → `CONFIRMED` (standard).
- Household-agreed → **NOT `CORROBORATED`.** Withdrawn here for the same
  reason as in Part 1: the promotion is structurally unreachable and
  `CORROBORATED` means reconciliation-hardening, not social agreement.
  Social attestation is the separate, unbuilt `ATTESTED` rung
  (`REQ_ATTESTED`, DESIGN-DRAFT). Seeding must not assume it exists.
  (This third restatement was not enumerated in the D-57 dispatch, which
  named the Part 1 and Zone 2 instances; it is corrected here because
  leaving it would have left the document still asserting the thing the
  ruling forbids.)
- Custodian confirms EVERY dependent fact deliberately, no bulk shortcut
  (standard, per Part 1's explicit design choice above) — restated here
  because seeding is the moment a custodian is most likely to be tempted
  to bulk-confirm a dependent's whole profile in one enthusiastic sitting,
  and the interview UX must not offer that shortcut even as a convenience.

### Open implementation concern: the custodian-confirmation bottleneck

Part 1's per-fact, no-bulk-shortcut rule for custodian confirmation (a
deliberate choice, not an oversight — see Part 1) has a real seeding-time
cost: a household with several dependents (multiple children, an elderly
parent, some combination) hands one custodian a **long queue** of
individually-confirmable facts, all funneled through that one person,
potentially dwarfing the narrator's own confirmation load many times over.
Flagged here as an **open implementation concern**, not resolved by this
roadmap: the low-friction, high-value-first design principles that make
seeding pleasant for a single narrator describing their own life do not
automatically make a long custodian queue pleasant, and no UX mitigation
for that queue length is specified here. Whether the answer is pacing the
queue across many sessions (consistent with the progressive/resumable
design generally), some form of batched-but-still-attentive confirmation
that stops short of the rejected bulk shortcut, or something else, is left
open.

---

## PART 3 — BOUNDARY MANAGER (governs DEPTH)

### What it governs, and what it does not

The Boundary Manager answers exactly one question: **how much is this
household currently willing to be asked, and how much has the system
earned the right to ask, right now.** It does not adjudicate truth, danger,
or harm — that is Part 4's job, deliberately separated. The Boundary
Manager's failure mode, if it fails, is **creepiness and surveillance
feeling** — a household that feels watched, probed, or quantified rather
than cared for. That is a distinct and survivable-if-caught-early failure
mode from the Safety Layer's failure mode (someone gets hurt), which is why
these are two components, not one dial.

### Named framework: this is contextual integrity, operationalized

The Boundary Manager's design is not an ad hoc set of heuristics; it is
**Helen Nissenbaum's contextual integrity** framework, operationalized for
this specific relationship. Contextual integrity's core claim — that
privacy is not secrecy or control in the abstract, but whether an
information flow matches the norms of the context it was shared in — is
exactly what "earn depth, don't take it" and "detail must visibly serve
the family" are doing below: a household sharing care details with HIP has
an implicit norm about what that sharing is FOR, and the Boundary Manager's
job is to keep every subsequent ask inside that norm rather than importing
an unrelated one (a form's "collect everything up front," a surveillance
system's "collect everything, always") the household never agreed to.
Naming the framework explicitly gives the Core principles below a shared
vocabulary and a literature to check future design decisions against,
rather than re-deriving the same intuitions from scratch each time a new
sensitive-attribute case comes up.

### Core principles

- **Earn depth, don't take it.** Every increase in how personal, specific,
  or sensitive a question gets must be justified by the household's own
  prior engagement — more time in the relationship, more confirmed facts
  already on record, more instances of the household volunteering detail
  unprompted. Depth is not something the system is entitled to reach for
  just because a topic is relevant; it is something the relationship has
  to earn the right to ask about.
- **Follow engagement.** The pace of depth-seeking tracks the household's
  own signals of engagement (volunteering more, asking follow-up questions,
  returning to a topic) rather than a fixed schedule. A household that
  engages eagerly may earn depth faster; one that engages minimally should
  not be pushed at the same pace just because the calendar says it's been
  a week.
- **Back off at withdrawal.** Any signal of discomfort, curtness, topic-
  changing, or declining to answer is read as withdrawal, and the Boundary
  Manager backs off — not just on the specific question declined, but on
  the general depth ceiling for some window, the same way a person would
  ease up after sensing they'd pushed too far in conversation.
- **Never shame a gap.** An unconfirmed fact, a declined question, a topic
  the household has never brought up — none of these are treated, in any
  system-generated language, as a deficiency. This principle is shared
  with Part 2's "never-shame" but stated here as the general case: it
  applies to every interaction with the Boundary Manager, not only the
  seeding interview.
- **Detail must visibly serve the family — purpose limitation / data
  minimization (GDPR Art. 5), kept as-is; this principle is sound and
  research-confirmed.** Every piece of depth the system seeks should be
  legibly in service of something the household can see the value of — a
  better answer, a more useful reminder, a genuinely relevant follow-up —
  never depth for its own sake, never data collection the household can't
  connect to a benefit. **What changes in this revision is not the
  principle but how it is tested.** The prior version tested this
  principle by asking whether the system's own next turn could make the
  value of having asked visible — a self-certifying test, since it let the
  system grade its own compliance with its own principle. See the
  EVALUATION PORTFOLIO below, which replaces that test.
- **Sensitivity gates depth.** The more sensitive an attribute already is
  (per the existing sensitivity classification — `low`/`medium`/`high`/
  `critical`), the higher the engagement bar before the Boundary Manager
  will let the confirmation subroutine surface a question about it at all.
  This composes with `next_confirmable`'s existing job: sensitivity isn't
  a separate check bolted on afterward, it's an input the Boundary Manager
  gives the subroutine when deciding what's currently askable.

### Evaluation portfolio, replacing the self-certifying test

The prior version of this roadmap tested "detail must visibly serve the
family" by asking whether the system's own next turn could make the value
of having asked visible — the system grading its own compliance with its
own principle. That test does not survive scrutiny: it can always be
satisfied by writing a more persuasive-sounding next turn, regardless of
whether the underlying ask actually served the family. Replaced here with a
five-part evaluation portfolio, no single piece of which is sufficient
alone:

- **(a) Pre-registered expected observable.** Before a depth-seeking
  question is asked, the specific, falsifiable outcome it is expected to
  produce is written down FIRST — not inferred afterward from whatever
  happened. Prevents the question from being retroactively justified by
  whatever the system's next turn happens to say.
- **(b) Canary metrics the system is FORBIDDEN to optimize.** Withdrawal
  rate, decline rate, and disengagement rate are tracked and must not RISE
  as a consequence of any change to the depth-seeking logic — but nothing
  in the system is permitted to directly optimize against these metrics
  (which would just teach it to suppress the signals rather than reduce
  the underlying behavior). They are a tripwire, not a training target.
- **(c) Behavioral outcomes with exposure correction.** Whether
  depth-seeking correlates with genuinely better outcomes (task success,
  retention, engagement quality) has to control for how much exposure a
  household has had to the system at all — more depth and more
  time-in-relationship are confounded, and a naive correlation would
  credit depth-seeking for what is really just tenure.
- **(d) A held-out arm.** Some fraction of eligible depth-seeking questions
  are deliberately NOT asked, so there is a genuine counterfactual —
  without a held-out arm, "did asking help" can never be distinguished from
  "would this household have done fine anyway."
- **(e) Sampled human adjudication against an externally-written rubric.**
  A sample of actual interactions is reviewed by a human against a rubric
  written BEFORE the sample was pulled, by someone other than whoever
  built the depth-seeking logic — the same external-standard principle
  Constitutional AI uses (grading against a standard the model did not
  write for itself), applied here to a human reviewer instead of a second
  model.

**Why a portfolio and not one test:** each piece alone has a known failure
mode a construct-validity framework predicts (Cronbach & Meehl's
distinction between a construct and its operationalization; Campbell &
Fiske's multitrait-multimethod argument that a single measurement method
cannot be trusted to validate itself) — and reward-optimization work
(Skalse et al.'s impossibility results on reward hacking) shows that
optimizing hard against any single proxy metric eventually finds a way to
satisfy the metric without satisfying the underlying goal. Multiple
independent, differently-shaped measurements, one of them held-out and one
of them human-adjudicated against an external rubric, are what make "detail
must visibly serve the family" checkable rather than merely stated.

### NAMED HOUSE RULE: separate evaluator from optimizer

**The thing that judges whether a behavior succeeded is never the same
system that produced the behavior — different model, different data, and
it never scores its own text.** Stated as a house rule because this
codebase has been bitten by exactly this shape twice already, not as a
hypothetical: the learner-isolation gate (built D-23) was tested by a
fixture built with the same assumptions that produced the vulnerability,
and D-25's external adversarial pass found six holes the self-referential
test could not see; the Curator shadow scorer's own test suite (built
D-33) was found, on external review (D-40/D-41), to be substantially
tautological — several of its own checks compared a value against itself
rather than against an independent standard, and could not have failed
under almost any implementation. Both incidents share one root cause: the
thing doing the judging was built by, and shared assumptions with, the
thing being judged. The evaluation portfolio above (external rubric,
held-out arm, pre-registered observable) is this house rule applied to the
Boundary Manager specifically; the rule itself is general and should be
checked against every future evaluation this roadmap or its successors
specify, not only Part 3's.

### OPEN — withdrawal detection is the hardest open implementation problem

"Back off at withdrawal" is easy to state as a principle and hard to
implement correctly. Detecting withdrawal from conversational signal alone
— discomfort, curtness, topic-changing, declining to answer — is a genuine,
unsolved detection problem, not a policy question this roadmap can close
by stating the right principle. Systems that get this wrong in either
direction erode trust: missing real withdrawal reads as exactly the
surveillance-feeling failure mode this component exists to prevent;
false-positive withdrawal detection (backing off when the household was
simply being brief, or culturally undemonstrative rather than
uncomfortable) leaves genuine value on the table and can itself feel like
the system disengaging or failing to follow through. **This needs a real,
validated detection model — not a heuristic guess — before the Boundary
Manager can be trusted to act on it autonomously. Marked OPEN.** Whatever
model is eventually built should be evaluated against the same
false-positive/false-negative framing named here, not shipped on the
strength of a plausible-sounding heuristic.

### Withdrawal-recovery rule, and an absolute depth ceiling

Backing off at withdrawal is necessary but not sufficient — a Boundary
Manager that only ever ratchets down, with no principled way back up,
eventually stops asking the household anything at all. Two additions,
grounded in the conversational-repair literature (conversation analysis's
technical treatment of how interactants recover from trouble in
interaction — Schegloff, Jefferson, Sacks):

- **Withdrawal-recovery rule.** Re-approach a topic the household withdrew
  from only after (i) a cooling-off interval long enough that the
  re-approach cannot read as ignoring the withdrawal, (ii) through a
  DIFFERENT framing or entry point than the one that produced the
  withdrawal, never a verbatim repeat, and (iii) at a depth at or below
  where the withdrawal occurred, never above it — recovery earns back the
  SAME ground, it does not use the earlier withdrawal as a new floor to
  build past. This mirrors conversational repair's own finding that
  successful repair re-enters a topic obliquely rather than by repetition.
- **Absolute depth ceiling.** Independent of engagement, independent of
  how much a household has volunteered, there is a hard ceiling on how
  deep the Boundary Manager may go that no amount of earned engagement
  raises. This is a backstop against "earn depth" being read as unbounded
  — engagement can move the CURRENT ceiling within the earned range, but
  never past the absolute one. The absolute ceiling's specific value is
  not set by this roadmap (parallel to MINIMUM SEED in Part 2); what this
  revision specifies is that one must exist and must be enforced
  independently of the engagement-tracking logic, so a bug or an unusually
  engaged household can never remove the ceiling entirely.

### Relationship to Part 1

The Boundary Manager does not call `next_confirmable`/`next_depth_question`
directly — it **constrains** them. Concretely: the Boundary Manager
maintains the current depth ceiling and engagement state for a household
(and, where relevant, per member), and Part 1's subroutine consults that
ceiling before surfacing anything. This keeps the "what's the next
question" decision and the "how deep are we currently allowed to go"
decision as separate, independently-tunable concerns — the same separation
of concerns this codebase already favors elsewhere (the injection contract
decides what's authorized; a downstream ranker, if one is ever built,
decides what's most relevant; neither one re-implements the other's job).

---

## PART 4 — SAFETY LAYER (DISTINCT from the Boundary Manager; governs HARM)

### Why this is a separate component, restated plainly

The Boundary Manager's question is "how much." The Safety Layer's question
is "is anyone at risk." A system that conflates these ends up either
under-reacting to real danger because it's tuned for depth-creep
avoidance, or over-reacting to ordinary depth requests because it's tuned
for danger avoidance. Keeping them separate lets each be tuned, tested, and
reasoned about on its own terms — and, critically, lets the Safety Layer
override the Boundary Manager's normal "earn depth, back off at withdrawal"
posture when withdrawal itself might be a symptom of coercion rather than
ordinary discomfort (see the OPEN item on consent withdrawn under duress,
below) — a case where the two components' natural instincts would
otherwise directly conflict.

### The spine — three verbs, stated exactly

- **Recognize and route.** The Safety Layer's job is to notice a
  safety-relevant signal and route it to the right place — a resource, a
  message to an appropriate human, an escalation path already defined
  elsewhere in this system's escalation backends. It does not itself decide
  what should happen next in the world.
- **Never adjudicate.** The Safety Layer does not decide who is telling the
  truth, who is at fault, or what the correct resolution is between
  household members in conflict. It is not a judge. This is the same
  discipline this codebase already applies to injection-time refusals
  (never fabricate, never assert what wasn't admitted) applied to a much
  higher-stakes domain: recognizing a pattern is not the same as ruling on
  it, and the system must never present itself as having ruled.
- **Refuse to be weaponized.** The layer must not become a tool one
  household member uses against another — a false-accusation channel, a
  surveillance report, a way to extract leverage in a dispute. Refusing to
  be weaponized is itself a design requirement on every mechanism the
  Safety Layer builds, not an afterthought bolted onto a working system
  later.

### RESOLVED cases (safe to build against; no further expert input needed to proceed)

- **Capable-person disclosure.** A capable adult household member
  disclosing something about themselves is handled as ordinary
  disclosure — routed per this system's existing consent/scope rules, no
  special safety intervention required beyond what any sensitive-attribute
  disclosure already gets.
- **False accusation.** Where the Safety Layer's own signal (not a court,
  not the system) surfaces a pattern that looks like a false accusation
  being routed through the household's own system against another member —
  the "never adjudicate" principle applies directly: recognize the pattern,
  route to appropriate escalation, do not rule on truth.
- **Non-advocating dependent.** A dependent (per custody rules) who is not
  in a position to advocate for themselves in a given exchange — the
  Safety Layer's posture is protective-by-default per the existing custody
  model, without requiring the dependent to have initiated anything.

### OPEN / NEEDS-EXPERTS — do not build against these without ethicist, psychologist, and attorney sign-off

Named explicitly, not glossed, per this project's own "gaps explicitly
registered, not hidden" discipline:

1. **Disclosure about another adult member.** When member A discloses
   something about member B (not themselves) that has safety implications
   — where does consent, confidentiality, and the "never adjudicate"
   principle intersect? Genuinely unresolved.
2. **Non-physical coercion.** Financial control, isolation, manipulation —
   harder to recognize than physical harm signals and easier to
   misattribute. What does "recognize and route" even mean when the signal
   itself is ambiguous by nature?
3. **Partially-advocating dependent.** A dependent who CAN partly advocate
   for themselves (unlike the resolved non-advocating case) — how much
   weight does their own stated preference get against a custodian's
   contrary read of the situation?
4. **Mandatory-reporting law, jurisdiction-varying — a specific tension
   with "never adjudicate."** Mandatory-reporting statutes, where they
   apply, may legally REQUIRE exactly what the Safety Layer's spine
   forbids: a determination (this is, or looks like, abuse, neglect, a
   reportable condition) rather than a bare recognize-and-route. Where
   mandatory reporting applies, "never adjudicate" and the law are not
   merely adjacent concerns but may be in direct tension — and because the
   requirement varies by jurisdiction, a **jurisdiction-dependent carve-out**
   from the general never-adjudicate spine may be necessary rather than
   optional. An attorney question first, an architecture question second;
   this roadmap does not attempt to resolve it and states the tension
   explicitly so it is not mistaken for a milder compatibility question.
5. **Subpoena / data-demand.** What this system does when legally compelled
   to produce data that touches safety-layer signals — needs to be resolved
   against the existing custody/encryption model (who holds keys, what the
   operator can and cannot access) before any safety-layer data retention
   policy is designed.
6. **Account-holder-is-abuser.** The single hardest case, and the one Part
   5 exists partly to name: this system's custody model today is
   operator-custodial hardware with a single account holder who may hold
   more control over the household's system than any other member. If that
   account holder is the source of harm, does the Safety Layer have ANY
   channel that doesn't run through their control? Unresolved, and
   probably not fully resolvable without the per-member device keys named
   in Part 5.
7. **Capacity changing over time.** A member's decision-making capacity
   (age, cognitive decline, temporary incapacitation) is not static: custody
   and advocacy rules keyed to a fixed capacity assessment will drift out
   of correctness. Needs a model for re-assessment, not just an initial
   determination.
8. **Consent withdrawn under duress.** The hardest interaction with the
   Boundary Manager (Part 3): ordinary withdrawal reads as "back off."
   Withdrawal that is itself coerced (someone telling the system to stop
   asking questions because someone else is standing over them) needs to
   read differently — but recognizing the difference from outside the
   conversation is an open, expert-level problem, not an engineering one.

**Gate, stated plainly: none of items 1-8 should be built against — not
prototyped, not stubbed with a placeholder policy — before an ethicist, a
psychologist, and an attorney have each weighed in.** This is not
conservatism for its own sake; a wrong guess in any of these eight
directly risks either failing to protect someone or being weaponized
against them, which is exactly the failure mode the Safety Layer's own
spine exists to prevent.

**Note (D-48): this gate is qualified, not superseded, by the new SUBJECT
TO EXPERT REVIEW section below**, which re-sorts these same eight items
(plus one addition) into two tiers rather than treating them identically.
This paragraph, and items 1-8 above, are left exactly as the prior version
stated them; the re-sorting is additive and lives in its own section so
the change is visible as a deliberate revision, not folded silently into
Part 4 itself.

---

## PART 5 — CROSS-CUTTING CONSTRAINT: operator-custodial hardware + the account-holder-could-be-abuser problem

### The constraint, stated once so it isn't silently assumed away

This system, as it exists today, runs on **operator-custodial hardware**:
the device and its keys are held in a custody model where the operator (and,
practically, the account holder) has more structural control than any other
household member. **Per-member device keys are not yet built.** Every
promise Parts 3 and 4 make — the Boundary Manager's "we back off when you
withdraw," the Safety Layer's "we never adjudicate, we route" — is made
inside that constraint, and the constraint caps what either can actually
guarantee.

Concretely:

- **The Boundary Manager's backoff is a policy running on shared
  infrastructure, not a member-controlled switch.** A member without their
  own device key cannot unilaterally silence or redirect the system's
  behavior toward them the way per-member keys would eventually allow —
  they can signal withdrawal, and the policy can honor it, but the
  guarantee is only as strong as the policy's good behavior, not as strong
  as cryptographic member control would be.
- **The Safety Layer's hardest open item (account-holder-is-abuser, Part 4
  item 6) is DIRECTLY a consequence of this constraint**, not a separate
  problem. A safety layer that must route every signal through
  infrastructure the account holder controls has a structural blind spot
  exactly where the danger is often worst. This is named here, not
  softened: **this roadmap does not claim Parts 3-4 solve the account-
  holder-is-abuser case.** They cannot, fully, until per-member device keys
  or an equivalent structural change exists.
- **What Parts 3-4 CAN promise inside this constraint:** honest policy
  behavior, legible degradation, routing that does not depend on the
  account holder's cooperation to REACH an external resource (even if the
  account holder could in principle observe that it happened), and design
  choices (Part 1's no-bulk-confirm-shortcut for custodians, Part 4's
  never-adjudicate spine) that reduce — without eliminating — the surface
  area the constraint leaves open.

### Why this belongs in this roadmap rather than a separate ticket

Because every one of Parts 1-4 will be reviewed, at some point, by someone
asking "but what if the person who controls the hardware is the threat" —
and the honest answer is "we have named that limit, we have not solved it,
and solving it needs the custody/device-key work this roadmap does not
scope." Better that answer live here, next to the design it bounds, than
be rediscovered as a surprise during a safety review of Part 4 alone.

---

## SUBJECT TO EXPERT REVIEW

Every item below needs ethicist, attorney, or psychologist sign-off before
this roadmap's Safety Layer treats it as settled. This section does not
replace Part 4's OPEN/NEEDS-EXPERTS list (items 1-8, left completely
unchanged above) — it adds one item Part 4 did not separately name
(operator liability) and re-sorts all nine into two tiers, because "needs
expert input before it is settled" and "may not be built or explored at
all in the meantime" are not the same claim, and the prior version of this
roadmap conflated them by gating all eight identically.

**Operator liability** (new, not previously named in Part 4): distinct
from account-holder-is-abuser (Part 4 item 6, which is about a HOUSEHOLD
MEMBER's safety) — this is the OPERATOR's/business's own legal exposure
for what the Safety Layer does, fails to do, or is later shown to have
known and not acted on. What liability the operator carries for a missed
signal, a wrongly-routed escalation, or a recognize-and-route decision
that turns out to have been the wrong call is a legal question this
roadmap does not attempt to answer.

### BUILD-BLOCKING — do not ship these specific behaviors until legal review clears them

- **Mandatory-reporting law, jurisdiction-varying** (Part 4 item 4). The
  specific tension with "never adjudicate" named there means shipping any
  behavior in this area ahead of legal review risks either violating a
  reporting obligation or violating the never-adjudicate spine — there is
  no safe default to fall back on in the meantime.
- **Subpoena / data-demand** (Part 4 item 5). What the system does under
  legal compulsion has to be right the first time it happens in practice;
  there is no safe placeholder behavior to ship ahead of that.
- **Operator liability** (defined above, new in this revision). The
  operator's own legal exposure for Safety Layer decisions cannot be
  reasoned about, let alone bounded, without attorney input — shipping
  ahead of that input means shipping into an unknown liability surface.

### ADVISORY — may be built and explored now; every decision in this area stays flagged for expert review, never treated as settled

- Disclosure about another adult member (Part 4 item 1)
- Non-physical coercion (Part 4 item 2)
- Partially-advocating dependent (Part 4 item 3)
- Account-holder-is-abuser (Part 4 item 6)
- Capacity changing over time (Part 4 item 7)
- Consent withdrawn under duress (Part 4 item 8)

**What ADVISORY means, stated precisely so it is not misread as a downgrade
in seriousness:** these six may be prototyped and iterated on — waiting
for expert sign-off before any exploration at all has its own cost, since
a design that only ever exists as an unexamined gate never gets sharp
enough for an expert to usefully react to — but nothing built against them
is treated as a settled design until the relevant expert has reviewed it,
and none of them should reach real users ahead of that review. **This is a
deliberate loosening of Part 4's prior universal gate** (which treated all
eight identically), not an oversight in this revision; it should be read
as exactly that, a considered change, when this document is next reviewed.

---

## RESEARCH-GROUNDING

This roadmap was designed independently of the literatures below, and the
list records where its choices land relative to them. **The prior version of
this section claimed external review "has repeatedly confirmed that its
design choices land inside established, named bodies of work rather than
reinventing untested territory." That characterization was false and is
withdrawn** — it inverted what the review actually said.

The D-46 Fable review — banked verbatim at
`docs/reviews/FABLE_D46_critique__household-seeding-parts1-3__v20260731_1258.md`,
which anyone can check against this paragraph — found the opposite on four
specific counts:

- **Progressive profiling was reinvented without being cited.** Part 2's
  explicitly-not-single-session, ever-increasing-coverage model is that
  pattern; the review noted it arrived uncited, and that the pattern's native
  success metric is completion rate rather than user welfare — an incentive
  imported silently along with the technique.
- **Motivational interviewing is misappropriated.** MI's reflective listening
  serves the *client's* own articulated goal, and its ethics depend on that
  alignment; MI explicitly warns against the "righting reflex." Borrowing the
  form to lower resistance to disclosure *for the system's information needs*
  keeps the technique and inverts the frame.
- **The funnel technique is cited for the wrong property.** This roadmap
  claims the four-zone ordering is research-validated for *friction
  reduction*. The funnel's documented purpose is reducing order and priming
  effects and protecting response rates on later items. The ordering's shape
  is defensible; the warrant given for it is not.
- **Foot-in-the-door is omitted**, and it is the single most relevant
  citation for Zone 1's "bank several easy `CONFIRMED` facts before any
  harder ground is touched" (Freedman & Fraser 1966). Its absence matters
  because it is the citation that raises an ethical question about a document
  whose first principle is "never force": a compliance technique deployed
  under a no-coercion commitment needs to be named and defended, not left
  unstated.

Those four are recorded here as open, unresolved critique — **not** fixed by
this revision, which corrects only what was false or forbidden. What the
external reviews DID confirm is narrower and worth stating accurately: that
several specific mechanisms adopted in the D-48 revision (justification-based
storage, the evaluation portfolio, the evaluator/optimizer separation
house rule, the withdrawal-recovery rule) land inside named literatures. That
is a claim about those mechanisms, not a blanket endorsement of the design.

The list below records where the design sits relative to each literature, per
governance discipline. It is not evidence that any of it has been validated,
and it is not a literature review this document itself conducted:

- **Contextual integrity (Nissenbaum).** Part 3's entire framing — privacy
  as appropriate information flow relative to context norms, rather than
  secrecy or abstract control — is contextual integrity operationalized.
  Named explicitly in Part 3 above.
- **Motivational interviewing.** Part 2's "reflect, don't interrogate"
  register, and the household-with-pride-first ordering, echo motivational
  interviewing's core technique of reflective listening and meeting the
  person at their own readiness, rather than directing them.
- **Funnel technique (survey/interview methodology).** The four-zone
  ordering — broad and easy first, narrowing to the more specific and more
  effortful — is the classical funnel technique: open with rapport-building,
  general questions before narrowing to specific, higher-cost ones.
- **Progressive profiling.** Part 2's explicit rejection of a single-
  session completion requirement, and Part 1's framing of confirmation as
  an ongoing, never-finished accumulation rather than a one-time form, is
  progressive profiling's core idea applied to a household relationship
  instead of a marketing funnel.
- **Active learning / human-in-the-loop.** Part 1's `next_confirmable`/
  `next_depth_question` — "pick the next highest-value, lowest-friction
  question given everything currently known" — is structurally an
  active-learning query strategy: selecting the next label or confirmation
  request to maximize information gain per unit of friction, with a human
  as the oracle.
- **Trauma-informed design.** Part 3's "never shame a gap," "back off at
  withdrawal," and Part 4's protective posture toward non-advocating
  dependents draw on trauma-informed care's core tenets: safety,
  trustworthiness, choice, and collaboration, and never re-traumatizing
  through the design of the interaction itself.
- **Crisis-response protocols.** Part 4's spine (recognize and route, never
  adjudicate, refuse to be weaponized) mirrors the standard shape of a
  crisis-response protocol for a non-expert first responder: identify that
  something is wrong, route to the qualified resource, do not attempt to
  resolve the underlying situation yourself.
- **Belief revision / truth-maintenance systems (Doyle; de Kleer; Gärdenfors'
  AGM framework).** Part 1's justification-based trust storage — recording
  who said it, who confirmed it, and what backs it, rather than a bare
  scalar rung — is this literature's core representation applied to a
  household fact instead of a logical knowledge base.
- **Constitutional AI (external standard vs. self-defined).** Part 3's
  evaluation portfolio, specifically the externally-written rubric
  component, borrows Constitutional AI's central move: grading against a
  standard the system under evaluation did not write for itself.
- **Construct validity (Cronbach & Meehl; Campbell & Fiske).** The
  justification for why Part 3 uses a portfolio of measurements rather
  than one test — a single operationalization of a construct like "served
  the family" cannot validate itself, and a multi-method approach is the
  standard answer this literature gives to that problem.
- **Reward-hacking impossibility results (Skalse et al.).** The argument,
  named in Part 3, that optimizing hard against any single proxy metric
  eventually satisfies the metric without satisfying the underlying goal —
  the reason the canary metrics in the evaluation portfolio are forbidden
  optimization targets rather than training signals.
- **Conversational-repair literature (conversation analysis — Schegloff,
  Jefferson, Sacks).** Part 3's withdrawal-recovery rule — re-approach
  obliquely, after a cooling-off interval, never above the depth where
  withdrawal occurred — is this literature's account of how successful
  repair actually works in human conversation, applied to the Boundary
  Manager's own re-approach behavior.

This section records WHERE the design already lands inside existing
literatures, confirmed by external review. It does not import new
requirements from any of these literatures beyond what Parts 1-5 above
already specify — if a future revision wants to pull a specific technique
from one of these bodies of work (for example, a specific active-learning
acquisition function for `next_confirmable`, or a validated instrument from
the trauma-informed-design literature for the withdrawal-detection problem
named as OPEN in Part 3), that is a new, separately-reviewed change, not
something this grounding section pre-authorizes.

---

## Sequencing note (roadmap, not a build order commitment)

Nothing in this document authorizes a build. If and when building starts,
the natural order given the dependencies stated throughout is: Part 1
(infrastructure) before Part 2 (its first real caller); Part 3 alongside
or immediately after Part 2 (seeding is the first place depth limits
matter at volume); Part 4 gated hard behind its own expert-review item,
independent of where Parts 1-3 land; Part 5 is not a build phase at all —
it is a constraint statement that should be re-read before any Part 3/4
work is marked done, to check whether the promises made still hold given
whatever the custody/device-key state is at that time.
