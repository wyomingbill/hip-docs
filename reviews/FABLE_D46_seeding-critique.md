# D-46 — Fable design critique: HIP_HouseholdSeeding_Roadmap, Parts 1–3

Gate: PASSED (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap).
Read-only. No lock taken. No design changed. No status proposed.
Doc reviewed: `docs/design/HIP_HouseholdSeeding_Roadmap__v20260730_1645.md` (536 lines), at HEAD 73ffadc.
Parts 4 and 5 deliberately NOT critiqued, per dispatch — except where Parts 1–3 depend on them.

Claims marked **[code-verified]** were checked against the repo this session.

---

## THE HEADLINE

Three findings would each individually block a build. In severity order:

1. **The CORROBORATED wiring is backwards, and the transition it specifies is
   structurally unreachable.** Part 1 claims to use the ratified ladder
   unchanged. It does not. **[code-verified]**
2. **"Self-healing" and "never re-ask a declined question" are in direct
   contradiction**, given the doc's own constraint that state be re-derivable.
   One of the two has to go.
3. **The depth mechanism is a positive feedback loop with no damping term, and
   its only brake selects against the users who most need it.**

Everything else below is real but subordinate to those.

---

## PART 1 — THE CONFIRMATION SUBROUTINE

### 1.1 The CORROBORATED promotion is a demotion, and it cannot fire **[code-verified]**

The doc states:

> "**Household agreement → `CORROBORATED`.** When a second household member
> independently affirms a fact already at `CONFIRMED` ... it is promoted to
> `CORROBORATED`. This roadmap does not change what `CORROBORATED` means."

Every clause of that is wrong against the ratified ladder in
`memory_engine/trust.py`:

```python
TRUST_RANK = {"CONFIRMED": 3, "CORROBORATED": 2, "ASSERTED": 1,
              "UNCONFIRMED": 0, "DERIVED": 0, "UNKNOWN": 0}
```

- **It is a demotion, not a promotion.** CORROBORATED (2) ranks *below*
  CONFIRMED (3). The doc's "promotion" moves a fact DOWN the ratified ladder.
- **It is structurally unreachable.** `classify_trust_props` is documented
  first-match-wins: `if confirmed_by is not None: return "CONFIRMED"` is
  evaluated *before* the CORROBORATED branch. Once a fact is CONFIRMED,
  `confirmed_by` is set, and the CORROBORATED branch is permanently shadowed.
  There is no input for which a CONFIRMED fact reclassifies as CORROBORATED.
- **It does change what CORROBORATED means.** In the ratified ladder,
  CORROBORATED is `confidence == "high" and _has_harden_transition(...)` — a
  **confidence-hardening event sourced from `reconcile`**, i.e. a
  consolidation/reconciliation signal. It has nothing to do with a second
  household member agreeing. The doc silently substitutes a *social* semantic
  for a *reconciliation* semantic and asserts it is the same thing.

This is not a wording nit. Part 2 builds an entire interview zone (Zone 2,
"People") around maximizing a state transition that cannot occur, and cites it
as that zone's primary justification. **Zone 2's stated purpose evaporates.**

Compounding: the codebase already carries a *third*, separately inconsistent
trust encoding — `curator_shadow._TRUST_ORDINAL` has `DERIVED: 1.0` above
`CONFIRMED: 0.9`, while `TRUST_RANK` puts `DERIVED` at **0**. So there are
already two mutually contradictory trust orderings in tree, and this roadmap
proposes a fourth semantic on top. Whatever else happens, someone needs to
declare which ordering is canonical before a fourth consumer is built.

**What the doc probably wants** is a genuine multi-party attestation concept —
"N independent household members assert this" — which the ratified ladder
does **not** currently express, since `confirmed_by` is a single scalar field
**[code-verified]**, not a set. That is a real schema extension, not a
"uses the existing ratified ladder; does not invent a new one" claim.

### 1.2 "Self-healing" contradicts "never re-ask a declined question"

The doc makes two requirements that cannot both hold:

> "whatever data structure represents 'this fact is awaiting confirmation from
> X' must be **re-derivable from state that already exists** (the trust ladder
> rung, the fact's `confirmed_by`/`write_state`, the roster of eligible
> confirmers) rather than a side-channel flag that can itself get stuck."

> "must never re-surface a fact the confirmer has already declined within some
> backoff window."

A decline leaves **no trace** in any of the three named sources. The fact stays
ASSERTED with `confirmed_by = None` — byte-identical to a fact nobody has ever
been asked about. Trust rung, `confirmed_by`, `write_state`, and the confirmer
roster are all unchanged by a decline. So:

- Derive strictly from existing state → the decline is invisible → the system
  re-asks immediately, violating "never re-ask" and, worse, violating "never
  force" by nagging.
- Track declines → you have exactly the "side-channel flag that can itself get
  stuck" the doc forbids.

There is a third path the doc doesn't take but should consider: declines are
*already* partially observable in the Stage-0 record stream —
`outcome.kind == "override"` fires on `path == "control_decline"`
**[code-verified]**. That makes decline history re-derivable from the record
log rather than a flag. Two problems with relying on it as written: (a) that
signal marks a *confirmation-gate* decline specifically, not the general
"declined to answer / changed the subject" withdrawal Part 3 depends on; and
(b) reconstructing per-fact decline history means replaying the whole log per
turn, which is the same O(entire-log)-per-turn scaling the Curator scorer
already carries as a named limit. Workable, but it needs saying, and the doc's
current three-source list is simply insufficient.

### 1.3 "Never dead-ends" — four facts that can never reach an authorized confirmer

The dispatch asked me to name one. There are four classes, two of them live today.

**(a) Facts about non-household third parties — structural, unfixable within
this model.** The confirmer model is subject-or-custodian. HIP records facts
whose subject is not a household member at all (a neighbour, an estranged
relative, a member's doctor); the injection contract's whole INJ-1 subject-scope
machinery exists because such facts exist **[code-verified]**. Neither the
subject (not a user) nor any custodian (no custody relationship) is an
authorized confirmer. These facts are permanently unconfirmable **by
construction**, and no re-routing helps. The doc's "never dead-end" is false as
an unconditional claim; it holds only for facts about enrolled members.

**(b) Every member-owned fact, today. [code-verified]** The doc mandates that
`eligible_confirmers` derive from server-authoritative state, "never asserted by
the caller," explicitly mirroring the isolation gate. Applied honestly, that
mandate currently returns nothing: `members.household_id` is **NULL for all five
rows** in the live registry (`bill`, `maya`, `sam`, `p4smoke_x`, `p4smoke_y`) —
the D-31b named limit, still open. Derivation of household scope for
member-owned facts fails closed. So the subroutine's confirmer lookup dead-ends
on essentially every personal fact until enrolment populates that column. The
doc inherits a known-broken dependency without naming it.

**(c) Dependents whose custody is dyad-modelled. [code-verified]** The `dyads`
table has columns `dyad_id, recipient_ref, household_id, dyad_pubkey, status,
created_at` — **no member columns at all**. The audience derivation in
`learner_isolation._audience_of` reads `member_a`, `member_b`, `caregiver`,
`recipient`; none exist (this is D-36 finding (c), previously confirmed against
the live DB). Custodian identity via a dyad is underivable, so a dependent whose
custodian is only expressible as a dyad has an empty eligible-confirmer set.

**(d) Sole-custodian incapacity.** Where custody names exactly one custodian and
that person dies, is incapacitated, or loses capacity, the doc's remedy
("re-route to another eligible confirmer") has no target. Notably, the
*recognition* of that situation is Part 4 item 7 (capacity changing over time),
which the doc gates behind ethicist/psychologist/attorney sign-off. **So Part 1
makes an unconditional runtime promise whose failure mode is only detectable by a
subsystem Part 4 forbids building.** That cross-part dependency is unstated.

The honest fix is small: restate the property as *"no fact dead-ends silently —
unconfirmable facts are tracked in a named terminal state with a reason"*, which
is achievable, rather than *"never dead-ends"*, which is not.

### 1.4 Progressive deepening: the runaway mode is real, and it selects for the vulnerable

The doc's central Part 1 claim is that confirmation and depth-seeking are "the
same mechanism running in two directions." They are not, and merging them is the
runaway.

**They have opposite consent polarities.** Confirmation asks about facts the
household *already volunteered* — it reduces uncertainty over an existing
disclosure, and the marginal privacy cost is near zero. Depth-seeking *elicits
facts the household has never disclosed* — it expands the collected set. Merging
them into one priority queue means **trust earned by the low-cost activity is
spent on the high-cost one**. A household that has been cooperative about
confirming what it already said has not thereby consented to being asked new
things.

**The feedback loop has no damping term.** Part 3 names "more confirmed facts
already on record" as a depth-earning criterion. So: confirming facts earns
depth → depth elicits new facts → new facts need confirming → confirming them
earns more depth. That is a closed positive loop, and the doc names **no**
saturation point, decay, or absolute ceiling — only a reactive brake
(withdrawal detection).

**The brake fails on exactly the wrong population.** The loop only stops when
someone signals withdrawal. Households that never signal — the agreeable, the
socially compliant, the lonely, the cognitively declining — are deepened
fastest and without limit. This is precisely inverted from the protection you
want: a conversational system's most engaged users skew toward the isolated
elderly, and this design reads engagement as consent-to-deepen. **The users who
most need a ceiling are the ones this design gives the highest one.**

Minimum fix: an absolute depth ceiling that engagement cannot raise (only
lower), decoupling the confirmation queue from the elicitation queue so earned
trust is not fungible across them, and a saturation term so returns to
"engagement" diminish.

### 1.5 Smaller Part 1 items

- **"Never force" vs the MINIMUM SEED degraded mode (Part 2) is a flat
  contradiction.** Part 1: "never to gate functionality on it, never to imply
  that a household member cannot be helped until they confirm something." Part 2:
  below-threshold households get a "plainly-communicated ceiling on a working
  system" and a message meaning "I can do more here once I know a bit more about
  X." That *is* gating functionality on confirmation and *is* implying reduced
  help pending disclosure. The invitational framing does not resolve it — it is
  the textbook soft-pressure form. One of these two principles has to yield, and
  the doc should say which.
- **`next_confirmable` is uncertainty sampling under another name.** Its known
  pathology is directly relevant: uncertainty-first selection preferentially
  surfaces the *most anomalous* items, which correlate with the weirdest and
  most sensitive facts — fighting the "low-friction first" principle head-on.
  Unmentioned.
- **Open question 2 (one queue or two) is not actually open** — 1.4 answers it.
  They must be two, for consent reasons, not tuning reasons.

---

## PART 2 — SEEDING / ONBOARDING

### 2.1 Narrator bootstrap collides with a Part 4 item the doc says not to build against

The narrator describes other household members; those descriptions enter the
graph as ASSERTED facts about people who have not consented to being described,
and who may not yet be enrolled. The doc addresses **confirmation routing** for
those facts thoroughly and **collection consent** not at all.

That gap is not a minor omission, because the doc *itself* classifies this
situation as unresolved: Part 4 item 1 is "**Disclosure about another adult
member** ... where does consent, confidentiality, and the 'never adjudicate'
principle intersect? Genuinely unresolved," gated behind ethicist, psychologist,
and attorney sign-off.

**Part 2's central seeding mechanic is an instance of a case Part 4 says must not
be built against.** Zone 2 ("People") is *entirely* narrator-describes-others.
Either the gate does not mean what it says, or Part 2's core flow is
gate-blocked. As written the roadmap asserts both.

This is also the sharpest contextual-integrity problem in the document (see
§4.1): the information flow "A tells the system about B's health" violates the
norms of the context in which B disclosed it to A, regardless of who may later
*read* it. The injection contract governs reading. Nothing here governs writing.

### 2.2 Custodian per-fact confirmation: the friction produces habituation, not attention

The stated rationale:

> "a custodian who could bulk-confirm a dependent's entire profile in one tap is
> a custodian who never actually reviewed most of it"

This is intuitive and, past a modest N, **empirically backwards**. The consent
literature (cookie-banner and EULA click-through studies; the broader
warning-fatigue and alarm-habituation work) is consistent: repeated,
individually low-stakes confirmations train automaticity. Attention per item
*declines* with the number of items. A custodian facing 60 sequential
confirmations is not 60× more attentive than one facing a structured summary —
they are less attentive by item 15, and the design has given them no way to
signal which items actually deserved scrutiny.

Scale check the doc never does: a dependent with a chronic condition plausibly
carries 50–200 facts. At even 10–15 seconds each, that is 15–50 minutes of
uninterrupted confirmation labour, in a **voice-first** interface, for one
dependent. The predictable outcomes are abandonment or rubber-stamping — the
exact failure the friction was introduced to prevent.

Better-supported alternative, consistent with the doc's own goals: **risk-tiered
review** — batch-confirm the low-sensitivity bulk with per-item opt-out, and
force genuine individual attention only on high/critical items. That spends the
custodian's finite attention where it matters instead of spreading it uniformly
until it is worthless. (This depends on sensitivity being trustworthy, which
§3.2 shows it currently is not.)

**Unaddressed gap:** what happens to a dependent's fact the custodian *declines*
to confirm? The dependent cannot self-confirm — that is the premise. So it sits
ASSERTED forever with no eligible confirmer remaining. Another instance of 1.3.

### 2.3 MINIMUM SEED: the denominator is undefined, and day one is always degraded

- **"Measured on CONFIRMED coverage" has no denominator.** Coverage is a ratio;
  the denominator is the set of facts the household *has not told you about
  yet* — unknowable by construction. If instead it is an absolute count, the doc's
  own anti-gaming goal fails in the other direction: 100 confirmed trivia about
  pets clears a bar that 10 confirmed care facts do not. The doc rules out
  volume-gaming while leaving the only two available metrics both gameable.
- **Every household is below threshold on day one, by definition.** So the
  universal first-run experience is degraded mode plus an explanation of the
  ceiling — directly at odds with Zone 1's stated job of establishing a warm,
  unclinical register. The first thing a household hears is a limitation notice.
- **CONFIRMED coverage requires two turns per fact** (assert, then confirm), so
  day-one coverage is near zero even for an enthusiastic narrator. The threshold
  metric is the slowest-moving quantity in the system, used to gate the moment
  when impressions are formed fastest.

Worth stating plainly: the roadmap correctly leaves the *number* open (good
discipline, matching the Gate A precedent), but the *metric* is underspecified
in a way that no choice of number fixes.

### 2.4 Four-zone ordering: the research supports the shape, but not the stated reason — and one principle is self-contradicted

**The ordering is defensible; the justification given for it is not.**

- **The doc's own "high-value, low-friction first" principle is violated by its
  own ordering.** Zone 3 (care, health, routines) is described as "the material
  the rest of HIP is actually built to help with" — i.e. the *highest*-value
  zone — and it is placed third. The actual ordering principle is
  **low-sensitivity first**, which is a different thing. The doc conflates "low
  friction," "low sensitivity," and "high value" and uses them interchangeably;
  they diverge exactly where it matters.
- **Funnel technique (survey methodology) partially supports it, for a different
  reason.** Broad→narrow and non-sensitive→sensitive ordering is standard, but
  its documented purpose is reducing *order/priming effects* and protecting
  response rates on later items — not reducing perceived friction. The doc claims
  a friction benefit the funnel literature does not establish.
- **What Zone 1 actually is, unnamed: foot-in-the-door.** "Bank several easy
  `CONFIRMED` facts before any harder ground is touched" is the Freedman &
  Fraser (1966) compliance procedure, near-verbatim: secure a small agreement to
  raise compliance with a larger later request. It works. It is also a
  **persuasion technique**, and a document whose governing principles are "never
  force" and "earn depth, don't take it" is, in its interview structure,
  deploying a documented compliance manipulation to increase disclosure. That
  tension is the most important unexamined thing in Part 2. It does not
  necessarily make the ordering wrong — but it must be named and defended, not
  presented as neutral friction-reduction.
- **Motivational interviewing is misappropriated.** "Reflect, don't interrogate"
  borrows MI's reflective-listening form. MI's reflections exist to help a client
  resolve *their own* ambivalence toward *their own* goal; the practitioner is
  explicitly not extracting information for third-party use, and MI's ethics
  depend on that alignment. Repurposing the technique to lower a subject's
  resistance to disclosure *for the system's data needs* inverts the ethical
  frame while keeping the surface behaviour. If the doc wants MI's warmth, it
  should say why the borrowed technique remains legitimate once the beneficiary
  changes — the research does not carry that over for free.
- **The unnamed prior art for all of Part 2 is progressive profiling** (CRO /
  marketing): incremental data capture across sessions instead of one long form.
  That is precisely what "progressive and resumable — explicitly not
  single-session" describes. Worth citing, and worth noting its native success
  metric is *completion rate*, not user welfare — importing the pattern without
  that caveat imports the incentive too.

---

## PART 3 — BOUNDARY MANAGER

### 3.1 Withdrawal detection is underspecified in three separate ways

**(a) The signals named are not reliably observable on this channel.** "Curtness"
is prosodic, not lexical; over ASR transcripts it is largely unrecoverable, and
what does survive (short utterance length) confounds with the member being busy,
driving, or simply having a short answer. "Topic-changing" is not distinguishable
from ordinary conversational drift without a topic model the doc does not
posit. Of the four listed signals, only "declining to answer" maps to anything
the system currently emits — `control_decline` → `outcome.kind == "override"`
**[code-verified]** — and that is confirmation-gate-specific, not general.

**(b) There is no re-approach criterion.** The doc says the manager "backs off ...
on the general depth ceiling for some window" and never says what ends the
window. Two failure modes: if nothing ends it, a single terse morning
permanently caps a household's depth; if wall-clock alone ends it, then
withdrawal is overridden by the calendar — which the doc explicitly rejects for
the *engagement* direction ("should not be pushed at the same pace just because
the calendar says it's been a week"). **The design is asymmetric in a way it
does not acknowledge: engagement is event-driven, withdrawal recovery is
unspecified.** Whatever fills that gap determines whether the whole mechanism
ratchets up, down, or oscillates — and it is the single most consequential
unspecified parameter in Part 3.

**(c) The base rate defeats the detector.** Genuine withdrawal signals are rare
and ambiguous; the surrounding conversation is overwhelmingly non-withdrawal.
Any detector sensitive enough to catch real withdrawal will fire mostly false
positives, and the doc's remedy for a false positive (drop the household's
general depth ceiling) is costly and invisible to the user, who cannot tell why
the system got quieter. There is no correction channel — no way for a member to
say "no, I'm fine, go on."

Note the interaction with §1.4: false negatives are *systematically*
concentrated in compliant users. The detector's errors are not randomly
distributed across the population; they are correlated with vulnerability.

### 3.2 "Sensitivity gates depth" breaks in two independent ways, one of them live **[code-verified]**

**(a) A static per-attribute label cannot express contextual sensitivity.** This
is the core claim of contextual integrity (Nissenbaum): informational norms are
relative to context, and sensitivity is not an intrinsic property of a data
type. `medication` is unremarkable in a household organised around chronic care
and critical in a household where one member is concealing a diagnosis from
another. The four-level scale attaches to the *attribute*, so it returns the same
answer in both. Meanwhile every *other* Part 3 principle (earn depth, follow
engagement, back off) is explicitly relationship- and context-dependent. **The
one input the doc calls "not a separate check bolted on" is the only
context-blind element in the component.**

**(b) Both existing sensitivity encodings mis-rank `critical`, in the permissive
direction. [code-verified]** The vocabulary is four-valued —
`SENSITIVITY_LEVELS = ("low", "medium", "high", "critical")`
(`harness/extraction_queue.py:95`), and `permissions.py:55` correctly pairs
`("high", "critical")`. But both ordinal encodings in tree are three-valued:

```python
harness/curator_shadow.py:95   _ORDINAL = {"high": 1.0, "medium": 0.5, "low": 0.0}
                              # "critical" misses -> default 0.5 -> ranks BELOW "high"
harness/hipconfig.py:30       SENSITIVITY_RANK = {"low": 1, "medium": 2, "high": 3}
                              # .get(tag, 0) -> "critical" -> 0 -> ranks BELOW "low"
```

If the Boundary Manager consumes either — and the doc says sensitivity is "an
input the Boundary Manager gives the subroutine" — then **the most sensitive
class in the system gates depth the least**, and in `hipconfig`'s case less than
the least sensitive class. Building a consent-adjacent control on either
encoding reproduces an existing bug in a place where it becomes a safety
property. Any spec for Part 3 must state which encoding is authoritative and fix
it first.

**(c) Who assigns sensitivity?** It is set at extraction time. If an LLM
extractor assigns it, the depth gate is controlled by an unconfirmed,
unaudited model output the household never sees — an unreviewable input to a
consent control. The doc's own instinct elsewhere (derive from
server-authoritative state, never trust the caller) argues against that, but the
doc does not apply it here.

**(d) Structural bias toward trivia.** Gating depth by sensitivity means the
system asks least about exactly what it exists to help with — Zone 3 is
simultaneously the highest-value and highest-sensitivity material. Combined with
2.3's confirmed-coverage threshold, a household can be pushed toward clearing
MINIMUM SEED on low-sensitivity trivia because that is what the boundary manager
most readily permits. The two mechanisms compose badly and the doc does not
check the composition.

### 3.3 "Detail must visibly serve the family" is a self-certifying test

The stated test: "can the system's own next turn make the value of having asked
visible." The system both asks the question and grades whether asking was
justified, using its own generated output as the evidence. A fluent generator
satisfies this trivially for almost any question — producing a plausible benefit
sentence is exactly what such a model is good at.

This is structurally the same anti-pattern this codebase has already been bitten
by twice: a check that hand-builds the object under test and then tests it. The
principle is right; the test is not a test. A real one needs an *external*
referent — a benefit the household can be observed to act on, or an
audit-time check by someone other than the asker.

### 3.4 The Part 1 / Part 3 separation is circular, and "independently tunable" is false

The doc claims a clean separation: the Boundary Manager "does not call
`next_confirmable`/`next_depth_question` directly — it **constrains** them,"
citing the injection-contract/ranker precedent.

The dependency is bidirectional. The manager maintains the ceiling; Part 1
consults it; but the engagement state that *sets* the ceiling is derived from
confirmation outcomes, which Part 1 produces via
`record_confirmation_outcome`. So: ceiling → what gets surfaced → what gets
confirmed/declined → engagement signal → ceiling. That is a closed loop, and it
means the two are **not** independently tunable: raising the ceiling changes
which questions are surfaced, which changes the engagement signal, which moves
the ceiling again.

The cited precedent does not apply. The injection contract does not read the
ranker's output; it is genuinely one-directional. This is not, and the doc
should either name the loop and specify its stability properties, or break it
(e.g. derive engagement from signals the ceiling cannot influence).

---

## 4. RESEARCH: WHAT SUPPORTS, WHAT CONTRADICTS, WHAT IS REINVENTED

### 4.1 Contextual integrity (Nissenbaum) — supports the architecture, contradicts two specifics
**Supports:** separating "who may read this" (injection contract) from "how much
may we ask" (Boundary Manager) is exactly CI's distinction between appropriate
flow and mere access control. The two-component split is well-founded.
**Contradicts:** (i) static per-attribute sensitivity, §3.2(a) — CI's central
claim is that appropriateness is norm-relative to context, which a fixed
four-level attribute label cannot encode; (ii) the narrator describing other
members, §2.1 — a textbook CI violation at the point of *collection*, which the
doc's read-side controls do not address.

### 4.2 Foot-in-the-door (Freedman & Fraser 1966) — the unnamed mechanism of Zone 1
Zone 1's "bank several easy CONFIRMED facts before any harder ground" is the FITD
procedure. Supports the ordering's *effectiveness*; raises an ethical question
the doc does not engage, given its own "never force" commitment. Name it and
defend it, or reorder.

### 4.3 Funnel technique / survey methodology — partially supports, wrong reason
Broad→narrow, non-sensitive→sensitive is standard and the doc's ordering roughly
conforms. But the technique's purpose is order-effect and response-rate
protection, not friction reduction. Also relevant and unused: survey research
consistently finds sensitive-item response improves with *explicit* purpose
statements and confidentiality assurances — which would support the doc's "detail
must visibly serve the family" principle far better than its self-certifying test.

### 4.4 Motivational interviewing — misappropriated, §2.4
MI is client-goal-directed and its ethics depend on that alignment. Borrowing
reflective listening to lower resistance to disclosure for the *system's*
information needs keeps the form and inverts the frame. MI also explicitly warns
against the "righting reflex" (pushing toward a goal the client hasn't chosen) —
which is arguably what the MINIMUM SEED nudge is.

### 4.5 Progressive profiling — the unnamed prior art for all of Part 2
Incremental cross-session capture is a well-developed CRO pattern. The doc
reinvents it without citation. Its documented failure mode is precisely the creep
Part 3 worries about, and its native success metric is completion rate — importing
the pattern without naming that incentive imports it silently.

### 4.6 Active learning / human-in-the-loop — supports the shape, warns about the pathology
`next_confirmable` is uncertainty sampling with a human oracle. Supported as a
design. But two documented pathologies land directly: **oracle fatigue** (bearing
on §2.2's per-fact custodian confirmation) and **sampling bias** — uncertainty-first
selection preferentially surfaces the most anomalous items, which fights
"low-friction first" head-on (§1.5). Neither appears in the doc.

### 4.7 Consent fatigue / warning habituation — contradicts §2.2's rationale outright
The custodian per-fact friction rests on an intuition the literature does not
support past small N. Attention per confirmation declines with count; uniform
friction converts review into ritual. This is the one place the doc's reasoning
is not merely underspecified but, on the evidence, backwards.

---

## 5. WHAT THE DOC GETS RIGHT (stated because a critique that lists only faults is not a fair reading)

- **Extracting confirmation into a subroutine rather than embedding it in
  onboarding is correct**, and the rationale given (every other path would
  otherwise reimplement the same judgment calls) is exactly right. This is the
  document's best decision.
- **Separating Boundary Manager from Safety Layer** — "too much" and "dangerous"
  as distinct failure classes with distinct remedies — is well-argued and matches
  CI's framing.
- **Deriving `eligible_confirmers` from server-authoritative state rather than
  caller assertion** is the right instinct, and correctly cites the isolation-gate
  precedent. (It just doesn't resolve to anything yet, §1.3(b).)
- **Leaving MINIMUM SEED's number open** rather than guessing, on the stated Gate A
  precedent, is good discipline.
- **Naming Part 5's constraint next to the design it bounds** rather than in a
  separate ticket is right, for the reason given.
- **"Progressive and resumable, no completion event"** is correct and rare;
  most onboarding designs assume a funnel with an end.

---

## 6. THE FOUR THINGS I WOULD FIX BEFORE ANY SPEC IS WRITTEN

1. **Resolve the CORROBORATED wiring (§1.1).** Decide whether the ladder gains a
   real multi-party attestation rung (schema change, `confirmed_by` becomes a
   set) or Zone 2's justification is rewritten. Also declare one canonical trust
   ordering — there are already two in tree that disagree.
2. **Split the confirmation queue from the elicitation queue (§1.4)**, add an
   absolute depth ceiling engagement can only lower, and specify the
   withdrawal-recovery criterion (§3.1(b)). These three together are the
   difference between "earn depth" and unbounded creep.
3. **Fix sensitivity before building on it (§3.2).** Declare the authoritative
   encoding, make `critical` rank highest in it, and decide whether a static
   per-attribute label is defensible at all given CI.
4. **Reconcile Part 2's narrator mechanic with Part 4 item 1 (§2.1)**, and
   Part 1's "never force" with Part 2's degraded mode (§1.5). Both are internal
   contradictions where the document currently asserts both sides.

No design was changed, no lock taken, no status proposed. Parts 4 and 5 were not
critiqued except where Parts 1–3 depend on them.
