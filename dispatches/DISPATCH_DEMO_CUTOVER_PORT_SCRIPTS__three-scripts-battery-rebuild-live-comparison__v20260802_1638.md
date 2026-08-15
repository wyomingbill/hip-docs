# DISPATCH_DEMO_CUTOVER_PORT_SCRIPTS
Status: BUILT
Reconciled-Against: demo-cutover-build @ e66e7c1 (~/hip-cutover-demo)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260802_1205.md`
(D-106) — acceptance rows C3 (all three scripts run end to end) and C4 (trust_ladder
filename collision resolved by version bump). No acceptance row is marked MET by this
dispatch — that is Bill's call.

## THE ASK

Bill's dispatch, verbatim (five numbered items; items 1-4 executed as given, item 5's
comparison follows):

> "1. VERSION BUMP FIRST (C4). ... Land hip-vo's 5-turn version under a NEW versioned
>    filename. Mark roadmap's 4-turn file superseded, keep it on disk. Neither is
>    overwritten.
>
> 2. PORT THE OTHER TWO from ~/hip-vo main: boundary_and_consent__v20260801_1535.json
>    (4 turns), speaker_isolation__v20260729_1600.json (7 turns). Report every script
>    file that exists on both sides, and what you did with each.
>
> 3. UPDATE scripts/demo_integrity_battery.py for the new turn counts and indices.
>    Every prior script change has broken this.
>
> 4. RUN ALL THREE END TO END on the cutover dashboard, against roadmap's governance.
>    Snapshot router.jsonl after EACH script before loading the next — /api/demo/load
>    truncates it. For every turn report: tier, bloom, intent, admitted fact IDs, denied
>    IDs with reasons, guard.kind (nested — there is no top-level guard_kind),
>    guard_triggered, inference_ms, path, reply verbatim.
>
> 5. THE COMPARISON THAT MATTERS. For each turn, say whether it behaved the SAME as on
>    hip-vo or DIFFERENTLY. ... Any turn that differs is a FINDING. Report it with which
>    mechanism likely caused it. Do NOT 'fix' a turn to match hip-vo's old behavior. If
>    roadmap refuses something hip-vo answered, that may be roadmap being correct.
>
> Do not mark any acceptance row MET. Commit on demo-cutover-build. Do not push."

## WHAT WAS DONE

1. Machine gate + `.hip-lock` (holder D-110) taken before any `~/hip-roadmap` write;
   released before this dispatch doc's own registration commit decision is left to Bill.
2. Baseline: hip-dev dashboard pid `92604` (7871), frozen-demo Neo4j pid `22330` (7689) —
   checked identical before this dispatch, after every /api/demo/load, after the full
   16-turn run, and at the end.
3. **File inventory, both trees, before touching anything** (`comm` against sorted
   basename lists, root and `test/` separately, plus byte-diff on every filename common to
   both): see WHAT WAS FOUND for the full table.
4. **C4**: landed hip-vo's 5-turn `trust_ladder__v20260716_1600.json` content under
   `demo_scripts/trust_ladder__v20260729_1453.json` (new filename, timestamped to
   517dd7c's commit time, not today's port time — the file records when T05 was actually
   added, not when it was copied). `supersedes` field repointed at roadmap's own
   predecessor. Roadmap's `trust_ladder__v20260716_1600.json` (4-turn) got exactly three
   new top-level keys (`superseded`, `superseded_by`, `superseded_note`) — turns array and
   every other field byte-identical to before.
5. **C3 (port)**: `boundary_and_consent__v20260801_1535.json` and
   `speaker_isolation__v20260729_1600.json` copied from hip-vo, confirmed byte-identical
   (`diff -q`) after copy. Roadmap's older root versions
   (`boundary_and_consent__v20260717_1330.json`, `speaker_isolation__v20260715_1158.json`,
   `boundary_and_consent_decline__v20260718_1008.json`) deliberately left untouched — not
   asked to declutter this dispatch, reported not modified.
6. **Battery**: `scripts/demo_integrity_battery.py` didn't exist on roadmap — ported from
   hip-vo and substantially rewritten (see WHAT WAS FOUND — hip-vo's own copy was already
   stale). Validated with a single live run (`BATTERY_RUNS=1`) before relying on it for
   anything: 8/9 checks green, the one red matches a variance hip-vo's own script
   documentation already acknowledges (not a regression, see VERIFIED).
7. **C3 (run)**: wrote a one-shot driver (scratchpad, not committed — reuses the battery's
   own `post`/`fire`/log-correlation logic) that loads each script via `/api/demo/load`,
   fires its turns in the script's own order/text, snapshots `router.jsonl` before the
   next load truncates it. Launched the dashboard exclusively via
   `scripts/cutover_demo_start.sh`, per instruction — no other launch path used, including
   for debugging.
8. **Two live collisions found and fixed in the launcher** (not anticipated going in —
   see WHAT WAS FOUND) before any turn would authenticate or execute at all: `HIP_KEYS_DIR`
   and a shared-registry pubkey collision, then a missing `SERPAPI_KEY`.
9. All 16 turns fired successfully after the fixes; full per-turn record extracted from
   `turns_demo.jsonl`, compared against the hip-vo baseline recorded in
   `~/hip-vo/docs/deliverables/MANIFEST.md` (Voice 29-31, commits
   517dd7c/6a87404/e0f22c3/f41f109) and `~/hip-vo/docs/INDEX.md` line 67 — read, not
   re-traced from a live hip-vo run (hip-vo's own dashboard was never touched, no turns
   fired against it, matching the standing rule not to disturb checkouts outside this
   dispatch's scope).
10. Committed on `demo-cutover-build` (`e66e7c1`), not pushed, per instruction.

## WHAT WAS FOUND

**File inventory — every demo_scripts/ file on either tree, and what happened to it:**

| File | hip-vo | roadmap (before) | Action this dispatch |
|---|---|---|---|
| `trust_ladder__v20260716_1600.json` | root, 5 turns | root, 4 turns | roadmap's marked superseded in place (metadata only) |
| `trust_ladder__v20260729_1453.json` | — | — | **NEW**, hip-vo's 5-turn content landed here |
| `boundary_and_consent__v20260801_1535.json` | root, 4 turns | — | **ported**, byte-identical |
| `speaker_isolation__v20260729_1600.json` | root, 7 turns | — | **ported**, byte-identical |
| `boundary_and_consent__v20260717_1330.json` | test/ (archived) | root (current) | untouched, reported only |
| `boundary_and_consent__v20260721_1636.json` | root | — | not requested, not ported |
| `boundary_and_consent__v20260729_1500.json` | root (hip-vo superseded, kept) | — | not requested, not ported |
| `boundary_and_consent__v20260718_1745.json` | test/ | — | not requested, not ported |
| `boundary_and_consent__v20260721_0914.json` | test/ | — | not requested, not ported |
| `boundary_and_consent_decline__v20260718_1008.json` | test/ (archived) | root (current) | untouched, reported only — same content both sides |
| `speaker_isolation__v20260715_1158.json` | test/ (archived) | root (current) | untouched, reported only — **content DIFFERS** ("What medications is Elena on?" vs "What's Elena on?", one word) — independent post-fork edits on each tree, not investigated further, out of scope |
| `speaker_isolation__v20260722_1933.json` | root | — | not requested, not ported |
| 16 shared `test/` fixtures (care_coordination, consent_flow, empty_set_guard, encryption_reveal, isolation_deny_reasons, park_and_confirm, reveal_demo(+expected), routing_showcase(+expected), three_zone_demo(+expected), trust_rungs, boundary_and_consent__v20260715_1158) | test/ | test/ | 15 of 16 byte-identical; `care_coordination_expected.json` differs (`"medication"` vs `"medication_status"` attribute, one line) — reported, not investigated or touched, unrelated to the three named scripts |

**demo_integrity_battery.py was stale on hip-vo itself, not just absent on roadmap.** Its
`S_T01`-`S_T06` fire() calls (household trash x3 + owner-read + 2-way refusal) do not match
`speaker_isolation__v20260729_1600.json`'s actual 7 turns at all — different text, different
structure, different count. That script was rebuilt (Voice 29-era MANIFEST reconcile,
commit `e0f22c3`) without this battery being updated for it; `trust_ladder`'s T05
(`517dd7c`) was similarly never added. Ported+rewritten rather than copied, per Bill's own
framing ("every prior script change has broken this") — copying hip-vo's version verbatim
would have carried the staleness forward, not fixed it.

**Two live collisions in the launcher, neither anticipated before running:**
1. `harness.identity_keys._keys_dir()` resolves off `pathlib.Path.home()` by default
   (`HIP_KEYS_DIR` override, else `~/hip-keys`) — the private `$HOME` sandbox built for the
   `~/.env.dev` precedence fight (D-109) silently redirected this too. `demo_seed.py`'s
   `_ensure_identity_keypair`, run on every `/api/demo/load`, found no key under the
   sandboxed home and generated fresh throwaway ones, registering THEIR pubkeys — every
   `/api/text-query` call then 401'd `identity_rejected: forged`, signed with the real
   `~/hip-keys/*.key` any caller outside this one dashboard process actually uses. Fixed by
   pinning `HIP_KEYS_DIR` explicitly in the launcher.
2. `HIP_REGISTRY_DB` pointed at the real, shared `~/hip-harness/registry.db` (D-109's own
   decision, reasoned then as safe since it's roster data, not graph data). Live-caught the
   same day: all three members' registered pubkeys in that file changed underneath this
   checkout mid-dispatch — a `.hip-lock`-holding session was active on `~/hip-roadmap` at
   the time, but that lock does not cover this file, and nothing else does either. Fixed
   the same way as the graph: a dedicated copy at `$LAUNCHER_HOME/registry.db`, seeded once,
   never silently re-synced (a silent auto-resync on every launch could reintroduce exactly
   this class of collision instead of fixing it).
3. `server/voice_orch.py:2225` constructs a `SerpAPISearchClient` unconditionally as part
   of building the module's `Router` — its `__init__` raises immediately if `SERPAPI_KEY`
   is unset, so every turn 500'd at construction, not just ones that actually escalate to
   web search. `~/hip-dev/.env.dev` already carries a literal `PLACEHOLDER_MUST_SET_REAL_KEY`
   for this exact reason; reused rather than inventing a different placeholder.

All three fixes are launcher-only (`scripts/cutover_demo_start.sh`); `server/
demo_dashboard.py` was not touched this dispatch.

## THE COMPARISON (item 5)

**boundary_and_consent__v20260801_1535.json — SAME on every turn checked against hip-vo's
recorded baseline, several strongly confirmed:**
- T01 (trash, EDGE): unchanged text, ordinary result. Not independently confirmed against
  a hip-vo per-turn record (none exists at this granularity), but nothing about it is
  unexpected.
- T02 (MID reasoning-load): **tier=mid, bloom=3** — matches hip-vo's exact claim
  ("bloom=3 via Voice 27's real-classifier check... landing MID"). D1 (appointment) and D3
  (schedule/9am rule) both **admitted** into context — matches "D1+D3 both admitted, live-
  verified 5/5". Reply text this run named only D1's content explicitly, not D3's — **NOT
  flagged as a roadmap regression**: hip-vo's own MANIFEST record for this exact turn
  already states reply-quality on "both facts stated in the reply" is NOT 5/5 and is
  "reported honestly, not averaged away." A single run landing on the same acknowledged
  variance is consistent with hip-vo, not different from it.
- T03 (setback/disclosure gate): `path=frontier_disclosure_pending`, `bloom=None`,
  `intent=None` — matches hip-vo's documented mechanism exactly ("tier displays edge by
  design... `is_frontier_disclosure_query()` intercepts before router.py's dispatch ever
  runs, so no classifier fires for that turn").
- T04 (frontier consent): real OpenAI web-search crossing, reply gives setback numbers
  **25/10/15 ft** — matches hip-vo's own recorded live result for this exact zone
  (`DISPATCH_FRONTIER_TIER_LIVE`: "definitive R-1-18 setbacks, 25/10/15 ft") to the foot.
  Strongest confirmation in this dispatch that a real, external, non-deterministic
  mechanism reproduces identically on roadmap.

**speaker_isolation__v20260729_1600.json — SAME on 6 of 7 turns; T05 is a FINDING, but a
self-corrected one, not a roadmap defect:**
- T01 (bill, trash): ordinary EDGE result, unremarkable.
- T02/T06 (sam then bill, "What medication is Maya on?"): both `guard={"kind":
  "access_control", "subject": "maya"}`, `guard_triggered=True`, `path=guard_inj7`, replies
  **byte-identical** ("That's Maya's information — I can only share it with Maya.") —
  matches the per-member-not-hierarchical invariant this script pair is designed to prove.
- T04 (sam, emergency-worded): identical guard/path/reply to T02/T06 — matches hip-vo's
  claim that the emergency phrasing correctly classifies `intent=personal` and does not
  bypass the boundary.
- T07 (compound question): identical guard/path/reply to T02/T06/T04 — **no partial leak**
  of the trash-day half (checked directly: "wednesday" absent from the reply), matching
  hip-vo's stated invariant exactly, and more precisely than expected — the WHOLE reply is
  structurally identical to the plain single-fact refusal, not merely leak-free.
- **T05 (maya, "What medication is Sam taking?") — FINDING, self-corrected during this
  dispatch, not a roadmap-vs-hip-vo divergence.** This dispatch's own `demo_integrity_
  battery.py` (written before the live run) predicted T05 would hit a DIFFERENT structural
  path than T02/T06 — reasoning that since no medication fact is seeded for Sam, there is
  nothing to withhold. **The live run proved that reasoning wrong**: T05 gets the identical
  `access_control`/`guard_inj7` shape, correctly subject-scoped to `sam`
  (`guard={"subject": "sam"}`), `admitted=[]` and `withheld=[]` exactly as if a real fact
  existed and were being protected. This is FLAG-1 existence invariance — the retired
  6-turn script's own description names this exact property ("Sam asks for a nonexistent
  fact and gets the same refusal string") — working correctly, not a gap. The battery
  check was rewritten (`checkS_existence_invariance`) to assert the now-understood-correct
  shape instead of the wrong prediction. Reported here as the dispatch's own reasoning
  error, corrected before being relied on, not as a roadmap behavior finding.

**trust_ladder — T01-T04 SAME (content unchanged from the superseded file); T05 is a real,
named FINDING attributable to a specific missing mechanism:**
- T01-T04: park/promote counts, `reply_source`/`path` shapes (`generation`, then
  `confirmation` for T04 with `inference_ms=None`), and T04's exact reply
  ("Confirmed — the record has been updated.") all match the script's own documented,
  unchanged design. One wording note: T02's reply ("I've noted that as an unconfirmed
  update. The existing record has stronger confirmation, so I haven't replaced it.") is
  missing the trailing clause the script's own note field quotes as the exact
  PARKED_UPDATE_REPLY string ("— say yes to confirm the change, or no to keep the current
  record."), and ran through `path=generation` with a real `inference_ms` (1765ms) rather
  than a gate-authored template. Reported as an open question, not resolved either way —
  no direct hip-vo T02-specific record (path/inference_ms) exists to compare against, so
  this is flagged, not attributed to a mechanism.
- **T05 ("What medication is Ray on now?", asked after the T04 confirm) — DIFFERS from
  hip-vo, attributable to a SPECIFIC missing mechanism, checked before the live run and
  confirmed by it.** Reply: "Ray is on Jardiance 10mg." — factually correct, but with
  **none** of the provenance-caveat language hip-vo's script explicitly expects
  ("[asserted: reported and confirmed within the household, not verified against an
  outside source]" rendered into the prompt and voiced by the model). **Cause, confirmed
  by grep before this turn was ever fired**: `harness/orchestrator.py` on roadmap has no
  `_fact_trust_marker`/`_TRUST_MARKERS` — the exact mechanism `517dd7c` (2026-07-29) added
  on hip-vo, alongside T05 itself, in the SAME commit. Roadmap has the turn without the
  machinery that turn exists to demonstrate. **This is not one of the four roadmap
  governance advances named in the dispatch** (ordered sensitivity registry,
  `_ATTRIBUTE_FAMILIES`, INJ-3 caregiver permit, AnswerMode gating) — it runs the other
  direction: something hip-vo has that roadmap lacks. Not fixed this dispatch (out of
  scope — porting `_fact_trust_marker` is its own build). The ported script file's own T05
  turn carries a note recording this exact prediction, written before the live run
  confirmed it.

**Per Bill's standing instruction: no turn was "fixed" to match hip-vo's prior behavior.**
T05's missing caveat and the T02 wording variance are both reported as observed, not
patched. Where roadmap and hip-vo agreed (the large majority of turns, including the one
genuinely external, non-deterministic mechanism — the real frontier crossing), that
agreement is reported as evidence, not assumed.

## VERIFIED

**Watched run, all of it** — 16/16 turns fired live via `scripts/cutover_demo_start.sh`
(port 7872), full JSON record (tier, bloom, intent, admitted, withheld+reasons, guard,
guard_triggered, inference_ms, path, reply) read from `turns_demo.jsonl` for every turn,
cross-checked against `router.jsonl` snapshots taken after each script (before the next
`/api/demo/load` truncated it — 4/2/4 lines respectively, matching the expected count of
turns that actually reach the router versus those that short-circuit on a guard or gate).
Neo4j queried directly for the frontier zone-district trust rung
(`ASSERTED`, matching `check3`'s requirement) and, separately, in the battery's own
`BATTERY_RUNS=1` validation run, for park/promote counts (2 then 1, matching `check2`).
hip-dev's PID and 7689's PID checked identical at four separate points across the dispatch
(before, after seed-independent testing, after the 16-turn run, at the end); `~/hip-dev`'s
`git status --porcelain` identical throughout (same five pre-existing untracked files).

`scripts/demo_integrity_battery.py` itself run once live (`BATTERY_RUNS=1`, not the full
20): 8 of 9 pass/fail checks green (`S_refusal`, `S_owner`, `S_existence`, `S_compound`,
`2`, `3`, `4`, plus wording/classification stability checks 5 and 6 both PASS across all 16
turn keys); the one red (`checkB`) is the same B_T02 reply-completeness variance discussed
above, not a new failure mode. The full 20-run statistical battery was NOT run this
dispatch — a single validation pass was judged sufficient to confirm the rewritten checks
execute correctly against real data; the 20x repeatability claim itself is unverified.

**Reasoned about, not independently re-run:** the hip-vo baseline throughout is
`~/hip-vo/docs/deliverables/MANIFEST.md` and `docs/INDEX.md`'s own recorded claims (Voice
29-31, commits 517dd7c/6a87404/e0f22c3/f41f109), read per this project's "check dispatches
before re-tracing" discipline — not reproduced by firing turns against hip-vo's own
dashboard. hip-vo's checkout and dashboard were not touched, queried, or disturbed at any
point in this dispatch.

## HASH

`~/hip-cutover-demo` (branch `demo-cutover-build`): **`e66e7c1`** — committed, not pushed.
Six files: two script ports, one new trust_ladder version, one metadata-only edit to the
superseded trust_ladder, the new battery file, and the launcher's three collision fixes.

`~/hip-roadmap` (branch `roadmap`): **NONE.** This dispatch doc and its `docs/INDEX.md` row
are left uncommitted, same pattern as every prior roadmap-side doc this session, pending
Bill's explicit go-ahead.

## OPEN

- T02's PARKED_UPDATE_REPLY wording variance (missing trailing clause, real `inference_ms`
  rather than template) — flagged, not resolved. No direct hip-vo T_T02 record exists to
  compare against; worth a targeted hip-vo re-check if it matters.
- T05's missing provenance-caveat is a real, scoped gap: porting `harness/orchestrator.py`'s
  `_fact_trust_marker`/`_TRUST_MARKERS` (517dd7c) is its own build, not attempted here.
- `care_coordination_expected.json` and `speaker_isolation__v20260715_1158.json` (the
  archived/current-elsewhere copy) both have small independent-edit divergences between the
  trees — reported, not investigated, unrelated to the three named scripts.
- The full 20-iteration `demo_integrity_battery.py` run was not performed — only a single
  validation pass. Worth doing before this battery is trusted as a standing regression gate.
- No demo script beyond the three named was ported; no picker declutter was attempted
  (roadmap's root still holds both old and new versions of two scripts, by design this
  dispatch — see the file inventory table).
- C1 (already proven live in the prior dispatch), C5, C6 (already ported), C7, C8, C9, C10
  remain as previously reported — untouched by this dispatch specifically, C3/C4 now live-
  verified and reported above.
- Whether to commit this dispatch doc + its `docs/INDEX.md` row in `~/hip-roadmap` is
  Bill's call, not taken here.
