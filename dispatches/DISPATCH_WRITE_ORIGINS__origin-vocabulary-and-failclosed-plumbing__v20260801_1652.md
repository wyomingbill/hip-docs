# DISPATCH_WRITE_ORIGINS
Status: BUILT
Reconciled-Against: b634962 (HEAD at gate)
REQ: `docs/requirements/REQ_ARCHITECTURE_BOUNDARY__reference-monitor-threat-model-and-contracted-clients__v20260801_0919.md` — steps 2+3 of the D-84 single-writer plan, atomic — and `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` R1/R10
Dispatch: D-97, 2026-08-01
**Status proposed: NONE. Nothing ruled MET. A10's xfail stays xfail — step 4 wires it.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @ `b634962`, clean.
`~/hip-vo`, `~/hip-dev`, `~/hip-harness` NOT touched. **Nothing ruled MET. A10's xfail stays
xfail — step 4 wires it, not this dispatch.** One commit; nothing landed between the steps.

---

## STEP 2a — the origin vocabulary, assessed against real callers before adoption

D-84's candidate set was adopted **unchanged** — every real caller fits one origin, none
was forced:

| Origin | Caller(s), verified at b634962 | Note |
|---|---|---|
| `extraction` | the session-end worker (`extraction_queue.py:1011`) | intrinsic to the path |
| `self_report` | `harness/fact_change.py` (live in-conversation change) | PATH name per R10's "explicit self-report path"; the fact's SUBJECT may be another member — TD-110's cross-member gap is unchanged by naming the path |
| `attributed_import` | `harness/disclosure.write_frontier_fact` (frontier answer, provenance-attributed) | R10: "attributed external claims still write where otherwise authorized" |
| `derivation` | `consolidate._write_derived_node` | intrinsic — hardcoded at the writer, not caller-supplied |
| `migration` | **NO current caller** — both `migrate_*` scripts SET, never CREATE (verified D-96) | RESERVED, stated; a future fact-creating migration must say so |
| `fixture` | `demo_seed` + every eval harness + seed scripts | fixtures construct states by definition; X-04's "D8 is seeded, not derived" is now recorded on the node |

The two archived scripts under `docs/dispatches/` are deliberately **not** plumbed — if
resurrected they fail loudly at the creator, which is fail-closed working as intended.

## STEP 2b — DERIVABLE_ATTRIBUTES, evidence-based, with the drift warning HANDLED

**The decisive finding:** `interpreter.abstract()`'s Groq prompt constrains the emitted
attribute **not at all** (`"attribute": "..."` — any string). That is R1's gap in one line,
and it means the allowlist cannot be "derived from what abstraction emits" — abstraction can
emit anything. So the list starts at the **evidenced** set and fail-closed refuses novelty:

- **`risk_pattern`** — Bill's ruling 2026-07-17 (REQ_D21_D23): deliberately non-canonical,
  derivation-only in production. (D8 is *seeded* — see the fixture carve-out below.)
- **`lifestyle`** — the standing MEM-111 contract: the only derivation attribute any
  harness pins (MockInterpreter's DerivedFact).

**Widening the list is a ruling, not an edit** — a derived fact with a novel attribute
(including a canonical one, e.g. a derived "preference") is refused at the creator until
the attribute is added with a citation. That is R1's "off-allowlist derived attribute is
refused" as specified.

**D-77's drift warning — mechanism, not discipline, on two independent legs:**
1. **Import-time laws.** `harness/write_origins.py` (one module owns BOTH vocabularies)
   executes `enforce_vocabulary_laws()` **at import** — L1: `risk_pattern ∈ DERIVABLE`
   (the ruling); L2: `risk_pattern ∉ CANONICAL` (its other half); L3: neither set nests in
   the other (the exact drift shape that produced the three trust orderings). A writing
   process with a drifted vocabulary **cannot start**.
2. **Standing battery.** CEIL-ORIG pins both sets' **exact contents**, so any addition or
   removal turns the suite red and requires a deliberate, cited edit. Fault twins prove
   each law can fire (a DERIVABLE missing risk_pattern fires L1; one nested inside
   CANONICAL fires L3), and an AST check proves the laws are still *called at import* —
   if someone removes that call, the guarantee visibly degrades to discipline and the
   battery says so.

Today the two vocabularies are **disjoint** (both derivable attributes are non-canonical),
which satisfies "overlap without nesting" trivially; the battery documents that the
disjointness line is the one that changes if a ruling ever makes a canonical attribute
derivable.

## STEP 2c — the checks, at create_fact_node, fail-closed

All at the single materialization point step 1 built, refusing **before any write**:

1. `origin` is a **required keyword** — an unplumbed caller gets a `TypeError`, the
   loudest possible break. No default anywhere (the R29 pattern).
2. Unknown origin → `UnknownOrigin`. Origin-as-a-property → refused (one authority: the
   keyword).
3. `origin == derivation` → attribute ∈ DERIVABLE_ATTRIBUTES (**R1 at the choke point** —
   the only thing standing between a model-invented attribute and the graph).
4. Derivable-only attributes (`risk_pattern`, `lifestyle`) → origin ∈ {derivation,
   **fixture**}. **The fixture carve-out is deliberate and on the record:** D8 is seeded,
   not derived (X-04); `demo_seed` writes `risk_pattern` as a fixture, and blocking it
   would break the frozen demo's reseed path. The origin property now makes X-04's
   honesty structural — a CEIL-ORIG case exists specifically so the carve-out reads as a
   decision, not a hole. **Flagged for your review rather than silently chosen.**
5. Origins {extraction, self_report, attributed_import} → attribute ∈
   CANONICAL_ATTRIBUTES (**R10's registry revalidation**). Verified redundant against
   today's callers — extraction's `_coerce_fact`, fact_change's enum check
   (`fact_change.py:688`), the frontier's literal `zone_district` — which is what a
   REvalidation should be: it exists for the alternate writer that bypasses upstream.
6. The origin is **stored on the node** (`origin: $origin` in the one CQL), creator-
   stamped like the R30 version. **No backfill of the 12 existing facts — not ordered,
   not invented**; old facts carry no origin key, verified live after all runs.

## STEP 3 — the plumbing: enumerated first, then edited, then swept exhaustively

**64 call sites across 17 files**, every one stating its origin explicitly:

| Category | Sites | Origin |
|---|---|---|
| extraction worker | 1 | `extraction` |
| fact_change | 1 | `self_report` |
| write_frontier_fact | 1 | `attributed_import` |
| consolidate | 1 (intrinsic) | `derivation` |
| demo_seed | 1 | `fixture` |
| eval/memory_harness (33), truth_harness (13), memory_e2e (4), harnesslib/layer1 (2 + 3 wf), layer7_crypto (3), layer7_crypto_v2 (2 + 1 wf) | 61 | `fixture` |
| care_coord_run (3 wf), integration_harness (1 wf), realtime_voice_demo (1 wf), realtime_care_coord_smoke (1 wf) | 6 | `fixture` |

**Fail-closed caught my own enumeration miss, and that is worth recording.** My first
sweep used a regex that excluded `.encode(` to skip string methods — and swept the
module-qualified `store.encode(` sites with it. The first `--layer 7` run then died with
`TypeError: encode() missing 1 required keyword-only argument: 'origin'` at
`layer7_crypto.py:234` — **the exact loud break the mechanism promises**, caught in the
harness rather than shipped. The final sweep is **AST-exhaustive** (walks every call node
in five packages, checks for the origin keyword): **zero originless call sites**.

**One eval fixture edit beyond plumbing, purpose-preserving and disclosed:** the OB4
fault-injection probe drove `_write_derived_node` with a synthetic attribute
(`ob4_probe_attribute`), which the allowlist now refuses. The probe tests **sealing**
(key_version=2), not vocabulary — its attribute was arbitrary, so it now uses the
allowlisted `lifestyle`, and the AUDIT fixture marker was repointed to the probe's
still-distinctive subject. OB4's check itself is unchanged and passes.

## STOP conditions — checked, none fired

| Condition | Result |
|---|---|
| a caller fitting no origin | none — the assessment table above covers every caller |
| a caller whose origin can't be determined from code | none — the two archived docs/ scripts are dead and deliberately unplumbed |
| a DERIVABLE/CANONICAL conflict resolved by choosing | none — the sets are disjoint today; the one judgment call (the fixture carve-out for derivable-only attributes) is flagged above for your review, with the alternative (breaking demo_seed's reseed) stated |
| anything ABSOLUTE red | none — all five PASS, read individually |

## Evidence

```
standing batteries (16 files): 243 passed, 9 xfailed
  (test_write_origins.py: 25 new; CEIL-CONV updated to fixtures v2 — the D-96
   capture plus exactly one sanctioned delta, the origin property)
== AUDIT:  8/8   == DISC: 1/1   == L7: 27/27
== L7V2:   27/28 (1 opt-in skip)   == SCHEMA: 1/1   == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.   0 scenario FAILs.
ABSOLUTE, individually: G0 PASS, PSA1 PASS, CTX-STRIP PASS, LI1 PASS, CS1 PASS.
```

**Memory harness: 13/17 — identical to D-96's baseline, failing the identical four**
(MEM-115/116/117/118, pre-existing and environmental). Zero delta — the STOP condition
did not fire. MEM-111 now exercises the real derivation path *through the allowlist*
(`lifestyle`) and passes. Run with the repo `.env.dev` only, per the dispatch's note.

**The strict A1/A10 xfails stayed red** (no unexpected pass): A10 because encode's
R10 checks live at the creator and step 4's battery is not wired; A1 because its
predicate looks for `DERIVABLE_ATTRIBUTES` in four candidate files that deliberately do
not include `write_origins.py`. **Flag for step 4:** A1's enforcement now substantively
EXISTS at the creator — its predicate needs re-derivation when step 4 wires A10, or it
stays red claiming "not built" about a thing that is built.

`--full` not attempted — TD-129's guard, as anticipated. Live graph verified untouched
after every run: 12 facts, 12 `pre-registry`, 0 carrying origin (backfill not ordered).

## What this did NOT do

- **Step 4** — no A10 battery, no A1 re-derivation. Both flagged for it.
- **No origin backfill** of existing facts — not ordered.
- **No behavior change to any production write** — the registry revalidations are
  proven no-ops against today's callers; the only writes now refused are ones no
  current caller makes (model-invented derived attributes, derivable-only attributes
  through production origins, unknown origins).
- **Ruled nothing MET.**
