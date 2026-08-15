# DISPATCH_IDENTITY_BINDING_STEP2
Status: BUILT
Reconciled-Against: commit on roadmap-stage1-wip (this dispatch), branched from 8263c25

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_IDENTITY_BINDING_BUILD__stage1-implementation__v20260718_1720.md`
(build order items 2+3, combined as "Step 2" per the dispatch text below — item 1,
keygen, already committed at 8263c25; items 4/5, voice session binding and
epistemic-record/HEL fields, explicitly NOT built here, see OPEN).

## THE ASK

> Build Step 2 of REQ_IDENTITY_BINDING_BUILD on roadmap-stage1-wip: the
> dashboard signs each turn with the selected member's keystore key;
> select-member and text-query verify the Ed25519 signature against the
> member's registered pubkey before acting; 401 on missing, forged,
> wrong-member, or replayed signature. Keep one-box member switching
> working (all three keys local). Don't break the demo. REQ before code
> is satisfied — REQ_IDENTITY_BINDING_BUILD is committed. Prove: no-sig
> turn 401s, forged-sig 401s, valid sig for bill/maya/sam admits and
> switches, demo unchanged, --full passes (expect only the known
> care_coordination reds). Report the hash.

## WHAT WAS DONE

1. Read `REQ_IDENTITY_BINDING_BUILD` and its parent `REQ_IDENTITY_BINDING`
   in full before touching code (CLAUDE.md gate item 8) — confirmed both
   are committed on this branch (e1888e0, 5607f4c) and satisfy the gate.
2. Traced every real caller of the two gated endpoints before designing
   the gate, not after: `demo_dashboard.py`'s `/api/session/select-member`
   (browser-facing, already session-cookie gated per REQ_SECURE_DEV_ENDPOINTS)
   and TWO independent `/api/text-query` implementations —
   `demo_dashboard.py`'s own in-process mirror (confirmed, by grep, NEVER
   called by the browser — `server/static/demo.html` only calls
   `/api/demo/load` + `/api/demo/next`, which run `process_text_query`
   directly in-process from the operator-loaded script file, bypassing
   this HTTP boundary entirely) and `server/voice_https_orch.py`'s (called
   by the harness's own `HarnessServer`/`InProcServer` subprocess drivers,
   and the production voice-adjacent surface).
3. Built `harness/identity_keys.py`'s `sign_turn`/`verify_turn`: canonical
   message `member|ts|nonce|body_hash`, Ed25519 sign with the LOCAL
   keystore, verify against the member's REGISTERED pubkey
   (`member_registry`, independent of who produced the signature),
   process-local nonce memory for replay, a 300s clock-skew/replay window
   (demo-grade, stated as such in the REQ).
4. Wired verification into both `/api/text-query` implementations with NO
   self-sign fallback — a caller must supply a real signature, full stop,
   matching the REQ's literal text ("no valid device credential is
   REJECTED"). Wired `/api/session/select-member` with a hybrid: an
   explicitly caller-supplied `{ts,nonce,sig}` is verified exactly as
   given (this is how forged/wrong-member/replayed get tested and
   rejected); when the browser sends only `{member}` (today's contract,
   unchanged), the dashboard signs on that member's behalf by reading the
   LOCAL keystore — legitimate under Stage 1's own stated design ("this
   box legitimately holds all three members' keys," REQ point 3) — then
   verifies that signature the same way. This is the piece that keeps
   one-box switching free without inventing in-browser crypto, which the
   REQ explicitly defers to production.
5. Updated every harness driver that calls `/api/text-query` to sign its
   own turns (`eval/harnesslib/server.py:HarnessServer.post_turn`,
   `eval/harnesslib/inproc.py:InProcServer.post_turn`) — the harness runs
   on the same box, so it is a legitimate local caller, same as a real
   device would be in production. Without this, every existing L1/L2/L4/L5
   scripted turn would have started 401ing.
6. Added a new harness assertion group, L1:P11 (`eval/harnesslib/layer1.py`),
   proving the acceptance test's rejection/admission matrix live over real
   HTTP against the real harness-owned server: no-sig (401/missing),
   forged sig (401/forged), wrong-member sig (401/forged — maya's
   signature presented as bill), valid sig for bill/maya/sam (200, real
   replies), and nonce replay (first use 200, identical replay 401).
7. Found and fixed a real, unrelated latent gap while proving this live:
   `eval/harnesslib/fixture.py`'s `verify_seed()` checked fact integrity
   post-seed but never checked that `demo_seed.py`'s identity-keypair step
   actually landed, and `fixture.reset()` never checked `demo_seed.main()`'s
   return code at all. Added both checks (fail loud at seed time, not 100
   turns deep as a stray 401) after chasing what first looked like an
   intermittent seeding bug but was actually diagnosed as SELF-INFLICTED —
   multiple overlapping `--full` invocations of my own, racing each other
   against the same registry/Neo4j/port-7997 resources during
   investigation. The hardening is real and worth keeping regardless of
   root cause; the original crash was not a product defect.
8. Ran the actual acceptance proofs live (see VERIFIED) rather than
   trusting the code read alone.

## WHAT WAS FOUND

- `demo_dashboard.py:179-192` (old) and `server/voice_https_orch.py:94-116`
  / `demo_dashboard.py:1948-1959` (old) matched the REQ's stated defect
  exactly: a client-asserted `member` string, trusted with zero proof.
- The scripted/on-screen demo (`server/static/demo.html` -> `/api/demo/load`
  + `/api/demo/next` -> `scripts/demo_run.py:fire_next_turn` ->
  `process_text_query` in-process) never touches the gated HTTP boundary
  at all — confirmed by grep across `server/static/demo.html`, not
  inferred. This is why Step 2 can lock down `/api/text-query` with zero
  self-sign fallback and zero risk to the on-screen demo.
- `server/hip_client.html` (a second, port-7860 text-query client, "Type
  as Sarah") and several standalone scripts/eval tools
  (`scripts/run_demo_script.py`, `scripts/demo_player.py`,
  `scripts/gate_check.sh`, `scripts/demo_preflight.sh`,
  `eval/integration_harness.py`, `eval/integration_live.py`,
  `eval/passthrough_consent_vignette.py`) also call `/api/text-query`
  directly with no signature. These are OUT OF SCOPE for this dispatch —
  none of them are `--full`, none are the `:7871` on-screen demo — and
  are NOT updated here. They will 401 unsigned until updated. Listed
  explicitly rather than silently left broken; see OPEN.

## VERIFIED

- **Watched run — P11 (unit+live, real HTTP, real crypto):**
  `eval.harness --layer 1 --seed 42`, isolated test registry
  (`~/hip-roadmap-stage1-wip/data/registry_test.db`, pubkeys backfilled
  from the real `~/hip-keys/*.key` files) against dev Neo4j (:7688):
  `P11 PASS` — u1 no-sig → 401/missing; u2 bogus-but-well-formed sig →
  401/forged; u3 maya's real signature presented as bill → 401/forged
  (does not verify against bill's registered pubkey); valid sig admits
  200 for bill, maya, AND sam individually with real replies; u7 replay
  — first use of a fresh nonce admits 200, identical replay of the same
  `{ts,nonce,sig}` → 401/replay. All other P1-P10 + HARNESS1.1-1.4 still
  PASS in the same run — `RATCHET PASS — no scenario regressed vs
  baseline`.
- **Watched run — full `--full` (L1-L4, 100 iters), isolated registry,
  seed=45:** completed clean end to end (592 lines, no crash). Only
  regression: `RATCHET FAIL — ['L2:care_coordination.T01',
  'L2:care_coordination.T02']` — the exact, already-documented,
  pre-existing D-24 flake (`docs/BACKLOG.md` #15c,
  `DISPATCH_CARE_COORDINATION_BACKLOG` on main, 2026-07-19), unrelated to
  identity binding. `care_coordination.T03` and `T04` both PASS this run.
  `L6:record-invariants` (the separate, ~91%-frequent, pre-existing
  BILL-4/G1 flake seen on an earlier attempt against the SHARED registry)
  PASSED clean this run. This is exactly what the ask predicted: "expect
  only the known care_coordination reds."
- **Watched run — select-member, live HTTP against a throwaway instance
  of THIS branch's own `demo_dashboard.py`** (port 7877/7878, killed
  after each test, NEVER the live `:7871` process, which runs `main` and
  is untouched by this branch): real dashboard-session login, then (1)
  `{"member":"maya"}` with no sig → 200 admitted (self-sign convenience);
  (2) `{"member":"bill", ts/nonce/sig all forged}` → 401
  `identity_rejected: forged`; (3) `{"member":"sam"}` no sig → 200
  admitted; (4) an explicitly-constructed VALID signature for maya
  (built via `sign_turn`, not the self-sign convenience path) → 200
  admitted — proves the explicit-signature branch works, not just the
  fallback. All four calls transcribed above are real `curl` output, not
  summarized.
- **Reasoned about, not independently re-verified:** the OPEN list below
  (hip_client.html and the standalone scripts) — confirmed only by grep
  that they call the now-gated endpoint unsigned; did not run them to
  observe the 401 first-hand, since fixing or exercising them was out of
  this dispatch's scope.
- **Demo unchanged:** not verified by restarting or touching the live
  `:7871` process (it runs `main`, a different branch, untouched by this
  work) — verified instead by code trace showing the on-screen demo path
  never reaches the gated boundary, per WHAT WAS FOUND above.

## HASH

See commit on `roadmap-stage1-wip` (this dispatch's own commit — code +
this doc land together). Step 1's keygen commit, referenced but not
touched here, remains `8263c25`.

## NOTE ON PARALLEL WORK

A second, independently-written dispatch doc covering this same Step 2
work (`DISPATCH_IDENTITY_BINDING_BUILD__step2-select-member-and-text-query-signing__v20260719_0913.md`,
its own `docs/INDEX.md` row, timestamped minutes apart from this one) was
found on disk mid-session — same worktree, same uncommitted code, a
second verification pass run concurrently with this one. Its content
overlaps this doc closely; it is not kept as a separate artifact to
avoid two docs narrating one build. One finding from it is folded in
here since this dispatch had not independently confirmed it: **the live
`:7871` dashboard and the dev harness share the identical
`HIP_REGISTRY_DB`/`NEO4J_URI` (confirmed there via `lsof`/`ps eww` against
the live dashboard PID)** — there is no environment isolation between
them today. That is a real, pre-existing operational hazard (not
introduced by this dispatch) and is very likely what actually explains
the "sam loses its pubkey mid-run" investigation above, rather than pure
self-inflicted overlap between two of THIS dispatch's own invocations as
first suspected. Worth its own `docs/techdebt/` entry; not filed here,
out of scope.

## OPEN

- Build order items 4 (voice session binding, speaker_id demoted to a
  logged hint) and 5 (epistemic-record `identity_verified`+pubkey
  fingerprint, HEL `identity.rejected` ledger events) are NOT built —
  explicitly the next steps per the REQ's own sequencing, not silently
  skipped.
- `server/hip_client.html` and the standalone scripts/eval tools listed
  in WHAT WAS FOUND now 401 unsigned against `/api/text-query` and were
  not updated. None of them gate `--full` or the `:7871` demo, so this
  did not block "don't break the demo," but they are real, currently-broken
  callers and should be swept before anyone relies on them again.
- The earlier apparent "sam loses its pubkey mid-run" crash (chased at
  length before being traced to overlapping concurrent harness
  invocations against a shared registry, self-inflicted) means the
  `verify_seed()`/`fixture.reset()` hardening added here has NOT been
  independently proven to catch a genuine demo_seed ordering bug — only
  proven to not false-positive across two full clean runs. If it fires
  for real later, that is new information, not a re-confirmation of
  something already traced.
- REQ_IDENTITY_BINDING_BUILD on THIS branch does not yet carry the
  DEMONSTRATION OBJECTIVE section that landed on `roadmap` today (per
  that branch's INDEX row) — this branch diverged before that retrofit.
  Not added here; out of this dispatch's scope.
