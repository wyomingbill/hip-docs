<!-- STATUS: IN_PROGRESS -->
<!-- RECONCILED-AGAINST: server/voice_orch.py:110-111 (handle_reconsider, handle_frontier_request imported and called at lines 1443, 1467, 2150, 2165); harness/control_flow.py header ("scaffold, NOT wired" — contradicted by live imports; wiring is done, full fidelity unknown) — 2026-07-05 -->

# Control Flow — RECONSIDER and FRONTIER_REQUEST

Phase 2 design document. Describes the state machine, session-state schema,
and auditable-privacy invariants for the two non-standard query paths introduced
by the Phase 1 control classifier (`harness/control_classifier.py`).

This document is the authoritative spec. The stub module (`harness/control_flow.py`)
is the code skeleton. Neither is wired into the live voice pipeline until Phase 3.

---

## 0. Background: the three buckets

`harness/control_classifier.py` → `classify_control(query)` returns one of:

| Label | Meaning |
|---|---|
| `NEW_QUERY` | Ordinary content question — route normally via `Router.route()`. |
| `RECONSIDER` | User pushes back on the *current* answer. Stay on-net, try harder. |
| `FRONTIER_REQUEST` | Explicit ask to leave the device. Requires a codeword to proceed. |

`NEW_QUERY` is the pass-through default and not described further here.

---

## 1. Tier model recap

On-net tiers (all local, all private):

```
EDGE  — trivial / short queries; lightest model config
MID   — moderate queries; the common voice turn
CORE  — complex multi-step; max on-net capability
```

Off-net:

```
ESCALATE — frontier backend (Claude, or whatever config.yaml points to)
```

RECONSIDER navigates EDGE/MID/CORE. FRONTIER_REQUEST is the only legal path
to ESCALATE. These two control paths are structurally separate and MUST remain
so (see §5, Invariants).

---

## 2. RECONSIDER — state machine

### 2.1 Purpose

The user isn't satisfied with the current answer. They're not asking to leave
the device — they want the device to try harder. The system re-runs the
*previous* query at the next on-net capability tier.

### 2.2 Tier progression

```
prev_tier → reconsider_tier
──────────────────────────────
EDGE      → MID
MID       → CORE
CORE      → CORE  (ceiling; announce "giving you my best local answer")
```

At CORE the system is already at maximum on-net capability. It re-runs the
query at CORE once more (the model may produce a better answer with a slightly
different prompt path) and then announces the limit. It does NOT offer the
frontier; that is the user's choice to initiate separately with a
FRONTIER_REQUEST.

### 2.3 State transitions

```
[IDLE]
   │
   │  turn N completes (any NEW_QUERY or RECONSIDER turn)
   ▼
[TURN_STORED]   ← prev_query, prev_tier, prev_answer, prev_sensitivity all set
   │
   │  classify_control(turn N+1) == RECONSIDER
   ▼
[RECONSIDER_ACTIVE]
   │
   ├─ prev_tier == EDGE  → route at MID   → answer → announce "trying at mid tier"
   ├─ prev_tier == MID   → route at CORE  → answer → announce "going deeper"
   └─ prev_tier == CORE  → route at CORE  → answer → announce "that's my best local answer"
   │
   ▼
[TURN_STORED]   ← update prev_* with this turn's result (query=prev_query, new tier)
```

### 2.4 What "route at tier X" means

`handle_reconsider()` in `control_flow.py` sets `RouteDecision.tier` to the
target tier and calls the orchestrator's `_decide_and_route()` with that
decision pre-made, bypassing the normal `Router.route()` call. The local model
is called with the same query, same context, same injected facts — only the
tier (which may affect model config, prompt length, temperature, etc.) changes.

### 2.5 RECONSIDER with no prior turn

If `TurnSessionState.prev_query` is `None` (first turn of a session, or session
was just wiped), `handle_reconsider()` returns a `ControlFlowResult` with
`action="decline"` and `spoken_response="I don't have a previous answer to
reconsider."` No query is re-run.

---

## 3. FRONTIER_REQUEST — state machine

### 3.1 Purpose

The user explicitly asks to cross off-net (e.g., "use the frontier", "go
online", "check the web"). This is a deliberate, user-initiated privacy
crossing. It is gated behind a codeword to prevent accidental or coerced
off-net dispatch.

### 3.2 Full gate sequence

```
classify_control(query) == FRONTIER_REQUEST
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Step 1 — Sensitivity check                                  │
  │                                                              │
  │  Is the CURRENT query (or any retrieved fact it references)  │
  │  sensitive? (reuse router._is_query_sensitive + prev_sens)   │
  │                                                              │
  │   YES ──► emit spoken confirmation request:                  │
  │           "This query is sensitive. Answering it will send   │
  │            information off your home network. Confirm?"      │
  │           → set frontier_confirm_pending = True              │
  │           → return ControlFlowResult(action="confirm_needed")│
  │                                                              │
  │   NO  ──► continue to Step 2                                 │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼  (next user turn while frontier_confirm_pending == True)
  ┌──────────────────────────────────────────────────────────────┐
  │  Step 1b — Confirm/decline resolution                        │
  │                                                              │
  │  classify_control(user_response):                            │
  │   RECONSIDER or explicit decline signal ──► stay_local       │
  │           → frontier_confirm_pending = False                 │
  │           → route original query as NEW_QUERY at prev_tier   │
  │                                                              │
  │  Explicit confirm ("yes", "go ahead", "confirm"):            │
  │   → frontier_confirm_pending = False                         │
  │   → continue to Step 2                                       │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Step 2 — Codeword check                                     │
  │                                                              │
  │  Does the utterance contain HIP_FRONTIER_CODEWORD            │
  │  (read from env, never hardcoded)?                           │
  │                                                              │
  │   YES ──► continue to Step 3                                 │
  │                                                              │
  │   NO  ──► return ControlFlowResult(action="stay_local")      │
  │           spoken: "I need the codeword to go off-device."    │
  │           → route as NEW_QUERY (best local answer)           │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Step 3 — Log + cross                                        │
  │                                                              │
  │  1. log_frontier_authorized_event(session_id, query_hash,    │
  │       tier="escalate", sensitivity_tag)                      │
  │     → writes FRONTIER_AUTHORIZED record to routing telemetry │
  │                                                              │
  │  2. strip_context_for_tier(messages, "frontier", query)      │
  │     → drops all context; sends only bare query off-net       │
  │                                                              │
  │  3. announce: "Sending that off-device now."                 │
  │                                                              │
  │  4. dispatch to TIER_ESCALATE (frontier backend)             │
  │                                                              │
  │  5. return ControlFlowResult(action="frontier_cross",        │
  │       tier=TIER_ESCALATE, audit_event="FRONTIER_AUTHORIZED") │
  └──────────────────────────────────────────────────────────────┘
```

### 3.3 Codeword extraction

The codeword is matched against the full utterance text (not the post-stripped
query). The match is case-insensitive; the check uses `hmac.compare_digest` to
be constant-time against timing side-channels. The codeword is read once at
module import from `os.environ["HIP_FRONTIER_CODEWORD"]`; a missing env var
raises `RuntimeError` at import time (fail-loud, not fail-open).

### 3.4 Query sensitivity for FRONTIER_REQUEST

Sensitivity is the union of:
- `router._is_query_sensitive(query)` on the frontier-request utterance itself
- `prev_sensitivity` from `TurnSessionState` (the preceding turn's sensitivity,
  which may reflect injected high-sensitivity facts)

If either is `"high"` or `"medium"`, Step 1 fires the confirmation prompt.
`"low"` on both skips directly to the codeword check.

---

## 4. Session state — where and how

### 4.1 `TurnSessionState` dataclass (defined in `harness/control_flow.py`)

```python
@dataclass
class TurnSessionState:
    prev_query:              str | None = None
    prev_tier:               str | None = None   # TIER_EDGE / MID / CORE
    prev_answer:             str | None = None
    prev_sensitivity:        str | None = None   # "low" / "medium" / "high"
    frontier_confirm_pending: bool = False
```

### 4.2 Storage location

`TurnSessionState` is stored as a new attribute `control_state` on each
`SessionMemory` instance in `harness/session_memory.py`. This keeps per-session
mutable control state co-located with the per-session transcript, under the
same `threading.Lock`.

Concretely (Phase 3 wiring, not done yet):

```python
# In SessionMemory.__init__:
self.control_state = TurnSessionState()
```

`SessionMemoryStore.get_or_create()` already returns a per-session
`SessionMemory`; callers that need `control_state` access it as
`mem.control_state`.

### 4.3 Update discipline

`TurnSessionState` is updated by the orchestrator *after* a turn completes
successfully (answer generated and spoken), not before. This prevents a failed
or interrupted turn from clobbering the previous good state.

Update fields:

| Event | Fields updated |
|---|---|
| NEW_QUERY turn completes | `prev_query`, `prev_tier`, `prev_answer`, `prev_sensitivity` |
| RECONSIDER turn completes | same four (query stays the same as original; tier is the new tier) |
| FRONTIER_REQUEST crosses off-net | all four; `frontier_confirm_pending = False` |
| FRONTIER_REQUEST stays local (no codeword / decline) | `frontier_confirm_pending = False`; prev_* unchanged |
| Session starts | all fields at their `None`/`False` defaults |
| Session ends (store.remove) | discarded with the session |

### 4.4 Persistence

`TurnSessionState` is intentionally ephemeral — in-process only, no disk
write, no Neo4j write. The `prev_query` and `prev_answer` are not persisted
across sessions. This is a deliberate privacy choice: a guest or household
member's prior turn is not written to durable storage via this path (durable
memory happens through the extraction queue and is owner-scoped).

---

## 5. Hard invariants (enforced in code, documented here)

### INV-1: RECONSIDER NEVER crosses off-net

`handle_reconsider()` MUST NOT:
- Return a `ControlFlowResult` with `tier == TIER_ESCALATE`
- Call the frontier backend (escalation_backends.py)
- Call `log_frontier_authorized_event()`
- Read or check `HIP_FRONTIER_CODEWORD`

If `_next_reconsider_tier()` ever returns `TIER_ESCALATE`, that is a bug.
The function contains a runtime assertion:

```python
assert result != TIER_ESCALATE, "INV-1: reconsider tier must never be ESCALATE"
```

The CORE ceiling is the on-net hard stop. At CORE the system announces its
limit and returns the best local answer. It does not offer or hint at the
frontier. The user may independently issue a FRONTIER_REQUEST.

### INV-2: No off-net dispatch without a FRONTIER_AUTHORIZED log event

The only legal call site for the frontier backend is `handle_frontier_request()`
inside `control_flow.py`, and only after `log_frontier_authorized_event()` has
been called successfully. The log call is not optional and is not skippable by
any configuration.

`FRONTIER_AUTHORIZED` records are written to the routing telemetry log
(`harness/routing_telemetry.py`) with fields:
- `event: "FRONTIER_AUTHORIZED"`
- `session_id`
- `query_hash` (SHA-256 of the stripped query, NOT the raw query with context)
- `sensitivity_tag`
- `timestamp`

### INV-3: Separate code paths, no shared dispatch

RECONSIDER and FRONTIER_REQUEST are handled by two separate entry-point
functions (`handle_reconsider`, `handle_frontier_request`) that share no code
path to the frontier backend. The orchestrator calls one XOR the other based on
`classify_control()` output. There is no "escalate from reconsider" shortcut.

### INV-4: Codeword is never hardcoded

`HIP_FRONTIER_CODEWORD` is read from `os.environ` only. It must not appear as
a literal string in any source file, log, or test fixture. Tests that need a
codeword use `monkeypatch.setenv("HIP_FRONTIER_CODEWORD", "test-word")`.

### INV-5: Context is stripped before any off-net dispatch

`strip_context_for_tier(messages, "frontier", query)` (already implemented in
`harness/orchestrator.py`) is called before dispatching to the frontier backend.
The frontier model receives only the bare query — no injected facts, no
conversation history, no system prompt with personal information.

---

## 6. Hook points (not yet wired — Phase 3)

```
Voice pipeline (server/voice_orch.py or voice_https_orch.py)
  └─ per-turn handler
       │
       ├─ classify_control(transcript)           ← already available
       │
       ├─ if NEW_QUERY:
       │    orchestrator.handle_turn(...)         ← existing path, unchanged
       │
       ├─ if RECONSIDER:
       │    control_flow.handle_reconsider(       ← new
       │        session_state=mem.control_state,
       │        session_id=session_id,
       │    )
       │
       └─ if FRONTIER_REQUEST (or pending confirm):
            control_flow.handle_frontier_request( ← new
                query=transcript,
                session_state=mem.control_state,
                session_id=session_id,
                sensitivity_tag=...,
                codeword=_extract_codeword(transcript),
            )
```

The orchestrator's `_decide_and_route()` method is the internal path that both
handlers will call with a pre-computed `RouteDecision`. No changes to
`Router.route()` are required.

---

## 7. Out of scope (not Phase 2)

- Automatic RECONSIDER retry on low satisfaction score (satisfaction.py) — would
  require wiring the satisfaction classifier output back into the control path.
- Multi-turn FRONTIER_REQUEST confirmation dialog beyond one confirm/decline — the
  current model keeps the pending flag for exactly one follow-up turn.
- FRONTIER_REQUEST with a partially-redacted query — stripping happens at the
  frontier backend boundary, not mid-query.
- Per-member codeword differentiation — one household codeword, env-var backed.
