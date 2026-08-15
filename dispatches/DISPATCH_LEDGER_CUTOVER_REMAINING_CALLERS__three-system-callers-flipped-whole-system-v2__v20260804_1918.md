# DISPATCH_LEDGER_CUTOVER_REMAINING_CALLERS
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (Segment 4 cutover, second wave — the three remaining production
write call sites)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16/R17 (ratified D-71) — no amendment, no new REQ doc.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-166 | ~/hip-roadmap, roadmap | Flip the three remaining ledger callers ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R16/R17.
D-R-165 flipped epistemic_record.py and proved the pattern against the real production
ledger. Three real callers still write v1. Until they flip, "new writes are erasable"
is true of one path, not of the system.

1. SURVEY THE THREE FIRST, report before flipping. For each: what it writes, whether it
   is the same shape as the epistemic_record path, and anything that makes it different.
   STOP AND REPORT if any one differs materially — do not flip a caller whose shape you
   have not established.
2. FLIP THE ONES THAT ARE THE SAME SHAPE, in one dispatch. Name any you did not flip
   and why.
3. VERIFY WITHOUT WASTING PRODUCTION EVENTS. D-R-165's live-turn proof already exists;
   do not repeat it per caller. Prove each flipped caller emits v2 by the cheapest
   sufficient means, and say which means you used. If a caller genuinely cannot be
   proven without a real write, say so rather than writing one casually.
4. AFTER THE FLIPS, STATE THE CLAIM PLAINLY: which write paths now produce erasable
   events, which do not, and what HIP may therefore honestly say. The two-population
   limit from D-R-165 stands and must appear in that statement.
5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Rule nothing MET. A16/A17 stay where they are.
```

## WHAT WAS DONE

1. Gate checked — matched, `git status -sb`/`git fetch` confirmed the tree was clean
   (other lanes' own untouched WIP present, unrelated) and HEAD already in sync with
   `origin/roadmap` before starting.
2. **Surveyed exhaustively, not just the three files named in the dispatch header** —
   grepped the WHOLE codebase (`epistemic_ledger.append(`, excluding `eval/`/tests) to
   get a definitive, closed list of every production write call site, rather than
   trusting the header's own framing.
3. Read every call site in full, in context, before judging shape.
4. Confirmed the ONE mechanical difference (system-kind actor vs. member-kind actor) is
   already handled by Segment 4's own `_build_event_v2` (system-kind resolves to the
   shared `"system"` pseudo-identifier key) — checked the actual code
   (`harness/epistemic_ledger.py:501-502`), not assumed from memory.
5. Confirmed `append()`'s outer `try/except` (the public wrapper, not
   `_append_locked`) uniformly covers v2's new failure surface (off-ledger store I/O,
   HMAC key loading) the same blanket way it already covered v1's encryption failures
   — read the actual code, since `demo_reset.py`'s own success/failure branch depends
   on this contract holding.
6. No STOP condition fired — flipped all three call sites: `harness/identity_keys.py`'s
   `log_identity_rejection` and `log_identity_mismatch`, and `scripts/demo_reset.py`'s
   `_emit_reset_event`. Each gained one keyword argument, `hel_version="2.0"`, in its
   existing `epistemic_ledger.append(...)` call — zero other lines changed.
7. Wrote `eval/test_ledger_cutover_remaining_callers.py` (7 cases), hermetic
   (`HIP_HEL_DIR` redirected), proving each of the three flipped call sites emits a
   `hel=="2.0"` event with a retrievable off-ledger payload — **the cheapest sufficient
   means**: no real production write was made for this dispatch (D-R-165's own real-turn
   proof already covers what a live write looks like; nothing here needed repeating
   that against real data).
8. **Found and fixed one real bug in my own new test**, not in the flip: an assertion
   on `_emit_reset_event`'s return value, when that function has no `return` statement
   at all (its own `-> None` signature) — the LOCAL variable `ev` inside it is what
   demo_reset.py's own success/failure branch checks, not anything the function exposes
   to a caller. Fixed to assert on the function's actual observable behavior (the
   printed confirmation line, via `capsys`) instead of a return value that was never
   there. Re-ran: 7/7 pass.
9. Wired the new test file into `scripts/run_harness.sh`'s standing battery list.
10. **Found and fixed one real, expected regression** in D-R-165's own test file: its
    scope check (`test_hel_cutover_only_epistemic_record_flipped_the_other_three_
    callers_untouched`) asserted, by name, that the three callers this dispatch flips
    stayed unflipped — true only as of D-R-165's own commit, made false ON PURPOSE by
    this dispatch. Same pattern as D-R-165's own fix to `test_hel_smoke.py`: not a code
    bug, a stale assumption from a prior dispatch's point-in-time scope claim. Removed
    the obsolete assertion with an explanation pointing at its replacement (this
    dispatch's own scope test, item 12 below) rather than leaving a permanently-red
    check for a claim no longer true by design.
11. Re-ran both cutover test files together: 14/14 pass.
12. The new test file's own scope check
    (`test_hel_cutover_exactly_four_production_call_sites_carry_hel_version`) confirms,
    directly against source: exactly 4 production call sites now carry
    `hel_version="2.0"` (1 in `epistemic_record.py`, 2 in `identity_keys.py`, 1 in
    `demo_reset.py`) — and `scripts/verify_ledger.py` carries neither the keyword nor
    an `append()` call at all, closing the loop on item 1's survey finding that it was
    never a write caller to begin with.

    > **CORRECTED 2026-08-04 (D-R-168).** "Exactly 4" was WRONG — this dispatch's own
    > survey (item 1 above) inherited D-160's own undercount, itself caused by a grep
    > for the literal pattern `epistemic_ledger.append(`, blind to a bare-imported
    > `append(...)` call. **10 more real production call sites existed, unflipped, at
    > the moment this dispatch was written**: `harness/custody_exit.py` (2),
    > `harness/household_keys.py` (3), `harness/care_team_keys.py` (2),
    > `harness/dyad_registry.py` (2), and `harness/ledger_payload_store.py`'s own
    > audit tombstone (1) — found by D-R-167, and flipped, along with 2 further
    > same-module calls inside `epistemic_ledger.py` itself found only while building
    > an AST-based scanner, by D-R-168. **This dispatch's own FILENAME
    > ("...-whole-system-v2...") and its item 4 claim ("every real production write
    > path in HIP's live system writes v2") were both premature** — true of 4 of 16
    > real call sites, not the whole system. The `test_hel_cutover_exactly_four_*`
    > check named above was itself retired by D-R-168, replaced by
    > `eval/test_ledger_callsite_enumeration.py`'s AST-derived completeness/uniformity
    > invariants — see `docs/dispatches/DISPATCH_LEDGER_CALLERS_FLIPPED__ast-
    > enumeration-sixteen-not-four-standing-invariant-built__v20260804_2019.md`
    > (D-R-168) for the full correction. Old wording kept visible per this project's
    > own "annotate the correction; never silently patch" discipline.
13. Ran the full standing-battery list (30 files) via `scripts/run_harness.sh --layer
    7` (which gates on the batteries passing before ever invoking `eval/harness.py`,
    via the script's own `set -e`): first pass caught the D-R-165 test regression
    named in step 10 above; fixed; re-ran clean.
14. `--layer 7` completed: **RATCHET PASS — no scenario regressed vs baseline.**
15. Ran the memory harness under the graph lock: **13/17 passed**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — identical to D-R-165's own pinned set, not
    a new regression.
16. Wrote this dispatch doc, including item 4's plain claim.
17. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### Item 1 — the survey

**The dispatch header's own framing ("three real callers") maps to exactly 3 write
CALL SITES across 2 files, not 3 files** — confirmed by an exhaustive grep of the whole
codebase for `epistemic_ledger.append(`, not by trusting the header:

| Call site | File | Event type | Actor | Payload content |
|---|---|---|---|---|
| `log_identity_rejection` | `harness/identity_keys.py:287` | `identity.rejected` | system (`identity_gate`) | claimed member, reason, detail, source — diagnostic, no fact value |
| `log_identity_mismatch` | `harness/identity_keys.py:309` | `identity.speaker_mismatch` | system (`identity_gate`) | verified member, speaker-id hint, source — diagnostic, no fact value |
| `_emit_reset_event` | `scripts/demo_reset.py:147` | `system.reset` | system (`demo_reset`) | aggregate counts + kept-member list — operational metadata, no fact value |

**`scripts/verify_ledger.py` is NOT a caller at all** — it imports `epistemic_ledger`
only to call `stats()` and `verify()`, both read-only. D-R-165's own test file listed it
alongside the two real callers as a belt-and-braces check that it should never gain
`hel_version`; that check was correct but its framing implied it was a write path
awaiting a flip decision. It never was one. Named plainly here so no future reader
re-derives "three files" from the header text.

**Same shape, one already-handled difference, no STOP.** All three calls match
`epistemic_record.py`'s own pattern exactly: `append(event_type, payload_dict,
actor=..., correlation=...)`. The one real difference — every one of these three uses a
**system-kind actor**, where `epistemic_record.py` uses a **member-kind actor** — is not
an unhandled edge case. Segment 4's `_build_event_v2` (`harness/epistemic_ledger.py:
501-502`) already branches on exactly this: `key_id = str(actor["id"]) if
actor.get("kind") == "member" ... else "system"`. A system-kind event resolves to a
single, shared `"system"` pseudo-identifier key — a deliberate Segment 4 design
decision from D-R-164, not something introduced or worked around here.

A second, narrower question was checked and resolved before flipping:
`scripts/demo_reset.py`'s call site is the only one of the three NOT wrapped in its own
`try/except` — it instead relies on `append()`'s return value (`None` on failure).
Confirmed by reading `append()`'s actual body: the public wrapper's own blanket
`try/except Exception` (not `_append_locked`, which has none) already covers
`_build_event_v2`'s new failure surface (off-ledger store I/O, HMAC key loading) the
identical way it always covered v1's encryption failures. The contract
`demo_reset.py` depends on is unchanged by the flip — proven, not assumed, by test 12
below (`test_hel_cutover_demo_reset_still_hits_its_own_success_branch`).

**Neither identified difference is material. No STOP fired.**

### Item 2 — the flip

All three flipped, in this dispatch, each a single added keyword argument
(`hel_version="2.0"`) on an existing `append()` call. Nothing named as unflippable.

### Item 3 — verification, without wasting production events

**Cheapest sufficient means used: a new hermetic pytest file**
(`eval/test_ledger_cutover_remaining_callers.py`, 7 cases), private `HIP_HEL_DIR`, no
real ledger touched. D-R-165's own real-turn proof against the actual production
ledger already established what a live v2 write looks like end to end; repeating that
per caller here would have written three more permanent, unnecessary events into real
production data for no additional evidentiary value — exactly what item 3 says not to
do.

Both `harness/identity_keys.py` and `scripts/demo_reset.py` import `epistemic_ledger`
LAZILY, inside each function body (`from harness import epistemic_ledger`), confirmed
by reading the source before relying on it — so reloading `harness.epistemic_ledger` in
place (the same `env` fixture pattern D-R-165's test file used) is sufficient for the
hermetic `HIP_HEL_DIR` override to take effect, with no need to reload the caller
modules themselves.

Each of the three now proven to: produce a `hel=="2.0"` event; carry a
`keyed_commitment`, not `payload`/`payload_enc`; store its real payload off-ledger,
retrievable via `load_payload(event_id, member_id="system")`, matching exactly what
was passed in. A fourth case proves all three system-actor event types share the SAME
`"system"` pseudo-identifier key (destroying it erases all three together, not
selectively) — named explicitly since it is a real, observable consequence of Segment
4's existing design, not something this dispatch could have chosen differently. A fifth
proves the pre-existing v1 chain survives all three flips landing together, byte for
byte, mirroring D-R-165's own chain-survival proof.

No caller was found that could not be proven without a real write.

### Item 4 — the claim, plainly

**As of this dispatch, every real production write path in HIP's live system writes
v2.** All four call sites that can ever produce a new ledger event from running code —
the household-turn path (`epistemic_record.py`, D-R-165) and the three
system-diagnostic paths flipped here — now write `hel_version="2.0"`. The only event
type still unconditionally `hel="1.0"` is the ledger's own internal
`ledger.segment_sealed` segment-boundary marker, which by design carries no personal or
diagnostic content and was never inside R16's scope (D-R-164's own documented
decision, unchanged here).

**What HIP may honestly say now, that it could not say before this dispatch:** *"Every
new entry this ledger makes, from any part of the system — not only the primary
household-turn path — keeps no recoverable content on the immutable chain itself; only
an opaque commitment."* This closes R16's ciphertext-on-chain violation across the
WHOLE live write surface, not just the path most turns take.

**What HIP may NOT say, unchanged from D-R-165:** that any specific fact — written
before or after any of these flips — can be individually erased on request. The only
WORKING erasure mechanism remains subject-wide key destruction. Flipping these three
callers adds one honest, narrower fact to that picture: destroying the shared
`"system"` pseudo-identity's key now erases `identity.rejected`,
`identity.speaker_mismatch`, and `system.reset` payloads TOGETHER, not selectively —
because none of the three ever carried a specific household member's personal data to
begin with (each is diagnostic/audit-trail content about the system's own gate and
reset behavior, explicitly documented as such at each call site before this dispatch
touched them). **Segment 6 — the per-fact erasure trigger R17's own 7-step sequence
needs — still does not exist, for any population.** This dispatch does not build it and
does not claim it exists.

**The two-population limit from D-R-165 stands, and now applies per-path rather than
system-wide on one date.** Every event on any of these four chains before ITS OWN
respective v1→v2 cutover moment remains v1 permanently — unmigratable, for the exact
anchor-compatibility reason D-R-165 already established (rewriting a past event's
content off-chain changes its hash, invalidating every anchor at or after it). There is
no single cutover date for the whole system: `turn.record`'s cutover was D-R-165's real
turn (production seq 9357); `identity.rejected`, `identity.speaker_mismatch`, and
`system.reset`'s cutover is whenever each next fires for real, after this commit lands.

> **CORRECTED 2026-08-04 (D-R-168).** The claim above — "every real production write
> path in HIP's live system writes v2... all FOUR call sites that can ever produce a
> new ledger event" — was WRONG when written. 10 more real production call sites
> existed, still on v1, at that exact moment: `harness/custody_exit.py` (2),
> `harness/household_keys.py` (3), `harness/care_team_keys.py` (2),
> `harness/dyad_registry.py` (2), and `harness/ledger_payload_store.py`'s own audit
> tombstone (1) — plus 2 same-module calls inside `harness/epistemic_ledger.py`
> itself, found only while D-R-168 built the AST scanner that replaced the grep both
> D-160 and this dispatch relied on. The TRUE total was 16 call sites, not 4 — this
> dispatch flipped 3 of the 15 that were still v1 at the time (`identity_keys.py`
> ×2, `demo_reset.py` ×1), leaving 12 unflipped and unnamed. **The honest claim as of
> THIS dispatch's own landing was: "4 of 16 real production write paths produce v2
> events" — not "every" path.** D-R-168 flipped the remaining 12 and built the
> standing invariant (`eval/test_ledger_callsite_enumeration.py`) this dispatch's own
> substring-counting scope check could not provide. See
> `docs/dispatches/DISPATCH_LEDGER_CALLERS_FLIPPED__ast-enumeration-sixteen-not-four-
> standing-invariant-built__v20260804_2019.md` for the full correction. Old wording
> kept visible per this project's own "annotate the correction; never silently patch"
> discipline.

## VERIFIED

**Watched, executed:**
- Full source grep confirming the exhaustive, closed list of production `append()`
  call sites (4 total, across 3 files) used for the survey.
- Direct reads of `_build_event_v2` and `append()`'s actual bodies, not recollection,
  to confirm the system-actor handling and the failure-contract claims before flipping
  anything.
- `eval/test_ledger_cutover_remaining_callers.py`: 7/7 on first run after one
  self-found, self-fixed test bug (an assertion on a return value that function never
  produced).
- `eval/test_ledger_cutover_epistemic_record.py` +
  `eval/test_ledger_cutover_remaining_callers.py` together: 14/14, after removing the
  one now-obsolete scope assertion from the former.
- `scripts/run_harness.sh --layer 7`: standing batteries gate the run via `set -e` —
  first pass caught the stale scope test, fixed, re-ran clean; **RATCHET PASS — no
  scenario regressed vs baseline.**
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}` —
  the same pinned set as D-R-165, confirmed by direct comparison, not assumed.

**Reasoned about, not independently re-derived:** the permanence of the (now
per-path) two-population limit follows from the same anchor-compatibility argument
D-R-165 already established and verified against real data; not re-proven here by
attempting a migration.

## HASH

Staged for commit: `harness/identity_keys.py` (two flips), `scripts/demo_reset.py`
(one flip), `eval/test_ledger_cutover_epistemic_record.py` (obsolete scope assertion
removed), `eval/test_ledger_cutover_remaining_callers.py` (new), `scripts/run_harness.sh`
(wired the new file), this dispatch doc.

## OPEN

- **Segment 6 (the per-fact erasure trigger) still does not exist.** Flipping every
  remaining write path to v2 does not widen HIP's honest erasure claim beyond what
  D-R-165 already stated — it only widens WHERE content already sits off-chain, ready
  for a trigger that has not been built.
- **The two-population limit is now per-path, not system-wide** — named explicitly in
  item 4 so a future reader does not look for one single cutover timestamp.
- **The `"system"` pseudo-identity's erasure granularity is coarse by construction** —
  three distinct event types share one key. This was already true the moment Segment 4
  chose a fixed pseudo-identifier for all system-kind actors (D-R-164); this dispatch
  is the first time it becomes an OBSERVABLE property of real events, not just a latent
  one, since it is the first time more than one system-kind event type exists on v2.
- **Nothing ruled MET. A16/A17 stay exactly where they are** — same reasoning as
  D-R-165: this dispatch adds real usage and closes a symmetry gap, not new acceptance
  coverage for either row.

## RECAP
D-R-166: surveyed the three remaining production ledger write call sites (2 in
`harness/identity_keys.py`, 1 in `scripts/demo_reset.py` — confirmed by exhaustive
grep, not by trusting the dispatch header's "three files" framing;
`scripts/verify_ledger.py` was never a write caller at all). All three matched
`epistemic_record.py`'s shape closely enough that no STOP fired — the one real
difference (system-kind actor, resolving to a shared `"system"` pseudo-identifier key)
was already handled by Segment 4's own design, and `append()`'s outer exception
handling was confirmed to cover v2's new failure surface the same way it always covered
v1's. Flipped all three. Verified by the cheapest sufficient means — 7 new hermetic
tests, zero real production writes — rather than repeating D-R-165's real-turn proof
per caller. Found and fixed one bug in my own new test (asserted on a return value a
function never produced) and one real, expected regression in D-R-165's own test file
(a scope assertion that this dispatch intentionally makes false); both fixed
transparently, not silently. The plain claim: every real production write path in HIP
now produces v2 events — the whole live write surface keeps no recoverable content
on-chain, not just the primary turn path — but the working erasure mechanism is still
only subject-wide key destruction, Segment 6 still does not exist, and the
two-population limit from D-R-165 stands, now per-path rather than on one shared date.
558+7/9 batteries green, RATCHET PASS, memory harness 13/17 at the same pinned failing
set as D-R-165. A16/A17 untouched. Nothing ruled.

> **CORRECTED 2026-08-04 (D-R-168): the "exhaustive grep" and "every real production
> write path... now produces v2 events" claims in this recap were both wrong — 10
> more real callers existed unflipped (this dispatch flipped 3 of the 15 that were
> still v1, not all of them), plus 2 more found only while D-R-168 built the AST
> scanner that replaced the grep. True total: 16 call sites, this dispatch left 12
> on v1. See DISPATCH_LEDGER_CALLERS_FLIPPED__ast-enumeration-sixteen-not-four-
> standing-invariant-built__v20260804_2019.md (D-R-168).**
