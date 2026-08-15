# FM 13 — ROTATE THE SECOND PLIST'S CREDENTIALS
Status: **PARTIAL — the rotatable half is DONE; the vendor keys await Bill's console step**
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap`. Board claim `bfeb347` / `a002a73`.

**NO CREDENTIAL VALUE APPEARS ANYWHERE IN THIS DOCUMENT.** Every comparison is by SHA-256
prefix or by exit code, the same discipline FM 11 used.

---

## 0. THE EXCEPTION LINE

```
FM 13 — ROTATE THE SECOND PLIST'S CREDENTIALS
COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING
```

**NEEDS BILL: three console rotations (§3).** Everything this dispatch could do without a
vendor console is done and proven.

---

## 1. `NEO4J_PASSWORD` (7689) — ROTATED AND PROVEN

**Precondition checked first**, per FM12-1's lesson that the lock table cannot answer *"is
anything mid-run"*: no battery, harness or gate process anywhere; `repo` and all `graph:` locks
free; and **zero established client connections on 7689** at the moment of the rotation, so
nothing was torn out from under a running lane.

| | before | after |
|---|---|---|
| value | `sha256:8675366c458e` | **`sha256:98d80ef9b56b`** |
| length / charset | 24 | **24, alphanumeric (TD-104)** — a shell-special character in this value trips zsh/plist/sed edits |
| distinct from every other lane's | — | **yes**, so one leak can never unlock two graphs |

**PROOF, BOTH DIRECTIONS, on `bolt://localhost:7689`:**

| check | result |
|---|---|
| NEW value authenticates | **YES** |
| OLD (exposed) value | **REFUSED — `AuthError`** |
| node count | **11 → 11, unchanged** |

Rotated with `ALTER CURRENT USER SET PASSWORD FROM … TO …`. **Backups of both mutated files
were taken first**, into `~/.hip-secrets/fm13-backups/` (dir 700, files 600).

### Every file touched — the complete list

| file | change |
|---|---|
| `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` | `NEO4J_PASSWORD` replaced; mode `644` → **`600`** |
| `~/hip-dev/.env.dev` | `NEO4J_PASSWORD` replaced; mode `644` → **`600`** (see §4 — it was world-readable) |
| `~/.hip-secrets/neo4j-7689.password` | **created**, mode 600 — an operator copy outside every repository |

**The rewritten plist was verified structurally, not just visually:** `plutil -lint` OK, XML
format preserved, **19 keys before and 19 after with an identical key set, and exactly ONE value
different** — the password. Nothing else in that file moved.

**End-to-end:** `~/hip-dev/.env.dev` now authenticates against 7689 and reads 11 nodes. The
frozen demo's own credential file works with the new value.

**7690 was not touched, opened, or read**, as the dispatch directed. Nothing was coordinated
with the cutover graph.

---

## 2. `HIP_MASTER_KEY` — NOT A SECRET. IT IS A PATH. NOTHING TO ROTATE.

This key is in the plist and is **not** in FM 11's list of that plist's credentials, so it
arrived here as an apparent fifth secret and a candidate for §3's treatment. **It is not a
credential at all**, and that was established from the code rather than from its name:

```
harness/encryption.py:70   def _master_key_path() -> pathlib.Path:
                               """Resolve the master-key path, honouring the $HIP_MASTER_KEY override."""
                               env = os.environ.get("HIP_MASTER_KEY")
                               return pathlib.Path(env) if env else DEFAULT_MASTER_KEY_PATH
```

The plist's value is a **filesystem path**, and the path exists. **The root secret is the file
it points at, not the variable** — and that file is already correct:

| | |
|---|---|
| target | a 32-byte key file under `~/hip-dev/data/encryption/` |
| mode | **600**, parent **700** |
| tracked? | **no** — `data/encryption/` is gitignored, with the comment *"Root secret for envelope encryption; losing it makes every encrypted :Fact value unrecoverable. Never commit."* |

**Recorded so nobody rotates a path.** Had this been treated as a secret by name, the "rotation"
would have replaced a working pointer with a random string and broken every encrypted fact read
on that lane — and it would have looked like a completed task. **The name says KEY; the code
says path; the code wins.**

---

## 3. THE THREE VENDOR KEYS — ⛔ STOPPED. THIS IS BILL'S STEP.

Prepared exactly as FM 11 prepared its two: consoles named, holder files enumerated, **nothing
rotated, nothing read aloud.**

### 3.1 `OPENAI_API_KEY` — the one this dispatch names

**Console:** **https://platform.openai.com/api-keys**
**Fingerprint:** `sha256:0618d5551430`, length 164.
**Update these two files after rotating, and nothing else:**

1. `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` → `EnvironmentVariables.OPENAI_API_KEY`
2. `~/.env.dev` → the `OPENAI_API_KEY` line

### 3.2 `SERPAPI_KEY` — **one key, THREE holders, and it spans both plists**

**Console:** **https://serpapi.com/manage-api-key**
**Fingerprint:** `sha256:faf88c81bf9a`, length 64.

**This is the same value FM 11 already queued for you from the other plist** — verified by
hash, not assumed. **One console rotation kills it in both**, but all three files must be
updated or something breaks:

1. `~/Library/LaunchAgents/com.hip.demo.dashboard.plist`
2. `~/Library/LaunchAgents/com.hip.voice.orch.plist`
3. `~/hip-harness/.env` — **a separate repository**, not a worktree of `hip-dev`

### 3.3 `GROQ_API_KEY` — a **SECOND, DIFFERENT** Groq key

**Console:** **https://console.groq.com/keys**
**Fingerprint:** `sha256:f13a4674175e`, length 56 — **different from the voice plist's
`sha256:1b204256f8e5`.**

**So there are TWO Groq keys to rotate, not one.** FM 11 queued the other. Rotating only one
leaves a live exposed credential. **Only holder:** the dashboard plist.

### What to do when you have rotated them

Say the word and the same two-direction proof runs on each: the new key works, and **the plists
hold only DEAD values**.

---

## 4. ⚠ FINDING — NINE WORLD-READABLE CREDENTIAL FILES, INCLUDING THE ONE THIS DISPATCH HAD JUST WRITTEN TO

Bill's ruling for this dispatch is explicit: *"Replacement credentials must NOT land in any
world-readable file."* **Checking that after the rotation is what caught this**, and it is the
most useful thing in this document.

**`~/hip-dev/.env.dev` was mode 644** — world-readable — **and the freshly rotated 7689 password
had just been written into it.** The constraint was violated at the moment of writing and would
have stayed violated if the check had not been run.

A sweep then found the same shape across the estate. **All nine closed to 600:**

```
644 -> 600   ~/.env.dev                     (also holds OPENAI_API_KEY — §3.1)
644 -> 600   ~/hip-dev/.env.dev             (the file this dispatch wrote to)
644 -> 600   ~/hip-roadmap/.env.dev
644 -> 600   ~/hip-vo/.env.dev
644 -> 600   ~/hip-nc/.env.dev
644 -> 600   ~/hip-harness/.env             (also holds SERPAPI_KEY — §3.2)
644 -> 600   ~/hip-dev/.env.demo
644 -> 600   ~/hip-cutover-demo/.env.demo
644 -> 600   ~/hip-vo/.env.demo
```

**Final state of every credential surface on this machine:**

| surface | mode |
|---|---|
| `com.hip.demo.dashboard.plist` | **600** |
| `com.hip.voice.orch.plist` | **600** (FM 11) |
| all nine `.env*` files above | **600** |
| `~/.hip-secrets/` | **700**, contents **600** |
| the fact-encryption master key | **600**, parent **700**, gitignored |

### The sweep was completed, not stopped at nine — and the tail was VERIFIED, not assumed

A closing pass found **five more files still at 644**, and each was checked for contents before
any conclusion was drawn:

| file | secret-shaped keys | verdict |
|---|---|---|
| `com.hip.autogate.plist` | **none** (`HOME`, `PATH`) | 644 is not a violation |
| `com.hip.voice.mem0.plist` | **none** (`PATH`) | 644 is not a violation |
| `com.hip.voice.plist` | **none** (`PATH`) | 644 is not a violation |
| `~/hip-nc/.env.demo` | **none** (`DEMO_MODE`, two Kokoro paths) | set to 600 for class consistency |
| `~/hip-roadmap/.env.demo` | **none** (same three) | set to 600 for class consistency |

**This confirms FM 11's "the other 12 plists are clean" against the artifact rather than
carrying it forward on trust** — which is the FM13-2 lesson applied to FM 13's own work. The
three plists keep mode 644 because there is nothing in them to protect, and saying so is more
useful than silently changing them.

**The limit, stated so mode is not overread — FM 11 said this and it still holds:**
`launchctl print` emits every environment value in full to any process running as this user,
whatever the file mode. **Mode closes the world-readable file; only rotation ends the exposure.**
That is why §3 is not cosmetic.

---

## 5. "WHERE POSSIBLE, STOPS HOLDING SECRETS AT ALL" — WHAT WAS AND WAS NOT DONE

The plist now holds **four** secret values (Groq, Neo4j, OpenAI, SerpAPI) at mode 600, down from
four at mode 644. **It does not yet hold none**, and that half of the ruling is not met.

**The mechanism that would meet it**, prepared and deliberately **not applied**: replace
`ProgramArguments` with a wrapper that sources a 600-mode secrets file and `exec`s the same
interpreter — the plist would then carry only non-secret configuration.

**Why it was not applied here.** It rewrites how the frozen demo's dashboard *starts*, and
proving it works means **loading a service in `~/hip-dev`** — the frozen demo, which the lane
rules place outside pre-authorization and which this dispatch's ruling does not mention. The
plist is currently **not loaded**, so a mistake would surface only when someone reaches for the
fallback, which is the worst possible moment to discover it. **Rotation and mode are reversible;
a fallback that will not start is not.**

**It is also cheap to do properly later**: one wrapper, one secrets file, and a start-test —
about the size of this dispatch, and safe once someone is willing to load and unload that
service deliberately.

---

## 6. FILED, NOT BLOCKING (3)

**(FM13-1) Nine world-readable credential files** — §4. Closed. The class question is what
*creates* them at 644: every one was written by some earlier tool or hand-edit that never set a
mode. **Nothing enforces 600 on a new `.env` file**, so this recurs the next time one is
created. A `lane_preflight.py` check is the natural home.

**(FM13-2) FM 11's key inventory for this plist was incomplete** — it named four keys and did
not name `HIP_MASTER_KEY`. On the evidence that omission was harmless, because the variable is a
path and not a secret (§2) — but the inventory was read as complete by this dispatch's own
tasking, and an inventory that is trusted must be complete or say that it is not. **Same shape
as FM3-2**: a claim about a file's contents that was not measured against the file.

**(FM13-3) The dashboard plist mixes two lanes.** Its interpreter, registry and logs are
`~/hip-dev`, while `WorkingDirectory` and `PYTHONPATH` are `~/hip-vo`. So the frozen demo's
dashboard would run **hip-vo's code against hip-dev's graph and registry**. Not touched — it is
pre-existing and outside this dispatch's scope — but it is exactly the cross-lane shape
`lane_preflight.py` exists to refuse, and no preflight guards a launchd plist.

---

## 7. WHAT THIS DISPATCH DID NOT DO

- **Did not read, print, or rotate** `OPENAI_API_KEY`, `GROQ_API_KEY` or `SERPAPI_KEY`.
- **Did not touch 7690, the cutover graph**, or coordinate anything with it.
- **Did not load, unload, or start any service.** Both plists remain unloaded.
- **Did not alter the fact-encryption master key or its file.**
- **Did not change `ProgramArguments`** on either plist — §5.
- **Did not commit any credential to any repository.** `~/hip-dev/.env.dev` is gitignored;
  `~/.hip-secrets/` is outside every repository.

---

## 8. CLAIM IMPACT

```
CLAIM IMPACT: none
```

---

## 9. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- Mid-run precondition checked by **process scan**, not by the lock table alone (FM12-1).
- Rotation proven in both directions with the node count unchanged, on a graph with **zero open
  client connections** at the time.
- Plist integrity checked structurally: `plutil -lint` OK, identical 19-key set, exactly one
  value changed.
- Board rows written by `claim_lane.py` under the repo lock, board-only, no passengers.
