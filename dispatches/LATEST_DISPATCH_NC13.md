# NC 13 — VOICE MIGRATION INTO THE KERNEL (F1 CAPABILITY, OPTION C)
Status: **PARTIAL — the gate landed and is proven; the decommission was not earned**
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ **`4ec102e`**. Board claim
`fde5aaf`/`3517473`; REQ `395592a`.

REQ: `docs/requirements/REQ_VOICE_INTO_KERNEL__f1-pipecat-pre-generation-dispatcher-fail-closed-decommission__v20260814_2013.md`
— filed **before the first code edit**.

---

## 0. THE EXCEPTION LINE

```
NC 13 — VOICE MIGRATION INTO THE KERNEL (F1 capability, option C)
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

**V1–V6 landed and are proven on the live path's code. V7 — the decommission — DID NOT
HAPPEN, and the branch count is reported going the wrong way rather than dressed up.**

---

## 1. WHAT LANDED

`harness.kernel.governed_decision(req) -> TurnDecision` is the **one deterministic
pre-generation dispatcher**, and `server/voice_orch.py:1682` is the line where the live
Pipecat path enters it:

```python
_kreq = spoken_request(query, claimed_member=self._member_id, session_id=self._session_id)
_kdec = await governed_decision(_kreq)
if not _kdec.proceed:
    self._last_reply = _kdec.reply or ""
    await self._speak(_kdec.reply or "")
    return True
```

**Everything above that line is transport, speaker identity and control-flow handling, and
none of it sends the transcript to a model.** From it, the governance-bearing pre-generation
decisions are the kernel's, and **streaming diverges only after `proceed=True`** — which is
exactly the shape the objective asks for.

| acceptance | result |
|---|---|
| **V1** voice builds a `TurnRequest`; the kernel decides | **PASS** — and the same dispatcher serves both modalities, asserted side by side |
| **V2** F2 — any exception in the governed stage fails closed | **PASS** — refuses, and **the model counter observes zero calls**; the reply says it will not answer rather than guessing |
| **V3** equivalence, text vs voice | **PASS** — `proceed`, `outcome`, `refusal_reason`, `reply` and `member` all match; **only the modality differs** |
| **V4** structural refusal = server refusal, no LLM, TTS renders, **with all models down** | **PASS** — `openai.AsyncOpenAI` made unconstructable; the refusal is still produced, is text, and is one utterance |
| **V5** latency | **19.2 / 19.4 / 21.8 / 22.3 / 19.5 ms; worst 22.3 ms** for the gate itself |
| **V6** grounding non-regression, actually exercised | **PASS** — a public turn reaches generation with its utterance intact; and the gate is proven not to be a blanket refusal |

**11 twins, every one executing. No source-text assertions.**

`/ws/voice`, `demo_dashboard` and the C8 surface were **not imported and not touched**, per
the ruling. **No route was retired** — the keeper table stands.

---

## 2. ⚠ WHAT DID NOT LAND — MEASURED, NOT ASSERTED

**V7 (decommission) did not happen, and item 1's full scope is not met.**

```
_on_user_text    lines 689 -> 712    control-flow 55 -> 56    delta +1
_governed_turn   lines 934 -> 934    control-flow 46 -> 46    delta  0
```

**Nothing was removed. The count went UP by one — the gate itself.**

**Why, stated as the reason and not as an excuse.** The kernel now owns the **store-down** and
**fail-closed** decisions. It does **not** yet own **speaker identity, confirmation,
disclosure, or memory-write** — those still live in `_governed_turn` for text and in
`_on_user_text`'s own flow for voice. So the parallel code that V7 would delete is code the
kernel **does not yet own**, and deleting it would remove governance rather than de-duplicate
it.

**The REQ's own OPEN section required exactly this answer:** *"how much of the 689 lines can
be decommissioned safely in one dispatch is an empirical question, and the answer must be
MEASURED and reported, not asserted. Removing governance code that the kernel does not yet own
would be a regression dressed as cleanup."* **It was measured. The answer is: none of it,
yet.**

**So the objective's headline — *"after this capability there is no second governance-bearing
decision path on voice"* — is NOT yet true**, and this dispatch does not claim it. What is
true is narrower and worth having: **no voice turn can now reach a model without passing the
kernel's pre-generation decisions, and a failure in that stage cannot forward the transcript.**

**One residual governance decision remains inside `_on_user_text`** — the `permit()` call at
`:2067`. That one is **correct where it is**: the gateway is a chokepoint at the egress point,
not a pre-generation decision.

---

## 3. SUITE DELTA

```
after NC 13 : 20 failed, 499 passed, 39 skipped, 21 errors
baseline    : 20 failed, 488 passed, 39 skipped, 21 errors
NEW: (none)     FIXED: (none)     +11 passed = exactly this dispatch's twins
```

Failure **SET** compared, not counts alone, by stashing only the source edits and hiding the
new test file.

---

## 4. FILED, NOT BLOCKING (2)

**(NC13-1) The capability is PARTIAL and the remaining half is the larger one.** Moving
speaker identity, confirmation, disclosure and memory-write into the kernel means
restructuring ~700 lines of a **live voice path**, and this worktree cannot exercise that path
end to end — no audio, no WebRTC, no services. **A half-migration verified only by unit twins
would be worse than a clean stop**, so the gate landed and the rest is named. The next
capability should own one decision at a time, each with its own equivalence twin, so the
branch count can be watched going *down*.

**(NC13-2) The gate costs ~20 ms per voice turn, and it is the store connectivity probe.**
Against M-0's baseline that is small, and it buys the refusal. But it is paid on **every**
turn including public ones, and a cached "known up" with a short TTL would remove most of it.
**Not done here** — caching a liveness answer is precisely the mistake NC 11's throwaway
driver avoids, and getting it wrong reintroduces finding 1.

---

## 5. WHAT THIS DISPATCH DID NOT DO

- **Touched no `~/hip-vo`, no `/ws/voice`, no `demo_dashboard`, no C8 surface.**
- **Retired no route** — the keeper table stands.
- **Removed no governance code** — §2, deliberately.
- **Stood up no service and wrote no graph.**
- **Did not claim the objective's headline.** §2.

---

## 6. CLAIM IMPACT

```
CLAIM IMPACT: none
```

---

## 7. NEEDS BILL

**One decision: whether to continue F1 as a sequence of single-decision migrations** (speaker
identity, then confirmation, then disclosure, then memory-write — each with its own
equivalence twin and a measured branch-count drop), **or to treat the pre-generation gate as
sufficient for now** and leave the parallel path in place until the live voice surface can be
exercised end to end.

**Nothing blocks either choice**, and the gate is safe to keep in both.
