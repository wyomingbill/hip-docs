# REQ_ERASURE_REQUEST_PATH
Status: BUILT
Reconciled-Against: see the dispatch doc's own HASH section

## THE REQUIREMENT

Bill's own words, verbatim (D-R-172):

> "Erasure is built, proven, and unreachable — no API, no voice command, no admin
> action calls it from a real request. A capability nobody can invoke is not a
> feature. HIP shall have a request path that reaches the built erasure mechanism.
> Who may request erasure of what is an authorization question and shall be answered
> explicitly, not inherited from whoever happens to be calling."

**Expanded**, per D-R-172's own item 1, answering the four required questions:

### (a) Who may request erasure of their own facts

**DETERMINED.** A member may request erasure of a fact where they are its `owner`
(the person whose key the fact is encrypted under — `harness.graph_erasure`'s own
existing granularity, matching `epistemic_ledger.destroy_member_key`'s identical
owner-keyed model) **and** the fact's `subject` is either absent or is that same
member. This is not invented here: it is the EXACT boundary the household-circle
widening restriction already ratified (2026-07-21, `harness/write_rule.py:160-168`):
*"an author may widen to household-circle only for facts about themselves or generic
household facts — never a fact about someone else without THEIR standing policy."*
Erasure is a strictly MORE consequential operation than widening audience; the same
boundary applies at least as strictly.

### (b) Whether anyone may request erasure of facts about another person

**UNDETERMINED for a non-owner (e.g., the fact's own `subject`, if they are a
different HIP member than its `owner`) requesting erasure of content someone else
wrote about them.** This requires a cross-person authority mechanism that does not
exist — the exact territory `REQ_CEILING_ACCEPTANCE`'s own A14/A15 rows already name
as blocked (`REQ_CARE_TEAM_READ_AUTH` NOT MET; A15 needs "Ethicist + attorney
sign-off," Part 4 ADVISORY tier). **What would settle it:** R14/R15 landing, with an
explicit ruling on whether a fact's subject (not its owner) may compel or request its
erasure. Not decided here — this build refuses every such request rather than
guessing (see WHAT'S KNOWN BROKEN).

### (c) What happens to facts a requester authored about someone else

**DETERMINED, by the SAME 2026-07-21 precedent cited in (a).** An owner-wide erasure
request (`harness.graph_erasure.erase_member_facts`, D-R-170) does NOT, by itself,
distinguish subject — it would erase every fact that owner ever wrote, including
facts about a different, specific person. The ratified widening restriction says an
author has no unilateral authority over a fact about someone else; by the identical
logic, **this request path's own authorization layer excludes any fact whose subject
is a specific person other than the requester from an owner-wide erasure request** —
narrower than the raw mechanism, not the mechanism's own unfiltered sweep. Those
excluded facts are named in the outcome, not silently skipped.

### (d) Immediate execution or a second step

> **RULED TWO-STEP — Bill, 2026-08-05, enacted D-R-194.**
>
> > "Question (d): TWO-STEP. A request creates a pending confirmation; a second
> > authenticated act by the same member executes it. Destruction is irreversible and
> > confirmations are already their own channel in this design."
>
> **BUILT:** `harness.erasure_request.begin_fact_erasure` authorizes and returns a
> pending token **without ever calling the erasure mechanism**;
> `confirm_fact_erasure` is the second act and executes. `POST /api/erasure/fact`
> serves both steps — no `token` in the body means step one, a `token` means step
> two — and **each step carries its own body-bound Ed25519 signature**, so the
> confirmation is a fresh authenticated act rather than a replay of the request.
>
> Authorization is checked at REQUEST time, not deferred to confirm, so an
> unauthorized request is refused before a pending row exists and the pending store
> cannot be used to probe which facts exist. Tokens are single-use, expire after 5
> minutes, and are held in memory per-process on purpose — a pending destruction
> must not survive a restart.
>
> **The store is deliberately NOT `harness.confirmation_gate`.** That gate resolves
> an AMBIGUOUS pending WRITE; this confirms an already-unambiguous, already-
> authorized DESTRUCTION. This document's own text below names them as different
> concerns, and sharing the store would couple a data-integrity mechanism to a
> destruction one.
>
> **Four fault twins, executed, spy at zero on every refusal:** an unconfirmed
> request erases nothing; a confirmation by a different member is refused; an
> expired confirmation is refused; a consumed token cannot be replayed. A fifth
> proves a signature made for one token cannot confirm another. The anti-vacuity
> control — a correct two-step that DOES reach the mechanism exactly once — is what
> makes those four mean anything.

**The original text is retained below as the record of what was open before the
ruling. It is superseded by it.**

~~**UNDETERMINED, and named as such rather than guessed.**~~ No ratified precedent
answers whether a real, ENABLED erasure request needs a confirm-then-execute step
(`harness.confirmation_gate`'s own P8 pattern resolves an AMBIGUOUS pending WRITE, a
different concern from confirming an already-unambiguous, already-authorized
DESTRUCTIVE request). **This build proceeds with immediate execution** for the
fixture-only, never-enabled proof this dispatch's own item 3 scope limit requires —
chosen because (i) it is the simplest reading directly matching R17's own seven-step
sequence, described as one atomic operation with no confirmation step of its own,
(ii) nothing built here touches real data regardless of this choice (item 3's own
scope limit), and (iii) layering a confirmation step on top later is additive, not a
rework — building "immediate" now does not foreclose "two-step" later. **What would
settle it for real enablement:** Bill's own ruling on whether a real request needs a
confirm step, named explicitly as still open in the dispatch doc's own OPEN section.

## THE ACCEPTANCE TEST

A request function, given a requester identity and a target (one fact, or "everything
I own"), either:

1. **Refuses structurally** — with NOTHING erased and NO call made into
   `harness.graph_erasure` at all — when the requester is not the `owner` of the
   target; proven by an executed test that patches `erase_fact`/`erase_member_facts`
   to record whether they were ever invoked, and shows they were NOT, for an
   unauthorized request.
2. **Executes and returns a `harness.erasure_report` result** — built from the SAME
   D-R-167/169/170 report machinery, not a new, separate "did it work" story — when
   the requester IS the owner, excluding (and naming) any fact whose subject is a
   different, specific person.

Both proven against disposable, uniquely-prefixed fixtures only. Nothing in this
build is enabled against the live demo graph, `hip-cutover-demo`, or any real
household data — confirmed by direct query, matching D-R-169/170's own posture.

## WHAT'S ALREADY DONE

- `harness.graph_erasure.erase_fact` / `erase_member_facts` (D-R-169/170) — the
  actual deletion mechanism, cascade-aware, fixture-proven. NOT rebuilt here.
- `harness.erasure_report.build_fact_erasure_report` / `build_member_erasure_report`
  / `verify_erasure_report` (D-R-167/169/170) — the machine-verifiable outcome
  instrument, all three target kinds. NOT rebuilt here — THIS dispatch's own request
  path returns exactly this report, per item 2's own instruction ("the report is the
  answer to 'did it work,' not a separate story").
- The 2026-07-21 household-circle widening restriction (`harness/write_rule.py`) —
  the ratified precedent this REQ's own (a)/(c) answers are derived from, not
  reinvented.

## WHAT'S KNOWN BROKEN

- ~~**No request path exists at all** — this is the entire gap this REQ exists to
  close. Zero API, voice command, or admin action anywhere calls `erase_fact`/
  `erase_member_facts` from real request-handling code (confirmed at D-R-170,
  unchanged).~~

  > **PARTLY SUPERSEDED 2026-08-05 (D-R-192). Annotated, not rewritten.** One route
  > now exists: `POST /api/erasure/fact` in `server/demo_dashboard.py`, wired to
  > `request_fact_erasure` only. The sentence above was true when written and is now
  > true only of the *other* surfaces — there is still **no voice command and no
  > admin action**, and `request_member_facts_erasure` (owner-wide) is still reached
  > by nothing, deliberately.
  >
  > **This does NOT mark anything MET** (D-R-192 item 6). The route is **OFF unless
  > `HIP_ERASURE_ROUTE_ENABLED` is set**, proven fixtures-only, and never enabled
  > against real data — the CONSTRAINTS below are unchanged and were honoured.
  > Questions **(b)** and **(d)** remain UNDETERMINED and are refused by default in
  > code: (b) by the request layer refusing every requester != owner, (d) by not
  > being answered either way in the route.
- **Cross-person erasure authority (question (b)) is unresolved** — this build does
  not invent an answer; it refuses every request where requester != target owner,
  full stop. A future dispatch resolving R14/R15 may widen this; nothing here
  forecloses that.
- **Confirmation-before-execution (question (d)) is unresolved for real use** — this
  build's own immediate-execution choice applies ONLY to the fixture-only,
  never-enabled proof this dispatch produces.

## CONSTRAINTS

- **Must not enable anything against real data.** Matching D-R-169/170's own posture
  exactly: fixtures only, disposable, uniquely-prefixed, cleaned up regardless of
  pass/fail, confirmed by direct query after every run.
- **Must not widen who can call `erase_fact`/`erase_member_facts` directly** — those
  functions are UNCHANGED by this dispatch. The new authorization layer sits IN
  FRONT of them, refusing before they are ever reached; it does not alter their own
  contracts.
- **Must not silently answer (b) or (d)** — both stay named as open, in this REQ and
  in the dispatch doc, regardless of which default this build proceeds with for (d).
- **The report returned must be the SAME report machinery (D-R-167/169/170), not a
  second, competing "did it work" story** — per item 2's own explicit instruction.
