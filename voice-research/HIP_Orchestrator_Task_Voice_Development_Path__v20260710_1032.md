---
doc: Orchestrator Task, Voice Interaction Development Path
purpose: Directive for the coding orchestrator (chat running CC) to analyze the voice research corpus and produce a staged development specification grounded in the actual codebase.
status: task directive
version: v20260710_1032
location: ~/hip-dev/docs/voice-research/
model_discipline: Sonnet for analysis and spec authoring. Fable only if a genuine multi-subsystem reasoning knot appears and Sonnet has failed on it twice. Never Opus.
constraints: no em or en dashes. Do not edit code in this task. Produce a spec, stop.
---

# Orchestrator Task: Analyze Voice Research and Spec the Development Path

## Purpose and boundaries

This is an analysis-and-specification task, not an implementation task. The output is a staged development specification for HIP's voice interaction layer, grounded in the actual current codebase and disciplined by the voice architecture research. No code is written or edited in this pass. The deliverable is a plan a person reads and approves before any build begins.

The governing constraint is HIP's layered architecture. The interaction surface is modular and replaceable. The routing cascade, the context graph, and the control plane are durable. Every recommendation in the spec must preserve that separation. Any recommendation that would couple the durable layers to a specific interaction-surface generation is wrong by construction and must be rejected in the analysis.

## Source material, and how to weight it

Read these as the authoritative research basis, in this order of priority:

1. ~/hip-dev/docs/voice-research/HIP_Voice_Architecture_Research_P4_Turn_Detection__v20260709_2157.md
   Primary for near-term work. The endpointing migration ladder is the near-term spine.
2. ~/hip-dev/docs/voice-research/HIP_Voice_Architecture_Research_P3_Interaction_Thinking_Split__v20260709_2157.md
   Primary for medium-term work. The interaction-and-reasoning split and its open problems.
3. ~/hip-dev/docs/voice-research/HIP_Voice_Architecture_Research_P1_Taxonomy__v20260709_2154.md
   The hybrid conclusion and the placement of the current cascade.
4. ~/hip-dev/docs/voice-research/HIP_Voice_Architecture_Research_P2_FullDuplex_Mechanics__v20260709_2157.md
   The longer-horizon full-duplex mechanics and the action-plane requirement.
5. ~/hip-dev/docs/voice-research/HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032.md
   The architecture and roadmap thesis this spec must serve and stay consistent with.

Treat everything under ~/hip-dev/docs/voice-research/Live/ as secondary context only. It is field observation of a competing system, carries an explicit coherence-check-not-validation caveat, and must never be treated as a design directive. Do not spec toward anything GPT Live said. Use it only to confirm that a direction already grounded in the P-docs is consistent with what the field is doing.

## What to analyze against the actual code

Ground every claim in the real codebase. Start with router.py and the voice orchestrator on port 7860, and follow the code as needed. For each finding, cite specific files and lines. Do not describe what the system probably does; read it and state what it does.

1. Current interaction surface. Identify the exact endpointing and turn-detection mechanism in the code today. If silence-threshold based, state the value and where it is set. Place the current voice path precisely on the P4 five-step migration ladder, with code evidence.

2. Current routing cascade. Confirm how router.py implements the tiered hierarchy and the complexity classifier. Map the current implementation onto the interaction-model-plus-reasoning-model split from P3. State explicitly which tier plays the interaction-model role and which tiers play the background-reasoning role today, and where the delegation boundary actually sits in the code.

3. The control plane. Locate where identity, consent, speaker verification, and permission enforcement live in the current code. Confirm whether enforcement is deterministic and outside the model, per the Layer 3 requirement. Flag any place where a hard constraint is currently resting on model behavior rather than deterministic code, since that is an architectural defect against the roadmap.

4. The coupling P4 and the roadmap both call out. Turn detection and the speaker-verification / identity kernel must be designed together, because whose-utterance-is-this and which-member's-permissions-apply are the same question. Identify where in the current code that coupling lands, or where it is currently absent and needs to be created.

5. The action-plane gap for the longer horizon. Per P2, full-duplex requires a second, structured output plane separate from speech, and that plane is where governance attaches. Assess whether the current architecture has any analogue to a structured action channel, and note what would have to exist for the control plane to intercept a full-duplex interaction model later. This is scoping for the far horizon, not a near-term build.

## What to produce

One versioned specification file written to ~/hip-dev/docs/, named:
HIP_Voice_Development_Spec__v<YYYYMMDD_HHMM Mountain>.md
No em or en dashes anywhere.

The spec is organized in three horizons, each bounded and each preserving layer separation:

**Near-term horizon.** The single highest-leverage, lowest-effort change, which the research expects to be replacing silence-based endpointing with fused semantic-prosodic turn prediction. Confirm or refute that expectation against the actual code. Name the specific open, CPU-viable, edge-compatible component to integrate first (from Silero VAD, Pipecat Smart Turn v3.2, LiveKit v1-mini, VAP) and justify the choice against the current stack. Provide a bounded, ordered step list for this one change. State the identity-kernel coupling explicitly, since the endpointing work and the speaker-verification work should be specced together. Define what "done" looks like and how it is verified on the edge hardware.

**Medium-term horizon.** Formalize the interaction-and-reasoning split that the routing cascade already embodies. Specify the delegation boundary, the gap-filling behavior, the result-integration point, and, critically, where the control plane intercepts. Pull the relevant open problems from P3 (semantic commitment, result staleness with context versioning, tool-safety commitment boundary) and state which of them HIP's existing components already partially address and which are net-new work. Keep this a specification of interfaces and boundaries, not an implementation.

**Longer-term horizon.** The governed interaction operating system and the eventual full-duplex integration. Specify the action-plane requirement from P2 as the governance attachment point, the empirical benchmark that gates any full-duplex decision (sustained encode-plus-model-plus-decode under the chunk duration on the target edge hardware, Jetson Orin Nano Super versus RTX PRO 6000), and the modular-adapter contract that lets a future interaction model drop into Layer 0 without disturbing Layers 1 through 3. This horizon is a research-and-scoping frame, not a committed build.

For every horizon, state the layer-separation invariant it must not violate, and flag any dependency that would force a durable layer to change in order to accommodate an interaction-surface change. Those flags are the most important output of the task, because they are where the modular architecture is at risk.

## Process discipline

Analyze against real code with file and line citations throughout. Do not speculatively refactor, do not branch into alternatives the research does not support, and do not editorialize. Produce the spec, write the one file, stop. Leave staging and commit to the operator. Use Sonnet. If a genuine multi-subsystem reasoning knot appears and two Sonnet passes have failed on it, escalate that single sub-problem to Fable and note the escalation in the spec. Never Opus.
