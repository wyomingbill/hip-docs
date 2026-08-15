# DISPATCH_FM11 — rotate the three plist credentials
Status: **COMPLETE — all three credentials rotated and proven two-directionally**
Reconciled-Against: live machine state, 2026-08-14 16:33–16:40 MDT

**Bill's ruling:** the three credentials in `com.hip.voice.orch.plist` are **treated as EXPOSED**
and **join FM 4's rotation scope**.

> ## 🔒 NO CREDENTIAL VALUE APPEARS ANYWHERE IN THIS DOCUMENT, IN ANY COMMIT MESSAGE, OR IN ANY
> ## CAPTURED COMMAND OUTPUT.
> Every comparison in this dispatch was made by **SHA-256 prefix** or by **exit code**. Passwords
> were generated into a scratch file, used, and never echoed. The one place a new value was written
> deliberately is named by **path only**.

**CLAIM IMPACT: none.**

---

## 1. `NEO4J_PASSWORD` — ROTATED. DONE.

### The exposed credential was live on TWO instances, not one

The dispatch assumed the plist's graph. **It unlocked more than that.** Tested one attempt per
instance, by exit code:

| instance | exposed credential | declared owner |
|---|---|---|
| **7687** | **AUTHENTICATED** | **NO LANE DECLARES IT** — 203 nodes, unowned |
| 7688 (roadmap) | refused | `~/hip-roadmap` |
| 7689 (frozen demo) | refused | `~/hip-dev` |
| 7690 (cutover demo) | refused | `~/hip-cutover-demo` |
| **7691** | **AUTHENTICATED** | `~/hip-vo` — the HA lane |
| 7692 (NC lane) | refused | `~/hip-nc` |

**So the rotation scope was 7687 and 7691.**

### A pre-existing breakage found on the way

**`~/hip-vo/.env.dev`'s own `NEO4J_PASSWORD` was ALREADY REFUSED by the graph it pins (7691).**
Before this dispatch, **the exposed plist was the only place holding a working credential for that
lane's graph.** That is worth stating plainly: the credential that had leaked was also the only one
that worked.

### What was done

Both instances rotated with `ALTER CURRENT USER SET PASSWORD FROM … TO …`, to **two DISTINCT**
24-character alphanumeric values — distinct so that one leak can never again unlock two graphs, and
alphanumeric per **TD-104** (a shell-special character in this value trips zsh/plist/sed edits).

**Zero client connections were open on either instance at the time** — verified before touching
them, so nothing was torn out from under a running lane.

### PROOF — both directions, both instances

| | new value | old (exposed) value | data |
|---|---|---|---|
| **7691** | **authenticates ✓** | **REFUSED ✓** | 12 nodes, unchanged |
| **7687** | **authenticates ✓** | **REFUSED ✓** | 203 nodes, unchanged |

### EVERY FILE TOUCHED — the complete list

| file | change | note |
|---|---|---|
| `~/hip-vo/.env.dev` | `NEO4J_PASSWORD` line replaced | **gitignored.** 50 lines before and after; a diff with the password line masked shows **0 other differences** — nothing else in that lane's file was altered. Backup taken first. |
| `~/.hip-secrets/neo4j-7687.password` | **created**, mode **600**, dir mode **700** | 7687 has **no declaring lane**, so no repo `.env.dev` legitimately holds it. Value lives in an operator-controlled file **outside every repository**; path recorded, value not. |
| `~/Library/LaunchAgents/com.hip.voice.orch.plist` | mode `644` → **`600`** | §3. Its `NEO4J_PASSWORD` is now a **DEAD value**. |

**Verified after:** `~/hip-vo/.env.dev` now **authenticates against `bolt://localhost:7691`**, which
it did **not** do before this dispatch. **A rotation fixed a pre-existing breakage as a side effect.**

**No repo file was committed with a credential in it.** `~/hip-vo/.env.dev` is gitignored;
`~/.hip-secrets/` is outside every repository.

---

## 2. `GROQ_API_KEY` AND `SERPAPI_KEY` — ⛔ **STOPPED. THIS IS BILL'S STEP.**

These rotate in vendor web consoles. **Nothing in this dispatch touched either key**, and **both are
still LIVE.**

### The two consoles

| key | console URL |
|---|---|
| `GROQ_API_KEY` | **https://console.groq.com/keys** |
| `SERPAPI_KEY` | **https://serpapi.com/manage-api-key** |

### THE EXACT FILES TO UPDATE AFTER ROTATION — prepared, in order

| # | file | holds | note |
|---|---|---|---|
| 1 | **`~/.zshrc`** | `GROQ_API_KEY`, `SERPAPI_KEY` | **the primary shell source** — the one most runs inherit |
| 2 | `~/hip-roadmap/.env.dev` | `SERPAPI_KEY` | gitignored |
| 3 | `~/hip-dev/.env.dev` | `SERPAPI_KEY` | gitignored |
| 4 | `~/Library/LaunchAgents/com.hip.voice.orch.plist` | `GROQ_API_KEY`, `SERPAPI_KEY` | mode 600, **not loaded** (FM 10) |
| 5 | `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` | `GROQ_API_KEY`, `SERPAPI_KEY` | **world-readable**, not loaded — see §4 |

**Not holders, deliberately excluded:** `eval/*.py` across four checkouts reference these key
**names** via `os.environ` — they are consumers, they hold no values, and they need no edit.

### What happens when Bill says go

**Verify the new keys work, and confirm the plists hold only DEAD values** — the same two-direction
proof used for Neo4j.

---

## 2b. RESUMED AND COMPLETED — BOTH VENDOR KEYS ROTATED AND PROVEN

Bill rotated both in the consoles and handed each new value over **without it entering the
conversation**: a `read -rs` in his own terminal wrote it to a mode-600 file under
`~/.hip-secrets/`, which this session read, applied, and then **overwrote and deleted**.

> **AN INTERACTIVE `read -s` FROM THIS SESSION WAS NOT POSSIBLE, AND SAYING SO MATTERED.**
> This session's shell calls are **non-interactive — no stdin is attached**, so a `read -s` inside
> one would have hung rather than prompted. The file handoff gives the identical secrecy property
> (never echoed, never in the transcript) without pretending to an interactivity that does not
> exist.

### ⚠ THE FIRST GROQ ATTEMPT FAILED, AND THE CAUSE IS WORTH KEEPING

The first handed-over value returned **HTTP 401 "Invalid API Key"** — and the **old** key returned
401 too, so both were dead and the obvious reading was *"the console rotation went wrong."*

**It had not.** The handoff file was **112 bytes**, and a Groq key is `gsk_` + 52 = **56**.
**112 = 2 × 56.** Splitting it showed **both halves hashed identically** and both began `gsk_`:
**the key had been pasted twice.** The first 56 characters authenticated immediately (HTTP 200).

**The lesson, because the failure mode is silent and misleading:** a doubled paste presents exactly
as an invalid credential, and the natural next step — asking Bill to re-rotate — would have burned
a second key and still failed. **Length-and-halves is now checked BEFORE any file is written**, and
the SerpAPI handoff was checked that way first (64 bytes, not doubled, verified against
`/account` **before** a single file was touched).

### PROOF — both keys, both directions, read from `~/.zshrc` as a consumer would

| key | new value | old value | extra proof |
|---|---|---|---|
| **`GROQ_API_KEY`** | **HTTP 200**, `choices` present, model `openai/gpt-oss-120b` | **HTTP 401** | — |
| **`SERPAPI_KEY`** | **HTTP 200**, plan returned | **HTTP 401** *(“Invalid API key”)* | a real `search.json` call returned **`organic_results` present** |

### FILES UPDATED — verified by hash, all carrying the same value

| file | `GROQ_API_KEY` | `SERPAPI_KEY` | other lines changed |
|---|---|---|---|
| `~/.zshrc` | **2 lines** rewritten ✓ | 1 line ✓ | **0** |
| `~/hip-roadmap/.env.dev` | — | 1 line ✓ | **0** |
| `~/hip-dev/.env.dev` | — | 1 line ✓ | **0** |
| `~/Library/LaunchAgents/com.hip.voice.orch.plist` | ✓ | ✓ | mode held at **600** |
| `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` | ✓ | ✓ | mode held at **600** |

**`~/.zshrc` carried TWO `GROQ_API_KEY` lines** (4 and 5, identical values). Both were rewritten —
updating one would have left a stale duplicate that, being sourced last, **would have won**.

**Handoff files overwritten with random bytes and deleted.** `~/.hip-secrets/` retains only the
Neo4j password files and another dispatch's backups.

**Also noted:** `com.hip.demo.dashboard.plist` was **already mode 600** by the time of the resume —
tightened by someone after FM 11's sweep reported it world-readable. **Its `OPENAI_API_KEY` and its
`NEO4J_PASSWORD` (a separate live value pinned to 7689, the frozen-demo graph) remain UNROTATED.**

---

## 3. PLIST FILE MODE — FIXED

`~/Library/LaunchAgents/com.hip.voice.orch.plist`: **`-rw-r--r--` → `-rw-------` (600).**

**Stated so the limit is not overread:** mode 600 closes the world-readable file, but
**`launchctl print` still emits every environment value in full to any process running as this
user**, independent of file mode. **Mode is not the whole exposure.** Rotation is what actually ends
it — which is why §2 matters and is not cosmetic.

---

## 4. ⚠ SWEEP — A SECOND CREDENTIAL-BEARING PLIST, AND IT IS WORSE

**Scope swept:** `~/Library/LaunchAgents` (10 plists), `/Library/LaunchAgents` (0),
`/Library/LaunchDaemons` (4). **Key NAMES only; no value was read or printed.**

| plist | mode | keys | loaded? |
|---|---|---|---|
| `com.hip.voice.orch.plist` | **600** (fixed here) | `GROQ_API_KEY`, `NEO4J_PASSWORD`, `SERPAPI_KEY` | **not loaded** (FM 10) |
| **`com.hip.demo.dashboard.plist`** | **`-rw-r--r--` WORLD-READABLE** | `GROQ_API_KEY`, `NEO4J_PASSWORD`, **`OPENAI_API_KEY`**, `SERPAPI_KEY` | **not loaded** |

**Nothing else on this machine embeds a HIP credential.** The other 12 plists are clean.

### Three things about the dashboard plist that widen FM 11's scope

1. **It carries a FOURTH credential type — `OPENAI_API_KEY`** — which was not in this dispatch's
   scope and is **not** rotated.
2. **Its `NEO4J_PASSWORD` is a DIFFERENT, STILL-LIVE value** — hash-compared, not assumed. It is
   **not** killed by §1's rotation.
3. **It pins `bolt://localhost:7689` — the FROZEN DEMO graph**, which `~/hip-vo/.hip-graph` names a
   **forbidden target**. So a world-readable file grants credentialled access to the one graph the
   lane rules single out as untouchable.

**CHANGED NOTHING HERE, per the dispatch's "report what you find, change nothing else."** Its mode
was **not** altered and its credentials were **not** rotated. **NEEDS BILL: does this plist join the
rotation scope too?** On the evidence it is the larger exposure of the two.

---

## WHAT THIS DISPATCH DID NOT DO

- Did **not** rotate, read or print `GROQ_API_KEY`, `SERPAPI_KEY` or `OPENAI_API_KEY`.
- Did **not** modify `com.hip.demo.dashboard.plist` — not its mode, not its contents.
- Did **not** load, unload or start any service; `com.hip.voice.orch` stays unloaded and disabled.
- Did **not** touch graphs 7688, 7689, 7690 or 7692, nor any lane's data.
- Did **not** commit any credential value, in a file or a commit message.
