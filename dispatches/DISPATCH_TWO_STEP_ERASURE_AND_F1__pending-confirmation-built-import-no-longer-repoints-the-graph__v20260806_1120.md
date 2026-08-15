# DISPATCH_TWO_STEP_ERASURE_AND_F1
Status: BUILT
Reconciled-Against: `roadmap` at **`bf113ca`** (2026-08-06). Branched from `8391c52`; `origin/roadmap` had not moved, so this landed as a fast-forward — verified `8391c52..HEAD` contains exactly one commit and no passenger (STANDARD PREAMBLE item 8).

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_ERASURE_REQUEST_PATH__owner-scoped-request-in-authorization-checked-report-out__v20260805_0658.md`
— ruling (d) recorded into it by item 1 of this dispatch.

**COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING**

## THE ASK

> === D-R-194 | ~/hip-roadmap, roadmap | Two-step erasure + fix F1 ===
> STANDARD PREAMBLE. Lane A. CHECK FIRST whether either piece already landed.
>
> BILL'S RULINGS 2026-08-05:
> - Question (d): TWO-STEP. A request creates a pending confirmation; a second
>   authenticated act by the same member executes it. Destruction is irreversible and
>   confirmations are already their own channel in this design.
> - F1: fixed, not just pinned. An import must never change which database a process
>   points at.
>
> 1. RECORD ruling (d) in REQ_ERASURE_REQUEST_PATH. The other undetermined question
>    stays refused by default.
> 2. BUILD the two-step flow on POST /api/erasure/fact: request -> pending, confirm ->
>    execute. Unconfirmed requests erase nothing, ever. Expired or mismatched
>    confirmations refused. Fault twins for both, executed, spy at zero.
> 3. FIX F1: env loading explicit at process start, never a side effect of import,
>    never overriding a pinned database target. The F1 pin test flips to asserting the
>    hazard's absence.
> 4. Fixtures only; enabling stays Bill's separate authorization.
> 5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 STOP.
> 6. Rule nothing MET.

## CHECK FIRST — neither piece had landed

```
grep -rniE "pending.*erasure|erasure.*pending|confirm.*eras|two-step" harness/ server/ eval/
  -> only PROSE naming (d) as undetermined; no pending flow anywhere
grep -rn "_load_env_file(pathlib.Path.home()" server/ harness/
  -> server/demo_dashboard.py:61  (F1 still live)
git log --all --grep="two-step" / --grep="F1"   -> nothing that built either
```

Nothing was redone.

## 1 — RULING (d) RECORDED

Written into the REQ's own §(d) as a quoted ruling block, with the original
UNDETERMINED text **retained below it, struck through**, as the record of what was
open before. **(b) is untouched and still refused by default** — the route comment
and the module docstring both say so explicitly, in neither direction.

## 2 — THE TWO-STEP FLOW

**The pending store lives in the DECIDER, not the route** — `harness/erasure_request.py`
— so D-R-192's "one door, one decider" still holds. The route authenticates and hands
over an identity; every authorization and state decision is the request layer's.

| | |
|---|---|
| `begin_fact_erasure(requester, fact_id, reason)` | authorizes, returns `{token, expires_in_s}`, **never calls the mechanism** |
| `confirm_fact_erasure(requester, token)` | the second act — re-checks member, token, expiry, and ownership *as it stands now*, then executes |

`POST /api/erasure/fact` serves both: **no `token` in the body → step one; a `token` →
step two.** Each step carries its **own body-bound Ed25519 signature** (step one binds
`{fact_id, reason}`, step two binds `{token}`), so the confirmation is a fresh
authenticated act, not a replay of the request.

**Four deliberate properties, each with a test:**

- **Authorization is checked at REQUEST time**, not deferred to confirm — an
  unauthorized request is refused *before* a pending row exists, so the store cannot
  be used to probe which facts exist or who owns them.
- **Tokens are single-use**, consumed before the mechanism runs, so a failed confirm
  cannot be retried blindly.
- **5-minute TTL**, and **in-memory per-process on purpose**: a pending destruction
  must not survive a restart. Losing a token costs one re-request; persisting one
  risks a confirmation landing against a token whose author is long gone.
- **Deliberately NOT `harness.confirmation_gate`.** That gate resolves an AMBIGUOUS
  pending WRITE; this confirms an already-unambiguous, already-authorized
  DESTRUCTION. The REQ names them as different concerns; sharing the store would
  couple a data-integrity mechanism to a destruction one.

### Fault twins — executed, spy at zero on every refusal

| test | asserts |
|---|---|
| `test_step_one_returns_pending_and_erases_nothing` | **the core of (d)** — a correctly signed, fully authorized request returns `pending:true` and `spy == []`; fact survives |
| `test_confirmation_by_a_different_member_is_refused` | `maya` authenticates perfectly, presents `bill`'s live token → **409**, `spy == []` |
| `test_expired_confirmation_is_refused` | valid token, TTL elapsed → **409**, `spy == []` |
| `test_unknown_token_is_refused` | **409**, `spy == []` |
| `test_a_token_is_single_use` | confirmed token replayed → **409**, spy still at exactly 1 |
| `test_confirm_signature_is_bound_to_the_token` | signature for token A cannot confirm token B → **401**, `spy == []` |
| `test_two_step_confirm_executes` | **ANTI-VACUITY** — the correct two-step reaches the mechanism exactly once, `actor={"kind":"member","id":"bill"}` |
| (extended) `..._cannot_erase_another_members_fact` | now also asserts **no pending row was created** for that fact |

Without the anti-vacuity control every `spy == []` above would also pass on a route
that is simply broken for all inputs.

## 3 — F1 FIXED, NOT PINNED

Two changes in `server/demo_dashboard.py`, both required:

1. **Env loading is explicit.** The two import-time `_load_env_file` calls moved into
   `load_process_env()`, called from `main()` at process start. **Importing the module
   now has no environment side effect at all.**
2. **The home file may never set a graph target.** `NEO4J_URI` is in
   `_GRAPH_TARGET_VARS` and is skipped unconditionally in the home-file override. The
   override still exists for its real purpose — `~/.env.dev`'s live `OPENAI_API_KEY`
   beating the repo's revoked one.

A third change was forced by the first: `NEO4J_URI`/`NEO4J_USER` were **module
constants bound at import**, which would have frozen before `load_process_env()` ran —
the same class of bug. They are now resolved lazily inside `_get_driver()`.

**Proven in a clean process, and the proof is not vacuous:**

```
AFTER  — import only, nothing preset
  before import: bolt://localhost:7688
  after  import: bolt://localhost:7688      CHANGED BY IMPORT: False

ANTI-VACUITY — the two semantics side by side, same process
  OLD semantics: bolt://localhost:7688 -> bolt://localhost:7689   <- the frozen demo
  NEW semantics: bolt://localhost:7688 -> bolt://localhost:7688
```

**The pin test is flipped.** `test_import_redirects_the_graph_to_the_frozen_demo`
(which asserted the hazard existed) is now
`test_import_does_not_change_the_graph_target`, asserting its absence, plus
`test_home_env_may_never_set_the_graph_target` (calls the real `load_process_env()`
with a hostile URI already set and asserts it survives) and
`test_graph_target_var_is_skipped_by_name` as its structural companion.

## 4 — SCOPE HELD

Still **off unless `HIP_ERASURE_ROUTE_ENABLED` is set**, still fixtures only.
Fixture leftovers confirmed **0** by direct query for `d-r-194-`, `d-r-192-` and
`d-r-172-` prefixes. **Enabling remains Bill's separate authorization**, and one of
its five preconditions — the (d) ruling — is now discharged.

## 5 — RUNS

| run | result |
|---|---|
| **BASELINE** `--layer 7` (before any edit) | 664 passed / 9 xfailed; AUDIT 8/8; DISC 39/39; L7 27/27; L7V2 27/28; RATCHET PASS |
| **AFTER** `--layer 7` | **672 passed / 9 xfailed** = 664 + exactly the 8 net added tests; **diff vs baseline IDENTICAL**; RATCHET PASS; EXIT=0 |
| erasure suites alone, under `graph:7688` | 27 passed |
| **memory harness** before / after | 13/17 both, failing set `{MEM-115,116,117,118}` both, `diff` IDENTICAL — inside the 13-15 pin, **not** the 16/17 STOP |
| **`--full`** | **DID NOT RUN** — `refuse: --full needs >=2GB free memory (TD-129); currently 0.79GB free` |

**Requirements Discipline item 12 is NOT satisfied** — third dispatch running, same
TD-129 memory refusal, same cause (unrelated user applications), and again nothing was
killed to force it. `--layer 7` did run its RATCHET.

## VERIFIED

**Watched run:** the CHECK-FIRST greps; both F1 proofs including the side-by-side
anti-vacuity; all 27 erasure tests under the graph lock; both harness runs; both
memory-harness runs; the fixture-leak query; the compile checks; and a direct check
that **today's demo is unaffected** — the running dashboard (PID 76965) serves
`~/hip-vo`, a different checkout from the one edited here, and still reports
`all_ok=true`.

**Reasoned from code, NOT executed:**
- **No dashboard process was started from this checkout and no live HTTP request was
  made.** All 20 route tests drive `fastapi.testclient.TestClient` in-process. The
  two-step flow has never run over a real socket.
- **`load_process_env()` has never run inside a real uvicorn boot.** It is called from
  `main()`, and `main()` was not executed here; the tests call it directly. The
  launchd path (`python -m server.demo_dashboard` → `__main__` → `main()`) is
  reasoned, not exercised.
- The 5-minute TTL was tested by forcing the constant negative, not by waiting.

## OPEN — Bill's

1. **`--full` still unrun** (TD-129). Item 12 unsatisfied for the third dispatch.
2. **Question (b)** — cross-person erasure authority — still UNDETERMINED and refused
   by default. Unchanged by this dispatch, by instruction.
3. **Enabling the route** remains unauthorized. Of D-R-192's five named preconditions,
   (d) and F1 are now discharged; who may set the enablement flag, the (b) ruling, and
   the absence of any undo remain.
4. **`server/voice_orch.py` and other modules were not audited** for the same
   import-time env pattern. F1 was fixed where it was found; whether the shape exists
   elsewhere is unmeasured.

Nothing marked MET.

---

**D-R-194: neither piece had landed — confirmed from the machine. Ruling (d) recorded
into the REQ with the superseded text struck through, not deleted. Two-step built with
the pending store in the DECIDER so "one door, one decider" holds: no token means
request, a token means confirm, each step carrying its own body-bound signature.
Unconfirmed requests erase nothing — proven, spy at zero — alongside refused
mismatched, expired, unknown and replayed confirmations, and an anti-vacuity control
proving the correct two-step still fires exactly once. F1 FIXED not pinned: env
loading is explicit at process start, the home file can never set a graph target, and
the module constants that would have re-created the bug are now lazy. Proven in a
clean process with the old and new semantics side by side — old flips to 7689, new
holds at 7688. The pin test is inverted to assert the hazard's absence. 672/9 =
baseline 664/9 + exactly the 8 net added tests, every layer identical, RATCHET PASS;
memory 13/17 on the same pinned set; zero fixture leaks; today's demo untouched.
`--full` REFUSED by TD-129 again. Nothing marked MET.**
