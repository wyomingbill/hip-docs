# DISPATCH_ENVDEMO_AND_MEM118
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (Part 1: fix + fault twin. Part 2: trace + file, explicitly NOT fix, per
instruction)

**REQ:** `docs/requirements/REQ_LOCK_ENFORCEMENT__td148-enforce-lock-and-separate-graphs__v20260803_2047.md`,
requirement 2 (graph separation) — extends D-146's build to a hazard it named and correctly
did not fix. Part 2 (MEM-118) has no governing REQ; it is a trace-and-file dispatch per
Requirements Discipline item 10.

## THE ASK

Dispatch text, verbatim:

```
=== D-147 | ~/hip-roadmap, roadmap | .env.demo hazard, then MEM-118 ===
STANDARD PREAMBLE. Lane A — you own the graph and the harness.
LOCK FIRST, before any read of a governed file. Late-take has happened twice.

PART 1 — THE TRACKED CONFIG HAZARD

D-146 named it and correctly did not fix it: .env.demo is TRACKED, so every worktree
carries a copy that sources the frozen demo's env in demo mode. Your own first port
survey tripped on it. Bill authorises the fix now.

1. SURVEY read-only first: every consumer of .env.demo, what each expects, and what
   breaks if it stops being tracked. hip-vo reaches 7689 through it and has no own
   .env.dev — that lane must keep working. STOP AND REPORT if any consumer cannot be
   satisfied without a behaviour change.
2. THEN FIX, to the same standard as D-146's fail-closed targeting: a worktree that
   has not been deliberately pointed at a graph must FAIL, never inherit the demo's.
   Untracked-and-gitignored where D-146's .hip-graph precedent applies.
3. Fault twin and anti-vacuity per D-87. The twin must reproduce today's hazard —
   a worktree silently resolving to 7689 — against the pre-fix shape.

PART 2 — MEM-118

MEM-118 went newly red at D-145 against D-127. D-145 hypothesised D-140's classifier
was refusing harness writes and killed its own hypothesis by reading the failure text
(trust-level and delta-transition mismatches, not refusals). Cause unestablished.

4. Re-run the memory harness AFTER part 1 lands. If MEM-118 goes green, the config
   hazard was the cause and you say so with the evidence.
5. If it stays red: trace it. Report the failure mode, whether it is deterministic
   across runs, and whether it is environmental (the D-108 four-grounds test) or real.
   UNKNOWN is an acceptable answer with what would determine it named.
6. Do NOT smooth it, do not update the baseline, do not accept it as a known red.
   File a TD if it is real.

RUNS: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
Read the ABSOLUTE checks individually from the log.
Rule nothing MET. Commit with explicit pathspecs around the cutover lane's WIP,
verify post-commit. Report LONG to a dispatch doc.
```

## WHAT WAS DONE

1. Gate checked — matched. **Lock taken FIRST, before any file read**, per the dispatch's own
   emphasis: `scripts/hip_lock.py` (D-146's kernel-enforced mechanism, which supersedes the
   old `.hip-lock` marker for this purpose) was confirmed free via `who repo`, then acquired
   by launching `hip_lock.py with repo "D-147..." -- sleep 7200` as a background holder —
   a real `fcntl.flock` held for the dispatch's duration, not a step that could be reordered.
2. Read `docs/HIP_HANDOFF.md`, the D-146-build dispatch doc, and the D-146-B3 addendum in full
   BEFORE surveying — substantial work had landed between D-146 (my own survey) and this
   dispatch: `scripts/hip_lock.py` built, `harness/graph_target.py` built, five dormant
   worktrees retired on Bill's authorization. Confirmed via `git worktree list` (9 → 4) and
   `git log` before doing anything else, so this dispatch's own actions are grounded in the
   CURRENT state, not the D-146 survey's now-stale one.
3. Surveyed `.env.demo`'s consumers directly: confirmed it is TRACKED (`git ls-files`), found
   every script referencing it (`demo_player.py`, `run_demo_script.py`, `demo_preflight.sh`,
   `demo_run.sh`, `demo_reset.sh`) and read each one's own folder guard.
4. Fixed: `git rm --cached .env.demo` (untracks; the physical file is BYTE-IDENTICAL before and
   after, verified by MD5) plus a `.gitignore` entry matching `.hip-graph`'s precedent and
   wording style.
5. Wrote and ran 5 new tests in `eval/test_lock_and_graph_separation.py` (D-87 discipline: an
   EXECUTED fault twin against the real file still on disk, plus anti-vacuity) — found and
   fixed a self-introduced bug mid-edit (an orphaned assert line left outside any function),
   caught by running the file, not by re-reading it.
6. Ran `--layer 7` under the harness runner's own new lock-precondition (`[hip_lock] acquiring
   graph:7688` → `holding graph:7688`, automatic, unprompted) — clean, exit 0.
7. Ran the memory harness — MEM-118 still red. Investigated `_run_mem_118` directly and found,
   while tracing it, a SEPARATE, significant methodology defect in my OWN prior invocations
   this session (see WHAT WAS FOUND) — corrected it immediately (re-ran under the right
   interpreter) rather than reporting a confounded result.
8. Traced MEM-118's real failure mechanism to a specific, named log line and confirmed it
   deterministically across 3 consecutive runs under the correct interpreter.
9. Filed TD-158 with the full mechanism, explicitly NOT fixed, NOT smoothed, baseline NOT
   touched, per instruction.
10. Ran `--layer 7` once more (post all changes) and the memory harness once more as the
    final, official evidence set.
11. Staged by explicit pathspec, committed, pushed, verified post-commit, released the lock.

## WHAT WAS FOUND

### Part 1 survey — `.env.demo`'s consumers

`.env.demo` is TRACKED and byte-identical across every remaining worktree (confirmed via MD5:
hip-roadmap, hip-dev, hip-cutover-demo, hip-vo). Its own content unconditionally runs
`source ~/hip-dev/.env.dev` — sourcing ANY checkout's copy redirects to the frozen demo's
graph, regardless of which checkout hosts it.

**Consumers, each checked for its own folder guard:**
- `scripts/demo_run.sh` — hard-gated to `$HOME/hip-dev` only (`ABORT: wrong checkout` if not).
  Cannot be triggered from any other checkout; the tracked file's presence elsewhere is inert
  for this consumer.
- `scripts/demo_reset.sh`, `scripts/run_demo_script.py` — same shape, both hard-gated to
  `~/hip-dev` only.
- `scripts/demo_player.py` — **no folder guard**, only a usage comment
  (`source ~/hip-dev/.env.demo`). The only consumer with no structural protection, though its
  documented usage already names hip-dev explicitly rather than a relative path.
- `scripts/demo_preflight.sh` — **found gated to `$HOME/hip-roadmap`**, the OPPOSITE checkout
  from `demo_run.sh`/`demo_reset.sh`. Since `demo_run.sh` (hip-dev-gated) itself calls
  `demo_preflight.sh` via `$REPO_ROOT` (which resolves to hip-dev when `demo_run.sh` runs),
  this reads as a genuine, pre-existing guard mismatch — **flagged, not fixed, out of this
  dispatch's scope** (auditing every demo script's own folder-guard consistency is a different,
  larger task than `.env.demo`'s tracking status).

**No consumer requires `.env.demo` to be TRACKED specifically** — every one either has its own
folder guard unaffected by tracking status, or (`demo_player.py`) only documents an explicit
`~/hip-dev` path already. **hip-vo's requirement — "that lane must keep working" — is satisfied
by leaving hip-vo's own physical copy untouched**, which `git rm --cached` does by construction
(it removes an entry from the INDEX on the CURRENT branch only; it does not touch any other
worktree's working directory, and `.env.demo` is tracked independently per-branch in any case —
hip-vo is on `main`, a different branch this dispatch's scope does not reach). No STOP fired.

### Part 1 fix

`git rm --cached .env.demo` on the `roadmap` branch (verified: physical file MD5
`7e4c47cce20a59b7fe189b7c1f84d7ed` unchanged before/after); `.gitignore` gains an entry
matching `.hip-graph`'s own precedent and explaining why. **Scope, stated precisely: this
fixes the `roadmap` branch only.** `.env.demo` is tracked independently on `demo-presenter-
package` (hip-dev), `demo-cutover-build` (hip-cutover-demo), and `main` (hip-vo) — three
DIFFERENT branches with their own independent history, none of which "Lane A" has authority
to modify. **The same hazard likely exists on those branches too — named as OPEN, not
performed.**

### Part 2 — MEM-118, traced to a specific, confirmed mechanism

**Re-run after Part 1 (item 4): MEM-118 stayed red.** The config hazard was NOT the cause —
stated with the evidence, not assumed: `.env.demo` was already untracked+gitignored on this
branch when the memory harness ran, and MEM-118's failure persisted unchanged.

**A methodology defect found while tracing it, corrected before drawing conclusions.** Direct
reproduction of `_run_mem_118`'s live-query step under plain `python3` (the interpreter this
session had used for every `eval.memory_harness` invocation from D-130 through D-146) printed
`ModuleNotFoundError("No module named 'pipecat'")` to stderr, swallowed by
`scripts/text_demo.py::run_query`'s own exception handler — producing "no new record in
turns_demo.jsonl", a failure that reads as MEM-118 being red but is actually an artifact of
running under the wrong Python. `$HIP_DEV_PYTHON` (`~/hip-dev/.venv/bin/python`, what
`scripts/run_harness.sh` already uses correctly) has `pipecat` installed; plain `python3`
(`/opt/homebrew/bin/python3`, confirmed via `which`) does not. **Re-ran under the correct
interpreter for every remaining check in this dispatch.** This does not change any prior
dispatch's gating decision (the failing COUNT and SET were identical either way — 13/17,
{115,116,117,118}), but any citation of MEM-116/117/118's specific failure TEXT from
D-130–D-146 should be read as possibly interpreter-confounded; recorded in TD-158, not
silently absorbed.

**Under the correct interpreter, MEM-118's real, deterministic failure:**
`MEM-118: delta transition='unresolved'` — reproduced identically across 3 consecutive runs.

**Traced to a specific mechanism, not inferred:**
1. TD-151 (D-130, this session's own fix): `_restore_ray_medication_fixture()` reseeds the
   `(maya, ray, medication)` D9 fixture to **CORROBORATED** trust in MEM-116/117/118's own
   `finally` blocks — verified directly: `classify_trust_props()` on the live post-restore
   node returns `CORROBORATED`.
2. MEM-118's live-pipeline step (Groq `detect_and_apply` → `memory_engine/store.py::encode()`)
   attempts to supersede that head with a single conversational turn's write.
3. `encode()`'s own P8 cross-principal write-monotonicity override fires (subject `ray` ≠
   owner `maya`; incoming trust cannot reach CORROBORATED from one live utterance) and forces
   the write to UNRESOLVED, retaining the head — confirmed via the EXACT log line it produces,
   captured live: `server/voice_orch.py:2403` — `"[text-query] P8: cross-principal
   trust-regression write parked (parked=1) — replacing ack with pending-confirmation reply"`.

**This is REAL, not environmental — the D-108 four-grounds framing does not apply, because
the mechanism is fully explained and reproducible, not ambiguous.** Two independently-correct
pieces of code (TD-151's fixture-restore discipline, honest and deliberate; P8's
cross-principal trust-monotonicity gate, a real governance control) interact so that
MEM-116/117/118's own scripted scenario — a single live utterance superseding a fixture that
is DELIBERATELY kept at CORROBORATED trust — cannot pass as currently written. **This same
mechanism explains MEM-116's "original fact still open" (the supersede never applied) and
MEM-117's "trust level CORROBORATED, expected ASSERTED" (the query finds the still-active D9
head, not a new write) — one root cause for all three, not three separate defects.** MEM-115
is unrelated (a different key, already explained by TD-146).

**Filed as TD-158**, with the full mechanism, the methodology finding, and three named
candidate fix directions — **none built**, and the baseline is untouched, per explicit
instruction.

## VERIFIED

**Watched run:**
- `.env.demo`'s untrack: `git rm --cached` executed, `md5` compared before/after (identical),
  `git status`/`git check-ignore -q` both confirmed post-fix.
- 5 new tests in `eval/test_lock_and_graph_separation.py`: `14 passed` standalone
  (`PYTHONPATH=$(pwd) python3 -m pytest ... --import-mode=importlib`), including the fault
  twin executed against the REAL `.env.demo` file still on disk.
- `--layer 7`, twice (before and after the MEM-118 trace work): both exit 0, RATCHET PASS,
  standing batteries `404 passed, 8 xfailed`. Lock self-acquisition observed live both times:
  `[hip_lock] acquiring graph:7688` → `[hip_lock] holding graph:7688`.
- Memory harness, under the CORRECT interpreter, 3 consecutive runs: `13/17`, failing set
  exactly `{MEM-115, MEM-116, MEM-117, MEM-118}` every time; `MEM-118`'s failure text identical
  (`delta transition='unresolved'`) every time. `graph_subject_ids()` confirmed `ray`/`dad`
  both active after the final run (TD-151's fix still holding).
- The P8 mechanism: reproduced by calling `_run_mem_118` directly and capturing the live log
  line naming the exact gate that fired, not inferred from the failure message alone.
- `git status` before and after commit: confirmed `docs/INDEX.md` and the four untracked
  `DISPATCH_DEMO_CUTOVER_*.md` files untouched.

**Reasoned about:** that the SAME P8 mechanism explains MEM-116 and MEM-117 (not just
MEM-118) is inference from their failure text matching the mechanism's predicted shape,
cross-checked against direct knowledge of `_restore_ray_medication_fixture`'s own behavior
(this session's own D-130 code) — not independently reproduced turn-by-turn for those two
scenarios specifically, since the dispatch's own scope was MEM-118.

## HASH

Staged for commit: `.env.demo` (deletion, tracking only), `.gitignore`,
`eval/test_lock_and_graph_separation.py`, `docs/techdebt/DEBT_REGISTER__v20260804_0525.md`
(new), `docs/techdebt/LATEST_DEBT.md` (repointed), this dispatch doc. `docs/INDEX.md`
deliberately NOT touched (see OPEN).

## OPEN

- **`.env.demo`'s same hazard likely exists on three other branches** (`demo-presenter-
  package`/hip-dev, `demo-cutover-build`/hip-cutover-demo, `main`/hip-vo) — each tracks it
  independently and this dispatch's authority does not reach them. Named, not performed.
- **`demo_preflight.sh`'s folder guard names `~/hip-roadmap`, while the scripts that call it
  (`demo_run.sh`) are gated to `~/hip-dev`** — a real, pre-existing mismatch found while
  surveying, not audited or fixed (out of scope: this dispatch is about `.env.demo`'s tracking
  status, not demo-script guard consistency generally).
- **TD-158 is filed, not fixed.** Three candidate directions named (scope P8 to exclude
  fixture-seeded heads; lower the restore's trust tier; rewrite the three scenarios to expect
  UNRESOLVED). Bill's call which, if any.
- **This session's own interpreter methodology defect (system `python3` vs. `$HIP_DEV_PYTHON`)
  is corrected going forward in this dispatch but was not retroactively corrected in D-130
  through D-146's own dispatch docs** — their aggregate pass/fail claims are unaffected and
  need no correction; any future reader citing their specific MEM-116/117/118 failure TEXT
  should cross-check against this dispatch first.
- **D-147's own INDEX registration is not performed** — added to the same pending-residual
  pile as D-143/D-144 (flagged at D-146, still outstanding). Out of this dispatch's own scope;
  not silently dropped.
- **Nothing ruled**, per instruction.
