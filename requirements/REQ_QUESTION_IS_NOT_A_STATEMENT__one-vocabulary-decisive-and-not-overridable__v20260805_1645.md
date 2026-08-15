# REQ_QUESTION_IS_NOT_A_STATEMENT
Status: IN_PROGRESS
Reconciled-Against: `roadmap`, this dispatch's own commit (D-R-189, 2026-08-05). Built and
run on `roadmap`; see BRANCH REALITY below for what is and is not true of
`demo-cutover-build`.

**SUPERSEDES `REQ_QUESTION_IS_NOT_A_STATEMENT__decisive-question-test-not-overridable__v20260805_1536.md`**
(D-R-188, the retroactive version). That document marked three things UNDETERMINED and named
what would settle each. **Bill ruled all three at D-R-189; this version records the rulings and
the build that implements them.** The prior version is retained unaltered as the record of what
was open before the ruling.

**THE SLUG CHANGED, deliberately.** `decisive-question-test-not-overridable` described only
half of what this requirement now is — the other half is the CONSOLIDATION ("one vocabulary,
defined once"), which the old slug does not mention. The SUBJECT is unchanged, so the lineage
and the `LATEST_` symlink still resolve.

> **THE RETROACTIVE FLAG IS DISCHARGED, NOT INHERITED.** The prior version was filed after the
> fact and flagged as such against Requirements Discipline item 8. **This version is not
> retroactive**: it was written from Bill's D-R-189 ruling text BEFORE the code in that
> dispatch was written, which is the order item 1 requires. The item-8 deviation belongs to the
> prior version and to `30adeaf`; it does not attach to this build.

**Nothing here is MET.** D-R-189 item 6: *"Rule nothing MET."* Status is IN_PROGRESS. C9 is not
ruled.

## THE REQUIREMENT

Bill's words, verbatim, D-R-189:

> "A question is text ending with a question mark, or opening with a recognized question
> word; has, have, is, are, do, does and did are question words. The decision may not be
> overridden downstream at any of the four sites, the voice path included. One vocabulary,
> defined once; every consumer imports it."

And, on the consolidation:

> consolidate the four lists into one, keeping the tell/show/give openers TD-119
> and D-20 added deliberately — dropping them silently reverses closed defects. Apply the
> single test at all four sites including confirmation_gate.py, which never got the fix.

**Expanded — the three sentences, as three separable obligations:**

1. **THE DEFINITION.** A question is text that (a) ENDS WITH `?`, or (b) OPENS WITH a
   recognized question word. Not "`?` anywhere" — ends with.
2. **THE BAN.** Where the test says question, `is_declarative` is False and no downstream
   classifier may raise it — not the SIO, not a caller that already decided "statement". At
   all four sites, the voice path included, plus `confirmation_gate.py`.
3. **THE CONSOLIDATION.** One vocabulary, one definition, imported by every consumer. The
   merge is a UNION: nothing TD-119 or D-20 added may be dropped.

## THE THREE RULINGS — what D-R-188 left UNDETERMINED

| D-R-188 asked | D-R-189 ruled |
|---|---|
| **(a)** `?` anywhere, or ends with `?` | **ENDS WITH `?`** — the narrower rule. Note this is *not* what the pre-existing `is_declarative_utterance` did (`"?" in t`), so the ruling changes roadmap behaviour, it does not merely ratify it. |
| **(b)** the one contract site, or all four | **ALL FOUR, voice path included, PLUS `confirmation_gate.py`** — which D-R-188 F6 found had never received the fix. |
| **(c)** consolidate, or keep separate with reasons | **CONSOLIDATE**, as a union that preserves TD-119's and D-20's imperative openers. |

Ruling (c) overrides D-D-158's recorded decision to keep the decisive list separate. That
decision's stated reason — merging would pull imperative verbs into the non-overridable path
and change the INJ-2 bypass — was sound and is now simply **accepted as the cost**: the
imperatives ARE in the decisive path by ruling. What the ruling buys is that there is no second
list to drift.

## THE ACCEPTANCE TEST

Six clauses. All six ran; results in
`docs/dispatches/DISPATCH_QUESTION_ONE_VOCABULARY__consolidated-decisive-test-built-and-run__v20260805_1645.md`.

**(1) THE UNION IS PRESERVED — nothing dropped.** Every token of all four pre-consolidation
lists is in `QUESTION_OPENERS`, and the set contains nothing else. Machine-checked against the
old lists read out of git (`HEAD` and `30adeaf`), not transcribed.
**PASS — 30 tokens, exactly the union, zero additions, zero drops.**

**(2) THE MEASURED HOLE IS CLOSED, PROVEN BOTH DIRECTIONS.** `"Has she taken her medication?"`
under a LIVE SIO returning `type="statement"` AND a caller passing `is_declarative=True`:
nothing `>= medium` is admitted. **And the fault twin must leak** — with the decisive test
disabled, the identical call admits the `MEDIUM` fact. A twin that does not leak means clause
(2) proves nothing.
**PASS both directions.** Fix live: `allowed=[]`, `inj2_declarative_override=0`,
`denied_reasons=['deny_relevance']`. Fault injected: `allowed=[('f-watch-medium','MEDIUM')]`,
`inj2_declarative_override=1`.

**(3) ONE DEFINITION, BY IDENTITY NOT EQUALITY.**
`injection_contract.is_question_utterance is question_words.is_question_utterance`, and the
same for `fact_change` and `confirmation_gate`. Two equal-but-separate definitions are exactly
what this replaces, so equality is not the test.
**PASS.**

**(4) NO SECOND LIST SURVIVES.** A source scan asserts that neither
`_QUESTION_OPENER_RE = re.compile(` nor the 6-word frozenset reappears in
`injection_contract.py`, `voice_orch.py`, or `fact_change.py`.
**PASS.**

**(5) STANDING BATTERIES DO NOT MOVE.** Against the **633 passed / 9 xfailed** pristine
baseline this checkout actually produces, plus AUDIT 8/8, DISC 39/39, L7 27/27, L7V2 27/28,
RATCHET PASS.
**PASS — 652 passed / 9 xfailed, which is 633 + exactly the 19 tests this build adds**; every
layer identical to baseline; RATCHET PASS. **Not clean on the first attempt — see (5a).**

**(5a) THE FALSE RED, AND WHY IT IS NOT WAIVED.** The first post-change run went **L7V2 27/28
→ 25/28** with `MUTATION-SCORE-SELFTEST` and `MUTATION-NO-SILENT-DISAPPEARANCE` red. Cause:
`eval/harnesslib/mutation_targets.py` addresses the INJ-7 block by HARDCODED LINE NUMBER, and
this build shifted `injection_contract.py` by +3 lines there. **This is the exact failure the
D-102 TD predicted in writing** (*"ANY edit inserting or removing lines above this point …
desyncs it silently into a false red that reads as a governance regression"*), and D-102 set
the precedent for the response: resync the coordinate and record it.
**The claim that nothing governance-level changed is EVIDENCE, not assertion:** survivor count
held at **32 → 32**, and keyed on `(module, func, operator)` — ignoring the line number — the
survivor lists either side are **IDENTICAL**, an exact 18-for-18 permutation, verified against
`logs/mutation_survivors.jsonl` **before** the coordinate was touched. Both runs are reported.

**(6) THE MEMORY HARNESS HOLDS ITS PIN.** 13-15/17; 16/17 is a STOP.
**PASS — 13/17, failing set exactly {MEM-115, MEM-116, MEM-117, MEM-118}, byte-identical to
the pre-change baseline.**

**NOT SATISFIED — stated, not papered over: `eval.harness --full` DID NOT RUN.** Requirements
Discipline item 12 wants the full ratchet, not a hand-picked subset. It refused at its own
guard: *"--full needs >=2GB free memory (TD-129, the --full killer); currently 0.38GB free."*
The machine was under memory pressure from unrelated user applications; nothing was killed to
force it. `--layer 7` DID run its RATCHET (PASS). **Item 12 is therefore NOT satisfied by this
build, and no claim here should be read as if it were.**

## BRANCH REALITY — read before citing any of this

**This build is on `roadmap`. `30adeaf` — D-D-158's version of the fix — is on
`demo-cutover-build` and is NOT an ancestor of `roadmap`.** The two lanes now hold *different*
implementations of the same requirement:

| | `roadmap` (this build) | `demo-cutover-build` (`30adeaf`) |
|---|---|---|
| vocabulary | ONE list, 30 tokens | TWO lists, 27 + 20 tokens |
| punctuation | ends-with `?` everywhere | ends-with `?` decisive, `?`-anywhere legacy |
| `confirmation_gate.py` | has the test | does **not** |
| `voice_orch` duplicate list | removed | still present |
| **INJ-1c** (`>= medium` subjectless admission gate) | **DOES NOT EXIST** | **EXISTS** |

**INJ-1c's absence on `roadmap` is why clause (2) is written against INJ-2's declarative
bypass** — that is the leak vector that actually exists here. The same sentence was
additionally run against the demo branch's INJ-1c with this build's vocabulary patched in
(`denied_sensitivity_subjectless=1` with the fix, leak without it), and that run is labelled in
the dispatch doc as a COMPOSITION CHECK, not a roadmap result. **Reconciling the two lanes is
not done and is not in scope here.**

## WHAT'S ALREADY DONE

- **`harness/question_words.py`** — THE vocabulary and THE test, a dependency-free leaf module.
- **The force inside `apply_injection_contract`** — the only structural site.
- **The four caller sites plus `confirmation_gate.py`.**
- **Both duplicate lists retired** — `voice_orch._QUESTION_OPENER_RE`/`_is_question` and
  `fact_change`'s 6-word set.
- **`eval/test_question_words.py`, 19 tests, WIRED INTO `scripts/run_harness.sh`** — per D-36
  finding (b), a battery referenced by nothing can regress to green-by-deletion silently.

## WHAT'S KNOWN BROKEN

1. **`--full` is unrun** (TD-129 memory guard). Item 12 not satisfied.
2. **The two lanes diverge** — see BRANCH REALITY. Unreconciled.
3. **The 400-item probe corpus cannot detect a vocabulary regression.** Measured: **296 of 400
   rows end with `?`, and 0 have a mid-text `?`** — so all three vocabularies (old-roadmap,
   old-demo, new) classify all 400 identically. Zero rows changed. That is a real result and a
   WEAK one: the corpus settles every question by punctuation and never exercises the word
   lists. **Do not read "0 of 400 changed" as "the vocabulary change is low-risk."**
4. **`is_declarative_utterance` widened on mid-text `?`.** Ruling (a) makes
   `"You said what? Her dose is 500mg."` declarative where it was not. Nothing in the corpus
   exercises it (item 3 above), so this is unmeasured in situ, not proven safe.
5. **The mutation registry is still line-number-keyed.** Resynced, not fixed. Third occurrence.

## CONSTRAINTS

- **Do not drop TD-119's or D-20's openers.** Clause (1) is the standing guard.
- **Do not re-split the vocabulary.** Clause (4) is the standing guard.
- **Do not amend ORTH-1.** DC-061/DC-080 stay unguarded; DISC held 39/39.
- **Genuine declaratives must still admit** — the INJ-2 bypass and the correction rule are the
  working path.
- **Do not remove `fact_change`'s internal gate** — defence in depth, not the mechanism.
- **Missing sensitivity RAISES.** No default anywhere near this axis.
- **The frozen demo (`~/hip-dev`, Neo4j 7689) is untouched.**
- **Nothing is MET. C9 is not ruled.**
