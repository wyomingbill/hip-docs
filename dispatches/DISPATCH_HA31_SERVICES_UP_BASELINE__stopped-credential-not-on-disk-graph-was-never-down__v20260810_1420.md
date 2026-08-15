# DISPATCH_HA31_SERVICES_UP_BASELINE — STOPPED: the credential is not obtainable, and the graph was never down
Status: **STOPPED AT ITEM 2 — NEEDS BILL.** Items 1 and 2's documentation complete.
Reconciled-Against: roadmap `4c5abc5`
Filed: 2026-08-10 (HA-31)
Decision-Owner: Bill
TYPE: MEASUREMENT. No test changes, no fixes, no deletions. Nothing ruled MET.

## THE FINDING THAT CHANGES HA-30's PREMISE

**The graph was never down.** `lsof` shows `java` listening on **7688** — the roadmap
`NEO4J_URI` from repo `.env.dev` — and `ollama` on 11434. Both were up while HA-30 recorded 41
reds as *"graph not running"*.

**What is actually missing is the credential.** `.env.dev` states it in its own comment:

> `NEO4J_PASSWORD` is deliberately NOT pinned here — it's a secret, sourced from the shell
> environment (same as the demo checkout already does; neither checkout writes it to disk).

**A session cannot obtain it.** The demo lane's password lives at
`~/hip-keys/neo4j-cutover-demo/NEO4J_PASSWORD`; there is no equivalent file for the roadmap
graph, and by design there should not be. **So items 3 and 4 cannot be executed by this session**
— not for want of context, but because the precondition is an operator secret.

**Why this matters beyond today:** a listening port and a usable graph are not the same thing, and
the suite cannot tell them apart — both produce `harness.graph_target.GraphTargetError`. HA-30
read "42 tests erroring on the graph" as "the graph is down" and was wrong about the mechanism
while right that the environment was the cause. That is now written into `CLAUDE.md` so the next
session does not repeat it.

## ITEM 1 — BOOKKEEPING, COMPLETE

**(a) HA-30's buckets corrected in place**, old label preserved verbatim, **Bill credited**. The
41 graph + 1 Groq rows are renamed **ENVIRONMENT-BLOCKED (42)** — *"outside this lane"* was wrong
in kind, not just wording: those are **this lane's own tests**, blocked by a missing environment,
and the old label quietly disowned 42 of them. "RELEVANT TO THIS LANE" likewise became
**POTENTIALLY RELEVANT**, which is what the evidence supported — the caveat was already recorded
and the label had overstated it.

| bucket | n |
|---|---|
| ENVIRONMENT-BLOCKED | **42** |
| DEMO-LANE / OTHER-REPO | **7** |
| KNOWN DEFECT | **1** |
| POTENTIALLY RELEVANT | **3** |
| UNKNOWN | **39** |
| **TOTAL** | **92** |

**(b) TD-R-177 filed, not fixed** — `tests/test_routing.py` cannot import `_classify_freshness`
from `harness.router`. A collection error, so none of its tests run. Recorded as not
environment-dependent: no service, credential or port affects the import of a name that is absent.

## ITEM 2 — PRECONDITIONS WRITTEN BEFORE EXECUTION, AS REQUIRED

Recorded in this doc and in `CLAUDE.md` beside the canonical command:

| service | where | verify UP |
|---|---|---|
| Neo4j (roadmap graph) | `bolt://localhost:7688` (repo `.env.dev`) | `lsof -nP -iTCP:7688 -sTCP:LISTEN` → `java` |
| Ollama | `http://localhost:11434` | `lsof -nP -iTCP:11434 -sTCP:LISTEN` → `ollama` |

Plus the two rules that make the difference: **`NEO4J_PASSWORD` must be supplied in the
environment by the operator** and is not on disk; and **use the repo `.env.dev`, never
`~/.env.dev`**, which pins 7689 with `override=True` and would silently redirect the run into the
frozen demo graph.

**Both services were already up. Nothing was started, so nothing was left running.**

## ITEMS 3 AND 4 — NOT PERFORMED

The canonical command, `--layer 7`, the RATCHET and the memory harness were **not run**, and
Bill's four questions are **unanswered**. Running them without `NEO4J_PASSWORD` would reproduce
HA-30's 92 reds exactly and answer nothing — the 39 UNKNOWN would stay unknown, and the 3
POTENTIALLY RELEVANT would be untestable for the same reason.

**No pin is claimed.** **Nothing is ruled MET.**

## WHAT IS NEEDED TO FINISH — one thing

**`NEO4J_PASSWORD` for the graph on 7688, supplied in the environment.** With it, a reissue runs
the four commands and answers (a)–(d) directly from the capture. Everything else is in place: the
services are up, the command is documented, the preconditions are written, and the buckets are
settled.

## CLAIM IMPACT

**None.** No measurement was taken, no status changed, nothing ruled MET. The bucket rename is a
correction to how 42 of this lane's tests were characterised, not a change in evidence.

## OPEN

- **Bill's four questions (a)–(d)** — blocked on the credential.
- **The 3 POTENTIALLY RELEVANT assertions** — disposition is Bill's per his ruling; still untested
  with a usable graph, still unfiled.
- **TD-R-177** — filed, not fixed.

---

# HA-31 REISSUE — authenticated preflight passed; suite run; four questions answered

Status: **COMPLETE WITH FINDINGS.** Reconciled-Against `0210310`. MEASUREMENT ONLY — no test
changed, no fix, no deletion. TD-R-177 untouched. **Nothing ruled MET.**

## ITEMS 1–2 — CONFIRMED, AND THE PREFLIGHT ADDED TO CLAUDE.md

**The 7689 trap is real and was verified, not assumed:** repo `.env.dev` gives
`bolt://localhost:7688`; `~/.env.dev` gives `bolt://localhost:7689`, the frozen demo graph. The
repo file is the one in effect.

**AUTHENTICATED PREFLIGHT → `GRAPH USABLE`** — a real driver connection at
`bolt://localhost:7688` with the operator-supplied credential, trivial read `RETURN 1` returned
`1`. The four-state classifier and its **STOP on anything but GRAPH USABLE** are now a standing
step in `CLAUDE.md`.

## ITEM 3 — RUNS

| command | result |
|---|---|
| **canonical batteries** | **1040 passed, 39 failed, 10 skipped, 9 xfailed, 2 errors** |
| `--layer 7` | **REFUSED, exit 1** — `HIP_REGISTRY_DB not set` |
| RATCHET `--full` | **REFUSED, exit 1** — same refusal |
| memory harness | **10/17**, exit 1 — decrypt failures, `no household_key_wraps row` |

**A SECOND PRECONDITION GAP, FOUND BY EXECUTING:** three of the four binding-gate commands need
`HIP_REGISTRY_DB`, which HA-31's own preconditions table did not name — it was written from
`.env.dev` and the graph alone. The refusal is deliberate and correct: Layer 7 would otherwise
fall back to the shared demo registry whose custody grants live in another checkout's ledger
(D-25). **`NEO4J_PASSWORD` alone is not "services up" for the gate.** Now in `CLAUDE.md`.

**The memory harness's 10/17 is NOT a pin measurement and NO STOP is declared on it.** It ran in
the same incomplete environment and its failures are decrypt errors from missing household key
wraps, not memory behaviour. Quoting 10/17 against a 13–15 pin would be exactly the misreading
this dispatch exists to prevent. **No pin claimed; no gate claim made.**

## ITEM 4 — BILL'S FOUR QUESTIONS

### (a) The 39 UNKNOWN — 16 collapse, 23 are real. Per module, by what changed.

| module | was | now | verdict |
|---|---|---|---|
| `eval/test_sensitivity_no_default.py` | 13 UNKNOWN (setup errors) | **gone** | **ENVIRONMENT — collapsed** |
| `eval/test_erasure_request.py` | 2 UNKNOWN | **gone** | **ENVIRONMENT — collapsed** |
| `eval/test_graph_erasure.py` | 1 UNKNOWN | **gone** | **ENVIRONMENT — collapsed** |
| `eval/oracle/test_disclosure.py` | 19 UNKNOWN (**errors**) | **19 FAILURES** | **REAL — they now execute and fail** |
| `eval/test_ledger_commitment.py` | 4 UNKNOWN | **4 FAILURES** | **REAL** |

**16 collapsed + 23 real = 39.** The distinction is exactly the one the bucket exercise could not
make from the old capture: the 19 disclosure-oracle items changed **from ERROR to FAILURE** — they
were never running before, and now they run and fail. **That is a real result, not an environment
artifact**, and it was invisible until the graph was usable.

### (b) The 3 POTENTIALLY RELEVANT — 2 green, 1 still red. NOTHING FILED.

| test | result |
|---|---|
| `eval/test_structural_refusal.py::test_sref_graph_known_set_is_not_vacuous` | **PASS** |
| `eval/test_structural_refusal.py::test_sref_ray_resolves_with_widened_set_only` | **PASS** |
| `tests/test_sensitivity.py::test_sensitive_queries_route_local` | **SAME FAILURE** — `AssertionError`, unchanged with the graph up |

The two `..._graph_...`-named tests were graph-dependent after all — **the caveat HA-30 recorded
rather than asserted was the right call.** The third is unaffected by graph state and is the only
one of the original 92 that is now a plain, environment-independent failure. **Disposition is
Bill's; nothing filed.**

### (c) The reproducible whole-suite number

> **1040 passed / 39 failed / 10 skipped / 9 xfailed / 2 errors**
> command: `PYTHONPATH=. ~/hip-dev/.venv/bin/python -m pytest -q --import-mode=importlib --continue-on-collection-errors`
> service state: Neo4j **7688 up**, Ollama 11434 up, `NEO4J_PASSWORD` supplied, `HIP_REGISTRY_DB` **unset**
> preflight: **GRAPH USABLE**

The 2 errors are the two known collection failures: TD-R-177 (`test_routing`) and the live-Groq
`scripts/test_groq_factchange.py`.

### (d) HA-28's 970 / 0 — NOT reproduced.

| | HA-28 | HA-31 (services up) | diff |
|---|---|---|---|
| passed | 970 | **1040** | **+70** |
| failed | 0 | **39** | **+39** |
| errors | — | 2 | — |

**Not reproduced in either direction:** 70 MORE tests pass than HA-28 reported, and 39 fail where
it reported none. A pure environment difference could explain more failures; it cannot explain 70
extra passes. **The likeliest reading is that 970/0 was a narrower selection, not the whole
suite** — but HA-28 does not record its command, so this stays unresolved rather than guessed.
**970/0 should not be quoted again.**

## CLAIM IMPACT

**None.** Measurement only; no status changed, nothing ruled MET, no gate claim made — three of
the four gate commands did not run. What changed is what is *known*: 16 of the 39 unknowns are
environment, 23 are real, and one lane-relevant assertion failure is isolated.

## OPEN

- **`HIP_REGISTRY_DB`** — needs a per-checkout path in `.env.dev` before any gate result exists.
- **23 real failures** — 19 disclosure-oracle, 4 ledger-commitment. Not investigated, not filed.
- **`test_sensitive_queries_route_local`** — Bill's disposition.
- **HA-28's 970/0** — unresolved; its command was never recorded.

---

# HA-31 CONTINUATION 2 — the first complete, valid-environment baseline

Status: **COMPLETE WITH FINDINGS.** Reconciled-Against `b2b40ad`. MEASUREMENT + FILING ONLY.
Nothing fixed — not the 23, not TD-R-177. **Nothing ruled MET.**

## ITEM 1 — `HIP_REGISTRY_DB` IS NOT A SECRET

`.env.dev:43` → `export HIP_REGISTRY_DB="$HOME/hip-roadmap/data/registry.db"`. A **path**, pinned
in the repo config, gitignored file, present on disk. **No STOP needed** — unlike
`NEO4J_PASSWORD`, it needs no operator. It is simply unset in a bare shell, which is why three of
four gate commands refused last time.

**Verified roadmap-local, not the demo checkout's:** the value resolves under `~/hip-roadmap/`,
and six `registry.db` files exist on this machine including `~/hip-harness/` and
`~/hip-dev/data/`. **D-25 is exactly this defect** (BACKLOG 0b, resolved `605bb79`): the var once
pointed at a shared registry while custody grants landed checkout-local, so Layer 7 counted one
checkout's wraps against another's grants. A shared path is now a **rejected** preflight state.

## ITEM 2 — EXTENDED PREFLIGHT, BOTH RESOURCES

```
NEO4J    : USABLE
REGISTRY : USABLE (15 tables, roadmap-local) -> [REDACTED-USER-PATH]/hip-roadmap/data/registry.db
VERDICT  : PROCEED
```

Four states each (service down / credential missing / auth rejected / usable); anything else
STOPs. Registry "auth rejected" explicitly includes a shared-registry path. Now standing in
`CLAUDE.md`.

## ITEM 3 — THE FIRST COMPLETE REPRODUCIBLE SERVICES-UP BASELINE

**Environment:** Neo4j `bolt://localhost:7688` up + `NEO4J_PASSWORD` from operator env; Ollama
11434 up; `HIP_REGISTRY_DB=$HOME/hip-roadmap/data/registry.db`; repo `.env.dev` (never
`~/.env.dev`). **Preflight: both USABLE, PROCEED.**

| command | result |
|---|---|
| `pytest -q --import-mode=importlib --continue-on-collection-errors` | **1048 passed, 31 failed, 10 skipped, 9 xfailed, 2 errors** |
| `eval.harness --layer 7` | **PASS, exit 0** |
| `eval.harness --full` (RATCHET) | **RATCHET FAIL** — `NEW FAILURES (not in baseline): ['L1:P12', 'L6:record-invariants']` |
| `eval.memory_harness` | **13/17 — INSIDE the 13–15 pin** |

**This is the first run where all four executed in a valid environment.** The pin applies and is
met at its floor. **No gate claim is made: the RATCHET is FAIL**, and per the standing rule
nothing may be called PASS while a red stands. **The two RATCHET new failures are reported, not
investigated** — this is a measurement dispatch.

**Supplying `HIP_REGISTRY_DB` alone moved the suite from 1040/39 to 1048/31** — 8 further tests
(all `eval/test_erasure_route.py`) were registry-blocked, not broken.

## ITEM 4 — FILED

**(a) TD-R-178 — the 19 disclosure-oracle failures, ONE grouped defect.** All 19 are
parametrisations of a single function, `test_disclosure_case[...]`, in one module. **Grouped on
that shared function and module, NOT on a proven shared root cause** — no per-case exception type
could be extracted from the capture, and that limit is stated so the grouping can be split if
triage disagrees. Environment-independent as far as measured: ERRORS with the graph down,
FAILURES with it up, still 19 FAILURES with the registry supplied.

**(b) TD-R-179 — `test_sensitive_queries_route_local`.** A plain `AssertionError`, identical
across **three** environment states. The only one of the original 92 proven
environment-independent; its two former bucket-companions both went green.

**(c) The remaining 4, named — and they are ONE defect, so filed as TD-R-180.**
`eval/test_ledger_commitment.py`: `test_hel_commitment_rejects_keys_shorter_than_the_floor`
`[empty]`, `[5-bytes]`, `[31-bytes-one-short]`, and `test_hel_commitment_rejects_a_non_bytes_key`.
**Every one asserts that a commitment REFUSES an invalid key, and every one fails** — a single
rejection path not rejecting, not four faults. The other 8 of the former "23 real" were
`eval/test_erasure_route.py` and are **now green**, registry-blocked all along.

**Nothing else is left for Bill to disposition** — all 33 current reds are accounted for:
19 (TD-R-178) + 4 (TD-R-180) + 1 (TD-R-179) + 7 demo-lane + 1 TD-R-177 + 1 live-Groq = **33**.

## ITEM 5 — HA-28's 970/0 SUPERSEDED, NOT DELETED

Marked in all three places that carried it — `docs/INDEX.md`, `docs/HIP_HANDOFF.md`, and HA-28's
own dispatch doc — with: *"Superseded as a canonical battery result. The exact invocation was not
recorded and the result is contradicted by the documented whole-suite invocation."* **The number
is preserved everywhere it appeared.**

## CLAIM IMPACT

**None.** Measurement and filing. No status changed, nothing ruled MET, **no gate claim** — the
RATCHET is FAIL. What changed is what is known: the environment is now fully specified, the
baseline is reproducible, and every red is attributed.

## OPEN

- **RATCHET FAIL** — `L1:P12`, `L6:record-invariants`. Reported, not investigated.
- **TD-R-178 / 179 / 180**, and TD-R-177. Filed, none fixed.
- **7 demo-lane failures** in `tests/test_demo_presentation.py` — belong to `~/hip-cutover-demo`.
