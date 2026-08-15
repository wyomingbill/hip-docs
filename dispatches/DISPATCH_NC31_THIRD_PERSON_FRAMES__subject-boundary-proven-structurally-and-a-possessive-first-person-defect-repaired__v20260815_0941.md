# DISPATCH_NC31 — third-person medical frames, the SUBJECT BOUNDARY proven structurally, and a possessive-subject defect that pre-dates the whole frame sequence
Status: **BUILT** — code landed `62c0848` (`~/hip-nc2` @ `nc-b0`); REQ Amendment 4 landed `cf7e184` (`~/hip-roadmap` @ `roadmap`)
Reconciled-Against: `62c0848`, over base `0ee55fb` (NC 26) — read from the machine; machine gate and lane preflight both passed
Dispatch: NC 31
Date: 2026-08-15 09:41 (Mountain)
REQ: **`REQ_UNRESOLVED_REFERENCE_DETECTOR__...__v20260814_2056.md`, AMENDMENT 4** — filed at `cf7e184` **before the first line of code**.
Type: **BUILD** (product code + twins), preceded by a docs-only amendment.

---

## 0. RECAP

```
NC 31 — third-person medical frames + Q1 clarify-as-built
COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING
```

**One sentence:** the four third-person frames are in and reuse NC 26's guardrails whole; ruling
2's subject boundary is proven **structurally** rather than behaviourally; Amendment 3's Q1 is
closed as clarify-as-built with the park table read rather than the label asserted — **and the
work uncovered a defect that pre-dates the entire frame sequence: `"my mother takes metformin
500mg"` was classified as a FIRST-PERSON write assertion.**

## 1. THE DEFECT, FIRST, BECAUSE IT IS THE MOST IMPORTANT THING HERE

Measured before a line of NC 31 code was written:

```
"my mother takes metformin 500mg"  →  FACT_ASSERTION_WRITE
                                      first-person+assert-verb:takes+dosage:500mg
```

**The reason string says "first-person" about a turn describing the speaker's mother.**
`_FIRST_PERSON` matches the possessive **`my`**, so any third-party assertion phrased with a
possessive was read as a first-person medical assertion with write semantics. Also affected:
*"my mother is on lisinopril 10mg"*, *"my wife started lisinopril 10mg"*.

**Name subjects routed correctly** — *"Maya takes metformin 500mg"* and *"Ray's on Jardiance
10mg now."* both went to `MEDICAL_OTHER` — **which is exactly why this survived NC 15, NC 25 and
NC 26.** Every existing third-person twin used a NAME. The possessive form was never tested.

**It is ruling 2's prohibited shortcut, arriving through the SUBJECT TEST rather than through the
frames** — which is why a dispatch about adding frames found it.

**THE REPAIR IS SUBJECT-DIRECTED, NOT VERB-DIRECTED.** The third-party check runs **before** the
`_FIRST_PERSON` test, so it covers `takes` and every other verb rather than only the four newly
ruled frames. Fixing it frame-by-frame would have left `takes` broken.

**SEVERITY, BOUNDED HONESTLY (P7.13).** Class (a) is not itself a write: it passes through to the
normal governed path, whose park-and-confirm machinery resolves the subject downstream. **What is
measured here is a wrong CLASSIFICATION asserting first-person subject semantics. Whether a
wrong-subject write actually lands is downstream and is NOT measured by this dispatch.** The
classification is wrong either way — ruling 2 says the split must not assert subject at all — but
the blast radius is stated rather than assumed.

## 2. RULING 1 — THE FOUR FRAMES, WITH NC 26's GUARDRAILS REUSED WHOLE

`X is on` · `X is taking` · `X started` · `X stopped`, where the subject is a kinship term with
or without a possessive, a third-person pronoun, or a capitalised given name.

**The object guardrails are NC 26's, reused rather than reimplemented** — the exclusion list, the
preposition/adjunct test, the whole-noun-phrase scan and the generic-medical-noun deferral. So
*"my mother is on vacation"* and *"Sam started school"* are released by **exactly the machinery
that releases *"I'm on vacation"* and *"I started school"***. One definition of "what counts as a
medication object", for both persons.

**A first-person subject before the verb disqualifies the frame outright**, so NC 25's and NC 26's
paths keep every turn they had — asserted by a twin, not assumed.

## 3. RULING 2 — THE SUBJECT BOUNDARY, PROVEN FOUR WAYS

A negative is proven by trying to violate it. The twins attack from four directions:

| clause | proof |
|---|---|
| **P7.8** | a third-party frame **never** yields `FACT_ASSERTION_WRITE`; it lands in `MEDICAL_OTHER`, the existing third-party path whose trust ladder and park machinery already own it |
| **P7.9** | **STRUCTURAL** — `MedicalSplit` carries exactly `cls` and `reason`, asserted from `dataclasses.fields`, and no field name contains subject/member/owner/person/actor |
| **P7.10** | the resolution step **still runs**: a recognized third-party assertion reaches the implementation, where `resolve_member()` lives, rather than being answered at the split |
| **P7.11** | an **unresolvable subject refuses** — a claim contradicting an authenticated principal gives `REFUSED_CLAIM_MISMATCH` with no model call, and the *same utterance without the conflict proceeds*, which is what makes the refusal evidence of anything |

**THE SUBJECT TOKEN IS VALIDATED AND THEN DELIBERATELY DROPPED.** It would be useful in the audit
trail and it is left out anyway: if the reason embedded `subject:mother`, a downstream caller
could parse a subject out of a classification. **Leaving it out makes the shortcut structurally
impossible rather than merely untaken**, which is what ruling 2 asks for. The reason says
`SUBJECT-NOT-ESTABLISHED` instead of saying who — and a twin asserts the mention is absent.

**P7.9 is the clause worth keeping.** A behavioural twin proves what the code does today; a
structural one proves what it cannot do. Ruling 2 is a permanent constraint, so it deserved the
permanent form of proof.

## 4. RULING 3 — Q1 CLOSED: CLARIFY-AS-BUILT

**Amendment 3's tier stands unchanged.** NC 26 read constraint 2 as two tiers and wrote the
uniform alternative into the REQ so it could be overruled in one line; **it is not overruled.**

Bill's addition sharpens it: ***"NEVER a pending write from uncertainty alone."***

**That is a claim about the PARK MACHINERY, not about a label** — so a twin asserting
`cls is AMBIGUOUS_WRITE` does not discharge it. The twins:

- read the pending table (`harness.confirmation_gate.peek`) and assert **0 parked rows**;
- read the model-call counter (`harness.model_calls.counting`) and assert **0 model calls**;
- and **prove the pending table can see a REAL park first** (NC 10's method — register one, see
  it, clear it), so "0 parked rows" is a measurement rather than a vacuous truth.

**Why the existing kernel gate suffices, asserted rather than assumed:** `governed_turn` gates
class (b) and returns **before `turn_impl` is ever called**, so no park can be registered on that
path. **Measuring the park table rather than the class is what makes a later reordering of that
gate fail the twin.**

Anti-vacuity for ruling 3 itself is twinned too: a corroborated assertion is **not** diverted to
clarification. A rule that clarified every medical turn would satisfy "never a pending write" and
destroy the feature.

## 5. AN EXISTING TWIN REFUSED THIS DISPATCH'S FIRST ATTEMPT, AND IT WAS RIGHT

To avoid a second copy of "words that are capitalised but are not names", the first version
**imported B1's list** from `harness.unresolved_reference` — reasoning, from NC 26, that a
duplicated list drifts silently while a broken import fails loudly.

**NC 15's `test_the_module_is_model_free_and_io_free_by_import` refused it.** It asserts against
the AST's real import table that `medical_intent.py` imports **nothing but `re`, `dataclasses`,
`enum` and `__future__`** — the purity that makes the split provably deterministic and
side-effect-free.

**That property outranks the duplication it costs.** Importing another harness module would have
traded a guaranteed property for a stylistic one. The import was reverted and a small,
purpose-built list defined locally — it guards a *subject slot*, so it needs only the words
capitalised for sentence position. **The reasoning now lives in the code beside the copy**, so the
next reader meets the argument rather than the smell, and NC 31's own twin re-asserts the purity
in the dispatch that tried to break it.

**Caught on the first run.** This is the second time in this sequence an existing twin has
governed a design decision rather than merely reporting one.

## 6. THE ACCEPTANCE, MEASURED

Environment: **lane graph 7693 has no listener** — this lane's honest default.
**`lane_preflight.py --tree ~/hip-nc2 --expect-branch nc-b0` → exit 0.** The **global `--busy`
scan returned exit 7**, and that is reported rather than rounded away: `~/hip-vo` was mid-run on
**7691** — a different tree and a different graph — and the lane check's own busy gate passed
without `--allow-busy`, so nothing here was contended.

### Twin counts by category — 44 new

| category | twins | what they hold |
|---|---|---|
| **Ruling 1** — the four frames | **19** | 4 recognized drug + 4 invented drug + 4 negated + 7 anti-vacuity controls |
| **Ruling 2** — the no-shortcut proof | **12** | 5 never-a-first-person-write + 1 structural (no subject field) + 3 reason-carries-no-subject + 1 resolution-still-runs + 1 unresolvable-refuses + 1 speaker-not-assigned |
| **Ruling 3** — Q1 | **8** | 4 uncertain→clarify/0 calls/0 parks + 1 instrument anti-vacuity + 1 deterministic + 1 says-nothing-recorded + 1 corroborated-not-diverted |
| **Neighbours + recorded residuals** | **5** | NC 26 unchanged, module still pure stdlib, question-shape-first, 2 inverted-question residual |

### NC 26's full twin set re-run green

**242 passed** across NC 15, NC 20, NC 25 and NC 26 — including the two NC 15/NC 25 twins NC 26
retired, and NC 15's purity twin.

### The suite, by SET comparison at a single HEAD (`0ee55fb`)

```
BEFORE:  20 failed, 816 passed, 39 skipped, 21 errors
AFTER:   20 failed, 860 passed, 39 skipped, 21 errors
failure+error SET: 41 entries before, 41 after, diff EMPTY
860 - 816 = 44, exactly the new twins
```

HEAD was re-verified as `0ee55fb` immediately before the after-run, so the comparison is
single-variable.

## 7. FINDINGS FILED — 3, NONE BLOCKING

**NC31-F1 — THE CLARIFICATION DOES NOT LITERALLY ASK A QUESTION.** Bill's ruling illustrates it
as *"do you mean a medication?"*, and `CLARIFY_REPLY` — NC 15's ruled constant — **contains no
`?` at all.** It explains, says nothing was recorded, and tells the member how to do either thing
on purpose, which is the substance; but it is a statement, not a question. **Left as-is
deliberately:** the constant is NC 15's, its exact bytes are a determinism guarantee (R3.1's
shape), and rewording it is a ruling rather than a refactor. A twin now asserts the absence, so
the wording cannot change silently in either direction. **Bill's call.**

**NC31-F2 — INVERTED QUESTIONS DO NOT MATCH THE DECLARATIVE FRAMES, in third person too.**
*"Is my mother on Zervolol?"* → `NOT_MEDICAL`, because `X is on …` matches and `is X on …` does
not: the auxiliary and the particle are no longer adjacent. **The direction is safe** — a question
cannot become an assertion, so no write can happen. This is the third-person twin of **NC26-F1**
and the second sighting of the same shape; a recorded residual, twinned so it fails visibly if it
changes. **If Bill wants interrogative frames, that is one ruling covering both persons.**

**NC31-F3 — A VERBLESS THIRD-PARTY MEDICAL NOUN PHRASE STILL CARRIES A FIRST-PERSON-FLAVOURED
REASON.** *"my mother's metformin 500mg"* has no frame verb, so it falls past the subject check to
the final fallback and lands in class (b) with reason `first-person-medical-unclear`. **Class (b)
writes nothing, so no ruling-2 violation of substance occurs** — nothing is written and no subject
is asserted as a write target — but the reason string is imprecise in the same way the repaired
defect was. Recorded rather than fixed: the repair NC 31 was asked for is subject-directed over
frame verbs, and widening the subject check to verbless noun phrases is a separate decision.

## 8. WHAT I DID NOT DO

- **No change to `CLARIFY_REPLY`** (NC31-F1) — a ruled deterministic constant.
- **No interrogative frames** (NC31-F2), in either person.
- **No change to NC 25's or NC 26's first-person paths** — the third-party check is gated on
  there being no first-person subject before the verb, and a twin asserts they are unchanged.
- **No weakening of NC 15's purity twin** to accommodate a convenient import. The import went,
  not the twin.
- **No REQ ruled MET, no acceptance row re-tiered, no baseline changed.**

## 9. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Recognition boundary and subject semantics of the medical split; no ledger claim's standing
evidence is touched.

## 10. VERIFIED

Machine gate (`bill-ai` / `[REDACTED-MACHINE-NAME]` / `~/hip-nc2` @ `nc-b0` @ `0ee55fb`, in
sync). Lane preflight exit 0 before any suite; the global busy scan's exit 7 reported with its
cause. Claim first (`289037e`), REQ Amendment 4 before code (`cf7e184`), code after (`62c0848`).
Repo lock held around each git operation only; every push verified to carry exactly one commit.
`.hip-scope` hand-written in `~/hip-nc2` (TD-R-194(a)). No contention: NC 30 is docs-only in
`~/hip-vo`. Every number above is from this session's runs, with the service state stated.
