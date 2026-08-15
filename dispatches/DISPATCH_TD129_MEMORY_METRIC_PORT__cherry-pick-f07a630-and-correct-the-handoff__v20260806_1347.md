# DISPATCH_TD129_MEMORY_METRIC_PORT — port the corrected `--full` memory metric to roadmap
Status: BUILT
Reconciled-Against: 2026-08-06, roadmap @ e6dcac0 → **cd07519** (this dispatch's own commit)

**Dispatch:** D-D-161. **REQ: SKIPPED by Bill's explicit ruling** — the literal words
*"skip the REQ"* appear in the dispatch text, which is CLAUDE.md Requirements Discipline
item 8's only exception. The skip is logged as **TD-R-168** as that item requires.

**ID-LANE ANOMALY, flagged for Bill's ruling, not silently resolved:** this dispatch was
issued as **D-D-161** — a *demo-lane* number (STANDARD PREAMBLE item 10) — but every
change it makes lands on **`roadmap`**. The debt it files is therefore roadmap debt and is
numbered `TD-R-166/167/168` per item 10; the dispatch keeps the identifier Bill assigned.
A reader standing on `demo-cutover-build` who looks up "D-D-161" in that lane's records
will not find this work. Roadmap's own next free dispatch number was **D-R-196**. Renaming
was NOT done — the dispatch ID is Bill's to assign, and item 10 forbids renumbering
existing IDs.

---

## 1. WHAT WAS ASKED

1. File the two TDs from D-D-161's read-only findings (pre-authorized: tool-infrastructure debt).
2. Cherry-pick `f07a630` onto `~/hip-roadmap` **and** `~/hip-roadmap-d195`.
3. Verify by running the guard live on both trees; report what it reads vs `memory_pressure`.
4. Update `HIP_HANDOFF.md:302` in the same commit.
5. Do not unload the Ollama model — the demo lane may need it warm.

## 2. WHAT WAS DELIVERED — and the two things that could not be done as written

| # | Asked | Outcome |
|---|---|---|
| 1 | File two TDs | **DONE**, three filed: `TD-R-166`, `TD-R-167`, plus `TD-R-168` (the REQ skip, mandatory per item 8) |
| 2 | Cherry-pick onto **two** trees | **DONE on `~/hip-roadmap`. IMPOSSIBLE on `~/hip-roadmap-d195` — that tree no longer exists.** See §3 |
| 3 | Verify live on both trees | **DONE on the one tree that exists**, plus `~/hip-cutover-demo` as the reference implementation. See §5 |
| 4 | Update `HIP_HANDOFF.md:302` | **DONE — but the passage is no longer at line 302.** See §4 |
| 5 | Leave Ollama warm | **HONOURED.** Nothing unloaded; `qwen2.5:7b` still resident with its 24h keep-alive |

## 3. `~/hip-roadmap-d195` NO LONGER EXISTS — target 2 of 2 is gone

The STANDARD PREAMBLE's item-1 machine gate caught this before any write. The checkout was
present and readable **earlier in this same session** — D-D-161's read-only pass recorded it
at `d195/req-offer-mechanism @ e6dcac0` and read its broken guard directly. By the time the
build phase began, `git -C hip-roadmap-d195 status` returned
`fatal: cannot change to 'hip-roadmap-d195': No such file or directory`.

**Cause, established from the reflog and not guessed:**

```
e6dcac0 HEAD@{2026-08-06 13:23:02 -0600}: merge d195/req-offer-mechanism: Fast-forward
```

At 13:23 another lane fast-forward-merged `d195/req-offer-mechanism` into `roadmap` and
cleaned up after itself — worktree removed, branch deleted (`git branch --list "*d195*"`
is empty; `git worktree list` no longer shows it; no prunable records remain). Its work is
**already in `roadmap` at `e6dcac0`**, which is the commit this dispatch built on.

**This is not a blocked deliverable — it is a deliverable that ceased to exist, and the
outcome it was meant to produce was achieved anyway.** The concern behind item 2 was "two
checkouts are running the broken guard." That is now false by a different route: d195's
broken copy was deleted along with its checkout. **After this commit, zero checkouts on
this machine run the broken metric.**

Nothing was created to stand in for it. Re-creating the worktree or resurrecting the
deleted branch to satisfy the letter of the instruction would have invented a target Bill
did not ask for and reintroduced a checkout its own lane deliberately retired.

## 4. `HIP_HANDOFF.md:302` HAD MOVED — the line number was stale by ~20 minutes

The same 13:23 fast-forward merge that removed the d195 worktree also rewrote
`docs/HIP_HANDOFF.md`. The memory-guard passage that D-D-161's read-only pass found at
**line 302** now sits at **line 325**. Line 302 today holds unrelated text about
concurrent-lane risk and TD-148.

**Editing "line 302" literally would have corrupted an unrelated paragraph.** The passage
was located by content, not offset, and corrected there. Recorded because the general
lesson outlives this dispatch: **in a repo where four worktrees share one commit graph, a
line number in a dispatch is a snapshot, not an address.** A `grep` for the passage's text
cost nothing and was the difference between a correct edit and a silent corruption.

Two sites were corrected, not one:

- **The guard section** (was :302, now :325) — described the broken metric as correct,
  prescribed a remedy for it, and cited its own false refusals as evidence.
- **The standing-debt list** (was :391, now :416) — listed `TD-129 (memory guard)` under
  *"Standing debt that is scoped and deliberately unfixed,"* encoding the bug as a
  deliberate choice. That framing is the reason a two-line fix sat unported for ~6 days
  after the demo lane had already made it. Filed as **TD-R-167**.

**The three historical `--full REFUSED` entries (handoff lines 66, 95, 131) were left
exactly as written.** They are dispatch history. The pre-authorized correction class
requires annotating a correction, never silently rewriting the record — so the guard
section now flags them as probable measurement artifacts instead of editing the record of
what past sessions observed and believed.

## 5. VERIFICATION — the guard run live

The guard block was **extracted verbatim from each tree's real `scripts/run_harness.sh`
and executed with `want_full=1`**. The harness itself was NOT run: no graph connection, no
`.env.dev` load, no model calls — so preamble item 3's `~/.env.dev` hazard was never in
play and no baseline could be disturbed.

```
--- [REDACTED-USER-PATH]/hip-roadmap        guard block lines 91-119
    GUARD OUTPUT: (silent — guard passed, harness would proceed)
    VERDICT: ALLOW

--- [REDACTED-USER-PATH]/hip-cutover-demo   guard block lines 84-107   [reference impl, unchanged]
    GUARD OUTPUT: (silent — guard passed, harness would proceed)
    VERDICT: ALLOW

############ GROUND TRUTH, same instant ############
memory_pressure free pct : 73%
  -> guard reads          : 23.36 GB  (73% of 32 GB)
OLD broken formula        : 0.66 GB  (Pages free 43571 x 16384)
  -> old verdict          : REFUSE (false)
```

**The number the guard now reads: 23.36 GB. The number the old formula read at the same
instant: 0.66 GB.** The old guard would have refused this run outright. Combined with the
earlier D-D-161 measurement (0.67 GB vs 14.72 GB at 46%), the understatement has now been
observed at ~22x and ~35x on the same machine within one session.

**Fail-closed path, also exercised:** with `memory_pressure` stubbed to return nothing, the
guard emits
`refuse: could not read memory_pressure's free percentage -- refusing --full rather than guessing (TD-129/TD-R-166).`
and exits non-zero. It does not fall through to a permissive default.

**NOT exercised, and named as the residual (TD-R-168):** the genuine-low-memory refusal —
`memory_pressure` reporting under 2GB. Forcing that state would have required evicting the
Ollama models Bill explicitly instructed be left warm. The floor's arithmetic is unchanged
from the version already proven on `demo-cutover-build`, but this lane has not observed it
fire on a true low-memory condition. Stated rather than implied.

## 6. PORT FIDELITY — what was taken from `f07a630` and what was deliberately not

`f07a630` touches three files. **Only one was taken.**

| File in `f07a630` | Taken? | Why |
|---|---|---|
| `scripts/run_harness.sh` | **YES** | The fix. Applied via `git cherry-pick -n`; auto-merged cleanly |
| `docs/techdebt/DEBT_REGISTER__v20260804_0523.md` | **NO** | The **demo lane's** register. Importing it would contaminate roadmap's debt history with another lane's IDs — the exact hazard preamble item 10 exists to prevent |
| `docs/techdebt/LATEST_DEBT.md` | **NO** | Demo's symlink repoint; conflicted, restored to roadmap's own |

Two deliberate deviations from a byte-exact port, both required by the preamble:

1. **The upstream comment cites `TD-145` bare.** On `demo-cutover-build` that is the
   memory-metric fix; on `roadmap` `TD-145` is the unrelated MEM-116 master-key finding. A
   verbatim import would have planted a citation that resolves to the wrong debt item for
   every reader of this branch. **Branch-qualified in place per item 10** ("existing bare
   IDs ... are branch-qualified in prose wherever they are cited across branches").
2. **The fail-closed message's `(TD-129/TD-145)` retargeted to `(TD-129/TD-R-166)`** for
   the same reason — it is operator-facing text pointing at a debt ID.

**The 2GB floor is byte-identical to upstream. No threshold was changed, no baseline
touched, no acceptance row re-tiered, nothing marked MET.**

## 7. PREAMBLE COMPLIANCE

- **Item 1 (machine gate):** `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `[REDACTED-USER-PATH]/hip-roadmap`,
  branch `roadmap`, HEAD `e6dcac0`. **The gate did real work here** — it is what caught the
  vanished d195 target before any write.
- **Item 2 (tree not clean):** four **untracked demo-lane dispatch docs**
  (`DISPATCH_DEMO_CUTOVER_*`) were sitting in roadmap's tree on arrival. **Left exactly as
  found.** No `git add -A`, no `git commit -a`; explicit pathspecs only. Verified absent
  from this commit.
- **Item 3 (`.env.dev`):** not loaded — the harness was never run.
- **Items 4/9 (lock):** `hip_lock.py who repo` → `free` on arrival. Lock taken **only**
  around the commit+push, as a child of `hip_lock.py with repo`. No sleep, no reservation.
- **Item 8 (commit and push same dispatch):** done — nothing left unpushed for another
  lane to carry.
- **Item 10 (lane prefixes):** new debt is `TD-R-166/167/168`. See the ID-lane anomaly at
  the top of this doc.

## 8. WHAT REMAINS OPEN

- **TD-R-168** — the under-floor refusal path is unexercised on this lane (see §5).
- **The ID-lane anomaly** — D-D-161 numbered in the demo sequence, landed on roadmap.
  Bill's call whether to re-file under `D-R-196`.
- **`~/hip-dev` and `~/hip-vo` have no `scripts/run_harness.sh`** and so were never
  affected. The frozen demo was not touched.
