# ANALYSIS: Classifier Placement and the Sovereign Claim
Status: BUILT
Reconciled-Against: docs corpus 2026-07-11 (SIA_SPEC__structured-intent-architecture__v20260710_1614 Phase B, SIA_SHADOW_DIFF__v20260710_2106/_2204 fallback rates, ANALYSIS__candidate-intent-deep-review__v20260711_0501, HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032, voice-research P7); no code changed

---

## 0. The decision under review

Phase B made the injection contract consume the SIO synchronously on every turn. One Ollama instance now serves the classifier, the extraction model, and the embedding calls, and the measured consequence is a 26 to 31 percent fallback rate under GPU contention and visibly slow turns. A GPT-Realtime voice demo will surface this as latency. Two fixes are proposed: (A) a dedicated, pre-warmed second Ollama instance for the classifier, everything stays on-device; (B) a cloud-hosted classifier (Groq, or the wired OpenAI account) for demos only, local path retained for the sovereign story.

Recommendation up front: A for the demo, A plus serving hardening for production, and B rejected for both, with one honest caveat about what B gets right (section 2.3). The reasoning follows the five questions asked.

---

## 1. Does cloud-for-demo undermine the pitch?

Yes, and the mechanism is worth stating precisely, because it is not "demos must be pure." Demos stage things constantly, and operator technical teams know it. Staging is fatal only when the staged component is the claim itself.

HIP's pitch to an operator is not "AI in the home." It is: the governance runs here, on this box, and no cloud party is in the loop between a household utterance and the decision about what may be disclosed or written. The SIO classifier is the first thing that happens to an utterance on the governed path. Cloud-hosting it means the demo's governance loop round-trips through a datacenter on every turn. The component being relocated is not adjacent to the claim; it is the entry point of the thing being claimed.

The credibility failure mode is concrete. A DD engineer asks "walk me through one turn." The honest answer under B is: audio goes to OpenAI Realtime, the transcript goes to Groq for classification, the classification comes back, and then the local envelope evaluates it. At that point the only load-bearing local components are Neo4j and the guard code, and the engineer's notebook says "local database with cloud AI." The pitch has inverted in one sentence.

Two aggravating factors specific to HIP:

- **The corpus is discoverable.** The whole diligence posture (deep review section 4) is built on the reconciled-against habit: testing docs, shadow diffs, and the MANIFEST are shown under NDA as evidence of engineering discipline. A `SIO_BACKEND=groq` demo configuration is a permanent artifact in git history, and this very document would sit next to it. HIP cannot stage B quietly, and a disclosed "cloud for demo, edge for production" reads as: the edge path does not meet its own latency bar on the target hardware. That is currently TRUE (the fallback rate says so), and the honest move is to present the problem and the fix, not to route around it in the one setting where the claim is being evaluated.

- **B forfeits the demo's best moment.** The strongest single thing a sovereign-governance demo can do is cut the network mid-session: the GPT-Realtime voice surface dies, and the governed text path keeps answering from local facts. That is the layered-architecture thesis (replaceable cloud interaction surface, durable local governance) performed live in ten seconds. Under B, cutting the network kills classification too, and the moment is unstageable.

Is "cloud for demo, edge for production" ever credible? Yes, when the demo is about UX and the staged part is not the differentiator. For an operator infrastructure pitch whose differentiator is where governance runs, it is not.

---

## 2. Is the classifier the right thing to put in the cloud?

This question has a more interesting answer than the positioning one, because the CandidateIntent architecture was specifically built so that the classifier is untrusted.

### 2.1 The line: decision plane versus data plane

The reasoning tiers already run off-net via Groq, and nobody considers that a sovereignty violation. The principled difference:

- **Data plane (Groq reasoning tier today):** the component receives only what the governance envelope has ALREADY decided to disclose. The envelope interposes before it. Its output is prose for the user, not input to an authorization decision. Off-net placement exposes post-envelope, already-authorized context.

- **Decision plane (the SIO classifier):** the component runs BEFORE the envelope, sees the raw utterance stream, and its output is what the envelope acts on. Off-net placement puts a network party upstream of every governance decision.

A component may live off-device when: (1) it receives only post-envelope disclosures, or zero governed data beyond what the interaction surface already conceded; (2) its output is treated as an untrusted proposal, never authority; and (3) its unavailability fails closed without breaking a core product promise. The reasoning tier passes all three. The classifier passes (2) by construction, passes (1) only in the specific GPT-Realtime demo context (section 2.3), and fails (3) for production outright: offline operation is a sovereignty promise (the eldercare pitch includes "works when the internet does not"), and a cloud classifier makes every governed turn network-dependent, with the deny-safe default converting every cloud blip into refused turns. The deep review (section 1.3) already flagged fail-closed availability as a safety property in a care context; B imports cloud availability into that equation permanently.

### 2.2 What actually changes, and what does not

Here is the honest architectural point, and it should go in the white paper regardless of this decision: **from an authorization standpoint, a cloud classifier is exactly as untrusted as a local one.** The identity envelope is bound locally by authentication and never by the model. `speaker_relationship` is derived by code from the authenticated member and the registry. Resolution only admits registry-known identities. The deny-safe default and the L3 mutation tests prove the consumers fail closed when the SIO is absent or hostile. P8 parks trust-regressing writes, P9 severs classifier confidence from fact trust, P10 makes parked writes non-confirmable by injection. The architecture would CONTAIN a malicious cloud classifier just as it contains a locally injected one. That containment is a real strength and the correct way to describe the design.

What placement DOES change: privacy (the raw utterance stream, including utterances about non-consenting household members and care recipients, transits and is retained by a third party under their policy, not the household's), availability (section 2.1), and positioning (section 1). So the answer to "where is the principled line" is: **placement of the classifier is a privacy, availability, and positioning decision, not an authorization decision.** The governance does not break under B. The promise does.

### 2.3 The one thing B gets right

In the GPT-Realtime demo specifically, the utterance stream ALREADY transits OpenAI: the microphone feed and transcripts go to the Realtime API. The marginal privacy exposure of also sending transcripts to Groq is one additional party, not a new class of exposure. Anyone rejecting B on demo-privacy grounds while running the demo on GPT-Realtime is applying the principle inconsistently. The rejection of B rests on positioning (section 1) and on availability precedent, not on demo-context privacy. Production is a different matter: the roadmap's target interaction surface is local, at which point a cloud classifier would be the ONLY raw-utterance exfiltration path, indefensible.

---

## 3. Latency reality check

Rough numbers, labeled as estimates; the P7 latency/cost model is the deeper reference.

| Path | Typical per-classification | Notes |
|---|---|---|
| Groq, 7-8B class, constrained JSON ~60 tokens | 150 to 350 ms | LPU decode is near-instant; RTT 30 to 80 ms dominates variance. Consistent. |
| Local qwen2.5:7b, uncontended, pinned | 400 to 1200 ms | M-series decode ~40 to 70 tok/s; prompt KV cache warm. |
| Local, contended (today) | 1.5 s timeout breached 26 to 31 percent of turns | Contention is mostly model EVICTION: three models sharing one Ollama instance cause reload storms measured in seconds, not decode-speed sharing. |
| Local, exact-match cache hit | ~0 ms | Stateless SIO makes the cache sound (SIA 1.1). |

Three observations that change the comparison:

1. **The fix for contention is pinning, not relocation.** The 26 to 31 percent fallback is not "a Mac Mini cannot run a 7B classifier"; it is one Ollama instance thrashing three models in and out of memory. A dedicated instance with the model pinned (`keep_alive`, own port) removes the reload storms. Option A's realistic result is the uncontended row: 400 to 1200 ms.

2. **The classifier is off the critical path by design.** SIA runs the SIO call concurrent with retrieval; the turn cost is max(SIO, retrieval) minus retrieval. With retrieval at 200 to 400 ms, a pinned local SIO adds roughly 100 to 800 ms to a turn. In a GPT-Realtime voice turn, whose own cloud round-trip and TTS pacing set a 1.5 to 2.5 s conversational rhythm, a 300 to 800 ms governed-context assembly is at or below the perception threshold. Groq at 200 ms would be faster on paper and imperceptibly different in the demo.

3. **Decode length is a free win.** The SIO's constrained JSON can shed tokens (short enum values, no rationale field); grammar-constrained decode (already recommended by the deep review for injection reasons) also shortens output. Halving output tokens roughly halves local decode time. A scripted text demo additionally rides the exact-match cache; a live-voice demo mostly will not (ASR transcript variance), so do not budget on cache hits for the Realtime demo.

So: would cloud give a BETTER demo experience? Marginally faster turns, invisibly so once A is done, in exchange for the section 1 costs. And if the local path were left contended and visibly laggy, the answer is still A: a slightly slower demo whose core claim is real beats a snappy demo whose core claim is staged, in front of the one audience whose job is to detect exactly that. The latency argument for B only holds while the serving problem is unfixed, and the serving problem is a config change plus a pre-warm script, not a research program.

---

## 4. The third option: severing governance-critical from quality classification

The proposed severing already exists structurally; it is the CandidateIntent pattern itself. Enumerating what is already deterministic and model-independent:

- Identity and `speaker_relationship`: bound by authentication, derived by code. No classification, local or cloud, touches them.
- Denial: SIO absent, malformed, or low-confidence produces the deny-safe default; guards fire; nothing personal is disclosed. L3 mutation tests prove it (disable SIO, no leak).
- Resolution: deterministic against the registry; the model cannot mint a subject.
- Write authority: statements produce proposals; P8 parks trust regressions; P10's confirmation path never touches the model.

What the model classification actually carries is admission QUALITY within the requester's own authorized scope (right attribute targeting, phrase-invariant recall) and write-detection triggering (bounded by parking). That is precisely "quality classification" in the question's terms. So the severing does not need to be built; it needs to be NAMED, as an invariant: **classification carries no authority; therefore classifier placement is never an authorization decision.** That is the sentence that resolves the tension in question 2, and it is the sentence the white paper's trust-boundary section should carry.

Does that make the cloud classifier acceptable, since it is quality-only? For the demo: it makes B DEFENSIBLE in principle, and still wrong in practice, because the positioning cost (section 1) is unchanged, and because once A exists, B buys nothing measurable (section 3). For production: no, because privacy and availability (section 2.1) are independent of the authority question, and production's local interaction surface removes the section 2.3 mitigation entirely.

One genuine simplification does fall out of this analysis: the deterministic pre-guards (the A6 injection needle check, the ack guard, the confirmation gate) plus the frozen regex fallback constitute a complete, model-free governance floor. The demo can state that floor explicitly: "if every model in this box lies, here is what still cannot happen." That is a stronger sovereign claim than "the classifier is local," and it is already true.

---

## 5. Recommendation

**Demo: option A, plus staging discipline.**
- Dedicated Ollama instance for the classifier, model pinned with keep_alive, own port, pre-warmed at server start. Extraction and embedding stay on the first instance; they are async and off the turn's critical path.
- Shorten the SIO decode (drop any free-text field from the schema output; grammar-constrained decode).
- Pre-warm the cache with the scripted phrasings where the demo is scripted; budget zero cache hits for live voice.
- Measure and show the number: fallback rate before (26 to 31 percent) and after isolation, as a slide or a dashboard panel. The contention incident becomes evidence of engineering rigor instead of a thing to hide, consistent with the containment-not-prevention posture from the deep review.
- Keep the network-cut moment in the script: kill the uplink, voice surface dies, text-path governance keeps working locally. That is the pitch, performed.

**Production: local, with serving isolation as a stated architectural requirement.**
- The classifier is decision-plane and stays on-device, not because the architecture would break otherwise (it would not; the envelope treats it as untrusted regardless) but because raw-utterance privacy, offline availability, and the sovereign promise all bind to placement.
- Serving isolation (dedicated inference lane for the governed-path classifier, so interaction-surface and background workloads cannot contend with it) should be written into the reference architecture (voice P8) as a requirement, with the P7 benchmarks gating hardware choices. A smaller distilled classifier (3B class), gated by the golden set, is the likely production shape on Jetson-class targets.

**What the demo must prove, stated once:** that a cloud interaction surface can be swapped in and out above a governance layer that never leaves the household. Option B would spend the demo disproving it.

**Rejected: option B**, for demo and production, with its one legitimate insight retained: the architecture's indifference to classifier trustworthiness is real, provable, and belongs in the white paper as the reason HIP can adopt ANY future classification model, local or hosted, without re-architecting governance. That claim sells optionality. Running the demo's governance through Groq to save 400 imperceptible milliseconds does not.

---

## 6. Positioning notes for the deliverables

- Part I (architecture): already marked NEEDS-UPDATE in the MANIFEST for the CandidateIntent pattern; this analysis adds the "classification carries no authority, placement is not an authorization decision" invariant and the decision-plane/data-plane distinction. Fold both into the same update.
- Part VI (Where Compute Must Live): the macro claim (inference distributes outward) needs one qualifying paragraph: decision-plane inference does NOT distribute; it anchors to the governance boundary. The existing Groq reasoning tier is the data-plane example; the classifier is the counterexample. Marked NEEDS-UPDATE in the MANIFEST with this scope.
- The demo script should add the network-cut beat and the fallback-rate before/after panel.
- Do not create any demo configuration that points classify_sio at a cloud endpoint. The config would outlive the decision in git history and read as the staged version of the core claim.
