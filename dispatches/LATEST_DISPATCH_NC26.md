# DISPATCH_NC26 — widen the medical-assertion frames: three frames added (not four), an unknown object routed to the RESTRICTIVE tier, and two green twins retired by the ruling they were built to force
Status: **BUILT** — code landed `0ee55fb` (`~/hip-nc2` @ `nc-b0`); REQ Amendment 3 landed `e971c29` (`~/hip-roadmap` @ `roadmap`)
Reconciled-Against: `0ee55fb`, over base `bfb09df` (NC 25) — read from the machine; machine gate and lane preflight both passed
Dispatch: NC 26
Date: 2026-08-15 08:01 (Mountain)
REQ: **`REQ_UNRESOLVED_REFERENCE_DETECTOR__...__v20260814_2056.md`, AMENDMENT 3** — filed at `e971c29` **before the first line of code**, per Requirements Discipline item 8.
Type: **BUILD** (product code + twins), preceded by a docs-only amendment.

---

## 0. RECAP

```
NC 26 — widen the medical-assertion frames
COMPLETE WITH FINDINGS — 4 ITEMS FILED, NOTHING BLOCKING
```

**One sentence:** the frame family is in — *"I'm on X"*, *"I started X"*, *"I stopped X"* now
reach medical governance with no lexicon entry anywhere, an object nothing corroborates lands in
**clarification rather than a write**, and the four utterances Bill named as ordinary stay
ordinary — with **63 new twins, 300 passing across all six NC suites, and a suite failure set
byte-identical to baseline at a single HEAD**.

## 1. WHAT THIS CLOSES, AND THE ROUTE IT TOOK

**NC 26 closes NC25-F1, which NC 25 filed rather than fixed.** NC 25 built structure-first
recognition for the take-forms, then stopped:

> *"Extending the structure to `on` / `started` / `switched to` is the same KIND of decision Bill
> just made and is his to make, so it is reported rather than taken."*

Bill made it. **A session declined to widen a boundary on its own authority, said so in writing,
and the ruling followed the next morning.** Recorded here because the value of that pattern is
invisible unless somebody writes down that it worked.

## 2. THREE FRAMES, NOT FOUR — AND WHY THAT IS THE RIGHT READING OF A FOUR-LINE RULING

Bill's family is `I'm on X` / `I'm taking X` / `I started X` / `I stopped X`. **The second one
already worked.** NC 25's take-frame matches a first-person subject followed by any of
`take|takes|taking|took`, so *"I'm taking lisinopril"* was already class (a) at `bfb09df`.

**Adding a fourth pattern would have been a second implementation of one behaviour, free to
drift from the first.** Frame 2 is therefore **twinned, not rebuilt** — and the twin asserts not
just that it is governed but that it is governed *by NC 25's code path*, by checking the reason
string reports `structural-medication-frame` and not NC 26's `medication-frame:`. If someone
later reimplements it here, that twin fails.

## 3. THE TIER — THE ONE INTERPRETIVE CALL, AND IT IS FLAGGED FOR OVERRULE

Constraint 2: *"Unknown-but-plausible medication object -> the RESTRICTIVE path (medical
governance / clarification), never permissive classification. Fail toward asking."*

**Both class (a) and class (b) are governance, and the ruling names *clarification*, which is
class (b)'s name in this codebase.** NC 26 reads it as two tiers:

| verb evidence | object evidence | class |
|---|---|---|
| `take` / `taking` | any non-excluded object | **(a)** — NC 25, **unchanged** |
| `on` / `started` / `stopped` | **corroborated** — a dosage, or a lexicon word elsewhere in the turn | **(a)** park-and-confirm |
| `on` / `started` / `stopped` | **uncorroborated**, not excluded | **(b)** clarify — **no model, no write** |
| any | **excluded** | `NOT_MEDICAL` |

**(b) IS THE MORE RESTRICTIVE DESTINATION, NOT THE SOFTER ONE.** (a) parks the fact and asks the
member to confirm it; **(b) writes nothing at all**, takes no model call, and returns a fixed
clarification. For an object nothing corroborates, writing nothing *is* "fail toward asking".
**Neither tier is permissive** — `NOT_MEDICAL` is the outcome constraint 2 forbids, and it is
unreachable from the frame path once an object survives the exclusion list.

**Why the asymmetry with NC 25 is principled rather than convenient:**

1. **Verb specificity is real.** *"I take X"* with an unfamiliar noun almost always means a
   medication. *"I'm on X"*, *"I started X"*, *"I stopped X"* carry vacations, schools, jobs,
   buses and diets as readily as drugs. Weaker evidence, more cautious destination.
2. **It is independently forced by the twins.** NC 25's twins assert *"I take lisinopril"* is
   class (a); a uniform rule sending every uncorroborated object to (b) would regress them, and
   this dispatch was required to keep NC 15's and NC 25's medical twins green.

**THE ALTERNATIVE IS WRITTEN INTO THE REQ SO ONE LINE FLIPS IT:** make all four frames behave
like `take` — every non-excluded object goes to (a). Simpler and more uniform; not chosen because
it treats *"I'm on Zoom"*-shaped turns with the same confidence as *"I take lisinopril"*, and
because it would make constraint 2 redundant with constraint 1.

## 4. CAPITALISATION IS NOT CORROBORATION — RULING 4, GENERALISED

**This is the design decision most likely to be questioned, so it is twinned directly.**

NC 25's take-frame may treat a brand-shaped capitalised token as a concrete value, because `take`
has already carried the medical weight. For the weaker frames it would be **the only evidence** —
and **capitalisation is a typing artifact that ASR does not produce.** Letting it decide the class
would make *"I'm on Zervolol"* (typed) and *"i'm on zervolol"* (spoken) land in different classes.

**That is precisely the modality-dependent classification F6 measured for punctuation and Bill's
ruling 4 forbade**, arriving through a different door. A dosage and a lexicon word survive
transcription; orthography does not. So corroboration is a dosage or a lexicon hit, and
*"I'm on Zervolol"* lands in **(b)** — governed, caught by structure, nothing written.

## 5. CONSTRAINT 1 — ANSWERED STRUCTURALLY WHERE IT COULD BE

| utterance | result | mechanism |
|---|---|---|
| *"I'm on vacation"* | `NOT_MEDICAL` | exclusion list |
| *"I'm taking the bus"* | `NOT_MEDICAL` | exclusion list (already, at `bfb09df`) |
| *"I started school"* | `NOT_MEDICAL` | exclusion list |
| *"I stopped at the store"* | `NOT_MEDICAL` | **structural — `at` is a preposition** |

**P6.3a is the part worth reading.** A frame verb followed by a **preposition** heads an adjunct,
not an object. That single test also releases *"I stopped by the pharmacy"* — **medical
vocabulary, and still not a medication assertion** — and *"I stopped for gas"*, which a word list
would have to enumerate one at a time. **A structural ruling deserved a structural answer.**

The exclusion list still grew, because three new verbs bring three new families of ordinary
objects: vacations, schools, jobs, shifts, calls, diets, weekdays and months. **Widening it
remains maintenance rather than a ruling**, on NC 25's stated grounds — an exclusion list only
ever RELEASES turns.

## 6. TWO DEFECTS FOUND WHILE BUILDING, BOTH FIXED, BOTH REPORTED

**Reported rather than absorbed, because each was a silent wrong answer rather than a crash.**

**(i) `_NEGATION` missed the two commonest negative forms.** *"I'm not on lisinopril"* contracts
to `'m not`, which the enumerated `am not` never matched, and *"I have not started lisinopril"*
is a perfect form that was not listed. **Both read as POSITIVE polarity** — a false record of
what a member said about their own medication, in the exact place P5.2 exists to get right. A
bare `not` now backs the enumeration: **a list of contractions is never finished.**

**(ii) The object slot read the first token, not the noun phrase.** *"I started a new job"*
stripped the determiner, read **`new`**, found it on no list, and **governed a career change as a
medication.** The exclusion list now sees the whole phrase — up to three tokens, **stopping at a
preposition** so that *"I started lisinopril for work"* is not released by `work`. Caught by
the constraint-1 twin, which is what that twin is for.

## 7. P6.6 — TWO GREEN TWINS RETIRED BY THIS RULING. THE TWINS WERE WORKING.

**This is the only place in the batch where a passing test had to go red, and both were built
for exactly this moment.**

| twin | asserted | its own docstring |
|---|---|---|
| NC 15 `test_the_recognition_boundary_is_the_documented_one` | *"I'm on metformin"* is `NOT_MEDICAL` | *"If someone widens the lexicon, this test makes the widening **a visible decision instead of drift**."* |
| NC 25 `test_R5_THE_NAMED_RESIDUAL_the_on_frame_is_still_out_of_scope` | the same | *"if it ever starts failing, someone widened the structure **without a ruling**."* |

**It started failing because someone widened the structure WITH one.** Both are **updated to the
newly ruled behaviour with their old assertions kept verbatim in the test body**, alongside the
ruling that changed them — never deleted, never silently patched. Each keeps doing its original
job: it will fail again the next time the boundary moves.

**They were the ONLY two that went red.** Every other NC 15 and NC 25 medical twin passed
unchanged — a widening that quietly re-tiered a neighbouring case would have failed P6.6b.

## 8. THE ACCEPTANCE, MEASURED

Environment: **lane graph 7693 has no listener** — this lane's honest default, the environment
NC 21, NC 25 and this dispatch all measured in. **`lane_preflight.py` OK** (hip-nc2 @ nc-b0
writes 7693), **NOT BUSY**, run before any suite.

### Twin counts by category — 63 new

| category | twins | what they hold |
|---|---|---|
| **Constraint 1** — verbs are never triggers | **20** | 4 ruled utterances + 11 other ordinary objects + 5 preposition/adjunct |
| **The frame family** | **8** | 4 frames × a real drug, 3 reason-names-the-frame, 1 frame-2-is-NC-25's |
| **Constraint 2** — restrictive tier | **17** | 5 invented names, 4 uncorroborated→(b), 5 corroborated→(a), 1 no-drug-cannot-park, 1 (b)-is-restrictive, 1 capitalisation |
| **Polarity** | **9** | 6 negated forms governed + 3 positives not mislabelled |
| **Constraint 3** — original survives | **6** | no mutation, 3 punctuation-tolerance, reason carries no rewritten utterance, question-shape-first |
| **Neighbours unmoved** | **3** | third person, NC 25 take-frame byte-for-byte, generic medical noun |

### The suite, by SET comparison at a single HEAD (`bfb09df`)

```
BEFORE:  20 failed, 753 passed, 39 skipped, 21 errors
AFTER:   20 failed, 816 passed, 39 skipped, 21 errors
failure+error SET: 41 entries before, 41 after, diff EMPTY
816 - 753 = 63, exactly the new twins
```

**Single-variable this time by construction** — HEAD was verified to still be `bfb09df`
immediately before the after-run, which NC 25 learned to check the hard way when NC 24 landed
mid-comparison. **300 passed** across all six NC suites (NC 15, 20, 22, 24, 25, 26) run together.

## 9. FINDINGS FILED — 4, NONE BLOCKING

**NC26-F1 — INVERTED QUESTION FORMS DO NOT MATCH THE FRAMES.** *"Am I on Zervolol"* is
`NOT_MEDICAL`, because the frames are declarative-only (`I'm on …`, not `am I on …`). **The
direction is safe** — it cannot become an assertion, so no write can happen — and it was equally
true before this dispatch. Named because a reader who sees the on-frame recognised will
reasonably expect its question form to be recognised too. Adding interrogative frames is scope
beyond the ruling.

**NC26-F2 — THE THIRD-PERSON FRAME IS STILL OUT OF SCOPE.** *"My mother is on lisinopril"* is
`NOT_MEDICAL`. Bill's four frames are all first-person, and third-person medical assertions have
their own existing trust-ladder path (NC 15's `MEDICAL_OTHER`) which only engages once the
lexicon or a dosage recognises the turn. **So the widening that just landed for first person has
no third-person counterpart**, and household members' medications are the obvious case where
that matters. **This is the natural successor to NC25-F1 and is offered the same way: reported,
not taken.**

**NC26-F3 — THE ACCEPTED FALSE-POSITIVE HAS A NAME NOW: *"I'm on Zoom"*.** An unknown object
outside the exclusion list is governed, so app and brand names in the `on`-frame draw a
clarification. **Under the tier this costs a clarification and not a park**, which is materially
cheaper than NC 25's equivalent residual (*"I take the ferry"* → park-and-confirm). Mitigation is
maintenance: add the term to `_NOT_A_MEDICATION`. Recorded so it is met as a decision.

**NC26-F4 — TD-R-194(b), FIFTH HAND-EDIT ON THE SAME BRICKED ROW.** The NC lane row still carries
7 bare pipes against a 6-pipe header, so `claim_lane.py` refuses every edit and NC 22, NC 24,
NC 25 (×2) and now NC 26 have each hand-edited under the repo lock. **Deliberately NOT re-filed**
— `TD-R-194(b)` is already OPEN and a second row adds a count, not information. Same reasoning
NC 25 recorded.

## 10. WHAT I DID NOT DO

- **No fourth frame implementation** — frame 2 is NC 25's and stays that way.
- **No interrogative frames** (NC26-F1), **no third-person frames** (NC26-F2). Both are ruling
  territory, not refactor territory.
- **No change to NC 25's take-frame path** — the NC 26 branch is gated on `not structural`, and a
  twin asserts the take-frame's behaviour is byte-for-byte what it was at `bfb09df`.
- **No REQ ruled MET, no acceptance row re-tiered, no baseline changed.**

## 11. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Recognition boundary of the medical split; no ledger claim's standing evidence is touched.

## 12. VERIFIED

Machine gate (`bill-ai` / `[REDACTED-MACHINE-NAME]` / `~/hip-nc2` @ `nc-b0` @ `bfb09df`, in
sync). `lane_preflight.py` OK (7693) and NOT BUSY before any suite. Claim first (`02d7051`), REQ
Amendment 3 before code (`e971c29`), code after (`0ee55fb`). Repo lock held around each git
operation only; every push verified to carry exactly one commit and no passenger. `.hip-scope`
hand-written in `~/hip-nc2` (TD-R-194(a)). HEAD re-checked immediately before the after-run so the
set comparison is single-variable. Every number above is from this session's runs, with the
service state stated.
