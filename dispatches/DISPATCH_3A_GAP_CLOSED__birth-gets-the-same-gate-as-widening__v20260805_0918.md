# DISPATCH_3A_GAP_CLOSED
Status: BUILT
Reconciled-Against: `c1538d2` (2026-08-05, D-R-176)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
R11 (outbound propagation cap). No new REQ doc filed — this build closes a named
gap in R11's own existing text via Bill's ruling on TD-136, quoted verbatim below;
it is not a new requirement.

## THE ASK

```
=== D-R-176 | ~/hip-roadmap, roadmap | Close the 3a gap: birth gets the same gate as
    widening ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R11 — this build is what lifts its hold. Bill's
ruling on TD-136's answer, the requirement text:
"A fact may be born household-wide only if its subject is none or the author — the same
discipline the explicit share_household directive already carries. The incidental
classification path shall not do what the explicit path is forbidden from doing."

1. AMEND write_rule.py::classify — rule 3a gains Level 2's subject gate. A household-
   attribute fact with a person subject other than the author classifies member-private
   to the speaker, exactly as the refused directive does today.
2. D8 IS THE KNOWN COLLISION. The seeded fixture is a household-owned fact about dad —
   it would fail the new gate at reseed. Fixtures carry origin=fixture; decide whether
   the gate exempts fixture origin (say so explicitly, with the X-04 precedent) or D8's
   seeding changes. STOP AND REPORT if neither is clean — do not carve a silent
   exception.
3. THE FAULT TWIN: D-R-174's own live probe is the fixture — attr=household,
   subject=ray, no directive. Pre-fix it must reproduce born-household-wide; post-fix
   it must classify member-private. Run both directions.
4. BLAST RADIUS FROM AN EXECUTED RUN: what changes for the 9 existing
   attribute=household facts (all subject=household — should be untouched, prove it),
   for D8, and for the demo.
5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Report whether R11's hold can now lift on the evidence. Rule nothing.
```

## WHAT WAS DONE

1. **Read `harness/write_rule.py`'s rule 3a as it stood** (then lines 190-193):
   `if (author == "household" or attribute == "household"): return WriteClass(CLASS_HOUSEHOLD, "household", subject=subj, ...)` — no subject gate of any kind, distinct
   from the Level 2 `share_household` directive four lines above it (lines 160-168),
   which already carries the ratified 2026-07-21 restriction (`subj is None or subj ==
   author`).

2. **Applied the same gate to rule 3a**, to BOTH of its own triggers (`author ==
   "household"`, the system pseudo-owner; `attribute == "household"`) — not just the
   attribute one — because item 2's own framing ("D8 is the known collision")
   identifies D8 as reaching this rule via the AUTHOR trigger (D8's own attribute is
   `risk_pattern`, not `household`), so gating only the attribute trigger would have
   left the exact collision item 2 names ungated.

3. **Item 2's decision, made and recorded (not deferred):** fixture origin is **NOT**
   exempted from the gate. Reasoning: (a) a fixture-keyed bypass is the same
   "second code path keyed on caller-supplied mode" shape `harness/speaker_id.py`'s
   own REQ_VOICE_COMPONENT V1 already forbids elsewhere in this codebase; (b) a
   fixture exemption would mean the demo continues to DEMONSTRATE the exact privacy
   pattern this ruling closes, which defeats the point of closing it. D8's seeding
   changes instead — verified clean, not merely asserted (see WHAT WAS FOUND).

4. **Wrote the fault twin and the permitted-case tests** in
   `eval/test_ceiling_audience.py`, new section "A11.5 THE 3a GAP (D-R-176)":
   `_classify_3a`/`_unrestricted_classify_3a` (the twin reproducing the exact pre-fix
   rule 3a, no subject gate at all), a parametrized `[real, fault-twin]` test using
   item 3's own named probe shape (`author="bill", subject="ray"`), a test proving
   `subj is None`/`subj == author` still widen, a test proving the 9 existing
   household-wide fixtures' own shape (`author="household", subject="household"`) is
   untouched, and two tests proving D8's own reclassification (to CLASS_MEMBER via
   3c) still `encrypt_by_class`-encodes successfully and idempotently.

5. **Ran the full standing battery + `--layer 7`.** This surfaced a REAL, self-caused
   regression the first-cut fix did not anticipate: `L7:P1` ("every household adult
   can decrypt a household-shared fact") failed — see WHAT WAS FOUND for the root
   cause. **This is exactly what item 4 asked the run to catch** ("BLAST RADIUS FROM
   AN EXECUTED RUN... for... the demo"), and it did.

6. **Traced the P1 failure to its exact cause** by reading `_write_plain`'s real
   signature (not assumed), root-caused the gate's own blind spot, and broadened the
   gate's permitted condition by one clause: `subj == "household"`, alongside `subj is
   None` and `subj == author`. Added a dedicated test for this exact shape
   (`test_ceil_a11_household_sentinel_subject_still_widens_for_a_real_author`) and
   corrected the module docstring paragraph that had (now-stale) asserted the gate
   was only the two-clause version.

7. **Re-ran the full standing battery + `--layer 7`.** This surfaced a SECOND, honest
   consequence of the code edit: `MUTATION-NO-SILENT-DISAPPEARANCE` flagged 2
   previously-recorded `write_rule.classify` survivors (at the OLD single-line
   condition's line 204) as having disappeared. Traced (not assumed): they had not
   been killed — the line itself moved (204 -> 217/218) because the fix reformatted
   the if-statement across multiple lines and added a third clause. Accounted for
   this in `docs/techdebt/LATEST_DEBT.md`'s TD-134 entry (the entry this exact
   mechanism checks against, per its own `find_debt_carry` parser), per that entry's
   own established "UPDATE <date> (dispatch N):" convention, naming both the 2
   carried-forward survivors and the 2 genuinely new ones the added clause
   introduced, and citing TD-142's kinship (the same file:line-address-brittleness
   class, previously named for `injection_contract.py`).

8. **Re-ran the full standing battery + `--layer 7` a third time.** Clean:
   `RATCHET PASS`, `L7:P1` passes, `AUDIT:COVERAGE-GRID-RATCHET` passes (confirmed a
   downstream consequence of P1's own failure, not a separate defect — it recovered
   the instant P1 did, with no unrelated change), `MUTATION-NO-SILENT-DISAPPEARANCE`
   passes.

9. **Ran `eval/memory_harness.py` under the graph lock** (`scripts/hip_lock.py with
   graph:7688`), the correct interpreter (`$HIP_DEV_PYTHON`, not system `python3` —
   TD-158's own named hazard).

## WHAT WAS FOUND

- **Rule 3a pre-fix**, `harness/write_rule.py:190-193` (as it stood before this
  dispatch): no subject gate — `attribute == "household"` or `author == "household"`
  alone promoted to `CLASS_HOUSEHOLD` regardless of subject.

- **D8's actual shape**, `scripts/demo_seed.py:129-136`:
  `owner="household", subject="dad", attribute="risk_pattern"`. D8 reaches rule 3a
  via the **author** trigger, not the attribute trigger (its attribute is
  `risk_pattern`, not `household`) — confirming item 2's own framing exactly.

- **D8's reclassification, verified live (hermetic, isolated registry/keys dir), not
  merely reasoned about:** post-fix, `classify(owner="household", subject="dad",
  attribute="risk_pattern")` returns `CLASS_MEMBER`, `owner="household"`,
  `rule="3c-mandatory-exclusion-narrowed"` (falls through 3a to 3c, whose own
  `CLASS_MEMBER` return uses `author` as owner — and D8's author literally IS
  `"household"`, so D8's stamped owner property is unchanged either way).
  `harness.partition_crypto.encrypt_by_class` succeeds on this WriteClass without
  error, using the SAME idempotent, file-existence-checked auto-provisioned
  `"household"` pseudo-member seal keypair any CLASS_MEMBER write already uses
  (`harness/member_seal_keys.py`; `member_registry.get_member_by_id("household")`
  returns `None`, and `update_seal_pubkey` on a non-existent id silently no-ops
  rather than erroring). Confirmed idempotent across repeated `encrypt_by_class`
  calls via the key file's own unchanged mtime.

- **D8's oracle entry needs no change:** `eval/oracle/disclosure_oracle.py`'s
  `access()` function (lines ~101-108) keys ONLY off the `owner` property
  (`FIXTURE[fact_id]["owner"]`), never the internal `WriteClass.visibility` label —
  and D8's `owner` stays `"household"` before and after this fix.

- **The 9 existing seeded `attribute="household"` facts** (`demo_seed.py`'s D3/D7/D10/
  D11 and five more of the same shape) all use `subject=HOUSEHOLD_OWNER` (i.e.
  `subject="household"`, matching `author="household"`) — `subj == author` was
  already true for every one of them before this fix; the new gate does not change
  their outcome. Verified directly, not merely by inspection: `_classify_3a(author=
  "household", subject="household")` returns `CLASS_HOUSEHOLD`.

- **`L7:P1`'s own regression, root-caused via `_write_plain`'s real signature**
  (`eval/harnesslib/layer7_crypto.py:637`):
  `_write_plain(attribute, subject, owner, sensitivity, value, label, utterance="")`.
  P1's own fixture call (line 694):
  `_write_plain("household", "household", "bill", "low", "P1-TEST: trash pickup
  moved to Friday", "p1")` — i.e. `attribute="household"`, **`subject="household"`**,
  **`owner="bill"`** (a REAL member author, not the `"household"` pseudo-owner). The
  first-cut gate (`subj is None or subj == author`) blocked this: `"household"` is
  neither `None` nor equal to `"bill"`. It fell through to 3c and landed
  `CLASS_MEMBER`, owned by `"bill"` — the observed failure
  (`kv=2 owner=bill` where the check expected `owner='household'`).

- **`"household"` as a subject value is this codebase's own real, pre-existing
  convention for "no specific person, the household collectively"** — identical in
  shape to `demo_seed.py`'s own D3/D7/D10/D11 fixtures (`subject=HOUSEHOLD_OWNER`),
  and distinct from Bill's own named collision (a NAMED third party, e.g. `subject=
  "ray"`). The gate now accepts it as a third equivalent to `subj is None`:
  `harness/write_rule.py`, rule 3a's condition is now
  `(author == "household" or attribute == "household") and (subj is None or subj ==
  author or subj == "household")`.

- **`AUDIT:COVERAGE-GRID-RATCHET`'s FAIL on the intermediate run** (coverage
  0.090 -> 0.087, unflagged) was a downstream consequence of `L7:P1`'s own failure,
  not a separate defect — confirmed by its own recovery to PASS the instant `L7:P1`
  was fixed, with no other change in between.

- **`MUTATION-NO-SILENT-DISAPPEARANCE`'s FAIL on the second intermediate run**:
  the persisted trend log (`logs/mutation_survivors.jsonl`) shows the previous run
  recorded 2 `harness.write_rule.classify` survivors at line 204
  (`swap_compare Is->IsNot`, `delete_last_operand(And)`) — the SAME two mutant kinds
  now appear at lines 217/218 in the current run (line numbers shifted by the edit
  splitting one line into several), plus 2 genuinely new survivors
  (`swap_compare Eq->NotEq`, `delete_last_operand(Or)`) on the newly-added
  `subj == "household"` clause. Accounted for in `docs/techdebt/LATEST_DEBT.md`'s
  TD-134 row.

## VERIFIED

**Watched run** (executed, output observed, not reasoned about):
- `eval/test_ceiling_audience.py` standalone, three times across the fix's evolution:
  final run **16 passed, 2 xfailed** (`PYTHONPATH=$(pwd) $HIP_DEV_PYTHON -m pytest
  eval/test_ceiling_audience.py -q --import-mode=importlib`).
- `scripts/run_harness.sh --layer 7`, three times: first run surfaced `L7:P1` FAIL +
  `AUDIT:COVERAGE-GRID-RATCHET` FAIL (the blast-radius finding); second run (after the
  `subj == "household"` fix) surfaced `MUTATION-NO-SILENT-DISAPPEARANCE` FAIL (the
  line-shift finding); third run: **`RATCHET PASS — no scenario regressed vs
  baseline.`**, `L7:P1` PASS, `AUDIT:COVERAGE-GRID-RATCHET` PASS,
  `MUTATION-NO-SILENT-DISAPPEARANCE` PASS, `MUTATION-SCORE` 102/134 (0.76, unchanged
  outside write_rule's own 4 survivors), `MUTATION-SCORE-SELFTEST` PASS,
  `MUTATION-NO-SILENT-DISAPPEARANCE-SELFTEST` PASS.
- `eval/memory_harness.py` under `scripts/hip_lock.py with graph:7688`, the correct
  interpreter: **13/17 passed**, failures exactly `{MEM-115, MEM-116, MEM-117,
  MEM-118}` — the same pinned set every prior dispatch this session has reproduced,
  inside the accepted 13-15/17 range.
- D8's `encrypt_by_class` success and idempotency, via a live (hermetic) call inside
  the new test file.

**Reasoned about** (from reading code, not an independent live production turn):
- No REAL conversational turn was run that reaches rule 3a live, through the
  orchestrator, with a third-party subject and no directive — the fault twin and the
  permitted-case tests call `write_rule.classify` directly, which is the correct and
  sufficient proof for a DETERMINISTIC classification rule, but it is not the same
  claim as "a live household turn was observed being correctly narrowed." Named as a
  limit below.
- Level 2's own `share_household` directive gate (the ratified precedent this fix
  mirrors, `write_rule.py:160-168`) was not tested against the same
  `subject="household"` shape this dispatch found for rule 3a. Reasoned, not run:
  it is architecturally possible the identical gap exists there too (a real member
  invoking `share_household` with subject="household"), untested here, out of this
  dispatch's stated scope (rule 3a only).

## HASH

`c1538d2527bf153ff4297a5208f01613c5c0b37e` (short `c1538d2`) — pushed to
`origin/roadmap`. Filled in by a same-session follow-up edit after the commit
landed (the self-reference problem: a commit cannot name its own hash inside
the file it commits; matches the prior dispatch's own "staged for commit"
convention, made concrete here since the hash was already known at write time).
Contains: `harness/write_rule.py`, `eval/test_ceiling_audience.py`,
`docs/techdebt/DEBT_REGISTER__v20260804_2104.md` (LATEST_DEBT.md's symlink
target), this dispatch doc, `docs/INDEX.md`, `docs/HIP_HANDOFF.md`.

## OPEN

- **R11's hold, on the evidence (rule nothing MET, per instruction):** the write-time
  gap this dispatch was asked to close — an author birthing a household-attribute or
  `"household"`-authored fact about a NAMED third-party subject, with no directive
  spoken — is now closed and proven two ways: structurally (a new AST anchor,
  `test_ceil_a11_rule_3a_specifically_carries_the_gate_in_source`, anchored to the
  SPECIFIC if-statement returning `rule="3a-attribute-household"`, not just any
  subject/author comparison anywhere in `classify()`) and behaviorally (the fault
  twin, both directions, using Bill's own named probe shape). The 9 existing seeded
  household-wide facts are untouched. D8 correctly narrows and still safely encodes.
  The demo's own real household-attribute write path (P1's harness fixture, matching
  D3/D7/D10/D11's convention) still classifies correctly, verified live. Full battery
  green, RATCHET PASS, mutation-coverage disappearance accounted for, memory harness
  inside its pinned range. **This is the evidence a MET ruling on R11 would cite.**

- **Named limits that stay true regardless of any ruling:**
  1. Rule 3a is a deterministic-default fallback exercised here via direct classifier
     calls and fixtures, not via a live production turn through the orchestrator —
     no end-to-end conversational proof was run.
  2. Level 2's own `share_household` directive gate was not re-tested against the
     `subject="household"` shape found here; the same blind spot may exist there,
     unconfirmed either way, out of this dispatch's scope.
  3. R11's own text (`docs/requirements/REQ_STRUCTURAL_CEILING...v20260802_2205.md`)
     covers propagation broadly (engagement, corroboration, elapsed time, graph
     accumulation SHALL NOT widen scope) — this build addresses only the BIRTH-time
     (rule 3a classification) gap, not R11's neighbors (R12-R15) or every other
     propagation vector R11's own text names.
  4. **TD-136's own filed body** (`docs/techdebt/LATEST_DEBT.md`) is about a
     DIFFERENT, still-open question — whether the household exemption should extend
     past the network/egress boundary to an external clinician's servers — not the
     write-time subject gate this dispatch closes. Bill's ruling quoted in this
     dispatch's own text is taken as authoritative and applied as given; this
     dispatch does not reconcile or edit TD-136's own filed body, and flags the
     apparent scope mismatch here rather than silently assuming they are the same
     question.
