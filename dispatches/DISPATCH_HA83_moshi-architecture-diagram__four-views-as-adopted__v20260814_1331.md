# DISPATCH_HA83 — Moshi dual-model architecture diagram (design artifact)
Status: BUILT
Reconciled-Against: `roadmap` @ this dispatch's commit

> **RELABELED BY HA-84 (Bill's ruling, 2026-08-14).** The deliverable's category
> label **PROVEN is now LAB-MEASURED** wherever the underlying research artifact
> carries `Verification: UNVERIFIED`. **The label must carry the meaning itself;
> the footnote redefinition this dispatch used was REJECTED** — a reader who
> takes the label at face value, or quotes a row without the footnote, gets a
> stronger claim than the evidence supports.
>
> **This document is left as written**, per the pre-authorized correction class:
> annotate, never silently patch. Its tables below say PROVEN because that is
> what HA-83 produced. The deliverable itself now says LAB-MEASURED.

**TYPE:** BUILD (documentation artifact) — **docs only: no code, no lab run, no
graph, no harness.**

**REQ: NONE**, and correctly. This draws two already-banked design documents; it
builds no product behaviour and amends no plan of record. CLAUDE.md item 10
permits `REQ: NONE` for work that touches no code and requires it be said plainly.

**DELIVERABLE:**
`docs/design/HIP_DESIGN_DIAGRAM__moshi-dual-model-architecture-as-adopted__v20260814_1331.md`

---

## WHAT WAS BUILT

Four Mermaid views of the dual-model architecture **as adopted**:

* **D1 — runtime topology.** Mic → Moshi (owns WHEN; proposes ACTs; no direct
  speaker in M1) with raw audio in parallel → speaker ID **inside HIP's
  boundary** → HIP kernel (deterministic; act allowlist; semantic commit point)
  → reasoning model → `AuthorizedResponseEnvelope` (`may_paraphrase=false`) →
  governed TTS (Kokoro) speaking all substance.
* **D2 — the semantic commit point.** C0–C5, which side of the line each sits
  on, who may produce it, and the failure direction (**uncertain ⇒ block**).
* **D3 — latency split.** Interaction latency (Moshi's acknowledgment) vs
  information latency (first authorized substance), with HIP's work in the gap.
* **D4 — stage ladder** M0→M5, with the research/governed **border** drawn as
  absolute: nothing merges; graduation is re-implementation.

**Drawn from spec v2 where v1 and v2 differ.** Deliberately **not** drawn:
v1's *"Moshi may say harmless things itself"*, v1's phrase whitelist, and
Option 3 (Moshi answering freely), which v2 §6 rejects as initial architecture.

## THE LABELS

Every element carries **PROVEN** / **ADOPTED DESIGN** / **OPEN QUESTION**.

| PROVEN (M0/drift lab evidence) | ADOPTED DESIGN (ruled, unbuilt) | OPEN QUESTION |
|---|---|---|
| RTF **0.684** flat at steady state; two OS processes, rate-limited by the slower stage | Moshi owns WHEN; acts not audio | the **two-voice seam** vs G10 |
| text **causally upstream** of audio (Q3) | act allowlist replaces the phrase whitelist | **M4** text forcing — may resolve to "keep governed TTS" |
| audio suppressible while state advances (Q4) | speaker ID inside HIP's boundary | **M2** semantic gate — genuine research, can fail |
| duplex confirmed at a real mic (Q2) | C0–C5 classes and the commit point | no measured number for the **D3 gap** |
| **4096 frames = 5 min 28 s** codec ceiling, both directions, symptom is silence, ~0.61 s rebuild | governed TTS speaks all substance (Option 1) | the **4096 behavioural step** — architectural, not calibration |
| drift verdict **STATE-ARTIFACT at 4096**: not tunable, not co-tenancy, not the codec | the absolute research/governed border | no live full-pipeline run under real co-tenancy |

### One qualification the word PROVEN would otherwise hide

The M0 and drift findings are **research mode** — no REQ, no MET ruling, no
harness run — and their own summary carries `Verification: UNVERIFIED`. The
diagram states this once, prominently: **PROVEN means "measured in the lab",
never "verified by the governed process."** Presenting proposal as built is the
failure mode the honesty rule names; presenting *unverified research* as proven
is the same failure wearing a lab coat.

## A CORRECTION TO THIS DISPATCH'S OWN FRAMING

HA-83 described M0 as *"provisional-pass … Q2 mic pending"*. **That is stale.**
The verdict was `PROVISIONAL-PASS PENDING Q2 MIC` and **was resolved to PASS on
2026-08-14 by Bill's live microphone test** — Q2 is answered
(*"not walkie talkie"*, *"good at finding the semantic end point of my speech"*).
The diagram shows M0 as **PASS** and records why, rather than reproducing the
stale framing.

Also carried in, though the dispatch did not name it: the **drift finding**
(ML-02), whose STATE-ARTIFACT verdict at frame 4096 is one of the **two
constraints M1 inherits** and bears directly on D3's timing.

## VERIFIED

**Watched run:** all four Mermaid blocks extracted and **rendered with
`mermaid-cli`** — D1 26,701 B, D2 19,885 B, D3 32,628 B, D4 21,468 B of SVG.
GitHub-renderability is measured, not inferred from syntax.

**Reasoned about:** every label's basis is a citation to spec v2, the lane
method, or the banked findings — no element is labelled from recollection. Where
a source qualifies its own result (the drift study's decision-variable caveat,
its synthetic stimulus, the weak co-tenancy arm), the diagram carries the
qualification rather than the headline.

## REGISTRATION

* `docs/INDEX.md` — row under `## design/`.
* `docs/deliverables/MANIFEST.md` — **Section B** row, path relative to `docs/`
  per the Section B convention, plus this dispatch's note on the cumulative
  provenance line.
* **Section C CHECKED, NOT ASSUMED: no WP section maps to it.** It is an internal
  diagram of a research-lane direction that amends no plan of record, drawn from
  documents already banked; it introduces no new evidence and makes no product
  claim — the same reasoning HA-66 recorded for its sources. **No Section C row
  is marked NEEDS-UPDATE, and that is a check, not an omission.**

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **Nothing blocking.** The diagram is a reading aid over adopted decisions.
2. Worth knowing: the **5 min 28 s ceiling is accepted for the research lane
   only** and is explicitly **not discharged for the product** — a product claim
   resting on conversations past 5.5 minutes needs seamless or overlapping
   rotation, which is unbuilt and unruled.
3. The **two-voice seam** (D1) is an M1 finding by design; if configuration (b)
   sounds worse than today's (a), that is expected to surface at M1.
