# DISPATCH_DOC_CLEANUP
Status: BUILT
Reconciled-Against: 141fbe4 (HEAD at dispatch start)
REQ: NONE — documentation and governance cleanup; no code changed (CLAUDE.md item 10: an ANALYSIS/MEASUREMENT dispatch may have REQ: NONE, and this is why)
Dispatch: D-91, 2026-08-01
**Status proposed: NONE. Nothing ruled MET.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @ `141fbe4`, clean.
`~/hip-vo`, `~/hip-dev`, `~/hip-harness` NOT touched. **No code changed.**

---

## 1. THE "ORPHAN" REQ — PREMISE CORRECTION: it is not an orphan. It was filed at D-80.

**`REQ_DEMO_WEB_REPLAY` is already filed and has been since D-80.** Verified against git,
not memory:

```
8025e10  2026-08-01  D-80: file REQ_DEMO_WEB_REPLAY (R1 CLEARED, R3 N/A);
                     bank the D-78 recon and D-79 licensing evidence
```

Filed at `docs/requirements/REQ_DEMO_WEB_REPLAY__remote-voice-demo-surface__v20260801_0732.md`,
with `LATEST_REQ_DEMO_WEB_REPLAY.md` pointing at it.

**I did not refile it.** Refiling would have created a *second* REQ for the same subject
under a new timestamp, with the older one not marked superseded — a Naming Law problem, and
it would have destroyed the D-80 provenance trail. This is the same reasoning that stopped
D-81 from re-running when it had already landed.

Everything the dispatch specified is already present, checked line by line rather than
assumed:

| Dispatch requirement | State in the filed REQ |
|---|---|
| Status FILED, acceptance NOT run | line 3 — `Status: FILED — acceptance NOT run` |
| Reconciled-Against read, not remembered | line 7 — `d7322d7`, with the note "verified by reading HEAD at filing time, not a remembered hash" |
| **(a)** R1 → CLEARED per D-79 | line 59 — `R1 — LICENSING — CLEARED (D-79, 2026-08-01). No longer gates v1.` |
| kokoro-onnx MIT, dist-info/licenses, v0.4.7 | present, with the note that METADATA carries no License field — which is why D-78 could not resolve it |
| weights + voice packs Apache 2.0, not verifiable from the files | present, both stated separately and the non-verifiability called out |
| no watermark, verified two ways | present (line 99), contrasted with the Chatterbox PerTh finding |
| attribution not required, colophon recommended | present (line 94) |
| caveat: GPL dependency chain | present (line 107) — phonemizer-fork GPLv3+, espeak-ng |
| caveat: synthetic training data, hexgrad's risk | present (line 113) |
| **(b)** R3 → N/A, synthetic fixtures | line 136 — `R3 — DEMO PRIVACY — N/A (Bill's ruling, 2026-08-01). Not a gate today.` with the "stands as a constraint on any future fixture" clause at line 157 |
| D-79 evidence banked | `docs/reviews/FABLE_D79_kokoro-licensing__three-licenses-and-watermark__v20260801_0732.md` |

**Nothing was missing. Nothing needed re-applying.** The one real gap in that REQ was a
false provenance claim, fixed below.

---

## 2. STANDING RULE ADDED TO `CLAUDE.md` — item 13

Verification steps run **unchained**, or in a form that cannot short-circuit.

I demonstrated the mechanic before writing the rule, so it reads as evidence:

```
$ grep -c "absent" file.txt
0
$ echo $?
1          # non-zero, despite "0" being the correct and expected answer
```

The dangerous shape, and why it is worse than a crash:

```
grep -c ... && git add ... || echo "CONFIRMED: nothing to stage"
```

prints a reassuring success message **while the `&&` branch never ran.**

Cited instances: **D-70**, **D-75**, **D-88**, as you listed them. Two I can characterize
from this repository's own record — at D-70 `git add` was silently skipped and a trailing
`||` printed "CONFIRMED no code", caught only because the commit later failed; at D-88 the
same shape aborted an INDEX verification mid-chain where `0` was the correct answer. **The
D-75 instance I could not corroborate from the commit record** — I searched its message and
found no mention — so it is carried on your account rather than on evidence I verified.
Flagging that rather than presenting all three as equally sourced.

The rule generalizes past `grep`: **an exit code is not an answer.** `grep`, `diff`, and
`test` all encode "found nothing" as failure, so wherever "nothing" is the desired result,
the exit status inverts the meaning of the check.

---

## 3. STALE-CLAIM AUDIT

**Method:** every hash-shaped token in `docs/requirements/*.md` and `docs/INDEX.md` was
extracted and resolved against git — **140 distinct hashes**, each checked for existence,
subject line, and reachability from HEAD.

### 3a. Cited hashes — clean, with two things worth knowing

**No cited hash is superseded or wrong.** Every one resolves to the commit its surrounding
text describes. Two categories of "unreachable" turned up, and neither is an error:

| Hash | Where | Status |
|---|---|---|
| `f8fadbd` | `REQ_ARCHITECTURE_BOUNDARY:143`, `INDEX:223` | **Does not resolve in this repository.** `hip-harness` is a *separate repo*, not a worktree. The citation is accurate; a reader on roadmap simply cannot `git show` it. Left as-is; noting it so nobody reads it as corruption. |
| `3d4f46f`, `4390240`, `d4a8a90`, `d7cf895` | INDEX, `REQ_ARCHITECTURE_BOUNDARY` | Real commits, **not ancestors of roadmap HEAD** — they live on `demo-presenter-package` and `voice-port`. Cross-branch citations, correctly labelled as such where they appear. |

### 3b. `REQ_STRUCTURAL_CEILING` and `98dfb7a` — the flag does not hold

You flagged that it "cites 98dfb7a in places and was superseded the same day by b0bc8e3."
Checked, and the citations are **correct history, not stale claims**:

```
98dfb7a  D-70: file REQ_STRUCTURAL_CEILING      -> added v20260731_2057
b0bc8e3  D-71: R16 ruling, R12 rewording…       -> added v20260731_2129  (current)
```

The current file's line 8 reads *"Reconciled-Against: roadmap `78939bc` (content); this
version cut at `98dfb7a`"* — accurate: the tree was at `98dfb7a` when v2129 was written, and
it landed at `b0bc8e3`. The only other `98dfb7a` citation (`INDEX:227`) records that the
D-70 survey was read against that HEAD, which is also true. **`LATEST_REQ_STRUCTURAL_CEILING.md`
points at v2129.** Nothing cites `98dfb7a` as if it were current.

**A related claim of mine that WAS stale, and is now corrected in this report:** earlier
sessions carried a note that the ceiling REQ's Related line still falsely read
`REQ_CARE_TEAM_READ_AUTH (MET)`. It does not — **D-71 already fixed it**, and line 10 now
reads `(**NOT MET** — corrected D-71; see R14)`. The note about the false claim had itself
gone stale.

### 3c. Four real stale claims — FIXED, and here is exactly what changed

| # | What was wrong | What I changed |
|---|---|---|
| 1 | **`REQ_DEMO_WEB_REPLAY` header claimed both sources were "banked in docs/reviews/". Only one was.** D-80 flagged this rather than softening it. | **Banked the actual artifact** — `docs/reviews/CHATGPT_D78_remote-voice-demo__two-mode-replay-and-live-challenge__v20260801_1438.md`, body byte-verified (`5f0de761…`) — then rewrote the line to cite **both files by path**. The claim is now TRUE as written. Editing the header to claim less would have hidden the gap instead of closing it. |
| 2 | **`REQ_STRUCTURAL_CEILING__v20260731_2057.md` still read `Status: FILED — acceptance NOT run`** and did not know it had been superseded. A reader opening it directly saw an active requirements doc. | `Status:` → **SUPERSEDED**, naming the successor and `b0bc8e3`, with "do not read this version as current." |
| 3 | **The current ceiling REQ's status line read a bare `FILED — acceptance NOT run`** while §16 records three rulings and A18/A29/A30 run and pass. False for three rows. | Status line qualified: 27 of 30 unruled; **R29 MET, R30 NOT MET, R18 NOT MET**; §16 governs where they disagree; and the reminder that A18 passing does not carry R18. |
| 4 | **`REQ_CEILING_ACCEPTANCE` §2's tier table still listed A18 under STRICT XFAIL** while §7.3 (D-87) re-tiered it to LIVE. A reader hitting the table first gets the wrong answer. | The A18 entry now reads **"SEE §7.3 — RE-TIERED TO LIVE"**. The table is otherwise untouched: D-87 deliberately left §§1–5 as filed, and I did not rewrite the plan. |

**No other status line in `docs/requirements/` is contradicted by a later ruling**, and no
cross-reference points at a moved or renamed artifact — every `docs/reviews/…` and
`docs/requirements/…` path cited resolves to a file that exists.

---

## 4. STILL UNRULED — for whoever picks this up next

### 4a. R30 item 5 — the backfill question

R30 is **NOT MET** solely because `SENSITIVITY_REGISTRY_VERSION` is exposed but **stamped
nowhere**. The unmade decision:

> **Do facts already in the graph get stamped `sensitivity.v1` retroactively, or do they
> stay unstamped as pre-registry?**

Neither answer is free. **Retroactive stamping** asserts something not known to be true —
those facts were classified under the *old, divergent* encodings TD-137 documented, so
stamping them `sensitivity.v1` claims a vocabulary that was not in force when they were
written. **Leaving them unstamped** means the graph permanently contains two populations,
and every consumer must handle "no version" forever.

The live population is small enough that this is cheap to decide now and expensive later:
**12 `:Fact` nodes** (D-81's inventory), all mapping cleanly — low 5, high 5, medium 2, zero
NULL. Blast radius grows with every fact written.

Scope if it lands: three governed contracts — the D-1 epistemic record
(`harness/epistemic_record.py:96,:170,:266`), every `:Fact` node
(`memory_engine/store.py:159,:185,:220`), and the append-only ledger, which dual-writes the
record and inherits its shape.

### 4b. A12 and A16 — the two CONTRADICTED rows

Both untouched by D-86 and D-87 by instruction. **These need rulings, not fixtures** — an
xfail failing against an unbuilt feature says "not yet"; one failing against a *ratified
design* says the requirement and the architecture disagree and someone must choose.

- **A12 (R12) — author readback.** Fails against INJ-3's owner permit. Diverges on exactly
  two clauses: **aggregation** (the permit is per-fact and unbounded, so reading back every
  fact one ever stored about a subject reconstructs the forbidden cross-report file) and
  **derivatives** (a fact derived from the author's own statements is *owned* by the author,
  so the same permit reaches it). Flips on a ruling to bound the owner permit **or** a
  change to derived-fact ownership — both code changes to a live read path. R12's named
  limit stands regardless: the author's retention of their own ciphertext is entrenched by
  the DEK wrap, so A12 can never assert the author loses their own sentence.
- **A16 (R16) — ledger contents.** Fails against the ratified crypto-shredding design,
  whose driver is statutory (47 USC 551). **Not a defect.** Flips only when D-71's
  both-mechanisms ruling *builds*: opaque keyed commitments in the chain, payloads
  off-ledger under per-member keys. **A16 and A17 must flip together** — flipping A16 alone
  would certify commitments-only while the personal data persists elsewhere unerasable.

### 4c. Also open, carried from recent dispatches

- **A11's re-specification is built but R11 is not ruled** (D-87 wired the control
  assertion; the requirement itself remains FILED).
- **The anchor target decisions** (D-90): whether a countersignature is wanted for v1, and
  whether to install the daily launchd agent — deliberately not installed.
- **The 16 UNWRITABLE ceiling rows** still lack fixtures; three of them need explicit
  authorization (A9's sensitive-media fixtures, A3's ethicist review).

---

## Files changed

| File | Change |
|---|---|
| `CLAUDE.md` | standing rule 13 added |
| `docs/reviews/CHATGPT_D78_remote-voice-demo__…v20260801_1438.md` | NEW — banked verbatim, body byte-verified |
| `REQ_DEMO_WEB_REPLAY__…v20260801_0732.md` | provenance line corrected (fix 1) |
| `REQ_STRUCTURAL_CEILING__…v20260731_2057.md` | Status → SUPERSEDED (fix 2) |
| `REQ_STRUCTURAL_CEILING__…v20260731_2129.md` | status line qualified (fix 3) |
| `REQ_CEILING_ACCEPTANCE__…v20260801_0617.md` | §2 A18 row points at §7.3 (fix 4) |
| `docs/INDEX.md` | D-91 row + banked-review row |

**No code changed. Nothing ruled MET. `REQ_DEMO_WEB_REPLAY` was not refiled** — it was
already filed, and saying so is the finding.
