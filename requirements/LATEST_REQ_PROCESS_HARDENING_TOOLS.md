# REQ_PROCESS_HARDENING_TOOLS
Status: PLAN
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap` @ `8779b68` (FM 9 claim)

Filed by FM 9 **before the first code edit**, per Bill's ruling 1. Supersedes nothing.
Authority for the four tool designs: FM 6 §3
(`docs/dispatches/DISPATCH_FM6_PROCESS_HARDENING__stopped-at-the-req-gate-four-tools-specified-from-measured-evidence__v20260814_1408.md`),
lifted intact.

---

## THE REQUIREMENT

Bill's own words, 2026-08-14, verbatim:

> **1. FILE THE REQ. No exception phrase. Hardening obeys the gate it strengthens. FM 6 §3
> lifts in intact. File it BEFORE the first code edit, Status PLAN.**
>
> **2. claim_lane.py REFUSES the push when it would carry a passenger. Not report-only. A
> neighbour's unpushed work blocking a lane is the accepted cost.**
>
> **3. Provision the two bare lanes FIRST (~/hip-dev, ~/hip-cutover-demo), THEN
> lane_preflight.py refuses any unprovisioned lane.**
>
> **4. All four tools are repo-versioned centrally and enforced across every active worktree.
> Not per-worktree hooks.**

And, from the same dispatch:

> **Build all four: claim_lane.py, register_doc.py, lane_preflight.py, scrub.py. Each gets its
> pass/fail twin proven BOTH directions. STOP and report before anything destructive.**

**Expanded:** four executable tools under `scripts/`, each closing a gap that is already on the
record as a real incident rather than a hypothesis. Ruling 1 settles the meta-question FM 6
stopped on — the gate binds the hardening work too. Ruling 2 chooses strictness over
availability. Ruling 3 orders provisioning before enforcement so the preflight's refusal is
never a false positive on a lane nobody has set up. Ruling 4 rejects the per-worktree hook
pattern that `scripts/staging_guard.sh` currently uses and which its own header names as a limit.

---

## THE ACCEPTANCE TEST

**Eight observations. Each tool is proven in BOTH directions — a green case that must pass and a
red case that must fail — because a gate never exercised in the red is not known to be a gate.**

### A. `scripts/claim_lane.py`

- **A1 GREEN — two concurrent claims both land.** Two processes claim different lanes in a
  throwaway repository at the same time. **PASS iff** both rows are present in the final
  `docs/LANES.md`, neither row was swept, each commit contains **exactly one path**
  (`docs/LANES.md`), and the second process blocked on the `repo` lock rather than racing.
- **A2 RED — a passenger refuses the push.** A commit belonging to another lane sits
  committed-but-unpushed on the branch. **PASS iff** `claim_lane.py` exits **non-zero without
  pushing**, names the passenger commit by hash, and leaves the local claim commit intact.

### B. `scripts/register_doc.py`

- **B1 GREEN — a row lands in its own section.** Register a row under `## dispatches/`. **PASS
  iff** the row is the **first** row under that section's own separator, no other section's table
  is modified, and the file's other 12 tables are byte-identical.
- **B2 RED — a staled anchor aborts.** The section header is mutated between locate and write.
  **PASS iff** the tool exits **non-zero**, prints the reason to stderr, and leaves the file
  **byte-identical** — no partial write, no fallback to a nearby table.

### C. `scripts/lane_preflight.py`

- **C1 GREEN — an agreeing lane passes.** In a provisioned lane whose `.hip-owns`, `.hip-graph`
  and operative `.env.dev` pin all name the same port. **PASS iff** exit 0 and every source is
  printed with the value it contributed.
- **C2 RED — the NC 5 inherited-declaration shape refuses.** A checkout whose `.hip-owns` /
  `.hip-graph` name another lane's port, and separately a checkout whose declarations agree but
  whose `.env.dev` points elsewhere. **PASS iff** both exit **non-zero** and name **which two
  sources disagree and what each says**. An unprovisioned lane must also refuse (ruling 3).

### D. `scripts/scrub.py`

- **D1 GREEN — a planted address is scrubbed and verified zero-residual.** **PASS iff** the
  planted value is replaced with the project's `[REDACTED-*]` token and the zero-residual check
  is made **against the written file**, not an in-memory copy.
- **D2 RED — the FM 5 regression is caught.** A document that *quotes* a pattern while certifying
  it absent. **PASS iff** the verification goes **red**.

### E. Ruling 4 — central enforcement

- **E1.** The enforcement path is proven to fire **from a worktree other than `~/hip-roadmap`**,
  without that worktree carrying its own hook. **PASS iff** the same control is demonstrably
  active in a second worktree.

**"Done" is these nine observations recorded with their actual output. An error going away is
not done.**

---

## WHAT'S ALREADY DONE — DO NOT REBUILD

| piece | how it was verified |
|---|---|
| **`scripts/hip_lock.py`** — kernel-enforced `flock`, exit 75 on refusal, exports `HIP_LOCK_HELD` for tooling underneath to verify the lock rather than trust it | in continuous use; `who` verified `free` for all seven resources during FM 4 |
| **`scripts/staging_guard.sh`** — refuses a shared board file staged alongside other paths without the `repo` lock; exit 76 | FM 2 twin, 6/6 logic cases plus a live red/green on its own closing commit |
| **`scripts/push_docs.sh`** secret-scan pattern — the **detection** half of the scrub | read in full, FM 5 §2 |
| **The `[REDACTED-*]` convention** — already honoured by `push_docs.sh`'s own `grep -v` | used by the 2026-08-13 home-address redaction and by FM 5 |
| **`harness/lane_ownership.py`, `harness/graph_target.py`** | present in 2 of 5 and 3 of 5 worktrees respectively (FM 6 §2) |

**`claim_lane.py` must build on `hip_lock.py` and cooperate with `staging_guard.sh`, not
duplicate or replace either.** `scrub.py` must consume `push_docs.sh`'s pattern rather than
restate it — that shared table is the point of the tool.

---

## WHAT'S KNOWN BROKEN

**Each of the four is a measured incident, not a worry.**

1. **Board sweeps and passenger publication.** `git add docs/LANES.md` stages the whole file
   including another lane's in-progress edits: HA-78's `71601fc` swallowed FM 1's uncommitted
   row. Separately, **six passenger-commit incidents in two days** (VD-58, FM 1 FINDING 10,
   VD-59-2, FM 3's FM3-4 ×2, FM 5's FM5-2). `staging_guard.sh` names the residual hole in its own
   final paragraph: *"The lock stops the collision; only surgical staging stops you committing
   another lane's rows."*
2. **INDEX anchor ambiguity.** `docs/INDEX.md` carries **13 identical table headers, 16 identical
   separator rows, 15 category sections** — in both trees. The header text is not a unique
   anchor. TD-R-164 found **54 dispatch rows** filed into `requirements/`'s table, spanning D-90
   through D-162.
3. **Inherited lane declarations.** `~/hip-nc/.hip-graph` records it in its own words: the
   `natural-conversation` branch was cut from a commit carrying `~/hip-vo`'s lane files, so the
   checkout **inherited another lane's pin and declared a graph it did not own**. Nothing was
   written through it **only because `~/hip-nc` had no `.env.dev`** and every run failed closed at
   the password guard — **an unrelated fail-closed saved it, not the ownership machinery.**
   Compounding: `~/hip-vo/.hip-graph` states it is *"RECORD, NOT ENFORCEMENT … the operative pin
   is `.env.dev`"*, so the two **can disagree and only one decides**. And `~/.env.dev` pins
   **7689 — the frozen demo — live on this machine**, with `override=True`.
4. **Detector without a scrubber.** `push_docs.sh` greps and aborts; it has never substituted a
   character. Every redaction to date was written fresh by whichever dispatch needed it. **They
   had already drifted within a single dispatch**: FM 5's first build missed a bare domain suffix
   that `push_docs.sh`'s own pattern catches.
5. **Per-worktree hooks do not distribute.** `staging_guard.sh`'s header: *"hooks are
   per-worktree and are NOT version controlled. This protects `~/hip-roadmap` only."* Five
   worktrees share one git dir; four have no guard.

---

## CONSTRAINTS — WHAT MUST NOT REGRESS

- **No product runtime code.** `harness/`, `server/`, `truth_layer/`, `memory_engine/` are out of
  scope. This is `scripts/` and lane declaration files only.
- **No graph writes, no demo runs, no heavy suites.** VD-61 owns the heavy-test slot.
- **`~/hip-dev` is the FROZEN DEMO and is the fallback, not a lane.** Ruling 3 authorises
  provisioning it — **that authorisation extends to adding declaration files and nothing else.**
  No code change, no graph touch, no service restart in that tree.
- **`hip_lock.py` and `staging_guard.sh` keep working exactly as they do now.** A new tool that
  makes either weaker is a net loss regardless of what else it achieves.
- **No lane's in-flight work is disturbed.** Other lanes are live; nothing here may restart a
  service or take a long lock. Item 9 holds: the lock wraps the git operation only.
- **Exit codes are not answers.** Requirements Discipline item 13 — three false all-clears
  (D-70, D-75, D-88) came from `grep -c` exiting non-zero on a legitimate zero. Every
  verification step in these tools and their twins runs **unchained**.
- **STOP and report before anything destructive** (Bill's instruction, same dispatch). Nothing in
  this REQ's scope should be destructive; if that turns out to be false, the dispatch stops.

---

## OPEN — NOT DECIDED BY THIS REQ

**Ruling 4's mechanism is not specified by Bill, only its outcome** ("repo-versioned centrally,
enforced across every active worktree, not per-worktree hooks"). The available mechanisms differ
in blast radius — a shared `core.hooksPath` in the common git dir reaches every worktree at once
and therefore changes every lane's commit behaviour in one step. **The implementing dispatch must
state which mechanism it used and what it now affects**, and must not widen enforcement beyond
what it can demonstrate.

---

# AMENDMENT 1 — MID-RUN DETECTION (FM 14, 2026-08-14)

**AMENDED, NOT REPLACED.** Everything above stands exactly as filed; this section adds one
capability to `lane_preflight.py` and one pair of acceptance observations. Bill's instruction:
*"REQ: amend REQ_PROCESS_HARDENING_TOOLS, don't file new."*

## THE REQUIREMENT — Bill's words, 2026-08-14, verbatim

> **FM 12 proved "all locks free" ≠ "nothing running": the battery held a live bolt socket to
> 7690 and no lock. Build the process scan into lane_preflight.py: detect live
> battery/dispatch processes and ESTABLISHED bolt connections per graph port, report WHAT is
> running WHERE, and give FM 12's precondition a real check to call. Twins both directions
> (live process detected = refuse; clean machine = pass).**

**Expanded:** the gap is not that `hip_lock.py` is wrong — it locks what a caller asks it to
lock, and a battery never asks. The gap is that **no instrument answers "is anything running"**,
so every dispatch that needs that answer hand-rolls a `ps` pipeline, and FM 12 is the proof that
reading the lock table instead returns a confident false all-clear.

## THE ACCEPTANCE TEST — two more observations, both directions

### F. `lane_preflight.py --busy` (and the same scan inside the default check)

- **F1 GREEN — a clean machine passes.** With no matching process and no ESTABLISHED
  connection on the scanned ports. **PASS iff** exit 0 and the report states, positively, what
  was scanned — patterns and ports — rather than printing nothing.
- **F2 RED — a live process is detected and refused.** A process whose command line matches a
  work pattern, and separately an ESTABLISHED TCP connection on a scanned port. **PASS iff**
  both exit non-zero, and the output names **WHAT** (pid, elapsed, the matched command) and
  **WHERE** (the tree or the port). A refusal that says only "something is running" fails this.

**Both cases must be provable without depending on what happens to be running on the machine at
the time** — the twin creates its own subject and scans its own port, or it is measuring the
weather rather than the tool.

## WHAT'S KNOWN BROKEN — the incident this amendment is made of

**FM 12, 2026-08-14.** Every one of the seven lock resources reported `free` while
`scripts/demo_integrity_battery.py` (PID 2827) ran a 20-iteration canonical battery in
`~/hip-cutover-demo` against `bolt://localhost:7690`, holding an ESTABLISHED socket. A
precondition answered from the lock table alone would have returned "all clear" and been wrong,
and the flip it guarded would have landed on top of a live evidence run.

## CONSTRAINTS — added by this amendment

- **Read-only.** The scan may not signal, stop, or otherwise touch any process it finds.
- **No new dependency.** `ps` and `lsof` are already relied on across this project's scripts.
- **A scan that cannot run is not a pass.** If `ps` or `lsof` fails, that is an explicit
  UNKNOWN and a non-zero exit, never a silent green — the same fail-closed rule
  `push_docs.sh` now follows for its pattern.

# AMENDMENT 2 — THE SCRUBBER FAILS CLOSED (FM 28, 2026-08-15)

## THE REQUIREMENT — Bill's words, FM 28, verbatim

> Bill's ruling: the scrub tool must not report "clean" against an empty local PII policy;
> round 3 was hand-verified and has SHIPPED — this is the tooling fix behind it.
>
> 1. Create ~/.hip-scrub-local (0600): the machine-local PII class — the household address
>    forms NC 27 enumerated by hand, tailnet hostnames/domains, LAN identifiers, user-
>    specific paths. Values enumerated from the two shipped packages' redaction records,
>    never invented.
> 2. FAIL CLOSED: the scrub tool REFUSES to certify a package when .hip-scrub-local is
>    missing or empty — "clean" against no policy becomes an error, not a pass. Twin both
>    directions: file absent -> refuse; file present -> the NC 27 address forms are caught.
> 3. Record Bill's redaction policy in the tool's doc verbatim: city-only and zoning-
>    district references STAY (test semantics needed for review); actual private-network
>    identifiers, hostnames, credentials, precise private addresses, machine/user-specific
>    material are scrubbed.

This resolves NC 27 §4.2 (`.hip-scrub-local` does not exist — the tool's PII class is
empty; *"the current behaviour, a silent zero-pattern pass, is the dangerous one"*) by
taking BOTH halves of the direction NC 27 referred: the file is created AND the tool
refuses without it. It also rules NC 27 §5's referral: city-only and zoning-district
references stay.

## THE ACCEPTANCE TEST — twins both directions

- **F1 RED — policy ABSENT refuses.** With the local policy unresolvable (explicit
  `$HIP_SCRUB_LOCAL` pointing at a missing file, or no file at any resolution path),
  `scrub.py --check` and `--scrub` EXIT with a dedicated non-zero code and a message
  naming the paths consulted. **PASS iff** neither mode prints a clean verdict.
- **F1b RED — policy EMPTY refuses.** A present file with zero usable entries (blank /
  comments-only / malformed lines) refuses identically. An unreadable-but-present file is
  the same refusal, never a silent skip.
- **F2 GREEN — policy PRESENT certifies and catches.** With a policy present, the
  mechanism substitutes its entries and verifies zero-residual (hermetic twin with a
  fixture entry), and — live, on this machine — the NC 27 household-address forms are
  caught by the real `~/.hip-scrub-local` (verified in the FM 28 dispatch; values never
  quoted in tracked files).
- **D1/D2/D3 UNCHANGED** — the existing acceptance stands; the self-test provides the
  fixture policy explicitly so those observations still bind.

## CONSTRAINTS — added by this amendment

- **No personal value enters git**, exactly as the table's own design note requires: the
  policy file lives at `~/.hip-scrub-local` (0600), outside every checkout; tracked files
  reference classes and counts only.
- **Resolution order is explicit and documented:** `$HIP_SCRUB_LOCAL`, else
  `~/.hip-scrub-local`, else the legacy `<repo>/.hip-scrub-local` — first file that
  exists; refusal names the chain.
- `--emit-detect-pattern` (push_docs.sh's detector feed) is NOT widened by this
  amendment; whether the mirror-push detector should also fail closed on an empty local
  policy is named in the FM 28 dispatch as a residual for a separate ruling.

# AMENDMENT 3 — `--emit-detect-pattern` FAILS CLOSED (FM 29, 2026-08-15)

## THE REQUIREMENT — Bill's words, FM 29, verbatim

> Bill's ruling verbatim: if the local scrub policy is absent or contains no effective
> patterns, --emit-detect-pattern refuses with exit 8 and identifies the paths consulted.
> Existing behavior with a valid policy remains BYTE-FOR-BYTE compatible for consumers
> such as push_docs.sh. Do NOT reopen FM 28; do NOT alter the city/zoning policy.

This closes the residual Amendment 2 deliberately left open (its constraints named
emit-mode as "NOT widened by this amendment; … a residual for a separate ruling"). The
ruling arrived; the scope is exactly that residual and nothing more.

## THE ACCEPTANCE TEST — twins plus two proofs

- **E1 RED — policy ABSENT refuses.** `--emit-detect-pattern` exits **8**, stderr names
  every path consulted, **stdout is EMPTY** (a consumer capturing stdout must never
  receive a partial pattern).
- **E1b RED — policy EMPTY (comments-only / no effective patterns) refuses** identically.
- **E2 GREEN — valid policy emits, structurally verified.** Exit 0, and the emitted
  alternation equals the expectation constructed in-process from the same table — the
  equality that makes byte-compat structural, not incidental.
- **BYTE-COMPAT PROOF (one-time, recorded in the FM 29 dispatch):** the pre-change output
  was captured for BOTH scopes with the real policy present, hashed, and diffed against
  the post-change output — byte-identical or the dispatch stops.
- **CONSUMER TEST (push_docs.sh, both directions):** against the refusing state the
  UNMODIFIED script aborts in its scan phase with its own visible
  "SECRET SCAN UNAVAILABLE … Refusing to push." and publishes nothing; against the valid
  policy its scan phase runs to "Secret scan: clean." on the byte-identical pattern. The
  valid-direction run STOPS BEFORE the subtree split/push — publishing the public mirror
  is not licensed by this dispatch — and the truncation is stated, not hidden.

## CONSTRAINTS — added by this amendment

- FM 28's refusal predicate is REUSED (`require_local_policy()`), not duplicated — one
  policy gate, three modes; FM 28 is not reopened and the city/zoning policy is untouched.
- The refusal goes to stderr only; stdout stays empty on refusal in every mode.

---

# AMENDMENT 4 — THE PUSH SCRIPT'S SCAN FAILS CLOSED (FM 31, 2026-08-15)

Status: IN_PROGRESS
Owner debt: **TD-R-197** (SEC), filed by FM 29 — *"the public-mirror scan verdict is FALSE
whenever there are hits"*. Filing was pre-authorized (tool infrastructure); **FIXING needs a
REQ, which is this amendment**, and it is written **before the first code edit**.

## THE REQUIREMENT — Bill's words, FM 31, verbatim

> 1. Fix the exclusion filter so it cannot die on its own pattern (the newline-separated
>    branches ending in `|`), and REMOVE the error-swallowing: a scan-stage failure is a
>    refusal to push, never an empty HITS.
> 2. Fail-closed contract for the whole scan: any stage erroring -> visible refusal, exit
>    nonzero, nothing published. Twins: the reproduced broken-pattern case -> refuses; a
>    planted secret in `docs/` -> caught and refuses; clean `docs/` -> passes; the FM 29
>    absent-policy case still refuses.
> 3. RETROSPECTIVE, read-only: enumerate what past mirror pushes published while the scan was
>    broken — run the FIXED scan against the mirror's current published set and report hits
>    (values never in output, classes + counts only). If any real secret is live on the
>    mirror, STOP and flag for Bill before anything else.

## ⚠ IT CORRECTS AMENDMENT 3'S OWN CONSUMER TEST — stated, not silently absorbed

Amendment 3's CONSUMER TEST records that against a valid policy `push_docs.sh`'s *"scan phase
runs to `Secret scan: clean.`"* and treats that as the GREEN direction. **That green was the
defect.** The scan reached "clean" because its third stage had already died; FM 29's test read
the verdict line, which is exactly what TD-R-197 says is false.

**FM 29's amendment is not wrong about what it tested** — it tested that the *pattern emitter*
fails closed, and it does. It is narrower than its green direction reads, and the narrowing is
recorded here rather than left for a later reader to discover the same way FM 29 did.

## THE ACCEPTANCE TEST

### F1 — THE EXCLUSION PATTERN CANNOT DIE ON ITSELF
The exclusion list is expressed so that **no branch can become an empty alternative**: either a
single line with no embedded newline, or one `-e` per branch. **PASS/FAIL:** the reproduced
pre-fix invocation exits **2** with `grep: empty (sub)expression`; the repaired one exits 0 or 1
and never 2, on the same input.

### F2 — NO STAGE'S FAILURE IS SWALLOWED
`|| true` is gone. Every stage's exit code is read and classified: **0 = matched, 1 = no match,
anything else = THE SCAN FAILED**. **PASS/FAIL:** a stage forced to exit 2 produces a refusal,
not an empty `HITS`.

### F3 — FAIL-CLOSED FOR THE WHOLE SCAN
Any stage erroring produces a **visible refusal on stderr**, a **nonzero exit**, and
**nothing published** — no subtree split, no push. **PASS/FAIL:** in the induced-failure twin the
process exits nonzero and the split/push commands are never reached.

### F4 — THE FOUR TWINS, BOTH DIRECTIONS
| twin | expected |
|---|---|
| **T1** the reproduced broken-pattern case | **REFUSES** |
| **T2** a planted secret in `docs/` | **CAUGHT — refuses** |
| **T3** clean `docs/` | **PASSES** |
| **T4** the FM 29 absent-policy case | **still REFUSES**, unchanged |

**T3 is the anti-vacuity row and is not optional:** a scan that refuses everything would pass
T1, T2 and T4 and make the mirror unpublishable. **T2 is the row TD-R-197 exists for** — before
this amendment a planted secret in `docs/` was reported clean.

### F5 — THE RETROSPECTIVE, READ-ONLY
The FIXED scan is run against the **mirror's CURRENT published set**, and the report states
**classes and counts only**. **NO MATCHED VALUE, AND NO LINE CONTAINING ONE, MAY APPEAR IN ANY
OUTPUT, ARTIFACT OR COMMIT MESSAGE** — a retrospective that prints the secret it found has
republished it into the private repo's own history.
**If any real secret is live on the mirror: STOP. Flag for Bill before anything else.**

## CONSTRAINTS — WHAT MUST NOT REGRESS

1. **The one-table discipline holds.** The detect pattern still comes from
   `scripts/scrub.py --emit-detect-pattern` (FM 9); this amendment does not reopen the table,
   the vocabulary, or FM 28's city/zoning policy.
2. **FM 29's refusal is untouched** — T4 proves the absent-policy path still refuses with its own
   message.
3. **The exclusion list's MEANING is preserved.** Re-expressing the pattern must not silently
   drop or widen a branch: the repaired list carries the same branches, and a change to what is
   excluded is a separate ruling.
4. **Nothing is published by this dispatch.** The twins stop before the subtree split, exactly as
   Amendment 3's consumer test did, and the truncation is stated rather than hidden.

---

# AMENDMENT 5 — GUARDS INSPECT THE STAGED PAYLOAD (FM 32, 2026-08-15)

Status: IN_PROGRESS
Owner debt: **TD-R-198** (board rows malformed → the tool refuses → lanes hand-edit),
**TD-R-194(b)** (close mode cannot touch a malformed row), **TD-R-196**
(`lane_preflight` returns OK on a fully-HELD seam).
Written **before the first code edit**, per ruling 1 of this REQ.

## THE REQUIREMENT — Bill's words, FM 32, verbatim

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

## THE PRINCIPLE, STATED ONCE

**A guard that reads the working tree is guarding the wrong object.** What gets published
is the **index** — the staged payload — and the two can differ for entirely ordinary
reasons: another session stages into the shared index (NC 24 §8.6), a file is staged and
then edited back, `git add -p` takes a hunk the working file no longer shows. **Every
existing guard in this tool family infers safety from the working tree, and that inference
is what NC 22's passenger incident is made of.**

## THE ACCEPTANCE TEST

### G1 — THE TWO BOARD ROWS ARE REPAIRED, AND THE TOOL PROVES IT
Both malformed live-lane rows carry exactly the header's bare-pipe count afterwards, and
**`claim_lane.py` performs a real edit on each** — the proof is the tool accepting them,
not a recount.
**MEANING IS PRESERVED: no word is moved, added or deleted; only `|` → `\|`.**

### G1b — WHERE A CELL BOUNDARY IS GENUINELY AMBIGUOUS, THE CHOICE IS STATED
A row with more structural-looking pipes than the header has columns cannot be repaired
without deciding which one is the accident. **The rule: keep the FIRST candidate boundary
after the preceding cell and escape the later one** — the column order defines the first,
so a later one is necessarily the extra. **The choice is recorded in the dispatch doc with
its reasoning**, and it moves no text.

### G2 — CLOSE MODE PARSES ESCAPE-AWARE (TD-R-194(b))
`claim_lane.py close` operates on a row containing escaped `\|` without miscounting cells,
so a malformed-then-repaired row never needs hand surgery again.
**PASS/FAIL:** a fixture row carrying `\|` inside a cell is edited by the tool; the same
row with a BARE stray pipe is still REFUSED, loudly. **Both directions.**

### G3 — SURGICAL STAGING AND CLOSE VERIFY THE STAGED SET
Before committing, the tool reads **`git diff --cached`**, not the working file, and
refuses if the staged payload contains anything but its own single row.
**PASS/FAIL — the twin that decides this amendment:** a foreign row staged into the index
and **absent from the working tree** is **REFUSED**. A guard that reads the working tree
passes this case, which is why it is the twin.

### G4 — `lane_preflight` DETECTS A FULLY-HELD SEAM (TD-R-196)
Liveness is no longer process-only. A worktree that is **claimed** (a `.hip-scope` present)
and **dirty** (uncommitted or untracked work) reads as **HELD**, whether or not any process
is currently running in it.
**PASS/FAIL, both directions:** a claimed+dirty worktree with **no live process** reports
HELD (today it reports OK — that is TD-R-196); a clean, unclaimed worktree still reports
OK, so the guard does not refuse every lane on the day it lands.

## CONSTRAINTS

1. **No board row's TEXT changes.** Repair is escaping only.
2. **FM 28/29's refusals and FM 31's fail-closed scan are untouched.**
3. **`lane_preflight` must FAIL OPEN on infrastructure and CLOSED on policy** — the
   dispatcher's own existing rule; a preflight that cannot read a worktree must not thereby
   declare it held.
4. **No twin publishes anything**, and none writes to a real board.

---

# AMENDMENT 6 — `.hip-scope` WIDENS, NEVER REPLACES (FM 38, 2026-08-15)

Status: IN_PROGRESS
Written **before the first code edit**, per ruling 1 of this REQ.

## THE REQUIREMENT — Bill's words, verbatim

> claim_lane's .hip-scope write must WIDEN, never REPLACE. Multiple concurrent lane
> claims in one worktree must preserve all active attributed scope declarations. Add a
> twin proving lane B's claim cannot erase lane A's scope.

## THE DEFECT, AND THE EVIDENCE THAT IT IS NOT THEORETICAL

`_write_and_verify_scope` builds the whole file from this lane's prefixes and
`os.replace`s it. **Every claim therefore destroys whatever declaration was already
there.** Three independent kinds of evidence:

1. **THE FM 36 INCIDENT.** A `claim_lane.py` invocation *"executed and PUSHED `c0cc0d7`
   ('probe'), replacing FM 34's identifier with a test placeholder and **overwriting
   `~/hip-roadmap/.hip-scope`**"* — recorded on the board, the bad commit deliberately not
   rewritten.
2. **THE WORKAROUND IS ON THE BOARD, REPEATEDLY.** HA-97, NC 27, NC 30 and NC 22 each say
   some version of *"scope appended to `.hip-scope`, **widened not replaced**"* — every one
   of them a lane doing BY HAND what the tool should have done, because the tool could not.
3. **IT HAPPENED AGAIN WHILE THIS AMENDMENT WAS BEING WRITTEN.** FM 38's own claim
   (`c9e836b`) replaced `~/hip-roadmap/.hip-scope`, discarding FM 34's block. **The defect
   demonstrated itself one last time in the act of being filed**, and that is recorded here
   rather than tidied away.

**The cost is exactly what `.hip-scope` exists to prevent.** `scope_guard.sh` refuses a
commit that stages files outside the declared scope; a lane whose declaration has been
silently replaced by a neighbour is either unguarded, or guarded against the wrong set —
and the guard reports neither. **A safety declaration that a neighbour can delete without
either lane noticing is not a declaration.**

## THE SHAPE

Each lane's declaration is an **attributed block**, delimited and keyed on the lane:

```
# >>> hip-scope lane: <lane key> | claim: <message>
docs/
scripts/foo.py
# <<< hip-scope lane: <lane key>
```

## THE ACCEPTANCE TEST

### W1 — A CLAIM WIDENS
A claim writes ONLY its own block. Every other block in the file is preserved
**byte-for-byte**, and so is every line outside any block.

### W2 — RE-CLAIMING THE SAME LANE UPDATES, IT DOES NOT DUPLICATE
The same lane claiming twice leaves exactly one block for that lane, carrying the newer
prefixes — otherwise a lane that re-claims accumulates stale scope and the guard widens
without anyone deciding to widen it.

### W3 — A CLOSE REMOVES ONLY ITS OWN BLOCK
And leaves every other block, and all unattributed content, exactly as found.

### W4 — LEGACY CONTENT SURVIVES — the row this amendment could most easily fail
**Every `.hip-scope` in the estate today is hand-written**, with comments and bare prefixes
and no block markers at all. A build that only understood its own format would erase all of
it on first contact — **landing this fix by committing the exact defect it repairs.**
Unattributed content is preserved verbatim, in place.

### W5 — THE TWIN BILL ASKED FOR, BOTH DIRECTIONS
**Lane B's claim cannot erase lane A's scope.** Positive: after B claims, BOTH declarations
are present and each is attributed to its own lane. Negative: **the same fixture against
the pre-amendment write must LOSE A's declaration** — the FM 36 incident shape reproduced,
then dead.

### W6 — FAIL-CLOSED ORDERING IS UNCHANGED
A scope failure still happens BEFORE the board is touched, so "the board row is not
written" stays true by construction (ruling 12). A widening write that cannot be verified
restores the prior file byte-identical, exactly as the replacing one did.

## CONSTRAINTS

1. **No existing `.hip-scope` in the estate may lose a line** when a claim next runs in its
   worktree (W4).
2. **`scope_guard.sh` is not changed.** It reads every non-comment line; the block markers
   are comments, so the union of all blocks is what it enforces — the widened set — with no
   edit to the guard at all.
3. **The fail-closed ordering and the atomic write are untouched** (W6).

---

# AMENDMENT 7 — PREFLIGHT HELD-SEAM BEHAVIOUR (FM 39, 2026-08-15)

Status: IN_PROGRESS
Supersedes: **Amendment 5's G4 disposition**, which FM 32 left as *"refusal opt-in behind
`--held` until Bill rules"* and explicitly referred. **The ruling arrived; this is it.**
Written **before the first code edit**, per ruling 1 of this REQ.

## THE REQUIREMENT — Bill's ruling, verbatim

> held detection stays OPT-IN and VISIBLE, never a blocking default. The default preflight:
> 1. ALWAYS reports the other active holder prominently — identifies BOTH lanes and BOTH
>    scopes in the output.
> 2. BLOCKS on: actual scope overlap; ambiguous ownership (either lane's scope
>    unreadable/undeclared); staged changes that would overwrite another lane's attributed
>    board/scope state (FM 32's staged-diff check feeds this).
> 3. ALLOWS demonstrated non-overlapping parallel work — the FM 35/36 co-residency shape
>    with disjoint scopes passes with the report visible.

## WHAT THIS SETTLES

FM 32 measured that blocking on ANY held seam refuses lanes that are legitimately parallel
— FM 14's *"clean machine passes"* twin went red the moment it landed, because a
neighbour's worktree is routinely claimed-and-dirty. **The ruling keeps that finding and
sharpens it: co-residency is not the hazard. OVERLAP is.**

**So the default gate stops asking "is anyone else here" and starts asking "would we
collide".** Presence is reported; collision is refused.

## THE ACCEPTANCE TEST

### P1 — THE REPORT IS UNCONDITIONAL AND NAMES BOTH SIDES
Every default preflight prints the other active holder **prominently**, identifying
**BOTH lanes and BOTH scopes**. Not a footnote, not conditional on the verdict: a pass with
a co-resident lane is exactly when the operator most needs to see who else is there.
**PASS/FAIL:** with a co-resident holder, both lane keys and both scope sets appear in the
output — on the passing path as well as the blocking one.

### P2 — BLOCKS ON ACTUAL SCOPE OVERLAP
Two declarations overlap when one prefix contains the other by path. **PASS/FAIL:** an
overlapping sibling blocks with a distinct exit code and names the overlapping prefixes.

### P3 — BLOCKS ON AMBIGUOUS OWNERSHIP
**Either** lane's scope unreadable **or undeclared** — a sibling worktree that is dirty and
carries no `.hip-scope` — is ambiguous, and ambiguity blocks. **You cannot prove disjoint
against an unknown.** This is the fail-closed-on-policy half of the dispatcher's own rule,
and it is the condition most likely to be mistaken for a nuisance: a lane working without a
declaration is not "probably fine", it is unmeasurable.

### P4 — BLOCKS ON A STAGED COLLISION
Staged changes that would overwrite another lane's attributed board/scope state block.
**FM 32's staged-diff check feeds this**: the index diverging from HEAD on a shared board or
scope file, while a co-resident holder exists, is the collision — detected at preflight
rather than at commit time, which is the point of a preflight.

### P5 — ALLOWS DEMONSTRATED NON-OVERLAPPING PARALLEL WORK
**The FM 35/36 co-residency shape passes.** Disjoint scopes, both declared, no staged
collision → **exit 0, with the report visible.** A gate that refused this would be the
Amendment 5 default all over again, and FM 14's twin would go red again.

### P6 — HELD DETECTION STAYS OPT-IN
`--held` still blocks on ANY held seam, unchanged. **It is never the default**, and the
default's three blocking conditions are not "held" — they are overlap, ambiguity and staged
collision.

### P7 — A SOLO LANE IS BYTE-UNCHANGED
No co-resident holder → the preflight behaves exactly as it did before this amendment.

## CONSTRAINTS

1. **`--busy`'s existing contract is untouched** — it answers "is anything MID-RUN".
   Amendment 5's repair of the FM 14 regression stands.
2. **Fail open on infrastructure, closed on policy.** A worktree that cannot be read is
   AMBIGUOUS (P3, blocks); a worktree list that cannot be obtained is UNKNOWN and must not
   be reported as a clean pass.
3. **No new scope format.** Overlap is computed over the declarations FM 38's attributed
   blocks already produce, and over legacy unattributed lines, which are still valid scope.

## ALSO RECORDED BY THIS DISPATCH — THE INTERIM RULE IS RETIRED

**The one-worktree-one-dispatch interim rule is RETIRED as of this ruling.** It existed
because co-residency could not be made safe; the ruling makes it measurable instead, and a
rule that forbids what the gate now permits would contradict the gate. Recorded in
`docs/design/HIP_PROCESS__development-operating-model__v20260814_1025.md`.
**Debt-register row cleanup stays QUEUED for the next process pass** — not done here, and
not silently dropped.
