# FM COORDINATOR CHECKPOINT — FABLE MASTER state
Status: LIVE
Reconciled-Against: `roadmap` @ `57ce2d4`, 2026-08-14 10:25 MDT

**Purpose: session recovery.** If the FABLE MASTER chat is lost, a successor reads THIS FILE FIRST,
then `docs/LANES.md`, then recent `docs/dispatches/`, then git state, then `docs/HIP_HANDOFF.md`
CURRENT STATE — and **never reconstructs coordination state from memory or an old chat.** The
recovery order and its reasoning are §3 of
`docs/design/HIP_PROCESS__development-operating-model__v20260814_1025.md`.

**This is a POSITION REPORT, not a summary.** Where a fact could not be established it reads
`UNKNOWN — <why>`. Nothing here is a ruling.

> ⚠ **CURRENCY WARNING — read before trusting any line below.** FM 1 watched this board move **four
> times in twelve minutes**, and by the time FM 2 wrote this checkpoint **every worktree HEAD it had
> recorded had already changed** (HA-78 swept the estate). A checkpoint is a photograph. **Re-read
> git before acting on any hash here.**

---

## 1. DATE AND HEADS READ

**2026-08-14, 10:25 MDT.** Machine: `bill-ai` @ `[REDACTED-MACHINE-NAME]`
(MacBookPro18,1, Apple M1 Pro).

| checkout | branch | HEAD @ this checkpoint | vs origin |
|---|---|---|---|
| `~/hip-roadmap` | `roadmap` | `57ce2d4` | ahead 1 (FM 2's own claim) |
| `~/hip-vo` | `main` | `65c263e` | in sync |
| `~/hip-cutover-demo` | `demo-cutover-build` | `a869637` | in sync |
| `~/hip-dev` | `demo-presenter-package` | `442050a` | in sync |
| `~/hip-nc` | `natural-conversation` | `b404df7` | no upstream configured |
| `~/hip-harness` | `voice-latency` | `14ac694` | **SEPARATE REPOSITORY** — not a worktree |

**The first five share one commit graph** (`~/hip-dev/.git`) and **one `repo` lock**. There is no
lane isolation: a commit in one is immediately in the graph every other pushes from.

---

## 2. ACTIVE WORKTREES + TARGETS

| checkout | branch | what it is for |
|---|---|---|
| `~/hip-roadmap` | `roadmap` | Advisor lane (`HA-nn`) **and** the FM coordinator lane. Holds `docs/LANES.md`, the dispatch archive, `CLAUDE.md`'s STANDARD PREAMBLE, and this checkpoint. |
| `~/hip-vo` | `main` | Voice / governed-build lane. **Runs an older `CLAUDE.md` with no STANDARD PREAMBLE.** |
| `~/hip-cutover-demo` | `demo-cutover-build` | Demo lane (`VD-nn`). |
| `~/hip-dev` | `demo-presenter-package` | **The frozen demo — the fallback. NOT a lane.** Touching it is a NOT-pre-authorized class and needs Bill's explicit dispatch. |
| `~/hip-nc` | `natural-conversation` | Natural-conversation work. **No upstream configured** — nothing here is pushed anywhere. |
| `~/hip-harness` | `voice-latency` | Separate repo. Carries its own copy of harness code (TD-132). |

---

## 3. WORKER ASSIGNMENTS

| seat | assignment | notes |
|---|---|---|
| **CC-1 BUILD A** | **this session** (FM 2) | Also acting as FABLE MASTER coordinator while the model is being stood up. |
| **CC-2 BUILD B** | **the HA-78 session** | Ran the Groq estate sweep. **LANDED** — see §4. Seat now free. |
| **CC-3 VERIFY** | **UNASSIGNED** | |
| **CC-4 FLEX** | **UNASSIGNED** | |

**Roles are stable; assignments are temporary** (operating model §1). A seat name confers no
subject-matter ownership.

**Sessions observed on the machine at checkpoint time: 2 live `claude` processes**, down from 5
earlier in the day as the Voice and demo lanes closed out. Process identity does not map to seat —
`cwd` is `[REDACTED-USER-PATH]` for all of them because each `cd`s per command.

---

## 4. ACTIVE CAPABILITIES

### Board position

| lane | last issued | state |
|---|---|---|
| **FM** — `~/hip-roadmap` @ `roadmap` | **FM 2** | **IN FLIGHT** — this dispatch |
| Advisor — `~/hip-roadmap` @ `roadmap` | **HA-78** | **LANDED.** Next free: **HA-79** |
| Advisor — `~/hip-vo` @ `main` | **HA-74** | CLOSED |
| Demo — `~/hip-cutover-demo` @ `demo-cutover-build` | **VD-57** | LANDED — **nothing in flight** |
| Voice — `~/hip-vo` @ `main` | **Voice 42** | **IDLE** — session closeout. Next free: `Voice 43` |
| Research lab — `~/moshi-lab` | **ML-02** | LANDED |

**HA-78 LANDED — the Groq decommission is COMPLETE across the estate.** Five trees on
`openai/gpt-oss-120b` ahead of the **2026-08-16** cutoff (`~/hip-dev` `442050a`, `~/hip-cutover-demo`
`a869637`, `~/hip-harness` `14ac694`, plus HA-77's `~/hip-roadmap` and `~/hip-vo`). Zero residual
executable literals; live smoke green on all three new trees. **This was the only item on the board
with a hard external deadline, and it is closed.**

### FinishPlan position

**CURRENT STEP: 7 of 14 — "erasure prerequisites", finish condition "all erasure surfaces
enumerated". BLOCKED.**

Steps 1–6 are closed: the demo lane is past VD-39/VD-40; A6/A12/A16 landed at HA-38; C-14 was ruled
PROVEN 2026-08-11; and **`REQ_OFFER_MECHANISM` is MET — Bill, 2026-08-11**, which is step 6's exact
finish condition.

**What blocks step 7:** row 19 — `logs/transcript/` holds **850 files / 27,732 turns** of verbatim
member utterances, **the writer is still producing more**, and four options exist with **none
chosen**. Plan of record:
`docs/deliverables/HIP_FinishPlan__three-finish-lines-14-steps__v20260811.md`.

### Standing gates — both in force

- ⛔ **ERASURE-ENABLEMENT GATE** (Bill, 2026-08-06). No real-data erasure until **both** key-custody
  consolidation **and** the semantic-metadata cascade have landed. **Neither is started.**
- ⛔ **HEL 1.0 ISOLATION GATE** (Bill, 2026-08-10). HEL 1.0 is an immutable legacy DEV artifact;
  a clean HEL 2.0 chain starts before real household data. Reason is **format deficiency**, not
  plaintext retention.

### Evidence position

**Claims: 15 total — 10 PROVEN (6 Bill-ruled), 4 PARTIAL, 1 UNPROVEN** (C-09, erasure leaves no
readable trace — exactly what steps 7–9 exist to move).
**Debt: 58 OPEN on the roadmap lane** (46 summary-table + 12 section-form), plus 3 partial and 5
whose status cells are malformed. **The `main` lane runs its own `TD-V-nnn` register this checkout
cannot read**; TD-V-022/023/025/026/027/029 are open there.

---

## 5. OPEN DECISION QUEUE FOR BILL

**Nine carried, plus two opened by FM 2.** Ordered: blocking first.

### Blocking the current phase (step 7)

1. **Row 19 — `logs/transcript/` plaintext (HA-45).** Four options, none chosen. Blocks the phase.
2. **Row 19 consumers (HA-47).** `/api/transcript`'s demo band and
   `eval/passthrough_consent_vignette.py:202` genuinely need the words. The Q3-C sealed-content
   workaround was **deliberately not taken** — it needs the key decision that *is* condition 1 of
   the erasure-enablement gate. Four options, none chosen.
3. **`REQ_ERASURE_SURFACES` — six decisions (HA-43).** *"Governed surface"* and *"relevant keys"* are
   undefined and **block execution, not just wording**.

### Not blocking step 7

4. **Custody authorship (HA-18).** (a) who authors a household-attribute fact; (b) supersede or
   delete the one legacy D8 row — **graph surgery, destructive, not pre-authorized.**
5. **`_FRONTIER_CONFIRM_MSG` unclassified.** One live egress site needs a taxonomy ruling.
6. **HA-76 §9.4 — two PROPOSED sharpeners: confirm or strike.**
7. **Reprice the CORE token rate** — now **across five trees** (HA-77 opened it; HA-78 widened it).
8. **TD-125 false negative cascading into a HARD ZERO G1 violation.** TD-125 stays open and has now
   been named three times as *"passed BY THE RETRY — not validation"*.
9. **The demo batteries have no non-destructive smoke mode** (HA-78). `demo_integrity_battery.py`
   resets and re-seeds the demo graph, so it could not be run to check demo impact.

### Opened by FM 2

10. **GATE ANOMALY — "the Mini".** FM 2's machine gate says *"expect the Mini; STOP if not"*. This
    machine is a **MacBook Pro** (MacBookPro18,1), and **no Mac Mini exists on the tailnet** — only
    `iphone-13-mini`, an iOS device. FM 2 **proceeded** because four signals inside the dispatch
    point here: it names `~/hip-roadmap @ roadmap`, it says to serialize against live HA-78 (which
    ran and landed on this machine), it assigns CC-2 to the HA-78 session, and it builds on FM 1
    which ran here. **Recorded, not absorbed. If a Mini is real, FM 2 ran on the wrong machine.**

    **A Mini IS real in HIP's history, so this is not a phantom reference:** MANIFEST Section C
    carries `EVAL__chatterbox-tts-apple-silicon__v20260714_2310.md` — *"Chatterbox TTS (MIT)
    measured on **the Mini**"*. So Bill has used a Mac Mini for HIP work. **It is not on the
    tailnet now and it is not this machine**, and no HIP worktree, board, lock or service was found
    on anything but this MacBook Pro. **The question FM 2 cannot answer: whether a Mini exists that
    should have received this dispatch.** Everything FM 2 wrote is on `roadmap` and portable; if the
    answer is yes, nothing is lost but the work is on the wrong host.
11. **Proposed sixth entry to the never-overwrite exemption list — NOT self-granted.** A coordinator
    checkpoint's whole job is to be current, which is the exact argument that exempted `INDEX.md`,
    `BACKLOG.md`, `LATEST_DEBT.md`, `HIP_HANDOFF.md` and `LANES.md`. **The list is CLOSED and adding
    to it is Bill's ruling, not a session's** — so FM 2 versioned this file per the Naming Law and
    used a `LATEST_FM_CHECKPOINT.md` symlink for currency. **Flagged as proposed, exactly as Voice 2
    flagged `LANES.md` rather than self-granting it.** Until ruled, each checkpoint update writes a
    new version and re-points the symlink.

### Non-blocking, flagged for overrule (Voice 41, `~/hip-vo` @ `main`)

The 0.55 confirmation floor (**TD-V-025**), re-tiering L1's three stale probes (**TD-V-029**), and
whether `/ws/voice` egress belongs to A1b (**TD-V-022/023**).

---

## 6. REVIEW QUEUE

| package | built | state |
|---|---|---|
| `~/Desktop/hip_review_f2f17ca.zip` | 2026-08-12 13:33 | **ROUND CLOSED** — closeout on `main`, `42a6604`; findings became TD-V-018/019/021, all resolved |
| `~/Desktop/HIP_CODE_REVIEW.zip` | 2026-08-13 15:49 | **BUILT / SEND-UNCONFIRMED — findings NOT returned** |
| `~/Desktop/HIP_VO_REVIEW.zip` | 2026-08-13 16:21 | **BUILT / SEND-UNCONFIRMED — findings NOT returned** |
| `~/Desktop/HIP_CODE_REVIEW_REDACTED_20260813.zip` | 2026-08-13 16:44 | **BUILT / SEND-UNCONFIRMED — findings NOT returned** |

**No findings document, closeout, or TD attributable to the three 2026-08-13 packages exists on
either `roadmap` or `main`.** Whether they were sent is **UNKNOWN — only Bill knows.** FM 1's
extended-attribute evidence is circumstantial: `HIP_CODE_REVIEW.zip` and the redacted copy carry a
`com.apple.macl` (a sandboxed app was granted access, consistent with upload); `HIP_VO_REVIEW.zip`
carries **no extended attributes at all**, so nothing indicates it was ever opened.

**Staging directory** `~/Desktop/HIP_CODE_REVIEW/` holds `MANIFEST.txt` and
`APPENDIX_A_REAL_ADDRESS_FILE_LIST.txt`. The redacted package is a **separate artifact** from the
original — the delivered evidence was not scrubbed in place.

---

## 7. MACHINE / RUNTIME NOTES A SUCCESSOR NEEDS

- **SIX Neo4j instances are live** (was five; **NC 5 added the sixth on 2026-08-14**):
  bolt **7687** (brew default), **7688** (`~/neo4j-dev`), **7689** (`~/neo4j-hipdev-demo`),
  **7690** (`~/neo4j-cutover-demo`), **7691** (`~/neo4j-vo`, the HA lane — **fenced**),
  and **7692** (`~/neo4j-nc`, http 7479 — **the natural-conversation lane**, stood up by NC 5 on
  Bill's authorization).
  **7691 and 7692 both sit outside the 7687–7690 range** that surveys habitually scan — a survey
  that scans only that range now reports four graphs when six are live.
- **Lane→graph ownership is declared in each checkout's tracked `.hip-owns` / `.hip-graph`**, and
  `harness/lane_ownership.py` reads them before any destructive step. **NC 5 found `~/hip-nc`'s
  pair INHERITED from `~/hip-vo`, declaring 7691** — another lane's graph — and corrected them.
  A worktree cut from another lane's commit inherits its ownership declaration; **check these two
  files whenever a lane is opened.**
- **Services:** `voice_https_orch` on **`0.0.0.0:7860`** (LAN-reachable, from `~/hip-vo`);
  `demo_dashboard` on `127.0.0.1:7872` (from `~/hip-cutover-demo`).
- **Tailscale Funnel: `No serve config`** — nothing is published externally.
- **`~/.env.dev` does not exist**, so the STANDARD PREAMBLE item 3 hazard is currently absent.
- **No heavy suite was running at checkpoint time.** Check with `ps` before starting one —
  locks do not reveal it (FM 1 found a `--full` running with every lock free).
- **Locks:** take them through `scripts/hip_lock.py`. `repo` is **one lock per repository, shared by
  every worktree**. Exit **75** means refused — report the holder and defer. **Never delete
  `~/.hip-locks/*.holder` files**; ask `hip_lock.py who`.

---

## 8. WHAT IS NOT ESTABLISHED

- **Whether the 2026-08-13 review packages were sent.** UNKNOWN — circumstantial only.
- **The demo lane's in-flight state from this checkout.** Read from commit subjects on
  `demo-cutover-build`, not from that lane's own report (`docs/LANES.md` LIMIT 2).
- **Anything on `main` that this branch cannot see.** `roadmap` and `main` diverged at `688386f` and
  are ~430 / 107 commits apart. **A worker in `~/hip-vo` @ `main` cannot read this checkpoint, the
  board, or the operating model.** This is the largest hole in the coordination model and it is not
  fixed here.
- **`TD-R-174`, `TD-R-175`, `TD-R-176`** do not exist anywhere in the debt register. Whether they
  were skipped or lost is unestablished.
