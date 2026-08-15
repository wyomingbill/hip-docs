<!-- STATUS: PLAN -->
<!-- RECONCILED-AGAINST: eval/ (no truth2_harness.py); harness/orchestrator.py:237 (read_user_facts still live — prerequisite memory swap-in not done); TRUTH_LAYER_SPEC hard prerequisite not yet cleared — 2026-07-05 -->

# HIP Truth-Management Layer — Phase 2: Truth Reasoning (Architecture Spec)

**Status: PLAN. Nothing in this document is implemented.**

> ## ⛔ HARD PREREQUISITE — read before anything else
>
> **Phase 2 does not begin until the memory engine is swapped in and live**:
> the integration milestone of `docs/MEMORY_ENGINE_SPEC.md` §10 — pipeline
> runs `candidate_facts()` in place of `read_user_facts()`, memory harness
> wired into `gate_check.sh` as check 7, **all seven gates green**. The
> engine and the Phase-1 truth layer are proven **in isolation**; they are
> not live. Building truth *reasoning* on a not-yet-live engine stacks
> unproven on unproven — Phase 2 reasons over engine state, mutates trust
> ranking through the consolidation machinery, and annotates disclosure, so
> every one of its guarantees inherits from engine behavior that must first
> be proven under live traffic. This spec is the plan; the build waits.

Companion to `docs/MEMORY_ENGINE_SPEC.md` (Phases A–E) and
`docs/TRUTH_LAYER_SPEC.md` (Phase 1: provenance, belief-over-time,
correction-history, trust classification). Phase 1 **formalized** what the
engine already records. Phase 2 is **net-new capability**: reasoning on top
of it.

---

## 0. One-paragraph summary

Phase 2 adds three bounded capabilities and inherits a fourth for free.
**Authority-weighted truth**: an explicit, human-editable, per-domain
authority config that deterministically breaks ties between conflicting
facts — medical authority is not schedule authority — with every override
logged, reversible, and non-destructive, and the overridden fact retaining
full audit standing. **Cross-attribute contradiction detection**: an
offline consolidation sub-pass that detects when facts undermine each other
across attributes (a medication whose motivating condition was retracted)
and **flags to the must-confirm queue, never auto-resolves**. **Trust
inheritance**: derived facts inherit a confidence cap from their
least-trusted source — one hop, no propagation graph, deliberately.
**Dispute resolution** between household members is explicitly *not* a new
component: both assertions stored, flagged UNRESOLVED, authority breaks the
tie where a rule exists, the existing confirmation colloquy handles the
rest. Model involvement at truth-decision time: zero.

---

## 1. Ratified decisions (inputs to this spec, not open questions)

1. **Authority = explicit per-domain config.** Deterministic, auditable,
   human-editable. **Never model-inferred.** A model that guesses who
   outranks whom on medical facts is a liability; a config file the
   household can read and correct is a guarantee.
2. **Contradiction detection = detect-and-flag first.** Contradictions
   route to the must-confirm queue (existing machinery). Auto-resolution is
   a roadmap phase (§4.3) gated on measured false-resolution rate — spec'd
   here, **not built**.

---

## 2. Boundaries (extends the Phase-1 ownership table)

| Concern | Owner | Where |
|---|---|---|
| Authority rules (who outranks whom, per domain) | **Phase 2 config** — human-edited, git-versioned | `config/authority.yaml` (planned) |
| Applying authority to conflicts | **Phase 2 code** — new consolidation sub-pass | `memory_engine/consolidate.py` AUTHORITY pass (planned) |
| Cross-attribute contradiction detection | **Phase 2 code** — consolidation sub-pass, bounded predicates | CONTRADICT pass (planned) |
| Trust inheritance for derived facts | **Phase 2 code** — extends existing derived-cap | ABSTRACT pass extension (planned) |
| Storage, tiers, retrieval, queue, reversal | Memory engine — unchanged machinery, extended vocabulary | existing |
| Disclosure | Injection contract — **frozen, untouched** | `harness/injection_contract.py` |

Phase-2 rules, inherited and extended:

- Truth reasoning **re-ranks trust; it never deletes, hides, or rewrites**.
  Every mutation it makes is an annotation or a logged, reversible
  consolidation action — the same mutation vocabulary as demote/promote.
- All reasoning is **offline** (the REM pass). No authority decision, no
  contradiction check, no inheritance recomputation happens in a live turn.
- Every user-facing effect is **additive annotation** over the frozen
  interface; the injection contract's decisions are byte-identical with
  Phase 2 on or off (§7, TRUTH2-100).

---

## 3. Authority-weighted truth (§highest rigor — the valuable, dangerous one)

### 3.1 The authority config

`config/authority.yaml` — git-versioned, human-editable, schema-validated
at load, refused (fail-closed: no overrides at all) on validation error:

```yaml
version: 1                     # bumped on every edit; hash logged per decision
domains:
  medical:
    attributes: [medication, allergy, health_condition]
    ranks:                     # rank 0 outranks rank 1 outranks rank 2…
      - [role:medical-professional]
      - [subject-self]         # the fact's subject asserting about themself
      - [member:*]             # any household member
  schedule:
    attributes: [schedule]
    ranks:
      - [subject-self]
      - [member:*]
  finance:
    attributes: [financial]
    ranks:
      - [role:finance-owner]
      - [member:*]
roles:                         # explicit member bindings — never inferred
  medical-professional: []     # e.g. [dr-chen] when a provider identity exists
  finance-owner: [bill]
```

Semantics, all deterministic:

- **Domains are configurable groupings of attributes.** An attribute in no
  domain has **no authority rules — no override ever happens** (fail-closed
  default; authority is opt-in per domain).
- **Source selectors**, evaluated against a fact's asserting `owner` (and
  `subject` for `subject-self`): `member:<id>`, `subject-self`,
  `role:<name>` (resolved through the explicit `roles:` registry),
  `member:*`. A fact's rank = the best (lowest-numbered) rank containing a
  selector that matches it.
- **Same rank = no decision.** Authority breaks ties only between
  *different* ranks. Two rank-equal conflicting facts fall through to the
  existing machinery (UNRESOLVED + confirmation colloquy). Authority never
  flips a coin.
- **Config identity is part of every decision**: each authority action logs
  `authority_config_hash` (sha256 of the loaded file) and the matched
  rule (`medical/rank0:role:medical-professional`), so any decision is
  traceable to the exact config text that produced it.

### 3.2 What counts as a conflict

Two facts conflict when **all** hold: same `(subject, attribute)`;
attribute **not** in `MULTI_VALUED` (allergies coexist; that is not a
conflict); both rows current (`valid_to IS NULL`); values distinct. This is
precisely the state today's engine leaves as coexisting AUGMENT/UNRESOLVED
rows when the write-time signal was ambiguous.

### 3.3 The AUTHORITY sub-pass (consolidation)

New REM sub-pass, order: RECONCILE → **AUTHORITY** → ABSTRACT → PROMOTE →
DEMOTE → ESCALATE. After RECONCILE (context may genuinely resolve the
lineage — authority only touches what reconciliation leaves conflicting),
before ESCALATE (a conflict authority settles does not also nag a human).

For each conflicting pair in a configured domain where ranks differ:

- **Winner** (higher authority): annotated `authority_preferred: true`,
  `authority_rule`, `authority_ts`.
- **Loser**: annotated `authority_shadowed: true`, `authority_shadowed_by:
  <winner_fact_id>`, `authority_rule`, `authority_config_hash`,
  `authority_ts`. **Nothing else changes**: `valid_to` untouched (this is
  not SUPERSEDE — the world didn't change), `record_closed_at` untouched
  (not CORRECT — nobody proved error), tier untouched, confidence
  untouched. Shadowing is a **trust re-ranking, not a lifecycle event**.
- Report entries: `{pass: "authority", action: "shadow", fact_id,
  winner_fact_id, rule, config_hash, …}` — same NDJSON report, same
  `reverse_consolidation_pass` machinery: reversal removes the marks and
  logs `unshadow`.

**Retrieval effect** (engine-shaping, contract untouched): the current-
query candidate set excludes `authority_shadowed` rows, exactly as it
excludes `valid_to IS NOT NULL` rows; historical queries include them,
annotated. The engine shapes candidates; the contract governs disclosure of
whatever is shaped — the same split as temporality, ratified in the engine
spec §1.

**Disclosure annotation** (additive): the winner renders with its
provenance — *"per Elena's cardiologist (medical authority, Jun 12)"* — via
the Phase-1 trust-tagging path (TRUTH_LAYER_SPEC §5.3), applied strictly
after `apply_injection_contract`. The shadowed fact, when surfaced
historically, renders *"overridden by [source] per medical authority on
[date] — retained in full"*.

### 3.4 The guardrail: how a WRONG authority rule is caught and corrected

An explicit config can be wrong — a bad rule **confidently overrides
correct information**. This is the highest-risk behavior in Phase 2 and the
reason for every property below:

1. **Deterministic**: same config + same facts → same decision, always.
   No sampling, no model, no time-of-day dependence. A wrong outcome is
   reproducible, therefore diagnosable.
2. **Logged with config identity**: every shadow records the config hash
   and matched rule. "Why did HIP prefer this?" has a one-line answer.
3. **Non-destructive and visible**: the overridden fact keeps its tier,
   lineage, provenance, and full audit standing. It appears in historical
   queries and `lineage()` walks, labeled — an override is *displayed*, not
   disappeared. A household member seeing "overridden by X" on a fact they
   know is right is the primary detection path, by design.
4. **Reversible two ways**: (a) mechanically —
   `reverse_consolidation_pass` on the authority pass restores the prior
   state; (b) by correction — **fix the config and re-run**: the AUTHORITY
   pass is idempotent from current config, so a corrected rule re-ranks the
   same conflicts, emitting logged `unshadow`/`shadow` transitions. No
   state is manufactured or lost in either direction.
5. **Human-editable, human-governed**: the config is a plain file in git.
   Who may edit it is a household governance question (honest limit, §9),
   but every edit is a diff with an author — never a silent model update.

### 3.5 Dispute resolution — falls out, not a component

Two members asserting conflicting facts is **already handled** by the
composition of existing machinery + §3: both facts stored (non-destructive,
always); the conflict lands UNRESOLVED (engine Phase A) or is caught by the
conflict definition (§3.2); if an authority rule covers the domain and the
asserters rank differently, AUTHORITY breaks the tie, logged and reversible;
if not — same rank, or unconfigured domain — the existing confirmation
colloquy (engine §8: fluid then intentional, ownership-gated authority to
confirm) resolves it with a human answer, which is terminal ground truth.
**No new component is built for disputes.** TRUTH2-109 proves the
composition.

---

## 4. Cross-attribute contradiction detection (detect-and-FLAG)

### 4.1 What it detects — two bounded detector classes, both code

Runs offline in the REM pass (new CONTRADICT sub-pass, after AUTHORITY,
before ESCALATE — its flags feed ESCALATE's queue machinery).

**D1 — orphaned support.** A current fact whose recorded support link
points at a fact that has since been closed as error (`closed_reason =
'error'`) or retracted. Example: *medication X recorded in the same breath
as condition Y; Y is later CORRECTed away; X is now suspect.* Link sources,
in order of trust: `derived_from` (exists today for derived facts);
`linked_fact_ids` — a **new, optional** ENCODE capture where the write-time
interpreter may record that an utterance asserted a dependency ("X *for*
Y"). The model contributes links **at write time only** — the edge of the
model/code boundary where interpretation already lives; detection itself
never calls a model.

**D2 — declared-constraint conflicts.** Config-declared attribute pairs
checked by a small, enumerable predicate library — initially two
predicates: `temporal-overlap` (two schedule facts occupying the same
window) and `mutual-exclusion` (config-listed value pairs that cannot
coexist). The library is code; the pairings are config; there is **no
open-ended semantic inference**. If a contradiction class can't be
expressed as a predicate over stored fields, Phase 2 does not detect it —
stated as a limit (§9), not papered over.

### 4.2 What a flag does — and everything it does not do

A detected contradiction produces exactly one thing: a **must-confirm queue
entry** via the existing `_enqueue_must_confirm` (idempotent by fact_id),
salience-scored by the existing formula (stakes of the flagged attribute),
with a deterministic, machine-generated rationale naming both facts and the
predicate that fired: *"medication 'X' links to health_condition retracted
2026-06-30 (orphaned-support)"*.

It does **not**: close either fact, change confidence, change tier, shadow,
or resolve. Resolution is human, through the existing colloquy. The queue
consumer (engine Phase E) needs zero changes — a contradiction flag is just
a queue entry with a richer rationale.

### 4.3 ROADMAP — detect-and-auto-resolve (spec'd, NOT built, separately gated)

Criteria that would make auto-resolution safe, all required:

1. **Decisive inputs**: an authority rule covers the domain and ranks the
   parties differently, **and** the confidence gap between the facts is
   maximal (`high` vs `low`), **and** the losing fact is not
   human-confirmed (a `confirmed_by` fact is never auto-overridden by
   inference).
2. **Measured, not assumed, safety**: during the flag-only phase, a
   **shadow-mode instrument** records what auto-resolution *would* have
   decided for every flag; when a human later resolves that flag, agreement
   is scored. Auto-resolution may be enabled **per domain** only after ≥ 50
   human-resolved flags in that domain with ≥ 98% would-have-agreed — and
   is disabled again automatically if rolling agreement drops.
3. **High-stakes floor**: `medication`, `allergy`, `health_condition`,
   `financial` (the existing HIGH_STAKES set) are **never** auto-resolved
   regardless of measured rate; flags in those domains always reach a
   human.
4. Auto-resolutions, if ever enabled, use the same logged/reversible
   action vocabulary as every consolidation decision.

Until those numbers exist, auto-resolve is a paragraph, not a feature.

---

## 5. Trust inheritance (bounded — deliberately not a graph)

**Whole scope:** a derived fact's confidence is capped at the *minimum* of
(a) `medium` — the existing derived cap, unchanged — and (b) the lowest
confidence among its `derived_from` sources, evaluated at derivation time
and re-evaluated during RECONCILE when a source's confidence changes
(one-step clamp per pass, as all confidence moves). A derived fact built
partly on a `low`-confidence source is `low`, and its `confidence_log`
entry says which source capped it and why.

**Anti-over-engineering boundary, stated as a decision:** this is
**one-hop, cap-only inheritance — not a trust-propagation graph.** No
transitive recomputation cascades through chains (a derived-of-derived
fact applies the same rule at its own creation against its own direct
sources); no weighted blending; no dampening factors. A propagation graph
is where explainability goes to die — "why did this fact's trust drop?"
must never require walking twelve edges of float arithmetic. Bounded
inheritance captures the real value (garbage-in is visibly labeled
garbage-out) and every cap is explainable in one sentence from its own
log entry. If evidence ever demands more, that is a future spec with its
own falsifiable case; the default answer to "should trust propagate
further?" is **no**.

---

## 6. Model/code boundary (restated for Phase 2)

**Model role at truth-decision time: zero.** The authority config is
human-written; rank matching, conflict detection, shadowing, contradiction
predicates, queue routing, inheritance caps — all deterministic code over
stored state, reproducible from (facts, config, code version) alone. The
model's only Phase-2 contribution is `linked_fact_ids` capture at **write
time** (§4.1) — the same edge where write-state classification already
lives, recorded as provenance and then *judged later by code*. Nothing in
Phase 2 asks a model "who should win?", "is this a contradiction?", or
"how trustworthy is this?" — those are exactly the questions that must
have auditable answers.

---

## 7. Frozen-interface and contract guarantees (the MEM-100 rule, again)

- All Phase-2 fact effects are **additive annotation keys**
  (`authority_shadowed`, `authority_preferred`, `authority_rule`,
  `linked_fact_ids`, inheritance entries in `confidence_log`) or existing
  logged consolidation actions. The 7-key pipeline shape is untouched.
- **TRUTH2-100 asserts byte-identical `InjectionResult`** — same allowed
  set, same denied set, same guard state, same order — with Phase-2
  annotations present vs stripped. The contract never reads an authority
  key; authority can change *which candidates the engine shapes* (§3.3,
  the engine's ratified job) but never *what the contract permits* of any
  candidate it sees.
- Candidate-set shaping by `authority_shadowed` is engine-track behavior
  gated by the memory harness, exactly like tier and temporality filters.

---

## 8. Claims discipline (unchanged rules, Phase-2 vectors added)

Language: **"built, tested, and integration-ready behind the frozen
injection contract"** until swap-in; after swap-in, live claims cover only
what the seven green gates cover. **Never "can't leak"** — the permitted
form remains: *structurally constrained from injecting facts outside the
contract, with deterministic disclosure controls and auditability.*

Phase-1's six residual vectors (TRUTH_LAYER_SPEC §8) carry forward
unchanged. Phase 2 adds:

| # | Residual vector | Status |
|---|---|---|
| 7 | **Wrong authority config** — a bad rule confidently and *systematically* prefers wrong facts | Mitigated: deterministic + config-hash-logged + visible override labels + non-destructive + reversible + human-editable (§3.4). Not eliminated: a wrong rule operates until a human notices. The overridden fact's retained standing is the recovery guarantee. |
| 8 | **Authority-config governance** — whoever edits the config holds structural power over household truth | Out of scope technically (it's a file with git history); named honestly: HIP makes the power *visible and auditable*, it cannot make it wise. |
| 9 | **Link quality** — `linked_fact_ids` come from the write-time model; missed links = missed contradictions (false negatives), spurious links = noisy flags | Mitigated: links only ever produce *flags to a human*, never resolutions; a spurious flag costs a question, a missed one costs nothing that today's system catches either. |
| 10 | **Predicate coverage** — D2 detects only what its enumerable predicates express | By design (§4.1); the alternative is open-ended model judgment at decision time, which is the boundary this architecture exists to hold. |

---

## 9. Honest limits

- **An explicit authority config can be wrong** — and wrong with
  confidence. Full mitigation stack in §3.4; the irreducible residual is
  the window between a bad rule taking effect and a human noticing a
  visible override label. Non-destruction bounds the damage: nothing is
  lost, everything is recoverable, the audit trail is complete.
- **Authority ranks sources, not truth.** A cardiologist can be wrong; the
  config encodes *whom the household chooses to prefer*, and the rendering
  says "per [source]", never "true".
- **Detection is bounded by links and predicates** (§4.1). Contradictions
  invisible to both detector classes persist exactly as they do today.
- **Flag fatigue is a real failure mode**: over-eager predicates would
  flood the must-confirm queue and train humans to ignore it. The salience
  gate and idempotent enqueue are the existing controls; flag volume is a
  measured quantity in the shadow-mode instrument, watched from day one.
- **Trust inheritance is only as good as `derived_from`** — same episode-
  clustering caveat as the engine spec §11.
- **Everything above inherits the engine's own §11 limits** — write-time
  misclassification most of all.

---

## 10. Tests — `eval/truth2_harness.py` (TRUTH2-1xx)

Independent gate on the engine track; same conventions (dev port guard,
throwaway namespace, MockInterpreter, per-scenario PASS/FAIL). **Wired into
`gate_check.sh` at/after swap-in only** — consistent with the prerequisite:
these tests exist before the build, gate the build, and join the wall only
when the wall is real. Authority scenarios get the most rigor (they guard
the highest-risk behavior).

| ID | Scenario | Load-bearing assertion |
|---|---|---|
| TRUTH2-100 | Contract byte-identity | `InjectionResult` byte-identical with Phase-2 annotations present vs stripped; contract never reads an authority key |
| TRUTH2-101 | Authority determinism | same config + same conflicting facts → same winner across repeated passes; action logs config hash + matched rule |
| TRUTH2-102 | Override reversibility + retention | shadowed fact still in historical retrieval + `lineage()` with full provenance; `reverse_consolidation_pass` restores pre-shadow state exactly |
| TRUTH2-103 | **Wrong-config correction** | bad rule shadows the correct fact → config fixed → re-run unshadows and re-ranks; every transition (`shadow`→`unshadow`→`shadow`) in the report; nothing lost |
| TRUTH2-104 | Fail-closed defaults | unconfigured domain → zero authority actions; invalid config → load refused, zero overrides, conflict falls to existing UNRESOLVED path |
| TRUTH2-105 | Same-rank no-decision | two rank-equal conflicting facts → no shadow; lineage proceeds to confirmation machinery |
| TRUTH2-106 | D1 orphaned support | retract the linked condition → dependent medication flagged to must-confirm queue with deterministic rationale; **both facts untouched otherwise** |
| TRUTH2-107 | D2 declared constraint | temporal-overlap fixture flagged; not resolved; salience-scored; idempotent re-run adds no duplicate |
| TRUTH2-108 | Trust inheritance | derived fact from a `low` source caps at `low` with attributing log entry; source hardens later → derived recomputes up one clamped step |
| TRUTH2-109 | Dispute composition | two members conflict: with covering rule → ranked + logged; same-rank/unconfigured → UNRESOLVED + colloquy. Proves §3.5 needs no new component |
| TRUTH2-110 | Shadow-mode instrument | flag-only phase records the would-have-been auto-resolution per flag; no resolution performed; agreement scoring computes from fixtures |
| TRUTH2-111 | Confirmed-fact floor | a `confirmed_by` fact is never shadowed by a lower-rank assertion and never auto-resolvable (roadmap floor holds structurally) |

Ratchet rule inherited: any bug found during the Phase-2 build lands as a
TRUTH2-1xx scenario before its fix merges.

---

## 11. Phased plan + honest cost

Preconditions: swap-in milestone complete (all seven gates green);
Phase-1 T-A..T-C landed (trust classification + tagging exist for authority
annotations to extend).

| Phase | Contents | Cost / risk |
|---|---|---|
| **2-A Authority** | `config/authority.yaml` + schema validation; AUTHORITY sub-pass; shadow/unshadow actions + reversal; candidate-set exclusion; disclosure annotation; TRUTH2-100..105, 109, 111 | ~6–8 eng-days. **Highest risk in the phase — most test rigor by design** (7 of 12 scenarios). Risk is concentrated in retrieval exclusion (gated by full MEM harness re-run) and config semantics (fail-closed everywhere). |
| **2-B Contradiction detect-and-flag** | `linked_fact_ids` ENCODE capture (small engine-track write change, MEM-gated); D1 + D2 predicates; CONTRADICT sub-pass → queue; TRUTH2-106..107 | ~4–5 eng-days. Low risk: output is only queue entries. Flag-volume watch from day one. |
| **2-C Trust inheritance** | min-of-sources cap at derivation + RECONCILE recompute; TRUTH2-108 | ~1–2 eng-days. Lowest risk; extends an existing cap. |
| **2-D Shadow-mode instrument** | would-have-resolved recorder + agreement scoring; TRUTH2-110 | ~1–2 eng-days. Pure instrumentation; the data that gates the §4.3 roadmap. |
| **Roadmap (not scheduled)** | detect-and-auto-resolve per §4.3 criteria | Gated by 2-D's measured numbers, per domain, high-stakes floor permanent. No date until the data exists. |

Explicitly deferred: auto-resolution (§4.3); trust-propagation beyond one
hop (§5, default answer no); provider-identity infrastructure (the
`roles:` registry accepts bindings but building provider identities is not
a truth-layer concern); any UI beyond dashboard consumption of the new
annotations.
