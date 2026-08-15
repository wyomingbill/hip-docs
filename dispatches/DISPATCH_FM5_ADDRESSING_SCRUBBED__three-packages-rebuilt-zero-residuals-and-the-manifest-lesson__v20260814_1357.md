# FM 5 — REBUILD THE THREE REVIEW PACKAGES WITH ADDRESSING SCRUBBED
Status: BUILT — **LANDED**
Reconciled-Against: 2026-08-14. Packages pinned at `hip-cutover-demo 7904c36`,
`hip-roadmap d9e2010`, `hip-vo 65c263e` — unchanged from FM 3. Board claim `cae959a`.

REQ: **NONE.** Repackaging and verification; no product code changed. Requirements
Discipline item 10 allows an ANALYSIS/MEASUREMENT dispatch to carry REQ: NONE if it says
why. This says why.

---

## 0. THE EXCEPTION LINE

```
FM 5 — REBUILD THE THREE REVIEW PACKAGES WITH ADDRESSING SCRUBBED
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

**NEEDS BILL: upload when ready.** Nothing is outstanding for a decision; the three paths
are in §4.

---

## 1. THE LESSON THIS DISPATCH IS ORDERED TO RECORD PROMINENTLY

> ## **FM 3's FINDING FM3-2 WAS FALSE. NO CREDENTIAL WAS EVER EXPOSED.**
>
> ## **THE RULE: MEASURE THE CLAIM AGAINST THE ARTIFACT, NEVER AGAINST ITS MANIFEST.**

**What FM 3 claimed (FM3-2, 2026-08-14):**

> *"Package 1 shipped credential and runtime files that package 3 excluded — 14 named,
> including `hip-roadmap/.env.dev` and `certs/voice.key`."*

**What was actually true.** `MANIFEST_REDACTED.txt` inside
`HIP_CODE_REVIEW_REDACTED_20260813.zip` prints a section headed *"Credential/runtime files
excluded (14)"*. **That is that package's own EXCLUSION list** — the files it walked past
in the LIVE TREES and deliberately did not package. FM 3 read it as an inventory of what a
*different* package contained, and produced a shipped-credentials finding out of a list of
not-shipped credentials.

**The mechanics of the error, stated plainly because the shape recurs.** An exclusion list
and an inventory are **the same shape** — a heading, then a list of paths, then sizes. They
carry opposite meaning, and the meaning lives entirely in the heading. FM 3 had the zip on
disk the whole time and reasoned from a *description of* the artifact instead of the
artifact. The check that settles it is one command:

```
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.env"                ->  2   (both .env.dev.example)
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.key$"               ->  0
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.db($|-wal$|-shm$)"  ->  0
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.pem$"               ->  0
```

**What FM 4 measured instead** (4,921 text files across all three 08-13 packages): no
`.env`/`.env.dev`/`.env.demo`, no `*.key`/`*.pem`/`*.p12`, no `*.db*`, no `*.npz`
voiceprints, no PEM private-key material, no provider API-key literal. Only
`.env.dev.example` — a git-tracked template whose one value is
`HIP_FRONTIER_CODEWORD=CHANGE_ME` — and `certs/voice.crt`, **the public certificate half**;
`voice.key` is absent. Every `NEO4J_PASSWORD`/`api_key`/`password=` hit is source code
reading `os.environ`. Every 64-hex string is a `script_sha256` or a ledger `head_hash`.

**Why this stays on the record rather than being quietly dropped (Bill's ruling).** The
error was cheap only because the next dispatch enumerated before acting. Had FM 4 followed
its own instruction and rotated first, the cost would have been two in-flight lanes
interrupted, a set of provider rotations Bill did not owe, and a false exposure event
cited as fact by everything downstream. **The habit that saved it — enumerate the artifact,
then act — is the thing worth keeping, and it only reads as a habit if the failure it
caught stays visible next to it.**

**The rule already existed one level down.** The redaction work has always verified against
the *delivered artifact*, never the staging copy. FM 3 followed that faithfully for
redaction and abandoned it for provenance in the same document. **The rule is not
"check redactions against the artifact" — it is "check claims against the artifact."**

**This dispatch was subject to the same rule and it caught this dispatch too.** §3.3: the
first scrub pass verified clean in staging and **failed against the delivered zip.**

---

## 2. THE RULING, AND WHAT "THE EXISTING MECHANISM" TURNS OUT TO BE

**Bill's ruling, 2026-08-14:** scrub the tailnet addresses, the `*.[REDACTED-TAILNET-DOMAIN]` hostname and the
LAN address from all three packages **using the existing project scrub mechanism —
`scripts/push_docs.sh`'s rules — not a parallel redaction scheme.** Keep the three-way
split; each package keeps its distinct review purpose.

**Read literally, that instruction has a wrinkle worth naming: `push_docs.sh` cannot
scrub.** It is a **detector**. It greps `docs/` before a public mirror push and *aborts* on
any hit; it has never substituted a character. So "its rules" resolves to the two things it
does own, and both are reused verbatim:

| what was reused | where it comes from |
|---|---|
| **the definition of sensitive** | `push_docs.sh`'s own scan alternatives — `100\.72\.236` and `ts\.net` |
| **the replacement convention** | the `[REDACTED-*]` token, which that scan already honours via `grep -v "\[REDACTED"`, and which the 2026-08-13 home-address redaction already used |

**One addition beyond the script, recorded as an addition rather than folded in silently:**
the **LAN address is not in `push_docs.sh`'s pattern.** Bill's ruling names it explicitly,
so it is scrubbed — but a later reader should know it came from the ruling, not from the
script. The script's coverage was not retroactively overstated to make the two agree.

**A second limit, stated so the mechanism's authority is not overclaimed:** the rest of
`push_docs.sh`'s pattern (`password`, `secret`, `api[_-]?key`, `token`, `NEO4J`, `bearer`)
is tuned for `docs/` and **fires on ordinary source code by design** —
`NEO4J_PASSWORD = os.environ.get(...)` is a match and is not a secret. Running the full
pattern over `source/` would produce noise, not a verdict. **Only the addressing half is a
meaningful gate for a source package**, and that is the half applied and verified.

---

## 3. THE SCRUB

### 3.1 Values enumerated from the packages, not assumed

Before substituting anything, the staged trees were scanned for every distinct matching
token. **Three values, and no others:**

| class | distinct values found |
|---|---|
| tailnet address | **1** (`100.72.236.x`, one host) |
| tailnet hostname | **1** — and note it embeds both the machine name and the tailnet name |
| LAN address | **1** — the same value that is the CN of the self-signed voice certificate |

**No certificate or key file is inside any of the three packages** (checked: zero `*.crt`,
`*.pem`, `*.key`), so there is no base64-embedded CN that text substitution would miss.
That mattered: had `voice.crt` been bundled, scrubbing the prose would have left the same
value readable inside the DER.

### 3.2 Substitutions per package

| package | tailnet address | tailnet host | tailnet domain | LAN address | **total** | files |
|---|---|---|---|---|---|---|
| `demo-cutover_7904c36` | 6 | 1 | 1 | 2 | **10** | 9 |
| `advisor-roadmap_d9e2010` | 7 | 1 | 1 | 2 | **11** | 10 |
| `governed-voice_65c263e` | 5 | 1 | 1 | 2 | **9** | 8 |

The address / host / LAN counts reconcile exactly with FM 4's independent measurement of
the unscrubbed packages (6+1+2, 7+1+2, 5+1+2). **The `tailnet domain` column is the fourth
rule, added mid-dispatch — see §3.3.**

**FM 3's staged trees were copied, not modified.** The pinned content behind `7904c36`,
`d9e2010` and `65c263e` is intact on disk, so the scrubbed builds are provably the same
content plus token substitutions.

**No tenth document was added.** The scrub is recorded as a new section inside each
package's existing `REDACTION.md`, which is where that package already documents what was
changed in the copy — keeping the standard nine exactly nine.

### 3.3 THE FIRST BUILD FAILED VERIFICATION, AND THIS IS WHY THE CHECK IS WHERE IT IS

The first pass verified clean in staging and **failed against the delivered zip, on two
distinct causes:**

1. **This dispatch's own new `REDACTION.md` section quoted the patterns literally** while
   certifying they were absent — the document asserting "zero occurrences" contained the
   strings. **The 2026-08-13 manifest made exactly this mistake with the home address and
   its own extraction check caught it**; the note recording that was in the very file being
   extended, and the mistake was repeated anyway. Fixed by describing the patterns instead
   of quoting them.
2. **`KNOWN_ISSUES.md` carried a bare domain-suffix mention** with no hostname attached
   (`.[REDACTED-TAILNET-DOMAIN] URL reachable`). The hostname rule did not cover it — but `push_docs.sh`'s
   rule is the bare string `ts\.net`, so under the ruling's own mechanism it is a hit and
   would abort a docs push. A **fourth rule** was added and the packages rebuilt.

**Neither would have been caught by checking the staging copy**, which is the entire reason
the verification runs against the delivered artifact. Recorded rather than silently fixed,
because §1's rule earned its keep twice in one day.

---

## 4. VERIFICATION — AGAINST THE DELIVERED ZIPS

Each finished archive was extracted to a clean directory and re-scanned. **Not the staging
copies.**

| check | demo-cutover | advisor-roadmap | governed-voice |
|---|---|---|---|
| files extracted | 343 | 413 | 297 |
| tailnet prefix (`push_docs.sh` rule 1) | **0** | **0** | **0** |
| tailnet domain (`push_docs.sh` rule 2) | **0** | **0** | **0** |
| LAN range (Bill's ruling) | **0** | **0** | **0** |
| home address (the 08-13 class) | **0** | **0** | **0** |
| PEM private-key material | **0** | **0** | **0** |
| provider key literal | **0** | **0** | **0** |
| the nine standard documents | **ALL 9** | **ALL 9** | **ALL 9** |
| `REVIEW_REQUEST.md` cited paths unresolved | **0** | **0** | **0** |
| header names its own zip | ✅ | ✅ | ✅ |
| cold-start sections (role / findings format / verdict / TOP 3 / ground rules) | **ALL** | **ALL** | **ALL** |

**Total residual occurrences across all three delivered zips, all six patterns: ZERO.**

`REVIEW_REQUEST.md` remains self-contained and executable cold: every file path it cites
resolves inside its own package, its header names the package now being sent, and the five
sections a zero-context reviewer needs are all present. **The three-way split is kept and
each package keeps its distinct review purpose** — demo governance and on-screen
truthfulness; erasure, transcripts and the record; a spoken turn as the same governed turn.

### THE THREE UPLOAD PATHS

```
[REDACTED-USER-PATH]/Desktop/HIP_REVIEW_20260814/HIP_REVIEW_demo-cutover_7904c36_SCRUBBED.zip      2.1 MB
[REDACTED-USER-PATH]/Desktop/HIP_REVIEW_20260814/HIP_REVIEW_advisor-roadmap_d9e2010_SCRUBBED.zip   2.8 MB
[REDACTED-USER-PATH]/Desktop/HIP_REVIEW_20260814/HIP_REVIEW_governed-voice_65c263e_SCRUBBED.zip    1.7 MB
```

**Those three files are now the only contents of that folder**, so there is nothing to
pick wrong.

---

## 5. QUARANTINE — SEGMENT 4

The three **unscrubbed** FM 3 zips were moved to `~/Desktop/REVIEW_STALE_QUARANTINE/`,
beside the 08-13 set. **Nothing deleted.**

| file | SHA-256, taken BEFORE the move |
|---|---|
| `HIP_REVIEW_demo-cutover_7904c36.zip` | `2a9eb2ad129f99b3a8bc4c7262009ba8a153a5373e084a4bc7819a0cbab08a52` |
| `HIP_REVIEW_advisor-roadmap_d9e2010.zip` | `fd1e0cd61cda8d34c7a9019dbab1d31459a2aa2dfd49189078df74a367c5dc51` |
| `HIP_REVIEW_governed-voice_65c263e.zip` | `25606eb444722ad8db3bb0fae1089131806a89a60d983ef534e7840ba368328b` |

`SHA256SUMS.txt` now carries all six quarantined files. **`README.txt` was rewritten** to
cover both generations, to state that the sendable packages are elsewhere, and to carry
§1's correction and rule in full — so the folder reads correctly to someone who never sees
this dispatch. **None of the FM 3 packages was ever sent**, so superseding them costs
nothing: they are the same pinned content, differing only by the substituted tokens and the
added `REDACTION.md` section.

---

## 6. FILED, NOT BLOCKING (2)

**(FM5-1) `push_docs.sh` detects but cannot remediate, and nothing in the project can.**
Every redaction to date — the 08-13 home address, this addressing scrub — has been written
fresh by whichever dispatch needed it. The detector and the substituter are separate,
uncoordinated, and only the detector is in the repo. **The obvious answer is a
`scripts/scrub.py` that shares one pattern table with `push_docs.sh`, so a class added to
the detector is automatically removable and the two cannot drift.** Named as the known
answer; **deliberately not built here** — that is a build with a REQ, not a repackaging
task, and the finiteness rule says a finding does not automatically become the next task.

**(FM5-2) FM 5's closing push carried NC 6's `cbb769b` as a passenger.** It sat
committed-but-unpushed on `roadmap` when FM 5 closed. **The sixth instance in two days** —
VD-58, FM 1's FINDING 10, VD-59-2, FM 3's FM3-4 (two), and now this. Harmless in substance
every time; decided by no lane every time. At six occurrences this is no longer an incident
but a **property of the topology** — one commit graph, many worktrees, board rows committed
locally and published by whoever pushes next. Recorded, not corrected.

---

## 7. WHAT THIS DISPATCH DID NOT DO

- **Changed no pinned content.** Same three commits as FM 3; the staged trees were copied
  before substitution and remain intact.
- **Ran no test, suite, battery or gate.** VD-61 owns the heavy slot. Each package's
  `TEST_RESULTS.md` is unchanged from FM 3 and still reuses recorded runs only.
- **Did not merge, split, or re-scope the packages.** Three-way split kept per the ruling.
- **Did not add a tenth document.** The scrub extends each package's existing
  `REDACTION.md`.
- **Deleted nothing**, including the superseded zips of both generations.
- **Did not rotate any credential or touch any service** — FM 4 established there is
  nothing to rotate, and nothing here reopens that.
- **Did not build the shared scrub tool** named in FM5-1.

---

## 8. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Repackaging and verification; no evidence bearing on a ledger claim was produced or moved.

---

## 9. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- Board: **FM 5 claimed at `cae959a`** (first commit of the dispatch), closed by this
  dispatch's own commit.
- Every commit taken under `scripts/hip_lock.py with repo`; explicit pathspecs only.
- The scrub was applied to **copies**; FM 3's staged trees are unmodified on disk.
- Verification ran against the **delivered zips**, and its first pass **failed** — §3.3.
