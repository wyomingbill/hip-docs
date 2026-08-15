# REQ_CONFIDENCE_DISCIPLINE: Truth Track
Version: v20260721_0945
Status: NOT MET
Branch: roadmap
Reconciled against: DISPATCH code trace of intent_classifier.py, subject_resolution.py, orchestrator.py, trust.py, voice_orch.py (2026-07-21, this session); REQ_PARTITION_CUSTODY__stage2-ratification (deterministic policy layer this REQ sits above); REQ_TRUTH_TRACK__stage5-fail-open-and-metrics (SUPERSEDED 2026-07-21, folded in below — this doc now carries Stage 5 phases A-G + T02/D-24 in full, Bill-confirmed by phase map); live reproduction of T02 against the dev graph, 2026-07-21 (AMENDMENT below — the real mechanism differs from the fold-in's original assumption)

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

**RETRIEVAL-RELEVANCE is a fourth kind of uncertainty (AMENDMENT, 2026-07-21
— found by live reproduction of T02, see CARRIED FROM REQ_TRUTH_TRACK
below).** The original DESIGN above named three uncertain axes — WHO,
WHAT-WAS-ASKED, WHETHER-TRUE. Live reproduction of T02 surfaced a fourth,
distinct from all three: the query resolves a real subject correctly
(RESOLVED, not AMBIGUOUS), intent classifies correctly (`"personal"`, not
UNCERTAIN), the reader is authorized (INJ-1/INJ-3 both already passed), and
the fact itself is fully known and true — yet the fact still fails to reach
the reader, because the retrieval layer's own relevance check (INJ-2 keyword
match, or SIO exact-attribute-equality) missed. This is not identity
uncertainty, not subject uncertainty, and not fact-truth uncertainty: every
upstream signal was confidently, correctly RESOLVED. The uncertainty lives
entirely inside the retrieval layer's judgment of whether an admitted,
authorized fact is *relevant* to the phrasing used — a structural gap, not a
confidence signal from any stage this REQ already modeled.

The root shape: `CANONICAL_ATTRIBUTES` deliberately splits one underlying
concept across sibling attributes for WRITE-time precision (e.g.
`medication` vs `medication_status` — a status-change event needs its own
narrow attribute so `harness/fact_change.py`'s supersession detection fires
correctly). A READ-time query in ordinary language ("what did I tell you
about Elena's medication?") is semantically relevant to the whole family,
not just the one sibling the fact happens to be filed under — but INJ-2's
keyword pattern and the SIO's exact-attribute-equality check both operate
attribute-by-attribute, with no notion that two attributes are the same
concept split two ways. The result: an authorized, resolved, true fact is
silently dropped into `empty_set` — indistinguishable, from the reply alone,
from a fact that genuinely does not exist.

**The rule:** when subject resolution is RESOLVED, the reader is authorized
(INJ-1/INJ-3 pass), and a fact exists and is true, but INJ-2 relevance
denies solely because the query matched a sibling attribute's form rather
than the fact's own exact attribute — surface the fact via `ATTRIBUTED_HEDGE`
(or, where the fact's own trust level is CONFIRMED/high-corroboration,
`PLAIN_STATEMENT` — the answer-mode is still governed by the fact's own
trust ladder, per the existing enum above; this amendment changes only
whether the fact reaches that decision at all, not which mode it lands in
once it does). It is never treated as `STRUCTURAL_REFUSAL` or `empty_set` —
those remain correct for a fact that is genuinely absent, or a reader who is
genuinely unauthorized. The same principle already governing every other
axis applies unchanged here: authorized + fact-known → surface, never
silently refuse; the axis is new, the fail-closed/fail-open discipline is
not.

This is deliberately the GENERAL fix for the attribute-taxonomy-mismatch
class, not a per-attribute keyword patch: `incident`/`medication_status`
(TD-120/D-21/D-23, 2026-07-17) and `appointment` (PW023-25) were each
independently found and fixed as one-off "this attribute has no keyword
pattern at all" gaps. This amendment names the broader pattern those fixes
were instances of and gives it a standing rule (a declared attribute-family
equivalence, checked structurally) rather than requiring the same
investigation to repeat for the next sibling pair.

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
done where a threshold actually exists. (The concrete calibration
MEASUREMENT task this principle governs is carried from REQ_TRUTH_TRACK
Phase E below — this paragraph states the policy; that section states the
deliverable.)

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

## CARRIED FROM REQ_TRUTH_TRACK (folded in 2026-07-21, per Bill-confirmed phase map)

REQ_TRUTH_TRACK__stage5-fail-open-and-metrics__v20260719_0910 is superseded by
this doc (see that file's own header note). Phases C (G0) and D (decision
table) were already fully covered above and are not repeated. Phase A (fail-
closed routing) is covered above by the CLARIFICATION fallback and Acceptance
Test #2, with one gap noted there (fail-open rate must be GATED, not merely
measured — folded into Phase F's metric #1 below, now explicit). The five
items below had no home in this REQ before this fold-in; they are carried
here verbatim in substance so nothing is dropped on supersession.

### Phase B — SIA (subject-intent-agreement) contradiction check

A named, independent cross-check, distinct from the classifier itself:
`resolved_subjects` naming a tracked household member or care recipient
WHILE `intent == "knowledge"` is a contradiction — this single record state
should never occur, because a query that resolves to a real tracked person
is definitionally not an impersonal knowledge query. SIA asserts this rule
and fires on the contradiction, catching the "What's Ray on?" / "Who was Ray
Charles?" collision from the SUBJECT side, independent of whatever the
classifier itself concluded. This is deliberately a second, independent
check, not a restatement of the classifier's own threshold logic — it
catches the case where the classifier is confidently WRONG, not just
unconfident.

**Baseline (measured, not cited):** SIA fires on 14.3% of turns in the
probe set it was measured against (REQ_TRUTH_TRACK, 2026-07-19). This figure
is a starting measurement, not a target — the acceptance bar is that the
rate is tracked per push and driven down, not that it hits zero on day one.

**Acceptance:** SIA fires on the contradiction; the rate is re-measured
(not re-cited from the 2026-07-19 figure) at each push and trends down.

### Phase E — Calibration measurement (the concrete deliverable)

The DESIGN section above states the calibration PRINCIPLE (calibrate only
where a threshold gates a safety branch, re-measure on model swap). This is
that principle's concrete, required deliverable: measure the intent
classifier's **margin distribution** (top1-top2 cosine score gap across the
route set) as a per-push metric, so the 0.30 `CONFIDENCE_THRESHOLD` cutoff
(`harness/intent_classifier.py:144`) is verified as a principled cutoff
against the actual score distribution, not carried forward as a guessed
constant. A cutoff with no margin-distribution evidence behind it is not
calibrated, regardless of how long it has been in place unquestioned.

**Acceptance:** margin distribution (top1-top2) is measured and reported per
push; the 0.30 cutoff is either confirmed against that distribution or
adjusted with the new value justified by it — never left as an assumption.

### Phase F — The truth metrics (per push; fail-open rate already covered above as Acceptance Test #1 — the remaining six carried here)

The numbers that make truthfulness visible, in the original priority order:

1. ~~FAIL-OPEN RATE~~ — already this REQ's Acceptance Test #1 above. Restated
   here only to preserve the original numbered list's completeness: this
   metric must be GATED (push-blocking above a threshold), not merely
   measured-and-visible — the one gap Phase A/D left open, now made explicit
   as this REQ's own requirement, not just REQ_TRUTH_TRACK's.
2. **THIRD-PARTY PERSONAL RECALL** on a caregiver-shaped probe set — near
   zero today, and the beachhead: a flat red line for the project's history
   until fixed. This is the metric that measures exactly the failure mode
   this REQ exists to close (a caregiver asking about someone else's facts),
   so it is the most direct evidence of whether the REQ's architecture is
   actually working, not just internally consistent.
3. **CORPUS-TO-EXEMPLAR COSINE DISTANCE** (the `{noun}` finding as a number)
   — how far real queries sit from the intent classifier's hand-written
   exemplars, made measurable rather than anecdotal.
4. **ORACLE AGREEMENT RATE** — see Phase G below; this metric's ratchet
   polarity is opposite every other metric here (must not DECREASE, where
   everything else here trends toward a floor or a hard zero).
5. **WITHHELD-OWN-FACT COUNT** — the utility-regression guard: the flip side
   of fail-closed. A system that hedges or withholds a member's OWN facts
   out of excess caution has traded one failure mode for another; this
   metric is the check that fail-closed didn't overshoot into fail-useless.
6. **G0/G1/G4 COUNTS** over the harness's own turn log — how often each
   fabrication-class invariant actually fires in practice, not just whether
   it CAN fire under fault-injection.

**Acceptance:** all six metrics exist, are measured per push, and are
visible together (not scattered across ad hoc scripts) — the third-party
recall number specifically must exist and move off zero, not merely exist
as a static probe set nobody reruns.

### Phase G — The gate bifurcation (full ratchet taxonomy)

Not one ratchet. Three distinct tiers, and this REQ's CONSTRAINTS section
above already states the G0-specific instance of the third tier; the full
taxonomy, carried here so the other two tiers and G1/G4's inclusion are not
lost:

1. **MONOTONIC RATCHET** — structural/negative invariants (the general case:
   a scenario that passed must not regress to failing).
2. **OPPOSITE-POLARITY RATCHET** — exactly one metric runs this direction
   today: oracle-agreement rate (Phase F #4) must not DECREASE. Stated
   separately because a single "never regress" ratchet framing would get
   this backwards if applied uniformly.
3. **HARD ZERO, never baselinable** — on ALL THREE fabrication-class
   invariants, **G0, G1, AND G4** (not G0 alone — this REQ's CONSTRAINTS
   section previously named only G0; G1 and G4 are added here to close that
   gap). `--accept` is refused outright on these three, with no exception
   path. Every OTHER `--accept` (on any invariant outside this fabrication
   class) must carry either an explicit expiry or a linked defect/debt ID —
   a failing positive case must never be baselined into silent permanence
   with a bare justification string.

**Acceptance:** the harness enforces all three tiers distinctly; a fault-
injection test confirms `--accept` is mechanically refused on G0/G1/G4
specifically (not just documented as refused); every existing non-fabrication
`--accept` in the codebase is audited to confirm it carries an expiry or debt
ID, with any that don't flagged as a pre-existing gap to close.

### T02 / D-24 fold-in (backlog #15c) — carried verbatim below; AMENDED 2026-07-21 with the actual root cause

**AMENDMENT (2026-07-21):** live reproduction of T02 (see VERIFIED-style
record in the dispatch that produced this amendment) shows the (a)/(b)
framing below was built on an incorrect assumption — that T02 fails because
"the query classifies wrong." It does not. Live record: `intent: "personal"`
(correct), `resolved_subjects: ["bill", "elena"]` (correct), yet
`path: "guard_empty_set"`, `admitted: []`. Neither the intent classifier nor
subject resolution is wrong or uncertain anywhere in this turn. The actual
mechanism is RETRIEVAL-RELEVANCE (the new DESIGN section above): the fact
was written under `medication_status` (correct, precise, write-time
classification of "switched from metformin to Jardiance"), and T02's
ordinary follow-up ("about Elena's medication") matches the sibling
attribute `medication`'s keyword pattern, not `medication_status`'s narrow
status-change pattern — so INJ-2 denies a fact that is fully authorized,
resolved, and true. Option (a) below (narrow the classifier's trigger
language) would not have fixed this even if built — the classifier was never
the problem. The real fix is the attribute-family relevance rule in
`harness/injection_contract.py` (RETRIEVAL-RELEVANCE, above), not a change
to intent classification at all. The (a)/(b) text and DECISION FOR BILL are
kept below verbatim for the historical record of what REQ_TRUTH_TRACK
originally proposed; they are superseded by this amendment, not merged with
it.

care_coordination T02 is a REAL defect, not test debt: a caregiver asks
about a medication change and gets "I don't have that confirmed yet." when
Jardiance should surface. The fixture asserts on reply content; fixing the
test would delete the assertion that caught it. D-24's two options:

(a) Narrow the classifier's trigger language so the medication-change
    phrasing classifies personal (not knowledge), so the fact is retrieved.
(b) Widen medication-keyed retrieval so the fact surfaces even when
    classification is imperfect.

**RECOMMENDATION (carried from REQ_TRUTH_TRACK):** (a) is the right primary
fix because it is the same root cause as Phase A / this REQ's fail-open
finding — the query classifies wrong and loses its facts. Fixing
classification fixes T02 and the whole class. (b) is a retrieval band-aid
that masks the classifier without fixing it, and widening retrieval risks
surfacing facts the partition should have withheld — it fights the crypto
track (REQ_PARTITION_CUSTODY). Do (a). Keep (b) only as a measured fallback
if (a) cannot reach the phrasing.

**DECISION FOR BILL — SUPERSEDED 2026-07-21, no longer open:** the (a) vs
(b) choice above assumed a classifier-side root cause that live reproduction
disproved. The fix actually shipped is neither (a) nor (b): it is the
attribute-family relevance rule (RETRIEVAL-RELEVANCE, above), which requires
no classifier change and no retrieval-widening band-aid — it closes the
exact gap (a)/(b) were both reaching for, at the layer where the defect
actually lives. Bill confirmed this direction (fold in as an
`ATTRIBUTED_HEDGE`/surface case) live, in-session, 2026-07-21.

## ACCEPTANCE TEST (observable, pass/fail)

1. **Fail-open rate is measured, not invisible, AND gated.** The fraction of
   turns hitting the intent classifier's below-threshold-or-embed-failure
   fallback (`harness/intent_classifier.py:197,211`) is emitted as a
   per-push metric (Phase F #1, above) AND the push gate blocks on it
   exceeding a set ceiling — measurement alone is not sufficient; this closes
   the gap the original wording of this test left open before the Phase A/F
   fold-in above.
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
6. **SIA fires on the contradiction.** (Phase B, folded in.) A turn with a
   resolved tracked-person subject and `intent == "knowledge"` is
   constructed; PASS: SIA flags the contradiction independent of the
   classifier's own confidence. FAIL: the contradictory state passes
   unflagged.
7. **Calibration measurement exists.** (Phase E, folded in.) PASS: margin
   distribution (top1-top2) is measured and reported per push. FAIL: the
   0.30 cutoff remains an unmeasured constant.
8. **The six remaining truth metrics exist and are visible together.**
   (Phase F, folded in.) PASS: third-party personal recall, corpus-cosine
   distance, oracle agreement rate, withheld-own-fact count, and G0/G1/G4
   counts are all measured per push. FAIL: any is missing or ad hoc.
9. **The three-tier ratchet is mechanically enforced.** (Phase G, folded
   in.) PASS: `--accept` is refused by the harness itself (not just by
   policy) on G0, G1, and G4; oracle-agreement rate ratchets in the opposite
   direction from every other monotonic invariant; every other `--accept`
   in the codebase carries an expiry or debt ID. FAIL: any fabrication-class
   invariant can be silenced with a bare `--accept` string.
10. **(AMENDMENT) Retrieval-relevance surfaces, never silently refuses, for
    an authorized resolved subject.** T02 exactly: bill (authorized,
    resolved as subject via first-person + named-entity) asks an ordinary
    medication question; the authorized fact was written under a sibling
    attribute (`medication_status`). PASS: the fact surfaces (Jardiance
    present in the reply, no "I don't have that"/"confirmed yet" refusal
    strings). FAIL: `guard_empty_set`/`admitted: []` for a fact that is
    authorized, resolved, and true. This must hold WITHOUT loosening
    INJ-1/INJ-3: an UNauthorized cross-member query for the same fact
    (a different member asking about someone else's medication with no
    ownership/subject relationship) must still refuse — this amendment
    changes relevance judgment only, never access control.

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
- **The 14.3% SIA baseline measurement.** (Folded from REQ_TRUTH_TRACK
  Phase B.) Measured 2026-07-19 against the probe set described there — a
  real prior measurement, not a re-derivation; carried here as the starting
  point, not re-verified in this fold-in.
- **(AMENDMENT) T02's live-reproduced record, precisely diagnosed.**
  Reproduced 2026-07-21 against the dev graph via `--layer 2 --script
  care_coordination`: `intent: "personal"` (correct), `resolved_subjects:
  ["bill", "elena"]` (correct), `path: "guard_empty_set"`, `admitted: []`.
  Traced to `harness/injection_contract.py:279-311`'s `_inj2_relevance` —
  the SIO exact-attribute-equality path and the keyword-pattern path both
  check the fact's own attribute (`medication_status`) against the query,
  which matches only the sibling `medication` pattern. Confirms the defect
  is retrieval-relevance, not intent/subject classification.

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
  record from a confident one. (This is exactly the collision Phase B's SIA
  check, folded in above, catches from the subject side.)
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
- **SIA (the named contradiction check) does not exist as code.** (Folded
  from REQ_TRUTH_TRACK Phase B.) Only the 2026-07-19 measurement of the
  14.3% baseline exists; no code asserts or enforces the contradiction rule.
- **No margin-distribution calibration measurement exists.** (Folded from
  Phase E.) The 0.30 threshold has never been checked against an actual
  top1-top2 score distribution.
- **Five of the seven truth metrics do not exist.** (Folded from Phase F.)
  Only fail-open rate (partially — measured but not gated) and, arguably,
  ad hoc G0/G1/G4 fault-injection counts (not a per-push metric) have any
  presence today.
- **No mechanically-enforced ratchet taxonomy exists.** (Folded from Phase
  G.) `--accept` today is a free-text justification field
  (`eval/harness.py --accept`); nothing in the harness currently refuses it
  outright on G0/G1/G4, and no opposite-polarity ratchet exists for oracle
  agreement.
- **(AMENDMENT) T02's real defect is retrieval-relevance, and the (a)/(b)
  framing was wrong.** No `UNCERTAIN` intent, no `AMBIGUOUS` subject exists
  anywhere in T02's live-reproduced record — the defect is entirely inside
  `_inj2_relevance`'s attribute-exact-match, which has no notion that
  `medication`/`medication_status` are one concept split for write-time
  precision. Fix status: designed and applied
  (`harness/injection_contract.py` attribute-family relevance, see
  RETRIEVAL-RELEVANCE above); live verification pending as of this
  amendment's commit — see the dispatch that ships alongside it for
  results.

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
- **G0, G1, and G4 must not become optional or config-gated.** (Widened on
  fold-in from G0 alone.) Every other invariant in this system (INJ-7,
  empty-set, fail-private) is mandatory by design; this fabrication-class
  trio is this REQ's version of that, and any build treating any one of the
  three as an opt-in check has not built this REQ.
- **No general calibration subsystem.** Do not build infrastructure to
  calibrate every score in the system preemptively. Calibrate only the
  thresholds that actually gate a safety branch, and only when a model/
  embedding swap makes the existing calibration suspect. The margin-
  distribution measurement (Phase E, folded in) is the one concrete,
  bounded exception — a single measurement task, not a subsystem.
- **Fail-closed must not over-withhold a member's OWN facts.** (Folded from
  REQ_TRUTH_TRACK CONSTRAINTS.) The withheld-own-fact count (Phase F #5)
  guards this directly. Fail-closed applies to THIRD-party uncertainty, not
  to a member asking about themselves.
- **Gate on policy-level stage outputs, not intent equality.** (Folded from
  REQ_TRUTH_TRACK CONSTRAINTS.) Intent is an implementation intermediate,
  tracked as a metric; the answer-mode decision above is already built this
  way (it reads `resolved_subjects`, fact trust state, and guard/path
  outputs, not a bare intent string) — this constraint is stated explicitly
  here so a future build does not regress it by gating on intent directly.
- **T02's fix must not delete the assertion that caught it.** (Folded from
  REQ_TRUTH_TRACK CONSTRAINTS.) The test stays; the system changes.
- **The fabrication-class ratchet (G0/G1/G4) is hard-zero and non-
  baselinable; every other `--accept` requires an expiry or a linked debt
  ID.** (Folded from Phase G, widened per the full taxonomy above.)

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, as a co-equal objective to the policy itself. We do not rig the build for it.

SHOW: Speak a below-threshold personal question about a resolved household member — show it land on CLARIFICATION, not a confident guess. Speak "Who was Ray Charles?" alongside "What's Ray on?" with a household member named Ray enrolled — show the record's subject state distinguishing a genuine household reference from a coincidental name match, not both silently resolving the same way, and show SIA firing on the contradiction independent of the classifier's own read. Show a turn's record on screen, and show the answer-mode field predicting the reply's shape before the model has generated anything. Break something upstream on purpose (force a subject mismatch) and show G0 catch the resulting reply before it reaches the caller. Show the fail-open rate, third-party recall, and the other truth metrics on a dashboard, nonzero, trending in the right direction. Show `--accept` mechanically refused against G0/G1/G4.

LET THEM RUN: Hand the engineer the record schema and the answer-mode enum. Let them construct their own ambiguous utterance, predict which mode it lands in, and run it. Let them try to make a hedge slip into an access grant (ask a question the fact-truth layer is unsure about, phrased so the model might be tempted to just answer plainly for an authorized reader) and watch it come back attributed, not withheld and not overclaimed. Let them try to trigger G0 directly by asking about a specific tracked person's specific unadmitted attribute, and watch it fire. Let them try to `--accept` a G0 failure and watch the harness refuse it outright.

THE CLAIM IT PROVES: "Whether HIP is sure enough to answer plainly, hedge, or ask you back is a rule you can read off a record before generation ever runs — not a hope that the model noticed it was unsure. And no amount of confidence, from any stage, ever grants an access the deterministic policy layer didn't already grant. We measure how often we're unsure, we catch the fabrication class with an invariant that cannot be silenced, and the numbers move in front of you, every push."

THE HARDEST QUESTION + HONEST ANSWER: "Doesn't this mean HIP will annoyingly ask for clarification more often than a system that just guesses, and how many phrasings still fabricate beyond the one you showed me?" Answer, limit stated first: we do not claim zero fabrication anywhere in the system — we claim a MEASURED and FALLING fail-open rate, a hard-zero invariant trio (G0/G1/G4) that catches the fabrication class rather than one phrasing, and more visible "I'm not sure, do you mean—" moments as the deliberate cost of that guarantee. The honest gap: the classifier was trained almost entirely on first-person examples, so third-party caregiver recall starts near zero and is this project's beachhead metric — we show that number and its trend rather than a single passing demo. A system that claimed no fabrication would itself be the fabrication. We claim we measure it, gate the worst class at hard-zero, and it improves every push. And note the separate, narrower limit on G0 itself: it catches the reply-side symptom of every upstream failure, but it is a backstop, not a substitute for fixing the upstream stages — a system that relied on G0 alone, with sloppy upstream typing, would still ask badly and hedge badly even while never leaking. G0 makes leaks impossible; it does not make the system's manners good on its own.
