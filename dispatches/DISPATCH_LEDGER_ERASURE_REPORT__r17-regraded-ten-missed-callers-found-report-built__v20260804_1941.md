# DISPATCH_LEDGER_ERASURE_REPORT
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (R17 step 7 — the machine-verifiable erasure report) + a material
correction to two prior dispatches' own claims, found while re-grading.

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R17 (ratified D-71). No amendment, no new REQ doc.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-167 | ~/hip-roadmap, roadmap | R17: the erasure sequence ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R17, under the D-71 ratification. R16's mechanism
is built and every production write path is now v2 (D-R-166). R17 is what makes erasure
real rather than available.

1. RE-GRADE R17's SEVEN STEPS AGAINST HEAD, not against D-160's survey. The cutover
   changed the substrate under it. For each step say: exists and wired, exists and
   unwired, or absent. Cite call sites. If your grading differs from D-160's, say where
   and why — do not silently supersede it.
2. NAME WHICH REMAINING SEGMENT THIS IS. D-160 planned seven; 1-4 are done, 5 is split
   out pending an identity scheme. If the erasure sequence is segment 6, say so; if the
   plan's segment numbering no longer matches the work, say that plainly rather than
   forcing it.
3. THEN BUILD THE CHEAPEST STEP THAT MAKES ERASURE VERIFIABLE — including the
   machine-verifiable erasure report R17 requires. A report that asserts success
   without evidence is worse than none.
4. STOP AND REPORT before anything destructive. Any step that deletes real data needs
   Bill's explicit authorization first, named as such.
5. Acceptance per D-87: executed fault twin proving the report catches an erasure that
   did NOT fully happen, plus anti-vacuity.
6. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
7. Rule nothing MET. A16/A17 stay where they are.
```

**Item 4's own premise needed checking before anything else, and turned out to be
false: this dispatch found HIP's live write surface is NOT "every production write
path... v2" as D-R-166 reported.** See the correction below — found while doing item
1's own work, not gone looking for separately.

## WHAT WAS DONE

1. Gate checked — matched, tree clean except other lanes' own untouched WIP, HEAD in
   sync with `origin/roadmap`.
2. Read R17's full text (`:646-666`) fresh, and D-160's own survey doc in full (400
   lines) — its Item 2 table (R17's seven steps, as graded then) and Item 4 (the
   7-segment plan) were the baseline this dispatch re-derives against, not re-reads
   blind.
3. Confirmed via `git log d77af0f..HEAD` that every file D-160's own survey cited for
   the GRAPH side (`harness/extraction_queue.py`, `harness/encryption.py`,
   `harness/custody_exit.py`, `memory_engine/`) has **zero commits** since D-160's
   survey — the graph side is byte-for-byte unchanged; re-confirmed the specific cited
   code (`retract_fact`'s `SET`, never `DELETE`) directly rather than trusting the old
   citation alone.
4. Re-read `harness/epistemic_ledger.py`'s current `erase_payload` (v1 targeted) and
   `destroy_member_key` (subject-wide) in full, and `harness/ledger_payload_store.py`'s
   `erase_payload_for_event` (v2 targeted) in full — all THREE built since D-160 (two
   already existed; the third is Segment 2's own D-R-163 addition).
5. **Grepped for every real caller of `epistemic_ledger.append()`, using the SAME
   pattern D-R-166's own survey used** (`epistemic_ledger\.append(`) — got the same 4
   results D-R-166 reported. Then, because item 1 requires citing call sites and this
   dispatch's own build was about to depend on exactly how many real callers exist,
   **grepped independently for every file that imports `epistemic_ledger` in ANY
   form** (`import epistemic_ledger`, `from harness import epistemic_ledger`, `from
   harness.epistemic_ledger import ...`) — found **5 additional production files**
   D-R-166's own pattern never matched, because they do `from harness.epistemic_ledger
   import append` and then call the bare name `append(...)`, which
   `epistemic_ledger\.append(` cannot match syntactically.
6. Read every one of the 10 additional call sites in full, in context, confirming each
   is a real, live `append()` call (not a dead import) — see the correction below for
   the complete, cited list.
7. Re-graded all seven of R17's steps against this fuller picture — see item 1 below.
8. Answered item 2 (which segment) against both D-160's plan and the newly-found
   scope gap.
9. Designed and built `harness/erasure_report.py` — the cheapest verifiable step:
   a machine-verifiable report for TARGETED (single-artifact) ledger-payload erasure,
   covering both the v1 (`erase_payload`) and v2 (`erase_payload_for_event`)
   mechanisms, mirroring `harness/ledger_anchor.py`'s own allowlisted-field,
   `build_X`/`verify_against_X`, `(ok, msg)` idiom — the pattern D-160's own survey
   named as the closest existing template.
10. Confirmed, fresh (not cited from D-160 alone), that no vector/index/cache
    subsystem anywhere in this codebase touches ledger payloads — `memory_engine/`
    never references the ledger; the ledger modules never reference embeddings —
    before marking R17 step 4 `None` (N/A) rather than `False` for this artifact type.
11. Wrote `eval/test_erasure_report.py` (9 cases): 2 green-path (v1 and v2 complete
    erasure verifies true), 1 anti-vacuity baseline (an untouched event must show
    incompleteness, not a free pass), 3 EXECUTED FAULT TWINS (bypass the real erasure
    function directly — delete the v2 file, or null the v1 content field — so the
    content is genuinely gone but the audit tombstone never landed; separately, a
    hand-forged report claiming success against an untouched event), 1 scope-honesty
    check (N/A steps never silently read `True`), 1 leak-discipline check mirroring
    `ledger_anchor`'s own, 1 unknown-target error case. All 9 pass on first run.
12. Removed one unused import found during a self-review pass before running anything
    (`_ledger_dir` imported but never referenced) — a real, if trivial, cleanup, not
    left in.
13. Wired the new test file into `scripts/run_harness.sh`'s standing battery list.
14. Ran the full standing battery (31 files) via `scripts/run_harness.sh --layer 7`
    (gated by `set -e` on the batteries passing first): **RATCHET PASS — no scenario
    regressed vs baseline.**
15. Ran the memory harness under the graph lock: **13/17**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — the same pinned set as D-R-165/166, not a
    new regression.
16. Confirmed nothing destructive was ever run against real data — every erasure
    exercised in this dispatch, including both fault twins, ran against a hermetic,
    private `HIP_HEL_DIR` (`tmp_path`), matching every prior ledger dispatch's own
    posture. No real member's key, real ledger event, or real Neo4j row was touched.
17. Wrote this dispatch doc.
18. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### MAJOR CORRECTION, found while doing item 1's own work

**D-160's own survey (`item 10` of its own WHAT WAS DONE) and D-R-166's own survey
both undercounted HIP's real production ledger write callers, for the identical
reason: both greped for the literal pattern `epistemic_ledger.append(`, which cannot
match a file that imports the bare name (`from harness.epistemic_ledger import
append`) and calls it unqualified.** D-R-166's own dispatch doc states, verbatim:
*"Confirmed exhaustively: exactly 4 PRODUCTION (non-test) call sites of
`epistemic_ledger.append(`"* — true for that literal grep pattern, false as the
"exhaustive" claim about the complete write surface it was used to support two
sentences later: *"every real production write path in HIP's live system writes
v2."* **That claim is not true. It was not true when D-R-166 made it.**

**The real, now-exhaustively-confirmed list — 14 production call sites across 8
files, not 4 across 3:**

| File | Call sites | Event types | v1/v2 |
|---|---|---|---|
| `harness/epistemic_record.py:360` | 1 | `turn.record` | **v2** (D-R-165) |
| `harness/identity_keys.py:287,309` | 2 | `identity.rejected`, `identity.speaker_mismatch` | **v2** (D-R-166) |
| `scripts/demo_reset.py:147` | 1 | `system.reset` | **v2** (D-R-166) |
| `harness/custody_exit.py:69,287` | 2 | `custody.continuity_gap`, `key.recovery` | v1 — **missed** |
| `harness/household_keys.py:206,252,282` | 3 | `household_circle.grant`, `household_circle.revoke`, `household.key_grant` | v1 — **missed** |
| `harness/care_team_keys.py:153,169` | 2 | `care_team.grant`, `care_team.revoke` | v1 — **missed** |
| `harness/dyad_registry.py:240,415` | 2 | `custody.grant`, `custody.exit`/`custody.evict` | v1 — **missed** |
| `harness/ledger_payload_store.py:150` | 1 | `payload.erased` (the v2 store's OWN audit tombstone) | v1 — **missed, and notable: the v2 erasure mechanism's own audit trail is itself unflipped** |

**Why this matters for R17, not just for bookkeeping:** every one of the 10 missed
call sites writes household key-management/custody/care-team audit events carrying
stable, plaintext household-visible identifiers (`member_id`, `custodian_member_id`,
`caregiver_member_id`, `recipient_ref`, `dyad_id`) inline, on the immutable chain,
exactly the shape of R16 violation D-160 already found in `epistemic_record.py`
before D-R-165 fixed it. **These 10 are the SAME violation, still live, on the exact
population R17's erasure sequence would need to reach for those event types.** A
household custody/care-team transition is not hypothetical content — it is real
household administrative history, and today it sits inline and unerasable-by-design
(other than subject-wide crypto-shred, unchanged) on every one of these 10 paths.

**Not fixed here.** Flipping 10 more call sites is materially more work than this
dispatch's own scope (R17's erasure report) and was not asked for — named as a
finding and a clear follow-up recommendation (see OPEN), not silently absorbed into
this dispatch's build. **D-160's and D-R-166's own docs are not edited** (append-only,
per this project's own discipline) — this section is the correction, per CLAUDE.md's
own pre-authorized class ("correct its own prior report when later evidence
contradicts it... in a new record that names the old one").

### Item 1 — R17's seven steps, re-graded against HEAD

Two surfaces, graded separately, because the cutover changed only one of them:
**GRAPH** (`:Fact` nodes in Neo4j — unchanged since D-160, confirmed by `git log`
above) and **LEDGER** (the ledger's own off-ledger/inline payload copy — substantially
built since D-160: Segments 1-4, D-R-165, D-R-166, and this dispatch's own report).

| step | GRAPH (unchanged) | LEDGER (this dispatch's own surface) | vs. D-160 |
|---|---|---|---|
| **1. revoke active access paths** | PARTIAL, same as D-160 — `retract_fact` is a retrieval filter, not access revocation (`harness/extraction_queue.py:713-765`, `SET valid_to`) | **EXISTS AND WIRED** for a targeted ledger artifact — collapses with step 3 (see below); proven both directions by this dispatch's own fault twins | **NEW GRADE, ledger surface only** — D-160 had no v2 store to grade this against |
| **2. destroy/render unavailable key material** | PARTIAL, same as D-160 — per-fact DEK exists structurally (`harness/encryption.py`), `retract_fact` never nulls it | **N/A for TARGETED erasure** (this dispatch's own report scope) — a single artifact's erasure must not destroy the member's shared key, which other still-active artifacts need. **EXISTS AND WIRED for SUBJECT-WIDE erasure** (`destroy_member_key`, unchanged, proven in D-R-165/166's own hermetic tests) — a DIFFERENT operation this dispatch's report does not cover (see OPEN) | Unchanged reasoning from D-160 for the graph; the ledger's own subject-wide mechanism was already noted by D-160 as "the hard infrastructure already built" — still true, still not report-verified (see OPEN) |
| **3. delete active database rows where supported** | DOES NOT HAPPEN, same as D-160 — `SET`, never `DELETE`, re-confirmed directly | **EXISTS AND WIRED** — `erase_payload_for_event` (v2) `path.unlink()`s the file outright; `erase_payload` (v1) nulls the content field in place (weaker — see below). Both now **independently, machine-verifiably proven**, not just asserted, by this dispatch's report | **UPGRADED from D-160's "does not exist"** for the ledger surface specifically — D-160 graded this against the graph only, since no ledger-side deletion mechanism existed to grade at all before Segment 2 |
| **4. remove vector entries, caches, search indexes** | DOES NOT EXIST, same as D-160 | **N/A, confirmed fresh** — no ledger payload, v1 or v2, is ever embedded/indexed/cached anywhere in this codebase (re-confirmed by source grep this dispatch, not cited from D-160 alone) | Same conclusion, independently re-verified rather than carried forward unchecked |
| **5. append an opaque tombstone to the ledger** | MECHANISM EXISTS, NOT WIRED to fact retraction — `retract_fact` still has zero ledger references, re-confirmed | **EXISTS AND WIRED**, for real — `erase_payload`/`erase_payload_for_event` both append a real `payload.erased` audit event today; this dispatch's own report independently checks the tombstone actually landed (its fault twin proves a bypassed erasure — content gone, no tombstone — is CAUGHT) | **UPGRADED for the ledger surface** — D-160 correctly noted the primitive existed; this dispatch proves it is not just present but independently VERIFIABLE, which D-160 explicitly left as step 7's own open gap |
| **6. schedule backup expiry** | DOES NOT EXIST, same as D-160 — no backup system anywhere in this codebase, re-confirmed no backup infrastructure landed since | Same — N/A, no ledger-specific backup system either | Unchanged |
| **7. produce a machine-verifiable erasure report** | DOES NOT EXIST for the graph — no fact-level erasure operation exists to report on | **NOW EXISTS** — `harness/erasure_report.py`, this dispatch's own build, for targeted ledger-payload erasure (v1 and v2), independently re-derived from live state, not a self-signed claim | **CLOSED, for this one artifact type** — the gap D-160 named as fully absent is now built, tested, and D-87-accepted for the scope this dispatch covers |

**Where this grading differs from D-160's, and why, stated plainly per item 1's own
instruction:** steps 1, 3, 5, and 7 are graded MORE COMPLETE here than D-160 found
them — not because D-160 was wrong at the time, but because the substrate it graded
against (no off-ledger store, no v2 writer) did not exist yet. D-160 graded the GRAPH
surface exhaustively and correctly; this dispatch adds a SECOND surface (the ledger's
own payload copy) that came into existence after D-160's survey and grades it
separately, rather than blending the two into one misleading composite grade. Steps 2,
4, and 6 are UNCHANGED from D-160 in substance, independently re-verified rather than
assumed stable.

### Item 2 — which segment this is

**Bill's own framing — "R16's mechanism is built and every production write path is
now v2" — turned out to be false** (see the correction above), so the premise D-160's
Segment 6 depends on ("Segment 4 is done") is true as a MECHANISM claim and false as a
WIRING claim: the v2 writer exists and works, but reaches 4 of 14 real callers, not
all of them.

**This dispatch is NOT Segment 6 as D-160 planned it.** D-160's own Segment 6 text:
*"null `encrypted_dek` (step 2)... `DELETE` the row (step 3)... remove the embedding
(step 4)... erase the off-ledger payload + append a HEL tombstone (step 5)"* —
describes a COMBINED graph-plus-ledger operation. The graph half (DEK nulling, row
deletion, embedding removal) is **completely unbuilt** and **genuinely destructive**
against real Neo4j data — exactly the case item 4 says to STOP on, not build.

**This dispatch is a slice of Segment 7 (the erasure report) that turned out NOT to
depend on Segment 6 the way D-160's plan assumed — say so plainly, per item 2's own
instruction, rather than forcing the numbering.** D-160 sequenced Segment 7 after
Segment 6 because it pictured the report describing a NEW fact-erasure operation
Segment 6 would build. But the report this dispatch built verifies erasure
mechanisms that **already existed** (`erase_payload`, `destroy_member_key`, both
pre-dating D-160's own survey) plus one built in Segment 2
(`erase_payload_for_event`) — none of which needed a not-yet-built Segment 6 as a
prerequisite. **The plan's segment numbering does not match the work here**: this
dispatch is Segment 7's own artifact, built and proven, for a scope Segment 6 was
never actually a dependency of.

**What remains, unbuilt, and is genuinely Segment 6 as D-160 defined it:** the
graph-side per-fact erasure operation (DEK destruction, row deletion, embedding
removal) against real `:Fact` nodes. Not attempted here — see item 4.

### Item 3 — the cheapest verifiable step, built

`harness/erasure_report.py` — `build_erasure_report()` / `verify_erasure_report()` /
`erasure_report_leaks()`, mirroring `harness/ledger_anchor.py`'s own
allowlisted-field, independently-re-derived-not-trusted idiom exactly (D-160's own
named template). Scope: TARGETED (single-artifact) erasure only, covering both
`hel=="1.0"` (`erase_payload`) and `hel=="2.0"` (`erase_payload_for_event`) targets,
since the two-population reality (D-R-165) means both are live simultaneously and
will be for a long time — a report that only covered v2 would already be incomplete
against real production data today. SUBJECT-WIDE erasure (`destroy_member_key`)
reporting is explicitly NOT covered — named in OPEN, not silently folded in, because
R17's own text describes a PER-ARTIFACT report ("each revocable fact or smallest
practical revocation unit"), and a subject-wide report is a structurally different,
larger shape (enumerating every event a member ever wrote) that deserves its own
design pass rather than being bolted on cheaply.

### Item 4 — nothing destructive was run

**Every erasure this dispatch exercised — both green-path cases and both fault
twins — ran against a hermetic, private `HIP_HEL_DIR` (pytest's own `tmp_path`),
identical in posture to every ledger dispatch since D-R-161.** No real member's key,
real ledger event, real off-ledger payload, or real Neo4j row was read, written, or
deleted by this dispatch. **The one thing that WOULD require Bill's explicit
destructive-write authorization — building and running the graph-side per-fact
erasure operation (DEK destruction + row `DELETE` + embedding removal) against real
`:Fact` data — was not attempted**, matching D-160's own original finding that this
step needs that authorization first, and matching this dispatch's own item 4
instruction not to build it without asking.

### Item 5 — D-87 acceptance

**Executed fault twin (three of them, not one) proving the report catches an erasure
that did NOT fully happen:**
- `test_erasure_report_catches_incomplete_v2_erasure_missing_tombstone` — bypasses
  `erase_payload_for_event` entirely: deletes the off-ledger file directly (content
  genuinely gone) without appending the audit tombstone. `build_erasure_report` shows
  step 1/3 honestly `True` (the content really is gone) and step 5 `False` (no
  tombstone) — `verify_erasure_report` returns `False`, naming `5_tombstone_appended`
  by name.
- `test_erasure_report_catches_incomplete_v1_erasure_missing_tombstone` — same shape,
  v1: hand-nulls the content field in the raw segment file, bypassing `erase_payload`'s
  own tombstone append. Caught identically.
- `test_erasure_report_catches_a_forged_claim` — a different fault shape: an
  UNTOUCHED event, then a report HAND-FORGED to claim every step succeeded.
  `verify_erasure_report` re-derives fresh from live state rather than trusting the
  report's own claim, and catches the mismatch by name.

**Anti-vacuity:** `test_erasure_report_anti_vacuity_unerased_event_shows_incomplete`
proves the report is not trivially true-by-construction — an event that was NEVER
erased must show every applicable step `False`, and `verify_erasure_report` must
refuse it. Without this case, a `build_erasure_report` that hardcoded every step to
`True` would still pass the green-path tests (they would just be redundant with a
no-op check); this is what proves the steps are genuinely computed from live state,
not asserted. A second anti-vacuity angle,
`test_erasure_report_na_steps_are_never_true`, proves steps 2/4/6 are `None` on BOTH
an untouched and a fully-erased report — never silently flipping to `True`, which
would overclaim completeness for steps this artifact type genuinely cannot satisfy.

## VERIFIED

**Watched, executed:**
- `git log d77af0f..HEAD` on every file D-160's graph-side survey cited: zero commits,
  confirming that surface's grading carries forward unchanged, not re-asserted blind.
- Direct re-read of `retract_fact`'s current body: still `SET`, never `DELETE`.
- Direct re-read of `erase_payload`, `destroy_member_key`, `erase_payload_for_event`
  in full, current code, not recollection.
- The independent, broader import-grep that found the 10 missed call sites — each of
  the 10 read in full context, confirming a real, live `append()` call, not a dead
  import.
- Fresh source grep confirming zero embedding/index/cache references anywhere near
  the ledger, both directions (`memory_engine/` → ledger, ledger → embeddings).
- `eval/test_erasure_report.py`: 9/9 on first run.
- `scripts/run_harness.sh --layer 7`: standing batteries (31 files, `set -e`-gated)
  passed before `eval/harness.py` ran at all; **RATCHET PASS — no scenario regressed
  vs baseline.**
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}` —
  same pinned set as D-R-165/166, confirmed by direct comparison.

**Reasoned about, not independently re-derived:** the claim that flipping the 10
missed callers would follow the same safe pattern D-R-166 already proved (system-kind
actor handling, `append()`'s outer exception-handling contract) is inferred from
their call shapes being visibly similar, not verified case-by-case the way D-R-166
verified its own three — named as a real follow-up, not asserted as proven here.

## HASH

Staged for commit: `harness/erasure_report.py` (new), `eval/test_erasure_report.py`
(new), `scripts/run_harness.sh` (wired the new file), this dispatch doc.

## OPEN

- **10 real production ledger write call sites remain on v1**, found by this
  dispatch, not fixed by it: `harness/custody_exit.py` (2), `harness/household_keys.py`
  (3), `harness/care_team_keys.py` (2), `harness/dyad_registry.py` (2),
  `harness/ledger_payload_store.py` (1, the v2 store's own audit tombstone). Each
  carries plaintext household-visible identifiers inline, the same R16 violation
  category `epistemic_record.py` had before D-R-165. **Recommended as a direct
  follow-up dispatch** (a natural "D-R-168"), same shape as D-R-166's own work:
  survey each call site's actual shape, flip the ones that match, verify hermetically.
- **The graph-side per-fact erasure operation (D-160's own "Segment 6") remains
  completely unbuilt.** DEK destruction, row `DELETE`, embedding removal against real
  `:Fact` nodes — genuinely destructive, needs Bill's explicit authorization before
  any dispatch attempts it, named here as still true.
- **Subject-wide erasure reporting (`destroy_member_key`) is not covered by this
  dispatch's report** — a structurally different, larger report shape (every event a
  member ever wrote, not one artifact) that deserves its own design pass. Named, not
  built.
- **Step 6 (backup expiry) and step 2 for graph-side facts remain genuinely absent
  dependencies**, not gaps this dispatch could have closed — no backup system exists
  anywhere in this codebase; the graph's per-fact DEK nulling has no caller.
- **D-160's own "4 real callers" citation and D-R-166's own "every real production
  write path... v2" claim are both corrected here**, not edited in place — named so a
  future reader who finds either claim first is pointed at this correction.
- **Nothing ruled MET. A16/A17 stay exactly where they are** — this dispatch closes
  one of R17's seven steps for one artifact type; it does not touch either
  acceptance row's own criteria.

## RECAP
D-R-167: re-graded R17's seven erasure steps against HEAD across two surfaces — the
graph (`:Fact` nodes, unchanged since D-160, confirmed via `git log`) and the ledger
(substantially built since D-160: steps 1/3/5 now EXIST AND WIRED for a targeted
artifact, step 7 now EXISTS for the first time via this dispatch's own build; steps
2/4/6 remain N/A or absent, honestly marked, not glossed). **Found, while doing item
1's own work, that D-160's and D-R-166's own "4 real callers"/"every write path is
v2" claims were both wrong — 10 additional real production write call sites exist
across `custody_exit.py`, `household_keys.py`, `care_team_keys.py`,
`dyad_registry.py`, and `ledger_payload_store.py`'s own audit tombstone, all still v1,
missed by a grep pattern that couldn't match a bare-imported `append(...)` call.**
Corrected explicitly, not fixed silently — flipping them is real, separate follow-up
work, recommended but not built here. Named this dispatch's own build as Segment 7's
artifact, built for a scope that turned out NOT to depend on Segment 6 the way
D-160's plan assumed — the graph-side "Segment 6" itself remains fully unbuilt and
genuinely destructive, not attempted, no authorization sought because none was
needed for what WAS built. Built `harness/erasure_report.py` (targeted, v1+v2-aware,
mirroring `ledger_anchor.py`'s own idiom) and `eval/test_erasure_report.py` (9 cases:
2 green-path, 2 anti-vacuity, 3 executed fault twins — two bypassed-erasure gaps, one
forged-claim gap — 1 leak check, 1 error case), all passing, D-87-accepted. 559+9/9
batteries green, RATCHET PASS, memory harness 13/17 at the same pinned failing set.
Nothing destructive run against real data. A16/A17 untouched. Nothing ruled.
