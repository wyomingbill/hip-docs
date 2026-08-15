# REQ_CARE_TEAM_READ_AUTH
Status: NOT MET
Reconciled-Against: REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831 (e4804a6); REQ_WRITE_TIME_CLASSIFIER__stage4-phase2__v20260721_0839 (cfc9e2b); harness/injection_contract.py as of 8a71d6b

## THE REQUIREMENT

Bill's own words (dispatch, 2026-07-21): "SCOPE THEN BUILD recall_from_cold
CROSS-AUTHOR CARE-TEAM AUTH. REQ first (docs), then code. This extends the
injection contract's authorization model — bigger blast radius than a
decrypt fix." And: "authorization keys on care-team ENROLLMENT (is_active_
caregiver at the fact's roster epoch), not authorship."

Expanded: `harness/injection_contract.py`'s INJ-3 (`_inj3_cross_member_
deny`) denies any fact where the requester is neither its `owner`
(author) nor its `subject`, with a household bypass. That is correct and
must stay correct for ordinary personal facts — INJ-3's own docstring
states the invariant it protects: "a third party (Sarah) can NEVER read a
fact Bill stored about Elena." But a care-team-private fact is
structurally different from an ordinary personal fact: REQ_PARTITION_
CUSTODY's ratified scope definition says its readable audience is "the
care recipient plus ALL explicitly enrolled caregivers," not just its
author. Decrypt already enforces this correctly (REQ_WRITE_TIME_
CLASSIFIER, verified 2026-07-21: an enrolled caregiver's decrypt of a
co-caregiver-authored care-team fact succeeds). INJ-3 does not know this
audience exists — it still denies by authorship alone, so a correctly-
decryptable fact never reaches the model. This REQ adds ONE narrow,
enrollment-gated permit condition to INJ-3, changing nothing else about
what it denies.

## THE ACCEPTANCE TEST

Pass/fail only, live against the dev graph, no `--full`:

1. An enrolled active caregiver reads a care-team-private fact authored
   by a DIFFERENT enrolled caregiver about their shared recipient — the
   fact is admitted (passes INJ-3; still subject to INJ-1/2/5/6/6b like
   any other fact).
2. A household adult who is NOT enrolled on that recipient's care team
   still cannot read that fact — INJ-3 still denies them, unchanged from
   today.
3. A fact sealed with `subject_visibility=EXCLUDE` for a given caregiver
   stays excluded from that caregiver even though they are otherwise
   enrolled — verified as a consequence of decrypt failing for them (no
   wrap exists), not a new INJ-3 branch: the fact dict is never built for
   an excluded reader, so it never reaches `apply_injection_contract` at
   all. The acceptance test asserts this end-to-end (excluded caregiver's
   read attempt returns nothing), not that INJ-3 contains exclusion logic
   it does not need.
4. A caregiver removed from the care team (past the epoch that covers
   the fact — `care_team_keys.remove_caregiver` already run) cannot read
   a care-team-private fact via this new permit path. (Whether they can
   still read facts from BEFORE their removal is a backfill/historical-
   access question REQ_PARTITION_CUSTODY's custody policy already
   answers — "historical events require an explicit backfill grant" —
   and is out of this REQ's scope; this test only asserts the negative:
   no NEW enrollment-based access for a currently-removed caregiver.)
5. Every existing INJ-1/INJ-2/INJ-3/INJ-4/INJ-5/INJ-6/INJ-6b/INJ-7
   access-control denial that holds today still holds — run the existing
   eval/injection_harness.py and eval/test_seam_s3_facts_grounding.py
   suites (or whichever this build's own diagnosis names as covering
   INJ-3 directly) alongside the 13-row REQ_PARTITION_CUSTODY table and
   lean `--layer 7`, and report all three, not just the new behavior.

Any single failure among 1-5 is FAIL. There is no partial credit.

## WHAT'S ALREADY DONE

- Decrypt-layer cross-author care-team reads: BUILT and verified live,
  2026-07-21 (prior session, "THREAD recipient_ref THROUGH THE READ
  PATHS"). All six disclosed read paths (`truth_layer/queries.py`,
  `server/voice_https_orch.py`, `server/demo_dashboard.py` x2,
  `harness/disclosure.py`, `memory_engine/recall.py`,
  `memory_engine/api.py`) now fetch and pass `f.recipient_ref` through
  `decrypt_fact_value_for_caller`, which dispatches to
  `care_team_keys.decrypt_fact_value_for_care_team` when set. Verified
  directly, isolated from the injection contract: a care-team fact
  authored by "maya" decrypts successfully for enrolled caregiver "sam"
  (`decrypt directly: there was an incident`) and raises `LookupError`
  for a non-enrolled reader.
- `CLASS_DYAD`/`CLASS_HOUSEHOLD` renamed to their ratified string values
  (`pair-private`/`household-circle-shared`), coupled with
  `eval/harnesslib/layer7_crypto.py`'s PS3 update, commit `8a71d6b`.
  Verified: `== L7: 19/19`, RATCHET PASS.
- `care_team_keys.is_active_caregiver(recipient_ref, caregiver_member_id)`
  — the exact primitive this REQ's fix calls — already exists, already
  used by `write_rule.classify`'s own coordination-class check and by
  `server/demo_dashboard.py`'s decrypt-visibility gate (WIP e3). No new
  care-team primitive needs building.
- The 13-row REQ_PARTITION_CUSTODY acceptance table: 13/13 passing as of
  the prior session's final verification, after all seven read-path
  commits (`0d09330`..`8a71d6b`).

## WHAT'S KNOWN BROKEN

- `harness/injection_contract.py:373`, `_inj3_cross_member_deny`: three
  PERMIT conditions (`owner == requester`, `subject == requester`,
  `owner == 'household'`), no fourth condition for care-team enrollment.
  This is the sole reason `recall_from_cold` (and every other caller)
  returns nothing for a correctly-decryptable, cross-author care-team
  fact — traced and isolated live, 2026-07-21: `decrypt directly: there
  was an incident` succeeds; `apply_injection_contract(...)` on that same
  decrypted fact returns `allowed: 0 denied: 1`.
- The `fact` dict `_inj3_cross_member_deny` receives does not carry
  `recipient_ref` at all — not a missing check, a missing FIELD. Every
  caller that builds a fact dict for `apply_injection_contract` needs
  `recipient_ref` added to that dict, not just to the earlier decrypt
  call (which was WIP e1-e6's scope, already done). Confirmed absent in
  `memory_engine/api.py:candidate_facts`'s returned shape — that
  function's own docstring calls its 7 keys a "frozen interface... never
  redo," so adding an 8th key is itself a disclosed, deliberate part of
  this REQ, not incidental.
- 17 total callers of `apply_injection_contract` exist in this codebase
  (`grep -rl`), including production-critical ones this REQ's build must
  account for: `harness/orchestrator.py` (the live turn path),
  `server/voice_orch.py`, `server/memory_dashboard.py`,
  `memory_engine/recall.py`, `memory_engine/api.py` — plus roughly a
  dozen eval/test harness files whose own fixtures may assert INJ-3's
  CURRENT strict behavior and could regress if the build changes more
  than the one narrow permit condition this REQ scopes.

## CONSTRAINTS

- Change the enrollment CHECK, not the deny STRUCTURE. `_inj3_cross_
  member_deny` gains one additional `if` branch; INJ-1/INJ-2/INJ-4/
  INJ-5/INJ-6/INJ-6b/INJ-7 are not touched, and the existing three
  permit conditions in INJ-3 are not touched or reordered.
- Every genuine cross-member denial that holds today must still hold —
  the build's own verification must show this, not assume it (acceptance
  test item 5). In particular: an ordinary personal fact (no
  `recipient_ref`) between two non-care-team members must deny exactly
  as it does today — Sarah must still never read Bill's fact about Elena
  when neither is a care team.
- Do not weaken `subject_visibility=EXCLUDE`. The build must not add a
  new INJ-3 permit path that a decrypt-excluded caregiver could reach —
  item 3 of the acceptance test exists specifically to catch that.
- Do not touch `harness/write_rule.py`, `harness/care_team_keys.py`,
  `harness/partition_crypto.py`, or any of the six decrypt-routing
  fixes from the prior session — this REQ is authorization-layer only,
  downstream of an already-correct decrypt layer.
- Must not break the 13-row REQ_PARTITION_CUSTODY table or lean
  `--layer 7` (PS1-PS4 + fault injections). Both must be re-run and
  reported green before any push, same standard as every prior phase in
  this Stage.
- No new model call. `is_active_caregiver` is a deterministic SQLite
  lookup, same as every other input INJ-1 through INJ-7 already read.

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, as a
co-equal objective to the fix itself. We do not rig the build for it.

SHOW: sam and maya both enrolled on ray's care team. Maya authors "Ray
fell last night." Sam asks a query that resolves to ray and matches the
fact's attribute. The fact is admitted, live, visibly — not narrated.
Then: bill (not enrolled) asks the identical query about ray — the fact
is withheld, visibly, the same INJ-3 deny path as any other cross-member
personal fact.

LET THEM RUN: hand the engineer the fixture. Let them enroll a fourth
member on a recipient's care team, write a fact as one caregiver, and
read it as another — watch it work. Let them try to read a `flag_safety`
-excluded fact as the excluded caregiver — watch it fail exactly as it
would for a total stranger, because the wrap never existed for them.

THE CLAIM IT PROVES: "A care team's shared visibility is a real,
enrollment-gated audience — not a backdoor, not a wider default, one
narrow rule that only fires when enrollment actually exists, and every
other cross-member wall in this system is unchanged."

THE HARDEST QUESTION + HONEST ANSWER: "You just widened the rule that
protects every private fact in this system from every other member
reading it — how do you know you didn't loosen something you didn't
mean to?" Answer: the acceptance test's item 5 is the answer, not a
promise — every existing INJ-1 through INJ-7 denial is re-verified, not
assumed, in the same run that proves the new permit path. If any of
those regress, this REQ is not MET, full stop, regardless of whether the
new care-team read works. The honest limit stated before they find it:
this REQ does not audit all 17 callers of `apply_injection_contract`
individually for correctness with the new field — it fixes the
authorization RULE and the production-critical fact-dict builders named
above; a caller this REQ's build did not touch and did not verify keeps
its old, unmodified behavior (denies a care-team fact it can't yet see
the enrollment for) rather than silently gaining new access it was never
tested to have.
