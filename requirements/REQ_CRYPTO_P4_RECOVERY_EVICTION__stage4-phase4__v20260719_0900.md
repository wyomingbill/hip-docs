# REQ_CRYPTO_P4_RECOVERY_EVICTION: Stage 4 Phase 4 — Recovery and Custody Exit
Version: v20260719_0900
Status: NOT MET
Branch: roadmap
Reconciled against: REQ_CRYPTO_P1_DYAD_KEYS, P2, P3 (MET first); REQ_PARTITION_CUSTODY D2 (quorum composition); dyad spec 601ac25 s5-s6; REQ_CRYPTO_HARNESS (N3)

## What this is

The last crypto phase, and the one where cryptography meets the legal surface. It builds two operations that turn out to be the SAME primitive:

1. Recovery: a member lost their device/key; the household regains access to their sealed data without the operator being able to do it alone.
2. Custody exit / eviction: a custodian leaves a dyad, cooperatively or not; their old key must stop working, and someone must be able to remove them even without their cooperation.

Both are a 2-of-3 threshold operation over the same three shares. The quorum that reconstructs a lost key is the quorum that revokes a custodian. Build it once.

## Why exit is here and not Phase 1

Phase 1 built entry (grant a custodian a key). Exit was deferred to here because exit requires RE-ENCRYPTION so the old key dies, and re-encryption is the Phase 2 re-seal machinery. Exit = revoke + re-seal the dyad's facts to a fresh dyad key that the exited custodian was never given. Without Phase 2's re-seal, exit would be "stop showing them the data" (a filter) instead of "the old key no longer decrypts" (crypto). We build the real one.

## The three shares (Stage 2 decision D2, ratified here)

Any 2 of 3 reconstruct a member/dyad key or authorize an eviction:
- Share A: operator escrow. Held by the operator. Cryptographically insufficient ALONE — this is what preserves operator-blind: the operator holding one share cannot recover or evict by itself.
- Share B: household admin (Bill, in the demo).
- Share C: a second family principal OR a verified legal instrument (a PoA credential).

2-of-3: any two agree. The operator can participate but never acts alone. A family can act without the operator (B+C). A legal instrument can substitute for the second family principal (contested PoA, estrangement).

## The operations

RECOVERY (lost key):
- Two share-holders present shares; the threshold reconstructs the member's key material (or a re-wrap of it to a new device key).
- HEL event: key.recovery, recording which two shares were used.

CUSTODY EXIT (cooperative):
- Custodian consents to leave. Dyad re-keys: new D_priv, facts re-sealed to the new key, exited custodian's wrap removed.
- Old key is dead forward (N3). HEL event: custody.exit.

EVICTION (non-cooperative):
- Same re-key + re-seal, but authorized by 2-of-3 quorum instead of the custodian's consent. The custodian does not participate; the quorum removes them.
- HEL event: custody.evict, recording the two shares used and the reason code (dispute / abuse / death / estrangement).

The exit and eviction produce identical cryptographic outcomes (old key dead, facts re-sealed). They differ only in authorization: consent vs quorum. Same primitive, two doors.

## The honest limit, built in

Exit means NO NEW ACCESS. It does not unremember. A custodian who read facts before exit still knows them and may have copied them. Re-encryption kills future decryption of the store; it cannot retract what a human already saw. This is stated in every ledger event, every demo script, every doc. Do not design around it or imply otherwise.

## THE ACCEPTANCE TEST (pass/fail)

Turns green:
- N3: after custody exit or eviction, the removed custodian's old key cannot decrypt any re-sealed fact. Count of post-exit successful decrypts with the old key: 0.

New assertions:
- RE1: 2-of-3 threshold — any two shares reconstruct/authorize; any one share alone cannot. Count of single-share successes: 0. This is the operator-blind-preserving property: prove the operator's share alone does nothing.
- RE2: recovery restores a lost member's access (right party regains read) without the operator acting alone. Positive-half: locked-out-after-recovery count: 0.
- RE3: eviction (non-cooperative) produces the same dead-old-key outcome as cooperative exit. The evicted custodian's key fails on re-sealed facts; the remaining custodians still read.
- RE4: every recovery/exit/evict emits an ordered, hash-chained HEL event with the shares used and (for evict) a reason code. Ledger completeness: 0 unlogged custody changes.
- RE5: overlapping dyads — evicting a custodian from maya-ray does NOT affect sam-ray, even though both concern ray. Re-key is scoped to the one dyad.

Fault-injection (mandatory): attempt recovery/eviction with a single share; RE1 must reject it. Leave the old wrap in place after eviction (skip re-seal); N3 must go red. Prove the threshold and the re-seal both actually gate.

## DEMONSTRATION OBJECTIVE

Co-equal to the build. Not rigged. This is the demo that answers "what happens in a divorce / a death / an abuse case" — the questions every eldercare buyer asks.

SHOW: Evict a custodian by quorum (B+C, no operator, no custodian consent). Show their old key now fails on the dyad's facts, while the remaining custodian still reads. Then show the operator alone trying to recover or evict with only share A: it cannot. Then the ledger: every custody change logged, ordered, with the reason.

LET THEM RUN: Let the engineer play each role. Hold only the operator share and try to act alone: fail. Hold two family shares and evict: works. Take the evicted key and try to read a re-sealed fact: fail. Check the ledger themselves.

THE CLAIM IT PROVES: "Custody changes are enforced by cryptography and authorized by a quorum the operator cannot satisfy alone. A family can remove a bad actor without us; we can never remove one without the family. And every change is on an audit trail no one can edit."

THE HARDEST QUESTION + HONEST ANSWER: "You evicted the custodian, but she already saw the mother's medical history. You have not protected anything." Answer, limit stated first: correct, and we never claim otherwise. Exit means no NEW access, not amnesia. What eviction guarantees is that from this moment the removed custodian's key decrypts nothing further, every future fact is sealed away from her, and the removal is on an immutable ledger. We protect the forward boundary and the audit trail. We do not claim to erase human memory or copies already made — no honest system can, and a system that claimed to would be lying. The value is real: a estranged or abusive custodian is cut off going forward, provably, without the operator's unilateral power and without waiting on the operator at all.

## CONSTRAINTS

- Recovery and eviction are ONE primitive (threshold re-key). Do not build two mechanisms.
- The operator's single share must be provably insufficient alone (RE1). This is the operator-blind property extended to custody; if the operator can recover or evict alone, the phase failed.
- Exit/eviction re-seals; it does not filter. The old key must actually fail (N3), verified cryptographically, not by hiding rows.
- Re-key is dyad-scoped (RE5). One dyad's eviction never re-keys another.
- The "no new access, not unremembers" limit appears in every ledger event and every demo script. Never imply erasure.
- Reason codes on eviction are recorded but the system does not adjudicate them — humans manage the relationship, the system enforces the boundary (the standing dyad principle).
