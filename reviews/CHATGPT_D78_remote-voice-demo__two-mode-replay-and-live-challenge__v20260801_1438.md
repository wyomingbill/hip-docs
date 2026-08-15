# CHATGPT_D78_remote-voice-demo — two-mode replay, live challenge, evidence bundle

Reviewer: ChatGPT (external research pass, routed by Bill)
Dispatch: banked D-91 (the pass predates and informed D-80's filing of REQ_DEMO_WEB_REPLAY)
Subject: how to show the governed voice demo to a remote viewer — what a replay actually
proves, the operational friction of sending browser audio alongside a live call, and what
format is defensible at this stage.
Method: external research. NOT a code read of this repository — where it describes HIP it
is repeating Bill's framing, not verified observation. The code-grounded companion is the
Fable four-tree recon banked alongside it.
Version: v20260801_1438 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED. Findings and recommendations are the reviewer's and have not been
confirmed by any dispatch. Proposes no status and no REQ.
Date: 2026-08-01

**WHY THIS IS BANKED NOW, LATE.** `REQ_DEMO_WEB_REPLAY` names two sources in its header and
states both were "banked in docs/reviews/". At filing (D-80) only the Fable recon was — the
claim was **half false**, and D-80 flagged it as needing its own correction pass rather than
quietly softening the wording. This is that pass: banking the actual artifact makes the
header's claim TRUE, which is the honest repair. The alternative — editing the header to
claim less — would have hidden a real provenance gap instead of closing it.

Headline as filed: the two-mode plan is "directionally right," but it **overestimates what a
replay proves** and **underestimates the operational friction** of sending browser audio
alongside a live call. Recommends four things in order — a short deterministic captured run,
a synchronized replay surface rendered from the actual exported event record, a narrow live
challenge where the viewer supplies the question verbatim, and a downloadable evidence
bundle — and explicitly advises **against** building a general-purpose remote voice sandbox
at this stage.

---

Bottom line
Your two-mode plan is directionally right, but you are overestimating what a replay proves and underestimating the operational friction created by sending browser audio alongside a live call.
The strongest early-stage format is:
	1	A short, deterministic captured run that tells the story cleanly.
	2	A synchronized replay surface whose dashboard is rendered from the actual exported event record.
	3	A narrow live challenge in which the viewer supplies the question, you submit it verbatim, and the resulting record and audio appear in their browser.
	4	A downloadable evidence bundle showing exactly what was captured.
Do not build a general-purpose remote voice sandbox yet. Your core claim is governed execution and auditable decisions, not that you have solved arbitrary remote conversational UX.

1. What voice companies actually do remotely
There is no single accepted convention. The observed market pattern is a stack of increasingly credible demonstration modes.
Public marketing layer: polished recordings
Recorded product videos, narrated walkthroughs, webinars, embedded audio examples, and scripted use-case demonstrations are normal. ElevenLabs uses both “watch demo” content and browser-integrated agent experiences; PolyAI uses recorded webinars and guided sales demos; Hume has published interactive demonstrations alongside product videos and technical quickstarts. (ElevenLabs)
These assets answer:
	•	What does it sound like?
	•	What problem is being solved?
	•	What is the intended interaction?
	•	Is the product visually coherent?
They do not establish robustness.
Self-serve experience layer: browser or phone interaction
Voice infrastructure companies commonly offer a live browser agent, a phone number, or a simple text-to-speech playground:
	•	Vapi has a live browser voice-agent demo.
	•	Retell and Cognigy promote live call demonstrations.
	•	Cartesia offers a type-and-listen voice generator.
	•	ElevenLabs distributes an embeddable conversational-agent web widget.
	•	Hume provides browser SDKs and interactive voice experiences. (Vapi)
This is the most relevant convention for you: put the audio endpoint in the listener’s browser or phone, rather than relying exclusively on conference-call audio.
Technical-evaluation layer: sandbox, logs, or pilot
For serious enterprise evaluation, the credible endpoint is usually not a better demo. It is a controlled test environment, pilot, configurable agent, or access to call records and monitoring. Retell, ElevenLabs, Vapi, and similar platforms frame their products around building, testing, deploying, and monitoring rather than treating a canned demo as sufficient proof. (Retell AI)
What investors and evaluators expect
The expectations differ:
Audience
What normally satisfies them
Initial investor meeting
A short, clear recording or tightly controlled live sequence
Product investor or operator
Some genuine interaction, preferably using a prompt they influenced
Technical evaluator
Live challenge, logs, architecture explanation, failure behavior
Enterprise buyer
Guided demo followed by controlled pilot or test environment
There is no evidence that investors universally demand a live demo. Practitioner advice is contradictory: some explicitly recommend recording fundraising demos to eliminate operational risk, while others prefer live demonstrations but insist on having a recording as backup. That contradiction is the honest signal: there is no established consensus. (Alexander Jarvis)
Your audience will not ask, “Was every frame generated live?” They will ask, explicitly or implicitly:
	•	Did this system actually produce this result?
	•	Did you cherry-pick it?
	•	Can it survive a question you did not script?
	•	Is the displayed governance record real or decorative?
	•	Does it fail safely?

2. Is replay perceived as fake?
Replay is not inherently perceived as fake. Undisclosed replay is.
“Captured from a real run” is a credible description, provided the surface clearly distinguishes:
	•	Capture time
	•	Replay time
	•	System version
	•	Exact input
	•	Actual output
	•	Recorded execution events
	•	What is and is not being claimed
A recorded run can credibly prove:
	•	The depicted system produced these artifacts at least once.
	•	The policy engine generated the displayed decision.
	•	The routing sequence and TTS output are internally consistent.
	•	The viewer can inspect the complete resulting record.
It cannot prove:
	•	The behavior is robust across phrasings.
	•	The run was not cherry-picked.
	•	The latency shown is representative.
	•	The displayed trace came from the same execution unless the system establishes that linkage.
	•	There were no hidden prompts, overrides, or manual interventions.
	•	The software currently behaves the same way.
The terminology problem
Do not call the replay itself “falsifiable.” The viewer can inspect and challenge the record, but cannot falsify the entire product claim from a single capture.
Better language:
Tamper-evident captured execution
or:
A captured run with independently verifiable artifacts
That is narrower and defensible.
What makes a replay credible
Use a visible status badge:
CAPTURED EXECUTION — not currently live Run: demo-2026-08-01-0042 Build: 8f23d9a Captured: 2026-08-01T12:41:08Z
Then expose:
	•	Exact input
	•	Identity and household role used
	•	Access-control result
	•	Policy or rule identifier
	•	Model-routing decision
	•	Response text
	•	TTS file
	•	Event timestamps
	•	Full downloadable record
	•	Verification status
A technical evaluator will generally accept this as evidence of a real captured execution. They will still treat it as one sample.
The best credibility move
Include at least one run that is not cosmetically perfect:
	•	A denial that sounds slightly awkward
	•	A slow turn
	•	A corrected transcription
	•	A routing fallback
	•	A pending or unresolved decision
A gallery containing only flawless runs looks more manufactured than a clearly labeled replay.

3. Making the recorded demo auditable
Security and software-supply-chain systems offer useful patterns, but there is no established standard specifically for “auditable AI demos.”
The most applicable patterns are:
	1	Structured execution attestations
	2	Cryptographic artifact hashes
	3	Signed manifests
	4	Append-only transparency records
	5	Published test procedures
	6	Reproduction bundles
The in-toto attestation framework is designed for verifiable claims about how an artifact was produced. Sigstore and Cosign provide signing, verification, and transparency-log mechanisms. MITRE’s adversary-emulation work publishes methodology and emulation plans so others can understand and reproduce evaluations. (GitHub)
Critical limitation
A signature proves integrity and issuer identity. It does not prove that the signed claim is true.
The new IETF SCITT architecture states this explicitly: issuers can register false statements; registration establishes who produced the statement and that it has not been silently altered, not that its contents are accurate. (IETF Datatracker)
Therefore, do not say:
“The signed record proves the AI really did this.”
Say:
“The signature proves this is the record we captured and that its contents have not been modified since capture.”
Recommended evidence-bundle structure
demo-run-0042/
├── manifest.json
├── manifest.sig
├── verify.sh
├── input/
│   ├── prompt.txt
│   └── prompt.sha256
├── trace/
│   ├── events.jsonl
│   ├── spans.json
│   └── trace.sha256
├── output/
│   ├── response.txt
│   ├── response.mp3
│   └── response.sha256
├── policy/
│   ├── policy-bundle.json
│   └── policy-bundle.sha256
└── environment/
    ├── build.json
    └── model-config.json
The manifest should include:
Field
Purpose
run_id
Unique execution identifier
captured_at_utc
Capture timestamp
git_commit
Exact code revision
container_digest
Executable environment identifier
policy_digest
Governance configuration used
model_identifiers
STT, LLM, routing and TTS versions
input_digest
Hash of exact input
event_log_digest
Hash of execution trace
audio_digest
Hash of delivered TTS
previous_event_hash
Optional event-level hash chain
signing_identity
Who or what signed the bundle
Use a canonical serialization before signing. RFC 8785 defines a JSON canonicalization scheme; otherwise semantically identical JSON can produce different hashes because of key ordering or formatting. (RFC Editor)
Trace design
Use one causal trace ID across:
input accepted
→ identity resolved
→ access policy evaluated
→ route selected
→ model invoked
→ response filtered
→ audit record committed
→ TTS requested
→ first audio generated
→ playback artifact finalized
W3C Trace Context and OpenTelemetry provide established structures for propagating trace identity and representing spans and timestamped events. (W3C)
Your dashboard must not be a second narrative
The dashboard should be rendered from the same event records included in the evidence bundle.
Do not have:
Execution system → audit log
Demo frontend    → separate animation state
Use:
Execution system → event stream → audit bundle
                               ↘ demo frontend
Otherwise, the dashboard is theater even if the backend is legitimate.
Minimum useful cryptography
For an investor demo, a complete transparency-service architecture is overkill.
Use:
	•	SHA-256 hashes
	•	Canonical JSON
	•	One signed manifest
	•	A tiny browser or command-line verifier
	•	A public verification key
	•	Optional Sigstore/Cosign signing
Do not build a blockchain.

4. Mode 2: what will break first
At one viewer and one dev machine, raw WebSocket scale is not your primary problem.
The likely failure sequence is:
1. Browser audio activation
Browsers commonly block audio that begins without a user gesture. Web Audio contexts may start suspended, and programmatic playback can be rejected unless the viewer has clicked something first. (MDN Web Docs)
Your landing page needs an explicit:
Enable demo audio
button that plays a short test sound.
Do this before introductions, not when the first important response is ready.
2. Echo and competing audio channels
The viewer is simultaneously:
	•	Listening to you on the call
	•	Listening to the assistant in the browser
	•	Potentially sending the browser sound back through their call microphone
Headphones need to be part of the preflight. Google’s own Meet troubleshooting guidance recommends headphones and lower speaker volume to prevent echo. (Google Help)
You must stop narrating while the TTS plays. There is no reliable way for your web player to duck Zoom, Meet, or Teams audio.
3. Tail latency, not average latency
Voice-agent latency accumulates across:
	•	End-of-turn detection
	•	STT finalization
	•	Policy processing
	•	LLM time to first token
	•	Tool or retrieval calls
	•	TTS time to first audio
	•	Network and playback buffering
LiveKit describes accumulated pipeline latency and treats sub-one-second responses as the target for natural interaction. A 2026 enterprise voice-agent tutorial achieved approximately 947 ms median time-to-first-audio with a fully streamed cascade, demonstrating that even a carefully constructed pipeline has little margin. (LiveKit Docs)
Deepgram recommends measuring every latency component separately, rather than relying only on total duration. Its published examples also show how non-streaming TTS can add seconds compared with streaming output. (Deepgram Docs)
The live demo will fail on P95 latency, not on your carefully measured median.
Record and display:
Input accepted                 0 ms
Policy decision               31 ms
Route selected                42 ms
First LLM token              386 ms
First TTS audio              712 ms
Playback started             781 ms
Do not display only a single “total latency” number.
4. Audio and dashboard desynchronization
Your UI may say “responding” while audio is still buffering, or advance to the next turn while the previous audio is playing.
Use explicit states:
RECEIVED
POLICY_DECIDED
GENERATING_TEXT
GENERATING_AUDIO
PLAYABLE
PLAYING
COMPLETE
FAILED
Drive them from backend events, not client-side timers.
5. The dev machine
A single dev machine creates obvious failure modes:
	•	Sleep
	•	Thermal throttling
	•	GPU-memory contention
	•	Local process crash
	•	ISP upload instability
	•	Tunnel expiration
	•	Software update
	•	Authentication token expiration
Have the dev machine make an outbound persistent connection to a cloud relay. Do not depend on the viewer reaching an improvised inbound port or a freshly created local tunnel.
The relay should assign:
	•	run_id
	•	sequence numbers
	•	idempotency keys
	•	authoritative timestamps
That protects you from duplicated turns after reconnects.
6. Transport
For actual low-latency voice media, WebRTC is generally better suited than treating audio as generic WebSocket messages. ElevenLabs moved its browser-agent transport toward WebRTC for native browser integration, echo cancellation, and noise handling; LiveKit similarly uses WebRTC between the frontend and the voice agent. (ElevenLabs)
Plain browser WebSockets also lack automatic backpressure. If messages arrive faster than the client processes them, buffering can consume memory or make the page unresponsive. (MDN Web Docs)
However, for your first version, you do not necessarily need streaming media:
	1	Execute the turn live.
	2	Generate the complete TTS file.
	3	Upload it to the relay or object storage.
	4	Notify the browser that the audio is playable.
	5	Play it.
That will not demonstrate natural turn-taking latency, but it will demonstrate genuine execution, governance, routing, and TTS output with much less fragility.
Attack on your assumption about conference audio
“Video-call audio is unusable” is too absolute. Zoom supports shared computer audio and stereo/high-fidelity modes, and Teams has a high-fidelity mode. But configuration, bandwidth adaptation, echo processing, and participant equipment make the result inconsistent. (Zoom)
So your conclusion is right—browser playback is more controlled—but your premise should be:
Conference audio is too variable to be the authoritative voice-quality path.

5. Minimum viable version, ranked
Recommended order
Rank
Option
Effort
Persuasive value
Main limitation
1
Synchronized replay page
Medium-low
Very high
Does not prove robustness
2
Static evidence page with audio controls
Low
High
Less theatrical and less synchronized
3
Presenter-driven live execution with completed audio file
Medium
High
Does not show conversational streaming
4
Locally captured video plus downloadable trace
Very low
Medium-high
Viewer cannot inspect while it plays
5
Receive-only streamed live audio
High
High when working
Transport and synchronization risk
6
Full viewer-operated voice sandbox
Very high
Potentially highest
Exposes phrasing, microphone and latency failures
Option 1: synchronized replay page
This is your best value.
The page contains:
	•	Viewer-selectable scenarios
	•	Visible “captured run” label
	•	Transcript
	•	Per-turn audio
	•	Governance decision
	•	Routing decision
	•	Timeline
	•	Downloadable record
	•	Verification button
The viewer clicks Next turn, or you enable paced playback. Do not have both you and the page narrating simultaneously.
Option 2: static HTML evidence page
This is the genuine minimum.
<h2>Turn 3 — Access denied</h2>
<p><strong>Question:</strong> Has Michael started drinking again?</p>
<p><strong>Result:</strong> Denied</p>
<p><strong>Policy:</strong> MEMBER_PRIVATE / health-sensitive</p>

<audio controls preload="auto">
  <source src="turn-003.mp3" type="audio/mpeg">
</audio>

<a href="turn-003.json">View record</a>
Add:
	•	Run metadata
	•	Hash values
	•	Download bundle
	•	Three scenarios
	•	A visible system-version badge
This alone solves the browser-audio problem.
Option 3: presenter-driven live, without streamed audio
This is probably sufficient for your live mode.
Workflow:
	1	Viewer puts the proposed question into the video-call chat.
	2	You copy it verbatim.
	3	The browser displays the exact input before execution.
	4	You press Execute.
	5	Policy and routing events appear live.
	6	The generated audio file appears and plays.
	7	The complete record becomes downloadable.
This establishes viewer influence without exposing microphone or phrasing variability.
Option 4: locally captured video
Use a local screen recorder, not the conference recording. Capture:
	•	Screen at native resolution
	•	System audio directly
	•	Optional microphone narration on a separate track
Embed the resulting video in a page that also provides the trace bundle.
A video by itself underserves your falsifiability pitch. A video plus artifacts is credible.
Do not start with full WebRTC
Full WebRTC is justified when you need to demonstrate:
	•	Interruption
	•	Barge-in
	•	Semantic endpointing
	•	Duplex behavior
	•	Actual conversational latency
	•	Microphone handling
Your current persuasive core is access control and observable governance. WebRTC is not necessary to prove that.

6. What you are not asking
A. Is voice quality actually the central claim?
Your product’s differentiator is not TTS. High-quality voices are increasingly available from multiple vendors through generators, APIs, widgets, and browser agents. (Cartesia)
Do not let the voice demo turn into an ElevenLabs comparison.
The voice should establish:
	•	This is a household interaction.
	•	The denial sounds socially appropriate.
	•	The system remains useful while enforcing boundaries.
	•	The record corresponds to what was heard.
B. Are you proving governance or merely displaying it?
A colorful dashboard that says:
ACCESS DENIED
Reason: privacy
is not convincing.
Show:
Requester: Susan
Subject: Michael
Attribute: substance-use status
Requested operation: read
Resource scope: MEMBER_PRIVATE
Applicable policy version: household-policy-17
Rule: deny_cross_member_sensitive_health
Result: DENY
Appeal/recovery path: ask Michael directly
The evaluator needs to see that the denial followed from a structured rule, not an LLM-generated explanation.
C. Your “viewer-typed input is out of scope” rationale is dangerous
“Known phrasing fragility” is not just a demo limitation. It is a product limitation.
A technical evaluator will infer:
The governance layer may work only on prepared utterances.
Do not hide this. Bound the claim:
“This demo evaluates governance execution after intent has been resolved. It is not an evaluation of arbitrary-language classification robustness.”
Then demonstrate the classifier separately with a test matrix.
A better compromise is:
	•	Viewer chooses the household role.
	•	Viewer chooses a challenge category.
	•	Viewer supplies one question.
	•	You submit it exactly.
	•	If intent classification is ambiguous, the system must show UNRESOLVED or ask for clarification rather than silently forcing a prepared interpretation.
D. Cherry-picking
One live run does not eliminate cherry-picking. It only creates a fresh anecdote.
Provide a small run set:
12 allowed requests
12 denied requests
6 ambiguous requests
4 policy conflicts
4 system failures
Show aggregate pass/fail counts and let the viewer open individual traces.
E. Privacy of the demonstration itself
Do not use actual household records or actual relatives’ voices.
Use:
	•	Synthetic household members
	•	Synthetic facts
	•	Clearly disclosed synthetic or licensed voices
	•	No production credentials
	•	No actual personal data in downloadable bundles
F. Gating friction
An account-registration gate will hurt you.
Prefer:
	•	Expiring unlisted link
	•	Simple access code
	•	No password setup
	•	No email verification during the call
	•	Browser check completed before the meeting
The demo link should remain forwardable to another decision-maker only when you intentionally permit it.
G. Mobile and corporate-browser behavior
Technical viewers may open the page:
	•	Inside an email client’s embedded browser
	•	On Safari
	•	Behind a corporate proxy
	•	With autoplay disabled
	•	With WebRTC UDP blocked
	•	With no microphone permissions
	•	On a Bluetooth headset in low-quality call mode
Build a preflight page that checks:
Audio playback             PASS
WebSocket/control channel  PASS
Live backend               PASS
Headphones recommended     ACKNOWLEDGED
Browser supported          PASS
Demo version               0.4.2
H. What happens when live mode fails?
Do not awkwardly switch browser tabs.
The same surface should have:
Live connection unavailable — continue with captured execution
The fallback run should use the same scenario and the same visual structure.

Recommended demo design
Opening: 60–90 second captured sequence
Show three consecutive turns:
	1	Allowed: a household-shared question
	2	Denied: a private question about another member
	3	Qualified: a question that requires clarification or limited disclosure
Let the voice play cleanly. Keep narration minimal.
Inspection: viewer checks one turn
Pause and open:
	•	Identity
	•	Resource
	•	Rule
	•	Decision
	•	Route
	•	Timing
	•	Audio hash
	•	Full event record
This is where your product becomes differentiated.
Live challenge
Ask the viewer to put a question in the call chat.
Then:
	•	Copy it verbatim
	•	Show the received string
	•	Execute it
	•	Display policy events live
	•	Play the generated audio in their browser
	•	Export the record
State clearly:
“The execution is live. Audio playback begins after the current TTS file is complete; this mode is demonstrating governed execution, not full-duplex conversational latency.”
That sentence prevents an evaluator from attributing capabilities you are not yet demonstrating.
Leave-behind
Give them:
	•	Unlisted replay URL
	•	Three to five captured scenarios
	•	Downloadable signed bundles
	•	A one-command verifier
	•	A short architecture diagram
	•	Known limitations
	•	Test-matrix results

Final judgment on your current plan
Keep
	•	Gated or controlled web surface
	•	Captured-run replay
	•	Viewer-visible transcript and decision panes
	•	Per-turn TTS files
	•	Presenter-driven live challenge
	•	Viewer suggestions rather than unrestricted microphone access
Change
	•	Replace account gating with an expiring link or code.
	•	Label replay aggressively and precisely.
	•	Render the UI from the actual trace.
	•	Add downloadable evidence.
	•	Submit viewer questions verbatim from call chat.
	•	Separate governance evaluation from language-understanding evaluation.
	•	Avoid streamed live audio initially.
	•	Add visible latency components and error states.
	•	Require an audio/headphone preflight.
Do not claim
	•	That a signed record proves truth.
	•	That one captured run proves robustness.
	•	That a live run cannot be cherry-picked.
	•	That the demonstration is fully falsifiable.
	•	That presenter-entered questions are equivalent to viewer-controlled interaction.
The replay is not your credibility problem. Unbounded claims are. A precisely labeled captured execution, backed by real artifacts and followed by one narrow live challenge, is more credible than a fragile “fully live” voice performance.
