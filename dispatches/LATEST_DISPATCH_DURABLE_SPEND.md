# DISPATCH_DURABLE_SPEND — spent-ness survives the process, `--full` unmasks a blocker, and the mute guard is built

Status: BUILT
Reconciled-Against: roadmap `dded3ae` (pre-build HEAD). **LANDED AT `4bb78c3`** — backfilled by the immediately following commit, because a commit cannot contain its own hash.

**HA-08** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD (code)**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1625.md`,
**§12 LANDING ORDER step 5** (step 4 follows separately).
**NOTHING RULED MET.**

**LINEAGE:** drafted as HA-07; that number was spent on the standing-rules check
(`dded3ae`). This dispatch is **HA-08**.

## 1. CHECK FIRST

| Item | Found | Action |
|---|---|---|
| §12 step 5 | HA-06's `OfferInstanceRegistry` — one instance per situation, **in a dict**, and its own docstring says the guarantee dies with the process | **Built the durable machine.** HA-06 untouched. |
| **Item 4's guard-metric port** | **ALREADY ON ROADMAP.** `scripts/run_harness.sh` already reads `memory_pressure`'s free percentage, keeps the 2GB floor, and fails closed on an unreadable value — ported by **D-D-161** and filed as **TD-R-166**. `f07a630` is not an ancestor because it was ported, not merged. | **Nothing to port.** What remained was the half that matters: run `--full` and report item 12 honestly (§4). |

## 2. THE DURABLE SPEND MACHINE (items 1–3)

`harness/spend_ledger.py`. Append-only JSONL at
`logs/offer_control_plane/spend_ledger.jsonl`, `fsync`ed per append.

- **`Transition`** — §9's five permitted edges, closed. A string transition is refused.
- **A situation is SPENT FROM PRESENTATION**, not from a terminal state. R8's first
  sentence is explicit; everything after is bookkeeping about an already-spent situation,
  which is why no terminal state clears `is_spent` and there is no edge back to ELIGIBLE.
- **Append-only, deliberately.** R8's terminal states are permanent, and a store that can
  be updated in place can be updated backwards. The ledger's history IS its state; spent-ness
  is derived by replay, not held in a mutable cell.
- **`present()` refuses a second attempt AND RECORDS THE REFUSAL.** A silent refusal would
  leave no evidence that anything tried to re-present — which is what an audit needs most.
- **NOT the household graph (R20).** A standing test AST-scans the module and fails if it
  imports `neo4j`, `memory_engine.*`, or `harness.extraction_queue`. R21 forbids a decline
  becoming a fact about the member; the cleanest guarantee is that the two never share a store.

## 3. THE PROOFS — `eval/test_spend_ledger.py`, 18 tests, 18 pass

**Item 2's restart proof is a REAL PROCESS KILL, not an assertion.** One subprocess
presents and exits — its interpreter, its ledger object and every dict it held are gone. A
second, independent `sys.executable` starts, replays the file, and is refused.
**HA-06's in-process registry would pass a same-process test and fail this one**, which is
the entire difference step 5 exists to make.

**And that proof is itself anti-vacuity-checked:** with no prior process, the second
child's presentation SUCCEEDS. So the refusal is caused by the durable record, not by a
broken child or an unpresentable situation.

| Twin | What it proves |
|---|---|
| present-after-restart refused | the durable record survives the process (above) |
| replayed event → same `situation_id`, creates nothing | built on HA-03's normalisation; exactly one PRESENTED event survives, and only the refusal is added |
| second presentation refused, **refusal recorded** | and the record is durable — re-read from a fresh ledger |
| every terminal state leaves it spent | ACCEPTED / DECLINED / LAPSED / INVALIDATED, **each its own case** so a regression names the state |
| one terminal state only | a decline cannot be overwritten by an acceptance after the fact |
| torn final line | a process killed mid-append must not un-spend what came before — fail-closed |
| **ANTI-VACUITY** | a fresh situation presents once; distinct situations are independent |

## 4. `--full` — RUN, AND ITEM 12 REPORTED HONESTLY (item 4)

**The guard did NOT refuse.** `memory_pressure` reported **12.16GB free** against the 2GB
floor. The old metric, measured alongside: **`vm_stat` raw Pages free = 0.06GB** — the
understatement the port fixed, ~200x on this machine right now.

**`--full` then ABORTED at Layer 2:**

```
795 passed, 9 xfailed          <- standing batteries green
== Layer 2: demo regression
FIXTURE DRIFT: D8 decryption returned None — key mismatch or corrupt ciphertext
               for (household,dad,risk_pattern)
```

**ITEM 12 IS NOT SATISFIED, and this is the first time in weeks `--full` got far enough to
say why.** The memory guard's refusal had been MASKING a real Layer-2 blocker — fixing the
metric did not merely enable `--full`, it uncovered what the refusal was hiding.

**NOT CAUSED BY THIS SESSION'S WORK — evidenced, not asserted.** The D8 row exists with
`sensitivity='high'`, `key_version=2`, ciphertext and encrypted_dek both present, `dyad_id`
and `recipient_ref` null: household-tree-sealed, and the failure is an unwrappable
household key, **not** D-R-196's sensitivity change (which requires a label, and this row
has one). `~/hip-keys/household.seal.key` was last modified **2026-08-05 09:02**, untouched
by any dispatch today, and this session's fixtures left **zero** household-owned facts.

**NOT BISECTED** — finding the commit or environment change that broke the D8 wrap is its
own dispatch. **Filed as TD-R-171**, which records the consequence plainly: item 12 cannot
be satisfied by any dispatch until this clears.

## 5. THE TD-R-170 MUTE GUARD (item 5) — built exactly to the ruling

`scripts/dispatch_done.sh` checks output mute state **before** attempting playback.
Distinct causes, distinct exit codes, and **the script does not modify system volume or
mute state**. Its header now states what a zero exit means: *the playback command completed
on a non-muted output — NOT that the alert was audible.*

**ACCEPTANCE — three executed runs, raw output:**

```
##### (a) MUTED
$ osascript -e 'output muted of (get volume settings)'
true
$ scripts/dispatch_done.sh findings
dispatch_done: refused: output is muted — the alert would NOT have been audible.
Playback was NOT attempted. Unmute and re-run, or report the refusal.
EXIT: 4

##### (b) UNMUTED
$ osascript -e 'output muted of (get volume settings)'
false
$ scripts/dispatch_done.sh findings
EXIT: 0                        <- COMMAND success only; audibility is Bill's to confirm

##### (c) MUTE STATE UNREADABLE  (osascript shadowed by a failing stub on PATH)
$ PATH=<stub>:$PATH scripts/dispatch_done.sh findings
dispatch_done: refused: output mute state could not be determined (got <empty>)
— playback was NOT attempted rather than played blind.
EXIT: 5
```

Mute was set for (a) and **restored immediately**; final state `muted=false`. Run (b) is
reported as command success only — **this dispatch does not claim it was audible**, which
is the ruling's own distinction and needs Bill's confirmation.

## 6. RUNS (item 8)

| Run | Result |
|---|---|
| Standing battery | **812 passed, 1 skipped, 9 xfailed** — 795/9 + the 18 added tests |
| `--layer 7` L7 / L7V2 | **27/27** / **27/28** |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS** |
| Memory harness | **13/17**, failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the pin |
| `--full` | **ABORTED at Layer 2** (§4). Item 12 NOT satisfied. |

**The 1 skip is named rather than glossed:** `eval/test_record_graded_refusal.py:295 — "no
guarded turns recorded yet"`, a pre-existing conditional skip in a battery this dispatch
did not touch. All 18 spend-ledger tests pass. (Noted in passing: that battery skipping
when the record log has no guarded turns is a mild vacuity risk in the REQ HA-04/HA-05
amended — not chased here.)

## 7. FINDINGS

1. **TD-R-171 — `--full` aborts at Layer 2 on the D8 fixture drift.** Blocks item 12 for
   every dispatch until cleared. Not caused by this session (§4); not bisected.
2. **TD-R-172 — every fixture-writing battery leaks a per-owner `*.seal.key` to
   `~/hip-keys/` and never removes it.** 18 today: `_snd_*`/`_probe_*` from D-R-196/HA-02,
   **and `memtest-*` from the memory harness itself** — a general harness-hygiene gap, not
   one battery's bug, and calling it only mine would be wrong. **DELIBERATELY NOT FIXED:
   CLAUDE.md's NOT-pre-authorized list names "key destruction" explicitly.** Deleting 18
   key files is exactly the tidy-up a session must not do on its own initiative.
3. **The guard-metric port was already done** (§1) — D-D-161/TD-R-166. Re-porting it would
   have been busywork presented as progress.
4. **`control_flow.py`'s stale "stubs — NOT connected" comment** — fifth report
   (HA-01, HA-02, HA-03, HA-06, here). Still outside every dispatch's scope that finds it.

## 8. SCOPE HELD (item 6)

Fixtures only. Nothing presents to a real member, nothing initiates, nothing is enabled.
`harness/offer_instance.py`, `harness/material_change.py` and `harness/initiation.py` were
not touched. The mute guard's scope was the alert script and this ruling record only.
New battery registered under the manifest mechanism (item 7).
