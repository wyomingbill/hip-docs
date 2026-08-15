# REQ_SIA_PHASEB
Status: IN_PROGRESS
Reconciled-Against: c86a414

This doc exists because it should have existed before c86a414. Item 0 of the
risk memo's §9 (F3 gate widened to all declaratives + detection retry)
shipped against a requirements doc written retroactively, after the fact —
flagged by the same session that wrote it. This doc corrects that: it
governs what ships next, points at the requirement that actually authorizes
this work, and reconciles three places where the surrounding plans had
drifted out of sync with each other.

## THE REQUIREMENT

**Empty. No verbatim requirement exists.** This is not a placeholder pending
an answer — it is the answer. Asked directly, confirmed: the SIA/exit-gate
track originates from a chat session's theory doc
(`HIP_Theory__turn-type-ontology__v20260715_2230.md`), then Fable's review of
it (`ANALYSIS__postcondition-gap-review__v20260716_1512.md`), then the risk
memo built from that review, then Bill adopting the result. **That is an
adopted analysis, not a stated requirement.** Nobody should go looking for a
missing Bill quote here; there isn't one, by construction, and back-filling
one would repeat the exact mistake this doc exists to stop (see c86a414).

**This track originates from analysis adopted on 2026-07-16.**

**But the work IS governed — by a different, existing, on-file requirement:
`docs/requirements/REQ_VOICE_DEMO__one-screen-script-plus-live-voice__v20260715_1601.md`.**
Bill's words there, verbatim (stated three times, on file once):

> "There are two parts to this demo. There is the scripted part and there is
> the audio part. It's all in one. Once you get done with the scripted part,
> then you go to the audio part and start talking to it. And all the
> dashboard shit should work like it worked in the scripted."

REQ_VOICE_DEMO's own acceptance test, item 2, is "Run a script to
completion." Script 3 is `trust_ladder`. T04 of that script says *"Got it,
confirmed"* and confirms nothing (D-03/D-18) — the parked row stays
UNRESOLVED, the graph is unchanged, and the script has not, in any honest
sense, completed. That failure is not a side detail; it is a direct hit on
REQ_VOICE_DEMO's own acceptance test, item 2, in Bill's own words. The exit
gates in the risk memo's §9 (item 0's F3 fix, already shipped; item 0's
D-03/D-18 close, and item 0b's G0, not yet shipped) exist because of that
hit, not because of the theory-draft-to-risk-memo chain that produced their
design. **REQ_VOICE_DEMO is the parent requirement for this work. Point every
future dispatch on the exit-gate sequence at it, not at this doc's own empty
REQUIREMENT section, and not at the risk memo.**

One honest limit on that parentage: REQ_VOICE_DEMO's text does not name
`trust_ladder`, D-03, D-18, or G0 — its acceptance test is generic ("run a
script to completion"). The connection above is this doc's inference, not a
quote. It is a tight inference (a fabricated confirmation is definitionally
not "a script run to completion"), but it is an inference, and the next
session should read it as one.

## THE ACCEPTANCE TEST

Narrowed to two clauses. Spanish and the idiom bank are dropped from this
REQ entirely — reasons below, filed so neither resurfaces here.

**"On the text path, HIP does not state a false claim about its own actions,
and does not state a claim about a person it has no admitted facts for."**

- **Clause 1 (own actions) — testable now.** The epistemic record carries
  `delta`, `park`, and `confirmation` per turn. "Claimed a write happened"
  vs. "delta is empty," and "claimed a confirmation happened" vs.
  "confirmation state unchanged," are both mechanically checkable today.
  c86a414 already gates the write half of this (F3 + retry), live-verified.
  The confirmation half needs D-03/D-18 closed (item 0's second half, not
  yet shipped) before it is equally covered.
- **Clause 2 (person with no admitted facts) — needs G0.** This is G0,
  verbatim, and G0 does not exist anywhere — not in the harness, not
  offline, not in shadow (confirmed by grep this session). Building it
  requires: a registered-member + care-recipient name list to check mentions
  against, a way to detect a person MENTIONED in free-text model output
  (name/pronoun resolution — "your father," "he," "Dad" all have to
  resolve), and cross-referencing that mention against `resolved_subjects`
  and `admitted[]`. Real, unbuilt work. **Not testable until item 0b ships.**

**STATUS accordingly: clause 1 is IN_PROGRESS (write half done, confirm half
open on D-03/D-18); clause 2 is PLAN (blocked on G0/item 0b, entirely
unbuilt).** The acceptance test as a whole does not pass yet and should not
be reported as passing until both halves do.

**Dropped, filed so they do not resurface as part of this REQ:**

- **Spanish.** `harness/orchestrator.py:416` and `server/voice_orch.py:1842`
  both instruct the model *"Never output Chinese, Mandarin, Spanish,
  French, German, Japanese..."* — the product is currently prompt-enforced
  English-only. There is no Spanish golden set, no Spanish idiom bank, and
  no Spanish-capable false-claim oracle (name/negation detection in Spanish
  is a different NLP problem, not a translation of the English one). This is
  **an open product question — should HIP ever answer in Spanish — not a
  defect and not a test gap.** A previous session escalated this as a live
  business risk; it was not one then and is not one now. It is a product
  decision nobody has made, filed here explicitly so it does not resurface
  as if it were a known-broken test target. If it becomes a real question,
  it needs its own REQ, not a clause borrowed from this one.
- **Idiom bank.** HarnessPlan Phase 4.1 territory, tracked as H-05. Not this
  REQ's scope. Referenced in the plan reconciliation below because Phase 4's
  status matters to the harness picture generally, not because this REQ's
  acceptance test depends on it.

## RECONCILE THE PLANS

### 1. HarnessPlan phases 2, 4, 5, 6, 7 — dead, deferred, or superseded?

**None are dead or superseded.** Phase 5 gets a different verdict below —
it was not deferred, it was dropped, and that gap is now closed by this doc.

- **Phase 2 (one oracle).** Tracked: H-01..H-04, "NOT FIXED — Phase 2."
  Sequenced at `ORDER` step 6. Live, intended, just last in priority behind
  D-06/D-07 (blocking), D-01, D-05, G0, H-06.
- **Phase 3 (fail closed / G0).** Live, explicitly not superseded by
  today's work — the risk memo says so directly ("shipping 0/0b does not
  remove the need to fix D-01 eventually"). G0 (3.3) is I-06, `ORDER`
  step 4, still entirely unbuilt.
- **Phase 4 (traffic that grows / idiom bank).** Tracked: H-05, "NOT
  FIXED — Phase 4," sequenced at `ORDER` step 6. Confirmed unbuilt by grep.
  Live, not superseded, not started.
- **Phase 5 (metrics) — WAS dropped silently. Now fixed: see H-09 below.**
  Had no defect ID, was not in `ORDER`, was not referenced by the risk memo
  or anything else since HarnessPlan specced it 07-15. This is the third
  clause of Bill's own verbatim harness requirement — REQ_HARNESS: "...that
  has metrics that we can track" — and it went missing with no decision
  behind the silence, which is a worse failure mode than the other four
  phases' "sequenced last." As of this session: **H-09 added to
  `HIP_DefectRegister__v20260715_1930.md`, and Phase 5 added to its `ORDER`
  section** (see WHAT'S ALREADY DONE). It is now tracked exactly like
  Phase 2/4/7. Nothing about Phase 5 has been built — only found and given
  an ID, which is what "not deferred, it went missing" required as a fix.
- **Phase 6 (record fidelity).** Tracked: H-07, "PARTIAL — Phase 6." Live,
  genuinely in progress, not superseded.
- **Phase 7 (the gate, bifurcated).** Tracked: H-08, "NOT FIXED — Phase 7,"
  sequenced at `ORDER` step 6. Live, not superseded.

### 2. G0 — HarnessPlan 3.3 ("not optional") vs. risk-memo item 0b. One authority.

**The risk memo is authoritative on runtime G0's build priority. This is no
longer just this doc's call — `HIP_HarnessPlan__v20260715_1600.md` §Phase 3
has been amended in place to say so, in this session, so the two documents
stop disagreeing on the page.**

The amendment preserves HarnessPlan's original 3.3 text (it still specs a
real, separate artifact — the harness-side/offline invariant, which gates a
push, not a live reply) and adds a dated note underneath: risk-memo item 0b
governs when the *runtime* gate ships, and it ships far earlier than Phase
3's position in HarnessPlan's own sequence would suggest, because it closes
a live-reply defect class (I-06: the atorvastatin/D-03/D-18 family) that an
offline check alone leaves exposed indefinitely. Both artifacts are real and
both are still needed; only their relative priority was in conflict, and
that conflict is now resolved on the page, not just in this reconciliation
doc. **Item 0b itself is still unbuilt** — c86a414 shipped item 0 (F3 +
retry) only.

### 3. REQ_HARNESS — PARTIALLY MET, plan half-abandoned. What does that mean for STATUS?

**STALLED, not IN_PROGRESS-as-momentum.** REQ_HARNESS's header still reads
`Status: IN_PROGRESS`, and that is not being changed by this doc — nothing
regressed, nothing was decided against it, and changing another REQ's status
is not this doc's authority to exercise unilaterally. But the plain fact,
stated here so it stops being implied away: **REQ_HARNESS is stalled on two
named Bill-decisions, I-10 and D-17, and no commit has touched
`eval/harness.py`, `eval/oracle/record_invariants.py`, or
`eval/harnesslib/reporter.py` since 07-16 08:49** (`546bd52`/`483dd3b`).
Every commit since then — the postcondition-gap review, both risk-memo
versions, and c86a414 — is SIA-track work, not REQ_HARNESS work. I-10 (G1
hard-zero gate fails ~91% of `--full` runs on a pre-existing, unrelated
detection flake, three options on file, none chosen) and D-17 (the reporter
masks regressions behind brand-new failures, fix identified, not applied,
"Bill's call before touching") are the two things blocking it, and both are
explicitly waiting on Bill, not on more engineering. `IN_PROGRESS` should not
be read as "actively advancing" until one of those two decisions lands.

## WHAT'S ALREADY DONE

- Item 0 of the risk memo's §9 (F3 gate widened to `is_declarative_utterance`,
  detection retry at temperature=0.2) — shipped c86a414, four live proofs
  observed, retroactive REQ filed and flagged. Governed, after the fact, by
  `REQ_atorvastatin-false-ack__f3-gate-widen-and-detect-retry__v20260716_1713.md`.
- **H-09 added to `HIP_DefectRegister__v20260715_1930.md`** (Phase 5/metrics,
  dropped silently, found by this doc's reconciliation) and Phase 5 added to
  that register's `ORDER` section alongside Phase 2/4/7.
- **`HIP_HarnessPlan__v20260715_1600.md` §Phase 3 amended in place** — a
  dated note under 3.3 states the risk memo governs runtime G0's build
  priority, resolving the two-documents-disagreeing gap from RECONCILE
  THE PLANS §2 above.
- TD-121 F1/F3 original fix, D-05 (park-query gate + two live bugs found
  fixing it), D-15 (mic-path INJ-6 declarative exemption), D-13 (phantom
  record) — all RESOLVED/FIXED, tracked in the defect register, unaffected
  by anything in this doc.
- REQ_HARNESS Phase 1 (Layer 6 wiring, G3 falsy-check fix, phantom-record
  handling, run-contamination fix) — built, per REQ_HARNESS's own WHAT'S
  ALREADY DONE section.

## WHAT'S KNOWN BROKEN

- G0 (item 0b) is specced twice (HarnessPlan 3.3, defect register I-06),
  reprioritized once (risk-memo amendment, now cross-referenced in
  HarnessPlan itself), and built nowhere. Clause 2 of THE ACCEPTANCE TEST
  cannot pass until it exists.
- D-01 (fail-open routing default), D-03/D-18 (confirmation gate fallthrough)
  are open. D-03/D-18 are the specific reason `trust_ladder` T04 fails
  REQ_VOICE_DEMO's acceptance-test item 2 ("run a script to completion") —
  untouched by c86a414, which only closed the atorvastatin leg of item 0.
- D-06/D-07 (`ORDER` step 1 in the defect register — "blocks everything: if
  the guard does not fire when its predicate is True, no result from today
  can be trusted") are still UNDER TRACE, unresolved, not investigated in
  any session so far.
- I-10 and D-17 are both open, both explicitly "Bill's call," both blocking
  REQ_HARNESS's literal acceptance-test bar — see RECONCILE THE PLANS §3.
- Spanish support is an open product question, not a defect — see THE
  ACCEPTANCE TEST above. Do not re-file it as a test gap or a business risk
  without a product decision behind it first.

## CONSTRAINTS

- This doc authorizes exactly the work its parent requirement
  (REQ_VOICE_DEMO) already covers: closing the defects that block
  `trust_ladder` (script 3) from completing — D-03/D-18 now, G0/item 0b as
  the next piece. It does not authorize the rest of the risk memo's §9
  (items 1-6, the SIA/Gate-B adjudication work) — that remains ungoverned
  by any on-file requirement, per THE REQUIREMENT above, and should not
  proceed under this doc's name.
- Whatever ships next against D-03/D-18 or G0/item 0b should reference this
  doc, not the risk memo alone, since this doc is what actually authorizes
  the work per REQ_VOICE_DEMO.
- Do not re-open Spanish or the idiom bank as if they were gaps in this
  REQ's acceptance test. They are out of scope by design, not by oversight.
- Do not read REQ_HARNESS's `IN_PROGRESS` status as "actively advancing."
  It is stalled on two named Bill-decisions (I-10, D-17) as of 07-16 08:49.
