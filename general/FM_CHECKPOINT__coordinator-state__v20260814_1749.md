# FM COORDINATOR CHECKPOINT — FABLE MASTER state
Status: LIVE
Reconciled-Against: machine read at 2026-08-14 17:49 MDT (FM 16). Supersedes `v20260814_1025` (FM 2).

**Purpose: session recovery.** If the FABLE MASTER chat is lost, a successor reads THIS FILE FIRST,
then `docs/LANES.md`, then `docs/dispatches/` by mtime, then git state, then `HIP_HANDOFF.md`
CURRENT STATE (operating model §3).

**This is a POSITION REPORT, not a summary.** Every fact below was read off the machine at
checkpoint time. Where a fact could not be established it reads `UNKNOWN — <why>`; a guess is not
an answer.

---

## 1. DATE AND HEADS READ

**2026-08-14, 17:49 MDT.** Machine: `bill-ai` @ `[REDACTED-MACHINE-NAME]`

| checkout | branch | HEAD | sync |
|---|---|---|---|
| `~/hip-roadmap` | `roadmap` | `786b199` FM 16 claim | in sync |
| `~/hip-vo` | `main` | `324932d` HA-89 | **AHEAD 1 — UNPUSHED** |
| `~/hip-cutover-demo` | `demo-cutover-build` | `6304ac1` VD-64 | in sync |
| `~/hip-dev` | `demo-presenter-package` | `442050a` HA-78 | in sync |
| `~/hip-harness` | `voice-latency` | `14ac694` HA-78 | in sync |
| `~/hip-nc` | `natural-conversation` | `b423829` NC 6 correction | in sync |
| `~/hip-nc2` | `nc-b0` | `f6dcdd3` NC 8 (B0) | in sync |

**⚠ `~/hip-vo` carries ONE UNPUSHED COMMIT** — `324932d` *"HA-89: Tier L probes /hip not the gated
/api/members, and an unreachable server…"*. Preamble item 8: a committed-but-unpushed commit sits
where **any** other lane's next push will carry it, published without either lane deciding to.
**Named here so it is not carried as a passenger.**

## 2. ACTIVE WORKTREES + TARGETS

**SEVEN worktrees, not five** — the prior checkpoint listed five. `~/hip-nc` and `~/hip-nc2` are
the Natural Conversation lanes and are ACTIVE. An eighth path,
`~/hip-dev/.claude/worktrees/bridge-cse_01K1ppSwGuCbcU6vG8NQhPH3` (`65c263e`), is a tool-created
worktree, not a lane.

**All of the above share ONE commit graph (`~/hip-dev/.git`) and ONE `repo` lock. `~/hip-harness`
is a SEPARATE REPOSITORY** (`github.com/wyomingbill/hip-harness`, TD-132) — a fix landed in one is
not landed in the other, which is exactly how HA-51 shipped fixes to a service that was not serving
them.

## 3. WORKER ASSIGNMENTS (CC-1..4, current)

| seat | lane | last observed work |
|---|---|---|
| **CC-1** | `~/hip-vo` @ `main` | filed TD-R-191/192 from the governed-voice review |
| **CC-2** | `~/hip-vo` @ `main` | HA-86 / HA-87 (this session): review repairs, F3b, F4, egress re-rule |
| **CC-3** | `~/hip-cutover-demo` | VD-61 → VD-65: net-label truth, endpoint closure, freeze, rulings |
| **CC-4** | `~/hip-nc` / `~/hip-nc2` | NC 6 → NC 8: B0 ground hardening |

**Roles are stable; assignments are temporary** (operating model §1). A seat name confers no
authority. **HA-88 and HA-89 landed on `~/hip-vo` from a seat this session did not observe
directly** — attribution above is by lane and commit, not by claim.

**Live `claude` processes at checkpoint time: 1.** Down from 2 at FM 2 and 5 earlier. **A session
count is not a work count** — most lanes are between dispatches, not idle-forever.

## 4. ACTIVE CAPABILITIES

### Board position
Next free: **HA-90**, **VD-66**, **FM 17**, **NC 9**. Closed series: `D-R-nnn` (ended `D-R-196`).

### Landed today, roadmap/voice lane
* **HA-86** — F3a (permit obeyed), F2 (governed failure refuses), F6 (egress suite joined the gate).
* **HA-87** — S2 F3b (destination truth), S3 F4 (route closure), S4 (egress re-ruled). **S1 STOPPED.**
* **HA-88 / HA-89** — landed on `main`; HA-89 repairs a Tier L probe that hit HA-87's new `/api/members` guard.

### Demo lane
* **VD-61 → VD-63** — net-label repair, endpoint closure, **FREEZE**.
* **VD-64** — both demo REQs ruled MET. **VD-65** — freeze record's working copy restored.

### Standing gates
* **`~/hip-vo` governance gate is RED at HEAD, BY INSTRUCTION** — 328 collected, 320 passed, 2
  failed, 6 skipped, 0 errors. The two are **TD-V-031** (`/ws/voice` direct egress). Not silenced,
  no test weakened, `KNOWN_UNROUTED` still empty.
* The demo tree is **FROZEN** (below).

## 5. REQUIREMENTS STATUS — including today's two MET rulings

| REQ | status | evidence |
|---|---|---|
| **REQ_NET_LABEL_TRUTHFUL** | **MET — Bill, 2026-08-14 (VD-64)** | VD-61, twin on BOTH surfaces at `7ec9c61`, battery green |
| **REQ_DEMO_ENDPOINT_CLOSURE** | **MET — Bill, 2026-08-14 (VD-64)** | VD-62, inventory 8/8 at 401, `/ws/voice` 404, green at `d0282bd` |
| **REQ_EGRESS_GATEWAY** | **NOT MET — re-ruled Bill, 2026-08-14 (HA-87 S4)** | HA-86 falsified its own exemption premise; TD-V-031. Returns to MET when F1's migration removes the route |
| REQ_EGRESS_DESTINATION_TRUTH | IN_PROGRESS (HA-87 S2) | 16 twins; **not ruled** |
| REQ_VOICE_ENDPOINT_CLOSURE | IN_PROGRESS (HA-87 S3) | 14 twins; **not ruled** |
| REQ_GOVERNED_TURN_REFUSAL | IN_PROGRESS (HA-86 F2) | 9 twins; **not ruled** |
| REQ_GATE_SELF_INFLICTED_REDS | PLAN | filed on `main`, credential-provenance |

**Both REQs ruled MET today live in `~/hip-cutover-demo`, not `roadmap`** — VD-64's dispatch
assumed roadmap and was corrected against the machine.

## 6. OPEN TECH DEBT — the named items

| id | lane | state |
|---|---|---|
| **TD-R-191** | roadmap (code in `~/hip-vo`) | governed turn fails OPEN — **FIXED at HA-86 F2**, register row not yet closed |
| **TD-R-192** | roadmap (code in `~/hip-vo`) | permit computed and discarded — **FIXED at HA-86 F3a**, row not yet closed |
| **TD-V-P191 / TD-V-P192** | hip-vo | POINTER rows only — authoritative entries are TD-R-191/192. Register follows the CODE, not the dispatch lane (Bill, 2026-08-14) |
| **TD-V-029** | hip-vo | `--full` never baselined on this lane; three probes stale vs TD-V-018. **OPEN — needs a clean lane baseline first** |
| **TD-V-030** | hip-vo | caller-supplied transcript given SPOKEN provenance. **OPEN — Bill's ruling required.** ⚠ **Its scope note is now STALE**: it states the service is *"live whenever the machine is up"*, and `com.hip.voice.orch` is **NOT LOADED** (HA-87) |
| **TD-V-031** | hip-vo | `/ws/voice` direct server-side egress outside the gateway. **OPEN — Bill's ruling required; gate RED at HEAD by instruction** |

## 7. BILL DECISIONS PENDING

### Credentials / keys — the live cluster
1. **FM 11's rotation is HALF-APPLIED.** It rotated the graph credentials and handed Bill a file
   list to update; **`com.hip.voice.orch.plist` is still outstanding.** Consequence, measured at
   HA-87 by hash and never printed: the installed plist and the 0600 sanctioned store both carry a
   credential the live 7691 graph **REJECTS**; only `~/hip-vo/.env.dev`'s literal authenticates.
   **This is why HA-87 S1 stopped** — restoring the sanctioned mechanism as ordered would have made
   that lane authenticate with a rejected credential.
2. **A graph credential is COMMITTED IN GIT** — `launchd/com.hip.voice.orch.plist` on `hip-vo`,
   tracked since HA-53 `e96f4ac`. Stale value, but in history. **History rewriting is not
   pre-authorized.**
3. **`com.hip.demo.dashboard.plist` is world-readable with four credentials** (FM 11), including an
   `OPENAI_API_KEY` and a *different, still-live* `NEO4J_PASSWORD` pinning **7689, the frozen demo
   graph**. FM 11 changed nothing there and asked whether it joins the rotation scope. **Unanswered.**
4. **`REQ_ERASURE_SURFACES` — six decisions (HA-43)**, carried; *"governed surface"* and *"relevant
   keys"* still undefined.

### Voice / research
5. **F2's broad `except`** (HA-86) — kept deliberately against the dispatch's literal "narrow the
   except", reasoning recorded. Confirm or overrule.
6. **`LOCAL_ALLOWED_HOSTS` is empty** by design (HA-87 S2) — a live constraint if any deployment
   legitimately reaches a non-loopback on-box address.

### CORRECTION — "Q2 mic" is NOT pending
**FM 16's dispatch lists Q2 mic among pending decisions. The machine says otherwise and the machine
wins.** M0's verdict was `PROVISIONAL-PASS PENDING Q2 MIC` and **was resolved to PASS on 2026-08-14
by Bill's own live microphone test** (*"not walkie talkie"*, *"good at finding the semantic end
point of my speech"*), recorded in
`docs/design/HIP_DESIGN_DIAGRAM__moshi-dual-model-architecture-as-adopted__v20260814_1331.md`, which
explicitly flags the "Q2 mic pending" framing as **stale**. **Carried here as CLOSED.** If Bill
means a different Q2, it needs naming — this checkpoint could not establish another.

## 8. REVIEW QUEUE

| package | state |
|---|---|
| `hip_review_f2f17ca.zip` (2026-08-12) | **ROUND CLOSED** — findings became TD-V-018/019/021, all resolved |
| **Governed-voice review (F1–F7)** | **IN REMEDIATION.** F2/F3a fixed (HA-86), F3b/F4 built (HA-87), F6 gated (HA-86), F5 filed as TD-V-030. **F1 is the open one — TD-V-031 and the `REQ_EGRESS_GATEWAY` re-rule both hang off it** |
| **Demo-cutover package** | findings **NOT YET RECEIVED** |
| **Advisor-roadmap package** | findings **NOT YET RECEIVED** |

**Per Bill (FM 16).** This supersedes FM 2's "SEND-UNCONFIRMED" reading of the three 2026-08-13
packages: the governed-voice one demonstrably returned findings; the other two have not.

## 9. DEMO STATE

**FROZEN.** Tag **`demo-freeze-20260814`** → commit **`d0282bd`** (annotated tag; verified via
`rev-parse ^{commit}`, not assumed). Tree `~/hip-cutover-demo` @ `demo-cutover-build`, HEAD
`6304ac1` (VD-64's docs-only ruling, landed after the freeze under the precedent VD-63 set for
itself: *"this doc lands after it and changes no behaviour"*).

**Any change to that tree needs Bill's explicit unfreeze.**

**Evidence path:** `docs/dispatches/DISPATCH_VD63_DEMO_FREEZE__d0282bd-tagged-demo-freeze-20260814-with-its-certifying-battery__v20260814_1658.md`
(certifying battery banked in-repo). **That file's working copy was found overwritten by a stray
paste and was byte-restored at VD-65** — HEAD was never affected.

**Uncommitted in that tree, left exactly as found:** one modified VD-60 dispatch doc, plus untracked
`.hip-graph`, `.hip-owns`, and three probe-result CSVs.

## 10. NEXT MILESTONE

**NC Demo v1**, with **B0 IN FLIGHT** on `~/hip-nc2` @ `nc-b0` (`f6dcdd3`, NC 8 — B0 ground
hardening: typed intent failure, closed ingress, gated search). `~/hip-nc` @ `natural-conversation`
(`b423829`) carries the NC design line.

**FinishPlan position is UNKNOWN at this checkpoint** — FM 2 recorded step 7 of 14 ("erasure
prerequisites"), and nothing read today either advanced or contradicted it. **Stated as unverified
rather than carried forward as current.**

## 11. KNOWN LIMITS OF THIS CHECKPOINT

* **Worker seat attribution is by lane and commit, not by observation.** Only one live `claude`
  process existed at read time; HA-88/HA-89's seat is inferred.
* **It does not re-derive claim or debt totals.** FM 2's counts (15 claims / 58 open roadmap debt)
  were not re-counted here and must not be quoted from this file as current.
* **`docs/LANES.md` lives on `roadmap` and `main` diverged from it at `688386f`** — a dispatch
  running in `~/hip-vo` claims against a board it cannot read. Unchanged, still open.
