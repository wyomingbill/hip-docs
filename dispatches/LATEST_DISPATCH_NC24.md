# DISPATCH_NC24 — F5/F3 repair, one decision point for both modalities: F5 BUILT AND GREEN; F3-interim NOT BUILT because NC 22 landed it first
Status: **BUILT — F5 landed `422d330` on `nc-b0`; F3-interim not built, by measurement (§3)**
Reconciled-Against: `0c7b6ee` (`~/hip-nc2` @ `nc-b0`, NC 22's Conversation Episode) → `422d330` (this dispatch). Roadmap `57e7e2b` → `f0b3583`.
Dispatch: NC 24
Date: 2026-08-15 06:47 → 07:20 (Mountain)
REQ: **`REQ_VOICE_INTO_KERNEL` Amendment 2**, filed at `f0b3583` **before the first code edit**.
Method: read-only measurement first, then build. All twins EXECUTE the consumer path; the one
structural assertion says so in its own name.

---

## 0. THE EXCEPTION LINE

```
NC 24 — F5/F3 repair: one decision point for both modalities
STOPPED AT SEGMENT 2 — NEEDS BILL
```

**Segment 1 (F5) is BUILT, GREEN and PUSHED.** Segment 2 (F3-interim) did not run, and the
reason is not difficulty: **NC 22 landed the thing F3-interim was dispatched to build, at the
exact line it targeted, while this dispatch was reading.** Cancelling it is Bill's ruling, so
the honest form is the second one.

---

## 1. THE GATE, AND THE THIRTEEN MINUTES

**MACHINE GATE — PASSED.** `bill-ai` / `[REDACTED-MACHINE-NAME]` / `~/hip-nc2` / `nc-b0` /
HEAD `04a63f8`, matching the dispatch's stated target.

**PREFLIGHT — BOTH READINGS, because they disagreed and the disagreement is a finding.**

| time | result |
|---|---|
| 06:41 | **REFUSED, exit 7** — "this lane is MID-RUN — 2 work process(es)" |
| 06:44 | **OK** — `hip-nc2 @ nc-b0 writes bolt://localhost:7693` |

The processes at 06:41 were `pytest eval/test_nc22_episode_substrate.py` (pid 43064) running
inside `~/hip-nc2` from another session's shell. **NC 22 was mid-flight in the same worktree**,
with five modified files, two untracked ones, an open board row, and a hand-written
`.hip-scope` naming every file both NC 24 repairs must edit. This dispatch therefore stopped on
its own handoff clause — *"if it is mid-flight, coordinate via the board and queue behind it"* —
claimed NC 24 **docs-only** at `57e7e2b`, and did not touch the seam.

**At 06:53, thirteen minutes in, NC 22 LANDED `0c7b6ee` and the tree went clean.** The clause's
other branch — *"if NC 22 has landed when you start, build on its substrate instead and say
so"* — then applied, so the claim was amended in place at `edb2cc5` (**the docs-only scope was
kept, not patched away**, because it is the record of why the dispatch stopped), code scope was
taken on `harness/kernel.py` plus a new twin file, and the build proceeded. Scope was checked
against NC 25's claim first: **disjoint by construction**, and stated on the board so NC 25 can
rely on it.

---

## 2. WHAT NC 21 MEASURED, RE-MEASURED AT HEAD BEFORE ANY EDIT

| NC 21's finding | at `04a63f8` | at `0c7b6ee` (post-NC 22) |
|---|---|---|
| `governed_decision` has ONE production call site | `server/voice_orch.py:1637` — confirmed | `:1659`, **still exactly one** (NC 22's inserts moved it 22 lines) |
| The R4 window is inert | `kernel.py:293` `getattr(req, "conversation_window", None)`, no field, no caller | **SUPPLIED** — see §3 |

---

## 3. F3-INTERIM WAS NOT BUILT, AND THE REASON IS MEASURED, NOT ARGUED

**NC 22's landed code supplies B1's window at the exact line F3-interim targeted**
(`harness/kernel.py:365-366`):

```python
_window = (episode.conversation_window() if episode is not None
           else getattr(req, "conversation_window", None))
```

Three further facts, each read from the landed source:

- **The window F3-interim was told to plumb is RETIRED.** `server/voice_orch.py:519`,
  `_trim_context`: *"**RETIRED ON THE LIVE PATH BY NC 22 — no caller remains** … Calling it
  again would reinstate a second lifetime over one conversation."* F3-interim's brief —
  *"callers supply the live window (the existing session store, existing 8-turn trim)"* — is an
  instruction to re-plumb the function NC 22 unplugged.
- **The mechanism would contradict the landed rule.** `harness/turn_request.py` gained
  `episode: Any | None = None` with *"Normally left None by callers: `kernel.governed_decision`
  resolves the episode from `session_id`."* F3-interim would add a **caller-supplied** window to
  the same dataclass whose new field is **kernel-resolved** — two owners for one need.
- **B1's own scope note already records the handoff as done.**
  `harness/unresolved_reference.py`: *"**R4's SUPERSESSION HAS NOW HAPPENED (NC 22,
  2026-08-15)**."* The clause NC 24 was told to reference —
  `REQ_UNRESOLVED_REFERENCE_DETECTOR` §R4, *"The Episode capability supersedes this clause when
  it lands"* — has fired.

**It is not merely superseded in principle: the outcome is delivered and now PROVEN on the
typed path** by twin E6 (§5), which is the release direction R4 states and NC 21 could reach
only by calling `detect()` directly.

**RECOMMENDATION, Bill's ruling to make:** **CANCEL F3-interim.** What remains after NC 22 is a
different and much smaller question — *should any caller ever supply `conversation_window` on a
turn with no episode?* — and it is not what NC 24 was dispatched to build.

---

## 4. WHAT F5 BUILT — `422d330`

`kernel.governed_turn` is the typed funnel (`text_turn` → `text_reply` → both
`/api/text-query` routes, Tier L, the eval harnesses). It now calls the **same** decision point
the spoken path crosses, as its first action. Per Amendment 2:

- **A2.1 — one call site per modality, and no route file edited.** One call in the funnel is
  one call per typed turn.
- **A2.2 — same order, and the order IS the repair.** Spoken runs episode → B1 → store-down;
  running the decision point first reproduces it exactly.
- **A2.3 — no copy.** The store-down gate that used to live in `governed_turn` is **removed**,
  not reordered. It was the copy that decided first, which is how the divergence arose.
- **A2.4 — `governed_decision` accepts `store_probe`** and passes it to `store_reachable`.
  Additive, defaulted, **the spoken call site is untouched**. Without this, A2.3 would have
  traded a duplicated gate for an untestable one.
- **A2.5 — `TurnResult` carries `episode_id` and `notice`** on *every* exit of the funnel
  (refusal, claim mismatch, disclosure, error, answered). NC 22's Q4 rule is *"Callers must
  deliver this whether the turn proceeds or not"*, and after A2.1 this function is a caller.

**`governed_decision`'s docstring has always said *"The live Pipecat path calls THIS, and so
does the typed path."* Until this commit that was the only false sentence in the file.**

---

## 5. THE TWINS — 14 NEW, ALL GREEN, ALL ON THE CONSUMER PATH

`eval/test_nc24_one_decision_point.py`. **None of them calls `governed_decision` directly** —
that is NC 21's finding applied: NC 20's twins passed while the production seam was inert
because they handed the detector a window no real caller supplied.

| twin | what it proves | result |
|---|---|---|
| **E1** | Bill's equivalence twin: same dependency phrasing through `text_turn` and `voice_turn` → same class, **byte-identical** reply | PASS |
| **E1b** | anti-vacuity: they did not converge by both being wrong (class is not STORE_DOWN) | PASS |
| **E2** | a typed turn reaches the decision point **exactly once**, counted at the function | PASS |
| **E2b** | the spoken path still has **exactly one** production call site (structural, and says so) | PASS |
| **E2c** | the kernel grew **no second** `governed_decision` call — a call, not a copy | PASS |
| **E3** | precondition: the phrasing IS household-dependent (else E3 proves nothing) | PASS |
| **E3** | store down + dependency phrasing → `REFUSED_UNRESOLVED_REFERENCE`, **not** `REFUSED_STORE_DOWN` — the measured F5 symptom, repaired | PASS |
| **E4** | household-dependent NON-dependency turn still refuses `STORE_DOWN` — no refusal became softer | PASS |
| **E4b** | the `store_probe` seam still decides at the one decision point | PASS |
| **E5** | no answering model call on the typed dependency refusal, observed at the counter | PASS |
| **E6** | with a live Episode carrying the prior turn, the typed path **proceeds** — the window reaches typed | PASS |
| **E6b** | anti-vacuity: the same turn without the episode still refuses | PASS |
| **E7** | the expiry `notice` crosses the typed boundary **on the refusal path** | PASS |
| **E7b** | no notice when nothing expired | PASS |

**Cross-modality equivalence result, stated as the dispatch asked:** the same dependency
phrasing spoken and typed now lands in **`REFUSED_UNRESOLVED_REFERENCE` on both**, with the
reply **byte-identical** to `CLARIFICATION` on both, and `modality` still differing as a field.
Before this commit the same pair returned two different classes and two different replies.

**Neighbour suites, run whole:** NC 20's B1 twins, NC 22's episode substrate, the kernel
governed-turn suite, NC 15's medical split, NC 13, NC 11, A1 governed voice, B0 ground
hardening — **214 passed, 0 failed.**

---

## 6. SUITE DELTA — MEASURED TWICE, AND THE SECOND TIME IS THE ONE THAT COUNTS

**Service state: no Neo4j on 7693 (this lane stands none up, `.hip-graph`), store-down
throughout, both halves.**

**First comparison, in the shared `~/hip-nc2`:**

| | passed | failed | skipped | errors |
|---|---|---|---|---|
| baseline `0c7b6ee` | 629 | 20 | 39 | 21 |
| after | **643** | 20 | 39 | 21 |

`+14` passed is exactly the 14 new twins; failure **set** identical (41 items both sides,
`diff` empty).

**THAT COMPARISON IS NOT LIKE-FOR-LIKE, AND THIS DISPATCH SAYS SO RATHER THAN BANKING IT.**
NC 25 began editing `harness/unresolved_reference.py` (07:09:19) and `harness/medical_intent.py`
(07:14:02) in the same worktree — the first landed **before** the after-run started, the second
**during** it. The after-run therefore executed NC 25's in-flight B1 policy edits as well as
NC 24's change. Identical sets are reassuring; they are not a clean measurement of one lane.

**Second comparison, ISOLATED — a detached worktree at `0c7b6ee` that no other lane touches,
with NC 24's two files as the ONLY delta:**

| | passed | failed | skipped | errors |
|---|---|---|---|---|
| isolated baseline (`0c7b6ee`, NC 24's change ABSENT) | 629 | 20 | 39 | 21 |
| isolated after (`0c7b6ee` + NC 24's two files, nothing else) | **643** | 20 | 39 | 21 |

```
baseline set: 41   after set: 41
diff → empty.  IDENTICAL — zero new failures by set comparison.
```

**`+14` passed, and 14 is exactly the number of twins this dispatch added.** Failure set and
error set byte-identical, 41 items each side. The worktree was created and removed under the
repo lock and is gone (`git worktree list` back to seven).

---

## 7. WHAT COULD NOT BE RE-RUN, STATED PLAINLY

**NC 21's probe set is NOT re-runnable and was not re-run.** Its own dispatch doc records
*"Probes live in the session scratchpad"* — they were never committed, and that session's
scratchpad is gone. The acceptance line asked for them; this is the honest answer, not an
omission. **NC 20's 26 twins WERE re-run** (§5, green), and NC 24's own 14 twins cover the two
findings NC 21's probes measured on this seam.

---

## 8. RESIDUALS AND FILINGS — NAMED, NOT SILENTLY LEFT

1. **`server/voice_https_orch.py:469` is a SECOND spoken entry that bypasses the kernel funnel
   entirely** — it calls `voice_orch.process_governed_turn` directly, crossing neither
   `governed_turn`'s gates nor `governed_decision`. A2.1 does not reach it. Closing it edits a
   route file and cannot be executed in this lane (import fail-closed in the bare env, NC 21).
   **Filed, not fixed.**
2. **No typed route renders `notice`.** A2.5 carries it to the boundary; delivering it to a
   member on a typed surface is a user-visible route decision and is Bill's.
3. **B1 now decides before the claim-mismatch surfaces on the typed path** — because
   `ClaimMismatch` is raised inside the implementation, which the decision point precedes.
   **This is alignment, not novelty: the spoken path already had that order.** Measured
   consequence: a mismatched claim carrying a dependency phrasing is HELD (clarified) on that
   turn instead of refused-for-mismatch, and the mismatch surfaces on the next turn. **No answer
   is produced on either path**, and every claim-mismatch test in the suite still passes.
4. **TD-R-196 — `lane_preflight.py` returns OK on a seam that is fully HELD.** Its mid-run test
   is process-liveness only; it cannot see another lane's uncommitted work or its `.hip-scope`.
   Demonstrated twice in three minutes (§1). **Filed, not fixed** — the FINITENESS RULE keeps it
   filed rather than making it the next task.
5. **The number moved from 195 to 196 for this dispatch's own reason:** TD-R-195 was free when
   the register was read at 06:46 and taken by NC 22 (uncommitted) by 06:50.
6. **PASSENGER INCIDENT, reported because "who decided" is the test (D-158's rule).**
   **NC 22's commit `c034229` published this dispatch's TD-R-196 row.** The row was staged into
   this session's git index alone, but the WORKING file carried it, and NC 22's `git add` of the
   same shared register took it. Nothing was lost and the content is correct; the defect is that
   one lane published another lane's row and **neither lane chose that**. It is the D-158 shape,
   arriving through a mechanism the scoped-claim tooling does not cover: **`.hip-scope` makes
   FILE ownership disjoint, but two sessions sharing one worktree still share one index and one
   set of shared registers.**

---

## 9. NEEDS BILL

1. **Ruling: CANCEL F3-interim** (§3). Recommended, with the measurement behind it.
2. **Ruling: residual 1** — is `voice_https_orch:469` a follow-on dispatch, or does it stay
   filed? It is the last governance-bearing entry that crosses no kernel gate.
3. **Ruling: residual 2** — should a typed surface render the episode-expiry notice?
4. **Noted, no decision requested:** three dispatches (NC 22, NC 24, NC 25) worked in one
   worktree this hour. It worked — scopes stayed disjoint — but §6 and §8.6 are both direct
   costs of it.

---

## 10. CLAIM IMPACT

```
CLAIM IMPACT: none
```

No ledger claim's evidence is touched: this is an internal governance-path repair with no
deliverable-facing measurement.

---

## 11. VERIFIED

- Machine gate and both preflight readings read from the machine (§1).
- Every source citation read at the stated revision — `04a63f8` and `0c7b6ee` via `git show` /
  `git grep`, working-tree state via `git diff`.
- Twins executed, not asserted: 14/14 green, plus 214 green across the neighbour suites.
- The suite comparison was re-run in isolation once the first was found contaminated (§6),
  rather than reported with a caveat.
- Both commits contain exactly their own files, verified with `git show --stat`: `422d330` =
  `harness/kernel.py` + the new twin; roadmap commits = their own docs only.
- No verification step ran inside an `&&`/`||` chain whose exit status was read as a truth
  value (Requirements Discipline item 13).
