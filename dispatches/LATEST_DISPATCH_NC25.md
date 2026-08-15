# DISPATCH_NC25 — the B1 POLICY BATCH: Bill's rulings 1-5. Classes not phrases, a narrow pleonastic-it exemption, punctuation normalized for classification only, and medical recognition inverted to STRUCTURE-first
Status: **BUILT** — code landed `bfb09df` (`~/hip-nc2` @ `nc-b0`); REQ Amendment 2 landed `c56c7a9` (`~/hip-roadmap` @ `roadmap`)
Reconciled-Against: `bfb09df`, over base `422d330` — read from the machine, not remembered; machine gate and lane preflight both passed
Dispatch: NC 25
Date: 2026-08-15 07:35 (Mountain)
REQ: **`REQ_UNRESOLVED_REFERENCE_DETECTOR__b1-structural-stop-on-missing-conversational-state__v20260814_2056.md`, AMENDMENT 2** — filed at `c56c7a9` **before the first line of code**, per Requirements Discipline item 8. Ruling 5 additionally cross-references `REQ_KERNEL_GOVERNED_TURN`, which specifies the medical split itself.
Type: **BUILD** (product code + twins), preceded by a docs-only amendment.

---

## 0. RECAP

```
NC 25 — B1 POLICY BATCH: Bill's rulings 1-5
COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING
```

**One sentence:** all five rulings are discharged — three new dependency **classes** (not nine
phrases), a pleonastic-`it` exemption narrow on both sides, punctuation normalized for
classification only with the original preserved in the record, and medical recognition
**inverted from lexicon-first to structure-first** so an invented drug name is governed with no
list entry anywhere — with **110 new twins, every class twinned both directions, and a suite
failure set byte-identical to baseline at a single HEAD**.

## 1. WHAT WAS ASKED, AND WHERE EACH RULING LANDED

| ruling | subject | landed in | NC 21 finding answered |
|---|---|---|---|
| **1** | dependency **CLASSES**, not a phrase list | `harness/unresolved_reference.py` | **F1** — nine phrasings undetected |
| **2** | narrow pleonastic-`it` exemption | `harness/unresolved_reference.py` | **F2** — two standalones wrongly held |
| **3** | pending-write "yes" — **NOT in scope** | **nothing built, by instruction** | **F4** — deferred to A4, recorded |
| **4** | punctuation normalization, classification only | `harness/unresolved_reference.py` | **F6** — punctuation flips the class |
| **5** | medical assertions **structurally** | `harness/medical_intent.py` | **F7** — lexicon-shaped bypass |

## 2. RULING 1 — THE DISTINCTION THAT IS THE WHOLE FIX

**F1 measured nine dependency phrasings passing undetected. Nine phrasings are not nine bugs.**
They are **three missing shapes**, and a detector patched with nine literals would have learned
nine utterances instead of three families — the same mistake in a smaller font. Bill's ruling
says this in its first four words (*"DEPENDENCY CLASSES, not a phrase list"*), and the build
follows it:

| new class | shape | example |
|---|---|---|
| `ordinal-back-reference` | positional determiner over a **placeholder head** | *"the previous one"*, *"the second one"*, *"same thing"* |
| `elliptical-follow-up` | interrogative or elaboration request with **no proposition of its own** | *"why?"*, *"how many?"*, *"more details please"* |
| `unresolved-pronoun-reference` | **third-person** pronoun whose referent came from a prior turn | *"when is her appointment"* |

**THE DISCRIMINATOR IS WHAT KEEPS ANTI-VACUITY ALIVE.** An ordinal is a back-reference only
when it governs a **placeholder** head — so *"the first day of the week"* and *"the next trash
pickup"* put an ordinal in front of a real head noun and answer on their own. A wh-word is an
ellipsis only when it stands **alone** — so *"why is the sky blue"* is a whole question. Each
of the three classes carries its own standalone twin, which is the ruling's explicit per-class
requirement rather than one global gesture.

**`my` / `our` / `your` STAY OUT.** They are household-record dependencies and remain the
store-down ruling's case — clause **C3**, untouched. *"What is my address"* is still not B1's.

**P1.3 — the same-turn antecedent.** *"Sarah is coming Tuesday — when is her appointment?"*
resolves **inside its own turn** and B1 does not fire; *"when is her appointment"* alone does.
A detector that fired on the first has stopped reading its own subject, which is **missing**
state. Sentence-initial capitalisation is not evidence of a name, so a stoplist carries the
words that get capitalised for position rather than for reference.

## 3. RULING 2 — NARROW ON BOTH SIDES, WHICH IS WHY IT IS SAFE

F2 measured the cost of an exact-match guard: *"what time is it now"* is **one word longer**
than the ratified *"what time is it"*, so it fell through to the anaphor pattern where `\bit\b`
caught an `it` that refers to nothing. NC 21's sentence is the one that matters: **the live
streaming path deterministically clarified a standalone weather question.**

The exemption releases `it` **only** when both hold:

1. the turn matches a **closed, visible** weather / time / ambient predicate list, and
2. `it` is the **sole** anaphor present.

**Clause 2 is what stops the exemption becoming a hole.** *"Is it raining over by that one"*
still holds, because a weather word must not launder a turn that also carries a real referent.
*"Is it still active"* still holds — that twin is the ruling's own test of narrowness.

**The residual is named rather than hidden:** *hot*/*cold*/*dark* can describe a prior referent
("is it hot?" about soup). The ambient reading is dominant for a bare `it` and the cost of being
wrong is one answered turn instead of one clarification — but it is a judgement, and the module
says so where a reader will meet it.

## 4. RULING 3 — THE DEFERRAL, AND THE TWIN THAT ASSERTS AN ABSENCE

Bill: *"Pending-write 'yes': NOT in scope — A4 owns confirmation precedence/routing. Record the
deferral in the REQ so it is not orphaned; build nothing for it here."*

**Nothing was built.** A bare *"yes"* with no window is still a B1 detection, exactly as before.
The REQ carries the deferral (P3.1-P3.4) and **a twin asserts the absence of the change** — if a
later dispatch carves a parked-write exception into the assent class without going through A4,
`test_R3_a_bare_YES_is_STILL_a_B1_detection_because_nothing_was_built_for_F4` is what notices.

NC 21's pre/post distinction is kept attached, because it decides urgency: **pre-B1 that "yes"
fell through to the model and also never confirmed** — and generated. **B1 made an existing dead
end deterministic and audible; it did not create it.**

## 5. RULING 4 — BOTH HALVES, TWINNED ADJACENTLY

F6: `[.!?]?$` allowed **exactly one** trailing character, so *"ok"* and *"ok!"* were held while
*"ok!!"*, *"yes,"*, *"yes…"* and *"sure —"* passed. Typed turns carry punctuation and ASR mostly
does not, so **the same word landed in two classes by modality** — which is what D3 forbids.

- **Classification half:** normalization is **trailing-only**. It must not reach inside the
  utterance, because *"how many?"* and *"how many"* differ only at the tail while *"do that,
  again"* differs in a way that is not keyboard habit.
- **Record half:** `detect()` does not mutate its input, returns no normalized text, and
  `query_hash` remains the caller's **over the original**. Two turns that classify identically
  stay **distinguishable in the record** — a record that hashed the normalized form would have
  quietly merged two different things a member said. **E1 is untouched: still no raw utterance.**

The two halves are twinned **in the same file, adjacent**, so a later edit cannot satisfy one and
silently drop the other.

## 6. RULING 5 — RECOGNITION INVERTED. THIS IS THE LARGEST CHANGE IN THE BATCH.

**What F7 measured:** *"I am taking lisinopril"* and *"I am not taking lisinopril anymore"* were
**both** `NOT_MEDICAL`, reason `no-medical-lexicon-hit`. The dosage anchor held under
name-mangling (*"Zervolol 20mg"* caught) and **dropped the moment the dose was absent**. A closed
lexicon can only recognise the drugs someone thought to list, and the drugs that matter most are
the ones nobody listed.

**The inversion:** recognition WAS lexicon-first — no lexicon hit, no governance. It is now
**structure-first**: first-person subject + take-verb + medication-shaped object is governed
**whether or not any word is known to any list**.

```
I take Zervolol   ->  fact_assertion_write
                      structural-medication-frame:take+proper-token:Zervolol+polarity:positive
```

*"Zervolol"* is in **no** lexicon in this repository and carries **no** dosage — verified as a
precondition inside the twin itself, not asserted. Only the structure catches it.

**What the lexicon's job becomes.** It no longer decides what IS medical; a new
`_NOT_A_MEDICATION` list carries the ordinary objects of "I take …" so *"I take the bus"* and
*"I take notes"* are not swallowed. **That is the sense in which "lexicon supplements": it
carves out what is not.** Note the asymmetry — widening an exclusion list only ever RELEASES
turns, so it is maintenance, the opposite of widening a recognition lexicon.

**Both polarities, and the reason names which.** *"I don't take X"* is as durable a claim about
a member's medications as *"I take X"*, and F7 measured that the split could not tell them apart
because it saw neither.

**THE FAILURE DIRECTION IS NAMED, NOT HIDDEN.** An object outside the exclusion list is treated
as a medication, so *"I take the ferry"* would be governed as a medical assertion. **That costs
a confirmation prompt, not a leak, and it is the correct direction to be wrong in** for a rule
whose whole purpose is that unrecognised drug names stop escaping governance.

**A regression caught by NC 15's own twins, and what it taught.** The frame first claimed
*"I take pills"* and *"put down that I take medicine for my blood pressure"*, moving both from
class (b) to class (a). **A generic medical noun is a category, not a drug NAME** — it carries
no concrete value and belongs in (b) exactly where NC 15 put it. The frame now defers to
`_MEDICAL` for that judgement rather than keeping a second copy that could drift. **Two NC 15
twins caught this within one run of writing it**, which is the argument for their existence.

## 7. THE ACCEPTANCE, MEASURED

Environment stated with every number: **lane graph 7693 has no listener** — this lane never
stood one up, it is its honest default, and it is the environment NC 21 measured in.
**Preflight: `lane_preflight.py` OK** (hip-nc2 @ nc-b0 writes 7693; `.hip-owns`/`.hip-graph`
agree), **NOT BUSY** (4 connections, all resident services on 7690).

| clause | result |
|---|---|
| **X1** every class twinned **both directions** | **110 new twins**, `eval/test_nc25_b1_policy_batch.py` |
| **X2** NC 20's 26 re-run | **26/26 pass** |
| — NC 15's twins (ruling 5's neighbours) | **20/20 pass**, unchanged |
| — NC 22's and NC 24's suites, run together with the above | **237 passed** across all five files |
| **X3** NC 21's probes re-mapped | below |
| **X4** zero new suite failures **by set comparison** | below |

### X3 — NC 21's probe set, re-run and re-mapped

| probe | NC 21 measured | now | ruled class |
|---|---|---|---|
| **F1** *"the previous one"*, *"the second one"*, *"the first option please"*, *"same thing"* | `detect=False` | **detected** | `ordinal-back-reference` |
| **F1** *"what did you say"*, *"more details please"*, *"why?"*, *"how many?"* | `detect=False` | **detected** | `elliptical-follow-up` |
| **F1** *"when is her appointment"* | `detect=False` | **detected** | `unresolved-pronoun-reference` |
| **F2** *"what time is it now"*, *"is it raining"* | wrongly **held** | **answer** | released, pleonastic |
| **F6** *"ok!!"*, *"yes,"*, *"yes…"*, *"sure —"* | passed | **held with their bare form** | `bare-assent` |
| **F7** *"I am taking lisinopril"*, *"I am not taking lisinopril anymore"*, *"Zervolol every morning"* | `NOT_MEDICAL` | **governed** | `fact_assertion_write` |

**All nine of F1 land in their ruled classes; both of F2 release; all four F6 variants agree
with their bare form; all three F7 forms are governed.**

### X4 — the suite, by SET comparison at a single HEAD

```
BEFORE (422d330, NC 25 reverted):  20 failed, 643 passed, 39 skipped, 21 errors
AFTER  (bfb09df):                  20 failed, 753 passed, 39 skipped, 21 errors
failure+error SET:                 41 entries before, 41 after, diff EMPTY
753 - 643 = 110, exactly the new twins
```

**THE BASELINE WAS RE-TAKEN, AND BOTH ATTEMPTS ARE REPORTED** (pre-authorized correction class:
a check re-run after tracing its own invocation error). The first baseline ran at `0c7b6ee`;
**NC 24 then landed `422d330` mid-dispatch**, adding 14 passing tests, so the first before/after
straddled two lanes' changes and its `+124` did not reconcile against a 110-test file. The
baseline was re-taken at `422d330` with NC 25's three files reverted — **backed up first and
restored byte-identical, verified by `shasum`** — which makes the comparison single-variable and
makes the arithmetic close exactly.

**One line was excluded from the set extraction, and it is named rather than quietly dropped:**
`ERROR    harness.extraction_queue:extraction_queue.py:1109 extraction failed for session
sess-ext` is a captured **logging record**, not a pytest node — it has no `::` node id. It
appeared in one run's captured output and not the other's. The extraction now requires a
path-shaped node id. **Reported because a filter that silently changed a set comparison's answer
would be exactly the kind of confident false statement Requirements Discipline item 13 is about.**

## 8. FINDINGS FILED — 3, NONE BLOCKING

**NC25-F1 — THE `on`-FRAME IS STILL OUTSIDE THE SPLIT, AND THAT IS A HELD SCOPE, NOT A GAP.**
Bill ruled the forms *"I take <medication>"* / *"I don't take <medication>"*. **`"I'm on
metformin"` therefore remains `NOT_MEDICAL`** — NC 15's boundary twin still asserts it, and a
new NC 25 twin records the residual so it cannot become an undiscovered gap. Extending the
structure to `on` / `started` / `switched to` is **the same KIND of decision Bill just made**
and is his to make, so it is reported rather than taken. **This is the single most likely next
ruling in this area.**

**NC25-F2 — NO "A4" WORKSTREAM DOCUMENT IS RESOLVABLE IN THIS LANE'S `docs/`.** Ruling 3 defers
the pending-write "yes" to A4, *confirmation precedence and routing*. Searched, not assumed: the
A-numbers on disk here are `REQ_CEILING_ACCEPTANCE` rows, a different series. The deferral
points at the name Bill gave it, and F4 stays attached to that name — but **the pointer is a
name, not a link**, and reconciling it is a docs item somebody should close before F4 is picked
up. Not treated as a reason to widen scope.

**NC25-F3 — THE NC LANE BOARD ROW IS STILL PIPE-BRICKED (TD-R-194(b) recurrence, fourth
sighting).** The row carries **7 bare pipes against a 6-pipe header**, so FM 25's `claim_lane.py`
refuses every edit to it and NC 22, NC 24 and NC 25 have each hand-edited under the repo lock on
the HA-94 precedent. Each entry is inserted **inside** the existing cell and adds no pipe, so the
malformation is neither worsened nor silently repaired.

**DELIBERATELY NOT FILED AS A NEW TD, and the reasoning is the point:** `TD-R-194(b)` already
describes this exact defect and is **OPEN**. A second row would add a count and no information,
while editing HA-94's existing row to add a tally is the rewrite NC 22 explicitly avoided when
it filed the sibling `TD-R-195` separately. **The recurrence is recorded here, in the dispatch
that hit it, and the register is left alone** — the finiteness rule working as intended rather
than a filing reflex. What is new and worth a reader's attention is only the frequency: three
lanes hand-edited the same bricked row within ninety minutes.

## 9. COORDINATION — THREE LANES IN ONE FILE, AND HOW IT RESOLVED

This is worth recording because it is the process working rather than a near-miss.

**At claim time (`074a286`, 06:53) rulings 1, 2 and 4 were BLOCKED.** All three land in one file,
`harness/unresolved_reference.py`, and **NC 22 held it mid-flight** — uncommitted, in its
hand-written `.hip-scope`, edited two minutes before this dispatch ran its machine gate. NC 25
**claimed them as queued and said so on the board** rather than editing around another lane's
uncommitted lines. **NC 24 reached the same conclusion independently** for F3/F5 and claimed
DOCS ONLY (`57e7e2b`).

**NC 22 then landed (`0c7b6ee`, row closed `86c80b4`)**, so NC 25 took the second branch of the
same COORDINATE clause — *build on their landed state* — and built all four buildable rulings.
**NC 24 landed `422d330` later still.** Both peers' work is committed and untouched; NC 25's
commits carry three files by explicit pathspec.

**That landing also materially changed this dispatch's evidence: NC 22 repaired F3.**
`governed_decision` now passes `episode.conversation_window()` as `window=`, so the R4 release
path — *prior turn present → B1 does not fire* — **is reachable from a production caller for the
first time**, which NC 21 had measured as *"B1 sees every turn as windowless, forever."* Every
window twin here asserts against that repaired seam.

## 10. WHAT I DID NOT DO

- **No F4 work** (ruling 3), and a twin asserts the absence.
- **No F3 or F5 work** — NC 22 and NC 24 own those and both landed during this dispatch.
- **No widening of the medical structure beyond the take-verb family** (NC25-F1).
- **No REQ ruled MET, no acceptance row re-tiered, no baseline changed.** The REQ's `Status:
  PLAN` header was **flagged in place rather than corrected**: NC 20 landed code against it and
  left it at PLAN, and re-tiering is outside the pre-authorized correction classes.

## 11. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Detector policy and the medical split's recognition boundary; no ledger claim's standing
evidence is touched by this dispatch.

## 12. VERIFIED

Machine gate (`bill-ai` / `[REDACTED-MACHINE-NAME]` / `~/hip-nc2` @ `nc-b0`, in sync with
origin). `lane_preflight.py` OK (7693) and NOT BUSY, run before any suite. Claim first
(`074a286`), REQ amendment before code (`c56c7a9`), code after (`bfb09df`). Repo lock held around
each git operation only, never around a survey or a sleep; all three pushes carried no passenger.
`.hip-scope` hand-written in `~/hip-nc2` (TD-R-194(a) again). Every number above is from this
session's runs, with the service state stated.
