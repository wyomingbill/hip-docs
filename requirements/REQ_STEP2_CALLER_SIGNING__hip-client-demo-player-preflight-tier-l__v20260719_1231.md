# REQ_STEP2_CALLER_SIGNING
Status: IN_PROGRESS — 4 of 5 acceptance items MET live (items 1/2/4/5); item 3
(gate_check.sh check 4 exits 0) BLOCKED, not on the signing fix, but on
D-24 (docs/BACKLOG.md #15c on main) — Tier L's own 6 failing scenarios
(E1/E2/E7/E8/G2/T119) are that same defect's signature reaching a second,
older harness now that signing unblocked it. Bill's explicit call
(2026-07-19): do NOT refresh eval/integration_live_baseline.json to
paper over this — that would bake the bug in as expected/accepted
instead of tracked as open. Item 3 stays blocked until D-24 itself is
fixed, which is REQ_TRUTH_TRACK's (Stage 5) territory, not this REQ's —
see that REQ's own "THE T02 / D-24 DECISION" section, which already
recommends option (a) and is waiting on Bill's confirmation. Not marked
BUILT: forcing item 3 green would misreport a real, separate, unresolved
defect as closed.
Reconciled-Against: roadmap-stage1-wip da40862 (caller inventory); REQ_IDENTITY_BINDING_BUILD step 2 (f271265); D-24 / docs/BACKLOG.md #15c (main); REQ_TRUTH_TRACK (roadmap, Stage 5) names the actual fix track

## THE REQUIREMENT

Bill's own words, across two dispatches:

"Write a short REQ (REQ_STEP2_CALLER_SIGNING) covering: hip_client.html,
scripts/demo_player.py, and scripts/demo_preflight.sh must use the Step 2
signing path so they stop 401ing on text-query. Acceptance: each of the
three sends signed requests and gets real replies; demo.html on 7871
unchanged; --full still passes. Then implement it. Prove hip_client.html
returns a real reply (not the 401 text), demo_player.py speaks a real
answer, demo_preflight.sh check 4 passes. Don't touch the dev-only
callers. Report the hash."

Then, asked directly how to resolve `demo_preflight.sh` check 4 depending
on `gate_check.sh` which depends on `eval/integration_live.py` (Tier L) —
a caller named dev-only in the same instruction — Bill chose: **"Also
sign Tier L"** — widen scope to sign `eval/integration_live.py`'s own
turns too, so check 4 genuinely passes end to end, rather than fake it
with `--quick` or carve a skip-flag into `gate_check.sh`.

Expanded: this REQ's scope is therefore four files, not three —
`server/hip_client.html`, `scripts/demo_player.py`,
`scripts/demo_preflight.sh`, and `eval/integration_live.py` (the last one
solely because `demo_preflight.sh` check 4 transitively depends on it via
`gate_check.sh`, not because Tier L itself was asked for). Every OTHER
dev-only caller named in the caller inventory
(`DISPATCH_IDENTITY_STEP2_CALLER_INVENTORY`) — `scripts/gate_check.sh`
itself (its own code, as opposed to what it calls), `eval/
integration_harness.py` Tier P, `eval/passthrough_consent_vignette.py`,
`scripts/run_demo_script.py` — stays untouched, per the explicit
instruction.

## THE ACCEPTANCE TEST

1. `server/hip_client.html`'s free-text box (`sendTextQuery()`) and its
   own scripted-demo player both return HIP's actual generated reply, not
   an `identity_rejected` error string, when driven against a real
   instance of this branch's own `voice_https_orch.py`.
2. `scripts/demo_player.py`, run against a real server, prints/speaks a
   real reply for a turn, not the literal string `[error: ...]`.
3. `scripts/demo_preflight.sh`, run in full (non-`--quick`) mode against
   a clean environment, reports check 4 (`gate_check.sh`) as PASS —
   `gate_check.sh` itself exits 0, including its Tier L step.
4. `server/static/demo.html` and `server/demo_dashboard.py` (port 7871)
   are unmodified by this REQ — diff confirms zero lines touched there.
5. `eval.harness --full` still passes with no new regression beyond the
   pre-existing `care_coordination.T01`/`T02` flake (D-24).

## WHAT'S ALREADY DONE

- The actual signing primitive: `harness/identity_keys.py`'s
  `sign_turn`/`verify_turn` (REQ_IDENTITY_BINDING_BUILD step 2, commit
  `f271265`). This REQ adds NO new cryptography — every fix here is
  "get a caller to construct/attach `{ts,nonce,sig}` before it POSTs,"
  reusing `sign_turn` exactly as `HarnessServer.post_turn` already does.
- The verify path on both `/api/text-query` implementations and
  `/api/session/select-member` is unchanged and not touched by this REQ.
- The full caller inventory and demo-path risk classification
  (`DISPATCH_IDENTITY_STEP2_CALLER_INVENTORY__unsigned-callers-and-demo-path-risk__v20260719_0941.md`)
  — this REQ does not re-survey, it acts on that inventory's findings.

## WHAT'S KNOWN BROKEN

- `server/hip_client.html`: pure browser JavaScript, no filesystem
  access, cannot read `~/hip-keys/*.key` or call `sign_turn` itself. Its
  two `/api/text-query` call sites POST `{query, member}` with no
  signature fields at all — both now 401, and the UI does not treat that
  specially, so `data.error` (`"identity_rejected: missing — ..."`) is
  shown/read as if it were HIP's actual reply.
- `scripts/demo_player.py`: a local Python CLI with real filesystem
  access — CAN sign, just doesn't yet. Currently catches the resulting
  `HTTPError` and substitutes the string `[error: <exception>]` as the
  reply, which then gets spoken aloud via TTS if not `--silent`.
- `scripts/demo_preflight.sh` check 2: a bash fallback probe (only
  reached if `/api/health` is missing), POSTs an unsigned
  `{"query":"ping","member":"bill"}`. Low-frequency in practice (the
  primary `/api/health` check normally succeeds first) but still
  unsigned and would now report a false PASS-via-workaround or FAIL
  depending on exact status code, not a meaningful health signal.
- `scripts/demo_preflight.sh` check 4 → `gate_check.sh` → its Tier L step
  (`eval/integration_live.py`): unsigned `requests.post`, launches its
  own `voice_https_orch` subprocess exactly like `eval.harness`'s
  `HarnessServer` did before Step 2 fixed it — same class of gap,
  same fix.

## CONSTRAINTS

- `server/static/demo.html` and `server/demo_dashboard.py` — zero lines
  touched. The on-screen `:7871` demo already works and must stay exactly
  as it is; it never reached the gated boundary before this REQ and does
  not need to now.
- No other dev-only caller from the inventory gets touched:
  `scripts/gate_check.sh`'s own code (as opposed to what check 4 calls),
  `eval/integration_harness.py` Tier P, `eval/passthrough_consent_vignette.py`,
  `scripts/run_demo_script.py` all stay unsigned and will continue to
  401 if run directly — unchanged from today, not this REQ's problem.
- `eval.harness --full` must not regress. In particular, `eval/
  harnesslib/inproc.py`'s `InProcServer` (Layer 3, mutation testing) is
  NOT the same code as `eval/integration_live.py` despite both launching
  a `voice_https_orch` subprocess — already fixed in Step 2, not touched
  again here, and this REQ's Tier L fix must not collide with it.
- **Honest limit, stated not hidden:** `hip_client.html` needs a new
  server-side convenience to get a signature into browser JS at all — a
  new endpoint, `POST /api/sign-turn` on `voice_https_orch.py`, that
  signs `{member, body}` via the local keystore on request. This endpoint
  carries NO additional caller authentication, because `voice_https_orch.py`
  has no session/login concept to reuse (unlike `demo_dashboard.py`'s
  operator-token-gated `select-member`) and building one is out of a
  "short REQ"'s scope. Concretely: any caller who can reach this
  endpoint can obtain a valid signature for any registered member, then
  pass `/api/text-query`'s gate with it — functionally restoring
  `text-query`'s pre-Step-2 trust-the-caller exposure ON THIS ONE SERVER,
  for anyone who discovers the new endpoint. This is the SAME "the box
  legitimately holds all three members' keys, the seam is stated not
  hidden" precedent Step 2 already used for `select-member`'s self-sign
  convenience — extended here to a second, harder case where the caller
  genuinely cannot sign for itself. It is also not a fresh hole:
  `voice_https_orch.py` already has other unauthenticated endpoints today
  (`/api/reset`, `/api/facts`, `/api/decrypt`) per the pre-existing,
  UNGOVERNED `TD-101` (broader) tech-debt item — this REQ does not close
  that gap and does not pretend to; it adds one more endpoint to the same
  known-open list, named explicitly rather than silently. A session that
  wants THIS endpoint gated behind real caller auth should file that as
  its own REQ against `voice_https_orch.py`'s auth model generally
  (TD-101's own recommended shape), not bolt a one-off gate onto this one
  route.
- **Do not refresh `eval/integration_live_baseline.json`'s `E1/E2/E7/E8/
  G2/T119` entries to close item 3.** Their current failure is D-24
  (`docs/BACKLOG.md` #15c), a real, open, already-tracked defect —
  updating the baseline to expect the CURRENT (buggy) behavior would
  bake it in as accepted rather than leave it visibly red until the
  actual fix (REQ_TRUTH_TRACK, Stage 5) lands. Item 3 stays failed on
  purpose until then; that is correct, not a gap in this REQ's work.
