# DISPATCH_QUESTION_ONE_VOCABULARY
Status: BUILT
Reconciled-Against: `roadmap` at **`a3fb1f2`** (2026-08-05). Built on `8700fe1` (D-R-190);
verified `8700fe1..HEAD` contains exactly one commit and no passenger (STANDARD PREAMBLE
item 8).

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_QUESTION_IS_NOT_A_STATEMENT__one-vocabulary-decisive-and-not-overridable__v20260805_1645.md`
(finalized by item 1 of this dispatch, from Bill's ruling, BEFORE the code was written —
superseding D-R-188's retroactive version).

**COMPLETE WITH FINDINGS — 4 ITEMS FILED, NOTHING BLOCKING**

## THE ASK

D-R-189, verbatim:

> === D-R-189 | ~/hip-roadmap, roadmap | Question detection: finalize the REQ and build it ===
> STANDARD PREAMBLE. Lane A.
> GOVERNING REQ: the D-R-188 retroactive REQ. Bill's three rulings, the requirement text:
> "A question is text ending with a question mark, or opening with a recognized question
> word; has, have, is, are, do, does and did are question words. The decision may not be
> overridden downstream at any of the four sites, the voice path included. One vocabulary,
> defined once; every consumer imports it."
>
> 1. FINALIZE the REQ with those rulings. Where D-R-188 marked UNDETERMINED, these settle it.
> 2. BUILD: consolidate the four lists into one, keeping the tell/show/give openers TD-119
>    and D-20 added deliberately — dropping them silently reverses closed defects. Apply the
>    single test at all four sites including confirmation_gate.py, which never got the fix.
> 3. THE FAULT TWIN THAT MATTERS: "Has she taken her medication?" under a live SIO must be
>    a question and inject nothing >= medium — that is the exact measured hole. Prove it
>    executed, both directions.
> 4. BLAST RADIUS FROM A RUN: what changes for the 26 declarative carve-out rows, and
>    whether any standing battery moves.
> 5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 STOP.
> 6. Rule nothing MET.

## WHAT WAS DONE

1. **Machine gate.** `bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` /
   `roadmap`. Tree carried 4 untracked `DISPATCH_DEMO_CUTOVER_*` docs (another lane's) —
   left exactly as found.
2. **BASELINE FIRST, before any edit** — `--layer 7` and the memory harness. Item 4 asks what
   moves; that is unanswerable without a before.
3. Surveyed roadmap's own copies of the four sites (they differ from `30adeaf`'s).
4. Built `harness/question_words.py`, then edited the six consumers.
5. Proved the union mechanically, against the old lists read out of git.
6. Ran the fault twin, both directions, twice — once against roadmap's real leak vector and
   once against the demo branch's INJ-1c as a labelled composition check.
7. Measured the classifier delta over the real 400-row probe corpus, **with an anti-vacuity
   check** because the result was zero.
8. Ran `--layer 7` again; **it went red**; traced, proved the cause, resynced, re-ran, and
   reported both runs.
9. Added a 19-test standing battery and wired it into `scripts/run_harness.sh`.
10. Ran `--layer 7` a third time, the memory harness, and attempted `--full`.

## WHAT WAS BUILT

**`harness/question_words.py`** — THE vocabulary and THE test. A dependency-free leaf module
(no `harness.*` imports, deliberately, so every consumer can import it with no cycle risk).

- `QUESTION_OPENERS` — one frozenset, **30 tokens**.
- `_QUESTION_OPENER_RE` — compiled FROM the frozenset, so the regex cannot drift from the set.
- `is_question_utterance(text)` — ends with `?` OR opens with a recognized question word.
- `is_declarative_utterance(text)` — the EXACT complement on non-empty text. There is no
  separate statement test that could disagree with the question test.

| file | change |
|---|---|
| `harness/injection_contract.py` | list + `is_declarative_utterance` REMOVED, re-exported from `question_words`; decisive force added inside `apply_injection_contract` (`_forced_question`, plus `and not _forced_question` on the SIO branch) |
| `harness/orchestrator.py` | decisive test first at the `_is_declarative` site |
| `harness/realtime_adapter.py` | same; its `_FC_QUESTION_WORDS` first-word check removed as redundant-and-narrower |
| `server/voice_orch.py` | own `_QUESTION_OPENER_RE` + `_is_question` DELETED; decisive test at `_is_decl_query` AND `_is_decl_speaker`; escalation-suppression site repointed; write-detection first-word check removed |
| `harness/confirmation_gate.py` | **the site that never got the fix** — now calls `is_question_utterance` directly |
| `harness/fact_change.py` | 6-word frozenset retired to an alias of `QUESTION_OPENERS`; its two internal gates collapsed into one `is_question_utterance` call |

## WHAT WAS FOUND

### F1 — the union is exactly preserved (item 2)

Old lists read out of git (`HEAD` for the three on roadmap, `30adeaf` for the decisive one),
never retyped:

```
NEW consolidated vocabulary: 30 tokens

  L1 injection_contract._QUESTION_OPENER_RE     27 tokens   SUPERSET — nothing dropped
  L2 _DECISIVE_QUESTION_OPENER_RE (demo)        20 tokens   SUPERSET — nothing dropped
  L3 fact_change._QUESTION_WORDS                 6 tokens   SUPERSET — nothing dropped
  L4 voice_orch._QUESTION_OPENER_RE             19 tokens   SUPERSET — nothing dropped

Bill's named words [are did do does has have is]: all present
union of all four old lists = 30; new = 30; added by consolidation = []
```

**Exactly the union. Zero drops, zero speculative additions.** `tell show give list name
remind` (TD-119) and `explain trace` (D-20) are all in.

### F2 — THE FAULT TWIN (item 3), both directions, on roadmap

`"Has she taken her medication?"`, LIVE SIO `type="statement"`, caller passing
`is_declarative=True` — both overrides attempted at once.

**The leak vector on roadmap is INJ-2's declarative bypass, not INJ-1c** (see F5). The watch
fact is `address`/`MEDIUM`, an attribute the query's INJ-2 keywords do NOT match, whose stored
value contains a word present in the utterance — so it can enter *only* through the bypass.

```
DIRECTION A — fix live
  contract's own is_question_utterance -> True
  allowed = []      denied_reasons = ['deny_relevance']
  inj2_declarative_override = 0        >= medium admitted = []

DIRECTION B — FAULT INJECTED (decisive test disabled inside the contract)
  contract's own is_question_utterance -> False
  allowed = [('f-watch-medium', 'MEDIUM')]
  inj2_declarative_override = 1        >= medium admitted = ['f-watch-medium']
```

**PASS both directions.** B leaking is what makes A load-bearing rather than incidentally
satisfied. The fault is asserted to have taken effect and asserted to be reverted.

**Composition check, LABELLED AS SUCH — not a roadmap result.** The same sentence against
`30adeaf`'s contract (which HAS INJ-1c) with this build's vocabulary patched in, subjectless:
fix live → `denied_sensitivity_subjectless=1`, `allowed=[]`; fault injected →
`allowed=[('f-hh-medium','MEDIUM')]`. Both directions PASS.

### F3 — BLAST RADIUS on the 400-row probe corpus (item 4), and why it is weak evidence

Three classifiers over all 400 rows of
`cutover_set{1,2}_results__RECONCILED__v20260805_1450.csv`:

```
A. vs OLD-ROADMAP (the baseline this build changes)              CHANGED: 0 of 400
B. vs OLD-DEMO / D-D-158 (what changes for the carve-out rows)   CHANGED: 0 of 400
```

**Zero is a result that hides a broken comparison, so it was anti-vacuity checked before being
believed:**

```
old_roadmap=True  old_demo=False NEW=False  'You said what? Anyway her dose is 500mg.'
old_roadmap=False old_demo=True  NEW=True   'Why is the sky blue'
old_roadmap=True  old_demo=False NEW=True   'Has she taken her medication'
old_roadmap=True  old_demo=False NEW=True   "Tell me Elena's medication"
```

The classifiers genuinely disagree. **The corpus is why the answer is zero:**

```
questions under NEW / OLD-ROADMAP / OLD-DEMO : 296 / 296 / 296
texts ending with '?'                        : 296
texts with '?' NOT at end                    : 0
texts opening why/which/whose                : 32   (all also end with '?')
texts opening has/have                       :  1   (also ends with '?')
```

**Every question-shaped row in that corpus carries a trailing `?`, so all three vocabularies
agree by punctuation alone and the word lists are never exercised.** The carve-out rows are a
subset of these 400 and are therefore unchanged — *the state D-D-159 measured (25 genuinely
declarative subjectless rows, down from 26) is untouched by this build.*

**Stated plainly because it would be easy to over-read: "0 of 400 changed" is a true result and
weak evidence. This corpus CANNOT detect a vocabulary regression.** The 19-test battery exists
because of that gap, not in spite of it.

*(Note on the item's wording: the count is **25**, not 26 — D-D-159 re-ran all 400 after
D-D-158 and one row moved. "26" is that run's structural-refusal count, a different figure.)*

### F4 — A STANDING BATTERY DID MOVE (item 4), and it was a false red

**First post-change run: `L7V2 27/28 → 25/28`, EXIT=2, RATCHET did not pass.**

```
NEW FAILURES (not in baseline): ['L7V2:MUTATION-SCORE-SELFTEST',
                                 'L7V2:MUTATION-NO-SILENT-DISAPPEARANCE']
```

Both anchored to `harness/injection_contract.py:<line>`. **Cause: hardcoded line-number
addressing.** `eval/harnesslib/mutation_targets.py` scopes the INJ-7 mutant sweep with
`_INJ7_LINENO_RANGE = (656, 674)` and the self-test seeds a mutant at `lineno == 664`; this
build shifted that block +3 (net +3 in the file: −16 where the list moved out, +19 where the
force went in). The INJ-7 `if` moved 664 → 667.

**This is the failure that file predicts in writing**, from D-102:

> TD FILED (D-102): this hardcoded-coordinate addressing is brittle by construction — ANY edit
> inserting or removing lines above this point in harness/injection_contract.py desyncs it
> silently into **a false red that reads as a governance regression**.

**The "nothing governance-level changed" claim is evidence, not assertion.** From
`logs/mutation_survivors.jsonl`, read BEFORE any coordinate was touched:

```
prev survivors 32   cur survivors 32
disappeared 18      appeared 18
content-keyed identical (ignoring lineno)?  True
```

Survivor count held at 32; keyed on `(module, func, operator)` the two lists are **identical**
— an exact 18-for-18 permutation. No mutant changed status.

**Response: resync the coordinate, as D-102 did, and record it** — `_INJ7_LINENO_RANGE →
(659, 677)`, seeded mutant `664 → 667`, in `mutation_targets.py` and `layer7_crypto_v2.py`,
with the old values and the reasoning left visible in the comment. **No baseline was changed**
(that is not pre-authorized); a hardcoded source coordinate was pointed back at the construct
it names.

### F5 — INJ-1c does not exist on roadmap

`grep` for the `>= medium` subjectless admission gate returns it on `30adeaf` (`INJ-1c`,
`denied_sensitivity_subjectless`, `_sensitivity.at_or_above`) and **nothing on `roadmap`**.
`REQ_UNRESOLVED_SUBJECT_GUARD`'s admission gate was the revised requirement, status PLAN,
never built here. This is why F2's roadmap twin is written against INJ-2's bypass, and it is
recorded in the REQ's BRANCH REALITY table with the other four lane divergences.

## RUNS (item 5)

| run | result |
|---|---|
| **BASELINE** `--layer 7` (pre-change) | 633 passed / 9 xfailed; AUDIT 8/8; DISC 39/39; L7 27/27; **L7V2 27/28**; RATCHET PASS |
| **AFTER, attempt 1** | 633 / 9; **L7V2 25/28**; 2 NEW FAILURES; **EXIT=2** — F4 |
| **AFTER, attempt 2** (coordinates resynced) | 633 / 9; L7V2 27/28; RATCHET PASS; EXIT=0 — **diff vs baseline: IDENTICAL** |
| **FINAL** (new battery wired in) | **652 passed / 9 xfailed** = 633 + exactly the 19 added tests; every layer identical to baseline; RATCHET PASS; EXIT=0 |
| **memory harness, baseline** | **13/17**, failing {MEM-115, 116, 117, 118} |
| **memory harness, after** | **13/17**, same set, `diff` IDENTICAL — inside the 13-15 pin, **not** the 16/17 STOP |
| **`--full`** | **DID NOT RUN** — `refuse: --full needs >=2GB free memory (TD-129, the --full killer); currently 0.38GB free` |

`tests/test_injection_declarative.py` (not in the standing battery) also re-run: 16 passed.

**All three runs item 5 named were executed. `--full` was not, and Requirements Discipline item
12 is NOT satisfied** — the machine was under memory pressure from unrelated user
applications and nothing was killed to force it. `--layer 7` did run its RATCHET.

## VERIFIED

**Watched run:** the union proof; both fault twins (both directions each, with the fault
asserted to take and to revert); the blast-radius sweep and its anti-vacuity check; the
survivor content-comparison; all four harness runs and both memory-harness runs; the 19-test
battery; the declarative suite; every `git` query; the import-identity check
(`ic.is_question_utterance is qw.is_question_utterance` → True for all three consumers).

**Reasoned from code, NOT executed:**
- **No live turn was fired. No dashboard was started. No real SIO was called.** Every SIO in
  every probe here is a hand-constructed dict (`{"type": "statement", "sio_source": "model"}`).
  The claim "a live SIO returning statement" is a *simulation of that condition*, not a
  measurement that the real classifier returns `statement` for this sentence.
- The voice and Realtime paths were **not exercised end to end** — their edits are covered by
  import/compile checks and the shared-definition identity test, not by a voice turn.
- F3's per-route consequences are unchanged from D-R-188 and were not re-derived.

## OPEN — Bill's

1. **`--full` is unrun** (TD-129). Item 12 unsatisfied; a re-run on a machine with 2GB free is
   the only thing that closes it.
2. **The two lanes now hold different implementations of the same requirement** — see BRANCH
   REALITY. `roadmap` has one 30-token list, `confirmation_gate` wired, no INJ-1c;
   `demo-cutover-build` has two lists, no `confirmation_gate` fix, and INJ-1c. **Reconciling
   them is unruled and not in scope here.**
3. **The mid-`?` widening is unmeasured in situ** — ruling (a) makes
   `"You said what? Her dose is 500mg."` declarative where it was not, and the probe corpus
   contains zero such rows.
4. **The mutation registry is still line-number-keyed** — third occurrence (D-101 → D-102 →
   this). Resynced, not fixed. A TD already exists from D-102; **no new TD was filed** and no
   existing one was edited, since D-R-189 item 6 said rule nothing and this is that TD's own
   subject, not a new finding.

Nothing marked MET. C9 NOT ruled.

---

**D-R-189: REQ finalized from Bill's three rulings BEFORE the code (so this build is not
retroactive); four lists consolidated into ONE 30-token vocabulary in
`harness/question_words.py`, proven to be exactly the union with TD-119's and D-20's openers
intact; the single test applied at all four sites plus `confirmation_gate.py`; both duplicate
lists deleted. The fault twin passes BOTH directions on the exact measured sentence — and the
fault-injected direction leaks, which is what makes it proof. Batteries: a real red first
(L7V2 25/28), traced to D-102's predicted line-number desync, proven harmless by a 32→32
content-identical survivor comparison made before anything was touched, resynced, re-run green
— both runs reported. Final 652/9 = baseline 633/9 + exactly 19 new tests, every layer
identical, RATCHET PASS, memory harness 13/17 on the same pinned set. `--full` REFUSED by
TD-129's memory guard: item 12 NOT satisfied. Nothing marked MET. C9 NOT ruled.**
