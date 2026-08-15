# HIP STRATEGY: Positioning and Market
Status: BUILT
Reconciled-Against: commit cfb774c (2026-07-12); firms.json + category_mesh.json 40-firm ecosystem; GOVERNANCE_SCOPE_v1__LOCKED; HIP_STATE cold-resume v20260711_1700; MARKET_RESEARCH verified + external v20260712_1331; HIP_EcosystemAnalysis_NDA v20260707_0814
Sources used:
- business/ecosystem/firms.json (40 firms, 9 categories)
- business/ecosystem/category_mesh.json (9 category mesh narratives)
- business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx (full NDA analysis)
- docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-verified__v20260712_1331.md
- docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-external__v20260712_1331.md
- docs/general/GOVERNANCE_SCOPE_v1__LOCKED__v20260712_1245.md
- docs/general/HIP_STATE__cold-resume__v20260711_1700.md

This document is the single source of truth for HIP strategic positioning. Cascade targets are named in Section 8. The cited-vs-modeled discipline in Section 4 must be preserved in every downstream surface.

---

## 1. Thesis

Raw AI intelligence is a commodity. Every capable model will know what a household is. None of them will govern it.

HIP's thesis rests on a structural asymmetry: the large foundation models (GPT-4o, Gemini, Claude) commoditize factual recall, reasoning, and natural-language interaction at a pace no startup can match by competing on those dimensions. The moat is not model intelligence. The moat is what the model is permitted to know and who decides.

**Governed household context compounds over time. Raw model intelligence does not.**

Every fact added to a household graph increases the fidelity of future disclosures. A medication record that exists today makes a drug-interaction query answerable next year. A caregiver grant established today makes a remote-monitoring session authorizable next month. A trust ladder that tracks the provenance of every fact today makes a contradiction resolvable tomorrow. The context layer is the durable asset; the model is the interchangeable inference engine above it.

Three architectural properties make HIP's context layer defensible:

**Model-neutral.** HIP governs context that any model can reason over. When GPT-5 ships, HIP's household graphs do not migrate. When a better edge model replaces qwen2.5:7b, the trust ladder does not rebuild. HIP does not bet on one model winning. It bets on context mattering regardless of which model is currently best.

**Operator-hosted.** HIP runs on operator infrastructure (cable broadband, telco, managed service) at the household edge. The operator owns the last-mile relationship, the billing relationship, and the trust relationship that national labs demonstrably do not own. Operator-hosted means HIP reaches households through a channel labs cannot replicate and incumbents (Amazon, Apple, Google) will not create because it undermines their data-harvest model.

**Operator-blind.** Household plaintext content is decrypted only inside attested confidential-computing enclaves. The broadband operator does not receive the household encryption key or access to household plaintext. This is not a policy claim. It is an architectural constraint: per-member encryption (Fernet/HKDF-SHA256), keys never committed, enclaves attested. Operator-blind is the property that makes household adoption possible in a post-breach regulatory environment, and it is the property that differentiates HIP from any cloud AI product that holds household data in cleartext on a commercial cloud.

The thesis, compressed: raw intelligence commoditizes; governed household context, built once per household, compounds for life and is owned by no one but the household.

---

## 2. Moat and Flywheel

### 2.1 The three-part moat

**Multi-principal governance.** HIP enforces access control, trust hierarchies, and disclosure rules across distinct authenticated principals sharing a household. This is not a feature. It is a set of deeply interlocked architectural invariants: P1 (member isolation), P4 (refusal correctness), P8 (write monotonicity), P10 (confirmation gate), INJ-7 (existence invariance on cross-member denials). The five direct competitors (Maple, Nori, Ohai, b.well, Life360) are building on ordinary cloud infrastructure. Multi-principal governance at this depth is not closeable with a release; it requires either an operator partnership or a capital-intensive independent build that none of them is funded to execute.

Amazon conceded the field by implementing a 6-digit PIN for Alexa multi-user mode. Apple proximity-based switching assumes co-location. Google Voice Match treats members as independent users with no shared governance layer. The incumbents solved convenience, not governance. HIP solves governance.

**Model-neutral portable context.** HIP's trust ladder, fact lifecycle, and injection contract are independent of any model. The SIA classifier (classification layer) is the only model-touching component at the governance boundary, and it emits a structured proposal that the deterministic policy envelope evaluates without model confidence having any authority. Context recorded under GPT-4o is fully available to Gemini, Claude, or the next edge model. This portability is rare. Every model-specific memory product (ChatGPT Memory, Gemini context) creates lock-in by design. HIP's model neutrality is a structural choice that makes household adoption possible without betting on a model winner, and makes operator procurement possible without locking the operator to a specific AI vendor.

**Operator-blind custody.** The per-fact consent-and-routing ledger (planned in TD-108, required pre-scale) will carry: fact_id, owner, attribute, sensitivity classification, allowed destinations, retention limit, and an immutable audit trail. Every fact disclosure is logged. Every consent grant is revocable. The blast radius of any single failure is bounded by the ledger, not by the operator's goodwill. This is what separates HIP from a cloud storage layer with a permission flag. No household AI product shipping today has this. It is the property that makes healthcare (HIPAA workspace) and financial (SOC 2) operator channels viable.

### 2.2 The dual flywheel

**Data flywheel (per household).** Every fact added increases the quality of future disclosures. Every caregiver grant made today is a policy that can be evaluated instantly tomorrow. Every trust-level assignment accelerates future write-conflict resolution. Context that compounds is context worth holding. The longer a household runs on HIP, the more fidelity the governed layer has, and the harder it becomes to replace with a blank-slate competitor. This is the same compounding dynamic as a credit history: the value is not in the day-one record but in the longitudinal provenance chain.

**Network flywheel (platform ecosystem).** Each of the nine categories in the 40-firm ecosystem analysis produces a category mesh effect on a shared household substrate. A school event entered in the family-coordination app propagates to the education tutor and the household calendar because they share the same governed graph. An eldercare visit from Honor arrives with the same authorized context as the Ianacare family-caregiver session because both read and write the same permissioned household memory. A Monarch Money budget responds to the eldercare cost from the same graph that the insurance vertical watches for coverage gaps. None of these category compositions exist today; each becomes natural on a shared substrate. Each new app on HIP raises the value of every other app already present. That is a genuine network effect, and it is why the 40-firm ecosystem is not a market to be divided but a flywheel to be turned.

The nine categories and their firms (all from firms.json and category_mesh.json):

| Category | Firms (exemplars) | Mesh produced on HIP |
|---|---|---|
| Family coordination | Cozi, Maple, FamilyWall, OurHome, Nori | One household graph; calendar propagates to every surface; roles set once, applied everywhere |
| Eldercare | CareLinx, Honor, Papa, Ianacare, Zingage, Lotsa | Permissioned care memory across paid+family care; handoffs carry context; payer sees authorized audit trail |
| Health data | Human API, 1upHealth, Particle Health, Validic, b.well | Clinical rails + device streams interpreted under household consent; records become household decisions |
| Household finance | Monarch, Copilot, YNAB, Plaid, MX | Finance rails (Plaid, MX) feed household-aware budgeting that sees eldercare cost and insurance gap |
| Smart home | Home Assistant, SmartThings, Matter/Thread, Josh.ai | Device execution tied to household context, roles, and routines, not dumb automation |
| Family safety | Life360, Bark, Qustodio, Circle (Aura) | Signals compose: location alert reads custody schedule; monitoring flag reads child roles |
| Education | Khanmigo, IXL, Sizzle | Tutoring shares household learning memory; multi-child history compounds across sessions |
| Insurance | Policygenius, Lemonade, Hippo | Continuous household risk management on the same graph as finance and eldercare |
| Emerging household AI | Ohai, Nori/Domus, Hearth, Luffu, Honeydew | Partners become premium surfaces on a substrate they do not have to fund; race shifts to experience, not infrastructure |

---

## 3. Alpha

Three structural forces open a narrow window in which HIP can establish the household substrate before a re-consolidation closes it. The window is not permanent.

**The commoditization window.** Model performance on factual recall, reasoning, and conversation is converging toward parity across the major providers. A household AI that differentiates on model quality in 2026 will lose that differentiation by 2028. The firms that survive are those whose moat is not the model. The commoditization of inference is the tailwind for a governance layer that sits above inference: the worse the model moat, the more valuable the governance moat.

**Operator owns the household.** Cable broadband operators (Comcast: 28.7M subscribers; Charter, Cox: together 39M additional households) have four assets that national AI labs do not: last-mile physical infrastructure, billing relationships, customer service touchpoints, and an existing trust relationship with households. The lab model (cloud-hosted, data-harvesting, consumer-direct) is the exact architecture operators have commercial and regulatory reasons to oppose. HIP is the product that lets an operator offer a household AI service on their own infrastructure, under their own brand, with household data never leaving the operator's edge enclave. This is the operator's incremental AI service line, not a lab partnership. No lab will willingly fund this. No lab product is designed to run this way. HIP's channel is structurally closed to the competition.

**Incumbents conceded multi-person governance.** Amazon PIN (6-digit code, no trust hierarchy), Apple proximity switching (physical co-location required, no grants), Google Voice Match (parallel independent users, no shared context layer). Each incumbent has shipped a feature-level multi-user mode that does not attempt to solve household governance. These decisions were not accidents. They are architectural reflections of a business model that depends on individual user data. HIP does not compete with Amazon on convenience. It occupies the governance layer that Amazon's architecture excludes. The incumbent concession is real, and it is load-bearing for HIP's strategic position.

---

## 4. Beachhead

The beachhead is the trust dyad: one principal whose information must remain controlled, and one explicitly authorized second party (spouse, adult child, caregiver) who assists locally or remotely.

**Demographics (cited numbers only):**

- 1-2 person households are 63.7% of all US households: 84.2M of 132.2M in 2024. [CITED: Census CPS ASEC, Historical Households Table HH-4]
- One-person: 38.5M (29.1%). Two-person: 45.7M (34.6%). [CITED]
- 29.2M married-couple-only households (lower bound). [CITED: CPS 2023 Table H1]
- 15.2M households with a 65+ adult living alone. [CITED-derived: ACS B11010]
- 63M family caregivers in 2025, 24% of all US adults. [CITED: AARP/NAC 2025]
- ~3 in 10 adult care recipients in home/community settings live alone. [CITED: AARP/NAC 2025]
- Caregiver remote monitoring use: 13% (2020) to 25% (2025). [CITED: AARP/NAC 2025]
- Solo-living growth 2010-2020 was entirely driven by 65+ households. [CITED: CPS]
- Boomers moving through ages 75-85 between 2025 and 2045 is the product-relevant wave. [CITED: Census P25-1144 projections used as basis]

**Modeled numbers (must be labeled every time used in any downstream surface):**

- Core near-term addressable segment: 45-55% of US households, roughly 60-73M. [MODELED: external analysis, no source measures this intersection directly]
- Eldercare wedge: 15-25% of US households, roughly 20-33M HH. [MODELED: applies involvement rates to 65+ solo HH base]
- Functionally multi-principal (once involved outside parties counted): 78-85% of HH. [MODELED]
- Genuinely single-principal (no involved other): only 15-22% of HH. [MODELED]

**The discipline sentence:** The verified mass-market number is the 63.7% structural figure. Every percentage above that is a modeled derivation and must be presented as such. "45-55% core addressable" is an analyst model, not a Census citation, and must be labeled accordingly in every external surface.

**The dyad argument in one sentence:** The demand center of gravity for HIP is exactly the v1 taxonomy (two competent adults, or one adult plus one remote caregiver with explicit grants), and the GSS kin-centering trend (mean confidants: 2.94 in 1985, 2.08 in 2004; McPherson et al. ASR 2006) says trust circles are getting smaller and more household-shaped over time. The product architecture matches the empirically observed trust topology.

---

## 5. Wedge

The eldercare wedge is the first paid vertical. Five properties make it the right wedge:

**Urgency.** Eldercare is not a latent need waiting to be activated. A household managing a 78-year-old parent's medication, appointments, and remote access today does not have the option to wait for a better product. The consequence of information failure is concrete (missed dose, denied authorization, emergency with no context). Urgent buyers have low patience for alternatives.

**Funded.** Two payment channels exist and are currently underserved. Consumer: families already pay $6,200/month for assisted living and $25-48/month for monitoring subscriptions; the coordination layer between them does not yet exist. Reimbursed: CMS launched the GUIDE Model in July 2024, an eight-year program paying providers $4,000-6,000 per beneficiary per year for dementia care coordination. HIP does not bill Medicare directly; the provider bills, and HIP is the platform the coordination runs on. The reimbursed path removes willingness-to-pay as the binding constraint and replaces it with a procurement decision by a provider partner.

**Inherently multi-member.** The eldercare dyad (older adult plus family caregiver, plus often a paid care agency) is the canonical multi-principal use case. It is not a simplification of HIP's governance model; it is the direct application. P8 (write monotonicity), P10 (confirmation gate), INJ-7 (existence invariance), and the caregiver-grant mechanism were built for exactly this configuration. The product is not being adapted to the wedge; the wedge is the product.

**Remote-managed.** 11% of caregivers of adults 50+ live an hour or more away [CITED]. Roughly 3 in 10 adult care recipients live alone [CITED]. These are the governed remote-access configurations: an adult child who needs scoped read access to a parent's medication list, appointment schedule, and emergency contacts, without receiving unrestricted access to the parent's full household context. This is precisely what the caregiver-grant mechanism delivers: explicit delegation, scoped to the grant, revocable, audit-logged. No competing product ships this. Remote caregiving is digitizing rapidly (13% to 25% remote monitoring adoption 2020-2025 [CITED]); the household AI coordination layer is the natural next step.

**Operator's strength.** Cable broadband operators already sell home monitoring subscriptions to this demographic. Eldercare is not a new customer segment for Comcast or Charter; it is an existing billing relationship waiting for a higher-value service to sit on top of it. HIP's operator-hosted, operator-blind model is exactly what an operator needs to offer a compliant, privacy-defensible eldercare coordination service without the regulatory exposure of holding household health data in cleartext.

**Fastest-growing household configuration.** The US 85+ population goes from 6.3M (2024) to 11.8M (2035) to 13.7M (2040) [Census P25-1144]. The caregiver support ratio (adults 45-64 per adult 80+) falls from 7:1 (2010) to 4:1 (2030) to under 3:1 (2050) [AARP PPI]. Each remote adult child carries more parents with less sibling backup, increasing per-dyad willingness to pay. This is the demographic wave; the eldercare wedge is positioned to be in market before the steepest part of the slope.

---

## 6. Land-and-Expand

### 6.1 v1 bounded principals (built, gated, green)

The v1 scope is fully specified in GOVERNANCE_SCOPE_v1__LOCKED__v20260712_1245.md. The v1 principal taxonomy:

- **Competent adults as full members.** Identity envelope, per-member encryption (Fernet/HKDF-SHA256), injection contract enforcement, write authority.
- **Care recipients as non-credentialed subjects under declared caregiver grants.** Subject in the fact store, not an authenticated principal. Grant is explicit declaration, not inferred.

All four governance behaviors are built and harness-gated: Admit (INJ-1 thru INJ-7), Refuse with reason (access_control and empty_set, distinguishable), Park pending confirmation (P8 + P10), Encrypt per member (TD-030 enforced at epistemic record layer).

The v1 bound is a product decision, not an architectural limit. Every deferred case fails closed: the system refuses or parks rather than guessing or leaking. Deferral is safe without any change to the enforcement path.

### 6.2 v2+ expansion via OP-1..5 as roadmap

The five named open problems in GOVERNANCE_SCOPE_v1__LOCKED are the v2+ expansion roadmap. They are not product gaps; they are research assets. Each comes with: a precise definition, an honest statement of why it is hard, a safe-failure proof for the v1 deferral, and a line of attack. Naming them proactively is a stronger diligence position than quietly narrowing the product.

| Open Problem | v2+ scope | Why it is defensible IP |
|---|---|---|
| OP-1: Minors and consent gradients | Principal with evolving consent capacity, age-threshold delegation, per-jurisdiction rules | No competitor has shipped this; wrong rules are worse than no rules; HIP has the architecture to do it safely |
| OP-2: Relational facts (co-ownership) | Facts owned by no single principal (shared care plan, co-signed document) | Requires joint-grant tuple + merge policy enum; one-owner invariant P3 enforces safe deferral today |
| OP-3: Recipient-competence-aware disclosure | Modulating disclosure to a recipient based on assessed capacity | Ethical hazard is severe; only implementable as opt-in, externally-supplied, time-bounded grant with ethics review |
| OP-4: Contextually variable sensitivity | (fact, asker, context) triple-axis policy evaluator | DSL + harness invariant required; static per-attribute sensitivity is conservative; over-restricts rather than leaks |
| OP-5: Coercion and duress detection | Detecting compelled queries and modifying system behavior | Not a near-term build item; honest position: no access control system is coercion-proof; the bank does not detect a robbery withdrawal |

Each OP is a frontier research problem that HIP is architecturally positioned to solve and competitors are not. The kernel is built once. v2 scope is additive invariants on top of a running harness.

---

## 7. Honest Boundary

### 7.1 What HIP governs

HIP governs the system's disclosures: which facts are disclosed to which principals under which conditions, enforced deterministically by the injection contract (INJ-1 thru INJ-7), the trust ladder (P8 write monotonicity), and the confirmation gate (P10). This is the correct and honest scope of an access-and-disclosure system.

HIP does NOT govern what an authorized principal does with a fact after receiving it. A bank enforces who may withdraw funds; it does not control what the account holder does after the withdrawal. A medical records system enforces who may view a chart; it does not control what a clinician does after reading it. HIP enforces which facts are disclosed to which principals under which conditions. The scope ends at the point of disclosure.

Naming this boundary explicitly is a stronger position than eliding it. Auditors, diligence reviewers, and ethics boards will ask where the system's authority ends. The honest answer is: at the point of disclosure to an authorized principal.

### 7.2 The open-room vs private channel dimension

There is a disclosure dimension that incumbents have not addressed and that HIP is uniquely positioned to name as a differentiator.

The same fact disclosed in a shared acoustic space (a living room where multiple people can hear the assistant's reply) is a different governance event from the same fact disclosed in a private channel (a phone call, a headset, a text notification to a single recipient). A medication reminder spoken aloud when a family member is in the room is functionally a disclosure to that family member. A medication reminder sent to the patient's phone is a disclosure to the patient alone.

HIP's current architecture governs who may authorize a disclosure; it does not yet model the physical or channel context of the delivery. This is named as an honest limitation and a future research direction, not a current feature claim. The competitors have not addressed this at all. HIP has named it.

This is OP-4 territory (contextually variable sensitivity) applied to the output channel rather than the input sensitivity. It is a named research asset, not a product gap.

### 7.3 Scope statement for external use

HIP governs which facts its AI system discloses to which principals, and under what conditions, enforced through deterministic code rather than model judgment. It does not govern what an authorized principal chooses to do with a fact after receiving it, the acoustic environment in which a disclosure is received, or coercive or social pressures acting on a principal before or after a query. These boundaries are clear, accurate, and defensible under regulatory and ethics review.

---

## 8. Cascade Map

### 8.1 White Paper

**Part III (Household forces / why the market now):**
Add the following, sourcing Section 4 of this document:
- Lead with 63.7% / 84.2M 1-2 person HH [CITED: CPS 2024 HH-4]. This is the structural foundation.
- 29.2M couple-only dyads + 15.2M 65+ solo HH = ~45-50M before caregiving overlay [CITED floor; MODELED range label required].
- 63M caregivers, 3 in 10 care recipients live alone, remote monitoring 13% to 25% (2020-2025) [CITED].
- State explicitly: "45-55% core addressable" is a modeled derivation from applying involvement rates; it is not a Census citation.
- The trust-circle literature (McPherson et al., ~2 confidants, kin-centered) supports the dyad architecture.
- Growth trajectory: boomers 75-85 between 2025-2045 is the product-relevant wave, not merely "boomers turning 65."

**Part IX (Why now):**
Add the following, sourcing Sections 3 and 5 of this document:
- The commoditization window: model parity is converging; the moat must be governance, not inference.
- Operator channel opening: cable operators have the subscriber base, billing relationship, and regulatory incentive to offer a household AI service that does not route household plaintext to a national lab.
- CMS GUIDE Model (July 2024): reimbursed care coordination path, removes consumer willingness-to-pay ceiling for the eldercare wedge.
- Caregiver remote monitoring doubling 2020-2025: the digitization of care coordination is underway; HIP is the AI layer the digitization reaches next.
- Incumbent concessions (Amazon PIN, Apple proximity, Google Voice Match): the governance problem is unoccupied.

### 8.2 NDA

**Open-problems-as-roadmap section:**
OP-1 thru OP-5 from GOVERNANCE_SCOPE_v1__LOCKED should be presented in the NDA as the expansion roadmap, not as limitations. The NDA reader is a sophisticated operator or technical diligence reviewer. They will ask about scope limits; the response is to hand them the exact problems, the line of attack, and the safe-failure proof. Format: one paragraph per OP, structured as (what it is, why it is hard, why deferral is safe, line of attack). This is already written verbatim in GOVERNANCE_SCOPE_v1__LOCKED; the NDA section is a lightly reformatted extract.

**Cited-vs-modeled discipline in NDA market section:**
Every number from Section 4 that appears in the NDA must carry its label: [CITED] or [MODELED]. The 45-55% addressable figure must not appear in the NDA without a "(modeled, no direct Census source)" qualifier. The 63.7% structural figure is the safe citation floor.

### 8.3 Website

The website version of market positioning is filtered: no NDA-level financial projections, no OP details, no operator names. The public-facing version of the thesis:

- Lead with the structural household fact: 64% of households are 1-2 person; the modal American trust circle is 2-3 people, increasingly spouse and family.
- Name the problem: governed household AI context does not yet exist. Every AI product either holds household data in the cloud (privacy risk), runs as a single-user product (no governance), or requires technical configuration (not accessible).
- Name HIP without technical depth: the household operating system; context that compounds, governed by the household, accessible to the people they choose, on infrastructure they trust.
- No moat claims, no financial projections, no competitor names. The website sells the problem and the category; the NDA sells the architecture.

### 8.4 What must not cascade without labeling

The following claims must never appear unlabeled in any external surface:
- "45-55% addressable" without "(modeled estimate)"
- "78-85% functionally multi-principal" without "(modeled, no direct source)"
- "20-33M eldercare wedge" without "(modeled, based on involvement rates applied to 65+ solo HH base)"
- The ~80% older-adults-in-1-2-person-HH framing is REFUTED and must never appear in any surface.
- Layer 2/3/4 NDA TAM figures are directional; they must not appear in the website or any unqualified external statement.

---

## References

### Cited (primary, verified)
- Census CPS ASEC Historical Households Table HH-4: https://www.census.gov/data/tables/time-series/demo/families/households.html
- Census CPS ASEC 2023 Table H1: https://www.census.gov/data/tables/2023/demo/families/cps-2023.html
- ACS 2023 1-year Table S1101: https://data.census.gov/table/ACSST1Y2023.S1101
- AARP/NAC Caregiving in the US 2025: https://www.aarp.org/pri/topics/ltss/family-caregiving/caregiving-in-the-us-2025/
- McPherson, Smith-Lovin, Brashears, ASR 2006: https://journals.sagepub.com/doi/10.1177/000312240607100301
- Census P25-1144 Demographic Turning Points: https://www.census.gov/content/dam/Census/library/publications/2020/demo/p25-1144.pdf
- AARP PPI caregiver support ratio: https://www.aarp.org/content/dam/aarp/research/public_policy_institute/ltc/2013/baby-boom-and-the-growing-care-gap-insight-AARP-ppi-ltc.pdf

### Modeled estimates (derived, not directly cited)
- Core near-term segment 45-55% (60-73M HH): external market research, MARKET_RESEARCH__household-trust-circle-segment-sizing-external__v20260712_1331.md
- Eldercare wedge 20-33M HH: involvement rates applied to 65+ solo HH base; same external analysis
- Functionally multi-principal 78-85%: session deep-research synthesis, MARKET_RESEARCH__household-trust-circle-segment-sizing-verified__v20260712_1331.md

### Internal sources
- business/ecosystem/firms.json (40-firm scoring)
- business/ecosystem/category_mesh.json (9 category mesh narratives)
- business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx (four-layer TAM, competitor analysis)
- docs/general/GOVERNANCE_SCOPE_v1__LOCKED__v20260712_1245.md (OP-1..5, architectural boundary)
- docs/general/HIP_STATE__cold-resume__v20260711_1700.md (four-layer architecture, built state)
