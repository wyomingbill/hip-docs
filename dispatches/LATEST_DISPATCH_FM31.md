# DISPATCH_FM31_PUSH_SCAN_FAILS_CLOSED
Status: BUILT
Reconciled-Against: `f3bae8c` (`~/hip-roadmap` @ `roadmap`), 2026-08-15

**TYPE:** BUILD + MEASUREMENT

**REQ:** `docs/requirements/REQ_PROCESS_HARDENING_TOOLS__claim-lane-register-doc-lane-preflight-scrub__v20260814_1613.md`
— **AMENDMENT 4**, filed at `cf0cda4` **before the first code edit**. TD-R-197 states the
split explicitly: *"Filing pre-authorized (tool infrastructure); FIXING needs a REQ."*

**CLAIM IMPACT: none.** No ledger row gains or loses evidence.

---

## ✅ THE RETROSPECTIVE VERDICT, FIRST — NO SECRET IS OR WAS LIVE ON THE MIRROR

**No STOP condition. Nothing needed flagging before the rest of the work.**

| what was checked | result |
|---|---|
| the mirror's **current** published set (15 files) | **0 real-secret-class lines** |
| **every reachable published state** — all **17 commits**, 17 real-secret classes each | **0 in every one** |
| survivors of the fixed scan on the current set | **34 lines / 10 files, all `docs-secret-vocabulary`** — prose, the one non-substitutable class |

**And the exposure window was the script's entire life, not a recent regression.** The
multi-line exclusion string is present in `push_docs.sh`'s **first commit**, `b7fc7a5`
(2026-07-05) — verified by reading that blob, not inferred. **Stage 3 has never once run
successfully.**

### ⚠ THE VERDICT IS BOUNDED, AND THE BOUND MATTERS

**"Clean" here means: no class the table can detect AS A VALUE is present.** It does not mean
"no secret was ever published", and one known case proves the difference:

The mirror's newest commit is literally **`2717d82` — "security: redact rotated Neo4j
credential in security audit doc"** (2026-07-05). So a real credential *was* published, and:

- **its pre-redaction state is still publicly reachable** at `2717d82~1` — a force-push
  rewrites the tip, but all 17 commits are reachable from `HEAD` and any clone gets them;
- **no real-secret class matches it**, before or after — a Neo4j password belongs to none of
  the 17 substitutable classes, only to the detect-only `docs-secret-vocabulary` vocabulary;
- **the mitigation was rotation plus a human redaction**, per the commit message's own word
  *"rotated"* — **not this scan**, which could not have caught it then and cannot now.

**Recorded so nobody reads this dispatch's green as broader than it is.** Filed as an OPEN
item below rather than fixed here.

---

## THE ASK

Verbatim.

> FM 31 — REPAIR TD-R-197: THE PUSH SCRIPT'S FALSE-CLEAN SCAN
>
> PREAMBLE: STANDARD PREAMBLE. Claim FM 31 (scoped claim). REQ amendment before code.
> TD-R-197's row holds the defect + fix direction — read it first.
> 1. Fix the exclusion filter so it cannot die on its own pattern (the newline-separated
>    branches ending in |), and REMOVE the error-swallowing: a scan-stage failure is a
>    refusal to push, never an empty HITS.
> 2. Fail-closed contract for the whole scan: any stage erroring -> visible refusal, exit
>    nonzero, nothing published. Twins: the reproduced broken-pattern case -> refuses; a
>    planted secret in docs/ -> caught and refuses; clean docs/ -> passes; the FM 29
>    absent-policy case still refuses.
> 3. RETROSPECTIVE, read-only: enumerate what past mirror pushes published while the scan was
>    broken — run the FIXED scan against the mirror's current published set and report hits
>    (values never in output, classes + counts only). If any real secret is live on the
>    mirror, STOP and flag for Bill before anything else.
> RECAP: ID + title, twin results, the retrospective verdict plainly first, commits.

---

## WHAT WAS FOUND

### 1. THE DEFECT, REPRODUCED BEFORE IT WAS TOUCHED

```
=== STAGE 3 RUN ALONE ===
grep: empty (sub)expression
   stage-3 exit code: 2

=== THE FULL PIPELINE, AS SHIPPED ===
grep: empty (sub)expression
   HITS is empty: YES
   VERDICT the script would print: 'Secret scan: clean.'   <-- FALSE CLEAN
```

Exactly TD-R-197's mechanism: grep treats a newline inside a pattern as a **pattern
separator**, every branch line ending in `|` becomes an **empty alternative**, the stage exits
**2**, and `HITS=$(… || true)` converts that death into an empty string.

**One nuance TD-R-197 does not state, and it sharpens the finding rather than softening it:**
`grep: empty (sub)expression` **was printed to the operator's terminal** — stage 3's stderr was
never redirected. So the failure was *visible* while the **verdict line said clean and the
script pushed**. An operator reading the verdict — which is what a verdict is for — was misled
past a diagnostic that was on screen.

### 2. THE DECISIVE BEFORE/AFTER, ON ONE FIXTURE

A `docs/` containing a plain AWS access key, run against the **pre-fix script from git**:

```
Scanning docs/ for secrets before push...
grep: empty (sub)expression
Secret scan: clean.

Splitting docs/ subtree → branch docs-mirror ...
```

**It said clean and proceeded to publish.** The repaired script refuses the same fixture with
exit 1 and the hit listed. Same input, same script path, one commit apart.

### 3. WHAT THE REPAIR IS

- **The exclusion list is an array, one branch per element** (`EXCLUDE_BRANCHES`), expanded to
  `-e` per branch. No element contains a newline, so no element can be split; an accidental
  trailing `|` in one branch now breaks *that branch* loudly instead of silently emptying the
  whole expression. **`-e` per branch is semantically identical to one alternation under `-v`**:
  grep selects on ANY `-e` match and `-v` inverts. Nothing widened, nothing dropped
  (Amendment 4 constraint 3).
- **One deliberate change, named rather than slipped in.** The old continuation lines were
  indented, so the **first** branch on each carried five leading spaces baked into the pattern
  while later branches on the same line did not. Source formatting, not intent. Dropped. **It
  changes no behaviour, because stage 3 never executed successfully** — there is no prior result
  for it to differ from.
- **`|| true` is gone.** Each stage writes its own file and its exit code is classified: **0
  matched, 1 no match, anything else THE SCAN FAILED** → visible refusal on stderr, **exit 2**,
  nothing published. `grep` encodes "found nothing" as exit 1, which is exactly the inversion
  CLAUDE.md item 13 records as having produced three false all-clears.
- **Stage 1's `2>/dev/null` is gone too.** Its stderr is captured and shown on refusal — it hid
  the same class of failure one stage earlier.

### 4. THE TWINS — 4 passed, 0 failed, both directions

Every twin runs **the real `scripts/push_docs.sh`** against a fixture repo, so the shipped
script is what is exercised.

| twin | want | got | rc | said clean | reached split |
|---|---|---|---|---|---|
| **T1** reproduced broken pattern | REFUSE | **REFUSE** | 2 | no | no |
| **T2** planted secret in `docs/` | REFUSE | **REFUSE** | 1 | no | no |
| **T3** clean `docs/` | PASS | **PASS** | 128 | **yes** | **yes** |
| **T4** FM 29 absent-policy | REFUSE | **REFUSE** | 1 | no | no |

- **T2 took the HIT branch** (`SECRET SCAN FAILED — aborting push`), not the run-failure
  branch — the right refusal for the right reason.
- **T4 printed FM 29's own `SECRET SCAN UNAVAILABLE` message, unchanged.**
- **T3 is the anti-vacuity row and is not decoration:** a scan that refused everything would
  pass T1, T2 and T4 while making the mirror unpublishable forever.
- **T3's `rc=128` is the subtree split failing in a non-git fixture, after the scan passed.**
  The twins are abandoned there on purpose — **publishing the mirror is not licensed by this
  dispatch** (Amendment 4 constraint 4), and the truncation is stated rather than hidden, the
  same way Amendment 3's consumer test stated its own.

### 5. ⚠ THE CONSEQUENCE NOBODY HAS SEEN YET — THE NEXT PUSH WILL REFUSE

The repaired scan, run over the **private** `docs/` tree, completes all three stages for the
first time: **2497 → 2491 → 1818 lines.** Classified (**classes and counts only**):

| class | kind | files | lines |
|---|---|---|---|
| `docs-secret-vocabulary` | vocabulary | 346 | 1506 |
| `user-path` | **real secret** | 54 | 149 |
| `machine-hostname` | **real secret** | 84 | 93 |
| `tailnet-address` | **real secret** | 63 | 66 |
| `tailnet-address-host` | **real secret** | 63 | 66 |
| `home-address-street` | **real secret** | 12 | 21 |
| `user-ssh` | **real secret** | 14 | 18 |
| `home-address-full-city` | **real secret** | 9 | 17 |
| `lan-address` | **real secret** | 5 | 7 |
| `tailnet-domain` | **real secret** | 3 | 4 |
| `lan-cert-cn` | **real secret** | 4 | 4 |
| `tailnet-host` / `tailnet-name` | **real secret** | 1 / 1 | 1 / 1 |
| | | | **447 real-secret-class lines** |

**So the mirror is clean because nobody ran the push, not because the control worked.** Had
`push_docs.sh` been run at any point since 2026-07-05, it would have printed *"Secret scan:
clean."* and published all of it. **The repaired script now refuses — that refusal is the fix
working, and it makes the mirror unpublishable until these are triaged.**

**Two honest qualifications on that table:**
1. **Classification is by DETECT class, not by ruling.** FM 28's policy deliberately retains
   some categories (*"city-only and zoning stay"*), so a share of the `home-address-*` rows may
   be policy-permitted rather than defects. **This dispatch does not adjudicate them.**
2. **Widening the exclusion list to make the mirror publishable again is NOT this dispatch's
   call** — Amendment 4 constraint 3 makes any change to what is excluded a separate ruling,
   and tuning a filter until a scan goes green is precisely the shape this project forbids.

---

## VERIFIED

**Watched run** — five artifacts, all in the session scratchpad, all reproducible from this doc:
`fm31_repro.sh` (the defect, pre-touch) · `fm31_twins.sh` (the four twins) · the pre-fix
script from git against T2's fixture (the before/after) · `fm31_retrospective.py` (the mirror's
current set) · `fm31_retro_history.py` (all 17 reachable published states).

**No value was printed anywhere.** Every report is class + count. The mirror was cloned
**read-only** into the scratchpad; nothing was pushed to it, and nothing in this dispatch
publishes.

**Reasoned about — not independently executed:**
- That `-e` per branch preserves the alternation's meaning exactly. This is grep's documented
  semantics plus the observation that stage 3 never ran before, so there is no prior output to
  diff against. **A behavioural differential is impossible here by construction, and that is
  stated rather than papered over.**
- That the 17 substitutable classes are the complete set of "real secret as a value". Read from
  `scrub_patterns.entries("docs")`, which the code comments establish as the superset.

---

## HASH

| commit | what |
|---|---|
| `83f6313` | board claim |
| `cf0cda4` | **REQ Amendment 4 — before code** |
| `f3bae8c` | the repair + the measured before/after |
| *(this commit)* | dispatch doc, TD-R-197 status, INDEX |

---

## OPEN

1. **NEEDS BILL — the 447.** `docs/` carries 447 real-secret-class lines and the repaired scan
   correctly refuses to publish them. **Triage is a separate dispatch**, and the FINITENESS
   RULE keeps it filed rather than making it the next task. Do not widen the exclusion list to
   restore a green.
2. **NEEDS BILL — the bound on "clean".** A Neo4j credential belongs to no substitutable class,
   so the mirror scan cannot detect one as a value. `2717d82~1` — the pre-redaction state of the
   one known real exposure — **remains publicly reachable**, mitigated by rotation rather than
   by removal. Whether the mirror's history should be rewritten is Bill's.
3. **`FM 30` has no row on this board** — searched, zero occurrences. Not renumbered, not
   invented; recorded as a gap per STANDARD PREAMBLE item 10.
4. **Not measured: whether the exclusion list's branches are individually still correct.** They
   were preserved verbatim; nobody has ever seen them run, so nothing here says they exclude the
   right things — only that they now run at all.
