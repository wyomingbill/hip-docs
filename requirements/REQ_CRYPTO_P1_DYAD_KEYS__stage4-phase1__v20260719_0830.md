# REQ_CRYPTO_P1_DYAD_KEYS: Stage 4 Phase 1 — Dyad Custodial Keys
Version: v20260719_0830
Status: MET
Branch: roadmap-crypto-p1
Reconciled against: REQ_PARTITION_CUSTODY (Stage 2, MET first); REQ_CRYPTO_HARNESS (Stage 3, invariants exist first); dyad spec 601ac25 s2-s4; crypto design 47851d7 s2.1

UPDATED 2026-07-20: Built and MET on branch `roadmap-crypto-p1`. Prerequisite
gap found and handled explicitly, not silently assumed: REQ_PARTITION_CUSTODY
(Stage 2) and REQ_CRYPTO_HARNESS (Stage 3) were both still `NOT MET` in the
actual codebase when this phase started — no dyad/crypto-harness code
existed anywhere, only the two design/policy docs. Resolved by (1) getting
Bill's explicit ratification of REQ_PARTITION_CUSTODY's D1/D2/D3 in-session
before building (see that REQ's own UPDATED note), and (2) building the
minimal slice of REQ_CRYPTO_HARNESS's proposed L7-CRYPTO layer this phase's
OWN acceptance test needs — N2, P2, DK1-DK4, and the mandatory fault
injection — not that REQ's full N1/N3-N6/P1/P3/P4/R1-R7/L1-L3 scope, which
remains its own separate, not-yet-built REQ. See
DISPATCH_CRYPTO_P1_DYAD_KEYS__stage4-phase1-build__v20260720_0910.md for the
full account, hash, and --full result.

## What this is

The first crypto build phase. It creates the dyad as a real cryptographic object: a keypair the custodian holds on the care recipient's behalf, so a care recipient's private facts can be sealed to their caregivers and no one else. This is the mechanism the whole eldercare pitch rests on.

It builds only the dyad key machinery. It does NOT yet re-seal the fact store (that is Phase 2) or destroy the master key (Phase 3). After this phase, dyad keys exist and can seal/unseal, running alongside the current master-key envelope. Dual-envelope by key_version, per the migration plan.

## Prerequisites

- Stage 1 identity: each member has a device keypair (built, committed 8263c25). The dyad key is sealed TO a member's public key, so member keys must exist first. They do.
- Stage 2 partition: the class "dyad-private" is defined, and the write rule routes subject-in-active-dyad facts to a dyad. This phase builds the keys those facts will be sealed to.
- Stage 3 harness: invariants N2 (dyad isolation) and P2 (custodian can read) exist as tests, currently expected-red because no dyad keys exist. This phase turns them green.

## What gets built

1. Tables (per dyad spec):
   - dyads: dyad_id, recipient_ref, status (active/exited), created_at.
   - dyad_members: dyad_id, custodian_member_id, role, added_at, removed_at.
   - dyad_key_wraps: dyad_id, custodian_member_id, wrapped_D_priv (D_priv sealed to that custodian's member pubkey), key_version.

2. Dyad keypair: an X25519 keypair per dyad. D_pub is stored plainly (it seals things). D_priv is never stored in the clear; it is sealed to each custodian's member public key and stored in dyad_key_wraps, one row per custodian.

3. Two-hop unwrap: a custodian reads a dyad-private fact by: member_privkey (on device) unwraps D_priv from their dyad_key_wraps row, then D_priv unwraps the fact DEK. Two hops, both client-holdable.

4. Seal-to-dyad: given a fact classified dyad-private (Stage 2 write rule), its DEK is sealed to the dyad's D_pub. Any current custodian can unwrap; no one else can.

5. Enrollment (entry): adding a custodian to a dyad seals D_priv to their member pubkey, writes a dyad_key_wraps row, and emits a HEL custody.grant event. For the demo, the fixture pre-enrolls the dyads: maya-ray and sam-ray (overlapping on ray, per the spec's care-circle example).

## What does NOT get built here

- Re-sealing existing facts (Phase 2).
- Master key destruction / operator-blind (Phase 3).
- Exit re-encryption and recovery quorum (Phase 4). Entry is built here; exit is Phase 4, because exit's re-seal depends on Phase 2's re-seal machinery.

## THE ACCEPTANCE TEST (pass/fail, extends the Stage 3 harness)

Turns green (were expected-red):
- N2: a key outside the owning dyad cannot decrypt a dyad-private fact. Count of cross-dyad decrypts: 0.
- P2: every current custodian of a dyad can decrypt that dyad's facts. Count of locked-out custodians: 0.

New assertions this phase adds:
- DK1: D_priv is never stored in plaintext anywhere. Grep + store inspection: 0 plaintext D_priv.
- DK2: two-hop unwrap works end to end for maya on maya-ray and sam on sam-ray.
- DK3: overlapping dyads — ray is in both maya-ray and sam-ray; a fact sealed to maya-ray is readable by maya, NOT by sam (different dyad, even though both are ray's caregivers). This proves dyads isolate, not just "caregivers vs not."
- DK4: a custody.grant HEL event exists for every dyad_key_wraps row, hash-chained and ordered.

Fault-injection (mandatory): break the seal-to-dyad so a DEK is sealed to the wrong D_pub; N2/P2 must go red. Prove the tests can fail.

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, co-equal to building the keys. We do not rig it.

SHOW: Seed maya-ray and sam-ray. Write "Ray fell" as sam. Show maya (sam's co-caregiver on ray in a SEPARATE dyad) cannot read it, while sam can. Then show what an operator sees in the store: D_priv rows are ciphertext, sealed to member keys, not derivable server-side.

LET THEM RUN: Let the engineer pick any member and any dyad-private fact and try to decrypt across the boundary. Let them inspect dyad_key_wraps directly and confirm no plaintext private key. Let them run DK3 — the overlapping-dyad case — themselves.

THE CLAIM IT PROVES: "A care recipient's private facts are sealed to their caregivers cryptographically, per caregiving relationship, not by a filter the server could bypass. The parent holds no key and needs no device; the caregiver holds it for them."

THE HARDEST QUESTION + HONEST ANSWER: "The custodian holds the key, so you have just moved the trust to the daughter. What stops HER from leaking the parent's data?" Answer, limit stated first: nothing cryptographic — the custodian can read the parent's facts, that is the design; the parent's medical facts are readable by their caregivers by definition. What we prevent is everyone OUTSIDE the dyad, including the operator and other household members, reading them. We protect the parent from the system and from the rest of the house, not from their own chosen caregiver. That is the honest boundary, and it matches how care actually works: the daughter already knows the medications.

## CONSTRAINTS

- Dual-envelope: dyad keys run ALONGSIDE the master envelope (key_version distinguishes). Nothing is destroyed this phase. The demo still runs on existing data.
- D_priv never written in clear, never logged, never returned by an API.
- No operator-derivable path to D_priv. If the server can compute D_priv, this phase has failed regardless of what the tests say — check this explicitly.
- Overlapping dyads must isolate (DK3). A design that treats "all ray's caregivers" as one bucket is wrong; the unit is the dyad, not the recipient.
