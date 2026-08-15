# FM 6 — PROCESS HARDENING: THE FOUR FILED GAPS
Status: **STOPPED AT THE REQ GATE** — nothing built; four tools specified from measured evidence
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap`. Board claim `1e86cd8`.

REQ: **NONE NAMED BY THE DISPATCH — and that is why this stopped.** See §1.

---

## 0. THE EXCEPTION LINE

```
FM 6 — PROCESS HARDENING: THE FOUR FILED GAPS
STOPPED AT SEGMENT 1 — NEEDS BILL
```

**No code was written.** Segment 1 could not start, and segments 2–4 depend on it, so all four
are stopped at the same gate. What was produced instead is in §3: each of the four tools
specified against **measured** facts about this repository, so that the dispatch that does build
them writes code rather than re-deriving the ground.

---

## 1. WHY THIS STOPPED — REQUIREMENTS DISCIPLINE ITEM 8

`CLAUDE.md`, Requirements Discipline item 8, verbatim:

> **GATE, not a guideline: refuse any dispatch that asks for a code change and does not name a
> REQ doc in `docs/requirements/`.** Say what is missing and stop. Do not write the REQ
> retroactively to cover work already done or about to be done — that is a contradiction, not
> compliance. … The only exception: Bill says the literal words **"skip the REQ."** Not "he seems
> in a hurry," not "this is urgent," not inferred from tone or deadline pressure — the words
> themselves, in the dispatch.

**All three conditions are met, and I checked rather than assumed:**

| test | result |
|---|---|
| does this dispatch ask for a code change? | **Yes** — four new executable scripts under `scripts/`, plus four twins |
| does it name a REQ doc? | **No.** `ls docs/requirements/` matched nothing for *claim*, *lane*, *index*, *anchor*, *register*, *scrub*, *preflight*, *bootstrap* or *board* — the four subjects have no requirements doc at all |
| does it contain the literal words "skip the REQ"? | **No** |

**"Tooling only" does not open the gate — the rule closes that door by name.** The
pre-authorized ruling classes say: *"File any TD whose subject is TEST or TOOL infrastructure…
**Filing is pre-authorized; FIXING still needs a REQ** (Requirements Discipline item 8 is
untouched by this)."* This dispatch is fixing tool infrastructure. The gate applies in full.

**I cannot open the gate for myself, and that is stated in the rule too.** Writing a REQ here to
authorise work "about to be done" is the exact thing item 8 forbids and calls *"a contradiction,
not compliance."* So §3 is a **specification offered for approval**, deliberately **not** filed
in `docs/requirements/`, and it authorises nothing.

**The reason to hold the line here rather than anywhere else.** This is a dispatch to build
process-enforcement tooling. Bypassing a process gate in order to ship process gates would be
the strongest possible demonstration that the gates do not bind — and every one of these four
tools exists precisely because *"a rule that is only remembered is not a control"*
(`scripts/staging_guard.sh`'s own header). The tools are worth having; they are not worth having
at the cost of the rule they are meant to enforce.

**What unblocks it — one of two things, either is a one-liner:**

1. **File a REQ** covering the four (or four REQs, one each) — §3 is written so it can be
   lifted into `docs/requirements/` largely as-is; or
2. **Reissue with the literal words "skip the REQ"**, which item 8 provides for, and the TD-log
   obligation it attaches then applies.

---

## 2. WHAT DID RUN — READ-ONLY GROUNDING

No code was written, but the four designs are not speculative. Everything in §3 rests on facts
measured in this repository today. Nothing was executed beyond reads: no graph writes, no demo
tree, no heavy suites (VD-61 owns that slot).

| measured | value |
|---|---|
| identical 4-column table headers in `docs/INDEX.md` | **13** on `roadmap`, **13** on `demo-cutover-build` |
| identical `\|---\|---\|---\|---\|` separator rows | **16** |
| `## <category>/` section headers | **15** in both trees |
| worktrees carrying `.hip-owns` | **2 of 5** — `~/hip-vo`, `~/hip-nc` |
| worktrees carrying `.hip-graph` | **3 of 5** — `~/hip-roadmap`, `~/hip-vo`, `~/hip-nc` |
| worktrees carrying `harness/lane_ownership.py` | **2 of 5** |
| worktrees carrying `harness/graph_target.py` | **3 of 5** |
| `~/.env.dev` `NEO4J_URI` | **`bolt://localhost:7689`** — the FROZEN demo, live, exactly the trap STANDARD PREAMBLE item 3 names |
| lanes where `.env.dev` / `.hip-graph` / `.hip-owns` currently agree | **all of them that have the files** (7688 / 7691 / 7692) |

---

## 3. THE FOUR TOOLS, SPECIFIED — FOR APPROVAL, NOT AUTHORISED

Each entry gives the defect from evidence, the contract, and the acceptance test. **Acceptance
tests are stated as pass/fail observables**, so a REQ can be written from them without
interpretation (Requirements Discipline item 4).

### 3.1 `scripts/claim_lane.py` — the board claim tool

**The defect, from evidence.** Six passenger-commit incidents in two days (VD-58, FM 1 FINDING
10, VD-59-2, FM 3's FM3-4 ×2, FM 5's FM5-2) and one sweep: HA-78's `71601fc` swallowed FM 1's
uncommitted board row because `git add docs/LANES.md` stages **the whole file**, including
another lane's in-progress edits.

**What already exists, and must be built on rather than duplicated.** `scripts/staging_guard.sh`
refuses a shared board file staged alongside other paths without the repo lock, and
`scripts/hip_lock.py` exports `HIP_LOCK_HELD` so tooling underneath can *verify* the lock rather
than trust it. **The guard names its own residual hole in its final paragraph:** *"The lock stops
the collision; only surgical staging stops you committing another lane's rows."* **That sentence
is this tool's entire remit.**

**Contract.** `claim_lane.py <lane> --title "<title>"` (and `--close --commit <sha>`):

1. acquire the `repo` lock via `hip_lock.py` — the real work runs as its child, never a separate
   "take" step;
2. **re-read `docs/LANES.md` from disk under the lock** — never from a copy read before it;
3. rewrite **one row**, matched on the lane's own leading cell, asserting the pipe count is
   unchanged so the table cannot be broken;
4. `git add docs/LANES.md` and commit **that path only**, verified with
   `git diff --cached --name-only` before the commit, not after;
5. push, and **report any commit it carried as a passenger** rather than silently publishing it.

**Acceptance test (the dispatch's twin, made observable).** Two simulated concurrent claims, in a
throwaway repository: both rows land, neither is swept, and the loser blocks on the lock rather
than racing. **Fail if** either row is missing, either commit contains a second path, or the
table's column count changes.

**One open question a REQ must answer, not a session:** step 5 reports passengers — should it
also *refuse* to push when it would carry another lane's commit? That would make the sixth
recurrence impossible, and would also mean a lane can be blocked by a neighbour's unpushed work.
**That is a policy call, not an implementation detail.**

### 3.2 `scripts/register_doc.py` — the INDEX anchor gate

**The defect, from evidence.** `docs/INDEX.md` contains **13 identical table headers and 16
identical separator rows** across **15** category sections. The header text is therefore **not a
unique anchor**, and `requirements/` sits immediately before `dispatches/` in file order.
TD-R-164 found **54 dispatch rows** filed into `requirements/`'s table spanning D-90 through
D-162 — the project's entire history — for exactly this reason.

**Contract.** `register_doc.py --category <cat> --row "<markdown row>"`:

1. locate `^## <category>/$` — **the only unique anchor in the file**;
2. walk forward to the **first** separator row *inside that section*, refusing to cross the next
   `## ` heading;
3. **re-read and re-verify the anchor immediately before the write**, so a concurrent edit
   between locate and write is caught rather than raced;
4. assert the row's pipe count matches the table's, then insert as the **first** row
   (newest-first);
5. **ABORT loudly with a non-zero exit on a stale or missing anchor. Never silently skip.**

**Acceptance test.** A deliberately staled anchor goes red: mutate the section header between
locate and write and confirm a non-zero exit with the reason on stderr and **the file
byte-identical**. **Fail if** it exits zero, writes anything, or falls back to a nearby table.

**Note for whoever builds it:** exit codes are the trap here. `CLAUDE.md` Requirements Discipline
item 13 records three false all-clears (D-70, D-75, D-88) caused by `grep -c` exiting non-zero on
a legitimate zero. **This tool's own verification steps must run unchained.**

### 3.3 `scripts/lane_preflight.py` — the lane bootstrap check

**The defect, from evidence — and it is on disk, not hypothetical.** `~/hip-nc/.hip-graph` says
so in its own words: the `natural-conversation` branch was cut from a commit carrying
`~/hip-vo`'s lane files, so **the checkout inherited another lane's pin verbatim and declared a
graph it did not own** (7691). NC 5 corrected it to 7692. Nothing was written through it — but
**not because the ownership machinery caught it**: `~/hip-nc` had no `.env.dev`, so every run
failed closed at `harness/zep_store.py`'s password guard. **An unrelated fail-closed saved it.
An inherited declaration is not proof of ownership, and the declaration alone never was.**

**Two structural facts a REQ must decide on, because they change the tool's scope:**

- **The declarations are not the operative pin.** `~/hip-vo/.hip-graph` states it plainly:
  *"RECORD, NOT ENFORCEMENT … nothing reads this file yet … the operative pin is `.env.dev`."*
  So `.hip-graph` and `.env.dev` **can disagree, and today only `.env.dev` decides.** Detecting
  that disagreement is the tool's core value.
- **The machinery is only partly deployed:** `.hip-owns` in 2 of 5 worktrees,
  `.hip-graph` in 3 of 5, `lane_ownership.py` in 2, `graph_target.py` in 3. **`~/hip-dev` and
  `~/hip-cutover-demo` have none of it**, so a preflight demanding all four artifacts refuses
  those two lanes outright. **Is that the intent, or must those lanes be provisioned first?**

**Contract.** Before any graph-writing test: prove that lane identity, worktree path, branch,
`.hip-owns`, `.hip-graph` and the operative `.env.dev` pin **all agree**, and that the target is
not `7689` (the frozen demo) and not another lane's port. **Exit non-zero on any disagreement,
naming which two sources disagree and what each says.** Reading `~/.env.dev` — which pins
**7689** with `override=True` — must be treated as a hard failure, not a warning.

**Acceptance test.** Reconstruct the NC 5 shape: a checkout whose `.hip-owns`/`.hip-graph` name
another lane's port. **Red, with the two disagreeing sources named.** Second case: declarations
agree but `.env.dev` points elsewhere — **also red**, because that is the case the current
machinery cannot see.

### 3.4 `scripts/scrub.py` — the scrub unification

**The defect, from evidence.** FM 5 established that `scripts/push_docs.sh` is a **detector, not
a scrubber** — it greps and aborts, and has never substituted a character. Every redaction to
date was written fresh by whichever dispatch needed it: the 2026-08-13 home address, then FM 5's
addressing pass. **The detector is in the repo; no substituter is.** FM 5's first build then
failed its own verification on a class the hostname rule did not cover — a bare domain suffix
that `push_docs.sh`'s pattern *does* catch. **Detector and scrubber had already drifted, within
one dispatch.**

**Contract.** One pattern table as the single source of truth, consumed by both:

- each entry carries a **name**, a **detect** pattern and a **replacement token** in the
  project's existing `[REDACTED-*]` form, which `push_docs.sh`'s own `grep -v "\[REDACTED"`
  already honours;
- `push_docs.sh` reads its scan pattern **from that table** instead of an inline literal — this
  is the part that makes drift structurally impossible rather than merely unlikely;
- `scrub.py` applies the substitutions and **verifies zero residual against the written output**,
  not the in-memory copy;
- the table must carry **FM 5's fourth rule (bare domain suffix)** and **the LAN address**, which
  `push_docs.sh` does not currently cover and which entered by Bill's ruling.

**A caveat the builder must not paper over.** `push_docs.sh`'s pattern is tuned for `docs/`: its
`password`/`secret`/`api_key`/`token`/`NEO4J`/`bearer` alternatives fire on ordinary source by
design — `NEO4J_PASSWORD = os.environ.get(...)` is a match and is not a secret. **A shared table
must therefore mark which entries are safe to run over source and which are docs-only**, or the
unified tool will be unusable on the thing it is most needed for.

**Acceptance test.** A planted address in a staged doc is scrubbed, and verification against the
**written file** reports zero residual. **Plus the regression that FM 5 lived:** a document that
*quotes* a pattern while certifying it absent must go **red**.

---

## 4. WHAT THIS DISPATCH DID NOT DO

- **Wrote no code.** No file under `scripts/` was created or modified.
- **Did not write a REQ** — item 8 forbids a session authorising its own build that way.
- **Did not touch the ops doc or the FM 2 operating-model doc.** Both updates describe the four
  tools as the enforced path; naming an unbuilt tool as enforced would make the operating model
  false on the day it was written.
- **Ran no test, no suite, no gate**; touched no graph, no demo tree, no product runtime code.
- **Changed nothing in any other lane.**

---

## 5. FILED, NOT BLOCKING (1)

**(FM6-1) The staging guard protects one worktree, and its own header says so.** *"Hooks are
per-worktree and are NOT version controlled. This protects `~/hip-roadmap` only. A repo-wide
answer needs `core.hooksPath` committed to the tree; named, deliberately not taken."* Five
worktrees share `~/hip-dev/.git`; four of them have no guard. **`claim_lane.py` inherits this
limit** — a tool in `~/hip-roadmap/scripts/` is on the `roadmap` branch and is simply absent from
the others until each branch carries it. **Whatever is built in §3.1 will protect one lane unless
distribution is solved with it**, and distribution is a separate decision because it changes
every lane's commit behaviour.

---

## 6. CLAIM IMPACT

```
CLAIM IMPACT: none
```

---

## 7. NEEDS BILL

1. **File a REQ for the four tools — or reissue with the literal words "skip the REQ."** §3 is
   written to be liftable into `docs/requirements/` with its acceptance tests intact.
2. **§3.1 — should `claim_lane.py` refuse to push when it would carry a passenger**, or only
   report it? Refusing ends a six-occurrence pattern and lets a neighbour's unpushed work block a
   lane.
3. **§3.3 — `~/hip-dev` and `~/hip-cutover-demo` carry none of the lane-ownership machinery.**
   Should the preflight refuse them, or must they be provisioned first?
4. **§5 — distribution.** A tool on `roadmap` protects `roadmap`. Solving that means committing
   `core.hooksPath` or porting per branch, and it changes every lane's commit behaviour.

---

## 8. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- Board: **FM 6 claimed at `1e86cd8`** (first commit of the dispatch), closed by this dispatch's
  own commit, both `docs/LANES.md`-only and both under `scripts/hip_lock.py with repo`.
- The gate finding was measured, not assumed: `docs/requirements/` was listed and searched for
  all nine subject keywords before item 8 was invoked.
- Every figure in §2 was read from disk today; no value is carried from an earlier dispatch.
