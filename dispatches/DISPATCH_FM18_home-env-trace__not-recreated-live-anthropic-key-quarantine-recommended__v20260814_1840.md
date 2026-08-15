# DISPATCH_FM18 — `~/.env.dev` traced; the Anthropic key is LIVE
Status: BUILT
Reconciled-Against: machine read 2026-08-14 18:40 MDT; roadmap @ `a5be2c8`

COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING

**READ-ONLY on the file, as instructed. Nothing was moved, deleted, chmod'd, or edited.**
**RECOMMENDATION ONLY — Bill rules.** No value appears anywhere in this document or in any command
output; credentials are reported by length and SHA-256 prefix.

**REQ: NONE** — a trace and a recommendation build no behaviour.

---

## 1. WHO MADE IT — **the premise is false: it was NOT recreated**

| fact | value |
|---|---|
| **birth** | **2026-07-21 18:02:18** |
| **mtime** | **2026-07-21 18:02:18** |
| **ctime** | **2026-08-14 16:57:21** |
| mode / owner / size | `0600` / `bill-ai` / 360 bytes |

**birth == mtime == 2026-07-21, and only `ctime` is today.** That combination is decisive:

* **`birth` is the INODE's creation.** A file that was deleted and recreated gets a NEW inode and
  therefore a NEW birth. This one's is from July, so **the inode has existed continuously.**
* **`mtime` is unchanged since July**, so **the CONTENT has not been written since 2026-07-21
  18:02** — including the `ANTHROPIC_API_KEY` line.
* **`ctime` moves on METADATA changes only** — permissions, ownership, or a rename. Something
  touched the file's metadata **today at 16:57:21**.

**16:57:21 sits inside FM 11's credential sweep window** — `~/hip-dev/.env.dev` was modified at
**16:56**, one minute earlier. A `chmod`/permission pass across env files is the parsimonious
explanation for a ctime change with no mtime change, and FM 11 documented exactly such a sweep.
**Stated as the leading hypothesis, not as proof: nothing in the record names the command.**

### FM 1's "does not exist" is a FALSE NEGATIVE, not evidence of deletion

FM 1 recorded at 10:11 today: *"`~/.env.dev` **does not exist** on this machine."* **The inode
contradicts that** — the file cannot have been absent at 10:11 and then reappear with a July birth
time and July mtime. No mechanism available here does that: `cp -p` preserves mtime but mints a new
birth; `rsync -a` likewise; only a same-volume rename preserves both, and nothing in the record
renames it.

**The likeliest cause of the false negative is a REPOINTED `HOME`.** That is not speculation about
an unknown failure mode — **it is a demonstrated one in this codebase, twice today**: VD-62's route
test sets `os.environ["HOME"]` to a temp dir at module scope, and **HA-87 reproduced the same bug in
my own test**, where it errored four unrelated tests because the mutation is process-wide. **A check
for `~/.env.dev` from any process in that state reports ABSENT while the file sits untouched.**

### The creator, and what the record cannot establish

**UNATTRIBUTABLE.** Evidence gathered, all negative:

* **No script writes it.** Ten scripts across four trees *reference* `~/.env.dev`; **none writes,
  redirects into, or `tee`s to it.**
* **`.zsh_history` is NOT in extended format** — it carries no epoch timestamps (a timestamped scan
  returned **0** entries), so **no command in it can be dated.** Commands mentioning the file exist
  but cannot be placed on today's timeline, which is exactly what attribution would require.
* **No backup or quarantine sibling exists** (`~/.env.dev.bak`, `.disabled`, etc. are absent), and
  **no other file on disk shares its content** — the four `.env.dev` files all hash differently.

**One thing the history does show, and it did NOT take effect:**
`grep -v ANTHROPIC_API_KEY ~/.env.dev > /tmp/e && mv /tmp/e ~/.env.dev` appears **twice**, and an
`OPENAI_API_KEY` variant once. **Someone tried to strip these keys out.** The attempt is not
reflected in the file — the key is still present and mtime is still July — so it either predates
2026-07-21 18:02 or never completed. **Worth knowing that the intent to remove this key already
existed and did not land.**

## 2. WHAT READS IT — and whether anything is consuming the 7689 pin

**Four trees load it, three of them with `override=True`:**

| tree | site | override |
|---|---|---|
| `~/hip-cutover-demo` | `demo_dashboard.py:64` | **`override=True`, unconditional** |
| `~/hip-dev` | `demo_dashboard.py:61` | **`override=True`, unconditional** |
| `~/hip-roadmap` | `demo_dashboard.py:90` | **`override=True`** |
| `~/hip-vo` | `demo_dashboard.py:96` | **RESTRICTED** — an allowlist admits only `OPENAI_API_KEY` |

**IS ANYTHING LIVE CONSUMING THE 7689 PIN RIGHT NOW? NO — and the reason is not reassuring.**
HA-91 established two hours ago that **no Python process is listening on any port** and
`com.hip.demo.dashboard` is **NOT LOADED**. **The hazard is fully armed and simply not firing,
because nothing is running.** The first `demo_dashboard` start in any of the three unrestricted
trees silently repoints that process at **7689, the frozen demo graph** — which `.hip-graph` names a
forbidden target and which STANDARD PREAMBLE item 3 exists to prevent.

**`~/hip-vo` is the exception BY DESIGN and is the model for the fix**: its allowlist admits exactly
one variable, with the reason written beside it.

## 3. THE ANTHROPIC KEY

| property | finding |
|---|---|
| **live?** | **YES — HTTP 200** from `GET /v1/models?limit=1`. One auth-check call, **no content generated**, no message sent |
| identity | length **108**, prefix `sk-ant-…`, SHA-256[:12] **`8b581478ca30`** |
| **where else on disk** | **NOWHERE ELSE.** Absent from `~/.zshrc`, `~/.zprofile`, every `~/Library/LaunchAgents/com.hip.*.plist`, and all four repo `.env.dev` files |
| **committed anywhere?** | **NO.** `hip-roadmap` 11, `hip-vo` 8, `hip-cutover-demo` 12 tracked files mention `ANTHROPIC_API_KEY` — **a value-pattern scan returns ZERO in every tree**, so those are variable NAMES, not secrets |
| exposure | `0600`, owner `bill-ai`, **outside every repository** — so it is the *least*-exposed of today's credentials, unlike `com.hip.demo.dashboard.plist`, which FM 11 found **world-readable** with four |

## 4. RECOMMENDATION — Bill rules; nothing was done

### (a) QUARANTINE, DO NOT DELETE

**Rename it rather than remove it** — e.g. `~/.env.dev.QUARANTINED-FM18` — then start each
dashboard once and confirm nothing breaks.

**Why not delete:** `~/hip-vo`'s loader deliberately admits `OPENAI_API_KEY` from this file, and its
own comment records that the repo `.env.dev` has no valid one. **Deleting could remove the only
working OpenAI credential for that tree**, converting a latent graph hazard into an immediate
outage. A rename is reversible in one command; a delete of an uncommitted, unbacked-up 0600 file is
not — and **this file exists in exactly one place, with no copy anywhere.**

**Why quarantine at all:** the `NEO4J_URI=…7689` pin is a live wrong-graph redirect against three
trees, and the preamble already names it a hazard. Removing it costs nothing once the OpenAI
dependency is confirmed.

### (b) THE DURABLE FIX IS THE ALLOWLIST, NOT THE FILE

**Port `~/hip-vo`'s restricted loader to the other three trees.** Quarantining the file fixes
today; an allowlist fixes the class, and the pattern is already written and shipping in this repo.
**Deleting the file without this leaves three `override=True` call sites that will silently obey the
next home file anyone creates.**

### (c) DOES THE ANTHROPIC KEY JOIN ROTATION SCOPE — **RECOMMEND YES**

**It is live, and it was outside FM 11's scope purely because FM 11 scoped to the plists.** It sits
alongside two credentials already rotated. **Rotating it is cheap and the blast radius of not
rotating it is an active API key of unknown age with an unestablished creator.**

**Two honest qualifications against my own recommendation:**
1. **Its exposure is genuinely lower** than the plist credentials — `0600`, outside every repo, never
   committed, and no evidence it ever leaked. **On evidence alone this is the least urgent of the
   three.**
2. **`com.hip.demo.dashboard.plist` is the larger exposure and is still unanswered** — world-readable,
   four credentials, including a *different, still-live* `NEO4J_PASSWORD` pinning 7689. **If only one
   thing is rotated next, it should be that plist, not this key.**

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **Quarantine `~/.env.dev`?** Recommend rename-then-verify, not delete (§4a).
2. **Does the Anthropic key join rotation scope?** Recommend yes, with the qualification that the
   world-readable dashboard plist outranks it (§4c).
3. **Port hip-vo's allowlist loader to the other three trees?** This is the fix that survives the
   next home file (§4b).
4. **FM 1's absence finding should be corrected in its record** — the inode contradicts it, and the
   likely cause (a repointed `HOME`) is a live, twice-demonstrated failure mode worth naming so the
   next survey does not repeat it.
