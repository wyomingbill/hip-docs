COMPLETE WITH FINDINGS — 0 ITEMS FILED, NOTHING BLOCKING

# DISPATCH_HA49_SESSION_KEY_AND_COMMITMENT — step 2 built, and deliberately wired to nothing
Status: BUILT
Reconciled-Against: roadmap `bca2515` (HA-48) at start; landed this dispatch

**Dispatch ID: HA-49.** Authority: `REQ_TRANSCRIPT_STORAGE` as ratified, **step 2 of nine** — the
precondition for step 5.

**Built: the per-session content key and the durable member-keyed commitment.**
**No writer changed, no consumer changed, no corpus touched, and nothing calls either mechanism.**

---

## 1. WHAT EXISTS NOW, AND WHAT DOES NOT — item 5, stated plainly first

**EXISTS** (`harness/session_content_key.py`, 18 standing tests):

| thing | what it does |
|---|---|
| `SessionContentKey.create(session_id, members=…, operator=…)` | Mints a Fernet content key and wraps it to **exactly Q2's authorized set** — the speaking members plus the live operator |
| `.unwrap_for(member_id)` | Returns the key using **that member's own X25519 seal key**; `UnauthorizedMember` if they hold no wrap |
| `.seal(text)` / `.open_as(ct, member_id=…)` | Encrypt a turn / read it as an authorized member |
| `.end()` | Zeroes the buffer, drops every wrap; idempotent |
| `SessionKeyRegistry` / `REGISTRY` | The live sessions — a plain in-memory dict, **deliberately with no persistence layer** |
| `commit_turn(text, member_id=…)` | The **durable member-keyed commitment**, HMAC-SHA256 under the member's ledger key |
| `verify_turn_commitment(text, commitment, member_id=…)` | The governed read path; **reads the key without creating it** |

**DOES NOT EXIST, and this is the honest half:**

- **Nothing writes through this.** Verified, not asserted: a grep across `harness/`,
  `memory_engine/`, `server/` and `scripts/` finds **zero callers** outside the module itself.
- **Transcripts are not sealed.** `logs/transcript/` still receives verbatim words on every turn.
  **Row 19 is exactly as open as it was before this dispatch.**
- **No corpus was committed.** The 27,732 turns still carry no commitments; that is step 4.
- **`/api/transcript` is unchanged** — it still reads files and renders words. That is step 5,
  and this dispatch is its precondition, not its delivery.

**Stated this way round on purpose:** a module that exists and is called by nothing is easy to
mistake for a landed capability.

---

## 2. WHAT WAS BUILT, AND WHY IT IS SHAPED THIS WAY

### Two mechanisms, two existing key stores, no new scheme

The dispatch said reuse the proven mechanism and do not invent a second. **Nothing here is new
cryptography:**

| element | reused from |
|---|---|
| the wrap | `harness/dyad_crypto.seal_to_pubkey` / `unseal_from_privkey` (X25519) |
| the member seal keypair | `harness/member_seal_keys.ensure_member_seal_keypair` (`~/hip-keys/`) |
| the content cipher | `Fernet`, as in `harness/member_crypto` |
| the commitment | `harness/ledger_commitment.compute_keyed_commitment` (HEL 2.0, row 7) |
| the commitment key | `harness/epistemic_ledger._load_or_create_member_key` (`ledger/keys/`) |

**Two different key stores are in play and that is correct, not an inconsistency:** the wrap uses
the X25519 **seal** keypair; the commitment uses the 32-byte **ledger** key. Each is used for the
job it already does.

### Why the content key is session-scoped and the commitment is member-keyed

**Different lifetimes, so different keys.** The commitment must **outlive** the session — it is
what a durable record carries forever — so it keys to something durable, the member. The content
key must **not** outlive the session, because Q1 rules words recoverable only while the session
is live.

**Q2's erasure story then falls out of the construction rather than being layered on:** destroying
a member's key material makes their commitments unverifiable *and* any surviving wrap unopenable.
No policy check enforces either.

### The authorization set IS the wrap set

There is no permission list beside the wraps that could drift from them. An unauthorized member
is refused because **no ciphertext is addressed to them** — there is nothing for their key to
try. A test asserts the absence of a wrap rather than the presence of a "denied" flag.

### One thing deliberately NOT overclaimed

`end()` zeroes the key buffer, but **Python cannot guarantee no copy of the key remains in
process memory** — Fernet holds immutable `bytes` internally, uncontrollable from here. The
module's docstring says so. **The property actually guaranteed, and the one the twin verifies, is
that the key never reached DISK.** Claiming memory erasure would have been the more dangerous
error, and the twin would not have caught it.

---

## 3. FAULT TWINS — each proven RED by injecting its own defect, then restored

| twin | defect injected | result |
|---|---|---|
| **Unauthorized member cannot unwrap** | `unwrap_for` falls back to any available wrap | **2 failed** — `…cannot_unwrap`, `…cannot_read_sealed_content` |
| **Key is absent from disk after the session ends** | `create()` persists the key to `logs/` | **1 failed** — `…never_written_to_disk` |
| **Commitment fails on a tampered copy** | `verify_turn_commitment` returns True unconditionally | **2 failed** — `…fails_on_a_tampered_copy`, `…is_member_keyed_not_global` |

**Restored after each injection from a pre-edit copy; zero `DEFECT` markers remain; 18/18 green.**
The defect artifact directory the second injection created was removed.

### The disk twin SEARCHES, and carries its own anti-vacuity

"We never write it" is the claim under test, so the twin reads bytes off the filesystem: it walks
`logs/`, `ledger/`, `~/hip-keys/` and `harness/` looking for the raw content key **and** the wrap.

**It also searches for a control value that IS on disk**, so a searcher that can find nothing at
all — a broken glob, a wrong root — cannot pass by finding nothing.

---

## 4. ANTI-VACUITY — item 4

A key nobody can open would satisfy every refusal above. Each negative is therefore paired:

- **An authorized member CAN unwrap and read during the session** — all three of the speaking
  members and the operator round-trip `seal` → `open_as` and get the exact words back.
- **Commitments verify for all three current members** — `bill`, `maya`, `sam` each mint and
  verify, which is the corpus step 4 must commit.
- **A session with no authorized member is REFUSED**, not silently created — a key nobody can
  open would discard a session's words rather than protect them.
- **Session scoping is real**: session A's unwrapped key does not decrypt session B's content,
  while B's own member still reads B's content.
- **The commitment is not a bare digest** of the words (§3B) — asserted against both
  `sha256(text)` and `sha256(json)`.
- **`verify_turn_commitment` mints no key material** when the key is gone: the keys dir is
  asserted empty before and after, so the post-erasure state is observed rather than repaired.
- **A commitment that cannot be minted returns `None`, never the words.**

---

## 5. RUNS

Repo `.env.dev` sourced (`NEO4J_URI=bolt://localhost:7688`), never `~/.env.dev`.

| command | result |
|---|---|
| **Standing binding battery**, 58 files | **1197 passed / 0 failed / 9 xfailed** — was 1179/57; **+18 is exactly this dispatch's battery** |
| **`--layer 7`** | **EXIT 0.** L7 **27/27**, L7V2 **27/28** (1 skipped), AUDIT **9/9**, DISC 1/1, SCHEMA 1/1, VOICE 1/1 |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| **Memory harness** | **13/17** — inside the 13–15 pin. Not 16/17, so no STOP |

**No deterministic regression.** No live reds to report: `--full` was not run — this dispatch
changed no live path and asked for no collector run.

`eval/test_session_content_key.py` is **registered in `scripts/run_harness.sh`**, so the manifest
check cannot classify it as a silent skip.

**Corpus untouched:** `logs/transcript/` still 425 + 425 files and 27,732 lines. `recall_audit.jsonl`
moved 364 → 368 from the harness runs themselves, and those four entries carry commitments, not
words.

---

## 6. WHAT THIS UNBLOCKS, AND WHAT IT DOES NOT

**Unblocks step 5.** The read path can now express Q2's *"for whom"*: an in-memory band backed by
this key shows a viewer only what they hold a wrap for. Building step 5 before this existed would
have produced a buffer that was private only by accident of deployment — which is precisely why
Bill named step 2 as its precondition.

**Does not unblock steps 1, 4 or 7.** The source fix, the historical commitment mint and the
erasure still stand where they did, in that order. **The critical order is unchanged: source fix
→ commitments while keys exist → historical erasure → key destruction.**

**The commitment window is still open and still closing.** bill, maya and sam all hold keys, so
100% of the 27,732 turns remain committable — but **nothing has been committed yet**, and step 4
is what spends that window.

---

## CLAIM IMPACT

**none.**

C-09 is what this bears on and it gains nothing: **a mechanism with no caller changes no
observable behaviour.** Status is computed from standing runs by the generator, never declared by
a session.

---

## RECAP

**HA-49** — built step 2: the **per-session content key** (Fernet content key wrapped via X25519
to exactly Q2's authorized set, in memory only, gone at `end()`) and the **durable member-keyed
commitment** (`commit_turn` / `verify_turn_commitment`, HMAC under the member's ledger key, verify
never creating a key). **No new cryptography — every primitive reused.** **Three twins proven RED
by injected defects then restored** (authorization removed → 2 red; key persisted → 1 red;
verification always-true → 2 red); the disk twin **searches the filesystem and carries its own
anti-vacuity control.** Binding **1197/0/9xf**, layer 7 **exit 0**, RATCHET **PASS**, memory
**13/17**. **NOTHING IS WIRED: zero production callers, transcripts still write verbatim words,
row 19 is exactly as open as before.** Nothing ruled MET.
