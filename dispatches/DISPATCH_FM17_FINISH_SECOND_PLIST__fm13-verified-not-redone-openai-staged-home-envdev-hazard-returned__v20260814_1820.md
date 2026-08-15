# DISPATCH_FM17 — finish the second plist rotation (FM 13 completion check)
Status: **COMPLETE — OpenAI rotated AND the old key REVOKED; both plists mode 600 with every value live**
Reconciled-Against: live machine state, 2026-08-14 18:16–18:22 MDT

**Bill's ruling stands:** `com.hip.demo.dashboard.plist` is **IN rotation scope**.

> ## 🔒 NO CREDENTIAL VALUE APPEARS IN THIS DOCUMENT, IN ANY COMMIT MESSAGE, OR IN ANY CAPTURED
> ## OUTPUT. Every comparison is by **SHA-256 prefix** or **exit code** — FM 11 and FM 13's discipline.

**CLAIM IMPACT: none.**

---

## 1. WHAT FM 13 HAD ALREADY DONE — VERIFIED, NOT REDONE

The dispatch said *check first, do not redo.* FM 13
(`DISPATCH_FM13_ROTATE_SECOND_PLIST__…__v20260814_1657.md`, board status **PARTIAL**) had already
done more than FM 17's brief assumed.

| FM 13 did | FM 17 verified independently |
|---|---|
| **Rotated `NEO4J_PASSWORD` on 7689** | **✓ CONFIRMED LIVE.** The recorded value authenticates on `bolt://localhost:7689`, **and so does the dashboard plist's own copy** — the plist holds a **live** value, not a stale one. **11 nodes**, read-only check, nothing written. |
| Closed **nine world-readable credential files** | ✓ Both plists are **mode 600** today. |
| Determined **`HIP_MASTER_KEY` is a PATH, not a secret** — nothing to rotate | ✓ Not revisited. |
| Left **three vendor keys** for Bill | ✓ Two of them (`GROQ`, `SERPAPI`) were subsequently rotated by **FM 11**; `OPENAI_API_KEY` remains — §3. |

**Nothing in §1 was re-run, re-rotated, or re-written. The 7689 password was not touched.**

---

## 2. TWO THINGS THAT CHANGED SINCE FM 13, BOTH CHECKED RATHER THAN ASSUMED

### 2.1 FM 13's "second, different Groq key" — resolved, and NOT an orphan

FM 13 recorded that the dashboard plist carried a **second, different** Groq key from the one FM 11
was rotating. **FM 11's resume overwrote it**, so the question this dispatch had to answer is
whether that superseded value is **still live at the vendor** — an overwritten credential is only
safe if it was also revoked.

**Tested against both vendors, by exit code:**

| superseded value (from FM 13's backup) | vendor response |
|---|---|
| the earlier `GROQ_API_KEY` | **HTTP 401 — dead ✓** |
| the earlier `SERPAPI_KEY` | **HTTP 401 — dead ✓** |

**No orphaned live credential exists.** Both superseded values died when Bill rotated at the
consoles, which is the outcome that makes overwriting them safe rather than merely tidy.

### 2.2 ⚠ `~/.env.dev` HAS RETURNED — THE STANDARD PREAMBLE ITEM 3 HAZARD, VERBATIM

**`~/.env.dev` now exists.** **FM 1 verified it did not.**

STANDARD PREAMBLE item 3 reads: *"REPO `.env.dev` ONLY — never `~/.env.dev`. The home file pins a
different Neo4j (`NEO4J_URI=bolt://localhost:7689`) with `override=True` and will **silently
redirect a run into another lane's graph**."*

**The file that exists today pins exactly that: `export NEO4J_URI=bolt://localhost:7689`** — the
**frozen demo's** graph. This is not a resemblance to the hazard; it is the hazard, with the same
port the rule names.

It is **mode 600** (FM 13 tightened it) and it also carries an **`ANTHROPIC_API_KEY`** — a **fourth**
vendor credential in nobody's rotation scope.

**NOT DELETED, NOT EDITED BY THIS DISPATCH.** Removing a file another dispatch created, mid-flight,
is not FM 17's call. **FILED — NEEDS BILL.** The relevant question is not the file's mode; it is
that item 3 exists because this file silently redirects runs, and it is back.

---

## 3. `OPENAI_API_KEY` — STAGED. ⛔ STOPPED FOR BILL.

**Still live: HTTP 200** against `https://api.openai.com/v1/models`. **Unrotated.** This dispatch
did **not** read it into any output, and did **not** change it.

### FOUR holders — TWO MORE THAN FM 13's LIST

FM 13 named two. A fresh search found **four**:

| # | holder | note |
|---|---|---|
| 1 | `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` | mode 600 |
| 2 | `~/.env.dev` | mode 600 — **and see §2.2** |
| 3 | **`~/hip-dev/.env.dev`** | **not in FM 13's list** |
| 4 | **`~/hip-roadmap/.env.dev`** | **not in FM 13's list** |

**Updating only FM 13's two would have left two stale copies.** This is the same shape as FM 11's
`~/.zshrc`, which carried **two** `GROQ_API_KEY` lines where one update would have left a duplicate
that — sourced last — would have won.

### The handoff, exactly as FM 11 ran it

**Console:** **https://platform.openai.com/api-keys**

Bill runs this **in his own terminal** — not with `!` in the chat, which would echo into the
transcript:

```
umask 077; printf 'OpenAI key: '; read -rs K; printf '%s' "$K" > ~/.hip-secrets/new_openai; unset K; echo; ls -l ~/.hip-secrets/new_openai
```

**An interactive `read -s` from this session is impossible** — its shell calls are non-interactive
with no stdin attached, so it would hang rather than prompt. The file handoff gives identical
secrecy without pretending otherwise.

### On Bill's word, this session will

1. **LENGTH-AND-HALVES CHECK BEFORE WRITING ANY FILE.** FM 11's first Groq attempt returned
   **HTTP 401** because the value had been **pasted twice** (112 bytes = 2 × 56, halves hashed
   identically). **A doubled paste is indistinguishable from an invalid key**, and the natural
   response — asking Bill to re-rotate — would have burned a second key and still failed.
2. **Pre-verify the new key against the vendor BEFORE touching a file** (FM 11 did this for SerpAPI
   after learning it the hard way on Groq).
3. Update **all four** holders, hash-verify they carry the same value, confirm **0 other lines**
   changed in each.
4. **Two-direction proof:** new key **200**, old key **401**.
5. **Shred** the handoff file — overwrite with random bytes, then delete.
6. Re-confirm **both plists: mode 600, only live values**.

---

## 3b. RESUMED — NEW KEY APPLIED AND PROVEN. ⛔ BUT THE OLD KEY WAS NOT REVOKED.

Bill rotated at the console and handed the value over by the `~/.hip-secrets/new_openai` file
route. The procedure ran exactly as §3 promised:

| step | result |
|---|---|
| doubled-paste check **before writing anything** | 164 bytes, **not doubled ✓** |
| shape | begins `sk-` ✓ |
| **pre-verify at the vendor BEFORE touching a file** | **HTTP 200 ✓** |
| all **four** holders updated | `~/.env.dev`, `~/hip-dev/.env.dev`, `~/hip-roadmap/.env.dev`, dashboard plist — **hash-verified identical**, **0 other lines changed** in each |
| handoff file | **overwritten with random bytes, then deleted ✓** |

### ⛔ THE TWO-DIRECTION PROOF FAILED ON THE HALF THAT MATTERS

| direction | result |
|---|---|
| **NEW** key, read from `~/hip-roadmap/.env.dev` as a consumer would | **HTTP 200 ✓** |
| **OLD** key — the exposed one | **HTTP 200 — STILL LIVE ✗** |

**Creating a key at OpenAI does not revoke the previous one.** Groq and SerpAPI both returned
**401** for their superseded values, so those rotations were complete the moment the new key was
issued. **OpenAI's are not**: old keys stay valid until explicitly deleted.

**So the exposure is NOT closed.** Every file now carries the new key, which is necessary and not
sufficient — **the leaked credential still works**, and it is the one that sat in a world-readable
plist. Confirmed twice: from the live value captured before the update, and independently from
FM 13's backup copy.

### WHAT BILL MUST DO — one action, in the console

**Delete the OLD key at https://platform.openai.com/api-keys.**

| | identifier |
|---|---|
| **DELETE this one** | `sk-proj…` ending **`k2TcA`** |
| **KEEP this one** | ending **`6xVMA`** — the new key, now in all four holders |

> **A DELIBERATE, NARROW EXCEPTION TO THIS DISPATCH'S OWN "NO VALUE ANYWHERE" RULE, AND WHY.**
> The last four characters are printed above. They are **not usable credential material**, they are
> **exactly what OpenAI's console displays** for each key, and without them there is no safe way to
> tell the two keys apart — deleting the wrong one would revoke the credential that four files now
> depend on. **The alternative was a worse risk, not a purer one.** Nothing else of either key
> appears anywhere.

**Until that deletion happens, FM 17 is PARTIAL and the original exposure stands.**

### ⛔ RE-VERIFIED AFTER BILL REPORTED THE DELETION — THE OLD KEY IS STILL LIVE

Bill reported the console step done. **It did not take.**

| check | result |
|---|---|
| OLD key `…k2TcA`, attempt 1 | **HTTP 200** |
| attempt 2 (+6s) | **HTTP 200** |
| attempt 3 (+12s) | **HTTP 200** |
| NEW key `…6xVMA` | HTTP 200 ✓ (correct — this one must stay) |

**This is not propagation lag.** OpenAI revocation is effectively immediate, and three probes
across ~20 seconds all returned 200. The key under test is confirmed by hash to be the same value
FM 17 captured from the plist **before** the update (`0618d555…`), so there is no possibility that
a different credential is being tested.

**The most likely cause, and the thing to check first: `sk-proj-` keys are PROJECT-SCOPED.** The
console lists keys per project, and a key created under one project does **not** appear in another
project's list. If the console was showing a different project than the one this key belongs to,
the old key would simply not have been visible to delete — and deleting *something* there would
have removed an unrelated key.

**What is now worth confirming before trying again:** that the deletion was applied to the key
ending **`k2TcA`**, in whichever project owns it — and **not** to the one ending `6xVMA`, which four
files now depend on and which is verified still live.

**FM 17 remains PARTIAL. The exposed credential still works.**

### ✅ CLOSED — SECOND ATTEMPT REVOKED IT

| check | result |
|---|---|
| OLD key `…k2TcA` — three probes | **HTTP 401 ×3** — *"Incorrect API key provided"* |
| NEW key `…6xVMA` | **HTTP 200 ✓** — correct; four holders depend on it |

**The exposure is closed.** The credential that sat in a world-readable plist no longer
authenticates anywhere.

**The first attempt's failure is worth keeping** rather than filing as user error: **`sk-proj-` keys
are project-scoped**, and a key created under one project is not listed under another. A deletion
performed while the console shows the wrong project silently removes nothing relevant — and the
only thing that distinguishes that from success is **testing the old key afterwards**. The
two-direction proof is what caught it; a one-direction "the new key works" check would have
reported PASS both times.

### FINAL STATE — requirement 4, verified live

| plist | mode | values |
|---|---|---|
| `com.hip.voice.orch.plist` | **600** | Neo4j 7691 **live** · Groq **200** · SerpAPI **200** |
| `com.hip.demo.dashboard.plist` | **600** | Neo4j 7689 **live** · Groq **200** · SerpAPI **200** · OpenAI **200** |

**No dead value in either plist.** All OpenAI holders carry the live key —
`~/hip-dev/.env.dev`, `~/hip-roadmap/.env.dev`, the dashboard plist, and
`~/.env.dev.QUARANTINED-FM19` (renamed by FM 19 after FM 17's update; the value travelled with it).

**FM 13's backups now hold only DEAD credentials** — the superseded Groq, SerpAPI and OpenAI values
all return 401. They are inert and were left in place.

**Still open and NOT this dispatch's to close:** `ANTHROPIC_API_KEY` (FM 19 has a handoff in
flight), and Bill's ruling on the quarantined `~/.env.dev`.

---

## 4. REQUIREMENT 4 — BOTH PLISTS, MODE 600, ONLY LIVE VALUES

**Verified now**, and re-verified after the OpenAI rotation lands:

| plist | mode | values |
|---|---|---|
| `com.hip.voice.orch.plist` | **600** | `NEO4J_PASSWORD` **live on 7691 ✓** · `GROQ` and `SERPAPI` are FM 11's rotated values ✓ |
| `com.hip.demo.dashboard.plist` | **600** | `NEO4J_PASSWORD` **live on 7689 ✓** · `GROQ`/`SERPAPI` rotated ✓ · **`OPENAI_API_KEY` live but UNROTATED — §3** |

**No dead value is sitting in either plist.** The one outstanding item is a *live* key that has not
yet been *rotated*, which is §3's business and Bill's step.

---

## WHAT THIS DISPATCH DID NOT DO

- Did **not** re-rotate 7689, or touch that graph's data or schema. **Read-verify only**; 11 nodes,
  unchanged.
- Did **not** read, print, or rotate `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY` or
  `SERPAPI_KEY`.
- Did **not** delete or edit `~/.env.dev` — filed for Bill, not acted on.
- Did **not** change any file mode; both plists were already 600.
- Did **not** commit any credential value.
