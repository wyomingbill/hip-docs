# CHATGPT_EvalMethodology — evaluation methodology review

Reviewer: ChatGPT (external research pass, routed by Bill)
Subject: evaluation methodology for an access-controlled conversational system —
answers the prompt in research-technical/HIP_EvalMethodology_ReviewPrompt.md
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED. Findings and recommendations are the reviewer's and have not
been confirmed by any dispatch. Proposes no REQ status.
Source: gpt-test_research.txt (~/Downloads), banked verbatim, unedited below this header.
Date: 2026-08-03

---

Overall assessment
There is no single accepted evaluation standard for an access-controlled conversational AI. The defensible approach combines four established traditions:
	•	Access-control model verification
	•	Software model-based and property-based testing
	•	Behavioral and dynamic NLP evaluation
	•	Runtime trace verification and information-flow testing
The system should be evaluated as a policy-enforcement mechanism with a probabilistic language interface, not as a chatbot with some security tests added.

1. Generating inputs outside the system’s tuning distribution
Accepted practice
Practitioners generally use several complementary corpus sources rather than trying to calculate one universal “distance from training” score:
	1	Behavioral capability matrices: Enumerate phenomena such as indirect reference, slang, ellipsis, corrections, bundled requests, role claims, topic omission and speaker changes. For each phenomenon, create minimum-functionality, invariance and directional tests. This is the approach formalized by CheckList for NLP systems. (ACL Anthology)
	2	Human/model-in-the-loop challenge collection: Give people access to the current system and ask them to produce natural, valid inputs on which it fails. Dynabench is the best-known example of this dynamic evaluation approach. (ACL Anthology)
	3	Natural distribution shifts: Collect examples from different speakers, channels, rooms, microphones, dialects and interaction contexts, rather than only paraphrasing the original templates. WILDS uses naturally occurring domain shifts instead of assuming that synthetic perturbation captures deployment shift. (Proceedings of Machine Learning Research)
	4	Failure-derived transformations: Whenever production or human testing finds a failure, identify the linguistic phenomenon that caused it and create a family of structurally different examples—not lexical substitutions.
There is no accepted scalar measure of how far one free-form utterance lies from a language model’s tuning distribution. Embedding distance, perplexity and lexical novelty can help characterize a corpus, but none is a reliable operational definition of “tail difficulty.” Textual OOD itself contains different kinds of shift, including semantic and background shift. (ACL Anthology)
Practical construction
Tag every test by dimensions such as:
topic_named: yes/no
referent_named: yes/no
speaker_known: yes/no
prior_turn_required: yes/no
directness: direct/indirect
syntax: complete/fragment/self-correction
register: formal/casual/slang
request_shape: single/bundled
pressure: none/urgency/role/second-attempt
Then measure coverage of those dimensions and their interactions, not merely the number of utterances.
Cost
Medium to high. The expensive part is human production and independent adjudication, not generation.
Known failure
Model-in-the-loop collection can overrepresent contentious or genuinely ambiguous cases, and results can depend heavily on which model annotators were trying to defeat. It can create a harder set without creating a more representative one. (ACL Anthology)

2. A two-sided evaluation that does not reward blanket refusal
Accepted practice
Treat the policy decision as a binary decision problem:
Policy truth
System releases
System withholds
Release permitted
Correct release
False denial
Release prohibited
False release
Correct denial
The closest established analogy is biometric evaluation, which reports false-accept and false-reject rates separately rather than combining them into one accuracy score. (NIST Computer Security Resource Center)
For HIP, report at least:
False Release Rate
= prohibited cases that released protected information
  / all prohibited cases

False Denial Rate
= permitted cases that failed to provide the authorized information
  / all permitted cases

Useful Authorized Answer Rate
= permitted cases producing a substantively useful answer
  / all permitted cases
“Did not disclose unauthorized content” and “gave a useful authorized answer” are separate assertions. A vague response that avoids both disclosure and usefulness is not a successful allow case.
Avoiding metric gaming
Do not collapse these into one weighted score. Use independent release criteria:
	•	No critical false releases, or a specified statistical upper bound.
	•	False-denial rate below its own ceiling.
	•	Useful-answer rate above its own floor.
	•	Results stratified by sensitivity, speaker relationship and linguistic difficulty.
Where a threshold controls answering versus withholding, report a curve across thresholds. Selective-prediction research calls this the risk-coverage tradeoff: reducing errors by abstaining also reduces the fraction of requests the system serves. (ML Anthology)
Cost
Low to medium once the policy oracle exists.
Known failure
Aggregate rates hide rare but serious categories. A system can perform well overall while failing on medication, guests or cross-member questions. Report category-specific denominators and uncertainty intervals. The threshold should not be chosen from the same test set used for final reporting.

3. Deriving expected outcomes independently from implementation
Accepted practice
Access-control testing conventionally distinguishes:
	1	The intended policy.
	2	A policy model or specification.
	3	The enforcement implementation.
	4	Tests generated from or checked against the model.
NIST explicitly recommends policy models to bridge the gap between human policy and enforcement mechanisms, followed by verification and implementation-conformance testing. (NIST)
The practical middle ground is an executable decision model, not a full formal proof.
For each test, the oracle should consume structured inputs:
{
  "requester": "sam",
  "subject": "maya",
  "record_class": "medication",
  "operation": "read",
  "audience": ["sam"],
  "purpose": "general_inquiry",
  "consent_state": "none",
  "relationship": "household_member"
}
and return:
{
  "decision": "DENY",
  "reason": "CROSS_MEMBER_MEDICAL",
  "permitted_fields": []
}
Write this reference model from the policy document, preferably by someone who did not write the production enforcement code. Use decision tables for rule review and generate tests from the table.
Add policy mutation testing: deliberately alter a reference rule—swap allow/deny, remove a condition or broaden a subject class—and verify that the suite detects the change. NIST access-control work discusses test-oracle generation, model testing and mutation-style techniques because passing tests do not establish that the oracle or rule coverage is adequate. (NIST Computer Security Resource Center)
Cost
Medium. The hard work is resolving contradictions and omissions in the written policy.
Known failure
The reference model can encode the same misunderstanding as the implementation. Independent authorship reduces that risk but does not eliminate it. Ambiguous policy cases need an explicit status such as:
ALLOW
DENY
CONDITIONAL
POLICY_UNSPECIFIED
Do not force unspecified cases into allow or deny merely to make the test executable.

4. Testing the mechanism rather than refusal wording
Accepted practice
Use grey-box conformance testing against a stable semantic execution trace.
Runtime verification tests whether an execution trace satisfies a specification of permitted behavior. It is commonly paired with generated test cases where output alone cannot establish that the required internal sequence occurred. (OSL)
Define a test-facing trace contract containing semantic events:
speaker_authenticated
request_interpreted
policy_evaluated
record_authorized
record_withheld
prompt_manifest_committed
model_invoked
response_emitted
state_write_proposed
state_write_committed
Then assert properties such as:
When decision = DENY:
    model_invoked = false
    admitted_record_ids = []
    response_source = deterministic_policy_layer

When decision = ALLOW:
    prompt_record_ids = authorized_record_ids
    no other record IDs are present
Do not assert internal class names, function calls or source-file paths. Those are implementation details. Assert a versioned semantic trace API.
The record and prompt should derive from the same immutable authorization manifest:
policy decision
      ↓
authorization manifest
      ├── prompt assembler
      └── execution record
This is more important than checking that the log merely claims the right decision. Recent grey-box privacy testing has shown why inspecting internal control flow can detect violations that black-box outputs cannot reliably expose. (Pet Symposium)
Cost
Medium. It requires instrumentation and a stable event schema.
Known failure
Logs can lie, omit events or describe a different object from the one actually supplied to the model. Test the trace pipeline itself, including deliberately creating a prompt-manifest mismatch. Refactoring should be allowed to change implementation but not the semantic trace contract without an explicit schema version.

5. State discipline for mutating cases
Accepted practice
Divide tests into two categories.
Isolated transition tests
Each case begins from a known snapshot and runs one operation:
seed → execute → assert state and trace → discard
Use transaction rollback, database cloning, copy-on-write fixtures or a fresh household namespace. Randomize execution order periodically; an isolated suite should produce the same results in any order.
Stateful scenario tests
Test deliberate sequences against an explicit reference state machine:
initial state
→ Bill asserts X
→ Maya confirms X
→ Sam requests X
→ permission changes
→ Sam requests X again
Property-based state-machine testing generates valid action sequences, maintains an independent model of expected state and checks postconditions after each action. (ScienceDirect)
For every case, record:
starting_fixture_hash
starting_policy_version
starting_record_version
test ID
mutation set
ending_fixture_hash
A failure caused by an earlier case then becomes detectable rather than mysterious.
Cost
Low if the storage layer supports fast snapshots; potentially high if every test requires rebuilding external services.
Known failure
Perfect isolation misses bugs that arise only after long interaction sequences. Keep most tests isolated, but maintain a smaller dedicated sequence suite with generated and hand-authored state transitions.

6. Reporting something you structurally cannot measure
Accepted practice
Report it as:
NOT EVALUATED
Reason: Evaluation population contained no independent impostor speakers.
Evidence available: Genuine-speaker false-rejection testing only.
Conclusion permitted: None regarding false acceptance of other humans.
Do not report zero, “passed,” or an empty cell.
NIST’s AI RMF explicitly says that risks or trustworthiness properties that cannot be measured should be documented, and that inability to measure a risk does not imply either high or low risk. (NIST AI Resource Center)
With one enrolled human, you can evaluate:
	•	Genuine-speaker false rejection
	•	Repeatability across microphones and conditions
	•	Replay behavior, if relevant
	•	Some synthetic perturbation behavior
You cannot estimate a population-level false-accept rate for different humans. Synthetic voices or altered recordings can be labelled proxy engineering tests, but not substituted for the missing measurement.
Cost
Documentation costs almost nothing. Obtaining the missing evidence requires additional participants, consent procedures, representative recording conditions and enough trials to estimate a meaningful upper bound.
Known failure
Teams routinely turn proxy results into stronger claims than the evidence supports. Include an evidence-level field:
measured / proxy / analytically derived / not evaluated

7. Fixed suite versus regenerated suite
Accepted practice
Use a hybrid with three separately reported populations.
A. Frozen anchor suite
A versioned set that never changes within a major evaluation series. It provides the trend line and detects regressions.
B. Seeded rotating suite
Generate a fresh sample on each evaluation from a versioned generator. Record:
generator version
random seed
sampling weights
population definition
Report the mean and uncertainty across multiple seeds, not one run.
C. Sequestered challenge suite
Maintain newly discovered failures outside routine developer access. Use them for milestone or release evaluation. After they become known and fixed, promote them to the permanent regression suite and replace them with new hidden cases.
Dynamic benchmarks such as Dynabench address benchmark saturation by continually collecting examples against current systems, but they sacrifice some stability. (ACL Anthology)
NIST now distinguishes accuracy on a fixed benchmark from generalized accuracy over the population of similar possible test items. Those are different estimands and should not be presented as one continuous trend. (NIST)
Cost
Medium. The challenge set requires access control, adjudication and disciplined versioning.
Known failure
	•	Frozen sets become tuning targets.
	•	Generated sets inherit the generator’s blind spots.
	•	Hidden sets can be too small or leak.
	•	Changing generation weights creates an apparent trend unrelated to the system.
Never splice results from changed populations into one line without marking the population change.

8. Evaluating unresolved ambiguity
Accepted practice
This should be a separate evaluation axis, not folded into ordinary accuracy or refusal.
Label each input with one of:
UNAMBIGUOUS_AND_RESOLVABLE
AMBIGUOUS_MULTIPLE_AUTHORIZED_REFERENTS
UNRESOLVABLE_NO_REFERENT
REFERENT_EXISTS_BUT_IS_UNAUTHORIZED
Then classify system behavior:
ANSWERED_CORRECTLY
ASKED_CLARIFICATION
DECLARED_UNRESOLVED
ANSWERED_WRONG_REFERENT
LEAKING_CLARIFICATION
UNNECESSARY_CLARIFICATION
Primary metrics:
	•	False-resolution rate: answered when no unique authorized interpretation existed.
	•	Missed-resolution rate: failed to answer when one authorized interpretation was clear.
	•	Correct-referent rate
	•	Clarification success: one clarification produced enough information to continue correctly.
	•	Leak-free clarification rate
	•	Answer coverage versus wrong-resolution risk
The last measure adapts selective prediction’s risk-coverage framework: the system should answer more requests without increasing confident wrong-reference answers. (ML Anthology)
Dialogue research treats clarification exchanges as a distinct capability, but there is no settled standard metric for governance-sensitive clarification. Research still reports weak alignment between human and model clarification behavior, and earlier work explicitly identifies automatic evaluation of clarification quality as unresolved. (ACL Anthology)
Extrapolation: the four-way governance label and “leak-free clarification rate” are adaptations for your system, not established industry standards.
Cost
High. Referential ambiguity often requires multiple human judges and full dialogue context.
Known failure
Ambiguity is partly audience-dependent. What is obvious to household members may be unresolved to an outside annotator. Store both the intended referent and whether the utterance provides enough evidence for a reasonable listener to recover it.

9. Protected-content side channels
Accepted practice
Yes. Differences in latency, model invocation, clarification form, response length or error behavior can disclose whether protected content exists. Timing is a standard side-channel category because secrets can influence observable nonfunctional behavior. (NIST Computer Security Resource Center)
Use paired noninterference tests.
Create two worlds that are identical from the requester’s authorized perspective:
World A: protected Maya record exists
World B: protected Maya record does not exist
Submit the same request as Sam or a guest. Compare:
	•	Response category
	•	Clarification choices
	•	Whether a model was invoked
	•	Error code
	•	Response length
	•	Network-call pattern
	•	Latency distribution
	•	Number of internal policy steps exposed externally
Vary only the hidden record. Any reproducible observable difference is a candidate leak.
For timing, run repeated, randomly interleaved trials and use a predeclared statistical test with controlled false-positive probability. Current side-channel research emphasizes that noisy timing tests require explicit type-I-error control rather than visually comparing averages. (USENIX)
Cost
Medium to high. Functional side channels are inexpensive to test; latency requires repeated runs and controlled infrastructure.
Known failure
Finite testing can demonstrate a leak but cannot prove noninterference over all possible states. Infrastructure noise can hide real timing differences or create false alarms. Treat this as falsification testing, not proof.

The three things to build this quarter
1. An independent executable policy oracle
Create a compact policy model using decision tables and typed inputs. Generate expected allow, deny, conditional and unspecified outcomes from it. Keep it in a separate module with independent review.
Why first: without an independent oracle, every metric and generated case merely tests whether the implementation agrees with itself.

2. An isolated, trace-based two-sided harness
For every test:
	1	Start from a known state snapshot.
	2	Run the utterance.
	3	Compare the decision against the policy oracle.
	4	Assert the semantic execution trace.
	5	Verify the exact prompt authorization manifest.
	6	Score false release, false denial and useful-answer behavior separately.
	7	Discard the state.
Add stateful sequence testing as a second mode using an explicit reference state machine.
Why second: it tests the actual security claim—records were excluded before model invocation—not merely the wording displayed to the user.

3. A hybrid natural-language evaluation population
Maintain:
	•	A frozen anchor suite
	•	A regenerated seeded suite
	•	A sequestered human/model challenge set
Organize all three using a behavioral matrix covering omitted topic words, ambiguous references, slang, bundled requests, speaker changes, pressure, statements and ordinary non-household traffic. Include ambiguity as a separate labelled outcome.
Why third: the current generator’s defect is structural. More templates based on the same slots will produce more easy examples, not more coverage.
The resulting architecture is:
Written policy
      ↓
Independent executable oracle
      ↓
Natural and generated utterance populations
      ↓
Fresh-state system execution
      ↓
Semantic execution trace + prompt manifest
      ↓
Separate security, utility, ambiguity and side-channel metrics
That is a credible evaluation system. A larger template bank plus a stricter refusal gate is not.
