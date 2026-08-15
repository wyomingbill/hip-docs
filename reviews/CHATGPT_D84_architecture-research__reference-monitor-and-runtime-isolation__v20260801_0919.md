# CHATGPT_D84_architecture-research — reference monitor, complete mediation, runtime isolation

Reviewer: ChatGPT (external research pass, routed by Bill)
Dispatch: D-84 (companion to the Fable recon banked alongside this file)
Subject: an adversarial research pass on the monolith-vs-services question — whether
"monolithic inside a hard boundary, contracted outside it" is a named pattern and where it
is documented; whether distribution is a security property; how to make an in-process
boundary structural rather than conventional; what forces a split at tiny scale; whether a
self-auditing process is acceptable to real auditors; and where the inference boundary
belongs.
Method: literature-grounded argument. External research — NOT a code read of this
repository. Where it describes HIP's code it is repeating Bill's framing, not verified
observation; the code-grounded half of D-84 is the Fable recon banked beside it.
Version: v20260801_0919 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED. Citations are the reviewer's and have NOT been checked against
the cited sources by this dispatch. Proposes NO status and NO REQ.
Date: 2026-08-01

**This is a named source of `REQ_ARCHITECTURE_BOUNDARY`.** Banked verbatim under D-85 as
provenance for the ruling that the governance core is a REFERENCE MONITOR whose target
property is COMPLETE MEDIATION — vocabulary this pass supplies and which the REQ adopts.

Headline as filed: the conclusion is "partly right for the wrong reason." Keeping the core
in one deployable unit is sensible, but *monolithic* does not create the security property;
complete mediation does. The pass separates three boundaries Bill's ruling conflated —
source-code, runtime, and trust — and argues only the third bears on the product claim. Its
recommendation is not microservices but **one local reference-monitor daemon plus ordinary
clients over Unix-domain IPC**: logically monolithic, runtime-isolated.

Read alongside the Fable recon, the two agree on direction and differ in what they can
support: this pass supplies the literature and the naming; the recon supplies the file:line
evidence that the property is currently absent.

---

Verdict
Your conclusion is partly right for the wrong reason.
Keeping the governance core in one deployable unit is sensible. But “monolithic” does not create the security property you care about. The security property is:
Every read, disclosure, inference-context construction, mutation, and export involving governed data must be completely mediated by a small, tamper-resistant reference monitor.
A monolith can satisfy that. It can also fail catastrophically if arbitrary code in the same process can reach the database driver, mutate memory, invoke internal functions, use reflection, or obtain an unrestricted store handle.
Your current ruling conflates three different boundaries:
	1	Source-code boundary: modules and interfaces
	2	Runtime boundary: processes, address spaces, capabilities and operating-system permissions
	3	Trust boundary: what compromised or careless code is physically able to do
Only the third matters to your product claim.
The adversarial conclusion is:
Keep the policy semantics cohesive, but do not rely on in-process modularity as the structural enforcement boundary. Make the fact store and disclosure path accessible only through a narrow reference-monitor interface, preferably enforced by a separate process or equivalent runtime isolation.
That does not imply microservices. On one household box, it can be one small local daemon plus ordinary clients communicating over Unix-domain IPC.

1. What is this pattern actually called?
There is no single canonical pattern called “monolithic inside a hard boundary, contracted outside it.”
Your design combines several established ideas.
A. Modular monolith
“Modular monolith” is the closest contemporary architecture label:
	•	One deployment unit
	•	Internal modules with defined interfaces
	•	No requirement for network-distributed services
	•	Cohesion preserved within the process
But “modular monolith” is mostly practitioner terminology, not a formally defined security architecture. The deeper academic basis is Parnas’s information-hiding decomposition: divide modules according to design decisions likely to change, and hide those decisions behind interfaces rather than decomposing merely by execution sequence. (DOI)
That literature supports separating:
	•	Voice transport
	•	Governance semantics
	•	Demonstration machinery
	•	Storage implementation
	•	Model adapters
It does not establish that module boundaries enforce security against hostile in-process callers.
B. Ports and adapters / hexagonal architecture
Your “voice-to-core is a contract, not shared code” resembles ports-and-adapters architecture:
Voice adapter ──┐
Demo adapter  ──┼── Governance port ── Core
Admin adapter ──┘
That is useful for substitutability and testing. It is not a security mechanism unless the runtime prevents adapters from reaching around the port.
There is no strong empirical security evidence that hexagonal architecture itself prevents authorization bypass. Treat it as a maintainability structure.
C. Reference monitor / security kernel
This is the important name.
The classical reference-monitor requirements are:
	1	Complete mediation: every security-sensitive operation is checked.
	2	Tamper resistance: the mechanism cannot be altered or bypassed.
	3	Verifiability: it is small and simple enough to analyze.
Security research continues to use these as the criteria for deciding whether trusted software actually enforces policy. (usenix.org)
Your governance core is aspiring to be an application-level reference monitor.
More precisely, its minimum trusted subset is a security kernel:
Identity binding
Policy evaluation
Context construction
Authorized disclosure
Mutation admission
Audit commitment
Everything else should be outside the trusted computing base where practical.
NIST’s Policy Machine work makes the same high-assurance argument: reduce the amount of trusted enforcement code while supporting precise policy and confinement. (NIST)
D. Single-writer actor or state-machine owner
“Exactly one process owns writes” resembles:
	•	Actor ownership
	•	Single-writer state machine
	•	Encapsulated aggregate
	•	Serialized command processor
The useful property is not “actor” as branding. It is:
No other principal possesses the authority required to alter the authoritative state.
That is stronger than “everyone promises to call the right library.”
Recommended name
Call the architecture:
A local reference-monitor service implemented as a modular monolith, with capability-restricted ports and single-writer state ownership.
That is cumbersome but accurate.
Do not describe it simply as a modular monolith. That understates the security requirement.

2. Does distribution improve security?
Your intuition is too broad.
What distribution makes worse
Splitting each ordered gate into a separately callable service can increase:
	•	Authenticated endpoints
	•	Serialization boundaries
	•	Credential handling
	•	Service identities
	•	Retry behavior
	•	Partial failures
	•	Version skew
	•	Confused-deputy risks
	•	Opportunities to call gate 4 without gates 1–3
	•	Opportunities to replay an old authorization result
	•	Observability complexity
	•	Policy-state inconsistency
Microservice research reports that distributed characteristics introduce distinct security difficulties, including tool weakness, expanded interfaces and practitioner knowledge gaps. One empirical study analyzed 861 security-related artifacts from open-source systems and practitioner discussions; it does not prove microservices are categorically less secure, but it confirms that distribution creates a substantial additional security-management burden. (arXiv)
A newer literature review likewise identifies expanded attack surfaces, interaction complexity and dependency-management weaknesses across microservice systems. (arXiv)
There is no credible universal empirical result showing that microservices are more secure than monoliths or vice versa. Most claims are conditional architectural reasoning, case studies or practitioner reports.
What distribution can improve
Distribution can improve security when it creates a real trust separation:
	•	Different OS identities
	•	Separate address spaces
	•	Independent credentials
	•	Database permissions
	•	Sandboxing
	•	TEE isolation
	•	Independent administrators
	•	Distinct signing keys
	•	Network allowlists
	•	Minimal capabilities per component
For example, separating an untrusted parser from a sensitive store can reduce compromise impact if the parser process has no store authority.
Capsicum was built precisely to compartmentalize historically monolithic UNIX applications by placing components into capability-restricted sandboxes. Its security benefit comes from kernel-enforced authority restriction, not from service decomposition itself. (usenix.org)
PDP and PEP separation
Policy literature separates logical responsibilities:
	•	PDP: computes the authorization decision.
	•	PEP: actually prevents or permits the operation.
RFC 2753 defines these roles and describes a PEP at the protected node with a potentially remote PDP. (IETF Datatracker)
NIST similarly defines the PEP as the entity that enforces the authorization decision and the PDP as the decision function. (NIST Computer Security Resource Center)
But these are logical roles, not a mandate for separate network services. RFC 3838 explicitly allows the PDP–PEP interface to remain internal when both reside in the same implementation.
That directly undermines any claim that security architecture requires distributing PDP and PEP.
The real design rule
Keep PDP and PEP tightly coupled when:
	•	The protected resource is local
	•	Policy state is local
	•	There is no independent failure-domain need
	•	Network separation provides no meaningful trust boundary
	•	The operation must be atomic with authorization
	•	Latency and availability matter
Separate them when:
	•	Multiple independent enforcement points share policy
	•	The decision-maker requires information unavailable locally
	•	Policy administration must be independently governed
	•	Different trust levels require isolation
	•	A compromised resource process must not alter policy
	•	Central policy consistency outweighs availability concerns
For HIP, the dangerous split is:
Identity service
  → sensitivity service
  → consent service
  → sharing service
  → policy service
  → storage service
That architecture forces you to prove global ordering and freshness across distributed state.
A safer design is:
Governance transaction:
  bind principal
  resolve object
  evaluate policy
  construct permitted view
  commit decision
  mutate/disclose
  append audit event
inside one transactional authority.

3. Can you make the boundary structural inside one process?
The blunt answer
Not against genuinely hostile code with equal in-process privilege.
Code in the same address space generally shares:
	•	Process credentials
	•	Heap access, directly or indirectly
	•	Loaded secrets
	•	Database connections
	•	File descriptors
	•	Environment variables
	•	Native libraries
	•	Debugging and reflection facilities
	•	Crash authority
Language mechanisms can constrain ordinary code. They usually cannot withstand malicious code that can use unsafe operations, native extensions, reflection or runtime compromise.
Therefore, distinguish three threat classes.
Caller
Module privacy sufficient?
Careless developer
Often
Ordinary bug
Sometimes
Malicious dependency
Usually not
Compromised component
No
Native-code exploit
No
Process owner/root
No
Module privacy
Examples include private packages, non-exported functions, sealed modules and restricted constructors.
These prevent accidental misuse and reduce API surface. They do not normally create a security boundary against code executing with equivalent runtime authority.
Use them, but describe them as defect prevention, not hostile-code containment.
Type-level enforcement
Types can ensure that certain operations require values that can only be constructed through approved flows.
Example:
fn commit_write(
    authorization: WriteAuthorization,
    mutation: ProposedMutation,
) -> Result<CommittedMutation, Error>
where WriteAuthorization has a private constructor.
This can make bypass difficult in safe, statically checked code. Information-flow type systems can even prove noninterference properties under specified language assumptions. (arXiv)
But the guarantee collapses when:
	•	Unsafe code can fabricate values
	•	Serialization can reconstruct the type
	•	Reflection bypasses constructors
	•	The authorization object is cloneable or reusable
	•	The token is detached from exact mutation content
	•	FFI reaches the database directly
	•	A caller obtains the underlying store handle
	•	The codebase contains another write path
Types help prove properties of programs that obey the language model. They do not protect against arbitrary code execution in the process.
Capability tokens
Capabilities are stronger when they are:
	•	Unforgeable references
	•	Narrowly scoped
	•	Non-ambient
	•	Non-serializable or cryptographically bound
	•	Revocable where required
	•	Enforced by the runtime or OS
	•	Passed only to components that need them
The capability tradition goes back to Dennis and Van Horn’s protected computation model. (CiNii Research)
The practical lesson from Capsicum is that useful security comes when the operating system restricts what file descriptors and resources a compartment can access. (usenix.org)
An ordinary signed JSON “capability token” is weaker than an OS capability. It can still work, but now security depends on:
	•	Signature-key protection
	•	Audience binding
	•	Nonce handling
	•	Expiry
	•	Exact operation binding
	•	Replay prevention
	•	Revocation semantics
Admission proof
An “unforgeable admission proof” can be useful, but do not overrate it.
A proof or signed decision must bind at least:
principal
subject/member
operation
object or query
permitted fields
purpose
policy version
fact-store version
time or validity interval
request nonce
model destination
maximum disclosure
Otherwise, a caller can reuse a legitimate authorization for a different mutation or disclosure.
Even correctly designed, the proof is irrelevant if the caller can bypass the function requiring it and write directly to the store.
Single write path
This is the core.
The only defensible pattern is:
All other code:
    no database write credentials
    no writable file descriptor
    no direct mutable store reference

Governance owner:
    exclusive write authority
    validates commands
    executes mutation
    emits committed audit record
Inside one process, you can approximate this with:
	•	A private database connection
	•	No exported mutable repository
	•	An opaque command API
	•	Private authorization types
	•	Static dependency checks
	•	Build-time architecture tests
	•	No reflection or unsafe code in the trusted core
	•	Restricted FFI
	•	Code review and linting
	•	Property-based tests
	•	Mutation testing for bypasses
But against hostile code, move the writer to a separate process with separate OS credentials.
Best practical architecture
Not microservices. One local service:
hip-governance
  Owns:
    fact-store write credentials
    encryption keys
    policy evaluation
    authorized context construction
    audit commitment

  Exposes:
    Unix-domain socket
    small versioned protocol
    peer credential validation
    command-level authorization

voice
demo
admin UI
models
  Have:
    no fact-store credentials
    no encryption keys
    no direct writes
Process mediation research makes the central point: authorization should be automatically interposed on every controlled operation because relying on programmers to remember to call the monitor loses complete mediation. (usenix.org)
That is your present library problem exactly.

4. When should the governance core split?
Not when usage grows. Split when a trust, atomicity, failure or assurance boundary demands it.
Trigger 1: untrusted parsing or media code
Voice pipelines process complex media formats and large native-code dependency trees. A memory corruption bug in audio decoding should not imply fact-store access.
Split voice from governance now. You already ruled correctly on this.
Trigger 2: model runtime requires broad privileges
A local model server may require:
	•	GPU access
	•	Large native libraries
	•	Downloaded model artifacts
	•	Python packages
	•	Network access
	•	Plugin systems
That is an ugly trust domain. It should not share governance keys or storage credentials.
Trigger 3: remote inference
Once any context may leave the box, outbound disclosure becomes a PEP. It deserves a distinct, narrow interface and preferably a separate egress broker.
Trigger 4: independent audit protection
If reviewers require that compromised governance code cannot rewrite history, audit storage needs separate authority.
This does not necessarily require a separate physical machine. It can require:
	•	Separate process
	•	Separate key
	•	Append-only filesystem or database role
	•	TPM-backed signing
	•	Remote anchoring
	•	Operator-controlled witness
	•	Write-only log channel
Trigger 5: TEE placement
If keys or policy processing run in a TEE but model inference does not, the enclave boundary forces decomposition.
Do not move arbitrary application code into the TEE merely to say you use one. Keep the enclave-resident trusted computing base small.
Trigger 6: different update provenance
Suppose:
	•	Operator controls the base image
	•	HIP controls policy code
	•	TTS vendor updates voice models
	•	Household installs optional skills
Those have different supply-chain trust. Separate them before allowing independent update channels.
Trigger 7: safety-critical liveness
If governance crashing would also kill emergency communication, you may need a minimal independent path for:
	•	Emergency calling
	•	Device control
	•	Caregiver alerting
Do not put every function behind one failure domain merely because one writer is desirable.
Trigger 8: administrative separation
A future institutional customer may demand that:
	•	Policy authors cannot edit audit logs
	•	Developers cannot access household data
	•	Operators cannot decrypt content
	•	Support cannot modify policy
Those are separation-of-duty requirements, not scale requirements.
Trigger 9: availability policy
A remote PDP can fail closed and make the household product unusable. A local PDP/PEP can remain available but may operate on stale policy.
The moment HIP has remotely administered policy, you need an explicit answer to:
What is the safe behavior when policy freshness cannot be established?
Trigger 10: independent verification burden
If one component becomes too large to review as a reference monitor, split untrusted computation away from it. The reference-monitor principle explicitly values a small mechanism that can be analyzed. (usenix.org)

5. Is self-auditing a real problem?
Yes, but not always a disqualifying one.
What ordinary reviewers accept
Many production systems generate their own audit records. Regulators and security reviewers do not universally require an independent logging machine.
They generally expect:
	•	Defined auditable events
	•	Correct record content
	•	Reliable timestamps
	•	Retention
	•	Access restrictions
	•	Protection against modification and deletion
	•	Separation of audit-management privileges
	•	Review and alert procedures
	•	Response to logging failure
NIST guidance explicitly requires protecting audit information and logging tools from unauthorized access, modification and deletion, and limiting audit-management authority to a subset of privileged users. It warns that privileged users who are also audit subjects may undermine log reliability. (NIST Publications)
That does not require an independent process in every system.
What your ledger currently proves
An append-only hash chain inside the governance process can establish:
	•	Ordering
	•	Detection of later record alteration, if the terminal hash is preserved elsewhere
	•	Internal consistency
	•	Correlation among events
It cannot establish:
	•	That omitted events never occurred
	•	That the process logged denied and allowed actions completely
	•	That the process did not fabricate events
	•	That the process did not fork the ledger
	•	That the process did not rewrite the entire chain and its local head
	•	That timestamps are trustworthy
	•	That the running code matched the claimed build
This is the completeness problem, not merely the immutability problem.
A malicious process can produce a perfectly valid hash chain containing lies.
Minimum credible design
For a household product:
	1	Governance constructs the event.
	2	A separate append-only logger receives it over a write-only interface.
	3	The logger assigns or confirms sequence number and timestamp.
	4	The logger hash-chains the event.
	5	Periodically, the ledger head is signed with a hardware-protected key.
	6	The signed head is anchored outside the governance process.
Possible anchors:
	•	TPM monotonic state
	•	Operator service
	•	Household owner’s device
	•	Remote transparency service
	•	Periodic encrypted backup
Self-securing storage research shows why retaining versions outside the compromised host’s normal control improves forensic reliability: attackers cannot silently erase the earlier state. (usenix.org)
Recent audit-system research reaches the same underlying conclusion: once the operating system is compromised, unprotected local audit logs cannot be trusted, particularly if protection is delayed. (usenix.org)
But do not overbuild this
A separate logger still consumes events supplied by governance. It cannot independently know whether governance omitted an event unless it mediates the operation itself or receives corroborating observations.
Therefore:
	•	Separate logging improves tamper resistance.
	•	It does not automatically prove complete mediation.
For stronger assurance, the storage layer itself could emit mutation receipts, and the egress layer could emit disclosure receipts. Then the ledger correlates evidence from multiple enforcement points.

6. Should inference be outside the boundary?
Yes, but refine what “outside” means.
Treat every inference engine—local or remote—as untrusted with respect to policy.
That includes:
	•	STT models
	•	Embedding models
	•	Rerankers
	•	LLMs
	•	TTS models
	•	Classifiers
	•	Third-party APIs
	•	Locally downloaded weights
Why
A model can:
	•	Hallucinate authorization
	•	Ignore instructions
	•	Reconstruct sensitive facts from supplied context
	•	Emit data placed into its prompt
	•	Be prompt-injected
	•	Contain malicious or compromised code
	•	Log prompts
	•	Send telemetry
	•	Cache inputs
	•	Produce tool calls outside the intended scope
	•	Generate output that reveals more than requested
The model should never decide whether it is entitled to receive data.
Correct direction of authority
Untrusted request
      ↓
Governance identifies principal and operation
      ↓
Governance resolves permitted facts
      ↓
Governance constructs minimal context pack
      ↓
Inference receives bounded context
      ↓
Inference returns untrusted candidate output
      ↓
Governance performs output checks and disclosure decision
      ↓
Response delivered
The context pack is the controlled object.
The model must receive:
	•	No store handle
	•	No unrestricted retrieval tool
	•	No encryption keys
	•	No authority to expand scope
	•	No raw household graph
	•	No ability to commit memories directly
	•	No ability to address a different member
	•	No persistent capability beyond the turn
The mistake in “call from inside the boundary out”
If the governance process directly hosts generic HTTP clients, model adapters, SDKs and vendor libraries, you have pulled a large dependency surface into the reference monitor.
Prefer:
Governance process
    creates sealed inference request

Inference broker
    validates destination constraints
    calls local or remote model
    returns candidate output

Governance process
    validates response
    commits permitted effects
The broker receives only the released context, not store authority.
Local does not equal trusted
A local model server can still be:
	•	Compromised
	•	Misconfigured
	•	Replaced
	•	Maliciously updated
	•	Vulnerable through native libraries
	•	Able to read process memory if co-located without isolation
Locality solves some confidentiality and latency problems. It does not establish authorization correctness.
Output mediation is underdeveloped in your ruling
You focus heavily on what enters context. That is necessary but insufficient.
You also need to govern:
	•	What can leave the model
	•	Which member receives it
	•	Whether output combines individually harmless facts into a sensitive inference
	•	Whether the model repeats hidden metadata
	•	Whether generated tool calls exceed the original authorization
	•	Whether a permitted answer becomes impermissible after a speaker change
The PEP must sit at both context entry and response delivery.

7. What you are not asking
A. What exactly is the protected operation?
“Fact access” is too narrow.
HIP must mediate at least:
Read
Search
Traverse relationship
Infer
Aggregate
Summarize
Compare members
Export
Speak aloud
Display
Notify
Embed
Cache
Train or fine-tune
Correct
Supersede
Delete
Reclassify
Change sharing scope
Create derived fact
Invoke tool
A system can protect direct reads while leaking through summaries, embeddings or aggregate inference.
B. Are facts the correct security object?
Your rule says “a fact belongs to a member.” That may be structurally inadequate.
Many household claims involve multiple people:
	•	“Susan says Michael is drinking.”
	•	“John and Mary are divorcing.”
	•	“The caregiver missed Tuesday’s visit.”
	•	“Alice owes Bob money.”
	•	“The argument occurred in the kitchen.”
Who owns that fact?
Potential security principals include:
	•	Subject
	•	Speaker
	•	Creator
	•	Custodian
	•	Source
	•	Affected party
	•	Household
	•	Care team
	•	Legal authority
The access-control object may need to be an attributed claim with multiple stakeholder relationships, not a fact owned by one member.
This is probably a larger threat to your architecture than monolith versus services.
C. Can the policy chain be expressed as one decision?
An ordered chain of imperative gates invites hidden control-flow errors.
Consider representing it as:
	•	A formally specified decision function
	•	Explicit deny-overrides or precedence semantics
	•	A decision table
	•	A state transition
	•	A policy algebra
	•	A model-checkable rule set
FACPL research is relevant because it gives ABAC policy combination and missing/error values formal semantics and supports automated analysis through SMT encoding. (arXiv)
Your “ordered gates” may be understandable but harder to prove complete than a declarative policy with explicit combining semantics.
D. What happens on missing or contradictory attributes?
Examples:
	•	Speaker verification uncertain
	•	Subject unresolved
	•	Custody status stale
	•	Sharing policy unavailable
	•	Policy version mismatch
	•	Ledger unavailable
	•	Time source untrusted
	•	Caregiver role expired
	•	Two authorities conflict
You need explicit outcomes beyond allow/deny:
ALLOW
DENY
NOT_APPLICABLE
INDETERMINATE
REQUIRE_CONFIRMATION
DEFER
SAFE_LIMITED_RESPONSE
The most dangerous implementation is one where exceptions or missing data accidentally become allow.
E. Can authorization be revoked during a turn?
Voice interactions are not instantaneous:
	1	Speaker begins.
	2	Identity is resolved.
	3	Context is built.
	4	Model generation starts.
	5	Another person enters.
	6	Speaker identity confidence changes.
	7	Permission is revoked.
	8	Audio continues playing.
You need a revocation and re-evaluation model for long or streaming turns.
F. Is the identity evidence fresh enough?
Speaker verification is probabilistic. It is not a durable principal identity by itself.
Authorization decisions should include:
	•	Verification confidence
	•	Recent challenge state
	•	Device possession
	•	Physical context
	•	Session age
	•	Voice replay detection
	•	Whether another speaker is present
Your structural access-control claim is only as strong as principal binding.
G. Who can alter policy?
Your focus is runtime enforcement, but policy administration may be the easiest attack.
You must mediate:
	•	Who changes sharing scopes
	•	Who appoints caregivers
	•	Who adds household members
	•	Who changes recovery trustees
	•	Who resolves conflicting claims
	•	Who downgrades sensitivity
	•	Who deletes audit records
	•	Who rotates keys
The PDP can faithfully enforce maliciously altered policy.
H. Does the ledger create a new privacy hazard?
A comprehensive immutable household ledger may become the most sensitive object in the system.
It can reveal:
	•	Who asked about whom
	•	Suspicion and conflict
	•	Health concerns
	•	Relationship patterns
	•	Failed access attempts
	•	Presence and absence
	•	Behavioral changes
“Append-only” conflicts with minimization, correction, household departure and some deletion obligations. You need a design for:
	•	Encrypted event payloads
	•	Cryptographic erasure
	•	Retention tiers
	•	Redacted views
	•	Key revocation
	•	Minimal event content
	•	Ledger metadata leakage
I. What is the recovery authority?
If the governance daemon corrupts its policy database or loses keys, who restores it?
Recovery can silently create a superuser that bypasses the entire architecture.
Your recovery path belongs inside the threat model, not in operations documentation.
J. What is the trusted computing base?
Write it down explicitly.
A plausible first pass:
Trusted:
- Boot chain
- OS kernel
- governance daemon
- policy engine
- key service
- fact-store adapter
- disclosure/context builder
- audit commitment client

Conditionally trusted:
- append-only logger
- identity verifier
- time source
- update mechanism

Untrusted:
- voice stack
- demo UI
- model runtimes
- downloaded model weights
- remote APIs
- plugins
- household clients
- network
Then ask whether the trusted set is actually small enough to inspect.

Recommended ruling
Retain
	•	One governance authority per household
	•	Single writer to authoritative facts
	•	Cohesive policy evaluation
	•	Ordered or formally combined checks
	•	Voice and demo outside the core
	•	Models treated as clients
	•	Per-turn audit record
Change
1. Stop calling an in-process module a hard boundary
It is not one unless the language/runtime provides and preserves genuine isolation.
2. Make governance a small local daemon
Not a distributed cloud service. Not five microservices.
One box
One governance daemon
One authoritative store
One narrow IPC interface
Many untrusted local clients
3. Give only the daemon write authority
Enforce this with OS credentials, database permissions and key custody—not import discipline.
4. Separate policy semantics from enforcement mechanics internally
Within the daemon:
Request normalization
Principal binding
Policy evaluation
Authorized-view construction
Mutation/disclosure enforcement
Audit commitment
Separate modules, one transactional authority.
5. Move model SDKs and runtimes out
The daemon should emit a minimal sealed context request to an inference broker. It should not contain a zoo of model-vendor libraries.
6. Protect audit externally enough to match the claim
For an early system:
	•	Hash-chain events
	•	Separate logger process
	•	Hardware-protected signing key
	•	Periodic external ledger-head anchoring
	•	Explicit logging-failure behavior
Do not claim the ledger proves completeness.
7. Define the product claim carefully
Defensible:
“No component outside the governance authority has credentials or capabilities to read or mutate the authoritative household fact store directly.”
Potentially indefensible:
“No code can ever bypass governance.”
Root, kernel compromise, malicious firmware or governance-process compromise can defeat the system unless you add stronger hardware isolation.

Final adversarial assessment
Your instinct that “splitting the gates into services makes bypass easier” is generally plausible and supported by established complete-mediation reasoning. It is not established as a universal empirical law.
Your larger mistake is believing the alternative is “keep the gates in one process.”
The actual choice is:
	•	Conventional boundary: everyone imports the right library.
	•	Structural boundary: unauthorized components lack the authority required to reach the protected operation.
A monolithic governance daemon can provide the second. An in-process library usually cannot.
The architecture should therefore remain logically monolithic but runtime-isolated:
One local reference monitor, one writer, one transactional policy decision, narrow capability-bearing interfaces, untrusted inference outside, and audit evidence protected beyond the decision-maker’s sole control.
That is not premature microservices. It is the minimum architecture consistent with your central product claim.
