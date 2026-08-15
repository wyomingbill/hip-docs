# CHATGPT_ConversationMemory — conversation memory review

Reviewer: ChatGPT (external research pass, routed by Bill)
Subject: conversation memory — critique of HIP_ConversationMemory_ReviewBrief.md's
proposed solution (design/HIP_ConversationMemory_ReviewBrief.md)
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED. Findings and recommendations are the reviewer's and have not
been confirmed by any dispatch. Proposes no REQ status.
SOURCE WAS A CONVERSATION, NOT A FILE ChatGPT produced independently: the body below reads
in direct second-person address ("Your diagnosis is right...", "You have not overstated
it") and opens the same way the companion Fable conversation-memory review is known to —
this is a captured conversation transcript, not a standalone research file. "Verbatim"
here means faithfully captured from that conversation, not byte-comparable against any
independent upstream artifact — no such artifact exists to diff against, and no diff was
run and presented as verification of anything beyond faithful transcription.
Source: chatgpt research context.txt (~/Downloads, note the spaces in that original
filename), banked verbatim, unedited below this header.
Date: 2026-08-03

---

Bottom line
Your diagnosis is right, but the proposed solution is not yet safe.
	1	Naïve message history is a real cross-member leak in the current architecture. You have not overstated it.
	2	“Resolve references, never carry facts” is directionally correct but technically false. A resolved subject, date, event type, predicate, or prior conversational frame is itself information carried across turns.
	3	A generative query rewriter placed before governance becomes a declassification mechanism controlled partly by attacker-supplied dialogue. That is the central security defect.
	4	The deeper architectural problem is that HIP uses natural-language strings as both the interpretation layer and the authorization interface. As long as policy depends on words such as appointment, rewriting, paraphrasing, transcription errors, or prompt injection can change authorization outcomes.
	5	The right solution is not conversational history and not unrestricted query rewriting. It is a small, typed, provenance-bearing dialogue-state layer that stores opaque references and continuation frames, with a deterministic gate between resolution and authorization.
The immediate safe improvement is simpler: detect unresolved references and refuse to call the answering model. That alone eliminates the current confident-misinterpretation failure without enlarging the security boundary.

1. Hard technical critique
1.1 Naïve history is unsafe—but history itself is not inherently unsafe
Under the current design, earlier context was admitted for the earlier requester. If it is copied into the next prompt after a speaker change, it has bypassed reevaluation against the new requester. The current turn record would attest only the newly admitted fact set while the model actually saw earlier content as well. That is a straightforward policy-bypass and record-fidelity failure.
The overstatement is narrower: all history is not necessarily unsafe. Unstructured transcripts are unsafe. A policy-labelled, audience-scoped dialogue state can be safe if every carried object remains subject to information-flow rules.
The distinction is:
	•	Unsafe: “Here are the last eight user and assistant messages.”
	•	Potentially safe: “The current utterance proposes changing the time field of authorized request frame R17 from unspecified to 08:00.”
The latter carries state without carrying an uncontrolled natural-language transcript.

1.2 “Never carry facts” is not a property the candidate design actually has
Your proposed rewrite:
“What about 8am?” → “What about 8am on the 12th, regarding the appointment conflict?”
carries at least four pieces of information across the boundary:
	•	The relevant date is the 12th.
	•	The relevant domain is appointments.
	•	The prior operation was conflict checking.
	•	The current turn continues a prior request rather than starting a new one.
Those are facts or semantic commitments, even if they are not household graph records.
The more defensible claim is:
Never carry raw admitted graph content or unrestricted model-generated answers across turns. Carry only typed, policy-labelled dialogue references and operation frames.
That is materially different from “never carry facts.”

1.3 The resolver is a declassifier
The most serious objection in your document is correct. The resolver can introduce language that changes which facts pass INJ-2. Because the contract currently uses lexical matches against the query, rewriting the query can enlarge the authorization surface.
In information-flow terminology, the resolver is effectively deciding whether information from an earlier context may influence a new privileged computation. That makes it a declassification boundary, not a convenience NLP component.
Robust-declassification research addresses almost exactly this class of problem: an attacker must not be able to manipulate the mechanism that decides what confidential information becomes releasable. (Cornell CS)
A model may propose a binding. It must never be allowed to:
	•	Mint a new subject.
	•	Mint a new attribute category.
	•	Mint a new requested operation.
	•	Convert an ambiguous pronoun into an unrestricted database selector.
	•	Insert authorization-triggering vocabulary.
	•	Decide that an inaccessible prior turn is a valid antecedent.
A constrained grammar is not enough unless the output is validated against a finite set of already-authorized objects. “Pronoun and temporal substitution only” sounds safe but is not. Resolving her to Maya, that to medication, or then to a particular date may itself select a protected subject, attribute, or record.

1.4 The core defect is lexical authorization
The resolver attack is partly a symptom of the current contract, not merely a memory problem.
INJ-2 decides relevance by matching words in the raw query against attribute-specific regular expressions. Consequently:
	•	Semantically equivalent phrasing can produce different authorization results.
	•	A typo, ASR error, paraphrase, or resolver rewrite can change admission.
	•	A malicious user can intentionally insert a keyword.
	•	A benign reference such as “that” cannot be authorized without reconstructing trigger words.
	•	Security behavior is coupled to English wording rather than a stable request representation.
The appendix identifies two additional failures that make memory work unsafe to evaluate in isolation:
	•	Household-owned facts bypass all scoping checks.
	•	Low-confidence intent classification defaults to knowledge, which is the least restrictive path and disables guards.
Those are more fundamental than conversation memory. A secure resolver cannot repair a policy engine whose default-under-uncertainty is permissive and whose authorization decisions depend on lexical accidents.
Recommendation: eliminate raw query text as an input to fact authorization. The policy kernel should authorize a typed request object.

1.5 Prior queries are not necessarily safer than prior answers
The document treats prior answers as dangerous because they contain admitted facts. Correct. But prior queries can also contain:
	•	Sensitive self-disclosures.
	•	Claims about another member.
	•	Names, diagnoses, medication names, locations, dates, or relationship information.
	•	Adversarial instructions.
	•	False assertions intended to poison future reference resolution.
Example:
Attacker: “Maya’s chemotherapy appointment is on the 12th.” Later: “What about 8am?”
Even if HIP never confirmed the first statement, a resolver reading prior queries could create a structured request about Maya’s chemotherapy.
Therefore, the relevant divide is not:
	•	Queries: safe
	•	Answers: unsafe
It is:
	•	Raw natural-language dialogue: untrusted and variably confidential
	•	Kernel-created dialogue objects: typed, provenance-bearing and policy-labelled
State should be derived from the request and policy records, not reconstructed from either transcript side.

1.6 “Same speaker only” is insufficient
Same-speaker history is a useful initial restriction, but it does not establish safety.
The same nominal speaker may have:
	•	Changed devices.
	•	Failed or uncertain voice authentication.
	•	Lost a role or caregiving permission.
	•	Been removed from the household.
	•	Changed location or co-presence.
	•	Crossed an authorization expiry.
	•	Started a new conversation branch.
	•	Been impersonated.
	•	Moved from private interaction to a room containing other people.
Every continuation must therefore be checked against:
	•	Current authenticated principal.
	•	Authentication confidence.
	•	Current authorization epoch.
	•	Current audience or co-presence set.
	•	Conversation branch.
	•	Referent expiry.
	•	Current policy version.
A fixed session_id = text-{member} cannot express those distinctions.

1.7 Speaker identity is not enough; addressee and audience matter
A multi-party household conversation needs at least three separate concepts:
	•	Speaker: who produced the utterance.
	•	Addressee: who the utterance was directed toward.
	•	Audience: who was present or entitled to share that conversational context.
Multi-party dialogue research consistently finds that speaker and interaction structure materially affect interpretation, and current systems perform worse when a second user is introduced. (ACL Anthology)
Suppose Maya says aloud:
“My appointment is at nine.”
Bill hears this. HIP may legitimately treat the exact utterance as shared conversational context. That does not imply:
	•	Maya granted Bill access to her complete appointment record.
	•	Bill can query other appointments.
	•	The graph fact changed disclosure scope.
	•	HIP can persist the information indefinitely.
	•	HIP can use the statement in another room or session.
You need to distinguish:
	1	Conversation-disclosed proposition — ephemeral and scoped to the audience.
	2	Stored household fact — governed by the graph’s standing authorization policy.
	3	Authorization grant — a separate, explicit act.
Conflating those three will produce either leaks or unusable conversation.

1.8 Clarification can itself become a privacy oracle
The obvious safe fallback—ask a clarification question—can still leak hidden context.
Unsafe:
“Do you mean Maya’s oncology appointment or Bill’s dentist appointment?”
That exposes candidate existence and possibly sensitive categories.
More subtly, even differing behavior can leak:
	•	If a hidden antecedent exists, ask a particular clarification.
	•	If none exists, say “I don’t know.”
	•	If an authorized antecedent exists, call the model.
	•	If a denied antecedent exists, return faster or use different wording.
A hostile member can probe prior private conversations through the resolver.
The required security property is:
For an unauthorized requester, adding, removing or changing hidden prior turns must not observably change the response, clarification options, model-call path or ideally the timing class.
This is a dialogue-state form of noninterference. Classical information-flow work treats noninterference as the stronger property beyond ordinary access-control checks: protected inputs must not influence observable outputs except through deliberately authorized release. (Cornell CS)

1.9 The record currently audits authorization, not understanding
The document correctly identifies this gap: the record can show what facts were admitted but not whether the system understood the question coherently.
The record needs to attest at least four stages:
	1	What was heard: transcript and ASR confidence.
	2	What was interpreted: request frame, unresolved fields and candidate references.
	3	What was authorized: permitted reference bindings and admitted graph facts.
	4	What the model actually saw: exact model-input manifest or hash.
Without stage 2, the system cannot distinguish:
	•	Fully interpreted request.
	•	Unresolved anaphora.
	•	Guessed interpretation.
	•	Ambiguous interpretation.
	•	Attacker-influenced rewrite.
Without stage 4, the record cannot substantiate the product claim. Your existing prompt-rebuild defect is evidence that “record says admitted” and “prompt contains admitted” must be mechanically tied rather than separately constructed.

1.10 Free-form history creates error persistence, not merely disclosure risk
Dialogue-state research has repeatedly documented error propagation when a predicted prior state is used as the basis of later turns. Relevant-history selection also matters because carrying too much context introduces noise, while carrying too little loses dependencies. (ACL Anthology)
For HIP, error propagation is worse because a bad binding may become:
	•	A new retrieval key.
	•	A new policy input.
	•	A misleading audit record.
	•	A source for later pronouns.
	•	An apparent user commitment.
	•	A parked write or confirmation candidate.
A mistaken antecedent must never silently become authoritative state.

2. What prior art actually gives you
There is relevant prior art, but I did not find a mature architecture that combines all four of your requirements:
	1	Multi-party reference resolution.
	2	Current-principal authorization.
	3	Information-flow guarantees.
	4	Per-turn, model-input auditability.
You are combining established components in a novel security-sensitive way.
2.1 Dialogue-state tracking and query reformulation
The NLP literature commonly handles ellipsis and anaphora through:
	•	Dialogue-state tracking.
	•	Coreference links.
	•	Slot-value copying.
	•	Context-aware query reformulation.
Rastogi et al. model reference resolution as query reformulation. CREAD jointly predicts coreference links and produces a self-contained rewritten query. (ACL Anthology)
That validates your functional instinct: completing the current query is standard practice.
It does not validate the security architecture. Those systems optimize semantic accuracy. They generally assume that all supplied dialogue context is available to the model and do not treat rewriting as an authorization-changing operation.
The closer analogue for HIP is explicit slot connection, where a system identifies a source slot and copies its value instead of freely regenerating the whole request. (ACL Anthology)
Your design should resemble controlled slot binding, not natural-language rewriting.

2.2 Multi-party discourse and speaker-aware state
Multi-party research treats speaker identity, addressee and discourse links as explicit structure. Off-the-shelf coreference models still perform relatively poorly on broader multi-party dialogue, and recent multi-user DST evaluation found a substantial degradation when a second user was introduced. (ACL Anthology)
The implication is important:
Do not assume a general LLM can reliably infer the correct speaker-scoped antecedent and then place that inference inside the security path.
Multi-party reference resolution is not a solved preprocessing step.

2.3 Conversational grounding and repair
Grounding research frames conversation as the construction and maintenance of mutual understanding, not merely response generation. Recent architectural work explicitly recommends representing shared commitments and making clarification a first-class dialogue action. (ACL Anthology)
Clarification research also treats ambiguity repair as a core part of interpretation. Systems should ask a clarification question when the request is insufficient rather than guessing and answering. (ACL Anthology)
This supports your cheaper interpretation:
The first problem to solve is not full conversation memory. It is reliable detection of ungrounded references and an explicit repair path.
That should be the first release.

2.4 Information-flow control and robust declassification
This is the most important security lineage.
The decentralized label model represents per-principal confidentiality policies and supports controlled declassification. (Cornell CS)
More recently, Microsoft’s Fides work applies information-flow control to AI agents: data carry confidentiality and integrity labels, labels propagate through computation, and deterministic policy enforcement occurs before sensitive operations. (Microsoft)
HIP’s problem is structurally similar:
	•	Prior dialogue is an information source.
	•	The resolver is a transformation.
	•	The injection contract is a privileged policy boundary.
	•	The model prompt is a confidentiality-sensitive sink.
	•	The response is an external observable.
	•	Persistent dialogue state is a cross-session propagation channel.
The lesson is not necessarily to adopt Fides code. It is to adopt the information-flow model: every context object has confidentiality, integrity, provenance and permitted destinations.

2.5 Multi-user home access control
Home environments are not simple trusted domains. Research describes them as containing complex social relationships and potentially adversarial inhabitants. (USENIX)
Studies of home IoT access control recommend capability-level controls and show that desired permissions vary by both person and device capability. Multi-user smart-home work likewise finds that present systems often lack adequate access-control and intelligibility mechanisms. (USENIX)
That supports HIP’s central premise but also argues against a single “household conversation” security domain. The household must be treated as multiple principals operating over overlapping but nonidentical contexts.

3. Recommended architecture
3.1 Replace query rewriting with typed continuation binding
The target pipeline should be:
Raw utterance
    ↓
Ambiguity / reference detector
    ↓
Candidate binder — untrusted, may use a model
    ↓
Deterministic reference-policy gate
    ↓
Typed Request Frame
    ↓
Authorization / injection kernel
    ↓
Authorized fact retrieval
    ↓
Single-source prompt assembler
    ↓
Generation
    ↓
Complete epistemic + interpretation record
The resolver does not output:
"What about 8am on the 12th, regarding the appointment conflict?"
It outputs something closer to:
{
  "operation": "CONTINUE",
  "candidate_frame": "frame_7f19",
  "patch": {
    "time": "08:00"
  },
  "confidence": 0.94
}
The security kernel then decides whether the current speaker may continue frame_7f19 and whether time is an allowed patch field.

3.2 Introduce a RequestFrame
A request frame is a kernel-created semantic object:
RequestFrame
- frame_id
- source_turn_id
- authenticated_principal
- authentication_confidence
- operation
- subject_handle
- attribute_class
- temporal_scope
- requested_result_type
- audience_label
- conversation_branch
- policy_version
- authorization_epoch
- mutable_slots
- created_at
- expires_at
- integrity_label
- confidentiality_label
For the original question:
“How do I work out whether taking the car on the morning of the 12th conflicts with any appointments?”
the frame might be:
{
  "operation": "CHECK_SCHEDULE_CONFLICT",
  "resource": "CAR",
  "date": "2026-08-12",
  "time_window": "MORNING",
  "conflict_domain": "APPOINTMENT",
  "mutable_slots": ["time_window", "time"],
  "audience": ["Bill"],
  "expires_after_turns": 3
}
The next utterance:
“What about 8am?”
does not need a rewritten sentence. It proposes:
{
  "continue": "previous_authorized_frame",
  "patch": {
    "time": "08:00"
  }
}
That is substantially easier to constrain and audit.

3.3 Introduce opaque DiscourseHandle objects
References to people, events or prior results should use opaque handles:
DiscourseHandle
- handle_id
- semantic_type
- source_turn
- source_principal
- audience
- referent_policy_label
- provenance
- integrity
- authorization_epoch
- expiry
- permitted_uses
Crucially, the resolver does not need the underlying protected value to propose:
“The phrase ‘that appointment’ probably refers to handle H42.”
The deterministic gate can then determine whether H42 is usable by the current principal.
For highly sensitive objects, even the candidate resolver should receive only:
H42: type=EVENT, introduced=previous-turn
not:
H42: Maya's oncology appointment

3.4 Derive dialogue state from records, not assistant prose
Do not feed prior assistant answers into the resolver.
After each completed turn, the kernel should derive the continuation state from:
	•	The authorized request frame.
	•	The contract output.
	•	Structured retrieval results.
	•	The disclosed response plan.
	•	The audience label.
It should not re-parse model prose.
That avoids treating hallucinated or stylistically transformed answer text as authoritative state.
Example:
Turn record:
operation = CHECK_SCHEDULE_CONFLICT
date = 12th
result = CONFLICT_FOUND
disclosed_time = 09:00
The next-turn state can expose an authorized continuation frame without preserving:
“It looks like you have a medical appointment around nine, so taking the car may be difficult…”

3.5 Keep two dialogue-state planes
Private continuation state
Available only to the same currently authorized principal:
	•	Previous request frames.
	•	Private referents.
	•	Pending clarification.
	•	Pending fact writes.
	•	Personal task state.
Shared common-ground state
Available only to the labelled audience:
	•	Publicly spoken propositions.
	•	Jointly addressed requests.
	•	Shared task frames.
	•	Explicit conversational commitments.
	•	Nothing inferred solely from a private graph fact.
A cross-speaker continuation is permitted only from the shared plane.
This handles legitimate exchanges such as:
Maya: “My appointment starts at nine.” Bill: “How long will it take?”
without turning the whole household transcript into a shared prompt.

3.6 Re-run authorization after every binding
The binding does not inherit the earlier authorization result.
The sequence must be:
Prior frame selected
    ↓
Check current speaker and audience
    ↓
Check frame integrity and expiry
    ↓
Apply permitted patch
    ↓
Construct new request frame
    ↓
Run full authorization against current policy
    ↓
Retrieve facts from zero
That preserves your core principle: every turn is independently governed.
The earlier frame supplies semantics, not authority.

3.7 Remove lexical relevance from the policy kernel
The eventual contract should receive something like:
{
  "principal": "Bill",
  "operation": "CHECK_SCHEDULE_CONFLICT",
  "subjects": ["Bill"],
  "attribute_classes": ["APPOINTMENT", "VEHICLE_AVAILABILITY"],
  "time": {
    "date": "2026-08-12",
    "start": "08:00"
  },
  "purpose": "PERSONAL_SCHEDULING"
}
The policy engine should not search the English sentence for appointment, when, or calendar.
Natural language may determine a candidate request object. It must not directly determine admission.

4. Deterministic rules for the reference gate
The gate should enforce the following.
Candidate confinement
The resolver may select only from handles supplied by the kernel. It cannot return arbitrary names, entities, predicates or dates.
Patch confinement
A continuation may change only fields listed in mutable_slots.
For the example, changing time is allowed. Changing:
subject = Maya
attribute = medication
operation = disclose
is not.
Predicate continuity
The operation must come from an authorized prior frame or be explicitly expressed in the current utterance.
Current-policy reevaluation
Every continued frame is treated as a new request under the current speaker, current audience, current authentication and current policy version.
Audience containment
A frame may be reused only if the current principal belongs to its audience label.
Integrity threshold
A referent created from an unconfirmed user assertion cannot silently become a confirmed graph selector.
Expiry and branch locality
References should expire after a small number of turns, a topic shift, a long pause, a policy change, or a conversation-branch change.
No hidden-candidate oracle
Unauthorized handles must not appear in candidate lists, clarification choices, logs visible to the requester, or distinct response behavior.
No implicit write
Resolution may never create, correct, confirm or merge a household fact.

5. Correct failure behavior
You should have three outcomes, not two.
Resolved
Exactly one authorized continuation is available with sufficient confidence.
Proceed through the full contract.
Ambiguous
More than one authorized candidate exists.
Ask a narrow clarification based only on information already authorized to the current audience:
“Do you mean the time or the date?”
Prefer slot-level questions over naming candidate people or events.
Unresolved
No authorized candidate exists, confidence is inadequate, the reference depends on hidden context, or the proposed patch is not permitted.
Return a deterministic repair request and do not call the answering model:
“I’m not sure what 8 a.m. refers to. Please include the date or event.”
Do not say whether a hidden candidate existed.
The current system instead falls through to a confident answer to another question. That should be treated as a governance failure, not merely a quality defect.

6. Required audit record
Each turn should record:
raw_transcript
asr_confidence
authenticated_principal
authentication_confidence
audience_context
conversation_branch

reference_status
candidate_handle_ids
candidate_provenance
selected_handle_id
resolver_confidence
rejection_reason
continuation_patch

typed_request_before_policy
policy_version
authorization_epoch
admitted_fact_ids
denied_fact_ids
denial_reasons

model_visible_context_manifest
model_prompt_hash
model_called
generation_tier

clarification_or_response
response_disclosure_manifest
The most important implementation rule:
The prompt must be rendered exclusively from the recorded policy output.
Do not separately rebuild a local context variable. Ideally:
policy_result → canonical manifest → prompt renderer
                         ↘ record writer
The record and prompt should be two representations of the same immutable object.

7. Formal security properties to adopt
7.1 Hidden-history noninterference
For principal P, if two conversation histories differ only in content unauthorized to P, the observable result of P’s next turn should be equivalent.
Observable result includes:
	•	Response text category.
	•	Clarification structure.
	•	Whether a model ran.
	•	Candidate count exposed to the user.
	•	Error category.
	•	Preferably coarse timing behavior.
7.2 No authority amplification
A resolver proposal may not create an operation, subject, attribute class or privilege that is absent from:
	•	The current utterance; or
	•	An authorized, audience-compatible prior frame.
7.3 Prompt-record equivalence
The model-visible context manifest must equal the set represented in the turn record.
ModelVisibleObjects(turn) = RecordedModelVisibleObjects(turn)
7.4 Speaker-switch safety
Replacing the current principal with another principal must force complete policy reevaluation and must not expose prior private frames.
7.5 Revocation safety
After an authorization epoch changes, no prior handle may remain usable without reevaluation.
7.6 Integrity preservation
An attacker-controlled utterance may propose a reference but may not increase the integrity or confirmation status of the referent.
7.7 Fail-closed ambiguity
No answering model runs when a governance-relevant reference remains unresolved.

8. Test plan
Differential hidden-history tests
Run the same current turn against two histories:
	•	History A contains a hidden Maya appointment.
	•	History B does not.
Bill’s output must be equivalent in both.
Speaker-swap tests
Replay an identical continuation as:
	•	The original speaker.
	•	Another household member.
	•	An unknown voice.
	•	A low-confidence speaker match.
	•	A formerly authorized caregiver.
Resolver-poisoning tests
Prior utterances attempt to plant:
	•	Protected names.
	•	Attribute triggers.
	•	Fake consent.
	•	Instructions to the resolver.
	•	False graph facts.
	•	Cross-member references.
Patch-escalation tests
A continuation that should change only time attempts to change:
	•	Subject.
	•	Attribute category.
	•	Operation.
	•	Sharing scope.
	•	Write status.
Revocation tests
Create a valid handle, revoke access, then reuse the handle.
Branching tests
Two conversations introduce separate appointments. Test:
	•	“The other one.”
	•	“What about her?”
	•	“Move it earlier.”
	•	Speaker changes between branches.
Audit mutation tests
Deliberately alter:
	•	Contract result.
	•	Prompt manifest.
	•	Local prompt context.
	•	Record fact set.
The system should detect mismatch before model execution.

9. Recommended build sequence
Stage 0 — fix the unsafe defaults
Before adding memory:
	•	Change uncertain intent to the most restrictive path.
	•	Remove blanket household-fact admission.
	•	Make prompt assembly consume only the contract’s canonical output.
	•	Add a prompt/context manifest to the record.
	•	Treat unresolved anaphora as a pre-model hard stop.
Stage 1 — same-speaker typed continuation
Support only:
	•	Same authenticated principal.
	•	Same conversation branch.
	•	Previous one to three turns.
	•	Explicit mutable slots.
	•	Time, date and ordinal substitutions.
	•	No raw prior assistant text.
	•	No cross-speaker references.
This solves the 8am example safely.
Stage 2 — authorized private referents
Add opaque handles for:
	•	People.
	•	Events.
	•	Objects.
	•	Prior request frames.
Still restrict reuse to the same principal.
Stage 3 — audience-labelled common ground
Add multi-party continuation only after you can represent:
	•	Addressee.
	•	Audience.
	•	Co-presence.
	•	Ephemeral disclosure scope.
	•	Cross-speaker authorization.
	•	Hidden-candidate noninterference.
Stage 4 — model-assisted binding
Only after deterministic candidate generation and gating exist should an LLM rank or select candidate handles. The model remains outside the trusted computing base because it cannot mint or authorize objects.

Final architectural ruling
Do not implement the proposed free-form resolver.
Implement this instead:
A model may propose a continuation patch over a finite set of policy-labelled request frames and opaque discourse handles. A deterministic kernel validates that patch, reconstructs a typed request, and re-runs authorization from zero.
And immediately implement:
When anaphora is unresolved, no answering model runs.
The fundamental correction is to stop treating a rewritten English sentence as a trustworthy security input. Conversation state needs to be structured, labelled and provenance-bearing. Authorization then operates on that structure, while natural language remains an untrusted proposal layer.
