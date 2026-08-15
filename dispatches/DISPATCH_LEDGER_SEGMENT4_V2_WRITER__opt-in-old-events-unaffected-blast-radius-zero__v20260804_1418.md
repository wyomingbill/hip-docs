# DISPATCH_LEDGER_SEGMENT4_V2_WRITER
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (Segment 4 of the R16/R17 rebuild — the v2 writer, wiring Segments 1-3
together into an actually R16-compliant new event)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16 (ratified D-71) — no amendment, no new REQ doc, same posture as Segments 1-3.

## THE ASK

Bill's instruction, verbatim:

```
Go ahead with Segment 4.

Two conditions, because this is the first segment that changes a real write:
- Old events must stay readable and verifiable throughout. If any existing event
  becomes unreadable or its hash stops verifying, STOP and report before committing.
- Report the blast radius from an executed run, not from reading the diff: what
  changes for a write today, what the demo does differently, and which fixtures move.
```

## WHAT WAS DONE

1. Gate checked — matched, pulled clean, no lock held during design or build.
2. **Resolved the central design tension before writing code**: R16's own permitted-
   field list has no `actor` field at all (it has `service_role` instead) — but
   encryption and commitment computation both fundamentally need to know WHICH
   member's key to use. Decided NOT to rename or remove `actor` in the new format —
   pseudonymizing member identity is exactly Segment 5's own, explicitly-deferred
   question ("an identity-scheme decision, not a ledger change"), and inventing a
   `service_role` mapping here would have been building a worse, undocumented version
   of that same unmade decision. `actor` stays present, unrenamed, still carrying its
   already-known plaintext-identifier gap (`HEL-ACTOR-1`) — unchanged in this segment,
   not hidden by a cosmetic rename.
3. **Resolved the field-naming risk question**: chose to keep `seq`/`event_id`/
   `event_type`/`ts`/`prev_hash` as the ACTUAL dict keys in the new format too — NOT
   renamed to R16's own `opaque_event_id`/`operation_type`/`timestamp`/`previous_
   entry_commitment` vocabulary. `verify()`'s structural checks (contiguity, chain-
   linking) depend on these exact field names; renaming them would have meant editing
   code Bill's own condition 1 says must not become less certain, for a naming
   preference R16 does not actually require at the JSON-key level (the DATA satisfies
   R16's named fields semantically). Documented as a deliberate, conservative choice.
4. Registered `_HASH_FIELDS_V2` in Segment 1's own `_HASH_FIELDS_BY_VERSION` registry —
   `hel`, the structural fields above, `actor`, `correlation`, `keyed_commitment`
   (Segment 3), `prev_hash`. No `payload`/`payload_enc`/`payload_kid`/`payload_sha256`
   at all.
5. Built `_build_event_v2` as a **wholly separate function from `_build_event`** —
   not a branch inside it — so a diff reviewer sees ZERO changed lines in the existing
   v1 builder. Computes Segment 3's commitment, writes the real payload via Segment 2's
   store (keyed under `actor["id"]` for member events, the fixed pseudo-identifier
   `"system"` for system events — reusing `_load_or_create_member_key` exactly as
   written, since it does not care whether the string it receives is a real member id).
   `policy_version`/`registry_versions`/`service_role` declared explicit `None` —
   R16 names them, nothing in this codebase can honestly fill them, matching
   `InferencePermit`'s own 3-absent-fields precedent (R2/D-130) rather than guessed at.
6. Threaded a new `hel_version: str = "1.0"` keyword-only parameter through
   `_append_locked`/`append()` — **the seal-event build call (`ledger.segment_sealed`)
   was left completely unconditional, always v1**, a deliberate choice: a segment
   boundary marker carries no personal content and has no reason to change format
   ahead of whatever lands inside the segment it opens.
7. Updated `verify()` with a NEW `if ev.get("hel") == "2.0":` branch inserted BEFORE
   the existing payload-shape check, which becomes an `elif` — the entire v1 branch's
   own lines are untouched, only gated behind one added condition. The v2 branch
   checks only that `keyed_commitment` is present (there is no ciphertext or plaintext
   inline anymore to match against).
8. **Verified the whole design by hand, extensively, before writing any test**: a
   mixed v1→v2→v1 chain built via a fresh interpreter session, `verify()` at each
   step, `iter_events()` decrypting v1 correctly and leaving v2's own `payload` key
   absent (by design — the caller fetches it from Segment 2 directly), the commitment
   verifying against the actually-stored (TD-030-stripped) payload, targeted erasure,
   and `destroy_member_key` erasing BOTH a v1 inline payload and a v2 off-ledger one
   for the same member in the same run — all confirmed directly before any pytest was
   written.
9. **Found and corrected my own wrong test expectation, not a code bug**: an early
   hand-check compared the off-ledger payload against the UNSTRIPPED original dict and
   read as a mismatch — traced to TD-030's existing `_strip_value_keys` applying
   (correctly, consistently, unchanged from v1) to whatever payload reaches
   `_build_event_v2`, same as it always has for v1. Verified the commitment and the
   stored payload agree with EACH OTHER on the stripped shape, which is the property
   that actually matters (`verify_keyed_commitment` against real stored content).
10. Wrote `eval/test_ledger_v2_writer.py` — 16 cases, centered on
    `test_hel_v2_old_events_byte_identical_and_still_verify_after_a_v2_event_lands`:
    builds a chain using ONLY the unchanged v1 path, snapshots the raw stored lines
    byte-for-byte, appends a v2 event, and proves the original lines are untouched on
    disk AND each pre-existing event individually still re-hashes to its own stored
    hash. Also: v1 stays the unconditional default when the new kwarg is omitted, v2
    shape (no legacy fields, explicit-None absent fields), system-actor keying, an
    executed fault twin (a stripped `keyed_commitment` post-write is caught by
    `verify()`), both erasure paths proven on v2 events specifically, seal events
    staying v1 unconditionally, and anti-vacuity.
11. Ran the new file standalone: 16/16 passed, no fixups needed.
12. **Ran the full existing ledger test suite** (`test_hel_smoke.py`,
    `test_ledger_anchor.py`, `test_anchor_emitter.py`, `test_registry_version_stamp.py`,
    plus Segments 1-3's own files): 116 passed. **Ran `eval/test_hel_smoke.py` as the
    original standalone script, completely untouched by this dispatch**: 33/33 ALL
    PASS — the Phase 1 acceptance test, unmodified since before this whole rebuild
    began, still passes in full.
13. Wired `eval/test_ledger_v2_writer.py` into `scripts/run_harness.sh`'s standing
    battery list.
14. Ran the full standing-battery list (28 files): 550 passed, 9 xfailed — +16 over
    Segment 2's 534/9.
15. Ran `./scripts/run_harness.sh --layer 7` under the graph lock, held only for the
    run itself: AUDIT 8/8, L7 27/27, L7V2 27/28, SCHEMA 1/1, VOICE 1/1, **RATCHET
    PASS** — this exercises the REAL turn pipeline through `epistemic_record.py::log_
    epistemic_record` → `epistemic_ledger.append()`, unchanged, giving direct executed
    evidence for item 2 of Bill's own instruction, not just a read of the diff.
16. Ran `eval/memory_harness.py` under the graph lock, held only for the run itself:
    13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
17. **Confirmed from source, directly**: `grep -n "hel_version"` across all 4 real
    ledger callers (`epistemic_record.py`, `identity_keys.py`, `demo_reset.py`,
    `verify_ledger.py`) returns zero hits — none opts into v2.
18. Wrote this dispatch doc.
19. Staged by explicit pathspec; committed AND pushed as one lock-guarded command,
    lock held only for that sequence's actual duration.

## WHAT WAS FOUND

### Condition 1 — old events, proven not asserted

The centerpiece test builds a chain the EXACT way every real caller does today
(default `hel_version`), snapshots the raw JSONL lines, appends a v2 event, and
re-reads the file: **the original lines are byte-for-byte unchanged**, and **each
pre-existing event individually recomputes to its own already-stored hash** — not
merely "verify() returns True" (which could theoretically pass even if something subtly
shifted), but each old event checked on its own terms. `iter_events()` still decrypts
the old member payload correctly. `--layer 7`'s RATCHET PASS is the same claim proven
against the real, live turn-write pipeline, not a synthetic fixture.

### Condition 2 — the blast radius, from an executed run

**Zero, today, by design.** `hel_version` defaults to `"1.0"`; `append()`'s existing
signature and behavior for any caller not passing the new keyword are completely
unchanged. Confirmed two independent ways: (a) `grep` across all 4 real ledger callers
finds none passing `hel_version`, and (b) `--layer 7`'s own real turn pipeline ran
clean, RATCHET PASS, meaning the actual, unmodified call sites still produce exactly
the events they always have. **No fixture moves. The demo does nothing differently.**
This is a real, executed answer to the blast-radius question — the finding is "none,"
verified rather than assumed, not a default answer given without checking.

### What Segment 4 actually delivers

For the FIRST TIME, an R16-compliant write is POSSIBLE end to end: a caller that opts
in with `hel_version="2.0"` gets an event with no ciphertext, no plaintext payload, no
plaintext key identifier inline — only a keyed commitment, with the real content living
off-ledger under the same per-member key `destroy_member_key()` already, provably,
erases subject-wide. Nothing calls it yet. Flipping a real write path to v2 is
deliberately left as a separate, later, reviewable decision.

## VERIFIED

**Watched, executed:**
- Interactive smoke tests (three separate runs) proving round-trip, mixed-chain
  verify, targeted erasure, and destroy-key erasure, BEFORE any pytest was written.
- `eval/test_ledger_v2_writer.py`: 16/16 on first run.
- Full ledger test suite (`test_hel_smoke.py` + `test_ledger_anchor.py` +
  `test_anchor_emitter.py` + `test_registry_version_stamp.py` + Segments 1-3's own
  files + this segment's own file): 116 passed.
- `eval/test_hel_smoke.py` run as the ORIGINAL standalone script, unmodified: 33/33
  ALL PASS.
- Full standing battery (28 files): 550 passed, 9 xfailed (+16, exactly this
  dispatch's addition).
- `./scripts/run_harness.sh --layer 7`: RATCHET PASS, clean.
- `eval/memory_harness.py`: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117,
  MEM-118}`.
- `grep -n "hel_version"` across all 4 real ledger callers: zero hits.
- `git show --name-only`/`git status` before and after the guarded commit+push:
  confirmed only this dispatch's own files landed.

**Reasoned about, not independently re-derived:** that keeping v1 field names
identical in v2 (rather than renaming to R16's own vocabulary) is the right
risk/compliance tradeoff is this dispatch's own judgment, argued from Bill's explicit
condition 1 — not something Bill has separately ruled on. Named as a decision so it
can be revisited, not asserted as the only possible design.

## HASH

Staged for commit: `harness/epistemic_ledger.py` (version-gated writer + `verify()`
v2 branch), `eval/test_ledger_v2_writer.py` (new), `scripts/run_harness.sh` (wired the
new file), this dispatch doc.

## WHICH SEGMENT NEXT, AND WHY

**D-160's own sequence is now complete for the mechanism itself** (Segments 1-4 all
landed). What remains, per D-160's own segmentation: **Segment 5** (identifier
pseudonymization — already split into its own dispatch per Bill's earlier instruction,
not scheduled here) and **the cutover decision itself**: whether/when to flip real
callers (`epistemic_record.py` chiefly) to `hel_version="2.0"`. **Recommend that
decision be its OWN dispatch, not built here** — it is the first point where this
rebuild has any real, observable effect on the live system, exactly the kind of
threshold Bill's own two conditions on THIS segment suggest deserves its own explicit
go-ahead rather than being folded into "Segment 4 landed."

## OPEN

- **The cutover (flipping real callers to v2) is not scoped or built.** Named as the
  natural next decision, not decided here.
- **`verify()`'s v2 branch checks only that `keyed_commitment` is present**, not that
  it matches a still-existing off-ledger payload — matching R16's own "the chain
  survives erasure intact and verifiable" property (a v2 event with its payload
  already erased must still verify), but meaning `verify()` alone cannot detect a
  CORRUPTED (not erased) off-ledger payload; that check would need to read Segment 2's
  store directly, deliberately out of `verify()`'s own no-key, chain-only scope,
  matching v1's own identical limit for `payload_enc`.
- **Segment 5 (identifier pseudonymization)** remains split out, unscoped, per Bill's
  own earlier instruction — `actor` in v2 events carries the same known plaintext-
  identifier gap v1 always has.
- **Nothing ruled MET. A16/A17 unaffected, not re-tiered** — no real write changed
  format; the mechanism exists but is not in use.

## RECAP
D-R-164 (Segment 4): wired Segments 1-3 into a working v2 writer — `hel_version="2.0"`
opt-in, real payload off-ledger (Segment 2, shared per-member key), a keyed commitment
inline (Segment 3) instead of ciphertext or plaintext, `verify()` extended with an
additive-only v2 branch. **Condition 1 (old events unaffected) proven, not asserted**:
byte-identical stored lines and per-event hash re-verification after a v2 event lands,
plus the ORIGINAL, untouched `test_hel_smoke.py` script still 33/33. **Condition 2
(blast radius) reported from an executed run**: zero, confirmed both by grepping all 4
real callers (none pass the new parameter) and by a clean `--layer 7` RATCHET PASS
through the real turn pipeline. 550/9 batteries (+16), memory harness 13/17 inside
pin. Cutover to real callers proposed as its own future dispatch, not built here.
A16/A17 unaffected. Nothing ruled.
