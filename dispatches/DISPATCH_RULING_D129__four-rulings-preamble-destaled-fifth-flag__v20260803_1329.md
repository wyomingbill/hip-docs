# DISPATCH_RULING_D129
Status: BUILT (governance + doc corrections; no code changed)
Reconciled-Against: 2026-08-03 (D-129; parent 32cb04f at dispatch time)

**TYPE:** GOVERNANCE / RULING-RECORD + REQ FILINGS + DOC CORRECTION

**REQ:** NONE for the rulings and the preamble fix (governance records and
a doc correction under Bill's unconditional instruction — no code, no
build); the two REQs FILED here are artifacts of this dispatch, not its
authority.

## 1. THE FOUR RULINGS (Bill, 2026-08-03), recorded

**(a) TD-143 RULED RESOLVED** — closed by D-127's fix, three consecutive
structural runs. Register row status → RESOLVED (v20260803_1331).

**(b) TD-144 RULED RESOLVED-BY-CORRECTION-AND-REQ**, as proposed — with
the ruling's own record, in the row: the ORIGINAL HEADLINE WAS WRONG (no
dad-medication fact existed; sam owned the admitted content; nothing
leaked), and the CORRECTION, not a fix, is half of why it closes.
Residues stay in TD-149 and TD-136.

**(c) TD-149 gets a REQ — FILED, NOT built:**
`REQ_ASKED_ATTRIBUTE_COVERAGE__structural-refusal-for-untargeted-
attributes__v20260803_1329.md`, Status NOT MET. Bill's ruling verbatim as
THE REQUIREMENT; acceptance sketch fixes the shape (SIO-derived asked
with fallback keeping today's keyword behavior byte-for-byte; L4 rows for
the PW014/PW017 shape graded from the record; a NO-OVER-FIRE battery
honoring the :272 rationale by evidence, with a twin proving keyword-
widening would over-fire; the REQ_STRUCTURAL_REFUSAL non-regression set;
full RATCHET). One STOP pre-wired: SIO attribute-classification
reliability must be measured before the guard consumes it.

**(d) TD-150 gets a REQ — FILED, NOT built:**
`REQ_BASELINE_RECORD_INTEGRITY__updater-preserves-accepted-
justifications__v20260803_1329.md`, Status NOT MET. Bill's ruling
verbatim; both incidents recorded as evidence; acceptance is TD-150's
five-way scope verbatim (per-row targeting with refusing global form,
preserve-by-default with retired-text printing, still-red/-unrun refusal,
write-time _accepted diff, round-trip battery with twins for both
incidents).

## 2. THE CEILING PREAMBLE — DE-STALED, fifth flag, first unconditional instruction

Both fixes applied in place to REQ_STRUCTURAL_CEILING v20260802_2205,
each annotated rather than silently corrected:
- **Header**: "FIVE ARE RULED" / "25 of 30" → **"SIX ARE RULED" / "24 of
  30"**, with **R12 MET (D-103)** inserted where the D-113 re-count had
  omitted it. The parenthetical now records: re-counted D-129; the D-113
  re-count itself omitted R12 — the FIFTH staleness of this line (flagged
  D-88, D-92, D-100, D-120), fixed on Bill's first unconditional
  instruction.
- **§16 intro**: "NOT MET: R10 (D-100), R18 (D-88)" → **R18 moved to MET
  (D-113, on the D-111-amended rule)**, with the supersession noted in
  the line itself; "NOT MET: R10 (D-100)" only. Its own staleness
  parenthetical updated THREE→FOUR times, naming D-113's edit as the
  breaker of its "updated in the same edit" promise — restated, not
  trusted.
- Verified as values post-edit: zero "R18 (D-88)" strings remain; header
  and §16 now agree with §16's individual entries (the consistent record)
  everywhere.

## 3. CAN THE PREAMBLE BE MADE UNABLE TO GO STALE? — PROPOSED, NOT BUILT

A count is a claim that ages; a pointer is not. Two shapes, first one
recommended:

**(i) DELETE THE COUNT — the pointer shape (recommended, matches Bill's
own framing).** The header carries no numbers and no enumeration: only
"Rulings are recorded per-requirement in §16, which is the sole
authoritative record; this header intentionally carries no count." A
pointer cannot age. Cost: no at-a-glance summary — which five flags in
five weeks suggest was never actually reliable enough to glance at.

**(ii) KEEP THE COUNT, MAKE STALENESS RED — the derived-check shape.**
The count stays but an AUDIT-block check derives the MET/NOT-MET split by
parsing §16's own `### R<n> — **<STATUS>**` headings (first heading per
requirement wins, matching "§16 governs") and FAILS the harness when the
preamble's numbers disagree. Staleness becomes a red check instead of a
silent lie. Cost: a parser with its own failure modes, and the count
still lies between the edit and the next run.

Either is Bill's to pick; (i) is one edit, (ii) is a small build under
its own REQ if wanted.

## PROCESS NOTES

- Gate passed; lock read-first (free), noclobber take 13:29:32; released
  after push. Repo `.env.dev` only. No code changed.
- One self-caught naming-law violation: the register version was first
  written with a nonconforming stamp suffix (`v20260803_1329d129`) and
  renamed to `v20260803_1331` before anything referenced it.
- Committed AROUND the cutover lane's WIP — explicit pathspecs, surgical
  INDEX stage.

## OPEN

- REQ_ASKED_ATTRIBUTE_COVERAGE and REQ_BASELINE_RECORD_INTEGRITY await
  executing dispatches (item 8).
- The preamble-shape proposal awaits Bill's pick.
- Nothing ruled MET in this dispatch beyond the two TD rulings recorded.
