# DISPATCH_HA34_MUTATION_BASELINE — the pre-HA-33 baseline is identified and proven; **STOPPED, no restoration mechanism exists**

Status: **STOPPED AT ITEM 3 — NEEDS BILL**
Reconciled-Against: roadmap `a2c27be`
Filed: 2026-08-11 (HA-34)
Decision-Owner: Bill
Authority: Bill's ruling 2026-08-11 — repair the mutation-test starting state before the HA-33 build
Predecessor: `DISPATCH_HA33_WRITE_LOSS__reproduced-fixed-proven-blocked-by-l7v2-line-shift__v20260810_2015.md`

**Nothing was built. No product code, no mutation-tool code, and no log line was changed.**
Items 1 and 2 are COMPLETE and their answer is affirmative. Item 3's answer is **NO** — the
tooling has no way to select or restore a baseline — and item 3 instructs that this is a STOP.
Items 4 (census, fingerprint schema, RELOCATED build) and the HA-33 reapply were therefore
**not started**, deliberately.

---

## ITEM 1 — THE LAST CONTROLLED PRE-HA-33 RUN IS **RECORD 141**, `2026-08-10T22:50:28.012131+00:00`

Not assumed from its position in the file. Proven from four independent angles, each of which
would have falsified the answer on its own.

### 1a. SOURCE SHAPE — a live in-memory sweep of the current tree

`run_sweep(TARGETS)` executed against the working tree at `a2c27be`. This is the same call
Layer 7 makes at `eval/harnesslib/layer7_crypto_v2.py:1571`, run in isolation — `mutation_score`
and `mutation_targets` imported directly, `layer7_crypto_v2` never imported, so
`write_survivor_trend` was never reached.

```
LIVE SWEEP of current tree (a2c27be): generated=135 killed=102 survived=33
log untouched by this sweep: True      <-- (mtime, size) of mutation_survivors.jsonl
                                           captured before and after, compared, identical
```

Mutation is in-memory by construction (module docstring: `inspect.getsource` → mutated AST →
new function object → monkeypatched → restored in `finally`). No graph, no model, no disk write.

### 1b. SURVIVOR COORDINATES — exact set equality, on BOTH lists

Every persisted record was compared against the live sweep on the full `(module, func, operator,
lineno)` tuple set — survivors **and** `killed_mutants`, not counts.

| result | value |
|---|---|
| records matching the current tree EXACTLY | **29** |
| index range | **113 … 141**, contiguous (verified: no gaps) |
| first match | `2026-08-07T20:37:10.551969+00:00` |
| **last match** | **`2026-08-10T22:50:28.012131+00:00`  ← record 141** |
| records after the last match | **142** (`2026-08-11T00:50:11`), **143** (`2026-08-11T01:06:48`) — the only two |

Counts alone would not have distinguished these: **142 and 143 report the identical
`135/102/33`.** Only the coordinates separate them, which is the whole reason this check
compares identities rather than totals.

### 1c. THE 142/143 DELTA IS THE PATCH, AND NOTHING ELSE

The difference between record 143 and the live sweep is **exactly five entries, all
`harness.write_rule.classify`, all shifted +10 lines. Every other one of the 33 survivors and
all 102 killed mutants are identical.**

| in 143 only | in live sweep only |
|---|---|
| `:367 delete_last_operand(Or)` | `:357 delete_last_operand(Or)` |
| `:367 delete_last_operand(And)` | `:357 delete_last_operand(And)` |
| `:368 delete_last_operand(Or)` | `:358 delete_last_operand(Or)` |
| `:368 swap_compare Eq->NotEq` | `:358 swap_compare Eq->NotEq` |
| `:368 swap_compare Is->IsNot` | `:358 swap_compare Is->IsNot` |

The preserved patch's only `write_rule.py` hunk is `@@ -88,6 +88,16 @@` — **ten lines inserted
at line 88**, far above the mutated region, so everything below shifts by exactly ten.
357 + 10 = 367. 358 + 10 = 368. The observed delta and the patch arithmetic agree with no
residue. **Records 142 and 143 were produced by a tree carrying HA-33's patch.**

### 1d. REVISION — the shift came from an uncommitted working tree, so it cannot be a commit's doing

Local clock is **MDT (UTC−6)**; the log stamps UTC.

| record / commit | UTC | local | what was in the tree |
|---|---|---|---|
| **record 141** | `2026-08-10T22:50:28` | 16:50:28 | last unpatched run |
| commit `a7807d8` (HA-32) | — | 16:52:18 | 2 min after record 141 |
| **record 142** | `2026-08-11T00:50:11` | 18:50:11 | patched |
| **record 143** | `2026-08-11T01:06:48` | 19:06:48 | patched |
| commit `a2c27be` (HA-33) | — | 19:08:54 | 2 min after record 143 |

**No commit in that window touched any module under mutation.** Verified per commit — `5fa9d9c`,
`a7807d8` and `a2c27be` each checked against all four target modules plus the killer set
(`write_rule.py`, `injection_contract.py`, `g0_invariant.py`, `record_invariants.py`,
`mutation_targets.py`): **none touched.** `a2c27be` is docs-only (3 files: its own dispatch doc,
the patch, one HA-15 doc). So the committed source under mutation is byte-identical across the
entire window, and the +10 shift in 142/143 can only have come from an **uncommitted working-tree
change** — HA-33's patch, applied, swept, then reverted before `a2c27be` was committed. That
sequence is exactly what the HA-33 report describes.

---

## ITEM 2 — RECORD 141 **IS** THE CORRECT CONTROLLED PRE-HA-33 BASELINE

Established, on the evidence above:

- It **reproduces the current `a2c27be` tree exactly** — 33 survivors and 102 killed mutants,
  coordinate for coordinate (item 1b).
- It is the **last** record that does so; only 142 and 143 follow it, and both are patched-tree
  runs (item 1c).
- It was produced against a tree whose mutated source is byte-identical to today's (item 1d).
- The preserved patch still **applies cleanly** to `a2c27be` (`git apply --check`, nothing
  written), confirming the tree is in the exact pre-patch state record 141 was taken from.

Records 113–140 are equally valid as *content* — all 29 are identical — but 141 is the correct
one to restore, because it is the last, and restoring anything earlier would silently discard
the fact that 114 through 141 happened.

---

## ITEM 3 — **STOP. THE TOOLING CANNOT SELECT OR RESTORE A BASELINE. IT HAS NO SUCH MECHANISM.**

This is the finding, and per the dispatch it is where work halts.

### The complete API surface, `eval/harnesslib/mutation_score.py`

| function | signature | what it can do |
|---|---|---|
| `read_last_survivor_run` | `(path=SURVIVOR_TREND_LOG)` | reads every line, returns **the last non-blank one**. Nothing else. |
| `write_survivor_trend` | `(scores, *, timestamp, path=SURVIVOR_TREND_LOG)` | serialises a **live `scores` dict** and appends it. |

- **No selector of any kind.** Not by index, not by timestamp, not by revision, not by "the last
  run that passed". The only parameter either function takes is `path`.
- **Even `path` is unreachable.** `layer7_crypto_v2.py:1615` calls `read_last_survivor_run()`
  with **no arguments**, so the default is the only value it can ever have. `SURVIVOR_TREND_LOG`
  is a module constant derived from `__file__` — no environment variable, no override.
- **A stored record cannot be re-emitted.** `write_survivor_trend` builds its record from a live
  sweep result. There is no API that takes an existing record and re-affirms it, so the baseline
  cannot be restored without re-running the sweep — which is the one route the dispatch forbids.
- **No CLI flag.** `eval/harness.py` has `--update-baseline`, but it routes to
  `reporter.apply_baseline` (`eval/harness.py:725`) — the **RATCHET's** baseline, an unrelated
  mechanism that never touches `logs/mutation_survivors.jsonl`. No script in `scripts/` addresses
  survivors either.

### Every available route, and why each is closed

| route | verdict |
|---|---|
| delete records 142/143 | **forbidden by this dispatch** — and it would be editing history |
| run the gate once to teach it a new baseline | **forbidden by this dispatch** — and see below: it does not even work |
| hand-append a JSON line copying record 141 | **manufacturing a baseline by editing history** — forbidden; it would also be a forged record of a run that never happened |
| use a tooling mechanism | **no such mechanism exists** |

### THE ROOT DEFECT — a FAILING run persists its own survivor list as the next run's baseline

`layer7_crypto_v2.py:1634` calls `write_survivor_trend` **unconditionally**, at the same
indentation as the check above it, outside any pass/fail branch:

```python
s_no_silent_disappearance.check(_disappearance["pass"], ...)
reporter.add(s_no_silent_disappearance)
# Persist THIS run's survivors only after the comparison above has run ...
write_survivor_trend(_mut_scores, timestamp=...)
```

The ordering comment is correct as far as it goes — the comparison does run first, so a run never
compares against itself. **But nothing conditions the write on the comparison's verdict.** The run
that FAILED with five unaccounted disappearances then wrote its own survivor list as the record
the next run would be measured against. That is how 142 and 143 came to exist, and it is a defect
independent of the line-shift one HA-33 hit. **Filed as TD-R-181.**

Its consequence is live right now: with the tree reverted, the persisted baseline is pinned to
line numbers that no longer exist in the source. **The next clean, unpatched run will itself fail**
with five unaccounted disappearances at `:367/:368` — the same failure, direction inverted. The
failed run rewrote the reference point it was being measured against.

### A SECOND FINDING THAT CLOSES OPTION (b) OF HA-33's OPEN RULING

HA-33 left Bill two options: re-record the baseline, **or carry the five under a debt ID**.
**The second option cannot be exercised with a new roadmap-lane ID.**

`find_debt_carry` matches debt rows with `_TD_ROW_RE = ^\|\s*(TD-\d+)\s*\|` — `TD-` followed
immediately by **digits**. Every new roadmap debt ID carries the `TD-R-` prefix that STANDARD
PREAMBLE item 10 mandates. Tested, not inferred, on two otherwise byte-identical rows:

```
legacy 'TD-134'              row matches _TD_ROW_RE: True    find_debt_carry -> TD-134
lane-prefixed 'TD-R-181'     row matches _TD_ROW_RE: False   find_debt_carry -> None
```

Also verified against the live register: none of the five survivors is carried today
(all five → `None`). **Filed as TD-R-182.**

---

## GRAPH CENSUS — **NO HA-33 POLLUTION IS PRESENT. NO CLEANUP PERFORMED.**

Per the dispatch, cleanup only on proof that pollution is still there. It is not.

HA-33 reported four fixture facts written for `maya`/`medication` with write states
`augment`/`supersede`/`correct`/`unresolved`. Read-only census of the 7688 graph:

- **12 Fact nodes total; every one carries `origin: 'fixture'`.**
- **2** are `maya`/`medication`, timestamped **`2026-01-10`** and **`2026-03-03`** — both seeded
  fixtures long predating HA-33.
- **Zero** facts carry HA-33's signature (`owner=maya`, `attribute=medication`,
  `write_state ∈ {augment, correct, unresolved}`).
- The newest node is a seed fixture written `2026-08-11T01:06:23Z` — 25 seconds before record
  143's run — i.e. **the graph was reset and reseeded during HA-33's session**, which is what
  removed the four facts.

HA-33's OPEN item "four fixture facts on `maya`/`medication` in the 7688 graph" is therefore
**stale and should be closed**. Nothing was deleted by this dispatch.

---

## PREFLIGHT (run before any of the above)

Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `[REDACTED-USER-PATH]/hip-roadmap`, branch
`roadmap` — matches target. Locks `repo` and `graph:7688` both **free** at start.

| resource | state |
|---|---|
| Neo4j `bolt://localhost:7688` (repo `.env.dev`) | **GRAPH USABLE** — authenticated driver connection, trivial read returned 12 nodes |
| `HIP_REGISTRY_DB` = `~/hip-roadmap/data/registry.db` | **USABLE** — exists, opens read-only, 15 tables, roadmap-local (not `hip-harness/`, not `hip-dev/`) |

`NEO4J_PASSWORD` present in the operator's shell. Repo `.env.dev` sourced, never `~/.env.dev`.

---

## FINDINGS FILED

| id | what |
|---|---|
| **TD-R-181** | `write_survivor_trend` is called unconditionally by Layer 7, so a **failing** run persists its own survivor list as the next run's baseline. Root cause of records 142/143. |
| **TD-R-182** | `find_debt_carry`'s row regex cannot match lane-prefixed `TD-R-nnn` IDs, so "carried under a debt ID" is unreachable for any new roadmap-lane debt. Closes option (b) of HA-33's ruling. |

**Noted, not filed as debt:** the `docs/INDEX.md` dispatch ledger has **no row for HA-32 or
HA-33** — both landed without one, against the ledger rule that every new dispatch gets a row.
Not backfilled here: writing another dispatch's summary line is that dispatch's call, not this
one's. HA-34's own row is added.

---

## WHAT BILL MUST DECIDE

The baseline is identified and proven (record 141). Restoring it requires a mechanism that does
not exist, so building that mechanism is a ruling, not a session's call. Three shapes, stated
without preference between the first two:

1. **Add explicit baseline selection to the tooling** — e.g. `read_last_survivor_run` gains the
   ability to select the last record matching a given source state, or the last record from a
   run that PASSED. This is the general fix and it subsumes the specific one.
2. **Make the persist conditional (TD-R-181)** — Layer 7 writes the trend record only when the
   disappearance check passed. This prevents recurrence but does **not** repair the state already
   on disk; something still has to select record 141 once.
3. **Rule that an explicit, provenance-carrying restoration record may be appended** — a new line
   that re-affirms record 141's contents, marked as a restoration and citing this dispatch, with
   142/143 left in place as history. This is the only route that repairs the state without new
   code, and **it needs Bill's ruling precisely because it writes a record no sweep produced.**

Whichever is chosen, the fingerprint work HA-33 needs sits **behind** it: a fingerprint schema
changes what future records contain, and cannot repair the two records already written against
the old shape.

---

## CLAIM IMPACT

**none.** No product change landed, no gate was run, no requirement gained or lost evidence.
Nothing is ruled MET.

---

## OPEN

- **The restoration ruling above** — blocks the HA-33 build entirely.
- **TD-R-181** — the unconditional persist, unfixed.
- **TD-R-182** — `TD-R-` IDs invisible to `find_debt_carry`, unfixed.
- **Carried from HA-33, still open:** the seven absence proofs are executed but not standing
  tests; the fingerprint/RELOCATED design is authorized but unbuilt.
- **Closed by this dispatch:** HA-33's "four fixture facts in the 7688 graph" — census proves
  the graph clean.

---

**HA-34: STOPPED AT ITEM 3 — NEEDS BILL.** The pre-HA-33 baseline is **record 141**
(`2026-08-10T22:50:28Z`), proven four ways: a live in-memory sweep of `a2c27be` reproduces it
exactly on all 33 survivors and 102 killed mutants; it is the last record that does; records 142
and 143 differ from it **only** by the five `write_rule.classify` entries shifted +10 lines,
matching the preserved patch's `@@ -88,6 +88,16 @@` arithmetic exactly; and no commit in that
window touched any module under mutation, so the shift came from an uncommitted patched tree.
**Restoring it is impossible with the tooling as it stands — `read_last_survivor_run` takes the
last line and nothing else, `write_survivor_trend` can only serialise a live sweep, Layer 7 calls
both with no arguments, and no CLI flag or env var reaches either.** Root cause filed as
**TD-R-181**: the trend record is written unconditionally, so HA-33's FAILING run persisted its
own survivors as the next run's baseline. **TD-R-182** filed: `find_debt_carry` cannot match
`TD-R-` IDs, which closes option (b) of HA-33's open ruling. Graph census shows **no HA-33
pollution** — no cleanup performed. Nothing built, no product or mutation-tool code touched, no
log line added or removed. **CLAIM IMPACT: none.**
