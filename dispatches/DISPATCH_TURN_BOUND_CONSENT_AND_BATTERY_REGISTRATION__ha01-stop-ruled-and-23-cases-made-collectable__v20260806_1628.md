# DISPATCH_TURN_BOUND_CONSENT_AND_BATTERY_REGISTRATION — HA-01's stop ruled, and 23 cases made collectable

Status: BUILT
Reconciled-Against: roadmap `25daf17` (pre-build HEAD). **LANDED AT `45e5232`** — backfilled by the immediately following commit, because a commit cannot contain its own hash.

**HA-02** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD (code + REQ amendment)**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1625.md`
(cut by this dispatch) and `REQ_SENSITIVITY_NO_DEFAULT__…__v20260806_1351.md`.
**NOTHING RULED MET.** Both halves enact Bill's rulings; neither marks anything MET.

---

## BILL'S RULINGS, VERBATIM

> "RULING, Bill 2026-08-06: the frontier consent prompt is turn-bound consent inside a
> member-initiated exchange — a REPLY, not system-initiated speech. It is outside the
> initiation taxonomy by R1's own definition, and it belongs to the member-initiated
> grant-confirmation path named in Ruling 1. Add one clarifying line to the REQ's §2.2
> not-an-offer list: "turn-bound disclosure consent within a member-initiated exchange."
> Leave the prompt's behavior unchanged."
>
> "AND: register D-R-196's 23-case battery properly — convert the standalone script to
> pytest-collectable tests in the standing battery, asserting counts unchanged
> (23 in, 23 collected), so the fault twins run on every battery instead of by hand.
> This amends D-R-196's deliverable by my authorization."

---

## PART 1 — HA-01's STOP IS RULED

**HA-01 stopped on site 7** (`_FRONTIER_CONFIRM_MSG`, live from `server/voice_orch.py` via
`control_flow.handle_frontier_request`) because neither `AUTHORIZED_OPERATION` nor `OFFER`
fit. HA-01 named a third reading — that the prompt is outside R1's scope because the member
initiated the exchange — and deliberately did not take it unilaterally. **Bill has now
taken it.** The third reading is the ruling.

### The one line, and why it is cut as a NEW version rather than edited in place

`REQ_OFFER_MECHANISM…v20260806_1320.md` was filed at D-R-195 with a specific, testable
property: **its body is byte-identical to Bill's own revision.** Editing §2.2 in that file
would have destroyed exactly the property it was filed for. So:

- **NEW VERSION `…v20260806_1625.md`**, cut by `cp` and then changed in exactly two places:
  the Status header line, and the single added line in §2.2's not-an-offer list.
- **The prior version is RETAINED INTACT.** Only its own `Status:` header was flipped to
  SUPERSEDED with a pointer; **its body was not touched**, so it still stands as the
  byte-identical copy of Bill's revision.
- `LATEST_REQ_OFFER_MECHANISM.md` repointed.

**PROVEN, not asserted.** `diff` of the two filed versions shows exactly two changed lines
(the Status line, and the added item). And the new file's body was diffed against **Bill's
original source** (`/tmp/REQ_OFFER_MECHANISM_revised.md`, still on disk from D-R-195):

```
136a137
> - turn-bound disclosure consent within a member-initiated exchange;
```

**One added line. Nothing else in the body differs from Bill's own text.**

Placement: immediately after *"confirmation of a member-initiated request"*, because it
clarifies that entry rather than opening a new idea.

### What did NOT change

- **The prompt's behavior is untouched.** No code in `harness/control_flow.py` or
  `server/voice_orch.py` was modified. A member hears exactly what they heard yesterday.
- **`harness/initiation.py` is untouched.** The ruling puts site 7 OUTSIDE the taxonomy, so
  there is nothing to add to a three-member enum. **No fourth class**, and no alias.
- **No site was reclassified.** HA-01's survey table stands; site 7's disposition moves from
  "AMBIGUOUS — STOP" to "outside R1 by Bill's ruling, member-initiated grant-confirmation
  path". HA-01's own dispatch doc is NOT rewritten — this record names it instead.

### What the ruling leaves open, named rather than implied

The member-initiated grant-confirmation path is **named in Ruling 1 and built nowhere**.
Site 7 now belongs to a path that does not exist as code — `grep` finds no
grant-confirmation module, and `harness/offer_gate.py`'s own survey already recorded that
nothing in this codebase issues or confirms a grant. **So the ruling correctly classifies
the prompt and does not, by itself, govern it.** That is a later step of §12, not a gap in
this ruling.

---

## PART 2 — D-R-196's 23-CASE BATTERY IS NOW COLLECTABLE AND REGISTERED

### What was actually wrong

`eval/test_sensitivity_no_default.py` shipped as a **standalone script**: a `main()` plus
helpers named `_site1`, `_site2`, … Pytest matches the FILENAME, so it would import the
module and collect **ZERO** tests from it. Adding it to the standing battery in that state
would have been **worse than leaving it out** — the list would have looked complete while
running nothing. HA-01 found this and reported it; D-R-196's own report had claimed those
23 cases as evidence without noting they sat outside the battery.

### The conversion

**All 23 cases are unchanged — same IDs, same assertions, same evidence.** Nothing was
dropped, weakened, or merged. What changed is shape:

- Each case is now its own pytest test, so a failure names the case instead of one script
  reporting a tally.
- The four sites whose fault twin and anti-vacuity read the SAME live call (S3, S4, S5, S6)
  keep that property: the call is made once in a module-scoped fixture and the two tests
  assert on the same observation. **Splitting them into two independent calls would have
  quietly weakened the pair** — "the same call returns one and refuses the other" is the
  claim, and two calls cannot make it.
- Live-graph work moved into module-scoped fixtures with cleanup finalizers. Two separate
  synthetic owners (write-boundary vs read-boundary) so the fact counts in S1a/S1b/S1c/S1d
  are not perturbed by the seeded read fixtures.
- `_check_env` now **fails** rather than `sys.exit`, and still refuses 7687 and 7689.

### "23 in, 23 collected" — the guard, and the honest arithmetic

`CASE_IDS` is a frozen manifest of the 23 IDs. A `@case(...)` decorator claims IDs, and
**raises at import time if two tests claim the same ID**, so the count cannot be padded.
`test_all_23_cases_are_collected` asserts `len(CASE_IDS) == 23` and **set equality**
between the manifest and what was actually registered — a set comparison, not a count,
because a RENAMED case is as much a drift as a deleted one and a count would miss the swap.

**THE FILE COLLECTS 24 PYTEST ITEMS: the 23 cases plus that one guard.** Stated here and in
the module docstring rather than rounded to 23, because a reader who counts 24 and finds no
explanation is right to distrust the number.

Measured: `pytest --collect-only` → **24 tests collected**; `pytest -q` → **24 passed**.

### Registered

`scripts/run_harness.sh`'s standing battery now lists `eval/test_sensitivity_no_default.py`.
It is graph-dependent, which is precedented in that list (`eval/test_erasure_route.py`
already is), and the harness holds the `graph:7688` lock across the battery block, so these
live writes are serialised with every other lane.

---

## RUNS

| Run | Result |
|---|---|
| Standing battery | **713 passed, 9 xfailed** — 689/9 + exactly the 24 newly-collected items |
| `--layer 7` L7 | **27/27** |
| `--layer 7` L7V2 | **27/28** (1 skipped — the opt-in live-output check) |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| Memory harness | **13/17** — failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the D-109/D-110 pin |

`--full` NOT run; Requirements Discipline item 12 is NOT satisfied and is not claimed.

## FINDINGS

1. **The ruling classifies site 7 but does not govern it** — the member-initiated
   grant-confirmation path it now belongs to is named in Ruling 1 and built nowhere.
2. **The battery list is still manual.** HA-01 filed this; HA-02 adds a second file to it
   and does not fix the mechanism. A new battery still runs only when someone remembers to
   name it, and the failure is silent — a green run and an un-run battery look identical.
   The durable fix would be a collection check that fails when an `eval/test_*.py` is absent
   from the list; deliberately not built here.
3. **`control_flow.py`'s stale "stubs — NOT connected to the pipeline" comment** is still
   stale (HA-01 finding 2). Site 7 being ruled makes that comment more misleading, not less,
   because a reader now has a ruling that depends on the prompt being live. Still not
   corrected — it remains a code change outside these two rulings' scope.
