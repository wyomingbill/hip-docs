# HIP Claims Register

Status: AUDIT RECORD (read-only extraction; no prose changed in any
surveyed document -- this is a register, not a rewrite)
Reconciled-Against: roadmap 175de2b; docs/rendered/ baseline at 556848a;
the ten gated site pages at https://hip.olindasolutions.com/d-7h4k2m9x/
(fetched live this session); docs/deliverables/HIP_PackageDirectory__v20260727_1716.md
(Part 1 of this same dispatch)
Date: 2026-07-27 17:29 MT

## How to read this

Every load-bearing claim the package makes about what HIP **is** or
**does** -- architecture, identity, encryption, scoping, model
hosting/attribution, kernels, governance. Sourced from `docs/rendered/`
for the white paper (Confidential WP, reconstructed, `v20260727_1104`),
Technical Annex, Prototype Evidence, and Ecosystem Analysis (docx content
read from its text rendering throughout, never parsed directly); read
directly for NDA Open Problems and the Governance Proof (already `.md`);
fetched live for the ten gated site pages. Five claims were seeded by
Bill verbatim; the rest were found independently this session, several
via direct code inspection (not just document cross-reading) where a
seeded claim's own evidence pointed at a specific mechanism.

**STATUS** is PROVEN, DESIGNED, ASPIRATIONAL, WRONG, or UNVERIFIED (one
seeded claim keeps Bill's own word, DISPUTED, verbatim -- see CLAIM-04).
Where marked UNVERIFIED, the row says exactly what would settle it. **No
document is corrected here.** Several claims are internally consistent
with the ratified truth in one location (usually the reconstructed
Confidential WP) and wrong in another (usually the site or the Technical
Annex) -- both locations are listed, and the status reflects the claim
*as asserted*, not the best version of it anywhere in the package.

---

## CLAIM-01 — Members are identified by voiceprint

**Locations:** site `overview.html` ("Members are identified by
voiceprint"); site `architecture.html` §Data protection ("Voiceprint
recognition authenticates household members"); site `platform.html`
§Identity ("HIP identifies household members by voiceprint and scopes
what each member can see and do"); Technical Annex §6 ("HIP identifies
household members by voiceprint. This is the identity mechanism at the
primary interface... it is the anchor for the member-scoped subkeys");
Technical Annex §4.3 ("Root key... Derived from voiceprints of enrolled
members plus a hardware root of trust").

**Evidence:** `docs/requirements/REQ_IDENTITY_BINDING__device-binding__v20260718_1530.md`
(Stage 1 decision: "identity = device binding, device X25519/Ed25519
keypair, not voiceprint/session token alone"); built at `harness/identity_keys.py`
+ `harness/member_seal_keys.py`, REQ_CRYPTO_P1_DYAD_KEYS MET (dyad
custodial keys, X25519). Confirmed live: Prototype Evidence §9's own
honest-scope statement states voiceprint-based identity discrimination
across two or more real voices is explicitly **not claimable** from this
package.

**Status: WRONG**, all five locations above. **Ratified truth** (stated
correctly in the reconstructed Confidential WP, Part I: "It identifies
who is speaking by possession of that member's own device key, not by
voice" and "Members are identified by possession of their own device
keypair, generated at enrollment and never shared. Voiceprint is a hint
and a step-up signal for turn-taking and convenience; it is not
authentication-grade and it is never a key input"): identity is
possession of the per-member device keypair; voiceprint is a hint/step-up
signal only. **Limit:** even the ratified design's own honest section
(WP Part II) says speaker-verification-adjacent binding has its own
attack surface (replay, cloning, insider mimicry) and the expanded
attack-surface paragraph is an unfilled `[PLACEHOLDER -- Bill to write]`
in the WP itself (see CLAIM-16).

**DISPOSITION 2026-07-28 (annex retirement):** `HIP_TechnicalAnnex__v20260702_1155.docx`,
the two locations of this claim in that document (§6, §4.3), is RETIRED,
superseded-by `HIP_ArchitectureForDiligence`, no successor minted.
**retired-with-annex** -- `HIP_ArchitectureForDiligence` names no identity
mechanism anywhere (grepped for "voiceprint"/"device key", zero hits); no
live document carries this claim, correct or wrong, going forward. The
Confidential WP's own correct statement (quoted above) remains the
ratified truth of record independent of the annex's retirement.

---

## CLAIM-02 — The operator cannot read household data

**Locations:** site `overview.html`, `architecture.html` §Data
protection, `moat.html` §The extraction inversion ("The operator cannot
read it"), `why-now.html` §The privacy reckoning; Technical Annex §4.1,
§4.4 ("Operator does not hold the keys required to decrypt... even under
legal compulsion"); Confidential WP Part I, Part II, Part XII §12.2.

**Evidence:** `docs/requirements/REQ_CRYPTO_P3_OPERATOR_BLIND__stage4-phase3__v20260724_1129.md`,
**MET** at `ffe4d67`. PS1 (no v1-path openable), PS2 (no
master-derived-key unwrap), OB4 (static scan), OB5/OB6 (destroyed-key
hard-refusal, no silent auto-create), master key destroyed
Bill-authorized and proven live against all 12 facts (12/12 fail via
master path, 12/12 open via real class keys with zero master key
present). `REQ_CRYPTO_P2_PARTITION_SEALED` MET at `7b1f087` (partition
cryptographically sealed).

**Status: PROVEN AT REST.** **Limit** (this exact phrase appears
correctly in the package's most honest location, Confidential WP Part I:
"This tier is architecture, not yet a running fact. The property proven
today is encryption at rest, not at inference"; Part XIII §13.1: "The
operator-edge confidential-computing path is architecture, not running
fact, today"): at inference, the model decrypts plaintext into memory;
closing that gap needs confidential computing, which is not built (see
CLAIM-08). Technical Annex §4.4's "even under legal compulsion" is the
same at-rest claim stated more strongly than the WP states it, with no
at-inference caveat attached in that location.

---

## CLAIM-03 — Scoping is enforced at retrieval, not at storage

**Location:** Technical Annex §6.3 ("Every fact in the context graph is
scoped either to the household (shared) or to a specific member
(private)... This scoping is enforced at retrieval, not at storage. All
facts live in one graph. Retrieval respects the scoping and returns only
the subset the querying member is authorized to see").

**Evidence:** `docs/requirements/REQ_CRYPTO_P2_PARTITION_SEALED__stage4-phase2__v20260719_0840.md`
MET at `7b1f087` (write-time key-wrap sealing per the ratified four-class
partition); `docs/requirements/REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md`
(ratifies the four-class scope model: member-private, pair-private,
care-team-private, household-circle-shared); write-time classifier
(`harness/write_rule.py:classify`) stamps a class at write time; a fact
sealed to a scope the requester's key-wrap set does not include cannot be
opened by that requester's key at all -- there is no plaintext row a
retrieval filter is trusted to withhold.

**Status: WRONG on current code.** Enforcement is key-wrap omission and
class sealing at write time, not a retrieval-time filter over one shared
plaintext graph (that description matches the *pre-partition* filter-only
model this codebase moved off of -- see `DISPATCH_ISOLATION_TRACE` /
`HIP_MemberIsolation` design docs' own framing of the prior state as
"filter, not crypto"). This is the single most consequential technical
error in the Technical Annex, because §6.3's model implies a compromised
retrieval layer could return everything; the real, built model does not
have that failure mode for sealed classes.

**DISPOSITION 2026-07-28 (annex retirement):** `HIP_TechnicalAnnex__v20260702_1155.docx`
RETIRED, superseded-by `HIP_ArchitectureForDiligence`, no successor
minted. **corrected-by-supersession** -- `HIP_ArchitectureForDiligence`
line 28 already states the correct fact: "The four write-time partition
scopes and the write precedence that assigns a fact's audience are
ratified as decisions, per REQ_PARTITION_CUSTODY... The classifier that
would assign a written fact to one of the four scopes automatically is
unbuilt." Write-time enforcement, not retrieval-time filtering, is on
record in the live document going forward.

---

## CLAIM-04 — The freshness tier sends only the query string, never household context

**Locations:** Technical Annex §2.3 ("The router sends only the
rewritten query string, stripped of household context and member
identity. The external provider sees a generic query that could have
come from any user"); site `architecture.html` ("never sends household
context, and it never sends member identity"); Confidential WP Part I
("it sends only the search string. It never sends household context or
identity").

**Evidence (found by code inspection, not document reading):**
`server/voice_orch.py:1959-2003` -- the mid/core-tier Groq call is gated
by `config.yaml`'s `routing.groq_is_onnet` (currently `false`, i.e.
strip-by-default in this checkout); when `false`, `strip_context_for_tier`
(`harness/orchestrator.py:661-720`) removes the "Recent context about
this person" / "Things you know about this person" system-prompt
sections via `_PERSONAL_SECTION_RE` (`orchestrator.py:655-658`) and drops
sensitivity-flagged prior turns. **Gap found in that same mechanism**:
`local_system_prompt` (`orchestrator.py:388-444`) appends three
*independently conditional* sections -- the two `_PERSONAL_SECTION_RE`
matches, plus a third, "Confirmed facts about other people"
(`orchestrator.py:441-443`, populated from `other_subject_facts`, i.e.
real facts about OTHER household members) that `_PERSONAL_SECTION_RE`'s
pattern does not include. Because the regex only truncates from its
first match, a turn whose system prompt contains a populated "Confirmed
facts about other people" section but an empty "Recent context" and
"Things you know" section (both plausible independently, per the code's
own three separate `if` blocks) would have that cross-member fact
section pass through `strip_context_for_tier` untouched -- and, if
`routing.groq_is_onnet` were `true`, would go to Groq in full regardless.

**Status: DISPUTED** (Bill's own word, kept as given -- this is a
seeded claim). What the code shows, precisely: the current checked-in
default (`groq_is_onnet: false`) does apply real stripping, so "no gate
at all" overstates the default-config behavior; but the stripping
mechanism has a real, located coverage gap (household facts about a
*different* member can leak through the ungated third section) and the
on-net/off-net behavior is a config flag, not an architectural
impossibility -- flipping one boolean sends "full context including
personal facts and conversation history" by the code comment's own
words (`orchestrator.py`/`voice_orch.py` inline comment,
`server/voice_orch.py:1963-1967`). **What would fully settle it**:
reproduce Bill's own referenced live trace (not done this session), or
construct a turn with `other_subject_facts` populated and `known`/`mem`
empty, run it through `strip_context_for_tier`, and confirm the
cross-member section survives unstripped -- the code reading above
predicts it will, but was not executed as a live turn this session. No
existing TD/REQ names this gap; it is new to this session's verification
pass, not filed as debt here (register only, per instruction).

**UPDATE 2026-07-27 (later):** registered as **D-28** in
`docs/deliverables/HIP_DefectRegister__v20260715_1930.md`, status NOT
FIXED -- registered, not built, per instruction (no code changed). Same
class of exposure as `TD-131` on the `main` branch (commit `4390240`,
"household facts reach MID/CORE Groq payload unfiltered") -- `roadmap`'s
own `TD-131` slot is a different, unrelated entry (a cross-branch ID
collision, named in D-28's own text). See D-28 for the full line-by-line
verification trace.

---

## CLAIM-05 — Llama 3.3 70B hosted inside the operator's enclave, attributed to Groq

**Locations:** Technical Annex §2.4 ("Model of record: Groq Llama 3.3
70B, hosted inside the operator's confidential computing enclave");
Technical Annex §4.2 ("Enclave workload: The tier three (core) model,
Groq Llama 3.3 70B... runs entirely inside the enclave").

**Evidence:** `harness/*.py`/`server/voice_orch.py` confirm Groq is
called via `AsyncOpenAI(base_url=GROQ_BASE_URL, ...)` against
`api.groq.com` -- a third-party hosted inference API, over the network,
with no code path that runs Groq's model weights on operator-controlled
hardware. `GROQ_MODEL_CORE`/`GROQ_MODEL_MID` resolve to
`llama-3.3-70b-versatile` / `llama-3.1-8b-instant` (`server/voice_orch.py:1969-1970`),
matching the model names claimed, over Groq's API.

**Status: WRONG as written.** Groq is a hosted inference provider; its
service, by construction, cannot run "inside" an operator-controlled
confidential-computing enclave the operator does not control the
provider's infrastructure for. The real mechanism (confirmed by code) is
an API call to Groq's cloud endpoint, not on-enclave, on-operator-hardware
inference. The Confidential WP's own honest framing (Part I, Part XIII)
avoids this specific attribution error by describing the enclave tier as
"designed to... run inside a confidential computing enclave on the
operator's infrastructure" without naming Groq as the host for it -- the
error is localized to the Technical Annex.

**DISPOSITION 2026-07-28 (annex retirement):** `HIP_TechnicalAnnex__v20260702_1155.docx`
RETIRED, superseded-by `HIP_ArchitectureForDiligence`, no successor
minted. **retired-with-annex** -- `HIP_ArchitectureForDiligence` names no
inference-hosting provider anywhere (grepped for "groq", zero hits); no
live document attributes a model to Groq, correctly or incorrectly, going
forward. The error does not propagate because the vendor name itself is
gone from the corpus, not because it was corrected.

---

## CLAIM-06 — Five kernel services (Identity, Context, Trust, Inference, Institutional integration)

**Locations:** site `platform.html` §The five kernel services; site
`overview.html` ("identity, context, trust, inference, and institutional
integration as shared kernel services"); `HIP_Site_Changes_for_WP_NDA__v20260703_1016.md.docx`
§1.1 (Institutional integration named as "net-new," the fifth, added to
what was previously "four kernel services").

**Evidence:** No `kernel` abstraction, module, or service boundary named
"Identity"/"Context"/"Trust"/"Inference"/"Institutional integration"
exists anywhere in `harness/`, `server/`, or `eval/` (grepped this
session). The underlying pieces exist unevenly: context/routing/trust
(injection contract) are real and gated; "institutional integration"
(a certification stack: SOC 2 Type II, ISO 27701, HIPAA covered-entity
readiness, NYDFS Part 500) has no code, no cert, and no REQ anywhere in
this repo.

**Status: DESIGNED**, unevenly. "Kernel services" is marketing/product
framing over pieces at very different maturities -- three (context,
inference routing, trust/governance) are built and gated in code today;
"identity" as *described on the site* is the WRONG mechanism (CLAIM-01);
"institutional integration" is pure roadmap (no code, no partner, no
certification underway) -- see CLAIM-24.

---

## CLAIM-07 — Cryptographic keys generated and held in hardware secure elements

**Locations:** site `overview.html`, `architecture.html` §Data protection
("Cryptographic keys are generated and held in secure elements under the
household"; "Key stored in secure element of the existing modem or
router" and "secure element of a household member's phone"); Technical
Annex §4.3 ("hardware root of trust anchored in the secure element of the
household gateway... The root key is never exported from a secure
element"; "Mobile anchor: Each enrolled member's phone secure element
holds a member-scoped subkey").

**Evidence:** The real, built key-management code
(`harness/identity_keys.py`, `harness/member_seal_keys.py`,
`harness/dyad_crypto.py`, `harness/encryption.py`) is software key
derivation and storage (X25519 keypairs, HKDF, Fernet envelope
encryption, SQLite-backed registries) -- no code path in this repo talks
to a TPM, a phone Secure Enclave/StrongBox, or a modem/router hardware
security module. `docs/requirements/REQ_IDENTITY_BINDING_BUILD__stage1-implementation__v20260718_1720.md`
Status: **NOT MET** (its own defect notes selective gaps in the software
implementation, not a hardware integration).

**Status: ASPIRATIONAL.** The keys-not-held-by-operator property is real
and proven (CLAIM-02); the specific *hardware secure element* custody
mechanism described is not built anywhere in this codebase today. No REQ
targets phone/gateway secure-element integration.

---

## CLAIM-08 — Confidential computing enclave, hardware-attested, with a measured throughput penalty

**Locations:** Technical Annex §4.2 ("Confidential computing mode enabled
through NVIDIA CC and hardware attestation... Prototype benchmarks fall
in the 8 to 15 percent range for the workloads HIP runs"); site
`architecture.html` ("hardware-attested, encrypted in memory during
processing, and encrypted at rest"); Ecosystem Analysis (`v20260707_0814.docx`)
line ~173 ("household content is decrypted only inside attested
confidential-computing enclaves").

**Evidence:** Confidential WP Part I ("This tier is architecture, not yet
a running fact. The property proven today is encryption at rest, not at
inference") and Part XIII §13.1-13.2 ("The operator-edge
confidential-computing path is architecture, not running fact, today...
The confidential-computing enclave is prior-art and adopted, not built")
-- both in the SAME package, both explicit that no CC enclave exists.
Prototype Evidence's own "What is working" list (§2) does not mention
confidential computing, attestation, or an enclave anywhere; its Known
Issues section names no CC work either.

**Status: WRONG** in the three locations cited (Technical Annex's
specific "prototype benchmarks fall in the 8 to 15 percent range" is
fabricated precision for something the same package's own honest
sections say was never run) **and ASPIRATIONAL** at the general
"enclave exists" framing on the site and in Ecosystem Analysis. The
Confidential WP itself (Part I, Part XIII) states this correctly and is
the one location where this claim is accurate.

**DISPOSITION 2026-07-28 (annex retirement):** `HIP_TechnicalAnnex__v20260702_1155.docx`
RETIRED, superseded-by `HIP_ArchitectureForDiligence`, no successor
minted. **corrected-by-supersession** -- `HIP_ArchitectureForDiligence`
already states the correct fact in two places: line 52 ("Confidential-
computing hardware and attestation. Adopted, not built... Commodity
because this is vendor silicon and vendor firmware") and line 144 ("At
inference, the caller's own key unwraps a fact, and the local model holds
that fact as plaintext in memory... Closing this gap requires
confidential computing, which... is adopted infrastructure not yet
integrated into HIP's inference path. The claim is exact and must stay
exact: operator-blind at rest, not operator-blind at inference."). No
fabricated benchmark number exists in the live document; the annex's own
"8 to 15 percent" figure is not replaced by anything, per instruction --
none exists.

---

## CLAIM-09 — Ten canonical fact-attribute types; extending beyond ten requires an architecture change

**Locations:** Technical Annex §3.1 (lists exactly 10: medication,
allergy, health_condition, dietary, preference, schedule, employer,
relationship, household, financial; "Extending beyond ten requires an
architecture change, not a data change"); Prototype Evidence §2 (same 10
named).

**Evidence:** `harness/extraction_queue.py`'s real `CANONICAL_ATTRIBUTES`
already carries 11 values (`DISPATCH_ENUM_AUDIT__seed-fixtures-outside-detector-schema__v20260717_1135.md`
confirmed 11 by direct grep, missing `incident`/`medication_status`
relative to seeded fixtures); `address` and `zone_district` were added
under `REQ_FRONTIER_TIER__script1-t04-t05-openai-switch__v20260718_0539.md`
without any architecture rewrite -- a data-schema change, exactly the
kind of change §3.1 claims is impossible without one.

**Status: WRONG / STALE.** The "ten, and extending requires an
architecture change" framing does not match the code as it exists today
or as it evolved -- the enum has grown twice since this annex was
written (2026-07-02) via ordinary schema edits.

**DISPOSITION 2026-07-28 (annex retirement):** `HIP_TechnicalAnnex__v20260702_1155.docx`
RETIRED, superseded-by `HIP_ArchitectureForDiligence`, no successor
minted. **retired-with-annex** -- `HIP_ArchitectureForDiligence` mentions
"the attribute taxonomy" only generically (line 199, positioning content,
no count given); it states neither ten nor any other number, so it does
not carry the correct fact forward, only the concept. Live-reverified
2026-07-28 for the record: `harness.extraction_queue.CANONICAL_ATTRIBUTES`
is now **17** (address, allergy, appointment, care_plan, dietary,
employer, financial, health_condition, household, incident, medication,
medication_status, preference, relationship, schedule, vitals,
zone_district) -- up from the 11 this register found on 2026-07-27,
confirming the "extending requires an architecture change" framing was
wrong twice over in the intervening day alone.

---

## CLAIM-10 — Internal inconsistency: four inference tiers vs. five

**Locations:** Technical Annex §2 ("four inference tiers"); site pages
(`overview.html`, `architecture.html`, `platform.html`) all describe four
(Primary, Freshness, Enclave, Passthrough); Prototype Evidence §2 table
names five distinct labels: "EDGE (qwen2.5:7b local), MID (Groq
llama-3.1-8b), CORE (Groq llama-3.3-70b), FRONTIER (BYOK passthrough),
WEB (SerpAPI freshness)" and its own prose calls it "the same five-tier
inference hierarchy."

**Evidence:** Read directly from both renderings; no code check needed --
this is a claim-vs-claim inconsistency within the package itself
(Technical Annex's own §2.3 bundles what Prototype Evidence calls two
separate tiers, WEB and MID, into one "freshness" tier).

**Status: WRONG** as an internally consistent package -- the two
companion documents (Technical Annex, Prototype Evidence) that are
supposed to describe the identical architecture disagree on how many
tiers it has.

**DISPOSITION 2026-07-28 (annex retirement): NEITHER BUCKET -- flagged,
not closed.** `HIP_TechnicalAnnex__v20260702_1155.docx` RETIRED,
superseded-by `HIP_ArchitectureForDiligence`, no successor minted. This
claim does not cleanly fall into corrected-by-supersession or
retired-with-annex: `HIP_ArchitectureForDiligence` line 34 itself says
"The tiered inference cascade across edge, mid, core, and frontier
tiers" -- **four tiers, the same undercount as the retiring annex, WEB
still missing.** Retiring the annex removes one wrong carrier but leaves
a second, currently-ratified document stating the same wrong count. This
is not resolved by retirement and should not be read as such --
`HIP_ArchitectureForDiligence` line 34 needs its own correction (to five:
EDGE/MID/CORE/FRONTIER/WEB, per Prototype Evidence's own table, unchanged
citation) in a separate pass. Named here for Bill rather than silently
carried as closed.

---

## CLAIM-11 — CandidateIntent: model proposes, deterministic policy layer decides; containment not prevention

**Locations:** Confidential WP Part II §The trust boundary is the second
half of the moat; site `moat.html` §The trust boundary (implicitly, via
"boundary... enforced at the platform level").

**Evidence:** Real, gated code: `harness/injection_contract.py` (INJ-1
through INJ-7), `eval/harnesslib/check_registry.py`, layer-7/layer-6
harness scenarios this session directly observed passing
(`scripts/run_harness.sh --layer 7`: `AUDIT` 8/8, `L7 24/24`, `L7V2
27/28`, `RATCHET PASS`). `docs/requirements/REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827.md`
MET.

**Status: PROVEN.** The specific figures cited in the WP (133-utterance
corpus, 26 governance-critical entries at 100%, 85.7% on the full
133-entry corpus) are structurally consistent with the real conformance
split in `eval/harnesslib/sia_conformance.py` (governance-critical must
be 100%, overall agreement target >=90%); exact current percentages were
not independently re-run this session -- **UNVERIFIED on the precise
number**, PROVEN on the mechanism (deterministic policy layer overrides
model classification, containment demonstrated via a real logged
injection attempt).

---

## CLAIM-12 — Recovery authority and training authority are structurally isolated, never coupled

**Locations:** Technical Annex §5.2, §5.5; Confidential WP Part XII
§12.3 ("stated explicitly because it is the one place... that could be
merged for engineering convenience, and merging them is exactly what
would collapse the trust boundary").

**Evidence:** `docs/requirements/REQ_LEARNER_SIGNAL_ISOLATION__training-signal-partition-parity-with-retrieval__v20260727_0828.md`,
Status **NOT MET** -- its own text states plainly "no learner/ranker/
reward/gradient code exists anywhere in this codebase today." Recovery
mechanics: `REQ_CRYPTO_P4_RECOVERY_EVICTION` MET at `e975695` (2-of-3
threshold quorum, real).

**Status: DESIGNED.** The isolation rule is a real, ratified design
constraint and recovery itself is built and proven; the isolation from
training is currently **vacuously true** rather than tested, because no
training/fine-tuning pipeline exists at all yet for it to be coupled to
or isolated from. Not WRONG -- but "isolated" implies two things that
could touch and don't; today there is only one of the two things.

---

## CLAIM-13 — Consortium expansion with per-operator custody, context never pooled across operators

**Location:** Confidential WP Part XIV.

**Evidence:** No multi-operator code, config, or data-boundary mechanism
exists in this repo; one Neo4j graph (`roadmap`, port 7688) and one demo
graph (`hip-dev`, port 7689) exist, both single-operator/single-household
development instances (`docs/deliverables/HIP_OperationsRunbook`).

**Status: ASPIRATIONAL.** Financial-model scenario and governance
narrative only (Financial Annex `SCENARIO_LOG`, per Part 1's audit);
nothing about actual multi-operator custody isolation has been built or
tested. Stated as future-stage narrative in its own location (Part XIV
"Stage 1: Second operator... Stage 2: Consortium" are explicitly future
triggers), so this is a lower-severity ASPIRATIONAL than claims presented
as already true.

---

## CLAIM-14 — Model portability: architected to swap models quarterly; GLM-5.2 named as a current model

**Locations:** site `substrate.html` §Open models ("Current models like
GLM-5.2 operate at roughly a tenth of the price... designed to swap in
new models quarterly"); Confidential WP Part II/IV (model-agnostic
framing, no specific model named as currently running).

**Evidence:** Technical Annex and Prototype Evidence -- the two documents
that name the actual models running today -- name qwen2.5:7b/32b (local,
Ollama) and Groq-hosted Llama 3.1/3.3/4-Scout. GLM-5.2 appears nowhere in
Technical Annex, Prototype Evidence, or any harness/code reference
(`config.yaml`, `harness/*.py`) checked this session.

**Status: WRONG** as a statement of the current model. The
swap-architecture claim itself (routing/orchestration is model-agnostic
by design) is **DESIGNED** and consistent with the real routing code's
structure (tier assignment is independent of which model serves a tier);
the specific "current models like GLM-5.2" attribution does not match
any model actually named as running anywhere else in the package.

---

## CLAIM-15 — Reference hub-node BOM (~$53K/node, 2,000-5,000 subscribers/node, specific GPU pricing)

**Locations:** Technical Annex §7.3; site `operator-case.html` §Required
infrastructure, `economics.html`.

**Evidence:** Internally consistent with `business/financial/HIP_FinancialAnnex__v20260713_2010.xlsx`'s
`node_capex` input per Part 1's audit and this session's business/
research; not independently re-priced or verified against a live vendor
quote this session.

**Status: UNVERIFIED.** Internally consistent across the package's own
financial and technical documents (a real, non-trivial check already
done -- the BOM figures were not found to contradict the Financial
Annex); what would settle it as PROVEN vs. DESIGNED: an actual purchase
order or vendor quote at the stated 2026 MSRP, which is outside this
repo's evidence.

---

## CLAIM-16 — Speaker-verifier attack surface (replay, cloning, insider mimicry) is documented and contained

**Location:** Confidential WP Part II, immediately after the CandidateIntent
section -- the paragraph itself is `[PLACEHOLDER -- Bill to write]` in
the live document.

**Evidence:** Read directly from `docs/rendered/whitepaper/nda/HIP_WhitePaper_Confidential__v20260727_1104.docx.md`
line 162 -- the placeholder names its own required content (three attack
vectors, TD-109 citation, possession-based escalation path) and states
the exact prose was never recovered.

**Status: ASPIRATIONAL** (the surrounding paragraphs' honest framing of
the limitation is real and PROVEN as a stated position; the specific
promised paragraph does not exist yet in the actual document a
counterparty would read). Named here because a claims register auditing
"what the package asserts" must also flag what it visibly intends to
assert but has not yet written.

---

## CLAIM-17 — Prototype hardware and evidence scope (Mac Mini M1 Pro, ~40 real traces, single real voice)

**Location:** Prototype Evidence §2, §9 (Honest Scope Statement).

**Evidence:** Read directly. Self-consistent with Technical Annex §8
("The prototype runs on a Mac Mini M1 Pro ([REDACTED-USER]@[REDACTED-LAN-ADDRESS]...)").

**Status: PROVEN** as an honest, self-limiting statement -- included in
this register specifically as the contrast case to CLAIM-01: this same
package, in this location, correctly disclaims exactly the
multi-voice-identity claim that other locations in the same package
assert as true. All eight `[EVIDENCE PLACEHOLDER]` blocks in sections
3-8 remain unfilled (TD-049 through TD-052, per the document's own
Known Issues section) -- the routing/latency/Bloom-agreement numbers
Technical Annex cites in passing have no populated evidence file in this
companion document to back them.

---

## CLAIM-18 — Institutional integration: certified integration surface for regulated institutions (SOC 2, ISO 27701, HIPAA, NYDFS Part 500)

**Locations:** site `platform.html` §Institutional integration;
`HIP_Site_Changes_for_WP_NDA__v20260703_1016.md.docx` §1.1 (introduces
this as "net-new," the fifth kernel).

**Evidence:** No certification, audit engagement, or compliance-program
code/doc exists anywhere in this repo. `docs/deliverables/HIP_DebtRegister_NDA_Appendix`
names TD-108 (per-fact consent ledger, IN_PROGRESS) and TD-109
(biometric consent, OPEN build requirement) as the closest real
adjacent work, both short of an actual certification.

**Status: ASPIRATIONAL.** Positioning/roadmap content, explicitly
introduced in the update guide as new site content to be reflected
*into* the WP/NDA documents -- not a built or in-progress capability.

---

## Cross-references

- **Package index**: `docs/deliverables/HIP_NDA_Package__tier1-diligence__v20260714_1400.md`
  is the structural source for which documents this register reads (its
  own Stage 1/Stage 2 item list); see
  `docs/deliverables/HIP_PackageDirectory__v20260727_1716.md` (Part 1 of
  this dispatch) for the fresh status/existence audit of every document
  named above, including the finding that the Technical Annex and
  Prototype Evidence are both STALE and excluded from the Tier-1 package,
  and that the Confidential WP location cited throughout this register is
  specifically the 2026-07-27 RECONSTRUCTED version
  (`whitepaper/nda/HIP_WhitePaper_Confidential__v20260727_1104.docx`),
  not the phantom claimed-CURRENT `v20260712_1852` (never produced).
- **HIP_PropagationWorkOrder**: never filed anywhere in this repository
  (confirmed independently this session: `find`/`git log --all
  --diff-filter=A` both zero hits across every local branch). One
  correction to how this cross-reference was asked for: the literal
  string `HIP_PropagationWorkOrder` does not appear in `build_nda.js` --
  it appears in `docs/techdebt/LATEST_DEBT.md` (TD-108: "See CHG-1 in
  HIP_PropagationWorkOrder") and in
  `business/financial/build_fin_chg5_risk_opex.py` ("PROVISIONAL CHG-5
  pending DECISION-1 see HIP_PropagationWorkOrder"). `business/ecosystem/build_nda.js`
  instead names a second, sibling, equally-never-filed document,
  `HIP_FinalizationOrder` (lines 122, 194, 200, 202 -- "FINAL CHG-1/2/4
  ... see HIP_FinalizationOrder"). Both phantom documents were already
  independently found and documented by
  `HIP_EcosystemAnalysis_Recovery__version-divergence-and-missing-decisions__v20260727_1235.md`
  (lines 158-169 of that doc), which this register's finding corroborates
  rather than duplicates. Whatever instructed CHG-1 through CHG-8 and
  DECISION-1/2/3 across the financial model and the ecosystem NDA builder
  was never filed as its own document under either name, anywhere, on any
  branch.

## Summary

- **18 claims** registered: 5 seeded by Bill, 13 found independently this
  session.
- **WRONG:** 7 (CLAIM-01, 03, 05, 08 [partially], 09, 10, 14)
- **ASPIRATIONAL:** 6 (CLAIM-07, 08 [partially], 13, 16, 18, and CLAIM-06's
  institutional-integration component)
- **DESIGNED:** 3 (CLAIM-06 in part, CLAIM-12, CLAIM-14's architecture half)
- **PROVEN (fully or "at rest"/mechanism-level):** 4 (CLAIM-02, 11, 17,
  and CLAIM-11's mechanism half)
- **DISPUTED:** 1 (CLAIM-04, Bill's own word, kept as given, with a new
  located code gap as supporting evidence)
- **UNVERIFIED:** 2 (CLAIM-11's exact percentages, CLAIM-15's BOM pricing)
- One claim (CLAIM-04) was substantiated with a genuinely new finding
  this session -- a real, located gap in `strip_context_for_tier`'s
  section coverage (`harness/orchestrator.py`) -- not previously named in
  any TD/REQ. Named here, not filed as debt, per instruction to register
  rather than correct.

**UPDATE 2026-07-28: annex retirement disposition pass.** Counts above
are the original 2026-07-27 audit and are left as the historical record,
not restated. `HIP_TechnicalAnnex__v20260702_1155.docx` (the location for
CLAIM-01/03/05/08/09/10, and the "Technical Annex" location generally) is
now RETIRED, superseded-by `HIP_ArchitectureForDiligence`, no successor
minted -- Bill's ruling that a second live architecture document would
re-create the duplicate/phantom-document problem this register and the
Package Directory audit exist to kill. Each of the six claims carries its
own dated DISPOSITION note above: CLAIM-03 and CLAIM-08
corrected-by-supersession (the surviving document already states the
correct fact, cited by line); CLAIM-01, CLAIM-05, and CLAIM-09
retired-with-annex (no live document carries the claim, right or wrong,
going forward); CLAIM-10 is the exception -- flagged, not closed, because
`HIP_ArchitectureForDiligence` line 34 repeats the annex's own four-tier
undercount rather than correcting it.
