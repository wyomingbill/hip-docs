# DISPATCH_LEDGER_CUTOVER_EPISTEMIC_RECORD
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (Segment 4 cutover — the first observable-effect change, flipping the
one call site every real household turn reaches)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16/R17 (ratified D-71) — no amendment, no new REQ doc.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-165 | ~/hip-roadmap, roadmap | Flip the first real write path to v2 ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R16/R17. Segments 1-4 are complete and nothing
calls them. This is the first change with observable effect on the live system.

1. ANSWER TWO QUESTIONS BEFORE BUILDING, and STOP AND REPORT if either has no clean
   answer:
   a. WHAT HAPPENS TO EVENTS ALREADY WRITTEN IN v1. Do they stay v1 permanently, get
      migrated, or something else? If they stay v1, HIP has two populations and the
      erasure story covers only one — say so plainly and name what that means for R17.
   b. WHEN THE PUBLIC CLAIM CHANGES, AND FOR WHICH DATA. Today's only honest promise
      is "revocation prevents new authorized access." After this flip, what becomes
      true, for facts written when? A claim that holds for some events and not others
      is not a claim HIP may make yet.
2. THEN FLIP ONE PATH — epistemic_record.py. One path only. Do not flip the others in
   the same dispatch.
3. VERIFY FROM AN EXECUTED RUN, not from the diff: a real turn writes a v2 event; the
   pre-existing chain still verifies event-by-event against stored hashes; the anchor
   compatibility proof still holds; and both erasure paths still work across the
   v1/v2 boundary.
4. REPORT THE BLAST RADIUS as observed — what the demo does differently, which
   fixtures move, what a reader of the ledger sees that they did not see yesterday.
5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Rule nothing MET. A16/A17 stay where they are.
```

## WHAT WAS DONE

1. Gate checked — matched, pulled clean, no lock held while answering item 1.
2. **Answered both questions before touching code** — see WHAT WAS FOUND. Neither
   lacked a clean answer; the STOP condition did not fire.
3. Flipped the ONE call site: `harness/epistemic_record.py::log_epistemic_record`'s
   own `epistemic_ledger.append("turn.record", ...)` call gained `hel_version="2.0"` —
   a one-parameter change, with a comment naming what it means for the permanent
   two-population split.
4. Verified with a hand-run smoke test before writing any pytest: a call through the
   real `log_epistemic_record` function produces a `hel=="2.0"` event with a
   `keyed_commitment`, retrievable from the off-ledger store.
5. Wrote `eval/test_ledger_cutover_epistemic_record.py` (8 cases) proving, THROUGH the
   real caller (not the lower-level `append()` API Segment 4's own tests already
   covered): a real turn writes v2; a pre-cutover chain (built via the OLD, unflipped
   call shape) survives byte-for-byte when the first post-cutover event lands; the
   anchor compatibility proof holds across the cutover boundary; both erasure paths
   work across it; the demo-log dual-write is untouched; and only `epistemic_record.py`
   was flipped (checked directly against the other 3 callers' own source).
6. Ran the new file standalone: 8/8 passed, no fixups needed.
7. Ran the full existing ledger regression suite: **found two REAL regressions, not
   hypothetical** — `eval/test_hel_smoke.py`'s own checks 7b and 14 (the ORIGINAL Phase
   1 acceptance script) call `epistemic_record.log_epistemic_record` directly and
   asserted the record lands as an INLINE, decrypted `payload` field — an assumption
   this cutover makes stale BY DESIGN for exactly the call it exercises. **Fixed
   transparently, not silently**: both checks now read from the off-ledger store for a
   v2 event, falling back to the old inline field for a v1 one — the check's own
   PURPOSE ("the same d1.1 dict landed somewhere retrievable") is unchanged; only
   WHERE it looks changed, annotated with why.
8. Re-ran the standalone script: ALL PASS (33/33) again.
9. Wired the new test file into `scripts/run_harness.sh`'s standing battery list.
10. Ran the full standing-battery list (29 files): 558 passed, 9 xfailed.
11. **Attempted to verify item 3 via `--layer 7`, as done for Segments 1-4 — and found
    my own EARLIER claim (D-R-164's dispatch doc) was WRONG.** Investigated rather than
    assume: grepped every scenario file `--layer 7` runs for `epistemic_record`/
    `log_epistemic_record`/`emit_epistemic_record` references. Found only
    `build_epistemic_record` (constructs the dict, never writes it) and one SOURCE-TEXT
    scan (`.read_text()`, not a live call). **`--layer 7` does not exercise
    `log_epistemic_record` at all — RATCHET PASS on `--layer 7` is real evidence that
    nothing ELSE broke, but it is NOT evidence that a real turn writes a v2 event,
    which is what item 3 specifically asks for.** Confirmed by inspecting the real
    ledger's own tail after a `--layer 7` run: no new `turn.record` events, hel or
    otherwise, from that specific invocation.
12. **Got the real evidence item 3 actually asks for**: ran ONE real turn through the
    complete production pipeline — `scripts/text_demo.py --member maya "What's on my
    schedule today?"` — against the REAL Neo4j graph and the REAL `ledger/` directory
    (holding `graph:7688` for the run's own duration), the same way any real household
    turn reaches this code. Confirmed directly against the resulting ledger state (see
    WHAT WAS FOUND).
13. Ran `python3 scripts/verify_ledger.py` against the REAL, now-9357-event production
    chain: verifies clean, both populations.
14. Reconstructed an anchor at the real chain's OWN seq 9356 (its state immediately
    before this dispatch's real turn landed) from the real stored event, and verified
    it against the chain AFTER the v2 event appended — D-89's compatibility proof, on
    real production data, not a synthetic fixture.
15. **Did NOT run either erasure path against the real production ledger** — destroying
    a real member's key or deleting a real off-ledger payload is genuinely irreversible
    against production data and is not authorized by this dispatch's own scope.
    Erasure-across-the-boundary is proven hermetically (item 5 above,
    `test_hel_cutover_destroy_member_key_erases_both_sides_of_the_boundary` and
    `test_hel_cutover_targeted_erasure_of_a_post_cutover_event_leaves_pre_cutover_
    intact`, both passing) — the SAME mechanism, on synthetic data, deliberately not
    repeated destructively against real households' keys.
16. Ran `eval/memory_harness.py` under the graph lock, held only for the run itself:
    13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
17. Wrote this dispatch doc, including the correction of D-R-164's own claim.
18. Staged by explicit pathspec; committed AND pushed as one lock-guarded command,
    lock held only for that sequence's actual duration.

## WHAT WAS FOUND

### Item 1a — what happens to v1 events

**They stay v1 permanently. No migration exists or could exist without breaking the
exact property Segment 1 was built to protect.** Rewriting a past event to move its
content off-ledger would change that event's hash, which would invalidate every anchor
taken at or after it — precisely the failure mode Segment 1's version-gating exists to
prevent. The ONLY things that can ever happen to a v1 event's content are the two paths
that already existed before this rebuild: `destroy_member_key` (crypto-shred — the
ciphertext bytes remain inline forever, only decryptability is destroyed) and
`erase_payload` (null the one event's content field in place, chain-preserving).
**Neither removes the ciphertext's PRESENCE from the immutable chain** — R16's own
prohibited list names "ciphertext containing the claim" as something the chain SHALL
NOT contain, and a crypto-shredded v1 event still contains it, merely unreadable.

**HIP now has two permanent populations, stated plainly, per instruction:**
- **v1 events** (everything written before this dispatch, and anything written by the
  3 still-unflipped callers going forward): ciphertext or plaintext inline, forever;
  erasable only via subject-wide crypto-shred (undecryptable, still present) or a
  targeted in-place null (content gone, but the event's HAVING BEEN ciphertext on the
  immutable chain is not undone).
- **v2 events** (everything through `log_epistemic_record` from this dispatch
  forward): the chain never at any point contains the content — only an opaque
  commitment. "An operator compelled to produce the chain produces commitments, not
  content" (R16's own text) is TRUE for this population and was NEVER true for the
  other one.

**What this means for R17**: R17's own erasure sequence (7 steps) is reachable in
principle for v2 events in a way it structurally cannot be for v1 — step 3 ("delete
active database rows where supported") and the "absence from the log" half of R16's
own two-mechanism design apply ONLY to the off-ledger store, which only v2 events use.
**No fact written before this dispatch can ever have R17's full promise — only
crypto-shred, which is real but is not what R16 asked the rebuild to add.** This is a
permanent, structural asymmetry, not a temporary one that a future migration closes.

### Item 1b — when the public claim changes, and for which data

**The claim does not, and cannot, change uniformly — and this dispatch does not widen
what HIP may claim about erasure at all, for either population, because R17's own
per-fact erasure TRIGGER (Segment 6, never built) still does not exist.**

Precisely, what becomes newly true, and what does not:

- **NEW, true only for facts written from this dispatch forward**: the immutable
  ledger itself never at any point contains the fact's content, in any form —
  ciphertext or plaintext. This closes R16's specific "ciphertext containing the
  claim" violation for new data. It is a real, structural, permanent property of the
  new format.
- **UNCHANGED, identically true for BOTH populations, before and after this
  dispatch**: the only WORKING erasure ACTION today remains subject-wide key
  destruction (`destroy_member_key`). No per-fact, user-facing "erase this specific
  fact" trigger exists anywhere in this codebase — Segment 2's `erase_payload_for_
  event` is a real, tested, CALLABLE primitive, but nothing calls it from any real
  erasure workflow (`retract_fact`, `harness/fact_change.py`, or anywhere else).

**The honest, narrow claim this dispatch's own flip supports**: *"For facts recorded
from 2026-08-04 forward, the immutable ledger's own record of that fact contains no
recoverable content — only an opaque commitment. This does not change what erasure
means or does for any fact, old or new; that remains exactly what it was before this
dispatch."* A wider claim — implying facts written today are more ERASABLE than facts
written yesterday — would be false; only their PRESENCE ON THE CHAIN differs, not
whether an end user can currently get either one actually erased on request.

### Item 3 — verified from an executed run, with a correction along the way

**A real turn writes a v2 event — proven against the real production system, not a
test double.** `scripts/text_demo.py --member maya "What's on my schedule today?"` ran
the complete pipeline (pipecat, the exemplar router, the real orchestrator, injection
contract, model call) and produced a normal `[maya] ... → EDGE [GUARD] admitted=0
withheld=0` response. The REAL `ledger/hel-000001.jsonl` (9357 events now, spanning
this project's full history) gained exactly one new event: `hel: "2.0"`, `turn.record`,
`actor: {maya}`, `keyed_commitment` present, timestamped at the moment the command ran.

**The pre-existing chain still verifies, event-by-event, against real data**:
`scripts/verify_ledger.py` against the full 9357-event real chain: `VERIFIED — chain
OK: 9357 events (8660 encrypted, 1 v2/commitment), 1 segment(s), 0 tombstoned
payload(s), final seq 9357`.

**The anchor compatibility proof holds, against real data**: reconstructed an anchor at
the real chain's seq 9356 (its exact state one event before this dispatch's turn
landed) and verified it against the chain with the new v2 event appended —
`verify_against_anchor` returns `True, "chain matches anchor at seq 9356"`. A fresh
anchor at the new head (seq 9357) leaks nothing (`anchor_leaks` returns `[]`).

**Both erasure paths still work across the boundary — proven hermetically, not against
real households' keys.** `eval/test_ledger_cutover_epistemic_record.py`'s own
`test_hel_cutover_destroy_member_key_erases_both_sides_of_the_boundary` and
`test_hel_cutover_targeted_erasure_of_a_post_cutover_event_leaves_pre_cutover_intact`
both pass, on synthetic data. Deliberately NOT re-run destructively against the real
`ledger/` — the crypto-shred and targeted-erasure functions are irreversible by design,
and running either against a real member's key or a real event is outside anything
this dispatch was asked or authorized to do.

**CORRECTION, found while chasing this item, not carried forward silently: D-R-164's
own dispatch doc claimed `--layer 7`'s RATCHET PASS was "direct executed evidence" that
the real turn pipeline reaches `log_epistemic_record` unchanged. That claim was never
independently verified at the time and is WRONG** — grepping every scenario `--layer 7`
runs for `epistemic_record`-adjacent calls found only `build_epistemic_record` (which
constructs a dict, never writes it) and one source-text scan. `--layer 7`'s RATCHET
PASS (both then and now) is real evidence that nothing ELSE in the harness broke; it
was never evidence about this specific call path, and D-R-164's report overstated what
it had actually shown. Not correcting D-R-164's own doc (append-only, per this
project's own discipline) — corrected here, naming the old claim, per CLAUDE.md's own
"correct a prior report" pre-authorization.

### Item 4 — the blast radius, as observed

- **What the demo does differently**: nothing. The real turn above produced a normal,
  unremarkable response; the user-facing behavior is identical.
- **Which fixtures move**: none. No fixture file, demo script, or seed data was
  touched.
- **What a reader of the ledger sees that they did not see yesterday**: starting at
  the real chain's seq 9357, a `turn.record` event's own shape changes — no
  `payload_enc`/`payload`/`payload_kid`/`payload_sha256`, a `keyed_commitment` field
  in their place, and the underlying record content is retrievable only via
  `harness.ledger_payload_store.load_payload`, not via `iter_events`'s own automatic
  decryption (which still works, unchanged, for every event before it).

## VERIFIED

**Watched, executed:**
- Hand-run smoke test of the flip before any pytest was written.
- `eval/test_ledger_cutover_epistemic_record.py`: 8/8 on first run.
- Full ledger regression suite: found and fixed two real, stale assumptions in
  `test_hel_smoke.py`; re-ran clean, ALL PASS (33/33) standalone.
- Full standing battery (29 files): 558 passed, 9 xfailed.
- **A REAL turn through the complete production pipeline**, against the real Neo4j
  graph and the real `ledger/` directory: confirmed the resulting event directly.
- `scripts/verify_ledger.py` against the real, 9357-event production chain: clean.
- Anchor compatibility, reconstructed and verified against real chain data, both
  pre-turn and post-turn.
- `eval/memory_harness.py`: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117,
  MEM-118}`.
- `grep`-confirmed only `epistemic_record.py` was flipped; the other 3 real callers
  are byte-for-byte unchanged.
- `git status`/`git show --name-only` before and after the guarded commit+push:
  confirmed only this dispatch's own files landed, and that `ledger/`'s real,
  gitignored state (including the new `ledger/payloads/` directory the real turn
  created) was never staged.

**Reasoned about, not independently re-derived:** the permanence of the two-population
split (item 1a) follows from Segment 1's own anchor-compatibility design, argued here,
not separately re-proven by attempting an actual migration (which this dispatch
explicitly does not build).

## HASH

Staged for commit: `harness/epistemic_record.py` (the flip), `eval/test_hel_smoke.py`
(two stale checks corrected), `eval/test_ledger_cutover_epistemic_record.py` (new),
`scripts/run_harness.sh` (wired the new file), this dispatch doc.

## OPEN

- **The two-population split is permanent**, per item 1a's own finding — not a gap
  this dispatch failed to close, a structural consequence of the hash-chain design
  Segment 1 correctly protected. Named so a future reader does not propose "just
  migrate the old events" without re-deriving why that cannot work.
- **R17's own per-fact erasure trigger (Segment 6) still does not exist** — this
  dispatch does not widen HIP's honest erasure claim beyond what it was before,
  despite the format change. The mechanism (`erase_payload_for_event`,
  `destroy_member_key`) is callable and tested; nothing calls it from a real
  workflow.
- **D-R-164's own "executed evidence via --layer 7" claim is corrected here**, not
  edited there — named explicitly so a future reader who finds the old claim first
  is pointed at the correction.
- **The other 3 real callers remain unflipped** (`identity_keys.py`, `demo_reset.py`,
  `verify_ledger.py`) — per this dispatch's own explicit one-path-only scope, not an
  oversight.
- **Nothing ruled MET. A16/A17 stay exactly where they are** — this flip does not
  change either row's tier; the underlying mechanism (build) was already unrelated to
  their acceptance criteria, and this dispatch adds real usage, not new coverage.

## RECAP
D-R-165: flipped the one real write path every household turn reaches
(`harness/epistemic_record.py::log_epistemic_record`) to `hel_version="2.0"`. Answered
both required questions before building: v1 events stay v1 PERMANENTLY (no migration
can exist without breaking anchor compatibility) — HIP now has two permanent
populations, and R17's full erasure promise structurally can never reach the older one;
the honest public claim is narrow — new facts' content never touches the immutable
chain, but erasure ITSELF (the actual mechanism) is unchanged for either population,
since Segment 6 (the erasure trigger) was never built. Verified from an EXECUTED run
against the REAL production system — one real turn through the full pipeline produced a
v2 event; the real 9357-event chain still verifies; an anchor reconstructed at the real
pre-turn state still verifies against the post-turn chain. **Found and corrected a real
overclaim in D-R-164's own report** (`--layer 7` never actually exercises this call
path — a source-grep confirmed it, not assumed). Found and fixed two real, stale
assumptions in the original `test_hel_smoke.py` script, transparently, preserving what
each check verifies. Both erasure paths proven across the v1/v2 boundary hermetically,
deliberately not repeated against real household keys. 558/9 batteries, memory harness
13/17 inside pin. Blast radius: zero user-facing change, one new field shape in the
ledger going forward. A16/A17 untouched. Nothing ruled.
