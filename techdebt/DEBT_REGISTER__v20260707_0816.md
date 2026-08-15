# HIP Tech Debt Register — known issues
STATUS: LIVE
RECONCILED-AGAINST: session 2026-07-07, HIP_FinalizationOrder CHG-8
Rule: one running register. New issues appended with an ID. Resolved issues marked RESOLVED with the commit that closed them, never deleted. When this file changes materially, cut a new timestamped version and repoint LATEST_DEBT.

## Severity: SEC (security) | GATE (blocks a promotion/demo) | ENG (engine track) | OPS (tooling/reliability)

| id | sev | issue | source | status |
|----|-----|-------|--------|--------|
| TD-101 | SEC | Unauthenticated dashboard endpoints still present; embed_text(fact["value"]) TD-030 gap open (embedding path may touch a fact value pre-encryption); git-history scrub pending | SECURITY_AUDIT (INDEX, STALE) | OPEN |
| TD-102 | GATE | issue_INT-001_*.json appeared in eval/integration_issues/ after a passing 6-check gate; likely transient run against unseeded state. Verify before next promotion. | Truth-layer delivery report | OPEN |
| TD-103 | OPS | launchd bootstrap for com.hip.voice.orch fails 1-in-N (I/O error 5), does not inject NEO4J_PASSWORD reliably; voice server start is non-deterministic. Fix: committed start_manual.sh that exports the password and launches directly. | 2026-07-05 session | OPEN |
| TD-104 | OPS | Neo4j password contains shell-special char (!); trips zsh/plist/sed edits. Rotate once to a 24-char alphanumeric to remove the recurring friction. | 2026-07-05 session | OPEN |
| TD-108 | SEC | Per-fact consent-and-routing ledger not yet shipping: every fact must carry sensitivity classification, owner identity, source provenance, consent scope, allowed destinations, retention limit, and immutable audit trail before the router can enforce delivery. PRIMARY LIABILITY-SEVERITY REDUCER - ship pre-scale, not as a later hardening step. Breach blast radius is unbounded without this control. FINAL CHG-6 see HIP_FinalizationOrder. | HIP_PropagationWorkOrder CHG-1/CHG-6 | OPEN |
| TD-109 | SEC | BUILD REQUIREMENT CHG-8 - Biometric consent-and-retention control for on-device speaker recognition. Gates any public claim that speaker recognition has consent controls. Scope: (1) speaker recognition off by default; (2) per-speaker written or electronic consent at enrollment (or legally authorized representative); (3) consent screen must state: what is collected (local speaker embedding), purpose (speaker recognition, role permissions, household privacy controls), storage (local device only, encrypted at rest), sharing (not sold, not advertising, not model training, not uploaded unless separately authorized), retention (deleted on profile removal, consent withdrawal, purpose satisfied, or statutory maximum); (4) published biometric retention schedule: delete on request or profile deletion, delete after speaker-recognition disablement, delete no later than 3 years after last interaction where BIPA-style rules apply, device reset and household transfer deletion; (5) non-biometric fallback (PIN, passphrase, device possession, manual speaker selection); (6) audit enrollment, consent, deletion, and export events. | HIP_FinalizationOrder CHG-8/DECISION-3 | OPEN |

## Notes
- TD-101 is the highest-severity open item; it sits in the STALE security audit. Engine-track, but do not let a public-facing demo run against unauthenticated endpoints.
- TD-103 blocks the voice track and the TD-042 mic test until closed.
- TD-108 is the primary liability-severity reducer for the platform. The per-fact consent ledger caps breach blast radius. It must ship before scale, not after. See CHG-1 in HIP_PropagationWorkOrder and Ecosystem NDA Section 4.3 for the full liability argument.
- TD-109 is a build requirement, not a debt item. No public claim about speaker-recognition consent controls is accurate until TD-109 ships. The CHG-3 wording in the NDA states the architecture fact only; TD-109 is the control that backs any future consent claim.
