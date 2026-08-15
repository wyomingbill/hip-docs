# REQ_UNRESOLVED_REFERENCE_DETECTOR
Status: PLAN
Reconciled-Against: 2026-08-14. Kernel pinned at **`8ad909a`** (`~/hip-nc2` @ `nc-b0`).
Amendments: **1** (NC 20, R2/R3/R4 — `a856863`) · **2** (NC 25, Bill's rulings 1-5 — the B1
POLICY BATCH, 2026-08-15, reconciled against `04a63f8`) · **3** (NC 26, widen the medical-assertion
frames, 2026-08-15, reconciled against `bfb09df`) · **4** (NC 31, third-person frames + the SUBJECT
BOUNDARY + Amendment 3's Q1 RULED, 2026-08-15, reconciled against `0ee55fb`). **All four are
appended at the bottom in order, and each changes what the one before it accepts — read them
forwards. Amendment 4 also CLOSES Amendment 3's open question Q1: clarify-as-built, and never a
pending write from uncertainty alone.**

> **STATUS HEADER LEFT AT `PLAN`, DELIBERATELY, AND FLAGGED RATHER THAN CORRECTED.** NC 20 landed
> B1 code (`41c130a`) against this REQ and left the header at PLAN; NC 25 is not re-tiering it.
> Re-tiering an acceptance row and ruling a REQ MET are both **outside** the pre-authorized
> correction classes — sessions report readiness, Bill rules. **Recorded here so the stale-looking
> header reads as an unmade ruling and not as an oversight.**
Map: `docs/design/HIP_EXECUTION_MAP__natural-conversation-demo-v1-preflight-excavation__v20260814_1720.md` (NC 7).

Drafted by **NC 17 — DOCS ONLY. No code was written, and none may be until NC 16's
verification of the kernel this sits on lands.** Every integration point below is cited at
`file:line` **as it exists at `8ad909a`**, not as it is remembered.

---

## THE REQUIREMENT

From the ratified acceptance design. The detector's subject, stated first because it is the
clause most easily lost:

> **It detects DEPENDENCY ON MISSING CONVERSATIONAL STATE — not pronouns.**

A pronoun is one symptom. *"And the other one?"*, *"same as last time"*, *"do that again"*,
*"what about Tuesday"* and a bare *"yes"* all depend on state the turn does not carry, and
several contain no pronoun at all. Conversely *"what is my address"* contains a pronoun and
depends on **household record**, not conversational state — the kernel already governs that
(`kernel.is_household_dependent`, `harness/kernel.py:128`) and **B1 must not fire on it**.

**B1 fires when answering requires a prior turn that this turn does not carry.**

### The five ratified clauses

1. **STRUCTURAL STOP.** On detection the turn stops **structurally**: **no model call, no
   frontier call, no resolver, no write, no retrieval** — and a **deterministic stop reason**
   accompanies it.
2. **NONINTERFERENCE.** A turn that does not depend on missing state is unaffected, and this
   is proven by twins rather than asserted.
3. **ANTI-VACUITY.** **Standalone short questions still answer.** A detector that stops
   everything short would pass clause 1 and destroy the product; brevity is not dependency.
4. **ASR TWINS.** The spoken path's transcription errors must not manufacture detections, and
   must not mask them.
5. **AUDIT FIELDS.** Every detection is recorded with fields sufficient to reconstruct why.

---

## THE ACCEPTANCE TEST

### A. Structural stop — proven at the boundaries, not by the reply text

- **A1** on detection, **zero answering model calls**, observed at
  `harness/model_calls.py` (`record()` / `counting()`), which NC 11 wired at the two answering
  sites in `server/voice_orch._governed_turn`.
- **A2** on detection, **no egress permit is requested** — asserted at
  `harness.egress_gateway.permit` (`harness/egress_gateway.py:permit`), because a stop that
  still asks the gateway has already assembled a payload.
- **A3** on detection, **no retrieval and no write**: `harness.extraction_queue`'s
  `read_user_facts` / `write_facts` are not called, and no `:Fact` is created.
- **A4** the stop carries a **deterministic reason** — the same input yields the same reason
  string, and the reason names **which state is missing**, not merely that something is.
- **A5** the stop is a **typed outcome**, not a sentinel string: a new
  `TurnOutcome.REFUSED_UNRESOLVED_REFERENCE` alongside the four at `harness/kernel.py:46`, so
  a caller distinguishes it by value exactly as it does `REFUSED_STORE_DOWN`.

### B. Noninterference

- **B1** a turn with no dependency on prior state reaches generation **unchanged** — the
  utterance that arrives at the implementation is byte-identical to the one that entered.
- **B2** the detector adds **no branch to the answering path**: on a non-detection it returns
  and nothing else changes, proven by the same equivalence shape NC 14 used per segment.

### C. ANTI-VACUITY — the clause that keeps the product alive

- **C1** each of these **answers** and must NOT be detected:
  *"what time is it"* · *"when is trash pickup"* · *"who am I"* · *"help"* ·
  *"what's the weather"*. **Short is not dependent.**
- **C2** a detector that fires on **all** of C1 fails this REQ even if every other clause
  passes. **The twin asserts the negative case as strictly as the positive one.**
- **C3** the household-dependent case is **not** B1's: *"what is my address"* is governed by
  `kernel.is_household_dependent` (`harness/kernel.py:128`) and must reach that path, not this
  one. **B1 and the store-down ruling must not shadow each other**, and a twin proves each
  fires on its own case and not the other's.

### D. ASR twins (spoken path)

- **D1** a transcription that garbles a standalone question must not become a detection —
  the detector reads `TurnRequest.utterance` and may consult
  `TurnRequest.transcript_confidence` (`harness/turn_request.py:105`), but **low confidence is
  not dependency**.
- **D2** a genuinely dependent utterance is still detected when transcribed imperfectly.
- **D3** the twins run on `spoken_request` (`harness/turn_request.py:210`) **and** on
  `typed_request` (`:193`) with the same text, and the detection **matches** — the modality is
  a field (`TurnRequest.source`, `:101`), never a different answer.

### E. Audit fields

- **E1** every detection records: the **stop reason**, the **missing-state class**, the
  **modality** (`source`), the **session id** (`:106`), the **member**, and a **query hash** —
  never the raw utterance, matching the shape `resolve_disclosure_block`'s record already uses
  (`harness/kernel.py:506`, `DisclosureRefusal.record`).
- **E2** the record is **derived from the decision object**, not built beside it — the
  property NC 14 S3 established so a record cannot disagree with what was decided.

---

## INTEGRATION POINTS — CITED AT `8ad909a`

| what | where | why it is the seam |
|---|---|---|
| **`TurnRequest`** | `harness/turn_request.py:76`, fields `utterance:100`, `source:101`, `principal:102`, `claimed_member:103`, `verification:104`, `transcript_confidence:105`, `session_id:106`, `source_detail:107` | the detector's **only** input contract; it must read these and nothing else |
| `typed_request` / `spoken_request` | `harness/turn_request.py:193` / `:210` | both adapters must produce a request the detector treats identically (D3) |
| **`governed_decision()`** | `harness/kernel.py:234` | **the insertion point.** It already runs *before* any model on both modalities and returns a `TurnDecision` (`:218`) with `proceed=False` |
| `TurnDecision` | `harness/kernel.py:218` | the stop travels as `proceed=False` + `reply` + `outcome` + `refusal_reason` — B1 needs **no new mechanism**, only a new outcome |
| `TurnOutcome` | `harness/kernel.py:46` | add `REFUSED_UNRESOLVED_REFERENCE` here (A5) |
| the voice call site | `server/voice_orch.py:1633-1637` | `governed_decision` is already called on the Pipecat path; B1 inherits it with **no voice edit** |
| the typed call site | `harness/kernel.py:150` `governed_turn` → `:281` `text_turn` → `:288` `text_reply` | and `server/voice_orch.process_text_query` delegates to `text_reply`, so both HTTP routes inherit it |
| **model-call observation** | `harness/model_calls.py` `record()` / `counting()` | A1's instrument; already wired at the two answering sites |
| **egress** | `harness.egress_gateway.permit` | A2's instrument |
| **conversational state that EXISTS today** | `server/voice_orch.py:519` `_trim_context(max_turns=8)`; `harness/session_memory.py` `session_store` (imported `voice_orch.py:119`); `self._last_reply` `voice_orch.py:1089`; `self._last_facts` `:1095`; `control_state` via `session_store.get_or_create(...)` | **what "missing" is measured against.** NC 7 §4 recorded eight stores across three lifetimes and **no single conversation-state owner** |

---

## WHAT'S ALREADY DONE — REFERENCED, NOT REBUILT

The kernel is the one pre-generation dispatcher (NC 13), both rulings fire on the default path
(NC 11), and S1–S4 moved speaker identity, confirmation, disclosure and memory-write into it
(NC 14). **B1 adds an outcome to an existing decision point. It builds no second path**, and a
draft that proposed one would be re-litigating charter §15.

## WHAT'S KNOWN BROKEN — the constraint B1 inherits

**There is no conversation-state owner** (NC 7 §4). `_trim_context`'s fixed 8-turn window is
the closest thing to episodic memory, and it is a prompt-assembly device, not a state store.
**So "the state is missing" is currently only answerable against a window whose boundary is
arbitrary** — see the open question below.

## CONSTRAINTS

- **DOCS ONLY until NC 16 lands.** This REQ authorises no code.
- **No second decision path.** B1 enters at `governed_decision` or not at all.
- **B1 must not shadow the store-down ruling**, and the store-down ruling must not shadow B1
  (C3).
- **No raw utterance in any audit record** (E1).
- **Fail-closed is not automatic here and must be decided, not assumed** — see below.

---

## OPEN QUESTIONS FOR BILL — TWO, AND BOTH ARE POLICY

**Q1 — Which way does B1 fail when it cannot tell?** Every other kernel decision fails closed:
unclassifiable intent is household (NC 8/NC 11), an unreadable registry refuses a web search
(NC 11), a registry miss is a guest (HA-50). **Failing closed here means stopping a turn we are
unsure about, and clause 3 (ANTI-VACUITY) exists because that is expensive.** The two rules
point in opposite directions and the conflict is real, not apparent. **A default is not
proposed here** — this is the security-policy class this project reserves.

**Q2 — What counts as "missing" while there is no state owner?** With `_trim_context`'s 8-turn
window as the only episodic surface, "the prior turn is not carried" is measurable **only
inside that window**. A dependency on turn 9 is indistinguishable from a dependency on nothing.
**Either B1 is scoped to the window and says so, or the Episode capability lands first.**
NC 7 §4 named the missing owner; this is where it starts to cost.

---

# AMENDMENT 1 — BILL'S RULINGS R2, R3, R4 (NC 20, 2026-08-14)

**AMENDED, NOT REPLACED.** Everything above stands as drafted by NC 17. This section carries
the three rulings that answer the draft's open questions and adds the acceptance they require.
Filed **before the first line of B1 code**.

## THE RULINGS — verbatim

> **R3: ambiguity fails CLOSED via deterministic fixed clarification; NO answering model call
> while the required reference/intent is unresolved. Anti-vacuity twins prove all five
> standalone short questions still answer — a detector failing them fails the REQ.**
>
> **R4: "missing" scoped to the existing 8-turn window, stated in the REQ as TEMPORARY BOUNDED
> SCOPE superseded by Episode.**
>
> **R2 (inherited): class (a) medical assertions never leave at web egress — extend NC 15's
> egress inherit; twin it.**

## R3 ANSWERS Q1, AND THE ANSWER IS NOT A COMPROMISE

The draft named the conflict honestly: every other kernel decision fails closed, and failing
closed here collides with anti-vacuity. **R3 resolves it by changing what "closed" costs.**
Failing closed does **not** mean refusing the turn — it means **asking one deterministic,
fixed question** and taking no model call until the reference resolves. The turn is not lost;
it is held. **That is why anti-vacuity survives the ruling rather than being traded against
it**, and why the five-question twin is a *hard* gate: a detector that clarifies everything has
not failed safely, it has failed.

- **R3.1** on detection the reply is a **fixed, deterministic clarification** — the same input
  yields the same words, byte for byte.
- **R3.2** **no answering model call** while unresolved, observed at `harness/model_calls.py`.
- **R3.3** all five standalone short questions still answer. **A detector failing them FAILS
  THIS REQ**, whatever else passes.

## R4 ANSWERS Q2 AS A BOUNDED, TEMPORARY SCOPE

**"Missing" means: not present in the existing 8-turn window** (`server/voice_orch.py:519`
`_trim_context(max_turns=8)`).

**TEMPORARY BOUNDED SCOPE — SUPERSEDED BY EPISODE.** This is stated in the REQ, as the ruling
requires, so nobody later mistakes an interim boundary for a design: a dependency on turn 9 is
**out of scope and undetectable**, and B1 must not pretend otherwise. **The Episode capability
supersedes this clause when it lands**; until then the detector's reach is the window's reach,
and the audit record says which.

- **R4.1** the detector reads only the window it is given, and the window size is **explicit**.
- **R4.2** a dependency beyond the window is **not** a detection — it is out of reach, and the
  stop reason must never claim otherwise.

## R2 EXTENDS NC 15'S EGRESS INHERIT

NC 15 refused class **(b)** — ambiguous write — at web egress
(`harness/escalation_backends.py`, `EgressAmbiguousMedicalWrite`). **R2 adds class (a),
`FACT_ASSERTION_WRITE`: a medical assertion never leaves at web egress either.**

- **R2.1** a class (a) utterance reaching web egress is **refused**, with **no socket opened**.
- **R2.2** class (c) `MEDICAL_QUERY` and `NOT_MEDICAL` are **unchanged** — anti-vacuity applies
  here too: a rule that refused all medical egress would pass R2.1 and break the product.
- **R2.3** the refusal is **defence in depth**, and says so: the kernel gate is where a class
  (a) turn is meant to be handled, so one arriving at egress means a path skipped the kernel.

## ADDED ACCEPTANCE

- **N1 NONINTERFERENCE** — for an **unauthorized requester**, the outcome is **identical
  whether or not the secret exists**. A detector whose behaviour differs is an oracle.
- **N2 ASR** — a manufactured anaphor, a manufactured name, a dropped negation and a changed
  number are each twinned: transcription damage must neither manufacture nor mask a detection.
- **N3 AUDIT** — fields **derived from the decision object** (NC 14 S3's rule), and **no raw
  utterance**.

---

# AMENDMENT 2 — BILL'S RULINGS 1-5, THE B1 POLICY BATCH (NC 25, 2026-08-15)

**AMENDED, NOT REPLACED.** Everything above stands as drafted by NC 17 and amended by NC 20.
**Filed BEFORE the first line of NC 25 code**, per Requirements Discipline item 8.

**WHAT THIS AMENDMENT IS ANSWERING.** NC 21 attacked the detector by execution and filed seven
findings (`04a63f8`, `DISPATCH_NC21_ADVERSARIAL_VERIFY_B1__...__v20260815_0626.md`). It fixed
nothing, deliberately, because it had found a **policy boundary and not a bug**: in its own
words, *"the class set is Bill's policy surface."* These five rulings are that policy, and they
land against four of those seven findings by name — **F1, F2, F6, F7**. The remaining three are
addressed elsewhere or deferred, and this amendment says which, so no finding is orphaned.

| NC 21 finding | what it measured | answered by |
|---|---|---|
| **F1** | nine dependency phrasings pass B1 undetected | **ruling 1** |
| **F2** | two standalone questions WRONGLY HELD by pleonastic "it" | **ruling 2** |
| **F6** | punctuation flips the bare-assent class ("ok" held, "ok!!" passes) | **ruling 4** |
| **F7** | medical assertions bypass the split when the drug is outside the lexicon | **ruling 5** |
| **F4** | a spoken "yes" to a pending parked write is unreachable | **ruling 3 — DEFERRED, see below. NOT built here.** |
| **F3** | the R4 window is inert in production | **NOT NC 25 — and REPAIRED during it.** NC 22 landed the live Episode at `0c7b6ee`; `governed_decision` now passes `episode.conversation_window()` as `window=`. |
| **F5** | B1 has ONE production call site; cross-modality drift is path-level | **NOT NC 25.** NC 24 claimed the repair (`57e7e2b`). |

## THE RULINGS — VERBATIM

> **1. DEPENDENCY CLASSES, not a phrase list: add ordinal/back-reference ("previous one",
> "second one"), elliptical follow-up ("why?", "how many?"), unresolved pronoun/reference
> ("her appointment"). EACH class gets standalone anti-vacuity twins proving legitimate
> standalones still answer.**
>
> **2. PLEONASTIC-IT exemption: genuine standalone forms (weather/environment) answer; keep the
> exception NARROW and twin it against real referential "it" ("is it raining" answers; "is it
> still active" about a prior referent holds).**
>
> **3. Pending-write "yes": NOT in scope — A4 owns confirmation precedence/routing. Record the
> deferral in the REQ so it is not orphaned; build nothing for it here.**
>
> **4. PUNCTUATION NORMALIZATION for classification ONLY: "ok" and "ok!!" classify identically;
> the ORIGINAL transcript stays verbatim in the epistemic/audit record — twin both halves.**
>
> **5. MEDICAL ASSERTIONS STRUCTURALLY: "I take <medication>" / "I don't take <medication>" are
> governed even when the drug name is unknown to any closed list — the structure, not the
> lexicon, is the boundary; lexicon supplements. Required twins: positive form, negative form,
> and an INVENTED drug name ("I take Zervolol") caught by structure alone; plus anti-vacuity
> ("I take the bus" / "I take notes" NOT governed as medical).**

---

## RULING 1 — CLASSES, NOT PHRASES. THE DISTINCTION IS THE RULING.

**The failure F1 measured was not nine missing phrases. It was three missing CLASSES**, and a
phrase list is what produces that failure a second time — NC 20's four classes are each a
*shape* (`_ANAPHOR`, `_CONTINUATION`, `_BARE_ASSENT`, `_REPEAT`), and the fix must add shapes,
not strings. A detector extended by adding *"the previous one"* to a regex has learned one
utterance; a detector extended by an ORDINAL/BACK-REFERENCE class has learned the family.

Three classes are added to the four NC 20 ratified:

- **P1a — ORDINAL / BACK-REFERENCE.** A positional determiner over a **placeholder head**:
  *"the previous one"*, *"the second one"*, *"the first option please"*, *"the last one"*,
  *"same thing"*. The position is only meaningful against an enumeration a prior turn supplied.
- **P1b — ELLIPTICAL FOLLOW-UP.** A wh-word standing alone with **no predicate of its own**:
  *"why?"*, *"how many?"*, *"when?"*, *"how come?"*, *"what did you say"*, *"more details
  please"*. The utterance carries an interrogative and no proposition to interrogate.
- **P1c — UNRESOLVED PRONOUN / REFERENCE.** A **third-person** pronoun or possessive whose
  referent was set in a prior turn: *"when is her appointment"*, *"what is his dose"*,
  *"their address"*.

### The carve-outs, stated so they are not re-derived

- **`my` / `our` / `your` STAY OUT of P1c, exactly as they stay out of `_ANAPHOR`.** They are
  **household-record** dependencies and belong to the store-down ruling — clause **C3** above,
  which this amendment does not touch. *"What is my address"* is still not B1's case.
- **P1c is THIRD PERSON ONLY.** `her/him/his/hers/she/he/they/their/theirs`. This is the line
  between *conversational* state (a referent introduced in a prior turn) and *household record*
  state (a member relationship the store owns).

### P1 ACCEPTANCE — every class twinned BOTH directions

- **P1.1** each of the three classes has at least one twin that **FIRES** (`detected=True`,
  `missing_class` naming that class) with no window.
- **P1.2** each of the three classes has at least one **STANDALONE ANTI-VACUITY twin that does
  NOT fire** — a legitimate utterance carrying the class's own surface marker that answers on
  its own. **This is the ruling's explicit requirement, per class, not once globally.** The
  twins ratified here:
  | class | anti-vacuity twin | why it must answer |
  |---|---|---|
  | **P1a** | *"what is the first day of the week"*, *"when is the next trash pickup"* | an ordinal over a **real head noun** is not a back-reference |
  | **P1b** | *"why is the sky blue"*, *"how many days until Christmas"* | a wh-word **with a predicate** is a whole question |
  | **P1c** | *"when is Sarah's appointment"*, *"Sarah is coming Tuesday — when is her appointment?"* | a referent **named in this same turn** is not missing state |
- **P1.3** the **SAME-TURN ANTECEDENT** case in P1.2's third row is normative, not decorative:
  a pronoun whose antecedent appears **earlier in the same utterance** resolves, and B1 must
  not fire. A detector that fires there has stopped reading its own subject — *missing* state.
- **P1.4** the existing anti-vacuity five (**C1**) still answer, unchanged, and **R3.3 remains
  a hard gate**: a detector failing them fails this REQ whatever else passes.
- **P1.5** the reason string names **which class**, as R3.1 already requires.

## RULING 2 — THE PLEONASTIC-IT EXEMPTION, AND WHY IT IS DELIBERATELY NARROW

**F2 is the exact cost of an exact-match guard.** NC 20's anti-vacuity check matches the five
ratified **strings**; the SIXTH form of a ratified question (*"what time is it now"* — one word
longer than *"what time is it"*) falls through to `_ANAPHOR`, where `\bit\b` catches an *it*
that refers to nothing at all. NC 21 measured the consequence precisely: **the streaming voice
path deterministically clarifies a standalone weather question.**

**The exemption is for PLEONASTIC "it" — the grammatical dummy subject of weather, time and
environment predicates.** It is not a general softening of `\bit\b`, and the ruling says
NARROW twice over: narrow by construction, and twinned against real referential *it*.

- **P2.1** a **pleonastic frame** — weather / time / ambient-environment predicate — **ANSWERS**:
  *"is it raining"*, *"what time is it now"*, *"is it cold outside"*, *"is it going to snow"*.
- **P2.2** a **referential** *it* about a prior referent **STILL HOLDS**: *"is it still active"*,
  *"is it ready yet"*, *"can you send it"*. **This twin is the ruling's own test of narrowness**
  — an exemption that also released these would have widened `it` into meaninglessness.
- **P2.3** the exemption is a **CLOSED, VISIBLE list of predicates**, not an open heuristic, and
  it is stated in the code as such. **Widening it is a ruling, not a refactor** — the same
  sentence `medical_intent.py` already carries about its own lexicon.
- **P2.4** the exemption does **not** depend on `is_local_now_query`'s clock shortcut. F2 proved
  the shortcut masks *"what time is it now"* on the live path and **does not mask "is it
  raining"** — so the fix must hold at the detector, where both are the same failure.

## RULING 3 — DEFERRAL, RECORDED SO IT IS NOT ORPHANED. NOTHING IS BUILT FOR IT HERE.

**The finding being deferred is NC 21's F4**, in its own measured words: on the streaming path a
parked write's confirmation question is answered *"yes"*, and **B1 clarifies the "yes"** as a
bare assent, so the parked fact can never be confirmed by voice there. `check_spoken_confirmation`
runs only inside `_governed_turn`, which the streaming path does not call.

> **Bill's ruling, verbatim: "Pending-write 'yes': NOT in scope — A4 owns confirmation precedence/
> routing. Record the deferral in the REQ so it is not orphaned; build nothing for it here."**

- **P3.1 NC 25 BUILDS NOTHING FOR F4.** No precedence rule, no routing change, no exception
  carved into `_BARE_ASSENT`. A bare *"yes"* with no window is still a B1 detection after this
  amendment, exactly as before it.
- **P3.2 THE OWNER IS NAMED: A4 — confirmation precedence and routing.** The deferral points at
  the name Bill gave it.
- **P3.3 HONEST LIMIT ON P3.2, so the pointer is not read as a link it is not:** **no document
  defining an "A4" workstream is resolvable in this lane's `docs/` at `04a63f8`** — searched,
  not assumed. The A-numbers that *are* on disk here are `REQ_CEILING_ACCEPTANCE` rows, which
  are a different series and not this. **This is recorded as a reconciliation item, not treated
  as a reason to widen scope:** the ruling is unambiguous about what NC 25 does, which is
  nothing.
- **P3.4** the pre/post distinction NC 21 recorded stays attached to the deferral, because it
  decides how urgent this is: **pre-B1 that "yes" fell through to the model and also never
  confirmed** — and generated. **B1 made an existing dead end deterministic and audible; it did
  not create it.** F4 is a real defect and it is not a B1 regression.

## RULING 4 — NORMALIZE FOR CLASSIFICATION ONLY. BOTH HALVES ARE TWINNED.

**F6 measured a class boundary drawn by keyboard habit**: `_BARE_ASSENT` ends `[.!?]?$`, which
allows **at most one** trailing character, so *"ok"* and *"ok!"* are held while *"ok!!"*,
*"yes,"*, *"yes…"* and *"sure —"* pass. Typed turns carry punctuation; ASR mostly does not. The
same word therefore lands in two different classes depending on the modality's punctuation
habits — which is precisely what **D3** forbids: *the modality is a field, never a different
answer.*

**The ruling has two halves and they pull in opposite directions, which is why it twins both.**

- **P4.1 CLASSIFICATION HALF.** Trailing punctuation and surrounding whitespace are **normalized
  before classification**: *"ok"*, *"ok!!"*, *"ok…"*, *"ok ."* and *"OK!?"* all reach the same
  `missing_class`. Normalization is **trailing-only** — it must not reach inside the utterance,
  because *"how many?"* and *"how many"* differ only at the tail while *"do that, again"* is a
  different string in a way that is not punctuation habit.
- **P4.2 RECORD HALF — THE ORIGINAL STAYS VERBATIM.** Normalization exists **only** inside the
  classifier. It must not propagate into what is recorded:
  - **P4.2a** `detect()` **does not mutate its input** and does not return a normalized string;
    the caller's utterance object is byte-identical after the call.
  - **P4.2b** the audit record's `query_hash` is computed over the **ORIGINAL** utterance, so
    two turns that classify identically remain **distinguishable in the record**. A record that
    hashed the normalized form would have quietly merged two different things a member said.
  - **P4.2c** **E1 is untouched**: still no raw utterance in the record. "Verbatim in the
    epistemic/audit record" means the record is derived from the ORIGINAL, not that the original
    is written into it — the two clauses are compatible and both hold.
- **P4.3** both halves are twinned **in the same test file**, adjacent, so a later edit cannot
  satisfy one and silently drop the other.

## RULING 5 — MEDICAL ASSERTIONS ARE GOVERNED BY STRUCTURE. THE LEXICON SUPPLEMENTS.

**Authority note:** the split itself is specified by `REQ_KERNEL_GOVERNED_TURN` Amendment 2
(NC 15's ruling) and implemented in `harness/medical_intent.py`. Ruling 5 amends **that
boundary**, and is recorded here because this batch is where Bill ruled it and because
**Amendment 1 already carried a medical clause into this REQ** (R2, the class-(a) egress
inherit). `REQ_KERNEL_GOVERNED_TURN` is cross-referenced so the split's own spec is not orphaned.

**What F7 measured:** *"I am taking lisinopril"* and *"I am not taking lisinopril anymore"* are
**both** `NOT_MEDICAL`, reason `no-medical-lexicon-hit` — a bare drug name is not in the lexicon,
so **both forms bypass medical governance entirely.** The dosage anchor holds under name-mangling
(*"Zervolol 20mg"* → class (a), caught) but drops the moment the dose is absent (*"Zervolol every
morning"* → `NOT_MEDICAL`, flows ungoverned).

**The ruling inverts the boundary.** Recognition today is *lexicon first*: no lexicon hit, no
governance. Bill's ruling makes it *structure first*:

> **the structure, not the lexicon, is the boundary; lexicon supplements.**

- **P5.1 THE STRUCTURAL FRAME IS THE TRIGGER.** First person + a take/assert verb + a
  medication-shaped object is a governed medical assertion **whether or not any word in it is
  known to the lexicon**. *"I take Zervolol"* is caught **by structure alone**.
- **P5.2 BOTH POLARITIES ARE GOVERNED.** *"I take X"* and *"I don't take X"* / *"I am not taking
  X anymore"* both land in the governed class, and **the reason string names the polarity** — a
  negative assertion is still a durable claim about a member's medications, and F7 measured that
  today the two are indistinguishable at the split.
- **P5.3 ANTI-VACUITY IS PART OF THE RULING, NOT A COURTESY.** *"I take the bus"* and *"I take
  notes"* are **NOT** governed as medical. The frame alone would swallow them; an **exclusion
  list of known non-medication objects** is what keeps the product usable. **That is the sense
  in which "lexicon supplements":** it no longer decides what IS medical — it carves out what
  is not.
- **P5.4 QUESTION-SHAPE-FIRST SURVIVES (A2-5).** *"Do I take Zervolol?"* is a `MEDICAL_QUERY`,
  never an assertion. The structural frame must be evaluated **after** the question test, or
  ruling 5 would silently repeal *"no categorical refusal of first-person medical."*
- **P5.5 THE FAILURE DIRECTION IS NAMED, NOT HIDDEN.** An unknown object outside the exclusion
  list is treated as a medication — so *"I take the ferry"* would be governed as a medical
  assertion. **That cost is a confirmation prompt, not a leak, and it is the correct direction
  to be wrong in** for a rule whose whole purpose is that unrecognized drug names stop escaping
  governance. It is recorded here so that a later reader meets it as a decision rather than a
  bug, and so widening the exclusion list is understood as the maintenance this design requires.
- **P5.6 R2 INHERITS AUTOMATICALLY AND MUST BE TWINNED.** A structurally-caught class (a)
  assertion is a class (a) assertion, so Amendment 1's **R2.1** applies to it: it is **refused at
  web egress with no socket opened**. An invented drug name must not be governed at the kernel
  and ungoverned at egress.
- **P5.7 NC 15's TWINS MUST NOT REGRESS.** `eval/test_nc15_medical_intent_split.py` passes
  unchanged. Widening recognition must not re-tier anything the split already classified.

---

## DISPATCH-LEVEL ACCEPTANCE (Bill's, verbatim)

> **ACCEPTANCE: every class twinned both directions; NC 20's 26 + NC 21's probe set re-run —
> NC 21's F1/F2/F6/F7 probes must now land in their ruled classes; zero new suite failures by
> set comparison.**

- **X1** every class above — the three new dependency classes, the pleonastic exemption, the
  punctuation normalization, and the structural medical frame — is twinned **both directions**:
  one twin that fires, one standalone/anti-vacuity twin that does not.
- **X2 NC 20's 26 twins re-run and still pass**, at the commit this lands on.
- **X3 NC 21's probe set re-run**, and the **F1, F2, F6 and F7 probes land in their ruled
  classes** — F1's nine detected, F2's two released, F6's punctuation variants agreeing with
  their bare forms, F7's positive/negative/invented forms governed.
- **X4 ZERO NEW SUITE FAILURES BY SET COMPARISON — not by count.** The before and after failure
  **sets** are compared by name; a count that matches while the membership changed is not a pass.
  The service state is stated with every number (this lane's graph 7693 has no listener, which is
  its honest default and the environment NC 21 measured in).

## SCOPE — THE CONTESTED SEAM, AND HOW IT RESOLVED MID-DISPATCH

**AT CLAIM TIME (`074a286`, 06:53 MT) rulings 1, 2 and 4 were BLOCKED.** All three land in
exactly one file, `harness/unresolved_reference.py`, and **NC 22 held that file mid-flight** —
uncommitted at `04a63f8`, named in its hand-written `.hip-scope`, edited two minutes before
NC 25 ran its machine gate. Per this dispatch's own COORDINATE clause — *queue behind or build
on their landed state, never edit the same seam concurrently* — **NC 25 claimed them as
queued**, and said so on the board rather than editing around another lane's uncommitted lines.
NC 24 reached the same conclusion independently for F3/F5 and claimed DOCS ONLY (`57e7e2b`):
**three dispatches in one morning found the same file held by the same in-flight build.**

**THE BLOCK CLEARED DURING THIS DISPATCH. NC 22 LANDED AT `0c7b6ee`** (board row closed at
`86c80b4`), leaving the `~/hip-nc2` tree clean. **NC 25 therefore takes the second branch of
the same clause — BUILD ON THEIR LANDED STATE — and builds rulings 1, 2 and 4 after all.**
The queue was real, it was recorded, and it lasted about twenty minutes; the record is kept
because the board row and the claim commit both assert the blocked state, and a reader meeting
those must be able to see what changed rather than conclude one of them was wrong.

**What NC 22's landing changes for THIS amendment, materially and not just procedurally:**
**F3 is repaired.** `kernel.governed_decision` now passes `episode.conversation_window()` as
`window=`, so **the R4 window is no longer inert in production** — the condition NC 21 measured
as *"B1 sees every turn as windowless, forever."* Every twin below therefore asserts against a
detector whose release path (*prior turn present → B1 does not fire*) is **reachable from a
production caller for the first time**, which is a stronger test than NC 20's twins could run.

**Ruling 5 was never blocked** (`harness/medical_intent.py`: not modified, not in NC 22's
scope). **Ruling 3 builds nothing, by instruction.** This amendment covers all five rulings.

**Status of this REQ is unchanged by this amendment: it is not ruled MET here.** Sessions report
readiness; Bill rules.

---

# AMENDMENT 3 — WIDEN THE MEDICAL-ASSERTION FRAMES (NC 26, 2026-08-15)

**AMENDED, NOT REPLACED.** Everything above stands. **Filed BEFORE the first line of NC 26
code**, per Requirements Discipline item 8. Reconciled against `bfb09df` (NC 25's landing).

**THIS AMENDMENT CLOSES NC25-F1, AND THE ROUTE IT TOOK IS THE POINT.** NC 25 built structure-first
medical recognition for the take-forms and then **refused to extend it**, filing the `on`-frame as
a named residual: *"extending the structure to `on` / `started` / `switched to` is the same KIND of
decision Bill just made and is his to make, so it is reported rather than taken."* Bill has now
made it. A session declined to widen a boundary on its own authority, said so in writing, and the
ruling followed — which is the mechanism working, not a delay.

## THE RULING — VERBATIM

> **add the frame family**
>
> ```
>   I'm on <candidate medication>
>   I'm taking <candidate medication>
>   I started <candidate medication>
>   I stopped <candidate medication>
> ```
>
> **Constraints:**
>
> **1. The VERBS are never medical triggers by themselves — "I'm on vacation", "I'm taking the
> bus", "I started school", "I stopped at the store" remain NOT_MEDICAL.**
>
> **2. Unknown-but-plausible medication object -> the RESTRICTIVE path (medical governance /
> clarification), never permissive classification. Fail toward asking.**
>
> **3. Original utterance preserved verbatim in the record (NC 25's normalization-for-
> classification-only rule inherits).**

## WHAT IS ALREADY DONE — FRAME 2 IS NC 25's, AND IS NOT REBUILT

**`"I'm taking <X>"` ALREADY LANDS IN GOVERNANCE at `bfb09df`.** NC 25's take-frame matches a
first-person subject followed by any of `take|takes|taking|took`, so *"I'm taking lisinopril"* is
already class (a) with its polarity named. **NC 26 therefore adds THREE frames, not four** — `on`,
`started`, `stopped` — and **twins frame 2 rather than reimplementing it**, so there is one
implementation of the take-verb and no second copy to drift. Requirements Discipline item 11's
principle applied to code: check what is already traced before re-tracing it.

## Q1 — THE ONE INTERPRETIVE CALL IN THIS AMENDMENT, FLAGGED FOR OVERRULE

**Constraint 2 says an unknown-but-plausible object takes "the RESTRICTIVE path (medical
governance / clarification)" and to "fail toward asking". Both class (a) and class (b) are
governance, and the ruling names *clarification*, which is class (b)'s name in this codebase.**
NC 26 reads it as a **two-tier** rule, and states the alternative so it can be overruled in one
line:

| verb evidence | object evidence | class |
|---|---|---|
| **take / taking** (NC 25's frame) | any non-excluded object | **(a) FACT_ASSERTION_WRITE** — unchanged from `bfb09df` |
| **on / started / stopped** | **corroborated** — a dosage, a brand-shaped token, or a medical lexicon hit in the turn | **(a) FACT_ASSERTION_WRITE** |
| **on / started / stopped** | **uncorroborated but not excluded** | **(b) AMBIGUOUS_WRITE** — deterministic clarification, **NO model, NO write** |
| any | **excluded** (`_NOT_A_MEDICATION`) | **NOT_MEDICAL** |

**WHY THE TIER, AND WHY THE ASYMMETRY WITH NC 25 IS PRINCIPLED RATHER THAN CONVENIENT:**

1. **Verb specificity is real and measurable in ordinary English.** *"I take X"* with an
   unfamiliar noun almost always means a medication. *"I'm on X"*, *"I started X"*, *"I stopped
   X"* are general-purpose and carry vacations, schools, jobs, buses and diets as readily as
   drugs. **The new frames are weaker evidence, so they get the more cautious destination.**
2. **Class (b) is the more restrictive of the two, not the softer one.** (a) parks the fact and
   asks for confirmation; **(b) writes nothing at all**, takes no model call, and returns a fixed
   clarification. For an object we cannot corroborate, writing nothing is the conservative answer
   and is exactly *"fail toward asking"*.
3. **It is independently forced by the twins.** NC 25's twins assert *"I take lisinopril"* is
   class (a). A uniform rule sending every uncorroborated object to (b) would regress them, and
   this dispatch is required to keep NC 15's and NC 25's medical twins green.

**THE ALTERNATIVE, STATED PLAINLY: make all four frames behave like `take` — every non-excluded
object goes to (a).** That is simpler and more uniform. It is not chosen because it treats *"I'm
on Zoom"*-shaped turns with the same confidence as *"I take lisinopril"*, and because it would
make constraint 2 redundant with constraint 1. **One line from Bill flips it.**

## P6 — ACCEPTANCE

### P6.1 THE FRAME FAMILY

- **P6.1a** each of the three new frames — `on`, `started`, `stopped` — recognises a medication
  object and routes it into governance, with synonyms held to a **visible, closed** list
  (`quit`, `discontinued`, `began`, `come off`) rather than an open heuristic.
- **P6.1b** frame 2 (`taking`) is **twinned, not rebuilt**, and the twin names NC 25 as its owner.
- **P6.2** the reason string **names the frame and the polarity**, so a stop reason stays
  actionable and the record shows which shape fired.

### P6.3 CONSTRAINT 1 — THE VERBS ARE NEVER TRIGGERS BY THEMSELVES

The four utterances Bill named are **binding twins**, not examples:

| utterance | must be | why it is not medical |
|---|---|---|
| *"I'm on vacation"* | `NOT_MEDICAL` | excluded object |
| *"I'm taking the bus"* | `NOT_MEDICAL` | excluded object (already, at `bfb09df`) |
| *"I started school"* | `NOT_MEDICAL` | excluded object |
| *"I stopped at the store"* | `NOT_MEDICAL` | **no direct object at all** — `at` is a preposition |

- **P6.3a** *"I stopped at the store"* is excluded **STRUCTURALLY, not by stoplist**: a frame verb
  followed by a **preposition** heads an adjunct, not an object. This generalises to *"I stopped by
  the pharmacy"* and *"I stopped for gas"*, which a word list would have to enumerate one by one.
  **A structural exclusion is the right answer to a structural ruling.**
- **P6.3b** the exclusion list grows to carry the ordinary objects of the three new verbs
  (vacation, school, work, leave, a diet, a call, and so on). **Widening it remains maintenance
  rather than a ruling**, on NC 25's stated grounds: an exclusion list only ever RELEASES turns.

### P6.4 CONSTRAINT 2 — FAIL TOWARD ASKING

- **P6.4a** an unknown-but-plausible object is **never** `NOT_MEDICAL`. Permissive classification
  is the failure this constraint forbids.
- **P6.4b** it lands in **(b) AMBIGUOUS_WRITE** per Q1 — clarification, **no model call, no
  write** — and a twin asserts all three properties, not just the class.
- **P6.4c** an **invented** name (*"I'm on Zervolol"*) is caught **by structure alone**, with its
  absence from every lexicon and the absence of any dosage **verified as preconditions inside the
  twin** rather than asserted in prose.

### P6.5 CONSTRAINT 3 — THE ORIGINAL SURVIVES

- **P6.5a** `medical_split` **does not mutate its input** and classification is punctuation-
  tolerant: *"I'm on Zervolol"* and *"I'm on Zervolol!!"* classify identically. **NC 25's ruling 4
  inherits**: normalization is for classification only.
- **P6.5b** the reason string carries the **object token and the frame**, never a rewritten or
  normalized copy of the utterance — so nothing downstream can mistake the classifier's working
  form for what the member actually said.
- **P6.5c** question-shape-first still wins: *"I'm on Zervolol?"* is a `MEDICAL_QUERY`. **A2-5 is
  not weakened by a third widening.**

### P6.6 TWO EXISTING TWINS ARE RETIRED BY THIS RULING — DELIBERATELY, AND WITH ANNOTATION

**This is the only place in the batch where a green twin must go red, and it is the twin doing
its job rather than failing at it.**

1. **NC 15's `test_the_recognition_boundary_is_the_documented_one`** asserts *"I'm on metformin"*
   is `NOT_MEDICAL`. Its own docstring states its purpose: *"If someone widens the lexicon, this
   test makes the widening a visible decision instead of drift."* **This ruling is that decision.**
2. **NC 25's `test_R5_THE_NAMED_RESIDUAL_the_on_frame_is_still_out_of_scope`** asserts the same
   thing and says *"if it ever starts failing, someone widened the structure without a ruling."*
   **It started failing because someone widened the structure WITH one.**

- **P6.6a** both are **updated to the newly ruled behaviour, never deleted**, and each keeps its
  **old assertion visible** in the test body with the ruling that changed it — the pre-authorized
  correction class's rule: *annotate the correction; never silently patch.*
- **P6.6b** every OTHER NC 15 and NC 25 medical twin passes **unchanged**. A widening that quietly
  re-tiered a neighbouring case would have failed this amendment.

### P6.7 THE SUITE

- **P6.7** zero new suite failures **by SET comparison, not by count**, taken at a single HEAD
  with the service state stated. Same method NC 25 used, including the requirement that the
  arithmetic between the two runs closes exactly against the number of twins added.

**Status of this REQ is unchanged by this amendment: it is not ruled MET here.** Sessions report
readiness; Bill rules.

---

# AMENDMENT 4 — THIRD-PERSON MEDICAL FRAMES, THE SUBJECT BOUNDARY, AND Q1 RULED (NC 31, 2026-08-15)

**AMENDED, NOT REPLACED.** Everything above stands. **Filed BEFORE the first line of NC 31
code**, per Requirements Discipline item 8. Reconciled against `0ee55fb` (NC 26's landing).

**THIS AMENDMENT CLOSES NC26-F2 AND ANSWERS AMENDMENT 3's Q1.** Both were filed by sessions that
declined to decide them; both are now Bill's. That is the second time in this sequence the same
mechanism has run — NC 25 filed NC25-F1, NC 26 built it; NC 26 filed NC26-F2 and Q1, NC 31 builds
them.

## THE RULINGS — VERBATIM

> **1. THIRD-PERSON FRAMES: add**
>
> ```
>      X is on <candidate medication>
>      X is taking <candidate medication>
>      X started <candidate medication>
>      X stopped <candidate medication>
> ```
>
> **Same anti-vacuity guardrails: "my mother is on vacation", "Sam started school" remain
> ordinary. Twins per frame: recognized drug, invented drug (structure catches it), negated
> form, the non-medical controls.**
>
> **2. BILL'S BOUNDARY, structural: medical-frame detection establishes SENSITIVITY/WRITE
> SEMANTICS ONLY — it does NOT establish subject and does NOT authorize a write about the named
> person. "my mother" / "Maya" / any third party still goes through the normal subject-
> resolution, authority, and park-and-confirm machinery, which FAIL CLOSED. Twin the prohibited
> shortcut explicitly: a recognized third-person frame must NOT auto-assign the speaker (or the
> named person) as subject — prove the resolution step still runs and an unresolvable subject
> refuses.**
>
> **3. AMENDMENT 3 Q1, ruled: uncertain medication object -> deterministic clarification ("do
> you mean a medication?"), NEVER a pending write from uncertainty alone. Record the ruling in
> the REQ; twin: ambiguous object -> clarification, 0 model calls, 0 parked rows.**

---

## RULING 3 FIRST, BECAUSE IT SETTLES A QUESTION THIS REQ WAS ALREADY CARRYING

**Amendment 3's Q1 is now closed: CLARIFY-AS-BUILT.** Amendment 3 read constraint 2 as a two-tier
rule and stated the uniform alternative so it could be overruled in one line. **It is not
overruled.** An uncertain medication object takes the deterministic clarification, and Bill's
addition sharpens it further than the original tier did:

> **NEVER a pending write from uncertainty alone.**

- **P7.1** Amendment 3's tier **STANDS UNCHANGED**. `on` / `started` / `stopped` with an
  uncorroborated object remain **class (b) AMBIGUOUS_WRITE**.
- **P7.2 THE NEW CLAUSE IS THE PROHIBITION, AND IT NEEDS ITS OWN PROOF.** *"Never a pending write
  from uncertainty alone"* is a claim about the **park machinery**, not about the class label —
  so a twin that only asserts `cls is AMBIGUOUS_WRITE` does not discharge it. **The twin must
  assert 0 parked rows**, read from `harness.confirmation_gate` (`peek` / `clear_all`), and
  **0 model calls**, read from `harness.model_calls`.
- **P7.3** the existing kernel gate is the mechanism, and its adequacy is asserted rather than
  assumed: `kernel.governed_turn` gates class (b) and returns **before `turn_impl` is ever
  called**, so no park can be registered on that path. **If a later change moves the gate below
  the implementation call, P7.2's twin fails** — which is the point of measuring the park table
  rather than the class.

## RULING 1 — THE THIRD-PERSON FRAMES

- **P7.4** the four frames — `X is on`, `X is taking`, `X started`, `X stopped` — are recognized
  with **the same object guardrails NC 26 built**: the exclusion list, the preposition/adjunct
  test, the generic-medical-noun deferral, and the whole-noun-phrase scan. **They are reused, not
  reimplemented** — one definition of "what counts as a medication object" for both persons.
- **P7.5** the subject slot accepts a **third-party reference**: a kinship term with or without a
  possessive (*"my mother"*, *"his father"*, *"grandma"*), a third-person pronoun, or a
  capitalised given name. **A first-person subject before the verb disqualifies the frame** — the
  first-person path (NC 25/26) owns those turns.
- **P7.6 ANTI-VACUITY, per Bill's clause:** *"my mother is on vacation"* and *"Sam started
  school"* remain `NOT_MEDICAL`. Twins per frame: **recognized drug, invented drug, negated form,
  and the non-medical control.**
- **P7.7 THE TIER APPLIES IN THIS PERSON TOO,** for the same reason and by ruling 3:
  corroborated object → recognized medical; **uncorroborated object → clarification, never a
  pending write**.

## RULING 2 — THE SUBJECT BOUNDARY. THIS IS THE HEART OF THE AMENDMENT.

**What the ruling forbids, stated as the property to be proven:** recognition of a medical frame
must establish **sensitivity and write semantics** and **nothing about who the fact is about**.

- **P7.8 A RECOGNIZED THIRD-PERSON FRAME MUST NOT PRODUCE A FIRST-PERSON WRITE CLASS.** It lands
  in **`MEDICAL_OTHER`** — the existing third-party path, whose trust-ladder and park-and-confirm
  machinery already own it — **never `FACT_ASSERTION_WRITE`**, which is the first-person
  park-and-confirm class.
- **P7.9 THE SHORTCUT MUST BE STRUCTURALLY IMPOSSIBLE, NOT MERELY UNTAKEN.** `MedicalSplit`
  carries exactly two fields, `cls` and `reason`, and **neither is a subject**. The twin asserts
  the dataclass's own field set, so no downstream caller can read a subject off a classification
  even by mistake. **A behavioural twin proves what the code does today; a structural one proves
  what it cannot do.**
- **P7.10 THE RESOLUTION STEP MUST BE PROVEN STILL TO RUN.** `resolve_member()` lives downstream
  of the split (`server/voice_orch.py:2844`, inside `process_governed_turn`). A recognized
  third-person frame is **not** gated at the kernel, so it reaches that path. The twin proves the
  turn arrives there rather than being answered by the classifier.
- **P7.11 AN UNRESOLVABLE SUBJECT MUST REFUSE, AND THE MEDICAL FRAME MUST NOT BUY A BYPASS.** A
  third-person medical frame on a turn whose identity cannot be resolved — a claim contradicting
  an authenticated principal — **refuses**, with **no model call**. The twin runs the same
  utterance with and without the identity conflict and shows the medical frame changes nothing
  about the refusal.

### THE DEFECT THIS RULING EXPOSES, MEASURED AT CLAIM TIME AND FIXED HERE

**`"my mother takes metformin 500mg"` classifies as `FACT_ASSERTION_WRITE`, reason
`first-person+assert-verb:takes+dosage:500mg`.**

`_FIRST_PERSON` matches the **possessive `my`**, so a turn about the speaker's *mother* is read as
a first-person medical assertion with write semantics. The same holds for *"my mother is on
lisinopril 10mg"* and *"my wife started lisinopril 10mg"*. **Name subjects route correctly**
(*"Maya takes metformin 500mg"* → `MEDICAL_OTHER`), so the gap is precisely the
**possessive-kinship subject**.

**This pre-dates NC 25 and NC 26** — it is NC 15's `_FIRST_PERSON` including `my`/`me` — and it is
**exactly the shortcut ruling 2 forbids**, arriving through the subject test rather than through
the frames.

- **P7.12** the fix is **subject-directed, not verb-directed**: a medical assertion whose subject
  is a third party is `MEDICAL_OTHER` **whatever the verb**, so the repair covers `takes` and
  every other verb rather than only the four newly ruled frames.
- **P7.13 HONEST BOUND ON THE SEVERITY, so this is not overstated.** Class (a) is not itself a
  write: it passes through to the normal governed path, whose park-and-confirm machinery resolves
  the subject downstream. **What is measured here is a wrong CLASSIFICATION asserting first-person
  subject semantics; whether a wrong-subject write actually lands is downstream and is NOT
  measured by this dispatch.** The classification is wrong either way — ruling 2 says the split
  must not assert subject at all — but the blast radius is stated rather than assumed.

## P7.14 — ACCEPTANCE

- **P7.14a** twins **per frame**: recognized drug, invented drug caught by structure, negated
  form, and the non-medical control (ruling 1's own list).
- **P7.14b** the **no-shortcut proof**: P7.8 (no first-person write class), P7.9 (structural —
  no subject field exists), P7.10 (resolution still runs), P7.11 (unresolvable subject refuses).
- **P7.14c** ruling 3's twin: ambiguous object → clarification, **0 model calls, 0 parked rows**,
  the last two measured at their instruments.
- **P7.14d NC 26's FULL TWIN SET RE-RUN GREEN**, and NC 15's and NC 25's with it.
- **P7.14e** zero new suite failures **by SET comparison**, single HEAD, service state stated.

**Status of this REQ is unchanged by this amendment: it is not ruled MET here.** Sessions report
readiness; Bill rules.
