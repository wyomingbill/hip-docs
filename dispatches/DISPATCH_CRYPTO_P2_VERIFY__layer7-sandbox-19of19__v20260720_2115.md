# DISPATCH_CRYPTO_P2_VERIFY
Status: BUILT
Reconciled-Against: 1e549a8

**TYPE:** MEASUREMENT

**REQ:** `docs/requirements/REQ_CRYPTO_P2_PARTITION_SEALED__stage4-phase2__v20260719_0840.md`

## THE ASK

Two dispatches in one session, verbatim:

> Lean verify ONLY layer 7 crypto — NOT the 100-iteration --full that keeps
> dying. Report: does PS1 (derivation audit, ~11 sites closed, 0
> server-derivable) pass? PS2 (no DEK to master)? Any layer-7 crypto
> invariant fail? If the process is killed again, say so — then it's a
> memory problem bigger than one daemon and we stop and fix the box, not
> the build.

> push roadmap-crypto-p2 to origin from this scratchpad worktree. Then mark
> REQ_CRYPTO_P2_PARTITION_SEALED status MET as of 1e549a8 — proof is the
> layer-7 19/19 sandbox pass, note real-graph migration still pending on
> the mini. Commit, push, report the hash.

## WHAT WAS DONE

1. Session started on the laptop (Bills-MacBook-Pro), which the dispatch's
   runbook did not fit: no `~/hip-roadmap-crypto-p2` worktree, no `.env.dev`
   anywhere on disk, no Neo4j install at all (only the Python driver), zero
   ollama processes. Recreated the worktree there from
   `origin/roadmap-crypto-p2` (tip 1e549a8) so both machines carry it.
2. Moved to the mini (`[REDACTED-USER]@[REDACTED-MACHINE-NAME]`) over SSH — the box
   the runbook actually describes. Confirmed its worktree is at the same
   1e549a8, dev graph open on 7688, `.env.dev` present.
3. Did NOT kill either ollama daemon. The "duplicate" premise is wrong:
   config.yaml:4-7 deliberately runs two instances — :11434
   (extraction/embedding) and :11435 (classifier-only, the INFRA-1
   isolation note). PID 1399 serves 11435, PID 37901 serves 11434, both
   answered HTTP 200. The memory pressure is the model-runner child
   processes, releasable via `ollama stop <model>` without touching daemons.
4. Ran the lean verify on the mini: `source .env.dev` +
   `python -m eval.harness --layer 7` (GROQ_API_KEY comes from the mini's
   `~/.zshrc`, which non-interactive SSH does not source — had to source it
   explicitly).
5. Marked the REQ MET in place (Status line + UPDATED note), matching the
   REQ_CRYPTO_P1_DYAD_KEYS precedent; wrote this dispatch doc; pushed
   `roadmap-crypto-p2`.

## WHAT WAS FOUND

- `== L7: 19/19 (0 flaked, 0 skipped)`, exit 0, RATCHET PASS, no scenario
  regressed vs baseline. The process was not killed — the OOM theory never
  got tested because layer 7 needs no server stack
  (eval/harness.py:261 `needs_server` covers layers {1,2,4,5} only).
- PS1 PASS: 0 unaccounted `decrypt_fact_value`/`encrypt_fact_value`/
  `_derive_key` call sites outside the allowlist
  (eval/harnesslib/layer7_crypto.py:89 `_PS1_ALLOWLIST`); the v2 fact is
  not openable via the v1 server-derivable path (`server_derivable=False`).
- PS2 PASS: no v2 fact's `encrypted_dek` unwraps via
  `Fernet(_derive_key(owner))` (`dek_opens_via_master=False`).
- PS1/PS2 fault injections both PASS: a fact mislabeled `key_version=2`
  but actually master-sealed flips each red — the audits are not
  vacuously green.
- Full slate green: N1/N2/N4, P1/P2/P4, DK1/DK3/DK4, PS3 (re-seal
  round-trip per class, v1 path fails after), PS4 (dual-envelope
  coexistence), write-rule rows 1-9 classify AND seal correctly, HEL
  custody chain verifies (848 events, 795 encrypted, 0 tombstoned).

## VERIFIED

- **Watched run:** the layer-7 harness run on the mini against the real
  dev graph (bolt://localhost:7688), twice — once for the full scenario
  output, once re-run to capture the `== L7: 19/19` header before writing
  that number into the REQ. Ollama port/PID mapping watched via
  `lsof -nP -iTCP -sTCP:LISTEN` on the mini.
- **Reasoned about:** the OOM cause of prior `--full` deaths (not
  reproduced — this dispatch deliberately avoided `--full`); the
  model-runner-children-hold-the-memory claim (from process list + ollama
  behavior, not from a measured before/after).

## HASH

The commit carrying this doc, the REQ MET flip, and the INDEX row —
recorded in git as the tip of `roadmap-crypto-p2` at push time (child of
1e549a8; verification target itself unchanged at 1e549a8).

## OPEN

- Real-graph migration on the mini is NOT done: existing v1 facts remain
  master-sealed until Phase 3's re-seal cutover runs against the live
  graph. This dispatch proved the re-seal function (PS3), not the cutover.
- CLAUDE.md item 12 (full ratchet before "done") is satisfied for this
  REQ's own acceptance slate but `--full` (100-iteration) has NOT run
  green on this branch — it was dying on the mini before this session,
  cause still undiagnosed. Next `--full` attempt: try
  `ollama stop <loaded models>` first, keep both daemons.
- Why the laptop lost its worktree/.env.dev is unexplained.
