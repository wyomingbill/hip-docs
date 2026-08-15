# REQ_SENSITIVITY_NO_DEFAULT — a missing sensitivity label is refused, never stamped

Status: IN_PROGRESS — built D-R-196, 2026-08-06. **NOTHING RULED MET.** Acceptance
C1–C9 below are reported, not self-ruled; the MET call is Bill's.
Reconciled-Against: roadmap `a32ddaa`. **The tree moved mid-dispatch and this line
records it rather than hiding it:** this REQ was written against `e6dcac0`, and while the
build was in progress the roadmap lane advanced to `a32ddaa` (D-D-161's TD-129 memory-guard
metric port, which also committed the `scripts/run_harness.sh` edit that was sitting
uncommitted in this tree at the machine gate, and repointed `LATEST_DEBT.md` to
`DEBT_REGISTER__v20260806_1347.md`). Nothing D-D-161 landed touches any of the seven sites;
the C9 runs below were executed on the merged state.

**Dispatch:** D-R-196
**Supersedes:** nothing. **Amends nothing.** This REQ is NEW; it carries a ruling that
`REQ_STRUCTURAL_CEILING`'s R29/R30 already implied but did not enforce at these sites.
**Related:** `REQ_STRUCTURAL_CEILING` R29/R30 (both ruled MET 2026-08-01) and A29/A30;
`TD-D-148` on `demo-cutover-build` (the two-site version of this finding);
`harness/sensitivity.py` (the registry that already refuses).

---

## 1. THE REQUIREMENT — Bill's words, verbatim

> "A fact with no sensitivity label is refused at every boundary, not stamped medium.
> The default parameter is removed from the production write path entirely — a caller
> that omits sensitivity gets an error, not a quiet label. The eleven LOW defaults on
> turn-level disclosure records are ruled separately as their own question, not swept
> into this one."
>
> — Bill, 2026-08-06 (D-R-196)

Nothing above is paraphrased anywhere in this document. Where this REQ uses different
words, those words are this REQ's reading of the ruling, and are marked as such.

## 2. WHAT THE RULING DECIDES, AND THE ONE THING IT DOES NOT

The ruling settles the WRITE path without ambiguity: the default parameter is removed,
and omission is an error.

It says "refused at every boundary." **A read boundary has no caller to hand an error
back to** — it is a loop over stored rows assembling a candidate set, and the row with
no label is one row among many. So "refused" has two possible enactments there:

- **(a) REFUSE THE ROW** — the unlabelled fact does not enter the returned set; the
  boundary logs it and continues. One bad row costs that row.
- **(b) RAISE** — the unlabelled fact takes down the whole read, and with it the turn.
  One bad row costs the turn.

**THIS BUILD IMPLEMENTS (a) AT READ BOUNDARIES AND HARD-RAISE AT THE WRITE BOUNDARY,
AND THAT SPLIT IS THIS SESSION'S READING, NOT BILL'S WORDS.** It is flagged here as
the single interpretive call in the build, because it is the one place a reviewer could
reasonably have expected the other answer.

The reasons for (a), stated so the choice can be overruled on its merits:

1. **It is the house pattern already at every one of these sites.** All four read
   boundaries sit inside a per-row loop that already does exactly this for the adjacent
   failure — `log.warning("decrypt failed ... skipping"); continue`. (a) makes a missing
   label behave like a fact that cannot be decrypted: not returned, loudly logged.
2. **(b) converts a silent degradation into an outage.** `TD-D-148` named this in
   advance as the reason it declined to fix the read sites inside another dispatch:
   "changing them turns a currently-silent degradation into a raise on a live read path."
3. **(a) is strictly fail-closed for the harm this REQ exists to prevent.** The harm is
   an unclassified fact being GATED AS THOUGH classified. A refused row reaches no gate,
   no prompt, and no model — which is more restrictive than any stamp, `critical`
   included.

**What (a) costs, stated plainly:** a refused row is invisible to the member as well as
to the model. If a real household fact loses its label, the member stops seeing it and
gets no error saying why — only a warning line in a log they do not read. (b) would be
noisy and obvious. **If Bill wants the noisy failure, this is a one-line change per site
and the tests are already written per-site.**

## 3. WHAT IS IN SCOPE — the seven substitution sites

A **substitution site** is a place where a missing sensitivity BECOMES a value. That is
the acceptance bar's own definition (§5, C1) and it is what the enumeration below counts.
Explicit `sensitivity="medium"` at a CALL SITE is not a substitution — the caller stated
a label, and whether it stated the right one is a different question this REQ does not open.

| # | Site | Idiom, quoted from the live file | Boundary |
|---|---|---|---|
| 1 | `memory_engine/store.py:605` | `sensitivity: str = "medium"` (`encode()` signature) | WRITE — the production write path named in the ruling |
| 2 | `harness/extraction_queue.py:318-319` | `if not sens:` → `sens = "medium"` | WRITE — model-extraction admission |
| 3 | `memory_engine/recall.py:249` | `"sensitivity": row["sensitivity"] or "medium"` | READ — cold recall |
| 4 | `memory_engine/api.py:241` | `sensitivity = row["sensitivity"] or "medium"` | READ — `candidate_facts` |
| 5 | `harness/extraction_queue.py:874` | `"sensitivity": r["f.sensitivity"] or "medium"` | READ — retrieval |
| 6 | `harness/extraction_queue.py:954` | `"sensitivity": r["sensitivity"] or "medium"` | READ — scored retrieval |
| 7 | `server/memory_dashboard.py:132` | `"sensitivity": row.get("sensitivity") or "medium"` | READ — dashboard inspector |

Sites 3 and 4 are `TD-D-148`'s two, quoted there verbatim and unchanged since. Sites 1
and 2 are the two the dispatch named directly. Sites 5, 6 and 7 are the three the
two-site filing did not reach.

**Test harnesses carrying the same default** (dispatch item 3 — same treatment):

| # | Site | Idiom |
|---|---|---|
| T1 | `eval/integration_harness.py:122` | `FixtureFact.sensitivity: str = "medium"` |
| T2 | `eval/injection_harness.py:44` | `make_fact(..., sensitivity: str = "medium")` |

## 4. WHAT IS EXPLICITLY OUT OF SCOPE

- **The eleven LOW turn-level disclosure defaults — Bill's own carve-out, item 7.** Not
  touched, not tested, not counted in the seven. Enumerated in the dispatch doc so the
  separate ruling has a list to rule on.
- **`harness/zep_store.py:109-112` (`_DEFAULT_TAGS["sensitivity"] = "medium"`).** An
  eighth site by the acceptance bar's own definition, in a DIFFERENT store (graphiti/Zep,
  reached only from `server/voice_mem0.py` and `voice/`). Not in the seven the dispatch
  scoped, and NOT fixed. **Named here rather than quietly left out**, because §5 C1's grep
  will surface it and a reader must not think it was missed.
- **Whether any currently-stored fact lacks a label.** Unchanged from `TD-D-148`'s
  finding: the defect is dormant on a populated graph and arms on the first unlabelled write.
- **`scripts/routing_benchmark.py:301`** (`raw.get("sensitivity", "none")`) — a benchmark
  script, not a boundary; noted, not fixed.

## 5. THE ACCEPTANCE TEST

Each clause is observable and can only pass or fail.

| ID | Clause |
|---|---|
| C1 | **The grep bar, from the pitch's own sentence:** a reviewer greps the repo and finds no site where a missing sensitivity becomes a value. Run in the report, output included, scope stated. |
| C2 | `encode()` has no `sensitivity` default. A call omitting it raises; **nothing is persisted** — proven by a fact count taken before and after, not by the absence of an exception. |
| C3 | Anti-vacuity for C2: the SAME call WITH a valid label succeeds and persists exactly one fact. |
| C4 | `extraction_queue._coerce_fact` returns `None` for a fact with no sensitivity, matching its own sibling branch for an unrecognized one. |
| C5 | Each of the four read boundaries (sites 3–6) excludes an unlabelled row from its result and logs it; a labelled row in the same call is returned. Fault twin and anti-vacuity per site. |
| C6 | Site 7 (dashboard) excludes an unlabelled row; a labelled row in the same call is returned. |
| C7 | T1/T2 have no `sensitivity` default; every existing call site already passes one, so the test suite's own counts are unchanged by their removal. |
| C8 | The 19 `encode()` call sites that relied on the default now state a label, and the label each states is recorded in the dispatch doc — not chosen silently. |
| C9 | Runs: `--layer 7`, RATCHET, and the memory harness. Memory harness pinned at 13–15/17; **16/17 is a STOP**, not a pass. |

**Acceptance tier: ABSOLUTE for C1–C6.** A substitution site is a durable
misclassification of a fact the system could not classify, which is the failure R30
exists to prevent.

## 6. WHAT'S ALREADY DONE — do not redo

- **`harness/sensitivity.py` ALREADY REFUSES.** `rank()`/`normalize()` raise
  `UnknownSensitivity` on anything unrecognized, and a missing value normalizes to
  `"none"`/`""` which is not in the order — so the registry has been correct since D-75.
  **The seven sites are not a missing mechanism; they are seven bypasses of a mechanism
  that already exists.** This REQ adds no new ordering, no new level, and no second
  vocabulary.
- **`extraction_queue`'s UNRECOGNIZED-value branch is already hardened** (D-75) and
  refuses. Site 2 is the MISSING-value branch three lines below it, which the same
  dispatch deliberately left alone and flagged in its own comment: "FLAGGED for Bill's
  ruling, not silently changed." **This REQ is that ruling arriving.**
- **`PRE_REGISTRY` is a VERSION marker, not a level.** A pre-registry fact still carries
  a real level; it is stamped `sensitivity_registry_version = "pre-registry"` (D-93).
  `TD-D-148` worried that refusing would strand pre-registry facts — **it does not**, and
  that concern is discharged here rather than carried forward.
- **No production caller of `encode()` omits `sensitivity`** — 60 call sites surveyed by
  AST (not grep: `str.encode()` is textually identical), 41 already pass it, and all 19
  that do not are in `eval/memory_harness.py`.

## 7. WHAT'S KNOWN BROKEN

1. **A29 was ruled MET on 2026-08-01 while these seven sites were live.** A29's own
   acceptance text reads "local enums and defaults fail static/runtime tests." Seven
   defaults were in the tree and no test failed. **The requirement was met in the
   registry and unmet at the boundaries, and the acceptance check could not tell the
   difference.** Recorded as a finding against the acceptance, not as a re-ruling of A29 —
   re-tiering an acceptance row is not pre-authorized.
2. **The 19 memory-harness call sites were hiding site 1.** Every one of them wrote a
   fact whose label nobody chose. Dispatch item 3's sentence — "a test that depended on
   the default is a test that was hiding the defect" — is literally true of these 19.
3. **The read-boundary refusal is invisible to the member** (§2, "what (a) costs").
4. **This REQ does not prove the seven are all of them.** It proves the grep in C1 is
   clean at the moment it ran, over the scope it states. A substitution written in a
   shape the grep does not match would not be caught.

## 8. CONSTRAINTS — what must not regress

- **No new sensitivity vocabulary, ordering, or level.** One registry (R29). Every
  refusal in this build routes through `harness/sensitivity.py`, which is the only module
  allowed to decide what a valid level is.
- **The eleven LOW turn-level defaults are not touched.** Bill's carve-out.
- **Nothing marked MET.** C1–C9 are reported; the ruling is Bill's.
- **`--full` is not the bar here** (TD-129's memory guard); C9's three runs are.
- **The frozen demo (`~/hip-dev`, 7689) is not touched.**

## 9. LANDING ORDER

1. This REQ (item 1 of the dispatch — written before any code).
2. One refusal helper in `harness/sensitivity.py`; no second definition anywhere.
3. Site 1, then site 2 (the two write boundaries), with their fault twins.
4. Sites 3–7 (the read boundaries), with their fault twins.
5. T1/T2, then the 19 call sites that relied on site 1.
6. C1's grep, then C9's three runs.
