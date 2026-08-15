# DISPATCH_SENSITIVITY_NO_DEFAULT — kill the sensitivity defaults: refuse, don't stamp

Status: BUILT
Reconciled-Against: roadmap `a32ddaa` (pre-build HEAD after the mid-dispatch move; see §0).
**LANDED AT `90da7fb`** — backfilled by the immediately following commit, because a commit
cannot contain its own hash.

**D-R-196** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD (code)**
**REQ:** `docs/requirements/REQ_SENSITIVITY_NO_DEFAULT__missing-label-refused-at-every-boundary__v20260806_1351.md`
— written FIRST, before any code, per Requirements Discipline items 1 and 8.
**NOTHING RULED MET.** C1–C9 are reported below; the ruling is Bill's.

---

## 0. MACHINE GATE, AND THE TREE MOVING UNDER THE DISPATCH

`bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` / branch `roadmap`.
Graph `bolt://localhost:7688` from the REPO `.env.dev` (never `~/.env.dev`). All four Neo4j
instances were live.

**Two things the gate found, both reported rather than worked around:**

1. **`scripts/run_harness.sh` was dirty at the gate** — another lane's uncommitted TD-R-166
   work (the TD-129 memory-guard metric port). It was left exactly as found and never staged.
2. **HEAD MOVED MID-DISPATCH, from `e6dcac0` to `a32ddaa`.** D-D-161 landed on `roadmap`
   while this build was in progress: it committed that same `run_harness.sh` edit, filed
   TD-R-166/167/168, and repointed `LATEST_DEBT.md` to `DEBT_REGISTER__v20260806_1347.md`.
   Nothing it landed touches any of the seven sites. **Every run reported below was re-run
   on the merged state after the move** — the `--layer 7` figures come from a second,
   post-move execution, not from the pre-move one.

**A CORRECTION THIS DISPATCH MADE AGAINST ITSELF.** An early check reported all four Neo4j
ports CLOSED and nearly routed into "the harness cannot run." That check used `/dev/tcp`,
a **bash** feature; this shell is **zsh**, where it silently fails. All four ports were open
the whole time (`lsof` and a Python socket probe both confirm). Recorded because the failure
mode is the expensive one: a confident false negative that would have produced a STOP report
on an environment that was fine.

## 1. ALREADY-FIXED CHECK (the dispatch's first instruction)

`git log` on every cited file, run BEFORE any edit. **None of the seven had been fixed.**

| File | Most recent commit touching it | Fixed? |
|---|---|---|
| `memory_engine/store.py` | `ec6b2d3` D-158 (R4/R8 explicit-unknown marker) | no |
| `memory_engine/recall.py` | `9ebfa83` WIP e5 (recipient_ref threading) | no |
| `memory_engine/api.py` | `60f45f4` WIP f2 (widen candidate_facts) | no |
| `harness/extraction_queue.py` | `23b26d1` D-146 (lock enforcement / graph targeting) | no |
| `server/memory_dashboard.py` | `40ce5db` (original dashboard build) | no |
| `harness/sensitivity.py` | `b4ea004` D-93 (registry-version stamp) | n/a — already correct |

`harness/sensitivity.py` needed no fix and got none of that kind: **it has refused since
D-75.** `rank()`/`normalize()` raise `UnknownSensitivity` and a missing value normalizes to
something outside the order. **The seven sites are not a missing mechanism — they are seven
bypasses of a mechanism that already existed**, which is why the fix adds one helper and no
new vocabulary.

## 2. THE SEVEN SUBSTITUTION SITES

A substitution site = a place where a **missing** sensitivity **becomes a value**. An
explicit `sensitivity="medium"` at a call site is not one: the caller stated a label.

| # | Site | Was | Now | Boundary |
|---|---|---|---|---|
| 1 | `memory_engine/store.py:605` | `sensitivity: str = "medium"` | `sensitivity: str` (required) + `require()` as the first statement of the body | WRITE |
| 2 | `harness/extraction_queue.py:318` | `if not sens: sens = "medium"` | logs and `return None` — refuses the fact | WRITE |
| 3 | `memory_engine/recall.py:249` | `row["sensitivity"] or "medium"` | `require()`; row excluded + logged | READ |
| 4 | `memory_engine/api.py:241` | `row["sensitivity"] or "medium"` | `require()`; row excluded + logged | READ |
| 5 | `harness/extraction_queue.py:874` | `r["f.sensitivity"] or "medium"` | `require()`; row excluded + logged | READ |
| 6 | `harness/extraction_queue.py:954` | `r["sensitivity"] or "medium"` | `require()`; row excluded + logged | READ |
| 7 | `server/memory_dashboard.py:132` | `row.get("sensitivity") or "medium"` | `require()` raises; caller skips + logs | READ |

Sites 3 and 4 are `TD-D-148`'s two, quoted there verbatim and unchanged since it was filed.
Sites 1 and 2 are the two the dispatch named. **Sites 5, 6 and 7 are the three the two-site
filing never reached** — found by this dispatch's own survey, since no seven-site survey
document exists in either lane's records (see §8, finding 1).

**Test harnesses carrying the same default** (dispatch item 3): `eval/integration_harness.py`
`FixtureFact.sensitivity` and `eval/injection_harness.py` `make_fact(...)`. Both defaults
removed. `FixtureFact.sensitivity` also MOVED above the defaulted fields, because a dataclass
field without a default may not follow one that has it; all 7 call sites pass the first four
arguments positionally and `sensitivity` by keyword, so **no call site moved**.

## 3. ONE REFUSAL, ONE DEFINITION

`harness/sensitivity.py` gains `MissingSensitivity` (a **subclass** of `UnknownSensitivity`,
so every existing `except UnknownSensitivity` keeps working) and `require(value, *, where)`.
No fallback argument, no default parameter. `where` names the boundary and travels into the
message, so a refusal in a log says which of the seven refused.

Absent = `None`, `""`, whitespace, `"none"`, `"null"` (any case). Unrecognized-but-present
still raises the original `UnknownSensitivity`. **The two are distinguishable on purpose** —
"never labelled" and "labelled with something we do not know" are different upstream defects,
and the `or "medium"` idiom collapsed both into one silent outcome.

## 4. THE ONE INTERPRETIVE CALL, FLAGGED

The ruling settles the write path exactly. At a READ boundary there is no caller to hand an
error to, so "refused" was enacted as **the row does not enter the result set**, logged at
WARNING — not as a raise that takes the turn down.

**That split is this session's reading, not Bill's words**, and §2 of the REQ carries the
full argument, the cost, and the one-line-per-site change that would reverse it. Short form:
it is the house pattern already at all four sites (the adjacent decrypt failure does exactly
this), `TD-D-148` named the raise-on-a-live-read-path risk in advance as its reason for not
fixing them inline, and exclusion is strictly more restrictive than any stamp — a refused row
reaches no gate, no prompt, and no model. **Its cost is stated too:** a refused row is
invisible to the member as well as the model, with only a log line to say why.

## 5. BLAST RADIUS (dispatch item 6)

Surveyed by **AST, not grep** — `str.encode()` is textually identical to the write entry
point and grep cannot separate them.

- **60 `store.encode()` call sites. 41 already passed `sensitivity`. 19 did not.**
- **All 19 are in `eval/memory_harness.py`. No production caller relied on the default.**
- All 19 now state `sensitivity="medium"` — **the exact value the removed default supplied**,
  so the change is behaviour-preserving by construction and any movement in the memory-harness
  result would be attributable to the seven fixes, not to relabelled fixtures.
- Re-surveyed after the edit: **60 call sites, 60 pass a label, 0 omit.**

**FINDING, NOT ACTED ON:** 15 of those 19 fixtures are `medication` or `allergy` facts that a
real classifier would very likely rank `high`, not `medium`. Reclassifying them would change
what the harness measures and is a separate question — the same shape as Bill's own carve-out
for the eleven LOW defaults. Named here so the `medium` choice reads as a decision, not an
oversight.

## 6. FAULT TWIN + ANTI-VACUITY PER SITE (dispatch item 4)

`eval/test_sensitivity_no_default.py` — **23 cases, 23 pass, 0 fail.** Every fault twin is
paired with an anti-vacuity case, because a battery that only proves refusal cannot
distinguish "refuses the unlabelled row" from "refuses everything."

**"Nothing persisted" is proven by a graph fact-count before and after each refused write —
not by the absence of an exception.**

| Case | Proves |
|---|---|
| S1a | `encode()` with the kwarg OMITTED → `TypeError`; facts 0 → 0 |
| S1b/S1c | `sensitivity=None` / `""` → `MissingSensitivity`; facts 0 → 0 |
| S1d | `sensitivity="bogus"` → `UnknownSensitivity`; facts 0 → 0 |
| S1-AV | the SAME call with `"low"` → writes exactly one fact, 0 → 1 |
| S2a/S2b/S2c | `_coerce_fact` returns `None` for missing, empty, and unrecognized |
| S2-AV | `"low"` still produces a fact carrying `low` |
| S5 / S5-AV | `read_user_facts` **live**: unlabelled row absent, labelled row still returned in the same call |
| S3 / S3-AV | `recall_from_cold` **live**: exactly one refusal record for the unlabelled row, none for the labelled one |
| S4 / S4-AV | `candidate_facts` **live**: unlabelled row refused (record + absence), labelled row still in the candidate set |
| S6 / S6-AV | scored embedding retrieval **live**: same, both directions |
| S7 / S7-AV | `_annotate` raises on missing, returns the row when labelled |
| T1/T2 + AV | `FixtureFact` and `make_fact` require a label; both still build with one |

**Read sites 3–6 are exercised on GENUINE rows** — written through `encode()` so they carry
real ciphertext, real DEKs and real write-rule classification, then one row's `sensitivity`
NULLed by Cypher. Site 6's rows are given an embedding first, because the retrieval Cypher
filters on `f.embedding IS NOT NULL` and `encode()` writes `embedding=None`; the vector is
identical on both rows, so ranking cannot be what separates them.

**S3 IS ASSERTED ON THE REFUSAL RECORD, NOT ON EMPTINESS, AND HERE IS WHY.** A control run
was executed first: `recall_from_cold` returns **ZERO rows for a synthetic owner even when
nothing is NULLed and one fully-labelled cold fact exists**. The cause is downstream (the
injection contract does not admit a fixture owner holding no household key wraps) and predates
this change. So "0 returned" would be true with or without the refusal — **an emptiness
assertion there would have been vacuous**, which is the exact shape this battery exists to
avoid. The non-vacuous observable is that the boundary's own refusal fires for the unlabelled
row and does not fire for the labelled one, in the same call.

## 7. RUNS (dispatch item 8)

| Run | Result |
|---|---|
| Standing battery | **672 passed, 9 xfailed** — unchanged from D-R-194's baseline |
| `--layer 7` L7 | **27/27** (0 flaked, 0 skipped) |
| `--layer 7` L7V2 | **27/28** (0 flaked, 1 skipped — the opt-in live-output check) |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| Memory harness | **13/17** — failures exactly {MEM-115, MEM-116, MEM-117, MEM-118} |

**The memory-harness result is inside the pinned band and was PROVEN NEUTRAL, not assumed.**
The pin (D-109/D-110, in the register's Notes) is 13–15/17 with failures a strict subset of
those four; 16/17 is a STOP because MEM-115(b) and MEM-116 are structurally red. A **control
run on pristine code** — this dispatch's nine files stashed, everything else identical —
produced **13/17 with the same four failures**. Patched and pristine failure sets are
identical, so the change is provably neutral on this harness rather than merely "inside the
pin." (The stash was verified byte-identical on restore, 9/9 files.)

**`--full` was NOT run** and Requirements Discipline item 12 is therefore NOT satisfied. The
dispatch named three runs and `--full` was not among them; it is not claimed here.

## 8. C1 — THE GREP BAR, AND WHERE IT IS NOT CLEAN

The bar, from the pitch's own sentence: *a reviewer with grep finds no site where a missing
sensitivity becomes a value.* Run with comment lines stripped by `tokenize` — a plain regex
also matches the annotations this build added quoting the removed idiom, which is the trap
`eval/test_sensitivity_registry.py`'s own docstring warns about.

**15 code-line matches remain. ZERO of them are among the seven.** Full attribution:

| Count | Where | Disposition |
|---|---|---|
| **11** | `server/voice_orch.py` — `sensitivity=d.get("sensitivity_tag") or "low"` | **These ARE Bill's eleven.** The count is exactly 11, which is what identifies them. Untouched per item 7. |
| 1 | `harness/control_flow.py:166` — `prev_sensitivity or "low"` | Turn-level prior-turn tag, same family as the eleven, NOT a fact label. Untouched; named for the same separate ruling. |
| 1 | `harness/extraction_queue.py:293` | Matches the pattern but now **flows into the refusal branch** — no longer a substitution. |
| 1 | `harness/zep_store.py:280` (+ `_DEFAULT_TAGS`, `:109-112`) | **A GENUINE EIGHTH SITE, NOT FIXED.** Different store (graphiti/Zep, reached from `server/voice_mem0.py` and `voice/`), outside the seven the dispatch scoped. |
| 1 | `scripts/routing_benchmark.py:301` | Benchmark script, not a boundary. |

**SO C1 IS MET FOR THE SEVEN AND NOT MET REPO-WIDE**, and the difference is `zep_store`. A
reviewer running this grep tomorrow will find it; saying "the grep is clean" would be false.

## 9. FINDINGS FOR BILL

1. **No seven-site survey document exists in either lane's records.** `TD-D-148` (on
   `demo-cutover-build`, still worded as of today's register) names **two** sites. The other
   five were found by this dispatch. The enumeration in §2 is therefore this dispatch's own,
   presented in the order the survey found them — the two the dispatch named, then TD-D-148's
   two, then the three neither had reached.
2. **A29 was ruled MET on 2026-08-01 while all seven were live.** Its acceptance text reads
   "local enums and defaults fail static/runtime tests." Seven defaults sat in the tree and no
   test failed. Recorded as a finding against the ACCEPTANCE CHECK, **not** as a re-ruling of
   A29 — re-tiering an acceptance row is not pre-authorized.
3. **`TD-D-148` was NOT edited from this lane** (dispatch item 9). It is a demo-branch ID in
   a demo-branch register; the STANDARD PREAMBLE's own lesson is that a lane does not write
   another lane's records, and the symmetric precedent is D-D-161 filing TD-R-166/167/168 for
   roadmap-branch debt rather than reaching the other way. **The roadmap-lane record is
   `TD-R-169`** (register `v20260806_1407`, LATEST repointed), which carries all seven sites,
   the cross-branch pointer, the eleven-LOW carve-out and the unfixed eighth site. Closing
   TD-D-148 is the demo lane's act — **and that is a decision, not an omission: say the word
   and it gets done from `~/hip-cutover-demo`.**
4. **The eighth site (`harness/zep_store.py`) is open.** Same defect class, different store.
5. **The read-boundary refusal shape** (§4) is the one place a reviewer could reasonably have
   expected the other answer.
6. **`sensitivity="medium"` on the 19 relabelled fixtures** preserves behaviour exactly, but
   15 of them are medication/allergy facts (§5).

## 10. WHAT WAS NOT DONE

- Nothing marked MET; no acceptance row re-tiered.
- The eleven LOW turn-level defaults: untouched, per item 7.
- `harness/zep_store.py`: not fixed, named.
- `--full`: not run; item 12 not satisfied and not claimed.
- The frozen demo (`~/hip-dev`, 7689): not touched. The battery hard-refuses 7687 and 7689.
- Another lane's four untracked demo-cutover dispatch docs in this tree: left exactly as found,
  never staged.
