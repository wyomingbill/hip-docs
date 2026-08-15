# D63_dimensioned-ceiling-axes — Candidate Content for the Four Ceiling Axes

**TWO SOURCES IN ONE FILE.** This artifact carries two independent passes on the
same question, captured verbatim and unedited, in the order they were produced.
They are not merged, not reconciled, and not adjudicated against each other —
where they disagree, both readings stand as filed.

| | Source 1 | Source 2 |
|---|---|---|
| Author | **Fable** (codebase pass) | **ChatGPT** (literature pass) |
| Lines in this file | **42–319**, opening `# D-63 — Candidate content…` | **321–1226**, opening `# Core correction` |
| Method | Grounded in the HIP codebase, read-only, at **HEAD 9acc5a2**; claims marked `[code-verified]` were checked against the repo during the pass | Literature and regulatory grounding; not a codebase read |
| Dispatch | D-61/D-63 line of work | prompted by Bill |

Subject: candidate content for the DIMENSIONED structural ceiling Bill ruled for —
**categories, retention, audience, inferential reach** — which engagement cannot
raise. Scalar depth stays UNSET and instrument-blocked; "Follow engagement" and all
three depth-earning justifications are dead.

Status: BANKED
Verification: UNVERIFIED
Date: 2026-07-31
Version: v20260731_1917 (Mountain Time, per the CLAUDE.md Naming Law)

**No REQ is proposed by this document. It changes no design and no status.** Per the
`docs/reviews/` convention both passes are UNVERIFIED by any separate dispatch unless
one says otherwise. The Fable pass's `[code-verified]` marks attest that a line was
read at 9acc5a2 — not that the conclusion drawn from it is correct.

Note for readers comparing the two: the second pass covers the same four axes and adds
a fifth section, **offer governance**, which the first pass did not scope. The first
pass identified that gap in D-61 (the offer/authorize split leaves offer RATE
ungoverned) without proposing content for it.

Related banked artifacts: `CHATGPT_research-pass4-engagement-authorization.txt` (the
progressive-authorization answer these axes operationalize) and
`FABLE_D61_critique__progressive-authorization__v20260731_1831.md` (its critique
against HIP).

---

# D-63 — Candidate content for the dimensioned ceiling, grounded in the codebase

Gate: PASSED (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap), HEAD 9acc5a2.
Read-only. No lock. No design changed. No status proposed. Nothing banked.

Ruling this serves: adopt a DIMENSIONED structural ceiling — categories, retention,
audience, inferential reach — which engagement cannot raise. Scalar depth stays UNSET
and instrument-blocked. "Follow engagement" and all three depth-earning justifications
are dead.

All findings **[code-verified]** at 9acc5a2 unless marked otherwise.

---

## TWO FINDINGS THAT CHANGE THE SHAPE OF THIS BEFORE THE AXES

**1. HIP already has a category-level write restriction, ratified, and it is the exact
mechanism this axis needs.** `harness/extraction_queue.py:160-167`:

> "`risk_pattern` is deliberately NOT a canonical attribute (Bill, 2026-07-17,
> REQ_D21_D23): it is DERIVED/system-computed, never spoken in first-person
> conversation — **a detector that classifies live utterances should not be able to
> emit a fact type nobody says out loud.** D8's seed keeps this attribute string on
> purpose, outside the enum, as a structural marker that it can only ever be written by
> the derivation path, never detected from a live turn."

That is a per-category, per-write-path restriction, already ruled, already enforced by
omission from the enum. The categories axis does not need a new mechanism — it needs
this one generalized. Worth knowing before designing something parallel.

**2. I overstated inferential reach in D-61, and the correction matters.**
`interpreter.py:388-392` builds the model's input as:

```python
facts_block = "\n".join(
    f'  [{f.get("fact_id","?")}] {f.get("attribute","?")} '
    f'(confidence={f.get("confidence","?")})' for f in episodes)
```

`abstract()` sees **attribute names and confidences only — never values.** So HIP's
inference surface is metadata-over-metadata: it can infer from the co-occurrence of
`medication` + `incident` + `appointment`, but it cannot read what the medication is.
That is a materially narrower reach than my D-61 critique implied, and it is a real
existing control that the inferential-reach axis should build on rather than replace.

---

## AXIS 1 — CATEGORIES

### What HIP already enforces

The collectable vocabulary is 17 canonical attributes (`extraction_queue.py:122-159`):
`medication, allergy, health_condition, dietary, preference, schedule, appointment,
employer, relationship, household, financial, incident, medication_status, address,
zone_district, vitals, care_plan`.

Enforcement is real but **one-sided**: `extraction_queue.py:229` and `:903` both do
`if attribute not in CANONICAL_ATTRIBUTES: return None` — the extraction path refuses
anything off-enum. Two other write paths do not: `memory_engine/store.py::encode` does
not re-validate, and `consolidate.py` never checks `df.attribute` at all (see Axis 4).

### Candidate content — and the eldercare collisions, which are worse than "add a rule"

**The cognition collision is not what it looks like.** There is no `cognition`
attribute to refuse. Cognitive facts are *already collectable today* under
`health_condition` ("Diagnosed or reported health conditions") and arguably under
`incident` ("a discrete reported event — fall, accident, injury, hospitalization").
So a categories ceiling that refuses cognition does not decline to add something —
it must **carve a subject out of two attributes in active use**, which needs a
value-level test that the enum cannot express and that content-blindness (D-50
Principle 6) forbids the system from making.

That is the sharpest finding on this axis: **HIP's category vocabulary is
attribute-shaped, and the categories worth refusing are subject-shaped.** They do not
line up. Any candidate below inherits that mismatch.

| Candidate refusal | Already collectable via | What refusal costs |
|---|---|---|
| Cognition / decline | `health_condition`, `incident` | The core eldercare signal. Refusing it removes the reason the system exists for a declining parent. **Flagged as the obvious collision.** |
| Substance use | `health_condition`, `preference` | Medication-interaction safety. Also the honest-disclosure case D-50's stress-test Case 3 is built on. |
| Finances | `financial` (canonical, in use) | Deletes an attribute already seeded and fixture-covered. Elder financial abuse is precisely what the pass-4 answer says to watch for — refusing collection also removes the ability to notice it. |
| Intimate relationships | `relationship` (canonical, MULTI_VALUED) | Relationship graph is load-bearing for subject resolution and INJ-1. |
| Employment | `employer` (canonical) | Low cost. Plausible candidate with little eldercare value. |
| Municipal zoning | `zone_district` (canonical) | Low cost, but it exists for a reason (D10/D11) I have not traced. |

**The honest reading:** the only cheap refusals are the categories eldercare does not
need, and every category eldercare *does* need is one the pass-4 answer names as
high-risk. The axis is real but it will not buy much unless HIP accepts a
value-level test, which collides with content-blindness.

**Better-shaped candidate, from HIP's own precedent:** rather than refusing categories
outright, restrict them **by write path**, as `risk_pattern` already is. E.g. `vitals`
and `care_plan` writable only via the care-team path, never from a live conversational
turn. This preserves the capability, constrains who may originate it, and reuses a
ratified mechanism.

---

## AXIS 2 — RETENTION: mostly theatre today, and one part is structural

### What is actually enforceable

Three mechanisms exist, and only one of them deletes anything:

1. **`valid_to` tombstone.** `retract_fact` (`extraction_queue.py:644-680`) sets
   `valid_to = ts, closed_by = 'retracted', closed_session = sid`. **The row, its
   ciphertext, its encrypted DEK, and its embedding all persist.** This is a
   stop-reading, not a delete.
2. **Tier demotion.** `consolidate.py` moves facts `hot → warm → cold`
   (`:574, :636, :675, :890`). Demotion changes retrieval priority. It deletes nothing.
3. **One hard delete in the entire codebase:** `server/demo_dashboard.py:1890` —
   `MATCH (f:Fact) DETACH DELETE f`. Nuke-the-whole-graph, demo reset only. There is
   **no per-fact, per-member, per-category, or per-age delete call site anywhere.**

### What is theatre

Any retention promise finer-grained than "delete everything" has no implementing call
site. Specifically:

- **Per-category expiry** — no mechanism. Would be a new build.
- **Per-fact deletion on request** — no mechanism. `retract_fact` is the nearest and it
  does not delete.
- **Embedding expiry — and this one is a live narrow leak.** Embeddings are stored on
  the fact over `"{owner} {attribute}"` only, never the value (TD-030/TD-033,
  `extraction_queue.py:23, 32-38`). Retraction does not clear them. So a retracted
  medication fact leaves a durable, searchable `"bill medication"` vector behind: the
  *existence and shape* of the retracted fact survives its retraction, even though its
  value never entered the vector. Small surface, real, and unscoped.
- **`derived_from` cascade** — written by `consolidate.py:525`, never read for
  invalidation (I checked every occurrence). Retracting a source leaves its derived
  child standing.

### What is structural, not merely unbuilt

The epistemic ledger (`harness/epistemic_ledger.py`) is an append-only hash chain
(`prev_hash`, `payload_sha256`, sealed segments). **Retention limits cannot apply to it
without destroying the tamper-evidence it exists to provide.** This is not a gap to
close; it is two ratified goals in direct conflict, and it needs a ruling rather than a
build.

**Candidate content for this axis, honestly scoped:** the only retention promise HIP can
make today is *"we stop surfacing it, we do not forget it."* That is exactly what
`injection_contract.py:492-493` already says in the codebase's own words — revocation
gives *"no new access, not unremembers ... the same limit as every other revocation in
this codebase."* A retention axis that promises more than that is writing a cheque the
storage layer cannot cash, and the ceiling should say so in those terms rather than
implying deletion.

---

## AXIS 3 — AUDIENCE: the author cannot be narrowed out

### What HIP already enforces

Audience is enforced on **two** layers, which matters for what a ceiling can do:

- **Policy:** INJ-1..7 (`injection_contract.py:5-52`). INJ-3 is the cross-member gate.
- **Crypto:** per-scope DEK wraps. `injection_contract.py:495` — *"an excluded caregiver
  holds no DEK wrap for the fact, so its decrypt already failed and no fact dict for
  them ever reaches this function."* Scope keys exist (household / dyad / care-team);
  **per-member device keys do not** (Part 5's named constraint).

### The reconciliation the dispatch asks for

INJ-3's first permit is `fact.owner == requester` — *"owner reads any fact they stored
(any subject)."* Two consequences for an audience ceiling:

1. **An audience ceiling can narrow who ELSE reads a claim. It cannot narrow out the
   author.** The author wrote the ciphertext and holds the DEK wrap. Removing their
   access is not a policy edit — it is a re-encryption. So "the subject may restrict the
   audience of a claim about them" is buildable *except against the one person most
   likely to be the problem*, which is the same shape as Part 5's
   account-holder-is-abuser limit.
2. **The subject has no standing in the read path at all.** Not reduced standing —
   none. INJ-3 asks whether the requester is the owner, the subject, or an enrolled
   caregiver; the *subject of the claim* has no veto over the *owner's* access.

**Candidate content:** the defensible audience ceiling is a cap on *propagation* — how
far a claim spreads beyond its author — not a cap on the author. Concretely: default
`recipient_ref`-scoped claims to care-team-private (already the `vitals`/`care_plan`
default per REQ_WRITE_TIME_CLASSIFIER), and forbid engagement from widening scope. What
it newly forbids: any path where accumulated engagement promotes a member-private fact
to household-visible. What it costs: nothing currently built, because no such promotion
path exists — this axis is mostly *preventive*, which makes it the cheapest of the four.

---

## AXIS 4 — INFERENTIAL REACH: trust is capped, subject matter is wide open

### What HIP already enforces

- **Trust cap, already there.** `consolidate.py:435` — derived facts are *"always
  confidence='low', tier='hot', derived=True. They can only harden to 'medium' via
  human confirmation (Phase E)."* Inference cannot self-promote.
- **Evidence floor.** `_ABSTRACT_SYSTEM` requires *"each derived fact must be supported
  by ≥2 source facts"* and that `derived_from` name them.
- **Scope pin.** *"Use the same owner and subject as the sources"* — inference cannot
  jump principals.
- **Metadata-only input** (finding 2 above) — the model sees attribute + confidence,
  never values.

That is four real constraints. This axis starts from a stronger position than the
pass-4 answer assumes.

### What is wide open

**Subject matter is entirely unconstrained.** `_ABSTRACT_SYSTEM` emits
`{"attribute": "...", "value": "...", ...}` free-form, and **`consolidate.py` never
validates `df.attribute` against `CANONICAL_ATTRIBUTES`** — the enum is enforced at
`extraction_queue.py:229` and `:903`, both on the *extraction* path only. So
`abstract()` may mint any attribute string it likes.

That is deliberate at least in part: `risk_pattern` exists precisely so derivation can
emit a fact type conversation cannot. But the door is open generally, not just for the
one intended case.

**Candidate content:** a `DERIVABLE_ATTRIBUTES` allowlist validated in `consolidate.py`
before the write at `:525`.

- What it newly forbids: emergent attribute types nobody chose — including whatever a
  model decides to name a cognition pattern.
- What it costs: genuinely useful emergent categories, and it introduces a **second
  vocabulary to maintain**, because the allowlist must contain `risk_pattern` (which is
  deliberately *not* in `CANONICAL_ATTRIBUTES`) while excluding things `CANONICAL_
  ATTRIBUTES` contains. The two enums would overlap without nesting, which is a real
  maintenance cost and a drift risk of exactly the kind that produced the three
  contradictory trust orderings.

---

## COLLISIONS WITH RATIFIED OR MET DESIGNS — surfaced, not resolved

1. **REQ_CARE_TEAM_READ_AUTH (MET, 2026-07-21)** deliberately *widened* audience: a
   care-team-private fact's readable audience is the recipient's whole enrolled care
   team, keyed on live enrollment. Any audience ceiling narrows what a MET REQ
   deliberately opened. Direct collision on Axis 3.
2. **REQ_PARTITION_CUSTODY** — the ratified scope definition INJ-3's care-team permit
   cites. Audience-axis content sits on top of it.
3. **REQ_WRITE_TIME_CLASSIFIER** added `vitals` and `care_plan` to complete the
   coordination/observation enum, and requires they default **care-team-private
   (subject included)**. A categories refusal touching care attributes collides; an
   audience ceiling must preserve this default rather than tighten past it.
4. **REQ_D21_D23 / Bill's 2026-07-17 ruling** on `risk_pattern`'s deliberate exclusion.
   Axis 4's allowlist must preserve it, which is what forces the second vocabulary.
5. **The D-1 record contract + epistemic ledger** — append-only hash chain versus any
   retention limit. Structural conflict, Axis 2.
6. **REQ_CURATOR_SHADOW_SCORER (MET, D-44)** — its declared feature space is exactly ten
   keys including `attribute` and `sensitivity`, and L7:CS1 asserts that set *exactly*
   (ABSOLUTE tier). Removing or splitting a category changes the attribute space the
   scorer sees; a sensitivity-keyed ceiling inherits the `critical` misranking still
   live in `curator_shadow.py:95` and `hipconfig.py:30`.
7. **TD-030 / TD-033 embedding invariant** — the value is never embedded, but the
   subject+predicate vector survives retraction. Any retention promise must state
   whether it covers embeddings; the invariant protects the *value*, not the *trace*.
8. **D-50 Principle 6, content-blind custody** — "the system's protection cannot be the
   thing making a judgment about which content matters." A categories axis that refuses
   subjects rather than attributes requires exactly such a judgment. This is the
   deepest collision and it is with a principle, not a REQ.

---

## THE ONE THING I WOULD PUT FIRST

Axes 3 and 4 are cheap and mostly preventive — they forbid promotion paths that do not
yet exist, and Axis 4's allowlist is a ten-line validation at a single call site
(`consolidate.py`, before `:525`).

Axes 1 and 2 are expensive and partly impossible as stated: the categories worth
refusing are subject-shaped while the vocabulary is attribute-shaped, and retention
finer than "delete the whole graph" has no implementing call site and cannot touch the
ledger at all.

If the ceiling is to ship in a defensible form, the honest split is: **build 3 and 4,
and state 1 and 2 as limits rather than mechanisms** — with retention saying plainly
what `injection_contract.py` already says in code, that revocation is "no new access,
not unremembers."

Nothing banked. No design changed. No status proposed.

# Core correction

The second reviewer is right. **A structural ceiling plus grants still fails unless the system also governs solicitation.** Otherwise the system can repeatedly manufacture authorization opportunities until a deferential user accepts.

The four-axis ceiling therefore needs a cross-cutting fifth control:

> **Grant solicitation is a governed operation, not ordinary conversation.**

Offer frequency, sequencing, reframing, reminders and escalation must be fixed by policy. They cannot be optimized from engagement, acceptance rate, graph completeness or caregiver demand.

The four dimensions also cannot be independent. A health inference is simultaneously:

* a restricted **category**;
* subject to short or event-bounded **retention**;
* visible to a narrow **audience**;
* and produced only through permitted **inferential reach**.

A claim should inherit the most restrictive applicable rule across all four.

---

# 1. Categories

## The hard truth: topic-based prohibitions do not work well

Very few subject categories can defensibly be prohibited under all circumstances.

Eldercare may legitimately require information about:

* cognition;
* medications and diagnoses;
* precise location;
* finances;
* substance use;
* family conflict;
* sleep, toileting and personal care;
* religious practices;
* sexual health;
* suspected abuse.

Those are among the most sensitive categories, but also among the categories most likely to matter in an actual care emergency.

The defensible absolute bans are therefore mostly on:

1. **data representations that create disproportionate risk**;
2. **purposes the product should never serve**;
3. **claims the system is not competent to author**;
4. **information for which no eldercare necessity exists**.

GDPR’s special-category structure and HIPAA’s special treatment of psychotherapy notes support heightened controls, but neither provides a universal list of health-related facts that may never be processed. Both rely heavily on purpose, necessity and disclosure context. ([Eur-Lex][1])

## A defensible hard-prohibition list

### A. Authentication and authorization secrets

The system should refuse to store:

* passwords;
* PINs;
* one-time codes;
* recovery codes;
* private cryptographic keys;
* seed phrases;
* full payment-card security codes;
* answers intended solely as authentication secrets.

This is not primarily a consent issue. It is a security-design failure. An elder’s consent does not make a conversational memory graph an appropriate credential vault.

**Legitimate eldercare need:** almost none. The system may need to help the person reach a password manager, identify the correct account or contact a trusted helper. It does not need the secret itself.

### B. General-purpose raw surveillance archives

Prohibit persistent storage of:

* continuous household audio;
* continuous interior video;
* ambient conversations not directed to the system;
* recordings of visitors who have not entered the system’s consent model;
* covert monitoring initiated by one household member against another.

Smart-home research repeatedly identifies multi-user, bystander and interpersonal privacy as distinct from owner-versus-platform privacy. The device purchaser cannot provide complete authorization on behalf of everybody recorded in the home. ([Franziska Roesner][2])

**Legitimate eldercare need:** event detection may require transient sensing. The distinction should be:

* sensor processing: potentially permitted;
* short event buffer: purpose-limited;
* continuous replayable archive: prohibited by default.

For example, a fall detector may process audio locally and preserve a narrowly bounded event clip after a detected emergency. That does not justify keeping the preceding month of household speech.

### C. General-purpose biometric, genetic and identity-document archives

Prohibit general memory storage of:

* face templates;
* voiceprints;
* gait identities;
* fingerprints;
* raw genetic results;
* full passports, Social Security numbers and identity documents.

A voice template may be needed for local speaker recognition. It should be stored as a purpose-specific authentication artifact, isolated from the knowledge graph, unavailable to reasoning models and non-exportable.

Genetic and biometric data receive special treatment under GDPR. Genetic testing associated with Alzheimer’s risk also has limited predictive meaning and is ordinarily accompanied by clinical or genetic-counselling considerations. ([Eur-Lex][1])

**Legitimate eldercare need:** identity resolution and emergency identification. Solve those through isolated, tokenized systems—not conversational memory.

### D. Raw intimate media

Prohibit storage of intimate photographs, explicit sexual material or images of undressed household members except in a tightly bounded clinician-directed workflow, such as an explicitly requested wound-care image.

**Attack:** toileting, skin integrity, incontinence and sexual health can be real care issues. The ban should therefore target **raw intimate media and voyeuristic detail**, not the existence of a care fact such as “requires continence supplies.”

### E. Autonomous high-stakes labels

The assistant should never author, as its own durable conclusion:

* dementia or mild cognitive impairment;
* legal incapacity;
* financial incompetence;
* substance-use disorder;
* abuse perpetrator or abuse victim;
* criminality;
* deception or dishonesty;
* dangerousness;
* suicidality;
* sexual orientation;
* political or religious identity;
* personality disorder;
* caregiver unfitness.

It may retain:

* attributed statements;
* directly observed events;
* externally supplied professional diagnoses;
* narrowly defined functional support needs;
* a recommendation that professional review may be appropriate.

This is an inferential prohibition rather than a raw-category prohibition. It is necessary because capping the confidence of “Dad is probably incompetent” does not eliminate the harm produced by storing and exposing that label.

### F. Non-care third-party dossiers

Prohibit systematic collection about people who are not enrolled household members or enumerated care participants when the information is not necessary to care.

Examples:

* the neighbour’s drinking;
* the daughter’s marital problems;
* a home-health worker’s immigration status;
* a relative’s political beliefs;
* a visitor’s medical history.

Research calls the broader problem **interdependent privacy**: one person’s disclosure decision affects another person’s privacy. Existing platform consent systems generally handle this poorly. ([Springer Link][3])

---

## Restricted rather than prohibited categories

These should sit behind feature-specific ceilings:

| Category        | Permitted representation                                               | Prohibited representation                                |
| --------------- | ---------------------------------------------------------------------- | -------------------------------------------------------- |
| Cognition       | Specific observed difficulty; current support need; imported diagnosis | Autonomous dementia diagnosis; global competence score   |
| Medication      | Current medication plan; reminder status; observed missed event        | General “noncompliant patient” trait                     |
| Finance         | Bill due; authorized spending alert; suspicious transaction event      | Financial competence score; wealth profile               |
| Location        | Current safety state or destination needed for care                    | Indefinite movement history                              |
| Substance use   | Attributed report; immediate safety concern                            | Addiction diagnosis or moral/reliability score           |
| Family conflict | Attributed allegation; communication boundary                          | System-authored blame, motive or credibility finding     |
| Mood            | User’s stated mood; immediate support request                          | Persistent depression, manipulation or personality label |
| Personal care   | Functional assistance requirement                                      | Unnecessary intimate narrative or media                  |

---

## The cognition collision

Cognition is the strongest argument against a topic-only ban.

Adjacent clinical practice resolves this by separating:

1. **observation**;
2. **screening**;
3. **functional assessment**;
4. **diagnosis**;
5. **decision-specific capacity**.

Brief cognitive screens are intended to identify a possible need for further evaluation; they are not definitive diagnoses. Formal dementia evaluation combines history, functional assessment, cognitive assessment and other clinical information. Capacity is evaluated for a specific decision at a specific time rather than inferred globally from a diagnosis. ([Alzheimer’s Association][4])

Your system should reproduce that separation:

### Layer 1: Event observation

> “Bill asked what time the appointment was three times between 9:00 and 9:20.”

This is still sensitive, but it is falsifiable and provenance-preserving.

### Layer 2: Functional support state

> “Repeat appointment reminders are currently enabled.”

This describes what assistance is being provided, not why the person needs it.

### Layer 3: Clinical hypothesis

> “The recent pattern may warrant professional cognitive assessment.”

This should be temporary, tightly restricted and non-diagnostic.

### Layer 4: Diagnosis

> “Mild cognitive impairment diagnosed by Dr. X on date Y.”

This may enter only as an attributed external clinical claim or an explicit self-report.

### Layer 5: Capacity

> “Able to authorize financial sharing.”

The household assistant should not infer this from conversational behaviour. Capacity is decision-specific and consequential enough to require a qualified human process.

**Recommended hard rule:**

> The assistant may model the assistance a person currently needs. It may not convert that support model into a diagnosis, legal-capacity conclusion or general theory of the person.

That is the cleanest way to make cognition useful without turning HIP into an undeclared diagnostic system.

---

# 2. Retention

## Append-only audit and erasure are compatible only if the ledger does not contain the personal data

Do not write raw claims, transcripts, embeddings, subject identifiers or ordinary hashes of sensitive content directly into the immutable ledger.

The EDPB’s blockchain guidance warns against placing personal data in immutable systems where doing so conflicts with rectification and erasure. Its basic recommendation is architectural: keep personal data off-chain wherever possible. ([European Data Protection Board][5])

A plain hash is not necessarily safe. Short or predictable claims can be guessed and hashed, and repeated hashes permit linkage.

## Defensible ledger pattern

### Off-ledger mutable store

Contains:

* source statement;
* structured claim;
* speaker and subject;
* embeddings;
* summaries;
* supporting evidence;
* audience policy;
* retention deadline;
* derivation links.

Each claim or small claim group is separately encrypted.

### Append-only ledger

Contains only:

* opaque random event identifier;
* salted or keyed commitment;
* policy version;
* operation type;
* timestamp;
* actor or service role;
* previous-entry commitment;
* deletion or invalidation status.

### On deletion

1. Delete the active source object.
2. Destroy the claim-level encryption key.
3. Delete or invalidate its embeddings.
4. Traverse the derivation graph.
5. Delete or recompute affected summaries and classifications.
6. Append an opaque tombstone to the ledger.
7. Prevent restoration from backups.
8. Report any known areas where deletion cannot propagate.

NIST recognizes cryptographic erase as a sanitization technique, but its effectiveness depends on encryption and key-management design. It is not magic applied after the data have already been copied into uncontrolled systems. ([NIST Publications][6])

## “Beyond use” versus actual deletion

Backups are a legitimate practical problem. UK regulatory guidance recognizes that data may remain temporarily in backups where immediate deletion is not technically possible, provided it is placed beyond use, not restored into production and removed according to a defined backup cycle. ([ICO][7])

That supports an honest distinction:

* **active erasure:** unavailable to normal operation immediately;
* **cryptographic erasure:** ciphertext remains but keys are destroyed;
* **backup expiry:** unreachable backup copies age out on a documented schedule;
* **physical sanitization:** storage media are eventually purged or destroyed.

Do not describe all four as identical.

---

## Propagating revocation to derived data

There is prior art for parts of this problem, but no general turnkey solution.

### Data lineage and provenance

Database and workflow research has long used provenance to identify which outputs depend on which inputs. That is the necessary foundation for propagating invalidation. ([IUScholarWorks][8])

### Machine unlearning

SISA training structures model training so that deleting one person’s data requires retraining only affected model shards. Certified-removal research seeks guarantees that a model after removal is indistinguishable from one that never saw the data. These methods remain limited by model class, training architecture, computational cost and adaptive deletion behaviour. They are not a general solution for arbitrary foundation models. ([arXiv][9])

### The honest conclusion

For a household knowledge system, strong revocation is feasible **only if you design for lineage before collection**.

Every derived object needs:

```text
artifact_id
artifact_type
parent_artifact_ids
subjects
source_categories
purpose
audience
retention_deadline
policy_version
derivation_method
```

Then enforce:

```text
child_retention ≤ earliest applicable parent retention
child_audience ⊆ intersection of parent audiences
child_sensitivity ≥ most restrictive parent sensitivity
```

When a parent is revoked:

```text
if child can be recomputed entirely from authorized parents:
    recompute child
else:
    invalidate and delete child
```

Without this provenance graph, “revocation propagates” is theatre.

---

## Embeddings

Treat embeddings as transformations of the source, not harmless indexes.

Required controls:

* one claim or small revocable unit per embedding;
* stable mapping from vector to source artifact;
* deletable vector-store partitions;
* no household-wide irreversible vector aggregation;
* no embedding reuse in model evaluation;
* deletion verification through source-to-vector reconciliation.

Deleting the textual claim while leaving a retrievable embedding is not meaningful deletion.

## Summaries

Do not create monolithic household summaries such as:

> “Dad has memory problems, drinks too much and cannot handle money.”

Such summaries combine claims with different authors, subjects, purposes and retention periods. They are almost impossible to revoke correctly.

Use compositional summaries whose sentences retain source dependencies. If a summary cannot preserve lineage, it should remain ephemeral.

## Evaluation and training corpora

The clean structural rule is:

> Household production data do not enter general training or evaluation corpora by default.

Once a claim is exported into a disconnected corpus, copied into analyst notebooks or incorporated into a generally trained model, reliable revocation becomes expensive or impossible.

Separate consent to receive the care service from consent to contribute data to product development. The latter should never be necessary to use the product.

---

## What should set the retention clock?

Sensitivity alone is insufficient.

A useful rule is:

```text
expiry =
minimum(
    purpose_end,
    factual_validity_end,
    authorization_end,
    category_maximum,
    subject_policy_end
)
```

Four factors should determine the category maximum:

1. **Operational half-life:** how long the information remains useful.
2. **Harm persistence:** how damaging it remains if exposed.
3. **Correctability:** whether mistakes can realistically be repaired.
4. **Revocation difficulty:** how widely the information propagates.

### Examples

| Artifact                           | Appropriate retention basis                                                               |
| ---------------------------------- | ----------------------------------------------------------------------------------------- |
| Raw audio used for transcription   | Delete immediately after verified transcription unless an explicit event clip is required |
| Ordinary conversational transcript | Short staging period, then extract authorized claims and delete                           |
| Temporary location                 | Until the safety or navigation task ends                                                  |
| Medication schedule                | Until superseded, plus only the operational history needed for the care purpose           |
| Missed-medication event            | Until resolved or incorporated into an authorized care record                             |
| Cognitive hypothesis               | Short review window; expire unless reaffirmed by new evidence and permitted purpose       |
| Clinician-supplied diagnosis       | Until revoked, corrected, superseded or no longer needed for the care plan                |
| Low-risk preference                | Until stale; renew through ordinary use rather than permanent retention                   |
| Abuse allegation                   | Governed by safeguarding and legal policy, not ordinary household-memory retention        |
| Audit event                        | Long-lived opaque proof that an operation occurred; no recoverable claim content          |

There are no canonical research-backed numbers for a household AI. Anyone giving you universal 30-, 90- or 365-day thresholds is inventing product policy, not reporting settled literature.

---

# 3. Audience

## “The author always gets permanent readback” is not defensible

The fact that someone supplied information does not give them ownership of the system’s durable record about another person.

The author already knows what they said. Permanent system readback creates something additional:

* perfect recall;
* searchable history;
* aggregation;
* cross-session dossiers;
* derived conclusions;
* the ability to use the assistant as surveillance infrastructure.

Contextual integrity treats privacy as a function of the sender, recipient, subject, information type and transmission principle. “Who spoke” is only one element. ([Helen Nissenbaum][10])

## Separate four rights

### Author rights

The author should be able to:

* see that they made a contribution;
* inspect its attribution during a correction process;
* correct or retract their statement;
* understand its purpose and current audience.

The author should not automatically receive:

* permanent read access;
* the subject’s responses;
* corroborating reports from others;
* the system’s derived assessment;
* the subject’s broader profile.

### Subject rights

The subject should ordinarily be able to:

* know that information about them is retained;
* inspect the attributed source;
* dispute or contextualize it;
* restrict ordinary sharing;
* see what inferences have been made.

There must be narrow exceptions where disclosure would create credible risk of abuse, retaliation or evidence destruction.

### Care-recipient or beneficiary rights

The person for whose benefit the data are used should have the strongest claim over ordinary care use, but “beneficiary” cannot be used as a rhetorical excuse for caregiver surveillance.

### Authorized-care-role rights

Caregivers receive only information directly relevant to their enumerated function.

HIPAA’s family-disclosure rules use a comparable concept: information shared with family or others involved in care should be directly relevant to that involvement. If the patient is absent or incapacitated, disclosure is based on professional judgment and limited to what the recipient needs to know. ([HHS.gov][11])

HIPAA also allows a provider not to treat an apparent personal representative as the patient where abuse, neglect or endangerment is reasonably suspected. That matters because “caregiver” and “safe proxy” are not synonyms. ([HHS.gov][12])

---

## Proposed audience rule

For every claim, calculate audience from:

```text
authorized_audience =
    purpose-authorized recipients
    ∩ need-to-know roles
    ∩ each subject’s applicable sharing policy
```

Then apply explicit exceptions for:

* immediate safety;
* mandatory reporting;
* authorized clinical care;
* a legally valid representative;
* protected abuse review.

The **most restrictive applicable subject policy** should normally control. An exception must be recorded as an exception, not silently converted into permanent household sharing.

## Speaker and subject are different

For:

> “Susan says Dad is hiding his drinking.”

Store separate objects:

### Source contribution

```text
author: Susan
content: attributed allegation
subject: Dad
purpose: care concern
```

### Subject-related claim

```text
subject: Dad
predicate: possible alcohol use concern
status: asserted by Susan
```

### Relationship/conflict metadata

```text
subjects: Susan and Dad
predicate: disagreement regarding alcohol use
```

Those objects may have different audiences.

Susan may receive a receipt confirming that her report was recorded. That does not mean she should have permanent access to Dad’s resulting care profile, other reports about him or the system’s assessment of her credibility.

## Dependent or absent subject

Where the subject cannot participate:

1. Apply their prior standing policy or advance preference.
2. Use an authorized representative only for the relevant domain.
3. Limit disclosure to the care purpose.
4. Screen for conflicts of interest.
5. Preserve the dependent person’s behavioural dissent.
6. Revisit the arrangement if capacity or participation changes.

## Conflict and abuse allegations

Do not put allegations into ordinary pair-private or household-shared memory.

Create a separate **protected safeguarding channel**:

* the accused person does not automatically see the allegation;
* the reporter does not gain access to the subject’s entire file;
* the system does not decide who is truthful;
* no automated confrontation or “family reconciliation” occurs;
* escalation follows a separately designed safeguarding protocol;
* access is logged and independently reviewable.

This is one place where ordinary subject access and author readback rules may need temporary restriction. But “abuse concern” will itself be gameable by a hostile family member, so the exception must not become a general method for hiding claims from their subject.

---

# 4. Inferential reach

## A trust cap is not an inference ceiling

A low-confidence inference can still be:

* stigmatizing;
* exposed to caregivers;
* used to alter service;
* retained indefinitely;
* combined with other claims;
* treated as a search result;
* leaked to a clinician or insurer.

The system therefore needs restrictions on **what predicates may be generated**, not merely how much confidence they receive.

Research on high-risk inferences identifies a gap between regulating source data and regulating damaging, privacy-invasive or weakly verifiable conclusions. Smart-home research also demonstrates that sensitive household activities can be inferred from apparently innocuous device data. ([SSRN][13])

## The unrestricted abstraction call must go

An unrestricted model call over household memory effectively has this authority:

> Generate any claim about any person from any combination of available evidence.

That is incompatible with a dimensioned ceiling.

Replace it with a typed **Inference Permit**:

```text
inference_permit:
    permitted_output_predicates
    permitted_subject_roles
    permitted_input_categories
    prohibited_input_categories
    purpose
    permitted_audience
    retention_rule
    actionability
    required_evidence
    required_review
```

The model receives only inputs allowed by the permit and may emit only schema-valid outputs.

## Recommended inference classes

### Class A: Syntactic transformation

Examples:

* date normalization;
* unit conversion;
* entity resolution;
* pronoun resolution;
* duplicate detection.

These may generally be performed, but entity resolution across speakers can still create privacy problems and needs subject controls.

### Class B: Attributed semantic restatement

Input:

> “Mom hates taking the large blue pill.”

Output:

> “Speaker reports that Mom dislikes taking medication X.”

This does not create a new factual conclusion. It preserves attribution.

### Class C: Same-domain operational inference

Input:

* scheduled medication at 8:00;
* no confirmation by 9:00.

Output:

> “Medication confirmation remains outstanding.”

This may be useful and relatively bounded.

It should not become:

> “Mom is medication noncompliant.”

### Class D: Sensitive support hypothesis

Input:

* repeated missed appointments;
* repeated requests for the same reminder.

Output:

> “Additional appointment support may be useful.”

This requires:

* a specifically enabled care feature;
* a defined purpose;
* narrow audience;
* short retention;
* visible provenance;
* no diagnostic language.

### Class E: Cross-domain or high-stakes inference

Examples:

* missed bills + repeated questions → financial incapacity;
* late-night movement + slurred speech → alcoholism;
* private calls + church absence → depression;
* disagreement with caregiver → paranoia;
* inconsistent answers → deception;
* family argument → abuse perpetrator;
* medication mistakes → dementia;
* relationship patterns → sexual orientation;
* purchases and media use → political or religious identity.

These should be prohibited as durable system-authored claims.

---

## Core inferential rules

### 1. Output ontology allowlist

The system may write only predicates registered in a governed ontology.

The model cannot create new durable predicates such as:

```text
is_manipulative
is_probably_demented
is_untrustworthy
is_bad_with_money
```

Ontology changes require independent policy review.

### 2. No unrestricted cross-domain joins

Medication, finance, communications, location and relationship data should not be jointly available to a general abstraction model.

Cross-domain inference should require a separately approved use case.

### 3. No cross-subject inference by default

A claim about Susan should not silently update Dad’s profile merely because they share a household.

Likewise, one household member’s behaviour should not be used to classify another person.

### 4. Inference inherits restrictions

A derived object must inherit:

* every relevant subject;
* the highest input sensitivity;
* the narrowest audience;
* the shortest retention;
* the strictest purpose restriction.

An inference must never launder sensitive inputs into a less restricted label.

### 5. No inference from silence or absence without a validated sensing contract

Examples to prohibit:

* no medication confirmation means the medication was not taken;
* no response means confusion;
* reduced conversation means depression;
* a missed event means incapacity.

Silence is often missing data, not evidence.

### 6. Separate observation, hypothesis and determination

```text
OBSERVATION:
No medication confirmation received.

HYPOTHESIS:
Medication may not have been taken.

DETERMINATION:
Medication was missed.
```

Those are not interchangeable.

A determination requires an evidence rule appropriate to the domain.

### 7. Separate transient reasoning from durable memory

You probably cannot prevent a general model from forming an internal inference while generating a response.

You can control whether that inference is:

* written to memory;
* shown to another person;
* used to change permissions;
* used to initiate an action;
* included in a summary;
* exported outside the household.

The enforceable ceiling is therefore mainly on **persistence, disclosure and actionability**, not on every transient computation inside a foundation model.

### 8. Sensitive hypotheses cannot authorize their own collection

The system must not reason:

> “This person may have cognitive decline, so I should ask more cognition questions.”

That recreates the original positive-feedback loop.

A sensitive hypothesis may trigger:

* a pause;
* a neutral suggestion to seek human review;
* a predefined safety workflow.

It may not expand its own evidence-gathering authority.

---

# The remaining hole: offer governance

Your four harm dimensions still do not bound the rate at which grants are solicited.

Add a solicitation policy with these properties:

## Offers are purpose-triggered, not engagement-triggered

A sensitive grant may be offered only because a specific enabled care function requires it—not because the user is talkative, lonely, cooperative or highly engaged.

## No adaptive persuasion

The model may not:

* rewrite the offer until accepted;
* add emotional pressure;
* imply that refusal is unsafe or unhelpful;
* ask caregivers to pressure the subject;
* break one broad grant into a sequence of apparently trivial grants;
* present broader access after each narrow acceptance;
* use prior acceptance as evidence that the next offer is appropriate.

## Decline creates a presumption against repetition

A declined or ignored grant should not be re-offered unless there is a material change in circumstances or the user affirmatively reopens the subject.

The exact cooldown or number of permitted reminders is product policy; the literature does not supply a validated universal threshold.

## Acceptance rate is not a product KPI

Teams should not be rewarded for:

* percentage of users granting health access;
* decline-rate reduction;
* number of categories activated;
* graph completeness;
* caregiver conversion;
* low friction in sensitive authorization.

Otherwise the organization will optimize around every formal protection.

## Cumulative burden must be visible

Even when each grant is individually narrow, the system must display the resulting combined authority:

> “The system currently retains medication, location and cognitive-support information and shares selected alerts with Susan.”

Without cumulative disclosure, consent atomization becomes another dark pattern.

---

# Proposed ceiling specification

```text
COLLECTION_OR_INFERENCE_ALLOWED only if:

1. category is not prohibited;
2. representation is permitted;
3. purpose is enumerated and currently active;
4. solicitation policy permits the offer;
5. required authorization exists;
6. authorization is not sufficient by itself where a safeguard is required;
7. all subjects are identified or the third-party exception applies;
8. audience is within each applicable subject and purpose policy;
9. retention deadline is calculable;
10. every durable derivative will retain lineage;
11. output predicate is allowed by an inference permit;
12. the operation does not expand its own future authority.
```

And:

```text
IF any condition cannot be evaluated:
    do not collect or persist;
    provide the underlying service at the narrower ceiling where possible.
```

# Overall assessment

The dimensioned ceiling is materially stronger than a scalar depth score, but it will still fail unless you adopt four additional architectural conclusions:

1. **Categories must govern representations and purposes, not just topics.**
2. **The immutable ledger must prove operations without containing recoverable household facts.**
3. **Authorship does not create perpetual access to information about another person.**
4. **The model must receive typed inference authority; unrestricted abstraction is incompatible with the ceiling.**

The literature is strongest on data minimization, purpose limitation, capacity assessment, minimum-necessary disclosure, contextual information flows, provenance and the limits of machine unlearning. It is thin on validated, end-to-end governance for a multi-person household AI. The final policy choices—especially retention periods, offer budgets and conflict-handling thresholds—will be original system design, not implementation of an existing canonical standard.

[1]: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32016R0679&utm_source=chatgpt.com "REGULATION (EU) 2016 - EUR-Lex - European Union"
[2]: https://www.franziroesner.com/pdf/geeng-smarthomes-chi19.pdf?utm_source=chatgpt.com "Who's In Control?:Interactions In Multi-User Smart Homes"
[3]: https://link.springer.com/article/10.1007/s12525-022-00566-8?utm_source=chatgpt.com "Exploring interdependent privacy – Empirical insights into ..."
[4]: https://www.alz.org/professionals/health-systems-medical-professionals/cognitive-assessment?utm_source=chatgpt.com "Cognitive Screening and Assessment"
[5]: https://www.edpb.europa.eu/news/edpb-adopts-guidelines-on-processing-personal-data-through-blockchains-and-is-ready-to_en?utm_source=chatgpt.com "EDPB adopts guidelines on processing personal data through ..."
[6]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf?utm_source=chatgpt.com "Guidelines for Media Sanitization"
[7]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/?utm_source=chatgpt.com "Right to erasure | ICO"
[8]: https://scholarworks.iu.edu/dspace/bitstreams/ca836db4-e8d1-4817-9a50-1a20debe0c0d/download?utm_source=chatgpt.com "A Survey of Data Provenance Techniques - IU ScholarWorks"
[9]: https://arxiv.org/abs/1912.03817?utm_source=chatgpt.com "Machine Unlearning"
[10]: https://nissenbaum.tech.cornell.edu/papers/Contextual%20Integrity%20Up%20and%20Down.pdf?utm_source=chatgpt.com "Contextual Integrity Up and Down the Data Food Chain"
[11]: https://www.hhs.gov/hipaa/for-professionals/faq/disclosures-to-family-and-friends/index.html?utm_source=chatgpt.com "Disclosures to Family and Friends"
[12]: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/personal-representatives/index.html?utm_source=chatgpt.com "Personal Representatives"
[13]: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3248829&utm_source=chatgpt.com "A Right to Reasonable Inferences: Re-Thinking Data ..."


---

## CORRECTIONS

Appended 2026-07-31 (D-71). **The two passes above are unchanged — a banked review is
not rewritten.** This section records a factual error in Source 1 (the Fable codebase
pass) that was discovered after banking, in the pattern used on the D-46 bank.

**1. FALSE — `REQ_CARE_TEAM_READ_AUTH` is not MET.**

**What was claimed.** Source 1's collisions section, line 274, states:

> "1. **REQ_CARE_TEAM_READ_AUTH (MET, 2026-07-21)** deliberately *widened* audience: a
> care-team-private fact's readable audience is the recipient's whole enrolled care
> team, keyed on live enrollment. Any audience ceiling narrows what a MET REQ
> deliberately opened. Direct collision on Axis 3."

The same "(MET)" claim was carried into this artifact's `docs/INDEX.md` row.

**Why it is false.** `REQ_CARE_TEAM_READ_AUTH` is **NOT MET**, on three independent
checks made in D-67:

- its own doc header states `Status: NOT MET`
  (`docs/requirements/REQ_CARE_TEAM_READ_AUTH__cross-author-care-team-auth__v20260721_1027.md:2`);
- its `docs/INDEX.md` status column reads `NOT MET`;
- **no MET block exists anywhere in the document** — the only other occurrence of "MET"
  in it is line 176, *"if those regress, this REQ is not MET, full stop."*

**What is true.** The REQ was never ruled MET. Its five-row acceptance has **no
executable form**: no runner references it, and the fixtures it requires do not exist —
`care_teams` and `care_team_members` are both empty in the live registry, so
`is_active_caregiver` returns `False` for every input and the INJ-3 care-team permit
cannot fire in this deployment at all (D-68). The widening **is nonetheless live in
code** (`harness/injection_contract.py:515-518`), which is what made the collision worth
raising — but it is a widening shipped under an unruled REQ with an unrunnable
acceptance, not a widening a MET REQ deliberately opened.

**How the error arose, and its extent.** The date "2026-07-21" was taken correctly from
the code comment at `injection_contract.py:25`. The "(MET)" was the reviewer's own
inference and was not checked against the REQ's status. It propagated from this pass
into the D-70 filing of `REQ_STRUCTURAL_CEILING` (whose header Related line repeated it;
corrected in `v20260731_2129`) and into this artifact's INDEX row (corrected D-71).

**What survives the correction.** The *substance* of collision 1 stands and is arguably
sharper: an audience ceiling still collides with a live, shipped widening. What changes
is the character of the collision — it is not "a ceiling narrows what a MET REQ
deliberately opened," it is "a ceiling narrows an unproven widening that is already
governing live reads." Nothing else in either pass depends on the MET status.

**Related defect filed since.** `TD-138` (D-69, SEC, OPEN) records that the same code
path is epoch-blind: `is_active_caregiver` authorizes against the current roster where
the REQ requires authorization at the fact's roster epoch, so a newly-enrolled caregiver
gains read access to facts predating their enrollment. That REQ's acceptance row 4 tests
only the removal direction, so a fully-passing acceptance would have missed it.
