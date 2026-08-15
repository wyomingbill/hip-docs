COMPLETE WITH FINDINGS — 0 ITEMS FILED, NOTHING BLOCKING

# DISPATCH_HA49A_ENVELOPE_BOUND — the envelope bound, the key split, and the honest answer on operator access
Status: BUILT
Reconciled-Against: roadmap `f384259` (HA-49) at start; landed this dispatch

**Dispatch ID: HA-49A.** Authority: external review of HA-49, accepted by Bill.

**Still zero production callers. No writer change, no consumer change, no corpus touch.**
Transcripts still write verbatim words; **row 19 is exactly as open as it was.**

---

## 1. WHAT WAS BOUND — item 1

**Fernet is gone from this path.** It authenticates its ciphertext but carries **no context**, so
a valid encrypted utterance could be moved between sessions, turns or members and still verify.
The content cipher is now **AES-256-GCM with AAD** — not a new dependency; `epistemic_ledger`
already uses AESGCM.

**Every envelope binds five fields as additional authenticated data:**

```
{"v":"HIP-SESSION-ENVELOPE-v1","session_id":…,"turn_id":…,
 "member_id":…,"content_type":…,"epoch":…}
```

canonicalized by the same `_canon` convention (`sort_keys`, tight separators) the ledger uses.

**Checked on decrypt, in two independent gates:**

1. **The envelope must belong to THIS session** — an explicit equality check, so a whole-envelope
   move is refused *by name* rather than surfacing as a confusing decrypt failure.
2. **The AAD is re-derived from the envelope's own fields**, so tampering with `turn_id`,
   `member_id`, `content_type` or `epoch` makes the ciphertext undecryptable.

**A mismatch raises `EnvelopeBindingError` before any plaintext exists, and never returns
plaintext.**

---

## 2. THE KEY IS SPLIT — and this is what makes item 4 answerable

**The reviewer's point was real:** a wrap is sealed to a member's **long-lived** X25519 key, so a
persisted wrap would stay unwrappable forever. Wrapping the content key directly would mean
operator access never dies.

**So the content key is derived, not wrapped:**

```
content_key = HKDF-SHA256(share, salt=session_salt,
                          info=b"hip-session-content:v1:" + session_id)
```

- **`share`** — 32 random bytes, **wrapped** to each authorized member.
- **`session_salt`** — 32 random bytes, **never wrapped, never written, dies at `end()`.**

HKDF with a versioned info prefix matches `harness/encryption.py`'s existing
`hip-fact-envelope:v1:` pattern.

### Item 4, answered with both halves shown

> **The unwrap SUCCEEDS. The read still FAILS.**

`open_persisted_wrap()` exists precisely to demonstrate this and says so in its docstring. After
`end()`, a persisted wrap plus the operator's long-lived private key **does** yield the share —
that is the honest half, and pretending otherwise would have been the easy lie. **The share
alone cannot reconstruct the content key**, because the salt it was derived with is gone.

The twin proves both halves in one test: the unwrap returns 32 bytes, the derived key differs
from the real one, and decryption fails.

---

## 3. DOMAIN SEPARATION — item 2, with the exact bytes

**Exactly these five fields are canonicalized and committed:**

```
{"v":"HIP-TURN-COMMITMENT-v1","session_id":…,"turn_id":…,"member_id":…,"text":…}
```

serialized by `ledger_commitment`'s own `_canon` — **one convention in the codebase, not two** —
then HMAC-SHA256'd under the member's ledger key.

`"v"` is the **domain separator**. A different record type must use a different string, so two
record types cannot produce interchangeable commitments. **Asserted by a test that changes the
separator and requires the commitment to move.**

The commitment is now **bound to session and turn as well as member**: the same words in a
different turn produce a different commitment, and verification fails if any of the three is
wrong.

---

## 4. THE LIFECYCLE CASES — answered in code (item 3)

**Mechanism: authorization EPOCHS.** Each epoch has its own share and salt; wraps exist only for
the members authorized in that epoch.

| case | built behaviour | why |
|---|---|---|
| **Member joins mid-session — can they read earlier turns?** | **NO.** Authorising opens a **new epoch**; the joiner gets wraps from there on and none for earlier epochs. | **Least privilege.** They were not present. The alternative — one key per session — is one line simpler and silently hands a late joiner the entire backlog. |
| **Member leaves / authorization revoked** | **Forward-only.** They keep the ability to open epochs they were authorised for; no wrap for any later one. | They already saw those turns. Retroactive removal would be theatre — the words were on their screen. |
| **Operator changes** | A revoke plus an authorise at one epoch boundary. The old operator cannot read later turns; the new one cannot read earlier ones. | Same rule, applied twice. |
| **Same member reconnects** | Nothing happens — they hold whatever wraps they held. **A test asserts the epoch does not advance.** | Reconnection is not an authorization event; treating it as one would silently cut them off from the session they are still in. |
| **`end()` called twice** | Idempotent; every epoch's share, salt and wraps dropped. | — |
| **Crash before `end()`** | Everything is lost, because nothing was ever written. | The registry has **no persistence layer, deliberately** — Q1's rule enforced by construction rather than by a retention policy. A fresh registry stands in for the restarted process in the twin. |
| **Revoking the last member** | **Refused.** | A session nobody can open would discard its words rather than protect them. |

---

## 5. TWINS — every one proven RED by an injected defect, then restored

| defect injected | tests that went red |
|---|---|
| **AAD removed** (`encrypt(..., None)`) | **5** — another-turn, another-member, content-type, tampered-metadata, identical-utterances |
| **Session salt removed** (`salt=None` in HKDF) | **1** — the persisted-wrap/operator twin |
| **Epochs removed** (add the wrap to the current epoch) | **1** — late joiner reads earlier turns |
| **Commitment domain separation removed** (`{"text": text}`) | **2** — session/turn/member binding, interchangeable record types |
| **Memory overclaim introduced** into the docstring | **1** — the overclaim guard |

**Restored from a pre-edit copy after each; zero `DEFECT` markers remain; 30/30 green.**

**Twins required by item 5, all present and all red under their defect:** ciphertext from another
session; from another turn; attributed to another member; a wrap copied to another session; one
member cannot substitute another's wrap; restart cannot recover prior-session words; `end()`
idempotent; a missing member ledger key fails verification **and never recreates the key**;
tampered metadata fails with the ciphertext byte-identical; two identical utterances in different
turns are not interchangeable.

**The disk twin searches** `logs/`, `ledger/`, `~/hip-keys/` and `harness/` for the **share, the
salt and the wrap**, and carries an anti-vacuity control so a searcher that can find nothing at
all cannot pass.

---

## 6. THE MEMORY CLAIM WAS NOT STRENGTHENED — item 6

**Audited the module, the REQ, the HA-49 dispatch doc and the handoff.** Every existing phrasing
is *"held in memory"*, *"never written"*, *"no persistence layer"* — all accurate. **No overclaim
was found, so nothing needed correcting.**

Two things were added rather than corrected:

- **A standing test** (`test_the_module_does_not_overclaim_memory_erasure`) that fails if the
  module ever acquires phrasing like *"guarantees no copy"* or *"wiped from memory"*, and
  requires the disk-absence sentence to remain.
- **An explicit boundary note in the REQ's Q3**, stating that the guaranteed property is *"the
  key never reached disk"* and **not** memory erasure, with the reason: Python cannot guarantee
  it, `bytes` are immutable, and the cryptography library holds its own copies.

**The claim is now pinned from both sides — stated in the contract, and enforced by a test.**

---

## 7. RUNS

Repo `.env.dev` sourced (`NEO4J_URI=bolt://localhost:7688`), never `~/.env.dev`.

| command | result |
|---|---|
| **Standing binding battery**, 58 files | **1209 passed / 0 failed / 9 xfailed** — was 1197; **+12 is this battery growing 18 → 30** |
| **`--layer 7`** | **EXIT 0.** L7 **27/27**, L7V2 **27/28** (1 skipped), AUDIT **9/9**, DISC 1/1, SCHEMA 1/1, VOICE 1/1 |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| **Memory harness** | **13/17** — inside the 13–15 pin. Not 16/17, so no STOP |

**No deterministic regression.** No live reds: `--full` was not run — no live path changed.

**Still zero production callers**, verified by grep. **Corpus untouched:** 425 + 425 transcript
files, 27,732 lines.

---

## 8. WHAT THIS DOES AND DOES NOT CHANGE

**Changes:** the step-2 mechanism is now safe to wire. An envelope cannot be moved between
sessions, turns or members; a late joiner cannot read the backlog; a persisted wrap is inert once
the session ends; two record types cannot produce interchangeable commitments.

**Does not change:** **nothing is wired.** Transcripts still write verbatim words, no corpus is
committed, `/api/transcript` still reads files. Steps 1, 4, 5 and 7 all stand where they did.
**The critical order is unchanged: source fix → commitments while keys exist → historical erasure
→ key destruction.**

**The commitment window is still open and still unspent** — bill, maya and sam all hold keys, so
100% of the 27,732 turns remain committable, and **nothing has been committed yet.**

---

## CLAIM IMPACT

**none.** C-09 gains nothing: **a mechanism with no caller changes no observable behaviour**, and
hardening an unwired mechanism does not move a claim. Status is computed from standing runs by
the generator, never declared by a session.

---

## RECAP

**HA-49A** — **bound the envelope**: AES-256-GCM with AAD over
`{v, session_id, turn_id, member_id, content_type, epoch}`, re-derived and checked on decrypt,
plus an explicit session check. **Split the key** into a wrapped share and an in-memory-only
salt, which is what makes the operator answer true: **the persisted wrap still unwraps, and the
read still fails.** **Domain-separated the commitment** under `HIP-TURN-COMMITMENT-v1`, bound to
session, turn and member. **Answered the lifecycle in code with epochs — a late joiner CANNOT
read earlier turns; revocation is forward-only.** **Five defect classes proven red then
restored**, 30/30 green. **Memory claim audited and not strengthened** — no overclaim existed;
added a standing guard test and an explicit REQ boundary note. Binding **1209/0/9xf**, layer 7
**exit 0**, RATCHET **PASS**, memory **13/17**. **Still zero callers; row 19 unchanged.** Nothing
ruled MET.
