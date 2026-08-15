# Script 03: Trust ladder / P8 monotonicity

`trust_ladder__v20260716_1600.json`
Version: v20260716_1600 MT
Supersedes: no prior prep doc (first one for this script)
Script supersedes: `trust_ladder__v20260715_1158.json`

---

# USE CASE

A caregiver reports a medication change for a family member. The existing record has stronger confirmation than the incoming report. HIP parks the update rather than overwriting. The caregiver confirms. The record promotes.

The room watches the trust hierarchy enforce itself. Nobody types a command. Nobody configures a rule. A fact with weaker evidence cannot overwrite a fact with stronger evidence — and the system makes the caregiver prove she means it before the record changes.

---

# WHAT THIS SCRIPT SHOWS

| Turn | Beat | What the audience sees |
|------|------|------------------------|
| T01 | Baseline retrieval | HIP answers from the CORROBORATED head. One active node. |
| T02 | P8 park | Cross-principal ASSERTED write refused to overwrite CORROBORATED head. Two active nodes. PARKED_UPDATE_REPLY spoken. |
| T03 | Held in limbo | Same question, two rows in context. Does the model respect the trust hierarchy? This is the variance beat — classify every run. |
| T04 | Confirm | **BROKEN. Do not present.** |

---

# PHRASING IS LOAD-BEARING — DO NOT IMPROVISE T01 OR T03

**T01 and T03 must be spoken as: "What medication is Ray on now?"**

The previous phrasing, "What's Ray on?", dies at D-02 before the gate it exists to demonstrate. With that phrasing, intent classifies as `knowledge` and the path exits at `guard_empty_set` with `admitted=[]`. "Ray" does not resolve as a personal subject. The D-05 pending_park_gate is never reached. The variance beat at T03 cannot run.

The word "now" was previously excluded to avoid temporal loading in the R05 case (model picking an active row from a time-ambiguous query). That concern is void. The D-05 `pending_park_gate` fires before the model when two rows are in context — neither row reaches generation, and the model cannot pick. "Now" is inert with respect to R05.

**Do not hand anyone the keyboard on T01 or T03.** An engineer who phrases it naturally — "What's Ray on?" or "What is Ray taking?" — gets a guard refusal and the beat evaporates. The phrasing fragility is D-01/D-02 and is not fixed.

---

# T04 IS BROKEN — DO NOT PRESENT

T04: `"Yes, confirm that."`

`confirmation_gate.py` uses a closed vocabulary (`YES_VOCAB`). `"Yes, confirm that."` does not match. The gate does not fire. HIP replies `"Got it, confirmed"` — model-generated speech, plausible, false. The parked row stays UNRESOLVED after T04.

**Presenting T04 in front of an audience shows a feature that is not built.** The audience hears a confirmation. Nothing was confirmed. If anyone checks the graph afterward, the parked row is still there.

This is D-03. It is registered. It is not fixed. Until it is fixed, stop the script after T03.

---

# BEFORE YOU PRESS LOAD

Kill Ollama and restart before any run where T03 results matter:

```
pkill -f "ollama runner"; sleep 3
```

Ollama runner accumulates state. Skipping the restart makes T03 results non-reproducible.

---

# TURNS

| # | Speaker | Text | Path | Guard / note |
|---|---------|------|------|--------------|
| T01 | maya | "What medication is Ray on now?" | generation, edge | Single CORROBORATED head. Metformin. |
| T02 | maya | "Ray's on Jardiance 10mg now." | write, park | P8 fires. PARKED_UPDATE_REPLY. Two active rows. |
| T03 | maya | "What medication is Ray on now?" | pending_park_gate | D-05 gate fires. Template reply. Classify: does it name the head? |
| T04 | maya | "Yes, confirm that." | **D-03 BROKEN** | Gate does not fire. Do not present. |

---

# THE TWO BEATS

**After T01.**

> "One fact, one node, CORROBORATED. That's the head. What happens when Maya says the record is wrong?"

**After T02.**

> "The system didn't replace it. The incoming report is ASSERTED — Maya's word. The existing fact is CORROBORATED — something stronger than her word alone got it there. The trust hierarchy refused the overwrite. Both nodes are live. Maya has to claim it."

**After T03.** (This is the money beat — and it's the fragile one.)

Classify the response before narrating it. The model sees both rows — CORROBORATED head and UNRESOLVED park. It should surface the head and flag the park. On a bad run it answers Jardiance as fact.

> "Two values in the graph. The system prompt tells it the CORROBORATED row outranks the UNRESOLVED row. That's a model instruction, not a structural control. This beat shows you where the architecture is still soft."

---

# T03 VARIANCE — CLASSIFY EVERY RUN

T03 is structurally non-deterministic. The model sees both admitted rows. Record the response category for each run before presenting:

| Category | Reply | Verdict |
|----------|-------|---------|
| (a) | Named metformin AND flagged Jardiance as unconfirmed | Correct |
| (b) | Answered Jardiance as the current medication | Wrong — park bypassed |
| (c) | Said metformin, no mention of park | Partially correct, governance beat lost |
| (d) | Other | Investigate |

Do not present this script without at least three consecutive category-(a) runs. If you are getting (b) or (c), the run conditions are not stable — restart Ollama and try again. If (b) persists, do not present the script; the structural gap is showing.

---

# VERIFY BEFORE PRESENTING

| Item | Why |
|------|-----|
| T01 returns metformin | If it guards, "What medication is Ray on now?" is not resolving. The phrasing failed. Do not present. |
| T02 returns the PARKED_UPDATE_REPLY verbatim | If it returns anything else, P8 did not fire. Stop. |
| T03 category (a) on three consecutive runs | Before presenting to anyone. |
| T04 is excluded from the run | Never present a broken feature. |
| Neo4j after T02: two active Fact nodes for (maya, ray, medication) | One CORROBORATED, one UNRESOLVED. If there is one node, P8 did not fire. |

---

# KNOWN BROKEN / DO NOT PRESENT

| Defect | Turns affected | Status |
|--------|----------------|--------|
| D-03: YES_VOCAB closed vocabulary misses natural confirmation phrases | T04 | NOT FIXED. Stop at T03. |
| D-01/D-02: intent classification phrasing-fragile | T01, T03 | NOT FIXED. Use exact phrasing. No keyboard hand-off. |
| D-05: R05 double-context (G4 gate) | T03 | FIXED — pending_park_gate template replaces model reply when two rows are in context. T03 now returns the template, not a model guess. |

---

# ENGINEERING DETAIL

## P8 write monotonicity

`store.py:400-415`. On any cross-principal write (`subject != owner`) where incoming trust < head trust, `encode()` overrides SUPERSEDE to UNRESOLVED. The head is retained. The incoming fact is written as a parked row with `write_state=unresolved`.

Levels, descending: CORROBORATED > ASSERTED > INFERRED > CANDIDATE.

Maya (ASSERTED) cannot overwrite Ray's record (CORROBORATED). Not by prompt. Not by phrasing. By the trust arithmetic.

## P10 confirmation

`confirmation_gate.py:148-183`. Token registered at park time: `actor=maya, owner=maya, subject=ray, attribute=medication`. `YES_VOCAB` match promotes the parked row to ASSERTED, closes the CORROBORATED head (`valid_to` set), and consumes the token.

**D-03 caveat**: `YES_VOCAB` is a closed list. Natural confirmation phrases not in the list ("confirm that", "yes confirm", "that's right") pass through to the model, which speaks something plausible and does nothing. Until D-03 is fixed, T04 is cosmetic.

## D-05 pending_park_gate

When a query turn follows a park turn and both rows are in the admitted set, `pending_park_gate` fires before generation. The model is not called. The template reply is substituted. `record.reply_source = "pending_park_gate"`. G4 no-double-valued-attribute excludes these turns because two rows were admitted by design (the gate logic needs both to decide) but neither reached the model.

This is what makes T03 presentable despite structural non-determinism at the injection level: the gate fires first. The variance risk (category (b) runs) belongs to queries where the double-context escapes the gate, which is not the trust_ladder scenario — it is the residual R05 case for phrasings the gate pattern does not match.
