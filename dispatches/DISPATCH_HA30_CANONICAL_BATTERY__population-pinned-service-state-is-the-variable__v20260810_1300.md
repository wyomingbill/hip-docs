# DISPATCH_HA30_CANONICAL_BATTERY — invocation documented, service state named as the variable
Status: **COMPLETE WITH FINDINGS**
Reconciled-Against: roadmap `b99188a`
Filed: 2026-08-10 (HA-30)
Decision-Owner: Bill
TYPE: DOCUMENTATION + MEASUREMENT. No code. Closes HA-29's open item.

## WHAT WAS ASKED

Document the canonical battery invocation for this lane — the gap HA-29 left open when its
numbers (990/58/34) could not be reconciled with HA-28's (970/0).

## THE COMMAND — now in `CLAUDE.md`

```sh
cd ~/hip-roadmap
PYTHONPATH=. ~/hip-dev/.venv/bin/python -m pytest -q --import-mode=importlib \
  2>&1 | tee /tmp/roadmap_batteries_$(date +%Y%m%d_%H%M).txt
```

`--import-mode=importlib` is required (`eval/harness.py` shadows the `harness` package).
**The RATCHET — `python -m eval.harness --full` — is a separate command and is not the
batteries**, per Requirements Discipline item 12.

## THE FINDING — path selection is not the variable; SERVICE STATE is

Four invocations measured today, services **down**:

| selection | passed | failed | errors |
|---|---|---|---|
| `tests/` | 83 | 8 | 1 |
| `eval/` | 907 | 50 | 32 |
| whole suite minus `eval/`+`scripts/` | 83 | 8 | 1 |
| **whole suite** | **990** | **58** | **34** |

**`907 + 83 = 990` exactly.** The population is fully accounted for, so the whole-suite command is
the correct selection — **narrowing by path does not remove the failures, it removes tests.** Two
candidate invocations (`tests/` alone, and excluding `eval/`) were tried and rejected on this
evidence: each yields 83 passed, nowhere near either dispatch's figure.

**HA-28's `970 passed / 0 failed` was NOT reproduced, and the reason is service state, not
command.** The failures are live-dependent; a Neo4j connection error appears among them. HA-28
ran with the stack up. **Until the exact service preconditions are recorded, `970 / 0` should be
treated as unreproduced** — that is now written into `CLAUDE.md` rather than left for the next
session to rediscover, which is the third time this lane pair has paid for it (TD-D-165 in the
demo lane, HA-29 here, HA-30 now).

**Known-bad, not a regression:** `tests/test_routing.py` fails to import —
`cannot import name '_classify_freshness' from 'harness.router'`.

## THE RULE RECORDED

State the service state with every battery number; compare like with like, same command and same
service state, before and after; say PASS only when no red stands.

## WHAT THIS DOES NOT DO

**It does not establish a green baseline.** No services were started — that is a live-stack
operation outside a documentation dispatch, and inventing one would repeat the error being fixed.
**A services-up baseline is still owed**, and it is the one thing that would let this lane quote
an absolute number again.

**CLAIM IMPACT: none.** Documentation and measurement only.

## OPEN

- **A services-up baseline**, with the preconditions written down, to replace the unreproduced
  `970 / 0`.
- `tests/test_routing.py`'s import error.

---

# HA-30 REISSUED — full scope: the delta accounted for, bucket by bucket

Status: **COMPLETE WITH FINDINGS.** MEASUREMENT ONLY — nothing fixed, nothing deleted, no test
edited. Reconciled-Against roadmap `23abd3d`.

## ITEM 2 — EVERY ONE OF THE 92 IN EXACTLY ONE BUCKET

One unfiltered run, captured: **58 failed / 990 passed / 9 skipped / 9 xfailed / 34 errors**.
Buckets assigned mechanically from the captured exception type per node id, not by eye.

| bucket | reason | F | E | n |
|---|---|---|---|---|
| **OUTSIDE THIS LANE** | graph not running — `harness.graph_target.GraphTargetError` | 39 | 2 | **41** |
| **OUTSIDE THIS LANE** | demo-player surface, belongs to `~/hip-cutover-demo` (`FileNotFoundError` on a demo script) | 7 | 0 | **7** |
| **OUTSIDE THIS LANE** | live Groq API call at collection (`KeyError: 'choices'`) | 0 | 1 | **1** |
| **KNOWN/FILED** | `tests/test_routing.py` — `ImportError: cannot import name '_classify_freshness'`; documented in HA-30's first pass | 0 | 1 | **1** |
| **RELEVANT TO THIS LANE** | pure `AssertionError`, no infrastructure exception — see below | 3 | 0 | **3** |
| **UNKNOWN** | no exception type captured from the run output | 9 | 30 | **39** |
| | **TOTAL** | **58** | **34** | **92** |

**41 + 7 + 1 + 1 + 3 + 39 = 92. The buckets sum to the total.**

> ### CORRECTION 2026-08-10 — bucket renamed. Ruled by **Bill**.
>
> **The 41 graph rows and the 1 Groq row were labelled, verbatim:** *"OUTSIDE THIS LANE"*.
> **They are renamed ENVIRONMENT-BLOCKED (42).** "Outside this lane" was wrong in kind, not just
> in wording: those tests are this lane's own tests. Nothing about them belongs to another
> checkout — they could not execute because the environment they need was not supplied. Calling
> that "outside this lane" quietly disowns 42 of this lane's own tests.
>
> **HA-31 then found the premise underneath it was also wrong** — see that dispatch. The graph was
> never down: `java` listens on **7688**, the roadmap `NEO4J_URI`. What is missing is the
> credential, which `.env.dev` deliberately keeps off disk. **ENVIRONMENT-BLOCKED is the right
> label for a different reason than the one first given.**
>
> **FINAL BUCKETS:**
>
> | bucket | n |
> |---|---|
> | **ENVIRONMENT-BLOCKED** | **42** |
> | **DEMO-LANE / OTHER-REPO** | **7** |
> | **KNOWN DEFECT** | **1** |
> | **POTENTIALLY RELEVANT** | **3** |
> | **UNKNOWN** | **39** |
> | **TOTAL** | **92** |
>
> 42 + 7 + 1 + 3 + 39 = 92. "RELEVANT TO THIS LANE" is likewise renamed **POTENTIALLY RELEVANT**,
> which is what the evidence supported: the caveat was already recorded, the label had overstated it.

## ITEM 4 — RELEVANT AND UNKNOWN, NAMED FOR BILL. NOT FIXED, NOT FILED.

### RELEVANT TO THIS LANE — 3. These should be green here and are not.

- `eval/test_structural_refusal.py::test_sref_graph_known_set_is_not_vacuous`
- `eval/test_structural_refusal.py::test_sref_ray_resolves_with_widened_set_only`
- `tests/test_sensitivity.py::test_sensitive_queries_route_local`

Classified RELEVANT because each fails on a **plain `AssertionError`** — the assertion was
evaluated and was false — with no `GraphTargetError`, no missing file and no import failure.
**Caveat stated rather than hidden:** the first two are named `..._graph_...` and
`..._resolves_...`, so they may still be graph-dependent tests that degrade to an assertion
rather than raising. **That is a guess and it is not made here** — they are listed for Bill,
which is what item 4 asks.

### UNKNOWN — 39. Cannot be classified from this run's output.

Two clusters, both listed in full in the terminal transcript of this dispatch:

- **`eval/oracle/test_disclosure.py` — 19 setup errors.** Sibling parametrisations in the *same
  file* were captured as `GraphTargetError`, so co-location suggests the same cause. **Not
  asserted** — the exception type was not captured for these, so they stay UNKNOWN.
- **`eval/test_sensitivity_no_default.py` — 13**, plus **`eval/test_ledger_commitment.py` — 4**,
  **`eval/test_erasure_request.py` — 2**, **`eval/test_graph_erasure.py` — 1**,
  **`eval/test_erasure_route.py` — 2**. Same situation: siblings in these files *are* confirmed
  `GraphTargetError`, but these specific nodes did not yield a type.

**If the co-location signal holds, most of the 39 collapse into the graph-not-running bucket and
the true RELEVANT count stays at 3.** Establishing that needs one run with the graph up — which
is the services-up baseline this dispatch already says is owed.

## ITEM 5 — RUNS NOT PERFORMED, AND WHY

**`--layer 7`, the RATCHET (`--full`), and the memory harness were NOT run.** The graph is down —
that is the established cause of 41 confirmed reds — and all three are service-backed. Running
them now would produce failures caused by the missing stack and would tell Bill nothing about the
lane, while risking exactly the misreading this dispatch exists to prevent.

**No pin is claimed.** The memory-harness pin (13–15/17 inside, 16/17 STOP) is recorded in
`CLAUDE.md` as part of the binding gate, unmeasured today.

## CLAIM IMPACT

**None.** Measurement and documentation only. No claim gained or lost evidence; **no status
changed and nothing is ruled MET.** The one thing that changed is that the lane's red count is
now accounted for rather than unexplained — which is a change in what is known, not in what is
claimed.

## OPEN

- **The services-up baseline**, still owed. It would resolve the 39 UNKNOWN and confirm or refute
  the 3 RELEVANT.
- **The 3 RELEVANT items**, for Bill's word before anything is filed or touched.
- `tests/test_routing.py`'s import error.
