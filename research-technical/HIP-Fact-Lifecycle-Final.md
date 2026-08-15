# HIP Fact Lifecycle Redesign -- Implementation Spec (Final)

## Context

Read these files before writing any code:
- harness/extraction_queue.py (full file)
- server/voice_orch.py (lines 580-1000, contradiction handling + OrchestratorGate)
- harness/orchestrator.py (local_system_prompt method)
- scripts/demo_seed.py
- scripts/demo_reset.py

## Problem

Contradicted facts survive voice server restarts. Four subsystems (detection, suppression, extraction, supersession) operate independently. The user confirms a correction, the system suppresses it for the current session in a Python set, then the process restarts and the old fact is back. Meanwhile, extraction writes a negation fact ("does not take") alongside the original ("takes") because supersession only matches exact subject+predicate+owner.

## Design Principles

1. **Single write authority.** extraction_queue.py is the only component that mutates Neo4j. voice_orch.py detects, challenges, confirms, and suppresses in-memory. It never writes to the graph.
2. **Temporal facts.** Replace boolean `superseded` with `valid_from` / `valid_to` timestamps. Active facts have `valid_to = null`. Retraction, supersession, and dedup all close the temporal window.
3. **Retractions are first-class extraction events.** The extraction prompt recognizes contradictions and emits structured retraction objects. The write path matches them against active facts and closes temporal windows without creating new nodes.
4. **Deterministic retraction path.** When voice_orch confirms a contradiction, it appends a structured retraction marker to the session transcript. The extraction pipeline processes markers first (no LLM needed). Prompt-based retraction detection is the fallback for contradictions voice_orch missed.
5. **Hot cache stays.** The in-memory `_suppressed_facts` set in voice_orch.py continues to handle same-session UX. It is not a persistence mechanism.
6. **Read shape is unchanged.** `read_user_facts` continues returning `{subject, predicate, object, confidence}` by decrypting `ciphertext` internally. Orchestrator and tests do not change.

## Out of Scope

Do NOT build any of the following:
- Durable retraction event queue
- Per-turn crash recovery or transcript journaling
- Mandatory attribute_key taxonomy or fact normalization
- Manual correction review UI
- Complex confidence arbitration between competing facts
- Production-grade event sourcing
- Multi-tenant correction pipeline
- Separate memory audit service

This is an architecture prototype demonstrating the right seams, not a production correction platform.

## Implementation Order

This order is mandatory. Do not rearrange.

1. Add constants and new functions to extraction_queue.py (RETRACTION_THRESHOLD, _MEDICAL_KEYWORDS, _retract_one, _parse_retraction_markers)
2. Update _coerce_fact and EXTRACTION_PROMPT
3. Update _write_one to temporal properties
4. Deploy and run migrate_temporal.py
5. Verify migration: no facts have the old `superseded` property, all facts have `valid_from`
6. Update read path (read_user_facts, search_facts_by_embedding) to `valid_to IS NULL`
7. Update write_facts and process_session
8. Determine the correct marker injection target in voice_orch.py (investigation step below)
9. Wire retraction markers into voice_orch.py
10. Run all tests

Steps 4-6 are sequenced deliberately: if the read path switches to `valid_to IS NULL` before migration, old superseded facts (which lack `valid_to`) will appear active because a missing property IS NULL in Neo4j. Run migration first.

If for any reason migration cannot run before the read path change, use this temporary backward-compatible filter:

```cypher
WHERE f.valid_to IS NULL AND coalesce(f.superseded, false) = false
```

Remove the `superseded` clause after migration completes.

## Changes

### 1. New constants

File: `harness/extraction_queue.py`

Add next to the existing DEDUP_THRESHOLD:

```python
DEDUP_THRESHOLD = 0.90
RETRACTION_THRESHOLD = 0.90    # separate: retraction is more destructive than dedup
```

Add at module level (near other constants/regex):

```python
import re  # if not already imported

_MEDICAL_KEYWORDS = re.compile(
    r"\b(medication|medicine|meds|prescription|drug|dose|dosage|"
    r"allerg|diagnos|symptom|condition|treatment|surgery|therap)\b",
    re.IGNORECASE)
```

### 2. Schema: temporal facts

Replace `superseded` (bool) and `superseded_at` (timestamp) with four new properties on :Fact nodes:

- `valid_from` (string, ISO-8601 UTC): when the fact became active. Same value as `timestamp`.
- `valid_to` (string, nullable): when the fact was closed. Null means active.
- `closed_by` (string, nullable): why closed. Values: `superseded`, `retracted`, `dedup`.
- `closed_session` (string, nullable): source_session_id of the session that closed it.

Neo4j is schemaless. No DDL needed. New properties appear on nodes as they are written/modified.

### 3. Migration script

New file: `scripts/migrate_temporal.py`

```python
"""One-time migration: superseded/superseded_at -> valid_from/valid_to.

Run once after deploying the temporal fact schema. Idempotent.

    python scripts/migrate_temporal.py
    python scripts/migrate_temporal.py --dry-run
"""
from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from harness.extraction_queue import _get_driver  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python scripts/migrate_temporal.py",
        description="Migrate :Fact nodes from superseded to temporal schema.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print counts without modifying the graph.")
    args = parser.parse_args(argv)

    driver = _get_driver()
    with driver.session() as sess:
        # Count current state
        active = sess.run(
            "MATCH (f:Fact) WHERE coalesce(f.superseded, false) = false "
            "AND f.valid_from IS NULL RETURN count(f) AS n"
        ).single()["n"]
        closed = sess.run(
            "MATCH (f:Fact) WHERE f.superseded = true "
            "AND f.valid_from IS NULL RETURN count(f) AS n"
        ).single()["n"]
        already = sess.run(
            "MATCH (f:Fact) WHERE f.valid_from IS NOT NULL RETURN count(f) AS n"
        ).single()["n"]

        print(f"  Active (superseded=false, no valid_from): {active}")
        print(f"  Closed (superseded=true, no valid_from):  {closed}")
        print(f"  Already migrated (has valid_from):        {already}")

        if args.dry_run:
            print("\n(dry-run) no changes made.")
            return 0

        if active == 0 and closed == 0:
            print("\nNothing to migrate.")
            return 0

        # Migrate active facts
        sess.run(
            "MATCH (f:Fact) WHERE coalesce(f.superseded, false) = false "
            "AND f.valid_from IS NULL "
            "SET f.valid_from = f.timestamp, f.valid_to = null"
        )
        # Migrate superseded facts
        sess.run(
            "MATCH (f:Fact) WHERE f.superseded = true "
            "AND f.valid_from IS NULL "
            "SET f.valid_from = f.timestamp, "
            "    f.valid_to = coalesce(f.superseded_at, f.timestamp), "
            "    f.closed_by = 'superseded'"
        )
        # Remove old properties
        sess.run(
            "MATCH (f:Fact) WHERE f.superseded IS NOT NULL "
            "REMOVE f.superseded, f.superseded_at"
        )

        print(f"\n  Migrated {active} active + {closed} closed facts.")
        print("  Removed superseded/superseded_at properties.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 4. EXTRACTION_PROMPT: recognize retractions

File: `harness/extraction_queue.py`

Replace the existing EXTRACTION_PROMPT constant:

```python
EXTRACTION_PROMPT = (
    "Extract facts and retractions from these conversation turns.\n\n"
    "For each STATED FACT, output a JSON object with:\n"
    "  type: \"assertion\"\n"
    "  subject, predicate, object, confidence (high/medium/low), "
    "sensitivity (low/medium/high/critical)\n\n"
    "For each RETRACTION (the user denies, corrects, or contradicts a "
    "previously stated fact, and confirms the change), output:\n"
    "  type: \"retraction\"\n"
    "  subject, predicate, object (the fact being retracted, not the new value)\n"
    "  confidence: how confident the retraction is (usually \"high\" if confirmed)\n\n"
    "Retraction pattern: the assistant states a fact, the user says it is wrong, "
    "the assistant asks for confirmation, the user confirms. The retracted fact "
    "is the one the assistant quoted, not the user's correction.\n\n"
    "A transcript entry tagged [CONFIRMED_RETRACTION] is an explicit retraction "
    "marker. Always emit a retraction for it.\n\n"
    "Only extract facts and retractions, not questions or filler."
)
```

### 5. _coerce_fact: handle retraction type + sensitivity floor

File: `harness/extraction_queue.py`

Replace the existing `_coerce_fact` function:

```python
def _coerce_fact(raw: dict) -> dict | None:
    """Validate one raw fact dict; return a normalized fact or None to drop it."""
    if not isinstance(raw, dict):
        return None
    subj = str(raw.get("subject", "")).strip()
    pred = str(raw.get("predicate", "")).strip()
    obj = str(raw.get("object", "")).strip()
    if not (subj and pred and obj):
        return None
    conf = str(raw.get("confidence", "")).strip().lower()
    if conf not in CONFIDENCE_LEVELS:
        conf = "medium"
    fact_type = str(raw.get("type", "assertion")).strip().lower()
    if fact_type not in ("assertion", "retraction"):
        fact_type = "assertion"
    result = {"subject": subj, "predicate": pred, "object": obj,
              "confidence": conf, "type": fact_type}
    if fact_type == "assertion":
        sens = str(raw.get("sensitivity", "")).strip().lower()
        if sens not in SENSITIVITY_LEVELS:
            sens = "medium"
        if sens == "low" and _MEDICAL_KEYWORDS.search(f"{subj} {pred} {obj}"):
            sens = "high"
        result["sensitivity"] = sens
    return result
```

### 6. _write_one: temporal properties

File: `harness/extraction_queue.py`

Replace the existing `_write_one` function:

```python
def _write_one(tx, fact: dict, owner: str, session_id: str, timestamp: str,
               embedding) -> bool:
    """Write one assertion. Closes prior versions, creates new node with
    valid_from set and valid_to null."""

    # 1. Embedding dedup: skip if a newer duplicate exists
    dup_ids: list = []
    if embedding:
        rows = list(tx.run(
            "MATCH (f:Fact {subject: $subject, owner: $owner}) "
            "WHERE f.valid_to IS NULL AND f.embedding IS NOT NULL "
            "RETURN elementId(f) AS eid, f.embedding AS embedding, "
            "f.timestamp AS ts",
            subject=fact["subject"], owner=owner,
        ))
        for r in rows:
            if _cosine(embedding, r["embedding"]) >= DEDUP_THRESHOLD:
                if r["ts"] is not None and r["ts"] > timestamp:
                    log.info("skipping duplicate fact (newer exists): %s / %s",
                             fact["subject"], fact["predicate"])
                    return False
                dup_ids.append(r["eid"])

    # 2. Encrypt value
    ciphertext, encrypted_dek = encrypt_fact_value(fact["object"], owner)

    # 3. Close prior exact-match facts (subject+predicate+owner)
    tx.run(
        "MATCH (f:Fact {subject: $subject, predicate: $predicate, owner: $owner}) "
        "WHERE f.valid_to IS NULL "
        "SET f.valid_to = $ts, f.closed_by = 'superseded', "
        "    f.closed_session = $sid",
        subject=fact["subject"], predicate=fact["predicate"], owner=owner,
        ts=timestamp, sid=session_id,
    )

    # 4. Close embedding duplicates (different predicate, same attribute)
    if dup_ids:
        tx.run(
            "MATCH (f:Fact) WHERE elementId(f) IN $eids "
            "AND f.valid_to IS NULL "
            "SET f.valid_to = $ts, f.closed_by = 'dedup', "
            "    f.closed_session = $sid",
            eids=dup_ids, ts=timestamp, sid=session_id,
        )

    # 5. Create new fact
    tx.run(
        "CREATE (n:Fact {subject: $subject, predicate: $predicate, "
        "ciphertext: $ciphertext, encrypted_dek: $encrypted_dek, "
        "key_version: $key_version, owner: $owner, confidence: $confidence, "
        "sensitivity: $sensitivity, timestamp: $timestamp, "
        "valid_from: $timestamp, valid_to: null, "
        "source_session_id: $session_id, "
        "embedding: $embedding})",
        subject=fact["subject"], predicate=fact["predicate"],
        ciphertext=ciphertext, encrypted_dek=encrypted_dek,
        key_version=KEY_VERSION,
        owner=owner, confidence=fact["confidence"],
        sensitivity=fact["sensitivity"],
        timestamp=timestamp, session_id=session_id, embedding=embedding,
    )
    return True
```

### 7. New function: _retract_one

File: `harness/extraction_queue.py`

Add near `_write_one`:

```python
def _retract_one(tx, fact: dict, owner: str, session_id: str,
                 timestamp: str) -> bool:
    """Process one retraction. Finds the matching active fact and closes its
    temporal window. Does NOT create a new node.

    Matching strategy:
    1. Exact subject+predicate+owner match.
    2. Embedding similarity on subject+predicate (catches near-miss predicates
       like "takes" vs "takes medication").
    """
    # 1. Exact match
    result = tx.run(
        "MATCH (f:Fact {subject: $subject, predicate: $predicate, owner: $owner}) "
        "WHERE f.valid_to IS NULL "
        "SET f.valid_to = $ts, f.closed_by = 'retracted', "
        "    f.closed_session = $sid "
        "RETURN count(f) AS n",
        subject=fact["subject"], predicate=fact["predicate"], owner=owner,
        ts=timestamp, sid=session_id,
    )
    if result.single()["n"] > 0:
        log.info("retracted (exact match): %s/%s owner=%s",
                 fact["subject"], fact["predicate"], owner)
        return True

    # 2. Embedding similarity fallback
    retract_vec = embed_text(_fact_text(fact))
    if not retract_vec:
        log.warning("retraction embedding failed, no match: %s/%s",
                    fact["subject"], fact["predicate"])
        return False

    rows = list(tx.run(
        "MATCH (f:Fact {subject: $subject, owner: $owner}) "
        "WHERE f.valid_to IS NULL AND f.embedding IS NOT NULL "
        "RETURN elementId(f) AS eid, f.embedding AS embedding, "
        "f.predicate AS predicate",
        subject=fact["subject"], owner=owner,
    ))
    best_eid, best_sim, best_pred = None, 0.0, None
    for r in rows:
        sim = _cosine(retract_vec, r["embedding"])
        if sim > best_sim:
            best_eid, best_sim, best_pred = r["eid"], sim, r["predicate"]

    if best_eid and best_sim >= RETRACTION_THRESHOLD:
        tx.run(
            "MATCH (f:Fact) WHERE elementId(f) = $eid "
            "SET f.valid_to = $ts, f.closed_by = 'retracted', "
            "    f.closed_session = $sid",
            eid=best_eid, ts=timestamp, sid=session_id,
        )
        log.info("retracted (embedding, sim=%.3f, pred=%s): %s/%s owner=%s",
                 best_sim, best_pred, fact["subject"], fact["predicate"], owner)
        return True

    log.warning("retraction found no match: %s/%s owner=%s (best sim=%.3f)",
                fact["subject"], fact["predicate"], owner, best_sim)
    return False
```

### 8. write_facts: retractions first, then assertions

File: `harness/extraction_queue.py`

Replace the existing `write_facts` function. Retractions process before assertions so that "old fact is wrong / new fact is X" closes the old fact before the new one writes.

```python
def write_facts(facts: list[dict], *, owner: str, session_id: str,
                timestamp: str | None = None) -> int:
    """Process retractions and write assertions.

    Retractions: find and close matching active facts (no new nodes).
    Assertions: create new :Fact nodes (closing prior same-attribute facts).

    Retractions run first so that a transcript sequence of "old fact is wrong,
    new fact is X" closes the old fact before the new one writes.

    Returns the count of graph mutations (retractions applied + assertions written).
    """
    if not facts:
        return 0
    timestamp = timestamp or _now_iso()
    driver = _get_driver()
    mutations = 0

    retractions = [f for f in facts if f.get("type") == "retraction"]
    assertions = [f for f in facts if f.get("type", "assertion") == "assertion"]

    with driver.session() as sess:
        for fact in retractions:
            if sess.execute_write(_retract_one, fact, owner, session_id,
                                  timestamp):
                mutations += 1
        for fact in assertions:
            embedding = embed_text(_fact_text(fact))
            if sess.execute_write(_write_one, fact, owner, session_id,
                                  timestamp, embedding):
                mutations += 1
    return mutations
```

### 9. _parse_retraction_markers

File: `harness/extraction_queue.py`

New function. Add near `process_session`:

```python
def _parse_retraction_markers(turns: list[dict]) -> list[dict]:
    """Extract structured retraction facts from [CONFIRMED_RETRACTION] markers.

    These are deterministic (no LLM involved). The marker format is:
    {"role": "system", "content": "[CONFIRMED_RETRACTION] subject|predicate|object"}

    Pipe-delimited for simplicity. If object text contains a pipe character,
    only the first two pipes are split boundaries (maxsplit=2).
    """
    retractions = []
    for t in turns:
        if t.get("role") != "system":
            continue
        content = t.get("content", "")
        if not content.startswith("[CONFIRMED_RETRACTION] "):
            continue
        payload = content[len("[CONFIRMED_RETRACTION] "):]
        parts = payload.split("|", 2)
        if len(parts) == 3:
            retractions.append({
                "type": "retraction",
                "subject": parts[0].strip(),
                "predicate": parts[1].strip(),
                "object": parts[2].strip(),
                "confidence": "high",
            })
    return retractions
```

### 10. process_session: markers first, then LLM

File: `harness/extraction_queue.py`

Replace the existing `process_session` function:

```python
def process_session(session_id: str, turns: list[dict], owner: str) -> list[dict]:
    """Extract facts from one session's turns and write them to Neo4j.

    Two-stage extraction:
    1. Deterministic: parse [CONFIRMED_RETRACTION] markers from transcript.
    2. LLM: run extraction prompt over the transcript (markers filtered out).

    Marker retractions take priority. Any LLM-extracted assertion whose
    subject+predicate matches a marker retraction is dropped (the user already
    denied that fact). LLM-detected retractions that duplicate a marker are
    also dropped.
    """
    member = get_member_by_id(owner)
    owner_name = member["name"] if member else None

    # 1. Deterministic retraction markers (no LLM)
    marker_retractions = _parse_retraction_markers(turns)

    # 2. LLM extraction (filter out marker turns before sending)
    llm_turns = [t for t in turns if not (
        t.get("role") == "system"
        and t.get("content", "").startswith("[CONFIRMED_RETRACTION]")
    )]
    llm_facts = extract_facts(llm_turns, owner_name=owner_name)

    # 3. Merge: markers take priority
    marker_keys = {(r["subject"].lower(), r["predicate"].lower())
                   for r in marker_retractions}
    # Drop LLM assertions that markers already retracted,
    # and LLM retractions that duplicate markers.
    filtered_llm = [
        f for f in llm_facts
        if (f["subject"].lower(), f["predicate"].lower()) not in marker_keys
    ]
    all_facts = marker_retractions + filtered_llm

    written = write_facts(all_facts, owner=owner, session_id=session_id) if all_facts else 0
    log.info("session %s (owner=%s name=%r): markers=%d, llm=%d, wrote=%d",
             session_id, owner, owner_name,
             len(marker_retractions), len(llm_facts), written)
    return all_facts
```

### 11. Read path: valid_to IS NULL

File: `harness/extraction_queue.py`

**read_user_facts**: change the WHERE clause:

```
# Old:
"MATCH (f:Fact) WHERE f.superseded = false "

# New:
"MATCH (f:Fact) WHERE f.valid_to IS NULL "
```

The rest of `read_user_facts` is unchanged. It still decrypts `ciphertext` and returns `{subject, predicate, object, confidence}`. The external shape is the same.

**search_facts_by_embedding**: change the WHERE clause:

```
# Old:
"MATCH (f:Fact) WHERE coalesce(f.superseded, false) = false "

# New:
"MATCH (f:Fact) WHERE f.valid_to IS NULL "
```

**Grep for any other references:**

```bash
grep -rn "superseded" harness/ server/ scripts/ --include="*.py"
```

Update any remaining Cypher queries that filter on `superseded` to use `valid_to IS NULL`.

### 12. Retraction marker injection in voice_orch.py

File: `server/voice_orch.py`

**INVESTIGATION STEP (do this first):**

The marker must appear in the `turns` list that `enqueue_session_end` passes to `process_session`. Trace the data path:

```bash
grep -n "enqueue_session_end\|SessionMemory\|context(max_turns\|_messages" server/voice_orch.py
```

Determine which data structure holds the session transcript that the extraction pipeline receives. Options:

- A `SessionMemory` object with a `.context()` method
- `self._ctx._messages` (the Pipecat LLMContext)
- A separate transcript buffer

**The marker must be appended to the extraction transcript source, NOT to the live LLM context, unless they are the same object.** If `_ctx._messages` feeds both the live LLM and the extraction pipeline, appending there is acceptable for the prototype, but note it as tech debt: internal markers should not be visible to the live LLM.

If a separate transcript buffer exists, append there. If `_ctx._messages` is the only source, append there and accept the prototype limitation.

**IMPLEMENTATION:**

In the contradiction confirmation block (around line 975), after `self._suppressed_facts.update(new_suppressed)`:

```python
if new_suppressed:
    self._suppressed_facts.update(new_suppressed)
    logger.info(
        f"[contradiction] suppressing {len(new_suppressed)} fact(s) "
        f"mid-session: {new_suppressed}")

    # Append structured retraction markers to the session transcript.
    # The extraction pipeline processes these deterministically.
    for subj, pred in new_suppressed:
        # Recover the object value from the facts loaded on the
        # challenged turn.
        obj_value = ""
        for f in self._contradiction_facts:
            if (f.get("subject", "").lower() == subj
                    and f.get("predicate", "").lower() == pred):
                obj_value = f.get("object", "")
                break
        marker = {
            "role": "system",
            "content": (
                f"[CONFIRMED_RETRACTION] {subj}|{pred}|{obj_value}"
            ),
        }
        # APPEND TO THE EXTRACTION TRANSCRIPT SOURCE.
        # Replace <TRANSCRIPT_TARGET> with the actual list identified
        # in the investigation step above.
        <TRANSCRIPT_TARGET>.append(marker)
```

### 13. demo_seed.py and demo_reset.py

**demo_seed.py**: No changes. It calls `write_facts`, which now uses temporal schema.

**demo_reset.py**: Verify it deletes all :Fact nodes entirely (DETACH DELETE). If it only sets `superseded = true`, change to DETACH DELETE. Check:

```bash
grep -n "superseded\|DETACH DELETE\|DELETE" scripts/demo_reset.py
```

## File Summary

| File | Change |
|---|---|
| harness/extraction_queue.py | RETRACTION_THRESHOLD, _MEDICAL_KEYWORDS, EXTRACTION_PROMPT rewrite, _coerce_fact (type + sensitivity floor), _write_one (temporal), _retract_one (new), write_facts (retractions first), _parse_retraction_markers (new), process_session (two-stage), read_user_facts filter, search_facts_by_embedding filter |
| server/voice_orch.py | Append structured retraction marker to extraction transcript on contradiction confirmation (~line 975). Investigation step required to identify correct append target. No Neo4j writes. |
| scripts/migrate_temporal.py | New file. One-time migration from superseded to valid_from/valid_to. |
| scripts/demo_reset.py | Verify DETACH DELETE (likely no change). |

Files NOT changed: harness/orchestrator.py, scripts/demo_seed.py.

## Testing

### Test 1: Migration

```bash
python scripts/migrate_temporal.py --dry-run
# Review counts, then:
python scripts/migrate_temporal.py
```

Verify:
```bash
python3 -c "
from neo4j import GraphDatabase; import os
d = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', os.environ.get('NEO4J_PASSWORD','')))
with d.session() as s:
    for row in s.run('MATCH (f:Fact) RETURN f.valid_from IS NOT NULL AS migrated, f.superseded IS NOT NULL AS old_schema, count(*) AS n'):
        print(dict(row))
d.close()
"
# Expected: migrated=True, old_schema=False for all facts
```

### Test 2: Retraction via write_facts (unit)

```bash
python scripts/demo_reset.py --yes
python scripts/demo_seed.py

# Verify atorvastatin is active
python3 -c "
from harness.extraction_queue import read_user_facts
for f in read_user_facts('bill'):
    print(f'{f[\"subject\"]} {f[\"predicate\"]}: {f[\"object\"]}')
"
# Expected: Bill takes: atorvastatin 20mg daily

# Retract
python3 -c "
from harness.extraction_queue import write_facts
result = write_facts([
    {'type': 'retraction', 'subject': 'Bill', 'predicate': 'takes',
     'object': 'atorvastatin 20mg daily', 'confidence': 'high'}
], owner='bill', session_id='test-retract')
print(f'mutations: {result}')
"
# Expected: mutations: 1

# Verify gone
python3 -c "
from harness.extraction_queue import read_user_facts
for f in read_user_facts('bill'):
    print(f'{f[\"subject\"]} {f[\"predicate\"]}: {f[\"object\"]}')
"
# Expected: coffee and household only, no atorvastatin

# Verify audit trail
python3 -c "
from neo4j import GraphDatabase; import os
d = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', os.environ.get('NEO4J_PASSWORD','')))
with d.session() as s:
    for row in s.run(
        \"MATCH (f:Fact {subject: 'Bill', predicate: 'takes', owner: 'bill'}) \"
        \"RETURN f.valid_from, f.valid_to, f.closed_by, f.closed_session\"):
        print(dict(row))
d.close()
"
# Expected: valid_to set, closed_by='retracted', closed_session='test-retract'
```

### Test 3: Extraction prompt (unit)

```bash
python3 -c "
from harness.extraction_queue import extract_facts
turns = [
    {'role': 'user', 'content': 'What medication do I take?'},
    {'role': 'assistant', 'content': 'You take atorvastatin 20mg daily.'},
    {'role': 'user', 'content': 'I do not take any medication.'},
    {'role': 'assistant', 'content': 'Actually, I have on file that you take atorvastatin 20mg daily. Has that changed?'},
    {'role': 'user', 'content': 'Yes.'},
    {'role': 'assistant', 'content': 'Understood. I have noted that change.'},
]
facts = extract_facts(turns, owner_name='Bill')
for f in facts:
    print(f)
"
# Expected: at least one dict with type='retraction'
# If 7B fails, add few-shot examples or route extraction through Groq 70b
```

### Test 4: Marker parsing (unit)

```bash
python3 -c "
from harness.extraction_queue import _parse_retraction_markers
turns = [
    {'role': 'user', 'content': 'What medication do I take?'},
    {'role': 'assistant', 'content': 'You take atorvastatin 20mg daily.'},
    {'role': 'system', 'content': '[CONFIRMED_RETRACTION] Bill|takes|atorvastatin 20mg daily'},
    {'role': 'user', 'content': 'Thanks.'},
]
markers = _parse_retraction_markers(turns)
for m in markers:
    print(m)
"
# Expected: {'type': 'retraction', 'subject': 'Bill', 'predicate': 'takes',
#            'object': 'atorvastatin 20mg daily', 'confidence': 'high'}
```

### Test 5: process_session with markers (unit)

```bash
python scripts/demo_reset.py --yes
python scripts/demo_seed.py

python3 -c "
from harness.extraction_queue import process_session
turns = [
    {'role': 'user', 'content': 'What medication do I take?'},
    {'role': 'assistant', 'content': 'You take atorvastatin 20mg daily.'},
    {'role': 'user', 'content': 'I do not take any medication.'},
    {'role': 'assistant', 'content': 'Actually, I have on file that you take atorvastatin 20mg daily. Has that changed?'},
    {'role': 'user', 'content': 'Yes.'},
    {'role': 'assistant', 'content': 'Understood.'},
    {'role': 'system', 'content': '[CONFIRMED_RETRACTION] Bill|takes|atorvastatin 20mg daily'},
]
result = process_session('test-session', turns, 'bill')
print('Extracted:', result)
"

# Verify atorvastatin is closed
python3 -c "
from harness.extraction_queue import read_user_facts
for f in read_user_facts('bill'):
    print(f'{f[\"subject\"]} {f[\"predicate\"]}: {f[\"object\"]}')
"
# Expected: no atorvastatin
```

### Test 6: read_user_facts shape (unit)

```bash
python3 -c "
from harness.extraction_queue import read_user_facts
facts = read_user_facts('bill')
for f in facts:
    assert 'object' in f, f'Missing object key: {f}'
    assert 'subject' in f, f'Missing subject key: {f}'
    assert 'predicate' in f, f'Missing predicate key: {f}'
    assert 'confidence' in f, f'Missing confidence key: {f}'
    print(f'OK: {f[\"subject\"]} {f[\"predicate\"]}: {f[\"object\"]}')
print('Shape test passed.')
"
```

### Test 7: Marker plumbing (integration)

This test verifies the marker appended by voice_orch.py actually reaches process_session. Run AFTER the investigation step and marker wiring (step 12).

1. Start voice server
2. Trigger a contradiction (seed atorvastatin, deny it, confirm)
3. End the session
4. Check the extraction queue log for "markers=1":

```bash
grep "markers=" logs/voice_orch.log
# Expected: session <id> (owner=bill name='Bill'): markers=1, llm=N, wrote=M
```

If markers=0, the append target is wrong. Re-trace the transcript data path.

### Test 8: Full voice loop (integration)

1. `python scripts/demo_reset.py --yes && python scripts/demo_seed.py`
2. Clear logs
3. Start voice server
4. "What medication do I take?" -- answers atorvastatin
5. "I don't take any medication"
6. LLM challenges, user confirms
7. "What medication do I take?" -- says unknown (in-memory suppression)
8. End session. Wait for extraction queue to drain.
9. Restart voice server
10. "What medication do I take?" -- STILL says unknown (persistent retraction)

Step 10 is the regression.

### Test 9: Neo4j audit after voice test

```bash
python3 -c "
from neo4j import GraphDatabase; import os
d = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', os.environ.get('NEO4J_PASSWORD','')))
with d.session() as s:
    for row in s.run('MATCH (f:Fact {owner: \"bill\"}) RETURN f.subject, f.predicate, f.valid_from, f.valid_to, f.closed_by ORDER BY f.timestamp'):
        print(dict(row))
d.close()
"
# Expected: Bill/takes has valid_to set, closed_by='retracted'
# Bill/prefers has valid_to null (still active)
```

## Risks

**7B extraction quality.** The structured marker is the primary retraction path and does not depend on LLM quality. The prompt-based retraction detection is a fallback. If 7B cannot handle it, that fallback degrades gracefully.

**Embedding threshold.** RETRACTION_THRESHOLD at 0.90 may be too tight for near-miss predicates. The exact match fires first and handles the common case. Log near-misses to tune.

**Marker injection target.** The investigation step in section 12 is mandatory. Do not guess. Trace the data path from voice_orch through enqueue_session_end to process_session and identify the exact list. If the marker does not reach process_session, the deterministic path is dead and you are fully dependent on the 7B fallback.

**Session-end timing.** If the voice server crashes before session end, the retraction is lost. This is the existing TD-029 gap. Not made worse by this change.

## Demo Outcome

1. Seed fact: Bill takes atorvastatin.
2. HIP answers using that fact.
3. Bill corrects HIP.
4. HIP suppresses it immediately (hot cache).
5. Session ends. Extraction closes the fact with valid_to set.
6. Restart HIP.
7. HIP no longer retrieves the retracted fact.
8. Closed fact remains auditable in Neo4j with temporal history.

That demonstrates the pipes, the architecture, and the privacy-first memory lifecycle.
