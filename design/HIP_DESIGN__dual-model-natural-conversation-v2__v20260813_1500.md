# HIP Natural Conversation — Dual-Model Architecture, Spec v2
Status: ADOPTED DIRECTION (research lane; no requirement filed)
Reconciled-Against: f1c687f (roadmap HEAD at write time; tree clean apart from four untracked demo-cutover dispatch docs belonging to another lane, left as found). Banked at 4a7b82f, HA-66, 2026-08-13. Docs-only: banked VERBATIM from Bill's paste, reconciled against no code, no graph and no harness run.
Date: 2026-08-13
Consolidates three inputs delivered via chat 2026-08-13: CGPT "Dual-Model / Moshi Design Spec for Review", Fable review (ACCEPT WITH CHANGES, 5 changes), CGPT second-pass feedback. This document is the durable record of all three.
Relation to plan of record: does NOT amend the FinishPlan. Sequencing constraint in §8. Nothing here is a FinishPlan step.

## 1. Governing principle (revised)
Moshi decides WHEN a conversational act is appropriate. HIP decides WHAT acoustic content that act is allowed to produce. The Conversation Model never gets an uncontrolled speaker.
(Supersedes v1's "Moshi may say harmless things itself.")

## 2. Three components
- Conversation Model (Moshi-class, local): duplex timing, interruption detection, yield/stop, backchannel timing, act proposals. No authority, no memory authority, no direct speaker.
- HIP Kernel (deterministic, not a model): identity/tier, request framing, reference binding, authorization, memory admission, structural refusal, audit, the disclosure boundary. Unchanged from the governed text path.
- Reasoning Model: substance only, from GovernedRequest. Receives no authority from prior conversational turns.

## 3. Interaction-act gate (replaces v1's phrase whitelist)
Moshi's M1 output is an ACT, never audio:
  ACK         -> fixed utterance ("Mm-hm.")
  BACKCHANNEL -> fixed short set
  HOLD        -> fixed utterance ("One second.")
  YIELD       -> silence
  STOP        -> immediate audio halt
Deterministic map: act -> permitted rendering, spoken by governed TTS or fixed samples. Moshi's own acoustic output is not emitted in M1.
Rationale: classify-after-speech is a race — disclosure can precede classification. Act-before-render closes the race. M2's research question therefore becomes: can the vocabulary safely expand beyond a finite deterministic act set?
Carried constraint: act selection and timing must not depend on hidden household information (tested under G3, statistically).

## 4. Output classes (retained from v1)
C0 non-semantic and C1 procedural (both via the act map); C2 clarification (HIP-constructed only — options can leak); C3 substantive (requires AuthorizedResponseEnvelope); C4 structural refusal (canonical path; the model never decides, rewrites, explains, or embellishes); C5 memory/consent transactions (protocol messages, not conversation). Uncertain class -> block.

## 5. Interfaces (retained from v1)
ConversationObservation in (evidence; grants no authority). GovernedRequest to the Reasoning Model (unchanged). AuthorizedResponseEnvelope out, with may_paraphrase=false and may_expand=false for all prototypes through M4.

## 6. Who speaks substantive words
Option 1 — governed TTS bridge (Kokoro speaks HIP-authorized text): FIRST PROTOTYPE.
Option 2 — authorized exact-text rendering by Moshi: M4 research; likely requires fine-tuning; fallback is Option 1.
Option 3 — Moshi answers freely from supplied context: REJECTED as initial architecture.
TWO-VOICE RISK PROMOTED TO M1. Compare three configurations: (a) current Whisper->HIP->Kokoro; (b) Moshi interaction voice + Kokoro substantive voice; (c) Moshi timing control + one consistent renderer, if technically possible. If (b) sounds worse than (a), that is an M1 finding, not an M3 surprise.

## 7. Research stages, outcomes, LOE (dispatch-days)
M0 — measure unmodified Moshi locally (MLX). 2-4 dd. No HIP data, no HIP trees. FOUR QUESTIONS:
  Q1 sustained realtime factor <= 1 on this hardware
  Q2 duplex (interruption/overlap) works under realistic mic/speaker conditions
  Q3 usable programmatic access to the semantic/text stream BEFORE acoustic emission
  Q4 spontaneous speech can be suppressed while conversational-state processing continues
Q3 and Q4 outrank Q1. NAMED OUTCOMES: PASS (practical integration surface exists) / PARK-COMPUTE (works, hardware insufficient) / PARK-CONTROL (output boundary cannot be imposed cleanly) / FAIL-VALUE (duplex gain insufficient). Any PARK or FAIL parks the lane; the finding is the deliverable.
M1 — sidecar with the interaction-act gate + the two-voice comparison. 6-10 dd. Depends on A1 (governed voice) ONLY — not on conversation memory.
M2 — semantic-gate research (expanding beyond the finite act set). 8-15 dd. Genuine research; can fail; failure keeps M1's act set.
M3 — asynchronous HIP bridge (candidate request -> kernel -> AuthorizedResponseEnvelope). 5-8 dd. First intersection with the conversation-memory track. Full governed process from here.
M4 — governed exact-text rendering by Moshi. 10-20 dd. OPTIONAL; fallback Kokoro.
M5 — unified full-duplex prototype. 10-15 dd. Only after M0-M3 (M4 optional).
Usable Option-1 prototype = M0-M3, ~21-37 dd. Full vision ~40-70 dd.

## 8. Sequencing
M0 may run at any time as a bounded research spike: no HIP data, no HIP trees, no schedule claim, negative results save 20-60 dd downstream. Everything M1+ waits behind the FinishPlan's demo finish line and A1. Conversation memory (B2/B3) proceeds independently; the tracks intersect at M3. Nothing in this lane blocks, reorders, or amends the FinishPlan.

## 9. Voice evidence and speaker identity
Speaker verification stays inside HIP's boundary, computed on raw audio (Resemblyzer today; any successor later). Moshi never asserts identity and cannot upgrade an authentication tier (G4). The voice evidence envelope from v1 §12 stands. Uncertainty may reduce authority or defer a transaction; it may never increase authority.

## 10. Acceptance (G1-G10 retained, two amendments)
G3 (hidden-history noninterference) is tested STATISTICALLY: response-onset and behavior distributions must not differ between hidden-state conditions. The timing side channel is bounded, never claimed eliminated. G10's naturalness comparison begins at M1 via §6's three-configuration test, not at the end.

## 11. Disposition of the five Fable changes
1 name-the-gate -> resolved by §3 (the gate is an act allowlist, deterministic). 2 timing side channel bounded-not-eliminated -> §10. 3 M0 stop rule -> §7's four outcomes. 4 speaker-ID placement -> §9. 5 M1-needs-a-gate -> §3 (the gate IS M1's architecture, honestly ordered).
END OF DOCUMENT
