# DISPATCH_D23 — Curator Stage 1: the learner-isolation gate, built before any learner
Status: BUILT (assessment staged for Bill — no self-MET)
REQ: docs/requirements/REQ_LEARNER_SIGNAL_ISOLATION__training-signal-partition-parity-with-retrieval__v20260727_0828.md (extended same dispatch with Bill's 2026-07-29 rulings, REQ-first, before code)
Branch: roadmap
Reconciled-Against: layer-7 run 2026-07-29 (RATCHET PASS, exit 0), log in session scratchpad (d23_l7.log)

## RULINGS ENCODED (Bill, 2026-07-29, D-23)

1. STRICT isolation with carried household provenance; no cross-household
   pooling of household-sourced data; shared base ONLY from
   public/synthetic/centrally-authored examples (no household provenance).
2. Intra-household scope crossing is the SAME violation class (answers the
   REQ's open question 4). Audiences are rosters; test is set containment;
   broader-into-narrower admissible.
3. ABSOLUTE-tier layer-7 check, two-household fixture, two fault twins
   (cross-household pooling; intra-household scope crossing), each red
   naming the crossing.
4. Gate decisions structurally excluded from any feature space; labels
   computed only on post-gate outcomes.

## WHAT WAS BUILT (the gate — deliberately NOT a learner)

- `harness/learner_isolation.py` — enforcement surface the future learner
  MUST route training examples through: check_training_example /
  check_training_batch, GATE_DECISION_FEATURE_KEYS (recursive key ban),
  POST_GATE_LABEL. Pure provenance validator: no graph, no model, never
  reads example text; violations are naming strings, not booleans.
- `eval/harnesslib/layer7_crypto.py` — `L7:LI1` scenario, ABSOLUTE tier
  (joins G0/G1/G4/PSA1/CTX-STRIP in the absolute_keys gate). Two-household
  in-memory fixture: hh-alpha (alice/bob/mary rosters, extends RI1),
  hh-beta (dana/eli, disjoint).
- `eval/harnesslib/check_registry.py` — L7:LI1 entry, all four
  REQ_HARNESS_DISCIPLINE artifacts real (twin marker, fixture marker,
  coverage with the honestly-named unfixtured slice — pair/care-team
  rosters reduce to the same set-containment test, named for the first
  real learner build — and metamorphic probe ref).
- `eval/harnesslib/harness_audit.py` — executable probe
  `li1_query_reword` (verdict invariant under query rewording, both
  directions), registered in PROBES.

## RUN EVIDENCE (--layer 7 via scripts/run_harness.sh, zsh, 2026-07-29)

- `L7: 26/26` (up from 25/25 — LI1 joined clean), `AUDIT: 8/8`,
  `four-part-roster PASS (58 checks, 35 flagged gaps)` — 57→58, zero new
  gaps. `RATCHET PASS — no scenario regressed vs baseline.` Exit 0.
- LI1 sub-checks, all [ok], quoted from the log:
  - clean two-household fixture: zero violations.
  - FAULT-INJECTION (red): "cross-household pooling: example li-x1 from
    household 'hh-beta' in training signal for household 'hh-alpha'
    model curator-hh-alpha-household" — names example + both households.
  - FAULT-INJECTION (red): shared-base refusal — "example li-x2 carries
    household provenance 'hh-alpha' but target curator-shared-base is the
    shared base…".
  - FAULT-INJECTION (green): pooling removed, identical judge, zero
    violations.
  - FAULT-INJECTION (red): "intra-household scope crossing: example li-x3
    (scope 'member-private', audience ['alice']) would train model
    curator-hh-alpha-household whose audience ['alice','bob','mary']
    includes reader(s) ['bob','mary'] not authorized…".
  - FAULT-INJECTION (green): same example into the member's own model
    admissible.
  - gate-decision key (nested, 'meta.denied_reasons') refused;
    non-post-gate label refused.
  - METAMORPHIC: reworded query text changes neither verdict.

## ASSESSMENT vs the REQ's acceptance (MET is Bill's; not self-marked)

1. ABSOLUTE-tier hard-zero layer-7 check, auto-run, --accept refused —
   BUILT, green (item 1): wired unconditionally in layer7_crypto.py run().
2. Cross-identity pooling assertion + gate-decisions-excluded — BUILT,
   green (items ii/iv/v above); enforcement is provenance/roster-based
   per the D-23 rulings.
3. Fault-injection twin red-on-command/green-on-removal — BUILT, green,
   BOTH twins (household pooling AND intra-household scope), both
   directions each.
4. Ground-truth two-household fixture — BUILT (hh-alpha extends
   alice/bob/mary; hh-beta disjoint by construction; human-verified
   explicit data, no model grading).
5. Coverage entry — REGISTERED, with the unfixtured pair/care-team slice
   named rather than silently absent.
6. Metamorphic wrapper — REAL (in-scenario + executable audit probe), not
   an 'na'.
7. RATCHET PASS before and after — the 'after' is this run (exit 0, no
   regression, baseline respected); the standing prior-green record is the
   'before'. CLAUDE.md item 12's --full bar has not been run within this
   dispatch (layer 7 only, per the same posture the strip-context build
   took); named honestly for Bill's MET determination, not glossed.

NOT green-as-specified: nothing. Open questions 1-3 of the REQ remain
open (OQ4 answered by ruling 2). No learner exists; the gate now predates
it, as required.
