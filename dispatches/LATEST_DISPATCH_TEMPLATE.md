# DISPATCH_TEMPLATE
Status: BUILT
Reconciled-Against: 2026-07-16

Copy this template for every dispatch that produces a finding, a
measurement, or a code change. File it as
`docs/dispatches/DISPATCH_<SUBJECT>__<slug>__v<YYYYMMDD_HHMM>.md` (Mountain
Time — the time of the dispatch/work, not the time a later session happens
to backfill it), register it in docs/INDEX.md, and write it AS PART OF THE
WORK, not after. See CLAUDE.md Requirements Discipline.

Requirements docs cover what gets BUILT. This covers what gets ASKED,
TRACED, and MEASURED — including work that never touches code. A dispatch
doc is not a substitute for a REQ doc: BUILD dispatches reference their REQ;
ANALYSIS and MEASUREMENT dispatches may have none, and say so plainly rather
than inventing one.

Before starting any analysis, grep `docs/dispatches/` for whether this
question has already been traced. If it has, read that doc first and say
what is new in this one — do not re-trace from zero.

Fill every section. VERIFIED is not optional — say plainly which claims were
watched actually run and which were reasoned about from code alone. Three
artifacts on 2026-07-15/16 passed structural proof and failed live; this
section exists so that distinction is never silently lost again.

---

# DISPATCH_<SUBJECT>
Status: PLAN | IN_PROGRESS | BUILT | SUPERSEDED | STALE
Reconciled-Against: <commit-hash or date>

**TYPE:** BUILD | ANALYSIS | MEASUREMENT | PROCESS

**REQ:** the requirements doc this dispatch serves
(`docs/requirements/REQ_<...>.md`), or **NONE** with the reason it has none
(analysis/measurement dispatches routinely have none — say so, don't invent
one to fill the field).

## THE ASK

The dispatch text, verbatim, as given. Not a summary, not a paraphrase — the
actual words, quoted in full, the same discipline THE REQUIREMENT uses in a
REQ doc.

## WHAT WAS DONE

What was actually undertaken in response — the concrete steps, in the order
taken. Not the conclusion; the path to it.

## WHAT WAS FOUND

Findings with `file:line` for every code claim, and exact numbers for every
measurement. No claim about the codebase without a citation a reader can
open and check.

## VERIFIED

Split explicitly:
- **Watched run:** what was actually executed and observed (a live turn, a
  measured score, a passing/failing test) — with enough detail that another
  session could reproduce the observation.
- **Reasoned about:** what was concluded from reading code or from a prior
  doc, without an independent run to confirm it. Not lesser work — just a
  different kind, and the reader must be able to tell which is which.

## HASH

The commit this dispatch shipped, or **NONE** for analysis/measurement-only
work. If NONE, say why (no code changed, doc-only, blocked, etc.).

## OPEN

What this dispatch did NOT answer. The next question it raises, the
follow-up it's blocked on, or the scope it explicitly left out. A dispatch
doc that closes with nothing open is either the last word on the subject or
has not been read skeptically enough.
