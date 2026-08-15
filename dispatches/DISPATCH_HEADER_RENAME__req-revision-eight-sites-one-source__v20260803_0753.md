# DISPATCH_HEADER_RENAME
Status: BUILT
Reconciled-Against: 2026-08-03 (D-117; parent c0bca12 at dispatch time)

**TYPE:** BUILD

**REQ:** `REQ_STRIP_CONTEXT_COMPLETENESS__header-rename-facts-about-other-
people__v20260803_0731.md` — the REVISION D-117 directed, written FIRST from
Bill's ruling words, before any code was touched. The prior version
(v20260727_1851, MET) is superseded in place; its MET ruling stands there as
the record for the old literal. Symlink moved.

## CONTEXT — the gate, and a numbering note

This lane's D-116 (2026-08-03, earlier session turn) was REFUSED at CLAUDE.md
Requirements Discipline item 8: it asked for this same build and named no REQ
doc. D-117 cures the gate exactly as item 1 prescribes (REQ first, from
Bill's words, build under it). Numbering note for the record: the cutover
lane independently used "D-116" for its caveat-panel verification dispatch
(docs/dispatches/DISPATCH_DEMO_CUTOVER_VERIFY_CAVEAT_PANEL, 06:53) — same
number, different lane, no relation; "D-116's finding" below means this
lane's refusal report (the wrapped-pin grep evasion).

Backlog discipline: this jumped the queue as a direct Bill dispatch ruling a
flagged-open defect (the D-114/D-115 header mislabel); said here, not
silently.

## THE ASK (D-117, condensed)

> REQ first (a REVISION — the problem IS that the prior REQ's acceptance
> item 1 pins the old literal), then the rename at all sites in one edit.
> Ruling, Bill, 2026-08-02: the header becomes "Facts about other people" —
> the old wording is FALSE over a section that can carry confirmed,
> asserted, or unconfirmed lines, and the new wording is hip-vo's, so the
> checkouts re-converge. The check_registry pin held Bill's own D-28
> wording; changing it is DELIBERATE, not a correction of an error. Heed
> D-116's finding: the pin is split across two adjacent source strings, so
> a whole-literal grep false-zeros — verify wrap-tolerantly and report the
> method. Fix the guard's hardcoded copy properly. Prove strip behavior
> unchanged by before/after on real prompts — a change is a STOP. Pins:
> 13–15/17 memory harness, failures ⊆ {115,116,117,118}, 16/17 is a STOP.
> Rule nothing MET.

## THE EDIT — EIGHT SITES, NOT SEVEN

**D-115's "seven sites" was itself a victim of the wrap hazard it named.**
The wrap-tolerant scan (method below) found an EIGHTH site the survey's
repo-wide grep missed, for exactly the reason D-116 predicted greps miss
things here: the literal was wrapped across two source lines.

Live-code sites, all moved in one change-set before any verification ran:

1. `harness/orchestrator.py` — `SECTION_OTHER_PEOPLE` constant → `"Facts
   about other people"`. The whole constants block moved ABOVE
   `PERSONAL_FACT_GROUNDING_GUARD` so the guard can interpolate it.
2. `harness/orchestrator.py` — the guard's prose copy (D-115 site :129, the
   silent-miss hazard): now an f-string interpolating
   `SECTION_OTHER_PEOPLE`. One source, both directions — TD-137's lesson,
   same as D-114's marker text. (The guard's shortened "Recent context" /
   "Things you know" references are prefixes of the OTHER two headers —
   different strings, not copies of this one; out of scope per the REQ.)
3. `harness/orchestrator.py` — derivation-design comment (D-115 site :174):
   re-pointed to name `SECTION_OTHER_PEOPLE` instead of quoting the old
   text. History is referenced, not rewritten and not falsified.
4. `harness/orchestrator.py` — `local_system_prompt` docstring (D-115 site
   :429): now names the new header.
5. `harness/orchestrator.py` — `_personal_section_pattern` docstring (D-115
   site :770): re-pointed to the constant name.
6. `eval/harnesslib/check_registry.py` — the `L7:CTX-STRIP` ground-truth
   fixture pin. Re-pinned to the new literal, provenance comment re-cited
   to this ruling and stating the change of Bill's D-28 wording is
   deliberate. **Now on ONE source line** — the wrapped two-string shape is
   what evaded the greps; the single-line form kills that hazard at the
   root, and the battery pins it (`test_hdr_pin_is_single_source_line`).
7. **THE EIGHTH SITE** — `eval/harnesslib/layer7_crypto.py:1697`, the
   CTX-STRIP "(ii) D-28's own triggering shape" check LABEL, old literal
   wrapped across two adjacent strings. It describes what the check
   populates NOW, so it must say the current header: it interpolates
   `SECTION_OTHER_PEOPLE` (imported as `_ctx_other_header`) — derived, not
   re-copied.
8. `logs/harness_results.json` (D-115 site 7) — **deliberately NOT
   edited.** Gitignored, inert stored prompts from past runs; nothing
   re-reads it for stripping (D-115 verified). Hand-editing a run record
   would falsify history. It regenerates with the new header on future
   runs. 2 occurrences remain there at dispatch time; reported, not
   hidden.

## VERIFICATION METHOD (D-117 step 3) — and why it cannot false-zero

Three-path scan, none of which depends on a literal sitting on one line:

- **.py string constants: ast walk.** Python resolves implicit
  adjacent-literal concatenation AT PARSE TIME, so a wrapped literal
  arrives as one Constant value. f-string fragments are Constants inside
  JoinedStr; docstrings are Constants.
- **.py comments:** every `#` line's marker stripped, lines joined, then
  whitespace collapsed — a comment wrapped across lines rejoins before
  matching.
- **all other tracked text:** raw match PLUS whitespace-collapsed match.

**Result, read as values (not exit codes, per CLAUDE.md item 13):**
- LIVE CODE occurrences of the old literal: **0**
- docs/ occurrences: **47** — all records: verbatim Bill quotes in the two
  REQ versions, D-114/D-115 dispatch docs, the defect/debt registers'
  historical entries, INDEX rows. Records of what was true stay written.
- logs/ (gitignored): the 2 inert occurrences of site 8 above.

The scanner is not just dispatch evidence — it is a permanent battery case
(below), with the wrapped-pin and wrapped-comment shapes pinned RED so a
future wrapped reintroduction goes red instead of hiding.

## STRIP EQUIVALENCE (D-117 step 5) — proven, not inspected

Before/after capture on REAL prompts (`TurnOrchestrator.local_system_prompt`,
hand-supplied fact dicts, no graph): four cases — (A) all three sections
populated, mixed confirmed+asserted; (B) only other-people, D-28's own
triggering shape; (C) no sections; (D) A plus the grounding guard in-prompt
(intent="personal"). Frontier strip for all; mid-tier strip for A.

One normalization, disclosed: the prompt embeds the wall clock ("Right now
it is 7:32 AM…"), so the two legs differ by capture time no matter what the
code does; that single token is normalized on both sides. First comparison
run STOPPED on exactly that and was diagnosed to the clock line (case C —
sectionless, nothing renamed in it — differed only there) before the
normalization was added. Every other byte is compared.

**Result: every stripped output byte-identical before vs after** (A/B/D
frontier, A mid, C untouched-by-construction); the removed region identical
modulo the renamed text itself (D shows 2 occurrences: header + guard
prose). What leaves the device did not change. The STOP condition did not
fire.

## ACCEPTANCE (REQ items 6/8 + pin/guard coupling) — HDR-RENAME battery

`eval/test_header_rename.py`, 9 cases `test_hdr_*` (D-87 namespacing), wired
as the 21st standing battery in `scripts/run_harness.sh`:

- header true over a mixed confirmed+asserted prompt, through the real
  renderer; asserted line carries its marker under the renamed header
- render/strip closed loop: strip cuts exactly at the derived boundary
- hard zero: no fact-bearing section or fact value survives frontier strip
- old-literal zero over live code, wrap-tolerant (the scan above, as a test)
- fault twin RED: scanner must catch wrapped-pin, wrapped-comment, and
  plain shapes — a scanner that misses them fails the battery itself
- anti-vacuity: the same scanner must FIND the new literal at the known
  sites — an empty or misrooted walk cannot pass
- registry pin == live constant, and pin text present verbatim in
  orchestrator source (a one-sided rename goes red here AND in AUDIT)
- pin stays on a single source line (the wrap hazard, pinned)
- guard derives from the constant; no second hand-copy of the header in the
  guard's source segment (checked via ast, both directions)

**Mutant evidence, both directions, applied to the real tree and restored
byte-exactly:** reverting the registry pin to the old wrapped literal →
4 cases RED (pin-match, single-line, tree-scan, anti-vacuity); reverting the
constant alone → 5 cases RED (header-truth, old-literal-zero, pin-match,
single-line, guard-derivation). Restored → 9/9 green both times.

## HARNESS EVIDENCE, read individually

- Standing batteries (21, incl. HDR-RENAME): green — the runner's own
  `set -e` gate ran them before every harness pass below; HDR-RENAME also
  9/9 standalone, three times (initial + post-mutant-restore ×2).
- `--layer 7`: **L7 27/27** (0 flaked, 0 skipped), `four-part-roster PASS`
  (59 checks, 35 flagged gaps — unchanged), COVERAGE-GRID + RATCHET +
  SELFTEST PASS, mutation suite PASS with survivors accounted,
  **RATCHET PASS — no scenario regressed.**
- The two ABSOLUTE checks this could disturb, individually:
  **CTX-STRIP: PASS.** **PSA1: PASS.**
- `--full`, run TWICE (logs hip_harness_20260803_0743 and _0814; a third
  attempt between them was jetsam-killed at 0.06GB free before reaching
  the layers): AUDIT 8/8, DISC 1/1, L1 14/15, L2 25/35 (10 skipped),
  L3 3/3, L4 25/31 (4 skipped), L7 27/27, L7V2 27/28 (1 opt-in skip),
  SCHEMA 1/1, VOICE 1/1, COVERAGE-GRID-RATCHET PASS, CTX-STRIP / PSA1 /
  OB6 / G0 / LI1 individually PASS — all at baseline EXCEPT:
  **RATCHET NEW FAILURE, BOTH RUNS: `L6:record-invariants` — G1
  no-orphan-generation, ONE violation, the IDENTICAL record both times.**
  Root cause, evidenced not guessed: `[sam] "I take atorvastatin 20mg
  every morning."` (harness_run.jsonl smoke turn) — fact_change extraction
  returned zero changes, and the retry hit a Groq-side ReadTimeout
  (harness_server.log:77-78); the write dropped, the F3 gate honestly
  replaced the ack ("unable to save it to the household record"), and G1
  counts the orphan BY ITS OWN DOCUMENTED DESIGN (declarative with
  extraction failure is deliberately NOT exempt). The same utterance
  extracted fine elsewhere in the same runs (turns_demo.jsonl G1 PASS
  both times) — per-call service nondeterminism, the documented
  payload-biased Groq lineage (DISPATCH_MET_VERIFICATION 2026-07-26,
  DISPATCH_GROQ_400_ROOTCAUSE: "payload-biased coin, not deterministic"),
  now landing on this smoke payload. STRUCTURALLY UNREACHABLE by this
  dispatch: `harness/fact_change.py` contains zero references to the
  renamed constant or any section header, and the render/strip surface
  was proven byte-identical above. BASELINE NOTE, so nobody misreads
  D-114's row: D-114's "RATCHET PASS" was a --layer-7-scope run (its log
  has no L1-L6 blocks); the last true --full with L6 was 2026-07-30 —
  G1 PASS. Baseline NOT updated; the red is left LOUD per the
  DISPATCH_MET_VERIFICATION precedent; see OPEN.
  (TD-129 note: the runner's 2GB free-memory guard initially refused;
  freed by unloading an IDLE ollama model — qwen2.5:3b, 2 minutes from
  self-expiry, nothing had touched it — plus a kernel page-reclaim
  cycle. No other lane's service was touched; all four Neo4j instances
  left alone.)
- Memory harness: **14/17, failures exactly {MEM-115, MEM-116, MEM-117}**
  — within the 13–15/17 pin, failures ⊆ {115,116,117,118}, NOT the 16/17
  too-good STOP. Delta vs D-114's 15/17 {115,116}: MEM-117 ("no active
  medication fact for (maya, ray) after supersede") newly red — the same
  live-write/fact_change family as the L6 finding below, inside the pin's
  anticipated set, reported not smoothed.

## PROCESS NOTES

- Machine gate passed (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap
  / roadmap). `.hip-lock` taken FIRST, 2026-08-03T07:26:10-0600, before any
  write including the REQ revision.
- Repo `.env.dev` sourced exclusively (directly and via run_harness.sh's
  own sourcing). No other env file touched.
- Parallel-lane: committed AROUND the cutover lane's WIP — their modified
  `docs/INDEX.md` rows and four untracked dispatch docs left exactly as
  found; explicit pathspecs; surgical INDEX stage (save full copy → stage
  only this lane's rows → restore).

## VERIFIED

- **Watched runs:** the before/after strip captures and comparison; the
  HDR-RENAME battery ×3 including two real-mutant RED/restore cycles;
  `--layer 7`; `--full`; the memory harness. All outputs read as values.
- **Reasoned about:** logs file inertness (from D-115's caller analysis,
  re-checked: gitignored, nothing re-reads it); the guard's shortened
  first-two section references being prefixes of OTHER constants, not
  copies of this one.

## OPEN

- **The re-ruling itself**: the REQ revision is filed NOT MET and proposes
  READY FOR RE-RULING with this dispatch as evidence — with the L6 red
  attached and explained, not hidden behind it. Bill decides. Nothing
  ruled MET here.
- **`L6:record-invariants` red needs its own dispatch, not this REQ's.**
  The sam/atorvastatin smoke-turn extraction failed both attempts in both
  --full runs today while succeeding in turns_demo the same runs — the
  Groq payload-bias has shifted onto a new payload since the 2026-07-30
  green --full (the July occurrence was care_coordination's Elena
  payload, root-caused and closed at DISPATCH_GROQ_400_ROOTCAUSE). Same
  family as MEM-117's new red (live fact_change write). Handoff, same
  shape as DISPATCH_MET_VERIFICATION's: diff this smoke payload's
  fact_change request against a same-run succeeding one at the call
  site. NOT chased here — out of this dispatch's scope, and the working
  path (F3's honest refusal) behaved exactly as designed throughout.
- hip-vo convergence: this header now matches hip-vo 517dd7c. The guard
  prose differs by construction (roadmap interpolates; hip-vo carried
  dict + prose copies pre-TD-137) — convergence of TEXT, not of source
  layout. No hip-vo change made from this lane.
- `logs/harness_results.json` still carries 2 old-literal occurrences as
  inert history until the next run that rewrites it.
