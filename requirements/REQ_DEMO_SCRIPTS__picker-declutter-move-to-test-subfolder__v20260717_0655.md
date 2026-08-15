# REQ_DEMO_SCRIPTS__picker-declutter-move-to-test-subfolder
Status: BUILT
Reconciled-Against: (pending commit — see dispatch HASH)

## THE REQUIREMENT

Bill's own words, verbatim:

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

## THE ACCEPTANCE TEST

1. `GET /api/demo/scripts` (server/demo_dashboard.py, the live picker on
   port 7871) returns exactly 3 entries, with `file` values
   `boundary_and_consent__v20260715_1158.json`,
   `speaker_isolation__v20260715_1158.json`,
   `trust_ladder__v20260716_1600.json` — observed via a live curl against the
   running dashboard process on [REDACTED-MACHINE-NAME], before and after.
2. `demo_scripts/trust_ladder__v20260715_1158.json` does not exist on disk.
3. Every non-kept `.json` file formerly in `demo_scripts/` still exists on
   disk (moved to `demo_scripts/test/`, not deleted), and every reader of
   those files identified below still resolves the correct path.
4. `python -m eval.harness --full` exits green with the same pass/fail
   shape as the pre-move run (RATCHET output read directly, not assumed) —
   per CLAUDE.md item 12, this is checked with `--full`, not a hand-picked
   subset of L2.

## WHAT'S ALREADY DONE

- `demo_scripts/trust_ladder__v20260715_1158.json` was already deleted at
  commit 33049a4 ("remove superseded trust_ladder script (phrasing dies at
  D-02)"), confirmed absent from the working tree and from `git log
  --diff-filter=A` follow-up (no re-add since). The "delete it outright"
  clause of the requirement is therefore already satisfied on `main`; this
  REQ does not repeat that work, only verifies it stays true.
- Baseline picker count confirmed live: `curl 127.0.0.1:7871/api/demo/scripts`
  on the running `com.hip.demo.dashboard` process returns 13 entries
  matching the 13 non-`_expected` files physically present in
  `demo_scripts/` (18 files total minus 5 `*_expected.json` companions).

## WHAT'S KNOWN BROKEN

Nothing is broken yet. This REQ exists because the move is not
mechanically safe: `demo_scripts/` is read by more than the picker, and a
plain `git mv` without updating every reader would silently break coverage
that `eval.harness --full` gate item 12 (CLAUDE.md) exists to catch late,
not early. Readers found by grep, with exactly what breaks if untouched:

- `eval/harnesslib/layer2.py:43-44` (`SCRIPTS_DIR.glob("*.json")`, non-
  recursive) — L2 discovers scripts to run/skip by scanning `demo_scripts/`
  directly. Moving the 5 scripts that have real `_expected.json` pairs
  (`care_coordination`, `consent_flow`, `reveal_demo`, `routing_showcase`,
  `three_zone_demo`) into `test/` without updating this glob would make L2
  silently stop asserting them at all — this is the exact "deleting them
  breaks L2" Bill flagged, achieved without deleting anything.
- `eval/integration_harness.py:807,1438` — DEMO-003 scenario hardcodes
  `expect_chain_subject="three_zone_demo.json"` and resolves it as
  `ROOT / "demo_scripts" / script_file`. Breaks (`FileNotFoundError`) once
  `three_zone_demo.json` moves.
- `tests/test_demo_presentation.py:24` — `SCRIPT_PATH = ROOT / "demo_scripts"
  / "three_zone_demo.json"`, read directly by every test in the file via
  `load_for_presentation(SCRIPT_PATH)`. Same breakage.
- `scripts/demo_preflight.sh:144` — `SAMPLE=".../demo_scripts/
  three_zone_demo.json"` presence/turn-count smoke check. Breaks (FAIL line)
  once the file moves.
- `scripts/check_bytecompat_d1.py:159` and `scripts/capture_shadow_baseline.py:68`
  — both build `ROOT / "demo_scripts" / f"{script_name}.json"` for
  `script_name in ("care_coordination", "reveal_demo")`. Breaks (both are
  standalone manual tools, not part of `--full`, but still readers that must
  not silently rot).
- `scripts/demo_run.py:45-46` and `scripts/run_demo_script.py:14,17,21` —
  docstring usage examples naming `three_zone_demo.json` /
  `consent_flow.json` / `routing_showcase.json` directly under
  `demo_scripts/`. Not executed code, but a copy-pasted example would 404
  after the move; updated for accuracy, not because it's load-bearing.

Confirmed NOT readers (no change needed):
- `server/demo_dashboard.py` `api_demo_scripts`/`api_demo_load`/`api_demo_start`
  and `server/voice_https_orch.py` `hip_api_demo_scripts` both glob
  `demo_scripts/*.json` non-recursively — this is what makes moving files
  out of the root sufficient, by itself, to shrink the picker to 3. No code
  change needed for the picker itself.
- `server/demo_dashboard.py:1837-1842` `_L2_GROUPS` table only labels
  baseline dict keys (`L2:{name}.{tid}`) for the results dashboard; it does
  not touch the filesystem.
- `eval/test_demo_smoke.py` writes `"script": "three_zone_demo.json"` as
  descriptive status-file metadata only; it drives turns from a hardcoded
  literal list, never reads the JSON file.
- `eval/harness.py`, `harness/injection_contract.py`,
  `harness/confirmation_gate.py`, `eval/harnesslib/reporter.py`,
  `eval/disclosure_conformance.json`, `scripts/realtime_care_coord_smoke.py`
  reference script names only as comments, dict labels, or prose — no
  filesystem path built from them.

## CONSTRAINTS

- L2 coverage must not silently shrink. Every script that currently gets a
  real assertion run under L2 (the 5 with `_expected.json` pairs) must still
  get that same run after the move, from its new location.
- The picker (`GET /api/demo/scripts`) must show exactly the 3 kept scripts
  afterward — verified live, not just by code inspection.
- `python -m eval.harness --full` must stay green with the same shape it
  had before this change (no new regressions introduced by path edits) —
  full ratchet output read directly per CLAUDE.md item 12.
- Files are moved (`git mv`), never deleted, except the already-superseded
  `trust_ladder__v20260715_1158.json`, which stays deleted.
