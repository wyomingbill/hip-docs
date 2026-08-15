<!-- STATUS: IN_PROGRESS -->
<!-- RECONCILED-AGAINST: memory_engine/{api,store,consolidate,interpreter,recall}.py (present, beyond scaffold); eval/memory_harness.py (Phase A-D scenarios written); harness/orchestrator.py:237 (still calls read_user_facts — swap-in not done) — 2026-07-05 -->

# HIP Memory Engine — Tiered Consolidating Memory (Architecture Spec)

**Status:** PLAN — no implementation beyond the module scaffold
**Date:** 2026-07-04
**Author:** Bill Brewster (spec drafted with Claude)
**Track:** separate dev track; live pipeline and demo frozen throughout
**Baseline:** injection contract gated 11/11 (`eval/injection_harness.py`), gate_check.sh 6/6

---

## 0. One-paragraph summary

The memory engine replaces the flat `read_user_facts()` retrieval with a
tiered, bitemporal, self-consolidating store — while exposing exactly the same
question to the pipeline it answers today: *injectable facts for (member,
query, subject)*. Writes are classified into four states (SUPERSEDE / AUGMENT /
CORRECT / UNRESOLVED) by a prompted, swappable model; state, truth, disclosure,
and audit stay in deterministic code. An offline consolidation pass (the "REM
pass") revisits write-time guesses, hardens or loosens confidence, derives
tagged abstractions, and demotes stale facts down a hot → warm → cold tier
ladder. Nothing is ever deleted. Unresolved ambiguity is disclosed with
uncertainty and resolved either fluidly (woven into a related answer) or, for
high-salience items only, by an HIP-initiated confirmation session. The
injection contract (`harness/injection_contract.py`) is the frozen interface:
the engine may become arbitrarily sophisticated behind it, but what the
pipeline asks and what the contract permits returned never changes.

---

## 1. The frozen interface

### 1.1 What the pipeline asks today

```
read_user_facts(owner) ─┐
                        ├─→ resolve_subject(query, member, facts)
                        ├─→ route(query) → intent
                        └─→ apply_injection_contract(facts, member, query,
                                                     resolved_subjects, intent)
                              → InjectionResult(allowed, denied,
                                                guard_triggered, injected_fact_ids)
```

### 1.2 What the engine exposes (the contract surface)

One function, same shape in and out as today's retrieval:

```python
# memory_engine/api.py  (the ONLY import the live pipeline ever makes)

def candidate_facts(member: str, query: str, *, limit: int = 20) -> list[dict]:
    """Return injection-candidate facts for this member and query.

    Drop-in replacement for read_user_facts(). Each fact dict has EXACTLY the
    keys the pipeline consumes today:

        fact_id, attribute, value, owner, subject, confidence, sensitivity

    plus OPTIONAL additive annotation keys (§1.4) that existing code ignores.
    The caller then runs resolve_subject / apply_injection_contract UNCHANGED.
    """
```

The engine never calls the contract itself and never bypasses it. It shapes
the **candidate set**; the contract governs **disclosure**. This split is what
makes the engine swappable: the pipeline diff at integration time is one
import line.

### 1.3 Invariant map — each preserved invariant → where it is asserted

| Invariant | Enforced by | Asserted by |
|---|---|---|
| Deny-default cross-member (INJ-3) | `apply_injection_contract` (unchanged) | injection_harness 11/11 (existing) + MEM-107 (cold/warm facts obey INJ-3 identically) |
| Owner-read exception | INJ-3 permit branch (unchanged) | injection_harness (existing) |
| Never-volunteer (INJ-5) | `apply_injection_contract` (unchanged) | injection_harness (existing) + MEM-106 (historical query with knowledge intent still injects nothing personal) |
| Sensitivity ceiling | routing sensitivity gate (unchanged) | tests/test_sensitivity.py (existing) |
| Empty-set guard (INJ-6) | `apply_injection_contract` (unchanged) | injection_harness + seam S3 (existing) |
| Cold never in injection set | **structural**: `candidate_facts()` queries `tier IN ('hot','warm')` only; cold rows are unreachable from that code path | MEM-107: seed a cold fact matching the query perfectly; assert it is absent from the candidate set *before* the contract even runs |
| Warm only on historical query | deterministic temporal filter (§5.2) | MEM-105 / MEM-106 |
| Unresolved disclosed with uncertainty | annotation key + grounding formatter (§1.4) | MEM-104 |
| Derived never confused with asserted | `derived: true` tag + formatter prefix (§6.3) | MEM-111 |

**Contract-tolerance assertion (MEM-100):** run `apply_injection_contract`
over the same fact set with and without the engine's annotation keys; assert
byte-identical `InjectionResult`. This proves the additive keys cannot change
what the contract permits.

### 1.4 Additive annotation keys (allowed; never load-bearing for disclosure)

| Key | Type | Meaning |
|---|---|---|
| `unresolved` | bool | write-state was UNRESOLVED; formatter renders hedged ("she may have…") |
| `confirm_when_relevant` | bool | retrieval-time hook for fluid confirmation (§8.1) |
| `derived` | bool | consolidation-derived abstraction, never asserted by a human |
| `tier` | str | `hot` / `warm` (cold cannot appear here by construction) |
| `retired` | bool | `valid_to` is set; only present on historical-query results |

Rules INJ-1..6 read only the original seven keys. The harness asserts this
(MEM-100). If a future rule wants to read an annotation key, that is a
**contract change** and goes through the contract's own gate, not the engine's.

---

## 2. Model/code boundary (ratified design principle)

| Concern | Owner | Rationale |
|---|---|---|
| Write-state classification (4 states) | **MODEL** (prompted, swappable) | probabilistic judgment from messy language |
| Query temporality intent (current vs historical) | **MODEL** (bounded, intent only) | language interpretation |
| Reconciliation judgment (REM pass) | **MODEL** (batched Core tier) | weighing full history requires reading |
| Abstraction (derive schema from episodes) | **MODEL** (batched Core tier) | synthesis |
| Bitemporal store & every mutation | **CODE** | truth is structural |
| Temporal filters (valid_to, tier) | **CODE** | deterministic; a model must never decide what is "current" |
| Injection contract & disclosure | **CODE** (frozen) | security floor |
| Tier mechanics (demote/promote thresholds) | **CODE** (tunable constants) | auditable, reversible |
| Salience scoring | **CODE** (formula over stored metadata) | gates a user-facing interruption; must be explainable |
| Confirmation authority | **CODE** (mirrors ownership model) | permission is structural |
| Audit trail | **CODE** | non-negotiable |
| Queue/batch plumbing | **CODE** | plumbing |

### 2.1 The Interpreter interface (sliding boundary, made explicit)

All model judgment is isolated behind one protocol. Nothing else in the
engine ever constructs a prompt or parses model output:

```python
# memory_engine/interpreter.py

class Interpreter(Protocol):
    def classify_write(self, utterance: str, prior_facts: list[dict]
                       ) -> WriteDecision: ...
        # WriteDecision(state: SUPERSEDE|AUGMENT|CORRECT|UNRESOLVED,
        #               target_fact_id: str|None, confidence: float,
        #               rationale: str)

    def classify_query_temporality(self, query: str) -> Temporality: ...
        # Temporality(historical: bool, confidence: float)
        # INTENT ONLY — the filter that acts on it is code (§5.2)

    def reconcile(self, fact_lineage: list[dict], new_evidence: list[dict]
                  ) -> ReconcileDecision: ...
        # harden/loosen/resolve-unresolved/escalate + rationale

    def abstract(self, episodes: list[dict]) -> list[DerivedFact]: ...
```

Every call is: bounded (token + time budget), logged (prompt hash, model id,
raw output, parsed decision), schema-validated (retry-on-malformed like the
existing `fact_change.py` path), and **swappable** (model id is config, per
method — write-classification can run a small fast model while reconcile runs
the Core-tier model).

**Absorb-ability plan.** As models improve, logic migrates INTO the
Interpreter without rewrites, because callers depend on the decision types,
not the mechanism:

- *Today:* `classify_write` returns a state; code applies MULTI_VALUED
  attribute rules as a deterministic override (e.g. `allergy` never
  SUPERSEDEs on add). *Later:* fold the override into the prompt and demote
  the code rule to a logged assertion — same `WriteDecision` type.
- *Today:* reconcile handles one lineage at a time. *Later:* cross-attribute
  reconciliation (medication ↔ health_condition coherence) — same
  `ReconcileDecision` type, richer input.
- *Today:* salience components come from code lookups. *Later:* the model may
  propose a salience adjustment, but code clamps it to a bounded range —
  advisory only.

**Permanent structural floors — never migrate to the model:** the bitemporal
store and its mutation paths; `valid_to IS NULL` and tier filters; the
injection contract; the audit trail; confirmation authority; the demote/
promote executor. A model may *recommend* a demotion; only code executes it,
logs it, and can reverse it.

**No custom-trained model in scope.** Fine-tuning appears exactly once in
this spec: §10, Phase-C cost note — as a per-inference cost optimization for
the one narrow high-volume task (write-state classification), contingent on
measured economics, never as the memory owner.

---

## 3. Bitemporal data model

### 3.1 Two time axes

- **Valid time** — when the fact was true in the world: `valid_from`,
  `valid_to` (NULL = still true). Already in the schema.
- **Record time** — when the system learned/changed its belief:
  `recorded_at` (write), `record_closed_at` (when a later record superseded
  this row's *belief*, distinct from the fact ceasing to be true).

Two axes because the failure modes differ: "Elena stopped metformin last
week" closes valid time in the past; "I misspoke, it was never metformin"
closes record time — the belief was wrong from the start, and CORRECT must be
distinguishable from SUPERSEDE in the audit trail forever.

### 3.2 `:Fact` node — full property set

Existing properties unchanged (fact_id, owner, subject, attribute,
ciphertext, encrypted_dek, key_version, sensitivity, confidence, valid_from,
valid_to, superseded_by, source_session_id, embedding, timestamp,
migration_status). The engine **adds**:

| Property | Type | Notes |
|---|---|---|
| `recorded_at` | ISO-8601 | record-time open; backfilled = `valid_from` for migrated rows |
| `record_closed_at` | ISO-8601 \| null | record-time close (CORRECT sets this on the erroneous row) |
| `closed_reason` | enum \| null | `superseded` \| `error` \| `retracted` (extends existing `closed_by`) |
| `write_state` | enum | `supersede` \| `augment` \| `correct` \| `unresolved` — the model's decision at write |
| `write_confidence` | float 0–1 | the model's confidence in that decision |
| `driving_utterance_ct` | string | the utterance that caused the write, **encrypted like values (TD-030)** — it contains the fact |
| `tier` | enum | `hot` \| `warm` \| `cold` (default `hot`) |
| `salience` | float 0–1 | code-computed (§8.3); recomputed at consolidation |
| `confirm_when_relevant` | bool | set for UNRESOLVED; cleared on resolution |
| `confirmed_by` / `confirmed_at` | string \| null | human confirmation = ground truth (§8) |
| `derived` | bool | consolidation-derived abstraction |
| `derived_from` | list[fact_id] | provenance for derived facts |
| `last_accessed` / `access_count` | ISO-8601 / int | demotion inputs; updated on injection, not on candidate retrieval |
| `confidence_log` | list (append-only) | `{ts, from, to, source: write|reconcile|confirm, rationale_hash}` |

Supersession key stays `(owner, subject, attribute)`; MULTI_VALUED semantics
unchanged.

### 3.3 The four write states — lifecycle effect of each

| State | Prior row | New row | Signals (examples, not exhaustive — model judges) |
|---|---|---|---|
| SUPERSEDE | `valid_to=now`, `closed_reason=superseded`, `superseded_by=new_id` | opened, `tier=hot` | "switched to", "instead of", "not anymore, now…" |
| AUGMENT | untouched (stays current) | opened, `tier=hot` | "also takes", "added", new value with no replacement signal |
| CORRECT | `valid_to=now` **and** `record_closed_at=now`, `closed_reason=error`, `superseded_by=new_id` | opened; `valid_from` inherits the *erroneous row's* valid_from (the truth was always this) | "actually", "I misspoke", "that's wrong, it's…" |
| UNRESOLVED | untouched | opened with `write_state=unresolved`, `confirm_when_relevant=true`, `confidence` capped at `low`, salience computed | new value, prior exists, no clear replace-vs-add signal |

UNRESOLVED is a first-class state, not a failure: it is the honest answer
when "Elena started Jardiance" arrives and metformin is on file — add or
replace is genuinely undecidable from that sentence. Both facts remain
current; the new one carries its uncertainty into any disclosure (§6.2).

### 3.4 Bidirectional confidence

`confidence` moves both ways, only through logged transitions in
`confidence_log`:

- **HARDEN:** repeated consistent mentions; human confirmation (→ `high`,
  terminal for that lineage until contradicted); consolidation finding
  corroboration.
- **LOOSEN:** contradicting later utterance that itself lands UNRESOLVED;
  consolidation finding incoherence (medication for a condition that was
  retracted); long-aged UNRESOLVED that keeps being not-confirmed.

Code clamps: one consolidation pass may move confidence at most one step
(low↔medium↔high); only human confirmation jumps to `high` directly.

---

## 4. Tiers

| Tier | Contents | Retrieval | How a fact gets here |
|---|---|---|---|
| **HOT** | current (`valid_to IS NULL`) + recently-retired-still-relevant (retired < R days ago, R tunable, default 30) | default injection candidate set | every write opens hot |
| **WARM** | retired, still queryable | surfaced **only** on historical query (§5.2) | demotion from hot (age-since-retirement) |
| **COLD** | archived | **never** in any injection path; only `recall_from_cold()` (§7) | demotion from warm by consolidation criteria |

Cold's exclusion is structural, not policy: the candidate query is
`MATCH (f:Fact) WHERE f.tier IN ['hot','warm'] AND …` — there is no code path
from a live turn to a cold row. MEM-107 seeds a cold fact that would pass
every contract rule and asserts it never reaches the contract at all.

Demotion criteria (all code, all tunable, all logged): age since retirement,
`access_count` / `last_accessed`, confidence, supersession depth (how many
generations superseded). Promotion: a cold fact touched by `recall_from_cold`
gets `access_count` credit; consolidation may promote it back to warm.
Every tier move appends an audit record and is reversible by the inverse move.

---

## 5. Operations

### 5.1 ENCODE (online, write path)

Extends the existing `fact_change.py` flow (Groq Scout detector → Neo4j
apply) — same daemon-thread, never-block-the-turn stance:

```
utterance → Interpreter.classify_write(utterance, current_facts_for_subject)
          → WriteDecision{state, target_fact_id, confidence, rationale}
          → code applies lifecycle per §3.3 (single transaction)
          → audit append (decision, model id, prompt hash, confidence)
```

Code overrides (deterministic, logged when they fire): MULTI_VALUED
attributes never SUPERSEDE on a bare add; a CORRECT with no plausible target
row downgrades to UNRESOLVED; `write_confidence < θ_write` (default 0.6)
downgrades any state to UNRESOLVED — when the model is unsure, the system
stores the uncertainty rather than the guess.

### 5.2 RETRIEVE (online, read path — deterministic filter, bounded model intent)

```
query → Interpreter.classify_query_temporality(query)   # intent ONLY
      → if historical: SQL/Cypher filter tier IN (hot, warm)
        else:          filter tier = hot AND valid_to IS NULL
      → (unchanged) resolve_subject → apply_injection_contract
      → UNRESOLVED facts in the result raise the fluid-confirmation hook (§8.1)
```

The model classifies *what kind of question this is*; it never selects rows.
If the temporality call fails or times out, default = current (the safe,
narrower set). Retired facts surface only under the historical branch, and
they carry `retired: true` so the formatter can say "was on metformin until
June" rather than presenting stale state as current.

### 5.3 CONSOLIDATE (offline, batched — the REM pass)

Runs the Core-tier model, batched and rare (nightly default; tunable),
consistent with the unit-cost thesis: the request path stays edge-tier; the
expensive model runs when nobody is waiting. Four sub-passes, in order:

1. **RECONCILE** — for each lineage with UNRESOLVED rows or recent writes:
   `Interpreter.reconcile(lineage, evidence_since)`. Outcomes: harden /
   loosen confidence (clamped §3.4); resolve UNRESOLVED → retro-apply the
   correct state (e.g. now-clear SUPERSEDE closes the old row *at the
   original valid_from of the new one* — bitemporal makes late resolution
   exact); or leave unresolved. This is the correction path for write-time
   guesses.
2. **ABSTRACT** — derive higher-order facts from episode clusters ("Elena's
   medication changes cluster around cardiology appointments"), written as
   new rows with `derived=true`, `derived_from=[…]`, `confidence=low`,
   subject/owner inherited from the source facts (so the contract governs
   them identically). Derived facts never harden past `medium` without human
   confirmation.
3. **DEMOTE** — apply §4 criteria; hot→warm, warm→cold. Logged, reversible.
4. **ESCALATE** — irreconcilable high-salience lineages (contradiction the
   model cannot resolve, salience ≥ θ_salience) → must-confirm queue (§8.2).

Every sub-pass emits an NDJSON consolidation report (counts, per-fact
decisions, rationale hashes) so a bad pass can be audited and its tier moves
and confidence steps reversed mechanically.

### 5.4 RECALL (intentional cold search)

```python
def recall_from_cold(subject: str, query: str, *, requester: str,
                     reason: str) -> list[dict]:
```

Explicit, logged (who, when, why), deliberate — a distinct API that no
pipeline code calls. Results are returned to the caller (e.g. a future
"remember when…" feature acting on an explicit user ask) and **still pass
through the injection contract** before any disclosure. Never automatic,
never merged into a normal turn's candidates. Access credit may promote (§4).

---

## 6. Disclosure rules (unchanged invariants, new annotations)

1. Contract rules INJ-1..6 apply to every fact the engine returns, on every
   path (current, historical, recall). No engine path skips the contract.
2. UNRESOLVED → hedged rendering, never confident: the grounding formatter
   sees `unresolved: true` and renders "may have started Jardiance —
   unconfirmed" instead of "takes Jardiance".
3. Derived → prefixed rendering: "from patterns I've noticed (unconfirmed):…".
   A derived fact is never spoken as if a human asserted it.
4. Cold → structurally undisclosable in normal turns (§4).
5. Sensitivity ceiling, cross-member deny, owner-read, never-volunteer —
   all enforced where they are today, by code the engine does not touch.

---

## 7. Non-destructive guarantee

- **No deletion, ever.** No engine code path issues `DELETE`. Supersede,
  correct, retract close rows; demote moves tiers; that is the entire
  mutation vocabulary. (The existing `demo_reset.py` wipe is a dev tool
  outside the engine and stays that way.)
- **Full recoverability:** any prior belief state is reconstructible from
  (valid_from, valid_to, recorded_at, record_closed_at, closed_reason,
  superseded_by, confidence_log, tier audit log). "What did we believe about
  Elena's medication on June 1?" is a record-time query.
- **Reversibility:** every consolidation decision carries enough context in
  its report to be mechanically reversed (tier moves are inverse moves;
  confidence steps are logged transitions; resolved-UNRESOLVED retains the
  pre-resolution row state in the audit record).

---

## 8. Resolution paths for UNRESOLVED / must-confirm

### 8.1 FLUID (preferred, zero-friction)

The retrieval-time hook: when a turn's injected set contains a fact with
`confirm_when_relevant=true`, the response composer receives a
`confirmation_opportunity` alongside the facts — subject, attribute, the two
plausible readings. The model folds a natural clarifying question into its
answer: *"Sounds like Elena started Jardiance — is she still on metformin,
or did that stop?"* The user's reply flows through ENCODE like any utterance;
a clear answer resolves the lineage (CORRECT/SUPERSEDE/AUGMENT retro-applied,
`confirm_when_relevant` cleared, confidence hardened, `confirmed_by` set).

Fired at most once per lineage per session (no repeat-nagging within a
conversation); the opportunity is logged whether or not the model used it.

### 8.2 INTENTIONAL (last resort, higher friction)

For items the fluid path hasn't caught: HIP initiates a deliberate,
subject-scoped confirmation session ("Before we go on — I have two things
about Elena I want to get right."). Sourced from the must-confirm queue
(ESCALATE, §5.3d, plus aged high-salience UNRESOLVED). Human confirmation is
ground truth: hardens to `high`, records `confirmed_by`/`confirmed_at`,
clears the queue entry.

### 8.3 Guardrails

**Salience threshold gates the intentional session.** Salience is a code
formula over stored metadata (explainable, no model in the loop):

```
salience = w1·stakes(attribute)        # health/safety/finance = 1.0, else graded
         + w2·query_block_likelihood   # does ambiguity corrupt a likely answer?
                                       #   (attribute access frequency proxy)
         + w3·age_factor(unresolved_since)
```

Only `salience ≥ θ_intentional` (default 0.75) enters the intentional queue.
Low-stakes ambiguity stays quietly UNRESOLVED, disclosed with uncertainty,
forever if need be — **no nagging** is a feature, not a gap.

**Confirmation authority follows the ownership model.** Only someone with
standing to assert a fact has standing to confirm it: the fact's owner, or
its subject (self-confirmation), per the same permit logic as INJ-3 —
computed by mirroring the contract's ownership checks, so the colloquy is
governed by the same structure as disclosure, not a separate ungoverned path.
Sarah cannot "confirm" what Bill said about Elena. A confirmation attempt
without authority is logged and ignored (the session simply doesn't offer
that item to that member).

---

## 9. Memory harness (`eval/memory_harness.py`) — independent gate

Own corpus, own fixtures (in-memory + throwaway Neo4j namespace `:MemFact`
during development; real `:Fact` schema at integration), gated independently.
Added to `gate_check.sh` as **check 7 of 7 only at swap-in** — until then it
runs on the engine track only, so the live gate never depends on unfinished
work. Threshold: 100% (it guards disclosure-adjacent behavior).

Seed corpus (IDs are permanent; ratchet rule applies — every engine bug found
later becomes a MEM-1xx scenario before its fix merges):

| ID | Scenario | Key assertion |
|---|---|---|
| MEM-100 | contract tolerance | InjectionResult byte-identical with/without annotation keys |
| MEM-101 | supersede | one current + one warm-eligible retired row; `superseded_by` chain intact |
| MEM-102 | augment | two current rows, both injectable |
| MEM-103 | correct | prior row `closed_reason=error`, `record_closed_at` set; correction inherits valid_from |
| MEM-104 | unresolved | stored + flagged + rendered hedged; confidence capped low |
| MEM-105 | historical query | warm surfaced with `retired: true` |
| MEM-106 | current query | neither warm nor cold in candidates |
| MEM-107 | cold exclusion | cold fact matching query perfectly absent from candidate set (pre-contract) |
| MEM-108 | consolidation hardens | corroborated lineage steps up one confidence level, logged |
| MEM-109 | consolidation loosens | contradicted lineage steps down, logged |
| MEM-110 | demote + promote | hot→warm→cold on criteria; recall access promotes cold→warm; both reversible from audit |
| MEM-111 | derived tagging | derived fact carries `derived=true` + provenance; rendered with prefix; capped at medium |
| MEM-112 | fluid confirmation | related query surfaces confirmation_opportunity; clear reply resolves lineage |
| MEM-113 | intentional gating | low-salience unresolved never queued; high-stakes aged one queued |
| MEM-114 | confirmation authority | non-owner/non-subject confirmation ignored + logged |
| MEM-115 | recall path | recall_from_cold logged with reason; results still contract-filtered; never merged into a live turn |

---

## 10. Phased build order

Each phase lands green on the engine track before the next starts. Costs are
honest estimates: engineering days (one person, familiar with the codebase)
plus consolidation compute where it applies.

**Phase A — Bitemporal substrate + ENCODE (4 states).**
Schema migration (additive properties, idempotent, reversible — same rules
as P1-1), lifecycle transactions per §3.3, Interpreter protocol +
`classify_write` implementation extending the `fact_change.py` prompt/parse
path, code overrides, audit append. Harness: MEM-100..104.
*Why first:* every other operation reads or mutates this substrate; the
four-state vocabulary is the engine's atoms.
*Cost:* ~6–8 eng-days. No consolidation compute.

**Phase B — RETRIEVE (tiers hot/warm, temporality intent, deterministic filters).**
`candidate_facts()`, temporality classifier (bounded, fail-closed to
current), tier-aware Cypher, annotation keys, formatter hooks for
hedged/retired rendering. Harness: MEM-105..107 + MEM-100 re-run.
*Why second:* retrieval is the frozen-interface surface; proving it identical
-shaped early de-risks the eventual swap. Depends on A's tier column.
*Cost:* ~4–5 eng-days. Temporality call adds one small bounded model call per
text turn on the engine track (edge-tier scale, negligible).

**Phase C — CONSOLIDATE (reconcile, abstract, demote, escalate).**
Batch runner, the four sub-passes, consolidation report, reversal tooling,
salience formula. Harness: MEM-108..111, MEM-113 (queue side).
*Why third:* consolidation is meaningless without a populated bitemporal
store (A) and observable without retrieval (B).
*Cost:* ~8–10 eng-days. **Compute:** nightly batch, Core-tier local model;
est. 500–2,000 tokens per lineage reviewed, tens of lineages per household
per night → single-digit minutes of Core-tier inference per household per
night. On-box, so the cost is thermal/scheduling, not dollars — consistent
with the unit-cost thesis (expensive model runs when nobody waits).
*Phase-C cost note (the only fine-tuning mention, per the ratified boundary):*
if write-state classification volume grows to where per-inference cost of the
prompted general model measurably dominates, a small fine-tuned classifier
for that one narrow task MAY be evaluated as a drop-in behind
`Interpreter.classify_write` — contingent on measured economics, decided by
data, never the memory owner, never expanding beyond that task.

**Phase D — COLD tier + RECALL.**
Demotion to cold (extends C's demote), `recall_from_cold()` with logging and
contract filtering, promotion on re-access. Harness: MEM-107 (full), MEM-110,
MEM-115.
*Why fourth:* cold is a demotion target — it needs C's machinery; recall
needs B's contract plumbing.
*Cost:* ~3–4 eng-days.

**Phase E — Confirmation paths (fluid + intentional).**
Retrieval hook → confirmation_opportunity, composer integration, resolution
via ENCODE, must-confirm queue consumer, subject-scoped session flow,
authority checks. Harness: MEM-112..114.
*Why last:* touches conversation shape (user-visible), so it rides on a fully
proven substrate; fluid resolution needs B's hook and A's retro-apply.
*Cost:* ~6–8 eng-days.

**Integration milestone (after E):** memory_harness added to gate_check.sh as
check 7; pipeline swaps `read_user_facts` → `candidate_facts` (one import);
injection harness, integration harness, seams S1–S3 re-run unchanged; demo
preflight re-run. Swap only when all seven are green.

---

## 11. Honest limits

- **Write-time judgment is probabilistic and will be wrong sometimes.** The
  four-state decision comes from a general model reading one utterance.
  UNRESOLVED converts *known* uncertainty into stored, disclosed uncertainty
  — but a confidently-wrong model won't emit UNRESOLVED, so some
  misclassifications land as confident state. Mitigations, in order:
  consolidation revisits every recent write with more context (§5.3a);
  contradiction later LOOSENs confidence rather than silently coexisting;
  fluid confirmation fires when the affected lineage is actually queried;
  high-salience irreconcilables escalate to a human. Residual risk: a wrong,
  never-contradicted, never-queried, low-salience fact can persist
  indefinitely — bounded by the disclosure rules (it was low-stakes by
  construction) and by non-destruction (the correction, whenever it comes,
  has the full history to act on).
- **Fluid confirmation depends on related queries occurring.** A household
  that never asks about Elena's meds never gives the fluid path an opening;
  only salience-gated escalation catches it, and below the threshold it
  stays unresolved by design.
- **Temporality classification can misread a historical query as current**
  (fail-closed direction: the user sees fewer facts, never leaked ones — a
  UX miss, not a disclosure miss).
- **INJ-2 relevance is keyword-coarse** (unchanged from today). The engine
  inherits it; improving it is a contract-track change, deliberately out of
  scope here.
- **Derived facts are only as good as the episode clustering** — hence the
  hard cap at `medium` confidence and the permanent `derived` tag; a bad
  abstraction can be demoted/loosened by the same machinery as anything else.
- **Consolidation itself can be wrong.** That is why every pass is logged,
  clamped (one confidence step), and mechanically reversible, and why human
  confirmation is the only path to terminal `high`.

---

## 12. Scaffold status

`memory_engine/` package (namespace only, no live-pipeline imports) and
`eval/memory_harness.py` stub (exits 0, prints scaffold notice, NOT wired
into gate_check.sh) may land with this spec — nothing else until Phase A is
approved on the engine track.
