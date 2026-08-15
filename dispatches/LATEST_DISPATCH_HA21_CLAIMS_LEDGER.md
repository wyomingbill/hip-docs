# DISPATCH_HA21_CLAIMS_LEDGER — banked verbatim, CLAIM IMPACT rule added, generator filed

Status: BUILT (docs only — no code, nothing MET)
Reconciled-Against: roadmap `1f110cb` (pre-dispatch HEAD)

**HA-21** | 2026-08-09 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BANKING + GOVERNANCE**
**AUTHORITY:** Bill's ruling 2026-08-07, pasted into this dispatch.
**NO CODE CHANGED. NOTHING MET. The status generator was deliberately NOT built.**

---

## 1. ITEM 2 — TRUNCATION CHECK: **PASS**, both ends

Run on the written file, not on the paste:

```
FIRST LINE : # HIP CLAIMS LEDGER
LAST LINE  : END OF LEDGER v1
claim rows : 13
body sha256: 611838a9c2bbf6768c73bd82db8a7d1b7a6834896c8ec0b340e6f1d313eb3456
```

Both markers match exactly, so nothing was written under a truncated paste.

## 2. ITEM 1 — PLACEMENT: `docs/deliverables/`, and the folder law permits it

`docs/deliverables/HIP_ClaimsLedger__canonical-progress-instrument-13-claims__v20260809_1906.md`

**No STOP was required and no new folder was created.** The reasoning, since item 1 made
placement a gate:

- CLAUDE.md's LOCKED folder list has `docs/deliverables/` as *"canonical WP, NDA, and annex
  deliverables … MANIFEST.md governs what belongs here."* **The ledger is a canonical
  instrument governed by a MANIFEST row — that is exactly this folder's job.**
- **The instruction itself settles it.** Item 1 says *"Register in INDEX + MANIFEST Section
  B."* Section B is `docs/deliverables/`'s own canonical-version table; **no other folder is
  described by a Section B row**, so any other placement would make item 1's own
  registration instruction incoherent.
- **The folder already holds markdown, not only binaries** — including
  `HIP_ClaimsRegister__v20260727_1729.md`, its nearest relative. Precedent, not exception.
- `docs/status/` was considered and **rejected**: its own charter says *"Written by tooling,
  never by hand."* v1 is hand-written. It may become a *rendering target* of the generator,
  but the ledger source is not a generated board.

## 3. ONE DEVIATION, FLAGGED RATHER THAN SILENTLY EDITED

The banked content's own header reads:

```
Status: v1 DRAFT — claim wording awaits Bill's ruling; …
```

**`v1 DRAFT` is not one of the Naming Law's enumerated Status values**
(PLAN / IN_PROGRESS / BUILT / SUPERSEDED / STALE).

**Not corrected, and that is a decision rather than an oversight.** Item 1 says *verbatim*
and item 2 pins the exact first line, so a governance header could not be added above it and
the Status line could not be reworded without changing banked content. **Banked content is
Bill's to reword — a session that "fixes" a ruling's wording has quietly rewritten it**,
which is the failure the banking discipline exists to prevent (HA-12/HA-13 precedent). The
deviation is recorded here, in the INDEX row and in the MANIFEST row. **If Bill wants the
enumerated vocabulary, it is a one-word supersede and his call.**

## 4. NOT THE SAME DOCUMENT AS THE EXISTING CLAIMS REGISTER

`docs/deliverables/` now holds two similarly-named artifacts, and conflating them would
be easy and costly:

| | `HIP_ClaimsRegister__v20260727_1729.md` | **`HIP_ClaimsLedger` (this one)** |
|---|---|---|
| what it registers | claims the NDA package makes **in prose** | claims about **what the system does** |
| purpose | read-only AUDIT RECORD of package accuracy | **canonical progress instrument** |
| statuses | PROVEN / DESIGNED / ASPIRATIONAL / **WRONG** / UNVERIFIED | PROVEN / PARTIAL / UNPROVEN, **computed once the generator lands** |
| feeds | nothing | the **public test-results page**, from the same computation |

Stated in the MANIFEST row as well, so the distinction survives outside this dispatch.

## 5. ITEM 3 — CLAIM IMPACT LINE ADDED TO THE STANDARD PREAMBLE

Added as **item 11**, at the END of the preamble:

```
CLAIM IMPACT: C-02, C-03 — author validity enabled; both now carry standing evidence
CLAIM IMPACT: none
```

Three things the rule pins, because each is a way it could quietly fail:

1. **"none" is a real answer and MUST be written.** An absent line is indistinguishable from
   a forgotten one.
2. **It is a POINTER, NOT A RULING.** Naming C-11 does not make C-11 PROVEN. **Status is
   computed, never declared** — and once the generator lands, no session hand-edits one.
3. **Placed at the end deliberately.** Inserting it at 7 would have renumbered items 7-10,
   and **this preamble's own item 10 forbids renumbering identifiers other documents already
   cite.** The first draft of this edit did insert at 7; it was reverted for that reason.

## 6. ITEM 4 — THE GENERATOR IS FILED, NOT BUILT

Filed at the top of `docs/BACKLOG.md` as **NAMED NEXT BUILD — UNGOVERNED (needs a REQ)**,
carrying the two constraints most likely to be lost between here and the build:

- **ONE computation, two renderings.** The ledger's own rule is that the public page *"may
  never exceed this ledger."* Two computations can drift, and the dangerous direction is a
  public page claiming more than the evidence supports; one computation makes that
  structurally impossible instead of a review item.
- **The `Timeline` column must never touch a status** — *"forecast only and can never
  influence a status or weaken an acceptance."* A generator that reads it into a status has
  broken the instrument.

Also recorded: the claim WORDING is still v1 DRAFT awaiting Bill's ruling, so a REQ written
before that should say so.

## 7. WHAT WAS NOT DONE

- **No status generator** (item 4 forbids it here).
- **No status was assessed, changed or ruled by this dispatch.** The 13 statuses are exactly
  as pasted. Item 5's marking requirement was already satisfied by the content's own header,
  so nothing was added to satisfy it.
- **No claim wording touched.** Item 5 reserves that to Bill.
- **No runs.** Docs only; no repository code changed, so `--layer 7`/`--full` would
  re-measure HA-19's tree unchanged.

## 8. CLAIM IMPACT

**CLAIM IMPACT: none.** This dispatch produced no evidence about system behaviour — it banked
the instrument that will carry such evidence. **The first dispatch bound by item 11 is the
next one.**

*(Recorded here as the rule's own first observance: the dispatch that created the rule
follows it, including writing "none" rather than omitting the line.)*

**Worth flagging for Bill, since HA-19 landed one dispatch earlier and the ledger predates
it:** the pasted v1 lists **C-02 and C-03 as PARTIAL with "enablement = HA-19"**, and
**C-11 as UNPROVEN, "expected at HA-19."** HA-19 has since landed — both guards live, C1
11/11 — **and its `--full` ratchet FAILED**, so C-11's expectation did not hold. **Those
statuses are not adjusted here**: v1's statuses are draft, this dispatch rules nothing, and
the generator will compute them from standing runs. Named so the gap is visible rather than
discovered later.

## 9. FINDINGS

1. **Banked verbatim, truncation-checked both ends** (§1) — 13 claims, sha256 recorded.
2. **Placement is lawful without a new folder** (§2); `docs/status/` rejected on its own
   "never by hand" charter.
3. **One header deviation flagged, not silently fixed** (§3) — `v1 DRAFT` is outside the
   Naming Law's vocabulary, and banked content is Bill's to reword.
4. **Two similarly-named claims documents now coexist** (§4) and the distinction is recorded
   in the MANIFEST, not only here.
5. **CLAIM IMPACT is item 11, not item 7** (§5) — inserting mid-list would have renumbered
   identifiers the preamble itself forbids renumbering.
6. **HA-19 has already overtaken three of v1's draft statuses** (§8) — recorded, deliberately
   not adjusted.
