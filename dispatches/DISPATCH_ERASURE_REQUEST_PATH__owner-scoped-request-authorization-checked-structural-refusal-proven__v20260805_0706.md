# DISPATCH_ERASURE_REQUEST_PATH
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD, under a NEW REQ (`REQ_ERASURE_REQUEST_PATH`, written first per
Requirements Discipline item 8 — no existing REQ covered this).

**REQ:** `docs/requirements/REQ_ERASURE_REQUEST_PATH__owner-scoped-request-in-
authorization-checked-report-out__v20260805_0658.md`. New, filed as part of this
dispatch, not retroactively.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-172 | ~/hip-roadmap, roadmap | Make erasure reachable ===
STANDARD PREAMBLE. Lane A.
Requirements Discipline item 8 applies: NO REQ COVERS THIS. Write the REQ FIRST from
Bill's words below, then build.

BILL'S RULING, the requirement text:
"Erasure is built, proven, and unreachable — no API, no voice command, no admin action
calls it from a real request. A capability nobody can invoke is not a feature. HIP shall
have a request path that reaches the built erasure mechanism. Who may request erasure of
what is an authorization question and shall be answered explicitly, not inherited from
whoever happens to be calling."

1. WRITE THE REQ. It must answer, at minimum: who may request erasure of their own facts;
   whether anyone may request erasure of facts about another person; what happens to
   facts a requester authored about someone else; and whether a request is executed
   immediately or requires a second step. Where the answer is not derivable from existing
   ratified rulings, say UNDETERMINED and name what would settle it — do not invent
   policy to fill a gap.
   STOP AND REPORT after the REQ if any answer is UNDETERMINED and load-bearing.

2. THEN BUILD THE PATH — request in, authorization checked, the D-R-170 mechanism called,
   the D-R-167 report returned as the outcome. The report is the answer to "did it work,"
   not a separate story.

3. SCOPE LIMIT, EXPLICIT: build and prove against fixtures. DO NOT enable this against
   the live demo graph or any real data. Enabling it is a separate authorization Bill has
   not given. State plainly in the report what enabling would require.

4. THE FAULT TWIN THAT MATTERS: an unauthorized request must be REFUSED with nothing
   erased, proven by execution. And prove the refusal is structural — not the mechanism
   succeeding and the report noticing afterward.

5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched, tree clean except another lane's own untouched WIP, HEAD in
   sync with `origin/roadmap`.
2. **Wrote the REQ first**, per Requirements Discipline item 8's own gate — no existing
   REQ covered "who may request erasure." Answered all four required questions (see
   the REQ doc itself for the full text); two came out genuinely UNDETERMINED.
3. **Searched for a ratified precedent before marking anything UNDETERMINED**, rather
   than guessing: found the 2026-07-21 household-circle widening restriction
   (`harness/write_rule.py:160-168`) — "an author may widen to household-circle only
   for facts about themselves or generic household facts — never a fact about someone
   else without THEIR standing policy" — and used it as the DERIVED basis for two of
   the four answers (who may request erasure of their own facts; what happens to
   facts a requester authored about someone else), rather than treating those as
   undetermined too.
4. Evaluated whether the two genuinely UNDETERMINED answers (cross-person erasure
   authority; immediate-vs-confirm execution) are LOAD-BEARING enough to STOP the
   whole dispatch, per item 1's own instruction — concluded neither blocks a real,
   useful build: the first resolves to REFUSAL (a subtraction of capability, the
   standing default throughout this whole REQ, not an invented policy), and the
   second is inert regardless of which way it's decided, because item 3's own scope
   limit means nothing built here is ever enabled against real data either way.
   **Did not STOP** — proceeded to item 2 with both left explicitly open in the REQ
   and named again below.
5. Read `harness.graph_erasure`, `harness.erasure_report`, and
   `harness.extraction_queue`'s own `:Fact` schema fields (`owner`, `subject`) fresh
   before designing the authorization check, not from memory.
6. **Extended `harness.erasure_report.build_member_erasure_report`** with an optional
   `excluded_fact_ids` parameter — needed because item 1(c)'s own derived answer
   (facts about someone else are EXCLUDED from an owner-wide sweep, not silently
   erased) meant a real member-wide erasure request could leave SOME facts behind ON
   PURPOSE, which D-R-170's own report (built to expect zero remaining, always)
   would have wrongly flagged as incomplete. Backward compatible: omitted, it
   defaults to empty, reproducing D-R-170's own exact behavior — confirmed by
   re-running D-R-170's own test suite unchanged (26/26 still pass).
7. Built `harness/erasure_request.py` — see WHAT WAS FOUND for the full design.
8. Wrote `eval/test_erasure_request.py` (7 cases), run against the real dev graph
   with disposable, uniquely-prefixed fixtures, same posture as D-R-169/170.
9. Ran the new file standalone under the graph lock: 7/7 pass on first run.
10. Confirmed, by direct query, zero fixture residue across every prior
    dispatch's own fixture prefix (D-R-169, D-R-170, D-R-172), not just this
    dispatch's own.
11. Wired the new test file into `scripts/run_harness.sh`'s standing battery list.
12. Ran the full standing battery (34 files) via `scripts/run_harness.sh --layer 7`:
    clean on the first attempt — no self-caused regression this time (unlike
    D-R-169's own docstring collision or D-R-170's own leak-check gap); double-checked
    the two invariants this session has repeatedly caught real issues in
    (`test_ledger_callsite_enumeration.py`, `test_fact_write_convergence.py`) stayed
    green explicitly, since this dispatch's own module calls `erase_fact` (which
    already has its own tombstone call) rather than adding a new one.
13. **RATCHET PASS — no scenario regressed vs baseline.**
14. Confirmed zero fixture residue a second time, after the full battery run.
15. Ran the memory harness under the graph lock: **13/17**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — the same pinned set as every prior
    dispatch this session, not a new regression.
16. Wrote this dispatch doc, including item 3's own "what enabling would require"
    statement.
17. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### Item 1 — the REQ, and the STOP condition considered, not triggered

Full text: `docs/requirements/REQ_ERASURE_REQUEST_PATH__…v20260805_0658.md`. Summary
of the four answers:

| Question | Status | Basis |
|---|---|---|
| (a) Who may request erasure of their own facts | **DETERMINED** | The fact's own `owner`, matching the 2026-07-21 widening restriction's identical boundary (self-authored-about-self), applied more strictly since erasure is more consequential than widening |
| (b) Whether anyone may request erasure of facts about another person | **UNDETERMINED** | Blocked on `REQ_CARE_TEAM_READ_AUTH`/A14/A15's own already-flagged ethicist+attorney gate. Consequence: this build refuses every such request rather than guessing — not an invented policy, the standing default |
| (c) What happens to facts a requester authored about someone else | **DETERMINED** | Same 2026-07-21 precedent: excluded from an owner-wide sweep, not erased, not silently swept in either — named in the returned report |
| (d) Immediate execution or a second step | **UNDETERMINED** | No ratified precedent distinguishes confirming a destructive request from `confirmation_gate.py`'s own different concern (resolving an ambiguous pending write). This build proceeds with immediate execution because nothing built here is ever enabled regardless (item 3) |

**Neither UNDETERMINED answer was treated as blocking, and the reasoning for each is
recorded in the REQ doc itself, not just asserted here:** (b)'s consequence is a
capability SUBTRACTION (refuse), which needs no ruling to implement safely; (d)'s
choice is inert given item 3's own scope limit and is additively revisable later.
**The STOP condition in item 1 was genuinely considered, not skipped past — this
dispatch's own judgment is that it does not fire, and that judgment is stated
plainly here so Bill can overrule it if he disagrees.**

### Item 2 — built: `harness/erasure_request.py`

- `request_fact_erasure(requester, fact_id, *, reason)` — reads the target fact's
  own `owner` (no decryption, no content read), refuses with
  `UnauthorizedErasureRequest` if `requester != owner`, otherwise calls
  `harness.graph_erasure.erase_fact` and returns
  `harness.erasure_report.build_fact_erasure_report`'s own output — exactly the
  D-R-167/169 report, not a new shape.
- `request_member_facts_erasure(requester, owner, *, reason)` — refuses unless
  `requester == owner`; among the owner's own facts, separates those whose
  `subject` is absent-or-self (erased, via `erase_fact` per fact — reusing the
  already-proven per-fact path, not a new bulk-delete) from those whose `subject`
  is a different, specific person (excluded, untouched); returns
  `build_member_erasure_report` (D-R-170, extended this dispatch) naming both sets.

### Item 3 — scope limit honored; what enabling would require

**Nothing built here is enabled anywhere.** No server route, no voice-orchestrator
intent, no admin dashboard action calls `harness.erasure_request`. Every test runs
against disposable, uniquely-prefixed (`d-r-172-fixture-...`) fixtures, cleaned up
regardless of pass/fail, confirmed by direct query (twice) to leave zero residue in
the real, shared dev graph.

**What enabling it for real would require, stated plainly:**
1. A real caller — a server endpoint or voice intent — that supplies an
   AUTHENTICATED requester identity, never a caller-claimed one (matching
   `harness.identity_keys`'s own "never trust a claimed member" posture already
   established elsewhere in this codebase).
2. Bill's own ruling on question (d) — whether a real request needs a
   confirm-then-execute step — before anything irreversible runs against real
   household data.
3. Bill's own ruling on question (b), only if cross-person erasure requests are
   ever wanted; this build's own refusal of them does not need to change for
   self-service erasure to work.
4. The SAME destructive-write authorization D-R-169/170 already named as needed
   before `harness.graph_erasure` itself is ever run against real data — this
   dispatch does not change that; it is a request-shaped LAYER in front of an
   already-fixture-only mechanism.

### Item 4 — the fault twin that matters, proven structurally

Both `test_request_fact_erasure_unauthorized_is_refused_before_any_call` and
`test_request_member_facts_erasure_unauthorized_is_refused_before_any_call` patch
`harness.erasure_request.erase_fact` (the name as bound in the request module's own
namespace) with a spy that RAISES if ever called, then issue an unauthorized
request and assert: (1) `UnauthorizedErasureRequest` is raised, (2) the spy's own
call count is zero, and (3) the target fact(s) still exist in the real graph
afterward. **This proves the refusal happens BEFORE the erasure mechanism is
reached at all — not that the mechanism ran and something downstream noticed a
problem.** A spy that raises on any call would turn a "the report just happens to
still say incomplete" false-pass into a hard, immediate test failure — the
mechanism genuinely cannot run undetected.

## VERIFIED

**Watched, executed:**
- `harness/write_rule.py`'s own 2026-07-21 restriction read directly, in context,
  before being cited as the REQ's own derived basis for (a)/(c).
- `eval/test_erasure_request.py`: 7/7 on first run.
- Direct query confirming zero fixture residue, across every prior erasure
  dispatch's own fixture prefix, not just this one's — twice (after the standalone
  run and after the full battery run).
- `scripts/run_harness.sh --layer 7`: clean on the first attempt; explicitly
  re-checked the two invariants (`test_ledger_callsite_enumeration.py`,
  `test_fact_write_convergence.py`) this session has previously found real,
  self-caused regressions in — both stayed green; **RATCHET PASS**.
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
- `harness.erasure_report`'s existing D-R-170 test suite (26 cases) re-run
  unchanged after the `excluded_fact_ids` extension: all still pass, confirming
  backward compatibility, not assumed from reading the diff alone.

**Reasoned about, not independently re-derived:** whether the 2026-07-21 widening
restriction is the RIGHT precedent to extend to erasure (rather than, say, a
stricter or looser boundary) is a judgment call recorded in the REQ doc, not a
mechanically forced conclusion — Bill's own ruling could set a different boundary
without requiring this dispatch's own code to be rebuilt (the authorization check
is a single, isolated comparison, easily changed).

## HASH

Staged for commit: `docs/requirements/REQ_ERASURE_REQUEST_PATH__…v20260805_0658.md`
(new), `harness/erasure_request.py` (new), `harness/erasure_report.py` (extended,
`excluded_fact_ids`), `eval/test_erasure_request.py` (new),
`scripts/run_harness.sh` (wired the new file), this dispatch doc.

## OPEN

- **Question (b) — cross-person erasure authority — remains genuinely
  UNDETERMINED**, blocked on R14/R15's own already-flagged ethicist+attorney gate.
  This build's own refusal is the safe default, not a ruling.
- **Question (d) — immediate execution vs. a confirm step — remains genuinely
  UNDETERMINED for real use.** This build's own immediate-execution choice applies
  only to the fixture-only, never-enabled proof; Bill's ruling is needed before any
  real enablement, named explicitly here and in the REQ.
- **This mechanism has no real caller anywhere** — the SAME open question named at
  D-R-170/171: nothing in `server/` reaches it. Wiring a real caller is the FIRST of
  the four things item 3's own "what enabling would require" list names, and is a
  separate, larger decision this dispatch does not make.
- **The 2026-07-21 widening restriction was extended to erasure by this dispatch's
  own reasoning, not by a fresh ruling on erasure specifically** — recorded so a
  future session (or Bill) can revisit whether erasure's own boundary should differ
  from widening's.
- **Nothing ruled MET.**

## RECAP
D-R-172: wrote `REQ_ERASURE_REQUEST_PATH` first, per Requirements Discipline item 8
— no existing REQ covered "who may request erasure." Answered all four required
questions; found a ratified precedent (the 2026-07-21 household-circle widening
restriction) that DERIVES two of the four answers rather than leaving them
undetermined, and marked the other two (cross-person erasure authority;
immediate-vs-confirm execution) genuinely UNDETERMINED — considered, and declined,
stopping the whole dispatch over either, since neither is load-bearing enough to
block a real, useful, safely-scoped build. Built `harness/erasure_request.py` — the
FIRST real request-shaped caller of the D-R-169/170 erasure mechanism anywhere in
this codebase — refusing structurally (proven by an executed fault twin with a
raise-on-call spy, not a post-hoc report check) unless the requester is the target
fact's own owner, and excluding (not erasing, not silently sweeping in) any fact
about a different, specific person from an owner-wide request. Extended D-R-170's
own `build_member_erasure_report` to distinguish deliberately-excluded facts from
unexplained ones, backward-compatible, confirmed against its own existing 26-case
suite. Nothing enabled against real data — confirmed twice by direct query across
every prior erasure dispatch's own fixture prefix — and item 3's own "what enabling
would require" answered plainly: a real authenticated caller, Bill's own ruling on
confirmation, and the same destructive-write authorization D-R-169/170 already
named. 7 new tests, full battery green, RATCHET PASS, memory harness 13/17 at the
same pinned failing set. Nothing ruled MET.
