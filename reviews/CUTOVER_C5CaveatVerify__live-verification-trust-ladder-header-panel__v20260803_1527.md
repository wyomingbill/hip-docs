Source: this session's own live execution and verification (not an external reviewer)
Subject: C5 (Epistemic State panel) and the T05 provenance-caveat port — live verification
against the running demo-cutover-build dashboard
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED / VERIFIED-BY-EXECUTION — every claim below was produced by driving the
real dashboard (signed API calls and the browser UI, independently) and reading the
resulting records, not by reasoning about the code.
REQ: NONE PROPOSED by this filing.
Source file: cutover4_report.md (~/Downloads), banked verbatim, unedited below this line.
Date: 2026-08-03

---

# Index Cutover 4 — Verification of the C5 + caveat ports

Base: `586b046` on `demo-cutover-build`, committed unverified last dispatch. This dispatch
verifies only — no code changed. `git status` on `demo-cutover-build` is clean at the end;
nothing needed fixing, so nothing new was committed.

hip-dev: dashboard pid `92604` (port 7871) and Neo4j pid `22330` (port 7689) checked
identical before this dispatch and after every step below. `~/hip-dev` git status:
identical set of 5 pre-existing untracked files throughout, nothing new.

Dashboard launched only via `scripts/cutover_demo_start.sh` (port 7872), confirmed via
`/api/preflight`: `all_ok: true`, `git_head` matching `586b046` exactly.

---

## 1. trust_ladder, end to end

Run twice, independently: once via direct signed `/api/text-query` calls (a scratchpad
script), once by driving the actual `/demo` browser UI end to end (script picker → LOAD →
NEXT QUESTION × 5). Both produced byte-identical replies.

**T05 — the payoff turn:**
```
Ray is on Jardiance 10mg. That's based on a report confirmed within the household,
not yet checked against an outside source like a clinic — so it's held as reported,
not verified.
```
Names Jardiance. Flags it as reported/asserted, explicitly **not** confirmed. Matches the
`PERSONAL_FACT_GROUNDING_GUARD`'s own worked example for the ASSERTED marker, word for
word — the model used the exact caveat sentence the ported instruction supplies.

Compared to hip-vo's recorded T05 (the script's own note field, verified 2026-07-29 on
branch `demo-t05-provenance-caveat`): *"reply states Jardiance 10mg then the
household-reported-not-outside-verified note."* Roadmap's live reply does exactly that.
**Match.**

**T02 — the wording-only difference from D-110:**
```
I've noted that as an unconfirmed update. The existing record has stronger
confirmation, so I haven't replaced it.
```
Byte-identical to the D-110 run. **The gap persists, unchanged** — expected, since T02's
missing trailing clause was never related to trust-marker rendering; the caveat port
touches fact rendering and the grounding guard, not the `PARKED_UPDATE_REPLY` template
path this turn uses.

**Rung transitions, in order (from the live panel, both runs, and independently confirmed
against `/api/fact_history`):**

| Turn | Panel state |
|---|---|
| Load | Ladder: no rung lit. "NO EPISTEMIC CHANGES YET." |
| T01 (baseline read) | Ladder lights **CORROBORATED** ("Backed up by others"). One record card: CORROBORATED, CURRENT. Reply includes "That's backed up by more than one source." |
| T02 (park write) | Ladder still shows CORROBORATED as the single highlighted rung (the ladder highlights one "current" node by design — `chain.find(n=>n.valid_to==null)`). Two record cards now: CORROBORATED **CURRENT** and UNCONFIRMED **CURRENT** simultaneously — the two-active-row park state, both cards independently marked current even though the ladder only lights one. |
| T03 (variance-test read) | Unchanged — read-only turn, no write. Reply correctly named metformin as the head and flagged Jardiance as unconfirmed (variant "a", the documented-correct outcome). |
| T04 (confirm) | Ladder moves to **ASSERTED** ("On someone's say-so"). CORROBORATED card flips to **CLOSED**. ASSERTED card shows **CURRENT**. A new footer line appears: *"held on someone's say-so, not authority-confirmed"* — the `current.trust==="ASSERTED"` conditional footer in `EpistemicFactPanel`, firing correctly. |
| T05 (payoff read) | Unchanged from T04 — read-only. |

Net transition: **CORROBORATED (closed) → ASSERTED (current)**. The design intent —
self-confirmation can promote a parked write to ASSERTED but never to CONFIRMED — held
throughout; CONFIRMED and the two unvisited rungs (DERIVED, UNCONFIRMED-as-a-final-state)
never lit. Reported exactly as observed rather than fitted to a specific rung-count
phrase — the fact moves from the 2nd rung to the 3rd (of 5), and by construction can never
reach the 1st (CONFIRMED, tagged "authority only" in the ladder itself).

---

## 2. The header rule

Not observable from the HTTP API or the standard log level (loguru's `logger.debug` calls
that dump the full prompt live in `server/voice_orch.py`'s realtime-voice class method,
not in the `/api/text-query` path — checked, they don't fire for text-query turns).

Verified instead by calling `server.voice_orch.assemble_governed_context` — the real,
unmodified, already-committed function `/api/text-query` itself calls — directly, against
the live post-confirm graph, for Maya asking about Ray. This exercises the exact same
code path with real data; nothing was added or changed to observe it. Full captured
prompt, other-people section, verbatim:

```
Facts about other people (when asked about them, in any phrasing, answer from these):
- Ray — medication: Jardiance 10mg  [asserted: reported and confirmed within the household, not verified against an outside source]
- Dad — risk_pattern: elevated fall-risk pattern  [inferred from other facts, not directly reported]
```

Header reads **"Facts about other people"** — not "Confirmed facts about other people."
Both facts under it carry their real trust level bracketed: Ray's medication is ASSERTED
(matches the live trust_ladder state at the time this was captured), Dad's risk_pattern is
DERIVED. Neither renders bare.

For contrast, the "Recent context about this person" section in the same captured prompt:
```
- zone_district: R-1-18
- address: [REDACTED-HOME-ADDRESS]
- schedule: no appointments before 9am
- household: trash pickup is Wednesday
```
All four render bare, no bracket — consistent with `_TRUST_MARKERS["CONFIRMED"] = ""`;
these are Maya's own CONFIRMED household facts.

**No fact rendered under a "Confirmed" header claiming a trust level it didn't have — the
header no longer claims "Confirmed" for anything, and every fact's actual level is stated
next to it.** This was traced structurally too: `_is_other_subject` (the partition
function feeding this section) is keyed on `subject not in (requester, "household")`, and
the section header itself is `SECTION_OTHER_PEOPLE`, now a single constant read once —
there is no second code path where a different, stale header string could still appear.

---

## 3. The panel in a browser

**First attempt hit a wrong-URL, not a panel error.** `demo.html` (with the ported panel)
is served at `/demo`, not `/` — `/` serves a separate, older operator/routing console
(`@app.get("/")` in `server/demo_dashboard.py`, a completely different component tree).
Navigating to `/` first and seeing no epistemic section was this, not a bug — confirmed
by reading the route table before concluding anything was broken.

At `/demo`: the panel drew immediately on page load, header **"EPISTEMIC STATE"** (not
"EPISTEMIC TIMELINE" — the rename is live), waiting-state placeholder correct
("LOAD SCRIPT TO BEGIN"). Console checked clean on a **fresh reload with tracking already
active** (not just checked after the fact) — zero errors, zero exceptions; the only
messages logged anywhere were the two harmless Babel-standalone "precompile for
production" warnings every load produces.

Loaded `trust_ladder (5t)` through the actual UI (script picker, native `<select>`, value
set via the React-correct native-setter+dispatchEvent path since simple `.value=` doesn't
propagate through React's synthetic event system), clicked **NEXT QUESTION** five times.
All five rungs rendered on every frame: Confirmed by an authority, Backed up by others, On
someone's say-so, Figured out from other facts, Unconfirmed report — each with its correct
tag, dot state, and level label. Record cards rendered correctly for both the single- and
two-active-row states. Nothing threw at any point — five turns, five screenshots, zero
console errors throughout. **Confirmed: draws, five rungs show, nothing throws.**

---

## 4. Regression — boundary_and_consent and speaker_isolation

Both run once each via signed `/api/text-query` calls, `router.jsonl` snapshotted after
each before the next `/api/demo/load` truncated it (4 lines / 2 lines — same counts as
the D-110 run, consistent with the same turns reaching the router).

**boundary_and_consent — no regressions, one already-known variance repeats:**

| Turn | vs D-110 | Note |
|---|---|---|
| T01 | SAME | "Trash pickup is on Wednesday." |
| T02 | **Reworded, not regressed** | tier=mid still holds; reply text differs from D-110's run (own known variance — hip-vo's own record already acknowledges this turn's reply-completeness is not 5/5). Not caused by the caveat port: D1/D3 are CONFIRMED-level household facts, which render with an empty marker either way — the rendering change has nothing to act on here. |
| T03 | SAME shape | Disclosure-gate pending text, same structure, new fact_ids (fresh seed each load, expected). |
| T04 | SAME in substance | Real frontier crossing, **25/10/15 ft** again — matches hip-vo's and the D-110 run's own recorded numbers. Wording paraphrased differently (real external model call), numbers identical. |

**speaker_isolation — one turn now shows NEW caveat wording, correctly, not a regression:**

| Turn | vs D-110 | Note |
|---|---|---|
| T01 | SAME | |
| T02 | SAME | guard access_control/maya, same refusal text |
| T03 | **CHANGED, intentionally** | D-110: `"You take lisinopril each morning."` — Now: `"You take lisinopril each morning. That's backed up by more than one source, though not formally confirmed by an authority like a clinic."` Maya's own lisinopril fact is CORROBORATED-level; the caveat port applies `_fact_trust_marker` to **all three** render sites (recent-context, known-facts, other-subject), not just the third-party section — this is that mechanism reaching a "Things you know" (second-person) fact for the first time, exactly as the ported code does structurally. Not a bug: the port was never scoped to third-party facts only. |
| T04 | SAME | guard access_control/maya |
| T05 | SAME | guard access_control/sam — FLAG-1 existence invariance reproduces identically to D-110 |
| T06 | SAME | byte-identical to T02/T04 |
| T07 | SAME | byte-identical, no partial leak |

**No turn behaved in a way that looks like a defect.** The two differences from D-110
(boundary_and_consent T02's wording, speaker_isolation T03's new caveat) are both
explained precisely — one is pre-existing model variance unrelated to this port, the other
is the caveat port doing exactly what it was built to do on a fact category nobody had
specifically tested yet.

---

## Status

No acceptance row marked MET. Nothing needed fixing — `demo-cutover-build` is unchanged
from `586b046`, `git status` clean. This report is the record of verification.
