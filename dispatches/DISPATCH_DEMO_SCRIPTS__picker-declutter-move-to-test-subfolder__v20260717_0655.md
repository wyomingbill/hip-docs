# DISPATCH_DEMO_SCRIPTS__picker-declutter-move-to-test-subfolder
Status: BUILT
Reconciled-Against: (pending commit — see HASH)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_SCRIPTS__picker-declutter-move-to-test-subfolder__v20260717_0655.md`

## THE ASK

The dispatch text, verbatim:

> Demo scripts. The picker has 13 and I need 3.
>
> KEEP, these are the demo:
>   boundary_and_consent__v20260715_1158.json
>   speaker_isolation__v20260715_1158.json
>   trust_ladder__v20260716_1600.json
>
> Move everything else out of demo_scripts/ into a test/ subfolder so the picker
> only shows the three. Do NOT delete them — they are wired into harness layers
> and deleting them breaks L2. Check what reads them before moving anything, and
> update the paths.
>
> Also delete trust_ladder__v20260715_1158.json outright. Superseded, its
> phrasing dies at D-02, and two entries labeled "trust_ladder (4t)" in the
> picker is a hazard.
>
> The picker reads demo_scripts/. Confirm it shows only three after, and that
> --full still passes.

## WHAT WAS DONE

1. Checked `trust_ladder__v20260715_1158.json`: already absent from
   `demo_scripts/` on disk. `git log --all --full-history` shows it was
   removed at commit 33049a4 ("remove superseded trust_ladder script
   (phrasing dies at D-02)") — already on `main` before this dispatch
   started. No action taken; verified it stays gone.
2. Confirmed the live picker baseline before touching anything:
   `curl 127.0.0.1:7871/api/demo/scripts` against the running
   `com.hip.demo.dashboard` launchd process (this machine,
   [REDACTED-MACHINE-NAME]) returned 13 entries, matching the 13
   non-`_expected` files then present in `demo_scripts/`.
3. Grepped the whole repo for `demo_scripts` (excluding `.git`/`node_modules`)
   to find every reader before moving anything — 12 code files (`.py`/`.sh`)
   plus doc references. Read each hit in context to classify it as a real
   filesystem reader vs. a comment/label/prose mention.
4. `git mv`'d the 15 non-kept files (10 non-`_expected` scripts + their 5
   `_expected.json` companions) from `demo_scripts/` into a new
   `demo_scripts/test/` subfolder, leaving the 3 kept scripts in place.
5. Fixed every confirmed filesystem reader's path (list in WHAT WAS FOUND).
6. Re-confirmed the picker live (same running dashboard process, no restart
   needed — it globs on every request) — now 3 entries.
7. Ran `python -m eval.harness --full` twice in full (not `--layer 2`, not a
   hand-picked subset — CLAUDE.md item 12), reading the actual RATCHET FAIL /
   NEW FAILURES lines both times, not assuming green.

## WHAT WAS FOUND

Confirmed filesystem readers of `demo_scripts/`, fixed:

- `eval/harnesslib/layer2.py:43-146` — `_script_paths()` globbed
  `SCRIPTS_DIR.glob("*.json")` (non-recursive). This is the mechanism that
  would have "silently broken L2" exactly as Bill flagged: the 5 moved
  scripts with real `_expected.json` pairs (`care_coordination`,
  `consent_flow`, `reveal_demo`, `routing_showcase`, `three_zone_demo`)
  would stop being asserted at all, with no error, just absence. Changed to
  `SCRIPTS_DIR.glob("**/*.json")` (recursive) so L2 discovers scripts in
  both `demo_scripts/` and `demo_scripts/test/`.
- `eval/integration_harness.py:1438` — DEMO-003 scenario hardcoded
  `expect_chain_subject="three_zone_demo.json"`, resolved at line 807 as
  `ROOT / "demo_scripts" / script_file`. Changed to
  `"test/three_zone_demo.json"`.
- `tests/test_demo_presentation.py:24` — `SCRIPT_PATH = ROOT / "demo_scripts"
  / "three_zone_demo.json"`, read by every test via
  `load_for_presentation(SCRIPT_PATH)`. Added `/ "test"`.
- `scripts/demo_preflight.sh:144` — `SAMPLE=".../demo_scripts/
  three_zone_demo.json"` presence/turn-count smoke check. Added `test/`.
- `scripts/check_bytecompat_d1.py:159`, `scripts/capture_shadow_baseline.py:68`
  — both build `ROOT / "demo_scripts" / f"{script_name}.json"` for
  `script_name in ("care_coordination", "reveal_demo")`. Both are standalone
  manual byte-compat tools, not part of `--full`; fixed anyway since they're
  still readers. Added `/ "test"` to both.
- `scripts/demo_run.py:4,45-46`, `scripts/run_demo_script.py:14,17,21` —
  docstring usage examples naming moved files directly under
  `demo_scripts/`. Not executed code; updated so a copy-pasted example
  doesn't 404.
- `scripts/demo_run.sh:6` — same, one comment line.

Confirmed NOT readers, left untouched (checked, not guessed):

- `server/demo_dashboard.py` (`api_demo_scripts`, `api_demo_load`,
  `api_demo_start`) and `server/voice_https_orch.py`
  (`hip_api_demo_scripts`) both glob `demo_scripts/*.json` non-recursively —
  this is exactly what makes the file move sufficient, by itself, to shrink
  the picker to 3. No code change needed for the picker.
- `server/demo_dashboard.py:1837-1842` `_L2_GROUPS` only labels baseline
  dict keys (`L2:{name}.{tid}`) for the results dashboard; no filesystem
  path built from it.
- `eval/test_demo_smoke.py` writes `"script": "three_zone_demo.json"` as
  status-file metadata only; drives turns from a hardcoded literal list,
  never reads the JSON file.
- `eval/harness.py`, `harness/injection_contract.py`,
  `harness/confirmation_gate.py`, `eval/harnesslib/reporter.py`,
  `eval/disclosure_conformance.json`, `scripts/realtime_care_coord_smoke.py`
  — script names appear only as comments, dict labels, or prose.

## VERIFIED

**Watched run — picker, before/after:**
`curl -s http://127.0.0.1:7871/api/demo/scripts` against the live
`com.hip.demo.dashboard` process (pid confirmed via `pgrep -fl
demo_dashboard`), on this machine:
- Before the move: 13 entries — `boundary_and_consent__v20260715_1158.json,
  care_coordination.json, consent_flow.json,
  empty_set_guard__v20260712_1023.json,
  encryption_reveal__v20260712_1023.json,
  isolation_deny_reasons__v20260712_1023.json,
  park_and_confirm__v20260712_1023.json, reveal_demo.json,
  routing_showcase.json, speaker_isolation__v20260715_1158.json,
  three_zone_demo.json, trust_ladder__v20260716_1600.json,
  trust_rungs__v20260712_1023.json`.
- After the move (same running process, no restart): 3 entries exactly —
  `boundary_and_consent__v20260715_1158.json,
  speaker_isolation__v20260715_1158.json,
  trust_ladder__v20260716_1600.json`.

**Watched run — `python -m eval.harness --full`, twice, full output read
(not truncated, exit code captured explicitly since `| tail` masks it):**
- Run 1: `RATCHET FAIL — regressed vs baseline: ['L2:three_zone_demo.T02']`,
  `NEW FAILURES (not in baseline): ['L6:record-invariants']`.
- Run 2 (immediately after, no code changed in between): `RATCHET FAIL —
  regressed vs baseline: ['L2:three_zone_demo.T02']`, no NEW FAILURES line
  (L6 passed this time). `EXIT_CODE=1`.
- Both runs confirm L2 discovered and ran all 13 scripts from their new
  locations — `care_coordination.T01-T04`, `consent_flow.T01-T04`,
  `reveal_demo.R01-R07`, `routing_showcase.T01-T04`,
  `three_zone_demo.T01-T06` all fired and asserted (not silently skipped),
  which is the direct proof the `layer2.py` recursive-glob fix works, not
  just a reasoned claim about the code.
- `L2:three_zone_demo.T02` is the pre-existing D-21 defect ("sam/dad-fall
  fails on purpose — Groq's detector misses on both temp=0.0 and temp=0.2
  retry attempts... Deliberately left failing per Bill's instruction," per
  `docs/BACKLOG.md` item 15 and
  `dispatches/DISPATCH_D22_D20__confirmation-gate-write-loss-and-imperative-openers__v20260716_2238.md`,
  "D-21 still fails exactly as instructed"). It is not new and not caused
  by this move — same script, same turn, same failure mode, now sourced
  from `demo_scripts/test/three_zone_demo.json` instead of
  `demo_scripts/three_zone_demo.json`.
- `L6:record-invariants` (G1 hard-zero gate) flipping FAIL→PASS between two
  back-to-back runs with zero code change in between is direct, live
  confirmation of the pre-existing flake tracked as BILL-4/I-10 in
  `docs/BACKLOG.md` ("~91% failure rate on `--full` runs"), not something
  introduced here.
- L1:P2 iteration i016 (`maya preference='vegetarian meals on weekdays'` —
  write-landing timing check) failed on run 2 only; unrelated subsystem
  (user-preference write timing), not part of either run's RATCHET/NEW
  FAILURES comparison against baseline, consistent with pre-existing
  write-timing flake noise already documented elsewhere in this harness,
  not a regression this dispatch introduced.

**Reasoned about (not independently re-run):** the non-`--full` readers
(`scripts/check_bytecompat_d1.py`, `scripts/capture_shadow_baseline.py`,
`scripts/demo_preflight.sh`) were fixed by direct code read and pattern
match against the already-verified `layer2.py`/`integration_harness.py`
fixes, not executed live in this dispatch — they are standalone manual
tools normally run on the Mini or post-commit, outside this dispatch's
scope to invoke.

## HASH

Pending — see the commit that follows this dispatch doc in the same push.

## OPEN

- `docs/BACKLOG.md` item 15 / D-21 (`three_zone_demo.T02` Groq-detector
  miss) remains open and un-fixed, as instructed; this dispatch only
  confirms it is unchanged by the file move, not newly introduced.
- `docs/BACKLOG.md` BILL-4 / I-10 (L6 G1 hard-zero flake) remains open;
  observed again here as a live data point (FAIL then PASS, zero code
  change between), not addressed.
- The 8 scripts still lacking `_expected.json` pairs
  (`boundary_and_consent__v20260715_1158`,
  `speaker_isolation__v20260715_1158`, `trust_ladder__v20260716_1600`,
  `empty_set_guard__v20260712_1023`, `encryption_reveal__v20260712_1023`,
  `isolation_deny_reasons__v20260712_1023`,
  `park_and_confirm__v20260712_1023`, `trust_rungs__v20260712_1023`) still
  SKIP in L2, same as before this move — recording/reviewing them was out
  of scope for this dispatch.
- This session found `docs/BACKLOG.md`, `CLAUDE.md`'s new "Backlog
  Discipline" section, and a `DISPATCH_BACKLOG__...` doc already present as
  uncommitted working-tree changes at the start of this dispatch, made by
  a process other than this session. They are left uncommitted and
  untouched here — not this dispatch's work product, and not reverted per
  the standing instruction not to revert intentional changes found in
  progress.
