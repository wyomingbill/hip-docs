# REQ_TEMPLATE
Status: BUILT
Reconciled-Against: 2026-07-15

Copy this template to start any build. File it as
`docs/requirements/REQ_<SUBJECT>__<slug>__v<YYYYMMDD_HHMM>.md` (Mountain Time),
register it in docs/INDEX.md, and reference it in every dispatch and every
commit for that build. No build starts without one.

Fill every section. If you cannot fill THE ACCEPTANCE TEST so that it can only
pass or fail, the requirement is not clear enough to build from. Stop and ask
Bill. Do not start.

---

# REQ_<SUBJECT>
Status: PLAN | IN_PROGRESS | BUILT | SUPERSEDED | STALE
Reconciled-Against: <commit-hash or date>

## THE REQUIREMENT

Bill's own words, verbatim. Quote them. Do not paraphrase, do not summarize,
do not translate into engineering language. If an expansion or interpretation
is needed, put it BELOW the quote, clearly marked "Expanded:", so the original
words survive every rereading.

## THE ACCEPTANCE TEST

The observable outcome, stated so it can only pass or fail. A specific person
does specific things and specific results are observed. If any clause is
arguable ("works well", "is fast", "behaves correctly"), rewrite it until it
is not. This section is what "done" means. An error going away is not done.
This test passing is done.

## WHAT'S ALREADY DONE

Verified working pieces that this build must NOT redo. List each with how it
was verified (commit, test, observed output). A session that rebuilds
something on this list has failed the dispatch.

## WHAT'S KNOWN BROKEN

The actual gaps, stated precisely. What is missing, what is misdesigned, what
error is currently on screen and WHY it is a symptom rather than the problem.
This section exists so sessions chase the outcome, not the error.

## CONSTRAINTS

What must not regress. The working paths that are sacred. Anything that, if
broken while pursuing the requirement, makes the day a net loss regardless of
what got built.
