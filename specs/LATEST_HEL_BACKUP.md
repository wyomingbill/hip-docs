# HEL OQ-2: Ledger Durability — Sealed-Segment Backup and Replica
Status: PLAN
Reconciled-Against: 262dc9b (HEL spec commit, 2026-07-14)
Date: 2026-07-14 16:15 MT
Scope: SPEC ONLY. No build. Amends HEL v20260714_1700, resolves OQ-2.
Depends-On: HEL v20260714_1700 (base spec), harness/encryption.py (key architecture)

---

## 1. The Risk

`ledger/` on the Mini is one failure domain. Disk failure, theft, or the Mini
going offline permanently takes the entire audit trail. The diligence claim
("show me the governance record for any disclosure, 90 days ago") fails the
moment the hardware does. A sealed ledger on one drive is not an audit record
for any purpose that requires it to outlast the hardware.

This amendment resolves that. It does NOT change the HEL writer, the event
schema, or the migration phases — it defines what happens to sealed segments
after they close.

---

## 2. When a Segment Is Sealed and What That Means

From the base spec (§4.3): a segment seals at 64 MB or 30 days, whichever
comes first. The seal procedure (to be implemented):

1. Writer emits a `ledger.segment_sealed` event as the final line of the
   segment, recording: segment number, final hash, event count, first and last
   seq, first and last ts.
2. Writer writes `ledger/hel-<n>.sha256` — a sidecar manifest containing
   the sealed segment's final hash and byte count, signed by the same chain
   (i.e., the manifest's hash IS the `ledger.segment_sealed` event's hash).
3. Writer opens `ledger/hel-<n+1>.jsonl`. The first event of the new segment
   sets `prev_hash` to the sealed segment's final hash — this is the
   cross-segment chain anchor (see §5).
4. The sealed file is now immutable on the primary. No writer ever reopens it.

**What "safe to ship" means:** a sealed segment with its sidecar is
self-verifying. `verify_ledger.py` can authenticate it without the active
segment or any external state. It is the unit of backup.

---

## 3. Payload Encryption — the Crypto-Shredding Foundation

### 3.1 Why encryption is the backbone, not an add-on

Backup without a destruction mechanism creates operator liability: 47 USC 551
and the GDPR right-to-erasure reach every copy, including replicas. A backup
architecture that requires enumerating and individually wiping every copy when
a member exits is operationally fragile and auditorially weak. Crypto-shredding
fixes this: destroy the member's key once, and every payload that member ever
generated — on every copy, on every backup medium — is permanently
unrecoverable without any copy enumeration.

This argument holds ONLY if every copy holds ciphertext under the same key.
Therefore the key scheme must be decided BEFORE the first backup runs. Retrofitting
encryption to an existing backup of plaintext JSONL defeats the purpose.

### 3.2 What HEL event payloads contain that is PII

HEL's TD-030 enforcement (`_strip_values` on the ledger writer) ensures no
fact value appears in any payload. But `turn.record` events carry the d1.1
dict verbatim, which includes `query` and `reply` — the member's raw utterance
and HIP's response. These are the most sensitive PII in the system: the
emotional disclosures that are HIP's entire value proposition. The `actor.id`
field carries the member identifier. Both must be treated as PII regardless of
the TD-030 guarantee.

System-class events (`system.reset`, `ledger.segment_sealed`, `system.note`,
`harness`-actor events) contain no member PII and are not encrypted.

### 3.3 Per-member key scheme

**Key store:** `ledger/keys/` directory, chmod 0700, owned by the HIP process
user. One file per member: `member_<member_id>.key` — 32 random bytes
(AES-256 key), generated on the first event for that member, never derived,
never rotated except on explicit member deletion. The key store is backed up
alongside the segment files (§4) — without the keys, the encrypted segments are
permanently unreadable.

**Encryption per event:**
- Envelope fields (`hel`, `seq`, `event_id`, `event_type`, `ts`, `actor.kind`,
  `actor.id`, `correlation.*`, `prev_hash`, `hash`) — PLAINTEXT. These fields
  are what make the chain verifiable and what a compliance reviewer reads to
  orient in time without needing decryption.
- `payload` field — ENCRYPTED. Replaced in the JSONL line with two fields:
  - `"payload_enc"`: base64url(AES-256-GCM(nonce ‖ ciphertext ‖ tag)), where
    nonce is 12 random bytes prepended to the ciphertext blob
  - `"payload_kid"`: `"member:<member_id>"` — identifies which key decrypts it

**Chain hash:**
The `hash` field covers canonical JSON (sorted keys, no whitespace) of the
entire event as written to disk — including `payload_enc` (ciphertext), NOT
the plaintext payload. The chain therefore authenticates the ciphertext. A
verifier with the key can decrypt and inspect; a verifier without the key
can still verify chain continuity. Both properties are preserved after DEK
destruction: the chain remains intact and verifiable; the payloads are
permanently opaque.

**Non-member events** (`actor.kind` ∈ {system, operator, harness}): `payload`
field stored plaintext as in the base spec. No `payload_enc` / `payload_kid`.
The chain covers plaintext payload directly, as before.

### 3.4 Key relationship to existing encryption

`harness/encryption.py` uses HKDF-derived per-member keys for wrapping fact
DEKs — the member key is derived from a master key file + member_id. HEL
uses a DIFFERENT, INDEPENDENT key store: random per-member bytes in
`ledger/keys/`, not derived. Rationale:

- HKDF derivation means "destroy member key" = rotate master key excluding
  that member, which is a multi-step operation affecting all members.
- HEL keys are stored, not derived, so `rm ledger/keys/member_sam.key` is a
  single atomic operation that destroys exactly one member's HEL access.
- The two schemes are independent; rotating the fact-encryption master key does
  not affect HEL keys and vice versa.

The backup procedure MUST include `ledger/keys/` — if keys are lost, encrypted
segments are permanently opaque. The keys are small (≤100 members × 32 bytes =
~3 KB total) and should travel with every segment backup.

---

## 4. Where Backups Go — The In-Boundary Constraint

**Non-negotiable:** HIP is operator-custodial. The operator's boundary is the
trust boundary. Sealed segments contain operator-held PII. A backup that leaves
the operator's boundary (a third-party cloud service, a vendor-managed SaaS
storage endpoint) violates custodial posture and potentially the BAA. This
constraint is permanent, not a v1 limitation.

### 4.1 v1 — Local second copy (rsync within operator network)

Target: a second physical location reachable over the operator's local network
or a directly attached volume. For the demo household (Mini is the primary):
eligible destinations are the Mac, an operator-owned NAS, or an external drive
attached to the Mini in a separate enclosure.

Mechanism: `scripts/backup_sealed_segment.sh` — triggered by the seal procedure
after the sidecar is written:

```bash
rsync -a --checksum \
  ledger/hel-<n>.jsonl \
  ledger/hel-<n>.sha256 \
  ledger/keys/ \
  <BACKUP_DEST>/ledger/
```

`--checksum` (not `--times`) is required — it verifies byte-for-byte identity,
not mtime. The script exits non-zero on any transfer error; the failure is
logged to `ledger/spool.failsafe` and increments `hel_backup_failures`
(exposed on `/api/proof`). Backup failure never fails a turn or blocks the
ledger writer.

Configured via `ledger/BACKUP.conf` (operator-managed, gitignored):

```
BACKUP_DEST=/Volumes/operator-nas/hip-backup
# or: user@192.168.1.x:/backup/hip-ledger
```

Absent this file: backup is disabled, dashboard shows `backup: disabled`.

### 4.2 Production path — Operator object storage

For a production deployment in an operator's cloud tenancy (AWS, Azure,
on-premises MinIO): the backup destination is the operator's own S3-compatible
bucket, in the operator's account, in the operator's region. The upload script
uses the operator's credentials (IAM role, service account, mTLS) — HIP never
holds storage credentials for a third-party service.

Upload: `aws s3 cp` / `az storage blob upload` / `mc cp` depending on the
operator's stack, with server-side encryption at the operator's option (the
segments are already payload-encrypted; SSE is defense-in-depth, not the
privacy layer). Bucket policy: write-only from the HIP process, read by the
operator's designated backup administrator.

This path is an operator integration decision, not a HIP-code decision. HIP
ships a documented interface (§4.1's script) and the operator wires it to their
storage. HIP never chooses the storage provider on the operator's behalf.

### 4.3 What is NOT in scope

- Third-party backup SaaS (Backblaze, Glacier, Google Archive): excluded by
  in-boundary constraint regardless of encryption.
- HIP-managed cloud storage of any kind: HIP is not the custodian; the operator
  is; HIP's infrastructure may not hold the operator's member data.
- Cross-operator replication: ledgers are per-deployment; one operator's ledger
  is never replicated to another's.

---

## 5. Chain Integrity Across Copies

### 5.1 What makes a copied segment verifiable

A sealed segment + sidecar is self-verifying with `verify_ledger.py`:

```
verify_ledger.py --segment hel-<n>.jsonl --sidecar hel-<n>.sha256
```

The script:
1. Reads every line, re-derives each event's hash over its canonical JSON.
2. Confirms each `prev_hash` matches the prior event's `hash`.
3. Confirms the final event's `hash` matches the sidecar's recorded value.
4. Reports byte count matches sidecar.

Any single-byte tamper — whether in transit or at rest — breaks the chain at
the first modified event and surfaces immediately. The sidecar cannot be
independently forged because its value IS the final event hash, which is
chained to all prior events.

### 5.2 The cross-segment anchor

The base spec requires the first event of segment N+1 to set `prev_hash` to
segment N's final hash. This creates a chain that spans segments: to verify
segment N, you need its predecessor's sealed hash, which is recorded in the
first line of the successor. For an isolated restored segment (no successor
available), the sidecar is the anchor. For a full restore, the chain is
continuous end-to-end.

**Tamper detection on backup:** if a backup provider (even an operator employee)
modifies a segment after the fact, verification fails. The cross-segment anchor
means you cannot even replace a segment with a correctly-chained substitute
without having the prior segment's final hash — which is itself chained, all
the way back to segment 0. The audit trail is end-to-end tamper-evident from
genesis.

### 5.3 What verification does NOT prove

Verification proves the chain is intact from a given starting point. It does
not prove:
- The events were generated by the live HEL system (not synthesized). A
  complete chain forgery from genesis is possible if the private key material
  is compromised — mitigation is access control on the Mini and the backup
  destination, not cryptographic signing.
- The backup is complete (no segments missing). The restore procedure (§6.3)
  must check seq continuity across all restored segments. A gap in segment
  numbering is an integrity failure.

For v1 (demo household, controlled trust environment) this is acceptable. A
future amendment may add an HMAC-signed segment manifest if external diligence
requires stronger forgery resistance (HEL-INTEGRITY-1, reserved).

---

## 6. Retention, Rotation, and Restore

### 6.1 Retention policy

The base spec establishes indefinite retention as the default for governance
events, with `ledger/RETENTION.md` as the per-deployment declaration. This
amendment adds:

**Sealed segment TTL** (for deployments that define one): when a sealed segment
expires under the retention policy, the operator:
1. Emits a `system.note` event in the CURRENT active segment, recording: segment
   number, final hash (from sidecar), event count, expiry reason, actor.
2. Deletes the segment file and sidecar from all copies — primary AND all backup
   destinations.
3. Optionally deletes the member keys if all segments for that member are now
   expired (see §6.2 for member-specific deletion).

The `system.note` in the active segment is the permanent record that the
segment existed. Segment deletion does not produce a gap in seq — seq is
monotonic within the segment while it existed; the missing segment is the
evidence, not the absence.

### 6.2 Member deletion (47 USC 551 / GDPR)

When a member exits (account termination, right-to-erasure request):

1. **Delete the member's key:** `rm ledger/keys/member_<member_id>.key`. This
   is the crypto-shred. Every event payload encrypted under this key — on the
   primary AND every backup copy — is simultaneously permanently unreadable.
   No copy enumeration required. No segment file is touched.

2. **Emit `system.note`** in the active segment: `{"event": "member.key_destroyed",
   "member_id": "<id>", "reason": "member_exit|erasure_request|…", "actor": …}`.
   This is the permanent record of destruction. The chain continues.

3. **Propagate key deletion to backup:** the backup destination's
   `ledger/keys/member_<member_id>.key` must also be deleted. For rsync-based
   backup this is a second `rm` on the backup host. For object-storage backup,
   delete the key object from the bucket. This step is required; an undestroyed
   key in the backup is a copy of the PII that was not shredded.

4. **The envelope still exists in backup segments.** `actor.id` in the envelope
   is the member identifier (plaintext). This is a pseudonymous identifier, not
   a name, IF the system uses opaque member IDs. If member IDs are human-readable
   names (e.g. "sam"), this is residual PII — the payload is dead, but the
   identifier persists in the chain. **Resolution path (HEL-ACTOR-1):** member
   identifiers in the envelope should be stable UUIDs; the member registry maps
   UUID→name separately. Destroying the registry entry for a member (which
   demo_reset already does for fact erasure) handles the name exposure. This
   is a v2 hardening, not a v1 blocker, but must be declared in the retention
   policy as the residual.

### 6.3 What a restore looks like

Full restore (Mini is dead, recovering on new hardware):

1. Copy all segments + sidecars + `ledger/keys/` from backup to `ledger/` on
   the new box.
2. Run: `verify_ledger.py --all` — walks every segment in seq order, verifies
   the end-to-end chain from segment 0 to the last sealed segment.
3. Check seq continuity: no gaps in segment numbering. A gap indicates a missing
   backup and must be reported to the operator before declaring the restore
   complete.
4. The active (unsealed) segment from the primary may be partially or fully
   lost. The durable floor is the last sealed segment. Lost events in the tail
   of the active segment are documented in the incident record (`system.note`
   in the first event of the first new segment after restore).
5. Resume normal operation. The first new event's `prev_hash` is the final hash
   of the last verified sealed segment.

**What can be recovered:** all events up to and including the last sealed segment.
The tail (events in the active segment since the last seal) is at risk on a
disk failure without a real-time replica — sealed segments are backed up on
seal; the active segment is not replicated continuously in v1.

**Projection recovery:** `ledger_reader.py` projections rebuild deterministically
from the event log. `turns_demo.jsonl` (Phase 4 onward) regenerates from
`turn.record` events. The demo dashboard recovers automatically.

### 6.4 Active segment replication (out of scope for v1)

Continuous replication of the active (unsealed) segment would close the tail
risk. This requires either a streaming replica (rsync --daemon / inotify) or
a write-through to a second append target. Both add operational complexity
disproportionate to v1's scale. Sealed-on-seal backup is the v1 durability
floor; the tail risk is accepted and documented as HEL-TAIL-RISK-1 (distinct
from HEL-TAIL-1 in the base spec, which is latency tail, not data tail).

---

## 7. 47 USC 551 Analysis

47 USC 551(e): "A cable operator shall destroy personally identifiable
information if the information is no longer necessary for the purpose for which
it was collected and there are no pending requests or orders for access to such
information."

**The backup is operator-held PII.** HIP is operator-custodial: the operator
is the cable operator for purposes of this statute. Every copy — primary and
backup — is within the operator's custody. The destruction mandate reaches all
copies. An operator who deletes member data from the primary but retains an
encrypted backup with the member's live key has NOT satisfied §551(e).

**Crypto-shredding as destruction:** destroying a cryptographic key that is the
sole path to plaintext is recognized as functionally equivalent to data
destruction under FTC guidance on data security, NIST SP 800-188 (media
sanitization), and legal commentary on GDPR Art. 17. The argument: if no
recoverable key exists, the ciphertext is computationally equivalent to random
noise. For the prototype household (one operator, controlled environment) this
analysis is clean. For production, the operator's counsel confirms. HIP's
design makes this the ONLY path to member data — no secondary plaintext copy,
no key escrow — so the analysis is not contingent on external attestation.

**The `system.note` record of deletion is not PII** in the payload sense: it
records the fact of destruction (member_id, timestamp, reason), not the
destroyed data. The member_id in this event is residual identifier exposure
(§6.2 HEL-ACTOR-1). Counsel note: if member_id is a UUID not traceable to a
natural person without the destroyed registry entry, it is effectively
de-identified after registry deletion.

**Backup copies the operator CANNOT destroy are a compliance failure.** The
in-boundary constraint (§4) exists precisely because HIP cannot reach a
third-party storage endpoint to delete the operator's data on the operator's
behalf. Any design that places sealed segments outside operator custody creates
an undeletable copy and violates §551(e) regardless of encryption.

---

## 8. OQ-2 Resolution — Decisions

| Decision | Adopted |
|---|---|
| Sealed segment as the backup unit | Yes — active segment tail accepted as durable floor |
| Payload encryption required before first backup | Yes — no plaintext segment ever written to backup |
| Per-member key scheme (stored, not derived) | Yes — `ledger/keys/member_<id>.key`, 32 random bytes |
| Key store travels with every backup | Yes — without keys, encrypted segments are permanently opaque |
| v1 backup mechanism | rsync of sealed segments + keys after each seal |
| Backup destination | Operator-declared in `ledger/BACKUP.conf`; absent = backup disabled |
| In-boundary constraint | Non-negotiable — no third-party cloud, no HIP-managed storage |
| Crypto-shredding as the deletion path | Yes — rm key file on primary + backup; no segment file changes |
| Member deletion propagation to backup | Required — key deletion MUST reach all backup copies |
| Active segment replication | Out of scope for v1 (HEL-TAIL-RISK-1) |
| Tamper detection | Self-verifying per segment (chain + sidecar); cross-segment anchor in successor |
| 47 USC 551 satisfied by | DEK destruction (crypto-shredding) + envelope residual declared (HEL-ACTOR-1) |

**OQ-2 is CLOSED.** Phase 1 is unblocked. OQ-3 (retention default, GDPR
identifier handling) remains the last pre-Phase-1 question.

---

## 9. Open Questions Created by This Amendment

**HEL-ACTOR-1 (v2 hardening, declared residual):** member identifiers in
plaintext envelopes. Should use stable UUIDs not human-readable names. Envelope
`actor.id` is residual PII after crypto-shred if it is a name. Resolution:
enforce opaque member IDs at the HEL writer; registry holds UUID→name mapping.
Does not block Phase 1 (demo household uses "sam"/"bill" style IDs and a
controlled trust environment, no external households).

**HEL-ACTOR-1 Phase 1 decision (2026-07-14, build reconcile):** confirmed
DEFERRED — Phase 1 does NOT pseudonymize actor.id — but the residual is
upgraded from "v2 hardening" to a **hard precondition for the first
external household's first event**. Rationale: (1) every event in the demo
ledger is demo-household data in a controlled environment, and the first
production household starts a fresh ledger, so no immortal external PII is
being written in the interim; (2) the correct fix is registry-level opaque
member IDs — ONE identifier scheme across registry, facts, and ledger —
not an HEL-local HMAC layer that every Phase 2/3 correlation join
(fact.write, fact.detect by member and fact_id) would have to translate
across; (3) plaintext envelopes are load-bearing in this spec's own design
(§3.3: what a reviewer reads to orient without decryption) — a divergent
per-ledger pseudonym would break that while still leaving stable linkable
identifiers in the chain, i.e., cost without the anonymity. Gate wording:
the registry UUID migration must land, and HEL actor.id must carry the
opaque ID, before any non-demo household's first ledger event.

**HEL-TAIL-RISK-1 (declared gap, v2):** events in the active (unsealed)
segment since the last seal are not replicated in v1. On a catastrophic disk
failure, up to 30 days of events could be lost (if the segment never reaches
64 MB). For the demo household this is acceptable; for a live household it
requires either shorter seal intervals (reduce the tail window) or active
segment streaming. Decision for the first live-household deployment.

**HEL-BACKUP-1 (v1 gate criterion):** `backup_sealed_segment.sh` must verify
that the rsync completed and the remote sha256 matches the sidecar before
clearing the backup success flag. Without this check, "backup complete" means
"rsync exited 0," which includes partial transfers on pre-existing errors.
Add `sha256sum --check` on the destination after transfer.

**HEL-KEYMGMT-1 (production consideration):** `ledger/keys/` is a flat
directory of raw key files. For production, a hardware key store (HSM, TPM,
or the operator's KMS) is the right home. The KMS path requires the operator
to provision a key per member, which is an operator integration decision.
v1 (flat files, operator hardware) is correct at demo scale.

---

## 10. Relationship to Other Specs

- **HEL base spec (v20260714_1700, OQ-1 section):** §4.3 fsync policy is
  unchanged. This amendment adds §3/4/5/6 (encryption, backup, chain
  integrity, restore, retention). OQ-2 "Amended" note to be added to base spec.
- **harness/encryption.py:** per-member fact key derivation is INDEPENDENT of
  the HEL per-member key store. The two schemes coexist without interaction.
  A future consolidation (share the key vault between fact encryption and HEL
  encryption) is possible but would require the derived→stored migration above
  (HEL-KEYMGMT-1) and is a v3 concern.
- **TD-101b (vault decrypt auth gate):** Phase 3's `value.decrypt` event ships
  a plaintext payload (no member key, since the actor is the requestor, not the
  subject member). Revisit if the decrypt requestor's identity is also PII
  requiring encryption — deferred to TD-101b design.
- **demo_reset.py:** demo_reset is explicitly forbidden from touching `ledger/`
  (base spec). It must also not touch `ledger/keys/`. Verify in Phase 2 gate.
