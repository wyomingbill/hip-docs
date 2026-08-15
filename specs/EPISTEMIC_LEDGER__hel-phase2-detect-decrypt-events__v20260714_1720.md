# HEL Phase 2: fact.detect and value.decrypt Events
Status: PLAN
Reconciled-Against: 990dfe6 (HEL Phase 1 built at a637fa4; code read 2026-07-14)
Date: 2026-07-14 17:20 MT
Scope: SPEC ONLY. No build. Amends HEL base spec (262dc9b + OQ-1 + OQ-2
6b70121). Defines the two Phase 2/3 events the base spec reserved.

---

## 0. What Phase 1 Delivered and What This Closes

Phase 1 (a637fa4) built `harness/epistemic_ledger.py`: hash-chained
segmented JSONL, per-event F_FULLFSYNC, per-member payload encryption with
crypto-shredding, `verify()`, and dual-write of `turn.record` from
`log_epistemic_record()`. One event type is live.

Two audit gaps remain open, both named in the base spec's M-6:

- **Detection outcomes are invisible in the canonical record.** A
  `turn.record` with `writes_pending: true` is never terminated. The P2
  false-negative class (DIAG v20260714_1500, harness item i019) was only
  detectable via a 45-second poll ceiling, and the same run logged 29
  `detect_no_result`/`detect_no_changes` entries in `write_latency.jsonl`
  with only an `iter` tag — no turn_id, no way to say WHICH turn's write
  silently died. An auditor cannot distinguish "the member said nothing
  writable" from "the detector dropped it."

- **Plaintext exposure is unlogged.** `/api/decrypt`
  (demo_dashboard.py:187) decrypts any fact value for any caller — no
  auth (TD-101b), no record. The single most audit-worthy action in HIP
  currently leaves no trace anywhere.

This spec defines `fact.detect` and `value.decrypt`: schema, emit sites,
correlation, ordering, and the diligence claim each unlocks. It also fixes
the two code-level preconditions found in the reconciliation read (§1.3,
§2.2) without which the events cannot be correlated at all.

---

## 1. fact.detect — Detection Outcome as an Auditable Fact

### 1.1 The event

One `fact.detect` event per completed `detect_and_apply()` invocation —
including the failure paths. "The detector ran and found nothing" and
"the detector never answered" become distinct, durable, turn-joined facts.

```json
{
  "hel": "1.0", "seq": …, "event_id": "uuid4",
  "event_type": "fact.detect",
  "ts": "…",
  "actor": {"kind": "system", "id": "fact_change"},
  "correlation": {
    "turn_id": "<the turn that fired detection>",
    "session_id": "…",
    "fact_ids": ["<every fact_id touched by this cycle>"]
  },
  "payload": {
    "outcome": "committed | no_changes | no_result | error | skipped",
    "proposed": 3, "mutations": 2, "noops": 1, "parked": 0,
    "delta": [ {"fact_id": "…", "attribute": "…", "state": "supersede",
                "prior_fact_id": "…"} ],
    "park": {"parked_fact_id": "…", "prior_fact_id": "…",
             "transition": "…"} ,
    "owner": "ray",
    "utterance_sha256": "sha256:…",
    "model_id": "llama-3.3-70b-versatile",
    "latency_ms": {"total": 1840, "groq": 1620},
    "sync": true
  },
  "payload_kid": "member:<owner>", "payload_sha256": "…",
  "prev_hash": "…", "hash": "…"
}
```

Field decisions:

- **`outcome`** is the load-bearing field. Five terminal states:
  - `committed` — ≥1 mutation applied (mutations count says how many).
  - `no_changes` — Groq answered with an empty changes list. Honest
    negative: the model looked and found nothing.
  - `no_result` — the Groq call failed or timed out. THIS is the P2/i019
    class: the write may have been warranted and nobody looked. Making
    `no_result` a first-class outcome in the canonical chain is the whole
    point of the event.
  - `error` — `_apply_changes` raised (changes were proposed, application
    failed). Distinct from `no_result`: the model answered, the engine
    dropped it.
  - `skipped` — the pre-gates declined to run detection (utterance < 4
    words, question form). Emitted so that "writes_pending was never set"
    and "detection was gated off" are distinguishable. See §1.4 for why
    this outcome does NOT need an event in v1 (the turn.record already
    encodes it) — the value is schema-reserved.
- **`delta` / `park`** reuse `_project_write_record()`'s existing
  projection — the exact structure already in the d1.1 write block, values
  already stripped (TD-030). No new projection code, no drift between what
  the turn record shows and what the detect event shows.
- **`utterance_sha256`**, not the utterance. The turn.record already
  carries the query verbatim (encrypted under the member key); repeating
  it here doubles the PII surface for zero audit value. The hash lets an
  auditor confirm the detect event processed the same utterance as the
  turn it claims, without a second plaintext copy.
- **`actor` is system, not member** — detection is an engine action on
  the member's behalf. But `payload_kid` is the member's key anyway (see
  below): the payload names the member's facts and attributes, so it is
  member PII and must die with the member's crypto-shred.

  **Writer change this requires:** Phase 1's `_build_event()` selects
  encryption solely by `actor.kind == "member"`. Phase 2 adds an explicit
  override: `append(..., encrypt_for="<member_id>")` — encrypt the payload
  under that member's key regardless of actor kind. `fact.detect` passes
  `encrypt_for=owner`. This is also the mechanism `value.decrypt` needs
  (§2.4), so it ships once, in the writer, with both events using it.
- **`sync`** — true when detection ran synchronously in the turn (Seam A
  declarative path), false when fired post-reply. Lets Projection 3 pick
  the right timeout expectation per mode.

### 1.2 Emit site

Terminal lines of `detect_and_apply()` (fact_change.py) — exactly where
`_store_outcome()` + `_write_lat_record()` already sit. Three call points:

1. the `no_result` early return (~line 880),
2. the `no_changes` early return (~line 893),
3. the end of the main path after `_store_outcome(...)` (~line 915),
   with `outcome` = `committed` if mutations else (`error` if
   `_apply_changes` raised else `no_changes` — note a proposed-but-all-noop
   cycle is `no_changes` with `proposed > 0`, distinguishable by counts).

The emit is `epistemic_ledger.append(...)` — never-raise, so the
detection thread's behavior is unchanged on any ledger failure.
`write_latency.jsonl` keeps writing (DIAG-1 is measurement
instrumentation, not audit; it is not consolidated here).

### 1.3 The correlation precondition — turn_id must exist before detection

**Finding (code read, voice_orch.py):** `_turn_id = new_turn_id()` is
minted at line 2645 — AFTER the Seam A synchronous
`detect_and_apply_async()` fires at ~2626. On the declarative path, the
detection cycle starts before its turn has an identity. As built, the
event cannot carry the one field that justifies its existence.

**Required change (behavior-neutral, Phase 2 gate item):** hoist
`_turn_id = new_turn_id()` above the Seam A block. `new_turn_id()` is a
pure ID mint (turn_metadata.py); moving it earlier changes no governance
behavior. Then plumb it through:

- `detect_and_apply_async(..., turn_id: str | None = None)` →
  `detect_and_apply(..., turn_id=...)` — an explicit parameter, NOT a
  module-global tag. The existing `set_iteration_tag()` pattern is a
  race-prone workaround (pop-once global across threads) tolerated for
  harness instrumentation; the canonical record does not inherit it.
- All six call sites (voice_orch ×5, realtime_adapter ×1) pass the turn's
  id. The realtime_adapter path and any caller without a turn id pass
  None; the event is still emitted with `turn_id: null` — an honestly
  uncorrelated detection beats a dropped event.

### 1.4 How writes_pending is terminated

`writes_pending` on the turn.record stays exactly as built — this spec
does not touch the d1.1 schema (D-1's byte-compat guarantee is absolute).
Termination is a JOIN, not a mutation:

> A `turn.record` with `writes_pending: true` is **closed** by the first
> `fact.detect` event whose `correlation.turn_id` matches. It is **open**
> until then. An open record older than `DETECT_SLA_S` (default 60 s,
> twice the harness poll ceiling that caught i019) is a **detection
> loss** — the P2 class, now visible by construction.

This is Projection 3 of the base spec (`open-writes check`), now fully
specifiable: implemented in `ledger_reader.py` as a pure fold over the
event stream, surfaced on the dashboard `/api/proof` health block as
`open_writes: n`. The ledger is append-only; nothing ever rewrites the
turn.record — the closed/open status is derived state, recomputable by
any auditor from the chain alone.

Ordering guarantees (both orders occur, both are valid):

- **Post-reply async path** (the common case): `turn.record` (seq n) …
  `fact.detect` (seq n+k). writes_pending: true, later closed.
- **Seam A synchronous path**: detection completes BEFORE the record is
  built, so `fact.detect` (seq m) precedes its `turn.record` (seq m+j),
  and the record carries `writes_pending: false` with the delta already
  in its write block. The join key is turn_id, not seq adjacency;
  Projection 3 must treat a detect-before-record pair as trivially
  closed. Global seq order remains the arbiter of ledger truth; per-turn
  event order is a property of the turn's execution mode, and the `sync`
  flag records which mode applied.

Idempotency: exactly one fact.detect per detection cycle. A retry
architecture (TD-124 outbox, future) would emit one event per attempt
with an `attempt` counter — schema-reserved, not built.

### 1.5 Diligence claim unlocked

> "Every write-relevant utterance has a durable, hash-chained record of
> what the detector concluded — including the times it concluded nothing
> and the times it failed to answer. Silent write loss is structurally
> impossible to hide: an unterminated writes_pending is visible in the
> canonical record by inspection, and the projection that finds them is
> a 20-line fold any auditor can re-run."

The i019 post-mortem question — "how many other turns lost writes and
nobody noticed?" — becomes answerable retroactively for the whole ledger
lifetime, not just for instrumented harness runs. The 29 uncorrelated
`detect_no_result/no_changes` entries of that run would each have been a
chained event with a turn_id.

---

## 2. value.decrypt — Every Plaintext Exposure, on the Record

### 2.1 Principle

The ledger records that a value was exposed — never the value. The event
is metadata about an act of disclosure to an operator surface: who asked,
which fact, whose fact, under what authority, from where, and whether the
system said yes. TD-030 applies with zero exceptions: no plaintext, no
ciphertext, no key material in the payload.

Logged-but-open beats open-and-unlogged: this event ships BEFORE the
TD-101b auth gate, with the authority block honestly recording that no
authentication was performed. When the gate lands, the same schema
records the mechanism — the event schema is auth-agnostic by design.

### 2.2 The endpoint precondition — the event must be able to name the fact

**Finding (code read, demo_dashboard.py:187):** the request body is
`{ciphertext, encrypted_dek, owner}` — the endpoint never learns the
fact_id. The dashboard HAS the fact_id (it renders the fact list from
`/api/facts`); it just doesn't send it.

**Required change (Phase 2 gate item):** `fact_id` becomes a required
body field. The dashboard fetch (~line 1107) adds it. An exposure record
that cannot name the exposed fact is decorative; requiring the field at
the API boundary is the only place the requirement is enforceable.
Requests without it are rejected 400 — and the rejection is ALSO logged
(a caller probing the decrypt surface without naming a fact is itself
audit-worthy).

### 2.3 The event

```json
{
  "hel": "1.0", "seq": …, "event_id": "uuid4",
  "event_type": "value.decrypt",
  "ts": "…",
  "actor": {"kind": "operator", "id": "dashboard"},
  "correlation": {
    "session_id": null,
    "fact_ids": ["<fact_id>"]
  },
  "payload": {
    "fact_id": "…",
    "subject_member": "ray",
    "requester": {"kind": "operator", "id": "dashboard",
                  "remote_addr": "192.168.1.20",
                  "user_agent_sha256": "sha256:…"},
    "authority": {"authenticated": false,
                  "mechanism": "none (TD-101b open)",
                  "authorized": true,
                  "basis": "operator-custodial dashboard, LAN-scoped"},
    "result": "ok | error | rejected",
    "error_kind": null,
    "surface": "/api/decrypt"
  },
  "payload_kid": null, "payload_sha256": "…",
  "prev_hash": "…", "hash": "…"
}
```

Field decisions:

- **who** — `requester`: actor kind + id, plus `remote_addr` (the LAN
  address is in-boundary operational metadata, not member PII) and a
  HASH of the user agent (fingerprint without the string). Today every
  caller is "the dashboard"; post-TD-101b the id becomes the
  authenticated principal.
- **what** — `fact_id` + `subject_member`. Attribute/subject text is
  deliberately ABSENT: the fact_id joins to the `fact.write` /
  `turn.record` events that already carry attribute metadata under the
  member's key. Repeating attribute names in this plaintext payload
  would leak fact-existence structure that crypto-shredding is supposed
  to kill. The join is the auditor's job; the ledger's job is not to
  pre-join it in the clear.
- **when** — envelope `ts` (F_FULLFSYNC'd before the plaintext leaves
  the handler — see ordering, §2.5).
- **under what authority** — the `authority` block. Pre-TD-101b it
  records `authenticated: false, mechanism: "none (TD-101b open)"` —
  the honest statement that the door was open. `authorized: true`
  reflects the current policy (operator-custodial surface, LAN-scoped),
  not an auth check. Post-gate: `mechanism: "bearer|mtls|session"`,
  and `authorized: false` events appear for denials.
- **from where** — `remote_addr` + `surface` (the endpoint path;
  future decrypt surfaces — a CLI tool, a support console — each name
  themselves).
- **result** — `ok`, `error` (decrypt raised: wrong key, corrupt
  ciphertext — `error_kind` carries the exception class name, never the
  message, which can embed data), `rejected` (missing fact_id, and
  post-TD-101b, auth denials).

### 2.4 Encryption decision: plaintext payload — exposure records survive the shred

The payload is deliberately NOT encrypted under the subject member's key
(`payload_kid: null`), unlike `fact.detect`. Reasoning, made explicit
because OQ-2 §10 deferred exactly this question:

- A `value.decrypt` event is a record of the OPERATOR's conduct — who
  looked at a member's data. Its accountability function must survive
  the member's departure. If it died with the member's key, an operator
  could erase the evidence of every exposure by processing the member's
  own erasure request — the record of "who saw Ray's data" would be
  destroyed BY Ray leaving, which inverts the protection.
- What remains after a crypto-shred is: fact_id (opaque), subject_member
  (identifier), requester, timestamps. Identifiers-not-values, the same
  residual class as the envelope's `actor.id` — already declared as
  HEL-ACTOR-1, resolved by registry-level opaque member IDs. This event
  adds no new residual category, it widens an existing declared one.
- 47 USC 551(f) private right of action and (h) governmental access
  provisions both presuppose that disclosure records OUTLIVE the
  subscriber relationship. Retaining exposure metadata past erasure is
  not a compliance defect; destroying it would be.

This asymmetry is now the rule, stated once: **content-bearing events
(turn.record, fact.detect, fact.write) encrypt under the subject's key
and die with it; conduct-bearing events (value.decrypt, system.note,
member.key_destroyed) stay plaintext-identifier and survive it.** New
event types must classify themselves against this rule at design time.

### 2.5 Emit site and ordering

`api_decrypt()` in demo_dashboard.py. The append is issued AFTER the
decrypt attempt resolves (so `result` is truthful) and BEFORE the
response is returned to the caller. Because Phase 1's `append()` is
F_FULLFSYNC-before-return, this extends D-1's write-ahead property to
exposures:

> **No plaintext leaves the system before the durable record of its
> exposure exists.**

Cost: one ledger append (~4 ms p50 on the Mini) on a dashboard-only
endpoint. No turn-path impact. The append is never-raise; a ledger
failure does not block the decrypt (the failure is counted and spooled
per M-2 — availability of the operator surface is preserved, the loss
is observable).

No ordering relationship with `turn.record` exists or is claimed:
decrypts are operator actions on their own timeline, joined to turns
only through the fact_id → `correlation.fact_ids` chain.

### 2.6 Interaction with per-member key erasure

Two directions:

- **Erasure does not erase exposure history** (§2.4): after
  `destroy_member_key(ray)`, every `value.decrypt` naming Ray's facts
  remains readable. The fact_ids they name now join to
  crypto-erased content events — the auditor sees "this fact was
  exposed to the dashboard on this date; its content is destroyed."
  That is the correct end state.
- **Decrypt-after-erasure is itself an event:** a decrypt attempt
  against a fact whose HEL trail is shredded still hits
  `harness/encryption.py`'s SEPARATE key scheme (fact DEKs are
  independent of ledger keys — OQ-2 §3.4). If graph-level erasure has
  destroyed the fact DEK, the attempt fails and lands as
  `result: "error"` — a durable record that someone tried to read
  erased data. If the fact DEK still exists (member erased from ledger
  but not from the graph — an inconsistent half-erasure), the decrypt
  SUCCEEDS and the event records a plaintext exposure of a
  ledger-erased member's data. That event is the alarm for the
  half-erasure state. Erasure runbooks (OQ-2 §6.2) must destroy BOTH
  key families; the value.decrypt trail is what proves whether they did.

### 2.7 Diligence claim unlocked

> "Every time a human saw a stored value in plaintext, there is a
> durable, tamper-evident record of who, which fact, when, from where,
> and under what authority — written before the plaintext was released,
> surviving the member's own erasure, on an endpoint that predates its
> own authentication gate. We can enumerate every exposure ever made
> through the governed surface."

This is the record a compliance reviewer asks for by name ("access log
for PHI disclosures") in HIPAA §164.312(b) audit-control terms, and the
one HIP currently cannot produce at all.

---

## 3. Phase Map Reconciliation

The base spec's Phase 2 bundled `fact.write` + `fact.detect` +
`system.reset`; Phase 3 was `value.decrypt`. Phase 1 as built (a637fa4)
already delivers the writer, encryption, and `system.note`/erasure
machinery, and OQ-2 landed `destroy_member_key`. This spec re-cuts the
remaining phases; the base spec's phase numbers are superseded as
follows:

- **Phase 2 (this spec): fact.detect + value.decrypt.** Preconditions
  folded in: turn_id hoist + parameter plumb (§1.3), fact_id in the
  decrypt body (§2.2), `encrypt_for` writer override (§1.1).
  *Gate:* full harness green; every `writes_pending: true` turn.record
  in an L2 run has a terminal fact.detect (Projection 3 returns
  `open_writes: 0` at run end); a manual dashboard decrypt produces
  exactly one value.decrypt event with `result: ok`; `verify()` green
  across the run's segments.
- **Phase 3: fact.write + system.reset** (moved from old Phase 2;
  unchanged in content: dual-write from store.py's `_append_audit` site,
  demo_reset emits `system.reset` and is forbidden from touching
  `ledger/` including `ledger/keys/` — OQ-2 §10). *Gate:* encode_audit ↔
  fact.write count parity; a reset appears in the chain.
- **Phase 4: consumers cut to projections** (unchanged).
- **Phase 5: turns_demo.jsonl demoted** — see §4.

## 4. Which Phase Demotes turns_demo.jsonl, and the Byte-Identity Proof

**Phase 5** (unchanged from the base spec) demotes `turns_demo.jsonl` to
a regenerable view: `demo_reset.py` may truncate it freely; HEL is
canonical; a rebuild command regenerates it on demand.

The proof of byte-identity is two-sided:

1. **Replay proof:** `scripts/replay_ledger.py --rebuild-demo-log`
   iterates `turn.record` events in seq order, decrypts each payload
   (member keys required), and writes each d1.1 dict as
   `json.dumps(record, default=str)` — the EXACT serialization in
   `log_epistemic_record()` today (same code path, factored to be
   importable by both writers, so the two can never drift). The Phase 5
   gate diffs the rebuilt file byte-for-byte against a live
   `turns_demo.jsonl` from the same run: `cmp` clean, or the phase does
   not land.
2. **Standing regression:** `scripts/check_bytecompat_d1.py` gains a
   `--from-ledger` mode comparing the ledger projection against the same
   shadow baselines that guard D-1 today. The byte-compat guarantee
   transfers from the file to the projection.

Two consequences of Phase 1's encryption, stated so nobody is surprised
in Phase 5:

- Rebuild requires `ledger/keys/`. A restored-from-backup ledger without
  its key directory can verify its chain but cannot regenerate the demo
  log. The keys travel with every backup (OQ-2 §3.4) precisely so this
  works.
- A crypto-shredded member's turns CANNOT be regenerated — by design.
  The rebuilt demo log after an erasure omits those turns (they
  decrypt to None and are skipped, with a count reported). The
  regenerated view is the governed view; the erasure reaching it is the
  feature working, not replay loss. The gate's byte-identity check
  therefore only holds for runs with no intervening erasure — the gate
  script asserts zero `member.key_destroyed` events in the compared
  window before claiming byte-identity.

## 5. Residuals and Register Updates

- **HEL-ACTOR-1 (widened, not new):** value.decrypt payloads carry
  subject_member and requester ids in plaintext, surviving erasure.
  Same resolution: registry-level opaque member IDs before the first
  external household.
- **HEL-DETECT-1 (new, declared; resolution SPEC'd 2026-07-14 during
  the turn_id-hoist build):** detections fired without a turn_id emit
  `turn_id: null` — correlated only by session_id. Two such sites
  exist, and the code read during the hoist established the voice path
  is NOT structurally session-only — it already emits a per-turn
  d1.1 record, just with an id minted too late and in the wrong module:
  - `realtime_adapter._handle_user_transcript` fires detection at
    utterance arrival; the SAME adapter emits the turn's record at
    `response.done` (`_pump_turn`, `turn_id=str(uuid.uuid4())`). The
    turn is bounded (utterance → response.done) within one object.
    **Resolution (spec, not built):** mint `self._turn_id =
    new_turn_id()` in `_handle_user_transcript` before the detect
    dispatch; pass it to `detect_and_apply_async`; `_pump_turn` uses
    `self._turn_id` (falling back to a fresh mint if no utterance
    preceded — model-initiated audio) instead of its inline uuid4.
    One attribute, three lines, no cross-module plumbing. The only
    subtlety: overlapping turns (barge-in) must not reuse a stale id —
    clear the attribute at response.done.
  - `voice_orch` shadow-routing handler (~line 1536) fires detection
    for voice utterances whose record is emitted by the adapter above.
    Once the adapter mints at utterance arrival, this handler should
    RECEIVE that id rather than mint its own — same turn, one id. This
    is the one genuinely cross-module thread; it rides the same call
    path that already carries `query` from the adapter into the
    handler. Until built, `turn_id=None` — honestly uncorrelated beats
    a guessed join.
  Neither site is Phase 2-blocking: text-path turns (all nine d1.1
  record paths) are fully joined as of the hoist commit.
- **TD-101b:** unchanged and still open. This spec makes the endpoint
  logged, not gated. The auth gate drops into the `authority` block
  with zero schema change when it lands.
- **TD-124 (durable outbox):** fact.detect's `attempt` counter is
  schema-reserved for it (§1.4).
- Debt register: point TD-108's Phase 2 row at this doc.
