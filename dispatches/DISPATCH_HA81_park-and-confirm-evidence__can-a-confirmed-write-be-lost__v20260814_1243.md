# DISPATCH_HA81 — park-and-confirm evidence: can a confirmed write be lost?
Status: BUILT
Reconciled-Against: `roadmap` @ this dispatch's commit

**TYPE:** MEASUREMENT / ANALYSIS — **evidence only. No fixes, no pin changes.**
No product code was changed.

**REQ:** **NONE**, correctly — a measurement dispatch. CLAIM IMPACT: none.

**Graph:** `bolt://localhost:7688`, this tree's own pin. The demo graph (7689)
was never touched and no key operation was performed. All test rows were written
under a **test-scoped subject** and deleted afterwards; residual test rows
verified **0**.

**THE QUESTION:** after a user confirms a parked write, can the change be lost
with no refusal, no record, and no retry?

## THE ANSWER, PLAINLY

> **YES — on one path, and it is the most likely one in production.**
>
> When the parked row is no longer open at commit time, `apply_confirm` returns
> `False`, **the caller discards that return value**, and the user is told
> *"Confirmed — the record has been updated."* Nothing was promoted, nothing was
> raised, and no retry exists.
>
> The other two post-confirmation failure points fail **loudly**, and the parked
> data itself is never destroyed.

---

## 1. THE PATH, AND EVERY FAILURE POINT AFTER CONFIRMATION

```
park created        harness/fact_change.py  → encode() lands write_state='unresolved'
                                              (a REAL row in the graph)
token registered    confirmation_gate.register(actor, …, parked_fact_id)
                                              → _pending: an IN-MEMORY dict, never persisted
user says "yes"     confirmation_gate.check_confirmation()
                       └─ del _pending[member]      ← TOKEN CONSUMED HERE
                       └─ returns ("confirm", token)
commit              voice_orch.py:2899  apply_confirm(driver, token, …)
                       └─ ONE atomic Cypher: close old head(s) + promote parked row
reply               voice_orch.py:2900  _cg_reply = CONFIRM_REPLY
```

**Two structural facts decide the outcome:**

1. **The token is consumed BEFORE the commit runs.** `check_confirmation` deletes
   it and returns; `apply_confirm` is a separate call afterwards. There is a
   window in which the confirmation is spent but the promotion has not happened.
2. **`apply_confirm` returns `bool` and the caller discards it**
   (`voice_orch.py:2899` is a bare expression statement; AST-verified). It returns
   `False` when the parked row is not found open. `CONFIRM_REPLY` is then set
   **unconditionally** on the next line.

There is **no `try` anywhere inside `process_text_query`** (AST-verified), so a
raise propagates out of the turn.

| # | failure point after confirmation | mechanism |
|---|---|---|
| **FP-1** | process dies after the token is consumed, before `apply_confirm` | token gone, parked row still open |
| **FP-2** | parked row not open at commit (closed by a concurrent supersede, a consolidation pass, or a reset) | `apply_confirm` → `False`, discarded |
| **FP-3** | graph unavailable at commit | `apply_confirm` raises |

`apply_confirm` itself is **atomic** — a single Cypher statement closes the old
heads and promotes the parked row together — so a partial commit is not among
the failure points.

## 2. THE CLEAN PATH — 3/3

Live, through the real `process_text_query`:

```
clean run 1   told: CONFIRMED-UPDATED   raised: no   promoted: True (write_state=supersede)   token left: False
clean run 2   told: CONFIRMED-UPDATED   raised: no   promoted: True (write_state=supersede)   token left: False
clean run 3   told: CONFIRMED-UPDATED   raised: no   promoted: True (write_state=supersede)   token left: False
```

**The confirmed write lands 3/3.** The mechanism works.

## 3–4. FAULT INJECTION — VERDICT PER FAILURE POINT

| failure point | user was told | raised? | promoted? | parked data | **silently lost?** |
|---|---|---|---|---|---|
| **FP-1** process dies after confirm, before commit | *nothing* — the turn never completed | — | No | **survives**, `write_state='unresolved'`, still active | **NO** — not silent (no success reply), but the row is **orphaned**: its token is gone and nothing can resolve it |
| **FP-2a** parked row **deleted** at commit | **"Confirmed — the record has been updated."** | no | No | gone | **YES** |
| **FP-2b** parked row **closed** at commit *(realistic)* | **"Confirmed — the record has been updated."** | no | No | still `unresolved` | **YES** |
| **FP-3** graph unavailable at commit | *nothing* — turn failed | **yes**, propagates | No | survives | **NO** — loud |

**FP-2b is the one that matters**, and it was tested precisely because FP-2a
(deletion) is artificial. `apply_confirm` matches on `p.valid_to IS NULL`, so a
parked row that has merely been **closed** — by a concurrent supersede, by
`consolidate.py`, or by a demo reset between the park and the confirmation —
fails identically. That is an ordinary production sequence, not a contrived one.

**What the user experiences in FP-2:** they were asked to confirm, they
confirmed, and they were told the record was updated. It was not. Nothing in the
turn, the reply, or the logs contradicts the claim.

## WHAT IS *NOT* BROKEN, said as plainly as the defect

* **The parked data is never destroyed by any of these.** In FP-1 and FP-3 the
  `unresolved` row survives intact.
* **`apply_confirm` is atomic.** No half-committed promotion.
* **The confirmation itself cannot be faked** — deterministic vocabulary, bound to
  the authenticated member, no model call (`check_confirmation`'s own contract).
* **FP-3 is loud**, which is the correct behaviour for an unavailable graph.

## 5. FIX OPTIONS — proposals only, Bill rules

| option | what it does | cost / risk |
|---|---|---|
| **A. Use the return value** | `if not apply_confirm(...): _cg_reply = <a reply that does not claim success>`. | **One line, plus a reply string.** Removes the falsehood exactly, using a signal the function already computes and already returns. No new state, no retry semantics. Lowest-risk fix on the table. Does not recover the write — it stops the system claiming one. |
| **B. A + re-park on failure** | On `False`, leave/re-create the pending token so the user can be asked again. | Recovers the interaction rather than just reporting it. Costs a decision about TTL and about what happens if the row was closed *because* a newer value superseded it — re-parking a stale assertion could resurrect a value the user already replaced. Needs a ruling, not a patch. |
| **C. Commit before consuming the token** | Move `del _pending[member]` after a successful `apply_confirm`. | Closes FP-1's orphan window too. But it changes the gate's consumption semantics, and a naive move risks double-application on a retry — the reason it is separate from A rather than bundled with it. |
| **D. Persist the pending token** | Survive process death. | Largest change, and it puts confirmation state on disk — which collides with the memory-only custody properties Q1–Q3 assert. **Not recommended without a ruling on that tension.** |

**A is the minimal honest fix**; B and C are behaviour changes that need Bill's
ruling; D has a custody implication that should be decided before it is built.

## VERIFIED

**Watched run:** the 3 clean confirmations; FP-1, FP-2a, FP-2b and FP-3 each
fired live through `process_text_query` on graph 7688; graph state read back per
case; residual test rows verified 0 afterwards.

**Reasoned about:** the AST facts (return value discarded, no enclosing `try`)
were read from the source rather than exercised by forcing every caller path —
but both are corroborated by the live results above, which is why they are stated
as findings rather than as inferences.

**Note on FP-3's method:** the raise was injected at the `apply_confirm` boundary
rather than by taking the graph down, because taking 7688 down would have
affected other lanes on this machine. That tests the caller's handling — which is
the question — and is named here rather than presented as a full outage test.

## OPEN — NEEDS BILL

1. **FP-2 is a real silent-loss path** — which fix option, if any.
2. **FP-1 leaves an orphaned parked row** whose token is gone. Nothing reaps or
   re-offers it; it simply stays `unresolved` forever. Whether that needs a
   sweeper is a separate ruling.
3. **Option D's tension with Q1–Q3** (memory-only session state) should be
   decided before anyone persists confirmation tokens.
