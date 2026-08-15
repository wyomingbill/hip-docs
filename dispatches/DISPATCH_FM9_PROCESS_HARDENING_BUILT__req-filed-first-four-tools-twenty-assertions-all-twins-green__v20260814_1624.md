# FM 9 — PROCESS HARDENING: FILE THE REQ, THEN BUILD THE FOUR TOOLS
Status: BUILT — **LANDED**
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap`. Claim `8779b68`, REQ `1c72117`,
tools `21e6bd7`, hook `f6b1e2f`.

REQ: **`docs/requirements/REQ_PROCESS_HARDENING_TOOLS__claim-lane-register-doc-lane-preflight-scrub__v20260814_1613.md`**
— filed at `1c72117`, Status PLAN, **before the first code edit**, per Bill's ruling 1.

---

## 0. THE EXCEPTION LINE

```
FM 9 — PROCESS HARDENING: FILE THE REQ, THEN BUILD THE FOUR TOOLS
COMPLETE WITH FINDINGS — 4 ITEMS FILED, NOTHING BLOCKING
```

**All four tools built. All four twins GREEN, both directions, 20 assertions.** One thing is
built, proven and **deliberately not switched on** — §5, and it is the "STOP before anything
destructive" the dispatch asked for.

---

## 1. RULING 1 — THE REQ WAS FILED FIRST, AND THE ORDER IS PROVABLE

> *"FILE THE REQ. No exception phrase. Hardening obeys the gate it strengthens. FM 6 §3 lifts
> in intact. File it BEFORE the first code edit, Status PLAN."*

`1c72117` (the REQ) precedes `21e6bd7` (the first line of tool code) in the commit graph, and
`git show --name-only 1c72117` contains no file under `scripts/`. **The ordering is a fact in
the graph, not a claim in a report.** FM 6 stopped at exactly this gate; this is the thing that
was missing.

---

## 2. THE FOUR TWINS — 20 ASSERTIONS, EACH PROVEN IN BOTH DIRECTIONS

**A gate never exercised in the red is not known to be a gate.** Run with
`python3 scripts/lane_tools_selftest.py`. Everything runs in throwaway directories, and
`HIP_LOCK_DIR` is redirected so the claim twin never contends for the real `repo` lock that
live lanes are holding.

### TWIN 1 — `claim_lane.py` · GREEN

| assertion | result |
|---|---|
| A1 two concurrent claims both land, neither swept | **PASS** — exits 0/0, both rows present |
| A1 the commit is board-only | **PASS** — `['docs/LANES.md']` |
| **A2 a passenger REFUSES the push** | **PASS** — exit **3**, names the passenger by hash |
| A2 the claim is kept locally and nothing is published | **PASS** — local row present, origin clean of both the row and the passenger |

**Ruling 2 is implemented as a refusal, not a report.** The tool commits the claim, then
compares `origin/<branch>..HEAD`; anything there that is not its own commit is somebody else's,
and it exits 3 without pushing. The claim is not lost — it is committed and waiting.

### TWIN 2 — `register_doc.py` · GREEN

| assertion | result |
|---|---|
| B1 the row lands as the first row under **its own** section | **PASS** |
| B1 the neighbouring `requirements/` table is untouched | **PASS** — the TD-R-164 failure mode, which put 54 dispatch rows in the wrong table |
| B2 a missing/renamed anchor aborts non-zero | **PASS** — exit 2, reason on stderr |
| B2 the file is **byte-identical** after the refusal | **PASS** — no partial write, no fallback |
| B2b a row with the wrong column count is refused | **PASS** — exit 2, file unchanged |

**One honest note: the first run of this twin went RED, and the tool was not the problem —
the twin's own line arithmetic was off by one.** Recorded rather than quietly corrected,
because a twin that is wrong in the green direction would have passed a broken tool just as
easily.

### TWIN 3 — `lane_preflight.py` · GREEN

| assertion | result |
|---|---|
| C1 a lane whose sources agree passes | **PASS** — exit 0, every source printed with the value it contributed |
| **C2 the `~/hip-nc` inherited-declaration shape is refused** | **PASS** — exit **5**, both disagreeing values named |
| **C2 declarations agree but `.env.dev` points elsewhere** | **PASS** — exit **5**. *This is the case nothing currently sees* |
| C2 an unprovisioned lane is refused (ruling 3) | **PASS** — exit **4** |
| C1 provision, then pass | **PASS** |
| C2 provisioning refuses to change an existing declaration | **PASS** |

### TWIN 4 — `scrub.py` · GREEN

| assertion | result |
|---|---|
| D1 planted addressing is scrubbed | **PASS** — zero residual |
| D1 verification is against the **written file** | **PASS** — 4 `[REDACTED-*]` tokens read back from disk |
| **D2 a self-quoting certification goes RED** | **PASS** — exit **7**. *This is exactly FM 5's first-pass failure, now a permanent test* |
| D3 the emitted pattern carries both scopes | **PASS** — 343 chars, docs vocabulary included |
| D3 docs-only vocabulary is never substituted in source | **PASS** — `NEO4J_PASSWORD = os.environ.get(...)` left intact |

---

## 3. RULING 3 — PROVISIONED FIRST, THEN ENFORCED

All five worktrees now pass preflight. **`~/hip-roadmap` was found to be half-provisioned** —
it carried `.hip-graph` and no `.hip-owns`, so it refused with exit 4 the moment the tool
existed. That was not in the dispatch's list of two bare lanes and is a real find; the
provisioner was changed to write **whichever declaration is missing** while still refusing to
*change* one that already says something else.

```
hip-dev            OK — demo-presenter-package  -> bolt://localhost:7689
hip-cutover-demo   OK — demo-cutover-build      -> bolt://localhost:7690
hip-roadmap        OK — roadmap                 -> bolt://localhost:7688
hip-vo             OK — main                    -> bolt://localhost:7691
hip-nc             OK — natural-conversation    -> bolt://localhost:7692
```

**`~/hip-dev` was touched, and only in the way the ruling authorises.** Two declaration files
were added. No code, no graph, no service, no commit in that tree. The declaration records in
its own text that this checkout is the frozen demo and the fallback, not a lane.

---

## 4. THE SCRUB UNIFICATION IS REAL, AND IT FAILS CLOSED

`scripts/scrub_patterns.py` is now the one table. **`scripts/push_docs.sh` no longer contains a
pattern** — it calls `scrub.py --emit-detect-pattern --scope docs` and **refuses to push if it
cannot get one**, because no scan must never mean "clean". Proven by replacing `scrub.py` with
a stub that exits 3: the push refused. The old inline pattern is preserved in the file's
comment, per *annotate, never silently patch*.

**Two design points that are not incidental:**

- **`scope` carries FM 5's caveat into the tool.** Entries are `all` (substitutable anywhere)
  or `docs` (detect-only, because `password|secret|api_key|token|NEO4J|bearer` fires on
  ordinary source by design). A shared table that ignored that would be unusable on source —
  the thing it is most needed for.
- **No PII is in the tracked table.** Writing a real household address into a version-controlled
  file would put it in git history permanently — the mistake the 2026-08-13 manifest made once.
  Personal patterns load at runtime from an untracked local file.

---

## 5. RULING 4 — BUILT AND PROVEN, DELIBERATELY NOT SWITCHED ON ⚠

> *"All four tools are repo-versioned centrally and enforced across every active worktree.
> Not per-worktree hooks."*

**`scripts/hooks/pre-commit` is written, committed and proven. `core.hooksPath` is still
UNSET, and that is this dispatch's STOP.**

**What was proven**, in a throwaway two-worktree repository mirroring the real topology:

| | result |
|---|---|
| `core.hooksPath` set in one worktree's config is visible from the other | **YES** — the config is shared |
| the second worktree has a hook of its own | **NO** — 0 files, which is the point |
| the shared hook FIRES from the second worktree and allows a clean commit | **GREEN** |
| the same shared hook REFUSES a policy violation from the second worktree | **RED, HEAD unmoved** |

**Why it is not switched on.** One command changes the commit behaviour of **all five
worktrees at once**, and **two lanes are in flight** (NC 5, VD-61). The dispatch says *"STOP
and report before anything destructive"*, and the REQ's own OPEN section warned that this
mechanism's blast radius is the thing the implementing dispatch must state and not widen
beyond what it can demonstrate. **I can demonstrate it in a throwaway repo. I cannot
demonstrate it against five live worktrees without doing it.**

**The dispatcher is built to make that flip as safe as it can be**: it chains to any
pre-existing per-worktree hook (additive, never subtractive), fails **CLOSED** on a policy
violation, and fails **OPEN with a warning** on an infrastructure problem — a control that can
brick five lanes' commits when a path moves is a worse failure than the one it prevents.

**The one line, when you want it:**

```
git -C ~/hip-roadmap config core.hooksPath [REDACTED-USER-PATH]/hip-roadmap/scripts/hooks
git -C ~/hip-roadmap config --unset core.hooksPath      # to undo
```

---

## 6. FILED, NOT BLOCKING (4)

**(FM9-1) The lane declarations are tracked on some branches and gitignored on others.**
`.hip-owns` and `.hip-graph` are **TRACKED** in `~/hip-vo` and `~/hip-nc`; in `~/hip-roadmap`
`.hip-graph` is **gitignored**. The same file is version-controlled evidence on one branch and
local scratch on another. `~/hip-roadmap/.hip-owns` was committed here; **the four files
written into `~/hip-dev` and `~/hip-cutover-demo` were left UNTRACKED and uncommitted** — those
are other lanes' branches, one of them frozen and one with VD-61 in flight, and committing to a
lane's branch mid-dispatch is the intrusion preamble item 2 exists to prevent. **Each lane
should commit its own two files.**

**(FM9-2) `claim_lane.py` is not yet the enforced path, only the available one.** Nothing stops
a session hand-editing `docs/LANES.md`, exactly as every dispatch today still does — including
this one, whose own board rows were written by hand before the tool existed. **The tool closes
the sweep; adoption closes the class**, and adoption is either a convention (which item 6 of the
preamble already shows decays) or the hook in §5.

**(FM9-4) DOGFOODING FOUND A BUG IN `claim_lane.py`, WHICH IS THE POINT OF DOGFOODING.** This
dispatch's own closing board row was written by `claim_lane.py` — the strongest proof available
that the tool works on the real board — and doing that surfaced two things a twin had not.
**First,** `--new ""` was rejected: the required-argument check tested falsiness, and an empty
replacement is a legitimate operation (deleting text from a cell). Fixed at `7832bc3`; all four
twins re-run green. **Second, and not fixed:** the tool replaces a **substring**, so anchoring on
the first sentence of a cell leaves the rest of that cell dangling — this row briefly read as
LANDED followed by its own stale in-flight brief. Nothing was lost, the table stayed valid, and
the residue was removed with the fixed tool. **The real answer is cell-level replace semantics
(`--set-cell N`), so a close cannot half-happen.** Named, not built — that is a REQ change, and
the finiteness rule applies.

**(FM9-3) The tools live on `roadmap` only.** `scripts/*.py` is on this branch; the other four
worktrees do not carry the files. §5's hook reaches them by absolute path, which works and is
also a coupling: if `~/hip-roadmap` moves, four lanes' hooks break — mitigated by the fail-open
branch, which downgrades that to a warning rather than a wedged repository.

---

## 7. WHAT THIS DISPATCH DID NOT DO

- **Touched no product runtime code.** `harness/`, `server/`, `truth_layer/`, `memory_engine/`
  are untouched. `scripts/` and lane declaration files only.
- **Ran no test suite, battery or gate**; wrote to no graph; started and stopped no service.
  VD-61 owns the heavy slot.
- **Did not enable `core.hooksPath`** — §5.
- **Did not commit to any branch other than `roadmap`.**
- **Did not migrate existing board or INDEX edits to the new tools retroactively.**

---

## 8. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Process tooling; no evidence bearing on a ledger claim was produced or moved.

---

## 9. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- **REQ `1c72117` precedes tool code `21e6bd7` in the graph**, and carries no `scripts/` file.
- Twins: `python3 scripts/lane_tools_selftest.py` → **ALL FOUR TWINS GREEN**, 20 assertions.
- All five worktrees pass `lane_preflight.py`.
- `git -C ~/hip-roadmap config --get core.hooksPath` → **unset**. Nothing was flipped.
- Every commit under `scripts/hip_lock.py with repo`, explicit pathspecs, no passengers carried.
