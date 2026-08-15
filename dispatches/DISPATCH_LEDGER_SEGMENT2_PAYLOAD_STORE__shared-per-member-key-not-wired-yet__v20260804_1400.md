# DISPATCH_LEDGER_SEGMENT2_PAYLOAD_STORE
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (Segment 2 of the R16/R17 rebuild — the off-ledger payload store)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16 (ratified D-71) — no amendment, no new REQ doc, same posture as Segments 1 and 3.

## THE ASK

Bill's instruction, verbatim: **"Go ahead with Segment 2."** — approving
`docs/dispatches/DISPATCH_LEDGER_SEGMENT3_COMMITMENT__…v20260804_1341.md` (D-R-162)'s
own proposal to return to D-160's original sequence.

## WHAT WAS DONE

1. Gate checked — matched, pulled clean (already in sync), no lock held during design
   or build.
2. Designed the KEY QUESTION D-160's own survey left open: does the off-ledger store use
   its OWN new per-member key, or REUSE `epistemic_ledger.py`'s existing one
   (`ledger/keys/member_<id>.key`, already managing `payload_enc`)? **Decided to reuse,
   not invent a second namespace** — R16's own text requires that destroying ONE
   member's key render EVERY payload that member ever generated unrecoverable; two key
   namespaces would mean two keys to destroy for one erasure to be complete, a real way
   to leave a payload recoverable by forgetting the second key.
3. Built `harness/ledger_payload_store.py`: `store_payload`/`load_payload` reuse
   `epistemic_ledger._encrypt_payload`/`_decrypt_payload` directly (the SAME AES-256-GCM
   construction, not a copy) — files live at `<ledger_dir>/payloads/<opaque_event_id>.enc`,
   named by the SAME `event_id` UUID `_build_event` already generates, matching R16's own
   permitted-field name `opaque_event_id` exactly. `payload_exists` (structural only,
   never decrypts). `erase_payload_for_event` (targeted, R17 step 3 extended to this
   store — deletes the file outright, since unlike the ledger's own in-place-null
   `erase_payload` there is no chain hash here to preserve) appends a `payload.erased`
   audit event to the real HEL ledger, matching the ledger's own existing audit shape.
   **No new member-wide destroy function** — `member_erasure_note()` is a pointer, not a
   mechanism: subject-wide erasure is `epistemic_ledger.destroy_member_key()`, already
   built, already tested, D-89's own anchor-compatibility proof already covers it,
   because this store's payloads share that exact key.
4. Verified the whole design directly, by hand, before writing tests: store→load
   round-trip, wrong-member decrypt failure, targeted erasure, and the destroy-key path
   (file survives, decryption doesn't) — all against a real, temporary ledger directory.
5. Wrote `eval/test_ledger_payload_store.py`: round-trip, existence-before/after-erasure,
   missing-event safety, per-member cryptographic isolation (two members' payloads
   independently readable/unreadable), targeted-erasure idempotency and scoping (erasing
   one event leaves a sibling event untouched), the erasure audit event's exact shape,
   chain integrity after an erasure append, the shared destroy-key path proven against a
   REAL off-ledger file (file persists, content doesn't; other members unaffected), an
   anti-vacuity check that `member_erasure_note()` names a function that actually exists
   and is callable, encryption-at-rest (the raw file bytes never contain the plaintext
   value — OQ-2's own property, re-proven for this store), path-traversal/malformed-id
   refusal (parametrized: empty, `../../etc/passwd`, embedded slash, embedded backslash),
   and an executed fault twin reproducing the UNGUARDED path construction to show it
   really would escape the payloads directory.
6. Ran the file standalone: 19/19 passed on the first run, no fixups needed.
7. Wired `eval/test_ledger_payload_store.py` into `scripts/run_harness.sh`'s standing
   battery list, alongside Segments 1 and 3's own test files.
8. Ran the full standing-battery list (27 files): 534 passed, 9 xfailed — +19 over
   Segment 3's 515/9, exactly this dispatch's own addition.
9. Ran `./scripts/run_harness.sh --layer 7` under the graph lock, held only for the run
   itself: AUDIT 8/8, L7 27/27, L7V2 27/28, SCHEMA 1/1, VOICE 1/1, **RATCHET PASS, clean
   on the first attempt** — no repeat of Segment 3's transient mutation-survivor issue
   (`TD-R-161`, filed by another lane, not this dispatch).
10. Ran `eval/memory_harness.py` under the graph lock, held only for the run itself:
    13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
11. Wrote this dispatch doc.
12. Staged by explicit pathspec; committed AND pushed as one lock-guarded command
    (item 9's own discipline), lock held only for that sequence's actual duration.

## WHAT WAS FOUND

### The shared-key decision, and why the alternative was rejected

A NEW, DEDICATED per-member key for the off-ledger store was the more "separated" design
(the store as a conceptually independent system from the ledger) — and was rejected
specifically because it would have made R16's own erasure guarantee HARDER to keep true,
not easier: an operator who destroys `ledger/keys/member_<id>.key` (today's one, real,
tested erasure action) would leave a SECOND, freshly-invented key file behind, and
"destroy one key, render everything unrecoverable" would silently become false the
moment this store existed. Reusing the exact key `epistemic_ledger.py` already manages
keeps `destroy_member_key()` as the SOLE subject-wide erasure primitive, covering both
the ledger's own legacy inline payloads and this store's new off-ledger ones with the
identical action — proven directly (`test_hel_store_destroy_member_key_makes_stored_
payloads_unreadable`), not merely asserted.

### The two erasure paths this store now provides are genuinely different guarantees

`erase_payload_for_event` (targeted, file deleted) and `destroy_member_key` (subject-wide,
shared with the ledger, file SURVIVES but becomes permanently undecryptable) are not
redundant — R16's own text distinguishes them ("absence from the log" vs "cryptographic
shredding," each covering what the other cannot). This dispatch proved both independently
against real files, not assumed from the design.

### Blast radius: none

Nothing calls `harness/ledger_payload_store.py` outside its own test file. No existing
behavior changed. `--layer 7` and the memory harness both ran clean on the first attempt
this time — Segment 3's own investigated, correctly-attributed transient failure did not
recur.

## VERIFIED

**Watched, executed:**
- Hand-run smoke test (store/load/wrong-member/erase/destroy-key) against a real
  temporary ledger directory, before any test file was written.
- `eval/test_ledger_payload_store.py`: 19/19 on first run.
- Full standing battery (27 files): 534 passed, 9 xfailed (+19, exactly this dispatch's
  addition).
- `./scripts/run_harness.sh --layer 7`: RATCHET PASS, clean, first attempt.
- `eval/memory_harness.py`: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117,
  MEM-118}`.
- `git show --name-only`/`git status` before and after the guarded commit+push:
  confirmed only this dispatch's own files landed; the cutover lane's untracked files
  untouched.

**Reasoned about, not independently re-derived:** that reusing the shared key is
strictly better than a dedicated one is this dispatch's own design judgment, argued from
R16's own text — not a comparison Bill has ruled on. Named as a decision, not asserted
as the only possible one.

## HASH

Staged for commit: `harness/ledger_payload_store.py` (new), `eval/test_ledger_payload_
store.py` (new), `scripts/run_harness.sh` (wired the new file), this dispatch doc.

## WHICH SEGMENT NEXT, AND WHY

**Segment 4 (the v2 writer)** is next, and is now genuinely unblocked: Segment 1
(version-gated hashing, so a new `hel=="2.0"` format can exist without touching any past
event's hash or any anchor taken against it), Segment 3 (the keyed commitment
construction), and Segment 2 (this dispatch — the off-ledger store, keyed shared with the
ledger's own existing member key) are all now real, tested, and independent of each
other. Segment 4's job is to WIRE them together: for a `hel=="2.0"` event, compute
Segment 3's commitment, write the payload via Segment 2's store, and put only the
commitment + permitted metadata fields inline — the first segment where a NEW event, from
the moment it lands, is actually R16-compliant. **Not built here** — reported before
building, per the same standing instruction the prior two segments followed.

## OPEN

- **Segment 4 needs a design decision this dispatch did not make**: whether `verify()`
  needs to change AT ALL to handle a mixed `hel=="1.0"`/`hel=="2.0"` chain, or whether
  Segment 1's own version-gated `event_hash()` already makes `verify()`'s existing
  per-event logic correct as-is (it recomputes `event_hash(ev)` per event already, which
  now dispatches on that event's own `hel` — plausibly sufficient, not verified against a
  real mixed chain here).
- **Backup expiry (R17 step 6) remains entirely out of reach**, per D-160's own survey —
  this store's files are exactly the kind of data a backup system would need to schedule
  expiry against, and no such system exists in this codebase.
- **Nothing ruled MET. A16/A17 unaffected, not re-tiered** — this segment is an unwired
  primitive; no observable ledger behavior changed.

## RECAP
D-R-163 (Segment 2): built `harness/ledger_payload_store.py` — the off-ledger payload
store R16's second half requires, reusing (not duplicating) `epistemic_ledger.py`'s
existing per-member AES-256-GCM key so `destroy_member_key()` stays the SOLE subject-wide
erasure primitive for both legacy inline and new off-ledger payloads. Targeted
per-event erasure (file deleted, audited) and subject-wide erasure (file survives,
decryption doesn't) both proven directly against real files, not asserted. 19/19 new
tests including path-traversal refusal with an executed fault twin and OQ-2's own
encryption-at-rest property re-proven for this store. 534/9 batteries (+19), `--layer 7`
RATCHET PASS clean on the first attempt, memory harness 13/17 inside pin. Segment 4 (the
v2 writer) proposed next — the point where all three prerequisite segments converge into
an actually R16-compliant new event. Not built — reported first per instruction. A16/A17
unaffected. Nothing ruled.
