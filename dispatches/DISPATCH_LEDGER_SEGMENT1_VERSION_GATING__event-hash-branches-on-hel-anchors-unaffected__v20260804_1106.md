# DISPATCH_LEDGER_SEGMENT1_VERSION_GATING
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (Segment 1 of the R16/R17 rebuild D-160 proposed — pure prerequisite
infrastructure; A16/A17 unaffected)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16 (ratified D-71, "both mechanisms") — no amendment, no new REQ doc; this builds toward
the existing, already-ratified requirement, same posture D-130/D-140 took for R2/R8.

## THE ASK

Dispatch text, verbatim:

```
Proceed with the segmented build. Segment 1 (the version-gated event hash) first and
alone — nothing else touches the chain until anchors are proven to survive it.
Segment 5 splits out as its own dispatch; it is an identity-scheme decision, not a
ledger change, and the rest must not wait on it.
After segment 1 lands, report which segment you propose next and why before building it.
```

Following directly from `docs/dispatches/DISPATCH_R16_R17_LEDGER_SURVEY__stopped-before-
build-anchor-compatibility-conditional__v20260804_1026.md` (D-160)'s own proposed
7-segment sequence.

## WHAT WAS DONE

1. Gate checked — matched. **Mid-dispatch, discovered `CLAUDE.md` had gained three new
   coordination rules (items 8-10) from another lane sharing this checkout** — directly
   naming this session's own D-152/D-156 lock-holding pattern and D-158's unpushed-commit
   incident. Applied both new disciplines to this dispatch immediately:
   - **Item 9 (lock around the git operation only):** the survey/build/test work below
     ran with NO repo lock held at all — the lock was taken only for the final
     add+commit+push sequence, as one guarded command, and released automatically on
     exit (no `sleep`, no separate release step).
   - **Same principle applied to the graph lock** for the memory-harness run (not named
     explicitly in the new rule, but the same reasoning): the lock wrapped the ACTUAL
     `eval/memory_harness.py` invocation itself, not a `sleep` placeholder with the run
     happening outside it — this session's own prior pattern (D-149 through D-160) had
     been the same anti-pattern the new rule names, just on the graph resource instead
     of `repo`. Corrected here, going forward.
2. Read `event_hash()`, `_HASH_FIELDS`, and every real caller (`_build_event`,
   `verify()`, `harness/ledger_anchor.py`, and the 5 test files touching either) before
   changing anything — confirmed `_HASH_FIELDS` is asserted by name (not just content)
   in `eval/test_registry_version_stamp.py`'s own AST scan, so the existing name and
   object had to survive unchanged, not be renamed.
3. Built the version-gating: `_HASH_FIELDS_BY_VERSION = {"1.0": _HASH_FIELDS}` (the
   SAME object, not a copy — `harness/write_origins.py`'s own `DERIVABLE_ONLY`
   discipline, reused), `event_hash()` now looks up the field set by `event["hel"]`
   and raises the new `UnknownLedgerVersion` (the R29/D-105 fail-closed pattern) for
   any unregistered version — including a missing `hel` field entirely.
4. Ran the FOUR existing pytest files that exercise `event_hash`/`_HASH_FIELDS` before
   writing any new test — 53 passed, byte-identical to before the change.
5. Ran `eval/test_hel_smoke.py` directly (it is a standalone script, not
   pytest-collected — confirmed via `--collect-only`, "no tests collected," so it was
   never part of the 53 above) — 33/33 checks, ALL PASS.
6. Wrote `eval/test_ledger_hash_versioning.py`: registry-identity, byte-identical
   hashing for real `hel=="1.0"` events (reconstructing the pre-change computation by
   hand, not by calling `event_hash` twice — that would prove nothing), a real
   multi-event chain still verifying end to end, a version-branch proof (a synthetic
   `hel=="2.0"` field set produces a genuinely different hash, and registering it does
   NOT change what a real `hel=="1.0"` event hashes to), two fail-closed tests (unknown
   version, missing `hel`), an executed fault twin (a permissive lookup that WOULD
   accept the bad version, proving the real guard does real work), and anti-vacuity
   (two different real events still hash differently; `payload_sha256` still covered).
7. **Caught and fixed a real bug by running the file, not by re-reading it**: three
   exception-raising tests failed on first run — `pytest.raises(UnknownLedgerVersion)`
   didn't match the raised exception. Root cause: the `hel` fixture (matching
   `test_ledger_anchor.py`'s own established pattern) does `importlib.reload()`, which
   replaces `harness.epistemic_ledger`'s namespace in place — a name bound at
   collection time (`from harness.epistemic_ledger import ... UnknownLedgerVersion`)
   goes stale, and the reloaded module raises via its OWN, now-distinct class object.
   Fixed by referencing the module fresh (`import harness.epistemic_ledger as hel_mod`)
   at the point of use in those three tests, matching the pattern the file's own
   pre-existing fault-twin test already used correctly.
8. Ran the fixed file standalone: 11/11 passed. Ran it combined with the 4 pre-existing
   ledger test files: 64/64 passed.
9. Wired `eval/test_ledger_hash_versioning.py` into `scripts/run_harness.sh`'s standing
   battery list — real, D-87-tested coverage of new production code, same treatment
   every other REQ-relevant test file already gets.
10. Ran the full standing-battery list (25 files now): 498 passed, 9 xfailed — +11 over
    D-159's 487/9, exactly this dispatch's own addition.
11. Ran `./scripts/run_harness.sh --layer 7`: AUDIT 8/8, L7 27/27, L7V2 27/28, SCHEMA
    1/1, VOICE 1/1, RATCHET PASS.
12. Ran `eval/memory_harness.py` under the graph lock, held only for the run itself
    (item 1's own corrected pattern): 13/17, failing set exactly `{MEM-115, MEM-116,
    MEM-117, MEM-118}`.
13. Wrote this dispatch doc.
14. Staged by explicit pathspec, and — per the new item 9 — committed AND pushed as one
    lock-guarded command (`hip_lock.py with repo "..." -- bash -c 'git add && git commit
    && git push'`), lock held only for that sequence's actual duration.

## WHAT WAS FOUND

### The change is exactly as narrow as D-160 proposed

`event_hash()` now branches on `event["hel"]` via `_HASH_FIELDS_BY_VERSION`. For every
event that exists or will be written under `hel=="1.0"` (every event so far, and every
event until a `hel=="2.0"` writer is built in a LATER segment), the lookup resolves to
the identical `_HASH_FIELDS` object used before this change — **verified, not assumed**:
a real event's hash was reconstructed by hand using the pre-change computation and
compared byte-for-byte against `event_hash()`'s own output, and matched exactly.

### The anchor-compatibility property this segment exists to protect — confirmed intact

D-89's own compatibility proof (`harness/ledger_anchor.py`'s module docstring) depends
entirely on `event_hash()` never changing what it returns for an already-anchored event.
This segment's own acceptance test (`test_hel_1_0_events_are_unaffected_by_a_newly_
registered_future_version`) proves the SPECIFIC scenario that would break it — registering
a brand-new version in the lookup table — does NOT touch a real `hel=="1.0"` event's
hash. **No anchor taken to date is affected by this change, and none will be affected by
a future `hel=="2.0"` registration either**, which is the whole point of building this
segment before anything else touches the chain.

### The version branch is real, not decorative

`test_hel_a_future_version_can_use_a_different_field_set` proves a synthetic `hel=="2.0"`
registration produces a genuinely different hash than the same dict would get under
`hel=="1.0"` — the lookup is live, not a pass-through that happens to always resolve to
the same tuple.

## VERIFIED

**Watched, executed:**
- 53 pre-existing tests across 4 files: unchanged pass count and (spot-checked) output,
  before writing anything new.
- `eval/test_hel_smoke.py`: 33/33 ALL PASS, direct script execution (not pytest-collected
  — confirmed via `--collect-only`).
- `eval/test_ledger_hash_versioning.py`: 11/11, including the fault twin (a permissive
  lookup DOES succeed where the real guard refuses — the twin flips, proving the guard is
  load-bearing) and the byte-for-byte hand-reconstructed hash comparison.
- The reload-identity bug: reproduced (3 failures, `pytest.raises` not matching), root-
  caused (not guessed — traced to `importlib.reload`'s namespace-replacement semantics),
  fixed, and re-run green.
- Full standing battery (25 files): 498 passed, 9 xfailed (+11, exactly this dispatch's
  addition).
- `./scripts/run_harness.sh --layer 7`: RATCHET PASS, all named checks green.
- `eval/memory_harness.py`: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117,
  MEM-118}` — inside the pin.
- `git show --name-only`/`git status` before and after the guarded commit+push: confirmed
  only this dispatch's own four files landed; the cutover lane's untracked files
  untouched.

**Reasoned about, not independently re-derived:** that a FUTURE `hel=="2.0"` writer
(Segment 4, not built here) will actually use this registry correctly is a design
expectation this segment enables, not something it can itself prove — no `hel=="2.0"`
writer exists yet.

## HASH

Staged for commit: `harness/epistemic_ledger.py` (version-gated `event_hash`),
`eval/test_ledger_hash_versioning.py` (new), `scripts/run_harness.sh` (wired the new
file into the standing batteries), this dispatch doc.

## WHICH SEGMENT NEXT, AND WHY (per instruction — reported before building it)

D-160's own sequence named Segments 2 and 3 as independently parallel-buildable, both
prerequisites for Segment 4 (the v2 writer), neither touching the chain's writer or
reader today. **Recommend Segment 3 (keyed/salted commitment construction) next, not
Segment 2 (the off-ledger payload store) — reversing D-160's own listed order, for a
reason found only after Segment 1's own work:**

- Segment 3 is a small, self-contained crypto primitive (an HMAC-based commitment
  function) with a crisp, narrow acceptance bar: given the same input, it must be
  deterministic; given a keyed/salted construction, a low-entropy input must NOT be
  dictionary-testable against it (a directly testable property, the same shape as this
  segment's own fail-closed tests). It touches no storage, no key lifecycle, no backup
  story — it is closer in kind to Segment 1 than Segment 2 is.
- Segment 2 (the off-ledger payload store) is the LARGER of the two: new per-member key
  management, its own file layout, its own erasure primitive — real design surface D-160
  named but did not resolve (per-member key reuse from `epistemic_ledger.py` itself, or
  a separate keyring; directory layout; whether it reuses `harness.encryption`'s DEK
  pattern or `epistemic_ledger`'s own AES-256-GCM-per-member-key pattern). Building
  Segment 3 first produces the commitment function Segment 2's own design can then
  target concretely (what exactly gets committed, at what size, before deciding how the
  matching payload is stored) rather than designing the store first and discovering the
  commitment doesn't fit what got built.
- Neither segment blocks the other structurally (D-160's own finding stands: both are
  real prerequisites for Segment 4, and only for Segment 4) — this is a sequencing
  preference from having just done Segment 1, not a dependency this survey missed.

**Not proceeding to Segment 3 in this same dispatch** — per instruction, reporting the
proposal and stopping here for Bill's go-ahead before building it.

## OPEN

- **Segment 5 (identifier pseudonymization) is confirmed split out**, per this
  dispatch's own instruction — not touched, not scoped further here.
- **Segment 3 is proposed next, reversing D-160's listed order** — reasoning given
  above; this is a recommendation, not a decision already acted on.
- **New IDs from here mint with the lane prefix** (`D-R-nnn`/`TD-R-nnn`), per the new
  CLAUDE.md item 10 discovered mid-dispatch — this dispatch itself predates having a
  clean number to apply that to (Bill's own instruction had no explicit ID), so it is
  filed under its descriptive slug only; the NEXT dispatch in this sequence should carry
  an explicit `D-R-nnn` number if one is assigned.
- **Nothing ruled MET. A16/A17 unaffected, not re-tiered** — this segment changes no
  observable behavior of the ledger; it is pure hashing infrastructure.

## RECAP
D-R-161 (Segment 1 of the R16/R17 rebuild): `event_hash()` now branches on `hel` version,
via a registry where `"1.0"` maps to the EXACT SAME `_HASH_FIELDS` object used before —
every existing and future v1 event hashes byte-identically, forever, verified by hand-
reconstructing the pre-change computation and matching it exactly. Unknown/missing
versions fail closed (`UnknownLedgerVersion`), proven with an executed fault twin. No
anchor taken to date is affected, and none will be by a future v2 registration either —
the specific property D-89's own compatibility proof depends on. Caught and fixed a real
module-reload identity bug via running the tests, not re-reading them. 498/9 batteries
(+11), `--layer 7` RATCHET PASS, memory harness 13/17 inside pin. Applied the new
CLAUDE.md coordination rules discovered mid-dispatch (lock held only around the git
operation, for both `repo` and `graph` locks). Proposes Segment 3 next (reversing D-160's
own order, reasoned above) — not built, reported first per instruction. A16/A17
unaffected. Nothing ruled.
