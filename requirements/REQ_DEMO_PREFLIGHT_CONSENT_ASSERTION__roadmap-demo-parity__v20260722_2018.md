# REQ_DEMO_PREFLIGHT_CONSENT_ASSERTION
Status: MET
MET-Ruling: Bill, 2026-07-28 (D-03d dispatch) -- three assertions green
end-to-end (D-03c run, exit 0: pane == exactly the two derived D10/D11 record
IDs; approve -> real setback answer via openai:gpt-4.1; decline -> no send);
failure semantics match Check 5b; fresh-seed + finally-guarded restore; 7688
graph pin held; fault-injection twins proven red-on-command (D-03). Built on
branch demo-cutover (5b7a5bb), evidence in DISPATCH_D03 + /tmp/d03{,b,c}_report.md
Reconciled-Against: cfd1f96

## PROBLEM

demo_preflight.sh on roadmap executes exactly one real turn sequence, Check
5b, the metformin to Jardiance supersede beat, and asserts subject,
from_state, transition on the resulting delta. Every other check is static:
fixture correctness, file presence, server health, gate_check.sh exit code,
and routing via a direct harness.router.route call with no turn executed.
There is no assertion anywhere that the consent gate returns. The consent
gate is the central beat of the boundary_and_consent script: the pane lists
two facts by record ID, approval sends them, and real setback data comes
back. That behavior is currently unproven on roadmap.

## REQUIREMENT

demo_preflight.sh must execute the consent-gate sequence end to end on a
freshly seeded graph and assert three things: the consent pane payload
contains exactly the two expected fact record IDs and no others; approval
returns a non-empty answer containing real setback data; decline returns
without sending. Failure means the live demo beat is broken and must not be
presented, same standard as Check 5b.

## DEMONSTRATION OBJECTIVE

SHOW: preflight running on roadmap, red before the fix, green after.

LET THEM RUN: scripts/demo_preflight.sh on a clean checkout.

THE CLAIM IT PROVES: the consent gate is verified behavior on roadmap, not
verified behavior on main plus newer untested code on roadmap.

THE HARDEST QUESTION + HONEST ANSWER: does this cover the other three demo
scripts? No. It covers the consent beat only. speaker_isolation and
trust_ladder still have no execution assertion beyond 5b.
