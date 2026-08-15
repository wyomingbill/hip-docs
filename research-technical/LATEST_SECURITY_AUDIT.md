<!-- STATUS: STALE -->
<!-- RECONCILED-AGAINST: point-in-time audit 2026-07-03; server/voice_https_orch.py (unauthenticated endpoints still present); harness/extraction_queue.py:embed_text (embeds value, not attribute — TD-030 finding still open); git log -S [REDACTED-ROTATED-2026-06-20] (history scrub still pending per doc); no remediation tracking in this doc — 2026-07-05 -->

# Security Audit — HIP Harness (hip-dev)

**Date:** 2026-07-03  
**Auditor:** Single-pass sequential review (claude-sonnet-4-6)  
**Scope:** `~/hip-dev` — all Python source, config, committed data, git history.  
**Out of scope:** `~/hip-harness` (demo checkout), network infrastructure, OS-level hardening.

---

## Executive Summary

HIP is a local-first voice assistant with a thoughtful encryption design (envelope
encryption, per-owner HKDF keys, sensitivity-gated routing). The implementation has
one **critical** gap that renders the encryption largely moot: every API endpoint on
the live voice server is unauthenticated and reachable by any host on the local
network, including a dedicated `/api/decrypt` route that returns plaintext fact values
for any household member on demand. The remaining findings cluster around unauthenticated
API surface, a git-history secret that has been rotated at the DB level but not scrubbed
from history, and an embedding invertibility risk where plaintext fact values are
embedded and stored alongside their ciphertext. None of the findings require code
changes here — this document is findings and remediation guidance only.

---

## Findings

---

### [CRITICAL] `/api/decrypt` returns all decrypted facts with no authentication

**File:** `server/voice_https_orch.py:169`  
**Risk:** Any unauthenticated caller on the network can exfiltrate every household member's decrypted personal facts (medications, diagnoses, finances, relationships).

`GET /api/decrypt?member=<any_member_id>` takes the target member as an unvalidated
query parameter, builds a Neo4j query scoped to that member, decrypts every matching
`:Fact` node's ciphertext using the envelope-encryption key, and returns the results
as JSON. There is no session check, no bearer token, no IP allowlist, and no role
verification. The endpoint is served over TLS (self-signed cert) on port 7860, which
is accessible to any device on the same network (and, via Tailscale, potentially
wider). The encryption in `harness/encryption.py` is correctly implemented; this
endpoint bypasses it entirely by providing decryption as an unauthenticated service.

**Remediation:**
1. Add an API key or shared-secret header requirement to all `/api/*` routes. FastAPI
   example: `from fastapi.security import APIKeyHeader; key = APIKeyHeader(name="X-HIP-Key"); @app.get("/api/decrypt", dependencies=[Depends(verify_key)])`.
2. As an immediate stop-gap, restrict the endpoint to `127.0.0.1` only (add a
   middleware check on `request.client.host`) until proper auth is wired.
3. Re-evaluate whether `/api/decrypt` needs to exist at all — the dashboard reads
   `/api/facts` (metadata only) and facts are decrypted in the voice pipeline where
   member identity is established via speaker verification.

---

### [HIGH] `/api/routing` serves plaintext user queries with no authentication

**File:** `server/voice_https_orch.py:44` (endpoint) + `server/voice_orch.py:206` (write)  
**Risk:** Every spoken query — including sensitive health questions — is logged verbatim to `router.jsonl` and served to any unauthenticated caller via this endpoint.

`_write_routing_log` at `voice_orch.py:206` writes `"query": query` (the full
cleartext transcription) into `logs/router.jsonl`. `GET /api/routing` at
`voice_https_orch.py:44` reads and returns the last 50 entries from that file
with no auth check. A user asking "I take Ozempic for type 2 diabetes — when
should I eat?" produces a log entry with that exact text accessible to any
network peer. The same plaintext query field also appears in the per-session
trace files written by `_write_trace_log` at `voice_orch.py:313`, though those
files are not served via an API endpoint.

**Remediation:**
1. Protect `/api/routing` with the same auth as `[CRITICAL]` above.
2. Replace `"query": query` with `"query_hash"` only in the served response
   (the hash is already logged alongside the cleartext). Keep the full text
   in a local-only log file not served via any API if it is needed for debugging.

---

### [HIGH] `/api/text-query` allows arbitrary member impersonation

**File:** `server/voice_https_orch.py:63`  
**Risk:** Any unauthenticated caller can inject queries as any registered household member, triggering fact-change detection and memory writes under that member's identity.

`POST /api/text-query` accepts `{"query": "...", "member": "<member_id>"}` with no
authentication. It validates that the `member` field resolves in the registry
(`get_member_by_id` check at line 74) but does not verify that the caller *is* that
member. `process_text_query` then retrieves that member's personal facts, runs
fact-change detection (`detect_and_apply_async`), and potentially writes new
`:Fact` nodes attributed to that member. An attacker on the local network can
manipulate any member's stored facts by crafting POST bodies.

**Remediation:**
1. Protect with the same auth scheme as `[CRITICAL]`.
2. If the endpoint must remain for demo purposes, scope it to `127.0.0.1` only.

---

### [HIGH] `/api/reset` is an unauthenticated destructive endpoint

**File:** `server/voice_https_orch.py:83`  
**Risk:** Any unauthenticated network caller can wipe the entire Neo4j fact graph and reseed it with demo data, destroying all stored personal facts.

`POST /api/reset` runs `scripts/demo_reset.py --yes` (deletes all `:Fact` nodes
and non-Bill registry entries) followed by `scripts/demo_seed.py` (inserts fixed
demo facts), with no authentication, no CSRF protection, and no confirmation
parameter. There is no rate limit. In a production deployment, a single unauthenticated
POST from any device on the local network destroys all enrolled member data.

**Remediation:**
1. Protect with the same auth scheme as `[CRITICAL]`.
2. Consider removing `/api/reset` from the production server and keeping it
   only in a separate development/demo binary.

---

### [HIGH] Embedding of plaintext fact value stored alongside ciphertext (TD-030 invertibility risk)

**File:** `harness/extraction_queue.py:557`  
**Risk:** The `embedding` vector stored on each `:Fact` node encodes the cleartext value and can be used to approximately invert it, undermining envelope encryption.

`write_facts` calls `embed_text(fact["value"])` at line 557 — embedding the
cleartext value string — and stores the result as `embedding` on the `:Fact` node
alongside `ciphertext` and `encrypted_dek`. An adversary with read access to
Neo4j (e.g., via the Bolt port or a compromised `NEO4J_PASSWORD`) obtains
both the opaque ciphertext and a high-dimensional vector of the plaintext. For
medical facts with a constrained vocabulary (drug names, diagnoses), embedding
inversion via exhaustive nearest-neighbour lookup against a public medical corpus
is practical. This directly contradicts the TD-030 design intent ("fact value is
the sensitive payload"). The intended design — embeddings encoding
subject+predicate only, never the object — is **not implemented**; the current
code embeds the object (value) exclusively.

**Remediation:**
1. Replace `embed_text(fact["value"])` with `embed_text(fact["attribute"])` so
   the vector encodes only the attribute name (e.g., "medication"), which is
   already stored in cleartext and adds no new information.
2. Alternatively, embed a salted HMAC of the value rather than the value itself,
   so the vector is not invertible without the secret.
3. Migrate existing `:Fact` nodes: re-embed all active nodes with the
   attribute-only scheme and overwrite their `embedding` property.

---

### [HIGH] `[REDACTED-ROTATED-2026-06-20]` in git history — rotation done, history scrub pending (TD-021)

**File:** `harness/zep_store.py` in commits `165663a`, `6065ffc`, `0aaa934`  
**Risk:** Any future clone of this repository exposes the original Neo4j password in perpetuity; credential-scanning tools will flag it immediately.

The hardcoded default `[REDACTED-ROTATED-2026-06-20]` was introduced in commit `165663a` (initial
Zep substrate work) and documented in DECISIONS.md in commit `0aaa934`. It was
removed from source in commits `609f4c6` / `0c4d324` (2026-06-16, TD-021) and the
live DB password was rotated on 2026-06-20 (commit `8fe6802`). The rotation
invalidates the credential at the database level. However, `git-filter-repo` has
not been run — the six affected commits remain in full history and are visible via
`git log -p -S [REDACTED-ROTATED-2026-06-20]`. DECISIONS.md commit `0c4d324` explicitly notes:
*"A future git-filter-repo pass can scrub the history if needed."* That pass is
still pending.

**Remediation — exact steps:**

```bash
# 1. Install git-filter-repo (one-time)
pip install git-filter-repo

# 2. Create a replacements file
echo "[REDACTED-ROTATED-2026-06-20]==>REDACTED_TD021" > /tmp/replacements.txt

# 3. Run the scrub (rewrites history; back up first)
git filter-repo --replace-text /tmp/replacements.txt

# 4. Force-push ALL refs to every remote
git push --force --all
git push --force --tags

# 5. Notify all collaborators to re-clone — existing local clones retain the
#    old history and must be discarded.
```

> **Note:** The live Neo4j password has already been rotated. `[REDACTED-ROTATED-2026-06-20]` is
> no longer a valid credential at the database layer. The history scrub is a
> hygiene step to prevent credential-scanner alerts on future clones and to
> eliminate any DECISIONS.md documentation of the old value.

---

### [HIGH] SQLite extraction spool persists raw session transcripts in plaintext

**File:** `harness/extraction_queue.py:883` → `data/extraction_queue_spool.db`  
**Risk:** Every voice session's full transcript (including health disclosures) is written unencrypted to a SQLite file on disk before fact extraction runs.

`ExtractionQueue.enqueue()` at line 875 calls `json.dumps(turns_snapshot)` and
writes the serialised turns to `pending_jobs.turns` in `data/extraction_queue_spool.db`
for crash durability (TD-038). The `turns` column holds the raw `[{role, content}]`
transcript — e.g., `"I've been taking metformin 1000mg for six months"` — in
plaintext, in the same directory tree as the encrypted `:Fact` store. The spool
file persists until the extraction worker drains the queue and calls
`_delete_spooled`. A system crash, sleep, or slow Ollama call leaves the transcript
on disk indefinitely. The file is correctly gitignored (`data/extraction_queue_spool.db*`),
but no at-rest encryption is applied.

**Remediation:**
1. Encrypt the `turns` column using the member's owner key before writing to SQLite:
   `turns_enc = Fernet(derive_member_key(owner)).encrypt(json.dumps(turns).encode())`.
2. Alternatively, accept the risk for the local/household threat model and document it
   explicitly in KNOWN_ISSUES.md as a known cleartext-at-rest gap on the extraction
   spool.

---

### [MEDIUM] HKDF derivation uses `salt=None` — weakens domain separation

**File:** `harness/encryption.py:88`  
**Risk:** Absence of a salt means the KDF output is purely a function of the master key and the context string; cross-context collision requires only context-string reuse.

`HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=_HKDF_INFO_PREFIX + owner.encode())` uses no salt. RFC 5869 permits this but recommends a salt to provide an independent randomness source. The current design is safe as long as `_HKDF_INFO_PREFIX` is never reused for a different purpose (e.g., TLS key derivation, token signing) with the same master key. Given the master key is a dedicated 32-byte random file, this is a limited risk, but the pattern is fragile if the master key is ever reused across subsystems.

**Remediation:**  
Add a fixed, well-known random salt: `salt=b"\x8a\x3f…"` (32 bytes, generated once
and committed as a constant). Alternatively, derive the salt from a PBKDF2 pass over a
domain tag to make cross-purpose reuse impossible even if someone copies the key.

---

### [MEDIUM] `DEFAULT_MASTER_KEY_PATH` hard-codes the demo checkout path

**File:** `harness/encryption.py:44`  
**Risk:** If `$HIP_MASTER_KEY` is unset, the dev checkout reads/writes the same master key as the demo instance, making demo and dev fact stores share a cryptographic root.

`DEFAULT_MASTER_KEY_PATH = pathlib.Path.home() / "hip-harness" / "data" / "encryption" / ".master_key"` — this resolves to the demo checkout regardless of which repo directory the code runs from. The `.env.dev` file (committed at `01a8572`) correctly sets `HIP_MASTER_KEY` to a dev-specific path, so `dev.sh` sessions are isolated. However, any process that imports `harness.encryption` without sourcing `.env.dev` (e.g., a direct `python` call, a test runner, a script executed outside `dev.sh`) silently shares the production master key.

**Remediation:**  
Change `DEFAULT_MASTER_KEY_PATH` to resolve relative to the repo root:
```python
DEFAULT_MASTER_KEY_PATH = pathlib.Path(__file__).parent.parent / "data" / "encryption" / ".master_key"
```
This makes each checkout self-contained by default, without requiring the env var override.

---

### [MEDIUM] `SerpAPISearchClient` raises `ValueError` on bot startup if key is absent

**File:** `server/voice_orch.py:1869`  
**Risk:** Every WebRTC connection attempt fails with an unhandled exception if `SERPAPI_KEY` is unset; no degraded-local-only mode is possible.

`SerpAPISearchClient()` is instantiated unconditionally inside `async def bot(...)`.
Its `__init__` raises `ValueError("SERPAPI_KEY not set")` if the environment variable
is absent (`escalation_backends.py:362`). There is no `try/except` or conditional
instantiation. Since the bot function is the Pipecat entry point called per WebRTC
connection, a missing `SERPAPI_KEY` makes the server answer no voice calls at all —
even queries that would be routed locally. The launchd plist template has `REPLACE_ME`
as the placeholder; if deployed without replacing this value, the server is
permanently broken while appearing healthy at the `/health` endpoint.

**Remediation:**  
Wrap instantiation in a try/except and substitute a stub when the key is absent:
```python
try:
    _search = SerpAPISearchClient()
except ValueError:
    logger.warning("SERPAPI_KEY not set — web-fetch escalation disabled")
    _search = HttpWebSearchClient()  # stub that returns []
```

---

### [MEDIUM] Legacy `/chat` endpoint accepts arbitrary `user_id`

**File:** `server/app.py:16`  
**Risk:** Any caller can query the LLM as any user ID, and that user ID is written to the turn log.

The `ChatIn` model sets `user_id: str = "bill"` with no validation. `log_turn()`
writes `rec["user"] = inp.user_id` to `logs/turns.jsonl`. While this endpoint is
from the Phase 0 build and may not be on the live critical path, it remains reachable
and writes PII (the full message and reply) to the turn log without encryption or
access control.

**Remediation:**  
Remove or disable this endpoint in the orchestrator build, or add the same auth
header requirement as the `[CRITICAL]` finding above.

---

### [LOW] `/api/facts` exposes all-member fact metadata unauthenticated

**File:** `server/voice_https_orch.py:125`  
**Risk:** Attribute names, owners, sensitivity levels, and timestamps for every household member's facts are visible to any network peer without authentication.

`GET /api/facts` returns `attribute`, `owner`, `sensitivity`, `confidence`, and
`valid_from` for all active `:Fact` nodes across all members. While ciphertext and
encrypted DEKs are excluded, the attribute names themselves are sensitive
(`medication`, `health_condition`, `financial`, etc.) and the owner field identifies
which household member the fact belongs to.

**Remediation:** Protect with the same auth scheme as `[CRITICAL]`.

---

### [LOW] `/api/members` unauthenticated household roster enumeration

**File:** `server/voice_https_orch.py:217`  
**Risk:** Any network peer can enumerate all household member IDs, display names, and roles.

`GET /api/members` returns the full member registry — `member_id`, `name`, `role`,
`permission_level` — with no authentication. Member IDs are used as ownership keys
in the fact graph; knowing them aids member-impersonation attacks on `/api/text-query`
and `/api/decrypt`.

**Remediation:** Protect with the same auth scheme as `[CRITICAL]`.

---

### [LOW] `DEFAULT_DB_PATH` in member registry points at demo checkout

**File:** `harness/member_registry.py:38`  
**Risk:** Code executed from the dev checkout without `$HIP_REGISTRY_DB` reads/writes the demo's member registry.

`DEFAULT_DB_PATH = pathlib.Path.home() / "hip-harness" / "registry.db"` mirrors
the same cross-checkout sharing issue as the master key path. The `HIP_REGISTRY_DB`
env var override exists and is set in `.env.dev`, so `dev.sh` sessions are isolated.
Direct invocations without `.env.dev` silently operate on the demo registry.

**Remediation:** Same pattern as `encryption.py` — resolve relative to the file's
own `__file__` parent rather than a hardcoded `~/hip-harness` path.

---

## What an Operator's Security Team Would Flag First

1. **No API authentication on any endpoint** — The entire server surface (`/api/decrypt`,
   `/api/routing`, `/api/text-query`, `/api/reset`, `/api/facts`, `/api/members`) is
   unauthenticated. In a multi-tenant or household deployment with any network exposure,
   this is a Day 1 blocker. A shared API key in a `X-HIP-Key` header (stored in the
   launchd `EnvironmentVariables` alongside `NEO4J_PASSWORD`) would close all six
   unauthenticated endpoints in one change.

2. **Encryption subverted by an unauthenticated decrypt API** — The envelope encryption
   (TD-030) is carefully designed, but `/api/decrypt?member=sarah` returns the entire
   plaintext fact store for any member on a GET request. An operator who approved the
   encryption architecture would immediately flag that the threat model is completely
   inverted: the strongest threat (network attacker) bypasses the encryption trivially,
   while the weakest (local disk access) is the one being protected against.

3. **Git history contains cleartext credential** — Automated secret-scanning tools
   (GitHub secret scanning, truffleHog, gitleaks) will flag `[REDACTED-ROTATED-2026-06-20]` on first
   scan. Most enterprise security teams run these tools as a gate on new repositories.
   Even though the credential has been rotated, the finding blocks clean security
   certification until `git-filter-repo` is run and all collaborators re-clone.

---

*Live mic confirmation and NEO4J rotation still pending as of this audit.*
