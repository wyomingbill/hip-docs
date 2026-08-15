# DISPATCH_IDENTITY_STEP2_CALLER_INVENTORY
Status: BUILT (analysis only, no code touched)
Reconciled-Against: roadmap-stage1-wip f271265 (Step 2's own commit)

**TYPE:** ANALYSIS

**REQ:** NONE — pure inventory, no code change. Follow-up scoping work for
`REQ_IDENTITY_BINDING_BUILD` step 2, not a build itself.

## THE ASK

> Step 2 now 401s unsigned callers. List every caller of text-query and
> select-member that is NOT the dashboard's signed path — hip_client.html
> and any standalone scripts. For each, say whether it's on the demo path
> or dev-only. Don't fix yet — just the list and the demo-path risk.
> Report.

## WHAT WAS DONE

Grepped the whole tree (not just the two files touched in Step 2's own
dispatch) for every reference to `api/text-query` and
`api/session/select-member`, across `.py`, `.html`, `.sh`. 16 files
matched. For each, read the actual call site (not just the grep hit) to
determine: does it really call the gated HTTP endpoint (vs. bypass it
in-process, vs. just mention it in a comment/docstring); is it signed
(already fixed by Step 2) or not; what is it for; who would run it.

## WHAT WAS FOUND

### Already covered by Step 2 — excluded below, not re-listed as risk
- `eval/harnesslib/server.py` (`HarnessServer.post_turn`) and
  `eval/harnesslib/inproc.py` (`InProcServer.post_turn`) — the harness's
  own drivers, both updated in Step 2 to sign every turn.
- `eval/run_sia_shadow_diff.py` — calls `HarnessServer.post_turn`
  directly, inherits the fix for free.
- `server/static/demo.html` (the `:7871` on-screen dashboard) — grepped
  directly: calls `/api/session/select-member` ONLY (the Vault pane), and
  NEVER `/api/text-query` at all. This is "the dashboard's signed path"
  itself — select-member's self-sign convenience covers it.
- `eval/care_coord_run.py` — mentions `/api/text-query` in its docstring
  but actually calls `process_text_query()` directly in-process; never
  touches the HTTP boundary, never sees the gate.
- `server/voice_orch.py` — one comment referencing `/api/text-query` by
  name; not a call site.
- `server/demo_dashboard.py`, `server/voice_https_orch.py` — these ARE
  the gated endpoints, not callers.

### NOT the dashboard's signed path — will now 401 (or degrade) unsigned

| # | Caller | Calls | Demo path or dev-only | Risk if used on the demo path |
|---|---|---|---|---|
| 1 | `server/hip_client.html` (served at `/hip` on port 7860, `voice_https_orch.py`) | TWO unsigned `POST /api/text-query` call sites: (a) line 1044, its OWN scripted-demo player — loads any `demo_scripts/*.json` via `GET /api/demo-scripts/<name>` and plays every turn through unsigned text-query, entirely separate from `demo_dashboard.py`'s in-process `/api/demo/load`+`/api/demo/next` player; (b) line 1176, `sendTextQuery()` — the "Second-member text-input demo" / "Type as Sarah" free-text box | **DEMO PATH.** This is a real, presenter-facing branded client (own speaker picker, reset button, TTS narration, script player), not test tooling. It is a SEPARATE presentable surface from the `:7871` dashboard, on a different port, with its own independent script-playing mechanism. | **HIGH.** If anyone opens `/hip` (port 7860) instead of, or alongside, the `:7871` dashboard — to run a script, or to demo the "second speaker" text-input feature — every turn now fails. The UI does not crash; it shows `data.error` inline ("Error: identity_rejected: missing — ...") as if it were a real system response, in the middle of what looks like a working conversation. |
| 2 | `scripts/demo_player.py` | Unsigned `POST /api/text-query`, one call per script turn, via `requests` | **DEMO PATH.** Documented CLI usage: `source ~/hip-dev/.env.demo`, then plays a script with TTS narration and reads HIP's reply aloud "same voice as the live system." This reads as an alternate/backup presentation tool (e.g. no-browser or rehearsal use), not a test script — no pass/fail assertions, no exit code semantics. | **MEDIUM-HIGH.** Catches the HTTP failure and substitutes the literal string `[error: <exception text>]` as "HIP's reply," which then gets read aloud via TTS if not `--silent`. A presenter relying on this tool would hear an error message spoken as if it were the assistant's answer — worse than a crash, because it looks like partial functionality rather than an obvious break. |
| 3 | `scripts/demo_preflight.sh` | Two paths: (a) an unsigned `/api/text-query` fallback probe at check 2, only reached if `/api/health` is missing (unlikely to fire day-to-day, since `/api/health` exists); (b) check 4 runs `gate_check.sh`, which is broken by #4 below | **DEMO-PATH-ADJACENT.** Its own docstring: "Verifies seven things before a show... Exit codes: 0 all pass, safe to present; 1 one or more failed, do NOT present." This is the documented pre-show checklist on this branch. | **MEDIUM.** Following the documented workflow now produces a real FAIL at check 4 — but for a reason unrelated to whether the demo itself works (the failure comes from `gate_check.sh`'s Tier L step, `eval/integration_live.py`, not from anything on the actual `:7871` demo path). A presenter (or whoever runs this before a show) sees "do NOT present" printed by the script's own exit-code contract, for a false-alarm reason, unless they know to read past it. |
| 4 | `scripts/gate_check.sh` | Does not call the endpoint itself; runs `eval/integration_harness.py --tier F` (step 3, unaffected — Tier F is in-process/no-LLM, never touches HTTP) and `eval/integration_live.py` (step 10, unsigned, will fail) | **DEV-ONLY.** Its own header: "THIS IS THE GATE: nothing may be promoted from ~/hip-dev to ~/hip-harness unless this script exits 0." A pre-promotion merge gate, not demo-facing. Note: this branch's `docs/INDEX.md`/`BACKLOG.md` history this whole session references `eval.harness --full` as THE current gate (per `REQ_HARNESS`); `gate_check.sh` reads as legacy/parallel tooling, not confirmed still authoritative. | **LOW for the live demo, but real for engineering workflow** if this script is still trusted for promotion decisions — it will now permanently report step 10 FAIL until Tier L is either signed or retired. |
| 5 | `eval/integration_live.py` ("Tier L — LIVE-path integration harness, E1-E8") | Unsigned `requests.post(.../api/text-query)`, launches its own `voice_https_orch` subprocess, same pattern as `eval.harness`'s `HarnessServer` but a separate, older implementation | **DEV-ONLY.** Standalone CLI (`python eval/integration_live.py`) and the thing `gate_check.sh` step 10 calls. No presenter path reaches it. | **LOW** directly; feeds into #4's risk. |
| 6 | `eval/integration_harness.py`, Tier P only (`--tier P`, manual flag) | Unsigned `requests.post(https://localhost:{HIP_PORT}/api/text-query)`, default `HIP_PORT=7860` — the SAME port as `hip_client.html` | **DEV-ONLY.** Own docstring: "Tier P... runs before promotion (not in gate_check.sh)" — a manual, occasionally-run check, not automated, not demo-facing. Tier F (which IS in `gate_check.sh`) is unaffected — it never leaves in-process code, confirmed by reading `_run_tier_f`. | **LOW.** Appends `"Tier P HTTP call failed: 401 ..."` to that scenario's failure list; whoever runs Tier P manually will see it plainly. |
| 7 | `eval/passthrough_consent_vignette.py` | Unsigned POST via its own `_post()` helper, against `https://127.0.0.1:7863` (the `dev.sh` dev-voice-server port — neither `:7871` nor `:7860`) | **DEV-ONLY.** One-off diagnostic script, own docstring: "Beat assertions (captured honestly — no re-run to clean up)" — reads as exploratory/single-use tooling from an earlier control-flow build, not a repeatable presenter or CI path. | **LOW.** Records the HTTP status (401) alongside its beat assertions; a human reading the output would see it immediately. |
| 8 | `scripts/run_demo_script.py` | Unsigned `POST /api/text-query`, one call per script turn, asserts `expect_tier`/`expect_intent`/etc. against the response, pass/fail exit code | **DEV-ONLY** primarily — usage examples target the dev port (`7863`); frames itself as a routing-assertion QA tool ("A failure prints on screen in red; all passes → exit 0"), not a presentation tool like `demo_player.py`. It CAN be pointed at any server via `--base-url`, including the demo ports, so it is not purely un-reachable from the demo path — just not documented or intended as one. | **LOW-MEDIUM.** If someone did run it against `:7871` or `:7860` to sanity-check a script before a show (a plausible use, given its purpose), every turn would now fail on the identity gate rather than on an actual routing mismatch — a false negative that could be misread as "the demo is broken" when it is this tool that needs signing. |

## VERIFIED

- **Watched, not just read:** confirmed by direct code read (not
  assumption) that `demo.html` has zero `/api/text-query` call sites, that
  `eval/integration_harness.py` Tier F never leaves in-process code (read
  `_run_tier_f`), and that `gate_check.sh` invokes Tier F only (not Tier
  P) plus `integration_live.py` — none of this dispatch's classification
  claims rest on a grep hit alone; every file in the table above was
  opened and its actual call site read.
- **Not executed:** none of the 8 listed callers were actually RUN to
  observe a live 401 in this dispatch — Step 2's own dispatch already
  proved the underlying gate rejects unsigned calls (P11, live curl); this
  dispatch is a static inventory of who else reaches that same gate, per
  the ask ("don't fix yet — just the list").

## HASH

NONE — no code changed, analysis only.

## OPEN

- Whether `gate_check.sh` / Tier L / Tier P are still treated as
  authoritative anywhere (vs. superseded by `eval.harness --full`) was not
  confirmed here — flagged, not resolved. If they are still relied on,
  #4-6 above are a real, not just theoretical, workflow break.
- Whether `scripts/demo_preflight.sh` on THIS branch is the version
  actually run before a show, or has been superseded by a newer fast
  preflight tool (as happened on `main` per `DISPATCH_DEMO_SELF_VERIFYING`,
  which this branch predates) — not resolved here.
- No fix proposed or applied, per the ask. The straightforward fix for
  #1-3 (demo-path items) is the same pattern Step 2 already used for the
  harness: teach each caller to sign its own turns via
  `harness.identity_keys.sign_turn`, since all of them run on the same
  box and already have local keystore access. Not done here.
