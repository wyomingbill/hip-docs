# TD-108: Canonical Append-Only Epistemic Event Ledger (HEL)
Status: PLAN
Reconciled-Against: d6b4da6 (post D-1 complete; code read 2026-07-14)
Date: 2026-07-14 17:00 MT
Amended: 2026-07-14 (OQ-1 CLOSED -- measured on the Mini; per-event
F_FULLFSYNC adopted; group-commit and two-tier fallbacks retired)
Amended: 2026-07-14 (OQ-2 CLOSED -- backup/replica spec in
EPISTEMIC_LEDGER__hel-oq2-backup-replica__v20260714_1615.md: sealed-segment
unit; per-member payload encryption + crypto-shredding as backbone;
in-boundary rsync v1; operator object storage production path; chain
integrity via sidecar + cross-segment anchor; member deletion via key
destruction; 47 USC 551 analysis. OQ-3 is the last Phase 1 blocker.)
Scope: SPEC ONLY. No build. Phased migration gated on Bill's sign-off.

---

## Executive Summary

HIP's auditability claim rests on a demo log. The D-1 epistemic record (d1.1)
is real, complete per-turn, and proven byte-compatible — but it lands in
`logs/turns_demo.jsonl`, a file that `demo_reset.py` truncates to zero bytes
on every reset, whose writes are unsynced and silently lossy, and which no
mechanism protects from edit or deletion. Three other audit surfaces
(encode_audit, truth_audit, write_latency) are separate uncorrelated files
with the same properties.

This spec defines the **HIP Epistemic Ledger (HEL)**: a canonical, append-only,
hash-chained, fsynced event store that the D-1 record is *promoted into* as one
event type among several. The demo log becomes a projection of the ledger, not
the record itself. Migration is five phases, each gated, none of which touches
D-1's proven behavior until the final phase — and even then only by
re-derivation, verified byte-compatible.

---

## 1. What Exists Today

### 1.1 The D-1 record (d1.1) — the good part

`harness/epistemic_record.py` (spec: D1_RECORD_SPEC v20260712_1138, commit
1c717f5):

- `build_epistemic_record()` — pure projection, no engine calls, no I/O.
  Blocks: envelope (turn_id, ts, session_id, member, query, reply, path),
  routing (tier, complexity, bloom, net, sensitivity_tag, intent, sio_source),
  disclosure (admitted[], withheld[], denied_counts, guard, resolved_subjects,
  injected_fact_ids), write (delta[], park, confirmation, writes_pending),
  timing (routing_ms, inference_ms).
- TD-030 enforced twice: `_fact_entry()` never projects values;
  `_strip_values()` re-strips the write block as defense-in-depth.
- FLAG-1 enforced: withheld is structurally empty on access_control (INJ-7)
  records — existence-invariance holds in the log too.
- Nine emit sites in `server/voice_orch.py` covering all nine return paths of
  `process_text_query` (confirmation, local_now, control_decline,
  control_pending, drop, guard_inj7, guard_empty_set,
  generation_placeholder, generation).
- Byte-compat proven by `scripts/check_bytecompat_d1.py` against captured
  shadow baselines.

**The record content is canonical-grade. The record's destination is not.**

### 1.2 The destination — `logs/turns_demo.jsonl`

`log_epistemic_record()`: `open(path, "a")` + `write()` inside a bare
`try/except: pass`. No fsync. No lock. No sequence number (ordering is file
position only). No integrity mechanism. Gitignored, single disk, no rotation,
no retention policy.

### 1.3 The other audit surfaces (uncorrelated)

| Surface | Writer | What it records | Correlation to turn |
|---|---|---|---|
| `logs/memory_engine/encode_audit.jsonl` | `store.py:_append_audit` | Every encode: fact_id, requested vs actual write_state, override_reason, model_id, prompt_hash, prior_closed_fact_id | session_id only — **no turn_id** |
| `logs/truth_layer/truth_audit.jsonl` | `truth_layer/queries.py:_append_truth_audit` | Truth-layer queries (who asked what about which fact) | fact_id only |
| `logs/write_latency.jsonl` | DIAG-1 (294f259) | Measurement instrumentation (t0-t4, detect outcomes) | iter tag (harness-only) |
| Neo4j `:Fact` nodes | `store.py` | Current state + supersede chains (valid_to, superseded_by) | Not an event store; deleted wholesale by demo_reset |

Four write-side ledgers, one turn-side log, zero shared event identity, no
common ordering, and every one of them either truncatable or deletable by the
reset path.

### 1.4 Consumers (what must keep working)

- `server/demo_dashboard.py:/api/turns` — tail-reads turns_demo.jsonl,
  newest-first, `since=` filter
- `eval/harnesslib/layer1.py` — line-count-before / first-new-record-after
  pattern around each harness turn
- `eval/memory_harness.py` MEM-118, `eval/integration_harness.py`,
  `eval/test_demo_smoke.py` A1 — assert on new records and delta contents
- `scripts/check_bytecompat_d1.py` — compares records against shadow baselines
- `scripts/capture_shadow_baseline.py` — captures fixtures from the live file

---

## 2. Why turns_demo.jsonl Is Not a Canonical Event Record

Named precisely, in descending severity:

**M-1. It is truncated by design.** `demo_reset.py` line ~119:
`path.write_bytes(b"")`. Every demo reset zeroes the entire epistemic history.
The file's own name says demo. A canonical record that a routine operational
script erases is not a record; it is a scratch buffer.

**M-2. Loss is silent and undetectable.** `emit_epistemic_record` and
`log_epistemic_record` swallow every exception. "A record write must never
fail a user turn" is the correct invariant — but the current implementation
conflates *never fail the turn* with *never notice the loss*. Disk full,
permission error, corrupted mount: records vanish with no counter, no health
signal, no spool. An auditor cannot distinguish "nothing happened" from
"the log dropped it."

**M-3. No durability.** Buffered `write()` with no `fsync`. A power cut or
process kill loses the tail. The record of a disclosure decision can die with
the process that made it.

**M-4. No ordering guarantee.** No monotonic sequence number. `ts` is
wall-clock (NTP steps, clock skew). Ordering is file-append position, which is
only meaningful if appends never interleave — and there is no lock; a second
writer process (or a future async detection emitter) can interleave partial
lines above PIPE_BUF size.

**M-5. No integrity.** Plain text, world-editable by any process with file
access. No hash chain, no seal. A hostile or buggy process can rewrite
history and nothing detects it. The governance-proof artifact
(HIP_GovernanceProof v20260714_1345) was built by auditing this file — its
evidentiary weight is bounded by the file's integrity, which is zero.

**M-6. The taxonomy is turn-only.** The d1.1 record captures the turn's
governance decisions, but the epistemic lifecycle extends past the turn:
- The async detection daemon completes AFTER the record is emitted
  (`writes_pending: true` is honest, but no subsequent event ever closes it —
  the eventual write outcome lands in encode_audit.jsonl with no turn_id).
  A P2-style detection false negative (DIAG v20260714_1500) is *invisible*
  in the turn record: writes_pending stays true forever with no terminal event.
- Vault decrypts (`/api/decrypt` — currently unauthenticated, TD-101b, and
  unlogged) — the single most audit-worthy action in the system has no event.
- Member registry changes, voiceprint enrollment, consent grants/revocations,
  demo resets themselves: none are events anywhere.

**M-7. No retention, no replay, no verification tooling.** Nothing defines how
long records live, nothing can rebuild a view from them, and nothing can
verify the log wasn't tampered with.

---

## 3. What's At Risk — The Exposure, Stated Honestly

The following claims currently in circulation depend on a canonical record and
would not survive an engineer's diligence pass against the actual code:

1. **The auditability moat itself.** WP Part II and the strategy doc position
   the trust boundary + auditable governance as the second half of the moat.
   The BIZOPS brief (v20260714_1630) escalates this: "compliance is our
   currency," the governance-proof artifact as the enterprise wedge into CMS
   GUIDE / HIPAA BAA / senior-living procurement. **A compliance officer's
   first question is "show me the audit trail for this disclosure, 90 days
   ago." Today's true answer: "our log was truncated at the last demo reset,
   and if it hadn't been, we couldn't prove it wasn't edited."** The wedge
   claim is hollow until HEL exists.

2. **The governance proof's evidentiary status.** HIP_GovernanceProof is an
   audited transcript — audited from a mutable, unsynced file. As a demo
   artifact it stands; as diligence evidence its chain of custody is one
   question deep.

3. **TD-108's own framing.** The debt register names the per-fact
   consent-and-routing ledger the "primary liability-severity reducer. Must
   ship pre-scale." The liability argument (we can prove what was disclosed,
   to whom, under which consent) is precisely the thing a demo log cannot
   prove. Every day of live household data without HEL accrues liability that
   can never be retroactively documented.

4. **The emotional-disclosure moat monetization.** The BIZOPS brief's core
   thesis — elders disclose to HIP what they hide from family, safely, because
   routing is governed — is a *promise about records*. Insurer risk
   stratification and CMS care-coordination billing both require provable
   consent routing. No ledger, no billing-grade claim.

5. **NIST AI RMF mapping** (TEST_HARNESS doc) — the harness maps conformance
   to the framework; the framework's GOVERN/MAP functions assume traceable
   decision records. Currently traceable until the next reset.

What does NOT depend on it: the injection contract's runtime behavior, the
harness gates, the demo. The engine governs correctly; it just cannot *prove
that it did* after the fact. The exposure is evidentiary, not behavioral —
which is exactly why it is invisible in every test and lethal in diligence.

---

## 4. The Spec — HIP Epistemic Ledger (HEL)

### 4.0 Design stance

The d1.1 record is **promoted, not replaced**. HEL is a new durable layer
underneath; the d1.1 dict becomes the payload of one event type. The demo log
becomes a *projection* of the ledger. Nothing about what D-1 records changes;
what changes is where the truth lives and what else lives beside it.

Storage decision: **segmented, hash-chained JSONL on disk** — not Neo4j, not
SQLite.
- Not Neo4j: the graph is state, not history; demo_reset legitimately deletes
  it; the ledger must record resets, therefore must survive them; and the
  ledger must not share fate with the store it audits.
- Not SQLite: auditable-by-inspection matters more than query speed; a
  compliance reviewer can read JSONL with `less` and verify the chain with a
  50-line script; zero new dependencies matches the repo's posture.

Location: `ledger/` at repo root (sibling of `logs/`, NOT inside it —
nothing that sweeps `logs/` may touch it). Gitignored like other data, but
governed by an explicit retention policy (4.6).

### 4.1 Event envelope (every event)

```json
{
  "hel": "1.0",
  "seq": 18422,
  "event_id": "uuid4",
  "event_type": "turn.record",
  "ts": "2026-07-14T23:59:59.123456+00:00",
  "actor": {"kind": "member|system|operator|harness", "id": "sam"},
  "correlation": {"turn_id": "…", "session_id": "…", "fact_ids": ["…"]},
  "payload": { … },
  "prev_hash": "sha256:…",
  "hash": "sha256:…"
}
```

- `seq`: monotonic per-ledger, assigned under the writer lock. THE ordering.
  `ts` is informational.
- `hash`: SHA-256 over canonical JSON (sorted keys, no whitespace) of the
  event with `hash` removed. `prev_hash` = previous event's `hash`; first
  event of a segment chains to the sealed hash of the prior segment.
- `correlation`: the join key that today does not exist. Every event carries
  the turn_id/session_id/fact_ids it knows, enabling per-fact and per-turn
  timelines as projections (this IS the "per-fact consent-and-routing ledger"
  of TD-108's original title — a projection over HEL, not a separate store).
- TD-030 carries over absolutely: **no event payload ever contains a fact
  value.** `_strip_values` moves into the ledger writer as a final gate.

### 4.2 Event taxonomy (v1)

| event_type | Source | Payload | Closes gap |
|---|---|---|---|
| `turn.record` | the 9 emit sites (unchanged) | the d1.1 dict, verbatim | — (promotion) |
| `fact.write` | `store.py:_append_audit` site | encode_audit fields + turn_id when known | M-6: encode ↔ turn correlation |
| `fact.detect` | `fact_change.detect_and_apply` terminal | outcome (committed n / no_changes / no_result / error), turn_id | M-6: closes `writes_pending`; makes P2-class silent misses visible in the canonical record |
| `value.decrypt` | `/api/decrypt` handler | fact_id, requester, authorized (bool), auth mechanism | M-6; TD-101b companion — the decrypt event ships even before the auth gate does |
| `truth.query` | `_append_truth_audit` site | existing truth_audit fields | consolidation |
| `member.change` | registry add/remove/update, voiceprint enroll | member_id, change kind | M-6 |
| `consent.change` | future consent surface (TD-110) | reserved — schema TBD with TD-110 | forward slot |
| `system.reset` | `demo_reset.py` | what was reset (facts n, members kept, logs truncated) | M-1: resets become events IN the ledger, never erasures OF it |
| `system.note` | operator annotation tool | free text | audit narrative |
| `ledger.segment_sealed` | ledger writer | segment n, final hash, event count | M-5 |

v1 ships the first four + system.reset + ledger control. The rest are
schema-reserved.

### 4.3 Writer contract

Single module `harness/epistemic_ledger.py`:

- `append(event_type, payload, *, actor, correlation) -> None` — never raises
  toward the caller (the D-1 invariant stands: governance outcome identical
  with or without the record).
- Under the hood, per append: acquire `flock` on the active segment → assign
  `seq` → chain hash → write line → **`fcntl(F_FULLFSYNC)`** → release.

  **Sync policy (OQ-1 CLOSED, measured 2026-07-14):** per-event
  `F_FULLFSYNC`, unconditional. Not `os.fsync` — on Darwin, `os.fsync()`
  reaches the drive cache only (survives crash, not power loss);
  `F_FULLFSYNC` is the honest durability the spec's claims require.
  Measured on the Mini (arm64, `scripts/measure_fsync_floor.py`, 89302be),
  full HEL-style append (seq + sha256 chain + write + flush + sync):

  | Config | p50 | p99 | max |
  |---|---|---|---|
  | none, 1KB (today's turns_demo behavior) | 0.018 ms | 0.025 ms | — |
  | os.fsync, 1KB | 0.047 ms | 0.086 ms | — |
  | **F_FULLFSYNC, 1KB** | **4.006 ms** | **6.558 ms** | **9.163 ms** |
  | F_FULLFSYNC, 4KB | 4.034 ms | 9.972 ms | 16.602 ms |
  | flock+fsync ×3 concurrent, 1KB | 0.164 ms | 0.210 ms | — |
  | flock+fsync ×3 concurrent, 4KB | 0.197 ms | 0.352 ms | — |

  Against the guard-turn budget (56-82 ms, the tightest path): 4 ms p50 is
  5-7% of the turn; 6.5-10 ms p99 is 8-12%. Affordable per event. Lock
  contention is a non-issue (sub-ms at 3 writers).

  **Retired alternatives:** group-commit (`HEL_FSYNC=group`) and the
  two-tier policy (per-event `os.fsync` + periodic `F_FULLFSYNC`
  checkpoint) are both retired — they were hedges against a cost that does
  not exist on the target hardware. Per-event `F_FULLFSYNC` is simpler than
  either and strictly stronger: every append is power-loss durable, and the
  write-ahead property holds — **no reply leaves the system before its
  governance record is durable.** That property is a diligence claim in its
  own right; do not trade it away without a measured reason.

  **Platform note (why this was measured, not assumed):** the same script
  on the Intel Mac measured F_FULLFSYNC at 19 ms p50 / 36 ms p99 — ~5x the
  Mini, and a number that WOULD have blown the guard budget and forced
  group-commit. The sync policy is a per-platform measurement, not a
  constant. Any future deployment target (operator edge hardware) must
  re-run `measure_fsync_floor.py` before inheriting this policy
  (HEL-PORT-1).

  **Residual — the tail (HEL-TAIL-1):** the measured max is 16.6 ms (4KB),
  a 20-30% hit on the worst-case guard turn. Recommendation: **accept,
  unbounded.** Rationale: (a) it moves a canned reply from ~56 ms to ~73 ms
  worst case, far under any perceptibility threshold; (b) the escape hatch
  — emitting the record after the reply is sent — would surrender the
  write-ahead property above, which is worth more than 17 ms of tail on a
  canned reply; (c) the tail is a hardware property that the Phase 1 gate
  re-measures anyway. Revisit only if a future measurement shows the tail
  growing past ~35 ms (half the guard budget) on production hardware.
- **Failure is never silent (fixes M-2):** on any append failure, increment
  `hel_append_failures` (exposed via dashboard `/api/proof` health block) and
  attempt a one-line spool to `ledger/spool.failsafe` with best effort. The
  turn still never fails; the *loss is now observable*.
- Segments: `ledger/hel-<n>.jsonl`, sealed at 64 MB or 30 days, whichever
  first; seal writes `ledger.segment_sealed` + a sidecar
  `hel-<n>.sha256` manifest.
- `scripts/verify_ledger.py`: walks segments, re-computes the chain, reports
  first divergence. This script is itself a diligence deliverable.

### 4.4 Ordering and concurrency

One writer lock per ledger (flock on the active segment). Today all emit
sites live in one process (voice_orch/demo_dashboard server); the detection
daemon threads share it. The lock makes multi-process append safe anyway
(harness + server on the same box). Cross-process `seq` continuity is
re-derived from the last line of the active segment on open.

### 4.5 Replay and projections

- `harness/ledger_reader.py`: iterate events, filter by type/correlation,
  tail-follow.
- Projection 1 — **demo turn view**: `turn.record` payloads only, in seq
  order = exactly today's turns_demo.jsonl content. This is the byte-compat
  bridge (Phase 4).
- Projection 2 — **per-fact timeline** (TD-108's named deliverable): all
  events whose correlation carries a given fact_id: written → disclosed
  (admitted/withheld per turn) → decrypted → superseded. One function, no new
  store.
- Projection 3 — **open-writes check**: `turn.record` with
  `writes_pending: true` lacking a terminal `fact.detect` within N seconds =
  detection loss (the P2 class), surfaced on the dashboard instead of buried
  in a harness poll ceiling.

### 4.6 Retention

Governance events are retained indefinitely by default; the retention policy
is a per-deployment declaration (`ledger/RETENTION.md` stub in v1). Sealed
segments are the archival unit. Deletion of a sealed segment is itself
recorded (`system.note` with the segment manifest hash) — you can expire
data without erasing the *fact that data existed*. GDPR/right-to-deletion
interaction: payloads never contain values (TD-030), so fact deletion in the
graph does not require ledger rewrites; identifiers-only erasure requests are
handled at projection level. (Open question OQ-3.)

### 4.7 Relationship to D-1 — stated exactly

The d1.1 record **is** the `turn.record` event payload. Same builder, same
schema version, same nine call sites. D-1's byte-compat guarantee transfers:
`check_bytecompat_d1.py` gains a mode that compares the ledger projection
against the same shadow baselines. HEL adds envelope (seq, hash, correlation)
*around* d1.1; it never reaches *into* it. Future d1.2 schema changes remain
D-1's concern, not HEL's.

---

## 5. Migration Path — Phased, Gated, D-1-Preserving

**Phase 0 — Sign-off.** Bill answers OQ-1..3 below. No code.

**Phase 1 — Ledger exists, dual-write turn records.**
`epistemic_ledger.py` + `verify_ledger.py`. `emit_epistemic_record` writes
turns_demo.jsonl exactly as today AND appends `turn.record` to HEL.
*Gate:* check_bytecompat_d1.py green (proves the demo log unchanged);
verify_ledger green after a full L2 run; in-situ append latency confirms
the bench numbers (F_FULLFSYNC p99 ≤ ~10 ms on the Mini per OQ-1).
Rollback: delete one call line.

**Phase 2 — Write-side events + reset stops being an erasure.**
`fact.write` dual-written from store.py's audit site (encode_audit.jsonl
keeps writing); `fact.detect` terminal event from the detection daemon
(turn_id plumbed via the existing tag mechanism); `system.reset` emitted by
demo_reset.py, which is explicitly forbidden from touching `ledger/`.
*Gate:* full harness green; correlation check — every `writes_pending: true`
turn in an L2 run has a terminal `fact.detect`; encode_audit ↔ fact.write
record-count parity.

**Phase 3 — value.decrypt event.** The decrypt handler logs before it
returns plaintext. Ships independent of (and before) TD-101b's auth gate —
an unauthenticated-but-logged endpoint is strictly better than
unauthenticated-and-unlogged, and the event schema is the same after the
gate lands. *Gate:* smoke test — every dashboard decrypt produces an event.

**Phase 4 — Consumers cut to projections.** `/api/turns` and the harness
readers (layer1, memory_harness, integration_harness, smoke) read the ledger
projection via ledger_reader. turns_demo.jsonl is still written (compat).
*Gate:* projection output byte-identical to file tail for the same run;
full harness green on the new readers.

**Phase 5 — Demotion.** turns_demo.jsonl becomes a regenerable view
(demo_reset may truncate it freely — it regenerates from HEL on demand);
HEL is canonical. *Gate:* `replay --rebuild-demo-log` reproduces the
truncated file's would-be content; byte-compat harness passes against the
rebuilt file.

Each phase is a separate commit with its gate output in the commit message.
No phase alters injection-contract, routing, or confirmation behavior —
FLAG-2/3/7 discipline carries over to HEL verbatim.

---

## 6. Open Questions for Bill (block Phase 1)

**OQ-1 — Fsync policy floor. CLOSED 2026-07-14 (measured, Bill's verdict).**
Measured on the Mini via `scripts/measure_fsync_floor.py` (89302be):
F_FULLFSYNC 4.0 ms p50 / 6.6 ms p99 / 16.6 ms max — 5-12% of the guard-turn
budget. **Decision: per-event `F_FULLFSYNC`, unconditional.** Group-commit
and the two-tier (fsync + periodic checkpoint) proposals are retired.
Full policy, measured table, platform caveat (Intel Mac was 5x slower —
measure, never assume), and the HEL-TAIL-1 residual are in section 4.3.

**OQ-2 — Ledger home and backup.** `ledger/` on the Mini's disk is one
failure domain. Is a nightly rsync of sealed segments (to the Mac, or
operator object storage later) in scope for v1, or a follow-on? The hash
manifests make remote copies verifiable. Recommendation: v1 ships local +
a one-line launchd rsync; document as HEL-BACKUP-1 if deferred.

**OQ-3 — Retention default.** "Indefinite" is the right diligence answer and
the wrong GDPR answer if identifiers count as personal data. Default
indefinite with projection-level erasure, or segment TTL? Recommendation:
indefinite for the prototype household (it's Bill's data), decide policy
language before the first external household.

---

## 7. Debt Register / Backlog Reconciliation

- TD-108 is this spec. The original title ("per-fact consent-and-routing
  ledger") is delivered as Projection 2 over HEL, not a separate store —
  the debt register entry should be updated to point here.
- TD-124 (durable outbox) is adjacent but distinct: TD-124 makes *writes*
  durable before commit; HEL makes *the record of decisions* durable after
  them. `fact.detect` events give TD-124's future outbox its audit surface.
- TD-101b: Phase 3's `value.decrypt` event should land with or before the
  auth gate; neither blocks the other.
- TD-113 (operator-view epistemic pane) and DEMO-6 (dashboard redesign):
  the fact-lifecycle view being designed is exactly Projection 2 — the
  redesign should read from ledger_reader's interface even if v1 backs it
  with the demo log, so the cutover is invisible.
