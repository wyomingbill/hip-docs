# DISPATCH_R30_ITEM5
Status: BUILT
Reconciled-Against: 348b340 (HEAD at dispatch start)
REQ: `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` — R30 item 5
Dispatch: D-93, 2026-08-01
**Status proposed: NONE. R30 is NOT ruled MET by this dispatch.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @ `348b340`, clean.
`~/hip-vo`, `~/hip-dev`, `~/hip-harness` NOT touched. **Nothing ruled MET.**

R30's items 1–4 were already complete; **item 5 was the sole reason R30 is NOT MET**. This
builds item 5's mechanism. Whether that makes R30 MET is your ruling — and A30 already passes
while R30 is NOT MET, so a green battery here proves less than it looks like.

---

## Step 2 — inventory, before any change

| Measure | Value |
|---|---|
| total `:Fact` nodes | **12** — exactly D-81's baseline, unmoved |
| active (`valid_to IS NULL`) | 12 |
| already carrying a version stamp | **0** |
| sensitivity distribution | high 5, low 5, medium 2 |

Neo4j additionally reported that the property key `sensitivity_registry_version` **did not
exist in the database at all** — independent confirmation that nothing was stamped. **No stop
condition.**

---

## Step 3 — implemented across the three contracts

### The marker lives beside the version — one module owns both

`harness/sensitivity.py` now declares `PRE_REGISTRY = "pre-registry"` immediately after
`SENSITIVITY_REGISTRY_VERSION`, plus `VERSION_VALUES` as the complete legitimate set. A stamp
outside that set is a defect, not a new vocabulary. The comment says why in one line: *R29's
whole lesson is that a second vocabulary drifts from the first.*

### Contract 1 — the `:Fact` node. **Three write paths, not one.**

This is the part that would have silently broken the acceptance criterion. D-84 established
that `:Fact` is `CREATE`d in **three independent places**, kept in agreement by comment
discipline:

| Path | Stamped |
|---|---|
| `memory_engine/store.py::_new_node_props` + `_CREATE_FACT_CQL` | yes |
| `harness/extraction_queue.py::_write_one` | yes |
| `memory_engine/consolidate.py::_write_derived_node` | yes |

Stamping only `store.encode` would have satisfied a casual reading and made **"a fact with no
marker is impossible" false the next time either other path ran.** All three import the
constant; none carries a literal.

### Contract 2 — the D-1 record. **How the stamp does not break pure projection.**

You asked me to state this. The record has **two** version fields, and they are deliberately
different:

- **Per-fact entry** (`epistemic_record.py:105`) — `fact.get("sensitivity_registry_version")`.
  **Projected, never computed.** The record reports which vocabulary *the fact carries*; it
  does not decide one. A pre-registry fact says `pre-registry` here; a fact written today says
  `sensitivity.v1`. **Had this called the registry instead of reading the dict, every
  historical fact would be relabelled `sensitivity.v1` at read time — the exact untruth the
  backfill ruling rejected, reintroduced through the back door.** That is the whole reason the
  projection property survives.
- **Routing block** (`:280`) — `SENSITIVITY_REGISTRY_VERSION`, the current constant. Correct
  and not a contradiction: `sensitivity_tag` is computed by the router *this turn*, so the
  vocabulary in force is the current one. There is no stored decision to project.

### Contract 3 — the ledger

The ledger **dual-writes the record** rather than building its own payload, so the stamp
reaches it by construction. The chain covers it via `payload_sha256` over the payload, not
field-by-field — asserted in the battery so that a future divergence (the ledger growing its
own projection) becomes visible rather than silent.

### The migration — one-shot, applied

`scripts/migrate_sensitivity_registry_version.py`. Migration, not lazy-on-read, per the
ruling: lazy leaves the absence in storage forever and makes every reader special-case it.

```
BEFORE   total 12   unstamped 12   stamped 0
STAMPED 12 fact(s) with 'pre-registry'
AFTER    total 12   unstamped 0    by version {'pre-registry': 12}
OK — zero facts carry no marker.
```

**Idempotent, and narrowing by construction.** The MATCH is guarded `WHERE
sensitivity_registry_version IS NULL`, so it can never relabel a correctly-stamped fact as
pre-registry — the same untruth in the other direction. Second run: *"nothing to do — every
fact already carries a version marker."* It also refuses to report success if any fact remains
unstamped or if the fact count changes.

---

## Step 4 — acceptance, with evidence per row

`eval/test_registry_version_stamp.py` — **18 cases, all passing**, registered as the 14th
standing battery. Namespaced `test_ceil_rv_*` / **CEIL-RV** per D-87.

| Row | Evidence | Result |
|---|---|---|
| **1** — a new fact carries the current version | `_new_node_props(...)` executed → `'sensitivity.v1'`; plus the real `_CREATE_FACT_CQL` **EXPLAINed** against live Neo4j with the parameter bound | **PASS** (see limitation below) |
| **2** — pre-existing facts carry `pre-registry`, NOT the current version | live graph: 12 × `pre-registry`, **0 × `sensitivity.v1`** | **PASS** |
| **3** — zero facts carry no marker | live graph: **0** unstamped | **PASS** |
| **4** — record/ledger carry the same version as the fact | AST: the per-fact entry *projects* from the fact dict; the ledger inherits the record's payload | **PASS** |

**Fault twins**, one per row: an unstamped writer must fail the predicate; a writer using a
hardcoded literal must fail even though it stamps the right field; an unguarded migration
(`MATCH` without `IS NULL`) must fail the idempotency guard; and — the discriminating one — **a
record that stamps the current version onto a per-fact entry must be rejected**, because it
looks identical for facts written today and silently lies about every historical fact.

**Anti-vacuity**: all three write-path functions must exist and be findable, or a
parametrized scan would pass while checking nothing.

### Row 1's honest limitation

Row 1 is proven by the props builder plus an `EXPLAIN`, **not by an executed end-to-end
write.** The `--layer 7` run wrote no new facts (count stayed 12), and I chose not to write a
probe fact into the frozen demo graph to manufacture one. `EXPLAIN` proves the Cypher parses
and the parameter binds — a `CREATE` naming an unbound parameter is a `ParameterMissing`
error, so the property cannot be silently dropped — but it does not prove execution
semantics, and I am not claiming it does. **Row 1 will be fully live-proven the first time any
real turn writes a fact**, and the distribution query above is the check to re-run.

---

## Step 5 — harness

```
standing batteries (14 files): 201 passed, 9 xfailed   (test_registry_version_stamp.py: 18 new)
== AUDIT:  8/8   == DISC: 1/1   == L7: 27/27
== L7V2:   27/28 (1 opt-in skip)   == SCHEMA: 1/1   == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.   0 scenario FAILs.
```

All five ABSOLUTE checks read individually from the log: **G0 PASS, PSA1 PASS, CTX-STRIP PASS,
LI1 PASS, CS1 PASS.** `--full` not attempted — TD-129's memory guard refuses it on this
machine state, as anticipated.

**Note the schema change did not disturb `ORTH-2 fact schema (46 cases)`, which passed.** That
matters: adding a property to `:Fact` is exactly the kind of change that trips a schema
conformance check, and it did not.

## A predicate bug my own battery caught

First run: 3 failures. The structural predicate looked for
`sensitivity_registry_version` as a standalone AST token, which found only `store.py` —
because the other two paths embed the field name **inside a Cypher string literal**. The
battery was reporting that two of three write paths were unstamped when they were.

Fixed with `_mentions()`, which searches names *and* string-literal contents. Worth stating why
that is still not a source regex: it searches **string literals recovered from the AST**, so a
comment or docstring mentioning the field is invisible to it — comments are not AST nodes.
That is precisely the property D-75's first A29 guard lacked when it fired on its own
explanatory comment.

## Files changed

| File | Change |
|---|---|
| `harness/sensitivity.py` | `PRE_REGISTRY`, `VERSION_VALUES` — one module owns both strings |
| `memory_engine/store.py` | version imported, stamped into props, persisted in `_CREATE_FACT_CQL` |
| `harness/extraction_queue.py` | `_write_one` stamps (path 2 of 3) |
| `memory_engine/consolidate.py` | `_write_derived_node` stamps (path 3 of 3) |
| `harness/epistemic_record.py` | per-fact stamp **projected**; routing stamp current-version |
| `scripts/migrate_sensitivity_registry_version.py` | NEW — one-shot backfill, applied |
| `eval/test_registry_version_stamp.py` | NEW — 18 cases |
| `scripts/run_harness.sh` | 14th battery registered |

## What this does not do

- **Rules nothing MET.** R30's status is yours. Item 5's mechanism exists; the ruling does not
  follow automatically.
- Does not touch A12's read-path fix (its own scheduled dispatch), A16, or the 16 UNWRITABLE rows.
- Does not claim row 1 is executed end-to-end — stated above.
