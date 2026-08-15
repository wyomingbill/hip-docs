# REQ_DEMO_WEB_REPLAY — remote voice demo surface

Status: FILED — acceptance NOT run
Version: v20260801_0732 (Mountain Time, per the CLAUDE.md Naming Law)
Filed: 2026-08-01 (D-80)
Ruled-By: Bill, 2026-08-01 (v1 cut line; mode-2 gate; bundle deferral; R1 CLEARED and R3 N/A per this filing)
Reconciled-Against: roadmap `d7322d7` (verified by reading HEAD at filing time, not a remembered hash)
Component: SCRIPTED/DEMO (per the 2026-07-31 component ruling). One clause binds the
VOICE component's contract (R2). Nothing here lands on HIP core.
Related: REQ_VOICE_COMPONENT (NOT MET), TD-101 (SEC, OPEN), TD-030, D-1 record contract,
REQ_CEILING_ACCEPTANCE (tier vocabulary reused here)
Sources: D-78 recon (Fable, four-tree read-only) —
`docs/reviews/FABLE_D78_web-replay-recon__feasibility-across-four-trees__v20260801_0732.md`,
banked D-80; and the ChatGPT remote-voice-demo research pass —
`docs/reviews/CHATGPT_D78_remote-voice-demo__two-mode-replay-and-live-challenge__v20260801_1438.md`,
**banked D-91.** Both are now in docs/reviews/. NOTE (D-91): at filing this line claimed
both were already banked; only the first was. D-80 flagged it rather than softening it,
and D-91 closed it by banking the actual artifact, so the claim is true as written

---

## 1. WHY THIS EXISTS

All demos are remote. Video-call screen-share audio cannot carry TTS quality or
interaction feel, so the viewer must hear the voice through their own browser. The
web surface is therefore the PRIMARY demo surface, not an async leave-behind.

Both research passes converged: a precisely labeled captured execution, backed by
real artifacts, followed later by one narrow presenter-driven live challenge, is
more credible than a fragile fully-live voice performance. The replay is not the
credibility problem. Unbounded claims are.

**CONTROL RULE:** the surface never claims more than it demonstrates. Every mode
states what it is, on screen, at all times.

---

## 2. SCOPE — THREE MODES, TWO IN, ONE OUT

- **Mode 1 — REPLAY (v1).** Captured traces of real governed runs: transcript, pane
  states, tier signals, per-turn TTS audio. Viewer-paced or call-paced with the
  presenter narrating.
- **Mode 1.5 — PRESENTER-SPOKEN, TEXT-RENDERED (v1, the working mode).** The
  presenter speaks on the call; their voice feeds the mini's real voice path — VAD,
  STT, speaker verification, governed turn. The transcript renders on the shared
  surface as it resolves, panes light, the reply renders as TEXT. The viewer HEARS
  the presenter through the call and READS HIP's reply. No audio is streamed to the
  viewer. HIP's voice is heard from the captured set (R15b), not from this turn.
  This is the mode most calls will use. See section 4A.
- **Mode 2 — PRESENTER-DRIVEN LIVE CHALLENGE (v1.5, gated).** Viewer puts a question
  in call chat; presenter submits it VERBATIM; the received string is displayed
  before execution; policy events render live; the generated audio file plays in
  the viewer's browser. No streamed audio. No WebRTC.
- **OUT OF SCOPE — viewer-typed and viewer-spoken input.** Bounded claim, stated on
  the surface and in the VO: *"This demonstrates governance execution after intent
  is resolved. It is not an evaluation of arbitrary-language classification
  robustness."* The classifier is evaluated separately (R12). The phrasing-fragility
  finding is disclosed as a known limit, not hidden as a demo convenience.

---

## 3. GATES — WHAT MUST CLEAR BEFORE ANYTHING SHIPS

### R1 — LICENSING — **CLEARED (D-79, 2026-08-01). No longer gates v1.**
The requirement as written: the Kokoro model and voice-pack licenses SHALL be identified
and recorded before any generated audio is served to a third party. No LICENSE file sits
beside the model artifacts; serving audio is a distribution step the local demo never took.
If the voice packs carried terms incompatible with third-party distribution, v1 would be
blocked until a compliant voice was substituted.

**Resolved. Evidence banked at
`docs/reviews/FABLE_D79_kokoro-licensing__three-licenses-and-watermark__v20260801_0732.md`.**
Three licenses established separately, because they are not the same:

- **`kokoro-onnx` package v0.4.7 — MIT.** Verified locally against the actual LICENSE file
  at `dist-info/licenses/LICENSE` ("Copyright (c) 2025 github.com/thewh1teagle"). Note the
  package METADATA carries no `License:` field and no classifier, which is why the D-78
  recon could not resolve it and correctly refused to call it green. Covers the wrapper
  only, not the weights.
- **Model weights `kokoro-v1.0.onnx` — Apache 2.0**, per Kokoro-82M (hexgrad).
- **Voice packs `voices-v1.0.bin` — Apache 2.0** as part of Kokoro-82M, **not separately
  licensed**. The file is a zip of 54 per-voice NumPy style embeddings with no LICENSE or
  README member; 54 matches Kokoro-82M's published voice count exactly, and the local
  prefix breakdown matches. There is no separate voice license to find. Configured voice
  here is `af_heart`.

**NOT verifiable from the artifacts themselves, and recorded as such.** The ONNX header
carries producer `pytorch 2.6.0` and no embedded license, doc_string, or NOTICE; there is
no LICENSE file beside either artifact. The weights-and-voices license rests on upstream
publication, not on anything shipped with the bytes on this machine.

**Serving generated audio to third parties: PERMITTED.** Apache 2.0 has no field-of-use
restriction and no clause governing model output. Serving pre-generated per-turn audio to
a gated remote viewer is unrestricted by these licenses.

**Attribution: not required for audio-only output; recommended anyway.** Audio output is
not a derivative work of the licensed code or weights, so Apache 2.0 §4's obligations do
not attach to serving it. They DO attach if the model, voice packs, or package source ever
ship inside a deliverable. **A colophon credit — "Speech synthesized with Kokoro-82M
(Apache 2.0)" — SHALL appear on the replay surface**: it costs nothing, it is accurate, and
it pre-empts the provenance question in a diligence setting.

**Watermark: NONE, verified two ways.** (i) The installed `kokoro_onnx` package source
contains zero matches for `watermark`, `perth`, or `resemble`, and the synthesis path has
no post-processing stage where one could be applied; (ii) none documented upstream. The
"can it be disabled" question is therefore moot. This is the opposite of the Chatterbox
evaluation already on record (`hip-vo/docs/INDEX.md:212`), which CONFIRMED a PerTh
watermark at score 1.0 with no API off-switch.

**TWO CAVEATS CARRIED FORWARD — neither gates v1, both belong on the record:**

1. **The dependency chain is GPL even though the package is MIT.** `kokoro-onnx` requires
   `phonemizer-fork==3.3.1`, verified locally as **GPLv3+**, plus `espeakng-loader`
   (espeak-ng is GPLv3). This does not reach generated audio — GPL governs distribution of
   *software*, and audio output is not a derivative work of the phonemizer. It **would**
   matter if HIP ever ships the synthesis stack as part of a product. Recorded because "the
   TTS is MIT" is the natural shorthand and it is incomplete.
2. **Upstream training data included synthetic audio generated by closed TTS models from
   large providers**, alongside public-domain and permissively-licensed audio. That is
   **hexgrad's provenance risk, not HIP's**, and Apache 2.0 does not indemnify it. It is a
   known open question about Kokoro's lineage rather than a defect found here — but it is
   the question a diligence conversation asks, and "Apache 2.0" is not a complete answer to
   it.

### R2 — TRACE CAPTURE ENTERS THE VOICE CONTRACT (gates v1; binds VOICE)
The voice component SHALL retain per-turn TTS audio keyed to the turn record, as a
contract obligation, before the voice contract freezes.
- Capture hooks at synthesize_sentences(); per-turn encode (WAV via stdlib for v1);
  artifact at logs/turn_audio/<turn_id>.
- The record carries a REFERENCE (opaque id or content hash), NEVER audio bytes.
  The record is a pure projection (no I/O) and TD-030 bars values from logs; audio
  of a spoken reply is value-bearing by definition.
- The reference is permanent (the record dual-writes to the append-only ledger);
  the audio artifact is separately deletable. A dangling reference is a VALID state
  the replay surface SHALL tolerate and display honestly ("audio removed").
  This matches the chain-retained / payload-erasable shape and is deliberate.
- The L7 record-invariant checks SHALL be amended to accept the new field. If that
  amendment requires its own REQ under the D-1 contract's discipline, that REQ is
  filed BEFORE capture lands, not after.

### R3 — DEMO PRIVACY — **N/A (Bill's ruling, 2026-08-01). Not a gate today.**

**Ruling: `bill` / `maya` / `sam` are SYNTHETIC FIXTURES.** They are not real household
members and the graph holds no real personal data. The premise the requirement was drafted
against — "the current demo graph is real-shaped bill/maya/sam data" — is true as to
*shape* and false as to *provenance*. There is therefore nothing to substitute and no
capture to block, and R3 does not gate v1.

**The requirement STANDS as a standing constraint on any future fixture**, and is retained
here in full rather than deleted, because the moment a real household seeds a demo graph it
binds again without needing to be re-derived:

> Nothing served or downloadable SHALL contain real household facts or real relatives'
> voices. Before capture:
> - a SYNTHETIC demo household is seeded for captured runs (names, facts, and voices
>   disclosed as synthetic on the surface), OR
> - Bill explicitly rules the existing fixture acceptable for gated viewing with no
>   downloadable record, and that ruling is recorded here.
>
> No production credentials, no real personal data, in anything that leaves the mini.

**What N/A does and does not mean.** It means the *current* fixture triggers no privacy
gate. It does **not** retire the constraint, and it does **not** reach the second clause
above — "no production credentials, no real personal data, in anything that leaves the
mini" — which remains unconditionally in force regardless of fixture status, because it
governs the deployment rather than the data.

### R4 — MODE 2 GATE (gates v1.5, not v1)
Mode 2 SHALL NOT be built until ALL of:
- TD-101 closed: every dashboard endpoint authenticated, POST /api/demo/next first.
- A single-path, single-method allow-list proxy on a SEPARATE ORIGIN. Never a
  reverse proxy to the dashboard origin — co-residency exposes /api/facts,
  /api/decrypt, /api/members, and the graph-delete path.
- REQ_VOICE_COMPONENT's open rulings resolved or explicitly waived for this surface.
- A latency ruling: measured TTS first-byte is 1.3-3.5s with ~7.6-10.3s stack-up.
  Bill rules whether that demos acceptably over WAN before the proxy is built.

---

## 4. THE REPLAY SURFACE (v1)

### R5 — HONEST LABELING
Every replay screen SHALL carry a persistent badge:
  CAPTURED EXECUTION — not currently live
  Run: <run_id>   Build: <git_commit>   Captured: <UTC timestamp>
The surface SHALL NOT use the word "falsifiable." The defensible claim, used
verbatim where a claim is made: "tamper-evident captured execution."

### R6 — RENDERED FROM THE TRACE
Panes SHALL render from the captured trace via the same JSON shapes the live
dashboard consumes (/api/turns, /api/routing). A read-only trace server feeds the
existing frontend. No pane content may be authored for the replay; if it is not in
the trace, it is not on the screen.

### R7 — THE VAULT SNAPSHOT
The trace SHALL include a per-turn snapshot of the /api/facts response (metadata
only, never ciphertext, per that endpoint's own rule). Vault state SHALL NOT be
reconstructed from deltas: the delta projection is value-stripped, does not
represent retracts, and has already failed once as a reconstruction source (D-41).

### R8 — STRUCTURED DENIALS
Where a captured turn shows a refusal, the inspectable record SHALL show the
structured basis — requester, subject, attribute, scope, guard identifier, result —
not a colored badge. A denial the viewer cannot trace to a rule is decoration.

### R9 — THE RUN SET
The v1 scenario set SHALL include at least one run that is not cosmetically
perfect (a slow turn, an awkwardly worded structural refusal, a routing fallback),
clearly labeled as deliberately included. An all-flawless gallery reads as
manufactured. The 3-script set plus one imperfect run is the v1 floor; the full
aggregate run-matrix (allowed/denied/ambiguous/conflict/failure counts) is
DEFERRED to v2 with the evidence bundles.

### R10 — ACCESS
Gating SHALL be an expiring unlisted link or short access code on the existing
Edge Middleware pattern. No account registration, no email verification in the
meeting path. Links are single-audience; forwarding is a deliberate re-issue, not
a default.

### R11 — PREFLIGHT
A preflight page SHALL verify, before the meeting: audio playback, control
channel, supported browser, and headphone acknowledgment, and SHALL display the
demo version. Corporate-browser realities (autoplay disabled, embedded email
browsers, UDP blocked) are the design case, not the edge case.

---

## 4A. MODE 1.5 — PRESENTER-SPOKEN, TEXT-RENDERED (v1)

The presenter's own speech is the live input. This is a genuine governed execution
on the real voice path, not a text demo in voice framing: VAD, STT, and speaker
verification all fire, and the turn record is a real d1.1 record. What it withholds
is reply AUDIO to the viewer, which is what makes it shippable without R4.

### R15 — WHAT THE VIEWER RECEIVES
The shared surface SHALL render, live: the resolved transcript of the presenter's
utterance, the resolved speaker identity, the pane states, and the reply TEXT.
The surface SHALL NOT stream reply audio in this mode.
- **R15a — the on-screen statement.** Persistent, in place of the CAPTURED
  EXECUTION badge: *"LIVE EXECUTION — reply shown as text. HIP's spoken voice is in
  the captured runs."* The mode SHALL never be ambiguous with Mode 1.
- **R15b — the voice hand-off.** The scenario being executed live SHALL have a
  corresponding captured run in the v1 set, so the presenter can play the same
  scenario's audio immediately before or after. This is how the viewer hears HIP
  without any streaming.
- **R15c — reply-audio delivery is a SUB-OPTION, gated on R4.** Serving this turn's
  generated audio to the viewer's browser is deferred with Mode 2 and inherits the
  same gate. Mode 1.5 v1 ships text-only.

### R16 — HONEST TIMING
The surface SHALL display the turn's elapsed time and its components as they land
(STT, governed decision, generation). Dead air on a call is the dominant experience
cost — measured stack-up is 7.6-10.3s and STT adds to it. Showing where the time
goes converts a silence into an instrument. It SHALL NOT be hidden behind a spinner.

### R17 — THE FRAGILITY DISCLOSURE APPLIES HERE TOO
The presenter speaking does not make the input arbitrary — the presenter knows the
phrasings that land. The surface SHALL carry the same bounded claim as R12, and the
VO SHALL NOT imply that presenter-spoken input demonstrates language-understanding
robustness. If a spoken turn misclassifies live, the correct response is to show it,
not to re-phrase silently.

## 5. THE LIVE CHALLENGE (v1.5, behind R4)

### R12 — BOUNDED CLAIM, SEPARATED EVALUATIONS
The live mode's on-screen statement, verbatim or equivalent: *"The execution is
live. Audio playback begins after the TTS file is complete; this mode demonstrates
governed execution, not full-duplex conversational latency."* Language-understanding
robustness is evaluated separately via a published classifier test matrix; the demo
surface links to it rather than claiming it.

### R13 — VERBATIM SUBMISSION
The viewer's question arrives via call chat; the surface displays the received
string BEFORE execution; the presenter submits it unmodified. If intent
classification is ambiguous, the system SHALL show UNRESOLVED or ask for
clarification — never silently force a prepared interpretation.

### R14 — GRACEFUL FALLBACK
The same surface SHALL offer "Live connection unavailable — continue with captured
execution," same scenario, same visual structure. No tab-switching, no apology
theater.

---

## 6. CLAIMS DISCIPLINE — WHAT THIS SURFACE NEVER SAYS

The surface, the VO, and any leave-behind SHALL NOT claim:
- that a signed record proves the claim true (a signature proves the record is
  what was captured and unmodified — SCITT's own distinction);
- that one captured run proves robustness;
- that a live run cannot be cherry-picked;
- that the demonstration is fully falsifiable;
- that presenter-entered questions are equivalent to viewer-controlled interaction;
- that voice quality is the differentiator. The demonstrated claim is that THE
  RECORD CORRESPONDS TO WHAT WAS HEARD.

---

## 7. DEFERRED (v2, on demand — not built until someone asks)

- Signed evidence bundles (manifest + hashes + verify.sh, RFC 8785 canonical JSON).
- The aggregate run matrix with pass/fail counts.
- The downloadable leave-behind package (replay URL + scenarios + bundles +
  architecture diagram + known limitations + test-matrix results).
The bundle DESIGN from the research pass is recorded in the banked review and is
the spec when v2 opens. Nothing in v1 forecloses it: the trace format SHALL keep
per-artifact hashes computable (stable serialization, one file per artifact) so
bundles are an export step, not a re-capture.

---

## 8. SEQUENCING

Nothing here displaces the ceiling sprint. Order:
1. R1 licensing check (now — it is a reading task, not a build).
2. R2 trace capture (the one deadline-shaped item: enters the voice contract
   before it freezes). 2-3 dispatch-days.
3. Sprint closes (R18 landed, A18 flipped, rows wired).
4. R3 privacy ruling + synthetic fixture if ruled.
5. v1 replay server + surface (4-6 dispatch-days).
6. R4 gate work, then v1.5.

## 9. ACCEPTANCE (proposed, not run — tier vocabulary per REQ_CEILING_ACCEPTANCE)

| ID | Check | Tier at filing |
|---|---|---|
| W1 | A captured run replays end-to-end with per-turn audio in a clean browser profile with autoplay disabled until user gesture | UNWRITABLE until R2 lands, then LIVE |
| W2 | Every replay screen shows the CAPTURED EXECUTION badge with run/build/timestamp | LIVE at v1 |
| W3 | Pane content diffs empty against trace content (no authored panes) | LIVE at v1 |
| W4 | Vault pane at turn N matches the turn-N snapshot, including after a supersede | UNWRITABLE until R7, then LIVE |
| W5 | A deleted audio artifact renders as "audio removed," never as an error or a silent skip | XFAIL at capture, LIVE at v1 |
| W6 | A denial turn exposes requester/subject/attribute/scope/guard/result | LIVE at v1 |
| W7 | The run set contains >= 1 labeled imperfect run | LIVE at v1 |
| W8 | No real household fact or real voice in any served or downloadable artifact | LIVE at v1, gates release |
| W9 | Expired link yields no content and no trace listing | LIVE at v1 |
| W10 | Mode-2 proxy reaches exactly one path and one method; every other dashboard endpoint unreachable from the public origin | UNWRITABLE until R4 |
| W11 | A presenter-spoken turn renders transcript, resolved speaker, panes and reply text on the shared surface, and streams no audio | UNWRITABLE until the surface exists, then LIVE |
| W12 | Mode 1.5 shows the LIVE EXECUTION statement and cannot be confused with a captured screen; switching modes changes the badge | LIVE at v1 |
| W13 | Every live-executed scenario has a matching captured run in the v1 set | LIVE at v1 |
| W14 | Turn timing components render as they land; no component is hidden behind an indeterminate spinner | LIVE at v1 |

---

## 10. WHAT THIS REQ DOES NOT DO

- Does not build viewer-typed or viewer-spoken interaction.
- Does not stream live audio.
- Does not ship evidence bundles in v1.
- Does not touch HIP core, the graph write path, or the governance modules.
- Does not resolve REQ_VOICE_COMPONENT's open rulings; it names R4's dependency
  on them.
