# DISPATCH_ERASURE_ROUTE
Status: BUILT
Reconciled-Against: `roadmap` at **`a07bb51`** (2026-08-05). Started from `2499216`; another lane published **D-R-193** (`fa753a1`, `5bbaa75`) mid-dispatch, so this sits on top of it — verified `5bbaa75..HEAD` contains exactly one commit and no passenger (STANDARD PREAMBLE item 8). D-R-193 independently closed the two findings D-R-191 filed (the mirror-image INDEX row, the three stray pipes) and annotated the 322/350 denominator.

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_ERASURE_REQUEST_PATH__owner-scoped-request-in-authorization-checked-report-out__v20260805_0658.md`

**COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING**

## THE ASK

> === D-R-192 | ~/hip-roadmap, roadmap | Wire erasure to a real server route ===
> STANDARD PREAMBLE. Lane A. CHECK FIRST whether a server route to the erasure request
> path already exists — git log and server/*.py, not memory. Report instead of redoing.
>
> GOVERNING REQ: REQ_ERASURE_REQUEST_PATH (v20260805_0658). The request layer exists and
> refuses structurally before the delete code runs (D-R-172, 7/7). Nothing in the live
> server calls it — zero hits for erasure in server/*.py as of D-R-185's check.
>
> 1. BUILD ONE ROUTE: an authenticated member requests erasure of one of their own
>    facts. That is the narrowest case the REQ already answers. The two UNDETERMINED
>    questions (erasing facts about you written by others; one-step vs two-step) stay
>    refused by default — do not answer them in code.
> 2. The route calls the request layer; the request layer decides. The route itself
>    holds NO authorization logic — one door, one decider.
> 3. SCOPE LIMIT: fixtures only. The route exists but is NOT enabled against the live
>    demo graph or real data — enabling is Bill's separate authorization. Say in the
>    report what enabling would take.
> 4. FAULT TWIN: an unauthenticated request and a request for someone else's fact are
>    both REFUSED with nothing erased, proven by execution, refusal before the
>    mechanism runs.
> 5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 STOP.
> 6. Rule nothing MET.

## CHECK FIRST — nothing to redo

Confirmed from the machine, not memory:

```
grep -rniE "erasure|erase|right_to_be_forgotten|forget" server/*.py
  -> server/voice_orch.py:528  r"abort|forget it|skip this|stop enrollment)\b"
     (an enrollment-abort regex; unrelated)
git ls-files | grep -i eras   -> harness/*.py, eval/test_*.py, docs/* only; no server/
```

**D-R-185's finding holds: no server route reached the erasure path.** Nothing was
redone.

## WHAT WAS BUILT

**`POST /api/erasure/fact`** in `server/demo_dashboard.py` — chosen because that is
where the door already is: it owns both the dashboard-session check and the Ed25519
member verification (`/api/session/select-member`, REQ_IDENTITY_BINDING_BUILD step 2).
`server/app.py` was considered and rejected — it is a Phase-0 vestige with two routes
and no authentication at all.

Order of operations, which is what the fault twins prove:

| # | step | failure |
|---|---|---|
| 1 | enablement gate (`HIP_ERASURE_ROUTE_ENABLED`) | **503**, before anything is read |
| 2 | `require_dashboard_session` | 401 |
| 3 | **member Ed25519 signature**, verified against the REGISTERED pubkey | 401 |
| 4 | hand off to `harness.erasure_request.request_fact_erasure` | 403 / 404 / 200 |

**Item 2 — one door, one decider — is enforced, and asserted by a test.** The route
never compares caller to owner, never reads a fact's `subject`, never decides anything.
Every authorization outcome is `UnauthorizedErasureRequest` / `LookupError` from the
request layer, translated to a status code.
`test_route_holds_no_authorization_logic` greps the route's own source (docstring
stripped) for `.owner`, `owner ==`, `subject`, `requester ==` and fails if any appears.

**Two deliberate hardening choices, recorded rather than assumed:**

- **No self-signing fallback.** `/api/session/select-member` signs on the caller's
  behalf when `ts`/`nonce`/`sig` are absent, because this box legitimately holds every
  member's key and switching a view is reversible. **Erasure is not.** Accepting that
  fallback here would let anyone holding the dashboard token erase any member's facts
  by naming them — which *is* fault twin (2). The signature is mandatory.
- **The signature is BOUND TO THE BODY.** `verify_turn(..., {"fact_id":…, "reason":…})`
  folds a canonical hash of the operative fields into the signed message, so a
  signature captured for one fact cannot be replayed to erase another. Verified both
  ways before wiring: key-order independent, and a swapped `fact_id` is rejected
  (`reason="replay"`).

**Item 1 — the UNDETERMINED questions stay refused by default.** Only
`request_fact_erasure` is wired. `request_member_facts_erasure` (owner-wide) is
authorized by the same rule but is reached by nothing — its blast radius is every fact
a member ever wrote, a scope decision nobody has made. A source scan
(`test_owner_wide_erasure_is_not_exposed_by_this_route`) fails if it is ever wired,
so that cannot happen as a quiet refactor. (b) and (d) are not answered in either
direction.

## FAULT TWINS (item 4) — proven by execution, 12/12

`eval/test_erasure_route.py`, wired into `scripts/run_harness.sh`. Every refusal
asserts **`spy == []`** — a call-counting stand-in patched over
`harness.erasure_request.erase_fact`, the same seam D-R-172 used. Zero calls is what
distinguishes *refused before the mechanism ran* from *ran, then reported an error*; an
HTTP status alone cannot tell those apart.

| test | asserts |
|---|---|
| `test_route_is_disabled_by_default` | 503, no session, no signature, `spy == []` |
| `test_disabled_route_refuses_even_a_fully_valid_request` | a fully valid signed request still 503s; fact survives |
| **`test_no_dashboard_session_is_refused`** | **twin 1** — 401, `spy == []` |
| **`test_session_but_no_signature_is_refused`** | **twin 1** — a session is not an identity; 401, fact survives |
| `test_forged_signature_is_refused` | 401, `spy == []`, fact survives |
| `test_signature_for_a_different_fact_is_refused` | body binding: sig for fact A cannot erase fact B |
| **`test_authenticated_member_cannot_erase_another_members_fact`** | **twin 2** — `maya` authenticates *correctly*, asks for `bill`'s fact: **403, `spy == []`, fact survives** |
| `test_unknown_fact_is_a_404_not_a_silent_success` | 404, `spy == []` |
| **`test_authorized_owner_request_does_erase`** | **ANTI-VACUITY** — the same spy IS called once, with `actor={"kind":"member","id":"bill"}` |
| `test_owner_wide_erasure_is_not_exposed_by_this_route` | item 1 held still |
| `test_route_holds_no_authorization_logic` | item 2 held still |
| `test_import_redirects_the_graph_to_the_frozen_demo` | F1 below, pinned |

Without the anti-vacuity control every `spy == []` above would also pass on a route
that is simply broken for all inputs.

## F1 — THE FINDING THAT MATTERS: importing the dashboard re-points the graph at the FROZEN DEMO

`server/demo_dashboard.py:61` runs, **at import time**:

```python
_load_env_file(pathlib.Path.home() / ".env.dev", override=True)
```

and `~/.env.dev` contains `NEO4J_URI=bolt://localhost:7689` — **the frozen demo's
Neo4j.** So merely importing the module that now hosts the erasure route re-points the
process away from this checkout's pinned graph (7688, `.hip-graph`).

**This is not hypothetical — it is how it was found.** The first run of the new test
file died with:

```
GraphTargetError: NEO4J_URI='bolt://localhost:7689' resolves to port 7689, but this
checkout is PINNED to 7688 ([REDACTED-USER-PATH]/hip-roadmap/.hip-graph). Refusing rather
than writing into another lane's graph.
```

This is exactly the hazard STANDARD PREAMBLE item 3 names, arriving through a Python
import rather than a shell `source`. **`harness/graph_target.py` refused and nothing
was written** — that guard, not the route's own care, is what stands between the
erasure path and the frozen demo.

**One caveat found while pinning it:** the guard protects the **first** URI resolution
in a process. `extraction_queue._driver` is memoised, so once a driver exists a later
env change cannot re-trigger the check — which is *why* an import-time redirect is the
dangerous shape. The test asserts against `resolve_graph_uri` directly for that reason.

**NOT FIXED HERE.** The override exists so `~/.env.dev`'s live `OPENAI_API_KEY` beats
the repo's revoked one; narrowing it (e.g. adding `NEO4J_URI` to the `skip` set) is a
behaviour change to a shared module outside this dispatch's scope. Reported, with the
test holding it still.

## ITEM 3 — WHAT ENABLING WOULD TAKE

The route is off unless `HIP_ERASURE_ROUTE_ENABLED` is set to `1`/`true`/`yes`. It is
an env var, not a config-file setting, deliberately: it has to be set per process, per
run, by someone who meant it. **Nothing in this build was enabled against the live demo
graph, `hip-cutover-demo`, or real household data** — confirmed by direct query after
the run: `d-r-192-fixture` leftovers **0**, `d-r-172-fixture` leftovers **0**.

Enabling for real would take, at minimum:

1. **Bill's ruling on question (d)** — one-step or two-step. This build executes
   immediately, a choice the REQ scopes explicitly to the fixture-only proof. A real
   enabled route deleting on one unconfirmed HTTP call is a different risk posture.
2. **Resolving F1 first.** As it stands, a dashboard process has `NEO4J_URI` pointed at
   the frozen demo from import onward. Enabling the route in that process means the
   only thing preventing an erase against 7689 is the pin guard. That ordering should
   be fixed, not relied upon.
3. **A decision on who may enable it** — the env var is currently settable by whoever
   starts the process; the dashboard token holder and the fact owner are different
   people, and only the second is authenticated by the route.
4. **Question (b) still refused**, or ruled. Today every requester != owner is refused,
   including a fact's own subject asking about content someone else wrote about them.
5. **A retention/undo decision.** `erase_fact` is cascade-aware and real; there is no
   undo. Nothing in this dispatch built one.

## RUNS (item 5)

| run | result |
|---|---|
| **BASELINE** `--layer 7` (before any edit) | 652 passed / 9 xfailed; AUDIT 8/8; DISC 39/39; L7 27/27; L7V2 27/28; RATCHET PASS |
| **AFTER** `--layer 7` | **664 passed / 9 xfailed** = 652 + exactly the 12 added tests; **diff vs baseline: IDENTICAL**; RATCHET PASS; EXIT=0 |
| **memory harness, baseline** | 13/17, failing {MEM-115, 116, 117, 118} |
| **memory harness, after** | 13/17, same set, `diff` IDENTICAL — inside the 13-15 pin, **not** the 16/17 STOP |
| `eval/test_erasure_route.py` alone, under `graph:7688` | 12 passed |
| **`--full`** | **DID NOT RUN** — `refuse: --full needs >=2GB free memory (TD-129, the --full killer); currently 0.39GB free` |

**Requirements Discipline item 12 is NOT satisfied** — same TD-129 refusal as D-R-189,
same cause (memory pressure from unrelated user applications), and again nothing was
killed to force it. `--layer 7` did run its RATCHET.

## VERIFIED

**Watched run:** the CHECK-FIRST greps and `git ls-files`; the body-binding round trip
and its swapped-`fact_id` rejection; all 12 route tests under the `graph:7688` lock;
the fixture-leak query after the run; both harness runs and both memory-harness runs;
the compile checks.

**Corrected mid-dispatch, reported rather than buried:** the first fault-twin run was
issued under `graph:7687` — the wrong lock for a checkout pinned to 7688. It failed for
an unrelated reason (F1) before that mattered; re-run under `graph:7688`. Also, the
first version of the F1 test asserted through `_get_driver()` and did not raise, because
the driver is memoised; rewritten to assert against `resolve_graph_uri` directly.

**Reasoned from code, NOT executed:**
- **No dashboard process was started and no live HTTP request was made.** Every route
  test drives `fastapi.testclient.TestClient` in-process. The route has never been
  exercised over a real socket, and never with the enablement flag set outside a test.
- The "what enabling would take" list is analysis, not a rehearsal — none of those five
  steps was performed or tested.
- `request_member_facts_erasure` was not exercised at all here (it is deliberately
  unreachable); D-R-172's own tests remain its only coverage.

## OPEN — Bill's

1. **F1: the import-time redirect to the frozen demo's graph.** Reported, not fixed.
2. **Question (d)**, one-step vs two-step, still unruled — required before enabling.
3. **Question (b)**, cross-person erasure authority, still unruled.
4. **`--full` unrun** (TD-129). Item 12 unsatisfied.
5. **Who may set the enablement flag** — named in item 3 above, undecided.

Nothing marked MET. C9 not touched.

---

**D-R-192: no route existed — confirmed from the machine, nothing redone. Built ONE:
`POST /api/erasure/fact`, authenticated by a body-bound Ed25519 signature with no
self-signing fallback, holding zero authorization logic and handing the decision to
`request_fact_erasure`. Off unless `HIP_ERASURE_ROUTE_ENABLED` is set; fixtures only;
zero leftovers confirmed by query. Both fault twins proven by execution with a
call-counting spy at zero — unauthenticated 401 and another member's fact 403, nothing
erased — plus an anti-vacuity control proving the same spy fires when authorized. FOUND:
importing the dashboard re-points NEO4J_URI at the FROZEN DEMO's graph; the pin guard
refused, and that guard is the only thing standing there. 664/9 = baseline 652/9 + the
12 added tests, every layer identical, RATCHET PASS; memory harness 13/17 on the same
pinned set. `--full` REFUSED by TD-129. Nothing marked MET.**
