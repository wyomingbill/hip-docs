HIP Prototype Evidence
What Was Built, What Works, What the Data Shows
Confidential. For NDA Distribution Only.
SKELETON. Structure defined, evidence capture pending. See marked placeholders.
Bill Brewster
Olinda Solutions
July 2026

Table of Contents



1. Purpose and Scope of Evidence
This document is the credibility artifact in the Superset package. Where the Technical Annex describes what HIP is architected to do and the Financial Annex models what it is worth, this document shows what has actually been built and run, with data. It is written for the same three audiences as the rest of the package (cable operator senior leadership, financial buyers, strategic partners) and its job is narrow: answer the question "has any of this actually worked, even once, outside a slide."
This is a skeleton. The structure, the evidence categories, and the honest-scope statement are final. The actual capture data (session traces, routing and Bloom confusion matrices, latency histograms, vignette transcripts) is marked with placeholder blocks below and will be populated from the coding thread's capture workstream, tracked as TD-049 through TD-052 in KNOWN_ISSUES.md.
2. What the Prototype Is
The prototype is a working harness, not a demo shell. It runs the same five-tier inference hierarchy, Bloom-based routing, and fact lifecycle architecture described in the Technical Annex, on real hardware, answering real voice queries.
Component
Detail
Hardware
Mac Mini M1 Pro, functioning as the household edge node for prototype purposes.
Voice server
HTTPS orchestrator on port 7860, launchd-managed (com.hip.voice.orch), Tailscale Funnel enabled for remote demo access.
Inference tiers
EDGE (qwen2.5:7b local), MID (Groq llama-3.1-8b), CORE (Groq llama-3.3-70b), FRONTIER (BYOK passthrough), WEB (SerpAPI freshness).
Routing
Bloom's taxonomy classifier mapping query complexity to tier: Levels 1-2 to EDGE, 3-4 to MID, 5-6 to CORE.
Fact extraction
qwen2.5:32b session-end extraction against the canonical 10-attribute fact schema (medication, allergy, health_condition, dietary, preference, schedule, employer, relationship, household, financial).
Fact-change detection
Groq Llama 4 Scout, async, 0.5-second target for detecting when a new statement contradicts or updates an existing fact.
Storage
Neo4j graph database, :Fact nodes written by the extraction queue, retrieved via read_user_facts() into the live system prompt.
UI
HIP-branded interface at /hip, distinct from generic voice-assistant chrome.

What is working, as of this document: the full routing cascade across all five tiers, Bloom classification driving tier selection, fact extraction and storage into Neo4j, and retrieval of stored facts into live conversation context. What remains open is the multi-member identity and testing workstream, addressed directly in section 9.
3. Session Traces Methodology
Each session with the prototype is captured as a newline-delimited JSON trace: timestamp, transcribed query, routing decision (tier assigned and why), model response, latency by stage (transcription, inference, synthesis, TTS), and any fact extraction or retrieval events triggered by that turn. The trace format is designed so a reviewer can reconstruct exactly which tier handled a query and why, without needing to re-run the session.
[EVIDENCE PLACEHOLDER: Sample session trace (2-3 representative newline-delimited JSON records, redacted of any personally identifying content, annotated inline with what each field shows).]
[EVIDENCE PLACEHOLDER: Aggregate session count and date range actually captured against the lean evidence bar described in section 9 (~40 real traces target, not the original 50-session/500-fact statistical bar).]
4. Fact Lifecycle Examples
The fact schema supports assertion, retraction, and update, not just accumulation. This section shows the lifecycle working end to end: a fact stated, a fact retrieved in a later session, and a fact corrected when the household's situation changed.
[EVIDENCE PLACEHOLDER: Assertion example: a household member states a new fact (e.g., a schedule or preference change); show the extracted :Fact node structure and the schema attribute it maps to.]
[EVIDENCE PLACEHOLDER: Retrieval example: a later session query that requires the platform to recall the previously asserted fact; show the trace demonstrating read_user_facts() surfacing it into context.]
[EVIDENCE PLACEHOLDER: Update/retraction example: a fact that changed (e.g., a medication dosage) and the trace showing the old fact superseded rather than duplicated.]
5. Routing Accuracy Against a Labeled Query Set
A labeled set of test queries, each with a known correct tier assignment based on the freshness/complexity/sensitivity signals described in the Technical Annex, is run against the live router and scored for agreement with the label.
[EVIDENCE PLACEHOLDER: routing_matrix.csv summary: confusion matrix of assigned tier vs. labeled correct tier, overall accuracy percentage, and the specific query classes where the router most often disagrees with the label.]
Given the lean evidence bar (section 9), this is reported as a mechanism-proving sample, not a statistically powered accuracy claim. A confusion matrix built on a small labeled set demonstrates the routing logic is operating as designed; it does not substitute for the larger labeled set a production accuracy claim would require.
6. Bloom Classification Agreement
Separately from tier-routing accuracy, this section evaluates whether the Bloom's-taxonomy complexity classifier agrees with human-labeled complexity judgments on the same query set, since routing accuracy and Bloom-level agreement can diverge (a query can be routed correctly by tier while the underlying complexity label is borderline).
[EVIDENCE PLACEHOLDER: bloom_matrix.csv summary: agreement rate between classifier-assigned Bloom level and human-labeled level, with the specific level boundaries (e.g., Level 2 vs. Level 3) where disagreement concentrates.]
7. Latency Histograms Per Tier
End-to-end latency, voice input to voice output, is the user-facing metric that matters most for the primary (EDGE) tier in particular, where the Technical Annex targets sub-500ms.
[EVIDENCE PLACEHOLDER: latency_by_tier.csv summary: latency distribution (P50/P90/P99 or histogram) for each of the five tiers, with the EDGE tier's performance against the sub-500ms target called out explicitly.]
8. Three Demo Vignettes
Three scripted scenarios demonstrate the platform's core claims in a form a non-technical reviewer can watch or read end to end. The structure for each is fixed below; the actual captured transcript or video is pending.
8.1 Vignette: Care coordination
Demonstrates: household-scoped memory holding a family care situation across multiple turns and, ideally, multiple sessions, the core claim of Part I and Part III of the white paper.
[EVIDENCE PLACEHOLDER: Timestamped transcript or video of a care-coordination scenario (e.g., a household member asking about a parent's medication schedule, the platform recalling context asserted in an earlier session).]
8.2 Vignette: Freshness handoff
Demonstrates: the freshness tier correctly identifying a query that needs current information, stripping household context before the external call, and synthesizing the result back into household-scoped context on return, per the trust-boundary design in Part I of the white paper.
[EVIDENCE PLACEHOLDER: Timestamped transcript showing a freshness-tier query (e.g., weather or a live score), the stripped external call, and the synthesized response.]
8.3 Vignette: Passthrough consent
Demonstrates: the passthrough tier's explicit-crossing announcement when a subscriber routes a query to their own frontier model account, the visible boundary-crossing behavior that Part I of the white paper describes as always subscriber-initiated and always visible.
[EVIDENCE PLACEHOLDER: Timestamped transcript showing a passthrough-tier request, the platform's announcement of the boundary crossing, and subscriber confirmation before the query leaves the trust boundary.]
9. Honest Scope Statement
This section exists because the credibility of every other section in this document depends on stating plainly what the prototype is not, not just what it is. Overclaiming here would undermine every other claim in the Superset package.
Single-user primary, text-injected second participant. The prototype's primary tested user is Bill's own voice, enrolled and used for all voice-based sessions. A second participant, referred to as Sarah in internal testing, is represented via a text-injection toggle, not a second enrolled voice. Any claim about multi-member household behavior in this document should be read against that fact: it demonstrates the multi-member identity and permission logic is wired and functional, not that voiceprint-based identification has been validated across two real voices.
Approximately 40 real traces, mechanism-proving, not statistical. The evidence bar for this document is roughly 40 real session traces plus the three demo vignettes, sufficient to demonstrate the mechanisms in sections 3 through 8 are real and working. This is explicitly not the 50-session, 500-fact-assertion statistical bar originally scoped in the Superset project brief. That bar requires a second enrolled voice and a multi-week testing window that has not yet occurred.
What is NOT claimable from this document, stated explicitly so no reader infers it:
Voiceprint-based identity discrimination validated across two or more real, distinct voices.
A 200-query statistically powered confusion matrix for routing or Bloom classification.
The 50-session-across-two-weeks / 500-fact-assertion evidence bar from the original project brief.
Fact retraction and update behavior validated across real, extended household use rather than a constructed lifecycle example.
10. Known Issues
Distilled from KNOWN_ISSUES.md. These are the open engineering items most relevant to reading this evidence document honestly.
ID
Issue
Relevance to this document
TD-047
Echo cancellation
Affects voice session quality in demo conditions; may explain any transcription artifacts in captured traces.
TD-048
Barge-in handling
Affects turn-taking in voice sessions; relevant to interpreting latency data in section 7 if a session includes an interrupted turn.
TD-049 through TD-052
Evidence capture workstream
The open items that directly block populating the placeholders in sections 3 through 8 of this document.

