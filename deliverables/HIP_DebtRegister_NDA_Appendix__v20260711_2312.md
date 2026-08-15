# HIP Debt Register — NDA Appendix
Status: BUILT
Reconciled-Against: da5b84b355fa7b3e6ad66f6cf51bb6f9fb9a6fb8

---

## Preamble

This appendix presents the platform's known-gaps list proactively, to a counterparty conducting technical due diligence, rather than waiting for a review team to find it. Every item below is tracked internally with a register ID, a severity, a status, and a history of the finding that produced it. The internal register (`docs/techdebt/DEBT_REGISTER__v20260709_0855.md`) is the live artifact this appendix summarizes; nothing here is invented for the purpose of this appendix, and nothing in the internal register is omitted here because it is unflattering. The posture is: an architecture that survives scrutiny is not the same claim as an implementation that is finished, and this document is where the difference is made explicit.

---

## TD-101 — Unauthenticated dashboard endpoints

**Severity:** highest open item in the register (SEC).
**Status:** OPEN.

The live voice/demo server exposes several endpoints with no authentication, most seriously a dedicated `/api/decrypt` route that returns decrypted plaintext fact values for any household member on request, with the member ID taken as an unvalidated query parameter. Any host reachable on the same network as the server can exfiltrate every household member's decrypted personal facts (medications, diagnoses, finances, relationships) without credentials. A destructive `/api/reset` endpoint and unauthenticated fact/member enumeration routes carry the same underlying gap at lower severity.

**Constraint in force until resolved:** demos and any counterparty-facing access to the running system are local-only or over VPN. No unauthenticated network path is exposed to the public internet at any point.

---

## TD-108 — Per-fact consent-and-routing ledger not yet shipped

**Severity:** SEC, flagged as the primary liability-severity reducer for the platform.
**Status:** OPEN.

Every fact stored by the platform must eventually carry a sensitivity classification, owner identity, source provenance, consent scope, allowed destinations, retention limit, and an immutable audit trail before the router can enforce delivery against that metadata. This ledger is not yet built. It is a healthcare-relevant audit-trail gap in its current form: without it, the platform cannot yet produce a per-fact record of who consented to what disclosure and when. This must ship pre-scale, not as a later hardening pass, because the blast radius of a breach is unbounded without it.

---

## TD-110 — Cross-member write authority gap

**Severity:** ENG, governance-decision-required.
**Status:** OPEN.

Any authenticated household member can currently supersede another member's health fact (for example, one member overwriting another member's medication record) with no authority check, no provenance gate, and no corroboration requirement. The read side of the trust boundary blocks cross-member reads; the write side has no equivalent gate. Two forks are on the table and neither has been decided:

- **Block:** a cross-subject write from a non-owner lands as unconfirmed and requires a second signal (corroboration or explicit confirmation) before it can supersede the existing fact.
- **Capability grant:** a member can be granted explicit caregiver authority over another member's facts, and a supersede under that grant is correct behavior, but it must be visibly attributed ("Maya, caregiver, superseded Ray's record") rather than appearing as a silent overwrite.
- **HITL park:** leave the gap open, park the automated gate, and require human review of cross-subject supersedes until a decision is made.

This item was previously misfiled under the wrong register ID in one historical document; see the numbering-collision note below.

---

## Voice-path hardening (Code Review Finding #4)

**Severity:** critical, prototype governance.
**Status:** in progress; open engineering work.

The verification harness's proofs (Gate A 100 percent, Gate B 90.2 percent, the five-layer harness architecture) cover the typed interaction path (`process_text_query`) only. The live voice path (`_on_user_text`) does not yet run the same enforcement chain: no injection contract, no F3 write-confirmation gate, and no turn metadata are applied on that path today. Concretely, the live voice path can leak cross-member facts and can acknowledge a write that never actually landed. Hardening the voice path to run the identical enforcement chain as the typed path is open engineering work, tracked in the register against this finding.

---

## Key custody

**Severity:** disclosure-accuracy item, not a code defect.
**Status:** design not yet built.

Facts are encrypted at rest under an operator-side master key (32 random bytes, held in the operator's environment), from which a per-owner key is derived via HKDF-SHA256, and each individual fact is further encrypted with its own random Fernet key wrapped by the owner key. This is real encryption at rest, but custody of the root key is operator-side today. A household-held recovery design exists in the architecture research (`docs/research-technical/HIP_Architecture_Spine__v20260704_1315.md`, Section 4 and Section 9): device-held root keys, per-user and per-household wrapped data keys, and a threshold secret-splitting recovery scheme (Shamir/SLIP-39 shares, with a stated production target of a 2-of-3 or 3-of-5 split across user devices, a trusted recovery contact, and a neutral escrow/HSM) that would end operator sole custody. That design is specified, not built. No claim of household key control is accurate today.

---

## Availability and fallback under load

**Severity:** availability-affecting, not a governance breach.
**Status:** open; serving fix planned.

The classifier is fail-closed by design: when it cannot classify with confidence, or the edge inference tier is unreachable or overloaded, the system declines rather than guesses. Under GPU contention on current dev hardware, fallback rates of 26 to 31.5 percent have been observed in shadow-mode evaluation runs. This is deny-safe behavior, not a disclosure risk, but it is availability-affecting and would degrade the user experience at the rates observed. A dedicated serving fix (isolating the classifier onto its own inference instance) is planned to close this gap. Current classification quality, independent of the fallback-rate question, is Gate B 90.2 percent on the full 133-entry corpus (Gate A, the governance-critical 26-entry subset, is 100 percent).

---

## TD-109 — Biometric consent and retention (open build requirement)

**Severity:** SEC, build requirement (CHG-8), included here because the white paper references speaker verification.
**Status:** OPEN.

Speaker recognition consent-and-retention controls are not yet built: off-by-default enrollment, per-speaker consent capture and disclosure at enrollment, a published biometric retention schedule, a non-biometric fallback (PIN, passphrase, device possession, manual selection), and audit logging of enrollment/consent/deletion/export events. No public claim that speaker recognition carries consent controls is accurate until this ships. This is a build requirement, not a code defect, and it gates any future consent claim, not the current architecture claim (which is limited to stating that speaker verification exists and has a documented, non-zero attack surface).

---

## TD-109 / TD-110 numbering-collision note

One historical document (`docs/testing/HITL__phase4-findings__v20260708_0951.md`) mislabeled the cross-member write-authority finding (F-5) as "elevated to TD-109" in its section heading, even though the same finding's body text correctly says "Filed as TD-110." TD-109 has always meant biometric consent and retention (CHG-8) in every version of the debt register from `DEBT_REGISTER__v20260707_0816.md` onward; TD-110 is the correct and current ID for the cross-member write-authority gap. The historical document has been given a correction note rather than silently rewritten. Every other document in the corpus that references either ID uses them correctly as of this appendix.

---

## Source

Pulled from `docs/techdebt/DEBT_REGISTER__v20260709_0855.md` (latest register) and `docs/research-technical/CODE_REVIEW__harness-and-prototype__v20260709_2116.md` (voice-path finding). Gate A/Gate B figures from `docs/research-technical/SIA_SHIP_BAR__two-gate-conformance__v20260711_0842.md` and the current run.
