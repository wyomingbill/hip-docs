# DIAGRAM SPEC: HIP Architecture Visuals
Status: BUILT
Reconciled-Against: ANALYSIS__candidate-intent-deep-review__v20260711_0501, SIA_SPEC__structured-intent-architecture__v20260710_1614, SIA_SHIP_BAR__two-gate-conformance__v20260711_0842, ANALYSIS__classifier-placement-sovereignty__v20260711_1333, HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032, HIP_Architecture_Spine__v20260704_1315, TEST_HARNESS__architecture-and-invariants__v20260711_1900, HIP_STATE__cold-resume__v20260711_1700; no code changed this pass

---

## Purpose and Conventions

This is the single source of truth for seven architecture diagrams to be built as SVG and integrated into the White Paper and NDA Technical Addendum. The SVG build consumes this spec directly. No diagram may add nodes, arrows, or labels not specified here; no diagram may omit any element listed.

### Color and line conventions (apply consistently across all seven diagrams)

| Element | Stroke | Fill | Label color | Weight |
|---|---|---|---|---|
| Deterministic component (code, policy, immutable) | #1E3A5F (navy) | #EAF0FB (pale blue) | #1E3A5F | 2px solid |
| Probabilistic component (model, classifier) | #C0392B (red) | #FDECEA (pale red) | #C0392B | 2px dashed |
| Trust-ladder rung (active, populated) | #1E3A5F (navy) | #2E6DA4 (medium blue) | #FFFFFF | 2px solid |
| Trust-ladder rung (empty / not-yet-reached) | #ADB5BD (grey) | #F8F9FA (off-white) | #6C757D | 1px solid |
| Parked / UNCONFIRMED state | #7F6000 (amber) | #FFF8E1 (pale amber) | #7F6000 | 2px dashed |
| Enforcement gate / guard | #145A32 (dark green) | #E9F7EF (pale green) | #145A32 | 2px solid |
| Conformance contract boundary | #6C3483 (purple) | #F4ECF7 (pale purple) | #6C3483 | 2px solid |
| Off-device / cloud component | #E67E22 (orange) | #FEF5E7 (pale orange) | #E67E22 | 2px dotted |
| Ratchet / baseline | #117A65 (teal) | #E8F8F5 (pale teal) | #117A65 | 2px solid |
| Arrow: primary flow | #1E3A5F | -- | -- | 2px solid, arrow tip filled |
| Arrow: data (post-envelope) | #2E6DA4 | -- | -- | 1.5px solid |
| Arrow: injection / attack surface | #C0392B | -- | -- | 1.5px dashed, arrow tip open |
| Arrow: parks / deferred | #7F6000 | -- | -- | 1.5px dashed |
| Arrow: confirmation gate bypass | #145A32 | -- | -- | 2px solid, double-stroke |
| Label font | -- | -- | -- | 12px sans-serif, sentence case |
| Section header font | -- | -- | -- | 13px bold |

Background: white (#FFFFFF). No gradients. No shadows. No rounded corners on enforcement/deterministic boxes. Modest rounding (rx=6) on model boxes. No em dashes or en dashes anywhere in any label.

---

## Diagram 1: CandidateIntent Flow

**File:** `whitepaper/diagrams/source/D1_candidate_intent_flow.svg`
**WP placement:** Part II ("The Moat"), trust-boundary subsection
**Size:** 900 x 360 px, left-to-right flow

### Purpose

An engineer reading this diagram understands:
- every turn starts with an immutable identity binding that no model output can change;
- the SIO classifier is a red-dashed proposal box -- it operates inside the deterministic envelope but carries zero authority;
- all authority decisions (disclosure, write, refusal) are made in deterministic code after the envelope;
- confidence 0.99 from a malicious injection has exactly the same downstream authority as confidence 0.01 -- none.

### Nodes (left to right, with exact labels)

| ID | Label | Style |
|---|---|---|
| N1 | Utterance\n(raw text, untrusted) | Probabilistic (red-dashed) |
| N2 | Immutable Identity Envelope\nbinds: member_id, voiceprint event | Deterministic (navy solid) |
| N3 | Pre-Guard\ninjection detector\nfires before model | Enforcement gate (green solid) |
| N4 | SIO Classifier\n(qwen2.5:7b, temp 0, stateless)\nPROPOSAL -- no authority | Probabilistic (red-dashed) |
| N4a | Deny-Safe Default\ntype=question, empty subject\nsio_source="fallback" | Parked/UNCONFIRMED (amber-dashed) |
| N5 | Deterministic Resolution\nresolves mentions against registry\nspeaker_relationship derived by code | Deterministic (navy solid) |
| N6 | Policy Envelope\nINJ-1 thru INJ-7\nevaluates: identity + membership\n+ attribute sensitivity + grants | Enforcement gate (green solid) |
| N7a | Disclosure\n(admitted facts, scoped to owner) | Deterministic (navy solid) |
| N7b | Write Park / Promote\n(P8 monotonicity, P10 gate) | Parked/UNCONFIRMED (amber-dashed) |
| N7c | Governed Refusal\n(access-control or empty-set, existence-invariant) | Deterministic (navy solid) |

### Envelope groupings

Draw a thick navy rectangle (3px, no fill, label "Deterministic Envelope") enclosing N3, N4, N5, N6. The red-dashed N4 box is visually inside this envelope to show "untrusted classifier, governed context."

Draw a thin red-dashed rectangle (1.5px, no fill, label "Untrusted (proposal only)") around N4 alone.

### Arrows

| From | To | Label on arrow | Style |
|---|---|---|---|
| N1 | N2 | every turn | Primary flow |
| N2 | N3 | member_id bound | Primary flow |
| N3 | N4 | utterance text only (no identity, no facts, no history) | Primary flow |
| N3 | N4a | model unavailable / schema invalid / confidence < 0.6 | Arrow: deferred (amber) |
| N4 | N5 | SIO (type, subject, attribute, confidence) -- PROPOSAL | Primary flow |
| N4a | N5 | deny-safe SIO | Arrow: deferred (amber) |
| N5 | N6 | SIO + resolved subjects + member_id | Primary flow |
| N6 | N7a | admission: owner facts only | Data flow (blue) |
| N6 | N7b | cross-principal write / trust regression | Arrow: deferred (amber) |
| N6 | N7c | cross-member read / no subject / empty-set | Primary flow |
| N1 | N3 | (attack surface annotation only, no arrow) | Injection dashed-red label: "injection attack surface" |

### Annotation text (small, below flow)

"confidence is advisory: 0.99 has the same authorization power as 0.01 -- none"

---

## Diagram 2: Decision-Plane vs Data-Plane

**File:** `whitepaper/diagrams/source/D2_decision_vs_data_plane.svg`
**WP placement:** Part II (trust boundary subsection) and Part VI (where compute must live), cross-referenced
**Size:** 900 x 420 px, vertical split with dividing line

### Purpose

An engineer reading this diagram understands:
- the classifier must stay on-device because it runs BEFORE the envelope on raw utterances -- its output is what the envelope acts on;
- the reasoning tier can run off-device because it RECEIVES only what the envelope already decided to disclose -- it is downstream of the authority decision;
- the principled line is not "is the component trusted" but "does the component run before or after the policy evaluation";
- placement is a privacy/availability/positioning decision, not an authorization decision (the envelope treats both as untrusted proposals regardless).

### Layout

Two vertical panels separated by a bold vertical dividing line labeled "Policy Envelope (deterministic)". Left panel is labeled "Decision Plane / on-device required". Right panel is labeled "Data Plane / off-net permitted".

### Nodes -- left panel (Decision Plane)

| ID | Label | Style |
|---|---|---|
| D1 | Raw Utterance\n(enters L0, untrusted) | Probabilistic (red-dashed) |
| D2 | Pre-Guard\n(injection detector) | Enforcement gate (green) |
| D3 | SIO Classifier\n(qwen2.5:7b, dedicated Ollama port 11435)\ndecision-plane: runs BEFORE envelope\noutput IS what envelope acts on | Probabilistic (red-dashed) |
| D4 | Policy Envelope\nINJ-1 thru INJ-7\nidentity + membership + grants | Enforcement gate (green), straddles dividing line |

### Nodes -- right panel (Data Plane)

| ID | Label | Style |
|---|---|---|
| D5 | Admitted Facts\n(post-envelope, owner-scoped only) | Deterministic (navy) |
| D6 | Groq Reasoning Tier\n(Llama, Mistral, etc.)\ndata-plane: RECEIVES post-envelope disclosures\noutput is prose, not an authorization decision | Off-device (orange-dotted) |
| D7 | Response\n(governed, to member) | Deterministic (navy) |

### Nodes -- annotation column (far right, no boxes, plain text)

- "On-device: raw utterances, governance decisions, write detection"
- "Off-net OK: post-envelope prose generation, retrieval-augmented reasoning"

### Arrows

| From | To | Label | Style |
|---|---|---|---|
| D1 | D2 | raw (untrusted) | Primary flow |
| D2 | D3 | utterance only (no identity, no facts) | Primary flow |
| D3 | D4 | SIO proposal (type, subject, attribute, confidence) | Primary flow |
| D4 | D5 | authorized disclosures only | Data flow (blue) |
| D5 | D6 | disclosed facts + query | Data flow (blue) |
| D6 | D7 | prose response | Data flow (blue) |

### Annotation banner (below dividing line, spanning both panels)

"Placement is a privacy, availability, and positioning decision -- not an authorization decision.\nThe architecture contains a hostile classifier by construction regardless of placement.\nDecision-plane inference anchors to the governance boundary; data-plane inference does not."

---

## Diagram 3: Trust Ladder and Write Monotonicity (P8)

**File:** `whitepaper/diagrams/source/D3_trust_ladder_p8.svg`
**WP placement:** Part II (trust-boundary subsection), fact-lifecycle section
**Size:** 900 x 500 px, ladder on left, P8 example flow on right

### Purpose

An engineer reading this diagram understands:
- the five-rung ladder is an epistemic scale (how established is a fact), not an authorization scale;
- evaluation is first-match-wins top-to-bottom (DERIVED is the rarest, highest-confidence rung; UNCONFIRMED is the default landing);
- P8 prevents a lower-trust incoming write from silently closing a higher-trust head in a cross-principal write;
- the mechanism is parking (the incoming write lands UNCONFIRMED alongside the retained head, not replacing it).

### Left panel: Ladder

Five stacked horizontal boxes, top-to-bottom, labeled as rungs. Each rung box is 240px wide, 52px tall, separated by 8px.

| Rung (top to bottom) | Label inside box | Fill | Notes in small text below box |
|---|---|---|---|
| 1 (top) | DERIVED\n(provenance category, not strength) | Navy/blue (active rung) | "produced by deterministic inference from multiple CONFIRMED sources; not model output" |
| 2 | CONFIRMED\n(rank 3, evaluation wins first) | Navy/blue (active rung) | "written by authenticated member about themselves, plus confirmed_by annotation (e.g. clinic record)" |
| 3 | CORROBORATED\n(rank 2) | Navy/blue (active rung) | "corroborated by a second independent source (cross-session repeated assertion or external record)" |
| 4 | ASSERTED\n(rank 1) | Medium navy (active rung) | "single authenticated write, no corroboration; the normal write result" |
| 5 (bottom) | UNCONFIRMED\n(rank 0) | Grey/off-white (baseline rung) | "parked write, pending confirmation; also the landing zone for P8-triggered parks" |

Left of each rung, draw a left-pointing bracket label: "first-match-wins (top wins)" spanning all five rungs.

### Right panel: P8 Write Monotonicity Rule

Title: "P8 -- Cross-Principal Write Monotonicity"

Show a two-column mini diagram labeled "Cross-Principal Supersede Attempt":

Left column "Active Head":
- Box: CORROBORATED head\nmaya/ray/medication\n"metformin 500mg" (rank 2)

Arrow: "maya asserts (ASSERTED, rank 1)" pointing from utterance box to...

Gate box (green): P8 Guard\nrank(incoming) < rank(head)?

Arrow from gate "YES (1 < 2)" to:
- Box (amber-dashed): Park UNRESOLVED\n"jardiance" alongside head\nhead retained, trust_state=ACTIVE

Arrow from gate "NO (rank >=)" to:
- Box (navy): Supersede Executes\nold head closed\nnew head active

Below the P8 flow, add two exception boxes:

| Box | Label | Style |
|---|---|---|
| E1 | Self-Write Exempt\nowner == asserting member\n(prevents confirmation fatigue on own facts) | Deterministic (navy), smaller |
| E2 | Equal-Rank Permitted\nrank(incoming) == rank(head)\ncross-principal ASSERTED over ASSERTED | Deterministic (navy), smaller |

### Annotation text (bottom, full width)

"Classifier confidence (parse quality) never seeds ladder rank.\nLadder rank derives from write provenance and deterministic ladder rules only. (P9)"

---

## Diagram 4: Proof Harness Structure

**File:** `whitepaper/diagrams/source/D4_proof_harness.svg`
**WP placement:** Confidential Technical Addendum, NIST MEASURE section
**Size:** 1000 x 600 px, two-column layout: layers (left) and conformance/ratchet (right)

### Purpose

An engineer reading this diagram understands:
- the five layers cover different failure surfaces (governance invariants, regression, mutation, pairwise coverage, adversarial);
- the two conformance contracts (SIA two-gate, disclosure) run offline and orthogonally to the five layers;
- the ratchet is the enforcement mechanism that makes the suite a gate, not a report;
- the mapping to NIST AI RMF MEASURE function.

### Left column: Five Layers (stacked top to bottom)

Each layer is a box 420px wide, 68px tall.

| Layer box | Exact label | Style |
|---|---|---|
| L1 | Layer 1 -- Governance Invariants\nP1 member isolation, P2 owner retrieval, P3 write integrity\nP4 refusal correctness, P5 supersede integrity\nP6 epistemic non-fabrication, P8 write monotonicity\nP9 confidence/ladder severing, P10 confirmation gate\nseed-reproducible, 20-100 iterations per invariant | Enforcement gate (green) |
| L2 | Layer 2 -- Demo Regression\nhash-paired scripts vs expected output\nrequired_present + must_not_present token assertions\ngraph state assertions (active_count, value_substr)\nscripts: care_coordination, three_zone_demo, reveal_demo,\nconsent_flow, routing_showcase | Deterministic (navy) |
| L3 | Layer 3 -- Guard Mutation (in-process, port 7998)\ndisable each guard: assert leak / misfire occurs\novertrigger each guard: assert legitimate flow blocked\nINJ-3, INJ-6b, INJ-7 tested\nmonkeypatch isolation: mutations never bleed to subprocess | Deterministic (navy) |
| L4 | Layer 4 -- Retrieval Coverage (pairwise matrix)\n5 dimensions x pairwise reduction: 50-80 scenarios\ndimensions: speaker role, subject reference, attribute,\nphrasing, fact state\n`eval/pairwise_matrix.json` | Deterministic (navy) |
| L5 | Layer 5 -- Adversarial Boundary (19 attacks)\nA1 indirect extraction (4)\nA2 identity spoofing (4)\nA3 instruction injection (4)\nA4 inferential leakage (3)\nA5 write corruption (4) | Probabilistic (red-dashed) |

### Right column top: Conformance Contracts (two boxes, stacked)

| Contract box | Exact label | Style |
|---|---|---|
| SIA | SIA Conformance -- two-gate (`--sia-conformance`)\nGate A (governance-critical, 100% required, Phase B blocker):\n26 entries -- injection containment (A6), write-path type,\ncontrol-flow isolation, injection-disguised fail-safe\nGate B (classification quality, >=90% target):\n133 total golden-set entries\nOffline: hits Ollama 11435 only\nAppends to logs/sia_trend.jsonl | Conformance contract (purple) |
| DISC | Disclosure Conformance -- ORTH-1 (`--disclosure-conformance`)\napply_injection_contract() unit contract\n39 cases, 100% required\nCase groups: self_access, cross_member_refusal,\ncare_recipient_disclosure, empty_set_guard,\ninj6b_targeted_empty_set, owner_read,\nnever_volunteer, declarative_bypass, household_facts,\nsubject_scope, sio_override\nFully offline: no Neo4j, no server, no LLM | Conformance contract (purple) |

### Right column bottom: Ratchet

| Ratchet box | Exact label | Style |
|---|---|---|
| RATCHET | Ratchet -- harness_baseline.json\nREGRESSION (was true, now false): exit code 1 -- gate fail\nNEW FAILURE (key absent): exit code 2 -- gate fail\nKNOWN FLAKY (in quarantine): exit code 0\nIMPROVED (was false, now true): logged, no action required\nPASS: exit code 0\n--update-baseline requires --accept with justification\nAll accepted failures logged in _accepted audit trail | Ratchet (teal) |

### Gate mode table (small table, below ratchet box)

| Mode | Layers | L1 iterations |
|---|---|---|
| --quick (pre-commit) | L2 + L3 | none |
| --full (pre-push) | L1 + L2 + L3 + L4 | 100 |
| --pre-demo | L1 + L2 + L3 + L4 + L5 | 100 |

### NIST MEASURE mapping (annotation column, right of right column)

Small grey-outlined box, 160px wide:

"NIST AI RMF MEASURE\n\nMEASURE 2.5\nAdversarial testing: L5 A1-A5, SIA Gate A injection containment\n\nMEASURE 2.6\nRed-team: A2 identity spoofing, A3 injection, A6 corpus\n\nMEASURE 2.7\nCI gating: --quick pre-commit, --full pre-push, ratchet\n\nMEASURE 4.1\nDrift monitoring: harness_trend.jsonl, sia_trend.jsonl"

### Arrows (left column to right column)

| From | To | Label | Style |
|---|---|---|---|
| L1 | RATCHET | scenario results | Data flow (blue) |
| L2 | RATCHET | scenario results | Data flow (blue) |
| L3 | RATCHET | scenario results | Data flow (blue) |
| L4 | RATCHET | scenario results | Data flow (blue) |
| L5 | RATCHET | scenario results | Data flow (blue) |
| SIA | RATCHET | Gate A/B pass/fail | Conformance arrow (purple) |
| DISC | RATCHET | pass/fail (39 cases) | Conformance arrow (purple) |

---

## Diagram 5: Orthogonal Testing Boundaries

**File:** `whitepaper/diagrams/source/D5_orthogonal_contracts.svg`
**WP placement:** Confidential Technical Addendum, interface contract section
**Size:** 900 x 480 px, three horizontal bands representing the layer seams

### Purpose

An engineer reading this diagram understands:
- three interface contracts formalize the seam between each pair of layers, making components independently testable and swappable;
- each contract is an offline gate (no server, no Neo4j, no model for ORTH-1) -- it tests the component boundary, not end-to-end behavior;
- passing all three contracts proves the components compose correctly even when tested separately.

### Layout: three horizontal bands with components above and below each seam

**Band 1 (top): SIO Conformance Contract -- L0/L1 boundary**

Components above (L0 utterance entry):
- Box: Raw Utterance (style: probabilistic/red-dashed), label: "Raw Utterance\n(untrusted text, L0 input)"

Seam line (purple, 2px, full width), labeled:
"SIO Conformance Contract (`--sia-conformance`)\nGate A: 26 governance-critical entries, 100% required\nGate B: 133 total entries, >=90% target\nTests: injection containment, write-path type, control-flow isolation, fail-safe default\nOffline: Ollama port 11435 only"

Components below (L1 routing):
- Box (navy): Routing Cascade + Injection Contract, label: "L1 Routing\n(SIO consumer -- reads sio.type, sio.subject, sio.attribute)\nSIO is the ONLY input to injection contract gates"

**Band 2 (middle): Disclosure Conformance Contract -- L2/L3 boundary**

Components above (L2 context assembly):
- Box (navy): Governed Context Assembly, label: "L2 Context Organization\nassemble_governed_context(member_id)\nINJ-1 thru INJ-7 injection contract\nadmitted facts: owner-scoped, encrypted at rest"

Seam line (purple, 2px), labeled:
"Disclosure Conformance Contract ORTH-1 (`--disclosure-conformance`)\napply_injection_contract() direct unit test\n39 cases, 100% required\nTests: self_access, cross_member_refusal, care_recipient_disclosure,\nempty_set_guard, inj6b_targeted_empty_set, owner_read,\nnever_volunteer, declarative_bypass, household_facts,\nsubject_scope, sio_override\nFully offline: no Neo4j, no server, no LLM"

Components below (L3 enforcement):
- Box (green): Control Plane, label: "L3 Control Plane\npolicy evaluation, write authority\nP8/P9/P10 enforcement\nauthenticated identity immutable here"

**Band 3 (bottom): Fact Schema Conformance Contract -- L1/L2 boundary**

Components above (L1 write side):
- Box (navy): Write Detection + Store, label: "L1 Write Path\nencode() -> Neo4j\nbitemporal (valid_from, valid_to)\nHKDF-SHA256 encryption per owner"

Seam line (purple, 2px), labeled:
"Fact Schema Conformance ORTH-2 (`--fact-schema-conformance`)\ncanonical attribute roundtrip\nNeo4j schema vs expected shape after migration\n100% required\nPlanned: blocked on ORTH-2 schema migration landing"

Components below (L2 read side):
- Box (navy): Context Assembly (read path), label: "L2 Retrieval\nbitemporal read, decrypt, inject\ncleaved to owner via fact ownership check"

### Annotation (right side, vertical text or column)

"Each contract tests a boundary in isolation.\nComponents on either side are independently\nswappable as long as the contract passes.\nThis is the provability claim: governance holds\neven when the model changes, because the\nenforcement contract is separate from the model."

---

## Diagram 6: Four-Layer Architecture

**File:** `whitepaper/diagrams/source/D6_four_layer_architecture.svg`
**WP placement:** Part I (architecture overview), referenced from Part II and Part VI
**Size:** 1000 x 560 px, horizontal bands top-to-bottom with placement annotations

### Purpose

An engineer reading this diagram understands:
- L0 is the volatile surface (swappable adapter -- cascade today, full-duplex later);
- L1 is the routing cascade and classification boundary (where CandidateIntent lives, classifier isolation here);
- L2 is the governed context moat (owned data, compounding value, injection contract);
- L3 is the deterministic control plane (where identity, consent, policy, and P8/P9/P10 live);
- the key architectural principle: context compounds (L2/L3, own it), intelligence commoditizes (L0/L1 edge inference, rent it).

### Band layout (top to bottom)

**Band L0: Interaction Surface (volatile, swappable)**

Style: Off-device (orange-dotted border), fill: pale orange, label banner left: "L0 -- Interaction Surface\nVOLATILE: rent, keep swappable"

Boxes inside (left to right):
- "GPT Realtime\n(WebSocket, WeSpeaker voice ID)" (off-device style)
- "Pipecat / WebRTC\n(cascade: Whisper STT + Kokoro TTS)" (off-device style)
- "Full-Duplex Adapter\n(future swap-in at L0, no change below)" (off-device style, lighter)

Annotation right of band: "Any interaction model drops in here.\nL1 thru L3 unchanged on swap."

**Band L1: Routing Cascade (durable, already built)**

Style: Deterministic (navy border), fill: pale blue, label banner left: "L1 -- Routing Cascade\nDURABLE: own it"

Boxes inside:
- "Complexity Classifier\n(tier selector: edge / mid / core / frontier)" (deterministic)
- "SIO Classifier\n[CandidateIntent entry point]\nqwen2.5:7b, stateless, temp 0\ndedicated Ollama port 11435 (INFRA-1)" (probabilistic/red-dashed)
- "Write Detection\n(Groq API, async, post-200-OK)" (off-device for Groq part, with local wrapper)

Annotation right: "CandidateIntent:\nSIO is a proposal.\nClassifier is isolated\nfrom extraction workload."

**Band L2: Context Organization (governed context moat)**

Style: Enforcement gate (green border), fill: pale green, label banner left: "L2 -- Governed Context\nMOAT: own it"

Boxes inside:
- "Neo4j Household Graph\n(per-member, bitemporal, encrypted at rest\nHKDF-SHA256 Fernet per owner)" (deterministic)
- "Injection Contract\nINJ-1 thru INJ-7\nassemble_governed_context()" (enforcement gate / green)
- "Trust Ladder Store\nDERIVED > CONFIRMED > CORROBORATED\n> ASSERTED > UNCONFIRMED\nfirst-match-wins evaluation" (deterministic)

Annotation right: "Governed context:\nfact values stay owner-scoped.\nInjection contract is the\naccess-control enforcement."

**Band L3: Control Plane (trust guarantee)**

Style: Deterministic (navy border), fill: pale blue, label banner left: "L3 -- Control Plane\nTRUST GUARANTEE: own it"

Boxes inside:
- "Identity Envelope\n(voiceprint / session binding\nimmutable once bound)" (deterministic)
- "Policy Evaluation\n(auth + membership + sensitivity + grants)" (enforcement gate / green)
- "P8 Write Monotonicity\n(cross-principal trust guard)" (enforcement gate / green)
- "P9 Confidence Severing\n(SIO confidence never seeds ladder rank)" (enforcement gate / green)
- "P10 Confirmation Gate\n(closed-vocab, deterministic\nbypasses SIO classifier)" (enforcement gate / green)

Annotation right: "Deterministic enforcement:\nmodel cannot touch identity,\nconsent, or write authority."

### Vertical arrows between bands

| From | To | Label | Style |
|---|---|---|---|
| L0 bottom | L1 top | raw utterance (text or audio transcript) | Primary flow |
| L1 bottom | L2 top | SIO + member_id + tier assignment | Primary flow |
| L2 bottom | L3 top | admitted facts + resolved subjects | Data flow (blue) |
| L3 | L1 (write-back path) | write decision (park / promote / refuse) | Data flow (blue), upward arrow on right margin |

### Swap annotation (below L0, italics)

"Layer 0 has shifted three times in two years (cascade, turn-based audio-native, full-duplex).\nLayers 1 thru 3 are unchanged by that motion. The moat does not move when the interface does."

---

## Diagram 7: Confirmation-Gate Flow (P10)

**File:** `whitepaper/diagrams/source/D7_confirmation_gate_p10.svg`
**WP placement:** Part II (trust-boundary section) and Confidential Technical Addendum (P10 spec)
**Size:** 900 x 560 px, top-down flow with two parallel paths at the gate

### Purpose

An engineer reading this diagram understands:
- a sensitive write (cross-principal, trust-regressing) parks as UNCONFIRMED with an identity-bound capability token;
- the session enters a constrained-confirmation state: the NEXT utterance routes to a deterministic closed-vocabulary gate, NOT to the SIO classifier;
- the SIO model never sees the confirming utterance -- no model output participates in confirmation;
- injection cannot self-confirm because there is no model in the confirmation path;
- token binding (actor + action + subject + expiry) means a different member's "yes" returns verdict "none" and the token remains live.

### Nodes (top to bottom)

| ID | Label | Style |
|---|---|---|
| C1 | Statement Utterance\n(maya: "Ray switched to Jardiance")\ntype=statement (SIO) | Probabilistic (red-dashed) |
| C2 | Write Detection\n(Groq extraction: attribute=medication, subject=ray\nvalue=jardiance, write_state=supersede) | Off-device (orange-dotted, Groq part) |
| C3 | P8 Guard\neffective_subject (ray) != owner (maya)?\nrank(incoming ASSERTED=1) < rank(head CORROBORATED=2)? | Enforcement gate (green) |
| C4 | Park as UNRESOLVED\n"jardiance" write_state=unresolved\nactive alongside retained CORROBORATED head | Parked/UNCONFIRMED (amber-dashed) |
| C5 | Issue Capability Token\nbound: actor=maya, action=supersede\nsubject=ray/medication, expiry=N turns or session-end | Deterministic (navy) |
| C6 | Reply to Maya\n"I've noted that as an unconfirmed update.\nThe existing record has stronger confirmation,\nso I haven't replaced it -- say yes to confirm\nthe change, or no to keep the current record." | Deterministic (navy) |
| C7 | Next Utterance\n(from session member) | -- (input node, no fill) |
| C8 | Deterministic Closed-Vocab Gate\nexact match after normalization\n(yes / no / cancel + tight synonyms)\nSIO CLASSIFIER NOT CALLED | Enforcement gate (green, double-stroke border) |
| C9a | Identity Check\ntoken.actor == confirmed_speaker_id? | Enforcement gate (green) |
| C9b | TTL Check\nexpiry not exceeded? | Enforcement gate (green) |
| C10a | Confirm Path\napply_confirm(token)\npromotion: jardiance supersedes metformin\nold head closed, new head ASSERTED | Enforcement gate (green) |
| C10b | Decline Path\napply_decline(token)\nparked row discarded\nCORROBORATED head retained, no change | Deterministic (navy) |
| C10c | Wrong Member / Expiry\ntoken.actor mismatch or TTL exceeded\nverdict=none, token remains live\ntwo active rows persist | Parked/UNCONFIRMED (amber-dashed) |
| C10d | Ambiguous / Not Closed-Vocab\ndefaults to decline\nparked row persists (UNCONFIRMED)\ntoken expires per TTL | Parked/UNCONFIRMED (amber-dashed) |

### Arrows

| From | To | Label | Style |
|---|---|---|---|
| C1 | C2 | statement, type=statement | Primary flow |
| C2 | C3 | write decision | Primary flow |
| C3 | C4 | YES -- trust regression detected | Arrow: deferred (amber) |
| C3 | (bypass, exits right) | NO -- equal or higher rank: supersede executes normally | Data flow (blue) |
| C4 | C5 | park confirmed | Primary flow |
| C5 | C6 | token issued | Primary flow |
| C6 | C7 | awaiting member response | Dashed (amber) |
| C7 | C8 | next utterance | Primary flow |
| C8 | C9a | closed-vocab match (yes / no) | Confirmation gate bypass (green double-stroke) |
| C8 | C10d | no match / ambiguous | Arrow: deferred (amber) |
| C9a | C9b | identity match | Primary flow |
| C9a | C10c | identity mismatch | Arrow: deferred (amber) |
| C9b | C10a | "yes" + TTL valid | Confirmation gate bypass (green double-stroke) |
| C9b | C10b | "no" + TTL valid | Primary flow |
| C9b | C10c | TTL exceeded | Arrow: deferred (amber) |

### Key annotation box (right margin, purple border)

"Injection Non-Confirmability\n\nInjection cannot self-confirm because:\n1. The SIO model is not called on confirming turns\n2. Token binding requires actor == original speaker\n3. Closed-vocab match is exact (normalized), not semantic\n4. Ambiguous input defaults to decline\n\nThis is the independence principle from the two-man rule\napplied to voice: confirmation must not flow through\nthe same channel that produced the proposal."

### Second annotation box (bottom, full width, teal border)

"Session persistence:\nIf the session ends before the token resolves, the UNCONFIRMED fact persists.\nThe next session can surface it: 'you mentioned a medication change -- should I record it?'\nExpiry is conversation-relative (N turns or session-end), not wall-clock alone."

---

## SVG Build Notes

These notes are for the SVG author and are not part of the diagram content.

1. Every label uses sentence case and avoids em dashes and en dashes. Use "--" (two hyphens) where a dash is needed in labels (match this doc).
2. Diagram D4 is the largest. Prefer a 2-column layout over scaling text below 10px; break the NIST mapping into a sidebar rather than squeezing it into the main flow.
3. Diagram D3 has two distinct panels (ladder left, P8 flow right). These may be separated by a thin vertical rule at x=450.
4. For red-dashed boxes (probabilistic), use `stroke-dasharray="6 3"`.
5. For double-stroke confirmation gate arrows (D7), draw two parallel strokes 3px apart.
6. All diagrams share the same color constants (listed in the conventions table above). Define as SVG `<defs>` variables or CSS custom properties so the palette can be updated in one place.
7. No text should overlap any box border. Minimum 8px padding inside all boxes.
8. Export at 2x resolution for print; SVG is resolution-independent.
9. Diagram filenames are the canonical names; do not rename during SVG build.
