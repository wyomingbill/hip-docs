# DISPATCH_R2_R8_R10_MET
Status: BUILT
Reconciled-Against: 2026-08-05 (D-R-183; parent `8a08775`)

**TYPE:** BUILD (ruling record + one predicate correction, same-edit tier flip)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
R2, R8, R10 — existing REQ, no amendment; this dispatch records rulings and finishes
one predicate the ruling made buildable.

## THE ASK

```
=== D-R-183 | ~/hip-roadmap, roadmap | Record R2, R8, R10 MET. The not-met column
    closes. ===
STANDARD PREAMBLE. Lane A.

1. RECORD R2 MET (Bill, 2026-08-05, on D-R-180): part 1 built and enforced, A2
   executed and passing; parts 2 and 3 true because no code does either — 16 files
   read, nothing watching, and the ruling says so. A to-do is authorized for a
   standing check that catches new inference sites (same shape as the ledger
   call-site test). File it as a TD.
2. RECORD R8 MET (Bill, 2026-08-05): the hidden-guess problem is fixed — undetermined
   facts carry a marker naming their candidate labels, proven at D-158/D-159. Limits
   in the ruling text: two labels need reading the words (deferred by ruling), one has
   no signal, one waits on TD-160, and the marker is bookkeeping, not protection.
3. RECORD R10 MET (Bill, 2026-08-05): all four door checks proven firing at D-140;
   the only stated block was R2 and R8 unproven, both now MET.
4. Re-tier A2 and A10 LIVE. A10 is a strict xfail — the re-tier and the predicate
   correction land in THE SAME EDIT, per the A1/D-100 rule.
5. Do NOT restore the header enumeration. D-131 stands.
6. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 STOP.
7. Rule nothing else. Report SHORT.
```

## WHAT WAS DONE

1. Gate checked, matched. Tree clean except demo-cutover's own untouched WIP, lock
   free, HEAD at `8a08775` (D-R-180) at start.
2. Recorded R2, R8, R10 MET in `REQ_STRUCTURAL_CEILING` §16, newest-first after R17
   (today's own ruling chain), evidence exactly as items 1-3 specify, limits written
   INTO the ruling text per instruction. Old NOT MET entries (D-143, D-144, D-100)
   annotated `*(historical — see MET ruling above)*`, bodies untouched.
3. **A2 was already LIVE** (D-145, 2026-08-03) — nothing to re-tier there; noted in
   R2's own ruling text so a future reader isn't sent looking for a tier flip that
   already happened two days earlier.
4. **A10 re-tiered LIVE, predicate fixed in the same edit.** Read R10's own text
   (`store.py::encode` SHALL revalidate origin, attribute registry, representation
   class, permit) and `_a10_enforced_at_creator`'s existing two probes (origin,
   registry). Added two more, reusing CEIL-A8's and CEIL-A2's own real-path shapes
   rather than inventing a third: `representation` (an unrecognized attribute via the
   `fixture`-origin exemption is refused `UNKNOWN_HIGH_RISK`, no write) and `permit`
   (an off-permit `source_categories` value on a `derivation`-origin write is refused
   under `allowed_input_attributes`, no write). Manually confirmed both refuse for the
   SPECIFIC named reason, not merely some exception. Removed the `xfail(strict=True)`
   marker from `test_ceil_a10_all_four_revalidations_land_at_the_creator`; renamed and
   widened its anti-vacuity companion (`test_ceil_a10_the_two_buildable_checks_do_fire`
   → `test_ceil_a10_all_four_checks_do_fire`) to assert all four. The two existing
   meta-level fault twins needed no change (they monkeypatch the creator entirely).
5. Updated `REQ_CEILING_ACCEPTANCE`'s tier-count table (LIVE 11→12, STRICT XFAIL 5→4)
   and added §7.9 (A10's own re-tiering section, matching §7.6/§7.8's precedent shape).
   Did NOT touch the header/§16-intro enumeration — confirmed unchanged by diff (pure
   additions) — D-131 stands, per instruction.
6. Filed **TD-R-163** (new debt-register version, `v20260805_1355`, LATEST repointed —
   a material addition): the standing check authorized by item 1, same shape as
   `eval/test_ledger_callsite_enumeration.py`, not built (needs a REQ per Requirements
   Discipline item 8).
7. Ran `eval/test_ceiling_inference.py` standalone (15 passed), then the full standing
   battery + `--layer 7`: clean on the first run — `RATCHET PASS`, no new failures,
   `MUTATION-NO-SILENT-DISAPPEARANCE PASS` (write_rule.py untouched this dispatch, no
   line-shift risk). Memory harness under the graph lock: 13/17, failures exactly
   `{MEM-115, MEM-116, MEM-117, MEM-118}`, inside the 13-15/17 pin.
8. Wrote this dispatch doc, registered it in `docs/INDEX.md`, updated
   `docs/HIP_HANDOFF.md` CURRENT STATE, committed and pushed under the repo lock.

## WHAT WAS FOUND

Both new A10 probes verified to refuse for the exact named reason (not a lucky
coincidence): the representation probe's exception reads `"representation_class
classified as UNKNOWN_HIGH_RISK"`; the permit probe's reads `"outside R2's
allowed_input_attributes"`. `test_ceiling_inference.py`'s own R2 docstring section
("R2 IS RULED NOT MET...") was stale the moment this dispatch's ruling landed —
corrected in the same commit rather than left to drift.

## VERIFIED

**Watched, executed:** `eval/test_ceiling_inference.py` standalone (15 passed,
including the newly-live A10 row); a manual probe confirming both new A10 checks
refuse for their specific named reason; full standing battery + `--layer 7`
(`RATCHET PASS`, `MUTATION-NO-SILENT-DISAPPEARANCE PASS`, `COVERAGE-GRID-RATCHET
PASS`); memory harness under the graph lock (13/17, pinned set unchanged).

**Reasoned about:** that A2/A10's own passing rows constitute sufficient evidence for
R2/R10's MET rulings is Bill's own call, stated in his dispatch text, not re-derived
here — this dispatch executes the ruling and its mechanical consequences, it does not
re-argue the ruling's own grounds (those were established at D-R-180 and in Bill's own
words above).

## HASH

`57e3f51` — pushed to `origin/roadmap`. Filled in by a same-session follow-up edit
after the commit landed, per the D-R-176/179/180 convention. Contains:
`docs/HIP_HANDOFF.md`, `docs/INDEX.md`,
`docs/requirements/REQ_CEILING_ACCEPTANCE__...v20260801_0617.md`,
`docs/requirements/REQ_STRUCTURAL_CEILING__...v20260802_2205.md`,
`docs/techdebt/LATEST_DEBT.md` (repointed), `docs/techdebt/DEBT_REGISTER__v20260805_1355.md`
(new), `eval/test_ceiling_inference.py`, this dispatch doc.

## OPEN

- **TD-R-163 is authorized, not built** — needs a REQ before any code is written
  against it (Requirements Discipline item 8).
- **R5 and R6 still have no standing regression tripwire** — the same open item D-143
  and D-R-180 both named, unchanged; TD-R-163 is the filed placeholder for closing it.
- **Nothing else ruled**, per instruction.
