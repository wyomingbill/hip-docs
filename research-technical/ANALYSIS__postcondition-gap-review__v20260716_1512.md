# ANALYSIS: The postcondition gap — Fable review
Status: BUILT
Reconciled-Against: working tree at 420eb8a + uncommitted D-05 template edits, 2026-07-16

Review of: "The postcondition gap" (Sonnet, v20260716_1500 MT)
Method: every load-bearing claim checked against the code, not the prose. A
full-codebase sweep for any existing runtime output-side check was run before
this review was written, because the document's last theory died on exactly
that omission.

---

## VERDICT IN ONE PARAGRAPH

The central factual claim is **verified**: no production code path inspects
the model's reply against the record after inference. But the document's one
claimed example of an existing postcondition — G1 — is not a postcondition:
`g1_no_orphan_generation` never reads the reply text, and every input it does
read is in scope *before* the model call. The check the document actually
proposes (scan the reply for roster names) is **G0**, which already exists in
this repo as an unbuilt spec — HarnessPlan Phase 3.3, item "not optional,"
sitting in the document's own citation chain — and the document never names
it. So §8's last fear is realized, in the mild form: not a shadow
implementation this time, a shadow spec. The thesis survives in a corrected,
stronger form: the useful boundary is not precondition/postcondition (time of
check) but **question-keyed vs outcome-state-keyed** gates, and three of the
document's four defects close with outcome-state gates at an exit point the
codebase already has — no reply parsing, no wasted tokens, one of them a
one-condition change.

---

## 1. WHAT SURVIVED VERIFICATION

**1a. "Nothing governs what leaves the model" — TRUE, verified by sweep.**
The only post-inference reply manipulations at runtime are
`_gate_unconfirmed_update` (voice_orch.py:2276-2305, called at :3031) and the
`_ctrl_prepend` string. Neither reads reply content; the gate keys off the
popped write-detection outcome and substitutes a template wholesale.
`_gate_double_valued_park_query` (voice_orch.py:2238-2273) fires *before* the
model call. `g1_no_orphan_generation` is invoked only from `eval/harness.py`
Layer 6 over log files; no import of `record_invariants` exists anywhere in
`server/` or `harness/` runtime code. `reply_source` is set at two emit sites
(:3101, :2895) and consumed only by offline G4. On the realtime voice path,
`response.done` arrives *after* the audio has streamed
(harness/realtime_adapter.py:503-513) — the reply is logged, never gated.

**1b. "Fix D-01 completely and the atorvastatin reply still ships" — TRUE,
and the code makes it vivid.** At the emit site, `delta` from the popped
detection outcome is passed into the record (voice_orch.py:3097) and the
reply is returned two lines later (:3103) with no branch between them. The
system holds the evidence of the silent write failure in its hand, writes it
down, and speaks the false ack anyway. No classifier fix touches that.

**1c. The four-defects-one-shape grouping is genuine**, and the blast-radius
asymmetry (disclosure side clean, every defect on the generation side) matches
the register.

**1d. The capitalization gap is real** — `_extract_named_entities` requires
`token[0].isupper()` (harness/subject_resolution.py:162). Phases 1-2 are
case-insensitive regex, but they are English-only and first-person/relational,
so a lowercase third-party name resolves nothing.

---

## 2. WHAT BROKE — TAKING §8'S INVITATIONS IN ORDER

### 2a. "Is G1 a postcondition, or a precondition in a wig?" — A WIG. DEFINITIVE.

`g1_no_orphan_generation` (eval/oracle/record_invariants.py:59-81) reads
`path`, `resolved_subjects`, `delta`, `inj2_declarative_override`, and
`admitted`. It touches `r["reply"]` exactly once — in the *print* statement of
the runner (:226), for humans. Every one of its inputs is input-side or
write-outcome state, and all of it is in scope at voice_orch.py:3087-3101
before `return reply` — on Seam-A declarative turns, before the model call.

Three consequences:

1. **§4 property 1 ("It looks at the output") is false.** G1 looks at the
   same governance state the preconditions look at, evaluated later.
2. **§4 property 2 ("It never needs to understand the question") is false.**
   `resolved_subjects` IS question understanding — the same subject
   resolution whose fragility §3 documents. The register's own I-06 says it:
   a fabrication with `subjects=[]` passes all four G checks.
3. **§6's fourth limitation (tokens already spent) mostly evaporates.**
   Promoted to runtime *as-is*, G1's predicate can preempt the model call on
   Seam-A turns, exactly like the existing gates. It is cheaper than the
   document thinks because it is the thing the document was trying not to
   call it.

### 2b. §5's coverage claim contradicts the register's own I-06.

§5 promises the promoted check covers "Spanish, lowercase names, idiom, and
every phrasing nobody has imagined." For G1-as-implemented this is wrong:
lowercase "ray" → `resolved_subjects=[]` → G1 returns None (:63-64). Spanish
is covered only when the name happens to arrive capitalized. G1 inherits the
input pipeline's blindness *by construction*, because it reads the input
pipeline's outputs. The check that delivers §5's coverage is a reply-side
roster scan — which is a different, unbuilt check. Which brings us to:

### 2c. "The one I cannot see" — found. It is G0, and it is in the document's own evidence chain.

HarnessPlan Phase 3.3 (docs/deliverables/HIP_HarnessPlan__v20260715_1600.md,
sourced from the prior Fable review): *"G0: reply names a registered member
or care recipient while `resolved_subjects=[]` or nothing admitted about
them. Closes G1's blind spot."* Marked "not optional." Register I-06:
"needs G0." The generation-plane gap is also already named in
ANALYSIS__candidate-intent-deep-review__v20260711_0501.md ("CandidateIntent
governs the decision plane... not the generation plane"), and an
audience/output gate appears in the voice reference architecture doc.

So the proposal is: G0, promoted to runtime, unattributed. That doesn't make
it wrong — it makes two of its selling lines wrong:

- **"The check exists"** — no. G1 exists (and is a precondition in a wig).
  G0 — the check that actually reads the reply — exists nowhere, not even
  offline.
- **"Costs nothing new to build"** — the runtime G0 is genuinely small (see
  §3 below), but it is a build, not a promotion.

### 2d. "Is the claim-kinds list bounded?" — Directionally yes, but it leaks in the document's own evidence.

D-03's fabricated reply was "Got it, confirmed. **Today is Thursday, July 16,
2026, and it's morning.**" The date/time half is a temporal claim about the
world that doesn't sit cleanly in any of the four rows. Claims about
conversation history ("as you told me yesterday...") and about capability
("I can order that for you") are further kinds nothing in the table names.
The defensible form of the thesis is comparative, not enumerative:
**claim-kinds grow much slower than phrasings, and a new claim-kind is
discoverable from the reply side after one incident, whereas a new phrasing
must be imagined before it happens.** Keep that sentence; drop "four, maybe
five."

### 2e. "Does the value-blindness kill it?" — True offline, overstated at runtime.

The offline record is value-blind by design (epistemic_record.py: TD-030,
`_strip_values` at :56-64). But at the runtime exit site, the plaintext
values that entered the prompt are in scope —
`_gate_double_valued_park_query` reads `f["value"]` off
`injection_result.allowed` today (:2272). A runtime check is not
*structurally* value-blind; wrong-value detection is hard (paraphrase
matching), not impossible. The wrong-value class (H-01/H-02, PW029/PW030) is
real and this proposal does not touch it — the document is right to flag
that, and H-08's warning binds here: suppress-only exit gates push toward the
refuse-everything fixed point, so any runtime G-gate must land with the
plan's opposite-polarity metrics, not instead of them.

### 2f. "Output-side matching may be more reliable" — assertable, and stronger than the hedge.

The input side needed `isupper()` because it does open-ended named-entity
extraction. The output side matches against a **known, closed roster**
(household members + care recipients), so it matches case-insensitively and
never depends on capitalization at all. Residual, worth carrying: D-04-class
collisions cross to the output side — a reply about Ray Charles the singer
names roster `ray`. The guard-string fallback makes that failure safe
(refusal, not fabrication), which is the correct polarity.

---

## 3. THE CORRECTED FRAME, AND WHAT IT SAYS TO BUILD

The precondition/postcondition dichotomy is the wrong cut — §8's "distinction
without a difference" suspicion is half right. The cut that survives contact
with the code is:

> **Question-keyed gates** enumerate situations a user can create. Unbounded.
> **Outcome-state-keyed gates** enumerate states of HIP's own turn machine:
> wrote / parked / pending-confirmation / wrote-nothing. Bounded, small, and
> the system already owns the state.

The codebase already has two outcome-state exit gates
(`_gate_unconfirmed_update`, `_gate_double_valued_park_query`). They are the
precedent the document lists among the preconditions in §1 — mislabeled,
because the first one runs *after* inference and replaces the reply. The
plumbing the proposal needs already exists at the exact call site.

Against the document's own table:

| Claim about | Closes with | Reply parsing needed? | Size |
|---|---|---|---|
| an action HIP took — false ack (atorvastatin) | extend the F3 zero-write check past `_SUPERSEDE_PHRASE_RE` (:2296) to all declaratives | no | one condition at an existing call site |
| an action HIP took — false confirm (D-03) + instruction leak (D-18) | pending-confirmation state gate: unmatched confirmation attempt never falls through to the model (the register's own stated fix) | no | small, state machine already exists |
| a person (documentary; subjects=[] cases) | **runtime G0**: case-insensitive roster scan of the reply vs admitted-about-them, guard string on hit | yes | small; roster is closed; text path only |
| the world / HIP's own configuration | claim extraction against provenance | yes | **not thirty lines — do not schedule it as if it were** |

Two costs the document missed, both real:

1. **Voice path.** On the current realtime path the audio has already
   streamed when the transcript arrives (realtime_adapter.py:503-513) — a
   runtime exit gate cannot unspeak it. It covers the text path today and the
   voice path only under the cascade architecture the voice decision memo
   already chose, partly for this exact reason ("text checkpoint = governance
   requirement"). The postcondition thesis is an *argument for* the cascade
   decision and should be cited there, not silent about it.
2. **Detection false negatives become visible.** A zero-write gate on all
   declaratives converts the P2/i019 silent-miss class from false acks into
   user-visible "I didn't catch that" turns, at the miss class's true rate
   (see I-10's corrected measurement). That is the honest and correct
   behavior — but pair it with a detection retry (I-10 option c) or the demo
   will wear the rate on its face.

## 4. ORDERING — SPLIT VERDICT

- **Jump the queue:** the two outcome-state exit gates (D-03
  no-fallthrough + all-declarative zero-write). Smaller than anything in the
  register's order, they close the demo-blocking defect (T04, Script 03 "do
  not hand keyboard"), and they are preemptive — no tokens wasted, no reply
  parsing, no new failure surface.
- **With them, cheap:** runtime G0 on the text path, guard-string fallback.
  Register it as closing I-06's runtime half; the offline G0 (HarnessPlan
  3.3) still lands in Layer 6 so the harness sees what production suppressed.
- **Unchanged:** fail-closed D-01 stays exactly where the register put it.
  Exit gates convert fabrication into refusal; only the classifier fix
  restores the *answer*. An exit gate in front of a fail-open classifier is a
  system that refuses the beachhead's queries instead of fabricating at them
  — safer, and still broken. Both are needed; neither substitutes.
- **Do not schedule:** world-claim and self-configuration postconditions as
  if they were small. They are provenance-on-output, the hard version the
  document correctly flags in §8.

## 5. PROVENANCE FLAGS

1. The document's cited prior — `HIP_SIA_PhaseB__risk-memo__v20260716_0800.md`
   — does not exist in the repo or anywhere findable on this machine. Either
   it lives outside the repo or the citation is confabulated. In a project
   whose entire doctrine is provenance, a review document with an unauditable
   citation chain must be flagged: "your corrections, accepted" cannot be
   checked against anything.
   RESOLVED 2026-07-16 (post-review): the file was untracked/unfindable at
   review time, not confabulated — it has since landed in
   `docs/deliverables/` at commit `9017d10` and is registered in
   `docs/deliverables/MANIFEST.md` Section B ("SIA Phase B risk memo"). The
   citation chain is now auditable.
2. The reviewed document itself is not filed under the naming law. If its
   content is to be relied on, file it; this review is registered in
   docs/INDEX.md and cites it by its self-declared version string.
3. No MANIFEST change: nothing in Section B is touched by this review, and no
   commit accompanies it. If the ordering decision in §4 is adopted, the
   Script 03 prep doc and the register's ORDER section are the artifacts to
   update.
