# DISPATCH_A10_BATTERY
Status: BUILT (A10 wired; A1 STOPPED — false red, re-tiering is Bill's)
Reconciled-Against: ebb1713 (HEAD at gate); D-98 landed mid-dispatch, base moved to eb51f05
REQ: `docs/requirements/REQ_ARCHITECTURE_BOUNDARY__reference-monitor-threat-model-and-contracted-clients__v20260801_0919.md` — step 4 of the D-84 plan — and `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` R1/R10
Dispatch: D-99, 2026-08-01
**Status proposed: NONE. Nothing ruled MET. No tier changed.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @ `ebb1713`, clean.
Repo `.env.dev` only, per the note. **Nothing ruled MET. R10's status is yours.**

Step 4 of D-84's four-step plan — the last one. Steps 1–3 landed at `b634962` and D-97.

---

## THE HEADLINE — both rows are red for reasons that are not the ones they were filed with

Neither A1 nor A10 is what D-77 classified. Both predicates were stale, and they were stale
in **opposite directions**:

- **A10 was too pessimistic.** Filed as "encode performs *none* of the four." Two of four
  now land. **Re-derived and wired — still red, honestly.**
- **A1 was flatly false.** Its red says the mechanism does not exist. **It does.** Proven by
  probe below. **STOP CONDITION FIRED — the re-tiering is yours.**

---

## A10 — wired, and the finding is that it cannot flip on its own

R10 names four revalidations. Probed **behaviourally** at `create_fact_node` (a check counts
only if the creator raises **and** issues no write — a creator that raises *after* writing
has enforced nothing, the row is already in the graph):

| R10 check | State | Why |
|---|---|---|
| **origin** | ✅ enforced | `validate_origin()` — unknown origin refused, D-97 |
| **registry** | ✅ enforced | canonical-bound origins revalidate against `CANONICAL_ATTRIBUTES`, D-97 |
| **representation** | ❌ **unbuildable** | R8's representation classes **do not exist** — A8 is UNWRITABLE for exactly this: *"new enum + write-time validation; verified absent at HEAD"* |
| **permit** | ❌ **unbuildable** | R2's typed inference permit **does not exist** — A2 is UNWRITABLE: *"new permit type + registry + enforcement at the abstraction boundary"*. The lone `PERMIT` in the codebase is INJ-3's **read-side** owner permit, a different mechanism on the other side of the system |

**A10 is a DOWNSTREAM row, not an independent one.** It flips when A2 and A8 build — not
when someone finishes "step 4 leftovers." That is worth knowing before it gets scheduled,
and it is now written into the test's own docstring so the next reader gets it without
re-deriving it.

**What the re-derivation changed.** The old predicate read `encode`'s *source* for the four
check names. Correct when written, wrong now twice over: since D-96 the single
materialization point is `create_fact_node` and encode reaches it through the four lifecycle
transactions, so reading encode's body no longer sees the checks **even when they fire**;
and name-in-source is a weak proxy — a function mentioning "permit" passes it while
enforcing nothing.

Wired with a full complement, per D-87's convention:

- `test_ceil_a10_all_four_revalidations_land_at_the_creator` — the row, `xfail(strict=True)`, red at 2/4.
- `test_ceil_a10_the_two_buildable_checks_do_fire` — **not** xfail. Records the half that *is* built so the single red isn't misread as "no revalidation exists", and doubles as the probe's anti-vacuity guard: if this stops passing, the probe can no longer detect *any* check and the xfail above would be red for the wrong reason.
- `test_ceil_a10_fault_twin_a_creator_enforcing_nothing_scores_zero` — a permissive creator must score 0/4, proving the probe measures enforcement rather than reporting a constant.
- `test_ceil_a10_fault_twin_raising_after_the_write_does_not_count` — the discriminating condition, asserted directly.
- `test_ceil_a10_anti_vacuity_one_materialization_point_exists` — A10's premise.

Two obsolete companions of the removed source-reading predicate were deleted rather than
left dangling.

---

## A1 — STOP CONDITION FIRED. Its red is false, and I did not fix it.

Probed against live code, not reasoned about:

```
A1 half 1 — allowlist exists and is importable : True  ['lifestyle', 'risk_pattern']
A1 half 2 — off-allowlist derived attr REFUSED : True (and no write issued: True)
A1 twin   — risk_pattern ACCEPTED by derivation: True

==> A1, correctly re-derived, would PASS
```

That is exactly A1's requirement — *"off-allowlist derived attribute is refused and logged;
`risk_pattern` fault twin is accepted"* — satisfied by D-97's work.

**The predicate is stale in BOTH halves**, not the one D-97 flagged:

1. It looks for `DERIVABLE_ATTRIBUTES` in four candidate files that deliberately exclude
   `harness/write_origins.py`, where it now lives. *(the known half)*
2. It looks for enforcement **inside `_write_derived_node`** — which since D-96 **delegates**
   to `create_fact_node` rather than validating inline. So even pointed at the right module,
   it would still miss the enforcement. *(the half nobody had spotted)*

**I left it unchanged, deliberately.** Correcting the predicate makes the row XPASS, and a
`strict=True` xfail that passes is a red suite — so I cannot both re-derive it and leave the
tree green. Flipping the tier is yours, exactly as A18's was (D-86 reported, D-87 re-tiered
*and* re-wired in one move). The re-derived predicate is ready to apply with the re-tiering.

**But I did not leave the falsehood invisible.** The stale reason string is replaced with one
that says it is stale, and a `⚠ D-99` block sits directly above the marker recording that the
mechanism exists, that this was proven by probe, and why the row was left as-is. The module
docstring carries the same, for both rows. **No behaviour changed — the row still xfails,
the suite is still green, no tier was touched.**

### The re-derived predicate, ready to apply

```python
def _a1_enforced() -> bool:
    """R1 behaviourally: off-allowlist derivation refused with no write issued,
    and risk_pattern accepted. Follows the D-96 delegation instead of reading
    _write_derived_node's body."""
    from harness.write_origins import DERIVABLE_ATTRIBUTES        # must exist
    import memory_engine.store as _store
    rec = _ProbeRecorder()
    try:
        _store.create_fact_node(rec, _probe_props("not_on_the_allowlist"),
                                origin="derivation")
        return False                                              # not refused
    except ValueError as e:
        if "derivation may not emit" not in str(e) or rec.calls:
            return False                                          # wrong reason, or wrote
    rec = _ProbeRecorder()
    _store.create_fact_node(rec, _probe_props("risk_pattern"), origin="derivation")
    return bool(rec.calls)                                        # twin accepted
```

Applying it **requires** flipping `xfail(strict=True)` → LIVE in the same edit, or the suite
goes red on an XPASS.

---

## Evidence

```
standing batteries (16 files): 245 passed, 9 xfailed
== AUDIT:  8/8   == DISC: 1/1   == L7: 27/27
== L7V2:   27/28 (1 opt-in skip)   == SCHEMA: 1/1   == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.   0 scenario FAILs.
ABSOLUTE, read individually: G0 PASS · PSA1 PASS · CTX-STRIP PASS · LI1 PASS · CS1 PASS
```

**Memory harness: 13/17 — identical to the D-96/D-97 baseline, failing the identical four**
(MEM-115/116/117/118, pre-existing and environmental). **Zero delta; the step-5 STOP did not
fire.**

`--full` not attempted — TD-129's guard, as anticipated; not fought.

## Two parallel-lane collisions, handled

The tree did not stay still under this dispatch. Recorded because the lock protocol is the
only reason neither became a clobber:

1. **The D-98 lane (`sonnet5`) held `docs/.INDEX_MANIFEST_LOCK` mid-dispatch** — alive, mtime
   two minutes old, actively editing `DESIGN_LEDGER_ANCHOR` and `REQ_ARCHITECTURE_BOUNDARY`.
   I did the code work and the full evidence run but **did not touch INDEX** while it was
   held. It released and committed (`eb51f05`) before I registered; I re-checked rather than
   assumed, and my base moved `ebb1713` → `eb51f05` with no overlap.
2. Staged with **explicit pathspecs** throughout, so that lane's in-flight edits could not be
   swept into my commit.

## What this did NOT do

- **Did not re-tier A1.** Yours, and it needs the predicate swap in the same edit.
- **Did not rule R10.** Two of four checks land; whether that is MET is yours, and my read is
  that it plainly is not — A10 is blocked behind A2 and A8.
- **Did not touch A2, A8, or the 16 UNWRITABLE rows.**
- **No production code changed** — this dispatch touched one eval battery.
