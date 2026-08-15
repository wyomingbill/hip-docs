# DISPATCH_FM32_STAGED_DIFF_PROCESS_BATCH
Status: BUILT
Reconciled-Against: `cf791e2` (`~/hip-roadmap` @ `roadmap`), 2026-08-15

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_PROCESS_HARDENING_TOOLS__claim-lane-register-doc-lane-preflight-scrub__v20260814_1613.md`
— **AMENDMENT 5**, committed at `7c480a1` **before the first code edit**.

**CLAIM IMPACT: none.**

> **FM 32 WAS ISSUED ONCE AND NEVER EXECUTED.** It arrived mid-turn during FM 31, was
> deferred because FM 31 carried a possible live secret on a public mirror and because
> FM 32 item 1 rewrites the very tool FM 31 needed to close its own row — then FM 34 was
> issued before it started. Another session recorded the gap on the board rather than
> closing it silently. **This is the re-issue, executed in full.**

---

## THE ASK

Verbatim.

> 1. TD-R-198 FIRST: repair the two broken board rows — the Natural-conversation row
>    (7 bare pipes vs 6-pipe header) and the Advisor row (15) — escape the stray pipes so
>    claim_lane accepts edits again. Then TD-R-194(b): close mode handles pipe-malformed
>    rows so this never needs hand surgery again.
> 2. FM 30's missing board row: add it (verdict banking, done 2026-08-15 ~09:14) — Bill's
>    ruling.
> 3. Staged-diff rule (Bill, verbatim): "guards inspect the staged diff/commit payload,
>    never infer safety from the working tree." Surgical staging + claim close verify the
>    STAGED set; twin: a staged-but-not-working-tree foreign row is refused.
> 4. TD-R-196: lane_preflight detects a fully-held seam (two sessions, one worktree).

**The claim did NOT need a hand-claim** — the FABLE MASTER row was already well-formed at
6 pipes, so `claim_lane.py` took it normally (`578f28c`). Said because the dispatch asked
to say so either way.

---

## 1. THE TWO BOARD ROWS — REPAIRED, AND PROVEN BY THE TOOL

| row | before | after | escaped |
|---|---|---|---|
| `Advisor — ~/hip-roadmap @ roadmap` | **15** | **6** | 9 |
| `Natural conversation — ~/hip-nc @ natural-conversation` | **7** | **6** | 1 |

**ESCAPING ONLY. No text moved.** Asserted mechanically, not by eye: each repaired row is
byte-identical to the original once the added backslashes are removed, and word counts are
unchanged — **6171 → 6171** and **20220 → 20220**.

**THE PROOF IS THE TOOL ACCEPTING THEM, NOT A RECOUNT.** After the repair, `claim_lane.py
close` performed a real edit on each row, and those two commits are the evidence:

| proof commit | row |
|---|---|
| **`fa09f85`** | the Advisor `roadmap` row — the sentence it added was written *by the tool* |
| **`11b0c37`** | the Natural-conversation row — likewise |

### ⚠ THE AMBIGUOUS CASES WERE A DECISION, AND ARE RECORDED AS ONE

**Both rows carried MORE structural-looking pipes than the header has columns**, so neither
could be repaired without deciding which candidate boundary was the accident. Eight of the
Advisor row's nine were unambiguous content — two shell pipes inside an `lsof … | xargs`
code span, three boolean `||`, one quoted `'||'` — but **one on each row was a genuine
candidate cell boundary.**

**Rule applied (Amendment 5 G1b): keep the FIRST candidate after the preceding cell, escape
the later one** — the column order defines the first, so a later one is necessarily the
extra. On the Advisor row that keeps the HA-90 boundary and escapes the HA-89 one; on the
NC row it keeps the NC 22 boundary and escapes the NC 19 one. **Presentation only: no text
moves either way, and every word stays in the row.**

## 2. FM 30's MISSING ROW — ADDED, WITH ITS LIMIT

Added at **`3b8c9da`** on Bill's ruling. **The honest limit, searched and not assumed:
no commit anywhere in the repository mentions FM 30** — `git log --all --grep="FM 30"`
over every branch returns nothing — and no doc mentions it except the two that record the
gap. So the row states what Bill states and **claims no artifact**: a recap-only dispatch,
the FM 33 shape. Recorded that way so a later reader does not go hunting for a commit that
does not exist.

## 3. THE STAGED-DIFF RULE — THE GUARD NOW READS THE INDEX

**The hole, and why the old check could not see it.** `surgical_commit_and_push` verified
the staged **file list** — *which* files are staged. It never looked at *what was in them*.
So if another session had staged a different version of the board (a foreign row in the
index, absent from the working file), `git add` **overwrote the index with the working
tree** and their staged row was destroyed silently. The file list reads
`['docs/LANES.md']` either way, so nothing noticed. **Two sessions in one worktree share
ONE index** (NC 24 §8.6) — this is not hypothetical.

Two guards now, in order:

1. **BEFORE touching the index:** the index version of the board must equal HEAD's. Any
   divergence means somebody else staged something, and the tool **refuses rather than
   clobbers**.
2. **AFTER staging:** the **payload** is inspected — `git diff --cached -U0` must show
   exactly **one** row removed and **one** added, and the added row must start with this
   lane's prefix.

## 4. TD-R-196 — A SEAM CAN BE HELD WITH NOTHING RUNNING

`lane_preflight.scan_held()` reports a worktree **HELD** when it is **CLAIMED**
(`.hip-scope` present) **AND DIRTY beyond that file**. The second half is deliberate: a
stale `.hip-scope` would otherwise mark its worktree held forever. **Claimed-but-clean is a
note, never a block.** It enumerates the worktrees of the repo being preflighted, not of
the CWD.

Live, on this machine, right now:

```
  HELD     [REDACTED-USER-PATH]/hip-vo   — claimed AND dirty (2 uncommitted/untracked item(s))
  note     [REDACTED-USER-PATH]/hip-nc2  — claimed but CLEAN — not blocking
```

…while the existing `--busy` scan says **NOT BUSY**. That is TD-R-196 reproduced and then
detected.

### ⚠ A REGRESSION I INTRODUCED, CAUGHT BY AN EXISTING TWIN, REPORTED NOT EDITED AWAY

My first design folded held seams into `--busy`'s verdict. **FM 14's own twin — "clean
machine passes" — went from exit 0 to exit 7 the moment it landed**, because `~/hip-vo` is
legitimately claimed-and-dirty while another lane works in it.

**That twin was right and my default was wrong.** Editing FM 14's twin so my change went
green is exactly the shape this project forbids. So `--busy` still answers *"is anything
MID-RUN"* byte-for-byte as before, the held scan is **visible** in its output, and
**refusing on it is opt-in behind `--held`** until Bill rules. Promoting it to a default
refusal would refuse lanes that are legitimately parallel today — **measured, not
hypothesised, because that is precisely what it just did.**

---

## VERIFIED — ALL SEVEN TWINS GREEN

`python3 scripts/lane_tools_selftest.py` → **ALL TWINS GREEN**, including the five that
predate this dispatch.

| twin | direction | result |
|---|---|---|
| G3-1 foreign row **staged, absent from the working tree** | must REFUSE | **PASS** (rc=2, `INDEX ALREADY HOLDS`) |
| G3-1 reverse — clean index | must proceed | **PASS** (rc=0) |
| G3-2 two rows in the staged payload | must REFUSE | **PASS** (rc=2, `STAGED PAYLOAD CHANGES`) |
| G2 code-span pipe | must repair to the header count | **PASS** (rc=0) |
| G2 reverse — ambiguous boundary | must REFUSE, row untouched | **PASS** (rc=2, `REPAIR INCOMPLETE`) |
| G4 claimed + dirty, no process | must read HELD | **PASS** |
| G4 reverse — claimed but clean | note, NOT held | **PASS** |

**G3-1 is the twin that decides this dispatch.** A working-tree guard passes that case and
destroys the neighbour's staged content; only a guard that reads the index refuses it.

**Live, beyond the twins:** default `--busy` exits **0** (contract unchanged);
`--busy --held` exits **7** and names the held seam.

**A harness defect found and named, not quietly fixed:** the fixtures shared one bare
origin, so every repo after the first pushed non-fast-forward, its seed never reached
`origin/master`, and the **passenger gate fired on the fixture's own commit** — a harness
artefact that looked exactly like a real refusal (rc=3) in two of the seven cases. One
origin per fixture now. **Both cases were red for a reason that had nothing to do with the
mechanism under test**, which is worth stating: a twin that fails for a harness reason and
is "fixed" by weakening the assertion is how a green set stops meaning anything.

**Reasoned about — not independently executed:**
- That escaping code-span pipes can never change a table's meaning. It follows from a
  backtick span never being a cell boundary; the count-against-header check is what makes
  it safe in practice rather than in argument.
- That the index-vs-HEAD comparison catches every foreign-staging shape. It catches every
  shape where the index differs from HEAD, which is all of them for a tracked file — but
  **an untracked foreign file staged alongside is still caught only by the older file-list
  check**, which remains in place.

---

## HASH

| commit | what |
|---|---|
| `578f28c` | board claim (via the tool — no hand-claim needed) |
| `7c480a1` | **REQ Amendment 5 — before code** |
| `584fc90` | the two rows repaired, escaping only |
| `fa09f85`, `11b0c37` | **the tool editing each repaired row — the proof** |
| `3b8c9da` | FM 30's row added |
| `cf791e2` | G2 + G3 + G4 and the twins |
| *(this commit)* | dispatch doc, three TD statuses, INDEX |

---

## OPEN

1. **NEEDS BILL — promote `--held` to the default?** It would refuse lanes that are
   legitimately parallel today. The evidence is in §4.
2. **TD-R-194's own register row carries 7 bare pipes** against that register's shape — the
   same defect class, one file over. **Left exactly as found:** repairing another row while
   patching its status would be the silent sweep this whole batch exists to prevent. Named,
   not fixed.
3. **The repair mode cannot help a row whose stray pipe is outside a code span.** By design
   — that case is a ruling. Two such cases existed here and both were decided by hand under
   G1b.
4. **Not measured: whether any OTHER shared register or board file carries malformed rows.**
   The board's live-lanes table is now clean; nothing else was surveyed.
