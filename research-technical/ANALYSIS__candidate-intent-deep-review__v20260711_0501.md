# ANALYSIS: CandidateIntent Deep Review
Status: BUILT
Reconciled-Against: docs corpus 2026-07-11 (SIA_SPEC__structured-intent-architecture__v20260710_1614, SIA_SHADOW_DIFF__v20260710_2106 and __v20260710_2204, TRUTH_LAYER__phase1-provenance-trust__v20260705_0704, HITL__phase4-findings__v20260708_0951 F-5, DEBT_REGISTER__v20260709_0855); no code read in this pass

---

## 0. What is being reviewed, stated precisely

The decision under review: every model-produced classification is a CandidateIntent, a proposal with no authority. An identity envelope, established by authentication (voiceprint or session), never by the model, travels alongside it. A deterministic policy envelope evaluates the candidate against authenticated identity, household membership, attribute sensitivity, and explicit capability grants. The model cannot establish identity, authorization, consent, or permission to read or write governed data. Confidence is advisory: a malicious 0.99 has the same authorization power as an honest 0.01, which is none.

In the corpus this decision is embodied concretely: the SIA spec's Structured Intent Object is the CandidateIntent (stateless classification, strict schema validation, deny-safe default); `speaker_relationship` derived by code and never emitted by the model is the identity envelope discipline (SIA_SPEC section 2.2); the injection contract INJ-1 through INJ-7 is the policy envelope; and the motivating incident is real and documented: A6-05, where qwen2.5:7b obeyed embedded JSON in an adversarial utterance and returned type=statement, attribute=medication at confidence 0.9, and where a prompt-level defense did not fix it (SIA_SHADOW_DIFF v20260710_2204: A6-05 still fails post-fix; Phase A gate FAIL).

One housekeeping finding before the analysis, because a diligence team would trip on it in the first hour: the corpus has a TD-109 numbering collision. The debt register (every version from v20260707_0816 through v20260709_0855) defines TD-109 as the biometric consent-and-retention build requirement (CHG-8). The HITL Phase 4 findings say F-5, the cross-member write authority gap, was "elevated to TD-109." These are two different items sharing one identifier. The write-authority gap needs its own register ID before any external document references it. This review uses "F-5" for the write-authority question throughout.

---

## 1. Challenging the decision

The decision is correct as far as it goes. The honest critique is about where it stops, and about one foundation it takes for granted.

### 1.1 The identity envelope rests on another probabilistic classifier

The architecture's central claim is that identity is established out-of-band, deterministically, and the model cannot touch it. But the band's anchor is speaker verification, which is itself a probabilistic biometric model with a false-accept rate, a false-reject rate, and a commodity attack surface: replay of recorded audio, synthetic voice cloning (now achievable from seconds of sample audio with open tools), and mimicry by household members who have unlimited enrollment-quality samples of each other's voices. The CandidateIntent pattern does not eliminate the untrusted-classifier problem; it relocates it from intent classification to identity classification. That relocation is still valuable (the intent classifier sees attacker-controlled text every turn; the speaker verifier sees attacker-controlled audio only when the attacker is physically present or has planted a playback device), but the white paper must not describe the identity envelope as deterministic. It is deterministic *downstream of* a probabilistic authentication event. The honest formulation: the envelope is immutable once bound, and binding is a separately attackable step with its own error rates. TD-109's non-biometric fallback (PIN, passphrase, device possession) is not just a consent nicety; it is the only path to an identity binding that is not itself a model output. For high-sensitivity actions, the policy envelope should be able to demand escalation from voiceprint-bound identity to possession-bound identity.

### 1.2 The pattern governs authorization, not truth

CandidateIntent gates who may do what. It does not gate whether the content of an authorized write is correct. An authenticated member with legitimate write authority over their own record, whose utterance is mis-extracted (wrong attribute, wrong value, hallucinated entity), produces a wrong governed fact through a fully authorized channel. A6-05 is read in the corpus as an authorization threat, but its nearest-term consequence is a poisoning threat: injected text firing write detection puts attacker-chosen content into the store under the *speaker's own* legitimate identity. The trust ladder is the mitigation surface here (the fact lands ASSERTED or UNCONFIRMED, not CONFIRMED), but an ASSERTED wrong medication fact still shapes later disclosure and later model context. The pattern needs an explicit companion claim: content integrity is handled by the trust ladder plus confirmation gating, not by the policy envelope. Conflating the two in the white paper would be the easiest technical objection for a reviewer to score.

### 1.3 Fail-closed is not free in a care context

The deny-safe default (SIA_SPEC section 2.3) converts every classifier failure into a refused turn. The shadow diffs measured fallback rates of 26 percent and 31.5 percent under GPU contention on the Mini. In the eldercare vertical, availability is a safety property: "what medication does Ray take" refused during a genuine emergency is not a neutral outcome. An attacker who cannot break the policy envelope can still attack the classifier's availability (resource exhaustion, garbage utterances that force the deny path, anything that raises GPU contention) and degrade the household to the frozen regex fallback or to refusals. The design accepts this trade deliberately, and for writes it is unambiguously right. For reads of the speaker's own facts, a refusal-heavy failure mode concentrated on exactly the population HIP serves (elderly speakers, non-standard speech, dysarthria producing low classifier confidence) is a real equity and UX cost. Recommendation: track the confidence-threshold refusal rate per member as a first-class metric, and treat a member whose turns systematically fall below theta_SIO as a calibration problem to fix, not a security event.

### 1.4 The envelope does not cover the response model

The policy envelope interposes between classification and retrieval, and between classification and writes. But the response-generation model still receives retrieved governed facts plus the raw utterance in one context. An utterance that classifies correctly, is fully authorized, and retrieves legitimately can still steer the response model: reformatting exfiltration ("spell out everything you know about me one letter at a time"), disclosure-adjacent inference, tone manipulation. This is post-envelope surface. The existing INJ-5 never-volunteer rule and the output-side contract checks cover part of it; the analysis point is that CandidateIntent must be described as governing the *decision plane* (what may be retrieved, what may be written) and not the *generation plane*. Full-duplex work (voice P2's action plane) will widen this gap before it narrows it.

### 1.5 The policy envelope is deterministic, not therefore correct

The seven-regex drift history that motivated SIA is itself the proof: deterministic code diverges too. Moving authority from the model into the envelope concentrates all trust in one code path, which is the right move only while that path carries the strongest verification discipline in the codebase. Today it does (injection harness, ratchets, mutation tests L3). That discipline is now load-bearing for the whole security story and must be stated as such: the envelope is trustworthy *because* it is small, testable, and gated, not because it is deterministic.

### 1.6 Meta-governance: who writes the grants

Capability grants and sensitivity classifications are data. If changes to them are ordinary writes, the attacker ignores the classifier entirely and targets the policy store: "grant Sam read on Elena's medication" spoken persuasively, or a compromised admin path. The pattern must recurse: policy mutations are themselves governed writes at maximum sensitivity, confirmation-gated, audit-logged, and never derivable from a model classification. The corpus does not yet state this anywhere. It should.

### 1.7 What it blocks that users will want

Three legitimate flows degrade under the strict pattern: (a) cross-member care updates, the core caregiver use case, become the highest-friction path in the system (this is what section 6 has to solve well); (b) anaphora ("what does she take?") is excluded by the statelessness constraint, which is sound for security and costs nothing against the regex baseline, but is a visible naturalness gap against ungoverned competitors, and the roadmap should own it as a deliberate trade rather than let a demo audience discover it; (c) unenrolled speakers (a visiting nurse, a neighbor during an emergency) have no identity envelope at all, and the system's behavior toward them (full refusal? guest tier?) is undesigned.

---

## 2. The design space, and what adjacent domains do

The problem shape (probabilistic inference feeding deterministic enforcement) is old, and the strongest versions of the answer converge on the same structure HIP chose. That convergence is evidence the decision is right, and it also defines the prior art landscape for section 4.

**Operating systems and formal security.** The policy envelope is a reference monitor in the classic Anderson (1972) sense: always invoked, tamper-resistant, small enough to verify. Confirmation tokens bound to actor, action, subject, and expiry are capabilities in the capability-security sense: unforgeable, communicable authority tokens. The correct academic frame for the multi-entity problem is decentralized information flow control (Myers and Liskov's decentralized label model): each fact carries owner-set and reader-set labels, and declassification requires the owner's authority. HIP's per-member disclosure rules are a DIFC instance even though they were not derived from it; adopting the vocabulary would sharpen both the design and the paper.

**Aviation and control systems.** The Simplex architecture (Sha, UIUC): an unverified high-performance controller runs inside a verified safety envelope, with a deterministic decision module that reverts to the safe controller when the complex one proposes an out-of-envelope action. This is structurally identical to SIO-plus-deny-safe-default. Runtime assurance (ASTM F3269 for bounded flight controllers) is the certified form. The lesson HIP has not yet absorbed from this domain: the safety controller must be *independently* competent, not merely restrictive. HIP's frozen regex fallback is the degraded controller; Simplex practice says measure its competence explicitly and never let it silently rot.

**Healthcare.** CDS Hooks in the HL7 ecosystem returns "cards": suggestions from clinical decision support that a clinician must accept before they touch the record. That is CandidateIntent with a human as the policy envelope. The Epic sepsis model's external validation failure (Wong et al., JAMA Internal Medicine 2021: AUC far below vendor claims in deployment) is the canonical case for why vendor confidence scores must carry zero decisional authority, and is citable support for the confidence-is-advisory rule. FHIR's Consent and Provenance resources are the closest existing standards shape for the trust ladder's provenance records; aligning field vocabulary with FHIR Provenance costs little and buys interoperability credibility in the eldercare vertical.

**Finance.** SR 11-7 (Federal Reserve model risk management) mandates that models receive "effective challenge" and that model output feeds controls rather than constituting them; fraud scores advise, deterministic rule engines decide, and thresholds are human-owned. The maker-checker (four-eyes) pattern in payment operations is confirmation-gated writes, decades old, with a well-documented failure mode HIP must design against: checker habituation (section 6.2).

**Military C2.** DoD Directive 3000.09 requires appropriate human judgment over force decisions; the two-man rule binds high-consequence actions to two independent authenticated actors. The transferable insight is *independence of channels*: the confirmation must not flow through the same channel that produced the proposal. HIP's version of this is section 6.3's requirement that confirmation parsing never route through the full SIO classifier.

**LLM security specifically.** HIP independently replicated the field's consensus finding: instruction-hierarchy and prompt-level defenses do not withstand embedded instructions (A6-05 survived a prompt fix). The structural answers in the literature are the dual-LLM pattern (Willison: a quarantined model touches untrusted data, a privileged model never does) and CaMeL (Debenedetti et al., Google DeepMind 2025: capability-based policies over a control-flow/data-flow split, where untrusted text can never become control flow). SIA is a CaMeL-family design arrived at independently: the SIO schema is the control-flow interface, and strict enum rejection is what keeps utterance text from becoming control flow. Two design-space options the corpus has not evaluated: (a) constrained decoding at the token level (grammar-constrained generation, e.g. llama.cpp GBNF grammars through Ollama), which makes schema violation impossible rather than detected-and-rejected, and would have converted A6-05's obedient JSON into a parse the attacker cannot shape freely; note this constrains *form* only, not semantic obedience, so it complements rather than replaces the golden-set gate; (b) taint propagation, carrying an utterance-derived label on every SIO field through to the response so downstream code can distinguish "attribute=medication because the model said so" from "attribute=medication because a deterministic rule matched." Option (a) is cheap and recommended; option (b) is a Phase C consideration.

---

## 3. What is actually novel here

The generic untrusted-classifier pattern is not novel, and the white paper should not claim it is. The multi-entity household context changes the problem in ways the generic pattern does not address, and that is where the novelty lives.

**The adversary is inside the trust boundary, permanently.** Enterprise threat models assume attackers are outside or transient insiders. Household members are permanent insiders with physical device access, unlimited voice samples of each other, knowledge of each other's histories (defeating knowledge-based fallback auth), and social authority over each other. No commercial voice platform models this adversary at all.

**Existence-invariance between co-equal principals.** INJ-7's existence-invariant refusal already recognizes that between household members, *metadata is payload*: "I can't share that" versus "I have nothing about that" leaks whether a record exists, and between siblings or spouses that leak is the harm. Single-user governed systems never face this because there is no co-principal to leak to. HIP has a working structural answer (the F4 fix made cross-member denial existence-invariant) and should claim it explicitly; it is the most defensible novel control in the system.

**Disclosure into a shared acoustic channel.** Speaker verification authenticates the asker, not the audience. A correctly authorized disclosure spoken aloud reaches everyone in the room. No one has solved room-composition-aware disclosure; the honest options are conservative modes (sensitive facts only to authenticated single-listener channels like a phone), speaker-count estimation from audio (another probabilistic classifier, with the same CandidateIntent discipline applied), or explicit user-set modes ("private mode"). The white paper should name this as open rather than let a red team name it first.

**Cross-principal provenance.** Facts about member X asserted by member Y are the normal case in a household (that is what caregiving is), and they cross identity and authority boundaries at write time. The trust ladder plus the identity envelope gives HIP the machinery to represent this (provenance records who asserted; the envelope guarantees the who is authentic), which generic single-principal provenance systems do not need and do not have. F-5 is exactly this machinery missing one rule, not a redesign.

**Subjects who are not principals.** Ray and Elena are care recipients: data subjects with no credentials, possibly no capacity to consent, whose most sensitive data is precisely what the household needs to share to care for them. Guardianship as a runtime authorization concept (declared authority, scoped by attribute domain, revocable, with capacity gradients in both directions: children aging into rights, elders declining out of them) is unsolved in consumer AI and only partially solved in clinical systems (proxy access in patient portals is the nearest analogue, and it is coarse). This is HIP's hardest and most valuable open problem, and section 6 shows the confirmation-token schema is where it first becomes concrete.

**Coercion.** The policy envelope enforces rules; it cannot detect that a member is speaking under duress. Alarm-industry duress codes (a second PIN that opens the door and silently alerts) have no analogue in any AI memory system. Flag as future work; do not claim a solution.

---

## 4. Competitive and IP mapping

**Who else does this.** No consumer platform does policy-mediated multi-entity memory. Amazon and Google both treat voice identification as convenience-grade, not authorization-grade (Alexa requires a PIN for purchases regardless of voice ID; Google Voice Match documentation disclaims security use). Apple's HomePod personal requests punt entirely: identity for sensitive actions is delegated to phone proximity, which is possession-based auth and quietly concedes that voiceprint alone is insufficient, a concession that supports HIP's section 1.1 posture. Personal-memory startups (Rewind/Limitless class) are single-principal by construction. Enterprise AI governance (Purview-class DLP over copilots) governs org-versus-platform, not principal-versus-principal within a shared context. The combination (multi-entity governed memory, deterministic policy interposition, trust-graded provenance, edge-resident) has no visible occupant.

**IP surface.** The individually old components (reference monitor, capabilities, maker-checker, DIFC) are unpatentable prior art. The plausible claims are combinatorial and contextual: (1) an immutable identity envelope bound at a biometric or possession authentication event, traveling with untrusted classifier proposals through a household-scoped policy evaluation; (2) confirmation tokens bound to actor, action, subject, and expiry in a *voice* modality, with the independence property of section 6.3; (3) trust-ladder-gated supersession (write monotonicity, section 5.3); (4) existence-invariant cross-principal refusal in a shared-memory system. A patent attorney should assess (2) and (3) first; they are the most specific. Trade-secret posture on the harness corpus (golden sets, A-series attacks) is worth more than it looks: the attack corpus is the reproducible evidence of the security claims.

**What the white paper should claim.** The pattern, precisely: model classifications are proposals; identity, authorization, and consent are established outside the model; confidence carries no authority; enforcement is deterministic, small, and adversarially tested in CI. The finding: an edge classifier obeyed embedded instructions, a prompt-level defense failed, and the architecture is designed so that this class of failure is contained by construction, with the A6 harness as standing evidence. The honesty play is strong here: "our classifier was successfully injected, and here is why it did not matter" is a better NDA-appendix sentence than any claim of prevention.

**What it must not claim.** That prompt injection is prevented (A6-05 is open; the claim is *containment*). That speaker recognition is secure authentication (TD-109 is open; voice anti-spoofing is unproven; Apple's proximity punt shows the industry's own assessment). That consent controls exist (the register is explicit: no such public claim until TD-109 ships). Any quantitative security bound. Any compliance certification (see section 7; there are named gaps).

**Due diligence survivability.** A competent technical DD team would find, in rough order: TD-101 (unauthenticated endpoints, flagged in the register as highest severity: an immediate red flag they will weigh far above architectural elegance), the 26 to 31 percent fallback rate under GPU contention (undermines the edge-latency story until serving is fixed), the TD-109 collision (a documentation-integrity ding), TD-030/TD-122 (embedding pipeline gaps touching the encryption-at-rest story), and the open A6-05. They would also find things few startups have: a reconciled-against discipline linking every claim to a commit, a five-layer verification harness with ratcheted baselines, mutation testing of the security path, and a written record of the system's own failures. Verdict: the *architecture* survives scrutiny; the *implementation maturity* does not yet, and the corpus itself is honest about that. The correct NDA posture is to present the gap list proactively with the register as the artifact.

---

## 5. The trust ladder interaction

The ladder (evaluation order DERIVED, CONFIRMED, CORROBORATED, ASSERTED, UNCONFIRMED, first match wins, per TRUTH_LAYER section 4) is an epistemic lattice: how much to believe a fact. The policy envelope is an authorization lattice: who may see or change it. The central design question is whether they may couple, and the answer is: in one direction only.

### 5.1 Trust must not loosen disclosure

Should a CONFIRMED fact be disclosable under looser conditions than an ASSERTED one? No, and for two structural reasons. First, it creates a promotion attack: if higher trust buys wider disclosure, then the harden transition (repeated consistent assertion promotes toward CORROBORATED) becomes a privilege-escalation path. Two colluding members, or one member repeating an assertion across sessions, launder a fact up the ladder and out of its disclosure restrictions. Authorization would then depend on write history, which members control, rather than on grants, which policy controls. Second, it creates the side channel the question anticipates: if disclosure behavior varies with trust level, an authorized reader learns the trust level, and trust level reveals provenance shape ("the system hedged, so this came from Dad, not from the doctor"). Between household members, provenance is itself sensitive: *who told the system about Mom's diagnosis* can be a bigger secret than the diagnosis. The rule: the policy envelope evaluates identity, membership, attribute sensitivity, and grants. Trust level flows only to the presentation layer, as hedging language for readers who already passed the envelope. One consequence worth writing into the injection contract: the hedging text itself must not name or imply the asserting member to a cross-member reader unless provenance disclosure is separately granted.

### 5.2 Classifier confidence must not feed the ladder

A second coupling must be explicitly severed. SIO confidence measures parse quality ("how sure am I this utterance is a medication statement"). Ladder confidence measures world truth ("how well-established is this fact"). If extraction confidence seeds the fact's `confidence` field, then A6-05-class injection, which produced a 0.9, mints high-confidence facts, and the injected write lands mid-ladder instead of at the bottom. The invariant to state and gate: a fact's initial ladder position derives from write provenance and the deterministic ladder rules only; no model self-score appears anywhere in the ladder computation. Whether current code violates this is unverified in this pass; it belongs in the next harness sweep as a P-series invariant.

### 5.3 Where trust should gate: writes

The one correct coupling runs the other way, and F-5 is its proof. Maya's single ASSERTED statement silently superseded Ray's CORROBORATED seed fact: a lower-trust fact destroyed a higher-trust one. The ladder should gate *supersession* with a monotonicity rule: a write may not silently replace a fact with one of lower trust. It may append alongside it as UNCONFIRMED or shadow it pending confirmation, and a confirmation token (section 6) may authorize the supersede explicitly. This uses the ladder to protect data integrity (its native job) without ever letting it modulate access. Second-order effect worth noting: under this rule an attacker gains something from *blocking* promotion (keeping a true fact UNCONFIRMED so it can be superseded cheaply), which is another reason promotion transitions must be deterministic and logged, as TRUTH-104 already requires.

---

## 6. Confirmation-gated writes

The recommendation: sensitive writes require explicit confirmation tokens bound to the authenticated actor, the proposed action, the subject, and a time-bound expiry. Does it solve F-5 cleanly?

### 6.1 What it solves

It resolves Fork B exactly: no silent cross-member overwrite, because supersession of another principal's fact requires a token, and the token requires an explicit confirming act. The binding tuple is right: actor binding prevents token theft across members; action-and-subject binding prevents a token harvested for a benign write from authorizing a different one; expiry bounds replay. Structurally, the token is a capability, the confirming act is the maker-checker second signature, and the audit record (token issued, token consumed, by whom, for what) is precisely what F-5 found missing. It also composes with, rather than competes against, Fork A: a declared caregiver authority (Fork A) is naturally expressed as a standing grant that determines *who may confirm* writes about a given subject, while the token mechanics determine *how* confirmation happens and is proven. Ray cannot confirm writes about himself if capacity is gone; Maya's declared authority makes her the valid confirmer; the token binds her identity to the act. Forks A and B are one design, and the guardianship problem from section 3 gets its first concrete data structure: the confirmer role on the token.

### 6.2 Confirmation fatigue

The known failure mode of every maker-checker deployment: checkers habituate and approve reflexively, and the control degrades to theater. The mitigation is scope discipline. Tokens must gate only the intersection of high sensitivity, cross-principal effect, and trust regression (the section 5.3 monotonicity trigger). A member's routine writes about themselves must never prompt. If the prompt rate for a normal household week exceeds single digits, the scope is wrong and the control is eroding. This should be a measured quantity in the harness era, not a hope: log tokens-issued per member-week and alarm on drift, the same discipline as the fallback-rate alarm.

### 6.3 The recursion problem, which is the real design content

In a voice system, the confirming act is an utterance. If that utterance flows through the full SIO classifier, the confirmation is itself a CandidateIntent produced by the untrusted model, and the loop has a hole: injected text that fires a write could in principle also fire its own confirmation. The independence principle from the two-man rule applies: confirmation must not flow through the channel that produced the proposal. Concretely: a pending token puts the session into a constrained-confirmation state where the next turn is evaluated by a deterministic closed-vocabulary gate (yes, no, cancel, and tight synonyms; exact match after normalization; anything else is a decline), with the speaker identity of the confirming turn required to match the token's confirmer binding. The SIO model never sees the confirming turn as a classification task. A6-05-class injection then cannot self-confirm, because no model output participates in confirmation at all. This requirement is the difference between confirmation-gating as a control and confirmation-gating as a ritual, and it belongs in the spec as a LOCKED constraint.

### 6.4 Voice-flow edge cases

Mid-sentence and mid-conversation: the write parks. The ladder already provides the landing zone most systems lack: the proposed write lands immediately as UNCONFIRMED (visible, hedged, harmless to integrity), the token is issued, and the system requests confirmation at the next turn boundary. If confirmed, the write promotes and the supersede executes; if the token expires, the fact simply remains UNCONFIRMED. Expiry degrades epistemically instead of losing data, and nothing is silently dropped, which matters because "the system ignored what I told it" is a worse care-context failure than "the system is not yet sure." Expiry should be conversation-relative (N turns or end-of-session, whichever first) rather than wall-clock alone; a fixed five-minute window behaves badly in exactly the long, meandering conversations the user base will have. Session timeout mid-token: the token dies with the session, the UNCONFIRMED fact persists, and the next session can surface it ("you mentioned a medication change yesterday; should I record it?"), which turns the edge case into a feature. The unresolvable case: the confirmer is not the speaker and is not present (Maya asserts, Maya must confirm, Maya leaves). Same answer, UNCONFIRMED persistence plus deferred prompt; no design should try to be cleverer than that.

### 6.5 Verdict

Confirmation-gating solves F-5 cleanly *provided* three commitments are written into the spec: the section 6.3 independence constraint (no model in the confirmation path), the section 6.2 scope discipline with a measured prompt-rate, and the section 6.4 park-as-UNCONFIRMED semantics. Without 6.3 it is circular; without 6.2 it erodes; without 6.4 it loses data or blocks conversation. With all three it is the strongest single addition the architecture can make, because it also instantiates the guardianship model.

---

## 7. Production readiness against control frameworks

What a compliance team would find, mapped control-by-control. Summary first: the verification and change-management story is unusually strong for the maturity stage; the access-control and operations story has named holes; nothing found contradicts the architecture.

### 7.1 NIST AI RMF

| Function | Maps to | Assessment |
|---|---|---|
| GOVERN | INDEX.md discipline, reconciled-against fields, debt register | Strong documentation-of-record habit; gaps: no risk register distinct from tech debt, no roles/accountability statement (single maintainer), no AI policy document |
| MAP | SYSTEM_UNIVERSE, LIVE_CALLGRAPH, EPISTEMIC_PROCESS docs | Genuinely good: context, components, and divergences are mapped and dated |
| MEASURE | Five-layer harness, golden sets, ratcheted baselines, L3 mutation tests, A-series adversarial corpus | The standout. Ratcheted adversarial testing in CI maps directly to MEASURE 2.x TEVV expectations and exceeds most production teams; gap: no post-deployment monitoring plan beyond the fallback-rate alarm, no drift measurement for the classifier in the field |
| MANAGE | Deny-safe defaults, fail-closed enum rejection, fallback alarm | Fail-safe posture maps well to MANAGE; gaps: no incident-response procedure, no documented rollback, no user-facing redress path (a member disputing a fact about them has no defined channel) |

### 7.2 ISO 42001

An AIMS certification is premature and a team would say so in the first meeting: no scope statement, no management-system documentation, no internal audit function, and single-maintainer risk (bus factor of one) is an organizational nonconformity no architecture can fix. The interesting finding runs the other way: Annex A's impact-assessment requirement, applied to a multi-entity household, has no template anywhere; HIP performing and publishing a household-level AI impact assessment (who is affected, including non-consenting subjects like care recipients and visitors) would be both a compliance artifact and a differentiator, since the framework authors have not worked this case.

### 7.3 SOC 2

| Criteria | Finding |
|---|---|
| CC6 logical access | Immediate fail while TD-101 stands: unauthenticated endpoints void the story regardless of envelope quality. The policy envelope is strong *application-layer* access control sitting on an unlocked network layer |
| CC6 encryption at rest | Claimed for the store, undercut by TD-030 (embeddings encode fact values) and TD-122's fallback behavior; the embedding pipeline is inside the data-at-rest boundary and must be treated as such |
| CC7 monitoring | Partial: dashboard health panel and fallback alarm exist; no alerting path when nobody is watching the dashboard |
| CC8 change management | Strong and evidenceable: gate_check.sh, ratcheted baselines, RED-confirmed-before-fix discipline in the testing docs constitute a real change-control trail |
| Audit trail | Provenance records plus per-turn metadata are a good base; gap: no tamper-evidence on logs, and audit of *policy* changes does not exist yet (section 1.6) |

### 7.4 What they would praise

Deterministic enforcement outside the model with the model stripped of authority (maps cleanly to emerging EU AI Act human-oversight and logging expectations); existence-invariant refusal as a designed control rather than an accident; adversarial self-testing with the system's own confirmed failures documented in-corpus; and the reconciliation discipline, which is the rarest item on the list and the one that makes every other claim checkable.

---

## 8. Consolidated recommendations

1. Fix the TD-109 collision: assign F-5 its own register ID before any external document cites it.
2. Reframe the identity envelope honestly (section 1.1): immutable once bound, probabilistically bound; add possession-based escalation for maximum-sensitivity actions; this also derisks the TD-109 (biometric) claims path.
3. Adopt grammar-constrained decoding for the SIO call (section 2, option a): removes the free-form JSON attack surface A6-05 exploited; cheap; complements, does not replace, the golden-set gate.
4. State and gate the two severed couplings: trust never loosens disclosure (5.1); classifier confidence never seeds ladder confidence (5.2, add as harness invariant).
5. Adopt the write-monotonicity rule (5.3) and confirmation tokens with the three commitments of 6.5, including the LOCKED no-model-in-the-confirmation-path constraint (6.3).
6. Add meta-governance (1.6): policy and grant mutations are governed, confirmation-gated writes.
7. Before any operator demo or DD exposure: close TD-101, and fix classifier serving so the fallback rate reflects design intent rather than GPU contention (1.3, 7.3).
8. White paper language: claim containment, not prevention; claim the pattern, the finding, and the harness; do not claim consent controls, secure speaker authentication, or compliance readiness (4).
9. Name the open problems proactively in the NDA appendix: shared-acoustic-channel disclosure, guardianship and capacity, coercion (3). Naming them is credibility; being asked about them is not.

The decision itself is correct, convergent with the strongest analogous systems in five other domains, and worth committing to. The risks are not in the pattern; they are in the two places the pattern's own logic is not yet applied to itself: the authentication event that mints the identity envelope, and the policy store that the envelope consults.
