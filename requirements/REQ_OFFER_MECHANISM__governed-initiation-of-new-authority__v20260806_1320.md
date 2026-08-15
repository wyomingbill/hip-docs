# REQ_OFFER_MECHANISM — governed initiation of new authority

**Status:** **SUPERSEDED 2026-08-06 by `REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1625.md`** (HA-02, Bill's ruling: one line added to §2.2's not-an-offer list). **NOTHING IN THIS FILE'S BODY WAS EDITED — this header line is the only change, and the body below remains byte-identical to Bill's own revision, which is the property D-R-195 filed it for.** Prior status, preserved: DRAFT-RATIFIED-PENDING — Bill has revised this REQ; formal ratification is the D-R that lands step 1 of this REQ's own LANDING ORDER (§12), not that filing. Filed by D-R-195, 2026-08-06. Nothing built, nothing ruled MET, A1-A20 unattempted.
**Reconciled-Against:** roadmap `5c06b6d` (D-R-195, 2026-08-06). Body copied VERBATIM from Bill's revision; every line from the first `---` onward is byte-identical to the source, only the header lines above it differ.  
**Decision-Owner:** Bill  
**Prepared:** 2026-08-06  
**Related:** `REQ_STRUCTURAL_CEILING`, trigger registry, grant state, governed-decision record, member initiation policy  
**Supersedes:** the solicitation requirements in `REQ_STRUCTURAL_CEILING` once this REQ is ratified; that REQ SHALL retain only the cross-axis rule and a pointer here

---

## 0. RULINGS

### RULING 1 — an offer is the sole system-initiated path to new authority, not the sole path to speech

The sentence “the offer is the only way HIP ever initiates” is rejected as overbroad.

HIP may initiate speech only under one of three authorities:

1. **Authorized operation** — speech already permitted by an active capability, such as a medication reminder or appointment alert.
2. **Authorized safety interrupt** — speech permitted by a pre-existing validated sensing and safety contract.
3. **Offer** — a request for new authority.

No fourth class exists.

An offer is therefore:

> A system-initiated request for authority HIP does not currently hold.

An offer is required before HIP may initiate any expansion of collection, retention, audience, inferential reach, action authority, recurring initiation, or enabled capability.

A member asking HIP to do something new is not a system-initiated offer. It enters a separate **member-initiated grant-confirmation path**.

### RULING 2 — the trigger registry is the sole source of offer eligibility

An offer may exist only when the trigger registry emits one of its four already-ratified material-change kinds.

This REQ imports those four kinds unchanged. It does not create, rename, or broaden them.

The following remain non-triggers:

- passage of time;
- usage or engagement patterns;
- graph fullness;
- prior acceptance;
- prior refusal;
- unprompted disclosure;
- template revision;
- operator desire for more data;
- model recommendation unsupported by a registered world change.

### RULING 3 — one situation produces one minimal offer, once

Each material change creates one canonical `situation_id`.

A situation may produce at most one system-initiated offer. Presentation spends the situation. Acceptance, decline, non-response, expiry, invalidation, template change, service restart, or event replay SHALL NOT make the situation offerable again.

A registry entry SHALL map the situation to exactly one pre-approved, minimal authority delta. HIP may neither bundle unrelated authority into that offer nor split the delta into a staircase of smaller offers.

A member may later reopen the matter on their own initiative. That does not revive the spent situation or authorize HIP to re-solicit.

### RULING 4 — offer language and offer effect are one governed object

Every offer is defined by a versioned registry object containing both:

- the fixed human-facing template; and
- the exact machine-enforced authority delta.

The model may fill typed factual slots. It may not paraphrase, reorder, soften, intensify, personalize, shorten, extend, select a variant, or tune the pitch.

There is one active semantic template per offer kind and locale. Runtime experiment assignment, variant identifiers, and user-specific wording selection SHALL NOT exist in the offer path.

A template change is a governed policy revision applied prospectively. It does not reopen a spent situation.

### RULING 5 — a decline is control state, not a fact about the member

A decline, non-response, lapse, or invalidation SHALL be stored only in the offer-control plane and governed-decision record.

It SHALL NOT enter:

- the household knowledge graph;
- embeddings;
- summaries;
- member traits;
- trust scoring;
- vulnerability scoring;
- care-team projections;
- model context;
- inference inputs;
- feature eligibility other than suppression of the spent offer;
- operator optimization or personalization.

Audit functions may read offer state only to verify compliance with this REQ. They may not use it to improve acceptance.

### RULING 6 — acceptance changes authority by exact equality, not interpretation

Acceptance applies exactly the authority delta attached to the offer instance.

It grants nothing by implication. A grant SHALL NOT expand category, representation, purpose, audience, retention, inferential reach, action authority, recurrence, or downstream use beyond the words and machine-readable scope of the offer.

If the rendered offer and authority delta disagree, the offer is invalid and acceptance changes nothing.

---

## 1. CONTROL RULES

> No registered material change, no offer.  
> No offer, no system-initiated request for new authority.  
> No explicit acceptance, no scope expansion.

And:

> A decline changes only offer state. It is never evidence about the person.

---

## 2. DEFINITIONS

### 2.1 New authority

`NEW_AUTHORITY` means any positive change to one or more of:

- collectable categories or representations;
- purpose;
- retention;
- audience;
- inferential reach;
- external disclosure;
- action authority;
- recurring or proactive initiation;
- enabled care capability.

A revocation, narrowing, expiry, policy suspension, or safety shutdown is not new authority and does not require an offer.

### 2.2 Offer

An `OFFER` is a system-initiated request for a specific `AUTHORITY_DELTA` that HIP does not currently possess.

An offer is not:

- an ordinary question within current authority;
- an explanation requested by the member;
- a reminder already authorized;
- a safety interrupt already authorized;
- confirmation of a member-initiated request;
- notice that authority has expired or narrowed;
- a request to confirm an already-volunteered fact where no new collection authority is sought.

### 2.3 Situation

A `SITUATION` is the canonical policy identity of one registry-recognized material change.

It SHALL be generated from registered event identity and material state, not from model wording, prompt text, session identity, or operator labels.

Reprocessing the same underlying event SHALL resolve to the same `situation_id`.

### 2.4 Authority delta

An `AUTHORITY_DELTA` is the exact positive scope change requested by an offer:

```text
authority_delta:
    principal
    purpose_id
    capability_id
    representation_classes
    audience_projection
    retention_policy
    inference_permits
    action_authority
    initiation_authority
```

Every field is explicit. An omitted field means no change to that dimension.

### 2.5 Fixed template

A `FIXED_TEMPLATE` is reviewed language with typed slots. Slots may contain only registry-approved factual values such as a member name, care-function name, triggering event, recipient role, or retention description.

A slot SHALL NOT contain generated persuasion, reassurance, urgency, social pressure, or benefit framing beyond the reviewed template.

---

## 3. INITIATION CLASSES

### R1 — closed initiation taxonomy

Every system-initiated utterance SHALL declare exactly one initiation class:

```text
AUTHORIZED_OPERATION
AUTHORIZED_SAFETY_INTERRUPT
OFFER
```

If no class and active authority can be resolved, HIP SHALL remain silent.

### R2 — offers are required only for expansion

HIP SHALL use an offer for a system-initiated request that would positively expand authority.

HIP SHALL NOT use an offer to disguise ordinary operation, safety response, revocation, narrowing, correction, or member-requested explanation.

### R3 — operational and safety speech cannot smuggle solicitation

An authorized reminder, alert, check-in, or safety interrupt SHALL NOT append, embed, imply, or sequence into a request for new authority unless a separately eligible offer exists.

Operational urgency SHALL NOT create offer eligibility.

---

## 4. TRIGGER AND SITUATION GOVERNANCE

### R4 — trigger-registry exclusivity

Every offer SHALL reference:

```text
trigger_rule_id
trigger_rule_version
change_kind
source_event_id
situation_id
purpose_id
authority_delta_id
```

`change_kind` SHALL be one of the four already enforced by the trigger registry.

An offer lacking a valid registry decision SHALL NOT be rendered.

### R5 — non-trigger firewall

Time passing, engagement, usage frequency, answer length, warmth, graph fullness, prior yes, prior no, prior non-response, or a new template version SHALL NOT create or version a situation.

No downstream model or operator may submit an alternate “material change” label to bypass the registry.

### R6 — canonical situation identity

The trigger registry SHALL deduplicate event replay, retries, duplicate sensor delivery, service restart, and semantically equivalent operator submissions into the same situation.

A `material_circumstance_version` may change only when the registry receives a new qualifying world event under one of its four change kinds.

Policy, prompt, template, model, or business-rule changes do not create a new world event.

### R7 — one minimal delta per situation

Each trigger rule SHALL identify exactly one minimal `authority_delta_id` and one `offer_kind`.

Runtime code and models SHALL NOT:

- combine additional permissions into the offer;
- split the delta into multiple offers;
- add an adjacent recipient, category, inference, retention period, or recurring action;
- choose among competing deltas based on likely acceptance.

If a situation could support several useful capabilities, the registry SHALL select one minimal offer by pre-ratified precedence. The others require a distinct qualifying situation or member initiation.

---

## 5. ONE OFFER PER SITUATION

### R8 — presentation spends the situation

The first valid rendering of an offer moves its situation to `SPENT` for system initiation.

The situation remains spent after:

- acceptance;
- decline;
- non-response;
- lapse;
- invalidation;
- connection failure after confirmed delivery;
- template revision;
- model revision;
- service restart;
- reprocessing of the trigger event.

No reminder, retry, rewording, “are you sure,” adjacent offer, caregiver-mediated retry, or delayed resurfacing is permitted.

### R9 — delivery ambiguity fails closed

A situation is spent only after the system can prove that the complete offer was delivered to the intended principal.

A transport failure before completed delivery may retry the same immutable offer instance. It SHALL NOT create a new offer, new wording, or new situation.

### R10 — member reopening preserves agency without reviving solicitation

After a situation is spent, the member may explicitly request the same or narrower capability.

HIP SHALL process that request through the member-initiated grant-confirmation path. It SHALL NOT treat the request as permission to resume system-initiated offers in that situation or domain.

A caregiver, operator, or model speaking on the member's behalf does not count as member reopening unless an existing authority rule permits that principal to act for this exact decision.

---

## 6. FIXED WORDS, FIXED EFFECT

### R11 — immutable offer instance

Before rendering, HIP SHALL create an immutable offer instance containing:

```text
offer_instance_id
situation_id
intended_principal
offer_kind
template_id
template_version
template_hash
locale
slot_values
authority_delta_id
authority_delta_hash
rendered_text_hash
created_at
expires_under
```

The same instance SHALL govern display, response parsing, scope application, and audit.

### R12 — no generative pitch

The model may supply only typed slot values allowed by the template schema.

It SHALL NOT:

- paraphrase the template;
- reorder its clauses;
- choose synonyms;
- vary length or emotional tone;
- add reasons to accept;
- personalize persuasion from household history;
- omit the narrower service that remains after refusal;
- select a template variant;
- run an experiment branch.

If a slot cannot be safely resolved, the offer SHALL NOT be rendered.

### R13 — A/B testing absent by construction

The runtime offer interface SHALL expose no:

- experiment identifier;
- treatment arm;
- randomization input;
- conversion objective;
- user-segment wording selector;
- model-generated alternative text;
- fallback template selected for likely acceptance.

A reviewed template revision replaces the active version prospectively for new situations only. Historic situations remain spent.

### R14 — explanation without repitching

A member may ask what an offer means before deciding.

HIP may answer using reviewed explanatory material tied to the same offer kind. It SHALL NOT restate the offer as a new pitch, add urgency, recommend acceptance, or alter the authority delta.

The original offer instance remains the only offer.

---

## 7. RESPONSE AND SCOPE APPLICATION

### R15 — explicit response only

Acceptance or decline SHALL be tied to an active offer instance and the intended principal.

The following SHALL NOT count as acceptance:

- silence;
- continued conversation;
- answering an adjacent question;
- prior acceptance;
- a caregiver's preference without decision authority;
- inferred sentiment;
- engagement;
- “whatever you think”;
- an ambiguous response.

An ambiguous response changes no scope. HIP may provide a fixed neutral instruction describing how to accept or decline, but SHALL NOT ask again or reinterpret the response.

### R16 — exact-scope application

On acceptance, the grant engine SHALL apply exactly the referenced `authority_delta`.

The post-acceptance scope SHALL satisfy:

```text
scope_after = scope_before ∪ authority_delta
```

No policy default, model inference, caregiver role, product tier, or adjacent feature may enlarge the delta.

Any requested authority not explicitly present remains unauthorized.

### R17 — principal and authority validation

Only the intended principal, or a representative already authorized for this exact decision domain, may accept.

The offer path SHALL validate decision authority at response time. Household role, account ownership, caregiver status, or prior access alone SHALL NOT substitute for decision authority.

### R18 — text-to-effect identity

The plain-language offer SHALL be deterministically rendered from the same `authority_delta` applied by enforcement.

If the template, rendered text, slots, or delta fail integrity validation, the offer SHALL be invalidated and scope SHALL remain unchanged.

### R19 — revocation and narrowing need no offer

A member may revoke or narrow granted authority without a trigger and without receiving an offer.

HIP may also suspend or narrow authority when required by expiry, policy, safety, conflict, or invalidation. Narrowing SHALL NOT be delayed in order to preserve a product feature.

---

## 8. DECLINE IS NOT A MEMBER FACT

### R20 — control-plane isolation

Offer state SHALL be stored in a dedicated control-plane partition, not in the household epistemic graph.

The only permitted operational reads are:

- preventing a second system offer for the spent situation;
- displaying the member's own governed-decision history;
- validating grant state;
- compliance and safety audit.

### R21 — no downstream interpretation

A decline, lapse, non-response, invalidation, or explanation request SHALL NOT:

- create or update a fact about the member;
- affect trust, personality, cognition, cooperativeness, vulnerability, or risk scores;
- alter care-team access;
- notify a caregiver merely because of the response;
- change ordinary service below the pre-offer ceiling;
- trigger another offer;
- influence future offer wording or timing;
- enter model context, embeddings, summaries, or training/evaluation corpora.

### R22 — audit use is non-optimizing

Audit systems may measure whether the offer mechanism obeys this REQ.

They SHALL NOT use member-level or aggregate response outcomes to optimize acceptance, rank templates, compensate operators, tune models, or select future solicitation policy.

Template quality may be reviewed for comprehension, accessibility, semantic fidelity, and disparate failure—not conversion.

---

## 9. GOVERNED DECISION RECORD

### R23 — every transition is recorded

Each offer-state transition SHALL append a governed-decision event:

```text
event_id
offer_instance_id
situation_id
principal
transition
trigger_rule_id
trigger_rule_version
template_id
template_version
authority_delta_id
scope_before_commitment
scope_after_commitment
response_method
reason_code
timestamp
policy_version
```

Permitted transitions are:

```text
ELIGIBLE -> PRESENTED
PRESENTED -> ACCEPTED
PRESENTED -> DECLINED
PRESENTED -> LAPSED
PRESENTED -> INVALIDATED
```

All terminal states mark the situation spent for system initiation.

### R24 — the record proves process without becoming profile data

The governed-decision record SHALL contain enough information to prove:

- why the offer was eligible;
- exactly what words were shown;
- exactly what authority was requested;
- who responded;
- what scope changed;
- that no second offer occurred.

It SHALL NOT expose offer outcomes as general household facts or care signals.

### R25 — cumulative authority manifest

An accepted offer SHALL update the member's cumulative authority manifest with the exact active delta, purpose, audience, retention, inference, action, and initiation scope.

A declined, lapsed, or invalidated offer SHALL not appear as a trait or warning. It may appear only in the member's governed-decision history as a completed control event.

---

## 10. ACCEPTANCE

| ID | Requirement | Acceptance check |
|---|---|---|
| A1 | R1 | Every system-initiated utterance resolves to one of the three allowed initiation classes. An unclassified utterance is suppressed. |
| A2 | R2-R3 | An authorized medication reminder is delivered without an offer; an added request for broader health collection is blocked absent a separate eligible offer. |
| A3 | R4 | Every offer references a valid trigger-registry decision and one of the four existing change kinds. Fabricated or model-supplied trigger labels fail. |
| A4 | R5 | Time, engagement, graph fullness, prior yes, prior no, and template revision cannot create or version a situation. |
| A5 | R6 | Duplicate event delivery, retry, restart, and semantically equivalent resubmission resolve to the same `situation_id`. |
| A6 | R7 | One trigger maps to one minimal delta. Bundle and staircase fault twins are refused. |
| A7 | R8 | A delivered offer cannot be system-reoffered after acceptance, decline, non-response, lapse, invalidation, restart, template change, or elapsed time. |
| A8 | R9 | A pre-delivery transport failure may resend the same immutable instance; post-delivery retry is blocked. |
| A9 | R10 | A member can later initiate the same capability, but the original situation remains spent and no system solicitation resumes. |
| A10 | R11-R13 | Offer runtime has no experiment, variant, randomization, or generated-text interface. Slot mutation cannot change pitch or scope. |
| A11 | R14 | A requested explanation uses fixed explanatory content and does not create a second offer or altered delta. |
| A12 | R15 | Silence, continued conversation, “whatever you think,” and caregiver preference do not accept. Explicit valid response does. |
| A13 | R16 | Acceptance produces exact set equality with the declared delta. Widened audience, retention, inference, action, or recurrence fault twins fail. |
| A14 | R17 | Acceptance by the wrong principal or an overbroad representative role is rejected. |
| A15 | R18 | Any mismatch among template, rendered text, slots, and delta invalidates the offer and changes no scope. |
| A16 | R19 | Revocation and narrowing execute without trigger or offer and cannot be delayed for feature preservation. |
| A17 | R20-R21 | Decline state is absent from graph, embeddings, summaries, model context, care projections, scoring, and caregiver notifications. Offer suppression still works. |
| A18 | R22 | Product and model systems contain no acceptance-rate, decline-reduction, or template-conversion objective. Audit-only access is isolated. |
| A19 | R23-R24 | Record reconstruction proves trigger, wording, requested delta, response, exact scope change, and spent state without exposing decline as profile data. |
| A20 | R25 | Acceptance updates the cumulative authority manifest exactly; decline appears only in the member's governed-decision history. |

### Acceptance tier

- **ABSOLUTE:** A1-A20.
- Any reduction requires an explicit ruling because the mechanism is the sole system-initiated path to new authority.

---

## 11. NAMED LIMITS

1. **The four material-change kinds are imported, not restated.** This REQ cannot prove that those four kinds are complete or correctly designed; it governs their use after the trigger registry emits them.
2. **Fixed wording prevents adaptive persuasion, not bad policy.** A manipulative fixed template remains manipulative. Human review must evaluate comprehension, neutrality, accessibility, and semantic fidelity.
3. **One-offer enforcement depends on canonical situation identity.** If operators can manufacture new situation versions from the same world event, the rule becomes theatre. R5-R6 and A4-A5 are therefore structural, not bookkeeping.
4. **One offer per situation creates a bundling incentive.** R7 counters this by requiring one pre-ratified minimal delta and forbidding runtime bundling or staircasing.
5. **The governed-decision record still contains personal control events.** Isolation prevents those events from becoming household traits; it does not make the record non-personal or exempt from retention and access policy.
6. **No numeric time-based offer budget is needed.** The bound is event-identity based: one system offer per qualifying situation, ever.

---

## 12. LANDING ORDER

1. Define the closed initiation taxonomy and suppress unclassified initiation.  
2. Make trigger-registry decision and canonical `situation_id` mandatory for offer creation.  
3. Introduce immutable offer instances binding template and authority delta.  
4. Remove all generative and experimental interfaces from offer rendering.  
5. Implement the spent-situation state machine and duplicate-event reconciliation.  
6. Enforce explicit-response and exact-scope application.  
7. Isolate offer state from the knowledge graph and model context.  
8. Append governed-decision events and expose the cumulative authority manifest.  
9. Run A1-A20 before replacing the solicitation section of `REQ_STRUCTURAL_CEILING` with a pointer to this REQ.

---

## 13. COMPACT LAW

> HIP may initiate ordinary speech only under existing operational or safety authority.  
> HIP may initiate a request for new authority only through a registered offer.  
> A real world change creates one situation. One situation receives one fixed, minimal offer, once.  
> Silence and ambiguity grant nothing. Decline changes only offer state.  
> Acceptance applies exactly what the member was shown, and nothing else.
