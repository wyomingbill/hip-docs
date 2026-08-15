# F-4 Fix — INJ-7 access-control refusal (cross-member deny ≠ empty-set)
Status: BUILT
Reconciled-Against: Tier L 11/11 (E1-E8 + G2 + T119 + G4) twice, injection harness 11/11, baseline locked 2026-07-08

## Problem (HITL F-4/F-9, TD-112)

Sam asks "What medications does Maya take?" — Maya's lisinopril exists, but
the reply was "I don't have that confirmed yet": the privacy boundary
rendered as ignorance, indistinguishable from a true data gap. For a
governance instrument this hides the exact boundary it should showcase.

## Root mechanics

Live retrieval is owner-scoped (`read_user_facts(sam)`), so Maya's facts
never reach the injection contract at all — INJ-3 denial counts can never
detect the cross-member case on the text path. Worse, "Maya" was not even a
resolvable subject for Sam (known subjects come only from the requester's
own facts), so the turn fell through to INJ-6b's empty-set guard.

## Design — INJ-7, membership as the boundary

1. **Registered members are always resolvable subjects**
   (`resolve_subject(..., member_ids=...)`) — Phase-3 named-entity matching
   now unions the registry ids with fact-derived subjects.
2. **INJ-7 in the contract** (`apply_injection_contract(...,
   member_ids=...)`): a personal QUESTION whose resolved subject is a
   registered member other than the requester sets `access_denied` +
   `access_denied_subject`. Checked before the empty-set guards — the two
   refusals are mutually exclusive by construction. Declarative turns are
   exempt (statements about another member are the write path's concern —
   the TD-110 fork).
3. **Structural reply**: `access_control_refusal()` — "That's Maya's
   information — I can only share it with Maya." Model never invoked;
   metadata target `access_control_guard`.
4. **Existence-invariant**: membership, not fact existence, triggers the
   refusal — identical reply whether or not the fact exists, so the boundary
   cannot leak existence.
5. **Scope guards**: `member_ids=None` (default; every pre-F-4 caller
   including the frozen voice path) disables INJ-7 and the resolver change
   entirely. Care recipients who are not registered members (Ray, Elena)
   resolve exactly as before — caregiver reads untouched (E2/E5/G2/T119).

## Gate

- G4 (harness gap spec G-4), four assertions: no plaintext leak; NOT the
  empty-set string; access-control wording names the boundary;
  existence-invariance (fact-exists and fact-missing legs return identical
  replies).
- RED pre-fix: both legs returned the empty-set string. GREEN post-fix:
  Tier L 11/11 twice consecutively; injection unit harness 11/11; E6 still
  pins the empty-set string for the true-unknown case, so the two refusal
  paths are asserted distinct in every run.
