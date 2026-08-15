# DISPATCH_RULING_D128
Status: BUILT (governance only; no code changed)
Reconciled-Against: 2026-08-03 (D-128; parent 829464f at dispatch time)

**TYPE:** GOVERNANCE / RULING-RECORD + TD FILINGS

**REQ:** `REQ_STRUCTURAL_REFUSAL__adjacent-admissions-must-not-suppress-
empty-set__v20260803_1108.md` — the subject of the ruling. No build; no
code changed (D-128 step 5).

## SEQUENCING NOTE

D-128 arrived while D-127's full ratchet was still in flight. Per the
ruling's own guard ("if ANY of the above is not true in the final run, DO
NOT RULE"), the ruling was NOT recorded until D-127's runs completed and
each cited point was verified against them. D-127 committed first
(829464f); this dispatch follows. One lock covered both, annotated to say
so.

## 1. THE RULING — verified, then recorded

Each evidence point, checked against the FINAL runs (pairwise twice + the
full ratchet + the battery in every pass) before recording:

1. PW031-033 refuse structurally — `guard.kind='empty_set'`,
   `inference_ms=None`, model not called: TRUE in all three L4 passes. ✓
2. PW010 flipped to structural PASS, closing TD-143's red: TRUE. ✓
3. The fault twin reproduces the pre-fix mechanism and goes red
   (cannot pass vacuously): TRUE — the twin's red-direction assertion
   held in every battery pass (323-case suite green). ✓
4. No flip between runs; deterministic: TRUE — row-identical results. ✓
5. PW011/PW012 disclose exactly as before; INJ-7 untouched,
   battery-proven: TRUE. ✓
6. Resolution is not disclosure — admitted-set counts unchanged on every
   existing row: TRUE (unit assertion + live rows). ✓

**All six held → REQ_STRUCTURAL_REFUSAL is RULED MET (Bill, 2026-08-03),
recorded in the REQ's MET-Ruling block** with the three non-coverages the
ruling names: keying (3) is TD-149 (untargeted attributes still have no
structural path); TD-136 remains live (INJ-4 household exemption, its own
filing); PW016/PW018 still SKIP on unimplemented retract-without-
successor. The subject-knownness residual (D-127, ruling b) stands
recorded. The filing-time STATUS paragraph is retained for provenance.

## 2. TD-143 / TD-144 — STATUS PROPOSED, NOT SELF-RULED

- **TD-143: PROPOSED RESOLVED** — closed by D-127's fix. PW010 refuses
  structurally in three consecutive runs; the mechanism (resolution
  blindness) is D-126's trace; the baseline row flipped true via the
  sanctioned path. Bill rules.
- **TD-144: PROPOSED RESOLVED-BY-CORRECTION-AND-REQ** — the headline was
  corrected on the record (D-125/D-126: no dad-medication fact exists;
  sam owned the admitted content; nothing leaked); the row's expectation
  was itself the defect, corrected at D-127 per ruling (d), now green;
  its "needs its own REQ" is satisfied by REQ_STRUCTURAL_REFUSAL (MET),
  with residues scoped in TD-149 and TD-136. Bill rules.
Both proposals recorded as ADDENDA in the register (v20260803_1332),
original filings kept intact.

## 3. TD-150 FILED — the baseline updater is a record-integrity hazard

Register v20260803_1332, OPS. Two governance-relevant side effects in two
days, both caught only in diff review, neither announced by the tool:
D-126's `--accept` text applied to EVERY red row (clobbering TD-143's,
TD-144's, and L1:P2's justifications); D-127's plain `--update-baseline`
dropping the ENTIRE `_accepted` map including L1:P2's still-live entry
for a row that did not even run in that invocation. The justifications
carry defect IDs and Bill's rulings; the tool treats them as derived
state. Fix scoped, not built: per-row accept targeting with a refusing
global form; preserve-by-default (entries only retire when their row
flipped to passing in THIS run, printing the retired text); refuse to
drop a still-red row's justification; print an `_accepted` diff at write
time; a round-trip-stability battery case. UNGOVERNED — needs Bill's REQ
or DEFECT ruling before a build.

## 4. CEILING PREAMBLE — NO CHANGE from this ruling, checked as values

Zero references to REQ_STRUCTURAL_REFUSAL in either ceiling REQ (grep
count 0 in both; it postdates them). The split does not move. The
PRE-EXISTING staleness D-120 flagged — the header says "FIVE ARE RULED"
omitting R12 (six are ruled), and the §16 intro line still reads "R18
NOT MET (D-88)" against the D-113 MET entry in the same file — STANDS
UNFIXED: D-128's step 4 is conditional on THIS ruling changing the split,
which it does not, and D-120's instruction was explicit ("do not fix it
here"). Flagged now for the fourth and fifth time; fixing it needs its
own instruction.

## PROCESS NOTES

- Gate passed. The D-127 lock (read-first, noclobber, 12:42:41) was held
  through both dispatches, annotated with the sequencing note; released
  after this push. Repo `.env.dev` only. No code changed.
- Committed AROUND the cutover lane's WIP — explicit pathspecs, surgical
  INDEX stage.

## OPEN

- TD-143 and TD-144: proposals await Bill's ruling.
- TD-149 (untargeted attributes) and TD-150 (updater): await REQs or
  DEFECT rulings.
- The ceiling-preamble staleness: awaits its own instruction.
- Nothing else ruled.
