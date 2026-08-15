# HIP Finish Plan: three finish lines, 14 steps

Version: v20260811
Status: **PLAN OF RECORD**
Branch: roadmap
Banked by: HA-37, 2026-08-11, on Bill's instruction
Supersedes: `HIP_Roadmap__complete-sequence__v20260718_1600.md` (the July sequence doc), which
is marked SUPERSEDED and retained unaltered.
Amended by: `HIP_TrustBoundaryRoadmap__five-phase-egress-identity-authority__v20260812.md`
(HA-50, 2026-08-12) — five phases over egress, identity and authority. **It INSERTS into this
plan rather than forking it:** its phases 0-1 are demo-phase work inside the VD-40 freeze
criteria, and its phases 2-4 absorb work already sequenced here (R2 permit, ceiling audience
axis). **This plan is not superseded and remains the PLAN OF RECORD.**

## What this is, and what was done to it

**The plan of record for finishing HIP.** It defines three finish lines — demo, core product,
proof package — in that order, and a 14-step sequence with a finish condition per step.

**BANKED VERBATIM.** Everything below the rule is Bill's source text, reproduced intact from
`~/Downloads/Untitled.txt`: same wording, same order, same list structure, nothing added,
removed, reordered, summarised or corrected. Where the source used tab-indented list markers
from its origin format, they are rendered as Markdown lists; **no character of the prose was
changed.** This header is the only content that is not Bill's.

**Its own rule is now also STANDARD PREAMBLE item 12** (CLAUDE.md, landed by the same
dispatch), so it governs every session and not only readers of this file:

> A finding does not automatically become the next task. It becomes immediate work only if it
> blocks the current phase's acceptance criteria. Everything else gets filed and stays filed.

**This document plans; it builds nothing and rules nothing MET.** Statuses named inside it are
Bill's to rule, and the two status observations it makes about already-landed work (A19 done;
the binding set green after HA-36) are records of what was measured, not new claims.

---

You need a finish plan with hard stop rules. Otherwise every good finding turns into another week of work.
Definition of “done”
I would use three separate finish lines:
1. Demo done — you can show HIP honestly and cleanly.
2. Core product done — the requirements you consider fundamental are MET.
3. Proof package done — the claims ledger, test evidence, erasure proof, and remaining technical debt are cleaned up enough for an outside technical review.
Do them in that order.

Phase 1 — Finish the demo
Target: 2 dispatches. No expansion.
VD-39 — Fix only the four demo blockers
1. Provenance
    - Stop the model from generating trust wording on every factual-answer path.
    - Use the deterministic renderer everywhere.
    - The same fact must never say CONFIRMED to one person and ASSERTED to another.
2. Invisible turns
    - Write safe routing/display rows for:
        - access-control refusals;
        - confirmation turns.
    - Preserve opacity.
    - Goal: 16/16 demo turns visible.
3. B_T04 tier
    - Turn record must say frontier when the actual route was frontier.
    - Do not alter routing behavior.
4. Dashboard
    - Unlock the vault for the rehearsal/demo.
    - Fix or hide:
        - bogus 0% routing statistics;
        - cumulative query count if it looks session-specific;
        - any other number that is visibly false.
    - Do not build a new analytics system.
These are the actual problems VD-38 exposed in the room.
VD-40 — Final rehearsal
Fresh restart. Run exactly the three demo scripts.
Acceptance:
- 16/16 turns appear.
- Five privacy refusals appear and reveal nothing.
- Confirmation appears.
- No false provenance statement.
- Screen and record agree on routing.
- B_T02 gives a complete answer.
- Consent gate works.
- Trust sequence tells the correct evidence story.
- Vault is usable.
- No visibly false dashboard statistic.
- Capture final screenshots.
If those pass: freeze the demo.
No finding discovered during VD-40 becomes new work unless it makes the demo false, invisible, privacy-unsafe, or broken.

Phase 2 — Finish the core product requirements
After the demo, finish the offer mechanism. You have reduced this to three real gaps.
A19 is now done: exact offer wording survives a real process death and restart, byte-identical and hash-verified.
2A. A6 — minimal authority delta
HIP must be able to prove:
This offer asks for exactly the smallest authority change required for this situation.
Build:
- canonical representation of requested authority delta;
- minimality check;
- no bundled unrelated authority;
- fault twin with an over-broad offer.
Do not make this an LLM judgment.
2B. A12 — member utterance → ResponseKind
This is the important missing link behind C-14.
Build a tightly constrained classifier for things such as:
- accept;
- decline;
- ambiguous;
- question;
- invalid/non-response.
Then prove:
- only explicit acceptance grants authority;
- ambiguity grants nothing;
- wrong person grants nothing;
- classifier output, not raw prose, enters apply_response.
When this is done, C-14 can be reconsidered for PROVEN.
2C. A16 — narrowing/revocation
Build the inverse of grant:
- narrow authority;
- revoke authority;
- no new access after revocation;
- record exactly what changed;
- derivative/access consequences enforced.
2D. Full offer acceptance
Then rerun A1–A20.
Conditional clauses stay conditional.
Required result:
All applicable clauses PASS; no unconditional clause FAIL or CANNOT RUN.
Then rule REQ_OFFER_MECHANISM: MET.
Stop working on offers at that point.

Phase 3 — Finish erasure and operator-blind crypto
This is the remaining technically important part of the architecture.
3A. Finish erasure prerequisites
Before making strong erasure claims:
- metadata scrub cascade;
- no persistent raw recall/query text;
- derivative invalidation;
- graph cleanup;
- embeddings/indexes;
- summaries;
- caches;
- exports;
- audit surfaces;
- key generations;
- backups.
The acceptance question is not merely “was the DB row deleted?”
It is:
After subject erasure, can HIP still recover meaningful subject data through any supported path?
3B. Phase 3 — data at rest
Your graphic has this correctly as unfinished:
Destroy master key / remove operator-readable at-rest path.
Do this after the erasure inventory is complete, because otherwise crypto-erasure can give you a comforting answer while metadata survives elsewhere.
3C. Prove erasure
Run an actual erasure lifecycle:
1. Create controlled subject data.
2. Create derivatives.
3. Verify all expected copies exist.
4. Erase.
5. Destroy required key material.
6. Restart.
7. Attempt recovery through every governed path.
8. Verify only permitted opaque operational proof remains.
That is what moves the remaining erasure claim from UNPROVEN.
3D. Phase 4 — quorum recovery/eviction
Only after Phase 3 is solid:
- recovery quorum;
- eviction/revocation quorum;
- lost-device case;
- compromised-custodian case;
- no single operator/admin bypass.
This is important architecture, but it should not precede getting the current erasure path correct.

Phase 4 — Close the test system
Do this after the product requirements, not between them.
Fix the canonical test command
TD-R-183 is real: collection-time network activity can prevent the canonical suite from measuring anything.
Fix/document that.
Resolve the 31 health-check reds
Do them by group, not individually:
- 19 disclosure-oracle failures;
- 4 order/pollution ledger failures;
- 1 sensitivity routing failure;
- 7 demo-presentation failures.
The binding set is already green after HA-36: 1016/0 standing battery, Layer 7 exit 0, RATCHET binding tests pass, memory 13/17.
So these are cleanup/hardening work, not a reason to reopen already-proven product behavior.
Live-model rule
Keep collecting L1–L6 run data.
Do not invent a threshold yet.
Eventually answer from the collected data:
- what is normal variance;
- what failure frequency is unacceptable;
- how many runs constitute evidence;
- whether different live tests need different thresholds.
Until then, deterministic tests gate; live-model results report.

Phase 5 — Final claims and external-review package
Only after the product work above.
Regenerate the claims ledger
For every claim:
- PROVEN;
- PARTIAL;
- UNPROVEN.
Each should point to:
- requirement;
- standing test;
- dispatch;
- fault twin;
- known limitation.
No prose inflation.
Update the roadmap graphic
By then it should look more like:
Foundation
- device binding — done
- custody/authorship — done
- write guards — done
Offers
- offer controls — done
- acceptance — done
- no required gaps
Keys/erasure
- key hygiene — done
- backup exclusions — done
- erasure — proven or explicitly remaining
Operator-blind crypto
- Phase 2 — done
- Phase 3 — done
- Phase 4 — done or intentionally deferred
Tests
- binding battery — green
- mutation gate — green
- live-model rule — defined
Then freeze the development evidence and hand it to an outside reviewer.

The order from today
I would run the project in exactly this sequence:
Order
Work
Finish condition
1
VD-39 demo blockers
four blockers fixed
2
VD-40 rehearsal
clean 16-turn demo
3
A6
minimal authority structurally enforced
4
A12
real utterance → governed response
5
A16
narrowing/revocation proven
6
A1–A20 rerun
Offer REQ MET
7
erasure prerequisites
all erasure surfaces enumerated
8
Phase 3 crypto
at-rest operator access removed
9
erasure acceptance
erasure claim proven
10
Phase 4 quorum
recovery/eviction complete
11
test cleanup
health-check reds resolved/understood
12
live-model rule
reproducibility policy ratified
13
claims refresh
ledger reflects final evidence
14
external review
no undisclosed blocking issue
The rule that keeps this finite
From now on:
A finding does not automatically become the next task.
It becomes immediate work only if it blocks the current phase's acceptance criteria.
Everything else gets filed and stays filed.
That one rule is probably the difference between finishing this in a controlled sequence and still investigating adjacent defects a month from now.
