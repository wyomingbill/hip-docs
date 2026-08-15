# REQ_QUESTION_IS_NOT_A_STATEMENT
Status: IN_PROGRESS
Reconciled-Against: `30adeaf` on `demo-cutover-build` (2026-08-05). **NOT on `roadmap`** —
roadmap HEAD `3239ff8` does not contain `is_question_utterance` at all
(`git merge-base --is-ancestor 30adeaf HEAD` → exit 1).

> **FILED AFTER THE FACT, AND FLAGGED AS SUCH.** Requirements Discipline item 8 forbids
> writing a REQ retroactively to cover work already done — *"that is a contradiction, not
> compliance."* This document is exactly that, written on Bill's explicit instruction at
> **D-R-188** (*"A code change shipped at 30adeaf with no REQ… Do NOT revert: the fix works
> and closed both leaks. Write the requirement it should have had."*). The deviation is
> recorded here rather than hidden, on the precedent of
> `REQ_atorvastatin-false-ack__f3-gate-widen-and-detect-retry__v20260716_1713.md`, which was
> filed the same way and flagged the same way at `c86a414`.
>
> **Status is IN_PROGRESS, not BUILT.** Code landed; the requirement is not settled. Three
> scope questions below are **UNDETERMINED** and no ruling resolves them. Nothing here is
> MET. C9 is not ruled.

> **THE COMMIT DID NAME A REQ — the gap is narrower and more specific than "no REQ."**
> `30adeaf`'s message cites
> `REQ_UNRESOLVED_SUBJECT_GUARD__sensitive-facts-not-admitted-on-subjectless-turns__v20260804_2104.md`
> and uses that REQ's six acceptance checks as its acceptance test. Item 8's gate — *"does
> not name a REQ doc"* — was therefore satisfied on its face. What did not exist is a REQ
> covering the **mechanism that shipped**: a new decisive question classifier that overrides
> the SIO at four call sites. `REQ_UNRESOLVED_SUBJECT_GUARD` governs an **outcome** (facts at
> `>= medium` not admitted on subjectless turns) and says nothing about `is_declarative`,
> question detection, or the SIO override — a reading of that document confirms it, not an
> inference. **A second gap:** that REQ exists only on `roadmap`. It is absent from
> `demo-cutover-build`, the branch the code shipped on, so a session standing where the code
> is finds nothing at the cited path.

## THE REQUIREMENT

Bill's words, verbatim, from **D-R-188**:

> A code change shipped at 30adeaf with no REQ, against Requirements Discipline item 8.
> Do NOT revert: the fix works and closed both leaks. Write the requirement it should
> have had.

And from the dispatch this REQ retroactively covers (**D-D-158 / Index Demo 33**), the ruling
recorded in the shipped code comment at `harness/injection_contract.py:355-356`:

> Bill's ruling, Index Demo 33.

**Expanded — the requirement the shipped code implements:**

**A turn that is a question SHALL NOT be classified as a declarative statement, and no
downstream classifier may raise that classification back to "statement."** Where the turn is
a question, `is_declarative` is `False`, and neither the SIO (`harness/sio.py`) nor any caller
that has already decided "statement" may override it.

The consequence this exists to prevent, measured and not hypothesised: on `A002` ("Why blue
sky?") the SIO returned `type="statement"`, the `not is_declarative` carve-out skipped the
INJ-1c admission gate, and `risk_pattern/high` + `address/medium` rode into a plain
general-knowledge question. D-D-157 measured **8 of 400** subjectless probe rows doing this;
**B044** and **B092** — both carrying `risk_pattern/high` — were the two remaining leaks.

## THE THREE THINGS THIS REQ MUST SETTLE

D-R-188 names three questions the refusing session raised and none decided. Each is answered
below from evidence, or marked **UNDETERMINED** with what would settle it. **None of the three
blocks this REQ** — each concerns whether the shipped scope is *correct*, not whether the
shipped behaviour can be *stated*. All three are recorded as open rulings.

---

### (a) Does a question mean "?" anywhere in the text, or ends with "?"

**THE DISPATCH'S PREMISE DOES NOT MATCH THE CODE.** D-R-188 states *"The shipped code uses
the broader test."* It does not. The shipped `is_question_utterance` uses
**`t.endswith("?")`** — the **narrower** test:

```python
# harness/injection_contract.py:388-393  @30adeaf
    t = (text or "").strip()
    if not t:
        return False
    if t.endswith("?"):
        return True
    return bool(_DECISIVE_QUESTION_OPENER_RE.match(t))
```

The **broader** test (`"?" anywhere`) is what the two **pre-existing** functions use, both
untouched by `30adeaf`:

```python
# harness/injection_contract.py:346-350   is_declarative_utterance
    t = text.strip()
    if not t or "?" in t:
        return False

# server/voice_orch.py:585-586            _is_question
    t = text.strip()
    return "?" in t or bool(_QUESTION_OPENER_RE.match(t))
```

**So the shipped state uses BOTH rules, at two layers of the same decision:** ends-with-"?"
at the decisive, non-overridable layer; "?"-anywhere at the fall-through legacy layer.

**Measured divergence** (probe run, this dispatch — all four tests on the same sentence):

| sentence | L1 `is_declarative_utterance` | L2 `is_question_utterance` | L4 `_is_question` |
|---|---|---|---|
| `"You said what? Anyway her dose is 500mg."` | `False` (not declarative) | **`False`** (no force) | `True` |

**What that costs today.** On a sentence carrying a mid-text "?" that does not end with one,
the decisive test does not fire, so the value is decided by whichever route is live: a running
SIO returning `type="statement"` sets `is_declarative=True`; on the SIO-fallback route L1's
`"?" in t` returns `False` and `is_declarative` stays `False`. **Same sentence, two answers,
selected by whether the SIO model happens to be up.**

**UNDETERMINED.** No ruling in `DECISIONS.md`, `REQ_UNRESOLVED_SUBJECT_GUARD`, or
`docs/techdebt/LATEST_DEBT.md` settles which punctuation rule the decisive test should carry
(searched; no hits).

**What would settle it:** Bill ruling whether `is_question_utterance` adopts `"?" in t`, so
the decisive layer matches the legacy layer it sits in front of. **The ruling is cheaply
testable against evidence that already exists:** all 8 of D-D-157's misclassified rows end
with "?", so widening L2 to `"?" anywhere` would change none of them — it would only close
the SIO-dependent divergence above. A widening cannot regress the measured set.

---

### (b) Does the ban cover the one place inside the injection contract, or all four places

**AS SHIPPED IT COVERS ALL FOUR — and yes, it changes the voice path.** Evidence, per site:

| # | Site | form | strength |
|---|---|---|---|
| 1 | `harness/injection_contract.py:697-699` | `_forced_question = is_question_utterance(query)` → `if _forced_question: is_declarative = False`, plus `and not _forced_question` on the SIO branch | **STRUCTURAL** — a force inside the callee. A caller cannot smuggle a `True` in. |
| 2 | `harness/orchestrator.py:633-637` | `False if is_question_utterance(query) else (…)` | caller-side expression |
| 3 | `harness/realtime_adapter.py:572-576` | same | caller-side expression |
| 4 | `server/voice_orch.py:2517-2524` | same, computed **twice** — `_is_decl_query` (2517) and `_is_decl_speaker` (2521) | caller-side expression |

**The voice path is changed at two separate entry points, deliberately:**
`server/voice_orch.py` is the voice **text** path (`_is_decl_query` feeds
`apply_injection_contract` at 2530; `_is_decl_speaker` is consumed at 2577), and
`harness/realtime_adapter.py` is the **OpenAI Realtime** voice path. Both got the test.

**But the four sites are not equally binding, and the ban does not reach every consumer of
the same decision.** Only site 1 is enforced by construction; sites 2–4 are conventions a
fifth caller would not inherit. And **seven further sites decide the same axis with the raw
legacy test and never see the decisive one at all:**

`server/voice_orch.py:2407`, `:3062`, `:3127`, `:3167`, `:3224`, `:3227`, `:3440`, and
`harness/confirmation_gate.py:197` — every one calling `is_declarative_utterance` directly.

**UNDETERMINED.** What would settle it: Bill ruling whether *"not overridable"* is

- **a property of the injection contract only** — in which case sites 2–4 are consistency
  edits rather than contract, and `confirmation_gate.py:197` and the voice_orch write-detection
  gate at `:3062` are correctly out of scope; **or**
- **a property of the whole `is_declarative` axis** — in which case those eight raw-legacy
  sites are gaps to be closed, and the acceptance test below gains a route-parity clause.

The two rulings produce materially different builds, which is why this is not decided here.

---

### (c) Four question-word lists now exist and disagree — consolidate, or keep separate with the reason written down

**Four lists, four different token sets, two different punctuation rules.** Extracted from the
compiled patterns themselves (probe run, this dispatch — not transcribed by hand):

| | Location | tokens | punctuation rule | contents |
|---|---|---|---|---|
| **L1** | `harness/injection_contract.py:317` `_QUESTION_OPENER_RE` | **27** | `"?" in t` | 19 interrogatives **+ 8 imperatives** (`tell show give list name remind explain trace`) |
| **L2** | `harness/injection_contract.py:372` `_DECISIVE_QUESTION_OPENER_RE` | **20** | `t.endswith("?")` | adds `why which whose`; drops `has have` **and all 8 imperatives** |
| **L3** | `harness/fact_change.py:94` `_QUESTION_WORDS` | **6** | `endswith("?")` at `:922`; `rstrip("?")` at `:924` | `what who where when why how` |
| **L4** | `server/voice_orch.py:571` `_QUESTION_OPENER_RE` | **19** | `"?" in t` | L1 **minus** the 8 imperatives |

```
in all four  : how, what, when, where, who          (5 tokens)
in L1 not L2 : explain give has have list name remind show tell trace
in L2 not L1 : which whose why
in L2 not L4 : which whose why
```

**THE FINDING THAT MATTERS MOST — the fix's own list is narrower than the list it corrects, on
`has` and `have`.** Measured, not reasoned:

| sentence | L1 | **L2 (decisive)** | L3 | L4 |
|---|---|---|---|---|
| `"Has she taken her medication"` | not declarative | **`False` — does not fire** | not a q-word | question |
| `"Have you seen her chart"` | not declarative | **`False` — does not fire** | not a q-word | question |

`has` and `have` are ordinary yes/no interrogative openers present in **both** pre-existing
lists (L1 and L4) and absent from the new decisive one. With no trailing "?", the decisive
test does not fire on either sentence, so a live SIO returning `type="statement"` sets
`is_declarative=True` — **the exact TD-D-154 leak shape, still open on two tokens.**

D-D-158's own recorded rationale for a separate list (`harness/injection_contract.py:366-370`,
and its dispatch doc) names why/which/whose as the additions and the imperatives as the
deliberate exclusions. **It does not mention `has` or `have` anywhere.** On the evidence the
drop reads as unintended rather than reasoned — but this REQ rules nothing, and records it.

**UNDETERMINED.** No TD is filed on the list divergence on either branch (searched
`docs/techdebt/LATEST_DEBT.md`; no hits for `_QUESTION_OPENER_RE`, opener list, or question
word). What would settle it, as three separable rulings:

1. **`has`/`have` in L2** — restore, or keep out with the reason written down. Independent of
   consolidation and the cheapest of the three.
2. **L2 vs L1** — D-D-158's stated reason for separation is sound on its face (L1 carries
   imperatives that are not interrogatives; merging would silently change the INJ-2 bypass
   that dispatch was told to leave alone). The ruling needed is whether that reason is
   **accepted as permanent**, in which case it is written into this REQ and the divergence
   stops being debt.
3. **L4 vs L1** — `server/voice_orch.py:571` is a **verbatim duplicate** of L1's interrogative
   half in a second file, with no recorded reason for existing separately. This is the one
   with no stated rationale at all, and the strongest consolidation candidate.

## THE ACCEPTANCE TEST

Telemetry only, never prose — the turn record is the evidence, per
`REQ_UNRESOLVED_SUBJECT_GUARD`'s standing form.

**(1) THE MEASURED CASE — already passing at `30adeaf`, recorded here as the ratchet.** On
A002, B044 and B092: `is_question=True`, `resolved_subjects=[]`, `injected_fact_ids=[]`, and
both watch facts absent. No `risk_pattern/high` on B044 or B092. *(D-D-158 reports this
observed live on a restarted dashboard, PID 57569, preflight 5/5 — see VERIFIED in that
dispatch doc; this REQ did not re-run it.)*

**(2) THE OVERRIDE IS REFUSED, both routes.** With a `>= medium` fact present and the caller
passing `is_declarative=True`: SIO-live-says-statement and SIO-fallback both admit only the
`low` fact. *(D-D-158 records this as a unit check.)*

**(3) NON-QUESTIONS ARE UNTOUCHED.** "Trash collection moved to Thursday.", "Ray switched from
metformin to Jardiance.", "The property is in the R-1-18 zoning district." — all still
declarative; the INJ-2 bypass is unchanged.

**(4) `has`/`have` — CURRENTLY FAILING, and the reason this REQ is IN_PROGRESS.**
"Has she taken her medication" (no "?") with a `>= medium` fact present and the SIO returning
`type="statement"` must produce `injected_fact_ids` containing no `>= medium` fact. **Today
`is_question_utterance` returns `False` on this sentence** (measured above), so the force does
not fire. This clause passes only after ruling (c)(1).

**(5) ROUTE PARITY — writable only after ruling (b).** If the ban is ruled to cover the whole
`is_declarative` axis, then the same sentence yields the same question/statement verdict on
every route in the SURVEY table below. If the ban is ruled contract-only, this clause is
struck and the table's disagreements are documented as intended.

**(6) FULL RATCHET.** `python -m eval.harness --full` on a checkout where it can run, reading
actual RATCHET FAIL / NEW FAILURES output. **UNRUN and not runnable in `~/hip-cutover-demo`**
(no `.env.dev`, no in-checkout registry — the known gap `REQ_UNRESOLVED_SUBJECT_GUARD` already
records). D-D-158 ran the pytest standing battery instead: zero delta, sorted failure sets
diffing empty both directions. **Requirements Discipline item 12 is therefore NOT satisfied by
this REQ**, and that is stated rather than papered over.

## WHAT'S ALREADY DONE

Do not rebuild any of this.

- **`is_question_utterance` + `_DECISIVE_QUESTION_OPENER_RE`** — `harness/injection_contract.py:372-393`, shipped `30adeaf`.
- **The structural force inside the contract** — `:697-699`, including `and not _forced_question` on the SIO branch. This is the only enforced site.
- **The three caller-side edits** — `orchestrator.py:633`, `realtime_adapter.py:572`, `voice_orch.py:2517/2521`.
- **Live acceptance of `REQ_UNRESOLVED_SUBJECT_GUARD`'s six checks** — reported PASS by D-D-158, (c) keyed on maya and A/B-proven across with-fix / pre-fix / with-fix-again.
- **`is_declarative_utterance` was never the defect** — it already returned `False` for "Why blue sky?" via its `"?" in t` test. The defect was the four sites that could set `is_declarative` **after** it returned. Verified by reading; do not re-diagnose.

## WHAT'S KNOWN BROKEN

1. **`has`/`have` fall through the decisive test** (measured, §(c)). The TD-D-154 leak shape survives on two tokens.
2. **The mid-text-"?" divergence** (measured, §(a)). Same sentence, different verdict, decided by SIO liveness.
3. **`server/voice_orch.py:571` duplicates L1's interrogative half** with no recorded reason.
4. **Eight raw-legacy decision sites never see the decisive test** (§(b)).
5. **`harness/realtime_adapter.py` and `harness/confirmation_gate.py` never call `apply_injection_contract`** — the structural force cannot reach them by construction. See the SURVEY.
6. **THE CODE IS NOT ON `roadmap`.** `30adeaf` is on `demo-cutover-build` only. Anyone reading this REQ in a roadmap checkout will not find the functions it describes.
7. **The full ratchet is unrun** (§(6)).

## CONSTRAINTS

- **Do NOT revert `30adeaf`.** Bill's instruction at D-R-188: *"the fix works and closed both leaks."*
- **Do NOT merge L2 into L1.** Merging would pull L1's imperatives (`tell show give list name remind explain trace`) into the decisive, non-overridable path and silently change the INJ-2 declarative bypass that D-D-158 was told to leave alone. Any consolidation ruling must address this first.
- **Do NOT amend ORTH-1.** Standing ruling. DC-061 and DC-080 stay as written and stay unguarded.
- **Genuine declaratives must still admit.** The INJ-2 declarative bypass and the correction rule are the working path; widening question detection must not break them.
- **`fact_change.py`'s internal gate at `:918-924` is defence in depth, not the mechanism.** Do not remove it while closing anything above.
- **Missing sensitivity RAISES.** No default introduced anywhere near this axis.
- **The frozen demo (`~/hip-dev`, Neo4j 7689) is untouched.**
- **C9 is not ruled by this document. Nothing here is MET.**

## SURVEY — every list, every consumer, every route

Reproduced in full in
`docs/dispatches/DISPATCH_QUESTION_REQ_RETROFIT__four-lists-every-consumer-and-two-that-bypass__v20260805_1536.md`.
The two that bypass the main path — `harness/realtime_adapter.py` and
`harness/confirmation_gate.py`, neither of which calls `apply_injection_contract` — and the
per-route trace of the same sentence live there.

## NOT RULED

Nothing in this document marks any requirement MET. (a), (b) and (c) are UNDETERMINED. No code
was changed by the dispatch that wrote this. `TD-D-154`'s remaining half (the false Ray
rationale in the comment block) is untouched. The carve-out's other 26 subjectless rows remain
unruled. C9 is not ruled.
