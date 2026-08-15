# REQ_MASTERKEY_PATH: default master-key path fix
Status: MET
Reconciled-Against: 8add390
Version: v20260718_1745
Branch: fix-masterkey-path

## STATUS NOTE (post-commit)
Acceptance items 1-2 live-verified before commit. Item 3 (--full): zero
fernet/InvalidToken failures -- this REQ's bug is fixed. Two unrelated
inference-layer timeouts (L3:INJ-7, L4:PW027) appeared in the same --full
run; traced to server/voice_orch.py:3238 (local-Ollama APITimeoutError,
strictly downstream of decryption/access-control), reproduced clean 3/3 on
manual retry, and correlated with two duplicate `ollama serve` daemons found
running on this box since before this session (PID 1399 since Jul 11, PID
937 since Jun 3). Confirmed pre-existing, not fix-induced -- filed as its
own backlog item, not folded into this REQ.

## THE REQUIREMENT
The harness, demo_seed, and manual runs must read the same master key the live
dashboard uses, so encrypted facts decrypt. Today they do not.

## ROOT CAUSE (measured)
HIP_MASTER_KEY is a file-path override, not a key value. The launchd dashboard's
plist points at ~/hip-dev/data/encryption/.master_key. The code default
DEFAULT_MASTER_KEY_PATH points at ~/hip-harness/data/encryption/.master_key, a
stale file created before this divergence. Live graph: 11/11 active facts decrypt
under the hip-dev key, 0/11 under hip-harness. One population, all under hip-dev.
Predates identity-binding by ~2 weeks.

## THE FIX
Set DEFAULT_MASTER_KEY_PATH to ~/hip-dev/data/encryption/.master_key so every
process resolves to the live key with no env override needed. Env override still
honored. The hip-harness file is orphaned; no re-encryption needed.

## ACCEPTANCE (pass/fail)
1. With no HIP_MASTER_KEY set, the module resolves to the hip-dev key.
2. The baseline query that threw fernet InvalidToken now decrypts clean.
3. --full shows no fernet/InvalidToken failures. Remaining fails are only the
   known pre-existing flakes (D-21, D-24, INJ-3), not this bug.

## CONSTRAINTS
Do not re-encrypt or touch the graph. Do not touch main. Env override stays
functional. This is separate from REQ_IDENTITY_BINDING; do not fold into it.
