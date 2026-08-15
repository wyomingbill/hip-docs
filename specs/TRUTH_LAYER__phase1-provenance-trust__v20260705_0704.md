<!-- STATUS: IN_PROGRESS -->
<!-- RECONCILED-AGAINST: truth_layer/queries.py (scaffold, NotImplementedError bodies); eval/truth_harness.py (T-A + T-B scenarios written, not gated); harness/orchestrator.py:237 (read_user_facts still live, swap-in not done) — 2026-07-05 -->

# HIP Truth-Management Layer (Architecture Spec)

**Status: PLAN. Nothing in this document is implemented beyond the read-only
scaffold noted in §12.** The memory engine it formalizes over is built, tested,
and integration-ready behind the frozen injection contract (Phases A–E, gated
on the engine track) — it is **not live**; the live pipeline still runs
`read_user_facts()`. Every claim below should be read against that status.

Companion to `docs/MEMORY_ENGINE_SPEC.md`. This spec adds **no new memory
mechanics**. It names, bounds, and completes a layer that already exists in
pieces inside the engine.

---

## 0. One-paragraph summary

The memory engine already records everything a household needs to manage
*truth* — four write states that distinguish "the world changed" (SUPERSEDE)
from "we were wrong" (CORRECT), a bitemporal model that separates when a fact
was true from when we believed it, logged bidirectional confidence
transitions, the encrypted driving utterance behind every write, an
append-only audit trail, and ownership-gated human confirmation. What it does
not have is a **name** for this capability or a **first-class query surface**
over it. This spec formalizes the truth-management layer: a read-only,
deterministic, code-only query module that answers the four questions a
household actually asks about a stored belief — *why do we believe this, who
said it, was it ever corrected, should we trust it* — plus one additive
annotation (trust tagging at disclosure) that must be proven byte-identical
to the injection contract's decisions, exactly as MEM-100 proved for the
engine's annotations.

---

## 1. Naming and boundaries

### 1.1 What the truth-management layer is

The truth-management layer is the set of guarantees and queries concerning
**belief provenance, correction history, trust, and assertion authority**.
It sits alongside the memory-storage/tier layer, over the same `:Fact`
rows, and below the disclosure boundary.

### 1.2 Ownership boundaries (who owns what)

| Concern | Owner | Where |
|---|---|---|
| Storage, bitemporal schema, write states, tiers, consolidation, recall | **Memory engine** | `memory_engine/store.py`, `consolidate.py`, `api.py`, `recall.py` |
| Belief provenance (driving utterance, session, write decision, rationale) | **Truth layer** | `truth_layer/queries.py` (planned) |
| Correction history (CORRECT vs SUPERSEDE lineage, walkable chains) | **Truth layer** | same |
| Trust (confidence + confirmation status + write state + age → trust level) | **Truth layer** | same |
| Confirmation authority (who may confirm what) | **Truth layer** *defines*; engine §8.3 *enforces* | spec §5.4 here; `memory_engine` fluid/intentional paths |
| Disclosure (INJ-1..6, empty-set guard, sensitivity ceiling) | **Injection contract** — frozen, untouched | `harness/injection_contract.py` |

Three hard rules fall out of this table:

1. **The truth layer never stores.** It is read-only over engine state. Its
   only write is its own query-audit log (NDJSON, same pattern as
   `recall_audit.jsonl`).
2. **The truth layer never discloses.** It is a library. Every user-facing
   surface that renders its results passes them through
   `apply_injection_contract` first — the same rule the engine obeys on
   every path including `recall_from_cold`.
3. **The truth layer never decides.** No model call exists anywhere in it
   (§7). The model did its interpretation once, at write time; the truth
   layer replays and explains that record.

### 1.3 What already exists vs what this spec adds

| Capability | Engine state today | Truth-layer work |
|---|---|---|
| Driving utterance per write | `driving_utterance_ct/_dek` on node (encrypted, TD-030) | expose via named query |
| Write decision + confidence | `write_state`, `write_confidence` on node; requested vs actual + `override_reason` in `encode_audit.jsonl` | expose |
| Decision rationale | **hash only** (`rationale_hash` in `confidence_log`, `prompt_hash` in audit) | **gap G-1**: full text not recoverable |
| Belief-over-time | `recorded_at` / `record_closed_at` on every row | expose as named bitemporal query |
| CORRECT vs SUPERSEDE distinction | `closed_reason ∈ {superseded, error}` + `record_closed_at` | expose; make the distinction the *point* of a query |
| Lineage links | `superseded_by` (old→new), `derived_from` (derived→sources) | **gap G-2**: no backward walk; chain assembly is ad-hoc |
| Confidence history | `confidence_log` append-only list | expose |
| Human confirmation | `confirmed_by` / `confirmed_at` | input to trust classification |
| Trust as a first-class concept | not present | **gap G-3**: classification (§4) |
| Trust visible at disclosure | not present | **gap G-4**: additive annotation (§5.3) |

---

## 2. Implementation-status honesty (applies to every section)

Baked-in rule for this document and everything derived from it (READMEs,
demo scripts, commit messages):

- The engine + truth layer are **"built, tested, and integration-ready
  behind the frozen injection contract"** — never "live", "deployed", or
  "in production" until the §10 swap-in milestone of the memory spec has
  actually happened.
- **Never claim "can't leak."** The correct claim is: *structurally
  constrained from injecting facts outside the contract, with deterministic
  disclosure controls and auditability.* Structure reduces classes of
  failure; it does not abolish them. §8 enumerates the residual vectors.
- Claim **mechanism + threat model**, never absolute safety.

---

## 3. The four truth questions — first-class queries

All queries are read-only, code-only, deterministic, and auditable. Planned
module: `truth_layer/queries.py`. Signatures are the contract surface; a
future UI (the memory dashboard is the natural host) is a consumer, not part
of this spec.

### 3.1 PROVENANCE — "why do we believe X?"

```python
def provenance(fact_id: str, *, driver=None) -> Provenance:
    """The full write-time context behind one belief. Read-only."""
```

Returns, assembled from the node + `encode_audit.jsonl`:

| Field | Source |
|---|---|
| `driving_utterance` | node `driving_utterance_ct/_dek`, decrypted on read (caller governs disclosure) |
| `source_session_id` | node |
| `write_state` (actual) + `requested_state` + `override_reason` | node + audit record |
| `write_confidence` | node |
| `model_id`, `prompt_hash` | audit record |
| `rationale` | **G-1**: today only `rationale_hash`; see §6 |
| `recorded_at`, `valid_from` | node |
| `confirmed_by` / `confirmed_at` | node (null = never human-confirmed) |
| `derived` + `derived_from` | node (derived facts cite their source fact_ids) |

Answerable today except the full rationale text. The decrypted driving
utterance **contains the fact**; §5.2 governs who may see it.

### 3.2 BELIEF-OVER-TIME — "what did we believe about X on date D?"

```python
def believed_state(subject: str, attribute: str, at: str, *, driver=None) -> list[Fact]:
    """Record-time reconstruction: the rows the system believed at instant `at`."""
```

Pure bitemporal filter, fully supported by existing schema:

```
recorded_at <= $at AND (record_closed_at IS NULL OR record_closed_at > $at)
```

optionally intersected with the valid-time axis (`valid_from <= $at AND
(valid_to IS NULL OR valid_to > $at)`) to distinguish *"what did we believe
was true on D"* from *"what did we believe had ever been true as of D"*.
Both variants are named parameters, not separate functions. The engine's §7
guarantee ("any prior belief state is reconstructible") becomes an
executable query instead of a paragraph.

Key property this makes demonstrable: after a CORRECT, `believed_state` at a
date **before** the correction returns the erroneous row (that *was* the
belief), while current retrieval never does. SUPERSEDE does not close record
time, so the superseded row remains part of "believed true then" — the two
lifecycles are distinguishable per §3.3 of the engine spec.

### 3.3 CORRECTION HISTORY — "was X ever corrected?"

```python
def correction_history(subject: str, attribute: str, *, driver=None) -> list[Correction]:
```

Returns the lineage rows closed with `closed_reason='error'` (CORRECT),
explicitly **distinct** from rows closed with `closed_reason='superseded'`
(SUPERSEDE). Each entry carries: the erroneous value's fact_id, when the
error was recorded and when it was closed (`recorded_at`,
`record_closed_at`), what replaced it (`superseded_by`), and the replacing
row's provenance (§3.1). The truth-vs-change distinction — the reason the
engine has two time axes at all — becomes queryable rather than implicit.

### 3.4 TRUST — "should we trust X?"

```python
def trust(fact_id: str, *, driver=None) -> Trust:
    """Deterministic trust classification with the predicate that fired."""
```

Specified in full in §4. Returns `(level, basis, inputs)` where `basis` is
the human-readable predicate that assigned the level and `inputs` is the
raw evidence (confidence, write_state, confirmed_by, derived, age,
confidence_log length) — every classification is explainable from its own
return value.

### 3.5 PROVENANCE CHAIN — the walkable lineage (gap G-2)

```python
def lineage(fact_id: str, *, driver=None) -> list[LineageLink]:
    """Walk the full supersede/correct chain containing this fact, oldest first."""
```

`superseded_by` points old→new only. The backward step ("what did this
belief replace?") is the inverse query — `MATCH (prior:Fact {superseded_by:
$fid})` — which works but exists nowhere as a named operation. `lineage()`
assembles the whole chain in both directions and labels every link:

```
metformin ──superseded_by──▶ Jardiance          link type: superseded  (world changed)
lisinopril ──superseded_by──▶ losartan           link type: corrected   (belief was wrong)
   (record_closed_at set, closed_reason=error)
derived-fact ──derived_from──▶ [ep1, ep2, ep3]   link type: derived
```

Each link carries `{from_fact_id, to_fact_id, link_type: superseded|
corrected|derived, ts, closed_reason}` plus per-node §3.1 provenance on
request. Cycle-safe (visited set), bounded depth (default 50 — a lineage
longer than that is a data bug worth surfacing, not walking).

---

## 4. Trust model: classification, not score

**Decision: an ordered trust-level classification, not a numeric score.**

Why not a score: a formula like `0.4·confidence + 0.3·confirmation + …`
manufactures false precision — the difference between 0.79 and 0.83 is not
explainable to a household member, invites silent thresholding downstream,
and over-claims exactly the way §2 forbids. The inputs are mostly
categorical (write_state, confirmed_by, derived); forcing them through
arithmetic launders categories into a number that *looks* continuous. The
salience formula (engine §8.3) is a genuine magnitude over genuinely scalar
inputs; trust is not.

**The levels** (ordered, highest first; deterministic predicates evaluated
top-down, first match wins — code, no model):

| Level | Predicate | Render vocabulary |
|---|---|---|
| `CONFIRMED` | `confirmed_by IS NOT NULL` | "confirmed by Bill" |
| `CORROBORATED` | `confidence = high` via ≥1 logged `harden` transition, not derived | "consistently reported" |
| `ASSERTED` | `write_state ∈ {supersede, augment, correct}` AND `confidence ∈ {medium, high}` AND NOT derived | "Bill told me" (via provenance) |
| `UNCONFIRMED` | `write_state = unresolved` OR `confidence = low` | "may be — unconfirmed" |
| `DERIVED` | `derived = true` (checked **first**, before all above, as a category not a strength) | "from patterns I've noticed, unconfirmed" |

Evaluation order in code: `DERIVED` → `CONFIRMED` → `CORROBORATED` →
`ASSERTED` → `UNCONFIRMED` (derived is provenance-category, not
strength — a derived fact renders as derived even if consolidation
hardened it; engine already caps derived confidence at `medium`).

**Age modifier** (only modifier, applied after classification):
`stale: true` when `last_accessed` (or `recorded_at` if never accessed) is
older than `STALE_DAYS` (default 180) — surfaced as a flag beside the
level, never a level change. Staleness is information, not distrust; a
confirmed allergy does not decay into a rumor.

Every `trust()` return includes `basis` — the literal predicate string that
fired — so "should we trust X" is answered with evidence, not a verdict.

---

## 5. Disclosure governance and trust tagging

### 5.1 The layer is contract-neutral

`truth_layer/queries.py` is a library over Neo4j + NDJSON logs. It neither
calls nor bypasses `apply_injection_contract` — the same split the engine
made: the layer shapes *answers about beliefs*; the contract governs
*disclosure of them*.

### 5.2 Every user-facing surface passes the contract

Provenance results include the decrypted driving utterance and fact values.
Rules, matching engine precedent exactly:

- **User-facing paths** (a future "why do you think that?" feature, the
  dashboard's contract mode): results pass through the real
  `apply_injection_contract` before rendering, with requester/subject/intent
  exactly as `recall_from_cold` does today.
- **Operator/debug paths** (dashboard debug mode): permitted, labeled as
  disclosure-bypassed, and enumerated in §8 as a residual vector — not
  pretended away.
- **Query audit**: user-facing truth queries append `{ts, requester,
  fact_id/subject, query_kind, reason}` to
  `logs/truth_layer/truth_audit.jsonl` (the `recall_audit.jsonl` pattern).

### 5.3 Trust tagging at disclosure (gap G-4) — additive only

The grounding formatter should render trust honestly: "confirmed by Bill"
vs "model-inferred, unconfirmed" vs "derived pattern". Mechanism:

- After `apply_injection_contract` returns, annotate **allowed** facts with
  `trust_level` and `trust_basis` keys (computed by §4 code from fields the
  facts already carry — no second Neo4j round-trip needed for the common
  case).
- **Frozen-interface rule, MEM-100 analog:** annotation happens strictly
  *after* the contract call, on the allowed list only. TRUTH-100 (§9)
  asserts the `InjectionResult` is **byte-identical** with and without
  trust tagging — same allowed set, same denied set, same guard state, same
  order. The contract never sees, and can never be influenced by, trust
  keys.
- The formatter mapping extends `render_fact_hint` / `render_system_note`
  vocabulary; it never overrides them (an UNRESOLVED fact stays hedged even
  at `CONFIRMED` — impossible by construction, but the precedence is
  stated: write-state hedging wins over trust vocabulary).

### 5.4 Confirmation authority (already enforced; named here)

Authority to *confirm* follows the ownership model the engine already
enforces (§8.3 of the engine spec): only the fact's owner or subject has
standing; the check mirrors INJ-3's permit logic. The truth layer *names*
this as one of its guarantees and `trust()` reflects it — `confirmed_by` is
only ever set through that gated path, which is what makes `CONFIRMED`
trustworthy as a level.

---

## 6. Gaps — what "complete" requires (smallest honest list)

| Gap | What's missing | Fix | Track |
|---|---|---|---|
| **G-1 rationale text** | `WriteDecision.rationale` is hashed (`rationale_hash`) and discarded; provenance can prove *that* a rationale existed and match it, but not show it | persist `rationale_ct/_dek` (encrypted — rationale text contains fact content, TD-030 applies) on the node at ENCODE, alongside the driving utterance | **engine track** — the only write-path change in this spec; lands as a small ENCODE addition gated by the MEM harness, ratcheted like any engine change |
| **G-2 lineage walk** | backward supersession step has no named query; chain assembly ad-hoc | `lineage()` §3.5 | truth layer (read-only) |
| **G-3 trust classification** | not present anywhere | `trust()` §4 | truth layer (read-only) |
| **G-4 trust at disclosure** | formatter can't render trust | §5.3 additive annotation + TRUTH-100 | truth layer (read-only + one formatter hook) |
| **G-5 named bitemporal query** | reconstructible-in-principle, no executable surface | `believed_state()` §3.2 | truth layer (read-only) |

G-1 is the only gap that touches ENCODE. Until it lands, `provenance()`
returns `rationale: null, rationale_hash: <hash>` and says so — the spec
does not pretend hash-only is full provenance.

---

## 7. Model/code boundary (unchanged principle, restated for this layer)

**The model's role in the truth layer at query time is zero.** Trust
classification, provenance assembly, lineage walking, bitemporal
reconstruction, correction history — all deterministic code over stored
state. The model's interpretive work happened once, at write time (the
four-state decision, `write_confidence`, the rationale), and was recorded;
the truth layer is precisely the machinery that lets that recorded judgment
be **audited later without re-asking a model** — re-asking would replace
evidence with a fresh opinion. Same boundary as engine §2: model interprets
at the edges (write), code decides everywhere else (read, score, walk).

---

## 8. Claims language and residual vectors

The permitted claim, verbatim template:

> HIP's memory is **structurally constrained from injecting facts outside
> the injection contract, with deterministic disclosure controls and
> auditability.** Cold-tier facts are structurally excluded from the
> candidate set; every disclosure path — live retrieval, historical query,
> intentional recall, truth queries — passes the same frozen contract.

What that structure **reduces but does not eliminate**:

| # | Residual vector | Status |
|---|---|---|
| 1 | **Misclassification** — write-state, intent, or temporality judged wrong at the model edge; a confidently-wrong write lands as a confident fact | Mitigated: consolidation revisit, LOOSEN on contradiction, fluid/intentional confirmation, full correction machinery (CORRECT + lineage). Not eliminated — engine spec §11 owns the residual. |
| 2 | **Explicit-search side channel** — `recall_from_cold` and truth queries reach facts a live turn never would | Mitigated: contract applied to results, who/when/why audit, never merged into live candidates. The *existence* of the channel is by design and documented. |
| 3 | **Operator/debug access** — dashboard debug mode, direct Neo4j/Cypher, filesystem reads bypass the contract entirely | Mitigated only by labeling and dev-scoping (port guard, dev DB). **Out of scope**: operator threat model is an infrastructure concern (disk encryption, access control), not a contract concern. Stated, not hidden. |
| 4 | **Logging exposure** — audit NDJSON carries metadata (owner, attribute names, fact_ids, salience); values and utterances are encrypted, metadata is not | Mitigated: no plaintext values/utterances in any log (TD-030 discipline). Residual: metadata inference (that Elena *has* a medication row) remains. |
| 5 | **Backup exposure** — Neo4j dumps and log archives carry ciphertext + metadata wherever they are copied | Out of scope here; keys live separately (encryption layer), backup handling is infrastructure. Named so nobody claims otherwise. |
| 6 | **Prompt injection** — adversarial utterance content shaping the write-time model's decision (e.g., engineering a SUPERSEDE of someone else's fact) | Partially mitigated: ownership checks are code (a write lands under the speaker's ownership; INJ-3 governs cross-member disclosure; confirmation authority is code-gated). Residual: within a member's own scope, a manipulated model can still mis-write — consolidation + confirmation are the backstop. |

No sentence in HIP documentation may claim leak-impossibility. This table
is the honest replacement.

---

## 9. Truth harness — `eval/truth_harness.py` (TRUTH-1xx)

Independent gate on the engine track, same conventions as
`eval/memory_harness.py` (dev port guard, `:MemFact`-style throwaway
namespace, MockInterpreter fixtures, per-scenario PASS/FAIL, **NOT wired
into `gate_check.sh`** until the memory swap-in milestone of engine spec
§10).

| ID | Scenario | Load-bearing assertion |
|---|---|---|
| TRUTH-100 | **Contract byte-identity** (MEM-100 analog) | `apply_injection_contract` output is byte-identical with and without trust annotation; annotation exists only on post-contract allowed facts |
| TRUTH-101 | Provenance | `provenance()` returns the decrypted driving utterance, session, write_state (requested + actual + override_reason), write_confidence; rationale_hash matches the WriteDecision's rationale until G-1, full text after |
| TRUTH-102 | Belief-over-time | encode → CORRECT → `believed_state(D_before_correct)` returns the erroneous row; `believed_state(D_after)` returns the corrected row; current retrieval never returns the erroneous row |
| TRUTH-103 | Correct ≠ supersede | one lineage with a SUPERSEDE link and a CORRECT link: `correction_history()` returns only the CORRECT closure; the SUPERSEDE row appears in lineage as `link_type=superseded` |
| TRUTH-104 | Trust determinism | five fixtures, one per level (§4 table), classify to exactly the expected level with the expected `basis` string; repeated calls identical; `DERIVED` wins over a hardened derived fact |
| TRUTH-105 | Lineage walk | 3-generation chain (A superseded-by B corrected-by C, plus a derived fact citing A): `lineage(C)` walks to A oldest-first with correct link types; cycle guard and depth bound exercised |
| TRUTH-106 | Confirmation authority in trust | `confirmed_by` set via the authority-gated path → `CONFIRMED`; a fact whose confirmer lacked standing never has `confirmed_by` set (asserted structurally: no ungated write path exists) |
| TRUTH-107 | Truth-query audit + governance | a user-facing provenance call appends one audit record (who/when/why) and its rendered output passed the contract; cross-member requester gets INJ-3-denied provenance |

Ratchet rule inherited from the engine track: any bug found during the
truth-layer build lands as a TRUTH-1xx scenario before its fix merges.

---

## 10. Phased plan + honest cost

Formalization over proven ground — read-only, low-risk, no live-pipeline
change anywhere in T-A..T-C.

| Phase | Contents | Cost / risk |
|---|---|---|
| **T-A** | `truth_layer/queries.py`: `provenance()` (hash-only rationale), `believed_state()`, `correction_history()`, `lineage()`; truth audit log; TRUTH-101/102/103/105 | Thin query layer over existing rows + audit NDJSON. **Already answerable today** — this is exposure, not construction. Low. |
| **T-B** | `trust()` classification + stale flag; TRUTH-104/106 | New code formula, deterministic, ~100 lines. Low. |
| **T-C** | Trust tagging post-contract + formatter vocabulary hook; TRUTH-100/107 | The one piece touching the disclosure *surface* (never the contract). Byte-identity test is the safety proof. Low-moderate. |
| **T-D** | G-1: persist encrypted `rationale_ct/_dek` at ENCODE | **Engine-track change** (write path). Small, but gated by the full MEM harness + live 6-check gate like every engine change. Do last; everything else works without it. |

Explicitly deferred: any UI beyond the existing dashboard consuming these
queries; any "truth review" household feature; INJ-2 relevance improvements
(contract track); swap-in wiring (engine spec §10 owns that milestone).

---

## 11. Honest limits

- **Provenance is only as honest as the write-time model.** The rationale
  is the model's own account of its decision — evidence of what it claimed,
  not proof the claim was sound. Consolidation and confirmation exist
  because write-time judgment is fallible (engine spec §11 first bullet).
- **Trust levels classify evidence, not truth.** `CONFIRMED` means an
  authorized human asserted it; humans are wrong too. The level vocabulary
  deliberately says "confirmed by Bill", never "true".
- **`believed_state` is bounded by record fidelity.** Migrated pre-engine
  rows have backfilled `recorded_at = valid_from`; belief-over-time answers
  about the pre-migration era are approximations and the query result
  should carry a `migrated: true` flag per row so consumers can hedge.
- **The lineage walk trusts `superseded_by` integrity.** A hand-edited or
  partially-failed write could orphan a link; `lineage()` should surface
  gaps (`link_type: broken`) rather than silently truncating.
- **Trust tagging can be ignored by the formatter.** The annotation makes
  honest rendering *possible*, not inevitable — formatter conformance is a
  grounding-layer test, out of scope here.

---

## 12. Scaffold status

Permitted to land with this spec (and nothing else until T-A is approved on
the engine track):

- `truth_layer/` package: namespace + `queries.py` **stub** — signatures,
  docstrings, `NotImplementedError` bodies; no Neo4j calls at import, no
  live-pipeline imports, no contract imports.
- No harness file yet (TRUTH-1xx lands with T-A).
- Not wired into `gate_check.sh` — that decision belongs to the memory
  swap-in milestone, engine spec §10.
