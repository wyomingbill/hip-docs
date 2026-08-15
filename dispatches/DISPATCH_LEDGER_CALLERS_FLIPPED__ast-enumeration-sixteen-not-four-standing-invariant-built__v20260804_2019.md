# DISPATCH_LEDGER_CALLERS_FLIPPED
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (flip the remaining v1 write callers to v2) + a standing invariant
replacing a defective enumeration pattern + annotated corrections to two prior
dispatch docs.

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16/R17 (ratified D-71). No amendment, no new REQ doc.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-168 | ~/hip-roadmap, roadmap | Flip the ten missed callers ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: R16/R17 as ratified at D-71.

D-R-167 found ten production write sites still emitting v1 — missed because the
enumerating grep was blind to bare-imported append(...) calls. The "four real callers"
invariant and the whole-system-v2 claim are both wrong until this lands.

1. RE-ENUMERATE BY AST, NOT GREP. A pattern that misses an import style is the defect
   that caused this. Report the true total before flipping anything.
2. FLIP THEM. Name any you do not flip and why.
3. FIX THE STANDING INVARIANT — the exactly-four test is now wrong. Replace it with one
   that counts what actually exists and is derived the same way as the enumeration, so
   the test and the survey cannot disagree again.
4. CORRECT THE RECORD in D-160's and D-R-166's dispatch docs by annotation, not
   rewriting — same discipline used for the docstring and the retirement.
5. THEN STATE THE CLAIM: which paths emit erasable events, which do not, and what HIP
   may honestly say. The two-population limit stands regardless.
6. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
7. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched, tree clean except another lane's own untouched WIP, HEAD in
   sync with `origin/roadmap`.
2. **Built an AST-based scanner, not a grep**, resolving every real way this codebase
   can reach `harness.epistemic_ledger.append()`: cross-module imports (bare-named or
   aliased, `from harness.epistemic_ledger import append`, `from harness import
   epistemic_ledger`, `import harness.epistemic_ledger as X`) and — found only while
   building it, not part of D-R-167's own ten — the ONE same-module case, since
   `epistemic_ledger.py` defines `append` itself and calls it directly, twice, with no
   import at all.
3. Ran the scanner: **16 real production call sites, not 10, not 4** — D-R-167's ten
   plus the 4 already-flipped plus 2 same-module calls this scanner's own first draft
   also missed until read by hand and special-cased.
4. Cross-checked the scanner's own AST nodes for the literal `hel_version` keyword and
   its value, confirming — BEFORE flipping anything — exactly which of the 16 already
   carried `hel_version="2.0"` (4) and which did not (12).
5. Flipped all 12 remaining call sites: `harness/care_team_keys.py` (2),
   `harness/custody_exit.py` (2), `harness/dyad_registry.py` (2),
   `harness/household_keys.py` (3), `harness/ledger_payload_store.py` (1), and
   `harness/epistemic_ledger.py`'s own 2 same-module calls — one keyword argument
   added per call, zero other lines changed per call site.
6. **Investigated, before flipping it, whether `harness/epistemic_ledger.py`'s own
   two same-module calls were safe to flip** — found and reasoned through a real,
   pre-existing latent risk in `_load_or_create_member_key` (silently regenerates a
   key if the file is absent) that would matter ONLY if `destroy_member_key`/
   `erase_payload` were ever called with an actor that IS the subject being
   erased — confirmed this risk is IDENTICAL in v1 and v2 (both paths call the same
   key-loader), confirmed ZERO production callers of either function exist today (only
   tests, all using system/operator actors), and confirmed the flip does not introduce
   or worsen this risk. Named in OPEN, not fixed — out of this dispatch's own scope.
7. Flipping `harness/ledger_payload_store.py`'s own tombstone call meant its OWN
   `payload.erased` audit events became v2-shaped — found this would break
   `harness/erasure_report.py`'s own `_tombstoned()` helper (built D-R-167, reads
   inline `payload`), fixed it to read either shape, renamed it from the
   erasure-specific `_tombstone_payload` to the now-more-accurate, no-longer-private
   `read_event_payload` (reused across multiple event types, not just tombstones).
8. **Found and fixed FOUR real breakages this ripple caused**, each the same shape
   (inline `payload` read on an event that is now v2), each caught by actually running
   the affected code, not assumed safe:
   - `eval/test_hel_smoke.py` checks 3c (`erase_payload`'s own tombstone) and 11d
     (`destroy_member_key`'s own `system.note`)
   - `eval/test_ledger_payload_store.py`'s two audit-event checks
     (`erase_payload_for_event`'s own tombstone)
   - `eval/harnesslib/layer7_crypto_v2.py`'s **live scenario checks RE4 and RE6**
     (`custody.evict`/`key.recovery`/`custody.continuity_gap` payloads) — these are
     the two scenarios that showed as `NEW FAILURES (not in baseline)` on the first
     `--layer 7` run after flipping, caught by running the harness, not by code
     review
   - `eval/harnesslib/layer7_crypto.py`'s DK4 fault-injection check (`custody.grant`
     payload) — NOT currently red (the fault-injected dyad_id never matches
     regardless of whether the payload read succeeds, so this was passing by
     coincidence), fixed anyway rather than left as a landmine that reads the wrong
     field and happens to still work
   All four fixed with the same `read_event_payload` helper, confirmed passing.
9. Built the standing invariant item 3 asked for:
   `eval/test_ledger_callsite_enumeration.py`, embedding the AST scanner as a reusable
   `enumerate_ledger_append_call_sites()` function, plus two separate invariants
   (completeness — the closed, reviewed set by FILE; uniformity — every site carries
   `hel_version="2.0"` on its own AST call node) and two anti-vacuity cases proving the
   scanner catches BOTH defect classes found (bare-imported, same-module).
10. **Retired** `eval/test_ledger_cutover_remaining_callers.py`'s own
    `test_hel_cutover_exactly_four_production_call_sites_carry_hel_version` — the
    literal "exactly-four test" item 3 named — replacing its body with an explanation
    pointing at its replacement, matching the same discipline already used once this
    session (D-R-166 retiring D-R-165's own stale scope test).
11. **Annotated D-160's and D-R-166's own dispatch docs directly**, by insertion, not
    rewrite — three separate annotation blocks (D-160's item 10; D-R-166's item 12 and
    its own item-4 claim; D-R-166's own RECAP) — each quoting the wrong claim's
    location, stating what was actually true, and citing this dispatch. Caught and
    fixed one arithmetic error in my own first draft of these annotations before
    landing them (miscounted how many call sites were still v1 at the moment D-R-166
    made its own flip — 15, not 12; re-derived and fixed both instances before
    committing).
12. Wired the new test file into `scripts/run_harness.sh`'s standing battery list.
13. Ran the full standing battery (32 files) via `scripts/run_harness.sh --layer 7`:
    first pass surfaced `NEW FAILURES (not in baseline): ['L7V2:RE4', 'L7V2:RE6']`;
    fixed (step 8 above); re-ran clean.
14. **RATCHET PASS — no scenario regressed vs baseline.** Confirmed `DK4`/`RE4`/`RE6`
    each explicitly `PASS` in the log, not merely absent from a failures list.
15. Ran the memory harness under the graph lock: **13/17**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — the same pinned set as every prior ledger
    dispatch this session, not a new regression.
16. Wrote this dispatch doc, including item 5's plain claim.
17. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### Item 1 — the true total, by AST, before flipping anything

**16 real production call sites, not 10, not 4.** Two defect classes hid parts of this
count from three prior passes (D-160's own survey, D-R-166's own survey, and this
scanner's OWN FIRST DRAFT):

| Defect class | What it misses | Found by |
|---|---|---|
| Bare-imported call (`from harness.epistemic_ledger import append`, then `append(...)`) | Any grep for `epistemic_ledger.append(` | D-R-167 (10 sites) |
| Same-module direct call (`epistemic_ledger.py` defines `append` and calls it itself, no import) | An import-binding-only AST scan — including this scanner's own untested first draft | This dispatch, while building the scanner (2 sites) |

The full, closed, AST-confirmed list (file: count):
`harness/care_team_keys.py` (2), `harness/custody_exit.py` (2),
`harness/dyad_registry.py` (2), `harness/epistemic_ledger.py` (2, same-module),
`harness/epistemic_record.py` (1), `harness/household_keys.py` (3),
`harness/identity_keys.py` (2), `harness/ledger_payload_store.py` (1),
`scripts/demo_reset.py` (1). **Total: 16.**

Before this dispatch: 4 carried `hel_version="2.0"` (from D-R-165/166), 12 did not.

### Item 2 — flipped, none excluded

All 12 remaining call sites flipped. None were named as unflippable — every one
matched the same shape D-R-166 already established was safe (system or member-kind
actor, `append(event_type, payload_dict, actor=..., correlation=...)`), confirmed
individually by reading each in context before editing, not assumed from the pattern
alone. The two same-module calls inside `epistemic_ledger.py` needed a specific,
separate safety check (see WHAT WAS DONE step 6) before flipping — done, no blocker
found for THIS dispatch's own scope, one pre-existing risk named in OPEN.

### Item 3 — the standing invariant, fixed and now correctly derived

`eval/test_ledger_callsite_enumeration.py` replaces BOTH stale substring-counting
tests this session had already written (D-R-166's own "exactly four", named
explicitly in this dispatch's own ask, and D-R-165's own "only epistemic_record.py
flipped", already retired once by D-R-166 before this correction was even known to be
needed). The new invariant is **derived the same way this dispatch's own survey was**
— the SAME `enumerate_ledger_append_call_sites()` function is both the survey tool
and the test's own source of truth, so a future caller added anywhere in the codebase
changes the completeness check's own count immediately, rather than requiring a
second, independently-maintained enumeration that could drift from whatever a future
survey finds — precisely the failure this whole dispatch exists to close.

### Item 4 — the record corrected, by annotation

Three annotation blocks landed, each in place (quoting the original wrong claim,
explaining what was actually true, citing this dispatch), none of the original
wording deleted:
- `DISPATCH_R16_R17_LEDGER_SURVEY__…v20260804_1026.md` (D-160), item 10's "4" count.
- `DISPATCH_LEDGER_CUTOVER_REMAINING_CALLERS__…v20260804_1918.md` (D-R-166), item 12's
  "exactly 4" scope-check claim, item 4's "every real production write path... v2"
  claim, and the RECAP's own restatement of both.

### Item 5 — the claim, stated plainly

**As of this dispatch, every real production write path in HIP — all 16, the
complete, AST-confirmed, closed set — writes v2.** This is not the same sentence
D-R-166 wrote (which was true of 4 of 16 and did not know it); it is now backed by an
exhaustive enumeration method and a standing test that re-derives the count the same
way, not a hand-maintained list that can silently go stale again.

**Which paths emit erasable events:** all of them, as of their own next write.
Household-turn content (`turn.record`), identity-gate diagnostics
(`identity.rejected`, `identity.speaker_mismatch`), demo-reset audit
(`system.reset`), custody/dyad key events (`custody.grant`, `custody.exit`,
`custody.evict`, `custody.continuity_gap`, `key.recovery`), household-circle events
(`household_circle.grant`, `household_circle.revoke`, `household.key_grant`),
care-team events (`care_team.grant`, `care_team.revoke`), and the ledger's own audit
tombstones (`payload.erased`, the `system.note` for `member.key_destroyed`) — every
one of these event types' content now sits off-ledger from this commit forward, with
only an opaque commitment on-chain.

**Which paths do not:** none, going forward — except the ledger's own internal
`ledger.segment_sealed` marker, unconditionally v1 by design since D-R-164 (carries
no personal or diagnostic content, never in R16's scope).

**What HIP may honestly say now:** *"Every new entry this ledger makes, from any
subsystem, keeps no recoverable content on the immutable chain itself — only an
opaque commitment."* This is now true of the WHOLE live write surface, verifiably so
via the standing invariant, not asserted from an incomplete count.

**What HIP may NOT say, unchanged from D-R-165/166/167:** that any specific fact —
written before or after any of these flips — can be individually erased on request.
The only WORKING erasure mechanisms remain subject-wide key destruction and (for a
single artifact) `erase_payload`/`erase_payload_for_event`, both now provably
verifiable (D-R-167's `harness/erasure_report.py`) but neither wired to any real
per-fact erasure TRIGGER. Segment 6's graph-side operation (DEK destruction, row
`DELETE`, embedding removal against real `:Fact` data) still does not exist.

**The two-population limit stands, unchanged, exactly as D-R-165/166/167 already
established — this dispatch does not narrow it, only widens which paths reach the v2
side of it going forward.** Every event written before ITS OWN respective call site's
flip lands remains v1 permanently, unmigratable, for the same anchor-compatibility
reason proven at D-R-165. Twelve more paths just gained their own cutover moment, each
distinct, none retroactive.

## VERIFIED

**Watched, executed:**
- The AST scanner itself run standalone, cross-checked against every call site's
  actual keyword arguments (not just presence/absence of the call) before any edit
  was made.
- Direct reads of all 12 flipped call sites, in context, before editing each.
- The `_load_or_create_member_key` self-regeneration risk investigated by reading the
  actual function bodies (`_encrypt_payload`, `_build_event_v2`) and by grepping for
  every real caller of `destroy_member_key`/`erase_payload` (both zero production
  callers today, confirmed).
- `eval/test_ledger_callsite_enumeration.py`: 4/4 on first run.
- Full ledger test suite (10 files) run together in the OFFICIAL battery order: 576
  passed, 9 xfailed (an earlier, differently-ORDERED ad hoc combination produced 4
  unrelated `test_ledger_commitment.py` failures traced to test-pollution from running
  files in a non-standard order, not a real regression — confirmed by running that
  file alone, 17/17, and by running the exact official order, clean).
- `scripts/run_harness.sh --layer 7`: first pass surfaced 2 real new failures
  (`RE4`, `RE6`), fixed, re-ran clean; **RATCHET PASS**; `DK4`/`RE4`/`RE6` each
  individually confirmed `PASS` in the log.
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
- Both annotation math errors caught by re-deriving the before/after counts for each
  of D-R-165/166/167/168 methodically, not trusted from the first draft.

**Reasoned about, not independently re-derived:** whether any file OUTSIDE this
codebase's own `.py` sources (e.g., a shell script or notebook) could also call
`epistemic_ledger.append()` was not checked — the scanner covers every `.py` file in
the repository, which this project's own architecture makes the complete surface (no
non-Python write path exists), but that assumption itself was not independently
audited here.

## HASH

Staged for commit: `harness/care_team_keys.py`, `harness/custody_exit.py`,
`harness/dyad_registry.py`, `harness/epistemic_ledger.py`, `harness/household_keys.py`,
`harness/ledger_payload_store.py`, `harness/erasure_report.py` (rename +
generalization), `eval/test_hel_smoke.py`, `eval/test_ledger_payload_store.py`,
`eval/test_ledger_cutover_remaining_callers.py` (retirement), `eval/harnesslib/
layer7_crypto.py`, `eval/harnesslib/layer7_crypto_v2.py`, `eval/
test_ledger_callsite_enumeration.py` (new), `scripts/run_harness.sh`,
`docs/dispatches/DISPATCH_R16_R17_LEDGER_SURVEY__…v20260804_1026.md` (annotated),
`docs/dispatches/DISPATCH_LEDGER_CUTOVER_REMAINING_CALLERS__…v20260804_1918.md`
(annotated), this dispatch doc.

## OPEN

- **A pre-existing latent risk in `_load_or_create_member_key`**, found while
  checking this dispatch's own two same-module flips were safe, not introduced by
  them: if `destroy_member_key`/`erase_payload` were ever called with an actor that
  IS the subject being erased, the erasure's own audit event would silently
  regenerate a fresh key for that same subject. Identical in v1 and v2 (both paths
  share the same key-loader); zero production callers of either function exist today.
  Not fixed — out of this dispatch's own scope, named so it is not rediscovered from
  zero when either function gains a real caller.
- **Segment 6's graph-side operation (DEK destruction, row `DELETE`, embedding
  removal against real `:Fact` data) remains fully unbuilt** — D-160's own finding,
  unchanged through D-R-167 and this dispatch. Genuinely destructive; needs Bill's
  explicit authorization before any dispatch attempts it.
- **Subject-wide erasure reporting is still not covered** by D-R-167's
  `harness/erasure_report.py` — named there, unchanged here.
- **Whether any non-`.py` write path exists was reasoned about, not independently
  audited** — see VERIFIED.
- **Nothing ruled MET.**

## RECAP
D-R-168: re-enumerated every real caller of `epistemic_ledger.append()` by AST, not
grep — the exact defect class that hid D-R-167's own ten missed callers. **The true
total was 16, not 10, not 4** — this dispatch's own first-draft scanner ALSO missed 2
same-module calls inside `epistemic_ledger.py` itself (no import needed, since
`append` is defined there), found only by reading the file, not by any pattern.
Flipped all 12 remaining call sites, after checking a pre-existing (not
newly-introduced) latent key-regeneration risk in the two same-module cases and
confirming it doesn't apply (zero production callers of either function exist).
Flipping `ledger_payload_store.py`'s own tombstone call rippled into 4 real
breakages — two pytest files, and, caught by actually running `--layer 7` rather
than assumed safe, two LIVE harness scenarios (`RE4`, `RE6`) — all four fixed with
one shared v1/v2-aware helper (`harness.erasure_report.read_event_payload`), plus one
more (`DK4`) fixed pre-emptively though not yet red. Built the standing invariant
item 3 asked for (`eval/test_ledger_callsite_enumeration.py`), deriving its own count
the SAME way this dispatch's own survey did, so the test and any future survey cannot
silently diverge again — retiring D-R-166's own now-wrong "exactly four" test in the
process. **Corrected D-160's and D-R-166's own dispatch docs by annotation, in
place** — three blocks, one arithmetic error caught and fixed in my own first draft
before landing. The plain claim: all 16 real production write paths in HIP now
produce v2 events — the honest claim D-R-166 could not yet make. Erasure itself is
still unchanged: subject-wide key destruction and per-artifact erasure both work and
are now verifiable, but no per-fact erasure TRIGGER exists, and the two-population
limit stands exactly as before, now simply covering more paths' own future writes.
576+4/9 batteries green, RATCHET PASS (RE4/RE6/DK4 individually confirmed), memory
harness 13/17 at the same pinned failing set. Nothing ruled MET.
