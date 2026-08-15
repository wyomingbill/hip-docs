# REQ_CONFIDENCE_DISCIPLINE: Truth Track
Version: v20260721_0755
Status: NOT MET
Branch: roadmap
Reconciled against: DISPATCH code trace of intent_classifier.py, subject_resolution.py, orchestrator.py, trust.py, voice_orch.py (2026-07-21, this session); REQ_PARTITION_CUSTODY__stage2-ratification (deterministic policy layer this REQ sits above)

## THE REQUIREMENT

Bill's own words, verbatim:

> Confidence governs whether HIP is ready to decide; policy governs what HIP
> is permitted to do. Confidence may cause abstention, clarification, or
> hedging; it may never create permission.

Expanded: two axes that must never be allowed to substitute for one another.
Confidence (how sure HIP is about what was said, who said it, who was meant,
or whether a claim is true) governs READINESS TO ACT — it can make HIP stop,
ask, or soften a claim. Policy (identity, authorization, scope, retrieval
enforcement, key operations) governs WHAT HIP MAY DO — it is deterministic
and confidence never widens, narrows, or substitutes for it. A low-confidence
signal must never be silently upgraded into an implicit grant, and a
high-confidence signal must never be treated as a permission the deterministic
layer hasn't separately authorized.

## DESIGN (the ratified architecture)

**Two kinds of stage.** Perception stages carry typed uncertainty: intent,
subject resolution, transcription, speaker ID, fact-truth. Policy stages are
deterministic: identity, authorization, scope, retrieval enforcement, key
operations. Nothing in this REQ touches the policy stages' determinism —
see REQ_PARTITION_CUSTODY, which already covers that layer and needs no
confidence signal of any kind.

**Discrete state at the boundary, never a number.** Uncertainty crosses the
perception→policy boundary as a named discrete state, not a raw score. Intent
emits an explicit `UNCERTAIN` class (today it silently emits `"knowledge""`
instead — see WHAT'S KNOWN BROKEN). Subject resolution emits
`RESOLVED` / `AMBIGUOUS` / `NONE` (today it emits only a list, with no
state distinguishing "resolved with confidence" from "resolved by
coincidental token match" — see WHAT'S KNOWN BROKEN). The deterministic
table downstream of each stage has an explicit, conservative row for the
`UNCERTAIN`/`AMBIGUOUS` state — it is not an unhandled default that happens
to fall through to the same place a confident low-risk answer would.

**No unified confidence scalar.** Each stage keeps its own typed uncertainty
in its own vocabulary (a cosine score is not comparable to a transcription
word-confidence or a corroboration count, and forcing them into one number
destroys the information each carries). What unifies them is a single turn
RECORD carrying every stage's discrete state plus its raw score, so
cross-stage invariants (e.g. "no stage claims RESOLVED while its own raw
score sits below its stage's own floor") can be checked without inventing a
fake common unit.

**Propagation is dominance, not averaging.** The most conservative upstream
state wins. A confident-sounding downstream generation is not new evidence
that overrides an upstream AMBIGUOUS or UNCERTAIN state — a model producing a
fluent answer does not retroactively resolve who was asked about or whether
the classifier was sure. Proceed with a direct answer only when every
plausible interpretation of the turn yields the same subject, the same
permission outcome, and the same answer; otherwise the record carries
AMBIGUOUS/UNCERTAIN forward and the downstream stage must clarify rather than
pick one interpretation and run with it.

**Fallback is chosen by WHICH stage is uncertain, not one shared behavior.**
- Uncertain WHO (identity/speaker) → withhold + step-up. Identity uncertainty
  blocks access; it is never softened into a hedge.
- Uncertain WHAT-WAS-ASKED (intent/subject) → clarify. Subject uncertainty
  also blocks access to the ambiguous candidate's facts, same as identity.
- Uncertain WHETHER-TRUE (fact-truth/corroboration) → hedge, for an already-
  authorized reader. This is presentation only — it never blocks access to a
  reader who is otherwise permitted; it changes how the claim is phrased
  (see ATTRIBUTED_HEDGE below).

This is the load-bearing distinction: identity/subject uncertainty is an
ACCESS question and fails closed; fact-truth uncertainty is a PRESENTATION
question for an already-permitted reader and fails soft.

**Answer-mode is selected deterministically from the record, before
generation.** One of a fixed enum, chosen by code reading the upstream
record, not by the model deciding mid-generation:

- `PLAIN_STATEMENT` — subject RESOLVED, fact CONFIRMED/high corroboration,
  reader authorized.
- `ATTRIBUTED_HEDGE` — subject RESOLVED, reader authorized, fact-truth
  uncertain (ASSERTED/UNCONFIRMED/conflicting).
- `CONFLICT_PRESENTATION` — two admitted rows compete for the same
  (subject, attribute) — the D-05/G4 park case already built in
  `server/voice_orch.py:2343-2364` is a working instance of this mode; this
  REQ generalizes it to a named mode in the record rather than a special-cased
  template.
- `CLARIFICATION` — subject AMBIGUOUS or intent UNCERTAIN.
- `STRUCTURAL_REFUSAL` — policy layer denies (existing INJ-7/empty-set
  behavior); this mode is not new, it is named here so the record's mode
  field is exhaustive.
- `ESCALATION` — off-net/frontier turn, governed by the existing disclosure
  contract, named here for record completeness.
- `GENERAL_ANSWER` — genuine knowledge query, no tracked-person subject
  resolved, no personal facts admitted.

The model realizes the WORDING within the chosen mode. It never decides
disclosure, never decides certainty framing, and never picks its own mode.
`PERSONAL_FACT_GROUNDING_GUARD` (`harness/orchestrator.py:80-93`) is the
current closest approximation — a prompt instruction, intent-gated — and
this REQ's acceptance test requires replacing "prompt instruction the model
may ignore" with "mode selected in code before the model is called."

**G0: one mandatory output-side invariant, independent of every upstream
stage.** After generation, before the reply leaves the system: does the
reply name a tracked person while nothing was admitted about them in this
turn's record? If yes, hard-fail regardless of what any upstream stage
believed. This is the backstop for every failure mode above it — a wrong
intent class, a coincidental subject match, a hedge the model ignored — all
converge on the same observable failure (a specific claim about a specific
tracked person that was never authorized), so one check downstream of
everything catches what any single upstream fix might miss. Mandatory, not
optional, not deferred.

**Calibration is scoped, not built as a subsystem.** A numeric threshold is
calibrated only where it gates a genuine safety branch (e.g. the intent
`CONFIDENCE_THRESHOLD` at 0.30, the speaker-ID tier cuts at 0.75/0.50/0.30).
Every such threshold is re-measured on every model or embedding swap — a
threshold tuned against one model's score distribution is not assumed valid
against another's. The deterministic trust ladder (`CONFIRMED` >
`CORROBORATED` > `ASSERTED` > `UNCONFIRMED`/`DERIVED`, `memory_engine/trust.py:27-34`)
needs no calibration — it is an ordinal ranking over discrete write-time
events, not a tuned numeric cutoff. There is no general-purpose calibration
subsystem in this design; calibration work is one narrow task per threshold,
done where a threshold actually exists.

**Voice-specific rules (forward-looking; voice is the intended future
primary input mode):**
- Device-key possession is identity. Voiceprint match is a hint / step-up
  signal only — never sufficient alone to admit a turn as a given member
  (matches the already-built `server/voice_orch.py:1405-1471` demotion of
  speaker_id from gate to hint; this REQ ratifies that design as the
  standing rule rather than a one-off fix).
- Reads may hedge under fact-truth uncertainty (ATTRIBUTED_HEDGE, above).
  Writes must never be minted from uncertainty alone — a write triggered by
  a low-confidence hypothesis must go through an explicit readback-confirm
  step before it is committed, regardless of how fluent the transcript
  looked.
- Slot-level confidence is tracked on critical tokens (medication names,
  doses, dates, numbers) distinctly from utterance-level transcription
  confidence — an overall-confident transcript can still carry one
  low-confidence critical slot, and that slot's uncertainty must propagate
  even when the sentence around it sounds clean.
- Subject resolution for voice is case-independent (voice has no
  capitalization signal) — the current text-only heuristic
  (`_extract_named_entities`, `harness/subject_resolution.py:152-166`, which
  relies on capitalized tokens) is not portable to voice as-is and needs a
  distinct resolution path before voice becomes primary, not a reuse of the
  capitalization heuristic against a lowercased transcript.
- Generation is gated on transcript-final + full this-turn context — no
  answer is generated against a partial/interim transcript, and no slot's
  confidence is judged against anything other than this turn's own audio and
  context (not carried over from a prior turn's resolved state, matching the
  dominance rule above: an old resolved state is not evidence for a new
  turn's uncertain slot).

## ACCEPTANCE TEST (observable, pass/fail)

1. **Fail-open rate is measured, not invisible.** The fraction of turns
   hitting the intent classifier's below-threshold-or-embed-failure fallback
   (`harness/intent_classifier.py:197,211`) is emitted as a per-push metric.
   PASS requires the metric exists and is visible in harness output; FAIL is
   silence (the rate exists today but is not measured or reported anywhere).
2. **A below-threshold personal query with a resolved subject does not
   proceed as knowledge.** Construct a query that (a) the intent classifier
   scores below `CONFIDENCE_THRESHOLD` (or for which embedding fails) AND
   (b) `resolve_subject()` returns a non-empty, correctly-resolved household
   subject. PASS: the turn routes to `CLARIFICATION` or a withhold, never to
   unconstrained `GENERAL_ANSWER` generation. FAIL: the turn reaches
   generation with no grounding guard and no clarification, as it does today
   per the confirmed trace at `intent_classifier.py:211` →
   `router.py:753-754` fallthrough → `orchestrator.py:406` guard not applied.
3. **G0 fires hard-zero.** Construct a reply (by any upstream path, including
   a deliberately broken one) that names a tracked person while the turn's
   record shows nothing admitted about that person. PASS: G0 blocks the
   reply before it is returned, unconditionally. FAIL: any such reply reaches
   the caller.
4. **Answer-mode is derivable from the record alone.** Given a completed
   turn record (pre-generation), a second, independent process can compute
   the same answer-mode the system chose, using only the record's fields —
   no generation-time text needs to be inspected to know which of the seven
   modes applies. PASS: mode is a pure function of the record. FAIL: the
   mode can only be inferred after reading what the model actually said.
5. **(Voice) no medication write is minted from a single low-confidence
   hypothesis.** Feed a voice turn asserting a medication change where the
   critical-token (drug name or dose) slot confidence is below its floor.
   PASS: the system forces a readback-confirm before any write lands. FAIL:
   a write lands from the single low-confidence pass with no confirm step.

## WHAT'S ALREADY DONE

- **Intent classification computes a real score and has a real threshold.**
  `harness/intent_classifier.py:190-212` (cosine similarity, `:144`
  `CONFIDENCE_THRESHOLD = 0.30`). Verified by direct code read, 2026-07-21.
- **Subject resolution's empty-set fail-safe.** `harness/subject_resolution.py:281-285`
  — unresolvable → `[]`, never wrong-inject. This is the one piece of the
  discrete-state model already correctly built (a `NONE` state, in this
  REQ's vocabulary); `RESOLVED` vs `AMBIGUOUS` is not yet distinguished (see
  below).
- **The D-05/G4 double-valued-park template gate.** `server/voice_orch.py:2343-2364`
  — a working, already-built instance of deterministic, non-model-mediated
  answer construction for one specific conflict case. This REQ generalizes
  the pattern (CONFLICT_PRESENTATION as a named mode) rather than replacing
  working code.
- **Speaker-ID demoted from gate to hint.** `server/voice_orch.py:1405-1471`
  (REQ_IDENTITY_BINDING_BUILD step 4) — identity is authoritative from the
  verified session, speaker_id is logged only. This REQ's voice section
  ratifies this as the standing architecture, not a special case.
- **Deterministic write-time trust ladder.** `memory_engine/trust.py:27-34`,
  ordinal `CONFIRMED > CORROBORATED > ASSERTED > UNCONFIRMED/DERIVED`,
  already governs write monotonicity (`harness/fact_change.py`).
- **The policy layer this REQ sits above is already specified.**
  `REQ_PARTITION_CUSTODY__stage2-ratification` — deterministic partition,
  write-rule precedence, no confidence input anywhere in that layer. This
  REQ does not touch it or duplicate it.

## WHAT'S KNOWN BROKEN

- **Intent fails open to unconstrained generation.** Below-threshold
  (`intent_classifier.py:210-211`) and embed-failure (`:196-197`) both
  collapse to `("knowledge", ...)` — `best_route` is even initialized to
  `"knowledge"` at `:201`. Downstream, `router.py:753-754` sends this
  straight through the normal knowledge-query complexity/tier path, and
  `orchestrator.py:406`'s grounding guard is gated on `intent == "personal"`
  exactly, so a low-confidence personal question gets neither a
  clarification nor the anti-confabulation guard. There is no `UNCERTAIN`
  state anywhere in this path today.
- **Subject resolution is unscored and ungated, and over-matches.**
  `harness/subject_resolution.py:273-275` does a binary token-in-known-set
  match with no confidence and no context disambiguation. Confirmed
  concretely: "Who was Ray Charles?" and "What's Ray on?" both extract
  `"ray"` as a candidate and both resolve to the same household subject if
  `"ray"` is a known subject — capitalization is the only signal, nothing
  distinguishes a knowledge-query mention of a name from a personal-fact
  reference to a household member sharing it. No `RESOLVED`/`AMBIGUOUS`
  distinction exists; a coincidental match is indistinguishable in the
  record from a confident one.
- **Write-time trust labels do not reach the generation-time hedge
  decision.** `memory_engine/trust.py:27-34` and `harness/fact_change.py`'s
  use of them govern whether a write supersedes another write. Nothing
  carries that same CONFIRMED/ASSERTED/UNCONFIRMED distinction into a
  generation-time answer-mode decision — the only generation-time gate today
  is the prompt-instruction guard at `orchestrator.py:80-93,406`, which the
  model can ignore and which the intent-gating bug above can skip entirely.
- **No deterministic answer-mode selection exists.** There is no enum, no
  pre-generation mode decision. The model is asked to follow a prompt rule;
  disclosure and certainty framing are effectively decided inside
  generation, not before it, except for the one hand-built exception
  (`voice_orch.py:2343-2364`'s park template).
- **G0 does not exist.** No output-side check independent of upstream stages
  currently runs against "does this reply name a tracked person with nothing
  admitted about them." This is the single highest-leverage gap: every other
  gap above is a way to reach exactly this failure, and none of them are
  individually guaranteed to be found and fixed first.
- **Voice slot-level confidence and case-independent subject resolution do
  not exist.** `harness/speaker_id.py` produces a tiered utterance-level
  score; nothing tracks confidence per critical token (medication name,
  dose). `harness/subject_resolution.py`'s named-entity phase relies on
  capitalization (`:152-166`), which has no voice equivalent.

## CONSTRAINTS

- **This REQ changes no code.** It is policy/architecture, same as
  REQ_PARTITION_CUSTODY at this stage. Nothing here authorizes a build
  session to start; a separate REQ (or a Bill instruction naming this one as
  prerequisite) starts Stage work.
- **Never let confidence become permission, in either direction.** A build
  against this REQ must not let a high intent/subject/speaker score bypass
  or soften any deterministic policy check (identity, authorization, scope,
  retrieval enforcement, key ops) — REQ_PARTITION_CUSTODY's determinism is
  sacred and this REQ sits strictly above it, never inside it.
- **Fact-truth hedging must never become an access decision.** ATTRIBUTED_HEDGE
  softens wording for an already-authorized reader; it must never be used as
  a substitute for withholding from an unauthorized one. Confusing "I'm not
  certain this is true" with "you may not see this" collapses the
  identity/subject-uncertainty (access) and fact-truth-uncertainty
  (presentation) tracks this REQ deliberately keeps separate.
- **G0 must not become optional or config-gated.** Every other invariant in
  this system (INJ-7, empty-set, fail-private) is mandatory by design; G0
  is this REQ's version of that and any build treating it as an
  opt-in check has not built this REQ.
- **No general calibration subsystem.** Do not build infrastructure to
  calibrate every score in the system preemptively. Calibrate only the
  thresholds that actually gate a safety branch, and only when a model/
  embedding swap makes the existing calibration suspect.

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, as a co-equal objective to the policy itself. We do not rig the build for it.

SHOW: Speak a below-threshold personal question about a resolved household member — show it land on CLARIFICATION, not a confident guess. Speak "Who was Ray Charles?" alongside "What's Ray on?" with a household member named Ray enrolled — show the record's subject state distinguishing a genuine household reference from a coincidental name match, not both silently resolving the same way. Show a turn's record on screen, and show the answer-mode field predicting the reply's shape before the model has generated anything. Break something upstream on purpose (force a subject mismatch) and show G0 catch the resulting reply before it reaches the caller.

LET THEM RUN: Hand the engineer the record schema and the answer-mode enum. Let them construct their own ambiguous utterance, predict which mode it lands in, and run it. Let them try to make a hedge slip into an access grant (ask a question the fact-truth layer is unsure about, phrased so the model might be tempted to just answer plainly for an authorized reader) and watch it come back attributed, not withheld and not overclaimed. Let them try to trigger G0 directly by asking about a specific tracked person's specific unadmitted attribute, and watch it fire.

THE CLAIM IT PROVES: "Whether HIP is sure enough to answer plainly, hedge, or ask you back is a rule you can read off a record before generation ever runs — not a hope that the model noticed it was unsure. And no amount of confidence, from any stage, ever grants an access the deterministic policy layer didn't already grant."

THE HARDEST QUESTION + HONEST ANSWER: "Doesn't this mean HIP will annoyingly ask for clarification more often than a system that just guesses?" Answer: yes, deliberately — the alternative is the system we just found broken: a below-threshold personal question about a real household member silently answered as if it were a stranger's trivia question, with no signal to the user that anything was uncertain. The cost of this REQ is more visible "I'm not sure, do you mean—" moments; the cost of not having it is a system that is wrong in exactly the cases where it was least sure and gave no indication of that. And note the honest limit: G0 catches the reply-side symptom of every upstream failure, but it is a backstop, not a substitute for fixing the upstream stages — a system that relied on G0 alone, with sloppy upstream typing, would still ask badly and hedge badly even while never leaking. G0 makes leaks impossible; it does not make the system's manners good on its own.
