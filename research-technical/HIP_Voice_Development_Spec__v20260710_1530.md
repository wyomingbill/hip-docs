---
doc: HIP Voice Interaction Layer Development Spec
status: IN_PROGRESS
version: v20260710_1530
purpose: Staged development specification for the voice interaction layer.
         Grounded in codebase analysis and the voice architecture research corpus (P1-P4).
         No code is written or edited in this document. This is a plan for human approval.
constraints: no em or en dashes. Every claim maps to a real component or a stated R&D intent.
---

# HIP Voice Interaction Layer: Development Specification

Status: IN_PROGRESS
Reconciled-Against: 2026-07-10 (direct codebase read, commit on Mini branch main)

---

## 0. Codebase Baseline: What the System Does Today

This section grounds every subsequent recommendation in the actual code. Claims without a
file:line citation are not made.

### 0.1 Current interaction surface: turn detection

The live voice pipeline runs in `server/voice_https_orch.py` (port 7860), importing its
pipeline from `server/voice_orch.py`. Turn detection is a two-stage fixed-timer cascade:

**Stage 1: Silero VAD (activity detection).**
`server/voice.py:32` imports `pipecat.audio.vad.silero.SileroVADAnalyzer`. The class is
wrapped at `server/voice.py:95` in `EnergyAwareSileroVAD`, which adds an RMS-energy
fallback: if Silero stays below its confidence threshold but RMS exceeds `rms_floor`, the
frame is still classified as speech. The combined signal drives `VADUserStartedSpeakingFrame`
and `VADUserStoppedSpeakingFrame` emissions.

VAD parameters are read from `config.yaml:44-51` at module load (`server/voice.py:76`):

```
vad:
  confidence: 0.3          # min Silero confidence
  start_secs: 0.2          # speech must persist before turn starts
  stop_secs: 1.5           # trailing silence before end-of-speech is declared
  min_volume: 0.0          # RMS gate (disabled)
  user_speech_timeout: 0.6 # extra wait after VAD stop before firing the LLM
  rms_floor: 0.02          # RMS floor for the energy fallback
```

The `stop_secs: 1.5` parameter is the primary silence threshold. A turn is not ended until
Silero detects 1.5 consecutive seconds of sub-confidence audio. The downstream settle window
(`user_speech_timeout: 0.6`) adds another 0.6 s after the VAD stop event fires before the
merged utterance is handed to routing. Total worst-case latency from last word spoken to
routing: 1.5 + 0.6 = 2.1 seconds.

**Stage 2: SpeechTimeoutUserTurnStopStrategy.**
`server/voice.py:64` and `server/voice_orch.py:85` both import
`pipecat.turns.user_stop.SpeechTimeoutUserTurnStopStrategy`. The turn-stop strategy fires on
`VAD["user_speech_timeout"]` (0.6 s) with no semantic or prosodic input. There is no
confidence signal, no intent-based early cutoff, and no speaker-identity signal involved at
this stage. The turn boundary is purely temporal.

**Placement on the P4 five-step migration ladder:**
The current implementation is unambiguously at **Step 1: VAD plus fixed timer**. Silero
provides voice activity; a fixed `stop_secs` silence threshold ends the segment; a fixed
`user_speech_timeout` adds a settle window. No semantic signal is consulted, no prosodic
prediction is made. This is confirmed by the explicit comment at `server/voice.py:369-374`:
"Drive end-of-speech from Silero VAD (stop_secs) instead of the Smart Turn model, so the
config.yaml VAD knobs actually control turn-taking." The pipeline includes `UserTurnStrategies`
(`server/voice.py:373`) but the turn-stop strategy bound there is the fixed-timeout variant,
not Smart Turn.

**Multi-fragment buffering (TD-046).**
`server/voice_orch.py:941-960` implements an utterance merge layer: because a mid-sentence
pause can emit multiple `TranscriptionFrame` objects (each VAD segment yields its own),
`OrchestratorGate._flush_utterance` (`server/voice_orch.py:1138`) buffers fragments and
routes only once, after `VAD["user_speech_timeout"]` of no further segment. This is a
workaround for the Step 1 architecture's inability to predict end-of-turn from meaning; it
adds the 0.6 s settle window on top of the 1.5 s VAD silence.

### 0.2 Current routing cascade: the tiered hierarchy

`harness/router.py` is the router. The public surface is `route()` (line 680) and the
`Router` class (line 797). The cascade evaluates axes in this order:

1. **Noise filter** (line 706): `_is_noise()` from `harness/intent_classifier.py`. Pure
   heuristic, zero latency. Drops ambient-noise or sub-threshold segments before any model
   call.

2. **Intent classification** (line 710): `intent_classifier.classify()`. Embedding similarity
   against labelled exemplars, no LLM call. Returns one of: temporal, action, personal,
   knowledge, or low-confidence.

3. **Temporal intent early return** (line 725): if intent is "temporal," the turn escalates
   to off-net (TIER_ESCALATE, AXIS_INTENT) unless escalation is disabled in config or
   sensitivity blocks the off-net boundary. This is the de facto freshness axis; no separate
   `_classify_freshness()` function is wired into `route()` despite the AXIS_FRESHNESS
   constant being defined (line 76). The FRESHNESS label appears in the module docstring as
   "implemented" but in the `route()` body it is the temporal intent classifier that fires for
   time-sensitive queries, not a dedicated freshness axis.

4. **Action intent early return** (line 747): if intent is "action," the turn goes to
   TIER_LOCAL (edge) regardless of escalation status.

5. **Complexity classification** (line 757): `classify_complexity()` from lines 522-564.
   Two-stage: (a) feature classifier (`harness/complexity_features.py`) using Bloom's taxonomy
   levels (bloom 1-2 -> edge, 3-4 -> mid, 5-6 -> core); (b) exemplar embedding router as
   secondary; (c) rules fallback (token count, complex verbs, multi-part markers). This
   determines the on-net tier (edge/mid/core). Sensitivity cannot lower this tier; it can
   only block off-net escalation.

6. **Sensitivity gate** (lines 697-707): `_classify_sensitivity()`. Two paths: (a) fact-level
   sensitivity tag from the retrieved facts; (b) query-level PII or first-person personal-topic
   detection. When either fires, off-net escalation (freshness or capability axes) is blocked
   and the turn stays on-net at whatever tier complexity selected.

7. **Capability axis** (lines 767-783): config-gated, off by default. Heuristic detection of
   code execution, heavy math, or tool-use queries. If fired and not blocked by sensitivity,
   routes to TIER_ESCALATE.

8. **Default**: on-net at the complexity tier (edge/mid/core).

**Tier dispatch in voice_orch.py.** The `OrchestratorGate._decide()` call (not shown in the
read but referenced at `server/voice_orch.py:1503`) returns a dict including `decision`
(the `RouteDecision`). The voice loop then dispatches:
- TIER_EDGE / TIER_MID locally to the `LOCAL_MODEL` (`qwen2.5:7b`, see `config.yaml`).
- TIER_MID and TIER_CORE may route to Groq (`llama-3.1-8b-instant` or
  `llama-3.3-70b-versatile`) when `GROQ_API_KEY` is present and the sensitivity gate
  allows off-net. Models are defined at `server/voice_orch.py:142-145`.
- TIER_ESCALATE routes to the `TieredEscalationBackend` (SerpAPI web search) or the
  `LoggingEscalationStub` for capability escalations.

**Mapping to P3 interaction-plus-reasoning split.** The routing cascade already embodies this
split structurally, as the roadmap document notes (section 2, "Alpha 2"). Today:
- The interaction-model role is filled by `qwen2.5:7b` at the edge tier, handling the
  majority of conversational turns with locally injected facts. This is the fast on-device
  model.
- The background-reasoning role is filled by the Groq mid/core tiers
  (`llama-3.1-8b-instant`, `llama-3.3-70b-versatile`) and, for web knowledge, by the SerpAPI
  escalation backend. These handle turns that exceed the local model's knowledge or capability.
- The delegation boundary is the `route()` decision: TIER_EDGE goes local, TIER_MID/CORE
  go to Groq (when config and sensitivity allow), TIER_ESCALATE goes to the web backend.

The split is real and operational. What does not yet exist is a formal gap-filling protocol:
when the background tier is invoked mid-conversation, the local model does not fill the audio
gap with a natural deferral phrase correlated to the actual retrieval latency. The escalation
path speaks a placeholder and the Groq path blocks until the API returns. Neither has a
structured handshake with the interaction surface. This is the key formalization work for the
medium horizon.

### 0.3 The control plane: identity, consent, and permission enforcement

Speaker identity is handled by `harness/speaker_id.py`. The implementation uses Resemblyzer
GE2E embeddings (confirmed at `harness/speaker_id.py:85-86`). Per-turn verification runs
inside `OrchestratorGate._on_user_text()` at `server/voice_orch.py:1323-1390`: for each
transcription, every enrolled member's voiceprint is scored; the best medium-or-above match
sets `self._member_id`. If the match is below medium, the speaker is treated as guest: no
personal facts are injected and `sensitivity_override = "high"` blocks off-net escalation
(`server/voice_orch.py:1375`).

A pre-Whisper speaker gate (`SpeakerGateProcessor`, `server/voice_orch.py:641`) is
implemented but disabled by default (`config.yaml:57`: `speaker_gate: false`). When enabled,
it buffers each VAD segment and discards it before STT if no enrolled member matches at
medium-or-above confidence. This gate adds a second verification layer but is explicitly
disabled for demo and quiet-room use.

Permission enforcement is deterministic and outside the model. The injection contract
(`harness/injection_contract.py`, referenced at `server/voice_orch.py:127-130`) governs which
facts are injected per member. Cross-member access control (`INJ-7` in the harness spec) is
enforced by checking the `owner` field on retrieved facts before they reach the LLM context,
not by prompting the model to refuse. Per-member envelope encryption is in
`harness/encryption.py`. Session isolation (context flush on speaker change) is enforced at
`server/voice_orch.py:1252-1260`: on a detected speaker change, the LLM context is reset to
the base prompt and all prior messages are deleted before the new speaker's turn proceeds.

**Architectural assessment: deterministic or model-dependent?**
The hard constraints (member isolation, cross-member deny, sensitivity routing block) are
enforced in deterministic code. The injection contract is deterministic. The context flush on
speaker change is deterministic. No hard constraint is delegated to the LLM prompt alone.
One notable exception: the PERSONAL_FACTS_RULE in `_ORCH_BASE_PROMPT`
(`server/voice_orch.py:158-166`) instructs the model not to invent personal facts, which is
a soft constraint. The proof harness Layer 1 P6 (non-fabrication invariant) tests whether
this constraint holds; it is not guaranteed by deterministic code. This is the primary place
where a hard constraint currently rests on model behavior rather than enforcement logic, and
it is the right one to flag as an architectural gap against the roadmap's Layer 3 requirement.

### 0.4 Turn detection and speaker identity: the coupling gap

P4 identifies the critical coupling: "whose utterance is this" and "which member's permissions
apply" are the same question, and they must be answered by the same piece of infrastructure.

The current code handles this coupling, but in sequence rather than as a unified system.
Turn detection (Silero VAD, `stop_secs: 1.5`) fires first and determines the audio segment.
Then the segment goes to Whisper for transcription. Then `OrchestratorGate._on_user_text()`
runs speaker verification on the same audio. The two operations share the audio buffer
(`server/voice_orch.py:1109-1121`) but are independent computations. The VAD does not use
identity information; the speaker verifier does not influence the turn boundary.

The consequence of this sequencing is that in a multi-member household, a speaker change mid-
sentence is handled by retrospective re-attribution (detected after transcription), not by
proactive boundary placement. P4's recommendation to design turn detection and speaker
verification as a single fused operation is not yet implemented. The current coupling is
real but incidental: the audio buffer happens to be available to both operations because they
share the same frame loop, not because they were designed to share signal.

This gap matters when the near-term endpointing work is specced. Any replacement for the
fixed-timer VAD must preserve access to the raw audio segment, because Resemblyzer GE2E
verification operates on raw PCM (`harness/speaker_id.py`). A component that only exposes a
turn-end signal without the bracketed audio would break the verification path. This is the
coupling constraint the near-term spec must state explicitly.

### 0.5 Action-plane gap: full-duplex readiness

P2 specifies that full-duplex governance requires a second, structured output channel separate
from the audio stream. In the current architecture there is one analogue: the
`OutputTransportMessageFrame` used at `server/voice_orch.py:1163-1173` to relay the
authorized utterance text to the client. This is a structured message on a side channel,
not carried in the audio stream.

However, this channel is currently unidirectional and post-hoc: it carries text after routing
is complete, not a real-time action signal the control plane could intercept or modify during
speech. It is not an action plane in the P2 sense. The current architecture has no analogue
to a DuplexSLA action channel. The injection contract, consent enforcement, and sensitivity
gate all operate synchronously before generation begins, which is the correct design for the
cascade. For full-duplex, where generation and listening are concurrent, these pre-generation
checks cannot gate a speech stream that has already started; a separate channel carrying
structured action decisions in real time would be required. Nothing in the current codebase
begins this work.

---

## 1. Near-Term Horizon: Replace Fixed-Timer Endpointing with Fused Semantic-Prosodic Turn Prediction

**Layer-separation invariant: this change touches Layer 0 only. Layers 1 through 3 (the
routing cascade, the context graph, the control plane) must not change. Any endpointing
component that couples to routing logic, member identity, or fact retrieval is wrong by
construction and must be rejected.**

**Layer-separation flag: the replacement component must expose bracketed raw audio to the
speaker verification step. If a candidate component consumes audio internally and only emits
a turn-end event without the bracketed PCM, it breaks the speaker-identity coupling and
cannot be used without architectural surgery.**

### 1.1 The problem to solve

The current endpointing adds 1.5 s (VAD silence) plus 0.6 s (settle window) = 2.1 s of
fixed latency after the last word of every user turn. This is the primary source of
conversational unnaturalness in the current demo. A question that ends on a falling intonation
waits the same 2.1 s as a trailing "um" before a clause continues. The system cannot
distinguish end-of-turn from mid-turn pause by acoustic or semantic evidence.

The multi-fragment buffer (TD-046, `server/voice_orch.py:1138`) was added precisely because
the fixed timer fires incorrectly on mid-sentence pauses, producing multiple transcription
segments per utterance. The buffer is a compensating mechanism, not a fix.

### 1.2 Endpointing component selection

P4 evaluates four candidates against the criteria for HIP's edge deployment context: must run
on CPU (Jetson Orin Nano Super, which has an 8-core Cortex-A78AE; the NVIDIA Ampere GPU on
the Orin is available but power-constrained), must not require cloud inference, must integrate
with Pipecat's existing `UserTurnStrategies` seam (`server/voice.py:373-375`), and must
expose raw audio for the speaker-verification coupling.

**Recommended first integration: Pipecat Smart Turn v3.2.**

Rationale:
- BSD-2-Clause license; no usage restrictions.
- 8 MB quantized model, CPU inference, approximately 12 ms per frame on a modern CPU.
  Comfortably within the `encode + model + decode < chunk_duration` bound on the Orin.
- 23-language support, already tested against English in the Pipecat ecosystem.
- Designed to plug into the `SpeechTimeoutUserTurnStopStrategy` seam. Replacing the fixed
  `SpeechTimeoutUserTurnStopStrategy` with `SmartTurnUserTurnStopStrategy` (the class name
  in Pipecat v1.3) is the minimal-invasive swap. The VAD layer (Silero + energy fallback)
  stays unchanged; Smart Turn only changes the segment-end decision, not the segment-start.
- The bracketed audio (VAD start to Smart Turn end-decision) is still available in
  `OrchestratorGate._audio_buf` because the VAD frame events are unchanged. The speaker
  verification path is unaffected.

**Why not the others at this stage:**
- Silero VAD alone with a shorter `stop_secs` is already available (just change `config.yaml`)
  but solves nothing: it still has no semantic awareness and only trades false-positives
  (cutting off mid-sentence) for lower latency. It is a dial, not a step up the ladder.
- VAP (Voice Activity Projection): MIT-licensed, causal, 50 Hz frame-level. More powerful
  than Smart Turn but requires integration work beyond the `UserTurnStrategies` seam. Correct
  direction for Step 3 of the ladder. Not the lowest-effort near-term move.
- LiveKit v1-mini: fused semantic and acoustic, CPU inference. Requires evaluating LiveKit's
  audio pipeline integration against Pipecat's frame model. Appropriate if Smart Turn proves
  insufficient; not the first step.

### 1.3 Speaker-identity coupling: explicit requirement

The endpointing change must be specced jointly with the speaker-identity kernel. Per the gap
identified in section 0.4, the turn boundary and the identity attribution must remain
synchronized. The requirement is:

- The replacement stop strategy must fire `VADUserStoppedSpeakingFrame` (or its functional
  equivalent) in a way that makes the bracketed audio available before routing begins.
- The audio buffer in `OrchestratorGate` (`server/voice_orch.py:915-921`) must remain the
  canonical source for speaker verification; it is populated from `VADUserStartedSpeakingFrame`
  through `VADUserStoppedSpeakingFrame`. If Smart Turn fires a different stop event type, the
  buffer population logic at `server/voice_orch.py:1111-1116` must be updated to match.
- No endpointing component may be integrated without a verified pass of the speaker
  verification path on the same audio segment it would produce.

The pre-Whisper speaker gate (`SpeakerGateProcessor`, `server/voice_orch.py:641-735`) is
currently disabled (`config.yaml:57`). The gate also reads VAD frames for its audio buffer
(`server/voice_orch.py:676-727`). Any change to the VAD frame protocol must be verified
against the gate's logic before the gate is enabled in household deployment mode.

### 1.4 Ordered integration steps

1. **Baseline measurement.** Before any change, instrument the current turn latency for a
   standard demo script: time from last spoken word (determined from the Whisper transcript
   timestamp) to the first token of the LLM response. Record the distribution. This is the
   before-state the after-state must improve against.

2. **Dependency audit.** Confirm the Pipecat version pinned in `requirements-voice.txt`
   includes `SmartTurnUserTurnStopStrategy` (introduced in Pipecat v1.3). If not, document
   the upgrade path and the risk to other `server/voice.py` imports before proceeding.

3. **Config-plane integration.** The replacement should be config-gated: a new
   `voice.turn_stop` key in `config.yaml` with values `fixed_timeout` (current behavior) and
   `smart_turn`. The factory in `server/voice.py` reads the key and constructs the appropriate
   strategy. This preserves the ability to revert without a code change.

4. **Audio buffer verification.** Confirm that Smart Turn's stop event fires after (not
   before) the VAD stop, so `OrchestratorGate._audio_buf` (`server/voice_orch.py:1116`) is
   populated with the full segment audio before `_on_user_text` runs. If Smart Turn fires its
   stop signal before `VADUserStoppedSpeakingFrame`, the buffer will be incomplete.

5. **TD-046 buffer review.** After the swap, evaluate whether the multi-fragment utterance
   buffer at `server/voice_orch.py:1138` is still needed. If Smart Turn correctly delays the
   stop signal until semantic completion, mid-sentence pauses should no longer produce
   multiple transcription segments for a single utterance. A test with mid-sentence pauses
   is required to confirm this before the buffer is removed.

6. **Verification pass.** Run the proof harness against the endpointing change: at minimum,
   L2 (demo regression) and the speaker-identity scenarios. Any regression in L1 P6
   (non-fabrication) or speaker attribution tests is a blocking failure.

### 1.5 Definition of done

- The demo turn latency distribution (step 1 baseline) shifts measurably: the 95th-percentile
  post-last-word latency drops from approximately 2.1 s (current: 1.5 + 0.6) toward the
  Smart Turn model's semantic decision latency (target: under 0.8 s for typical conversational
  endings).
- No regression in L2 demo scenarios or L1 speaker-identity invariants.
- Speaker verification still operates on the correct audio segment: the post-change per-turn
  speaker log entries show the same member attribution as the pre-change run on identical audio.
- The change is config-reversible: setting `voice.turn_stop: fixed_timeout` in `config.yaml`
  restores the current behavior with no code change.
- Evaluated on Jetson Orin Nano Super (target edge hardware), not only the Mac development
  machine. Smart Turn's 12 ms CPU inference claim must be confirmed on the Orin's
  Cortex-A78AE cores under realistic load (Silero VAD + Whisper STT running concurrently).

---

## 2. Medium-Term Horizon: Formalize the Interaction-and-Reasoning Split

**Layer-separation invariant: this work formalizes the boundary that already exists between
Layers 0 and 1. It must not touch Layer 2 (the context graph schema) or Layer 3 (the
encryption or consent enforcement). It specifies interfaces and message contracts; it does not
change the routing logic inside `harness/router.py`.**

**Layer-separation flag: the delegation boundary is the `RouteDecision` dataclass
(`harness/router.py:96-126`). Any change to the medium-tier dispatch must flow through
`RouteDecision.tier` and `RouteDecision.axis`, not through side channels in the voice loop.
Adding fields to `RouteDecision` is acceptable; bypassing it is not.**

### 2.1 Current state of the split

Section 0.2 established that the routing cascade already embodies the interaction-plus-
reasoning split. The interaction tier (edge, `qwen2.5:7b` locally) handles conversational
turns. The reasoning tiers (Groq mid/core) handle queries above the local model's capability
or freshness horizon. The delegation boundary is the `route()` decision.

Three formalization gaps remain:

**Gap 1: Gap-filling behavior.**
When the routing decision is TIER_MID or TIER_CORE and the Groq call is made, the user hears
silence until the API returns. There is no gap-filling: no "let me check on that" phrase
spoken while retrieval is in flight, no timing correlation between the deferral and the actual
latency. The `_ctrl_prepend` mechanism (`server/voice_orch.py:1471, 1500`) exists for control-
flow announcements (RECONSIDER, FRONTIER_REQUEST) but is not used for routine mid/core routing.
A natural-sounding gap filler correlated to the actual routing decision is missing.

**Gap 2: Result integration point.**
When the Groq response returns, it is spoken directly. There is no structured hand-off: the
interaction surface (TTS, VAD, echo suppression) switches from silent to speaking. For a
full-duplex future, this hand-off needs to be a defined event the interaction layer can
prepare for. Today it is implicit in the control flow of the voice loop.

**Gap 3: Control plane intercept point.**
The sensitivity gate (`_classify_sensitivity`, `harness/router.py:197`) runs before routing
and can block off-net escalation. It does not run again at the result-integration point. If
a Groq response contains content the control plane would not have permitted from a local
response (because the sensitivity gate did not anticipate the response content), there is no
second intercept. This is not a current vulnerability (the sensitivity gate fires on the
query, not the response, which is the correct design for a pre-generation check), but for a
future where a background reasoning tier might return structured data with sensitivity tags,
a result-side intercept point needs to exist.

### 2.2 Open problems from P3 and their status in the current code

**Semantic commitment.** P3 defines the semantic commitment problem: the interaction model
commits to a conversational position ("I'll look that up") before knowing whether the
reasoning tier will confirm or contradict it. In the current implementation this is handled
by suppressing the gap filler entirely: the interaction tier says nothing while the Groq call
is in flight. This avoids semantic commitment at the cost of conversational naturalness. The
spec does not prescribe a specific gap-filling strategy; it requires that any strategy chosen
defines the rollback case if the reasoning tier returns a contradiction.

**Result staleness with context versioning.** P3 identifies that a reasoning result delayed
by retrieval latency may arrive after the conversation has moved on. The current code does not
handle this: a Groq call is awaited synchronously at `server/voice_orch.py` (the Groq call
blocks the voice loop turn). There is no mechanism for a reasoning result to arrive
asynchronously and be integrated with a stale context version. This problem does not manifest
today because turns block; it will emerge if asynchronous delegation is added. The spec
requires that any async delegation design include a context version tag in the delegation
request and a staleness check at integration.

**Tool-safety commitment boundary.** P3 identifies the question: at what point is a tool call
(a side-effectful reasoning action, such as a web search or a household device command)
committed such that it cannot be recalled? In the current architecture, SerpAPI web searches
are committed when `TieredEscalationBackend.escalate()` fires. There is no pre-commit
intercept for tool calls. For household device commands (not yet wired) this matters: a
command that reaches the device cannot be recalled. The control plane must intercept
before commitment, not after. The current escalation path has no intercept point between the
routing decision and the backend call. Speccing this intercept is part of the medium-horizon
formalization.

**Which problems HIP's existing components partially address:**
- Semantic commitment: partially addressed by the silence-on-Groq-call approach, which
  avoids a false commitment at the cost of naturalness.
- Result staleness: not addressed; the synchronous Groq call sidesteps the problem by
  making staleness impossible (no other turn can run while the call is in flight). When async
  delegation is added, this must be addressed.
- Tool-safety commitment boundary: not addressed for the Groq path (read-only, acceptable);
  not addressed for future device-command tools (write path, must be addressed before those
  tools are wired).

### 2.3 Specification of the formalization

**The delegation boundary interface.**
The `RouteDecision` dataclass (`harness/router.py:96`) already carries `tier`, `axis`,
`intent`, and `complexity`. For the medium horizon, the delegation event should be observable
by the interaction surface. This means the voice loop should emit a structured delegation
event (a new frame type, or an `OutputTransportMessageFrame` with a `label: "rtvi-ai"` and
`type: "delegation-started"` message) at the moment `route()` returns TIER_MID or TIER_CORE.
This event is the gap-fill trigger. The gap-fill response (if any) is parameterized by the
`axis` field: a complexity escalation calls for a different phrase than a freshness escalation.

**The gap-filling contract.**
A gap-fill phrase must be:
- Spoken immediately after the delegation event fires, before the reasoning call completes.
- Short enough to complete before a typical Groq response returns (target: under 1.5 s of
  speech).
- Semantically non-committal: it acknowledges that the system is working, but does not
  predict the content of the reasoning result.
- Consistent with HIP's persona (`_ORCH_BASE_PROMPT`, `server/voice_orch.py:152`).

The current `_ctrl_prepend` path (`server/voice_orch.py:1471`) shows the pattern but is
used only for control-flow announcements. The medium-horizon work extends it to routine
mid/core delegation.

**The result integration event.**
When the reasoning result returns, the interaction surface should receive a "delegation-
resolved" event before TTS begins speaking the result. This event carries the result text and
allows the interaction surface to prepare (e.g., the echo suppression to arm, the client to
show a "response incoming" indicator). Today this preparation is implicit; it should be
explicit so a future full-duplex layer can hook into it.

**The control plane intercept point.**
Before the backend call is made (`Router.dispatch()`, `harness/router.py:816`), and again
before the result is spoken, there must be an intercept point where the control plane can
inspect and, if required, block. Today there is one implicit intercept: the sensitivity gate
runs before routing. The medium-horizon spec requires a second, explicit intercept at result
time for future tool-call paths. This intercept is the hook where a "tool-safety commitment
boundary check" would live.

---

## 3. Longer-Term Horizon: The Governed Interaction Operating System and Full-Duplex Integration

**Layer-separation invariant: this horizon develops Layer 0 as a swappable adapter. Its
entire design must preserve the invariant that swapping the interaction model does not touch
Layers 1 through 3. Any design that couples the action plane to the routing cascade's
internal data structures (rather than to the `RouteDecision` public interface) violates the
invariant.**

**Layer-separation flag: the modular-adapter contract below defines the boundary the interaction
model must respect. Any full-duplex candidate that cannot satisfy this contract cannot be
integrated without re-architecting the durable layers, which is the failure mode the layered
architecture exists to prevent.**

### 3.1 The action-plane requirement

P2 establishes that full-duplex governance requires a structured output channel separate from
the audio stream. Section 0.5 confirmed the current architecture has no implementation of
this. The requirement for the longer horizon is:

The action plane is a real-time channel carrying structured decision records, one per
reasoning or governance event, in a format the control plane can inspect synchronously while
the audio stream continues. It is not a log; it is an interception bus. Each record carries:
- A turn identifier correlating the action to the audio segment that triggered it.
- The RouteDecision fields (`tier`, `axis`, `intent`, `complexity`).
- An action type: one of `speech_start`, `speech_stop`, `fact_inject`, `tool_commit`,
  `sensitivity_gate`, `cross_member_deny`.
- A commitment state: `pending`, `committed`, or `rolled_back`.

The control plane intercepts every `tool_commit` action before it transitions from `pending`
to `committed`. No side-effectful operation may reach a device or external service while its
action record is in `pending` state. This is the safety invariant for the action plane.

### 3.2 The empirical benchmark that gates any full-duplex integration decision

P2 states the hard constraint: `encode + model + decode < chunk_duration` sustained. For HIP
the target hardware is the Jetson Orin Nano Super (primary edge target) and the RTX PRO 6000
(studio/server deployment). The benchmark must be run on these platforms with:
- Audio chunk duration equal to the current pipeline's VAD segment duration (typically
  200-400 ms for a conversational segment at `start_secs: 0.2`).
- The candidate full-duplex model performing audio encoding, causal generation at the target
  output token rate for HIP's 2-3 sentence response length, and audio decoding of the
  generated speech, all within that chunk duration.
- Load condition: concurrent Silero VAD, Whisper STT for the second audio stream (the
  listening channel), and Resemblyzer speaker verification also running on the same hardware.

No full-duplex integration decision is made before this benchmark is run. The benchmark gates
the decision, not a theoretical capability claim from the model's documentation. The roadmap
document's framing (section 5) is precisely this: "when the reasoning, governance, and edge-
compute story matures." The compute story matures when the benchmark passes.

### 3.3 The modular-adapter contract

For any future interaction model (Step 2 through 5 on the P4 ladder) to drop into Layer 0
without disturbing Layers 1 through 3, it must satisfy this contract:

- **Input interface:** the adapter receives a `member_id` (string), a `facts` list (the
  output of the injection contract), a `session_id` (string), and the user utterance (text
  and/or audio depending on the model type). It does not receive raw routing cascade internals.
- **Output interface:** the adapter returns a response text (and/or audio) and emits action-
  plane records for each governance-relevant event. It does not call the routing cascade,
  the context graph, or the encryption layer directly.
- **Identity invariant:** the adapter does not perform speaker identification; it receives a
  verified `member_id` from the control plane. Turn detection and speaker identity remain the
  control plane's responsibility, not the model's.
- **Statefulness:** the adapter may maintain internal context (turn history) for the current
  session. It flushes this context on a speaker-change event, which the control plane delivers
  via a `context_flush` signal. It does not decide when to flush; the control plane does.

This contract means MoshiRAG (the P3 reference implementation for the open full-duplex stack)
would plug in as an adapter satisfying this contract: its `<ret>` delegation trigger would
emit a `fact_inject` action record and wait for the control plane to deliver injected facts,
rather than calling the fact store directly. This is the boundary that must be preserved.

### 3.4 Research-and-scoping frame

This horizon is not a committed build. It is the research direction the architecture is
designed to accommodate. The concrete work products for this horizon are:

1. A benchmark harness for the encode-plus-model-plus-decode constraint, runnable on target
   edge hardware, producing a pass/fail result against the chunk-duration bound. This is the
   gate metric.

2. A prototype action-plane record schema (JSON, validated against the types in section 3.1)
   exercised against the current cascade architecture to confirm the format is compatible with
   the existing routing telemetry (`harness/routing_telemetry.py`).

3. An evaluation of MoshiRAG's `<ret>` delegation mechanism against the modular-adapter
   contract (section 3.3), documenting where its interface matches the contract and where
   adaptation work is required.

None of these produces shipped code in this horizon. They produce the evidence base for the
decision about whether and when to proceed with a full-duplex integration.

---

## 4. Layer-Separation Flags: Summary

The following flags are the most important output of this analysis. Each identifies a place
where the modular architecture is at risk if a recommendation is implemented carelessly.

**Flag 1 (Near-term): Audio buffer coupling.**
The endpointing replacement must not discard the bracketed raw audio. If a Smart Turn
integration only exposes a turn-end event without the bracketed PCM, the speaker verification
path (`OrchestratorGate._audio_buf`, `server/voice_orch.py:915`) will lose its input.
Resolution: require that any endpointing component under evaluation be tested against the
speaker verification path before integration is declared complete.

**Flag 2 (Near-term): VAD frame protocol.**
`SpeakerGateProcessor` (`server/voice_orch.py:641`) depends on `VADUserStartedSpeakingFrame`
and `VADUserStoppedSpeakingFrame` for its audio accumulation. If the endpointing replacement
changes the protocol (different frame types, different timing relative to audio frames), the
gate breaks. This is a latent defect because the gate is currently disabled; it will surface
when the gate is enabled for household deployment.

**Flag 3 (Medium-term): Delegation event coupling.**
The delegation event (section 2.3) must be defined at the `RouteDecision` level, not at the
voice loop level. If it is implemented as an ad-hoc side effect inside `OrchestratorGate`,
it couples the medium-horizon formalization to the specific voice loop implementation and
must be re-implemented for any future interaction model. The event must be emittable by the
`Router.dispatch()` path, not only by `OrchestratorGate`.

**Flag 4 (Medium-term): Tool-safety commitment bypass.**
The Groq call in `OrchestratorGate._on_user_text()` currently goes directly to the Groq
API after the routing decision. There is no intercept point between the decision and the
call. For read-only tools (web search, knowledge retrieval) this is acceptable. For write-
path tools (device commands, data writes), routing to the reasoning tier without an intercept
would bypass the control plane's commitment-boundary check. Any wiring of write-path tools
through the Groq or escalation path must add the intercept before the tool call is committed.

**Flag 5 (Longer-term): Modular-adapter identity invariant.**
The modular-adapter contract (section 3.3) requires that the future interaction model receive
a verified `member_id` rather than performing speaker identification itself. If a full-duplex
model with built-in speaker diarization is integrated, there will be pressure to let that
model determine identity rather than HIP's Resemblyzer GE2E path. This must be resisted:
speaker identity is a Layer 3 (control plane) responsibility, and the model's diarization
is probabilistic, not deterministic. The control plane's verification result is what
determines permissions, regardless of what the model believes about speaker identity.

---

*Spec complete. No code was written or edited. Staging and commit are left to the operator.*
