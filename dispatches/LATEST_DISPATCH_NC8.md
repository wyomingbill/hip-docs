# NC 8 — B0 GROUND HARDENING (CAPABILITY DISPATCH)
Status: BUILT — **LANDED** on `nc-b0`
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ **`f6dcdd3`**, cut from `origin/main`
at `5c71e42`. Board claim `83802c7`/`d792be7`; REQ `f3a1302`.

REQ: `docs/requirements/REQ_B0_GROUND_HARDENING__typed-intent-failure-ungoverned-ingress-serpapi-permit-consumer-tests__v20260814_1733.md`
— filed **before the first code edit**. Map: NC 7's execution map, §9 and §§1.3, 3.2, 8.

---

## 0. THE EXCEPTION LINE

```
NC 8 — B0 GROUND HARDENING (CAPABILITY DISPATCH)
COMPLETE WITH FINDINGS — 4 ITEMS FILED, NOTHING BLOCKING
```

**All four items built. 21 executing tests, all passing. Zero new suite failures.**
**NEEDS BILL: two policy questions (§7) — neither blocks the build.**

---

## 1. THE WORKTREE — AND IT REPRODUCED THE NC 5 INCIDENT ON ARRIVAL

`~/hip-nc2` @ `nc-b0`, cut from `origin/main`. **`~/hip-vo` was never edited.**

**The moment the worktree existed, `lane_preflight.py` refused it:**

```
lane_preflight: REFUSED (exit 6)
  hip-nc2 targets 7691, which belongs to hip-vo.
```

`nc-b0` was cut from `origin/main`, which carries `~/hip-vo`'s lane files — so the new
worktree **inherited hip-vo's `.hip-owns` and `.hip-graph` verbatim** and declared a graph it
did not own. **That is exactly the `~/hip-nc` incident, reproducing itself on a fresh
worktree** — and the difference is the whole point of FM 9: *NC 5 was saved by the accidental
absence of a `.env.dev`; NC 8 was refused by the check built for it, before any edit.*

Corrected to **7693** (unclaimed by any lane), with the inheritance recorded in the files
themselves. Re-run: `OK — hip-nc2 @ nc-b0 writes bolt://localhost:7693`. **No Neo4j was stood
up and no graph was written.**

---

## 2. ITEM 1 — TYPED INTENT FAILURE · 8 TWINS

`classify()` now returns `IntentResult(intent, confidence, outcome)`.

| outcome | when | intent |
|---|---|---|
| `OK` | a route matched at or above threshold | the route |
| `NOISE` | filler utterance — a real answer, not a failure | `"noise"` |
| **`EMBEDDING_UNAVAILABLE`** | `embed_text()` returned `None` | **`None`** |
| **`BELOW_THRESHOLD`** | scored, but under `CONFIDENCE_THRESHOLD` | **`None`** |
| **`UNINITIALIZED`** | `initialize()` was never called | **`None`** |

**Three deliberate design choices, each closing a way the old bug could come back:**

1. **`UNINITIALIZED` is checked FIRST, and before spending an embedding.** It was previously
   invisible — an empty `_route_vecs` fell through the loop and returned the seeded
   `"knowledge"`, so **a deployment error presented as an ordinary low-confidence
   classification.** A twin asserts no embedding is requested in that state.
2. **`IntentResult` is deliberately NOT tuple-unpackable.** Any caller written against
   `intent, conf = classify(q)` now raises `TypeError` instead of silently receiving a
   permissive intent — **a migration that fails closed, like the thing it fixes.** One real
   caller was found and migrated (`eval/test_seam_s2_intent_routing.py:152`); a repo-wide
   search confirms none remain.
3. **`FAIL_CLOSED_OUTCOMES` is data, not a chain of `or`s at each call site.** A new failure
   mode is closed everywhere the moment it is added — the shape that let B0-1 survive was the
   check living at the call site instead of with the thing being checked.

**The caller fails closed (`harness/router.py`), and the REQ required the choice to be
stated rather than taken silently.** We do **not** drop the turn as the noise path does:
dropping would silence the assistant entirely whenever the embedder is down — a large
availability cost for a privacy gain available more cheaply. Instead the turn is pinned
**on-box (`TIER_LOCAL`), with no intent-driven branch and no escalation**, and the outcome
travels in the reason string so the three failures stay distinguishable in the routing log.

---

## 3. ITEM 2 — THE UNGOVERNED INGRESS IS CLOSED · 4 TWINS

`server/app.py` `POST /chat` now raises **410 Gone** and **reaches no model**. `GET /health`
is kept — it reads config, touches no model, carries no principal.

**Refused rather than deleted, on purpose:** a deleted route 404s with no explanation and the
next person who wants a quick local chat endpoint writes it again. A 410 that names the reason
and points at the governed ingress is a signpost. **The model call is gone either way — that is
the part that mattered.**

**Proven by calling it**, per acceptance 2b: `TestClient(app).post("/chat", …)` → 410; a forged
`user_id` → 410 with no completion in the body; and a twin that monkeypatches an HTTP client
onto the module and asserts it is **never reached**.

---

## 4. ITEM 3 — SEARCH EGRESS PASSES THE GATEWAY · 4 TWINS

Both sites now ask the gateway **before the socket is opened**:
`SerpAPISearchClient.search` (the `serpapi.com` call) and `HttpWebSearchClient.search` (the
config-supplied endpoint). `harness/escalation_backends.py` previously contained **no reference
to `egress_gateway` at all**.

**New: `harness/egress_gateway.classify_web(url)` — on-box → `LOCAL`, off-box → `None`.**

**`None` is not a TODO. It is `permit()`'s own C4 rule doing its job** — *"an undeclared
posture is refused rather than defaulted to send."* **There is deliberately no
`Destination.WEB`**, because adding one means deciding what protection an off-device *search*
egress gets, and that is a security-policy question this dispatch is not authorised to answer
(§7.1). **The bypass is closed either way**: the call goes through the gateway, and today the
gateway refuses.

The helper returns nothing — only "proceed" or an exception. **A boolean would invite a caller
to log it and send anyway, which is the shape being removed.**

Twins: off-box → `EgressRefused` **and the socket is never opened** (asserted, not assumed);
on-box → permitted and the call actually proceeds and returns results; `classify_web` rejects
`localhost.evil.example`, the spelling attack `_host_is_on_box` exists to defeat.

---

## 5. ITEM 4 — CONSUMER-PATH TESTS THAT ACTUALLY CALL THE KERNEL · 5 TWINS

**`eval/test_b0_ground_hardening.py` — 21 tests, every one executes code, and not one asserts
over source text.** NC 7 measured five files naming a kernel entry and **zero** calling one;
this file calls all three.

| kernel entry | executed as |
|---|---|
| `assemble_governed_context` | called; with no resolvable facts it raises **`DisclosureBlocked`** — asserted on the specific exception and its state, not on "it raised". A second twin asserts an unknown member is a `ValueError`. |
| `process_text_query` | called; green path returns a real reply carrying the query text through; refusal path raises `ClaimMismatch`. |
| `_governed_turn` | called through `typed_request`; returns a real reply, asserted on **content**. |

**Twin counts: item 1 → 8, item 2 → 4, item 3 → 4, item 4 → 5. Total 21, all passing.**

---

## 6. SUITE STATE AT HEAD

```
21 failed, 457 passed, 38 skipped, 21 errors      (services down; this worktree has no graph)
```

**ZERO new failures attributable to NC 8's source changes**, proven properly: the five edited
source files were stashed **while keeping the lane declarations**, the identical command was
re-run, and the failure **sets** were compared.

```
baseline failures: 29        after NC 8: 29
NEW failures:      (none)    FIXED:      (none)
```

**The first attempt at this comparison was wrong and is recorded rather than quietly
redone:** `git stash -u` also stashed the corrected `.hip-owns`/`.hip-graph`, so the baseline
ran against the *inherited 7691* declarations and reported nine phantom "new" failures. Those
nine are §7.3's finding, not regressions.

---

## 7. FILED (4) — TWO OF THEM NEED A RULING

### 7.1 ⚠ NEEDS BILL — what protection does an off-device SEARCH egress get?

Three defensible answers, and choosing between them is a security-policy decision:

- **`FRONTIER`'s policy (strip + consent gate)** — every web search would enter the consent
  flow. Defensible, and a real behaviour change.
- **Strip-only** — treats a search query as less sensitive than a model prompt. Needs an
  argument nobody has made.
- **Refuse** — what it does today, and the conservative reading.

**Until this is answered, web search fails closed.** That is a behaviour change on the
temporal-escalation path, and it is deliberate.

### 7.2 ⚠ NEEDS BILL — a governed turn ANSWERS with no fact store reachable

Measured, not theorised. `_governed_turn("when is trash pickup", "bill")` against an
unreachable graph returned:

> **"Trash pickup is on Wednesdays. I don't have that confirmed yet."**

**The governance layer worked** — it did not claim the fact was confirmed, and the provenance
caveat is exactly what it exists to add. **But the model still emitted a specific,
household-shaped claim with no fact behind it.** Whether a governance-bearing path should
answer at all when its fact store is unreachable — rather than say so — is a product-and-policy
question, and the vertical slice will inherit whatever answer it gets. **Not changed here:
outside the four-item list.**

### 7.3 Nine tests hard-code `7691`, so they fail in any worktree that is not `~/hip-vo`

`eval/test_lane_ownership.py`, `eval/test_fail_closed_graph_target.py` and
`eval/test_graph_resolver_consumers.py` assert this checkout is pinned to **7691** — hip-vo's
port. **A correctly-provisioned build worktree therefore fails them by construction**, which
puts "give build sessions their own worktree" (the ratified NC plan) and "the suite is green"
in direct conflict. **Not touched** — out of scope, and re-tiering an acceptance is not
pre-authorized.

### 7.4 My own first-draft tests were wrong twice, in the FM 9 twin-bug shape

**(a)** A test asserted against `req.query`; the field is `TurnRequest.utterance`. It passed
vacuously against an empty string until the content assertion caught it. **(b)** A test
asserted `_governed_turn` would *raise* with no graph. **It does not — it answers**, which is
§7.2's finding and a stronger assertion than the one I wrote. Both fixed by asking the system
rather than the docs (Requirements Discipline item 6). Recorded because **a twin that is wrong
in the green direction passes a broken tool just as easily.**

---

## 8. WHAT THIS DISPATCH DID NOT DO

- **Never edited `~/hip-vo`.** All work in `~/hip-nc2` @ `nc-b0`; `~/hip-vo`'s working tree
  carries only HA-88's own in-progress file.
- **Wrote no graph, stood up no Neo4j, started no service.**
- **Out of scope and untouched:** the kernel extraction, conversation state, voice changes,
  `/api/text-query` dedup, the frozen tree, the demo lane.
- **Invented no egress policy** (§7.1) and **changed no behaviour on the no-graph answer**
  (§7.2).
- **Did not re-tier or delete the nine port-pinned tests** (§7.3).
- **Merged nothing.** `nc-b0` is pushed and stands on its own.

---

## 9. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Ground hardening; no ledger claim's evidence was produced or moved.

---

## 10. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`.
- **REQ `f3a1302` precedes the code `f6dcdd3`** and contains no source file.
- `lane_preflight.py` **refused the worktree before any edit**, and passes after correction.
- 21 executing tests pass; the suite shows **zero new failures** against a properly isolated
  baseline.
- Board rows written by `claim_lane.py` under the repo lock, board-only, no passengers.
