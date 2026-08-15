# DISPATCH_IDENTITY_BINDING_STEP3
Status: BUILT (live-mic two-voice disagreement item explicitly deferred)
Reconciled-Against: commit cdff472 on `roadmap-stage1-wip`; --full/P11/P12 verified 2026-07-20 (this update)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_IDENTITY_BINDING_BUILD__stage1-implementation__v20260718_1720.md`
(build order items 4+5 — voice session binding + speaker_id demotion, and
record/ledger fields; items 1-3 already committed, see
`DISPATCH_IDENTITY_BINDING_STEP2__signing-verify-select-member-text-query__v20260719_0930.md`)

## THE ASK

> Build items 4 and 5 of REQ_IDENTITY_BINDING_BUILD on roadmap-stage1-wip:
> (4) voice session binding — voice path takes its member from the verified
> select-member session, never from speaker_id; on disagreement, verified
> member wins and the mismatch is logged. (5) record/ledger fields — every
> admitted turn's record gets identity_verified=true + the pubkey
> fingerprint; every rejection emits a HEL identity.rejected event with
> reason (missing/forged/replay/unknown). Acceptance: voice admitted only
> via verified session, speaker_id demoted to hint, rejection events land in
> ledger, --full passes with only known D-24/#15c reds. Live-mic proof needs
> Bill at the box — mark that acceptance item deferred if you can't run the
> mic, don't fake it. Report the hash.

## WHAT WAS DONE

1. Read `REQ_IDENTITY_BINDING_BUILD`, its parent `REQ_IDENTITY_BINDING`, and
   `DISPATCH_IDENTITY_BINDING_STEP2` in full before touching code (CLAUDE.md
   gate item 8) — confirmed items 1-3 are committed (8263c25, this branch's
   step-2 commit) and satisfy the gate for items 4/5.
2. Traced the actual voice surfaces before designing the gate: the live
   pipecat pipeline's per-turn speaker gate
   (`server/voice_orch.py:OrchestratorGate._on_user_text`, the
   `self._member_id` assignment at the old lines ~1431-1452) and the REST
   stand-in `/api/voice-query` (`server/voice_https_orch.py`) — both took
   their member SOLELY from `get_member_by_voice`/per-turn Resemblyzer
   scoring, exactly the defect item 4 names. Confirmed via TD-127
   (`docs/techdebt/DEBT_REGISTER__v20260712_2300.md`) that further building
   speaker verification itself is explicitly out of scope/against prior
   decision — this build demotes its role, it does not improve its
   accuracy, consistent with that decision.
3. Built the cross-process bridge item 4 needs: `demo_dashboard.py`'s
   select-member (port 7871) and the voice server (`voice_https_orch.py` /
   the live bot, port 7860) are separate processes with no shared memory —
   unlike `_vault_selected_member`, a verified selection has to reach the
   other process some way. New module `harness/voice_session.py`:
   `set_verified_session`/`get_verified_session`/`clear_verified_session`,
   a single-slot JSON file at `~/hip-harness/data/verified_session.json`
   (override `HIP_VOICE_SESSION_PATH`), atomic tmp+rename writes. Written
   ONLY by `demo_dashboard.py:api_session_select_member` — the ALREADY
   signature-gated build-step-2 endpoint — immediately after its own
   `verify_turn` succeeds; cleared on switch back to
   "operator"/"household" view.
4. Added `harness/identity_keys.py`: `pubkey_fingerprint(member_id)` (sha256
   of the registered raw pubkey, first 16 hex chars — carried on the record,
   never the pubkey itself), `log_identity_rejection` (HEL
   `identity.rejected`, system-actor/plaintext — a member-actor payload
   would key ledger encryption off a possibly-forged/unregistered name,
   which is the wrong trust boundary for a REJECTION event), and
   `log_identity_mismatch` (HEL `identity.speaker_mismatch`, item 4's "the
   mismatch is logged" clause — not a rejection, the turn is still admitted
   under the verified member).
5. `harness/epistemic_record.py`: added `identity_verified`/
   `pubkey_fingerprint` to `build_epistemic_record`'s schema (both default
   `None` — an honest gap, not a fake `True`, for the scripted/operator demo
   path that never reaches any signature gate).
6. `server/voice_orch.py:process_text_query`: added
   `identity_verified`/`pubkey_fingerprint` kwargs (default `None`); a local
   function named `emit_epistemic_record` shadows the module-level import
   for the duration of this call, forwarding both onto every one of the
   12 `emit_epistemic_record(...)` call sites inside the function body
   without editing any of them individually (verified by direct enumeration
   — script confirmed all 12 sites fall within this function's line range).
7. Wired every gated caller: `demo_dashboard.py` and `voice_https_orch.py`'s
   `/api/text-query` now pass `identity_verified=True,
   pubkey_fingerprint=pubkey_fingerprint(member)` into `process_text_query`,
   and call `log_identity_rejection` on the `IdentityVerificationError`
   branch (previously only returned the 401, no ledger event).
   `select-member`'s two failure branches (`FileNotFoundError` from
   `sign_turn`, `IdentityVerificationError` from `verify_turn`) do the same.
8. Rewrote `voice_https_orch.py:/api/voice-query` (item 4's REST surface):
   admission now reads `voice_session.get_verified_session()` first — no
   verified session -> 401 `identity_rejected: missing` +
   `log_identity_rejection`, before any audio is even inspected.
   Voiceprint matching (`get_member_by_voice`) still runs when `audio_b64`
   is supplied, but only to produce `speaker_id_hint` in the response and to
   fire `log_identity_mismatch` when it disagrees with the verified member —
   it can no longer choose who the turn is routed as. `audio_b64` is now
   optional (previously required) since admission no longer depends on it.
9. Rewrote the live pipeline's speaker gate
   (`server/voice_orch.py:OrchestratorGate._on_user_text`): `best_member_id`
   from voiceprint scoring is renamed `speaker_id_hint` and no longer
   assigned to `self._member_id`; `self._member_id` now comes from
   `get_verified_session()` (defensively re-checked against
   `get_member_by_id` in case a session points at a since-removed member).
   A hint/verified disagreement logs via `log_identity_mismatch`. No
   verified session -> guest mode (`sensitivity_override = "high"`, the
   same fallback the old "no speaker matched" case used, now for the
   correct reason), with one `log_identity_rejection` per unverified streak
   (a new `self._logged_missing_session` flag prevents logging every single
   guest utterance in a long unverified conversation — reset the moment a
   verified member is present again).
10. The old "explicit voice upgrade" cue (`_UPGRADE_TRIGGER`: a guest could
    say something to trigger a low-threshold voice rematch that directly
    set `self._member_id`) was the single clearest remaining load-bearing
    use of speaker_id in this codebase and could not be reconciled with the
    REQ's "speaker_id ... stops being load-bearing" — removed the
    identity-granting side effect; the cue now tells the speaker to select
    themselves from the dashboard instead of self-upgrading by voice alone.
11. Added `eval/harnesslib/layer1.py:run_p12` (registered in
    `eval/harness.py` after P11) — live, over HTTP, against the real
    harness-owned `/api/voice-query`: no-session 401 + a real
    `identity.rejected` HEL event lands; a verified session (written the
    same way `select-member` writes it, real `verify_turn` already having
    passed) admits with `identity_source=verified_session` and NO audio at
    all, proving admission doesn't depend on a speaker_id hint; the
    admitted turn's D-1 record carries `identity_verified=true` + the real
    fingerprint; clearing the session re-401s; `log_identity_mismatch`
    called directly lands a real `identity.speaker_mismatch` event.
    Deliberately does NOT synthesize a real speaker-id-vs-verified
    disagreement from fake audio (TD-127 + this dispatch's own OPEN item —
    see below).

## WHAT WAS FOUND

- `server/voice_https_orch.py:/api/voice-query` (old) and
  `server/voice_orch.py:OrchestratorGate._on_user_text` (old, the live
  mic pipeline) both matched the REQ's stated defect exactly:
  `self._member_id` / the routed member came directly from
  `get_member_by_voice`/per-turn Resemblyzer scoring, with no verified
  session concept anywhere in either process.
  `demo_dashboard.py` and `voice_https_orch.py`'s two `/api/text-query`
  gates (build steps 2/3) were unaffected by item 4 — they already bind to
  a signature, not a speaker_id.
- No existing cross-process channel existed between `demo_dashboard.py`
  (port 7871, where select-member/verify_turn already ran) and the voice
  server (port 7860, a separate process) — this is why item 4 needed the
  new `harness/voice_session.py` file-based bridge rather than an in-memory
  flag like `_vault_selected_member`.
- `eval/harnesslib/server.py:HarnessServer` runs the harness's own instance
  of `server.voice_https_orch` as a subprocess with `env=os.environ.copy()`
  — confirmed by reading the spawn call — so a file-path env override
  (`HIP_VOICE_SESSION_PATH`) or the shared default path both cross the
  process boundary the same way `HIP_REGISTRY_DB`/`HIP_KEYS_DIR` already do
  for build steps 1-3's tests.
- This worktree (`~/hip-roadmap-stage1-wip`) had no local `.env.dev` (it's
  gitignored, per-checkout, and this is a git worktree of `~/hip-dev`, not
  the directory that file already existed in) — copied from `~/hip-dev/.env.dev`
  to unblock running the harness at all; not a code change, not committed
  (still gitignored here).

## VERIFIED

- **UPDATE 2026-07-20 (Bill confirmed the box was free): ran the deferred
  proofs.** Sourced `.env.dev` (copied from `~/hip-dev/.env.dev` into this
  worktree, which had none — gitignored, per-checkout, not itself a code
  change), confirmed Neo4j `:7688`/Ollama `:11434`/`:11435` up, confirmed
  via `ps` that no other harness/voice process was running except the live
  untouched `:7860` demo, then ran
  `eval.harness --full` (venv python, `HIP_DEV_PYTHON`) end to end.
- **Watched run — P11 (build steps 2/3, unaffected by this dispatch):**
  `PASS` — u1 no-sig → 401/missing, u2 forged → 401/forged, u3
  maya's-sig-as-bill → 401/forged, valid sig admits bill/maya/sam, u7
  replay → 401/replay. Real HTTP bodies transcribed in the log, not
  inferred. No regression from this dispatch's changes.
- **Watched run — P12 (this dispatch's new scenario, real HTTP + real HEL,
  no mic/no fake audio):** `PASS`, all six checks, verbatim from
  `/tmp/step4_full_run.log`:
  - u1: no verified session → `401 identity_rejected: missing`.
  - u1b: that 401 landed a REAL `identity.rejected` HEL event
    (`reason=missing, source=voice-query`, real seq/hash/event_id in the
    chain — not asserted, the actual event dict is in the log).
  - u2: a verified session for `bill`, **zero audio supplied at all**,
    admits with `identity_source=verified_session` — proves admission
    does not depend on any speaker_id hint.
  - u3: that turn's real D-1 record carries `identity_verified: true` and
    `pubkey_fingerprint: 'b2f2373b6005f7ec'` (bill's real registered-key
    fingerprint, not a placeholder).
  - u4: clearing the session re-401s (proves the clear path actually
    revokes, not just that admission was never granted in u1).
  - u5: `log_identity_mismatch("bill", "maya", ...)` lands a real
    `identity.speaker_mismatch` HEL event with the correct payload.
- **Watched run — full `--full` (L1-L4, 100 iters, real dev Neo4j, live
  dashboard's shared registry, this checkout's own `.env.dev`):**
  completed clean end to end, 596 lines, no crash. `L6:record-invariants`
  (G1-G4) PASS, `SCHEMA` (ORTH-2, 46 cases) PASS, `VOICE` (BUILD-1
  conformance, 4 cases) PASS. Only ratchet line:
  `RATCHET FAIL — regressed vs baseline: ['L2:care_coordination.T01',
  'L2:care_coordination.T02', 'L2:three_zone_demo.T02']` — no separate
  "NEW FAILURES" line. Checked each by name against `docs/BACKLOG.md`
  rather than assuming: `care_coordination.T01`/`T02` match D-24's own
  documented signature (BACKLOG #15c; also independently confirmed in
  `DISPATCH_IDENTITY_BINDING_STEP2`, `DISPATCH_STEP2_CALLER_SIGNING`, and
  `DISPATCH_DEMO_PAYLOAD_PROOF`, all pre-dating this build);
  `three_zone_demo.T02` is D-21's own named signature, verbatim in
  `docs/BACKLOG.md` row 15 ("`--full` still fails `L2:three_zone_demo.T02`
  ... a residual ordinary stochastic miss"), itself observed recurring
  across multiple unrelated prior clean runs (`DISPATCH_DEMO_SCRIPTS`,
  `DISPATCH_FRONTIER_TIER_LIVE`). All three are pre-existing, independently
  documented, unrelated to identity binding — exactly what the ask
  predicted ("only known D-24/#15c reds"), plus the also-long-documented
  D-21 residual this branch's other dispatches have consistently tolerated
  too.
- **Live-mic proof (acceptance item 4's actual disagreement case: two real,
  different human voices, one claimed via a verified session, the other
  recognized by Resemblyzer) remains explicitly DEFERRED per Bill's own
  instruction — needs Bill at the box.** P12 (above) proves the
  mismatch-LOGGING mechanism and the session-authoritative GATE without a
  mic; it does not and cannot prove a live disagreement between two real
  voices without one.

## HASH

`cdff472130427e3b6b76e5ede31b1915342da25f` (code + this doc's original
checkpoint version landed together). This update adds no code, only the
VERIFIED section above and this doc's own status header.

## OPEN

- Live-mic proof for item 4's actual speaker-id-vs-verified disagreement
  case remains deferred to a session with Bill physically at the mic; P12
  covers everything provable without one (see VERIFIED). This is the only
  acceptance item not yet closed.
- The removed "explicit voice upgrade" cue (WHAT WAS DONE #10) changes
  live-demo behavior for an unenrolled/guest speaker who says the upgrade
  phrase: previously it could self-grant identity from voice alone; now it
  cannot, by design, per the REQ's own text. Called out explicitly to Bill
  as a demo-visible behavior change, not silently folded into the diff.
- `server/hip_client.html` and the standalone scripts/eval tools already
  flagged as OPEN in `DISPATCH_IDENTITY_BINDING_STEP2` remain unswept; this
  dispatch does not touch them (out of scope, same as step 2).
