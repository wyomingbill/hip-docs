# DISPATCH_HA79 — missed-save evidence: the L6 G1 violation from HA-77 C4
Status: BUILT
Reconciled-Against: `roadmap` @ this dispatch's commit

**TYPE:** MEASUREMENT / ANALYSIS — **evidence and root cause only. No fixes, no
pin changes, no expectation rebases.** Nothing in this dispatch changes product
behaviour.

**REQ:** **NONE**, and correctly so: this is a measurement dispatch, not a build.
CLAUDE.md item 10 permits `REQ: NONE` for analysis and requires it be said plainly.

**Bill's framing:** *a user-confirmed memory change silently disappearing must not
become accepted behaviour.*

---

## 1. RECONCILIATION — VERDICT: **(a)**, and (b) is its mechanism

**HA-77's failure is TD-147's known shape recurring, and TD-147's own corrected
mechanism is TD-125's detector false negative.** (a) and (b) are not competing
answers here — they are the same finding at two levels. It is **not (c)**.

**TD-147, verbatim:**

> L6:record-invariants RED on both D-117 `--full` runs … ONE G1
> no-orphan-generation violation, the IDENTICAL record both runs — **[sam] "I
> take atorvastatin 20mg every morning."**

**TD-147's ADDENDUM (D-119), which corrected its own first mechanism:**

> TRANSPORT EXONERATED … The write dropped because gpt-oss-20b returned
> `changes:[]` — **DETERMINISTICALLY**: the smoke sequence asserts this utterance
> 5x per run (maya, sam ×3, bill), and outcomes are position-identical across
> both runs (**sam #2 — the instance whose facts_block contains the fact sam #1
> just wrote — fails 2/2**, first call AND temp-0.2 retry; the other four succeed
> 2/2). The payload class is **RESTATEMENT-OF-AN-ALREADY-RECORDED-FACT**, the
> P2/i019 `changes:[]` family.

**TD-125, verbatim:** *"gpt-oss-20b returns `changes:[]` for some multi-party
contexts, deterministic at temperature=0.0"* — the same family.

**HA-77's run matches TD-147 position-for-position.** From
`logs/harness_run.jsonl` (12 atorvastatin turns this run):

| # | owner | delta | reply |
|---|---|---|---|
| 6 | **sam** | **1** | "You take atorvastatin 20mg every morning to help manage your cholesterol levels." |
| 7 | **sam** | **0** | **"I heard that as an update, but I was unable to save it to the household record just now."** ← the G1 violation |

Turn #6 is sam #1 — it **wrote the fact**, `transition: supersede`,
`new_fact_id: 4c9ed0df-4ac4-40f9-88db…`. Turn #7 is sam #2, the restatement of
the fact #6 just wrote. Exactly TD-147's signature.

**The detector model is unchanged by HA-77/HA-78.** Those dispatches swapped
CORE generation (`llama-3.3-70b-versatile` → `openai/gpt-oss-120b`); detection
runs on `openai/gpt-oss-20b`, which was never the decommissioned model. So this
is **not** a consequence of the model swap.

## 2. ROOT CAUSE — where the save died

**Not transport.** `logs/write_latency.jsonl` for this run, owner=sam:

```
('write_committed', 'supersede', 'ok', 1) x 44
('write_committed', 'augment',   'ok', 1) x 22
('detect_no_changes', None,      'ok', 1) x 14
```

`groq_status=ok`, `groq_attempts=1`, **zero call failures** — the same
exoneration D-119 recorded. The call succeeded and returned nothing.

**It died at the detector.** The model returned `changes:[]` for a restatement of
a fact already in its `facts_block`, so `mutations==0 AND noops==0`, and
`voice_orch.py:2407`'s F3 gate replaced the ack with the unconfirmed reply.

**DETERMINISTIC — measured directly, 3 calls per shape, on today's detector:**

| facts_block | utterance | result |
|---|---|---|
| fact **ABSENT** | "I take atorvastatin 20mg every morning." | **1 change ×3/3** |
| fact **PRESENT** (restatement) | identical utterance | **0 changes ×3/3** |

The variable is the payload, not the run. An L6 rerun was **not** used to test
this: a bare `--layer 6` re-scores the existing log (`eval/harness.py:366`) and
never re-fires the model, so it cannot answer a determinism question. The
detector was probed directly instead.

**The no-op path starves.** As D-119 put it: F3 already handles restatements —
`mutations==0` with `noops>0` is not gated — so the design is correct. The defect
is that the model omits the restatement entirely, so `noops` never increments and
the gate sees a total blank.

## 3. THE QUESTION THAT MATTERS — answered from the record

> Can a user-CONFIRMED change (park-and-confirm completed) be lost with no
> refusal, no record, no retry? Or does the record honestly show the failure?

**On this path, NO — nothing is lost, and the record is honest about the
failure. The defect is the opposite of silence.**

1. **The fact was saved.** Turn #6 carries a real delta with a `new_fact_id` and
   `transition: supersede`. The user's medication is in the record.
2. **The failure was loud.** Turn #7 produced a spoken refusal — *"unable to save
   it to the household record"* — not a false ack.
3. **The failure was recorded.** `delta: []` in `harness_run.jsonl`,
   `detect_no_changes` in `write_latency.jsonl`, and G1 fired in L6. Three
   independent instruments caught it.
4. **A retry did run.** TD-125's temperature-0.2 resample fired and did not
   recover — as TD-147 measured, this class fails both calls.

**So the answer to Bill's concern is reassuring, but there IS a real defect
underneath it, and it is the inverse of the feared one: the system told the user
a FALSEHOOD about a fact it had already saved.** D-119 named this exactly —
*"F3's failure claim is FALSE for a fact that exists."* The user is invited to
re-state a change that is already recorded, and to distrust a record that is
correct.

**SCOPE LIMIT, stated rather than glossed: park-and-confirm was never involved.**
The failing turn carries `park = None`, `writes_pending = False`, and the run
registered **zero** confirmation-gate entries. This shape cannot reach
park-and-confirm, because the detector proposes nothing and there is therefore
nothing to park. **This evidence says nothing about whether a genuinely
park-and-confirmed change can be lost** — that is a different path and would need
its own dispatch. Not asserting it is safe on the strength of this one.

## 4. A NEW FINDING — the instrument for this class is broken

`server/voice_orch.py:2408` logs the F3 gate with **`%s` placeholders through
loguru**, which uses `{}` formatting:

```python
logger.warning(
    "[text-query] TD-121 F3: declarative produced no write "
    "(proposed=%s mutations=%s noops=%s) "
    "— replacing ack with unconfirmed reply",
    outcome["proposed"], outcome["mutations"], outcome["noops"])
```

The log therefore reads, literally:

```
TD-121 F3: declarative produced no write (proposed=%s mutations=%s noops=%s)
```

**The counters that distinguish "detector proposed nothing" from "proposed but
starved" are dropped on the floor** — in the one diagnostic written for this
failure class. Filed, **not fixed** (this dispatch changes nothing). It is a
one-line change whenever Bill wants it.

## 5. FIX OPTIONS — proposals only, Bill rules

| option | what it does | cost / risk |
|---|---|---|
| **A. Structural restatement check before F3 fires** | Before replacing the ack, compare the utterance's asserted value against the active facts for that key; if it already matches, treat as a no-op instead of a failure. D-119 scoped this as a lever. | Model-free and deterministic, so it fixes the FALSE claim exactly. Needs a value-comparison rule — and HA-74's TD-V-021 ruling already built one (`canonical_fact_value` + exact equality) that could be reused rather than invented. Risk: a too-loose comparison silently swallows a real change, the exact failure HA-74 forbade substring/fuzzy matching to prevent. |
| **B. Extraction-prompt re-assert semantics** | Teach the detector to emit an explicit no-op for a restatement instead of an empty list. TD-123's track. | Fixes the root cause rather than the symptom, and would also close TD-125's family. But it is prompt work against a live model with no reproducibility rule yet — cost is a measured recovery rate, not a patch, and item 12's amendment forbids inventing a threshold. |
| **C. Fail loud to the user, differently worded** | Keep the refusal but stop claiming the save failed — say the change could not be confirmed as new. | Cheapest and most honest of the three; removes the falsehood without touching the write path. Does not fix the starved no-op, so L6 G1 stays red. |
| **D. Retry-with-record** | Re-run detection and record each attempt. | **Rejected on the evidence**, and worth saying so: TD-147 measured retry already saturated for this class (fails both calls), and this dispatch's 3/3 confirms it. More retries buy latency, not recovery. |

**Nothing here should touch the baseline or the pin.** TD-147's red is deliberate
and Bill already ruled it stays loud with the baseline unupdated.

## VERIFIED

**Watched run:** the 12 atorvastatin records in `logs/harness_run.jsonl` including
the two decisive turns; `write_latency.jsonl` counters for owner=sam; the 3×2
direct detector probe; `park`/`writes_pending`/confirmation-gate fields on the
failing turn; the literal `%s` in the server log and the loguru import that
explains it.

**Reasoned about:** that the park-and-confirm path is unaffected — argued from
this turn never reaching a park, **not** from exercising that path, which is why
§3 states the limit rather than clearing it.

## OPEN — NEEDS BILL

1. **Which fix option**, if any. A and C are cheap; B is the real cure and is
   measurement work; D is rejected on evidence.
2. **The broken F3 diagnostic** — one line, filed not fixed.
3. **Whether the park-and-confirm path needs its own evidence dispatch.** This
   one deliberately does not clear it.
4. **TD-147 and TD-125 stay OPEN and unchanged.** This dispatch adds a third
   data point and a direct determinism measurement to TD-147; it rules nothing.
