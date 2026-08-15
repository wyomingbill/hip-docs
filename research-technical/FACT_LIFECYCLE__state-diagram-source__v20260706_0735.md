# Fact Lifecycle — State Diagram Source
<!-- status: BUILT — extracted from live code 2026-07-06 -->

Extracted read-only from hip-dev. Every claim cited to file:line.
Use this as the authoritative input for the state diagram; see **§5** for spec gaps.

---

## 1. Trust Levels (States)

Evaluated **first-match-wins** in this order (`truth_layer/queries.py:694–724`).
`_CONF_ORDER = {"low": 0, "medium": 1, "high": 2}` — `queries.py:605`.

| Level | Exact Predicate | Fields Read |
|---|---|---|
| **DERIVED** | `derived == true` — wins over all other levels, checked first | `derived` |
| **CONFIRMED** | `confirmed_by IS NOT NULL` | `confirmed_by` |
| **CORROBORATED** | `confidence == "high"` AND `confidence_log` has ≥1 entry where `source == "reconcile"` AND `_CONF_ORDER[to] > _CONF_ORDER[from]` AND NOT `derived` | `confidence`, `confidence_log`, `derived` |
| **ASSERTED** | `write_state IN {"supersede","augment","correct"}` AND `confidence IN {"medium","high"}` AND NOT `derived` | `write_state`, `confidence`, `derived` |
| **UNCONFIRMED** | catch-all: `write_state == "unresolved"` OR `confidence == "low"` | `write_state`, `confidence` |

**Staleness** (`queries.py:624–635`): orthogonal boolean — `last_accessed` older than
`STALE_DAYS = 180`. Never changes trust level.

**⚠ Divergent duplicate:** `fact_change.py:142–167` has its own `_classify_trust()`.
Its CORROBORATED predicate checks any `reconcile` entry where `to IN ("medium","high")`
rather than the numeric `to > from` comparison in `queries.py`. Can classify the same
fact differently.

---

## 2. Write-States (Transition Types)

`WriteDecision.state` field (`interpreter.py:66`). Applied by `store.py:297–444`.

### SUPERSEDE (`store.py:226–260`)
- **Prior row(s):** `valid_to = now`, `closed_reason = "superseded"`, `superseded_by = new_fact_id`.
  Targets a specific `target_fact_id`, or ALL active rows for `(attribute, owner, subject)` if `target_fact_id is None`.
- **New row:** `valid_from = now`, `valid_to = null`, `write_state = "supersede"`, `confidence = base_confidence`.
- **Trigger:** model sees replacement signal ("switched to", "instead of").
- **Override:** SUPERSEDE on a `MULTI_VALUED` attribute is silently promoted to AUGMENT (`store.py:329–332`).

### AUGMENT (`store.py:263–265`)
- **Prior rows:** untouched; remain current.
- **New row:** created alongside existing rows.
- **Trigger:** model sees additive signal ("also", "added").

### CORRECT (`store.py:268–287`)
- **Prior row:** `valid_to = now`, `record_closed_at = now` *(only state that sets this)*, `closed_reason = "error"`, `superseded_by = new_fact_id`.
- **New row:** `valid_from` inherited from erroneous row's `valid_from`; `write_state = "correct"`.
- **Trigger:** model sees "was always wrong" signal ("actually", "I misspoke").
- **Override:** CORRECT with no `target_fact_id` → demoted to UNRESOLVED (`store.py:334–337`).

### UNRESOLVED (`store.py:290–293`)
- **Prior rows:** untouched; both old and new fact have `valid_to IS NULL` — injection set may contain both.
- **New row:** `write_state = "unresolved"`, `confidence = "low"` (capped), `confirm_when_relevant = true`.
- **Forced by three code overrides** (`store.py:325–347`):
  1. CORRECT + no `target_fact_id` → UNRESOLVED
  2. `write_confidence < 0.6` → UNRESOLVED regardless of requested state
  3. *(MULTI_VALUED + SUPERSEDE → AUGMENT, not UNRESOLVED)*

---

## 3. Transition Map

**Prior trust** = level of existing fact acted upon.
**New node trust** = level the newly created node starts at.
Harden/confirm mutations update the **same** node in-place (no new node created).

| Prior trust | Write-state | Prior node after | New node trust |
|---|---|---|---|
| Any | **SUPERSEDE** | closed: `valid_to`, `closed_reason="superseded"`, `superseded_by` | ASSERTED |
| Any | **AUGMENT** | untouched, stays current | ASSERTED |
| Any | **CORRECT** (with `target_fact_id`) | closed: `valid_to`, `record_closed_at`, `closed_reason="error"` | ASSERTED |
| Any | **CORRECT** (no `target_fact_id`) → override | untouched | UNCONFIRMED |
| Any | **UNRESOLVED** (`write_confidence < 0.6`) | untouched | UNCONFIRMED |
| ASSERTED | consolidation **harden** (reconcile pass) | mutates in-place: confidence_log entry added, confidence raised | → CORROBORATED (same node) |
| CORROBORATED | human **confirm** | mutates in-place: `confirmed_by`, `confirmed_at` set | → CONFIRMED (same node) |
| UNCONFIRMED | consolidation **resolve** | `_reconcile_pass` retro-applies SUPERSEDE/CORRECT/AUGMENT | new node at original `valid_from` |

### Spec-only / not-built cells
- **ASSERTED→CORROBORATED** and **UNCONFIRMED→resolved** require consolidation
  (`memory_engine/consolidate.py`), which is **built but not wired into the live pipeline**.
  Cannot happen in a live session without an explicit offline tool invocation.
- **Fluid confirmation** (`confirm_when_relevant=true` → clarifying question): flag written,
  nothing reads it in `harness/orchestrator.py`. **NOT BUILT.**
- **`must_confirm_queue` consumption:** queue appended by `_escalate_pass`; no live code reads
  it. **NOT BUILT.**

---

## 4. Terminal / Special States

### Superseded fact
- `valid_to` set; `closed_reason = "superseded"`; `superseded_by` → new fact id.
- **Still walkable:** `lineage()` (`queries.py:431`) BFS includes superseded rows.
  `correction_history()` excludes them (filters `closed_reason = "error"` only).
- **Never injected:** live retrieval (`read_user_facts()`) filters `WHERE f.valid_to IS NULL`.
- **Cannot be re-opened:** no code path clears `valid_to` on an existing node.
- `trust()` still evaluates it (no `valid_to` guard), but moot — never surfaces in injection.

### DERIVED fact
- Always written `confidence = "low"` (`interpreter.py:101`).
- `trust()` checks DERIVED before CONFIRMED (`queries.py:698–701`): a derived fact with
  `confirmed_by` set still returns DERIVED. **Trust level is permanently DERIVED.**
- Can be superseded, augmented, or corrected structurally — but trust stays DERIVED.
- **Spec/code gap:** spec §8 implies confirmed derived facts can reach CONFIRMED; predicate
  ordering makes that unreachable in `trust()`.

### UNRESOLVED fact
- `valid_to IS NULL` — it is current and competes in the injection set alongside prior facts.
- **Resolution paths:**
  1. `_reconcile_pass` (`consolidate.py:267`): offline only — retro-applies a write-state.
  2. Subsequent SUPERSEDE utterance closes it normally (qualifies under `valid_to IS NULL`).
  3. Fluid confirmation hook: **not implemented**.
- Can persist indefinitely if consolidation isn't run and no utterance supersedes it.

---

## 5. Spec vs Implementation Gaps

| Spec claim | Code behavior | Status |
|---|---|---|
| §8.1: `confirm_when_relevant=true` triggers `confirmation_opportunity` at turn time | Flag written (`store.py:364`). Nothing reads it in live orchestrator. | **NOT BUILT** |
| §8.2: `must_confirm_queue` consumed by HIP-initiated confirmation session | Queue appended by `_escalate_pass`; no live code reads it. | **NOT BUILT** |
| §4: WARM-tier facts surface on historical queries via tier filter | `read_user_facts()` uses `WHERE f.valid_to IS NULL`; no tier filter. `memory_engine/api.py:candidate_facts()` and `recall.py` implement tier-aware retrieval but are not called from `harness/orchestrator.py`. | **NOT WIRED** |
| §3.4: DERIVED can reach CONFIRMED after human confirmation | DERIVED predicate fires before CONFIRMED in `queries.py:698–701`; CONFIRMED unreachable for derived node. | **Code contradicts spec** |
| Two trust classifiers must agree | `fact_change.py:142–167` vs `truth_layer/queries.py:694–724` use different CORROBORATED predicates | **Divergence — can disagree** |
| §3.3: CORRECT inherits erroneous row's `valid_from` | `_tx_correct()` passes `f.valid_from` as `corrected_props["valid_from"]` (`store.py:283–286`). | **Matches spec** |
| No deletion ever | No `DELETE` in any reviewed path. | **Matches spec** |
| Consolidation pipeline runs as part of live turns | Implemented in `consolidate.py`; called from `api.py:consolidate_owner()`; that function is not called from `harness/orchestrator.py`. | **Built, not wired — offline only** |

---

## 6. Live Node Schema (confirmed from DB, 2026-07-06)

All §3.2 spec fields present on live `:Fact` nodes. Observed values:

```
fact_id, attribute, subject, owner
ciphertext, encrypted_dek, key_version
confidence:            "high" | "medium" | "low"
write_state:           "supersede"  (only value in sample)
valid_from:            ISO timestamp
valid_to:              null (active) | ISO (closed)
superseded_by:         null | uuid
closed_reason:         null | "superseded"
record_closed_at:      null  — only set by CORRECT, none observed
confirm_when_relevant: false
confirmed_by:          null
confirmed_at:          null
derived:               false
derived_from:          []
tier:                  "hot"
salience:              0.6
confidence_log:        [json_strings]
write_confidence:      0.75 | 0.9
embedding:             null  — not populated
last_accessed:         null
access_count:          0
migration_status:      "engine_phase_a"
```

No live facts with `derived=true`, `confirmed_by` set, `write_state="correct"`,
`write_state="unresolved"`, or `write_state="augment"` in the sample —
demo seed uses direct supersede writes only.
