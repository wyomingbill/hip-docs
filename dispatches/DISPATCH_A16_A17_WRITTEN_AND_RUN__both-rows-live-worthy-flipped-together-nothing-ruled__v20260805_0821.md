# DISPATCH_A16_A17_WRITTEN_AND_RUN
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (writing two ceiling acceptance rows for the first time against
already-built mechanism) — no new REQ needed; the ceiling REQ and
`REQ_CEILING_ACCEPTANCE` already govern acceptance-row authorship.

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16/R17, ratified D-71. No amendment.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-173 | ~/hip-roadmap, roadmap | Write and run A16 + A17 together ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R16/R17, ratified D-71. That ruling requires
A16 and A17 to flip TOGETHER. The both-mechanisms ledger is built and cut over
(D-R-161 through 168); erasure is complete (D-R-169/170). The blocker named for both
rows is gone. Fixtures only — no real data.

1. Read both rows as filed. Confirm the blocker is gone; STOP if not.
2. Write both to the D-87 standard, run both, report each individually.
3. A passing row does not carry its requirement. Rule nothing. Report what evidence
   R16 and R17 rulings would now cite.
4. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 STOP.
```

## WHAT WAS DONE

1. Gate checked — matched, tree clean except another lane's own untouched WIP, HEAD
   in sync with `origin/roadmap`.
2. Read A16's and A17's own filed text in `REQ_CEILING_ACCEPTANCE__…v20260801_0617.md`
   in full (§4's A16 section, `:131-145`; the row table's A17 entry, `:213`) — both
   explicitly state their own blocker and both explicitly say "must flip together."
3. **Grepped for any existing `test_ceil_a16_*`/`test_ceil_a17_*` function anywhere
   in `eval/` before writing a line of code** — zero hits. Despite the extensive
   ledger/erasure work this session (D-R-161 through D-R-172), NEITHER row had ever
   been formally written in this project's own `test_ceil_a<N>_*` acceptance-row
   convention; the generated status board would still show both at their stale,
   pre-rebuild tier.
4. Confirmed the blocker named for each row is gone, against HEAD, not assumed:
   - A16's own blocker ("Fails against: the ratified crypto-shredding design...
     erasure is by key destruction, not absence... What flips it: the R16 ruling of
     D-71 (both mechanisms) being built") — built: Segments 1-4 (D-R-161 through 164)
     plus the full v1→v2 cutover across all 17 real production ledger call sites
     (D-R-165, 166, 168).
   - A17's own blocker ("The only hard delete in the codebase is
     `server/demo_dashboard.py:1890`... No per-fact delete exists anywhere") —
     built: `harness.graph_erasure.erase_fact`/`erase_member_facts` (D-R-169/170),
     cascade-aware, fixture-proven, plus the machine-verifiable report (D-R-167,
     extended 169/170) and the real request path (D-R-172).
   - **No STOP fired — item 1's own condition was checked against the real code, not
     inferred from prior dispatch docs' own prose.**
5. Wrote both rows into `eval/test_ceiling_retention.py` — the established Axis-2
   home (R16-R22) alongside A19-A21 — rather than a new file, matching this
   project's own "one file per axis" convention.
6. **A16's own executed proof calls the REAL production caller function**
   (`harness.epistemic_record.log_epistemic_record`) against a HERMETIC ledger — the
   actual code that runs for a real turn, fixture-scoped storage, matching every
   ledger test this session's own established pattern.
7. **A17's own executed proof calls the REAL request path**
   (`harness.erasure_request`, D-R-172) against the REAL shared dev graph with
   disposable, uniquely-prefixed fixtures.
8. **Found and fixed a real, self-caused regression on the first `--layer 7` run**:
   my own A16 fixture reloaded `harness.ledger_commitment`/`harness.ledger_payload_store`
   (copying the pattern from other ledger test files' own `env` fixtures without
   checking whether it was actually needed) — since `test_ceiling_retention.py` now
   runs BEFORE `eval/test_ledger_commitment.py` in `scripts/run_harness.sh`'s own
   battery order, this created a NEW `WeakCommitmentKey` class object, breaking that
   file's own `pytest.raises(WeakCommitmentKey)` (bound at collection time, before
   the reload) — the exact `importlib.reload()` identity-mismatch class this session
   hit once before at D-R-161. **Fixed by checking whether the reload was even
   necessary first**: read `harness.epistemic_ledger._ledger_dir()` directly and
   confirmed it reads `HIP_HEL_DIR` fresh on every call, so `monkeypatch.setenv`
   alone is sufficient — removed every reload the fixture did not actually need,
   closing the regression at its root rather than reordering files to dodge it.
9. **Also fixed a second, familiar bug in my own new test**: the A17 cascade test's
   own derived-child fixture initially shared its parent's owner, making the
   erased-vs-cascade distinction untestable — the exact same test-design mistake
   made once before at D-R-170, caught the same way (the first run), fixed the same
   way (give the child a different owner, proving cross-owner cascade
   reachability instead of redundant owner-matching).
10. Ran `eval/test_ceiling_retention.py` standalone under the graph lock, then
    together with `eval/test_ledger_commitment.py` specifically to confirm the
    pollution fix: both clean.
11. Confirmed, by direct query, zero fixture residue (`ceil-a17-fixture-*` prefix)
    after the standalone run and after the full battery run.
12. Ran the full standing battery (34 files, unchanged wiring — both new rows landed
    in an already-wired file) via `scripts/run_harness.sh --layer 7`: first pass
    caught the regression in step 8; fixed; re-ran clean.
13. **RATCHET PASS — no scenario regressed vs baseline.**
14. Ran the memory harness under the graph lock: **13/17**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — the same pinned set as every prior
    dispatch this session, not a new regression.
15. Wrote this dispatch doc, including item 3's own "what evidence a ruling would
    cite" statement.
16. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### Item 1 — the blocker for each row, confirmed gone against HEAD

**A16.** Filed blocker: the ledger carried inline AES-256-GCM ciphertext, erasure
only by key destruction — "not absence." Confirmed gone: a real write through
`log_epistemic_record` now produces a `hel=="2.0"` event carrying ONLY
`keyed_commitment` and structural metadata — no `payload`/`payload_enc`, no
plaintext identifier. Confirmed across ALL 17 real production ledger call sites
(not just the one this row's own executed test exercises) via the pre-existing,
still-green standing invariant `eval/test_ledger_callsite_enumeration.py`'s own
`test_ledger_callsite_enumeration_completeness`/`_uniformity` — cited as supporting
breadth evidence, not reimplemented as a second, competing scan.

**A17.** Filed blocker: "the only hard delete in the codebase is
`server/demo_dashboard.py:1890`... No per-fact delete exists anywhere." Confirmed
gone: `harness.graph_erasure.erase_fact`/`erase_member_facts` are real, cascade-aware,
per-fact AND per-member deletes, with a machine-verifiable report proving every
applicable one of R17's seven steps, reachable through a real (if unenabled) request
path.

**No STOP fired for either row.**

### Item 2 — both rows, written and run, D-87 standard, reported individually

**A16 — `eval/test_ceiling_retention.py`, CEIL-A16 section (4 cases, all pass):**
- `test_ceil_a16_a_real_production_write_carries_no_forbidden_field` — executed:
  a real `log_epistemic_record` call (hermetic ledger) produces an event with zero
  forbidden fields, `keyed_commitment` present.
- `test_ceil_a16_fault_twin_a_v1_event_fails_the_same_check` — executed fault twin:
  the identical check, against a genuine `hel=="1.0"` event, correctly finds a
  forbidden field, proving discrimination.
- `test_ceil_a16_version_gated_hashing_registers_a_distinct_v2_shape` — structural
  anti-vacuity: the `hel=="2.0"` hash-field set is real and distinct from `"1.0"`,
  not a copy.
- `test_ceil_a16_anti_vacuity_forbidden_and_permitted_sets_are_real` — the checked
  sets themselves are non-trivial.

**A17 — `eval/test_ceiling_retention.py`, CEIL-A17 section (5 cases, all pass):**
- `test_ceil_a17_a_real_erasure_request_produces_a_verified_report` — executed:
  a real per-fact request (`harness.erasure_request.request_fact_erasure`) against
  a fixture, `verify_erasure_report` returns True.
- `test_ceil_a17_subject_wide_erasure_also_verified_with_cascade` — executed: a
  member-wide request erases every owned fact including a CROSS-OWNER derived
  cascade child, report verifies.
- `test_ceil_a17_fault_twin_an_incomplete_erasure_is_caught` — executed fault
  twin: cascade bypassed (orphan left behind), report correctly refuses to verify.
- `test_ceil_a17_anti_vacuity_erasure_mechanism_and_report_both_exist` — the
  functions under test are real, not renamed out from under the row.

### Item 3 — nothing ruled; what evidence R16/R17 rulings would now cite

**Nothing ruled here, per instruction.** If Bill rules on R16 and/or R17, the
evidence now on record: for R16, the executed proof that a real production write
(through the one call site every real household turn already reaches) carries no
forbidden field, the discriminating fault twin, AND the pre-existing standing
invariant proving this holds across all 17 real production call sites uniformly —
plus the PERMANENT, unavoidable limit this dispatch does not paper over: every
`hel=="1.0"` event written before its own respective cutover remains forbidden-field-
bearing forever (the two-population reality established at D-R-165, unaffected by
anything built since). For R17, the executed proof that a real (fixture-scoped)
erasure request — both per-fact and per-member, with cascade — produces a
machine-verifiable report proving completeness, the discriminating fault twin
proving an incomplete erasure is caught rather than passed, PLUS the equally
permanent limits: no backup system exists to schedule expiry against (step 6), no
embedding/vector mechanism exists for step 4 to remove (structurally N/A, not
unbuilt), and — the newest, most significant limit, named at D-R-170/172 — **no real
caller anywhere in this codebase reaches either mechanism from an actual request**;
everything proven here is fixture-scoped and unenabled. **A passing row is evidence
a ruling could cite, not the ruling itself.**

## VERIFIED

**Watched, executed:**
- Grep confirming zero pre-existing `test_ceil_a16_*`/`test_ceil_a17_*` functions,
  run before writing anything.
- `harness/epistemic_ledger.py::_ledger_dir` read directly to confirm it re-reads
  `HIP_HEL_DIR` on every call, before deciding the fixture's own reloads were
  unnecessary — not assumed from another file's own established pattern.
- `eval/test_ceiling_retention.py` + `eval/test_ledger_commitment.py` run together
  explicitly, confirming the cross-file regression found on the first `--layer 7`
  run was actually fixed, not just no-longer-observed by coincidence of a different
  run.
- Direct query confirming zero fixture residue (`ceil-a17-fixture-*`), after the
  standalone run and after the full battery run.
- `scripts/run_harness.sh --layer 7`: first pass caught one real, self-caused
  regression (step 8 above); fixed; re-ran clean; **RATCHET PASS**.
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.

**Reasoned about, not independently re-derived:** whether A16/A17's own executed
proofs constitute the SAME evidentiary weight as A2/A8's "real creator path" gold
standard (§7.7) is a judgment call, not mechanically decided — argued here that they
do, MORE fully than A23/A24's own "module-direct, no real caller" limitation, because
R16's mechanism DOES have real, live production callers (all 17), unlike R23/R24's
own zero.

## HASH

Staged for commit: `eval/test_ceiling_retention.py` (extended with CEIL-A16 and
CEIL-A17 sections), this dispatch doc.

## OPEN

- **This dispatch does not re-tier A16/A17 on the status board** — per instruction,
  "rule nothing." The generated `docs/status/CEILING_STATUS.html` still reflects
  their prior tier until Bill rules and a future dispatch regenerates it.
- **The two-population limit (R16) and the no-real-caller limit (R17) are
  PERMANENT, not gaps this or any future dispatch closes** — restated here so a
  ruling is made with full knowledge of what "MET" would and would not mean.
- **Nothing ruled MET.**

## RECAP
D-R-173: confirmed, against HEAD, that both rows' own filed blockers are gone —
zero `test_ceil_a16_*`/`test_ceil_a17_*` function existed anywhere despite the
extensive D-R-161 through D-R-172 mechanism build; wrote both for the first time in
`eval/test_ceiling_retention.py`, the established Axis-2 home. A16: a real write
through the one production call site every household turn reaches carries no
forbidden field, proven executed, with a discriminating fault twin and the
pre-existing standing invariant covering breadth across all 17 real call sites.
A17: a real (fixture-scoped) erasure request — per-fact and per-member, with
cross-owner cascade — produces a machine-verifiable report proving completeness,
with an executed fault twin proving an incomplete erasure is caught, not passed.
Found and fixed two real, self-caused bugs on the first run: a cross-file test
pollution regression (an unnecessary `importlib.reload()` copied from another
file's fixture without checking it was needed, closed at its root by confirming
`_ledger_dir()` reads its env var fresh), and the same derived-child-shares-owner
test-design mistake made once before at D-R-170, fixed the same way. Both rows pass;
neither row's passing is itself a ruling. Reported the evidence a ruling would now
cite for each, including the permanent limits (the two-population reality; no real
caller anywhere) that a "MET" ruling would need to be honest about regardless. 9
new tests, full battery green, RATCHET PASS, memory harness 13/17 at the same pinned
failing set. Nothing ruled MET.
