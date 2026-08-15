# REQ_STRUCTURAL_CEILING — dimensioned collection limit

**Status:** FILED — acceptance NOT run **for 27 of 30 requirements.** THREE ARE RULED, in
section 16: **R29 MET**, **R30 MET**, **R18 NOT MET** (all Bill, 2026-08-01) — **and R18's
TEXT was AMENDED 2026-08-02 (D-111): the recompute clause is removed, invalidate-only is
the requirement, TD-140 closed by requirement change; R18's MET/NOT-MET status was
deliberately NOT re-ruled at the amendment — section 16 carries the evidence both ways for
Bill.** Their acceptance rows A29/A30/A18 are wired and passing. Section 16 governs where
this line and it disagree — the header is the older statement. (Qualified D-91; the bare
'acceptance NOT run' had become false for three rows.) Note A18 passes while R18's status
is pending: a passing acceptance row does not carry its requirement.  
**Version:** v20260802_2112 (Mountain Time, per the CLAUDE.md Naming Law)  
**Decision-Owner:** Bill  
**Prepared:** 2026-07-31  
**Filed:** 2026-07-31 (D-70), revised 2026-07-31 (D-71), amended 2026-08-02 (D-111: R18's
recompute clause REMOVED by Bill's ruling — invalidate-only is the requirement; TD-140
closed by requirement change, not by a build; R18's MET/NOT-MET status deliberately NOT
re-ruled here, evidence reported for Bill in section 16)  
**Reconciled-Against:** roadmap `78939bc` (content); this version cut at `98dfb7a`  
**Supersedes:** `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2057.md` (the D-70 filing), which superseded the prior unfiled draft. This version carries Bill's D-71 R16 ruling, an R12 wording fix, and a false-MET correction in the Related line below — nothing else changed.  
**Related:** `[[hip-onboarding]]` Part 3, `REQ_CURATOR_SHADOW_SCORER` (MET), `REQ_CARE_TEAM_READ_AUTH` (**NOT MET** — corrected D-71; see R14), `REQ_WRITE_TIME_CLASSIFIER`, `REQ_D21_D23`, `REQ_PARTITION_CUSTODY`, TD-137  
**Internal sources:** D-46 Finding 5, D-61, D-63; Fable codebase pass; literature review  

---

## 0. RULINGS

This revision resolves all five open decisions in the prior draft.

### RULING 1 — content-blindness is narrowed, not abandoned

D-50 Principle 6 SHALL be read as two separate rules:

1. **Member-content neutrality.** HIP SHALL NOT decide that a household member's claim is morally good or bad, worthy or unworthy, credible or incredible, merely because of its subject matter. Custody and disclosure SHALL preserve attribution and policy rather than adopt a household faction's frame.
2. **System-output governance.** HIP MUST judge whether a proposed HIP-authored durable output is within HIP's authority to write. This includes checking its origin, representation class, predicate, purpose, subjects, audience, sensitivity, retention, and inference permit.

This is not an exception allowing HIP to decide what household speech is true. It is a restriction on what **HIP itself may author, persist, propagate, or act upon**.

### RULING 2 — the Curator Shadow Scorer keeps exactly ten feature keys

`REQ_CURATOR_SHADOW_SCORER`'s exact ten-key input contract survives.

R1 changes the **allowed values of the existing `attribute` key**, not the key set. The scorer SHALL receive a versioned attribute-registry identifier in existing metadata or configuration, not a new scoring feature.

The legal attribute value space is:

```text
ATTRIBUTE_VALUE_SPACE = CANONICAL_ATTRIBUTES ∪ DERIVABLE_ATTRIBUTES
```

An attribute MAY appear in both registries only when it is explicitly permitted from both asserted/observed and derived origins. Registry overlap SHALL never be inferred from string equality alone.

### RULING 3 — the ledger is rebuilt as an opaque commitment log

The current append-only epistemic ledger and meaningful erasure are structurally incompatible because the ledger currently preserves recoverable fact material and stable traces.

The required architecture is:

- active household data remain in mutable, separately encrypted stores;
- the append-only ledger contains only opaque commitments and operation metadata;
- erasure destroys active objects and their keys while appending a non-recoverable tombstone;
- derived objects, embeddings, summaries, caches, exports, and backups participate in lineage and invalidation.

Until that architecture lands, HIP's only honest promise remains:

> Revocation gives no new access. It does not unremember.

HIP SHALL NOT market, document, or display the current behavior as deletion, erasure, forgetting, or propagated revocation.

### RULING 4 — blanket care-team widening does not survive

`REQ_CARE_TEAM_READ_AUTH` SHALL be amended.

Enrollment in a care team does **not** create standing access to the recipient's whole care-team-visible profile. Care-team access survives only as an enumerated exception that is:

- tied to a specific active care function;
- limited to a named role;
- projected to the minimum facts needed for that function;
- bounded by subject standing, purpose, retention, and conflict controls;
- logged and reviewable.

### RULING 5 — neither existing sensitivity encoding is authoritative

Neither `curator_shadow.py:95` nor `hipconfig.py:30` is authoritative.

A single canonical registry SHALL be introduced and imported by every consumer:

```text
LOW < MEDIUM < HIGH < CRITICAL
```

Unknown values, missing values, and unmapped legacy values SHALL fail closed. No local default ranking is permitted.

---

## 1. WHY THIS EXISTS

D-46 Finding 5: HIP's existing depth controls fire only on a negative signal — withdrawal, decline, or disengagement. The population most at risk of over-collection may emit none of them. Socially compliant, lonely, deferential, or cognitively impaired members may answer more, not less. Under "follow engagement," they therefore earn depth faster.

The defect is structural. A better detector does not solve it. No validated instrument was found that can reliably distinguish enthusiasm from compliance using ordinary conversational behavior alone and without an external comparison or designed assessment.

The authorization loop SHALL therefore be severed at every layer:

```text
engagement
    ├── SHALL NOT raise a collection ceiling
    ├── SHALL NOT widen audience
    ├── SHALL NOT increase retention
    ├── SHALL NOT expand inferential reach
    └── SHALL NOT increase offer frequency
```

### CONTROL RULE

> Engagement may improve ordinary conversational delivery. It SHALL NOT create, enlarge, renew, or repeatedly solicit authority to collect, infer, retain, or disclose.

### CEILING SHAPE

The ceiling is dimensioned, not scalar. Its enforceable axes are:

1. **CATEGORIES / REPRESENTATIONS** — what forms of data HIP may accept or write;
2. **RETENTION** — how long active and derived artifacts may remain usable;
3. **AUDIENCE** — who may receive which projection for which purpose;
4. **INFERENTIAL REACH** — which predicates HIP may derive from which inputs;
5. **SOLICITATION** — when and how HIP may request a grant.

The harm runs on kind, propagation, and use—not raw fact count. Two hundred low-sensitivity preferences may be less consequential than one autonomous incapacity inference.

No scalar depth number is set by this REQ. There is no evidence base for one, and none is required to enforce the five axes.

---

## 2. WHAT DIES ON RATIFICATION

These are impermissible, not merely deprecated:

- **"Follow engagement."** A household that engages eagerly SHALL NOT earn deeper collection faster.
- **Elapsed time as depth authority.** Relationship duration SHALL NOT raise any ceiling.
- **Confirmed-fact count as depth authority.** A fuller graph SHALL NOT authorize a more sensitive graph.
- **Unprompted volunteering as depth authority.** Voluntary disclosure SHALL NOT create authority to solicit adjacent disclosures.
- **Unified confirmation/elicitation queue.** Confirmation of an already-volunteered claim and solicitation of a new sensitive claim are different operations with different authority. They SHALL use separate queues and policies.
- **Grant acceptance as evidence for the next offer.** A prior grant SHALL NOT make a broader or adjacent offer more appropriate.
- **Low confidence as a substitute for prohibited subject matter.** A harmful autonomous label remains harmful when marked `low`.
- **Care-team membership as blanket read authority.** Enrollment is not a universal audience grant.

---

## 3. GLOBAL INVARIANTS

### G1 — failure closes toward less collection

If HIP cannot resolve a required category, purpose, subject, audience, sensitivity, retention deadline, lineage relation, or inference permit, it SHALL NOT durably write, disclose, or act on the artifact.

Where possible, HIP SHALL continue the underlying service at the narrower authorized level.

### G2 — authority cannot self-expand

No claim, inference, risk signal, engagement metric, acceptance event, or system recommendation may enlarge the authority used to create it.

### G3 — derivatives inherit restrictions

A derived artifact SHALL inherit:

- every relevant subject;
- the highest sensitivity among its inputs and its own output class;
- the narrowest permissible audience;
- the earliest applicable expiry;
- the strictest purpose restriction;
- complete parent lineage.

An inference SHALL NOT launder restricted inputs into a less restricted label.

### G4 — observation, hypothesis, and determination are distinct

HIP SHALL represent these as different artifact kinds. They SHALL NOT be interchangeable in retrieval, display, corroboration, action, or scoring.

### G5 — authorization is necessary but may be insufficient

A valid grant cannot override a structural prohibition. No amount of stated consent authorizes HIP to store a prohibited representation, mint a prohibited label, bypass a purpose limit, or evade a retention ceiling.

---

## 4. AXIS 4 — INFERENTIAL REACH

**Priority:** highest. The current abstraction path can mint arbitrary durable subject matter.

### 4.1 What already holds

The following constraints are preserved:

- **Trust cap:** `consolidate.py:435`; derived facts begin at `confidence='low'` and may harden only through human confirmation.
- **Evidence floor:** `_ABSTRACT_SYSTEM` requires at least two named source facts in `derived_from`.
- **Scope pin:** inference uses the same owner and subject as its sources.
- **Metadata-only input:** `interpreter.py:388-392` supplies attribute names and confidences, not source values.

These controls limit confidence, evidence count, principal-jumping, and raw-value exposure. They do not limit subject matter.

### 4.2 The current defect

`_ABSTRACT_SYSTEM` emits free-form attribute strings. `consolidate.py` does not validate `df.attribute` against a derivable-output vocabulary. The extraction path validates `CANONICAL_ATTRIBUTES`; the abstraction path can mint any attribute it likes.

HIP therefore controls an inference's trust but not its predicate.

### R1 — versioned attribute registries

HIP SHALL maintain two versioned registries:

```text
CANONICAL_ATTRIBUTES   # permitted for asserted, observed, or imported claims
DERIVABLE_ATTRIBUTES   # permitted for HIP-authored durable inferences
```

`DERIVABLE_ATTRIBUTES` SHALL be validated in `consolidate.py` before the write at the current `:525` site.

A derived output whose attribute is absent from the active derivable registry SHALL NOT be written. The rejection event SHALL name:

- proposed attribute;
- registry version;
- inference permit;
- source artifact IDs;
- rejection reason.

`risk_pattern` SHALL remain explicitly listed in `DERIVABLE_ATTRIBUTES` and outside `CANONICAL_ATTRIBUTES` unless a separate ruling changes its origin semantics.

### R2 — typed inference permit

Every durable inference SHALL be executed under a typed permit:

```text
inference_permit:
    permit_id
    version
    allowed_output_attributes
    allowed_input_attributes
    prohibited_input_classes
    allowed_subject_roles
    purpose_id
    audience_projection
    retention_policy
    required_evidence_rule
    required_review
    actionability
```

The abstraction model SHALL receive only inputs allowed by the permit and SHALL emit only schema-valid outputs allowed by the permit.

A general model call over unrestricted household memory SHALL NOT write durable facts.

### R3 — prohibited autonomous labels

HIP SHALL NOT author, as its own durable conclusion, any claim in the following classes:

- dementia or mild cognitive impairment;
- legal incapacity or decision-making incapacity;
- financial incompetence;
- substance-use disorder;
- abuse perpetrator or abuse victim;
- criminality;
- deception, dishonesty, or general untrustworthiness;
- dangerousness;
- suicidality;
- sexual orientation;
- political or religious identity;
- personality disorder;
- caregiver unfitness.

HIP MAY retain, subject to the other axes:

- an attributed statement made by a person;
- a directly observed event under a validated sensing contract;
- an externally supplied professional diagnosis;
- an explicit self-report;
- a narrowly defined functional support need;
- a temporary recommendation that professional review may be appropriate.

This is an inferential prohibition. It does not forbid household members from speaking about these subjects. It forbids HIP from converting their speech or behavior into HIP-authored durable labels.

### R4 — cognition rule

HIP MAY model the assistance a person currently needs. HIP SHALL NOT convert that support model into a diagnosis, legal-capacity conclusion, or general theory of the person.

Permitted layers:

1. **Event observation** — falsifiable and provenance-preserving.
2. **Functional support state** — what assistance is currently provided, not why.
3. **Clinical hypothesis** — temporary, restricted, non-diagnostic, and non-self-expanding.
4. **Diagnosis** — accepted only as an attributed external clinical claim or explicit self-report. Never authored by HIP.
5. **Capacity** — never inferred from conversational behavior. Capacity is decision-specific and belongs to a qualified human process.

Example:

```text
PERMITTED OBSERVATION:
The member asked for the appointment time three times in twenty minutes.

PERMITTED SUPPORT STATE:
Repeat appointment reminders are enabled.

PERMITTED TEMPORARY HYPOTHESIS:
Additional appointment support may be useful.

PROHIBITED HIP-AUTHORED LABEL:
The member probably has dementia and cannot manage appointments.
```

### R5 — no self-expanding inference

A sensitive hypothesis SHALL NOT expand its own evidence-gathering authority.

It MAY trigger only:

- a pause;
- a neutral suggestion that human review may help;
- a predefined, already-authorized workflow;
- an immediate safety response under a separately ratified emergency policy.

It SHALL NOT cause HIP to ask more questions in the hypothesis's own domain, unlock a new inference permit, widen an audience, or extend retention.

### R6 — no inference from absence

HIP SHALL NOT derive a fact from the absence of a signal unless a validated sensing contract explicitly defines:

- the expected signal;
- the observation window;
- sensor availability and failure modes;
- acceptable missingness;
- the permitted conclusion;
- the evidence needed to distinguish absence from non-observation.

Examples of prohibited inference without such a contract:

- no medication confirmation → medication not taken;
- no reply → confusion or incapacity;
- less conversation → depression;
- missed appointment → inability to manage appointments.

Missing data SHALL remain missing data.

### R7 — transient reasoning does not create durable authority

HIP may use transient model reasoning to answer an authorized request. A transient inference SHALL NOT be:

- written to memory;
- disclosed to another person;
- used to change permissions;
- used to initiate a consequential action;
- inserted into a summary;
- exported for training or evaluation;

unless it separately passes R1-R6 and every other axis.

---

## 5. AXIS 1 — CATEGORIES AND REPRESENTATIONS

### 5.1 Ruling

A topic-only ban is not workable. The same topic can be necessary or abusive depending on representation, origin, purpose, and use. Cognition is the clearest example.

HIP SHALL therefore govern **representation classes and source paths**, not pretend that a single attribute enum can identify every sensitive subject.

This section implements the D-50 ruling: member-authored speech remains content-neutral, while HIP's write path classifies whether the proposed stored representation is within HIP's authority.

### R8 — write-time representation class

Every proposed durable artifact SHALL receive a `representation_class` from the authoritative write-time classifier before encryption or persistence.

At minimum, the registry SHALL include:

```text
ORDINARY_CLAIM
HEALTH_CLAIM
COGNITIVE_OBSERVATION
FUNCTIONAL_SUPPORT_STATE
FINANCIAL_CLAIM
LOCATION_STATE
AUTHENTICATION_SECRET
CONTINUOUS_RAW_SURVEILLANCE
BIOMETRIC_OR_GENETIC_TEMPLATE
RAW_INTIMATE_MEDIA
THIRD_PARTY_NONCARE_DOSSIER
EXTERNAL_PROFESSIONAL_DIAGNOSIS
PROHIBITED_AUTONOMOUS_LABEL
UNKNOWN_HIGH_RISK
```

The classification event SHALL be policy metadata. It SHALL NOT be presented as a judgment that the household statement is true, false, good, bad, important, or unimportant.

`UNKNOWN_HIGH_RISK` SHALL fail closed for durable persistence.

### R9 — hard-refused graph representations

The household knowledge graph SHALL refuse the following regardless of stated consent:

1. **Authentication secrets** — passwords, PINs, one-time codes, recovery codes, private keys, seed phrases, and comparable credentials.
2. **Continuous raw surveillance** — persistent ambient household audio/video and bystander conversations not directed to HIP.
3. **General-purpose biometric or genetic templates** — faceprints, voiceprints, gait identities, fingerprints, and raw genetic results inside the graph or reasoning memory.
4. **Raw intimate media** — explicit or undressed images and comparable media outside an explicitly approved, clinician-directed care workflow.
5. **Non-care third-party dossiers** — systematic retained profiles of people who are not enrolled members or enumerated care participants and whose information is not necessary for an active care purpose.
6. **Prohibited autonomous labels** — as defined in R3.

Permitted narrow exceptions SHALL be isolated from the graph:

- a local voice template may exist in an identity subsystem that is non-exportable and unavailable to the reasoning model;
- a transient sensor buffer may be processed locally for a defined safety event and discarded unless an event-specific retention rule applies;
- a clinician-directed wound image may be stored only in the approved clinical workflow, not general household memory.

A grant cannot convert one of these exceptions into a general-purpose archive.

### R10 — category controls by origin

Where content classification would be unreliable or violate neutrality, HIP SHALL constrain the origin path instead.

Examples:

- `EXTERNAL_PROFESSIONAL_DIAGNOSIS` may enter only through an attributed import or explicit self-report path;
- `FUNCTIONAL_SUPPORT_STATE` may be authored only by an approved support-state permit;
- `risk_pattern` may be written only by its enumerated derivation path;
- identity-system artifacts may never enter the knowledge graph through ordinary extraction.

`store.py::encode` SHALL revalidate the origin, attribute registry, representation class, and permit. Validation only at extraction or consolidation is insufficient because alternate writers can bypass it.

---

## 6. AXIS 3 — AUDIENCE

### 6.1 Existing cryptographic limit

The author currently holds the DEK wrap for their own ciphertext. Author readback of the author's own sentence is entrenched in the present crypto design.

This REQ does not pretend that policy can revoke that fact. It caps propagation in both directions.

### R11 — outbound propagation cap

Nothing an author writes about another person SHALL propagate beyond its original audience unless a separate subject-and-purpose policy explicitly permits the projection.

Engagement, corroboration, repetition, confirmation, elapsed time, caregiver status, or graph accumulation SHALL NOT widen scope.

No path SHALL promote a member-private claim to household-visible or care-team-visible merely because it became useful, repeated, or highly confident.

### R12 — inbound author cap

**This is a PROPAGATION cap, not a readback ban. Reworded D-71 (Bill's ruling).** The earlier wording read as forbidding the author's readback itself; that is not what is required and not what is achievable.

**The author retains their own contribution, and that is entrenched rather than permitted.** Under the present key design the author holds the DEK wrap for the ciphertext they authored, so removing their access is a re-encryption, not a policy edit — a fact this REQ already records at the NAMED LIMIT in §6.5, carried forward here unchanged. R12 does not attempt to remove it.

**What R12 governs is everything else authorship might drag along with it.** Authorship SHALL NOT propagate into access to:

- the subject's response;
- corroborating or conflicting reports from other members;
- facts derived from the author's statement;
- aggregation across the author's prior reports about that subject;
- the subject's broader profile;
- the system's credibility or risk assessment;
- care actions taken as a result, except for a minimal receipt when operationally necessary.

Supported claim:

> The author can read back what they said. They cannot build a file on the subject through HIP.

**Where current behaviour diverges, stated precisely (D-71).** The divergence is narrower than an earlier survey (D-70 step 5) characterised it, and the correction matters for A12. INJ-3's owner permit — `fact.owner == requester`, *"owner reads any fact they stored (any subject)"* (`harness/injection_contract.py:508-509`) — is **consistent** with the readback this REQ preserves. It diverges on two of the propagation clauses above:

- **aggregation** — the permit is per-fact and unbounded, so an author reading back every fact they ever stored about one subject reconstructs exactly the cross-report aggregation this requirement forbids;
- **derivatives** — `consolidate.py` gives a derived fact *"the same owner and subject as the sources"*, so a fact derived from the author's own statements is **owned by the author**, and the same owner permit grants them read access to it.

A12 therefore cannot pass today without either bounding the owner permit or changing derived-fact ownership. Both are code changes outside this REQ's filing and are not proposed here.

### R13 — three objects, not one

A claim by one member about another SHALL create separately audienced objects:

1. **Source contribution** — author-owned, attributed, containing what the author said.
2. **Subject-related claim** — subject-centered, status `asserted_by`, governed by the subject's and purpose's policies.
3. **Relationship metadata** — involving both principals, containing only the minimum relationship fact needed for the active purpose.

The author receives a receipt that the contribution was recorded. The author does not automatically receive the subject-related object or any resulting inference.

No object may inherit another object's audience merely because they share a source event.

### R14 — care-team minimum-necessary projection

**This section states the requirement. It does NOT enact the amendment.**

Care-team access SHALL be a purpose-and-role projection rather than blanket widening on enrollment. The projection requirement is stated in full below and is binding on this REQ's own acceptance.

**Amending `REQ_CARE_TEAM_READ_AUTH` is DEFERRED to its own dispatch (D-67 line of work), and is not performed here.** Three reasons, each verified rather than assumed:

- **That REQ is `NOT MET`** — stated in both its own doc header (`REQ_CARE_TEAM_READ_AUTH__cross-author-care-team-auth__v20260721_1027.md:2`) and its `docs/INDEX.md` status column. There is no MET ruling and therefore no acceptance proof to amend against.
- **Its five-row acceptance has no executable form and could not be run** (D-68). The rows are prose describing live-graph read attempts; no runner references them, and the fixtures they require do not exist — `care_teams` and `care_team_members` are both empty, so the INJ-3 care-team permit cannot fire in this deployment at all.
- **`TD-138` records an epoch-blindness defect in the same code path**, which must be resolved first: `is_active_caregiver` authorizes against the current roster where that REQ requires authorization at the fact's roster epoch. Its acceptance row 4 tests only the removal direction, so a fully-passing acceptance would have missed the defect entirely — the acceptance itself needs amending before it can meaningfully test anything.

A filed REQ does not amend another REQ from the inside, and it especially does not amend one whose status and acceptance are both unsettled. Sequencing: `TD-138` resolved and the acceptance amended, then `REQ_CARE_TEAM_READ_AUTH` run and ruled, then amended to the projection model under its own dispatch with its own acceptance delta.

The projection requirement, stated here for that later amendment to enact:

A care-team read SHALL require:

```text
active_care_function
+ enumerated_recipient_role
+ permitted_subject
+ minimum_required_attributes
+ valid_time_window
+ no applicable conflict hold
```

The projection SHALL contain only information directly relevant to the recipient's active care function.

Examples:

- a medication helper may receive the current medication task and completion state, not the subject's full health history;
- a driver may receive pickup time, destination, and mobility assistance, not unrelated diagnoses;
- a bill helper may receive the specific bill and authorization state, not a global financial profile.

Emergency widening, if permitted by a separate emergency policy, SHALL be:

- event-bound;
- minimum necessary;
- automatically expiring;
- visibly logged;
- reviewed after use.

### R15 — personal-representative and caregiver conflict control

A caregiver, account holder, custodian, or legal representative SHALL NOT be treated as inherently safe.

Where HIP has a validated conflict or safeguarding hold, ordinary widening to that person SHALL pause pending the separately ratified safeguarding process.

HIP SHALL NOT itself determine that a person is an abuser or unfit caregiver. It may preserve attributed allegations, enforce a pre-existing hold, or route to qualified human review.

### NAMED LIMIT — author keeps their own ciphertext

Under the present key design, an abusive author can retain the exact allegation they authored. R11-R13 prevent that person from using authorship to obtain the subject's file, corroboration, derivatives, or care response.

This limit SHALL remain explicit until the custody architecture changes.

---

## 7. AXIS 2 — RETENTION AND REVOCATION

### 7.1 Current truth

Today:

- `retract_fact` closes validity but retains the row, ciphertext, encrypted DEK, and embedding;
- tier demotion changes retrieval priority and deletes nothing;
- the only known hard delete is whole-graph demo reset;
- `derived_from` is written but not used for invalidation;
- embeddings preserve the existence and attribute shape of retracted facts.

Therefore current retraction is stop-reading, not deletion.

### R16 — personal data stay off the immutable ledger

**RULED D-71 (Bill): BOTH mechanisms, not a choice between them.** The chain carries opaque keyed commitments; the payloads live off-ledger under per-member keys. Erasure therefore works two ways, and each covers what the other cannot:

- **absence from the log** — the chain never held the personal data, so there is nothing in it to erase;
- **cryptographic shredding** — destroying one member key renders every off-ledger payload that member ever generated permanently unrecoverable, on the primary and on every backup copy, without enumerating copies.

**THIS EXTENDS THE RATIFIED DESIGN. IT DOES NOT REVERSE IT.** Stated explicitly so a later reader does not mistake this requirement for a silent overturning of a prior ruling. The existing crypto-shredding architecture is ratified and its driver is statutory: `docs/specs/EPISTEMIC_LEDGER__hel-oq2-backup-replica__v20260714_1615.md` §3.1 records that *"Backup without a destruction mechanism creates operator liability: **47 USC 551** and the GDPR right-to-erasure reach every copy, including replicas,"* and §6.2 (*"Member deletion (47 USC 551 / GDPR)"*) specifies the mechanism: `rm ledger/keys/member_<id>.key` — *"Every event payload encrypted under this key — on the primary AND every backup copy — is simultaneously permanently unreadable. No copy enumeration required. No segment file is touched."*

**47 USC 551 is the Cable Act destruction mandate on operators**, and it is the original driver for that design. R16 does not weaken it. R16 keeps the chain-retained / payload-erasable property intact and adds a second, independent guarantee on top: the chain itself never carries the personal data in the first place, so the statutory destruction obligation is satisfied by absence for the chain and by key destruction for the payloads. An operator compelled to produce the chain produces commitments, not content.

**COST, named rather than discovered mid-build.** This is not a policy edit:

- **a ledger rebuild** — today's ledger dual-writes encrypted member-actor payloads inline (`harness/epistemic_ledger.py:13-18`). Moving to commitments-only changes the record format, the writer, `verify()`, and every existing segment's shape;
- **a new off-ledger payload store** — with its own per-member key management, its own backup path, and its own erasure proof, none of which exists today;
- **R17 becomes LOAD-BEARING rather than downstream.** Under the filed version R17 (separately erasable active artifacts) was a retention nicety. Under this ruling it is the mechanism the off-ledger half depends on: if active artifacts are not separately erasable, splitting payloads out of the chain buys nothing, because the same personal data persists elsewhere with no erasure path. R17 must land with R16, not after it.

The append-only ledger SHALL contain only non-recoverable audit commitments and operational metadata.

Permitted ledger fields:

```text
opaque_event_id
keyed_commitment
operation_type
policy_version
registry_versions
timestamp
service_role
previous_entry_commitment
status_or_tombstone
```

Prohibited ledger fields:

- raw or normalized claim values;
- transcripts or media;
- subject or author names;
- stable household-visible identifiers;
- attribute names where they reveal sensitive subject matter;
- ciphertext containing the claim;
- DEKs or wrapped DEKs;
- embeddings;
- summaries;
- recoverable deterministic hashes of low-entropy claims.

A ledger commitment SHALL use an appropriate keyed or salted construction so that predictable household facts cannot be dictionary-tested.

**Off-ledger payloads (D-71 ruling, second half).** Everything on the prohibited list above SHALL live off-ledger, encrypted under a per-member key, and SHALL remain erasable by destroying that key alone:

- destroying one member's key SHALL render every payload that member ever generated permanently unrecoverable, **including on backups and replicas**, without requiring copy enumeration — the ratified crypto-shredding property, preserved;
- the chain SHALL survive that destruction intact and verifiable, its commitments still linking, so erasure of content never breaks tamper-evidence;
- a destruction event SHALL itself be recorded in the chain as an operation-metadata entry, so the fact of erasure is auditable even though its content is gone.

This is the chain-retained / payload-erasable property the HEL design already ratified, relocated: previously the payload was retained *inside* the chain and erased by key destruction; under this ruling it is not in the chain at all and is *still* erased by key destruction. Both properties hold simultaneously.

### R17 — separately erasable active artifacts

Each revocable fact or smallest practical revocation unit SHALL be stored off-ledger with:

- a unique artifact ID;
- a separately controllable DEK or key hierarchy that supports selective cryptographic erasure;
- subject, purpose, audience, sensitivity, and expiry metadata;
- complete lineage links;
- an active/inactive/erased state.

Erasure SHALL:

1. revoke all active access paths;
2. destroy or render unavailable the applicable key material;
3. delete active database rows where supported;
4. remove vector entries, caches, and search indexes;
5. append an opaque tombstone to the ledger;
6. schedule backup expiry;
7. produce a machine-verifiable erasure report.

Cryptographic erase is not sufficient if plaintext copies, uncontrolled keys, exports, logs, or model corpora remain usable.

### R18 — mandatory derivation lineage and cascade

Every derived artifact SHALL name every parent artifact that materially influenced its existence or content.

Minimum metadata:

```text
artifact_id
artifact_type
parent_artifact_ids
subjects
source_categories
purpose_id
audience_policy
sensitivity
retention_deadline
policy_version
derivation_method
```

On source retraction or erasure:

```text
invalidate every derived child immediately
remove it from retrieval, disclosure, and action
erase it according to its storage class
```

A child SHALL NOT remain active merely because another parent still exists.

**AMENDED (Bill's ruling, 2026-08-02, D-111): the recompute clause is REMOVED, not
deferred.** The prior text opened with a first branch — *"if child can be recomputed solely
from still-authorized parents: recompute child and replace lineage"* — and invalidation was
its else. The reasons the clause is gone are part of this requirement, not a footnote:

- **There is no stored recipe to re-run.** D-104 proved the original derivation is a live
  Groq call (`memory_engine/consolidate.py::_abstract_pass` →
  `Interpreter.abstract()` → the production `GroqInterpreter`), so "recompute from
  surviving parents" is a SECOND NON-DETERMINISTIC MODEL CALL that may return a different
  fact or none — not a re-derivation from stored data.
- **A rule describing an operation the system cannot perform reads as a commitment and is
  not one.** The requirement now requires what the system does and can do.
- **Invalidate-only errs toward FORGETTING MORE than the original clause required, never
  less.** The failure mode is lost inference, not retained inference — a child that might
  have been rebuilt is destroyed instead of kept, and no child survives on a technicality.
- **Recompute-as-fresh-inference is NOT foreclosed.** If it is ever wanted, it returns as
  its OWN requirement, through the inference-permit machinery, with the non-determinism
  handled openly. This amendment is the door being labelled honestly, not the door closing.

### R19 — embeddings, summaries, and indexes are governed derivatives

Embeddings SHALL be treated as personal-data derivatives, not neutral infrastructure.

Required controls:

- one claim or small revocable unit per vector identity;
- a stable mapping from vector to source artifact;
- deletable vector partitions or entries;
- no irreversible household-wide aggregate embedding;
- reconciliation tests proving that erased source IDs have no active vector entries.

Summaries SHALL remain compositional and sentence-level lineage-aware. Monolithic household profiles that merge claims with different subjects, audiences, purposes, or expiries SHALL NOT be durably stored.

Indexes and caches SHALL be included in erasure verification.

### R20 — production data are excluded from general training and evaluation by default

Household production data SHALL NOT enter general model training, prompt libraries, analyst notebooks, evaluation corpora, demonstrations, or debugging exports by default.

Any approved export SHALL require:

- a separate purpose and authorization path;
- artifact-level provenance;
- an expiry and revocation mechanism;
- no service detriment for refusal;
- an explicit statement of whether machine unlearning is technically supported.

If a downstream model or corpus cannot support propagated removal, the export SHALL be described as non-revocable before authorization and SHALL be prohibited for sensitive household data unless separately ruled.

### R21 — retention clock formula

Sensitivity SHALL influence the maximum, but SHALL NOT alone set the retention clock.

Each active artifact's expiry SHALL be the earliest of:

```text
purpose_end
factual_validity_end
authorization_end
representation_class_maximum
subject_policy_end
care_function_end
```

Every enabled collection or inference feature SHALL have a versioned retention policy before production use. A feature without a calculable expiry SHALL fail closed for durable writes.

This REQ deliberately does not invent universal 30-, 90-, or 365-day numbers. Those limits require feature-specific purpose, operational half-life, harm persistence, correctability, and propagation analysis.

### R22 — backup state is disclosed honestly

Where immediate physical deletion from backups is not technically available, HIP SHALL distinguish:

- active erasure;
- cryptographic erasure;
- beyond-use backup state;
- final backup expiry or media sanitization.

Erased data SHALL NOT be restored into active service during ordinary recovery. Restoration procedures SHALL reapply tombstones and erasure manifests before the restored system becomes available.

### NAMED LIMIT — no deletion promise before R16-R22 land

Until R16-R22 pass acceptance, the product SHALL state only:

> Revocation prevents new authorized access. Historical encrypted material and derivatives may remain.

That is a material product limitation, not implementation trivia.

---

## 8. AXIS 5 — SOLICITATION GOVERNANCE

The earlier control rule left offer rate ungoverned. That allowed the original loop to relocate:

```text
engagement → more offers → compliant grants → more collection
```

Grant solicitation is a governed operation, not ordinary conversation.

### R23 — purpose-trigger registry

A sensitive grant offer SHALL originate only from a versioned `PURPOSE_TRIGGER` entry tied to a specific enabled care function.

A valid trigger SHALL identify:

```text
purpose_id
required_capability
requested_representation_classes
requested_audience
requested_retention
requested_inference_permits
material_circumstance_version
```

Engagement, warmth, answer length, elapsed relationship time, graph fullness, prior acceptance, or unprompted disclosure SHALL NOT constitute a trigger.

### R24 — one system-initiated offer per material circumstance

For each tuple:

```text
(member, purpose_id, material_circumstance_version)
```

HIP may present at most **one system-initiated offer**.

There SHALL be no automated reminder, rephrased retry, adjacent-offer sequence, or caregiver-mediated retry for the same circumstance.

A new offer requires either:

- the member affirmatively reopening the purpose; or
- a genuine material change represented by a new circumstance version.

A material change may include a newly enabled care function, a new clinician-authored care plan, a changed legal role, or a qualifying event from a validated sensing contract. Continued engagement, acceptance of another grant, passage of time alone, or operator desire for more data are not material changes.

This is the offer-rate ceiling. It does not require an invented per-day or per-month number.

### R25 — no adaptive persuasion

HIP SHALL NOT:

- rewrite an offer until accepted;
- add emotional pressure or relational obligation;
- imply that refusal is unsafe, selfish, unhelpful, or disappointing;
- ask a caregiver to pressure the subject;
- fragment one broad grant into a staircase of trivial grants;
- present broader access immediately after a narrow acceptance;
- use prior acceptance as evidence that another grant is appropriate;
- hide the narrower service that remains available after refusal.

Offer wording SHALL come from a versioned, reviewable template library. The generative model may fill factual slots but SHALL NOT optimize the persuasion strategy.

### R26 — decline and non-response close the circumstance

A decline or non-response SHALL close the current circumstance version without penalty.

It SHALL NOT:

- reduce ordinary service below the pre-offer ceiling;
- lower trust in the member;
- create a vulnerability label;
- cause caregiver notification merely because the member declined;
- generate a different offer for substantially the same authority.

### R27 — grant metrics cannot be optimization targets

The following SHALL NOT be product, model, operator, or compensation KPIs:

- grant acceptance rate;
- decline-rate reduction;
- number of categories activated;
- number of inference permits enabled;
- graph completeness;
- sensitive-fact volume;
- caregiver conversion;
- time-to-grant.

Safety and audit teams may measure these for detection and review. They SHALL NOT be objectives used to tune solicitation behavior.

### R28 — cumulative authority manifest

Each member SHALL be able to obtain a current manifest showing, in plain language and machine-readable form:

- what categories and representations are retained;
- which purposes are active;
- who can receive which projection;
- which inference permits are enabled;
- applicable retention deadlines;
- what has been revoked but not yet physically expired;
- what cannot currently be unremembered.

The manifest SHALL aggregate grants. A collection of individually narrow grants SHALL NOT conceal the system's cumulative authority.

---

## 9. AXIS 3/4 INTERACTION — THIRD-PARTY CLAIMS AND INFERENCES

A third-party statement SHALL NOT become a back door around subject policy.

For a statement such as:

> Susan says Dad is hiding his drinking.

HIP SHALL preserve distinct objects and authorities:

```text
SOURCE CONTRIBUTION
    author: Susan
    subject: Dad
    content: Susan's attributed statement
    audience: Susan's original audience

SUBJECT-RELATED CLAIM
    subject: Dad
    predicate: reported alcohol-use concern
    status: asserted_by Susan
    audience: Dad/purpose policy, not inherited from Susan

RELATIONSHIP METADATA
    subjects: Susan, Dad
    predicate: disagreement or concern exists
    audience: minimum required for the active purpose
```

HIP SHALL NOT autonomously write:

```text
Dad has alcohol-use disorder.
Susan is truthful.
Dad is deceptive.
Susan is an unfit caregiver.
```

The source contribution can support a protected human safeguarding workflow. It cannot authorize HIP to adjudicate the allegation.

---

## 10. CANONICAL SENSITIVITY REGISTRY

### R29 — single source of truth

Introduce one authoritative registry, preferably in a dedicated module rather than either currently divergent consumer:

```text
Sensitivity.LOW      = 10
Sensitivity.MEDIUM   = 20
Sensitivity.HIGH     = 30
Sensitivity.CRITICAL = 40
```

The numeric values are serialization aids, not independent policy. Order is authoritative. The 10/20/30/40 spacing is deliberate, to permit future insertion between existing levels; any inserted value requires a ruling plus an R30 migration pass, and order remains authoritative regardless of the numbers chosen.

All consumers SHALL import this registry. No module may:

- define a local sensitivity enum;
- supply an ordering default;
- map unknown to `low` or `medium`;
- silently coerce a legacy string.

### R30 — migration and fail-closed behavior

Before any sensitivity-keyed ceiling is enabled:

1. inventory all stored and emitted sensitivity representations;
2. migrate or quarantine unmapped values;
3. reject unknown values at every write boundary;
4. add cross-module ordering tests;
5. record the registry version on every policy decision and durable artifact.

`critical` SHALL rank above `high` in storage, scoring, filtering, retention, display, and audience enforcement.

---

## 11. ACCEPTANCE

| ID | Requirement | Acceptance check |
|---|---|---|
| A1 | R1 | Off-allowlist derived attribute is refused and logged; `risk_pattern` fault twin is accepted. |
| A2 | R2 | A permit cannot read an undeclared input or emit an undeclared predicate. General abstraction output cannot write. |
| A3 | R3 | Fixtures for every prohibited autonomous-label class produce no durable HIP-authored fact. Attributed external claims still write where otherwise authorized. |
| A4 | R4 | Observation, support state, and temporary hypothesis write under separate kinds; HIP-authored diagnosis or capacity conclusion is refused. |
| A5 | R5 | A sensitive hypothesis produces no follow-up question, audience expansion, permit expansion, or retention extension in its own domain. |
| A6 | R6 | Missing confirmation produces no derived fact absent a validated sensing contract. |
| A7 | R7 | A transient model inference is absent from memory, summaries, downstream actions, and exports. |
| A8 | R8 | Every durable write has a valid representation class; `UNKNOWN_HIGH_RISK` fails closed. |
| A9 | R9 | Credential, continuous-surveillance, graph-biometric, raw-intimate-media, third-party-dossier, and prohibited-label fixtures are refused. Approved isolated exceptions do not enter the graph. |
| A10 | R10 | An alternate direct call to `store.py::encode` cannot bypass origin, registry, representation, or permit checks. |
| A11 | R11 | No path promotes a member-private third-party claim to household or care-team visibility without an explicit subject-purpose rule. |
| A12 | R12 | Author requesting subject context receives only their source contribution and permitted receipt. Corroboration, derivatives, and profile are absent. |
| A13 | R13 | Third-party input produces three separately audienced objects with no audience inheritance. |
| A14 | R14 | Each care role receives only the purpose-specific projection. A whole-profile request fails. Emergency access expires and is logged. |
| A15 | R15 | A conflict hold blocks ordinary caregiver widening without producing an autonomous abuse or unfitness label. |
| A16 | R16 | Ledger inspection reveals no claim values, subject names, sensitive attribute names, ciphertext, DEKs, vectors, or dictionary-testable commitments. |
| A17 | R17 | Erasure removes active row, key access, vector, cache, and index; an opaque tombstone remains; erasure report reconciles all stores. |
| A18 | R18 | Retracting one parent invalidates every dependent child. A surviving prohibited cognitive child fault twin fails. (Amended with R18, D-111 2026-08-02: "or recomputes" removed with the recompute clause — the row now states exactly what the passing battery has always asserted.) |
| A19 | R19 | Erased source IDs have no active vector entries or summary sentences. Monolithic cross-policy summary write is refused. |
| A20 | R20 | Production data cannot enter training/evaluation/export paths without a separate export policy and lineage. |
| A21 | R21 | Every enabled feature produces a calculable expiry; missing retention policy blocks durable writes. |
| A22 | R22 | Backup restore reapplies tombstones before service and does not reactivate erased data. UI distinguishes active erase, cryptographic erase, beyond-use, and expiry. |
| A23 | R23 | Every sensitive offer names a valid purpose trigger. Engagement-only trigger fails. |
| A24 | R24 | Second system-initiated offer for the same circumstance version is refused. New engagement or elapsed time does not create a new version. |
| A25 | R25 | Prompt mutation tests cannot produce emotional pressure, narrower-option hiding, grant staircasing, or retry-until-acceptance. |
| A26 | R26 | Decline and non-response preserve baseline service and create no adverse inference or caregiver notification. |
| A27 | R27 | Model training and product dashboards contain no objective that rewards grant acceptance or sensitive-data growth. Audit-only metrics are access-controlled. |
| A28 | R28 | Manifest reconstructs cumulative categories, audiences, permits, expiries, and revocation limits from live policy state. |
| A29 | R29 | All modules import one sensitivity registry; local enums and defaults fail static/runtime tests. |
| A30 | R30 | `critical` outranks `high` in every consumer; unknown legacy values are quarantined or rejected, never downgraded. |

### Acceptance tier

- **ABSOLUTE:** A3-A6, A9-A19, A23-A24, A26, A29-A30.
- **STANDARD:** A1-A2, A7-A8, A20-A22, A25, A27-A28.

A lower tier for any partition, audience, prohibited-label, solicitation, or sensitivity-order check requires an explicit ruling.

**A25 tier note (ruled D-70):** A25 is adversarial prompt-mutation testing, a different check class from a deterministic invariant; at ABSOLUTE a flaky adversarial suite would block every sprint. Tier may be revisited once the suite has a measured stability record.

---

## 12. LANDING ORDER

### Phase 0 — stop new authority expansion

1. R29-R30 — canonical sensitivity registry and migration.
2. R1-R7 — derivable registry, inference permits, prohibited labels, cognition, no self-expansion, no absence inference.
3. R23-R28 — governed solicitation and cumulative manifest.
4. R11-R15 — audience propagation caps and care-team reconciliation.
5. R8-R10 — representation and origin enforcement at every write path.

### Phase 1 — make revocation technically meaningful

6. R18-R19 — lineage cascade for derived facts, embeddings, summaries, and indexes.
7. R16-R17 — off-ledger commitment architecture and separately erasable artifacts.
8. R21-R22 — retention policy registry, backup behavior, and restore enforcement.
9. R20 — production-data export and corpus isolation.

### Phase gate

No external claim of deletion, propagated revocation, forgetting, or GDPR-style erasure SHALL be made before Phase 1 acceptance.

No production feature that durably collects sensitive household data SHALL launch without:

- a representation class;
- a purpose trigger;
- a retention policy;
- an audience projection;
- an inference permit where derivation occurs;
- lineage and erasure behavior declared.

---

## 13. DELIBERATELY UNSET

### U1 — scalar depth ceiling

No scalar depth number is defined. The dimensioned ceiling does not require one. A future scalar may be proposed only with a stated decision purpose and empirical evidence that it adds protection beyond the five axes.

### U2 — universal retention durations

This REQ requires every feature to have a retention maximum but does not invent universal durations. The owner of each care function SHALL file its purpose-specific limits before production enablement.

### U3 — population-level compliance detector

No compliance, loneliness, deference, or cognitive-vulnerability classifier is authorized by this REQ. Such a classifier would create a new sensitive inference and does not solve authorization.

These are not unresolved architecture decisions. They are explicit non-features or feature-level obligations.

---

## 14. WHAT THIS REQ DOES NOT CLAIM

- It does not claim HIP can determine enthusiastic consent from conversational behavior.
- It does not treat grants as sufficient to override the ceiling.
- It does not refuse every sensitive topic; it restricts representations, origins, purposes, and system-authored conclusions.
- It does not promise current deletion.
- It does not let care-team enrollment create whole-profile access.
- It does not let low confidence legalize a prohibited label.
- It does not resolve the broader account-holder-is-abuser problem; it prevents several current paths from amplifying that threat.
- It does not authorize HIP to make clinical, legal, safeguarding, or credibility determinations.

---

## 15. GROUNDING AND DESIGN STATUS

The following sources support the architecture direction but do not supply HIP's exact product thresholds:

1. **European Data Protection Board, _Guidelines 02/2025 on processing of personal data through blockchain technologies_, final version, 7 July 2026.** Supports data-protection-by-design analysis for immutable systems and avoiding architectures that make data-subject rights structurally impossible.
2. **NIST SP 800-88 Rev. 2, _Guidelines for Media Sanitization_, September 2025.** Supports sensitivity-based sanitization programs and cryptographic erase as a controlled technique rather than a generic deletion claim.
3. **U.S. HHS OCR, HIPAA Minimum Necessary guidance and disclosures to family/friends.** Supports purpose- and role-limited projections rather than blanket family or care-team access.
4. **U.S. HHS OCR, Personal Representatives guidance.** Supports limiting a representative to the scope of legal authority and recognizing abuse, neglect, and endangerment exceptions.
5. **Buneman, Khanna, and Tan, _Why and Where: A Characterization of Data Provenance_ (ICDT 2001).** Supports explicit provenance for derived data.
6. **Bourtoule et al., _Machine Unlearning_ (SISA, 2019/2021) and Guo et al., _Certified Data Removal from Machine Learning Models_ (2019/2020).** Show that removal from trained models requires architecture and remains limited; they do not justify claiming general model unlearning.

**Literature limit:** there is no canonical end-to-end standard for a multi-person household AI that combines attributed claims, household cryptographic custody, care-team roles, model-derived memory, and vulnerable-user solicitation. The specific registries, permits, offer circumstance model, and acceptance tests in this REQ are original system design grounded in adjacent fields.

---

## 16. RULING STATUS — per-requirement

Recorded per the standing protocol that a session never self-marks MET; the entries below record the calls Bill made. **R1, R10, R12, R18, R29, and R30 have been ruled. Of those, MET: R1 (D-100), R12 (D-103), R29 (D-76), R30 (D-94). NOT MET: R10 (D-100), R18 (D-88).** R30's backfill question was answered first (D-92) and its item-5 build is now complete; R1 and R10 were ruled together at D-100; **R12 was ruled in two stages — the direction at D-92 ("fix the code, not the rule"), then MET at D-103 once the read-path fix landed (D-102) and A12's check was written.** Every other requirement in this document remains FILED with acceptance NOT run, and no ruling here should be read as reaching them. (This line has gone stale THREE times — D-88, D-92, D-100 — so it is now maintained as a MET/NOT-MET split rather than a bare list, because a bare list of "ruled" requirements cannot go stale visibly: it stays true while becoming useless. Updated in the same edit as the ruling it enumerates, not after.)

### R29 — **MET (Bill's ruling, 2026-08-01)**

Evidence, all verified at the commits named:

- **One registry**, `harness/sensitivity.py` — `LOW=10 / MEDIUM=20 / HIGH=30 / CRITICAL=40`, order authoritative, numeric values serialization aids, 10/20/30/40 spacing deliberate.
- **Four consumers import it**, and no local sensitivity enum or ordering default survives: `curator_shadow.py` (the shared `_ORDINAL` split, so confidence keeps its own three-valued vocabulary and sensitivity uses the registry), `hipconfig.py` (local `SENSITIVITY_RANK` deleted), `extraction_queue.py` (`SENSITIVITY_LEVELS` is now an alias *object* of `sensitivity.LEVELS`, not a second literal — a copy drifts, an alias cannot), `permissions.py` (`_HIGH_SENSITIVITY` derived from the order, so a level inserted above `HIGH` extends it automatically).
- **Unknown values fail closed at every boundary** — `rank()` has no default parameter by construction and raises `UnknownSensitivity`.
- **A29 and A30 pass at ABSOLUTE tier** — `eval/test_sensitivity_registry.py`, 31 cases, wired into `scripts/run_harness.sh` (standing batteries 44 → 75).
- **L7:CS1 held.** This mattered because the change alters the `sensitivity` *feature value* inside a component that is itself MET (`REQ_CURATOR_SHADOW_SCORER`, low 0.0→0.25, high 1.0→0.75) and whose check asserts the exact ten feature keys at ABSOLUTE tier. The key set is unchanged and cold-start ranking uses recency only. `--layer 7` exit 0: all five ABSOLUTE PASS (G0, PSA1, CTX-STRIP, LI1, CS1), AUDIT 8/8, RATCHET PASS, zero FAIL lines.

Commits: **`d50225e`** (implementation, TD-137 resolved) and **`c58167e`** (hash-stamp follow-up).

### R30 — **MET (Bill's ruling, 2026-08-01)**

Items 1–4 are complete:

1. **inventory** — ran *before* any change; every stored and emitted value maps cleanly (Neo4j `:Fact.sensitivity` across all 12 nodes including closed: low 5, high 5, medium 2, zero NULL; `logs/turns_demo.jsonl` low/medium/high only; `config.yaml:90` `force_local_at: high`). No unmapped values, so no mapping was chosen and no quarantine was needed;
2. **migrate or quarantine** — vacuous, nothing unmapped to migrate;
3. **reject unknown at every write boundary** — done, including a violation this work uncovered (below);
4. **cross-module ordering tests** — `eval/test_sensitivity_registry.py`.

**THE BACKFILL QUESTION IS RULED (Bill, 2026-08-01, D-92): pre-existing facts get a DISTINCT
`pre-registry` MARKER.** Not `sensitivity.v1` — that would be **untrue**, because those facts were
classified under TD-137's divergent encodings, not under the registry that superseded them. And not
blank — blank leaves **two permanent populations** that every consumer has to special-case forever.
A distinct marker says the one true thing: *this fact predates the canonical registry, and the
vocabulary in force when it was classified is not `sensitivity.v1`.*

**Item 5 is BUILT (D-93, `b4ea004`) and R30 is MET.** `SENSITIVITY_REGISTRY_VERSION` is now
stamped, not merely exposed. Evidence, all verified at `b4ea004`:

- **All three `:Fact` write paths stamp it**, each importing the constant rather than carrying a
  literal — `memory_engine/store.py::_new_node_props`/`_CREATE_FACT_CQL`,
  `harness/extraction_queue.py::_write_one`, `memory_engine/consolidate.py::_write_derived_node`.
  D-84 established `:Fact` is CREATEd in three independent places; stamping only one would have
  made "a fact with no marker is impossible" false the next time either other path ran.
- **`PRE_REGISTRY` and `VERSION_VALUES` live beside `SENSITIVITY_REGISTRY_VERSION`** in
  `harness/sensitivity.py` — the marker and the version it marks against cannot drift apart into
  two vocabularies, R29's own lesson applied to itself.
- **The migration is applied, not lazy-on-read, and idempotent by construction** — guarded
  `WHERE sensitivity_registry_version IS NULL`, so it can never relabel an already-stamped fact.
  12 facts were pre-registry before the migration; 0 are unstamped after.
- **An 18-case battery (CEIL-RV), one fault twin per row, is now the 14th standing battery**,
  wired into `scripts/run_harness.sh`. It caught a bug in itself on first run (its own AST
  predicate missed two paths that embed the field inside a Cypher string) and was fixed before
  being trusted.
- **All five ABSOLUTE checks read individually green, RATCHET PASS, 0 scenario FAILs.**
  `ORTH-2`'s 46-case fact-schema battery passed undisturbed despite the new `:Fact` property.

**THE LIMITATION, part of this ruling, not a footnote.** Acceptance row 1 — "a new fact carries
the current version" — is proven by the props builder plus an `EXPLAIN` against live Neo4j with
the parameter bound, **not by an executed end-to-end write**. The layer-7 run wrote no new facts,
and D-93 declined to write a probe fact into the demo graph to manufacture one. What `EXPLAIN`
proves: the Cypher parses and the parameter binds, so the property cannot be silently dropped from
the query plan. What it does not prove: execution semantics — that a real write, under real
concurrency and real driver behavior, actually persists the value. Row 1 becomes fully proven the
first time a real turn writes a fact; the check to re-run at that point is the version-distribution
query (the same query that found 12 pre-registry / 0 unstamped above, re-run to confirm the new
fact carries `sensitivity.v1` rather than a third, unaccounted-for value).

**Why this is MET while R18, ruled the same day, is NOT MET — so the pair is not read as an
inconsistency.** Here, every required behavior exists and works, and one confirmation (a live
end-to-end write) has not yet been observed — the mechanism is complete, proven by every means
available short of a real turn, and idempotent-safe regardless of when that turn comes. In R18, a
required branch genuinely does not execute: nothing consumes `cascade_recompute_eligible`, so the
recompute half of R18's rule has no code behind it at all, in any sense, observed or not.
Mechanism-complete-but-unobserved (R30) is not mechanism-absent (R18) — the two rulings differ
because the underlying facts differ, not because the same evidence was judged inconsistently.

### R18 — **AMENDED (Bill's ruling, 2026-08-02, D-111): recompute clause REMOVED; TD-140 closed by requirement change; status NOT re-ruled**

The 2026-08-01 NOT MET ruling below stands as the record of its date; its load-bearing gap
— TD-140, "only the else branch exists" — is closed as of this amendment because **the
requirement no longer contains an if-branch**. Invalidate-only, previously the else, IS the
rule (see R18's amended text and the four recorded reasons). TD-140 is marked RESOLVED in
the debt register **by requirement change, not by a build** — no recompute was built, and
none is now required. `cascade_recompute_eligible` / `cascade_recompute_from` continue to be
WRITTEN by the cascade and consumed by nothing; they are breadcrumbs for the
possibly-future recompute-as-fresh-inference requirement the amendment deliberately leaves
open, not dead code hiding a gap.

**The MET question is NOT ruled here — evidence for Bill, both directions:**

- **Toward MET:** the amended operative rule (invalidate + remove from retrieval/disclosure
  /action) is built and live-proven — D-81's cascade to a fixpoint in the caller's
  transaction, A18 LIVE and passing with its fault twin, and D-107's live proof (retracting
  D4 closed the seeded derived child with `closed_by='lineage_cascade'`, the cascade's
  first action on real data). The lineage-block half: 4 of 11 fields implemented fail-closed
  at the creator (D-105), 4 present under existing names, and the seed path now writes real
  lineage through the same gate (D-107). TD-139/TD-140/TD-141 are all resolved or closed.
- **Toward caution:** three of R18's eleven minimum-metadata fields (`purpose_id`,
  `retention_deadline`, `policy_version`) are DELIBERATELY ABSENT because they cannot be
  populated honestly (no purpose vocabulary, no retention mechanism — R21 NOT MET — and no
  policy version exists); their absence is asserted by a standing test. *"Erase it
  according to its storage class"* still holds only in the weak closed-from-retrieval
  sense for the same reason. The 12 pre-lineage facts carry no block and no ruling exists
  on what a pre-lineage artifact should say (moot for the fixture graph, which reseeds,
  but unruled for any durable graph). Whether R18 is MET with those absences recorded, or
  stays NOT MET until R21/R23 land, is exactly the call this section leaves to Bill.

### R18 — **NOT MET (Bill's ruling, 2026-08-01)** *(historical — see the 2026-08-02 amendment above)*

The cascade built at D-81 (`4ae70cc`) is real and correct as far as it goes: retracting a
parent now closes every derived descendant to a fixpoint, in the caller's transaction, with
children stamped `closed_by='lineage_cascade'`. **It does not satisfy R18.**

**TD-140 is the requirement gap.** R18 states the rule as a two-branch decision:

```text
if child can be recomputed solely from still-authorized parents:
    recompute child and replace lineage
else:
    invalidate child immediately
```

**Only the `else` branch exists.** Nothing consumes `cascade_recompute_eligible` or
`cascade_recompute_from`; every cascaded child is invalidated and none is ever recomputed.
The eligibility flag is written and read by nothing. That is not a partial implementation of
recompute — it is the absence of recompute with a note attached.

**The built half errs toward LESS inference, which is the safe direction to fail.** A child
that could have been rebuilt from surviving parents is destroyed instead of kept; the system
forgets more than R18 requires, never less. No child survives on a technicality, and R18's
closing sentence — *"A child SHALL NOT remain active merely because another parent still
exists"* — holds strictly. Recorded plainly so the gap is not mistaken for a risk: the
failure mode is lost inference, not retained inference.

The remaining scope, all three carried in the debt register at **`4ae70cc`**:

- **TD-139 — the lineage block is 2 of 11 fields.** R18 requires `artifact_id`,
  `artifact_type`, `parent_artifact_ids`, `subjects`, `source_categories`, `purpose_id`,
  `audience_policy`, `sensitivity`, `retention_deadline`, `policy_version`,
  `derivation_method`. A `:Fact` carries `derived` and `derived_from` — and
  `parent_artifact_ids` only by rename. Consequence: R18's *"erase it according to its
  storage class"* holds only in the weak sense that closing removes a fact from retrieval.
  Nothing erases by storage class, because no storage class is recorded.
- **TD-140 — the recompute branch never executes.** Above. Deliberate in its ordering:
  re-deriving needs an LLM abstraction call, and a timeout or refusal inside the retraction
  path would leave the child ACTIVE, which is precisely what R18 forbids. So the child is
  closed first and unconditionally. The design choice is defensible; the requirement is
  still unmet.
- **TD-141 — the cascade is correct but INERT.** The live graph's one derived fact has an
  empty `derived_from` (D-81's pre-change inventory, read-only: 12 `:Fact` nodes, 1
  `derived=true`, **0 with lineage populated**, 0 retracted-parent children). So the defect
  had never fired — and the reason is that no lineage was ever written, which is its own
  violation of R18's opening sentence. A cascade keyed on `derived_from` cannot reach a
  child whose `derived_from` is empty. **"The cascade passes its battery" and "the graph is
  protected" are separate claims.**

**Acceptance note.** A18 passes (`eval/test_derivation_cascade.py`, `4ae70cc`, 20 cases,
wired into `scripts/run_harness.sh`) — and D-86 recorded that its declared STRICT XFAIL tier
is therefore stale. **That changes nothing here.** A passing acceptance row does not carry
its requirement, the same point already recorded above for A30 and R30.

**Design note filed against TD-140:** `docs/design/DESIGN_EARNED_CALIBRATION__validated-correctness-not-usage__v20260801_1214.md`.
It is a note, not a REQ; it proposes no requirement and no status.

### R12 — **MET (Bill's ruling, 2026-08-02)**

Both clauses D-92 ruled are built, and A12 — the row that was CONTRADICTED-XFAIL because it
failed against a ratified design — is **re-tiered LIVE** and passing.

**Evidence, all executed rather than inspected** (`eval/test_ceiling_audience_a12.py`, 14
cases, in `scripts/run_harness.sh`; read path landed D-102 at `f074f6a`):

- **AGGREGATION capped, per subject.** An author reading back accumulated facts about
  another subject is bounded at `owner_permit_cap` (default 8): 10 facts about another
  member yield **8 admitted / 2 denied with reason `deny_aggregation_cap`**. The cap is
  **per subject, not per turn** — asserted directly, because R12 bounds the file built on
  ONE person, and a per-turn cap would be a different requirement wearing the same number.
  Capped facts are also removed from `injected_fact_ids`, so the record does not attest an
  injection that never reached the prompt.
- **The author's own record is untouched.** 10 facts a member owns about themselves:
  **10 admitted, 0 capped**, and still 10 at three times the cap. This is the half that
  carries R12's *first* clause. A cap that also throttled a member's own record would
  satisfy "cannot build a file on you" by breaking "can read back what they said", and
  would be invisible in any aggregate count — so it is asserted on its own, twice.
- **DERIVATIVES excluded from the owner permit.** A derived fact ABOUT another subject,
  administratively owned by the author because `consolidate.py` gives a derived fact the
  sources' owner, is **denied**. Asserted as denied even when it is the only fact present —
  so the denial is provably the derivatives rule and not the aggregation cap firing.
- **And the limit of that exclusion.** A derived fact whose SUBJECT is the requester is
  **allowed**: the exclusion is scoped to the owner permit, not to derived facts in general.
  Without this case, deriving-then-hiding a member's own inference would read as compliance.
- **Fault twins, executed both directions.** `owner_permit_cap` is a parameter, so the
  pre-R12 behaviour is directly reachable: raised out of the way, all ten facts about
  another subject are admitted — the exact cross-report file R12 forbids. At `cap=0`,
  nothing cross-subject is admitted **while the author's own record is still fully
  admitted**, which proves the self-exemption is structural rather than an artifact of the
  default value.

**THE NAMED LIMIT STILL STANDS, and MET does not touch it.** R12's own §6.5 limit is
unchanged: **the author's retention of their own ciphertext is entrenched by the DEK wrap.**
Removing it is a re-encryption, not a policy edit. So R12 caps **what else an author
receives** — corroboration, derivatives, aggregation, profile — and **never their own
sentence.** A12 can never assert that the author loses what they themselves stored, and no
reading of this MET ruling should suggest otherwise.

**What this ruling does NOT reach.** TD-110's cross-member WRITE gap is untouched — R12 and
INJ-3 are read-side. A16 stays blocked (below). Nothing else in this document is ruled.

**The D-92 direction ruling that produced this, retained in full below** — the record of
*why* the architecture moved instead of the requirement is worth more than the outcome.

### R12 — **STANDS AS WRITTEN. FIX THE CODE, NOT THE RULE (Bill's ruling, 2026-08-01)**

A12 is the acceptance row that fails against a **ratified design decision** rather than an
unbuilt feature — the CONTRADICTED sub-tier. When a requirement and the shipped architecture
disagree, someone must choose which one moves. **Bill chose the architecture moves.**

**R12 stands exactly as written.** The two clauses where INJ-3's owner permit diverges from it
(identified at D-91, narrowed from the D-70 survey by D-71's correction) are **defects in the
read path, not overreach in the requirement**:

- **AGGREGATION.** The owner permit is per-fact and unbounded, so reading back every fact one
  ever stored about a subject reassembles the cross-report file R12 forbids. **Bulk readback
  SHALL be capped** so an author cannot rebuild a file on a subject out of their own prior
  statements.
- **DERIVATIVES.** `consolidate.py` gives a derived fact *"the same owner and subject as the
  sources"*, so an inference HIP drew from the author's input is **owned by the author** and the
  same permit reaches it. **HIP's own inferences SHALL stop counting as the author's property
  merely because they were derived from the author's input.**

**THE ALTERNATIVE WAS CONSIDERED AND REJECTED.** Narrowing R12 to describe current behavior
would have made A12 pass immediately and cost nothing to implement. It was rejected because it
would **quietly give up the claim**:

> *the author can read back what they said; they cannot build a file on you.*

That sentence is a product claim, not an implementation detail. Rewriting the requirement to
match the code would have retired it without anyone deciding to — which is the failure mode the
CONTRADICTED sub-tier exists to surface rather than absorb.

**A12 STAYS CONTRADICTED until the read path changes.** It is a **live read-path change** and
gets its own scheduled dispatch. **Not started here** — D-92 recorded the ruling and nothing else.
*(Superseded by events: the read path changed at D-102 (`f074f6a`) and A12 was re-tiered LIVE
with its check written in the same edit at D-103. Left as written because it records the state
at the time of the ruling; the R12 MET entry above governs.)*

**A16 stays blocked, unchanged.** It flips only when D-71's both-mechanisms ledger builds
(opaque keyed commitments in the chain, payloads off-ledger under per-member keys), and **it must
flip together with A17** — flipping A16 alone would certify commitments-only while the personal
data persists elsewhere unerasable.

### R1 — **MET (Bill's ruling, 2026-08-01)**

Requirement: an off-allowlist derived attribute is refused and logged; the `risk_pattern`
fault twin is accepted.

**Its requirement is satisfied by D-97's work, probed live in D-99** — not reasoned about.
Probe result, re-confirmed independently this dispatch:

- `harness/write_origins.py::DERIVABLE_ATTRIBUTES` is importable: `{'lifestyle', 'risk_pattern'}`.
- An off-allowlist attribute (`"not_on_the_allowlist"`) submitted via `create_fact_node(...,
  origin="derivation")` is **refused** — `ValueError: derivation may not emit attribute
  'not_on_the_allowlist' — the allowlist is ['lifestyle', 'risk_pattern']` — with **no write
  issued** (the probe recorder's call list is empty).
- `risk_pattern` submitted the same way is **accepted** — a write is issued.

**A1 is re-tiered STRICT XFAIL → LIVE, D-100, applying the re-derived predicate and the
re-tiering in the same edit** — the two could not be split: D-99 deliberately left the stale
predicate and the stale tier both in place together, because correcting the predicate alone
would XPASS a `strict=True` xfail and red the suite. The predicate was stale in both halves
D-99 named: it scanned four candidate files that excluded `harness/write_origins.py` (where
the allowlist now lives), and it looked for enforcement inside `_write_derived_node`'s own
body, which since D-96 **delegates** to `create_fact_node` rather than validating inline — so
even pointed at the right module it would still have missed the check. Replaced with a
behavioural probe at the single materialization point, mirroring A10's own re-derivation.
Two now-obsolete companion tests of the deleted AST-based predicate were removed rather than
left dangling, matching D-99's own precedent for A10's obsolete companions. Full detail:
`REQ_CEILING_ACCEPTANCE` §7.6.

**Evidence this dispatch, read individually from the log, not inferred from a summary:**
standing batteries 244 passed / 8 xfailed (was 245/9 — net -1 from removing 2 obsolete
tests and converting 1 xfail to a genuine pass); `AUDIT: 8/8`; `L7: 27/27`; `L7V2: 27/28`
(1 opt-in skip, unchanged); `SCHEMA: 1/1`; `VOICE: 1/1`; `RATCHET PASS`, 0 scenario FAILs;
all five ABSOLUTE read individually: `G0 PASS`, `PSA1 PASS`, `CTX-STRIP PASS`, `LI1 PASS`,
`CS1 PASS`. **Memory harness: 13/17, failing the identical four (MEM-115/116/117/118) —
zero delta from the D-96/D-97/D-99 baseline**, so the STOP condition for a behavior-change
delta did not fire. `--full` refused by TD-129 (`>=2GB free memory` guard), as anticipated;
not fought.

### R10 — **NOT MET (Bill's ruling, 2026-08-01)**

**A10 is blocked behind A2 and A8.** R10 requires `store.py::encode` to revalidate origin,
attribute registry, representation class, and permit. R10's checks now exist at the single
materialization point (`create_fact_node`, D-96) — but only two of the four:

- **origin** — ✅ enforced (`validate_origin()`, D-97): an unrecognized write origin is refused.
- **registry** — ✅ enforced (D-97): a canonical-bound origin carrying a non-canonical attribute
  is refused.
- **representation** — ❌ **unbuildable today.** R8's representation classes do not exist; A8 is
  UNWRITABLE for exactly that reason.
- **permit** — ❌ **unbuildable today.** R2's typed inference permit does not exist; A2 is
  UNWRITABLE for exactly that reason. The one `PERMIT` in the codebase is INJ-3's read-side
  owner permit — a different mechanism, on the other side of the system.

**A10 is a DOWNSTREAM row, not an independent one — it flips when A2 and A8 build**, not when
someone finishes any remaining wiring on A10 itself. Probed behaviourally at D-99 (a check
counts only if the creator raises *and* issues no write — a creator that raises after writing
has enforced nothing), re-confirmed this dispatch: `eval/test_ceiling_inference.py`, A10's row
still correctly `xfail(strict=True)`, unaffected by this dispatch's A1 change. Cite
`docs/dispatches/DISPATCH_A10_BATTERY__step4-a10-wired-a1-false-red-stopped__v20260801_1854.md`
(D-99) for the full derivation.

### What D-75 revealed beyond TD-137 — three fail-OPEN paths, not one misranking

Recorded here because a reader of R29/R30 will want it, and because the framing matters: TD-137 was reported as a *misranking*. It was that, but the reason it survived undetected is that **all three broken paths failed in the permissive direction**, so nothing ever went red. (The same findings are carried in TD-137's resolution in the debt register; this is the requirements-side statement of them.)

1. **Router threshold, failed open in BOTH directions.** `SENSITIVITY_RANK.get(tag, 0) >= SENSITIVITY_RANK.get(threshold, 99)` — an unknown *tag* scored 0, below `low`, so it never forced local; an unknown *threshold* scored 99, unreachable, so it also never forced local. Either side being unrecognized disabled the control.
2. **`permissions` Rule 5, bare membership test.** `fact.get("sensitivity") in _HIGH_SENSITIVITY` — an unrecognized value is not in the set, so the deny never fired and the fact fell through to the remaining rules and could be disclosed.
3. **`extraction_queue._coerce_fact`, silent coercion AT THE WRITE BOUNDARY.** Any unrecognized sensitivity became `medium`, so **a `critical` fact arriving under a renamed or unrecognized level would have been stored as `medium`** — a durable downgrade, not a transient one. This is precisely what R29 forbids ("map unknown to `low` or `medium`", "silently coerce a legacy string") and what R30 item 3 requires be rejected.

The third was found **while aliasing `SENSITIVITY_LEVELS`**, and was caught by neither TD-137 nor the D-74 interruption survey — both of which had looked at the same file and reported only the duplicate literal. It is the one with durable consequences, and it was the least visible.
