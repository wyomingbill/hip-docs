# REQ_OFFER_MECHANISM — governed initiation of new authority

**Status:** **MET — ruled by Bill, 2026-08-11.**

Ruled from the **A1–A20 + A20b acceptance table at 17 PASS / 0 FAIL / 4 CANNOT RUN**, the
manifest check (A20b), and HA-41's final runs: **binding standing battery 1158 passed / 0
failed / 9 xfailed**, **`--layer 7` exit 0**, **no deterministic regression**, and the **memory
harness at 13/17, inside the 13–15 pin**.

**THE FOUR CANNOT RUNs ARE EXACTLY THE FOUR CONDITIONAL CLAUSES — A2, A8, A9 and A11 — AND THEY
REMAIN CONDITIONAL ON THEIR NAMED FEATURES** (reminder delivery, transport layer,
member-initiated capability path, explanation feature), per Bill's ruling of 2026-08-10 recorded
in §10 and reaffirmed here. **This ruling does not waive them, does not convert them to PASS, and
does not force those features into existence.** Each binds when its feature exists, and not
before. The three clauses that were UNCONDITIONAL CANNOT RUNs at HA-28 — **A6, A12 and A16** —
are now PASS, built rather than excused.

**Evidence chain, by the dispatch that produced it:**

- **HA-39** — A6 delta minimality made MANDATORY with no bypass (`require_minimal_for` removed,
  nothing replacing it; the situation kind read off the situation, never accepted from the
  caller; fixtures on a structurally separate `FixtureOfferRegistry` path, production provably
  unable to reach it by a standing test that parses every `harness/` and `memory_engine/` module
  for an `eval` import). A12 and A16 built. **TD-R-184 fixed** (`granted |= (scope_after -
  scope_before)`). **TD-R-186 filed.** *HA-39 never landed itself; its work was committed by
  HA-41 at `1fa2258` — see the dispatch ledger row.*
- **HA-40** — **TD-R-186 fixed**, narrowly and on Bill's ruling: `authority_manifest_for`
  subtracts `authority_change` events in the same append-order fold, so R25's manifest reports
  **ACTIVE** authority and agrees with `current_authority`. No manifest redesign; still derived
  by replay, never stored. **A20b added** to this table. *Also landed by HA-41 at `1fa2258`.*
- **HA-41** — landed both of the above, added Bill's standing test, and ran the final
  measurement. Report:
  `docs/dispatches/DISPATCH_HA41_TDR186_ERASURE_INVENTORY__fix-landed-18-surfaces-two-collector-runs__v20260811_1510.md`
  (`d2d2e9d`; segment 1's code at `1fa2258`).
- **A19**, the one FAIL in the prior status line, was closed earlier by **HA-36** (R26 — the
  exact words shown survive a restart).

**Reconciled-Against:** roadmap `d2d2e9d` (HA-41, 2026-08-11).

**PRIOR STATUS LINE, RETAINED VERBATIM — superseded by the ruling above, not deleted:**

> **NOT MET — ruled by Bill, 2026-08-10**, from HA-28's CORRECTED acceptance table
> (`docs/dispatches/DISPATCH_HA28_OFFER_ACCEPTANCE__r23-wiring-finished-and-a1-a20-measured__v20260810_0917.md`,
> §4 A1–A20, as corrected by HA-29). That table counts **12 PASS / 1 FAIL / 7 CANNOT RUN**:
> PASS A1, A3, A4, A5, A7, A10, A13, A14, A15, A17, A18, A20; **FAIL A19**; CANNOT RUN A2, A6, A8,
> A9, A11, A12, A16. **A19 is a real defect** — the governed record survives a restart and the exact
> words shown do not — and it **stays a FAIL until the durable exact-wording fix lands** (Bill,
> 2026-08-10). See the CONDITIONAL-CLAUSE amendment on the acceptance table below.

**Prior status line, retained:** DRAFT-RATIFIED-PENDING — Bill has revised this REQ; FORMAL RATIFICATION IS THE D-R THAT LANDS STEP 1 OF THIS REQ'S OWN LANDING ORDER (§12), not this filing. Filed by D-R-195, 2026-08-06. **AMENDED BY HA-02, 2026-08-06, on Bill's ruling: ONE LINE ADDED to §2.2's not-an-offer list — "turn-bound disclosure consent within a member-initiated exchange". That is the ONLY body change from v20260806_1320; every other line is byte-identical to it and therefore still byte-identical to Bill's own revision.** Nothing built, nothing ruled MET, A1-A20 unattempted.
**Reconciled-Against:** roadmap `25daf17` (HA-02, 2026-08-06). Cut from `v20260806_1320` by `cp`, then ONE line added to §2.2 and the Status line rewritten — `diff` between the two files shows exactly those two changes and nothing else. The prior version is RETAINED INTACT with its body unedited; only its own Status header was flipped to SUPERSEDED with a pointer here.
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
- turn-bound disclosure consent within a member-initiated exchange;
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

### R26 — the exact wording is durably recoverable and verifiable

**ADDED BY AMENDMENT, HA-36, citing Bill's ruling 2026-08-11:**

> **A19 is a real failure. The durable record must hold the exact rendered wording.**

**The exact rendered wording of every presented offer SHALL be durably recoverable and
verifiable after restart, through a governed read.**

Concretely, at presentation time the offer control plane SHALL durably record: the offer
instance id and situation id; the template id and version; the authority delta; the slot
values; the **verbatim rendered text**; and an integrity hash of that text computed by the
same mechanism that produced `rendered_text_hash` (R11/R18). A read of the stored wording
SHALL go through a named permitted purpose (R20) — `member_own_history`, since **a member may
always see what they were shown**. A stored wording that fails its integrity check SHALL be
reported as a failure and SHALL NOT be presented as the record.

**WHY THIS IS AN ADDITION AND NOT A RESTATEMENT OF R24.** R24 already requires the record to
prove *"exactly what words were shown."* R23's enumerated sixteen fields carry `template_id`
and `template_version` and **neither the slot values nor the rendered text** — so R24's clause
was unsatisfiable from R23's own field list the moment a process restarted, which is precisely
what HA-28 measured: `instance_recoverable=FALSE`, `exact_words_recoverable=FALSE`. The words
lived only on the in-process `OfferInstanceRegistry`, whose own docstring said the guarantee
does not survive a restart.

**THE TENSION IS NAMED RATHER THAN RESOLVED SILENTLY.** Two readings of R24 were available:
that the governed-decision EVENT must itself carry the words, or that the RECORD — the control
plane's account of the transition — must be able to produce them. R26 takes the second, and
says so, because the first would require widening R23's enumerated field list and a
`policy_version` bump that would make every existing event a different shape. **R23's sixteen
fields are therefore UNCHANGED**; the wording is a separate durable record in the same control
plane, joined by `offer_instance_id`, and the governed-decision event keeps meaning exactly
what it meant.

**R26 IS SUBJECT TO R20, R21 AND R22 WITHOUT EXCEPTION.** The stored wording is offer control
state: it lives in the control-plane partition, **never in the household epistemic graph**,
never in model context, embeddings, summaries, training or evaluation corpora, and never in
any scoring or ranking path. It is what the SYSTEM said, not a fact about the member, and
storing it durably must not become a route by which offer state reaches the member's record.

**A PRE-R26 EVENT HAS NO STORED WORDING AND SHALL REPORT ITS ABSENCE AS `LEGACY`.** It SHALL
NOT be reported as satisfying this clause. An absent record is absence, never a pass — the
same fail-closed posture the rest of this REQ takes.

---

## 10. ACCEPTANCE

**ACCEPTANCE TABLE AMENDED — Bill's ruling, 2026-08-10 (HA-29).**

**A2, A8, A9 and A11 are CONDITIONAL clauses.** Each binds when its named feature exists —
reminder delivery, transport layer, member-initiated capability path, explanation feature — and
not before. **The requirement does not force those features into existence**, so their CANNOT RUN
in HA-28 is not a debt against this REQ.

**A6, A12 and A16 stay UNCONDITIONAL.** Their CANNOT RUN *is* real missing offer behaviour and
remains owed: delta minimality (A6), the utterance→`ResponseKind` response classifier (A12), and
revocation/narrowing (A16).

**A19 stays a FAIL** until the durable exact-wording fix lands. Not conditional, not waived.

| ID | Requirement | Acceptance check |
|---|---|---|
| A1 | R1 | Every system-initiated utterance resolves to one of the three allowed initiation classes. An unclassified utterance is suppressed. |
| A2 | R2-R3 | An authorized medication reminder is delivered without an offer; an added request for broader health collection is blocked absent a separate eligible offer. **CONDITIONAL (Bill, 2026-08-10):** binds when a reminder-delivery path exists, and not before. This requirement does not force that feature into existence. |
| A3 | R4 | Every offer references a valid trigger-registry decision and one of the four existing change kinds. Fabricated or model-supplied trigger labels fail. |
| A4 | R5 | Time, engagement, graph fullness, prior yes, prior no, and template revision cannot create or version a situation. |
| A5 | R6 | Duplicate event delivery, retry, restart, and semantically equivalent resubmission resolve to the same `situation_id`. |
| A6 | R7 | One trigger maps to one minimal delta. Bundle and staircase fault twins are refused. |
| A7 | R8 | A delivered offer cannot be system-reoffered after acceptance, decline, non-response, lapse, invalidation, restart, template change, or elapsed time. |
| A8 | R9 | A pre-delivery transport failure may resend the same immutable instance; post-delivery retry is blocked. **CONDITIONAL (Bill, 2026-08-10):** binds when a transport layer exists, and not before. This requirement does not force that feature into existence. |
| A9 | R10 | A member can later initiate the same capability, but the original situation remains spent and no system solicitation resumes. **CONDITIONAL (Bill, 2026-08-10):** binds when a member-initiated capability path exists, and not before. This requirement does not force that feature into existence. |
| A10 | R11-R13 | Offer runtime has no experiment, variant, randomization, or generated-text interface. Slot mutation cannot change pitch or scope. |
| A11 | R14 | A requested explanation uses fixed explanatory content and does not create a second offer or altered delta. **CONDITIONAL (Bill, 2026-08-10):** binds when an explanation feature exists, and not before. This requirement does not force that feature into existence. |
| A12 | R15 | Silence, continued conversation, “whatever you think,” and caregiver preference do not accept. Explicit valid response does. |
| A13 | R16 | Acceptance produces exact set equality with the declared delta. Widened audience, retention, inference, action, or recurrence fault twins fail. |
| A14 | R17 | Acceptance by the wrong principal or an overbroad representative role is rejected. |
| A15 | R18 | Any mismatch among template, rendered text, slots, and delta invalidates the offer and changes no scope. |
| A16 | R19 | Revocation and narrowing execute without trigger or offer and cannot be delayed for feature preservation. |
| A17 | R20-R21 | Decline state is absent from graph, embeddings, summaries, model context, care projections, scoring, and caregiver notifications. Offer suppression still works. |
| A18 | R22 | Product and model systems contain no acceptance-rate, decline-reduction, or template-conversion objective. Audit-only access is isolated. |
| A19 | R23-R24 | Record reconstruction proves trigger, wording, requested delta, response, exact scope change, and spent state without exposing decline as profile data. |
| A20 | R25 | Acceptance updates the cumulative authority manifest exactly; decline appears only in the member's governed-decision history. |
| **A20b** | **R25** | **The manifest reports ACTIVE authority: after accept A, accept B, then narrow-or-revoke A, the manifest shows A removed or narrowed and B untouched, identically to the access reader, and identically again when reconstructed from a fresh ledger. ADDED BY AMENDMENT, HA-40, citing Bill's ruling 2026-08-11 (TD-R-186).** |

### A20b — why R25 needed a second acceptance check (HA-40)

**ADDED BY AMENDMENT, citing Bill's ruling 2026-08-11.**

A20 as originally written checks that *acceptance updates* the manifest. It says nothing about
what happens afterwards, and **a manifest that only ever adds satisfies it completely while
reporting authority the member has revoked.** That is exactly what TD-R-186 was: R25's own
words are *"the exact ACTIVE delta"*, and the manifest replayed ACCEPTED events only, so a
revocation never reached it. A1-A20 could report a clean closure with the manifest false.

**A20b binds the sequence, not the single event**, and requires the manifest to agree with the
reader that decides access — because the failure was never "the manifest is wrong in
isolation", it was "two functions answer *what has this member granted?* and they differ".

Executed by `eval/test_authority_revocation.py::test_td_r_186_grant_a_grant_b_revoke_a_b_untouched_and_survives_a_fresh_ledger`,
which walks Bill's steps and compares both readers at every one.

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
