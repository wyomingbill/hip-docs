# REQ_TD126_REMEDIATION
Status: BUILT
Reconciled-Against: (see commit for hash)

Parent context: `docs/dispatches/DISPATCH_TD126__speaker-verification-floor-analysis__v20260716_1846.md`
(the ANALYSIS dispatch that found both defects this REQ fixes). No REQ
governs the analysis itself (ANALYSIS dispatches may have REQ: NONE, per
CLAUDE.md item 10) — this REQ exists because items 1 and 2 of the follow-up
dispatch are code changes, and code changes need one (CLAUDE.md item 8).
Item 3 of that same dispatch (register a new defect, update a prep doc) is
documentation only and is handled separately, without a REQ, since it
touches no code.

## THE REQUIREMENT

Bill's words, verbatim (items 1 and 2 of the three-item dispatch; item 3 is
out of scope for this REQ, see above):

> "1. FIX min_tier="low". voice_orch.py:1393-1394 — the explicit upgrade
> trigger ("it's me", "verify me") calls _tier() with min_tier="low", which
> has no floor. speaker_id.py:326-332 returns "low" for any score under
> 0.50, negatives included, as long as a print file exists. A guest says
> "it's me", gets scored against both placeholders, sam's -0.028 beats
> maya's -0.121, and HIP says "Got it, I recognize you now" and binds them
> to Sam. Confident wrong identification. Our integration bug, not
> Resemblyzer's.
>
> 2. FIX demo_reset.py:27. _HARNESS_ROOT is a literal Path.home() /
> "hip-harness", not derived from __file__, so it reaches across checkouts
> unconditionally. Derive it from __file__ like turns_demo.jsonl already
> does at line 22."

## THE ACCEPTANCE TEST

**Item 1 (floor):**
1. A score that is genuine noise relative to any real voice (measured:
   random 256-dim unit vectors against a real Resemblyzer embedding of
   actual recorded audio score in [-0.226, +0.182] over n=300, mean 0.0025,
   std 0.0637) must NOT clear whatever floor `min_tier="low"` requires.
2. The specific reported case — a guest saying an upgrade-trigger phrase
   while `hip-harness`'s current placeholders are on file — must return
   "I still don't recognize your voice," not a false bind to Sam or Maya.
   Re-run the exact measured comparison (`ref` vs the live `maya.npz`/
   `sam.npz` placeholders) through the actual `SpeakerVerifier`/`_tier`
   code path post-fix and confirm neither clears the new floor.
3. A score that plausibly represents "the same voice, degraded audio" must
   STILL clear the floor — the fix must not collapse the upgrade path's
   stated design purpose (a lower bar than the main attribution loop's
   "medium," for a voice that's a genuine but imperfect match) into
   requiring full "medium" and making the upgrade trigger pointless.
4. `harness/member_registry.py`'s and `server/voice_orch.py`'s
   `_TIER_RANK` dicts must treat the new below-floor case consistently as
   "does not count," at every `min_tier` value used anywhere in the
   codebase (grepped and enumerated in the dispatch: `"medium"` at two
   sites, `"low"` at one).

**Item 2 (checkout-scoped reset):**
5. Running `scripts/demo_reset.py` from hip-dev must truncate hip-dev's own
   `logs/voice_orch.log` and `logs/router.jsonl` (checkout-relative,
   matching what `server/demo_dashboard.py:62,65` and
   `server/voice_https_orch.py:32` already read/write at) — NOT
   hip-harness's copies.
6. Verify by inspecting file mtimes before/after a live run: hip-harness's
   `logs/voice_orch.log`/`router.jsonl` must be untouched; hip-dev's own
   `logs/voice_orch.log`/`router.jsonl` (creating them if absent) must be
   the ones truncated.

**RESULTS — all six watched live, 2026-07-16:**

1/2/4. Re-ran the exact measured comparison through the real
`SpeakerVerifier`/`_tier` post-fix:
```
maya (seed=7 placeholder):  score=-0.1211 tier=no_match  (was "low")
sam  (seed=13 placeholder): score=-0.0282 tier=no_match  (was "low")
```
`get_member_by_voice(ref_bytes, min_tier="low")` — the exact call site at
`voice_orch.py:1394` — no longer matches either placeholder. Second probe
with an entirely different, unrelated voice sample (`01_default_voice.wav`,
not `reference.wav`): `maya score=0.0216 tier=no_match`, `sam score=-0.0885
tier=no_match` — confirms the fix isn't an artifact of one specific probe
sample. PASS.

3. Bill's own real, untouched print (`bill.npz`, never reset — `KEEP_MEMBER`)
scored `0.6768`/`0.6537` against two different real audio samples — both
correctly `tier="medium"`, both correctly clear `min_tier="low"`'s floor
and get identified. The upgrade path's genuine-match case is unaffected by
the new floor. PASS. (Note: this also independently reproduces item 3's
finding — a different real voice recording scores in the medium band
against Bill's own print, not just against the synthetic control from the
original analysis — logged there, not re-litigated here.)

4. `_TIER_RANK` updated at both consumer sites
(`harness/member_registry.py:217-220`, `server/voice_orch.py:1340-1342`);
`"no_match"` ranked with `"unenrolled"` at 0 in both.

5/6. Ran the fixed `scripts/demo_reset.py --yes` live. Before: hip-dev
`logs/router.jsonl` = 101091 bytes (real data), no `voice_orch.log`;
hip-harness's copies both 0 bytes (already zeroed by this session's earlier,
pre-fix runs). After: hip-dev `logs/router.jsonl` truncated to 0 bytes,
mtime updated to the run time; hip-harness's `logs/voice_orch.log`/
`router.jsonl` mtimes UNCHANGED (still the pre-fix timestamp) — confirmed
not touched. PASS. (Voiceprint deletion still targets hip-harness for
maya/sam specifically, unchanged — see CONSTRAINTS above; that is the
registry's recorded path, not this constant, and is explicitly out of
scope for this REQ.)

Full baseline (Neo4j facts + registry members, incidentally cleared by
running the live reset for verification) restored via `demo_seed.py`
afterward.

## WHAT'S ALREADY DONE

- The measurement backing item 1's floor choice: `docs/dispatches/
  DISPATCH_TD126__speaker-verification-floor-analysis__v20260716_1846.md`
  — real voice vs. live placeholders (-0.121, -0.028), a 300-sample null
  distribution (max 0.1815), and the real-different-voice control (0.632),
  all against the actual `harness.speaker_id._embed`/`_cosine`, not a
  simulated embedding space.
- D-03/D-18 (`3c0cb74`) and item 0 (`c86a414`) — unrelated, unaffected by
  this REQ.

## WHAT'S KNOWN BROKEN (before this build)

- `harness/speaker_id.py:326-332` (`_tier`): only two cut points
  (`high`=0.75, `medium`=0.50); anything below `medium` is unconditionally
  `"low"`, with no lower bound. `speaker_id.py:341-344`'s `"unenrolled"`
  fires only when NO print file exists at all — a print that exists but
  scores like pure noise is indistinguishable, in the tier label, from a
  genuine (if weak) partial match.
- `server/voice_orch.py:1393-1394` is the only consumer of `min_tier="low"`
  in the codebase (confirmed by grep of every `min_tier`/`get_member_by_voice`
  call site) and therefore the only place this floor gap is reachable today.
- `scripts/demo_reset.py:27`, `_HARNESS_ROOT = pathlib.Path.home() /
  "hip-harness"` — a literal string, not derived from `__file__`. Reaches
  hip-harness's `logs/voice_orch.log`/`router.jsonl` regardless of invoking
  checkout, and — this REQ's own new finding, not previously stated in the
  dispatch — simultaneously means a hip-dev-invoked reset NEVER truncates
  hip-dev's OWN real log files at `hip-dev/logs/`, since nothing in the
  current `_LOGS` list points there for those two entries. The bug is not
  just "reaches too far," it's "reaches the wrong place instead of the
  right one."

## CONSTRAINTS

- **Floor value is a judgment call, not specified by the dispatch.** This
  REQ proposes 0.30 (config-driven, following this module's own stated
  convention — "behaviour changes are config edits, never code edits,"
  `speaker_id.py:19` — not a hardcoded number), justified by: 300 measured
  random-vector-vs-real-voice samples never exceeding 0.1815, giving 0.30 a
  ~2.5x-observed-max margin above real measured noise. Open to
  recalibration by Bill; not asserted as definitively correct, only as
  measured and reasoned.
- **Do not silently narrow the upgrade-trigger feature's stated purpose.**
  `voice_orch.py:1391-1392`'s own comment says the lower threshold exists
  so "a nearly-enrolled voice can self-identify" — i.e., the design intent
  was a genuine, bounded second-chance band below "medium," not merely "the
  same bar as everywhere else." The fix must give `"low"` a real floor, not
  eliminate the band by raising the effective bar to `"medium"`.
- **hip-harness (`~/hip-harness`) is a separate, frozen checkout with its
  own git remote.** This REQ fixes `scripts/demo_reset.py`,
  `harness/speaker_id.py`, and `config.yaml` in the hip-dev checkout only.
  hip-harness carries its own copies of all three files
  (`~/hip-harness/scripts/demo_reset.py`, `~/hip-harness/harness/
  speaker_id.py`, `~/hip-harness/config.yaml`) and is NOT touched by this
  build — flagged as an open item, not silently left inconsistent.
- **Must not regress D-03/D-18 or item 0** (unrelated code, but both live
  in files adjacent to this session's other work — `voice_orch.py`). No
  change to the confirmation gate or F3 gate paths.
- Verify the acceptance test live where a live measurement is possible
  (item 1: re-run the actual comparison through `SpeakerVerifier`/`_tier`
  post-fix); item 2's log-truncation behavior is directly observable via
  file mtimes and does not require a live voice/Groq/Neo4j session.
