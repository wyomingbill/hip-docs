# NC 9 — KERNEL EXTRACTION: ONE `governed_turn()` (CAPABILITY)
Status: BUILT — **LANDED** on `nc-b0`
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ **`05a356c`**. Board claim
`0b72c3e`/`6c1898b`; REQ `31c65f0`.

REQ: `docs/requirements/REQ_KERNEL_GOVERNED_TURN__delta-typed-result-strip-only-web-store-down-refuse__v20260814_1803.md`
— a **DELTA** per R-NC1-1, filed **before the first code edit**.

---

## 0. THE EXCEPTION LINE

```
NC 9 — KERNEL EXTRACTION: ONE governed_turn() (CAPABILITY)
COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING
```

**Kernel built, both rulings inside it, 19 executing twins, equivalence proven end-to-end,
zero new suite failures. NEEDS BILL: nothing.**

---

## 1. THE DELTA — WHAT WAS *NOT* BUILT MATTERS MOST HERE

**`server.voice_orch.process_governed_turn` already IS the one governed turn.** It takes a
`TurnRequest`, derives the member from the principal, raises `ClaimMismatch` in exactly one
place, and binds provenance across the whole turn so all fourteen record-emit sites inherit
it. **That contract was referenced and not rebuilt** — re-implementing it would have created
the second copy this capability exists to prevent.

**A correction to NC 7's own framing, carried into the REQ so the scope was not set from a
wrong number:** the map counted *8 duplicate implementations*, and **both `/api/text-query`
routes already call `process_text_query`**. The text-path duplication is at the **HTTP
surface**, not in the turn logic. So the kernel work was **typing and ruling**, not
de-duplicating a second turn — and one edit to the shared adapter gave both routes the
rulings without either route being touched.

---

## 2. THE KERNEL — `harness/kernel.py`

`governed_turn(req) -> TurnResult`. `TurnResult` carries `reply`, a typed `outcome`,
`modality`, `member`, `session_id`, `refusal_reason`, and — load-bearing — **`model_called`**.

The proven turn returns a bare `str` from **fifteen** return statements across ~930 lines, so
a caller could see what was *said* and never what *happened*. Now it can.

**Adapters:** `text_turn` / `text_reply` (typed) and **`voice_turn` (spoken)** — a real,
callable adapter, so *"voice is an adapter"* is a signature rather than a sentence.
**Migration of the live pipecat path is F1 and was not done here.**

---

## 3. RULING — STORE-DOWN REFUSE

**Decided BEFORE the turn is entered.** A refusal that happens after the model has spoken is
not a refusal, it is a retraction — so `model_called=False` is a fact about the process, not a
claim about it, and the twin asserts it at the boundary rather than reading the reply.

| direction | behaviour |
|---|---|
| **household turn, store down** | structural refusal, **no answering model call**, reply names the cause |
| **public turn, store down** | **still answers** |
| **cannot classify** | **household** — fail closed (B4) |
| **probe raises** | **down** — an exception is not optimism |

**The refusal is structural.** NC 8 measured the old path saying *"Trash pickup is on
Wednesdays. I don't have that confirmed yet."* — the governance layer was working, but the
model invented a specific household value. A twin asserts `"Wednesday"` cannot appear.

**Household-dependence reuses NC 8's typed intent outcomes**, which is the payoff of that
dispatch: an unusable classification can now mean *"assume household"*, an answer the old
permissive `knowledge` fallback could never give.

---

## 4. RULING — STRIP-ONLY WEB SEARCH

NC 8 left web egress failing closed **pending exactly this ruling** (NC8-1). It is now:

- **`Destination.WEB_SEARCH`** — in `OFF_DEVICE` (so it is stripped) and in a new
  **`STRIP_ONLY`** set (so **no consent gate** is imposed).
- **The test is inspectable, as the REQ's OPEN section required**: *a query is safe iff
  stripping does not change it.* If the strip removed something, the query was carrying
  protected household information — and a search query carries only what it needs, so what
  was removed was intrinsically required. Sending the remainder asks a different question and
  gets an answer to it, **which is worse than refusing because it looks like it worked.**
- The refusal is its **own exception type**, `EgressIntrinsicallyRequiresHousehold`, so the
  governed consent path can route it later **without parsing a message** — that is the seam
  the ruling's second half will attach to.
- **The permitted query REPLACES the original at both call sites.** Asking the gateway and
  then sending what you had is the hole a bare permission check leaves open; a twin asserts
  the original string never reaches the wire.

**The REQ's unsettled middle** — a query about a public place the household happens to live
near — **resolves to REFUSE**, because the strip decides and the strip is conservative. Stated,
not silently chosen.

---

## 5. EQUIVALENCE RESULT

**PASS, in both the weak and the strong form.**

| form | what it proves |
|---|---|
| **A2** — same request, doubled turn on both sides | reply identical; the same utterance reaches the turn; `member`, `modality`, `session_id` all match |
| **A2b** — **end-to-end through the REAL `process_governed_turn`, twice** | the old path answers, the kernel answers, `outcome=ANSWERED`, `model_called=True`, member and modality match the request |

The store probe is forced UP in A2b **so the ruling does not fire** — otherwise the two sides
would differ *by design* and the comparison would be measuring the ruling instead of the
equivalence. Nothing else is doubled.

**A2c** proves the shared adapter now inherits the ruling: `process_text_query` returns the
structural refusal and the turn is never entered — **both `/api/text-query` routes, one edit.**

---

## 6. TWIN COUNTS AND SUITE DELTA

**19 executing twins in `eval/test_kernel_governed_turn.py`. No source-text assertions.**

| group | twins |
|---|---|
| A — typed result, equivalence, adapters | **7** |
| B — store-down refuse, both directions + fail-closed | **6** |
| C — strip-only web search, both directions | **6** |

Combined with NC 8's file: **40 tests, all passing.**

**SUITE: 21 failed / 476 passed / 38 skipped / 21 errors — the failure SET is IDENTICAL to
baseline. Zero new, zero fixed.** Established by stashing only the source edits and hiding
the new test file, then comparing sets rather than counts.

---

## 7. ⚠ THREE GUARDS THIS PROJECT ALREADY HAD CAUGHT THREE REAL DEFECTS IN THIS WORK

This is the most useful thing in the dispatch and is recorded rather than smoothed over.
**Every one was a defect in code I had just written, and in each case the existing guard was
right and I was wrong.**

1. **`test_HA65_no_name_is_used_before_its_own_function_level_import`** caught an
   **UnboundLocalError hazard** in `kernel.py`: `impl = turn_impl` followed by
   `from … import process_governed_turn as impl` binds `impl` as a local at the import line,
   so the read above it is unsafe. Fixed by importing under a different name.
2. **NC 8's own refusal twin** caught a **lost contract**: routing `process_text_query`
   through the kernel swallowed `ClaimMismatch` and returned `""`. Both `/api/text-query`
   routes catch that exception — `demo_dashboard.py` imports it for exactly that. Re-raised.
3. **`test_A1_there_is_exactly_ONE_governed_implementation`** caught **a branch growing in the
   adapter** — its rule is *"any branch here is a second governed path"*, and my re-raise from
   (2) was that branch. **The guard is right**, so the branch moved into the kernel's own
   adapter layer (`text_reply`) where it is part of the one implementation. `process_text_query`
   is branch-free again, measured by AST: **0 control-flow nodes.**

---

## 8. FILED, NOT BLOCKING (3)

**(NC9-1) Two of NC 8's assertions are superseded, and are annotated rather than rewritten.**
NC 8 asserted that off-box search classified to `None` — refused — and said explicitly that the
policy did not exist yet. Bill's ruling created it, so those assertions now expect
`WEB_SEARCH`, with the supersession recorded in each docstring. **A1's guard is annotated the
same way**: its delegate moved one level *more* central, and its load-bearing half — the
no-control-flow rule — is untouched.

**(NC9-2) With the classifier uninitialised, a store-down machine refuses EVERYTHING.**
B4's fail-closed rule makes every turn household-dependent when the classifier cannot answer,
and `initialize()` needs embeddings — so a machine with both the graph and the embedder down
refuses every turn, including public ones. **That is the rule working**, and it is the correct
direction to fail. It is filed because it is an operational consequence someone will meet, and
because the fix is deployment discipline (initialise the classifier) rather than a softer rule.

**(NC9-3) My own edit silently no-op'd once.** A `str.replace` whose anchor did not match left
a test unchanged while reporting success, and the failure only surfaced on the next run.
Re-done with an assertion on the match count — the same discipline `claim_lane.py` enforces on
board edits. **An unasserted replace is a silent write.**

---

## 9. WHAT THIS DISPATCH DID NOT DO

- **Never touched `~/hip-vo`.** All work in `~/hip-nc2` @ `nc-b0`.
- **Did not migrate voice.** `voice_turn` is the seam; the live pipecat path is untouched and
  migration is F1.
- **Did not rebuild the governed turn** — the delta only.
- **Did not de-duplicate the HTTP-surface routes** — out of scope, and §1 explains why they
  were never the turn-logic duplication anyway.
- **Wrote no graph, stood up no Neo4j, started no service.**
- **Weakened no existing guard.** Two were annotated where a ruling superseded them; the
  load-bearing half of each is intact.

---

## 10. CLAIM IMPACT

```
CLAIM IMPACT: none
```

---

## 11. VERIFIED

- **REQ `31c65f0` precedes the code `05a356c`** and contains no source file.
- `lane_preflight.py` passes on `~/hip-nc2` before and after.
- 19 kernel twins + 21 NC 8 twins = **40 passing**.
- Suite failure **set** identical to baseline; comparison run twice, the first attempt's
  measurement error corrected rather than reported.
- Board rows via `claim_lane.py` under the repo lock, board-only, no passengers.
