# REQ_IDENTITY_BINDING_BUILD: Stage 1 Implementation
Version: v20260718_1720
Status: NOT MET
Branch: roadmap
Reconciled against: REQ_IDENTITY_BINDING e1888e0 (+SCOPE 3532f90); roadmap plan of record 3532f90; crypto design 47851d7 s2.1; code read of demo_dashboard.py:179-192, :1948-1968

## What this implements

REQ_IDENTITY_BINDING, filed at e1888e0. The requirement, acceptance test, scope, and constraints live there. This doc adds the implementation: what gets built, where, and the one design decision Stage 1 owns.

## The defect, in one sentence

Identity is a string the client sends. select-member (demo_dashboard.py:179-192) checks the string names a registered member and sets a process-global. text-query (:1948-1968) passes the string straight into process_text_query. Nothing proves the caller is that member.

## The fix, in one sentence

Identity becomes a signature the client must produce with the member's private key, verified against the member's registered public key, on every turn. No signature, no turn.

## The pieces

1. Member keypairs. Ed25519 per member, generated at enrollment. The private key is the credential. The server stores public keys only, in member_registry (new column or table: member_pubkeys). This is the same keypair the crypto build seals to later (crypto design s2.1: Ed25519 signing beside X25519 sealing). Stage 1 registers the signing half. Nothing about fact encryption changes in Stage 1.

2. Enrollment. Operator-approved, per the REQ. For the demo: the fixture (demo_seed) pre-enrolls bill, maya, and sam; keygen runs at seed time; private keys land in the local keystore (below); public keys land in the registry. Enrollment of a member not in the fixture is out of scope for Stage 1. No self-serve enrollment path exists, so none can be attacked.

3. The keystore (the Stage 1 design decision). Demo private keys live in a local keystore on this box: ~/hip-keys/<member>.key, mode 600, outside the repo. The dashboard signs turns by reading the selected member's key from the keystore.
   Why this and not in-browser signing: the demo requirement is one presenter switching among three members on one box. A local keystore satisfies that exactly. In-browser per-device signing is the production shape, but it adds WebCrypto key management and enrollment UX that change nothing the demo shows. The seam is stated, not hidden: PRODUCTION MOVES SIGNING TO THE MEMBER DEVICE. The keystore is the demo stand-in for three member devices, the same way the member dropdown was the stand-in for identity. The difference: the dropdown asserted, the keystore proves. The verify path (server-side signature check against the registered pubkey) is production-real and does not change when signing moves.

4. The gate. A turn carries {member, ts, nonce, sig} where sig = Ed25519(member_privkey, member || ts || nonce || body-hash).
   select-member: verifies sig against member's registered pubkey before setting _vault_selected_member. Fail: 401, member not set.
   text-query: verifies sig the same way before process_text_query. Fail: 401, no model call, no facts touched.
   Replay: nonce single-use within a window; stale ts rejected. Demo-grade window (minutes), stated as such.
   Voice: the voice path takes its member from the verified session established by select-member, never from speaker_id. speaker_id remains a hint (TD-127) and stops being load-bearing: if the verified member and the speaker_id disagree, the verified member wins and the mismatch is logged.

5. The switch. The demo member picker keeps working: picking maya makes the dashboard sign the next select-member call with maya's keystore key. All three keys are present locally, so switching is free. The rejection demo: a turn signed with the wrong key, or no key, gets 401 on stage. That is the show-able proof.

6. The record. Every admitted turn's epistemic record gains identity_verified: true and the pubkey fingerprint used. Every rejection emits a ledger (HEL) event: identity.rejected with reason (missing, forged, replay, unknown member). The harness asserts against these fields, not against reply prose.

## What does not change

The demo scripts, the panes, the voice pipeline, the fact schema, the encryption path, main. The member picker UI stays; only what it does underneath changes (assert -> sign).

## Acceptance (from e1888e0, mechanized)

1. text-query with no sig: 401, not answered as that member.
2. select-member with no sig or wrong-key sig: 401, member not set.
3. Forged/copied credential (sig by another member's key, tampered body, replayed nonce): 401.
4. Voice turn: admitted only via the verified session; speaker_id disagreement logged, never authoritative.
5. Valid sig for bill, maya, sam: admitted; presenter switches among all three; scripted and voice demo run unchanged.
6. No path admits an unverified member string: grep-level check that process_text_query and _vault_selected_member have no caller that skips verification.
7. --full passes. Done means the ratchet, not the narrow proofs.

## Build order

1. Keygen + registry column + fixture pre-enrollment (no gate yet; demo unchanged; verify keys exist).
2. Signing in the dashboard client path + verify in select-member. Demo still runs.
3. Verify in text-query. Demo still runs.
4. Voice session binding + speaker_id demotion to hint.
5. Rejection ledger events + record fields.
6. Harness: the acceptance checks above as pass/fail assertions; then --full.
Each step lands separately. The demo works after every step. No step breaks a verified path to fix an unverified one.

## Honest limits, Stage 1

Keys on one box means one box compromise yields all three credentials. Accepted: the box is the demo. Production seam is device-held keys; the verify path already matches it.
The nonce window is demo-grade. Production tightens it.
This proves possession of a key, not personhood. Device custody is the trust root now, as the crypto design says: a better place for it, not a free one.

## DEMONSTRATION OBJECTIVE (appended 2026-07-19)

Retrofitted per Bill's 2026-07-19 standing requirement that every REQ carry a DEMONSTRATION OBJECTIVE section. This REQ was filed 2026-07-18, before the requirement existed. Folded into this file in place rather than a separate addendum doc, per instruction.

We commit to passing this in front of a skeptical engineer, as a co-equal objective to the identity gate itself. We do not rig the build for it.

SHOW: On one screen, no terminal. Pick maya, ask a question, it answers as maya. Send a turn with no credential -> 401, refused. Send a turn signed with bill's key claiming to be maya -> 401, refused. Then switch cleanly among all three members and watch the legitimate case flow.

LET THEM RUN: Hand the engineer the keystore. Let them try to forge a turn: copy a signature, tamper the body, replay an old nonce. Watch each bounce. Let them switch members and confirm the legitimate path still works.

THE CLAIM IT PROVES: "Identity here is possession of a key, not a string you can type. You cannot be someone whose key you do not hold, and I will let you try."

THE HARDEST QUESTION + HONEST ANSWER: "It is all on one box and you are signing server-side. That is not real device binding." Answer, limit stated first: correct, the demo's keys live in a local keystore standing in for three member devices; the VERIFY path is production-real and identical, only the signing LOCATION moves to the member's device in production. We do not claim the device-custody property yet. We claim the gate, and the gate is real, verified against the actual endpoints (select-member, text-query) that were client-trusting before.
