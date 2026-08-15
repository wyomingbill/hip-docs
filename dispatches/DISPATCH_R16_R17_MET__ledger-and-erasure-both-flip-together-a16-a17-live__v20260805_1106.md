# DISPATCH_R16_R17_MET
Status: BUILT
Reconciled-Against: 2026-08-05 (D-R-179; parent `1fe90a1`)

**TYPE:** RULING-RECORD + REGISTER ADDENDUM (docs only; no code, no graph, no harness)

**REQ:** `REQ_STRUCTURAL_CEILING`, R16 and R17 — the subject of the ruling being recorded.
Nothing built. Nothing self-ruled.

## THE ASK

```
=== D-R-179 | ~/hip-roadmap, roadmap | Record R16 MET and R17 MET ===
STANDARD PREAMBLE. DOCS ONLY.
Bill ruled both MET, 2026-08-05, on D-R-173's executed evidence (ad90444).

1. RECORD R16 MET in §16. Evidence: a real production write through
   log_epistemic_record carries no forbidden field; discriminating fault twin proven
   against a genuine v1 event; the standing invariant holds across all 17 call sites.
   PERMANENT LIMIT IN THE RULING TEXT: every pre-cutover v1 event remains
   forbidden-field-bearing forever — the two-population reality, accepted as the price
   of anchor preservation at D-R-161.
2. RECORD R17 MET in §16. Evidence: fixture-scoped per-fact and per-member erasure with
   cross-owner cascade, machine-verifiable completeness report, executed fault twin
   proving incomplete erasure is caught. THREE LIMITS IN THE RULING TEXT: backup step
   externally blocked (no backup system); vector step N/A (no embedding store); and no
   real caller anywhere reaches either mechanism from an actual request — the request
   path is a separate, unfiled requirement.
3. Do NOT restore the header enumeration — D-131's pointer ruling stands, per D-R-178's
   own refusal. §16 carries the status; the board derives the rest.
4. Re-tier A16 and A17 LIVE if the acceptance doc has not already; same-edit rule
   applies if either is a strict xfail.
5. Rule nothing else. Report SHORT.
```

## WHAT WAS DONE

1. **Gate checked** — matched, tree clean except demo-cutover lane's own 4 untracked
   docs (left exactly as found), lock free, HEAD in sync with `origin/roadmap` at
   `62fd263` (D-R-178) at start.
2. **Confirmed D-R-173's evidence still stands**, not re-run: `ad90444` ("D-R-173: A16
   and A17 written and run for the first time, both pass") predates and is untouched by
   everything landed since (`c1538d2`, `1fe90a1`, `62fd263`) — none of which touch
   `eval/test_ceiling_retention.py` or anything A16/A17-related.
3. **Recorded R16 MET and R17 MET in `REQ_STRUCTURAL_CEILING`'s §16**, inserted
   immediately after R11's entry (matching D-R-178's own newest-first placement
   convention), each carrying: the evidence named in items 1/2 above, cited to the exact
   test names D-R-173 wrote, and the permanent limit(s) as **part of the ruling text
   itself**, exactly as instructed — not left as a residue to close later.
4. **Did NOT touch the §16 intro paragraph or the document's top-level header** — both
   deliberately carry no count/enumeration since D-131 (Bill's ruling, 2026-08-03), and
   D-R-178 already made and recorded this same refusal for R11. Verified by diff: the
   edit to `REQ_STRUCTURAL_CEILING` is a pure addition (48 insertions, 0 deletions).
5. **Re-tiered A16 (CONTRADICTED-XFAIL) and A17 (UNWRITABLE) to LIVE** in
   `REQ_CEILING_ACCEPTANCE__testing-plan-for-the-ceiling-sprint__v20260801_0617.md`:
   - §2's tier-count table updated (LIVE 9→11, CONTRADICTED-XFAIL 2→1, UNWRITABLE
     14→13), matching the exact enumeration/struck-through-departure convention D-145
     and D-148 already established for A2/A8.
   - §4's A16 entry given the same "RE-TIERED LIVE" heading treatment A12 received at
     D-103, with the original CONTRADICTED analysis retained as history below it.
   - §5's UNWRITABLE table row for A17 struck through with "REASON CLOSED" +
     "RE-TIERED LIVE, D-R-179", mirroring A2/A8's own row annotations exactly (§5
     itself stays otherwise as filed, per §7's own governing statement).
   - New **§7.8** added (after §7.7, the A2/A8 precedent), naming what closed each
     row's blocker, citing both rows' real mechanism/fault-twin/anti-vacuity evidence,
     and stating explicitly how this differs from A2/A8's own precedent: **R16 and R17
     are themselves ruled MET here**, not left NOT MET the way R2/R8 stayed after their
     own rows passed — the row's pass was the evidence, the ruling is a separate,
     later act.
   - **Same-edit rule note:** neither row was a strict xfail (A16 was CONTRADICTED-XFAIL,
     A17 UNWRITABLE), so that specific clause of item 4 does not apply as written; the
     tier-and-fixture-together discipline it protects was already satisfied earlier, at
     D-R-173, which wrote and ran both rows' real fixtures in the same dispatch that
     confirmed their blockers gone — this dispatch's tier flip lands on an
     already-proven row, not ahead of one.
6. **Wrote this dispatch doc**, staged by explicit pathspec, committed and pushed as one
   lock-guarded operation.

## WHAT WAS FOUND

No new code-level findings — this dispatch reads and records, it does not investigate.
Confirmed by direct read before writing anything:
- `REQ_STRUCTURAL_CEILING`'s §16 intro (`docs/requirements/REQ_STRUCTURAL_CEILING__...v20260802_2205.md:1098`) and top header (`:2-4`) both still carry the D-131 pointer-shape wording verbatim — no count, no enumeration — confirming there was nothing to "restore" and nothing this dispatch should add there.
- `REQ_CEILING_ACCEPTANCE`'s own §7 intro (`:349-351`, "sections 1–5 stay as filed") — read before editing §4/§5, confirming the established convention is surgical inline annotation (strikethrough + pointer to a new §7.N), not rewriting those sections, which is the same shape applied here.
- Grepped `docs/requirements/REQ_STRUCTURAL_CEILING__...v20260802_2205.md` for any prior R16/R17 MET entry — none existed before this dispatch.

## VERIFIED

**Watched (this dispatch):**
- `git log --oneline` confirming `ad90444` (D-R-173) is real, unamended, and not
  superseded by anything since.
- `git diff --stat` on both edited REQ docs after editing, confirming pure additions
  (`REQ_STRUCTURAL_CEILING`: 48 insertions/0 deletions; `REQ_CEILING_ACCEPTANCE`: 69
  insertions/8 deletions — the 8 deletions are the struck-through UNWRITABLE-reason and
  CONTRADICTED-XFAIL text being replaced with their own annotated versions, the same
  shape D-145's own diff shows for A2/A8).

**Reasoned about / carried, not re-verified in this dispatch:**
- A16/A17's own executed evidence (16 passed/2 xfailed equivalent — actually 4 + 5 = 9
  new cases, all passing) is D-R-173's own claim, re-cited here, not re-run — per this
  dispatch's own DOCS ONLY instruction and the STATUS check already confirming nothing
  since has touched that file.
- The full `--layer 7`/RATCHET/memory-harness runs this ruling's evidence rests on are
  D-R-173's and D-R-176's own executed runs (13/17 memory harness, RATCHET PASS both
  times) — not re-run here, since nothing in this dispatch changes code, graph state, or
  test files.

## HASH

`bb1ea1f` — pushed to `origin/roadmap`. Filled in by a same-session follow-up edit
after the commit landed (a commit cannot name its own hash inside the file it
commits), per the convention D-R-176 used. Contains: `docs/HIP_HANDOFF.md`,
`docs/INDEX.md`, `docs/requirements/REQ_CEILING_ACCEPTANCE__...v20260801_0617.md`,
`docs/requirements/REQ_STRUCTURAL_CEILING__...v20260802_2205.md`, this dispatch doc.

## OPEN

- **Nothing else ruled**, per instruction. R16 and R17 join R1, R11, R12, R18, R29, R30
  as MET; R2, R8, R10 stay NOT MET; every other requirement in `REQ_STRUCTURAL_CEILING`
  stays FILED, unruled.
- **R17's own "no real caller reaches it from an actual request" limit is the largest
  open item this ruling names but does not close** — a real, authorization-triggered
  erasure flow (as opposed to the proven-but-unconnected request path
  `harness.erasure_request` already provides) remains a separate, unfiled requirement.
- **The status board** (`docs/status/CEILING_STATUS.html`) was not regenerated by this
  dispatch — it derives its MET set from §16 on every run, so it will reflect R16/R17
  the next time it runs, not retroactively from this commit alone.
