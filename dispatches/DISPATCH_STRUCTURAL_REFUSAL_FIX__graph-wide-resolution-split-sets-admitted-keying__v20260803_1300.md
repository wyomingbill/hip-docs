# DISPATCH_STRUCTURAL_REFUSAL_FIX
Status: BUILT
Reconciled-Against: 2026-08-03 (D-127; parent 1591477 at dispatch time)

**TYPE:** BUILD

**REQ:** `REQ_STRUCTURAL_REFUSAL__adjacent-admissions-must-not-suppress-
empty-set__v20260803_1108.md` (named by D-127; evidence item 1 AMENDED in
place this dispatch per Bill's instruction — original wording kept,
annotated with D-126's traced mechanism). The REQ stays NOT MET; readiness
reported; Bill rules.

## THE RULINGS (Bill, 2026-08-03) AND WHERE EACH LANDED

**(a) Keying (1)+(2) built together** — neither closes the hole alone:
1. **Graph-wide resolution** (`harness/role_resolution.graph_subject_ids`,
   new): all subjects on ACTIVE facts, unioned at the voice_orch call site
   with `known_subject_ids()` (registry members + dyad recipients +
   care-team recipients) and registered members, passed to
   `subject_resolution.resolve_subject` as its Phase-3 known-set. Fails
   toward the OLD narrower resolution (any error → empty set → pre-D-127
   behavior), never toward a wrong refusal.
2. **Admitted-set keying** (`harness/injection_contract.py` INJ-6b): the
   refusal now keys on the ADMITTED set alone (`not allowed_hit`).
   **CRITICAL DESIGN POINT — TWO ID SETS, NEVER MERGED:** the widened set
   feeds ONLY `resolve_subject`; the contract's `member_ids` stays
   REGISTERED MEMBERS ONLY, because INJ-7 treats membership as the
   cross-member boundary — merging the sets would have made INJ-7 deny
   maya her own ray facts. The voice_orch call site carries the comment.

**(b) Deny-silently preserved by REFUSAL IDENTITY:** exists-but-withheld
and does-not-exist produce the identical structural refusal (battery case
`test_sref_deny_silently_refusal_identity` asserts identical guard kind,
identical admitted set, no needle). A named residual, honest not hidden:
subject-KNOWNNESS is now observable (a graph-known subject gets a fast
structural refusal; an unknown string goes to the model) — that leaks that
a NAME is known to the household graph, not that any FACT exists. Recorded
for Bill; fact-level indistinguishability is what ruling (b) demanded and
is upheld.

**(c) Withheld-but-visible OFF the model path:** INJ-6b's `candidate_hit`
carve-out REMOVED (it was a 4-line condition — small change, no STOP
needed). If the contract withheld a fact, the model does not receive it
and no longer gets to be the thing deciding the refusal. Blast radius
checked: the carve-out could only trigger for requester-visible-but-denied
facts (owner-scoped retrieval means another member's facts never reach
your candidates); the harness agrees — zero regressions (evidence below).

**(d) PW015's row expectation corrected** (matrix `_meta.d127_pw015_note`
records why, citing D-126): `empty_set` → `no_leak`. Sam's own
medication_status fact about dad is admitted and in family(medication);
the D-24 rule keeps the model in the loop BY DESIGN. The row now fails
only on a foreign-needle leak or wrong access-control denial — stable
against model whim in both directions. TD-144's accepted-red is
superseded by this correction.

**(e) SIO-derived asked-attributes NOT in scope — TD-149 filed** (register
v20260803_1310): the structural keying covers `_TARGETED_ATTRS`' twelve
attributes; the widening path is scoped there, UNGOVERNED, needs a REQ.

## RESOLUTION IS NOT DISCLOSURE — said in code, proven live

Said: in `graph_subject_ids`' docstring and the voice_orch call-site
comment. Proven: (unit) `test_sref_*` asserts the allowed set is
byte-identical with and without the widened resolution for the same
inputs; (live) every existing row's admitted counts unchanged across the
before/after matrix runs — PW011/PW012 owner reads disclose exactly as
before (verified individually below), PW013/PW014/PW017 admitted sets
unchanged, and the only rows whose records changed are the five whose
REFUSALS became structural.

## ACCEPTANCE — PW031-033 FLIP, twin red, anti-vacuity

- **PW031/PW032/PW033: FAIL → PASS with `guard.kind='empty_set'` and
  `inference_ms=None`** (structural, no model in the loop), BOTH runs.
- **PW010 flipped too** — same mechanism, same fix. TD-143's red is
  closed by this build, pending Bill's ruling on that TD.
- **PW015 PASSES under the corrected expectation**, model answering from
  admitted content (inference_ms ≈5860 — model path, as designed).
- **PW011/PW012 individually: PASS, value disclosed** (owner reads did
  not regress; PW011 `value 'metformin'`, PW012 `value 'empagliflozin'`).
- **The REQ's fault twin reproduces the broken mechanism and goes red**:
  `test_sref_ray_resolves_with_widened_set_only` first asserts the
  PRE-FIX known-set still yields `resolved=[]` (the red direction — if
  that stops reproducing, the twin loudly demands re-establishment), then
  that the widened set resolves ray (green). Anti-vacuity per D-87:
  `test_sref_graph_known_set_is_not_vacuous` requires {ray, dad} ⊆ the
  graph-known set, so an empty or misdirected graph read cannot pass.
- STRUCT-REFUSAL battery (`eval/test_structural_refusal.py`, 7 cases
  `test_sref_*`, 22nd standing battery in run_harness.sh): 7/7 —
  including `test_sref_inj7_member_boundary_unchanged` (member subject
  still access-denies; ray still does not) and
  `test_sref_owner_read_still_discloses`.

## RUNS, read individually

- Pairwise matrix, TWICE (Bill's step 4): **L4 30/34 both runs (0
  failures, 4 design skips), identical row-for-row — NO FLIP.** The four
  structural-refusal rows show `inference_ms=None` in both runs.
  Baseline: five rows locked in as improvements via `--update-baseline`
  (PW010, PW015, PW031-033). SECOND TOOL FINDING on that updater: this
  time it DROPPED the entire `_accepted` map including L1:P2's unrelated
  justification — restored by hand (L1:P2 only; the five retired
  justifications correctly expire, their record living in TD-143/144 and
  the D-126/D-127 docs). Same tool, second governance-relevant side
  effect in two days (D-126 recorded the first); TD-filing is Bill's
  call.
- `--layer 7`: **L7 27/27, L7V2 27/28 (opt-in skip), RATCHET PASS — no
  scenario regressed**; four-part-roster PASS (59 checks);
  COVERAGE-GRID-RATCHET PASS; batteries **323 passed / 8 xfailed**.
- The two ABSOLUTEs this could disturb, individually: **CTX-STRIP: PASS.
  PSA1: PASS.** (Also OB6/G0/LI1 PASS.)
- `--full` (log hip_harness_20260803_1300; first attempt refused by the
  TD-129 guard at 1.96GB free — reclaim decayed between check and launch;
  relaunched with in-line reclaim): AUDIT 8/8, DISC 1/1, L1 14/15,
  L2 25/35 (1 flaked-then-passed, 10 skipped), L3 3/3, **L4 30/34 — every
  flip holding in the full run**, L7 27/27, L7V2 27/28 (opt-in skip),
  SCHEMA 1/1, VOICE 1/1, COVERAGE-GRID-RATCHET PASS. **One NEW-FAILURE
  line, verified to be the identical TD-147 known red** (L6
  record-invariants: the sam/atorvastatin G1 orphan, same record text) —
  loud per Bill's own D-118 ruling that its baseline stays unupdated;
  documented Groq-extraction lineage, mechanism unreachable by this
  change and predating it.
- Memory harness, run twice (second run unintentional, reported not
  hidden): **14/17 failing {MEM-115, MEM-116, MEM-117}**, then **15/17
  failing {MEM-115, MEM-116}** — MEM-117 flipped between runs, confirming
  its fact_change live-write flake family (TD-147's addendum). Both runs
  inside the 13-15/17 pin, failures ⊆ {115,116,117,118}, NOT the 16/17
  STOP.

## PROCESS NOTES

- Gate passed; lock read-first (free), noclobber take 12:42:41; released
  after push. Repo `.env.dev` only.
- The mutation harness's hardcoded INJ-7 line anchors (TD-142,
  :656-674/:664): my INJ-6b edits sit BELOW that block — line numbers
  above it unchanged, self-test unaffected (verified by the layer-7 run's
  mutation suite passing).
- Committed AROUND the cutover lane's WIP — explicit pathspecs, surgical
  INDEX stage.

## OPEN

- **The REQ's MET ruling** — acceptance halves (a) and (b) both now have
  running evidence; Bill rules.
- **TD-143**: closed by this fix on the evidence; Bill rules the TD.
- **TD-144**: row expectation corrected per ruling (d); the TD's
  remaining substance (the class, not the row) is carried by the REQ.
- **TD-149**: the untargeted-attribute widening, needs a REQ.
- The subject-knownness residual named under ruling (b), if Bill wants it
  tracked.
- Nothing ruled MET.
