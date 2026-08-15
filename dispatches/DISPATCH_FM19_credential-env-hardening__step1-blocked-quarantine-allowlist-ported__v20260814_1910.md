# DISPATCH_FM19 — credential + env hardening, in Bill's six-step order
Status: BUILT (STEP 1 BLOCKED — needs a permission decision)
Reconciled-Against: roadmap @ `08f800c`; machine read 2026-08-14 19:10 MDT

STOPPED AT SEGMENT 1 — NEEDS BILL

**Steps 2, 3, 4, 5 and 6 completed. Step 1 is blocked by a permission gate, not by a defect**, and
step 3 stopped where Bill said to stop. No credential value appears anywhere below; credentials are
reported by length and SHA-256 prefix.

---

## STEP 1 — PLIST-EXPOSED LIVE SECRET — **VERIFIED, THEN BLOCKED**

### What I established (this half succeeded)

**The world-readable exposure is CLOSED.** Both plists are now `-rw-------`, owner `bill-ai`, inside
a `drwx------` parent. **FM 17 fixed that between FM 11's finding and now** — so, on Bill's stated
trigger (*"any live credential readable beyond the intended user/process boundary"*), **nothing
qualifies for rotation today.**

`com.hip.demo.dashboard.plist` still holds **five** secrets in `EnvironmentVariables`:
`GROQ_API_KEY`, `HIP_MASTER_KEY`, `NEO4J_PASSWORD`, `OPENAI_API_KEY`, `SERPAPI_KEY`.
`com.hip.voice.orch.plist` holds three.

**TWO CREDENTIALS WERE EXPOSED WHILE WORLD-READABLE AND ARE STILL LIVE AND UNROTATED:**

| credential | state | why I did not rotate it |
|---|---|---|
| **`NEO4J_PASSWORD` (7689)** | **CONFIRMED LIVE** — authenticated against `bolt://localhost:7689`, sha `98d80ef9b56b` | **7689 is the FROZEN DEMO graph.** Changing it alters the frozen demo, which needs Bill's explicit unfreeze |
| **`HIP_MASTER_KEY`** | present, len 50, sha `c53458fa2f2a` | **Rotating a master key without re-wrapping every DEK destroys access to encrypted household facts.** Not a chmod-class action |

**Neither is a rotation I can take unilaterally, and neither is triggered by Bill's own criterion,
which is present-tense and is now satisfied.** They are named here because "the exposure is closed"
and "the exposed credentials were replaced" are different claims, and only the first is true.

### What is blocked

**The second half — removing the secrets from the plists and replacing them with sanctioned
loading — was REFUSED by the permission classifier.** The operation reads credential values and
rewrites launchd service definitions, which is precisely the shape that gate exists to catch. **I
did not attempt to work around it.**

**The prepared change, for approval:** back both plists up to `~/.hip-secrets/fm19-plist-backups/`
(0600); write each service's secrets to `~/.hip-secrets/<label>.env` (0600, FM 17's existing
convention); rewrite `ProgramArguments` to `/bin/bash -c 'set -a; . <envfile>; set +a; <original
command>'` — a shape `com.hip.voice.orch` **already uses**; and delete those keys from
`EnvironmentVariables`. **Both services are currently NOT LOADED, so this is a zero-downtime window.**

**ONE CONSEQUENCE THAT MUST BE HANDLED IN THE SAME CHANGE, or it silently breaks:**
`scripts/hip_graph_secret.py sync` **reads `NEO4J_PASSWORD` out of the voice.orch plist** — that
plist is its source of truth. Emptying the plist breaks the sanctioned graph-secret tool unless it
is repointed at `~/.hip-secrets/` in the same commit. **HA-87 already found that chain
half-broken**; this would break it the rest of the way.

## STEP 2 — QUARANTINE `~/.env.dev` — **DONE**

**Renamed, not deleted**, to `~/.env.dev.QUARANTINED-FM19`. Evidence preserved and proven by
comparison: **inode `5319612` identical before and after**, mode `-rw-------`, birth
`2026-07-21 18:02:18`, size 360. **Retention remains a later explicit ruling; nothing was removed.**

**A CORRECTION TO MY OWN FM 18 REPORT, three hours old.** FM 18 recorded mtime as
`2026-07-21 18:02:18` and concluded the content had not been written since July. **At quarantine
time mtime read `2026-08-14 18:33:16`.** FM 17 wrote this file *after* my read — it was the fourth
holder of the new OpenAI key. **FM 18's finding was true when measured and is now superseded on that
one fact.** Everything else in FM 18 stands: the inode still proves continuous existence, so FM 1's
"does not exist" remains a false negative.

**The dependency was real, and quarantine broke it until provisioned.** `~/hip-vo/.env.dev`
contained **zero** `OPENAI_API_KEY` lines while hip-vo's loader admits exactly that one key from the
home file — **the home file was hip-vo's only source.** Provisioned into the lane-owned
`~/hip-vo/.env.dev` (0600, gitignored), value sha `c16aac8d507b`, **matching FM 17's new key**.
**The home file was NOT restored.**

## STEP 3 — ANTHROPIC KEY — **STAGED, STOPPED FOR BILL**

`~/.hip-secrets/HANDOFF_anthropic_FM19.txt` (0600). Console URL, the
`~/.hip-secrets/new_anthropic` one-liner with a **length floor of 100 checked BEFORE any write**
(FM 18 measured the current key at 108; a doubled paste shows ~216), and the apply-and-prove step.

**Recorded as PRECAUTIONARY HARDENING, not leak remediation** — FM 18 established the key was never
committed (value-scan zero in all three trees), exists nowhere else on disk, and sat 0600 in a 0700
directory. **No console action taken. No key written.**

**FM 17's trap carried forward explicitly:** creating a key at the vendor does **not** revoke the
old one — OpenAI's remained live after rotation. Deletion is a separate act, after the new key is
proven.

## STEP 4 — ALLOWLIST LOADER PORTED — **DONE (2 landed, 1 staged)**

`override: bool` is gone; a caller must now name **which** keys may win and **cannot express "all of
them"**. `_LANE_SCOPED` (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `HIP_REGISTRY_DB`,
`HIP_MASTER_KEY`) is **skipped outright**, so a home file cannot supply lane identity **even when
the process has none** — the case a merely de-prioritised skip gets wrong.

| tree | result |
|---|---|
| `~/hip-roadmap` | **APPLIED** |
| `~/hip-dev` | **APPLIED** |
| `~/hip-cutover-demo` | **FROZEN — patch staged at `/tmp/fm19_hip-cutover-demo_demo_dashboard.py`, filed as TD-R-193, not applied and not committed** |

**Twins, both directions, 8/8** (`eval/test_home_env_allowlist_fm19.py`): a planted home file cannot
set `NEO4J_URI`/`NEO4J_PASSWORD`/`HIP_REGISTRY_DB`/`HIP_MASTER_KEY` even with the process value
deleted, and cannot override an existing pin; **anti-vacuity** proves `OPENAI_API_KEY` still loads
*and* still overrides, so the fix is isolation rather than amputation.

**One test defect of mine, caught and fixed:** the source scan matched the loader's own docstring,
which names the banned tokens while explaining them. **Fourth occurrence of this trap in the
project** — fixed with the docstring-stripping helper and the reason recorded in the test.

## STEP 5 — FM 1 CORRECTED — **DONE**

FM 1's *"`~/.env.dev` does not exist"* is **annotated in place, original wording preserved**, per the
pre-authorized correction class. The annotation records the inode contradiction, the **demonstrated**
`HOME`-repoint failure mode (VD-62's test and HA-87's reproduction), that the **creator remains
UNATTRIBUTABLE**, and that the 16:57 ctime touch stays a **labelled hypothesis**.

## STEP 6 — PER-LANE VERIFICATION — **DONE, PROVEN NOT ASSERTED**

With **no home file present**, each lane sourced its own config:

| lane | `NEO4J_URI` | registry | OpenAI |
|---|---|---|---|
| `~/hip-vo` | `bolt://localhost:**7691**` | lane-owned | 164 chars |
| `~/hip-roadmap` | `bolt://localhost:**7688**` | lane-owned | 164 chars |
| `~/hip-dev` | `bolt://localhost:**7689**` | lane-owned | 164 chars |

**Three lanes, three distinct graphs, none redirected.** A docstring-stripped AST scan confirms the
blanket override is gone from all three; `~/hip-cutover-demo` alone still carries it (TD-R-193).

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **STEP 1's plist rewrite needs a permission decision.** The change is prepared and the services
   are down, so the window is clean. It must repoint `scripts/hip_graph_secret.py` in the same
   change or that tool breaks.
2. **Two exposed credentials remain live and unrotated** — `NEO4J_PASSWORD` (7689, frozen demo) and
   `HIP_MASTER_KEY` (needs DEK re-wrap). Both need your ruling; neither is a chmod-class action.
3. **The Anthropic handoff is staged** and waiting on the console step.
4. **TD-R-193** — the frozen cutover tree still takes `override=True`; patch staged, blocked on the
   demo unfreeze.
5. `~/.env.dev.QUARANTINED-FM19` is retained pending your retention ruling.
