# DISPATCH_R24_OFFER_GATE
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD, under `REQ_STRUCTURAL_CEILING` R24/R26 (named by the dispatch itself —
Requirements Discipline item 8's gate is satisfied by naming an EXISTING REQ's
requirement).

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-171 | ~/hip-roadmap, roadmap | R24: one offer per circumstance ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R24.
D-150 stopped on its own STOP: no PURPOSE_TRIGGER / material-circumstance vocabulary
existed. D-152 built it (harness/purpose_trigger.py — seven fields, NOT-list as real
callable code). R24's blocker is gone.

1. RE-CHECK THE BLOCKER FIRST. Confirm against HEAD that R23's registry gives R24 what
   it needs to tell one circumstance from another. STOP AND REPORT if it does not —
   D-150 refused to build a dedup function with nothing to validate against, and that
   judgment stands until the evidence changes.
2. THEN BUILD. One system-initiated offer per (member, purpose, material circumstance
   version). Decline or non-response closes the circumstance with NO penalty, no
   vulnerability label, no caregiver notification.
3. THE FAULT TWIN THAT MATTERS: a second offer for the same unchanged circumstance must
   be REFUSED, proven by execution. And a decline must leave no trace anywhere — prove
   that too, since "creates no record" is the claim that makes this different from
   every consent flow on the market.
4. Absent pieces stay absent and are asserted absent. D-152 flagged that two of R24's
   four material-change kinds have no representation — if that still holds, say so
   rather than inventing one.
5. Acceptance per D-87. Report whether A24 becomes writable; do not re-tier.
6. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
7. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched, tree clean except another lane's own untouched WIP, HEAD in
   sync with `origin/roadmap`.
2. Read R23-R27's full text and D-150's (R24 survey, STOPPED) and D-152's (R23 build)
   own dispatch docs in full, not from memory.
3. Read `harness/purpose_trigger.py` in full — confirmed its `PurposeTrigger` dataclass
   carries `purpose_id: str` and `material_circumstance_version: str` as two of its
   seven required fields, both structurally validated (non-empty) by
   `validate_purpose_trigger`.
4. **Item 1's check answered by making it the API's own shape**, not just by reasoning
   about it: `harness.offer_gate.OfferGate.present_offer` takes a validated
   `PurposeTrigger`, not bare strings — R24's dedup tuple is built directly from R23's
   own validated `purpose_id`/`material_circumstance_version`. No STOP condition fired.
5. Read `docs/requirements/REQ_CEILING_ACCEPTANCE__…v20260801_0617.md`'s A24 row and
   the current generated status board (`docs/status/CEILING_STATUS.html`) — confirmed
   A24 is UNWRITABLE, matching D-150's own last note, unchanged since.
6. **Searched independently for D-152's own "two of four material-change kinds have no
   representation" claim** (item 4's framing) — could not locate that exact
   characterization verbatim in D-152's own dispatch doc. Rather than assume a match,
   ran a fresh survey of all four kinds against HEAD (see WHAT WAS FOUND) and reported
   the fresh count honestly, naming where it could not confirm Bill's own framing
   rather than silently agreeing with it.
7. Grepped for `care_plan`/`legal_role`/`guardianship`/`power_of_attorney`/
   `poa_instrument`/`sensing_contract`/`qualifying_event` across `harness/`, `server/`,
   `memory_engine/`, `scripts/` — read every hit in context (not counted blind) to
   determine which, if any, of R24's four material-change kinds has real
   representation today.
8. Built `harness/offer_gate.py` — see WHAT WAS FOUND for the full design and what
   stays honestly absent.
9. Extended `eval/test_ceiling_solicitation.py` with a `CEIL-A24` section (23 new
   cases), matching this file's own established D-87/D-75 conventions.
10. **Caught and fixed a real bug in my own new module before writing tests against
    it**: `resolve_offer` would have silently let a second call overwrite an
    already-resolved offer's outcome (e.g. "declined" → "accepted") — fixed to raise
    `LookupError` on a second resolution attempt, matching "an offer gets exactly one
    outcome, ever."
11. **Caught and fixed a real bug in my own new TEST, on the first run**: a naive
    substring check (`"poa_instrument" in file_text`) tripped on my OWN module's
    docstring, which legitimately DISCUSSES `poa_instrument_hash` in prose while
    explaining why it is not used — the exact D-75 collision class this session has
    hit twice before (D-R-169's docstring/scanner collision). Fixed with an AST-based
    helper (`_has_real_code_reference`) that excludes `ast.Constant` nodes (docstrings)
    and only matches real identifiers — plus its own fault twin and a prose-ignoring
    case, matching this file's own "AST, never a source regex" discipline.
12. **Considered, and explicitly declined, touching A26's own existing xfail test**
    (`test_ceil_a26_non_response_is_modelled`, whose own reason string says "Flips when
    R24's circumstance model exists"). Investigated whether adding
    `harness/offer_gate.py` to its scanned files would flip it: it would NOT, as
    written — that test uses `_module_level_names` (top-level names only, A26's own
    established convention, explicitly preserved unchanged by D-152), and
    `record_no_response` is a CLASS METHOD, not a module-level function, so it would
    not be found even if the file were added to the scan. Left A26's own test
    completely untouched — re-tiering R26 is a different REQ's own decision, not an
    automatic side effect of building R24, matching this session's own restraint
    around touching other rows' tests.
13. Ran `eval/test_ceiling_solicitation.py` standalone: found and fixed the bug in
    step 11 above; re-ran clean: 59 passed, 2 xfailed (the same two pre-existing xfails
    from A23/A26, neither flipped).
14. Wired nothing new into `scripts/run_harness.sh` — `eval/test_ceiling_solicitation.py`
    was already in the standing battery list (D-152).
15. Ran the full standing battery via `scripts/run_harness.sh --layer 7`: clean on the
    first attempt.
16. **RATCHET PASS — no scenario regressed vs baseline.**
17. Ran the memory harness under the graph lock: **13/17**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — the same pinned set as every prior
    dispatch this session, not a new regression.
18. Wrote this dispatch doc, including item 4's honest, fresh material-change-kind
    count.
19. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### Item 1 — the blocker, re-checked against HEAD

**R23's registry gives R24 exactly what it needs, confirmed by making the connection
the API's own shape, not just by reading the schema.** `harness.purpose_trigger.
PurposeTrigger` carries `purpose_id: str` and `material_circumstance_version: str` —
the two of R24's three dedup-tuple dimensions R23 was ever meant to supply (the third,
`member`, is properly the CALLER's own context, not a trigger's own identity — a
trigger describes a purpose+circumstance, not who it was offered to). `harness.
offer_gate.OfferGate.present_offer(member, trigger)` requires a `PurposeTrigger` and
calls `validate_purpose_trigger` on it FIRST, before ever building the dedup key —
proven, not asserted, by `test_ceil_a24_present_offer_rejects_an_invalid_trigger` and
its own executed fault twin (`test_ceil_a24_fault_twin_r23_validation_disabled_admits_
an_invalid_trigger`, which patches validation to a no-op and shows the same invalid
trigger IS then admitted). **No STOP condition fired.**

### Item 2 — built: `harness/offer_gate.py`

`OfferGate` — per-process, IN-MEMORY-ONLY dedup state (see item 3's own "no trace"
discussion for why persistence was deliberately not built):
- `present_offer(member, trigger)` — validates the trigger via R23's own
  `validate_purpose_trigger`, then raises `DuplicateOfferError` if
  `(member, trigger.purpose_id, trigger.material_circumstance_version)` already has a
  non-reopened offer; otherwise records a pending `OfferRecord`.
- `resolve_offer(member, purpose_id, circumstance_version, *, outcome)` — closes the
  circumstance (R26). Raises `LookupError` if no offer is pending, or if it was
  already resolved (an offer's outcome is set once, never overwritten — the bug found
  and fixed in WHAT WAS DONE step 10).
- `record_decline`/`record_no_response` — named convenience wrappers around
  `resolve_offer`, given clear, discoverable names deliberately (not just for
  readability — see the A26 consideration in WHAT WAS DONE step 12 for why a
  well-named surface mattered even though it did not end up flipping that other row).
- `reopen_purpose(member, purpose_id, circumstance_version)` — R24's ONLY path to a
  new offer for an unchanged circumstance; never implicit, never triggered by
  engagement/time/prior acceptance.

### Item 3 — both fault twins, executed

**The one that matters, by name:** `test_ceil_a24_fault_twin_duplicate_offer_is_
refused` — presents an offer, then presents the SAME trigger to the SAME member
again, and asserts `DuplicateOfferError` is actually raised, executed, not inferred.
`test_ceil_a24_reopen_purpose_allows_exactly_one_more_offer` extends this: reopening
permits exactly one further offer; a THIRD attempt without a second reopen is refused
again — proving reopening is not sticky.

**"Creates no record" — proven in the strongest, most literal sense available:**
`test_ceil_a24_decline_appends_nothing_to_the_real_ledger` runs a real decline against
a hermetic HEL ledger (the same `HIP_HEL_DIR` redirection pattern every ledger test
this session uses) and asserts the event COUNT is byte-for-byte unchanged — not one
new event, tombstone, or note lands anywhere, proven by first writing an unrelated
real event to confirm the "before" snapshot is meaningful, not an empty directory.
`test_ceil_a24_offer_gate_imports_nothing_from_the_ledger_or_registry` is the static
half: an AST scan confirms `harness/offer_gate.py` names neither
`harness.epistemic_ledger` nor `harness.member_registry` in any import statement,
with its own executed fault twin proving the scan would catch it if it did.
`harness.offer_gate`'s own state is in-process memory only — the strongest available
reading of "leaves no trace anywhere," and an honest limit named in its own module
docstring: this guarantee does not survive a process restart, which is unexercisable
either way since nothing in this codebase calls this module from a real request path
yet.

### Item 4 — the four material-change kinds, a fresh count

**Could not locate D-152's own "two of four... no representation" framing verbatim in
its dispatch doc** — named honestly rather than assumed matched. A fresh survey
against HEAD (source grep, every hit read in context) found:

| Kind | Representation today |
|---|---|
| Newly enabled care function | **NONE** — no capability/care-function enablement mechanism exists anywhere (D-152's own identical finding, re-confirmed) |
| New clinician-authored care plan | **NONE** — `care_plan` exists only as an ordinary FACT ATTRIBUTE (alongside `vitals`, `incident`), not a structured plan-introduction event |
| Changed legal role | **ADJACENT, NOT USABLE** — `poa_instrument_hash` (`harness.quorum`/`harness.dyad_registry`/`harness.custody_exit`) is a real, structured legal-instrument credential, but it governs custody-key recovery/eviction authority; it is not exposed as, or checked against, a `material_circumstance_version` |
| Qualifying sensing-contract event | **NONE** — matches `REQ_CEILING_ACCEPTANCE`'s own A6 note verbatim: "a validated sensing contract... pure design today" |

**The honest count is worse than "two of four": zero of R24's four named
material-change kinds has a USABLE representation today.** One (legal role) has a
real, adjacent concept in a different subsystem, deliberately not repurposed here —
`harness/offer_gate.py` has zero code references to `poa_instrument`, confirmed by an
AST scan distinguishing real code from its own docstring's prose discussion of the
term (`test_ceil_a24_legal_role_adjacent_concept_exists_but_is_not_wired`). Nothing
invented; all four stay absent, asserted so.

### Item 5 — A24's writability, my assessment, not a ruling

**Same judgment call D-152 recorded for A23, restated for A24, not re-tiered here:**
- **For writable**: the dedup schema and the enforced refusal are real, tested code —
  a genuine, executed fault twin proves a second offer for an unchanged circumstance
  is refused, which is precisely what A24's own row text asks for ("Circumstance-
  version model").
- **Against writable in the A2/A8 sense**: exactly as A23, this has no real creator
  path — no code anywhere presents a real system-initiated offer for
  `harness.offer_gate` to gate. The tests call it directly and synthetically.

**A24 does NOT become writable by this dispatch's own recommendation — reported both
readings, Bill's call, not re-tiered.**

## VERIFIED

**Watched, executed:**
- `harness/purpose_trigger.py` and `harness/derivation_cascade.py`-adjacent custody
  files read directly, not from memory, before forming item 1's and item 4's claims.
- `eval/test_ceiling_solicitation.py`: found and fixed one real bug in the new test
  suite itself (the docstring-collision false positive) before landing; 59/59 passed,
  2/2 pre-existing xfails unchanged, on the clean re-run.
- `scripts/run_harness.sh --layer 7`: clean on the first attempt; **RATCHET PASS**.
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
- Direct read of `docs/status/CEILING_STATUS.html`'s current A23/A24/A26/A27 rows
  before writing item 5's own recommendation, not assumed from D-150/D-152's prose
  alone.

**Reasoned about, not independently re-derived:** whether `poa_instrument_hash`'s
own adjacent concept could ever be responsibly repurposed as a `material_circumstance_
version` representation was not designed here — named as a real, adjacent option for
a future dispatch to evaluate on its own, not decided in this one.

## HASH

Staged for commit: `harness/offer_gate.py` (new), `eval/test_ceiling_solicitation.py`
(extended), this dispatch doc.

## OPEN

- **A24 is a genuine judgment call, not a clean yes/no** — same shape as A23's own
  open question. Recorded with both readings, Bill's call, not re-tiered.
- **A26's own xfail test was deliberately left untouched** — its own reason text
  anticipates flipping "when R24's circumstance model exists," but its
  module-level-only name scan would not find `record_no_response` (a class method)
  even with `harness/offer_gate.py` added to its scanned files. Re-tiering R26 is that
  row's own decision, not an automatic consequence of this dispatch.
- **`poa_instrument_hash` is a real, adjacent "changed legal role" concept**, not
  repurposed here — named as a real option for whichever future dispatch takes up
  R24's own semantic-validity question (which material_circumstance_version strings
  denote a genuine material change), not decided in this one.
- **This mechanism has no real caller anywhere**, matching every module built this
  session under R16/R17/R23 — the same open question named at D-R-170: no live
  trigger connects any real request to `OfferGate.present_offer`.
- **Nothing ruled MET.**

## RECAP
D-R-171: re-checked R24's own blocker against HEAD and found it genuinely gone —
R23's `PurposeTrigger` carries validated `purpose_id`/`material_circumstance_version`,
and `harness.offer_gate.present_offer` now requires one, making the R23-R24 connection
the API's own shape, not just a compatible pair of strings. Built the dedup gate:
`OfferGate.present_offer` refuses a second offer for an unchanged
(member, purpose_id, material_circumstance_version) tuple, proven by an executed fault
twin; `reopen_purpose` is the only path to a new one. Proved R26's "no trace anywhere"
claim in the strongest available sense — a decline appends ZERO new events to a real,
hermetic HEL ledger, and the module imports neither the ledger nor the member
registry at all, both proven with executed fault twins, not asserted. Found and fixed
two real bugs before landing: a silent-outcome-overwrite bug in the module itself, and
a docstring-collision false positive in my own new test (the same class of
self-inflicted D-75 collision this session has hit before), fixed with an AST-based
scanner rather than a source regex. Fresh-surveyed R24's four material-change kinds
against HEAD rather than trust a prior characterization it could not verbatim locate:
the honest count is zero of four usable today, worse than "two of four" — one
(changed legal role) has a real, adjacent, deliberately-not-repurposed concept
(`poa_instrument_hash`), the other three have nothing at all. Considered and
explicitly declined to touch A26's own xfail test — its own flip condition would not
actually fire from this build, and re-tiering it is a different row's own call.
A24 stays UNWRITABLE, same judgment call as A23, not re-tiered. 59/2 new/extended
tests, full battery green, RATCHET PASS, memory harness 13/17 at the same pinned
failing set. Nothing ruled MET.
