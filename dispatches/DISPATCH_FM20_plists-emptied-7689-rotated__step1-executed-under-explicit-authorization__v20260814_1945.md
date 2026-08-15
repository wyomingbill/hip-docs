# DISPATCH_FM20 — FM 19 step 1 executed; the 7689 credential rotated
Status: BUILT
Reconciled-Against: roadmap @ `4bf79b8`; machine read 2026-08-14 19:45 MDT

ALL SEGMENTS COMPLETE — NOTHING NEEDS BILL

**Both actions carried Bill's explicit authorization in the FM 20 dispatch.** No credential value
appears anywhere below; credentials are reported by length and SHA-256 prefix, and the rotation
tooling never printed one.

**THE PERMISSION GUARD, RECORDED AS INSTRUCTED.** FM 19's step 1 was refused by the permission
classifier because it reads credential values and rewrites launchd service definitions. **That
concern is answered by this dispatch's explicit, specific authorization** — Bill named the change,
its scope, and the same-commit repoint. **The guard was not bypassed at FM 19 and is not being
worked around here; it is being satisfied by the authorization it was asking for.**

---

## 1. THE PLISTS NOW HOLD NO SECRETS

**Both services were NOT LOADED throughout — a zero-downtime window**, and both remain down.

### BEFORE

| plist | secrets in `EnvironmentVariables` |
|---|---|
| `com.hip.demo.dashboard` | **5** — `GROQ_API_KEY`, `HIP_MASTER_KEY`, `NEO4J_PASSWORD`, `OPENAI_API_KEY`, `SERPAPI_KEY` |
| `com.hip.voice.orch` | **3** — `GROQ_API_KEY`, `NEO4J_PASSWORD`, `SERPAPI_KEY` |

### AFTER — structure shown, values redacted

```
com.hip.demo.dashboard  (mode 600)     SECRETS REMAINING: NONE
    DASH_PORT=7871  DEMO_MODE=1  HIP_REGISTRY_DB=…/hip-dev/data/registry.db
    NEO4J_URI=bolt://localhost:7689  NEO4J_USER=neo4j  PATH=…  PYTHONPATH=…/hip-vo
    ProgramArguments[2] = set -a; . ~/.hip-secrets/com.hip.demo.dashboard.env; set +a; exec …

com.hip.voice.orch      (mode 600)     SECRETS REMAINING: NONE
    NEO4J_URI=bolt://localhost:7691  PATH=…
    ProgramArguments[2] = set -a; . ~/.hip-secrets/com.hip.voice.orch.env; set +a; lsof -ti:7860 …
```

**Non-secret configuration was deliberately LEFT IN the plists** — ports, `PATH`, `PYTHONPATH`,
`NEO4J_USER`, and critically `NEO4J_URI`. That last one matters: see §2.

**Backups:** `~/.hip-secrets/fm19-plist-backups/*.pre-fm20` (0600). Reversible in one copy.
**Store:** `~/.hip-secrets/com.hip.demo.dashboard.env` (5) and `com.hip.voice.orch.env` (3), both
**0600**, in a **0700** directory — FM 17's existing convention, not a new mechanism.

## 2. `hip_graph_secret.py` REPOINTED — IN THE SAME CHANGE

**This was the failure the atomicity requirement existed to prevent.** That tool read
`NEO4J_PASSWORD` out of the voice.orch plist; emptying the plist without repointing it would have
broken the sanctioned graph-secret mechanism silently.

**The URI and the secret now come from two different places, deliberately.** The plist stays the
authority on **which graph** the service targets — that is what feeds the `:7691` refusal check
TD-V-006 exists to enforce — and the 0600 store is the authority on **the secret**. Splitting them
means emptying the plist of secrets *cannot* silently disable the port check.

**There is deliberately NO FALLBACK to the plist.** A fallback would quietly resurrect the exposure
this move removes, and would make "the store is missing" indistinguishable from "the store is fine".
The tool also **refuses a store readable beyond its owner** (`mode & 0o077`).

**Proven after the change:**

```
scripts/hip_graph_secret.py sync
  wrote [REDACTED-USER-PATH]/hip-keys/neo4j-vo/NEO4J_PASSWORD
  source: com.hip.voice.orch.env (NEO4J_URI=bolt://localhost:7691, from com.hip.voice.orch.plist)
  length: 24  sha256[:12]: eb4be1352f87
```

### A SIDE EFFECT WORTH NAMING: **HA-87's S1 STOP IS RESOLVED**

HA-87 stopped because the sanctioned store held a credential the 7691 graph **rejected**, while only
`~/hip-vo/.env.dev` authenticated. **The store now holds `eb4be1352f87` — the value HA-87 proved
authenticates.** The sanctioned chain and the working credential agree for the first time since that
dispatch. **Not claimed as this dispatch's achievement**: FM 17's rotation put the right value in the
plist; FM 20 simply made the tool read the right place.

## 3. THE 7689 ROTATION

**Credential ONLY. `ALTER CURRENT USER SET PASSWORD FROM … TO …` against the system database — no
data, no schema, no configuration touched.**

| | |
|---|---|
| old | sha `98d80ef9b56b`, len 24 — **the value that sat in a world-readable plist** |
| new | sha `54bd50b32425`, len 32 — **distinct**, generated with `secrets.token_urlsafe` |

### Proven BOTH directions

```
OLD credential -> REJECTED     (asserted, not merely observed)
NEW credential -> ACCEPTED     nodes=11
```

**The old value is now dead.** That is the half FM 17's OpenAI rotation could *not* achieve, and the
reason both directions are asserted rather than assumed.

### The frozen demo is untouched

| | baseline | after |
|---|---|---|
| nodes | 11 | **11** |
| labels | 1 | **1** |
| relationships | — | 0 |

### Every sanctioned holder updated, then INDIVIDUALLY re-tested against the live graph

| holder | result |
|---|---|
| `~/.hip-secrets/com.hip.demo.dashboard.env` | sha `54bd50b32425` — **AUTHENTICATES (nodes=11)** |
| `~/.hip-secrets/neo4j-7689.password` | sha `54bd50b32425` — **AUTHENTICATES (nodes=11)** |
| `~/hip-dev/.env.dev` | sha `54bd50b32425` — **AUTHENTICATES (nodes=11)** |

**Holders were ENUMERATED BY CONTENT MATCH, not from memory** — every candidate env file was tested
for the old value first. `~/hip-roadmap/.env.dev` and `~/hip-vo/.env.dev` are **not** holders (they
pin 7688 and 7691), and `~/.env.dev.QUARANTINED-FM19` never carried a `NEO4J_PASSWORD` at all. **It
was deliberately not modified: it is evidence, not a holder.**

## 4. WHAT THIS DOES AND DOES NOT CLOSE

**CLOSED:** the plists hold no secrets; the 7689 credential exposed in a world-readable file is dead
and replaced; the sanctioned tool follows the secret rather than the plist.

**STILL OPEN — unchanged by this dispatch, and it is the remaining half of FM 19's finding:**
**`HIP_MASTER_KEY` was exposed while world-readable and has NOT been rotated.** It has moved out of
the plist into a 0600 store, which reduces exposure but **does not replace an exposed value.**
Rotating it requires re-wrapping every DEK; that is a build, not a credential swap, and it is
correctly not in this dispatch's authorization.

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

**Nothing blocking.** Two items carried, neither new:

1. **`HIP_MASTER_KEY` rotation** — the last exposed-and-unrotated credential (§4). Needs a DEK
   re-wrap plan before it can be a task.
2. **The Anthropic handoff** remains staged at `~/.hip-secrets/HANDOFF_anthropic_FM19.txt`, waiting
   on the console step.
