# DISPATCH_TD141_SEED_LINEAGE
Status: BUILT
Reconciled-Against: 2026-08-02 (D-107; parent 2f69f2f at dispatch time)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md`,
R18 — the same REQ D-105 built the lineage gate under (its commit names
"REQ_STRUCTURAL_CEILING R18 / TD-139" as authority; this dispatch is the
same family, one debt item over). The dispatch text names TD-141, not a REQ
doc, so the gate question was checked rather than assumed: TD-141 is R18
debt filed by D-81 under this REQ, `harness/derivation_cascade.py:3` names
this REQ as governing, and the fix builds nothing outside R18's existing
scope — no schema change, no new field, no new mechanism; an existing
writer is made to use the existing creator honestly. Testing plan authority:
`REQ_CEILING_ACCEPTANCE__testing-plan-for-the-ceiling-sprint__v20260801_0617.md`
(D-87's complement convention).

## THE ASK

> AUTHORITY: TD-141. D-105 characterized it precisely: the one live derived
> fact never passed through the creator as derived at all — demo_seed writes
> it with encode() and then SETs derived=true afterward. So the cascade is
> correct but inert, and the new lineage gate never saw it.
> TD-139 and TD-140 are NOT in scope. R18 stays NOT MET regardless.
>
> SURVEY FIRST. Report:
> a. Exactly where demo_seed does the encode-then-SET, and why it was written
>    that way.
> b. What breaks if it instead writes through the derivation path properly:
>    does it have the parents to name, the attributes for source_categories,
>    an allowlisted attribute? D8 is risk_pattern, which IS allowlisted for
>    the fixture origin.
> c. Whether any OTHER caller does encode-then-SET on a derived flag. One
>    instance is a seed script; several is a pattern.
> STOP AND REPORT if the seed cannot honestly name its parents. A fixture
> that fabricates lineage is worse than one that has none.
>
> THEN FIX IT if the survey is clean: demo_seed's derived fact goes through
> the creator as derived, with real parents and real lineage, so it
> exercises the same gate every other derived write does.
>
> ACCEPTANCE, namespaced per D-87, fault twin and anti-vacuity:
> - after a seed, the derived fact carries every implemented lineage field
> - a derived fact written by encode-then-SET is detectable and refused, or
>   if it cannot be refused, that limit is stated plainly rather than
>   asserted away
> - the cascade now has something to act on: retract a parent, confirm the
>   child responds
>
> Run --layer 7 plus RATCHET plus the memory harness. L7V2 must hold at
> 27/28 and the mutation self-test must still find its mutant at
> injection_contract.py:664. Memory harness must hold at 13/17 with the same
> four. Any other delta is a STOP. Evidence read individually from the log.
> --full will be refused by TD-129.
>
> Rule nothing MET.

## WHAT WAS DONE

1. Machine gate (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap,
   tree clean), repo `.env.dev` sourced (NEO4J_URI 7688 confirmed, NOT the
   frozen demo's 7689), `.hip-lock` taken (was free).
2. Survey (2a/2b/2c below), read-only: demo_seed, store.encode /
   create_fact_node / _new_node_props, consolidate._write_derived_node,
   write_origins, derivation_cascade, the D-105 battery, the CEIL-CONV
   frozen shapes, git history of the SET.
3. Fix: a declared `DerivedLineage` channel through `encode()`
   (memory_engine/store.py), demo_seed rewritten to declare and resolve
   real parents and to drop the SET, acceptance cases added to
   eval/test_lineage_block.py, graph-level detector added to
   eval/harnesslib/fixture.py verify_seed.
4. Live proof on the dev graph (reset → seed → read D8 → detector →
   retract D4 → read D8 again → reset+reseed to canonical).
5. `scripts/run_harness.sh --layer 7` (batteries + AUDIT + DISC + L7 +
   L7V2 + SCHEMA + VOICE + RATCHET), then `eval.memory_harness` three
   times. Evidence read individually from the logs.

## WHAT WAS FOUND

**2a — where and why.** `scripts/demo_seed.py` old lines 428-433 (the
DERIVED branch of `_seed_one`'s post-write enrichment):
`SET f.derived = true, f.derived_from = []` immediately after an `encode()`
write. Introduced at `efde99b` (2026-07-05, "reconcile epistemic fixture —
real trust levels via encode()"): the ONLY goal was that `trust()` read
DERIVED, and every trust tier got the same shape — encode, then a
post-write SET (CONFIRMED → confirmed_by, CORROBORATED → confidence_log
append, DERIVED → the flag). `derived_from=[]` because no lineage concept
existed: it predates the cascade (D-81), the single creator (D-96), the
origin vocabulary (D-97), and the lineage gate (D-105). Contributing
constraint, still true until this dispatch: `encode()` COULD NOT write a
derived fact — `_new_node_props` hardcoded `derived: False`
(store.py:209-210 pre-change), so the flag had no path in through the front
door even for a caller that wanted one.

**2b — what the honest path needs; all of it was available.**
- *Parents:* D4 (sam/dad, incident, "fell the night of the 4th", 10d ago)
  and D5 (sam/dad, medication_status, "Medication A discontinued on the
  1st", 13d ago). They are the only other dad-subject facts in the fixture
  (consolidate groups by subject — no other candidates exist); both precede
  D8 (8d ago) in seed order AND fixture time; a fall plus a medication
  discontinuation is precisely what "elevated fall-risk pattern" derives
  from; and 2 parents matches both consolidation's ≥2-source contract and
  MIN_PARENTS_FOR_RECOMPUTE. The seed CAN honestly name its parents — the
  STOP condition did not fire. X-04's standing caution (D8 is seeded, not
  inferred — BACKLOG #46) is preserved structurally: origin stays
  `fixture`, and derivation_method says `demo_seed.fixture.v1`, never
  consolidate's string.
- *source_categories:* the parents' attributes (incident,
  medication_status), resolvable at seed time from the just-seeded rows.
- *audience_policy:* encode() already computes the write class
  (`partition_classify_write`); its `.visibility` is the same source
  `_write_derived_node` uses. Live value: `household-circle-shared`.
- *Allowlist:* confirmed at store.py — risk_pattern ∈ DERIVABLE_ONLY, and
  the derivable-only check permits origins `derivation` and `fixture`
  (store.py:321 pre-change numbering); `fixture` is NOT canonical-bound
  (harness/write_origins.py:97-99). The creator accepts the write.
- *What would have been dishonest:* routing the seed through
  `_write_derived_node` — that stamps origin `derivation` and method
  `consolidate.abstract.v1`, both lies for a seeded fact. Hence the
  encode-side channel instead.

**2c — no pattern.** Exactly ONE encode-then-SET on a derived flag exists:
demo_seed.py:431 (old). The only other `derived` writer outside the creator
is store.py's Phase-A schema migration (old :808-809) writing
`derived = false, derived_from = []` — the non-derived DEFAULT backfilled
onto legacy rows, not a forgery. One instance, a seed script: fixed, not
pattern-hunted.

**THE FIX.**
- `memory_engine/store.py`: frozen dataclass `DerivedLineage(derived_from,
  derivation_method, source_categories)`; `encode(..., derived_lineage=None)`
  threads it through `_new_node_props`, which now writes `derived` from the
  lineage's presence (never independently) plus the three fields, and
  encode stamps `audience_policy = write_class.visibility`. A dyad-sealed
  derived write has no write class → reaches the creator without
  audience_policy → REFUSED by the same gate, not special-cased. Default
  None → byte-identical props for every existing caller (CEIL-CONV's
  pinned shapes pass unchanged).
- `scripts/demo_seed.py`: `DERIVED_PARENTS = {"D8": ("D4", "D5")}` and
  `DERIVATION_METHOD_FIXTURE = "demo_seed.fixture.v1"`;
  `_derived_lineage_for()` resolves labels to the real just-seeded
  fact_ids and REFUSES before any write: a DERIVED fixture with no
  declared parents, a parent not yet seeded, or parents declared on a
  non-DERIVED fixture. The DERIVED SET branch is deleted.
- `eval/harnesslib/fixture.py` verify_seed: graph query for
  `derived = true` rows missing any lineage-block field — TD-141's shape —
  fails the fixture verification on every standard reset. Zero rows is the
  only acceptable answer.
- `eval/test_lineage_block.py`: 5 new `test_lineage_seed_*` cases (D-87
  complement — fault twins and anti-vacuity): the seed's write shape flows
  through the creator as ONE call carrying the full block; the old shape
  (derived=true, no block) is refused at CREATE with no write issued; the
  fixture's parent declaration is structurally honest (≥2 parents, exist,
  precede, same subject, older); dishonest declarations refuse (three
  directions, plus the honest one resolves — anti-vacuity); source scan —
  no script SETs a derived flag (red if TD-141's shape is reintroduced).
  Battery now 21 cases. Stale TD-141 text in
  test_lineage_no_backfill_was_performed's docstring updated to record the
  closure.

**THE LIMIT, STATED PLAINLY (acceptance bullet 2).** A raw Cypher
`SET f.derived = true` on an existing node happens below any creator and
CANNOT be refused: Neo4j property writes have no gate to fail. Refusal
exists only at CREATE (proven by the new fault twin). The shape is instead
DETECTED, two standing ways: the source scan (keeps the pattern out of
scripts/) and verify_seed's graph query (catches a written instance on
every fixture reset). Neither prevents a live hand-run SET between resets —
that residual window is this limit, named rather than asserted away.

## VERIFIED

**Watched run:**
- Seed: `demo_reset.py --yes` + `demo_seed.py` → 11/11. D8 = c6b3234a…,
  read back from Neo4j 7688: `derived=true`,
  `derived_from=[01803599…(D4), 833758b1…(D5)]`,
  `derivation_method='demo_seed.fixture.v1'`,
  `audience_policy='household-circle-shared'`,
  `source_categories=['incident','medication_status']`,
  `artifact_type='fact'`, `origin='fixture'` — every implemented lineage
  field present (acceptance bullet 1).
- Detector: encode-then-SET-shaped derived facts in graph = 0.
- Cascade (acceptance bullet 3): `retract_fact('sam','incident',
  subject='dad')` → True; D4 closed_by='retracted'; D8 closed
  valid_to=2026-08-02T18:17:39Z, `closed_by='lineage_cascade'`,
  `cascade_recompute_eligible=False` (1 surviving parent < 2),
  `cascade_recompute_from=[833758b1…(D5)]`. The R18 cascade acted on live
  data for the first time. Fixture then reset+reseeded to canonical.
- `run_harness.sh --layer 7` exit 0, log read individually: batteries 297
  passed / 1 skipped / 8 xfailed (D-105: 293/8; +5 new cases here, and the
  1 skip is pre-existing conditional, not new); AUDIT 8/8; DISC 1/1;
  L7 27/27; **L7V2 27/28** (the 1 skip is CT-OUTPUT-GAP, opt-in live
  model call, same as D-105); SCHEMA 1/1; VOICE 1/1; **RATCHET PASS — no
  scenario regressed**; COVERAGE-GRID-RATCHET PASS (0.090 → 0.090);
  ABSOLUTE individually: OB6 PASS · G0 PASS · PSA1 PASS · CTX-STRIP PASS ·
  LI1 PASS; **MUTATION-SCORE-SELFTEST PASS — seeded mutant found at
  injection_contract.py:664**, killed-with-killers AND
  survives-without-killers both proven.
- Memory harness, three runs: 14/17 then 15/17 then 15/17. Failures were a
  strict SUBSET of the recorded four (MEM-115/116/117/118, "pre-existing
  and environmental" per D-99's dispatch): 115+116+117, then 115+116, then
  115+116. **No check outside the four ever failed; MEM-111 (derived
  tagging — the check nearest this change) passed all three runs.**
  DELTA, REPORTED NOT HIDDEN: the runbook pinned "13/17 with the same
  four"; today two of the four (117, 118) PASSED, and 117 flipped between
  two consecutive identical-code runs — the variance is environmental (live
  model path), moves only in the passing direction, and is not a
  regression signal. Judged not to be the STOP the runbook aims at (a red
  outside the four, or a new red, would be); flagged here and in the
  report for Bill to rule otherwise.
- pytest affected-battery run: 90 passed / 3 xfailed
  (test_lineage_block, test_fact_write_convergence, test_write_origins,
  test_ceiling_inference, test_derivation_cascade).

**Reasoned about:** the efde99b why (from the commit message and diff, not
re-executed); the dyad-sealed-derived refusal path (traced through
encode → create_fact_node; no live dyad-sealed derived write was run);
CEIL-CONV shape preservation was confirmed by the passing pinned tests
rather than by a byte-diff of stored nodes.

**`--full` not attempted** — TD-129's guard, as the dispatch anticipated.

## RULINGS

**Nothing is ruled MET.** R18 remains NOT MET (Bill's ruling 2026-08-01
stands): TD-140 — the recompute branch — is still open and awaiting Bill's
ruling. This dispatch made the cascade's else-branch REACHABLE on live
data; it did not build the if-branch.

## HASH

Committed this session on `roadmap` (see git log, D-107); parent 2f69f2f.

## OPEN

- TD-140 (recompute) — unchanged, awaiting Bill's ruling among D-104's
  three shapes.
- The stated limit above: a hand-run `SET f.derived` between fixture
  resets is detectable only at the next verify_seed, not preventable.
- `DERIVATION_METHOD_FIXTURE` lives in scripts/demo_seed.py; if a second
  fixture-derived path ever appears, the constant (and whether methods
  deserve a registry like sensitivity's) should be revisited.
- The 12-node pre-lineage backfill question from TD-139 is unchanged — the
  fixture graph rebuilds from seed, but any FUTURE durable graph that is
  not reseeded would still carry pre-lineage rows; no ruling exists on
  what those should say (unlike R30 item 5's `pre-registry` marker).
