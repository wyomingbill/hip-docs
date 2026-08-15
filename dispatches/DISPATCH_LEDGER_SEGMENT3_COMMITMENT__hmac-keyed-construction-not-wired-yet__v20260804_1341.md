# DISPATCH_LEDGER_SEGMENT3_COMMITMENT
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (Segment 3 of the R16/R17 rebuild D-160 proposed, reordered ahead of
Segment 2 per D-R-161's own recommendation)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16 (ratified D-71) — no amendment, no new REQ doc, same posture as Segment 1.

## THE ASK

Bill's instruction, verbatim: **"Go ahead with Segment 3."** — approving
`docs/dispatches/DISPATCH_LEDGER_SEGMENT1_VERSION_GATING__…v20260804_1106.md` (D-R-161)'s
own proposal to build Segment 3 (keyed/salted commitment construction) next, reversing
D-160's originally listed order.

## WHAT WAS DONE

1. Gate checked — matched. Pulled clean (fast-forward through `ef99a9c`, D-162's
   completion-alert script, and `a5ef735`, another lane's `REQ_UNRESOLVED_SUBJECT_GUARD`
   amendment) before starting, no lock held during the pull or the build/test work that
   followed — matching the new item 9 discipline this dispatch continues to apply.
2. Designed and built `harness/ledger_commitment.py`: `compute_keyed_commitment(payload,
   *, key: bytes) -> str` (HMAC-SHA256 over the same `_canon()` serialization
   `epistemic_ledger.py` already uses for `payload_sha256` — one canonicalization
   convention, not a second one) and `verify_keyed_commitment(...)` (constant-time
   comparison via `hmac.compare_digest`, never raises). Deliberately narrow, per D-R-161's
   own reasoning: the key is a caller-supplied parameter; this module does not decide
   whose key or where it lives (Segment 2's own question, still unbuilt) or wire into
   `epistemic_ledger.py` at all (Segment 4's job).
3. `MIN_KEY_BYTES = 32`, reused from — not invented alongside —
   `epistemic_ledger._load_or_create_member_key`'s own `os.urandom(32)` convention.
   `WeakCommitmentKey` (fail-closed, the R29/D-105 pattern) refuses any shorter key rather
   than silently accepting a weak one.
4. Verified the construction directly before writing tests: deterministic for the same
   (payload, key), key-sensitive, differs in shape from plain SHA256
   (`"hmac-sha256:"` vs `"sha256:"` prefixes), verify round-trips correctly and rejects a
   wrong key/tampered payload/malformed string.
5. Wrote `eval/test_ledger_commitment.py`: determinism, key-sensitivity across both
   payload and key, a dictionary-attack simulation giving the attacker every advantage
   except the key (exact canonicalization, exact HMAC construction, the correct value
   INSIDE the guessed dictionary) and proving none of it matches without the key, a
   distinct-construction check against `epistemic_ledger._sha256` directly, full
   `verify_keyed_commitment` coverage (true/false/malformed-never-raises), weak-key
   refusal (parametrized: empty, 5 bytes, 31 bytes — one short of the floor), an
   AST-verified cross-check that `MIN_KEY_BYTES` still matches a REAL `os.urandom(32)`
   call site in `epistemic_ledger.py` (so the two cannot silently drift apart), an
   executed fault twin (a key-ignoring construction passes determinism but fails
   key-sensitivity, proving the real test isn't vacuous), and anti-vacuity (the key
   never leaks into the commitment string).
6. Ran the file standalone: 17/17 passed on the first run, no fixups needed.
7. Wired `eval/test_ledger_commitment.py` into `scripts/run_harness.sh`'s standing
   battery list, alongside Segment 1's own test file.
8. **Ran `--layer 7` and got a real, unexpected FAIL**: `NEW FAILURES (not in baseline):
   ['L7V2:MUTATION-NO-SILENT-DISAPPEARANCE']`, naming 16 unaccounted disappearances in
   `harness/injection_contract.py`'s own mutation-survivor list — a file this dispatch
   never touched. **Did not proceed past this without understanding it.** Investigated
   rather than re-run blind:
   - Confirmed `harness/injection_contract.py` was last committed at D-127 (2026-08-01),
     nothing in this session's own window.
   - Found `logs/mutation_survivors.jsonl` (the persisted baseline this check compares
     against) is gitignored and untracked — a SHARED, LOCAL, UNLOCKED file in this same
     checkout, which multiple concurrent sessions have now been confirmed to share
     (`b6a7f63`, `f585443`'s own coordination-rule text, `ef99a9c`, `a5ef735` all landed
     in this exact working tree during this session's own window).
   - Re-ran `--layer 7` immediately, unchanged, under the graph lock held only for the
     run itself: **RATCHET PASS**, clean, no disappearances.
   - **While preparing to file a TD for this, found another lane had ALREADY filed
     `TD-R-161` in the same register, for a MORE PRECISE, CONFIRMED diagnosis of what is
     very likely the SAME EVENT**: a concurrent session (their own "Index Demo 14/15")
     built and then reverted `REQ_UNRESOLVED_SUBJECT_GUARD`, which included a six-line
     docstring addition to `harness/injection_contract.py` that shifted the INJ-7
     refusal condition from `:664` to `:670` — a TD-142 recurrence (hardcoded
     line-number addressing in `eval/harnesslib/mutation_targets.py`), not a
     baseline-persistence race as this dispatch first hypothesized. **Verified directly**:
     `harness/injection_contract.py:664` currently reads `if (member_ids is not None`
     (the correct, expected line) and `git status` on the file is clean — consistent with
     their account of having reverted it before this dispatch's second run.
   - **Did not file a competing or redundant TD.** Drafted one, then deleted it
     (uncommitted, never pushed) once TD-R-161's own, better-evidenced explanation was
     found — citing theirs here instead of asserting a weaker hypothesis as fact.
9. Ran the full standing-battery list (26 files now): 515 passed, 9 xfailed.
10. Re-ran `./scripts/run_harness.sh --layer 7` a second time (see item 8): AUDIT 8/8,
    L7 27/27, L7V2 27/28, SCHEMA 1/1, VOICE 1/1, RATCHET PASS.
11. Ran `eval/memory_harness.py` under the graph lock, held only for the run itself:
    13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
12. Wrote this dispatch doc.
13. Staged by explicit pathspec; committed AND pushed as one lock-guarded command
    (item 9's own discipline), lock held only for that sequence's actual duration.

## WHAT WAS FOUND

### The commitment construction, proven directly

`compute_keyed_commitment` is deterministic, genuinely key-sensitive (two different
keys never collide on the same payload), and demonstrably resists the SPECIFIC attack
R16 names: a dictionary attacker who knows the exact canonicalization scheme, the exact
HMAC construction, and has the correct value INSIDE their candidate list still cannot
produce a match without the key — proven by executing that attack against the real
function, not by asserting HMAC's textbook properties. This closes the gap D-160's own
survey named (finding 4: today's `payload_sha256`/`hash` are plain, unsalted SHA256).

### The `--layer 7` failure — a real coordination gap, not a defect in this build

This dispatch's own code introduced ZERO risk of the observed failure — `harness/
ledger_commitment.py` and its test file touch nothing `injection_contract.py`'s
mutation sweep scores. The failure was environmental: a concurrent session, sharing
this exact checkout, temporarily shifted line numbers in a file this dispatch never
opened, and the shared, unlocked, gitignored persisted-survivor file briefly reflected
that shift. **Already filed as `TD-R-161` by the lane that traced the precise cause** —
this dispatch adds no new filing, only independent corroboration: the re-run passing
clean, and the file's current line 664 matching the reverted, correct state.

## VERIFIED

**Watched, executed:**
- `harness/ledger_commitment.py` probed directly (determinism, key-sensitivity, shape,
  verify round-trip, weak-key refusal) before any test was written.
- `eval/test_ledger_commitment.py`: 17/17 on first run.
- Combined standing battery (26 files): 515 passed, 9 xfailed.
- `--layer 7`: FIRST run — real, logged FAIL (`L7V2:MUTATION-NO-SILENT-DISAPPEARANCE`,
  16 named disappearances). SECOND run, immediately after, unchanged code: RATCHET
  PASS. Both attempts reported, not just the passing one.
- `harness/injection_contract.py:664` read directly, post-investigation: matches the
  expected, un-shifted line. `git status` on the file: clean.
- `eval/memory_harness.py`: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117,
  MEM-118}`.
- `git show --name-only`/`git status` before and after the guarded commit+push:
  confirmed only this dispatch's own files landed.

**Reasoned about, not independently re-derived:** that this dispatch's own first
`--layer 7` failure and `TD-R-161`'s own traced event are THE SAME occurrence is
inference from timing and symptom match (identical file, identical check, a
now-reverted state matching their account) — not independently proven by, for example,
inspecting the other session's own transcript. Stated as "very likely," not certain.

## HASH

Staged for commit: `harness/ledger_commitment.py` (new), `eval/test_ledger_commitment.py`
(new), `scripts/run_harness.sh` (wired the new file), this dispatch doc. No techdebt
register touched — the draft filing was deleted before commit, per WHAT WAS DONE item 8.

## WHICH SEGMENT NEXT, AND WHY

**Segment 2 (the off-ledger payload store)** is next in D-160's own sequence, and this
dispatch does not find a reason to reorder further: Segment 3's own commitment function
is now the concrete target D-R-161 argued Segment 2's design needed — the store's own
erasure primitive can reuse `epistemic_ledger.destroy_member_key`'s established
per-member AES-256-GCM pattern (matching this codebase's own "reuse the proven
mechanism" discipline, `ledger_commitment.py`'s own docstring already states this
intention), and the commitment size/shape (`"hmac-sha256:" + 64 hex chars`, fixed) is
now known rather than guessed. **Not built here** — reported before building, per the
same standing instruction D-R-161 followed.

## OPEN

- **`TD-R-161`** (filed by another lane, not this dispatch) is the standing record of
  the `--layer 7` failure this dispatch hit and re-ran clean — cited, not duplicated.
- **`TD-142`'s own recurrence, now twice** (D-101/D-102's original instance, and this
  one) — the durable fix (an anchor comment, AST-located predicate, or content hash,
  per TD-142's own three named options) remains scoped, not built. Not this dispatch's
  scope to build.
- **Segment 2 is next**, per D-160's own sequence, no further reordering found
  necessary.
- **Nothing ruled MET. A16/A17 unaffected, not re-tiered** — this segment is an
  unwired primitive; no observable ledger behavior changed.

## RECAP
D-R-162 (Segment 3): built `harness/ledger_commitment.py` — HMAC-SHA256 keyed
commitments, closing R16's own named gap (today's plain SHA256 can be dictionary-tested;
this cannot, proven by executing the attack itself, not asserting HMAC's textbook
property). 32-byte key floor reused from the ledger's own existing per-member key
convention, fail-closed on anything weaker. 17/17 new tests, an executed fault twin, and
an AST cross-check keeping the key-size constant tied to its real source. Hit a REAL
`--layer 7` failure mid-dispatch (`MUTATION-NO-SILENT-DISAPPEARANCE`), investigated
rather than re-run blind, traced it to a concurrent session's own build/revert cycle —
found another lane had already filed the precise diagnosis as `TD-R-161` and cited it
rather than filing a redundant, weaker one. Re-run clean, both attempts reported. 515/9
batteries, memory harness 13/17 inside pin. Segment 2 proposed next, no further
reordering. Not wired into the ledger yet — Segment 4's job. A16/A17 unaffected. Nothing
ruled.
