# REQ_TRUST_AXES: Record Both, Rank Neither — Write Authority, and a Two-Signal Trust Record
Version: v20260731_0827
Status: PLAN
Branch: roadmap
Supersedes: REQ_TRUST_AXES__per-axis-trust-model__v20260731_0739.md (D-52, PLAN)
Reconciled-Against: 9788236 (2026-07-31). Diagnosis code-verified in D-51 against
`memory_engine/trust.py:27-34,70-78`, `harness/curator_shadow.py:79-83,96-97,199`,
`memory_engine/store.py:274,462`, `harness/extraction_queue.py:563`.

**NO CODE WRITTEN AGAINST THIS REQ.** Still REQ-first, still PLAN. D-52 filed the
predecessor; D-53 revises it on Bill's ruling after external evaluation. Nothing has
been built under either version.

## WHAT CHANGED IN THIS VERSION, AND WHY

The D-52 predecessor specified an **epistemic-strength ranking axis**: a second
ordering in which independent corroboration would outrank subject-confirmation for a
named list of attributes (adherence, alcohol, income, cognitive decline) and the
reverse elsewhere. **Bill ruled against that, after external evaluation.** This
version replaces it. Two things are removed and one is added:

1. **REMOVED — the ranking.** There is no second ordering. The system does not
   adjudicate self-report against corroboration.
2. **REMOVED — the motive-to-misreport attribute table.** This was a
   **content-blindness violation** and should not have been written. The D-50
   confirmation model's Principle 6 (Content-blind custody) states it directly:
   *"the system's protection cannot be the thing making a judgment about which
   content matters… the moment custody starts branching on content, some part of the
   system is silently adjudicating."* A table encoding "these are the topics people
   underreport" is exactly that branch. It would have made HIP the arbiter of which
   subjects its household lies about — and it fails D-50's own stress-test twin
   (Case 1 "I think Michael is drinking again" vs Case 2 "Michael likes jazz," which
   exist precisely to prove the machinery must not tell them apart).
3. **ADDED — a two-signal record.** For any claim, store two separate, co-existing
   signals and **never collapse them into a single trust verdict**:
   - `subject_asserted: bool` — did the subject themselves assert/confirm this?
   - `attestations: set` — independent attesting parties, **each carrying
     provenance** (per `REQ_ATTESTED`).

   The system **records both and ranks neither.** The consumer weighs them in
   context.

### The principle this extends

This is the D-50 portrait principle applied to trust strength. That document's core
analogy is *portraits, not photographs* — every claim an attributed rendering, signed
by its author, **two disagreeing portraits both kept**, the system rendering no
verdict. A ranking axis that declared "corroboration beats self-report for alcohol"
would have been the system rendering exactly the verdict the portrait model exists to
refuse. Recording both signals and declining to order them is the same move, one level
down: *hold the contradiction, let the consumer resolve it in context.*

D-50's Principle 3 already anticipated the shape — *"corroboration is tracked as its
own axis — a count or set of independent attesting parties per claim — sitting beside
the trust rung, not fused into it"* — and this REQ is the requirements-side statement
of it, minus the ranking the D-52 draft had added on top.

**Sources for the ruling:** the D-50 confirmation model
(`docs/design/HIP_ConfirmationModel_PortraitRethink__v20260731_0730.md`, Principles 3
and 6, and stress-test Cases 1–3), plus an external evaluation Bill refers to as
*gptresearch3*. **PROVENANCE GAP CLOSED 2026-07-31 (D-60).** That evaluation is now
committed at
`docs/reviews/CHATGPT_research-pass3-trust-axis-evaluation.txt` (1,166 lines,
banked verbatim), so the reasoning behind this ruling **is** verifiable from the
repo. It is the direct basis for "rank neither": it opens by stating there is *"no
defensible canonical total ordering of observed < asserted < corroborated <
confirmed."*

**History of this flag, kept rather than erased, because the correction was
itself wrong once.** The original D-53 filing flagged the evaluation as unbanked and
correct at the time. D-54/D-55 then *withdrew* that flag on the basis that the file
was present in `docs/reviews/` — but it was present **on disk and never committed**,
so the withdrawal was premature: an uncommitted file is not in the repo, and the gap
the flag named was still open. D-60 committed the file, which is what makes the
withdrawal true. The lesson is worth keeping in the record: "the artifact exists"
and "the artifact is in the repo" are different claims, and only the second one
closes a provenance gap.

## THE REQUIREMENT

Bill's ruling (D-53 dispatch), verbatim:

> "Bill ruled (after external evaluation) AGAINST a ranking axis. Revise REQ_TRUST_AXES:
>   - KEEP TRUST_RANK unchanged (write-authority axis).
>   - REPLACE the epistemic-strength RANKING with a RECORD: for any claim, store two
>     separate, co-existing signals — (subject_asserted: bool) and (independent
>     attestations: set with provenance) — and NEVER collapse them into a single trust
>     verdict. The system records both, ranks neither; the consumer weighs them in
>     context.
>   - REMOVE the motive-to-misreport attribute table entirely (it was a
>     content-blindness violation — the system must not decide which topics people
>     underreport).
>   - REWRITE acceptance A2: no longer 'order one pair differently.' Instead: prove
>     both signals are stored separately and are never collapsed into a single ranking
>     anywhere in the code path.
>   - Rationale to record in the REQ: this extends the Part 1 portrait principle (two
>     portraits kept, system renders no verdict) to trust strength — don't adjudicate
>     self-report vs corroboration, preserve both. Cite the D-50 confirmation model +
>     the external evaluation (gptresearch3).
>   - Keep REQ_ATTESTED's core requirement: attestations carry provenance so the system
>     can detect the echo case (B affirming a fact the system disclosed to B is not
>     independent evidence)."

## THE ACCEPTANCE TEST

Observable, pass/fail. Each must be demonstrable without reading a docstring for
reassurance.

**A1 — write authority is byte-unchanged.** `TRUST_RANK`'s values are identical to
`9788236`. A test asserts the exact dict, so a future reader "fixing" `DERIVED: 0`
fails a check rather than silently changing P8 behavior. The three comparison sites
(`store.py:274`, `store.py:462`, `extraction_queue.py:563`) produce identical verdicts
on a fixture table before and after. `TRUST_RANK` is named in-source as the
write-authority axis and nothing else.

**A2 — the two signals are stored separately and are NEVER collapsed. (REWRITTEN)**
This replaces the predecessor's "order one rung pair differently," which presupposed
the ranking this version removes. Three parts, all required:

- **A2a (separately stored):** `subject_asserted` and `attestations` round-trip as
  two independent fields. A claim can carry any combination —
  asserted-with-no-attestations, attested-but-not-self-asserted, both, neither — and
  all four states are representable and distinguishable on read.
- **A2b (never collapsed — the load-bearing test):** a test asserts there is **no
  function anywhere in the code path that takes both signals and returns a single
  scalar, rank, or ordering.** A static check over the trust surface (analogous to the
  CS1 prompt-touch scan, and subject to the same caveat that a regex scan is weaker
  than an import-graph scan — see CONSTRAINTS) plus a behavioral test: no consumer can
  obtain a combined verdict, because none is computed. If a single combined number can
  be read anywhere, A2 FAILS regardless of what that number is.
- **A2c (no content branching):** a test asserts the trust surface reads no attribute
  name, topic, or sensitivity value when recording or returning either signal — the
  drinking/jazz twin from D-50 Cases 1–2 produces byte-identical handling. This is the
  regression test for the removed motive-to-misreport table, so it cannot be
  reintroduced quietly.

**A3 — `_TRUST_ORDINAL` (`harness/curator_shadow.py:96-97`) no longer encodes a trust
verdict.** The current table is a scalar collapse and is inconsistent with itself
(`DERIVED: 1.0` above `CONFIRMED: 0.9`, contradicting `trust.py:17-18`'s explicit
"provenance category, not a strength"). Under this ruling the fix is **not** to derive
a better scalar — a scalar is the thing being refused. See OPEN item 1: the shadow
scorer's feature space is Bill's to rule on, and this REQ does not decide it.

**A4 — no rung reclassification.** `CORROBORATED` keeps its ratified
reconciliation-hardening meaning (`trust.py:73`). No fact already in the graph changes
rung. Social attestation stays in `REQ_ATTESTED` under its own name.

**A5 — `--layer 7` green, RATCHET PASS**, and `--full` green before any MET is
proposed.

## WHAT'S ALREADY DONE

- **The diagnosis, code-verified (D-51):** three orderings extracted verbatim;
  `_TRUST_ORDINAL` proven to be a one-to-one order-preserving map of the
  first-match-wins *evaluation* sequence at `trust.py:66-67` — a dispatch sequence
  mistaken for a magnitude.
- **`TRUST_RANK`'s purpose is documented and defended** at `trust.py:15-19`. A1 is a
  restatement, not a discovery.
- **CORROBORATED unreachability confirmed** (exhaustive, 144 combinations: 4 returns,
  zero with `confirmed_by` set). Context only; not fixed here, by ruling.
- **The predecessor REQ's three OPEN items are now two-thirds resolved by this ruling:**
  the motive-to-misreport list is REMOVED (moot, content-blindness violation), and the
  "callable return shape" question is answered — there is no ranking callable; there is
  a two-field record. Only the consumer question survives, as OPEN item 1 below.

## WHAT'S KNOWN BROKEN / OPEN

**OPEN 1 — the shadow scorer's `trust_rung` feature. Bill's ruling required; this REQ
does not decide it.** `DECLARED_FEATURE_KEYS` (`curator_shadow.py:79-83`) contains
exactly ten keys including `trust_rung`, and CS1 asserts that set exactly. Applying
"record both, rank neither" honestly to a learned ranker means giving it the two
signals **as two separate features** (`subject_asserted`, `attestation_count`) and
dropping the single collapsed `trust` scalar — a learner is precisely a consumer that
weighs signals in context, which is what the ruling asks for. But that changes the
declared feature space from ten keys to eleven, and the ten-key space was Bill's own
D-33 ruling, enforced by an ABSOLUTE check. Three options, his call:
  (i) replace `trust_rung` with the two signals (10 → 11 keys, CS1 updated);
  (ii) drop `trust_rung` from the feature space entirely (10 → 9);
  (iii) leave the scorer untouched this pass and scope it separately.
Note that (iii) leaves a known-inconsistent scalar live inside a MET component.

**RESTATED 2026-08-01 (D-55), not resolved — Bill's framing, so it stays visible:**
"does the shadow scorer consume the trust record as TWO features — honoring
'record both, rank neither' for the learner — which moves `DECLARED_FEATURE_KEYS`
from 10 to 11 and breaks the D-33 ten-key ABSOLUTE lock? Or keep the 10-key lock
and do not feed the scorer the trust record yet?" Fable named the three options
above and picked none. Still open, still Bill's call — this dispatch adds
visibility only, no ruling.

**OPEN 2 — does anything consume the two-signal record this pass**, or is it built
ahead of its caller (the pattern the isolation gate used)? Carried forward unresolved
from the predecessor.

**OPEN 3 — `attestation_count` is itself a collapse.** A count discards the provenance
that `REQ_ATTESTED` exists to preserve — three attestations of unknown independence and
three verified-independent attestations are not the same evidence, and per
`REQ_ATTESTED`'s echo case one of them may be worth zero. Whether any consumer may see
a bare count, or must see the provenance-bearing set, is unresolved and matters most
wherever the count would drive behavior.

**~~OPEN 4 — `gptresearch3` is not banked.~~ CLOSED 2026-07-31 (D-60).** The
evaluation is committed at
`docs/reviews/CHATGPT_research-pass3-trust-axis-evaluation.txt`; the ruling's basis
is verifiable from the repo and this is no longer a blocker to MET. See "Sources for
the ruling" above for why the earlier D-54/D-55 withdrawal of this flag was premature
(the file was on disk but uncommitted).

## CONSTRAINTS (what must not regress)

- **P8 write-monotonicity is ratified and load-bearing.** `TRUST_RANK` values must not
  change. `DERIVED = 0` is correct for the write-authority axis and is not a bug.
- **`CORROBORATED` keeps its reconciliation-hardening meaning.** Two specs pin it
  (`DEMO_SPEC:46`, `D1_RECORD_SPEC:51`) and a demo fixture depends on the current rank
  relationship (`demo_scripts/test/park_and_confirm__v20260712_1023.json:45`).
- **Content-blindness is a hard constraint, not a preference** (D-50 Principle 6). No
  part of the trust surface may branch on what a claim is about. A2c is its regression
  test.
- **`REQ_CURATOR_SHADOW_SCORER` is MET (D-44).** Any change under OPEN 1 touches its
  feature space and its ABSOLUTE check. If it regresses, the honest move is a pullback
  per the D-42 precedent — not a quiet re-baseline.
- **A2b's static scan is weaker than it looks.** D-46 §1.1 and the D-40 review both
  found regex-based structural scans in this codebase that a rename or an import alias
  defeats. A2b should prefer an import-graph or AST check over a regex, and if it uses
  a regex, that weakness must be named in the coverage entry rather than presented as
  proof.
- No self-MET. MET is Bill's ruling.
