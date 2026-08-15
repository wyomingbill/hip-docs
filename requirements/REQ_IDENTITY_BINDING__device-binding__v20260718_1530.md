# REQ_IDENTITY_BINDING — device binding
Version: v20260718_1530
Status: NOT MET
Branch: roadmap
Reconciled-Against: main 688386f (roadmap base); crypto design 47851d7; dyad spec 601ac25

## THE REQUIREMENT (Bill, verbatim)
"The system has to actually check who's talking before it trusts them, and you
can't fake being someone else — but I can still demo all three members on one
box."

## SCOPE
Single speaker, one member per turn. No shared-device conversation this
sprint. Do not build speaker arbitration. Device binding leaves the door
open for it later.

## THE ACCEPTANCE TEST (pass/fail)
1. A /api/text-query turn with a client-asserted `member` and no valid device
   credential is REJECTED — not answered as that member. (Today it is trusted
   as asserted.)
2. /api/session/select-member with no proof the caller holds that member's
   credential is REJECTED. (Today demo_dashboard.py:179-192 accepts any
   registered member_id.)
3. A turn presenting a forged/copied credential for a member is REJECTED.
4. Voice: a turn is admitted only on a proven device credential; speaker-ID
   (speaker_id.py) is a hint, not the identity root (TD-127).
5. A turn with a VALID credential for bill / maya / sam is ADMITTED, and the
   presenter can switch among all three valid members on the one demo box —
   scripted and voice demo run unchanged.
6. No code path admits an identity claim that was not credential-verified.

## WHAT'S ALREADY DONE (do not redo)
- Decision made: device binding over session token / voiceprint.
- Crypto design 2.1 specifies a per-member X25519/Ed25519 keypair, private
  half device-held. This REQ builds the IDENTITY use of that keypair; it IS
  the first brick of the crypto build, not a throwaway.
- Voiceprint stays a vendor stand-in (TD-127), not the identity root.

## WHAT'S KNOWN BROKEN (current state, code-grounded)
- /api/text-query trusts a client-asserted `member` string, no session binding.
- /api/session/select-member (demo_dashboard.py:179-192) sets the active member
  with no proof the caller is that member.
- Voice speaker-ID (speaker_id.py) error rate unquantified.
- The real per-member keys are design-only (both specs Status: PLAN); the demo
  runs on the existing master-key envelope. Identity verification is a
  trusted pass-through today.

## CONSTRAINTS (must not regress)
- Do not touch main. Work on roadmap.
- Do not break scripted or voice demo.
- One demo box holds all three member credentials legitimately — the gate
  rejects NO-credential and FORGED-credential turns, without blocking switching
  among the three valid members.
- Build identity so the same keypair carries into crypto 2 (build once) and so
  a custodian can later present a care-recipient's identity through her device
  (the dyad) — do not hardcode one device = one member.

## NOTES
- Stage 2 decision (a) uncertainty default = FAIL-PRIVATE (Bill, 2026-07-18).
- Stage 2 (b) quorum composition remains open — Stage 4 item.
