# DISPATCH_FM1 — FABLE MASTER state reconciliation
Status: COMPLETE WITH FINDINGS
Reconciled-Against: `roadmap` — **gate HEAD `fb6cee7` (10:11 MDT); final HEAD `71601fc` (10:15 MDT)**

> ## ⚠ THE STATE MOVED FOUR TIMES WHILE THIS DISPATCH WAS READING IT
>
> This is a reconciliation of a board that did not hold still. Between the machine gate and the
> commit, **four other commits landed on `roadmap` and one on `main`**, from at least three
> different sessions. Every fact below is stamped with which HEAD it was read at.
>
> | time | commit | what changed |
> |---|---|---|
> | 10:03 | `6e9117b` (`main`) | Voice 41 closed out — `--full` failure recorded as TD-V-029 |
> | 10:08 | `b088eba` | **Voice lane closeout — lane IDLE**, "coordination moves to a new master session" |
> | 10:08 | `4d33ff7` | **VD-57 closeout — demo lane NOTHING IN FLIGHT** |
> | 10:11 | `58f45d6` | **HA-77 LANDED** and closed its row |
> | 10:15 | `71601fc` | **HA-78 claimed — URGENT Groq sweep** …and **carried this dispatch's FM row into its own commit** (FINDING 10) |
>
> **The headline a coordinator needs first:** the Groq model `llama-3.3-70b-versatile` **dies
> 2026-08-16 — two days out**. HA-77 fixed `~/hip-roadmap` and `~/hip-vo`; **`~/hip-dev` (8 files),
> `~/hip-cutover-demo` (7) and `~/hip-harness` (2) still carry the dying id** and HA-78 is in flight
> against them right now. Nothing else on this board has a hard external deadline.

**TYPE:** SURVEY — **READ-ONLY except two writes** (`docs/LANES.md` FM row, this doc). No product
code, no test code, no scripts, no graph, no service touched. Nothing was run that writes.

**LANE OPENED:** `FM` — FABLE MASTER coordinator, `~/hip-roadmap` @ `roadmap`. First number `FM 1`.

**CLAIM IMPACT: none.** This dispatch produced no evidence bearing on any ledger claim; it reports
the ledger's existing state and changes nothing in it.

---

## SEGMENT 0 — MACHINE GATE: **PASS**

| check | value |
|---|---|
| `whoami` | `bill-ai` |
| `hostname` | `[REDACTED-MACHINE-NAME]` |
| checkout | `[REDACTED-USER-PATH]/hip-roadmap` |
| `git rev-parse --show-toplevel` | `[REDACTED-USER-PATH]/hip-roadmap` |
| `git branch --show-current` | `roadmap` |
| `git rev-parse HEAD` | `fb6cee781da2136c437c1c91c0250f81b311381a` |

**The dispatch was issued with the working directory at `[REDACTED-USER-PATH]`, which is not a git
repository.** The target checkout was resolved by locating the tree that carries `docs/LANES.md`
and the dispatch archive — `~/hip-roadmap` is the only one of the five worktrees holding
`docs/LANES.md`, and it holds 249 of the dispatch docs. Gate re-run inside that tree: PASS.

**Tree NOT clean at gate time — reported, not touched:**

- `roadmap` was **ahead 2** of `origin/roadmap` (HA-77's then-unpushed commits — see FINDING 1).
- Four **untracked** demo-cutover-lane dispatch docs sit in this tree (`DISPATCH_DEMO_CUTOVER_*`,
  dated 2026-08-02/03). **Left exactly as found**; not staged, not read, not moved.

**RE-GATED at 10:15 after HEAD moved.** `whoami`, `hostname`, checkout and branch are unchanged and
still correct; only HEAD advanced, `fb6cee7` → `58f45d6` → `71601fc`. The gate is a check on
*which machine and which tree*, and it still passes — but the HEAD it was taken against is stale,
which is why both hashes are recorded above rather than one.

---

## SEGMENT 1 — MACHINE / RUNTIME MAP

### Worktrees — five, all of the one repository `~/hip-dev/.git`

| checkout | branch | HEAD @ gate 10:11 | HEAD @ close 10:15 | vs origin at close |
|---|---|---|---|---|
| `~/hip-dev` (main worktree) | `demo-presenter-package` | `3d4f46f` | `3d4f46f` | in sync |
| `~/hip-cutover-demo` | `demo-cutover-build` | `2cc5105` (ahead 4) | `2cc5105` | **in sync — pushed during this dispatch** |
| `~/hip-nc` | `natural-conversation` | `fb94c1c` | `fb94c1c` | no upstream configured |
| `~/hip-roadmap` | `roadmap` | `fb6cee7` (ahead 2) | **`71601fc`** | **ahead 1 (HA-78's claim)** |
| `~/hip-vo` | `main` | `6e9117b` | `6e9117b` | in sync |

**`~/hip-harness` is NOT a worktree of this repository** — it is a separate git repository
(own `.git`), branch `voice-latency`, HEAD `c0dabd0`. Named here because it sits in the same home
directory and reads like a lane; it is not one, and it does not share this commit graph.

`~/hip-vo` is on **`main`**, not `voice-port`. `voice-port` exists as a branch at `9ab0dd7` but no
worktree is standing on it.

**`~/hip-vo` @ `main` MOVED DURING THIS DISPATCH.** First read `f074d8f`; re-read minutes later
`6e9117b`. Confirmed a real advance (`f074d8f` is an ancestor), not a misread — commit `6e9117b`,
2026-08-14 10:03, *"Voice 41: --full ran for the first time on this lane and failed — TD-V-029,
none of it A1's"*. **A live session is committing on that lane right now.**

### Live Neo4j instances

| port | PID | instance conf |
|---|---|---|
| bolt 7687 | 1123 | Homebrew default (`Cellar/neo4j/2026.05.0`) |
| bolt 7688 | 1453 | `~/neo4j-dev` |
| bolt 7689 | 22330 | `~/neo4j-hipdev-demo` |
| bolt 7690 | 20331 | `~/neo4j-cutover-demo` |
| **bolt 7691** | 63555 | `~/neo4j-vo` (also HTTP 7478) |

**Five graphs are live, not four.** `~/neo4j-vo` on **7691** falls outside the 7687–7690 range the
dispatch named (FINDING 7). All five are bound to `127.0.0.1` only.

### Services on 7860 / 7872

| port | PID | bind | command | started | cwd |
|---|---|---|---|---|---|
| 7860 | 72415 | **`0.0.0.0` (all interfaces)** | `python -m server.voice_https_orch --host 0.0.0.0 --port 7860` | 2026-08-14 09:27:36 | `~/hip-vo` |
| 7872 | 95706 | `127.0.0.1` | `python -m server.demo_dashboard --host 127.0.0.1 --port 7872` | 2026-08-13 14:27:10 | `~/hip-cutover-demo` |

The 7860 orchestrator is the service Voice 41's report calls "restored on 7860". It is **LAN-reachable**,
not localhost-only (FINDING 8).

### Tailscale

**CLI is not on `PATH`**; queried through `/Applications/Tailscale.app/Contents/MacOS/Tailscale`.

- **Funnel: `No serve config`** — nothing is published. The 7860 bind is not publicly exposed.
- Node is up: `[REDACTED-MACHINE-NAME]` (`[REDACTED-TAILNET-ADDRESS]`), plus `bills-macbook-pro` and
  `iphone-13-mini` on the tailnet.

### Locks

`scripts/hip_lock.py who` — **`repo` FREE**; `graph:7687`, `graph:7688`, `graph:7689`, `graph:7690`,
`graph:7691` all **FREE**. Holder files in `~/.hip-locks/` are stale reports only and were **not
deleted**, per STANDARD PREAMBLE item 4.

`~/.env.dev` **does not exist** on this machine — **⚠ CORRECTED BY FM 19 (2026-08-14). THIS FINDING WAS A FALSE NEGATIVE; the original wording is left standing per the pre-authorized correction class (annotate, never silently patch).** FM 18 read the inode: **birth == 2026-07-21 18:02:18**, and a deleted-and-recreated file gets a NEW inode and a new birth, so **the file existed continuously through this reconciliation** and cannot have been absent at 10:11. **The demonstrated cause is a REPOINTED `HOME`** — not a hypothesis about an unknown failure mode, but one shown TWICE on 2026-08-14: VD-62's route-inventory test sets `os.environ["HOME"]` to a temp dir at MODULE SCOPE, and HA-87 reproduced the identical bug in its own test, where the process-wide mutation errored four unrelated tests and pushed suite skips 6→25. **Any `~/.env.dev` check running in that state reports ABSENT while the file sits untouched.** **CREATOR REMAINS UNATTRIBUTABLE** (no script writes it; `.zsh_history` is not extended-format so no command in it can be dated), and the 16:57 ctime touch remains a **LABELLED HYPOTHESIS** (a permission sweep consistent with FM 11's 16:56 window), not a finding. **The file was QUARANTINED by rename at FM 19 — not deleted — to `~/.env.dev.QUARANTINED-FM19`, same inode `5319612`.** — the item-3 hazard (a home file silently
redirecting a run to 7689 with `override=True`) is currently absent. The repo `.env.dev` carries no
`NEO4J_URI` line.

---

## SEGMENT 2 — BOARD + LANES

`docs/LANES.md` was read in full at `fb6cee7`. It is **LIVE and, where it can be checked against the
machine, accurate** — the Voice 41 row names commits `a6ec151 → fb94c1c → 47a28ca → c97fdfd →
6e9117b` "all pushed", and `origin/main` is indeed at `6e9117b` with nothing unpushed.

### Live lanes — **as of close, 10:15, HEAD `71601fc`**

| lane | prefix | last issued | in flight AT CLOSE |
|---|---|---|---|
| **FM — coordinator, `~/hip-roadmap` @ `roadmap`** | `FM n` | **FM 1** | **FM 1 — this dispatch** |
| Advisor — `~/hip-roadmap` @ `roadmap` | `HA-nn` | **HA-78** | **HA-78 IN FLIGHT — URGENT.** Groq sweep over the remaining three checkouts: `~/hip-dev`, `~/hip-cutover-demo`, `~/hip-harness`. **HA-77 LANDED** (`fb6cee7` / `f074d8f`). |
| Advisor — `~/hip-vo` @ `main` | `HA-nn` | **HA-74** | HA-74 CLOSED |
| Demo — `~/hip-cutover-demo` @ `demo-cutover-build` | `VD-nn` | **VD-57** (`c334fb7`, 08-14 10:10) | **NOTHING IN FLIGHT — lane clean, committed and pushed** |
| Voice — `~/hip-vo` @ `main` | `Voice N` | **Voice 42** | **NOTHING IN FLIGHT — lane IDLE (session closeout).** Next free `Voice 43` |
| Research lab — `~/moshi-lab` | `ML-nn` | **ML-02** | ML-02 LANDED |
| Frozen demo — `~/hip-dev` @ `demo-presenter-package` | — | — | **not a lane** — the fallback. **HA-78 is touching it under Bill's explicit dispatch**, which is otherwise a NOT-pre-authorized class. |

**Next free HA number: `HA-79`** (was `HA-78` at gate; HA-78 was claimed at 10:15). Gaps
deliberately preserved: `HA-57` (never issued), `VD-06`, `VD-09`, `VD-10`. Closed series that must
not be issued from: `D-nnn` (final D-162), `D-R-nnn` (final D-R-196), `D-D-nnn` (final D-D-161),
`Index Demo N` (final 35), `D-V-nnn` (never issued).

**THE VOICE LANE HAS EXPLICITLY HANDED OFF TO THIS ONE.** Its closeout row reads: *"The chat that
ran `Voice 38`–`Voice 42` is closing; coordination moves to a new master session."* It leaves
**three things a successor must not undo**, reproduced here because they are now FM's to protect:

1. The egress suite is **RED ON PURPOSE** at `server/demo_dashboard.py:2765`. Re-adding the
   `CLIENT_SIDE_MARKUP` exemption **hides TD-V-022, it does not fix it.**
2. `SPOKEN_CONFIRM_MIN_CONFIDENCE = 0.55` is a **MEASURED** placement between an observed mis-hear
   (0.427) and the observed correct band (0.581–0.846). **Moving it needs a re-measurement, not a
   preference** (TD-V-025).
3. **A1b is NOT started** and its reply-generation latency is deliberately **NOT estimated**, per
   Bill's ruling R-1 *(a) THEN (b)*.

**Recorded collisions:** HA-66 (genuine, two dispatches, later renumbered HA-69); `Voice 39`
(ambiguous citation, not a board collision); HA-50 / HA-51 (one dispatch each, parts split across
branches). Root cause named by the board itself: **the HA series has been minted from two diverged
branches since 2026-08-12.**

### 10 most recent `docs/dispatches/` files by mtime

| # | file | mtime | status line |
|---|---|---|---|
| 1 | `DISPATCH_HA76_bank-three-rulings__…__v20260814_0855.md` | 08-14 08:56 | BUILT |
| 2 | `DISPATCH_HA75_transcript-band-off-files__…__v20260814_0804.md` | 08-14 08:50 | BUILT |
| 3 | `DISPATCH_HA49A_ENVELOPE_BOUND__…__v20260812_1259.md` | 08-12 13:00 | BUILT |
| 4 | `DISPATCH_HA49_SESSION_KEY_AND_COMMITMENT__…__v20260812_1221.md` | 08-12 12:22 | BUILT |
| 5 | `DISPATCH_HA47_TRANSCRIPT_STORAGE_CONTRACT__…__v20260812_0948.md` | 08-12 09:50 | BUILT (docs + read-only) |
| 6 | `DISPATCH_HA46A_RECALL_AUDIT_CORPUS_ERASED__…__v20260812_0702.md` | 08-12 07:03 | BUILT |
| 7 | `DISPATCH_HA45_STOP_PLAINTEXT_AT_SOURCE__…__v20260811_2224.md` | 08-11 22:25 | **BUILT (row 7) / STOPPED (row 19)** |
| 8 | `DISPATCH_HA43_ERASURE_SURFACES_REQ__…__v20260811_2050.md` | 08-11 20:55 | BUILT (docs only) |
| 9 | `DISPATCH_HA41_TDR186_ERASURE_INVENTORY__…__v20260811_1510.md` | 08-11 15:20 | ALL THREE SEGMENTS COMPLETE |
| 10 | `DISPATCH_HA38_A6_A12_A16__…__v20260811_1330.md` | 08-11 13:22 | ALL FOUR SEGMENTS COMPLETE |

**HA-77 has no dispatch doc yet** — consistent with it being in flight. Voice 40/41/42 wrote their
docs on `main` or were docs-only, so they do not appear in this tree's archive.

### Running `claude` / CC processes — **DISCOVERABLE**

**Five live `claude` processes**, all with `cwd=[REDACTED-USER-PATH]` (each `cd`s per command, so cwd does
not identify a lane):

| PID | started |
|---|---|
| 99076 | 2026-08-06 13:15:28 |
| 99137 | 2026-08-06 13:15:50 |
| 27706 | 2026-08-13 17:11:42 |
| 64330 | 2026-08-14 07:47:05 |
| 75599 | 2026-08-14 10:03:00 *(this session)* |

**And one live long-running job, which is the operationally important one:**

```
PID 74522 (parent 1, detached), started 2026-08-14 09:51:46, STILL ALIVE
zsh -lc cd [REDACTED-USER-PATH]/hip-roadmap; set -a; . ./.env.dev; set +a; \
  PYTHONPATH=. ~/hip-dev/.venv/bin/python -m eval.harness --full \
  > …/c89329f1-959f-4016-802c-025606bf2a1a/scratchpad/c4.log
```

**A `--full` harness run (L1–L4, 100 iters, harness-owned server, dev graph) was executing inside
`~/hip-roadmap`** during Segments 0–5, owned by CC session `c89329f1` — **not this session** — and
it ran **without any lock held** (FINDING 2).

**It finished during this dispatch: exit code `0`, at 10:08** (`c4.done`). This is HA-77's
verification run, and its green result is what let HA-77 land at 10:11. FM 1 neither waited for it
nor interfered with it.

**Process count at close: 2 live `claude` processes**, down from 5 — consistent with the Voice and
demo lanes closing out at 10:08.

---

## SEGMENT 3 — OPEN STATE

### Claims ledger — `docs/deliverables/LATEST_HIP_ClaimsLedger.md` → `…v5-c14-proven__v20260811_1549.md`

**15 claims: 10 PROVEN / 4 PARTIAL / 1 UNPROVEN.** Of the 10 PROVEN, **6 are Bill-ruled** and 4 are
still marked `(draft)`.

| status | claims |
|---|---|
| PROVEN — Bill-ruled | C-02, C-03 (08-07); C-07, C-10 (08-09); C-15 (08-10); C-14 (08-11) |
| PROVEN (draft) | C-01, C-06, C-12, C-13 |
| PARTIAL | C-04, C-05, C-08 (draft); **C-11 — Bill 08-09** |
| **UNPROVEN** | **C-09** — erasure leaves no readable trace |

C-09 is the single unproven claim and is exactly what FinishPlan steps 7–9 exist to move.

### Tech debt — `docs/techdebt/LATEST_DEBT.md` → `DEBT_REGISTER__v20260807_1057.md`

The register holds debt in **two formats**, and both must be counted:

| form | OPEN | PARTIAL / IN_PROGRESS | RESOLVED | INDETERMINATE |
|---|---|---|---|---|
| summary table | 46 | 3 | 16 | 5 |
| per-TD sections (TD-R-177…190) | 12 | 0 | 2 | 0 |
| **total** | **58** | **3** | **18** | **5** |

**OPEN ids — summary table (46):** TD-101, TD-102, TD-103, TD-104, TD-109, TD-110, TD-113, TD-115,
TD-118, TD-120, TD-122, TD-123, TD-124, TD-125, TD-127, TD-128, TD-129, TD-130, TD-131, TD-132,
TD-133, TD-135, TD-136, TD-138, TD-140, TD-142, TD-145, TD-146, TD-147, TD-148, TD-149, TD-150,
TD-152, TD-153, TD-154, TD-155, TD-156, TD-157, TD-158, TD-160, TD-R-161, TD-R-162, TD-R-163,
TD-R-168, TD-R-171, TD-R-173.

**OPEN ids — sections (12, all "FILED, NOT FIXED"):** TD-R-177, TD-R-178, TD-R-179, TD-R-180,
TD-R-181, TD-R-182, TD-R-183, TD-R-185, TD-R-187, TD-R-188, TD-R-189, TD-R-190.
*(TD-R-185 carries no explicit marker; it is recorded "OBSERVATION FROM COLLECTED DATA, NOT A DEFECT
CLAIM… Not investigated. Item 12: filed, not chased." Counted OPEN.)*

**PARTIAL:** TD-108 (IN_PROGRESS), TD-126 (PARTIALLY FIXED), TD-139 (PARTIALLY CLOSED).
**RESOLVED in sections:** TD-R-184 (HA-39), TD-R-186 (HA-40).

**This count is for the `roadmap` lane only.** The `~/hip-vo` @ `main` lane runs its own `TD-V-nnn`
register, which this checkout cannot read; per Voice 41, **TD-V-022/023/025/026/027/029 are OPEN**
and TD-V-024/028 RESOLVED there. Bare TD numbers do not resolve across branches (preamble item 10).

### FinishPlan — plan of record, `HIP_FinishPlan__three-finish-lines-14-steps__v20260811.md`

**CURRENT STEP: 7 of 14 — "erasure prerequisites", finish condition "all erasure surfaces
enumerated". IT IS BLOCKED (see pending decisions 1–3).**

Established, not assumed:

- Steps **1–2** (VD-39 demo blockers, VD-40 rehearsal) — the demo lane is at **VD-56**, well past both.
- Steps **3–5** (A6, A12, A16) — built and landed by **HA-38** (2026-08-11); **C-14 ruled PROVEN by
  Bill 2026-08-11**, which is A12's stated consequence.
- Step **6** (A1–A20 rerun → Offer REQ MET) — **`REQ_OFFER_MECHANISM` Status: MET — ruled by Bill,
  2026-08-11.** That is step 6's exact finish condition, so step 6 is closed.
- Step **7** — every roadmap dispatch since (HA-41, HA-43, HA-45, HA-46A, HA-47, HA-49, HA-49A,
  HA-75, HA-76) is erasure-surface / transcript-storage work. **HA-45 is the live edge and its
  status line reads `BUILT (row 7) / STOPPED (row 19)`.**

The remaining order for reference: 8 Phase-3 crypto → 9 erasure acceptance → 10 Phase-4 quorum →
11 test cleanup → 12 live-model rule → 13 claims refresh → 14 external review.

### Pending Bill decisions — **9 on this lane** (6 blocking step 7, 3 new from HA-77)

Per `docs/HIP_HANDOFF.md` CURRENT STATE, plus the board at close:

1. **Row 19 — `logs/transcript/` plaintext (HA-45).** ⛔ *"ROW 19 IS STILL STOPPED AND STILL BLOCKS
   THE PHASE."* 425 `.jsonl` + 425 `.txt` = 850 files, 27,732 turns, ~10.5 MB, span 07-18 → 08-11,
   **and the writer is still producing new plaintext.** Four options in HA-45's doc, **none chosen.**
2. **Row 19 consumers (HA-47).** Same underlying decision at the contract stage: `/api/transcript`'s
   demo band and `passthrough_consent_vignette.py:202` genuinely need the words. Q6 ruled it
   blocking. The Q3-C sealed-content workaround was **deliberately not taken** — it needs the key
   decision that *is* condition 1 of the erasure-enablement gate. Four options, **none chosen.**
3. **`REQ_ERASURE_SURFACES` — six decisions (HA-43).** Two words in Bill's lifecycle are undefined
   and **block execution, not just wording**: *"governed surface"* (all nineteen → fails today at
   eleven rows; graph + payload store → passes today) and *"relevant keys"* (destroying a shared
   household seal key erases other members, leaving lifecycle step 5 not executable).
4. **Custody authorship (HA-18).** (a) Who authors a household-attribute fact; (b) supersede or
   delete the one legacy D8 row. **Clearing it is graph surgery — destructive, not pre-authorized.**
   `REQ_DERIVED_WRITE_CUSTODY` remains NOT MET.
5. **`_FRONTIER_CONFIRM_MSG` unclassified (A1 speech taxonomy).** One live egress site
   (`server/voice_orch.py` via `control_flow.handle_frontier_request`) is unclassified and needs a
   ruling.
6. **HA-76 §9.4 — two PROPOSED sharpeners: confirm or strike.** The kernel process boundary as the
   conversation-state owner, and whether that owner inherits Q1–Q3 so state never becomes erasure
   surface #22.

**NEW at 10:11 — HA-77's three, landed after the gate:**

7. **Reprice the CORE token rate.** CORE swapped to `openai/gpt-oss-120b`; the cost model still
   carries the old rate.
8. **A TD-125 false negative was seen cascading into a HARD ZERO G1 violation.** TD-125 has now
   been named twice more as "passed BY THE RETRY — not validation" (HA-74, Voice 41) and stays open.
9. **Nothing arbitrates machine memory across concurrent `--full` runs.** Voice 41's run and
   HA-77's **OOM-collided**. This is a direct constraint on any FM plan that dispatches CC-1 BUILD A
   and CC-2 BUILD B to run batteries at the same time on this machine.

**Also outstanding, explicitly non-blocking** (Voice 41, `~/hip-vo` @ `main`, flagged for overrule):
the 0.55 confirmation floor (**TD-V-025**), re-tiering L1's three stale probes (**TD-V-029**), and
whether `/ws/voice` egress belongs to A1b (**TD-V-022/023**).

**Two standing gates remain in force** and are named here because they govern what any worker may
be dispatched to do:

- ⛔ **ERASURE-ENABLEMENT GATE** (Bill, 2026-08-06) — no real-data erasure until **both** key-custody
  consolidation **and** the semantic-metadata cascade have landed. **Neither is started.** Only
  Ruling 2's backup exclusions have landed, and those are a precondition, not either condition.
- ⛔ **HEL 1.0 ISOLATION GATE** (Bill, 2026-08-10) — HEL 1.0 is an immutable legacy DEV artifact;
  start a clean HEL 2.0 chain before real household data. The reason is **format deficiency**
  (no keyed commitment; a raw dictionary-testable `payload_sha256`), **not** plaintext retention.

---

## SEGMENT 4 — EXISTING COORDINATION ARTIFACTS

Searched `docs/` by filename and by content, excluding `docs/rendered/` (whitepaper renders produce
incidental prose matches).

| item | result |
|---|---|
| operating-model doc | **NONE.** Two content hits are unrelated: a job-search line in `SESSION_TRANSFER__july6-full-state-handoff` and a ranker recommendation in `HIP_CuratorResearch_B`. |
| coordinator checkpoint | **NONE** |
| worker board | **NONE** |
| review queue | **NONE.** The one hit, `docs/planning/PROMOTION__dev-demo-workflow__v20260702_1938.md`, is a *corpus-curation* review queue (auto-accept vs adjudicate), not a dispatch queue. |
| "FABLE MASTER" anywhere in `docs/` | **NONE** |

**What does exist, and is the nearest thing to each — named so no replacement is built over it:**

- **`docs/LANES.md`** — the one live dispatch board. It issues numbers, records in-flight work,
  closed series and collisions. **This is the existing coordination instrument**; FM claims into it
  rather than creating a parallel board.
- **`docs/HIP_HANDOFF.md`** — the live per-lane state document (CURRENT STATE, updated in the same
  commit as each dispatch).
- **`docs/design/HIP_PROCESS__moshi-research-lane-method__v20260813_1500.md`** — a lane-method doc,
  but scoped to the `~/moshi-lab` research lane only.
- **`CLAUDE.md`** — the STANDARD PREAMBLE, Naming Law, NUMBER-CLAIM LAW and RECAP-IDENTITY LAW.

**No replacement was created and nothing above was modified.**

---

## SEGMENT 5 — REVIEW QUEUE

Packages live on `~/Desktop`, outside every repository.

| package | size | built | state |
|---|---|---|---|
| `hip_review_f2f17ca.zip` | 10.9 MB | 2026-08-12 13:33 | **ROUND CLOSED** |
| `HIP_CODE_REVIEW.zip` | 17.5 MB | 2026-08-13 15:49 | **BUILT — findings NOT returned** |
| `HIP_VO_REVIEW.zip` | 3.3 MB | 2026-08-13 16:21 | **BUILT — findings NOT returned** |
| `HIP_CODE_REVIEW_REDACTED_20260813.zip` | 82.5 MB | 2026-08-13 16:44 | **BUILT — findings NOT returned** |
| `~/Desktop/HIP_CODE_REVIEW/` (staging dir) | — | 2026-08-13 16:03 | `MANIFEST.txt` (56 KB) + `APPENDIX_A_REAL_ADDRESS_FILE_LIST.txt` (6.4 KB) + `hip-roadmap/` + `hip-cutover-demo/` |
| `hip_source.zip` / `hip_main.zip` | 67.6 MB / 362 MB | 2026-08-12 16:54 / 16:59 | source snapshots, not review packages |

**The 2026-08-12 round is CLOSED, with a closeout document.** On `~/hip-vo` @ `main`:
`docs/general/CODE_REVIEW_CLOSEOUT__2026-08-12-review-closed-at-gate-run-8f2f51efe032__v20260813_1955.md`
(+ `LATEST_` symlink), landed by **HA-74 Part C, `42a6604`** — *"gate PASS at 8f2f51efe032 — REQ MET,
closures recorded, review CLOSED"*. Its findings became TD-V-018 / TD-V-019 / TD-V-021, all resolved.

**The 2026-08-13 round has produced nothing back.** A search of `docs/` on **both** `roadmap` and
`main` finds **no findings document, no closeout, and no TD** attributable to the three 2026-08-13
packages. Status: **BUILT, SENT-STATE UNCERTAIN, FINDINGS PENDING.**

**On whether they were sent — stated as inference, not fact.** macOS extended attributes show
`HIP_CODE_REVIEW.zip` carrying both `com.apple.lastuseddate#PS` and `com.apple.macl`, and
`HIP_CODE_REVIEW_REDACTED_20260813.zip` carrying `com.apple.macl` — a `macl` is written when a
sandboxed app (browser, Mail) is granted access to a file, which is **consistent with** upload.
**`HIP_VO_REVIEW.zip` has no extended attributes at all**, so nothing indicates it was ever opened or
sent. This is circumstantial; **only Bill knows what was actually sent.**

The redaction package matches the standing evidence rule: `APPENDIX_A_REAL_ADDRESS_FILE_LIST.txt`
enumerates the real-address files, and the redacted copy is a **separate artifact** from
`HIP_CODE_REVIEW.zip` — the delivered original was not scrubbed in place.

---

## SEGMENT 6 — LANE CLAIM

Two writes, exactly as scoped — **and the first of them did not land the way it was meant to:**

1. `docs/LANES.md` — new **FM** row at the top of the Live lanes table: lane `FM` = FABLE MASTER
   coordinator, `~/hip-roadmap` @ `roadmap`, LAST NUMBER ISSUED `FM 1`, IN FLIGHT `FM 1`, with the
   dispatch doc's path and a note that workers claim in their own lane's series, never from `FM`.
   **This row reached the board inside HA-78's commit `71601fc`, not FM 1's — see FINDING 10.** It is
   present, correct and committed; it is simply not in this dispatch's own commit.
2. `docs/dispatches/DISPATCH_FM1_master-state-reconciliation__…__v20260814_1011.md` — this document.

Committed with **explicit pathspecs only**; the `repo` lock was taken through `scripts/hip_lock.py`
around the git operations and nothing else (item 9 — no lock held around any survey or read). No
`git add -A`, no `git commit -a`. **The four untracked demo-cutover docs were verified absent from
the commit**, and no other lane's file was staged.

No third path was written. The FM row is closed out with the landing commit in a second, LANES.md-only
commit, per NUMBER-CLAIM LAW obligation 3.

---

## FINDINGS — 10 filed, none blocking

Filed under the FINITENESS RULE (preamble item 12): none of these blocks step 7's acceptance
criteria, so each is **filed and stays filed**. FM 1 chased none of them.

**FINDING 1 — the passenger exposure changed hands mid-dispatch, and still exists.**
At gate time `roadmap` was ahead 2 with HA-77's `9206c78` (09:11, board claim) and `fb6cee7` (09:43,
the Groq swap — 10 files, 310 insertions), so FM 1's push would have published another lane's work.
**HA-77 then pushed its own work at 10:11, clearing that exposure before FM 1 reached its commit.**

**It is now HA-78's.** At close, `roadmap` is ahead 1 with `71601fc` (10:15, HA-78's board claim),
so **FM 1's push publishes HA-78's claim commit.** Named per preamble item 8, whose test is *"who
decided"*, not *"was harm done"*. **Materially mitigating:** `71601fc` touches only `docs/LANES.md`,
and the NUMBER-CLAIM LAW's whole purpose is for a claim to be visible to other lanes as early as
possible — publishing it is aligned with what that row is for, though it was still not HA-78's
decision to make. Pushing was this dispatch's instruction and item 8 forbids leaving a commit
unpushed.

**FINDING 2 — a `--full` harness run executed in this worktree with no lock held, and the collision
it risked had already happened to someone else the same morning.**
PID 74522, 09:51:46 → 10:08 (exit 0), session `c89329f1`, `eval.harness --full` in `~/hip-roadmap`
against the dev graph — while `hip_lock.py who` reported `repo` and all five `graph:` locks **free**
throughout. Preamble item 4 makes lock acquisition a precondition of the tooling; this run bypassed
it. **This is not theoretical:** HA-77's own closing note records that Voice 41's `--full` and this
one **OOM-collided**, and Voice 41's row records its `--full` being *"contaminated by the concurrent
HA-77 lane's then-uncommitted CORE model swap."* Two lanes ran the heaviest job in the repo
simultaneously, unlocked, and each corrupted the other's result. Filed as a lock-protocol
observation; see pending decision 9, which is the same fact stated as a decision Bill owes.

**FINDING 3 — four untracked foreign dispatch docs in the `roadmap` tree.**
`DISPATCH_DEMO_CUTOVER_{PORT_SCRIPTS,SELFCHECK_C2GUARD,VERIFY_CAVEAT_PANEL,WIRE_AND_PROVE_C1}`,
dated 2026-08-02/03 — demo-lane documents sitting uncommitted in the advisor lane's checkout for
~12 days. Left exactly as found.

**FINDING 4 — the debt register's header is stale against its own body.**
`LATEST_DEBT.md` reads `RECONCILED-AGAINST: session 2026-08-07, HA-14`, but the file carries
sections through **TD-R-190**, filed 2026-08-12 by HA-47. The register has been appended to five
days past its own reconciliation line.

**FINDING 5 — five debt rows have malformed status cells, so no automated open-count can be exact.**
TD-134, TD-143, TD-144, TD-R-164 and TD-R-165 carry source-column text where the status belongs
(e.g. TD-R-164 reads `current file \`, TD-143 reads `Voice 37 build, 2026-08-02; D-127 fix; D-129
ruling`). Counted INDETERMINATE above rather than guessed at.

**FINDING 6 — TD-R-174, TD-R-175 and TD-R-176 do not exist anywhere in the register.**
The table ends at TD-R-173 and the sections begin at TD-R-177. Zero occurrences of the three
intervening ids in the file. Whether they were skipped or lost is not established here. Recorded
because the board's own precedent (HA-57) is that a gap must be *known* to be a gap.

**FINDING 7 — a fifth live graph sits outside the range this dispatch scanned.**
`~/neo4j-vo` listens on **bolt 7691** (HTTP 7478), PID 63555. The dispatch asked for 7687–7690, and
a scan of only that range reports four graphs when five are live. `graph:7691` has a lock key and a
holder file dated 2026-08-14 08:14, so the lane knows about it.

**FINDING 8 — `voice_https_orch` binds `0.0.0.0:7860`, not localhost.**
Every Neo4j instance and the demo dashboard bind `127.0.0.1`; the voice orchestrator alone is
LAN-reachable. **Tailscale Funnel reports `No serve config`, so there is no public exposure** — the
finding is the inconsistent bind, not a live internet-facing service.

**FINDING 9 — the board's LIMIT 1 applies to this lane too, and FM should not be assumed exempt.**
`docs/LANES.md` lives on `roadmap`; `main` diverged at `688386f` and is 430 / 107 commits apart. A
worker dispatched into `~/hip-vo` @ `main` **cannot read the FM row claimed here**, exactly as it
cannot read the HA rows. A FABLE MASTER coordinator that dispatches CC workers across both branches
inherits this hole unchanged. **Not fixed by this dispatch — made visible.**

**FINDING 10 — ANOTHER LANE COMMITTED THIS DISPATCH'S UNCOMMITTED BOARD ROW. The exact inverse of
the D-158 incident, and it happened to FM 1's own claim.**

FM 1 wrote its `FM` row into `docs/LANES.md` at ~10:13 and had not yet committed. At **10:15**,
HA-78 committed `71601fc` — *"HA-78: claim the board row"* — and that commit contains **three**
added lines: HA-78's own row, the updated next-free-number line, **and FM 1's FABLE MASTER row**.
Verified directly: `git show 71601fc -- docs/LANES.md` includes the `FABLE MASTER` line, and the FM
row is present in `HEAD`'s `docs/LANES.md` although FM 1 has committed nothing.

**Mechanism.** `docs/LANES.md` is one of the five never-overwrite-exempt shared files. A plain
`git add docs/LANES.md` stages *the whole file*, including any other lane's in-progress edits.
**Preamble item 2 anticipates exactly this and prescribes the fix** — for a shared file, *"stage
surgically: save the union copy, reset the file to HEAD, apply only your own rows, `git add`,
restore the union."* That procedure was not followed here.

**Why it matters more than the D-158 case it mirrors.** D-158 published another lane's *committed*
work; this published another lane's *uncommitted working-tree* edit — work that had not been
finished, reviewed, or chosen for the record by its author. And it lands on the one file whose
integrity the NUMBER-CLAIM LAW depends on.

**Consequence for this dispatch, stated plainly rather than papered over:** NUMBER-CLAIM LAW
obligation 2 requires a lane to claim *in its first commit*. **`FM 1`'s row is on the board and the
number is unambiguously claimed — but it landed inside HA-78's commit, not FM 1's.** The claim is
valid in substance (the row is committed, visible, and attributable) and defective in form. FM 1
did not re-add or re-write the row: it is already in `HEAD` and byte-correct, and rewriting it
would only create a spurious diff. **Recorded, not corrected.**

**This is the single most important finding for the FABLE MASTER model.** Four lanes writing to one
board file on one branch collided three separate ways in one morning — HA-66's duplicate number,
the OOM'd concurrent `--full` runs, and now a swallowed working-tree row. A coordinator dispatching
four CC workers into these same shared files will hit this constantly unless staging discipline on
`docs/LANES.md` is enforced by tooling rather than remembered.

---

## DEVIATION FROM THE NAMING LAW — flagged, not bypassed

The Naming Law's Workflow item 3 requires a new dispatch doc to be registered with a row in
`docs/INDEX.md` under the `## dispatches/` section, and a `LATEST_` symlink where applicable.
**This dispatch's instruction restricts writes to exactly two paths** — the FM lane row and this
document — so **no `docs/INDEX.md` row was added and no symlink was created.**

Per preamble item 5 ("on conflict with this law: flag it and follow the law — do not bypass"), the
conflict is recorded here rather than resolved by a session. **The narrower, explicit instruction
was followed.** `docs/INDEX.md` registration for `DISPATCH_FM1` is **owed** and is a one-row write
whenever Bill authorizes the third path.

---

## WHAT FM 1 DID NOT DO

- Ran nothing that writes: no harness, no gate, no seed, no reset, no service start or stop.
- Touched no graph, no key material, no product code, no test code, no baseline.
- Did not interrupt, inspect beyond `ps`/`lsof`, or interfere with the live `--full` run (PID 74522)
  or the live Voice lane on `~/hip-vo` @ `main`.
- Did not create an operating-model doc, coordinator checkpoint, worker board or review queue —
  Segment 4 says report, and explicitly says do not create replacements.
- Ruled nothing MET, moved no claim status, re-tiered no acceptance row, changed no baseline.
