# DISPATCH_FM35 — exclude-from-publication: manifest-driven, fail-closed
Status: **BUILT — PUBLISHED BY BILL'S RULING, 2026-08-15 (see S7)**
Status-History: `BUILT — COMMITTED, DELIBERATELY NOT PUSHED (Bill's instruction)` — the
wording while the original instruction stood. Kept visible: the dispatch obeyed it, and
two of its commits were published anyway by another lane's push (S7).
Reconciled-Against: `80d03c6` (`~/hip-roadmap` @ `roadmap`)
Dispatch: FM 35
Date: 2026-08-15 12:10 → 12:40 (Mountain)
REQ: **`REQ_PUBLICATION_MANIFEST`** — committed `c2163d3`, **BEFORE the first code edit**
Inputs: **FM 31** (the scan that fails closed — the detector) · **FM 34** (the triage — the seed)

COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING

---

## 0. AN INCIDENT THIS DISPATCH CAUSED, REPORTED FIRST

**`claim_lane.py` was invoked to test whether the row tooling would refuse the FABLE MASTER
row. It did not refuse — it executed and PUSHED.** Commit `c0cc0d7` ("probe") replaced FM 34's
identifier on the board with a test placeholder and overwrote `~/hip-roadmap/.hip-scope`.

- **Repaired at `80d03c6`**: FM 34's identifier restored, the placeholder gone (verified: zero
  occurrences), FM 35 claimed properly in the same edit.
- **The bad commit was NOT rewritten.** History rewriting is not pre-authorized, so `c0cc0d7`
  stays in the graph and is named here and on the board instead.
- **The lesson, recorded so it is not re-learned:** the tooling does **not** refuse this row, so
  the dispatch's "hand-claim if the tooling refuses" allowance was never needed — and a probe of
  claim tooling must run against a throwaway copy of the board, never the live file.

---

## 1. WHAT WAS BUILT

**`scripts/publication_manifest.tsv`** — four classes, one line per file:

| class | meaning |
|---|---|
| `PUBLIC` | may be mirrored |
| `PRIVATE` | never mirrored |
| `EVIDENCE-PRIVATE` | never mirrored **and never altered** — its worth is byte-identity |
| `PENDING-SCRUB` | carries a real-secret-class hit, not yet scrubbed; excluded until the scrub dispatch runs |

**It lives OUTSIDE `docs/` on purpose:** a public list of which files were withheld is a signpost,
and the manifest's job does not require publishing it.

**`scripts/publication_gate.py`** — classifies every file the mirror would touch and refuses
fail-closed. **`scripts/push_docs.sh` calls it BEFORE the subtree split**, which is the only
placement that means anything: a split publishes the whole subtree *and its history*, so once it
has run the exclusion decision is already spent.

## 2. THE DEFAULT, STATED AS ASKED

**Unclassified + a scrub-class match → REFUSE the publication. Unclassified + clean → PUBLIC.**

- **PUBLIC-if-clean preserves exactly today's behaviour.** The mirror already publishes everything
  under `docs/` when the scan is clean, and the detector deciding "clean" is the same one.
- **Defaulting to PRIVATE would silently un-publish several hundred documents** on the next run —
  a large invisible change wearing safety's clothes, and it would make adoption all-or-nothing.
- **The guarantee lives where the risk is:** unclassified **plus** a match refuses.
- **RESIDUAL, stated:** a secret of a class the detector does not know, left unclassified, would
  publish. That is the current pipeline's limit too. **Offered for overrule** — flipping it is one
  line plus a classification pass.

**The gate is deliberately STRICTER than `push_docs.sh`:** it runs the shared detect table and
drops already-redacted lines, but does **not** run the push scan's third stage (dropping
documented-usage prose). It can therefore refuse on a line the push scan would excuse. That is the
right direction for a gate — the third stage exists to keep a prose scan usable, and a
classification gate that inherits its excuses inherits its blind spots.

## 3. THE TWINS — 10, ALL GREEN

| twin | proves | result |
|---|---|---|
| **P1** | unclassified + match **REFUSES**, naming the file *and* the class | PASS |
| **P1b** | anti-vacuity: classifying that same file changes the refusal, so P1 tests the manifest and not the scanner | PASS |
| **P2** | **EVIDENCE-PRIVATE never reaches staging** — absent from the staged list *and* from the staging directory on disk | PASS |
| **P2b** | PRIVATE and PENDING-SCRUB are excluded too | PASS |
| **P3** | **PUBLIC clean passes** and is staged — the gate is not merely a brake | PASS |
| **P3b** | an unclassified **clean** file defaults to PUBLIC, as documented | PASS |
| **P4** | **the sha256 of an excluded artifact is unchanged after a full run** — exclusion is never implemented by editing the thing excluded | PASS |
| **P5** | a redacted derivative is a **new path**, labelled **NON-EVIDENCE**, original untouched and still excluded | PASS |
| **P6** | the shipped seed is exactly 12 EVIDENCE-PRIVATE, all non-`.md`, and ≥163 PENDING-SCRUB | PASS |
| **P6b** | every seeded path exists — a manifest naming absent files is a stale manifest | PASS |

## 4. THE SEED — AND TWO COUNTS THAT NEEDED CORRECTING

| class | seeded | dispatch said | reconciliation |
|---|---|---|---|
| `EVIDENCE-PRIVATE` | **12** | "25 bucket-(c) files" | **25 is the OCCURRENCE count; FM 34's own table says "25 occurrences … 12 files".** The manifest classifies files. Re-measured independently here: 12, and the list matches FM 34's exactly. |
| `PENDING-SCRUB` | **216** | "163 must-scrub .md files" | **163 is FM 34's number under the push scan's three stages; this gate runs two** (§2), so it counts every `.md` still carrying a real-class hit after already-redacted lines are dropped. The extra 53 are lines the push scan *excuses*, not new secrets. |

The 12 are FM 34's bucket (c): 4 captured frontier-call result JSONs, 1 banked proof asset
(`FM15_hook_enforcement_proof.txt`), and **the 7 runnable proof scripts, whose authoritative
copies stay private** as the dispatch requires.

## 5. THE GATE'S VERDICT ON THE REAL TREE — IT REFUSES, AND THAT IS CORRECT

```
PUBLICATION REFUSED — 228 file(s) classed PRIVATE / EVIDENCE-PRIVATE / PENDING-SCRUB
are still present under docs/.
```

**This is not a regression.** FM 31's scan already aborts this push; the gate makes the reason
per-file and explicit instead of a wall of grep hits. Publication stays blocked until the scrub
dispatch runs — which is the honest state, because those files carry unscrubbed private data
today.

## 6. THE REPRODUCIBILITY-CLAIM SWEEP — REPORT ONLY, NOTHING EDITED

Scoped to the **12 excluded proofs** (the PENDING-SCRUB `.md` set is a different question):

- **57 lines** across public-surface `.md` docs reference an excluded proof **by filename**.
- **0 of them claim it is publicly reproducible, re-runnable, or verifiable by a reader.**

**So the answer to Bill's item 3 is: no such claim exists.** The related exposure, which is real
and is *not* a claim: after exclusion those 57 references become **dangling pointers in the public
mirror** — a reader follows a path that is not there. Naming it is the finding; fixing it is not
this dispatch's to do, and nothing was edited.

Representative rows (full list reproducible by re-running the sweep):

| doc | line | names |
|---|---|---|
| `DISPATCH_D21_D23__…v20260717_1240.md` | 130 | `d21_live_proof_script__v20260717_1230.py` |
| `DISPATCH_DETECTION_MISS_MEASUREMENT__…v20260717_1117.md` | 11, 135 | `detection_miss_measurement_script__v20260717_1117.py` |
| `DISPATCH_FM15_HOOK_ENFORCEMENT_ON__…v20260814_1713.md` | 105, 123 | `assets/FM15_hook_enforcement_proof.txt` |
| `DISPATCH_FM34_TRIAGE_THE_447__…v20260815_1019.md` | 118-121, 135, 144-150 | all four result JSONs, the asset, all 7 scripts |

## 7. FILED

1. **The accidental claim** (§0) — repaired, the bad commit named not rewritten.
2. **The dangling-reference exposure** (§6) — 57 public references to files that will not be in
   the mirror.
3. **`.hip-scope` was overwritten mid-dispatch by the concurrent FM 32 session** in this same
   worktree, dropping FM 35's declared prefixes; re-widened with attribution rather than
   replacing FM 32's line. **Two sessions, one worktree, one scope file that each `claim_lane.py`
   run rewrites wholesale** — the same class as TD-R-194(a) and NC 24 §8.6.

## 8. NOT PUSHED — AND THE EXPOSURE, PER PREAMBLE ITEM 8

**Bill instructed "do NOT push".** Three commits sit locally on `roadmap`:

| commit | what |
|---|---|
| `c2163d3` | the REQ |
| *(this commit)* | gate, manifest, twins, `push_docs.sh` wiring, this doc |

**THE EXPOSURE, NAMED AS THE RULE REQUIRES:** these commits are on the shared `roadmap` branch in
a worktree **another live session (FM 32) is committing to**. **Any other lane's next
`git push origin roadmap` will publish them without either lane deciding to** — the D-158 shape.
The window is open until Bill pushes or resets. `80d03c6` (the claim + repair) **was** pushed,
before the instruction applied to build output.

## 9. CLAIM IMPACT

```
CLAIM IMPACT: none
```

## 10. NEEDS BILL

1. **The default** — PUBLIC-if-clean, or flip to PRIVATE-by-default with a classification pass?
2. **The 57 dangling references** (§6) — leave, or add a public note that proofs are withheld?
3. **The push** — three local commits, exposure named in §8.
4. **The filtered-mirror follow-on** — until it lands, the gate's honest behaviour is to refuse
   rather than to filter, because `subtree split` cannot omit a present file.

---

# SCOPE ADDITION — Bill, 2026-08-15, from the adopted ruling's final text

**Appended to this dispatch's own record rather than cut as a new doc: FM 35 was still in
flight (its row was open), so this is the work continuing, not a second dispatch.**
Authority: `REQ_PUBLICATION_MANIFEST` **Amendment 1**, filed before this amendment's code.

## S1 — ABSENCE NOW READS AS A DECISION (A1.1) — BUILT

**This reversed a reasoning in the parent REQ, and the reversal was right.** The parent kept the
manifest outside `docs/` because *"a public list of which files were withheld is a signpost."*
That answered the wrong risk: a placeholder naming the **class** discloses nothing the gap itself
does not, while an unexplained gap is strictly worse — and it left the **57 dangling references**
this dispatch had already found pointing at nothing. **The manifest's placement is unchanged; the
staged mirror gained notices.**

- a placeholder at **each excluded file's own path** (`<name>.WITHHELD.md`), so a reader
  following a reference lands on the explanation instead of a 404;
- a root **`WITHHELD.md`** index listing every withheld path with its class;
- **the notice names the class and nothing else — no excerpt, and NO HASH.** A digest of a
  withheld artifact is a weak oracle against guessed contents, and hash-verifiability was scoped
  to the private repo, which is where it stays. A twin asserts the notice leaks neither the value,
  nor an excerpt, nor the digest.

## S2 — THE ESCAPE IS DETECTED, NOT ONLY PREVENTED (A1.2) — BUILT

`verify_staged()` inspects a staged tree and goes **RED** if an excluded artifact is in it.
**Prevention and detection are different properties, and only one survives a bug in the
preventer.** Checked two ways: by path, and **by content hash**, so an escape arriving under a
different filename is still caught.

## S3 — SANITIZED PUBLIC REPRODUCERS (A1.3) — NOTED, NOT BUILT

Recorded in the REQ as a future capability, deliberately not built here. When it is: a reproducer
is a new path, labelled NON-EVIDENCE, classed PUBLIC, original untouched and still
EVIDENCE-PRIVATE. **What it must not become:** a reproducer presented as the proof — the original
produced the recorded result; a derivative produces *a* result, and the two must never be cited
for each other.

## S4 — TWIN RESULTS: 16/16 GREEN (10 parent + 6 new)

| twin | proves | result |
|---|---|---|
| **A1.1** | a placeholder exists at the excluded file's own path, naming the class | PASS |
| **A1.1b** | the placeholder leaks **neither the value, nor an excerpt, nor the digest** | PASS |
| **A1.1c** | the root index lists every withheld path with its class | PASS |
| **A1.2** | an EVIDENCE-PRIVATE artifact in staging turns the build **RED** | PASS |
| **A1.2b** | the **same content under a different filename** is still caught | PASS |
| **A1.2c** | the detector does **not** flag its own notices | PASS |

## S5 — DEMONSTRATED END TO END ON THE REAL TREE

```
staged (publishable) files : 645
withheld notices written   : 230
root index present         : True
verify_staged              : PASS — 876 files checked, 228 excluded artifacts known
```

**230 notices against 228 manifest entries, and the gap is the point.** `stage()` **re-measures**
rather than trusting the seed, so two files carrying hits that the manifest cannot know about were
still excluded and still got notices:

- `docs/dispatches/DISPATCH_FM32_STAGED_DIFF_PROCESS_BATCH__…__v20260815_1239.md`
- `docs/dispatches/LATEST_DISPATCH_FM32.md`

**Both landed at 12:39, four minutes after this manifest was seeded at 12:35.** A static list is
stale on arrival in a repository this active; the manifest is authoritative for **classification**
and the detector stays authoritative for **risk**. That division is what makes the seed safe to
ship without being complete.

## S6 — THE "DO NOT PUSH" INSTRUCTION WAS OVERTAKEN, AND HERE IS THE RECORD

The parent report named the exposure of holding commits unpushed on a shared branch. **It
fired.** `c2163d3` and `031b09d` are now on `origin/roadmap`, carried by **FM 32's push at
12:41** — the D-158 shape, from a worktree two sessions were committing to. Nothing was lost and
the commits are byte-identical to what was authored; **the defect is that neither lane decided to
publish them.** The instruction was followed — this dispatch pushed nothing — and it was
overtaken anyway, which is the argument for the exposure note being mandatory rather than polite.

## S7 — PUBLISHED BY RULING, AND THE TWO KINDS OF PUBLISHING SEPARATED

**Bill's ruling, 2026-08-15: push FM 35's remaining commits.** The parent dispatch's
"do NOT push" is lifted for this work, by decision.

**The record distinguishes two things that both put commits on `origin/roadmap`, because they
are not the same event and a later reader must not have to guess which happened:**

| commits | how they were published | decided by |
|---|---|---|
| `c2163d3`, `031b09d` | **carried, undirected** — swept along by **FM 32's push at 12:41** while they sat unpushed on the shared branch | **nobody.** Neither lane chose it. The D-158 shape. |
| `b81d7bc`, `5b347e0`, and this annotation | **pushed deliberately** | **Bill's ruling** |

**Why the distinction is worth a table rather than a sentence:** the first row is exactly the
failure STANDARD PREAMBLE item 8 exists to prevent, and it happened *to this dispatch* while the
dispatch was obeying an instruction not to push. "No harm done" is not the test — nothing was
lost, the commits were byte-identical to what was authored, and it is still a defect, because the
question the rule asks is **who decided**. For the second row the answer is a name; for the first
it is nobody.

**Status header amended accordingly:** this dispatch is no longer "committed, deliberately not
pushed" — it is **published, by ruling**, with the earlier accidental publication recorded rather
than absorbed.
