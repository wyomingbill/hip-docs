# DISPATCH_HA82 — confirmed-write honesty (FP-2 Fix A) + ruled G1 exemption
Status: BUILT
Reconciled-Against: `roadmap` @ `19873a5`

**TYPE:** BUILD

**REQ (part 1):** `docs/requirements/LATEST_REQ_D03_D18.md` — the confirmation gate.
**REQ (part 2):** `REQ_HARNESS__orthogonal-e2e-regression-per-push__v20260715_1700.md`
— record invariants G1–G4, as the harness itself cites them.

Both pre-exist; neither was written retroactively.

**Graph:** `bolt://localhost:7688` only. Demo graph never touched. Test rows used
test-scoped subjects; **residual rows verified 0.** No `--full`, no battery
(VD-60 owns the heavy slot).

---

## PART 1 — FP-2, RULED FIX A

HA-81 measured it: `apply_confirm` **already returned `False`** when the parked
row was no longer open at commit; the caller **discarded** the bool and told the
user *"Confirmed — the record has been updated."*

**The return value is now consumed.** On `False` the reply is
`CONFIRM_FAILED_REPLY` — no success claim — and a warning names the parked row
and the key.

**The record carried the same falsehood, one layer deeper and more durable.**
The d1.1 confirmation block set `"promoted_to": "ASSERTED"` whenever the verdict
was `confirm` — keyed on the user saying yes, **not on the promotion happening**.
It is now keyed on the commit result and additionally carries `"committed"`
structurally, so a reader or a future sweeper can find confirmations that did not
commit **without parsing reply text**.

**Not done, because not ruled:** no re-park (option B), no consumption-order
change (option C). Token persistence (option D) was **rejected by Bill**.

### Acceptance — live, graph 7688

| | required | result |
|---|---|---|
| **1** | FP-2a rerun (row deleted) — failure spoken and recorded | **3/3** |
| **2** | FP-2b rerun (row closed — the realistic shape) | **3/3** |
| **3** | anti-vacuity: clean confirmed write still lands and says so | **3/3** |
| **4** | FP-1 and FP-3 behaviour unchanged | **unchanged** |

```
(3) clean run 1-3   told: CONFIRMED-UPDATED   promoted: True (write_state=supersede)
(1) FP-2a run 1-3   told: "I couldn't complete that update…"   promoted: False (ROW GONE)
(2) FP-2b run 1-3   told: "I couldn't complete that update…"   promoted: False (still unresolved)
```

**FP-1** still leaves the parked row intact but **orphaned** (token consumed, user
told nothing — the turn never completes). **FP-3** still raises out of the turn.
Both identical to HA-81's measurements: this fix changes only the case that was
lying.

## PART 2 — THE RULED G1 EXEMPTION

> **Bill, verbatim:** a determined restatement is exempt from G1 **ONLY** when the
> record structurally carries `already_recorded=true`. Never a wording or model
> judgment, never a generic bypass. G1 still fires on unsupported generation.

**The marker did not previously reach the record at all.** HA-80 set
`already_recorded` on the detection *outcome*, and only `delta`/`park` were
projected into the d1.1 record. So the exemption had nothing to key on.
`harness/epistemic_record.py` now carries the field and the emit site passes it.

**The exemption is `r.get("already_recorded") is True`** — `is True`
deliberately, not truthiness: `None` means the check never ran for that turn, and
an absent or unparsed field must never earn an exemption.

### Acceptance — one twin per clause

| clause | case | result |
|---|---|---|
| 1 | restatement **with** the marker | **G1 silent** |
| 2 | planted unsupported generation | **G1 fires** |
| 3 | restatement **without** the marker (`False`, `None`, absent) | **G1 fires** |

Plus: **only the boolean `True` earns it** — `1`, `"true"`, `"True"`, `"yes"`,
`[1]`, `{"a": 1}` all still fire; the exemption node reads the marker **and
nothing else** (AST, scoped to the guard rather than the whole function, so it
does not match G1's own pre-existing subject normalisation); and the marker
demonstrably reaches the record.

**16 tests, all green** (`eval/test_confirmed_write_honesty.py`).

## RESULTING L6 STATE — reported precisely, not rounded up

`--layer 6` still reports **`G1 no-orphan-generation: FAIL (1)`**, and that is the
ruling working rather than a gap.

`turns_demo.jsonl` **accumulates**, and it now holds **two** restatement-shaped
turns:

| record | `already_recorded` | scored through `g1` |
|---|---|---|
| from **HA-80**, before the record carried the marker | `None` | **FIRES** |
| from **HA-82**, this dispatch | `True` | **SILENT (exempt)** |

So the remaining `FAIL (1)` is the **legacy** record — which is exactly clause 3:
*the exemption is the marker, not the shape of the turn.* A turn that looks
identical but predates the marker is still counted, by design.

**No pin, baseline or expectation was changed.** Whether the accumulated legacy
record should be aged out of `turns_demo.jsonl` is not this dispatch's call.

## VERIFIED

**Watched run:** all nine live confirmation cases (3 clean, 3 FP-2a, 3 FP-2b);
FP-1 and FP-3 re-fired; the 16-test suite; both restatement records scored
directly through `g1_no_orphan_generation`; `--layer 6`; the battery-manifest
test after registering the new file; residual test rows measured at 0.

**Reasoned about:** that FP-1's and FP-3's *code paths* are untouched — argued
from the diff (only the `confirm` branch changed) and corroborated by re-running
both, rather than by exhaustively re-deriving their behaviour.

**Also included:** `eval/test_groq_model_centralized.py`'s tree-aware skips — my
own HA-78 change, committed in the other three trees and left uncommitted here.
Named rather than slipped in.

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **FP-1's orphaned parked rows** — out of scope by instruction, filed. A
   confirmation consumed with no commit leaves an `unresolved` row that nothing
   reaps or re-offers.
2. **The legacy `turns_demo.jsonl` record** keeps L6's G1 at FAIL(1). Whether
   accumulated pre-marker records should age out is a separate call.
3. **`"committed": false` is now a findable signal** in the record. Whether
   anything should sweep for it — a confirmation that did not commit is exactly
   the thing worth noticing — is unbuilt and unruled.
