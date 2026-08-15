# REQ_WRITE_TIME_CLASSIFIER: Stage 4 Phase 2
Status: NOT MET
Reconciled-Against: REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831 (e4804a6)

Naming note, on the record: the plan of record's own Stage 4 order names
"partition sealed" as Phase 2, and that REQ (REQ_CRYPTO_P2_PARTITION_SEALED
__stage4-phase2, MET at 1e549a8) already carries the "stage4-phase2" slug —
its acceptance test proved the crypto-sealing MECHANISM (PS1-PS4: DEKs
sealed by class, zero server-derivable keys). This REQ is the piece of that
original phase's scope that was never built: the classification LOGIC that
decides which class a fact gets before sealing happens. It grew past what
"partition sealed" originally described as the ratifications (#1 dyad
access model, #2 household-circle, #3 role separation, #6 custody
governance) accumulated on top of REQ_PARTITION_CUSTODY. Filed under the
name given, flagged here rather than silently renamed.

## THE REQUIREMENT

The write path classifies every fact — per clause, after compound
splitting — into a scope, a subject_visibility (INCLUDE/EXCLUDE), and a
rung, deterministically, per REQ_PARTITION_CUSTODY's ratified rule. This
replaces the current `attribute == "household"` placeholder
(`harness/fact_change.py:646`) and the pre-ratification five-rule/
three-class logic in `harness/write_rule.py` with the actual ratified
model: four scopes, four-level precedence, role separation, and the
mandatory subject-exclusion rule in its widened form.

Expanded: there is no new policy decision in this REQ. Every rule it
implements is already ratified in REQ_PARTITION_CUSTODY. This REQ is
scope, not design — it turns ratified text into a buildable spec for
Stage 4 phase 2's actual build session, and does not reopen any of #1,
#2, #3, or #6.

## DESIGN

Every element below is cited from REQ_PARTITION_CUSTODY, not re-derived.
This REQ does not invent policy; it specifies how the already-ratified
policy becomes code.

**Four-role resolution** (REQ_PARTITION_CUSTODY, "Role separation," #3).
Per clause, after compound splitting, resolved deterministically, no
model call:
- AUTHOR: the authenticated identity whose device key signed the write.
- SUBJECT: from the existing subject-resolution mechanism
  (`harness/subject_resolution.py:resolve_subject`, currently wired only
  into the read path via `orchestrator.py` — this REQ's build wires it
  into the write path too) run against the enrollment roster.
  Unresolvable -> MEMBER-PRIVATE.
- OWNER (derived): SUBJECT when SUBJECT is an enrolled member with
  standing-policy rights, else AUTHOR.
- BENEFICIARY (derived): the computed key-wrap target set — the output
  of this classifier, never an author-supplied field.

**Four-level precedence** (REQ_PARTITION_CUSTODY, "The write rule"):
(1) OWNER's standing policy, (2) explicit per-fact author directive
("share with the family" / "share with the care team" / "just between
us" / "flag as safety concern"), (3) attribute+subject classification —
the deterministic default, including the coordination/observation
attribute enum and the mandatory subject-exclusion rule in its widened
form (SUBJECT != AUTHOR and attribute outside the enum -> pair-private-
or-narrower, covering subject-is-recipient as well as subject-is-
caregiver), (4) sensitivity affects handling only, never audience.

**Coordination/observation attribute enum**: `incident`, `medication_
status`, `appointment`, `vitals`, `care_plan`. Verified against
`harness/extraction_queue.py:122` (`CANONICAL_ATTRIBUTES`): `incident`,
`medication_status`, and `appointment` already exist there; `vitals` and
`care_plan` do not yet exist as canonical attributes and must be added
before this classifier can reference them, or the enum must be scoped to
the three that already exist with the gap logged, not silently
papered over.

**SUBJECT_VISIBILITY** (REQ_PARTITION_CUSTODY, "Role separation," #3):
INCLUDE or EXCLUDE, applied at key-wrap construction inside
`harness/partition_crypto.seal_by_class` — the subject's device key is
simply omitted from a care-team-class DEK's wrap set for that
value_version. Not a fifth scope. Not a decryption-time filter. Default
EXCLUDE when AUTHOR != SUBJECT and attribute is outside the coordination
enum; default INCLUDE for coordination attributes, SUBJECT == AUTHOR, or
an explicit directive.

**Compound-statement splitting** (REQ_PARTITION_CUSTODY, "Compound
statements are split, never single-classified"): a clause with mixed
audiences is split into separate facts before role resolution runs, each
classified independently. A classifier that cannot split falls back to
fail-private (member-private) for the whole statement.

**Key classes to wrap against** — three new, one existing:
- PAIR (existing, built): `harness/dyad_crypto.py` /
  `harness/dyad_registry.py`.
- MEMBER (existing, built): `harness/member_crypto.py`.
- CARE-TEAM (new): the care-team key class from REQ_PARTITION_CUSTODY's
  custody policy — wrapped to each enrolled caregiver, epoch-versioned.
  No existing file implements this; `harness/household_keys.py` is NOT
  this — see WHAT'S KNOWN BROKEN.
- HOUSEHOLD-CIRCLE (new): `harness/household_keys.py` exists but
  implements the superseded any-adult-inferred model, not the ratified
  enrolled-roster/epoch model — see WHAT'S KNOWN BROKEN. Requires rework,
  not net-new build from zero.

**OWNER's standing policy at level 1**: a policy object per OWNER,
evaluated deterministically at write and read time, never free-text the
model weighs. Where OWNER lacks capacity, an explicitly recognized legal
or delegated authority sets it (ties to REQ_PARTITION_CUSTODY #6's
tiered-consent language for who may set policy on OWNER's behalf).

**Mandatory subject-exclusion rule, widened form** (REQ_PARTITION_CUSTODY,
level 3, generalized 2026-07-21): SUBJECT != AUTHOR and attribute outside
the coordination/observation enum -> PAIR-PRIVATE-OR-NARROWER, HARD,
non-overridable, not releasable by a level-2 directive except through the
distinct "flag as safety concern" directive. This is the one rule in this
REQ's design that itself represents a change to previously-ratified text
(REQ_PARTITION_CUSTODY says so explicitly) — this REQ implements that
widened form, it does not choose between the old and new trigger.

## THE ACCEPTANCE TEST

Pass/fail only, against a live fixture, no `--full`:

1. The write path assigns the correct scope AND subject_visibility for
   every row of REQ_PARTITION_CUSTODY's 13-row table
   (`docs/requirements/REQ_PARTITION_CUSTODY__stage2-ratification__
   v20260721_0831.md`, "THE ACCEPTANCE TEST" section) — this is what
   finally makes that table runnable against a fixture instead of
   asserted by hand. All 13 rows, not a subset.
2. Wrong-key/wrong-subject cannot decrypt: for every row whose expected
   scope excludes an identity, that identity's attempted decrypt is
   denied — reusing the existing layer-7 N1/N2/N4 invariant pattern, run
   against classifier-assigned facts instead of manually-constructed
   test facts.
3. A characterization-about-another-person routes subject-excluded: row
   11's class ("Maya keeps leaving Ray alone all day," Sam, Maya an
   enrolled caregiver) and the Susan/Dad-drinking case from the role-
   separation ratification both land PAIR-PRIVATE with SUBJECT_VISIBILITY
   = EXCLUDE for the subject, and a bare "share with the care team"
   directive on the same fact does NOT release it.
4. A coordination event routes care-team INCLUDING the subject: row 2
   ("Ray fell last night," Sam, care team) lands CARE-TEAM-PRIVATE with
   SUBJECT_VISIBILITY = INCLUDE — Ray is not excluded from his own fall
   record.
5. Fault injection, mandatory per this repo's own pattern (every
   invariant in this doc set must be shown to go red on purpose before
   it is trusted): a hand-constructed fact whose classifier inputs
   should trigger EXCLUDE but whose wrap set is deliberately built with
   INCLUDE instead flips the wrong-subject-cannot-decrypt check red.

Any single failure among 1-5 is FAIL. There is no partial credit.

## WHAT'S ALREADY DONE

- The crypto-sealing MECHANISM this classifier's output feeds:
  `harness/partition_crypto.py` (`seal_by_class` / `decrypt_fact_value_
  for_caller`, the single chokepoint every v2 seal/unseal routes through),
  `harness/member_crypto.py` (member-private, one-hop), `harness/dyad_
  crypto.py` + `harness/dyad_registry.py` (pair-private, two-hop, custody
  wraps). Verified BUILT and MET via layer-7 PS1/PS2/PS3/PS4 and DK1/DK3/
  DK4 (`== L7: 19/19`, RATCHET PASS, 2026-07-20/21 runs on the mini's dev
  graph). This REQ's build must call into `seal_by_class`, not modify it.
- `harness/subject_resolution.py:resolve_subject` — a working subject-
  resolution primitive, currently wired only into the read path
  (`orchestrator.py:46`). Reusable for the SUBJECT role above; not yet
  reused.
- `harness/extraction_queue.py:122` `CANONICAL_ATTRIBUTES` — the
  attribute enum this classifier reads from, including `incident` and
  `medication_status` (already correctly typed for the coordination
  enum) and `appointment`.
- The 13-row acceptance table itself (REQ_PARTITION_CUSTODY) — ratified,
  not this REQ's to redesign, only to make executable.

## WHAT'S KNOWN BROKEN

- `harness/write_rule.py` implements the OLD five-rule/three-class model
  verbatim and unedited since before the 2026-07-20 ratification:
  `CLASS_HOUSEHOLD = "household-shared"`, `CLASS_DYAD = "dyad-private"` —
  neither the household-circle rename nor the care-team/pair-private
  split has reached this file. Its own docstring still cites "Phase 1
  built rule 3's lookup... this module is the full 5-rule order" — a
  description that predates every ratification since. This is the
  placeholder this REQ replaces.
- `harness/fact_change.py:646`: `effective_owner = "household" if
  attribute == "household" else owner` — the specific line-level
  placeholder named in the build's own dispatch history (cited there as
  line 630; verified here at line 646 — the file has moved since,
  cite the current line, not the historical one).
- `harness/household_keys.py` is NOT the household-circle key class this
  REQ needs. It is real, built code (302 lines) implementing the
  SUPERSEDED "household-shared: any adult member" model: membership
  inferred from adulthood, no explicit enrollment, no epoch versioning,
  and its own docstring defers revocation-on-removal to a different,
  not-yet-filed REQ ("REQ_CRYPTO_P4_RECOVERY_EVICTION's job, not this
  phase's"). Needs rework against REQ_PARTITION_CUSTODY's ratified
  enrolled-roster/epoch model, not net-new build from zero — and not a
  silent drop-in reuse either.
- No CARE-TEAM key class exists at all — not even a superseded one.
  Nothing in `harness/` wraps a key per enrolled caregiver-of-a-recipient
  set.
- `subject_visibility` / `SUBJECT_VISIBILITY`: zero occurrences anywhere
  in the codebase. Fully unbuilt.
- Role resolution (OWNER/BENEFICIARY derivation, the write-time wiring of
  SUBJECT via `resolve_subject`): fully unbuilt.
- The coordination/observation enum is incomplete against the ratified
  design: `vitals` and `care_plan` are not in `CANONICAL_ATTRIBUTES`.
  This REQ's acceptance test cannot be run as written until that gap is
  either closed or the enum is explicitly scoped down with the gap
  logged — silently treating the ratified five-item enum as the three
  that happen to exist today would understate what "coordination-class"
  covers and misroute real coordination facts filed under `vitals` or
  `care_plan` language.
- The 13-row acceptance table has never run against a fixture — this
  REQ's own acceptance test is what finally makes that possible; it does
  not run today because nothing computes SUBJECT_VISIBILITY or the four
  roles at all.

## CONSTRAINTS

- Do not break the existing layer-7 crypto invariants. `PS1`/`PS2`
  (server-derivation audit, no DEK to master), `DK1`-`DK4` (custody
  ledger, overlapping-dyad isolation), `N1`/`N2`/`N4`/`P1`/`P2`/`P4`, and
  both PS1/PS2 fault injections must stay green — run `python -m
  eval.harness --layer 7` (lean, not `--full`) before and after, and the
  post-build run must show `== L7: 19/19` with no new failures against
  the current baseline, the same standard applied to every prior Stage 4
  phase build in this doc set.
- Do not touch `harness/partition_crypto.seal_by_class`'s contract — this
  REQ's classifier is a new input to that function's existing
  classification call, not a rewrite of the sealing chokepoint itself.
  `seal_by_class` already imports `harness.write_rule`; swap what it
  calls, not how it seals.
- Do not touch the frozen main demo. This build lives on `roadmap` only;
  `main` is out of scope for every phase of this Stage, unchanged since
  Stage 0 branched at 688386f.
- No new model calls on the write path — every input this classifier
  reads (speaker, subject, attribute, sensitivity, dyad/care-team
  registry, directive text) must already exist at write time, per
  REQ_PARTITION_CUSTODY's own constraint, carried forward unchanged.
- Dual-envelope discipline holds: v1 facts are untouched by this build:
  this REQ classifies new v2 writes only. The re-seal/migration cutover
  is Phase 3's job, not this REQ's.

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, as a
co-equal objective to the classifier itself. We do not rig the build for
it.

SHOW: the 13-row table run live, each utterance spoken, the scope and
subject_visibility it lands in named aloud. "Susan: Dad is hiding his
drinking" lands pair-private, Susan only, Dad's key excluded from the
wrap — visibly, not narrated. "Ray fell last night" lands care-team-
private, Ray included. The fault-injection run flips a deliberately
miswrapped fact's wrong-subject-cannot-decrypt check red, on command.

LET THEM RUN: hand the engineer the fixture. Let them compose an
utterance naming a caregiver as its subject and watch the mandatory
exclusion fire without any directive telling it to. Let them try to
widen a characterization about someone else via "share with the care
team" alone, and watch it fail to release — only "flag as safety
concern" can.

THE CLAIM IT PROVES: "Every fact's audience is computed the same way,
every time, from fields that existed before generation started — not a
model's guess, not an author's unchecked say-so about who else it
concerns."

THE HARDEST QUESTION + HONEST ANSWER: "You're implementing a widened
mandatory rule that changes who reads facts already written under the
old write_rule.py logic before this build lands — what happens to
those?" Answer: nothing, on purpose, in this REQ. This classifier
governs new v2 writes only; nothing here re-classifies or re-wraps a
fact written before this build lands — that is a migration question,
explicitly out of scope here and belonging to Phase 3's re-seal cutover,
the same dual-envelope discipline every other phase in this Stage has
already accepted. A skeptical engineer should not be told this build
retroactively fixes every fact ever written under the old rule — it
does not, and the doc says so before they find it.
