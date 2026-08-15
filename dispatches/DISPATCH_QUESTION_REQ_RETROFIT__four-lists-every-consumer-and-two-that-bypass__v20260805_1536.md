# DISPATCH_QUESTION_REQ_RETROFIT
Status: BUILT
Reconciled-Against: `30adeaf` on `demo-cutover-build`; landed on `roadmap` at **`92a7999`**
(2026-08-05). Base at dispatch start was `3239ff8`; another lane pushed `6649ec5` mid-dispatch,
so this commit sits on top of it — verified `6649ec5..HEAD` contains exactly one commit and no
passenger (STANDARD PREAMBLE item 8).

**TYPE:** ANALYSIS + PROCESS

**REQ:** writes
`docs/requirements/REQ_QUESTION_IS_NOT_A_STATEMENT__decisive-question-test-not-overridable__v20260805_1536.md`.
This dispatch changed **no code** — D-R-188 item 3, *"Rule nothing. No code changes in this
dispatch."*

**COMPLETE WITH FINDINGS — 8 ITEMS FILED, NOTHING BLOCKING**

## THE ASK

D-R-188, verbatim:

> === D-R-188 | ~/hip-roadmap, roadmap | Retroactive REQ for the question-detection fix ===
> STANDARD PREAMBLE. Lane A. Check first whether this REQ already exists — do not
> re-issue completed work.
>
> A code change shipped at 30adeaf with no REQ, against Requirements Discipline item 8.
> Do NOT revert: the fix works and closed both leaks. Write the requirement it should
> have had.
>
> 1. WRITE THE REQ covering what shipped. It must settle three things the refusing
>    session named, none decided:
>    a. Does a question mean "?" anywhere in the text, or ends with "?"? The shipped
>       code uses the broader test.
>    b. Does the ban on overriding that decision cover the one place inside the
>       injection contract, or all four places? As written it reads as all four, which
>       changes the voice path too.
>    c. Four question-word lists now exist and disagree. Consolidate, or keep them
>       separate with the reason written down?
>    Where the answer is not settled by an existing ruling, say UNDETERMINED and name
>    what would settle it. STOP AND REPORT if any of the three blocks the REQ.
> 2. SURVEY, evidence not inference: every list, every consumer, and which two bypass
>    the main path. Say what the same sentence does on each route today.
> 3. Rule nothing. No code changes in this dispatch.

## WHAT WAS DONE

1. **Machine gate.** `bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` /
   branch `roadmap`. Matches the dispatch target. Tree not clean: **4 untracked
   `DISPATCH_DEMO_CUTOVER_*` docs**, another lane's work — left exactly as found, committed
   around with explicit pathspecs.
2. **Checked whether the REQ already exists** (the dispatch's first instruction). It does not:
   no filename match in `docs/requirements/` for question/declarative/utterance/interrogative,
   and no body hit for `is_question_utterance`, `DECISIVE_QUESTION`, or "question test". Not
   re-issued work.
3. **Read `30adeaf` in full** — message, stat, and the complete 4-file diff.
4. **Established which branch carries it** — `git merge-base --is-ancestor`, `git branch --contains`.
5. **Read `REQ_UNRESOLVED_SUBJECT_GUARD…v20260804_2104.md` end to end** to test the "no REQ"
   claim rather than repeat it.
6. **Enumerated every question test in the tree at `30adeaf`** by iterating `git ls-tree` and
   grepping each `.py` — not a working-tree grep, since the working tree does not contain the fix.
7. **Built the call graph for `apply_injection_contract`** across every `.py` at `30adeaf`.
8. **Ran a probe** (`scratchpad/probe.py`) that loads the `30adeaf` copies of
   `injection_contract.py` and `fact_change.py` and `exec`s voice_orch's own regex + `_is_question`
   source lines, then runs all four tests over the same 10 sentences and diffs the token sets.
   Token counts are read out of the compiled patterns, not transcribed by hand.
9. **Searched for a governing ruling** on the "?" test and on the list divergence —
   `DECISIONS.md`, `docs/BACKLOG.md`, `docs/techdebt/LATEST_DEBT.md`. None found on either branch.

## WHAT WAS FOUND

### F1 — THE CODE IS NOT ON `roadmap`

```
git merge-base --is-ancestor 30adeaf HEAD   → exit 1
git branch -a --contains 30adeaf            → demo-cutover-build, origin/demo-cutover-build
grep -rn is_question_utterance harness/ server/   → (no output)
```

`30adeaf` is on `demo-cutover-build` only. **This worktree does not contain
`is_question_utterance` at all.** The two branches also diverge independently on all four
touched files (237 insertions / 115 deletions between roadmap HEAD and `30adeaf`), merge base
`2f69f2f` (D-105). Every code citation in this dispatch and in the REQ is therefore read from
`30adeaf`, stated as such.

### F2 — "with no REQ" is not quite what happened; the real gap is narrower

`30adeaf`'s message **does** cite
`REQ_UNRESOLVED_SUBJECT_GUARD__sensitive-facts-not-admitted-on-subjectless-turns__v20260804_2104.md`
and uses its six acceptance checks as the acceptance test. Item 8's literal gate — *"does not
name a REQ doc"* — was satisfied on its face.

What did not exist is a REQ covering **the mechanism that shipped**. Reading that REQ end to
end: it requires that facts at `>= medium` not be admitted on subjectless turns, moves the
gate from refusal to injection, and constrains the backstop. It contains **no mention of
`is_declarative`, question detection, or the SIO override**. It governs the outcome; the
shipped code introduced a new classifier with an override ban, which is a mechanism no REQ
describes.

**Second gap:** that REQ exists only on `roadmap` —
`git ls-tree -r 30adeaf docs/requirements/ | grep -i unresolved` returns nothing. A session
standing on the branch where the code lives cannot open the REQ the commit cites.

### F3 — THE FOUR LISTS, from the compiled patterns

| | Location `@30adeaf` | tokens | punctuation rule | consumer count |
|---|---|---|---|---|
| **L1** | `harness/injection_contract.py:317` `_QUESTION_OPENER_RE` | **27** | `"?" in t` (`:348`) | 14 |
| **L2** | `harness/injection_contract.py:372` `_DECISIVE_QUESTION_OPENER_RE` | **20** | `t.endswith("?")` (`:391`) | 5 |
| **L3** | `harness/fact_change.py:94` `_QUESTION_WORDS` | **6** | `endswith("?")` `:922`; `rstrip("?")` `:924` | 3 |
| **L4** | `server/voice_orch.py:571` `_QUESTION_OPENER_RE` | **19** | `"?" in t` (`:586`) | 1 |

```
in all four  : how, what, when, where, who          (5 of 27)
in L1 not L2 : explain give has have list name remind show tell trace
in L2 not L1 : which whose why
in L1 not L4 : explain give list name remind show tell trace
in L2 not L4 : which whose why
```

A fifth classifier exists and is not a word list: `harness/sio.py:203`, the LLM prompt whose
`"type"` field is *"one of `question` (interrogative OR imperative information request …)"*.
It is the thing the decisive test was built to override.

### F4 — THE `has`/`have` GAP (the finding that matters most)

L2 is **narrower than both pre-existing lists** on `has` and `have` — ordinary yes/no
interrogative openers present in L1 and L4, absent from the new decisive list. Measured:

| sentence | L1 decl? | **L2 quest?** | L3 q-word? | L4 quest? |
|---|---|---|---|---|
| `Has she taken her medication` | `False` | **`False`** | `False` | `True` |
| `Have you seen her chart` | `False` | **`False`** | `False` | `True` |

With no trailing "?", the decisive test does not fire. A live SIO returning `type="statement"`
sets `is_declarative=True` and nothing overrides it — **the TD-D-154 leak shape, still open on
two tokens.** D-D-158's recorded rationale for a separate list
(`harness/injection_contract.py:366-370`) names why/which/whose as additions and the imperatives
as deliberate exclusions; **it does not mention `has` or `have`.** On the evidence this reads as
unintended. Not ruled here.

### F5 — THE "?" RULE SPLIT

`is_question_utterance` uses `t.endswith("?")` — the **narrower** test, not the broader one
D-R-188 describes. `"?" anywhere` is what the untouched `is_declarative_utterance` (`:348`) and
`_is_question` (`voice_orch.py:586`) use. The shipped state runs both, at two layers of one
decision. Measured discriminator:

| sentence | L1 decl? | **L2 quest?** | L4 quest? |
|---|---|---|---|
| `You said what? Anyway her dose is 500mg.` | `False` | **`False`** | `True` |

Mid-text "?" that does not end the sentence → no force → SIO decides. Widening L2 to `"?" in t`
would change **none** of D-D-157's 8 measured rows (all end with "?").

### F6 — EVERY CONSUMER, AND WHETHER THE DECISIVE TEST REACHES IT

| Site `@30adeaf` | test used | decisive applied? | reaches `apply_injection_contract`? | what it decides |
|---|---|---|---|---|
| `injection_contract.py:697` | L2, **forced** | **YES — structural** | *is* the contract | INJ-1c, INJ-2 bypass, INJ-6/6b/6c |
| `orchestrator.py:633` | L2→SIO→L1 | YES (caller-side) | yes, `:651` | text/harness main path |
| `voice_orch.py:2517` `_is_decl_query` | L2→SIO→L1 | YES (caller-side) | yes, `:2530` | voice text path injection |
| `voice_orch.py:2521` `_is_decl_speaker` | L2→SIO→L1 | YES (caller-side) | no — used at `:2577` | speaker-query declarative |
| `realtime_adapter.py:572` | L2→SIO→L1 | YES (caller-side) | **NO — never calls it** | Realtime write-detection gate |
| `voice_orch.py:2407` | **L1 raw** | no | no | TD-121 F3 ack replacement |
| `voice_orch.py:3062` | **L1 raw + L3** | no | no | voice-text write-detection gate |
| `voice_orch.py:3127/3167/3440` | **L1 raw** | no | no | `sio_shadow_fields` telemetry |
| `voice_orch.py:3224/3227` | **L1 raw** | no | no | double-value gate |
| `voice_orch.py:1700` | **L4** | no | no | escalation-placeholder suppression |
| `realtime_adapter.py:598` | **L1 raw** | no | no | `sio_shadow_fields` telemetry |
| `confirmation_gate.py:197` | **L1 raw** | no | **NO — never calls it** | confirmation pass / park |
| `recall.py:261`, `memory_dashboard.py:217` | contract default `False` | YES (contract forces) | yes | cold recall / dashboard |

**THE TWO THAT BYPASS THE MAIN PATH.** Taking the main path to be
`apply_injection_contract` — the choke point where the force is structural — exactly two
modules decide `is_declarative` and never call it. From the full call-graph grep over every
`.py` at `30adeaf`, neither appears among its callers:

- **`harness/realtime_adapter.py`** — the OpenAI Realtime voice path. Its `_is_declarative`
  gates `detect_and_apply_async` (write-detection), nothing else. **It DID get the decisive test.**
- **`harness/confirmation_gate.py`** — the confirmation / park path, `:197`. **It did NOT.**

The asymmetry is the finding: the two bypassing routes were treated differently, and neither
treatment is written down anywhere.

### F7 — THE SAME SENTENCE ON EACH ROUTE TODAY

**S1 = `"Has she taken her medication"`** (no "?"; L2 does not fire, so the SIO decides):

| route | verdict today | consequence |
|---|---|---|
| `orchestrator` → contract | SIO-live-statement → `is_declarative=True`; contract does not force | **INJ-1c carve-out skipped — leak shape live** |
| `voice_orch` text → contract | same | **same** |
| `realtime_adapter` write-detect | `_is_declarative=True`, `len(words)=5≥4`, `words[0]="has"` ∉ L3 | **write-detection FIRES on a question** |
| `voice_orch:3062` write-detect | L1 raw: `"has"` ∈ L1 → not declarative | does **not** fire |
| `confirmation_gate:197` | L1 raw: `"has"` ∈ L1 → not declarative | returns `"pass"` — **correct** |
| `voice_orch:1700` (L4) | `"has"` ∈ L4 → `_is_question=True` | escalation not suppressed |
| `fact_change:918-924` internal | ≥4 words, no trailing "?", `"has"` ∉ L3 | does **not** short-circuit — the backstop does not catch it either |

**Two write-detection gates, same sentence, opposite answers** — `realtime_adapter` fires,
`voice_orch:3062` does not — because one reads the SIO-overridable value and the other reads
raw L1.

**S2 = `"Why is the sky blue"`** (no "?"; L2 fires):

| route | verdict today | consequence |
|---|---|---|
| `orchestrator` → contract | forced `False` (question) | **fix working** |
| `voice_orch` text → contract | forced `False` | **fix working** |
| `realtime_adapter` write-detect | `_is_declarative=False` | does not fire — **fix working** |
| `voice_orch:3062` write-detect | L1 raw → **declarative `True`**; saved only by `"why"` ∈ L3 | does not fire — **by L3, not by the fix** |
| `confirmation_gate:197` | L1 raw → **declarative `True`** → not `"pass"` | **falls into the D-22 fact-assertion branch — wrong** |
| `voice_orch:1700` (L4) | `"why"` ∉ L4, no "?" → `_is_question=False` | treated as a non-question |

### F8 — NO GOVERNING RULING EXISTS FOR ANY OF THE THREE

Searched `DECISIONS.md`, `docs/BACKLOG.md`, `docs/techdebt/LATEST_DEBT.md` on `roadmap` and the
debt register at `30adeaf`. No hit for a "?" -test ruling, no hit for `_QUESTION_OPENER_RE`,
"opener list", "question word", or "four list". **No TD is filed on the list divergence on
either branch.** All three of D-R-188's questions are genuinely open.

## THE THREE QUESTIONS — DISPOSITION

**None of the three blocks the REQ**, so no STOP was taken. Each concerns whether the shipped
**scope** is correct, not whether the shipped **behaviour** can be stated; the REQ states the
behaviour as shipped and carries each scope question as UNDETERMINED with what would settle it.

- **(a) UNDETERMINED** — and the dispatch's premise is corrected: the shipped decisive test
  uses `endswith("?")`, the **narrower** rule. Settled by Bill ruling whether L2 adopts
  `"?" in t`. Cheap: cannot regress D-D-157's 8 measured rows.
- **(b) UNDETERMINED** — as shipped it covers all four, and it does change the voice path (both
  `voice_orch` and `realtime_adapter`). But only site 1 is structural; 8 further sites decide
  the same axis on raw L1. Settled by Bill ruling whether "not overridable" is a property of
  the contract or of the whole `is_declarative` axis. The two rulings produce different builds.
- **(c) UNDETERMINED**, as three separable rulings: `has`/`have` in L2 (cheapest, and the one
  with a measured live consequence); L2-vs-L1 (D-D-158's stated reason is sound — the ruling
  needed is whether it is permanent); L4-vs-L1 (a verbatim duplicate of L1's interrogative half
  with **no** recorded reason — the strongest consolidation candidate).

## VERIFIED

**Watched run:**
- `scratchpad/probe.py` — loaded the `30adeaf` copies of `injection_contract.py` and
  `fact_change.py`, `exec`'d voice_orch's own L4 regex and `_is_question` source lines, ran all
  four tests over 10 sentences, and diffed the token sets read out of the compiled patterns.
  Every cell in F3, F4, F5 and the L1/L2/L3/L4 columns of F7 is printed output.
- `git merge-base --is-ancestor`, `git branch --contains`, `git ls-tree`, and the
  `apply_injection_contract` call-graph sweep over every `.py` at `30adeaf` — all run, output read.

**Reasoned from code, NOT executed:**
- **Every "consequence" column in F7.** The route verdicts follow from reading the branch
  expressions at each cited line; **no live turn was fired**, no dashboard was started, no SIO
  was called. In particular the claim that S1 leaks under a live SIO **assumes the SIO returns
  `type="statement"` for that sentence** — that is the shape TD-D-154 measured for "Why blue
  sky?", not a measurement of this sentence. **It should be measured before it is acted on.**
- D-D-158's live results (A002/B044/B092, battery zero delta, the six acceptance checks) are
  **reported from that dispatch doc, not re-run here.**
- The full ratchet (`eval.harness --full`) was **not** run. Requirements Discipline item 12 is
  not satisfied by this dispatch and the REQ says so.

## OPEN — Bill's

1. **Rule (a)** — punctuation rule for the decisive test.
2. **Rule (b)** — scope of the override ban.
3. **Rule (c1)** — `has`/`have` in L2. Has a measured consequence; cheapest of the three.
4. **Rule (c2)** — L2 vs L1 separation permanent?
5. **Rule (c3)** — L4 (`voice_orch.py:571`) duplicate: consolidate or record a reason.
6. **`confirmation_gate.py:197`** — treats "Why is the sky blue" as a fact assertion while a
   park is live. Falls out of ruling (b).
7. **The two write-detection gates disagree** (`realtime_adapter:582` vs `voice_orch:3062`).
   Also falls out of (b).
8. **Cross-branch:** the code is on `demo-cutover-build`, this REQ is on `roadmap`, and
   `REQ_UNRESOLVED_SUBJECT_GUARD` — which `30adeaf` cites — is not readable from the branch the
   code lives on. **How REQs are made visible to the branch that consumes them is unruled.**

**A TD is warranted for the four-list divergence and is NOT filed here.** Filing TDs is
pre-authorized only for TEST or TOOL infrastructure; this is production classification code, and
D-R-188 item 3 says rule nothing. Recommended, awaiting Bill.

Nothing marked MET. C9 not ruled. No code changed.

---

**D-R-188: the retroactive REQ is written and flagged as retroactive on the atorvastatin
precedent. All three questions are UNDETERMINED with what would settle each; none blocked the
REQ, so no STOP. Survey found 4 lists sharing only 5 of 27 tokens, 13 consumer sites, and the
two that bypass `apply_injection_contract` — `realtime_adapter.py` (which got the fix) and
`confirmation_gate.py` (which did not). Two measured gaps in the shipped fix: `has`/`have` fall
through the decisive test, and the decisive test uses `endswith("?")` where D-R-188 assumed the
broader rule. The code is on `demo-cutover-build`, NOT `roadmap`. Nothing marked MET. C9 NOT
ruled.**
