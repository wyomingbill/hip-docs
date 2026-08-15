# DISPATCH_TD133_BURNDOWN_ITEM5
Status: BUILT
Reconciled-Against: see HASH below (same commit as this doc)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827.md`
(MET; this is ITEM 5 of Bill's five-item 2026-07-27 sprint instruction —
items 1-3 (`scripts/run_harness.sh`, mutation-survivor persistence,
coverage-grid) and item 4 (`REQ_DOC_RENDERING`) were built earlier the same
day by concurrent sessions in this same checkout; this dispatch is item 5,
the TD-133 burn-down, first slice)

## THE ASK

> Hold the write_rule burn-down. Bill has an open ruling on whether
> write-time directives should check attribute, and killing those mutants
> would lock current behavior in as intended before he decides.
>
> Start ITEM 5.
>
> TD-133 lists roughly 54 harness gaps, mostly missing fault-twins and
> metamorphic wrappers on crypto checks. Seven were closed on 07-26.
>
> Close the next TEN, in the priority order the HIP_TestingBestPractices
> research doc gives, CheckList-template and Hypothesis property-based
> generation first. Ten, not more, so the work stays reviewable.
>
> Each closure follows REQ_HARNESS_DISCIPLINE in full and the audit must
> pass on it by name. Skip any gap sitting on write_rule's directive/
> attribute path and say which you skipped.
>
> Report which ten you closed, which remain, and the new flagged count.
> Layer 7 green and RATCHET PASS after each checkpoint. Commit, push,
> report the hash. Do not mark any REQ MET.

## WHAT WAS DONE

1. Read `docs/deliverables/HIP_TestingBestPractices__research__v20260726_1005.md`'s
   own priority order (closing paragraph): "(1) CheckList template
   expansion + Hypothesis generation... closes the largest number of
   flagged twin/metamorphic gaps with two mechanisms; (2) semantic
   canary... (3) Wycheproof boundary vectors... (4) mutation score...".
   This dispatch's 10 closures are entirely priority-tier (1) — no
   semantic-canary, Wycheproof, or mutation-score work was touched, and
   none of the CT-family gaps (which belong to tier 2) were selected.
2. Ran a research pass (structural map, no code changed) over
   `check_registry.py`'s marker schema, `harness_audit.py`'s verification
   logic (`_verify_ref` — real verification against source/roster/probes,
   not presence-checking), and the exact implementation of every
   candidate check in `layer7_crypto.py`/`layer7_crypto_v2.py`, to select
   10 closures that were both high-leverage and genuinely CheckList/
   Hypothesis-shaped, not just convenient.
3. Confirmed `hypothesis` is not installed in `hip-dev/.venv` (checked
   directly: `ModuleNotFoundError`). Per `checklist_gen.py`'s own
   precedent (an in-repo template+lexicon generator instead of the real
   CheckList library, stated in its docstring), built a small in-repo,
   seeded generator instead of adding a new dependency mid-task.
4. Added `_property_seeded_values(label, n=6)` to
   `eval/harnesslib/layer7_crypto.py` — a deterministic (`random.Random`
   seeded on `label`, never wall-clock), varied-charset synthetic value
   generator. Wired it into 8 checks (`seal-to-dyad`, `DK2`, `N2`, `DK3`,
   `P2`, `P1`, `N1`, `N4`), each re-asserting its OWN existing invariant
   across 6 generated fact values (not just the one hand-picked demo
   string), through the SAME write helpers (`_write_dyad_fact`/
   `_write_plain`) and the SAME `written_fact_ids`/`finally` cleanup every
   other check in that file already uses — no new teardown mechanism.
5. Traced `DK2`'s twin gap by reading `L7:fault-injection`'s actual
   assertions (`layer7_crypto.py:510-521`): it already proves maya (DK2's
   own rightful custodian) is locked out of her own dyad's fact under the
   misseal-to-wrong-D_pub fault — DK2's own property, inverted. No new
   fault-injection code was needed; registered `L7:DK2`'s twin as
   `{"scenario": "L7:fault-injection"}`, the same reference N2/DK3/P2
   already use.
6. Read `layer7_crypto_v2.py`'s MT1/MT1-CHECKLIST code and
   `harness/injection_contract.py`'s `_inj3_cross_member_deny` to design a
   directional fault-injection twin for MT1: call the SAME judge
   (`apply_injection_contract`) with `requester_member_id="bob"` (enrolled,
   but not on alice's dyad for f1) against the SAME base query MT1's 12
   variants all admit for alice, and assert it is now DENIED. Verified
   the INJ-3 reasoning live (`bob_admitted=False`) before wiring the
   registry entry — REQ_CRYPTO_HARNESS_V2's own CONSTRAINT ("MT1 and MT2
   must never be conflated") is respected: this is a fault injected into
   the system under test, not a new member added to MT1's own 12/168-item
   wording corpus. MT1-CHECKLIST's twin reuses MT1's new one
   (`{"scenario": "L7V2:MT1"}`) — same judge, same property, same reuse
   pattern `ABM-route`/`FF1`/`FF3`/`FF4`'s `metamorphic` entries already
   use for MT1.
7. Registered all 10 in `check_registry.py`, replacing `_debt(...)`
   placeholders with real `{"marker": ...}`/`{"scenario": ...}` refs.
   First pass had a real bug (see WHAT WAS FOUND); fixed and re-verified.
8. Ran `scripts/run_harness.sh --layer 7` as a checkpoint after (a) adding
   the property/directional code, before touching the registry, and (b)
   after each registry-edit pass — not just once at the end.
9. Updated TD-133 (`docs/techdebt/DEBT_REGISTER__v20260727_1731.md`,
   symlink repointed) following its own established burn-down pattern
   (same shape as the 2026-07-26 entry): removed the 10 closed checks
   from the REMAINING-gaps prose, appended a dated BURN-DOWN paragraph.

## WHAT WAS FOUND

**A real bug in the first registry-wiring pass, caught by the audit
itself, not silently shipped.** `check_registry.py`'s marker verification
(`harness_audit.py`) reads a file's RAW SOURCE TEXT and checks for the
registry's marker string as a plain substring — not the Python-evaluated
string value. Six of my first-draft markers (`N2`, `DK3`, `P2`, `P1`,
`N1`, `N4`'s metamorphic markers) were chosen to include text that, in
`layer7_crypto.py`'s actual source, was split across TWO adjacent string
literals on separate lines (e.g. `"...N2 cross-dyad "` on one line,
`"isolation holds..."` on the next) — the Python VALUE concatenates
correctly at parse time, but the RAW FILE TEXT has a `"`-newline-`"`
sequence in the middle, so the substring search failed. First `--layer 7`
checkpoint after wiring the registry caught this immediately:
`NEW FAILURES (not in baseline): ['AUDIT:four-part-roster']`, with
`6 REJECTED` lines naming each broken marker exactly. Fixed by shortening
each registry marker to a substring guaranteed to sit entirely within one
unbroken source line (verified directly against each file's raw text with
a standalone probe script before re-running the harness) — `seal-to-dyad`
and `DK2`'s markers were unaffected because their chosen substrings
happened to fit on one line already. This is exactly the kind of mistake
REQ_HARNESS_DISCIPLINE's audit-verifies-not-declares design exists to
catch, and it did.

**Per-closure summary** (all 10, with the exact clause/mechanism):

- `L7:seal-to-dyad` (metamorphic) — property-based: 6 generated dyad-sealed
  values, `kv==2 and dyad_id==<correct>` holds for all.
- `L7:DK2` (twin + metamorphic) — twin: reused `L7:fault-injection` (zero
  new code); metamorphic: property-based, two-hop unwrap succeeds across
  6 generated values for both maya-ray and sam-ray.
- `L7:N2` (metamorphic) — property-based: 0 cross-dyad decrypt successes
  across 6 generated value pairs x 4 cross-attempt combinations.
- `L7:DK3` (metamorphic) — same generated corpus and assertion as N2 (they
  already shared `cross_dyad_successes` in the base check; the property
  wrapper preserves that sharing).
- `L7:P2` (metamorphic) — property-based: 0 locked-out custodians across
  6 generated dyad-sealed value pairs, enumerated via
  `dyad_registry.list_custodians`.
- `L7:P1` (metamorphic) — property-based: 0 locked-out household adults
  across 6 generated household-shared values.
- `L7:N1` (metamorphic) — property-based: 0 cross-member decrypt successes
  across 6 generated (bill, maya) member-private value pairs.
- `L7:N4` (metamorphic) — property-based: 0 of 6 generated dyad-sealed
  values leak into bill's household-scoped `read_user_facts` view.
- `L7V2:MT1` (twin) — fault-injection: `apply_injection_contract` with
  `requester_member_id="bob"` on the SAME base query and f1 fact alice's
  12 variants all admit; INJ-3 (`harness/injection_contract.py:475-519`)
  correctly denies (`bob_admitted=False`).
- `L7V2:MT1-CHECKLIST` (twin) — reuses MT1's new twin (same judge, same
  directional-flip property).

**Skipped, as instructed:** `L7:P4` (metamorphic), `L7:P4-EXT` (twin +
metamorphic), `L7:P4-EXT-row12` (twin + metamorphic), `L7:P4-EXT-row13`
(twin + metamorphic) — 7 flagged lines across 4 checks, all on
`harness/write_rule.py:classify`'s write-time directive/attribute
classification path. Not touched, not investigated further, per Bill's
open ruling on whether write-time directives should check attribute —
closing these mutants would lock current behavior in as intended before
that decision is made.

**Deferred, not skipped-forever** (kept the slice at exactly 10 per
Bill's own "ten, not more" instruction): `PS1`/`PS2` (retired v1-fixtures
— rebuilding either would require a genuine v1/master-sealed fixture,
categorically impossible post-master-key-destruction, violating this
session's own "do not touch any master key" constraint), `CT`/
`CT-VECTOR-INDEX`/`CT-OUTPUT-GAP` (the doc's own priority tier 2 —
semantic canary — not tier 1's CheckList/Hypothesis focus), `RI1`,
`RE1`-`RE7`, `ABM-route`, `FF1`, `FF3`, `FF4`, `SC1`, `SC1-E2E`,
`MT2-DECRYPT-REVOKE`.

**Score:** TD-133's four-part-roster FLAGGED count: **46 → 35** (56 checks
enumerated throughout, 0 missing/rejected both before and after).

## VERIFIED

- **Watched run:** a standalone probe script (`_property_seeded_values`
  called directly, each generated corpus fed through the real
  `_can_decrypt`/`_can_decrypt_caller` functions) confirmed every
  property-based check's invariant BEFORE wiring it into the registry —
  not assumed from reading the code.
- **Watched run:** the MT1 directional twin's `bob_admitted=False` result
  was observed in a live `--layer 7` run, not reasoned about from
  `_inj3_cross_member_deny`'s source alone (though that source WAS read
  first, to predict the outcome — the run confirmed the prediction).
- **Watched run:** `scripts/run_harness.sh --layer 7`, three times this
  session (after adding the property/directional code; after the first,
  buggy registry pass — caught the marker bug; after the fix). Final run
  (log: `/tmp/hip_harness_20260727_1729.log`): `L7: 24/24`, `L7V2: 27/28`
  (1 unchanged opt-in skip), `AUDIT: 8/8` (the extra 2 vs the 6 baseline
  are `REQ_DOC_RENDERING`'s new checks from item 4, unrelated to this
  dispatch), `four-part-roster PASS` (`56 checks enumerated; 0 missing
  artifact(s); 35 debt-flagged gap(s)`), `SCHEMA: 1/1`, `VOICE: 1/1`,
  `RATCHET PASS — no scenario regressed vs baseline`. None of the 10
  closed checks appear in the FLAGGED list any more (grepped by name to
  confirm, not just trusted the count).
- **Reasoned about:** the priority-order framing ("CheckList/Hypothesis
  first") is applied as stated in the research doc; whether a DIFFERENT
  10-item selection would have closed MORE gaps per unit of work was not
  exhaustively searched — this is a defensible, doc-consistent selection,
  not a proven-optimal one.

## HASH

See commit — this dispatch doc, `eval/harnesslib/layer7_crypto.py`,
`eval/harnesslib/layer7_crypto_v2.py`, `eval/harnesslib/check_registry.py`,
`docs/techdebt/DEBT_REGISTER__v20260727_1731.md` (+ `LATEST_DEBT.md`
repoint), and `docs/INDEX.md` all ship together.

## OPEN

- 35 TD-133 gaps remain. The doc's own priority order still has tier 1
  (CheckList/Hypothesis) headroom: `RI1` (roster invariant — twin +
  fixture, a natural property-based target not selected this slice to
  keep the count at exactly 10) and the `RE`-family's metamorphic gaps
  (structured custody/quorum records, same shape as the 8 crypto checks
  closed here) are the next highest-leverage tier-1 candidates.
- `write_rule`'s 7 flagged lines (`P4`/`P4-EXT`/`P4-EXT-row12`/
  `P4-EXT-row13`) stay open pending Bill's ruling on write-time
  directive/attribute checking — not this dispatch's to resolve.
- `RE2`/`RE3`/`RE4`/`RE5`/`RE6`/`RE7`'s twin gaps are flagged as "inline
  fault attempt per REQ_CRYPTO_P4; marker not individually re-verified by
  this audit build" — i.e. the fault-injection code may already exist and
  just need registration, the same shape DK2 turned out to be. Worth
  checking first in a future slice before building anything new for that
  family.
- No REQ was marked MET by this dispatch, per instruction.
