# REQ_CRYPTO_P3_OPERATOR_BLIND: Stage 4 Phase 3 — Operator-Blind at Rest
Version: v20260719_0850
Status: NOT MET
Branch: roadmap
Reconciled against: REQ_CRYPTO_P2_PARTITION_SEALED (MET first — re-seal function exists, sites closed); REQ_CRYPTO_HARNESS (N5, R7); crypto design 47851d7 s6 (migration); dyad spec 601ac25

## What this is

The phase that makes operator-blind true instead of built. Phase 2 closed the code paths and sealed new facts by class, but the master key still exists on disk and old facts still read through it. This phase runs the migration cutover: re-seal every remaining v1 fact to v2, then DESTROY the master key. After this phase, there is no key on the server that decrypts member data. An operator with full database and disk access reads ciphertext and nothing else.

This is the phase the entire trust claim depends on. Before it, "we can't read your data" is a policy statement. After it, it is a cryptographic fact you can hand an engineer to verify.

It is also irreversible. Destroying the master key means any v1 fact not re-sealed first is lost forever. The ordering is not negotiable: re-seal all, verify all, THEN destroy.

## The cutover, in strict order

1. Re-seal sweep. Run the Phase 2 re-seal function over every v1 fact: read under master, seal by class to v2, write. No fact skipped. This is idempotent and resumable (it can be interrupted and restarted without corruption).
2. Completeness proof. Assert zero v1 facts remain. Every fact is v2, sealed to a member/dyad/household key, none to master. This gate must pass before step 3. If one v1 fact remains, STOP — destroying the key now loses it.
3. Key destruction. Remove the master key from disk. Overwrite, not unlink. Confirm no copy remains in backups, swap, logs, or process memory dumps. The key file is gone and unrecoverable.
4. Verification. Re-run the full harness. N5 (no operator-decryptable fact) and R7 (operator reading the raw store decrypts nothing but their own) must now pass. Every P-invariant (right party can still read) must still pass — destroying the key must not lock out legitimate members.

## The irreversibility gate

Step 2's completeness proof is the safety interlock. It is not a test that reports a number; it is a HALT. The destruction step (3) does not run unless step 2 proves zero v1 facts remain. Build it so key destruction is physically gated behind the completeness proof passing — not a human remembering to check. A backup of the master key is retained OUT of band until step 4 verification passes, then that backup is destroyed too. Belt and suspenders on the one irreversible action.

## THE ACCEPTANCE TEST (pass/fail)

Turns green (the whole point):
- N5: no fact's DEK is decryptable by any operator-held key. Count of operator-decryptable facts: 0. Previously expected-red since Stage 3; this phase makes it pass.
- R7: the red-team operator (raw store + disk access, every key the operator legitimately has) decrypts only facts sealed to keys they hold as a member, nothing else. For a pure operator holding no member key: zero facts decrypt.

Must STILL pass (no regression from key destruction):
- P1, P2, P3: household / dyad / author reads all still work. Destroying the master must not lock out a single legitimate reader.
- N1-N4: all isolation invariants hold.

New assertions:
- OB1: zero v1 (master-sealed) facts remain in the store after cutover. Count: 0.
- OB2: the master key file does not exist on disk, in backups, or in the retained out-of-band location after step 4. Count of recoverable master-key copies: 0.
- OB3: the completeness gate (step 2) provably HALTS destruction when a v1 fact is present. Tested by injecting a stray v1 fact and confirming destruction does not run.

Fault-injection (mandatory): inject one un-re-sealed v1 fact before cutover; OB3 must halt the destruction. Restore a master-key copy in a backup path; OB2 must go red. Prove the interlocks fire.

## DEMONSTRATION OBJECTIVE

Co-equal to the build. This is the demo that closes an investor or an operator's security team. Not rigged.

SHOW: The cutover, then the proof. Run the re-seal sweep, show zero v1 remain, destroy the key on screen. Then become the operator: full disk, full database, the deleted key is gone. Try to read a member's fact. Ciphertext. Try every recovery — swap, backup, logs. Nothing. The wall is now the key's absence, not the code's politeness.

LET THEM RUN: This is the strongest proof in the whole system. Hand the engineer root on the box. Let them search for the master key, dump memory, read the raw store, run the decrypt function as the server. Let them try to read Ray's medication as the operator. It cannot be done, and they proved it themselves, with root.

THE CLAIM IT PROVES: "The operator cannot read customer data. Not 'does not' — cannot. There is no key on this machine that decrypts it, and you just verified that with root access."

THE HARDEST QUESTION + HONEST ANSWER: "The local model reads plaintext at query time to answer. So the operator CAN read the data — just snapshot memory during a query." Answer, limit stated first and unflinching: yes. This phase makes the operator blind AT REST and in the database. At inference time, the caller's key unwraps the fact and the local model sees plaintext in RAM for that turn; an operator who compromises the running host during an active query for that user can read that turn's data. That is the accepted boundary of this roadmap — enclaves close it and are a later tier, out of scope here. What we eliminated is the far larger exposure: the operator reading the whole store at leisure, any user, any time, from disk. We traded "read everything, always" for "maybe read one active turn if you compromise the live host in the moment." State that trade honestly; it is a strong one and it survives scrutiny precisely because we do not overclaim it.

## CONSTRAINTS

- Ordering is law: re-seal all, prove complete, destroy, verify. Destruction is gated behind the completeness proof as a physical interlock, not a checklist.
- Idempotent, resumable re-seal. A crash mid-sweep must not lose or double-seal a fact.
- Out-of-band master-key backup retained until step 4 verification passes, then destroyed. This is the only safe copy during the irreversible window.
- Do NOT claim operator-blind at inference. The claim is at-rest and in-store. Every demo script and doc states the inference-time limit in the same breath as the claim.
- The demo must still run after cutover. If any legitimate reader is locked out, the phase failed — P-invariants are the guard.
