# FM 3 — REVIEW PACKAGE RECOVERY + REFRESH FOR RESEND
Status: BUILT — **LANDED**
Reconciled-Against: 2026-08-14. Packages pinned at `hip-cutover-demo 7904c36`,
`hip-roadmap d9e2010`, `hip-vo 65c263e`. Board claim `d9e2010`.

REQ: **NONE.** Recovery, measurement and packaging; no product code changed. Requirements
Discipline item 8 gates dispatches that ask for a code change, and item 10 allows an
ANALYSIS/MEASUREMENT dispatch to carry REQ: NONE provided it says why. This says why.

---

## 0. THE EXCEPTION LINE

```
FM 3 — REVIEW PACKAGE RECOVERY + REFRESH FOR RESEND
COMPLETE WITH FINDINGS — 4 ITEMS FILED, NOTHING BLOCKING
```

**NEEDS BILL: one decision, not blocking** — §6.1, the shape change from two bundled
packages to three per-tree ones. The packages are built and uploadable either way; the
question is whether the reviewer should receive three requests or a bundle.

---

## 1. SEGMENT 1 — LOCATE

All three 2026-08-13 packages were found on the Desktop and opened. **None of them is a
capability-scoped package** in the operating model's sense — all three are whole-tree
source dumps, which is expected: they predate the operating model by a day.

| # | file | built | size | files | trees + HEAD |
|---|---|---|---|---|---|
| 1 | `[REDACTED-USER-PATH]/Desktop/HIP_CODE_REVIEW.zip` | 08-13 15:49 | 17.5 MB | 2197 | `hip-cutover-demo` @ **`e6b165c`** + `hip-roadmap` @ **`555cc2c`** |
| 2 | `[REDACTED-USER-PATH]/Desktop/HIP_VO_REVIEW.zip` | 08-13 16:21 | 3.3 MB | 686 | `hip-vo` @ **`fac5c8e`** (`git archive` of the pinned commit) |
| 3 | `[REDACTED-USER-PATH]/Desktop/HIP_CODE_REVIEW_REDACTED_20260813.zip` | 08-13 16:44 | 82.5 MB | 2457 | `hip-cutover-demo` + `hip-roadmap` — **HEAD not recorded in its manifest** |

### 1.1 Package 3's HEAD was not recorded, and was recovered rather than guessed

`MANIFEST_REDACTED.txt` names the trees but no commit. Recovered from the commit graph:
`demo-cutover-build` sat at `e6b165c` from 08-13 14:29 until 08-14 09:45, and `roadmap`
sat at `555cc2c` from 08-13 15:47 until 08-13 16:54. Package 3 was built at 16:42–16:44,
**inside both windows**, so its HEADs are `e6b165c` and `555cc2c` — the same pair as
package 1.

### 1.2 Package 3 SUPERSEDES package 1; they are one review, not two

Same trees, same commits. The differences are in the copy, not the code:

- **Package 3 carries the corrected redaction** — 137 substitutions across 57 files, adding
  the **URL percent-encoded** forms and the **newline-split** occurrences that package 1's
  pass (119 substitutions across 48 files) missed.
- Package 3 additionally **excludes** credential and runtime files (14 named) that package
  1 shipped, including `.env.dev` and `certs/voice.key` from `hip-roadmap`.
- Package 3 additionally **includes** the `business/` document tree (the 82 MB).

**So there were TWO reviews outstanding, carried by three files.**

### 1.3 Capability: there is none, and one was not invented

The operating model names packages `HIP_REVIEW_<capability>_<HEAD>.zip`, where a capability
comes from a capability dispatch. **No capability dispatch produced these** — they were
whole-codebase reviews. The `<capability>` slot is therefore filled with the **lane
identity**, which is factual and needs no invention: `demo-cutover`, `advisor-roadmap`,
`governed-voice`. Recorded here so a later reader does not mistake a lane name for a
capability that was scoped and never delivered.

---

## 2. SEGMENT 2 — DRIFT

**Measured as commits since each package's HEAD touching that package's reviewed surfaces.
Because all three packages reviewed the WHOLE tree, every commit in the window is drift on
a reviewed surface — the question is only how much and where.**

| package | window | commits | files | insertions | verdict |
|---|---|---|---|---|---|
| `hip-cutover-demo` (pkgs 1+3) | `e6b165c..7904c36` | **10** | 21 | +1662 / −17 | **STALE** |
| `hip-roadmap` (pkgs 1+3) | `555cc2c..d9e2010` | **66** | 45 | +6038 / −42 | **STALE** |
| `hip-vo` (pkg 2) | `fac5c8e..65c263e` | **31** | 65 | +8299 / −235 | **STALE** |

**All three are STALE. None is still reviewable as sent.** The verdict does not rest on
commit count alone — in every window, governance-bearing code moved:

- **`hip-cutover-demo`** — a model-provider decommission created `harness/groq_models.py`
  and a `config.yaml` `models.groq` block, and changed call sites in
  `harness/epistemic_record.py`, `harness/fact_change.py`, `scripts/generate_corpus.py`,
  `server/voice_orch.py` and `server/static/demo.html`. **This is egress-adjacent code —
  it decides which off-device model a turn reaches** — and the browser carries its own
  copy of the model-id set, so there are two sources of truth for one fact.
- **`hip-roadmap`** — transcript storage and session keys
  (`harness/session_content_key.py`, `harness/session_transcript_buffer.py`,
  `harness/transcript_log.py`), confirmed-write honesty
  (`harness/confirmation_gate.py`, `harness/canonical_value.py`, `harness/fact_change.py`),
  the same provider decommission, and test-collection tooling (`pytest.ini`,
  `conftest.py`, `eval/test_import_mode_shadowing.py`). `CLAUDE.md` itself changed.
- **`hip-vo`** — the A1 GOVERNED VOICE build (`harness/turn_request.py`,
  `harness/speech.py`, `harness/member_session.py`, `server/voice_https_orch.py` +186,
  `server/voice_orch.py` +95), the phased gate (`scripts/gate_check.sh`,
  `scripts/gate_state.py`, `harness/lane_guard.py`), supersede-vs-park
  (`eval/test_supersede_no_contradictory_state.py`), and egress
  (`harness/egress_gateway.py`, `eval/test_egress_gateway.py`).

**A second, independent reason all three are stale:** their findings were **never
returned**. There is no review to be continued, so the refresh is not a delta on prior
findings — it is a first review of the current code.

---

## 3. SEGMENT 3 — REBUILD

Three packages, at `~/Desktop/HIP_REVIEW_20260814/`:

| package | tree @ branch | pinned HEAD | zip size | files |
|---|---|---|---|---|
| `HIP_REVIEW_demo-cutover_7904c36.zip` | `~/hip-cutover-demo` @ `demo-cutover-build` | `7904c36` | 2.1 MB | 371 |
| `HIP_REVIEW_advisor-roadmap_d9e2010.zip` | `~/hip-roadmap` @ `roadmap` | `d9e2010` | 2.8 MB | 441 |
| `HIP_REVIEW_governed-voice_65c263e.zip` | `~/hip-vo` @ `main` | `65c263e` | 1.6 MB | 324 |

### 3.1 Contents — the dispatch's list, per package

`REVIEW_REQUEST.md`, `REQUIREMENT.md`, `DESIGN_DECISIONS.md`, `CHANGED_FILES.txt`,
`git.diff`, `TEST_RESULTS.md`, `KNOWN_ISSUES.md`, plus `GIT_STATE.txt`, `REDACTION.md`,
`source/` and `architecture/`. **All nine verified present in each delivered zip.**

- **`REVIEW_REQUEST.md` is self-contained**, hand-written per package. It opens with the
  reviewer role and the claim under test — *a deterministic core decides authorization,
  disclosure, consent and memory, not the model* — then what to review, at which HEAD,
  what the review should answer (6–7 numbered questions naming real modules), what is out
  of scope, the required findings format (`FINDING n` / `SEVERITY` / `WHERE` / `EVIDENCE` /
  `REQUIRED CHANGE`, then `VERDICT` CLOSED / CLOSED WITH CAVEATS / NOT CLOSED, then a
  ranked `TOP 3`), and ground rules. **A fresh thread with zero context can execute it.**
- **`REQUIREMENT.md` says plainly that the review is NOT scoped to one requirement**, and
  supplies the requirements register at the pinned commit instead — 83 / 86 / 41 docs, of
  which **30 / 19 / 4** are explicitly NOT MET. Bodies are not bundled; they are offered
  on request at the same commit.
- **`TEST_RESULTS.md` reuses recorded runs only. Nothing was executed.** Each figure
  carries its command, its commit and its source. **Where the newest recorded run predates
  the packaged commit, the package says so** — it does for all three.
- **`git.diff` and `CHANGED_FILES.txt` cover the review window**, previous package HEAD →
  this package's HEAD, so the reviewer can see what is newest and least-reviewed.

### 3.2 Packaging method — pinned commit, not working tree

Every file was read with `git show <HEAD>:<path>`. **Three lanes were editing these
checkouts during this dispatch** (VD-60 on the demo, HA-81 on roadmap, NC 5 claiming), so a
working-tree copy would have been a moving target. Untracked files, staged and unstaged
edits, and anything gitignored are absent **by construction, not by filtering** — stated in
each package's `GIT_STATE.txt` so nothing is inferred. **No live tree was written to.**

### 3.3 Redaction — carried over, not re-derived

The address pattern is reused **verbatim** from the corrected 2026-08-13 pass: it covers
the abbreviated / periodded / spelled-out street type, the optional city and city+state
forms, URL percent-encoding (`%20`, `%2C`, `+`) and occurrences split across a newline.
The first 08-13 pass missed the last two classes; reusing the corrected pattern is what
keeps that from recurring.

| package | substitutions | files |
|---|---|---|
| `demo-cutover` | 6 | 3 |
| `advisor-roadmap` | 7 | 4 |
| `governed-voice` | 6 | 5 |

**VERIFIED AGAINST THE DELIVERED ARTIFACT, not the staging copy:** the three zips were
extracted to a clean directory and scanned — **1053 files, ZERO occurrences** of the
identifying house-number-plus-street pair in any form, including within 40 characters in
either order.

**ONE residual fragment, left in deliberately and flagged:**
`HIP_REVIEW_demo-cutover_7904c36/architecture/docs/INDEX.md:265` — a **street-name-only**
fragment inside leak-analysis prose (`'You usually take … St…'`), which is the evidence of
what leaked. It carries no house number and no city. **Scrubbing it would destroy the
record of a real defect**, so it is flagged in that package's `REDACTION.md` for a separate
ruling rather than removed.

---

## 4. WHAT EACH REVIEW REQUEST ASKS FOR

Summarised so the board row does not have to be opened to know what was sent.

| package | the questions that carry the most weight |
|---|---|
| `demo-cutover` | is the deterministic core deterministic; can anything leave without the consent gate; **does the screen tell the truth** (browser re-derives what the server acted on); is the record enough to tell refusal from failure; what is tested vs merely collected |
| `advisor-roadmap` | **is erasure real, and what surfaces does it not reach**; does the transcript path's "never decrypts" hold structurally; egress permits; **can the record be made to lie**; shadowed tests |
| `governed-voice` | **is a spoken turn genuinely the same governed turn, or two paths that agree today**; is the egress gateway a chokepoint or one of several exits; where identity is lost; **is the gate honest** (can a phase report a step it did not run); and an explicit request to **adjudicate a live contradiction between two test layers** |

Each package discloses its own weak evidence up front rather than letting the reviewer
find it: the demo's battery has not run over its window, roadmap's `970/0` figure is
recorded as unreproduced and one vacuous PASS is labelled as such, and hip-vo's first-ever
`--full` run **failed** and is reproduced in full with its diagnosis offered for challenge.

---

## 5. FILED, NOT BLOCKING (4)

**(FM3-1) Package 3 recorded no HEAD.** `MANIFEST_REDACTED.txt` names its trees but not the
commits, so the single most important fact about a review package — *what code is this* —
had to be recovered from commit timestamps. Recovery succeeded and is shown in §1.1.
**Every package built here records its pinned commit in three places** (filename,
`GIT_STATE.txt`, `REVIEW_REQUEST.md` header).

**(FM3-2) Package 1 shipped credential and runtime files that package 3 excluded** — 14
named, including `hip-roadmap/.env.dev` and `certs/voice.key`. Package 1 is still on the
Desktop. **Nothing here deletes it** — destructive writes are not pre-authorized — but it
should not be sent, and if it was sent on 08-13 that is worth knowing. **The new packages
exclude `.env*`, keys, certificates and databases by construction.**

**(FM3-3) The `<capability>` slot has no capability behind it.** See §1.3. Filled with the
lane identity and flagged rather than invented.

**(FM3-4) FM 3's closing push carried TWO other lanes' claim commits as passengers** —
**NC 5's `6d4576d`** (13:20:13) and **HA-83's `534dfa4`** (13:30:09) both sat
committed-but-unpushed on `roadmap` when FM 3 closed, so FM 3's push published both.
VD-59 carried HA-81's `7a019aa` the same way earlier today, and the same shape is on
record at VD-58 and FM 1's FINDING 10 — **five instances in two days**, all from one
cause: every worktree shares one commit graph, so a claim row committed and not pushed is
published by whichever lane pushes next. Harmless in substance — publication is a claim
row's whole purpose — but **no lane decided it.** Recorded, not corrected.

**Worth noting alongside it, because it is the reason the pin is still sound:** both
passengers touch `docs/LANES.md` and nothing else, so **no reviewed source moved after
`d9e2010`** (§9). Board churn on a shared branch is loud but harmless to a package pin;
a code commit in the same position would not have been.

---

## 6. NEEDS BILL — ONE DECISION, NOT BLOCKING

### 6.1 Three per-tree packages, where there were two bundled reviews

**What was done and why:** the naming convention `HIP_REVIEW_<capability>_<HEAD>.zip` takes
**exactly one HEAD**, and packages 1/3 spanned two trees at two different commits. Splitting
per tree makes each package's identity exact, keeps each under 3 MB, and gives a
zero-context reviewer one tree, one HEAD and one request. It also cost nothing to reverse.

**What it changes:** the reviewer receives three requests rather than two. Since the
08-13 findings never returned, no continuity was broken by the split.

**The alternative, if you prefer it:** re-bundle `demo-cutover` + `advisor-roadmap` into one
zip named for the demo HEAD, with the roadmap HEAD stated inside. **Say the word and it is
a rebuild, not a redesign** — the staged trees are still on disk.

---

## 7. WHAT THIS DISPATCH DID NOT DO

- **Ran no test, suite, battery or gate.** VD-60 owns the heavy slot; every figure in every
  `TEST_RESULTS.md` is a recorded run with its provenance named.
- **Wrote nothing to any live tree.** Sources were read from pinned commits; the only
  writes are the new package directory, this doc, its INDEX row and the board row.
- **Deleted nothing.** The three 08-13 packages are untouched on the Desktop, including the
  one that carries credentials (FM3-2).
- **Did not send anything.** The packages are built and verified; uploading them is Bill's.
- **Did not bundle requirement or design document bodies** beyond `docs/design/` and
  `docs/specs/` — `docs/requirements/` is large and mostly historical, so the register is
  supplied and the bodies are offered on request at the same commit.
- **Did not touch `docs/deliverables/MANIFEST.md`.** The packages live outside the
  repository, so the Document Governance Rule's Section B/C obligations are not engaged.

---

## 8. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Recovery and packaging; no evidence bearing on a ledger claim was produced or moved.

---

## 9. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- Board: **FM 3 claimed at `d9e2010`** (first commit of the dispatch), closed by this
  dispatch's own commit with the package paths.
- **The `advisor-roadmap` package is pinned at `d9e2010`, and every commit after it on
  `roadmap` is a board row** — `6d4576d` (NC 5) and `534dfa4` (HA-83), plus this
  dispatch's own. `git diff --name-only d9e2010..HEAD` returns **`docs/LANES.md` and
  nothing else**. **No reviewed source moved after the pin**, so the package's HEAD is
  still an accurate name for its contents.
- Every file path cited in all six hand-written package documents was checked to resolve
  inside its own package: **zero unresolved citations.**
- Redaction verified against the delivered zips: **1053 files, 0 full-address occurrences,
  1 flagged fragment.**
