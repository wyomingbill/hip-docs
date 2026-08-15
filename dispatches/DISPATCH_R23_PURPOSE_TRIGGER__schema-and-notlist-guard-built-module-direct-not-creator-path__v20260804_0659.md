# DISPATCH_R23_PURPOSE_TRIGGER
Status: BUILT
Reconciled-Against: cb44ecb (pre-existing HEAD this dispatch built on)

**TYPE:** BUILD, under `REQ_STRUCTURAL_CEILING` R23 (named by the dispatch itself — the
REQ-naming gate, Requirements Discipline item 8, is satisfied by naming an EXISTING REQ's
requirement; no new REQ doc was needed for this build).

## THE ASK

Dispatch text, verbatim:

```
=== D-152 | ~/hip-roadmap, roadmap | R23: the purpose-trigger registry ===
STANDARD PREAMBLE. Lane A. GOVERNING REQ: REQ_STRUCTURAL_CEILING R23.
D-150 stopped because no material-circumstance vocabulary exists. R23 is that
vocabulary and it gates the whole solicitation axis — R24, R25, R26, R28 all sit
behind it.

1. SURVEY FIRST, report before building: R23's text as filed; every place the system
   could initiate a request for expanded access today; and what a "material
   circumstance" would have to be composed of to be distinguishable in code.
   STOP AND REPORT if the REQ's own text does not define enough to build against —
   an invented vocabulary is worse than none.
2. THEN BUILD what can be built honestly. The registry names what IS a trigger and
   what explicitly IS NOT — engagement, warmth, answer length, elapsed time, graph
   fullness, prior acceptance, unprompted disclosure. The NOT-list is not commentary;
   it is enforced content. Absent pieces stay absent, asserted absent by a standing test.
3. Acceptance per D-87: executed fault twin, anti-vacuity. Report whether A23 becomes
   writable, and whether A24/A25 become writable behind it. Do not re-tier anything.
4. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
5. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked (whoami/hostname/checkout/branch, matched). Repo lock acquired via
   `scripts/hip_lock.py with repo`. Found `.hip-lock` (the OLD marker mechanism, which
   does not cross-check the new one) held by fable5/D-153, own worktree, docs-only —
   noted, not treated as a block, since it declared a disjoint scope from this
   dispatch's files.
2. Read R23's full text (`:764-780`) and R24-R28 for the axis's shape (already read at
   D-150; re-confirmed present and unchanged).
3. Re-ran D-150's exhaustive offer-initiation search (zero hits, unchanged) and
   extended it: searched for `capability`/`care_function`/`care plan` vocabulary across
   `harness/`, `server/`, `memory_engine/` — the only "capability" hits are
   `harness/router.py`'s off-net compute-enclave routing axis, an unrelated concept:
   **no "enabled care function" or capability-enablement mechanism exists anywhere.**
4. Read `harness/inference_permit.py` in full — found its OWN docstring had
   independently re-confirmed the same purpose_id absence D-150 found, and explicitly
   named R23 as unbuilt. Read `harness/representation_class.py`'s registry
   (`REPRESENTATION_CLASSES`, 14 classes) as the one sibling registry R23's
   `requested_representation_classes` field could honestly cross-reference.
5. Read `REQ_CEILING_ACCEPTANCE` §7.7 (how A2/A8 went UNWRITABLE→LIVE) closely, because
   it is the precedent this dispatch's own "does A23 become writable" question turns
   on: A2/A8 assert against a REAL CREATOR PATH (`memory_engine.store.create_fact_node`,
   called on every real write) — "not against D-130's or D-140's own standalone probe
   scripts." R23 has no equivalent creator: no code issues a sensitive grant offer, so
   there is no real call site to wire a trigger-guard into. This shaped the whole
   build — see WHAT WAS FOUND.
6. Determined item 1's STOP condition does **not** fire: unlike R24 (D-150), R23's own
   text names its seven fields exactly and its NOT-list exactly — enough to build a
   schema and an enforced guard against, even though several of the schema's own
   fields have no real registry to validate against yet.
7. Built `harness/purpose_trigger.py` — see WHAT WAS FOUND for exactly what is real vs.
   honestly absent.
8. Extended `eval/test_ceiling_solicitation.py` (R23 is Axis 5, the same axis A26/A27
   already live there — kept one file per axis rather than starting a new one) with a
   `CEIL-A23` section: 31 new test cases (30 passing + 1 strict xfail), matching this
   file's own established D-87/D-75 conventions (executed fault twins, anti-vacuity,
   an xfail-plus-NOT-xfail-companion split, pinned NOT-list content).
9. **Caught and fixed my own bug before running anything**: my first edit changed the
   shared `_module_level_names` helper (which A26's already-passing tests depend on)
   from top-level-only (`tree.body`) to whole-tree (`ast.walk`), to support my own
   broader offer-issuing scan. That would have silently altered A26's behaviour as a
   side effect of unrelated work. Reverted `_module_level_names` to its original form
   and added a separate `_all_def_names` helper for A23's own scan instead.
10. Ran `eval/test_ceiling_solicitation.py` standalone first (42 passed, 2 xfailed) —
    clean on the first real run, no fixups needed.
11. Ran the full standing-battery list (the same 24 files `scripts/run_harness.sh`
    wires) directly: **454 passed, 9 xfailed** — exactly +30 passed / +1 xfailed over
    D-149's last-recorded baseline (424/8), matching this dispatch's own addition with
    nothing else disturbed.
12. Ran `./scripts/run_harness.sh --layer 7` in full (self-acquires the `graph:7688`
    lock as a precondition): **RATCHET PASS — no scenario regressed vs baseline.**
13. Ran `eval/memory_harness.py` directly (it does not self-acquire a lock, so I took
    `graph:7688` myself first): **13/17 passed**, failures exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — inside the pinned 13-15/17 range, the
    identical named baseline set, not the 16/17 STOP.
14. Reconciled with origin BEFORE committing: local HEAD was 2 commits behind
    (D-151, D-153), and `docs/INDEX.md` carried both the cutover lane's uncommitted WIP
    and my own about-to-be-added row. Used `git diff > patch` + `git stash push -- docs/
    INDEX.md` (reversible — `git checkout --` was correctly blocked by the permission
    layer as a discard-class command) + `git pull --ff-only` + `git stash pop`
    (auto-merged clean, verified: D-146's row removal, all 4 cutover rows, D-151's row,
    D-153's row all present, zero conflict markers) rather than force through it.
15. Added this dispatch's own `docs/INDEX.md` row (below D-153/D-151, same
    `## requirements/` table those used — R23 dispatches have landed there before,
    e.g. D-146/D-148/D-145/D-141, not in the separate `## dispatches/` table).
16. Staged by explicit pathspec (`harness/purpose_trigger.py`,
    `eval/test_ceiling_solicitation.py`, `docs/INDEX.md`, this dispatch doc — nothing
    from the cutover lane's own untracked files), committed, pushed, verified
    post-commit, released the lock.

## WHAT WAS FOUND

### R23's text (item 1)

`docs/requirements/REQ_STRUCTURAL_CEILING__…:764-780`. "A sensitive grant offer SHALL
originate only from a versioned `PURPOSE_TRIGGER` entry tied to a specific enabled care
function. A valid trigger SHALL identify: `purpose_id, required_capability,
requested_representation_classes, requested_audience, requested_retention,
requested_inference_permits, material_circumstance_version`. Engagement, warmth, answer
length, elapsed relationship time, graph fullness, prior acceptance, or unprompted
disclosure SHALL NOT constitute a trigger."

### Every offer-initiation site (item 1) — still none; every capability/care-function
mechanism — none

Re-confirmed D-150's zero-hit search, unchanged, and extended it to `capability`/
`care_function`/`care plan` vocabulary: the only "capability" hits anywhere are
`harness/router.py`'s/`harness/hipconfig.py`'s off-net compute-enclave routing axis —
a completely different, unrelated concept (whether a QUERY needs an off-machine model
call), not a care-function-enablement toggle. **No mechanism exists to make "a specific
enabled care function" (R23's own phrase) a real, checkable state.**

### Why item 1's STOP did NOT fire here, unlike R24 at D-150

R24's own text turns entirely on a `material_circumstance_version` VALUE the system has
no way to distinguish (D-150's finding, re-confirmed unchanged this dispatch). R23's
text is different in kind: it names its **seven fields exactly** and its **NOT-list
exactly** — a complete schema and a complete exclusion list, independent of whether the
fields' own registries exist yet. That is "enough to build against" in the same sense
`harness/inference_permit.py` (R2) and `harness/representation_class.py` (R8) were —
both built with some fields honestly absent, per the same discipline applied here.

### What was built — `harness/purpose_trigger.py`

- **`PurposeTrigger`** — a frozen dataclass with exactly R23's seven named fields (
  pinned by a dedicated test:
  `test_ceil_a23_schema_has_exactly_r23s_seven_fields`).
- **`NOT_A_TRIGGER`** — R23's seven-signal NOT-list, verbatim. **`assert_valid_trigger_
  basis(basis)`** raises `NotATriggerError` if `basis` (case/space/hyphen-normalized)
  names one of the seven — this is the "enforced content, not commentary" item 2 asked
  for: real, callable, tested code, not a docstring restating the REQ.
- **`validate_purpose_trigger(trigger)`** — structural validation: the five string
  fields must be non-empty; `requested_representation_classes` must be a subset of
  `harness.representation_class.REPRESENTATION_CLASSES` (the real, existing registry);
  `requested_inference_permits` must be a subset of `KNOWN_INFERENCE_PERMIT_IDS`
  (today, exactly `{ABSTRACTION_PERMIT.permit_id}` — the one real permit that exists).
- **What stays ABSENT, and why (item 2's own instruction)**: `required_capability` is
  accepted as a non-empty string but NOT validated against a real capability registry —
  none exists. `requested_audience` and `requested_retention` are likewise accepted
  structurally, unvalidated — no audience enum exists anywhere in this codebase (free
  text everywhere else too); R21 (retention clock) is NOT MET. `material_circumstance_
  version`'s SEMANTIC validity (is this a genuine material change, per R24's own closed
  list) is explicitly R24's concern, not re-attempted here — R23 only requires the
  field be present.
- **`PURPOSE_TRIGGER_REGISTRY`** — an EMPTY `MappingProxyType` (immutable — mutating it
  raises `TypeError`, tested). Empty not because the schema can't hold an entry, but
  because nothing in this codebase authors one: zero offer-initiation sites, zero
  enabled-care-function mechanism to tie a trigger to. **Asserted empty by a standing
  test** (`test_ceil_a23_registry_is_empty`), matching item 2's explicit instruction
  that absent pieces stay absent and asserted so, not silently seeded.

### What the new tests do and do NOT prove — stated plainly, not implied

`eval/test_ceiling_solicitation.py`'s new `CEIL-A23` section (31 cases): the NOT-list
guard rejects each of R23's seven excluded signals (parametrized, case/space/hyphen-
normalized), an executed fault twin proves the rejection tests depend on real behaviour
(wiping `NOT_A_TRIGGER` via monkeypatch re-admits "engagement" — the twin goes green,
proving the tests above were exercising something real), `validate_purpose_trigger`
rejects unknown representation classes/permits with a matching fault twin, the registry
is confirmed empty and immutable, and an **xfail** (`test_ceil_a23_an_offer_issuing_
mechanism_exists`, strict, AST-based per D-75 discipline, scanning
`harness/orchestrator.py`, `harness/confirmation_gate.py`, `harness/router.py`,
`server/voice_orch.py`) records the "no offer mechanism exists" finding as a standing,
re-checked assertion rather than a one-time claim — with a NOT-xfail companion
(`test_ceil_a23_predicate_accepts_a_conforming_fixture`) proving the scanner isn't just
blind, and another (`..._the_schema_and_guard_exist_today`) recording the half that IS
real, matching A26's own established split exactly.

**This is real, non-vacuous coverage of the MODULE.** It is **not** the same
evidentiary weight as A2/A8's write-boundary enforcement (`REQ_CEILING_ACCEPTANCE`
§7.7): those assert against `create_fact_node`, a REAL creator called on every real
write. `harness.purpose_trigger`'s guard has no equivalent real call site — nothing
anywhere issues a sensitive grant offer for it to gate. The tests call it directly and
synthetically. The module docstring says this explicitly, and this dispatch doc repeats
it so it cannot be read past.

### A23's writability (item 3) — my assessment, not a ruling

**Recommendation: A23 is a CANDIDATE for re-tiering, but not on the same footing as
A2/A8, and I am not re-tiering it.** Two readings compete, and I want both on the
record rather than picking silently:

- **For writable**: A23's fixture ("None — pure build," per `REQ_CEILING_ACCEPTANCE`'s
  own row) now exists — the schema and the enforced NOT-list are real, tested code, the
  same "small, cheap fixture, testable without the full mechanism existing" shape that
  document's own A6 discussion proposes as sufficient (a declared, checkable record
  standing in for a sensor that doesn't exist).
- **Against writable in the A2/A8 sense**: A23's own row text is specifically about
  OFFERS ("every sensitive offer names a valid purpose trigger") — a mechanism that
  does not exist at all, not even partially. A2/A8 could assert against a REAL creator
  because facts ARE created constantly; R23 governs something that has never happened
  once in this codebase. A6's fixture stands in for a missing SENSOR feeding an
  otherwise-real pipeline; an A23 fixture would have to stand in for the ENTIRE OFFER
  PIPELINE — a bigger, different-in-kind gap, not a small one.

I did not name the new tests with a re-tiering claim baked in beyond the `test_ceil_
a23_` prefix itself (used because this codebase's own convention already applies that
prefix to module-direct tests written before a row's official re-tiering — e.g.
`test_ceiling_representation_class.py`'s classifier-only cases predate D-145). D-149's
runner cross-check only inspects rows CURRENTLY tiered LIVE, so this naming carries no
risk of a false "verified" signal reaching the status board while A23 stays UNWRITABLE.

**A24 and A25 do NOT become writable behind this build.** A24 (D-150, unchanged):
`material_circumstance_version`'s SEMANTIC validity is still nothing this build
attempts — R23 only requires the field's presence. A25 (adversarial prompt-mutation
suite over offer WORDING) depends on an offer-templating mechanism that still does not
exist. Neither is re-tiered; both stay UNWRITABLE, matching D-150 and the acceptance
doc's own current 14-row UNWRITABLE set (unaltered by this dispatch).

## VERIFIED

**Watched run, all this dispatch:**
- `eval/test_ceiling_solicitation.py` standalone: 42 passed, 2 xfailed.
- Full standing-battery list (24 files, matching `scripts/run_harness.sh`'s own
  wired list, read from that script rather than re-typed): **454 passed, 9 xfailed**
  (D-149's last recorded baseline: 424/8 — the +30/+1 delta is exactly this dispatch's
  own addition, confirmed by re-running the identical command).
- `./scripts/run_harness.sh --layer 7`: AUDIT 8/8, DISC 1/1, L7 27/27, L7V2 27/28 (1
  opt-in skip), SCHEMA 1/1, VOICE 1/1, **RATCHET PASS — no scenario regressed vs
  baseline.**
- `eval/memory_harness.py`, run directly under a manually-held `graph:7688` lock
  (the script does not self-acquire one): **13/17 passed**, failing set exactly
  `{MEM-115, MEM-116, MEM-117, MEM-118}` — inside the pinned 13-15/17 range, not the
  16/17 STOP, identical to every prior recorded run this session's memory covers.
- `git diff --numstat`/`git show --name-only` before and after commit: confirmed only
  this dispatch's four files landed; the cutover lane's untracked dispatch docs
  remained untouched and unstaged throughout.

**Reasoned about:** "no offer-initiation mechanism exists anywhere" remains, as at
D-150, a negative claim supported by an exhaustive-as-practical search, not provable by
enumeration — the xfail test built this dispatch turns that claim into a standing,
re-checked assertion rather than leaving it as prose alone, which is the most this kind
of claim can honestly become.

## HASH

Staged for commit: `harness/purpose_trigger.py` (new), `eval/test_ceiling_solicitation.py`
(modified), `docs/INDEX.md` (this dispatch's own row only — the cutover lane's and
D-151/D-153's prior content preserved exactly via patch/stash/pull/pop, not retyped),
this dispatch doc (new).

## OPEN

- **D-149 and D-150 are themselves unregistered in `docs/INDEX.md`** — found while
  locating where to add this dispatch's own row. Out of this dispatch's own scope,
  flagged rather than silently absorbed, matching D-146's identical prior flag for
  D-143/D-144's rows.
- **A23's writability is a genuine judgment call, not a clean yes/no** — see WHAT WAS
  FOUND above. Recorded with both readings on the record rather than picking one
  silently; Bill's call, not re-tiered here.
- **`required_capability`, `requested_audience`, `requested_retention` have no real
  registry to validate against** — structural (non-empty-string) validation only. Each
  would need its own build (a care-function-enablement mechanism; R11-R15's audience
  work; R21's retention clock) before `validate_purpose_trigger` could check them for
  real content, not just presence.
- **Nothing ruled**, per instruction.

## RECAP
D-152: R23's purpose-trigger registry SCHEMA and enforced NOT-list built
(`harness/purpose_trigger.py`) — seven fields exactly per R23's text, the seven-signal
NOT-list is real callable code (not commentary), two fields cross-reference real
sibling registries (representation classes, inference permits), the rest stay honestly
absent and are asserted so. 31 new tests (30 pass + 1 strict xfail), all executed fault
twins and anti-vacuity checks green. A23 is a genuine candidate for re-tiering but not
on A2/A8's footing (no real offer-issuing creator path exists to assert against, unlike
`create_fact_node`) — reported both readings, not re-tiered. A24/A25 stay UNWRITABLE,
unchanged. 454/9 batteries, `--layer 7` RATCHET PASS, memory harness 13/17 inside pin
(failures = {115,116,117,118}), nothing ruled.
