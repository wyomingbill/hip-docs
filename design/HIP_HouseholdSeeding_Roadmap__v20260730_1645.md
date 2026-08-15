# HIP_HouseholdSeeding_Roadmap — Design Roadmap for Household Seeding, Confirmation, and the Boundaries Around Both

Status: DESIGN-DRAFT
Branch: roadmap
Reconciled-Against: nothing built yet — this is a pre-spec design roadmap,
not an implementable architecture. No code exists for any of the five
parts below. Where this roadmap touches already-ratified HIP architecture —
trust ladder (ASSERTED/CONFIRMED/CORROBORATED), the injection contract,
partition custody, the write-rule table — the existing ratified design
controls; this document proposes how a NEW subsystem (confirmation,
seeding, boundaries, safety) sits on top of that ratified layer, not a
replacement for it.

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
- **Never dead-end.** A fact that cannot currently be confirmed (the
  confirmer isn't present, isn't a customer yet, is a dependent who cannot
  self-confirm) does not sit forever as a silent gap. The subroutine
  re-routes: to another eligible confirmer (a custodian, per the trust
  ladder's existing rules), to a later turn, to a lower-friction channel.
  "We don't know yet and haven't found the moment to ask" is a tracked
  state, not an untracked one.
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
- **`next_depth_question(household, member?) -> topic | None`** — the
  depth-seeking twin of `next_confirmable`, gated by the Boundary Manager
  (Part 3).

### Trust-ladder wiring (uses the existing ratified ladder; does not invent a new one)

- **Subject confirms their own fact → `CONFIRMED`.** Standard case, no
  change to existing rules.
- **Household agreement → `CORROBORATED`.** When a second household member
  independently affirms a fact already at `CONFIRMED` (not merely
  repeating it back, but asserting it as true from their own
  knowledge — the same corroboration standard the existing epistemic
  ladder already defines elsewhere), it is promoted to `CORROBORATED`.
  This roadmap does not change what `CORROBORATED` means; it specifies
  where in the seeding/steady-state flow that promotion opportunity is
  most likely to arise (Part 2's "people" zone, where household members
  describe each other).
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

### Open questions this part does not resolve

- The exact backoff/re-ask cadence for a declined or deferred confirmation
  (hours? days? tied to conversation volume rather than wall-clock time?).
- Whether `next_confirmable` and `next_depth_question` should be one
  unified priority queue or two separately-tunable ones that get merged at
  the last moment before a turn. (This roadmap's position, stated above, is
  that they are the same underlying decision; whether the implementation
  literalizes that as one function or two cooperating ones is open.)

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

Ordered deliberately, high-value-low-friction first:

1. **Household-with-pride.** Open with what the household is happy to
   describe unprompted: names, who lives here, pets, the shape of daily
   life. This zone exists to establish the conversational register (warm,
   curious, not clinical) and to bank several easy `CONFIRMED` facts before
   any harder ground is touched.
2. **People.** Who's who, relationships, roles — the zone most likely to
   produce `CORROBORATED` promotions (per Part 1) as the narrator describes
   other members who later confirm independently.
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
- Household-agreed → `CORROBORATED` (standard, most likely to fire in the
  "people" zone).
- Custodian confirms EVERY dependent fact deliberately, no bulk shortcut
  (standard, per Part 1's explicit design choice above) — restated here
  because seeding is the moment a custodian is most likely to be tempted
  to bulk-confirm a dependent's whole profile in one enthusiastic sitting,
  and the interview UX must not offer that shortcut even as a convenience.

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
- **Detail must visibly serve the family.** Every piece of depth the system
  seeks should be legibly in service of something the household can see
  the value of — a better answer, a more useful reminder, a genuinely
  relevant follow-up — never depth for its own sake, never data collection
  the household can't connect to a benefit. This is the test for whether a
  question belongs in the interview at all: can the system's own next turn
  make the value of having asked visible.
- **Sensitivity gates depth.** The more sensitive an attribute already is
  (per the existing sensitivity classification — `low`/`medium`/`high`/
  `critical`), the higher the engagement bar before the Boundary Manager
  will let the confirmation subroutine surface a question about it at all.
  This composes with `next_confirmable`'s existing job: sensitivity isn't
  a separate check bolted on afterward, it's an input the Boundary Manager
  gives the subroutine when deciding what's currently askable.

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
4. **Mandatory-reporting law, jurisdiction-varying.** Whether and how this
   system's recognize-and-route obligations intersect with legal
   mandatory-reporting requirements that differ by jurisdiction — an
   attorney question first, an architecture question second.
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
