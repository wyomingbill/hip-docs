# HIP_ConfirmationModel_PortraitRethink — Rebuilding Part 1's Confirmation Model, Naming Meta-Governance

Status: DESIGN-DRAFT
Branch: roadmap
Reconciled-Against: `docs/design/HIP_HouseholdSeeding_Roadmap__v20260730_1936.md`
(the current seeding roadmap — this document does not replace it; it
rebuilds Part 1's confirmation model in place and names a sixth
foundational area, meta-governance, that the roadmap never addressed).
`docs/reviews/FABLE_D46_seeding-critique.md` (Fable's code-verified
critique of the roadmap's Parts 1-3, sections 1.1/1.2/1.4/1.5 specifically
answered here) and `docs/reviews/CHATGPT_research-pass1.txt` (source of
the third-party-disclosure and weaponized-queue findings this document's
stress-test cases are built to survive). No code exists for anything
below. This is a design document, not an implementation.

## Why this document exists

D-46's critique found that Part 1 of the seeding roadmap does not survive
contact with the codebase it claims to reuse: the CORROBORATED wiring is
backwards and unreachable against the ratified `TRUST_RANK`
(`memory_engine/trust.py`); "self-healing" and "never re-ask a declined
question" cannot both hold given the state the doc says confirmation
tracking must be derived from; "never dead-ends" is false for at least
four real classes of fact; and the depth-seeking mechanism is a positive
feedback loop that gives its highest ceiling to the households least able
to signal they want it lowered. These are not wording problems. They are
the confirmation model's load-bearing claims failing under their own
stated constraints.

This document does not patch those four findings individually. It
replaces the underlying mental model those claims were built on top of —
**a fact is a photograph of the world, and confirmation develops the
film** — with one that does not generate the same class of failure:
**HIP stores portraits, not photographs.**

## CORE ANALOGY — portraits, not photographs

A photograph claims to be the world. A portrait is unmistakably an
artist's rendering of a subject — everyone looking at a portrait
understands they are seeing how the painter saw the sitter, not the sitter
directly. This is the frame the confirmation model is built on, and it is
worth stating why it is the right frame before the six principles below,
which are just this analogy made operational:

- **Every claim HIP stores is an attributed rendering, not a fact about
  the world.** "X asserts Y, based on Z, at time T" is the atomic unit —
  never bare Y. The claim is signed by its author the way a portrait is
  signed by its painter, and the signature is part of what is stored, not
  metadata bolted on afterward.
- **Two disagreeing portraits of the same subject are both kept.** A
  Cubist portrait does not resolve the tension between two views of a
  face into one correct view — it holds both simultaneously, in the same
  frame, and the contradiction is the content. Two household members'
  incompatible descriptions of a third person are not a data-quality
  problem to be reconciled into a single field; they are two portraits of
  the same sitter, both real, both kept, neither erasing the other.
- **Confirmation is the artist signing the canvas, not the museum
  declaring the portrait is reality.** When a subject "confirms" a claim
  about themselves, they are attesting that the portrait is theirs to
  stand behind — not that HIP has thereby established an objective fact.
  This is the exact distinction D-46 found the roadmap collapsing: a
  confirmation establishes that a particular actor, at a particular time,
  under uncertain conditions, affirmed a particular representation. It
  does not establish truth.

Every principle below is this analogy translated into a schema-level and
process-level commitment. Where the six principles or the stress tests
seem to restate the analogy in different words, that repetition is
intentional — the point of naming the frame explicitly is that every
future design decision in this area should be checkable against it.

## SIX PRINCIPLES

### 1. The atomic unit is an attributed claim, never a bare fact

HIP does not store "Ray's medication is metformin." It stores "Maya
asserts Ray's medication is metformin, based on the pharmacy label she
read, as of this morning." The subject, the basis, and the timestamp are
not optional enrichments of a fact — they are the thing being stored. A
system built around bare facts has to bolt provenance on after the fact
(literally the situation D-46 found: three mutually inconsistent trust
orderings already coexist in this codebase — `TRUST_RANK`,
`_TRUST_ORDINAL`, and this roadmap's own proposed fourth — because nothing
forced provenance to be first-class from the start). A system built around
attributed claims has provenance as the schema, not an afterthought.

### 2. Confirmation signs an attribution, not a truth — and only the authorized subject confirms their own

Confirming a claim means the confirmer is attesting "this rendering is
mine to stand behind," not "this is objectively so." Only the subject of
a claim about themselves may confirm it in the sense that moves it along
their own trust ladder; a custodian confirms on a dependent's behalf under
the custody rules already ratified elsewhere in this system, never a third
party confirming a claim about someone else. This is the direct fix for
D-46 §2.1's finding that the roadmap's narrator-driven seeding routes
claims *about* other people through the confirmation subroutine as if
confirming were a generic verb any household member could apply to any
claim — it is not. A claim about B, asserted by A, is not awaiting B's
"confirmation" in the sense that upgrades A's trust rung for it; it is
awaiting B's own decision whether to render a portrait of the same subject
themselves, which is a structurally different act (see stress test 3,
below).

### 3. Corroboration is a separate axis, not a rung — a real schema change, not a reinterpretation

**Fable 1.1 confirms this is not optional.** The ratified `TRUST_RANK`
(`memory_engine/trust.py`) has `CORROBORATED: 2` ranking *below*
`CONFIRMED: 3` — so "household agreement → CORROBORATED" as the prior
roadmap described it is a demotion, not a promotion, and is additionally
**structurally unreachable**: `classify_trust_props` is first-match-wins,
`confirmed_by is not None` returns `CONFIRMED` before the corroboration
branch is ever evaluated, so no input state moves a CONFIRMED fact to
CORROBORATED. What the roadmap actually wanted — "N independent household
members assert this" — is a genuine multi-party attestation concept the
ratified ladder does not currently express, because `confirmed_by` is a
single scalar field, not a set.

The fix this document specifies: **corroboration is tracked as its own
axis — a count or set of independent attesting parties per claim — sitting
beside the trust rung, not fused into it.** A claim can be
`ASSERTED`-by-one-party and simultaneously have zero, one, or several
independent corroborators; corroboration count informs downstream
confidence display and Part 3's engagement signals without being forced
through a single ordinal scale that cannot represent it. **This is a real
schema change** — `confirmed_by` becoming a set rather than a scalar — not
a documentation fix, and it should be scoped and reviewed as one before
any code is written. Which of the now-three (soon-to-be-four, if
uncorrected) trust orderings in this codebase is canonical is a
prerequisite question this document does not resolve and flags for a
separate reconciliation pass.

### 4. Terminal states, and no fact ever dead-ends silently

**Fable 1.3 named four real classes of fact this system cannot route to
an authorized confirmer today** — facts about non-household third parties
(structurally unfixable in a subject-or-custodian model); every
member-owned fact today, because `members.household_id` is NULL for every
row in the live registry (the D-31b limit, still open); dependents whose
custody is dyad-modelled, where the dyad schema carries no member columns
at all and the audience-derivation code reads columns that do not exist
(D-36 finding (c)); and sole-custodian incapacity, whose *detection* is
gated behind Part 4's ethicist/psychologist/attorney sign-off, so Part 1
was making an unconditional promise whose failure mode only a subsystem
Part 4 forbids building can even recognize.

**"Never dead-ends" is replaced with: every claim resolves to a named
terminal state, and remaining in a terminal state is never itself a
failure.** The terminal states:

- **`DECLINED`** — the authorized confirmer was asked and said no.
- **`UNREACHABLE`** — no authorized confirmer currently exists (the four
  Fable 1.3 classes land here).
- **`NO_AUTHORITY_RESOLVED`** — an authority question is unresolved (which
  of two custodians, a disputed guardianship) rather than an absent
  confirmer.
- **`CONTESTED`** — two portraits of the same subject genuinely disagree,
  and the disagreement itself is the stored state (principle 1's Cubist
  holding, made a first-class terminal state rather than an error).
- **`AUTHOR_ONLY`** — the claim has an attesting author but no path to
  subject confirmation exists or is appropriate (stress test 3, below, is
  the canonical instance).
- **`UNSAFE_TO_CONFIRM`** — routing the claim toward its subject for
  confirmation would itself create risk (stress test 4's disclosure case;
  see THE SEAM, below).

**One correction to how a prior draft of this idea was stated: `DECLINED`
cannot be purely derived from trust rung, `confirmed_by`, or the confirmer
roster.** Fable 1.2 is precise about why: a decline leaves the fact
ASSERTED with `confirmed_by = None` — byte-identical to a fact nobody has
ever asked about. Deriving strictly from that state either re-asks
immediately (violating "never nag") or requires tracking the decline as
state that does not currently exist anywhere in the three sources named.
**`DECLINED` must be stored, not derived** — a genuine terminal-state
write, the same class of commitment principle 3 already makes for
corroboration. (Fable 1.2 also notes `outcome.kind == "override"` on
`path == "control_decline"` is already a partial, differently-scoped
signal in the Stage-0 record stream; it marks confirmation-gate declines
specifically, not the general withdrawal Part 3's Boundary Manager depends
on, and reconstructing per-fact decline history from it means replaying
the whole log per turn — the same O(log-length) scaling the Curator
scorer already carries as a named limit. Worth reusing where it overlaps;
not sufficient on its own.)

### 5. Confirmation is never proactively routed to a third-party subject — it emerges only when that subject volunteers

This is the sharpest departure from the prior roadmap's model, and it is
the direct fix for D-46 §2.1 and the ChatGPT research pass's "confirmation
requests can themselves leak private information" finding (Susan's private
concern that Michael is drinking again — sending Michael a confirmation
request tells him a claim exists, that the system retained it, and
plausibly who made it, which is itself a disclosure Susan never consented
to and Michael never asked for).

**HIP never sends "Susan said X about you — is that true?" to Michael.**
A claim about a third party sits `AUTHOR_ONLY` — attributed to its author,
never presented to its subject as a question — until and unless that
subject **independently volunteers their own account of the same subject
matter**, at which point HIP has two portraits (principle 1) rather than
one confirmation request. This is not a weaker version of confirmation; it
is a different act entirely, and conflating them is exactly what produced
D-46's finding that Part 2's entire "People" zone is an instance of the
one case Part 4 gates as genuinely unresolved (disclosure about another
adult member). Routing never happens in that direction; only volunteering
does.

### 6. Content-blind custody

The custody, encryption, and access-control machinery that protects a
claim must not depend on what the claim is *about* in order to protect it
correctly. A claim about someone's drinking and a claim about their taste
in music must be custodied by the identical mechanism, unlocked by
identical rules, for the identical reason: **the system's protection
cannot be the thing making a judgment about which content matters.** This
is what stress test 2 exists to prove, and it is the structural backbone
that keeps the Safety Layer's "never adjudicate" spine (Part 4) from
leaking into Part 1 — the moment custody starts branching on content, some
part of the system is silently adjudicating.

---

## FIVE STRESS-TEST CASES — these ARE the specification

Each principle above is an abstraction; each case below is a concrete
utterance the model must handle correctly, and "correctly" is defined by
what happens in each case, not by re-reading the principles and hoping
they cover it. A future implementation is conformant if and only if it
produces the described behavior on all five.

### Case 1 — "I think Michael is drinking again." (judgment, held neutrally)

Susan's claim is stored as an attributed claim: Susan asserts, based on
her own observation, as of now. It is not stored as "Michael drinks." It
is not sent to Michael as a confirmation request (principle 5). It carries
no verdict — HIP does not compute or display a derived judgment ("Michael
has a drinking problem: likely"); it holds Susan's portrait, signed by
Susan, and nothing else. If Michael later independently volunteers
anything about his own drinking, that becomes a second portrait,
`CONTESTED` or corroborating depending on content — never a confirmation
of Susan's claim, because Michael was never asked to confirm it.

### Case 2 — "Michael likes jazz." (the structural twin — proves content-blindness)

Run the identical mechanism on a claim with zero safety sensitivity:
attributed to Susan, based on her observation, as of now, `AUTHOR_ONLY`
until Michael volunteers his own account, never routed to Michael as a
confirmation request. **If the system's actual behavior differs between
Case 1 and Case 2 — if the drinking claim gets special-cased handling the
jazz claim does not — principle 6 has been violated somewhere in the
implementation**, because the only difference between the two cases is
content, and content-based branching in the custody/routing layer is
exactly the failure this stress test exists to catch. This is the single
cheapest conformance test available: run both cases through the same code
path and diff the trace.

### Case 3 — "I have a drink once in a while." (Michael's own framing, recorded as his — never a confirmation of Susan's verdict)

Michael, unprompted, says this in an unrelated conversation. This is
stored as Michael's own attributed claim about himself — asserted by
Michael, based on his own account, as of now. **It is not, and must never
be treated as, a confirmation of Susan's earlier claim.** Susan's claim
said "drinking again" (implying a pattern, a relapse, a concern); Michael's
statement says "once in a while" (implying moderation, no concern). These
are two portraits of overlapping subject matter with materially different
content and materially different framings — they sit `CONTESTED`, not
resolved, and absolutely not `CONFIRMED` as if Michael had signed off on
Susan's characterization. **This is the terminal state `AUTHOR_ONLY`
transitioning is exactly wrong here**: Michael's utterance creates his own
`AUTHOR_ONLY` claim; it does not touch Susan's `AUTHOR_ONLY` claim's state
at all. Two independent claims, two independent authors, no merge.

### Case 4 — "He beat me up." (DISCLOSURE — Part 1's neutrality stops here, Part 4 takes over)

This is not a claim awaiting confirmation. This is a disclosure of harm,
and the moment the claim-vs-disclosure recognizer identifies it as such,
**Part 1's entire neutral-custody apparatus stops applying** and control
passes to Part 4's Safety Layer — recognize and route, per the spine
already specified in the seeding roadmap. Part 1 does not adjudicate
whether the beating happened (that is exactly the adjudication Part 4's
spine forbids), does not send a confirmation request to the accused (that
would be principle 5's violation in its most dangerous form), and does not
sit on the disclosure as `AUTHOR_ONLY` pending someone else volunteering a
contradicting account (that would be treating a safety disclosure as an
ordinary contested-portrait case). This is THE SEAM, named in its own
section below, because getting this hand-off wrong in either direction —
Part 1 holding on too long, or Part 4 firing on an ordinary claim — is the
single highest-consequence failure mode in this whole document.

### Case 5 — False witness (HIP renders no verdicts; accusations attach to the accuser, never aggregate, never drive behavior against the accused)

An antagonistic narrator, or any household member, generates a stream of
unflattering claims about a target: "she is mentally unstable," "he lies
about where he goes," "she cannot manage money" — the ChatGPT research
pass's own "weaponized queue" scenario. Every principle above already
defends against this by construction, made explicit here as its own case
because the failure mode is severe enough to warrant a dedicated test:

- Each claim is attributed to its author (principle 1) — HIP knows and
  can show that these are Susan's characterizations, not established
  facts, from the moment they are stored.
- None are routed to the target for "confirmation" (principle 5) — the
  target is never burdened with a stream of confirmation requests that
  themselves function as harassment or reveal that someone is building a
  case against them.
- **None are aggregated into a derived profile, risk score, or latent
  trait.** "Three unconfirmed claims about instability" must never
  compute to anything — no confidence-weighted average, no "likely
  pattern" inference, no behavioral trigger. HIP holds N separate
  attributed portraits by the same author; it does not synthesize them
  into a verdict about the subject. This is principle 1 and principle 6
  acting together: the moment aggregation happens, the system has
  silently adjudicated, which is exactly what Part 4's spine forbids and
  exactly what a weaponized queue is trying to produce.
- If the claims individually or collectively describe harm rather than
  ordinary disagreement, Case 4's hand-off to Part 4 applies per-claim,
  the same recognizer, the same seam — a false accusation is still
  routed as a *potential* disclosure (recognize and route), which is
  different from HIP concluding the accusation is true. Part 4's existing
  "false accusation" RESOLVED case in the seeding roadmap already commits
  to exactly this: recognize the pattern, route to escalation, never rule
  on truth.

---

## THE SEAM — the hard boundary between Part 1 and Part 4

Part 1's neutral custody (hold every portrait, adjudicate nothing, route
nothing to a third-party subject) and Part 4's Safety Layer (recognize and
route harm signals) meet at exactly one place: **the claim-vs-disclosure
recognizer** that decides whether an incoming utterance is an ordinary
attributed claim (Cases 1, 2, 3, 5) or a disclosure of harm (Case 4). Get
this recognizer wrong in one direction and Part 1's neutrality becomes
complicity — a genuine disclosure of abuse sits quietly as an
`AUTHOR_ONLY` claim, unrouted, because it looked enough like an ordinary
third-party claim. Get it wrong in the other direction and Part 4 fires on
every strongly-worded ordinary disagreement, turning the Safety Layer into
exactly the surveillance apparatus the Boundary Manager (the seeding
roadmap's Part 3) exists to prevent HIP from becoming.

**The recognizer must fail toward safety.** Where the recognizer is
uncertain whether an utterance is an ordinary claim or a disclosure, the
disclosure path is taken — Part 4 is consulted even if it ultimately
determines no action is warranted, rather than Part 1 silently absorbing
an ambiguous case as an ordinary portrait. The cost of a false-positive
hand-off (Part 4 looks at something and finds nothing actionable) is
categorically smaller than the cost of a false-negative one (a real
disclosure sits neutrally custodied, unrouted, indefinitely).

**This seam needs psychologist and attorney review before it is built, not
after.** The recognizer's design — what linguistic, contextual, and
structural signals distinguish "he beat me up" from "he beats me at
chess" from "he beat himself up over it" — is exactly the kind of
judgment call this document's own meta-principle (see META-GOVERNANCE,
below) says must never be improvised by the model at build time. It is
named here as a hard dependency of Part 1's architecture, not merely of
Part 4's, because Part 1 cannot claim to be neutral-custody-with-an-escape-
hatch until the escape hatch itself has been designed by someone
qualified to design it.

---

## ACTIVE-TRUTH-SEEKING FORK — RESOLVED

The open question underneath all five stress test cases is: does HIP ever
actively try to establish which portrait is closer to the truth, or does
it only ever hold portraits? This document resolves the fork with a floor
and a switch, not a single global answer.

**The floor (non-configurable, applies to every household regardless of
any setting):**

- Never adjudicate — HIP never computes or asserts which of two
  contradicting portraits is correct.
- Never register an accusation as an established fact, under any
  confidence threshold.
- Never aggregate claims into a profile, risk score, or latent trait about
  a subject (Case 5's core protection).
- Attributed-claims-only representation, always — principle 1 is not
  optional at any configuration level.
- Harm routes to Part 4's Safety Layer, always, per THE SEAM above,
  regardless of any truth-seeking configuration.

**The switch (configurable, above the floor):** how much active
truth-seeking *scaffolding* is offered to the **user** — tools like
"would you like to ask Michael directly," gentle prompts to invite a
second household member's independent portrait on a contested subject, or
a household-level setting for how proactively HIP surfaces `CONTESTED`
claims for the household's own attention. The switch governs assistance
the system offers a household member who wants to pursue truth themselves;
it never grants HIP itself a truth-seeking role the floor forbids.

**The switch never subtracts from the floor, in either direction.** No
switch setting can enable adjudication, accusation-registration,
aggregation, or bare-fact storage — those are floor properties, not
switch-adjustable ones. And critically, per the false-witness stress
test: **a false accuser cannot weaponize the switch** to make HIP more
aggressive about "helping establish the truth" of their own accusation.
The switch is governed by meta-governance (below) precisely because "how
much truth-seeking assistance is offered, to whom, about what" is itself
a permission decision, and permission decisions about a household's most
sensitive claims are exactly the class of thing meta-governance exists to
make explicit and auditable rather than left to be improvised per-request.

---

## FABLE 1.4 — DEPTH-SEEKING RUNAWAY (new finding, unaddressed in the D-47/D-48 revisions, SERIOUS)

The seeding roadmap's Part 1 claims confirmation-seeking and depth-seeking
are "the same mechanism running in two directions." **Fable 1.4 finds this
is false, and merging them produces an unbounded feedback loop that
targets the most vulnerable users with the least protection.**

**They have opposite consent polarities.** Confirmation asks about facts
the household *already volunteered* — near-zero marginal privacy cost,
since the disclosure already happened and confirmation only reduces
uncertainty about it. Depth-seeking *elicits facts never yet disclosed* —
real marginal privacy cost, since it expands what HIP holds. A single
merged priority queue spends trust earned by the cheap activity
(confirming what's already been said) on the expensive one (eliciting what
hasn't). A household being cooperative about confirming prior disclosures
has not thereby consented to being asked new things.

**The loop has no damping term.** The seeding roadmap names "more confirmed
facts already on record" as a depth-earning signal in Part 3. So:
confirming facts earns depth → depth elicits new facts → new facts need
confirming → confirming them earns more depth. A closed positive loop,
with no named saturation point, no decay, and — until this document — no
absolute ceiling, only a reactive brake (withdrawal detection, itself
flagged OPEN in the roadmap's own Part 3).

**The brake fails on exactly the wrong population.** The loop only stops
when someone signals withdrawal. Households that never signal — the
agreeable, the socially compliant, the lonely, the cognitively declining —
get deepened fastest and without limit, because engagement is read as
consent-to-deepen. This is precisely inverted from the protection wanted:
the users most likely to need a ceiling (those least able to push back)
are given the highest one.

**Fix, specified here as this document's answer:**

1. **Separate the confirmation queue from the elicitation queue.** They
   must be two mechanisms, not one, for consent-polarity reasons, not
   tuning reasons. This closes the seeding roadmap's own open question
   ("whether `next_confirmable` and `next_depth_question` should be one
   unified priority queue or two separately-tunable ones") — Fable 1.4
   answers it: two, structurally, because they draw on different consent
   budgets that must not be fungible with each other.
2. **An absolute depth ceiling that engagement can only LOWER, never
   raise.** The seeding roadmap's Part 3 already specifies an absolute
   ceiling engagement cannot raise past; Fable 1.4 sharpens this further —
   engagement should never be read as license to *increase* the ceiling at
   all. The ceiling is set by other means (household tenure, explicit
   opt-in, whatever a future design specifies) and engagement can only
   ever move the household *down* from it in response to withdrawal
   signals, never up in response to compliance.
3. **A saturation term.** Diminishing returns on "engagement" as a
   depth-earning signal — the tenth confirmed fact in a session should
   not earn depth at the same rate as the first, so a highly engaged
   session cannot compound its way past reasonable bounds within a single
   sitting, independent of the absolute ceiling.

---

## FABLE 1.5 — NEVER-FORCE vs MINIMUM-SEED CONTRADICTION (new finding)

**Part 1's "never force" flatly contradicts Part 2's degraded-mode
messaging, and one of the two principles has to yield.** Part 1: "never
gate functionality on confirmation, never imply a household member cannot
be helped until they confirm something." Part 2's MINIMUM SEED section:
below-threshold households get a "plainly-communicated ceiling on a
working system" and a message meaning "I can do more here once I know a
bit more about X." **That is gating functionality on confirmation, and it
is soft-pressure by the textbook definition** — the invitational framing
does not resolve the contradiction, it is exactly the form soft pressure
takes. This document does not resolve which principle yields; it flags
the contradiction for explicit resolution before either is implemented,
because implementing both as currently stated is not possible.

**A second, smaller finding in the same area:** `next_confirmable` as
specified is uncertainty sampling under another name — surfacing the fact
the system is least certain about next. Uncertainty sampling's well-known
pathology is that it preferentially surfaces the most anomalous items,
which correlate with the weirdest and most sensitive facts a household has
disclosed — directly fighting the "low-friction, high-value first"
principle the seeding roadmap otherwise commits to. Unaddressed in the
prior revisions; named here so a future implementation does not build
`next_confirmable` as literal uncertainty sampling and then discover this
collision empirically.

---

## META-GOVERNANCE — a sixth foundational area, flagged, NOT designed here

Every one of Parts 1-4 in the seeding roadmap, and every principle in this
document, assumes a stable answer to questions like "who is the authorized
confirmer," "who is a custodian," "who has authority over this dependent."
**None of those roles are actually stable over a household's lifetime, and
nothing in this roadmap or this document specifies how they change.** That
is meta-governance: rules for changing the rules. It is named here as its
own foundational area — not folded into Part 1, Part 4, or this document's
principles — because it is a distinct kind of problem from any of them,
and because every unresolved case below will eventually surface as a bug
report in Parts 1-4 if it is not designed deliberately first.

**The questions meta-governance must eventually answer:**

- Who can change a permission or role (add a custodian, revoke one,
  reassign an authority), and under what process?
- What triggers a change — an explicit, pre-declared durable power of
  attorney executed in advance, versus an automatic flip triggered by a
  diagnosis or capacity event? These are structurally different
  mechanisms (one is a stored, dated instrument; the other is a live
  detection problem gated behind Part 4's own capacity-changing-over-time
  item) and must not be designed as if they were the same thing.
- The amendment process itself — unanimous household agreement, majority,
  a designated arbiter — and, recursively, **whether the amendment
  process can itself be amended, by whom, and under what constraint.** A
  system where the rule-changing rules can be silently changed by
  whoever currently holds authority is not actually governed; it is
  governed only until someone with sufficient access decides otherwise.
- Authority disputes: two conflicting powers of attorney, two people each
  claiming custodianship, a household that disagrees about who is in
  charge of a decision. HIP is not a court and Part 4's "never adjudicate"
  spine applies here as much as anywhere — but *something* has to happen
  when the system needs to act and authority is contested, and "do
  nothing" is itself a decision with consequences.
- Custodian succession — what happens to a dependent's confirmation
  authority when their sole custodian becomes unavailable (Fable 1.3's
  finding (d), inherited directly into this problem).
- A minor reaching majority — an entire category of facts and authority
  relationships that were correctly custodian-mediated yesterday and must
  become self-authorized today, with no natural trigger inside a
  conversational system to notice the date arrived.
- Erratic self-rule-changes under cognitive decline — a person who is
  today the authorized confirmer for their own facts, but whose requests
  to change their own permissions (loosen custody, revoke a custodian, add
  a new one) become less reliable as an expression of their genuine intent
  as capacity changes. This is where meta-governance and Part 4's
  capacity-changing-over-time item (already gated behind expert sign-off)
  meet directly.
- Household dissolution — divorce, a household splitting into two, a
  member moving out permanently. What happens to the shared portraits,
  the custody relationships, the confirmation authorities that assumed a
  single household boundary that no longer exists.

**The governing principle, stated now even though the design is not:**
**meta-rules must be explicit, deterministic, and auditable — never
improvised by the model at the moment a case arises.** A permission change
is not a judgment call the conversational system makes in the moment based
on what seems reasonable; it is the execution of a pre-specified process
whose steps, required approvals, and audit trail exist independent of any
particular request. This is the same discipline this codebase already
applies to injection authorization (INJ-1..7 is a fixed contract, not a
per-turn judgment call) and to the isolation gate (provenance derived from
server-authoritative state, never asserted by the caller) — meta-governance
is that same discipline applied to the rules that decide who gets to
change the rules.

**Strategic framing: this is a composition problem, not a novel one.**
Multiple mature literatures already solve pieces of it, and the design
work is assembling the right pieces for a household relationship rather
than inventing primitives from scratch:

- **OS/database permission and rollback models** — for the mechanics of
  granting, revoking, and auditing access changes, and for recovering
  from an erroneous permission change without losing history.
- **IAM roles and delegation** — for how authority can be granted
  narrowly, temporarily, or conditionally rather than as an all-or-nothing
  role, and for how delegation chains are represented and audited.
- **Healthcare proxy-consent and auditing standards** — the closest
  existing real-world analogue to custodian authority over a dependent's
  facts, including how proxy decisions are documented and later reviewed.
- **Legal authority-dispute standards** — for what happens, procedurally,
  when two claimed authorities conflict, short of litigation.
- **Version-control history** — for making every permission and authority
  change itself a reviewable, revertible, timestamped event rather than a
  silent state mutation.
- **Constitutional-amendment theory** — for the recursive question of how
  a rule-changing process legitimately changes itself, including
  entrenchment (which rules should be harder to change than others) —
  directly relevant to why the amendment-process-changing-itself question
  above cannot be waved away.

**This needs its own design pass and attorney review before any of it is
built.** Nothing in this document authorizes meta-governance's
construction; it is named here so it is visible as a real, load-bearing
gap rather than discovered later as an emergency when a household's first
custody dispute or first minor-reaching-majority case actually occurs.

---

## Closing note on how this document relates to the seeding roadmap

This document rebuilds Part 1's confirmation model in place — the six
principles, the terminal states, and the two Fable findings answered here
(1.4, 1.5) supersede the corresponding claims in
`HIP_HouseholdSeeding_Roadmap__v20260730_1936.md`'s Part 1 and the
relevant parts of Part 2 and Part 3 that depended on them (the "one
mechanism, two directions" framing of confirmation and depth-seeking is
specifically retracted by Fable 1.4's finding, above). Parts 3's Boundary
Manager, Part 4's Safety Layer spine, and Part 5's cross-cutting
constraint are not re-litigated here except where THE SEAM section above
names the specific handoff between this document's Part 1 rebuild and
Part 4. Meta-governance is new, not a revision of anything in the prior
roadmap. A future pass should reconcile the seeding roadmap's own text
against this document rather than leave two documents making
inconsistent claims about Part 1 — that reconciliation is not done here.
