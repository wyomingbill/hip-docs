# DISPATCH_DEMO_CUTOVER_VERIFY_CAVEAT_PANEL
Status: BUILT

**TYPE:** MEASUREMENT/VERIFICATION

**REQ:** `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260802_1205.md`
(D-106) — acceptance row C5, and the T05 provenance-caveat gap D-110's comparison found.
Verification only. `demo-cutover-build` @ `586b046` (D-114's WIP commit, port done, never
executed) unchanged by this dispatch — nothing needed fixing, nothing new committed.

## THE ASK

Bill's dispatch, verbatim:

> "Index Cutover 4 — verify the C5 and caveat ports. Base is 586b046 on demo-cutover-build.
> ... The caveat port and the panel port are committed at 586b046 and have NEVER EXECUTED.
> No turn has run against them. Verify, do not build.
> 1. TRUST_LADDER, end to end. [T05 reply verbatim vs hip-vo; T02 wording persistence;
>    every rung transition]
> 2. THE HEADER RULE. ... print the section header verbatim from the prompt. No fact may
>    render under a "Confirmed" header unless its trust level is actually CONFIRMED.
> 3. THE PANEL IN A BROWSER. It has never rendered. Confirm it draws, the five rungs show,
>    and nothing throws. If it errors, print the console error and STOP.
> 4. REGRESSION. Run boundary_and_consent and speaker_isolation once each. ...
> Do not mark any acceptance row MET. Commit only if something needed fixing. Do not push."

## WHAT WAS DONE

1. Machine gate, baseline PIDs (hip-dev `92604`/7871, Neo4j `22330`/7689), `.hip-lock`
   held by another session at dispatch start (`D-115`, unrelated survey) — worked entirely
   in `~/hip-cutover-demo` until the lock freed, then took it (`D-116`) only for this
   doc's own registration.
2. Launched the dashboard exclusively via `scripts/cutover_demo_start.sh` (port 7872).
   Confirmed via `/api/preflight`: `all_ok: true`, `git_head` matching `586b046` exactly —
   the exact commit under verification, nothing drifted.
3. Fired `trust_ladder__v20260729_1453.json` end to end TWICE, independently: once via
   direct signed `/api/text-query` calls, once by driving the real `/demo` browser UI
   (script picker → LOAD → NEXT QUESTION ×5), screenshotting every turn.
4. For the header rule: discovered the two existing `logger.debug` prompt dumps in
   `server/voice_orch.py` (lines ~1816/1941) live in the REALTIME-voice class method, not
   the `/api/text-query` path — they never fired for any turn this dispatch ran. Verified
   instead by calling `server.voice_orch.assemble_governed_context` directly — the same,
   unmodified, already-committed function `/api/text-query` itself calls — against the
   live post-confirm graph, capturing its literal return value. No code was added or
   changed to do this.
5. For the panel: first navigated to `/`, found the OLD operator/routing console (a
   completely separate route/component tree, `@app.get("/")` in `demo_dashboard.py`), not
   a panel error — traced the route table (`@app.get("/demo")`) before concluding
   anything, then navigated correctly. Console-message tracking started BEFORE a fresh
   reload (not after) specifically so load-time errors couldn't be missed.
6. Regression: re-ran `boundary_and_consent__v20260801_1535.json` and
   `speaker_isolation__v20260729_1600.json` once each via signed `/api/text-query`,
   snapshotting `router.jsonl` after each before the next `/api/demo/load` truncated it,
   compared turn-by-turn against the D-110 dispatch's saved baseline data.
7. Report written to `~/Downloads/cutover4_report.md` (10,800 bytes, 174 lines) — full
   detail there; this dispatch doc summarizes.
8. Killed the dashboard, confirmed port 7872 released, hip-dev/7689 unchanged.

## WHAT WAS FOUND

**T05 (the payoff turn) is correct and matches hip-vo, reproduced two independent ways:**
```
Ray is on Jardiance 10mg. That's based on a report confirmed within the household,
not yet checked against an outside source like a clinic — so it's held as reported,
not verified.
```
Names Jardiance, flags it asserted-not-confirmed, uses the ported grounding guard's own
worked example verbatim. Matches hip-vo's script-note baseline ("reply states Jardiance
10mg then the household-reported-not-outside-verified note").

**T02's wording gap (from D-110) persists unchanged** — byte-identical reply both before
and after this port, confirming it was never related to trust-marker rendering.

**Rung transitions, live-traced via the actual panel UI across all 5 turns:**
CORROBORATED (T01, current) → two-active-row park state (T02: CORROBORATED still marked
CURRENT on one card, a NEW UNCONFIRMED card also marked CURRENT, ladder highlights only
one per its own single-`current`-node design) → unchanged read (T03) → **ASSERTED**
(T04, confirm — CORROBORATED card flips to CLOSED, footer line "held on someone's say-so,
not authority-confirmed" appears, matching `EpistemicFactPanel`'s own conditional) →
unchanged read (T05). Net: CORROBORATED closed, ASSERTED current — CONFIRMED never
reached, by design (self-confirmation cap).

**The header rule — verified with the literal live prompt text, not inferred:**
```
Facts about other people (when asked about them, in any phrasing, answer from these):
- Ray — medication: Jardiance 10mg  [asserted: reported and confirmed within the household, not verified against an outside source]
- Dad — risk_pattern: elevated fall-risk pattern  [inferred from other facts, not directly reported]
```
Header reads "Facts about other people" (not "Confirmed..."); both facts carry their real
trust level bracketed (ASSERTED, DERIVED) — neither renders bare/as-if-confirmed. The
"Recent context about this person" section in the SAME captured prompt shows Maya's own
CONFIRMED household facts bare (empty marker), for contrast — the CONFIRMED-gets-no-marker
half of the design confirmed in the same evidence.

**The panel: renders, five rungs, zero console errors** across two independent load
attempts (API-fired data + full browser-driven run), one deliberate fresh-reload-with-
tracking-already-active check specifically to not miss load-time errors. Wrong-URL
red herring at `/` resolved by reading the route table, not by guessing.

**Regression: no defects found.** Two differences from the D-110 baseline, both explained:
`boundary_and_consent` T02's wording changed (pre-existing, hip-vo-acknowledged model
variance on that exact turn, unrelated to this port — the admitted facts there are
CONFIRMED-level and render with an empty marker either way); `speaker_isolation` T03 (Maya
reading her own lisinopril) now carries the CORROBORATED caveat for the first time — not a
regression, the caveat port was never scoped to third-party facts only, and this is that
mechanism correctly reaching a second-person ("Things you know") fact.

**Cross-lane note, flagged not chased:** `roadmap` branch (a different lineage from
`demo-cutover-build`) shows a same-day commit `14811f3`, "D-114: port the trust marker
from hip-vo — write-time labels reach the prompt" — a different session, apparently
similar underlying goal, different framing ("write-time labels"). Not investigated further
(out of scope, different branch, no file conflict with this dispatch) — surfaced for
Bill's awareness that two lanes converged on the same port independently the same day.

## VERIFIED

**Watched run, all of it:** every claim above is from a live turn, a live screenshot, or a
live direct function call against the running dashboard's real state — none reasoned about
from source alone. Full detail, every turn's reply/tier/guard and every panel screenshot's
observed state, in `~/Downloads/cutover4_report.md`.

**Reasoned about, not independently re-run:** the two `logger.debug` prompt-dump call
sites' scope (confirmed by reading, not by exhaustively tracing every code path that could
reach them) — sufficient to explain why they never fired for text-query turns, not
exhaustively proven to never fire under any condition.

## HASH

**NONE.** Verification only, nothing needed fixing. `demo-cutover-build` unchanged from
`586b046`; `git status` clean. This dispatch doc + its `docs/INDEX.md` row are themselves
uncommitted in `~/hip-roadmap`, same pattern as every prior round, pending Bill's
go-ahead.

## OPEN

- C5 and the T05 caveat gap are demonstrated live and correct; neither is marked MET —
  Bill's call, not taken here.
- The cross-lane `roadmap`-branch trust-marker port (`14811f3`) is unreconciled with
  `demo-cutover-build`'s own port — same day, different branches, not investigated.
- `boundary_and_consent` T02 and the general B_T02 reply-completeness variance remains
  open, pre-existing, unrelated to this dispatch.
- C1, C3, C4 already reported prior dispatches; C6/C2 already reported; C7, C8, C9, C10
  untouched by this dispatch.
