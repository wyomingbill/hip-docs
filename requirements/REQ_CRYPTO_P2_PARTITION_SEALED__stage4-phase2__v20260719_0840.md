# REQ_CRYPTO_P2_PARTITION_SEALED: Stage 4 Phase 2 — Partition Sealed Cryptographically
Version: v20260719_0840
Status: MET
Branch: roadmap-crypto-p2
Reconciled against: REQ_CRYPTO_P1_DYAD_KEYS (Phase 1, MET first — dyad keys exist); REQ_PARTITION_CUSTODY (the write rule); REQ_CRYPTO_HARNESS; crypto design 47851d7 s2, s4-s5 (the ~11 key-derivation sites); encryption.py:117-123

UPDATED 2026-07-20: MET as of 1e549a8, branch `roadmap-crypto-p2`. Proof is
the layer-7 sandbox pass on the dev graph (bolt://localhost:7688, mini):
`python -m eval.harness --layer 7` -> `== L7: 19/19 (0 flaked, 0 skipped)`,
RATCHET PASS, no scenario regressed vs baseline. That run covers this REQ's
acceptance slate — N1/N4/P1/P4 turned green, PS1 (server-derivation audit:
0 unaccounted call sites outside the allowlist, v2 fact not server-derivable
from its owner string), PS2 (no v2 encrypted_dek unwraps via
Fernet(_derive_key(owner))), PS3 (re-seal round-trip, one fact per class,
old v1 path fails after), PS4 (dual-envelope coexistence), and both
PS1/PS2 fault injections provably flip red on a mislabeled master-sealed
fact. Still pending, NOT claimed here: the real-graph migration on the mini
— existing v1 facts remain master-sealed until Phase 3's re-seal cutover
runs against the live graph; this REQ built and proved the re-seal function
only. See DISPATCH_CRYPTO_P2_VERIFY__layer7-sandbox-19of19__v20260720_2115.md.

## What this is

The phase that makes the partition a cryptographic fact instead of a filter. Today, member separation is a WHERE clause and one master key opens everything. This phase seals each fact's DEK to the reader-set its class allows, and removes every path where the server derives a key it should not have.

After Phase 1, dyad keys exist but the store still runs on the master envelope. After this phase, new writes are sealed by class (member-private to the author's key, dyad-private to the dyad key, household-shared to the household key tree), and the server can no longer decrypt a fact just because it is the server. The master key still exists (destroyed in Phase 3), but the code paths that abuse it are closed here.

This is the highest-risk phase. It touches the sites that currently make isolation theatre. Get it wrong and either the demo breaks (facts unreadable) or the wall has a hole (server still derives keys). Both are caught by the Stage 3 harness, which is why the harness came first.

## The core change

1. Household key tree: an X25519 household keypair. HH_priv wrapped per adult member (sealed to each member's pubkey), stored like dyad wraps. Household-shared facts seal their DEK to HH_pub. Every adult unwraps HH_priv via their device key, then the DEK.

2. Seal-by-class on write: when a fact is written, the Stage 2 rule assigns its class, and the DEK is sealed to:
   - member-private -> the author's member pubkey only
   - dyad-private -> the owning dyad's D_pub (Phase 1)
   - household-shared -> HH_pub
   No DEK is sealed to the master key. No DEK is sealed to an operator key. This is where fail-private lands cryptographically: unknown class -> member-private -> author only.

3. Close the derivation sites: the ~11 server-side sites where _derive_key(owner) or decrypt_fact_value(ct, dek, owner) let the server compute any owner's key. The chief one is encryption.py:117-123. Each site is changed so decryption requires an unwrapped key the CALLER holds, not a key the server derives. If any site can still server-derive after this phase, the phase has failed regardless of green tests — audited explicitly (see acceptance).

4. Dual-envelope, still: new writes are v2 (sealed by class). Existing v1 facts (master envelope) still read via the old path until Phase 3's migration re-seals them. key_version distinguishes. The demo keeps running throughout.

## The migration question this phase must answer, not dodge

Existing facts are v1 (master-sealed). New facts are v2 (class-sealed). Phase 3 destroys the master key. Something must re-seal the v1 facts to v2 BEFORE the master key dies, or they become unreadable forever. This phase builds the re-seal function (read under master, re-seal by class, write v2) but does not run the destructive cutover — that is Phase 3. The re-seal function is built and tested here so Phase 3 is a switch, not a new build.

## THE ACCEPTANCE TEST (pass/fail, extends the harness)

Turns green (were expected-red):
- N1: a member key cannot decrypt a fact not sealed to it. Count: 0.
- N4: a dyad-private fact never appears in a household-scoped query. Count: 0.
- P1: every household adult can read every household-shared fact. Locked-out count: 0.
- P4: the Stage 2 write-rule table (rows 1-9) classifies AND seals every row to the correct reader-set.

New assertions:
- PS1: THE SERVER-DERIVATION AUDIT. For every one of the ~11 sites, assert the server cannot produce plaintext without a caller-held key. This is the phase's whole point. Enumerate the sites, prove each is closed. Count of server-derivable facts: 0.
- PS2: no DEK is sealed to the master key on any v2 write. Count: 0.
- PS3: the re-seal function converts a v1 fact to v2 preserving plaintext, sealing to the correct class. Round-trip proven on one fact per class.
- PS4: dual-envelope coexistence — v1 and v2 facts both readable through their correct paths in the same run.

Fault-injection (mandatory): re-open one derivation site (let the server derive a key); PS1 must go red. Seal a DEK to the master key; PS2 must go red. Prove the audits can fail.

## DEMONSTRATION OBJECTIVE

Co-equal to the build. Not rigged.

SHOW: Two things an engineer wants to see. First, the write rule sealing live: write facts of each class, show each DEK sealed to a different reader-set, none to the master. Second, THE DERIVATION AUDIT: the enumerated list of the sites that used to let the server read anything, each now shown closed, with the fault-injection proving the audit turns red if a site reopens.

LET THEM RUN: Let the engineer act as the server — hold no member key, hold the master key if it makes them happy — and try to decrypt a v2 member-private or dyad-private fact. It fails. That is the operator-blind property arriving (fully complete after Phase 3, but the server-can't-derive half is provable here).

THE CLAIM IT PROVES: "Isolation is now cryptographic, not a query filter. The server cannot read a class-sealed fact because it does not hold the key, and we enumerate every place it used to be able to and show each closed."

THE HARDEST QUESTION + HONEST ANSWER: "The master key still exists on disk. So the server CAN still read everything, you just changed the code not to. That is a policy wall, not a crypto wall." Answer, limit stated first and this is the honest one: correct, until Phase 3 the master key exists and old v1 facts are still master-sealed, so this phase closes the CODE paths but not the KEY. The crypto wall is not complete until Phase 3 destroys the master key and the last v1 fact is re-sealed. What this phase proves is that NEW facts are sealed by class with no master path, and that every derivation site is closed and stays closed under test. We do not claim operator-blind yet. We claim the machinery for it is built and audited. Phase 3 makes the claim true.

## CONSTRAINTS

- The demo must run after this phase. Dual-envelope guarantees it: nothing is destroyed.
- The derivation audit (PS1) is the acceptance bar. A green harness with an unclosed site is a failed phase. Enumerate the sites from the crypto design (~11) and close each; do not stop at the chief one.
- No DEK ever sealed to master or operator key on a v2 write (PS2), no exceptions.
- The re-seal function is built and tested here but NOT run destructively. Phase 3 owns the cutover.
- If the local model needs plaintext at query time (it does — accepted limit), that plaintext comes from the CALLER's unwrapped key path, never from a server-derived key. The model seeing plaintext is not the same as the server being able to derive it.
