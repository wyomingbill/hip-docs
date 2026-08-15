# REQ_CRYPTO_P4_RECOVERY_EVICTION: Stage 4 Phase 4 — Recovery and Custody Exit
Version: v20260721_1511 (amends v20260719_0900)
Status: MET
Branch: roadmap
Reconciled against: REQ_CRYPTO_P1_DYAD_KEYS, P2, P3 (MET first); REQ_PARTITION_CUSTODY D2 (quorum composition) and #6 (custody consent/revocation/abuse resistance, ratified 2026-07-21); dyad spec 601ac25 s4/s6; crypto-partition design spec s4 (recovery); REQ_CRYPTO_HARNESS (N3); REQ_CRYPTO_HARNESS_V2 (MT2-DECRYPT-REVOKE scenario)

## BUILT 2026-07-21 — MET

BUILD REQ_P4_RECOVERY_EVICTION dispatch, Bill-approved acceptance test. Three new/changed modules:

- `harness/quorum.py` (new): genuine 2-of-3 Shamir secret sharing over GF(2^521-1). A single share is information-theoretically useless — Shamir's own proof, not a policy check — which is what makes RE1 a cryptographic fact. Share A (operator escrow) in the clear; Share B always sealed to the household admin; Share C sealed to a second principal or tagged to a disputable PoA instrument hash (RE7).
- `harness/dyad_registry.py` (extended): `atomic_rekey_dyad()` — mints a fresh dyad keypair, re-wraps every affected fact's DEK (value ciphertext untouched, only the wrap moves), re-seals to remaining custodians, destroys every old wrap including the exited custodian's, re-escrows the new key under quorum. Old D_priv comes from a remaining custodian's local unwrap, or — evicting a sole custodian — quorum reconstruction.
- `harness/custody_exit.py` (new): `exit_custody()` orchestrates the three #6 tiers (recipient-unilateral / authority-initiated, no quorum; peer-initiated, always quorum-gated), the continuity rule (RE6), and the contested-PoA freeze (RE7); also removes the exited party from the same recipient's care team if held. `provision_member_recovery()` / `recover_member_key()` implement RE2 (crypto design s4.2's recovery-blob construction).

Wired into `eval/harnesslib/layer7_crypto_v2.py`: MT2-DECRYPT-REVOKE turned from its NAMED-PENDING skip() into a real check (PASS), plus a new `_run_req_p4_recovery_eviction()` asserting RE1-RE7 each with its named fault-injection.

Verified (`--layer 7`, dev graph): `== L7: 23/23` (PS1-PS4, DK1-4, N1/N2/N4/P1/P4, 13-row table rows 1-9 + 10-13, all green, no regression), `== L7V2: 21/22` (1 pre-existing opt-in skip, unrelated) with MT2-DECRYPT-REVOKE and RE1-RE7 all PASS, **RATCHET PASS**. `eval/injection_harness.py`: 9/11, identical pre-existing baseline (two unrelated failures, confirmed not a regression). Commits: d0562d1 (atomic re-key + quorum primitive), acbe2dc (member-key recovery), 80f7021 (harness wiring).

## Why this version exists

SCOPE REQ_P4 RECOVERY/EVICTION dispatch (2026-07-21) asked for this REQ to be written fresh. It already exists — filed 2026-07-19, NOT MET, at INDEX row 104 — and its core primitive (2-of-3 threshold, one mechanism serving both recovery and eviction, operator-share-alone-insufficient) is unchanged and still correct. What's genuinely new since the original filing: REQ_PARTITION_CUSTODY's #6 was ratified 2026-07-21 (after v20260719_0900), and the MT2-DECRYPT-REVOKE harness scenario was built this session (also after). Both belong in this REQ's acceptance surface. This version amends v20260719_0900 rather than duplicating it: same REQ, same INDEX slot, new version file, symlink repointed. No content below is walked back — only added.

## What this is

The last crypto phase, and the one where cryptography meets the legal surface. It builds two operations that turn out to be the SAME primitive:

1. Recovery: a member lost their device/key; the household regains access to their sealed data without the operator being able to do it alone.
2. Custody exit / eviction: a custodian leaves a dyad, cooperatively or not; their old key must stop working, and someone must be able to remove them even without their cooperation.

Both are a 2-of-3 threshold operation over the same three shares. The quorum that reconstructs a lost key is the quorum that revokes a custodian. Build it once.

## Why exit is here and not Phase 1

Phase 1 built entry (grant a custodian a key). Exit was deferred to here because exit requires RE-ENCRYPTION so the old key dies, and re-encryption is the Phase 2 re-seal machinery. Exit = revoke + re-seal the dyad's facts to a fresh dyad key that the exited custodian was never given. Without Phase 2's re-seal, exit would be "stop showing them the data" (a filter) instead of "the old key no longer decrypts" (crypto). We build the real one.

## The three shares (Stage 2 decision D2, ratified)

Any 2 of 3 reconstruct a member/dyad key or authorize an eviction:
- Share A: operator escrow. Held by the operator. Cryptographically insufficient ALONE — this is what preserves operator-blind: the operator holding one share cannot recover or evict by itself.
- Share B: household admin (Bill, in the demo).
- Share C: a second family principal OR a verified legal instrument (a PoA credential).

2-of-3: any two agree. The operator can participate but never acts alone. A family can act without the operator (B+C). A legal instrument can substitute for the second family principal (contested PoA, estrangement).

## Revocation authority tiers (#6, ratified 2026-07-21 — new this version)

REQ_PARTITION_CUSTODY #6 sets three distinct paths into this REQ's single re-key mechanism, by who is initiating:

- **Recipient-unilateral**: a capacitated recipient may revoke custody of their own caregiver directly — no quorum required. Goes through this REQ's re-key/re-seal exactly as any other exit.
- **Authority-initiated**: a recognized authority (valid, uncontested legal instrument) may revoke directly — same re-key path, no quorum gate.
- **Peer-initiated — quorum-gated, deliberate asymmetry**: a peer caregiver acting alone CANNOT revoke another custodian. Peer-initiated revocation always requires the same 2-of-3 quorum as recovery. This is deliberate, not an oversight: evicting the honest custodian is itself the shape of an isolation attack, so the cheaper unilateral/authority paths are withheld from peers specifically.

This REQ's quorum mechanism (Share A/B/C) is the enforcement point for the third tier. The first two tiers still terminate in the same re-key primitive but do not require quorum reconstruction to authorize it — that authorization is the recipient's own consent or the authority instrument's validity, respectively. All three tiers converge on identical cryptographic output (old key dead, facts re-sealed); they differ only in what authorizes the re-key call, matching this REQ's existing "same primitive, two doors" framing extended to three.

## Continuity rule (#6 — new this version)

Custodian resignation or eviction, by any of the three tiers, must trigger a continuity event: no path in this design leaves the recipient custodian-less silently. If the exiting/evicted custodian was the recipient's only custodian, the re-key operation must surface this (HEL event, flagged) rather than complete quietly into an unattended state. This REQ does not mandate an auto-assigned replacement (that's a household/legal decision outside HIP's scope, per #6's own honest limit — HIP is a witness, not a guardian that intervenes on its own judgment) — it mandates that the condition is never silent.

## Contested-PoA freeze (#6 — new this version)

A contested PoA or an estrangement dispute freezes custody at last-known-good state, with elevated logging, rather than letting either side's claimed authority execute a re-key while the dispute is open. The quorum may impose an interim custodian during a freeze but does not adjudicate the legal instrument's validity on its content — that stays outside HIP, exactly as #6 states for consent-tier B. Practically: if Share C is presented as a PoA credential and its validity is actively disputed by another household principal, the re-key does not execute on that share alone; the dispute must resolve (freeze lifts) or the quorum falls back to B+(a non-disputed C) before the operation proceeds.

## The operations

RECOVERY (lost key):
- Two share-holders present shares; the threshold reconstructs the member's key material (or a re-wrap of it to a new device key).
- HEL event: key.recovery, recording which two shares were used.

CUSTODY EXIT (cooperative — recipient-unilateral or authority-initiated tier):
- Custodian consents to leave, or a valid uncontested authority instrument executes exit. Dyad re-keys: new D_priv, facts re-sealed to the new key, exited custodian's wrap removed.
- Old key is dead forward (N3 / MT2-DECRYPT-REVOKE). HEL event: custody.exit.

EVICTION (non-cooperative — peer-initiated tier, quorum-gated):
- Same re-key + re-seal, but authorized by 2-of-3 quorum instead of the custodian's consent. The custodian does not participate; the quorum removes them.
- HEL event: custody.evict, recording the two shares used and the reason code (dispute / abuse / death / estrangement).

The exit and eviction produce identical cryptographic outcomes (old key dead, facts re-sealed). They differ only in authorization: consent, valid-authority, or quorum. Same primitive, three doors.

## The honest limit, built in

Exit means NO NEW ACCESS. It does not unremember. A custodian who read facts before exit still knows them and may have copied them. Re-encryption kills future decryption of the store; it cannot retract what a human already saw. This is stated in every ledger event, every demo script, every doc. Do not design around it or imply otherwise.

## THE ACCEPTANCE TEST (pass/fail)

Turns green:
- **N3 / MT2-DECRYPT-REVOKE**: after custody exit or eviction, the removed custodian's old key cannot decrypt any re-sealed fact. This is the named harness gate (eval/harnesslib/layer7_crypto_v2.py) — GREEN as of 2026-07-21 (see BUILT note above): `dyad_registry.atomic_rekey_dyad()` replaces the old classification-only `mark_exited()` path for actual exit/eviction. Count of post-exit successful decrypts with the old key: 0, live-verified.

New assertions:
- RE1: 2-of-3 threshold — any two shares reconstruct/authorize; any one share alone cannot. Count of single-share successes: 0. This is the operator-blind-preserving property: prove the operator's share alone does nothing.
- RE2: recovery restores a lost member's access (right party regains read) without the operator acting alone. Positive-half: locked-out-after-recovery count: 0.
- RE3: eviction (non-cooperative, quorum-gated peer tier) produces the same dead-old-key outcome as cooperative exit (recipient-unilateral or authority tier). The evicted custodian's key fails on re-sealed facts; the remaining custodians still read — this is the "valid caregiver retains access through re-key" property.
- RE4: every recovery/exit/evict emits an ordered, hash-chained HEL event with the shares used (or tier/authority for non-quorum paths) and (for evict) a reason code. Ledger completeness: 0 unlogged custody changes.
- RE5: overlapping dyads — evicting a custodian from maya-ray does NOT affect sam-ray, even though both concern ray. Re-key is scoped to the one dyad.
- **RE6 (continuity — new this version)**: if the exiting/evicted custodian was the recipient's sole custodian, the re-key emits a flagged continuity HEL event rather than completing silently. Count of silent sole-custodian exits: 0.
- **RE7 (contested-PoA freeze — new this version)**: a re-key attempted on a disputed Share C (contested PoA) does not execute while the dispute is open; it either blocks or requires a non-disputed B+C combination. Count of re-keys executed on a contested instrument alone: 0.

Fault-injection (mandatory): attempt recovery/eviction with a single share; RE1 must reject it. Leave the old wrap in place after eviction (skip re-seal); N3/MT2-DECRYPT-REVOKE must go red. Attempt a peer-initiated revocation without quorum; must be rejected (proves the #6 asymmetry is enforced, not just documented). Mark a Share C instrument disputed and attempt re-key; RE7 must reject it. Prove the threshold, the re-seal, the tier asymmetry, and the freeze all actually gate.

## WHAT'S ALREADY DONE

The crypto envelope/sealing mechanism this phase builds atop: dyad-private, care-team-private, and household-circle-shared key classes are all sealed and verified working (PS1-PS4, DK1-4, N1/N4/P1/P4 green, REQ_CRYPTO_P1/P2/P3 MET). Three classification-only removal stubs already exist and correctly disclose their own limit rather than silently under-delivering:
- `harness/dyad_registry.py::mark_exited()` — sets status to 'exited'; docstring names this REQ by name as the owner of the actual re-key.
- `harness/care_team_keys.py::remove_caregiver()` — docstring names REQ_PARTITION_CUSTODY #6 as the owner of full quorum-gated eviction (same underlying work this REQ now formalizes; the two forward-references are reconciled by this REQ existing).
- `harness/household_keys.py::remove_circle_member()` — docstring discloses it does not re-key or strip the existing wrap, blocks only future wrap-healing inclusion.

## WHAT'S KNOWN BROKEN

Revoked-caregiver decrypt still works today because the atomic re-key doesn't exist, confirmed by direct docstring/code read (2026-07-21) across all three removal stubs above. The severity differs by key-sharing model, noted here for completeness though this REQ's own acceptance test (RE1-RE7 / N3) is scoped to the dyad mechanism, matching MT2-DECRYPT-REVOKE's own target:

- **Dyad** (shared D_priv/D_pub per dyad): an exited custodian's key continues to decrypt both existing AND any newly-written dyad facts sealed under the unrotated key, until this REQ's re-key runs. This is this REQ's primary, in-scope target.
- **Household-circle** (shared HH_priv/HH_pub tree): same shared-key exposure — `remove_circle_member` never strips the removed member's existing wrap of the current HH_priv, and `ensure_household_keys`'s wrap-healing only adds wraps for currently-listed members, never revokes one for a departed member. A removed circle member's old wrap continues to unlock the unrotated key for old AND new facts. Structurally the same gap as dyad's, on a different key. Flagged here as a related, NOT-currently-in-this-REQ's-acceptance-test finding for Bill's awareness — extending RE1-RE7 to household-circle is a scope question, not assumed into this filing.
- **Care-team** (per-fact wrap, not a shared key): narrower exposure — a removed caregiver's wrap on facts sealed BEFORE removal persists (no retroactive strip), but facts sealed AFTER removal correctly omit them (the wrap set is derived from the live roster at seal time, not a shared key). This matches the accepted "no new access, not unremembers" honest limit already stated for exit generally; it is not the same live gap as dyad/household-circle's continued-access-to-new-facts problem.

## CONSTRAINTS

- Recovery and eviction (and, per #6, the three revocation-authority tiers) are ONE primitive (threshold re-key). Do not build separate mechanisms per tier.
- The operator's single share must be provably insufficient alone (RE1). This is the operator-blind property extended to custody; if the operator can recover or evict alone, the phase failed.
- Exit/eviction re-seals; it does not filter. The old key must actually fail (N3/MT2-DECRYPT-REVOKE), verified cryptographically, not by hiding rows.
- Re-key is dyad-scoped (RE5). One dyad's eviction never re-keys another.
- The "no new access, not unremembers" limit appears in every ledger event and every demo script. Never imply erasure.
- Reason codes on eviction are recorded but the system does not adjudicate them — humans manage the relationship, the system enforces the boundary (the standing dyad principle, and #6's own "witness, not guardian" honest limit).
- Must not break PS1-PS4 sealing (REQ_CRYPTO_P2_PARTITION_SEALED, MET) or the REQ_PARTITION_CUSTODY 13-row acceptance table. Both are regression floors, not this REQ's to modify.
- The peer-initiated quorum requirement (#6's asymmetry) must be enforced by the mechanism, not left as a documented-but-unchecked convention — the fault-injection list above requires proving a peer-alone attempt is actually rejected.

## DEMONSTRATION OBJECTIVE

Co-equal to the build. Not rigged. This is the demo that answers "what happens in a divorce / a death / an abuse case" — the questions every eldercare buyer asks.

SHOW: Evict a custodian by quorum (B+C, no operator, no custodian consent). Show their old key now fails on the dyad's facts, while the remaining custodian still reads. Then show the operator alone trying to recover or evict with only share A: it cannot. Then show a peer caregiver trying to revoke another custodian alone (no quorum): rejected. Then the ledger: every custody change logged, ordered, with the reason and tier.

LET THEM RUN: Let the engineer play each role. Hold only the operator share and try to act alone: fail. Hold two family shares and evict: works. Take the evicted key and try to read a re-sealed fact: fail. Try a peer-alone revocation: rejected. Check the ledger themselves.

THE CLAIM IT PROVES: "Custody changes are enforced by cryptography and authorized by a quorum the operator cannot satisfy alone. A family can remove a bad actor without us; we can never remove one without the family; and a caregiver can never unilaterally remove a peer — only the recipient, a valid authority, or a quorum can. Every change is on an audit trail no one can edit."

THE HARDEST QUESTION + HONEST ANSWER: "You evicted the custodian, but she already saw the mother's medical history. You have not protected anything." Answer, limit stated first: correct, and we never claim otherwise. Exit means no NEW access, not amnesia. What eviction guarantees is that from this moment the removed custodian's key decrypts nothing further, every future fact is sealed away from her, and the removal is on an immutable ledger. We protect the forward boundary and the audit trail. We do not claim to erase human memory or copies already made — no honest system can, and a system that claimed to would be lying. The value is real: an estranged or abusive custodian is cut off going forward, provably, without the operator's unilateral power and without waiting on the operator at all.
