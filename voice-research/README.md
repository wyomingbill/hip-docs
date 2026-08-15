# HIP Voice Interaction Research Corpus

This folder holds the full voice interaction research corpus for the HIP project.

## Reading Order

| # | File | Description |
|---|------|-------------|
| P1 | HIP_Voice_Architecture_Research_P1_Taxonomy__v20260709_2154.md | Taxonomy of voice interaction models; establishes the hybrid conclusion and places the current routing cascade on the landscape. |
| P2 | HIP_Voice_Architecture_Research_P2_FullDuplex_Mechanics__v20260709_2157.md | Full-duplex streaming mechanics, latency budgets, and the action-plane requirement for governed real-time voice. |
| P3 | HIP_Voice_Architecture_Research_P3_Interaction_Thinking_Split__v20260709_2157.md | The interaction-model/reasoning-model split, delegation boundary design, and the open problems in semantic commitment and result integration. |
| P4 | HIP_Voice_Architecture_Research_P4_Turn_Detection__v20260709_2157.md | Turn detection and endpointing; the five-step migration ladder from silence threshold to fused semantic-prosodic prediction. |
| P5 | HIP_Voice_Architecture_Research_P5_Edge_Model_Selection__v20260710_1137.md | Edge model selection criteria; evaluation of CPU-viable, edge-compatible components against the current stack. |
| P6 | HIP_Voice_Architecture_Research_P6_Speaker_Identity__v20260710_1137.md | Speaker identity and verification; the coupling between endpointing and the identity kernel and where permissions enforcement must live. |
| P7 | HIP_Voice_Architecture_Research_P7_Latency_Cost_Model__v20260710_1137.md | Latency and cost modeling; encode-decode-model budget analysis and the empirical benchmarks that gate full-duplex decisions. |
| P8 | HIP_Voice_Architecture_Research_P8_Reference_Architecture__v20260710_1137.md | Reference architecture; the modular adapter contract that lets a future interaction model replace the current surface without disturbing durable layers. |

## Synthesis and Directive Documents

`HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032.md` is the NDA-facing synthesis: the architecture thesis and roadmap derived from the corpus above, written for external stakeholder review.

`HIP_Orchestrator_Task_Voice_Development_Path__v20260710_1032.md` is the coding-orchestrator directive derived from the same set: it tasks the CC session with grounding the research in the actual codebase and producing a staged development specification.

## Live/ Field Observations

`Live/` holds GPT Live field observation logs. These are secondary context only. They record behavior of a competing system under real conditions and carry an explicit coherence-check-not-validation caveat. They must not be treated as design directives. Use them only to confirm that a direction already grounded in the P-docs is consistent with what the field is doing.

## Priority by Horizon

- **Near-term:** P4 drives the work. The endpointing migration ladder is the near-term spine.
- **Medium-term:** P3 drives the work. The interaction-and-reasoning split and its open problems.
- **Longer-term:** P8 drives the work. The reference architecture and the full-duplex modular adapter contract.
