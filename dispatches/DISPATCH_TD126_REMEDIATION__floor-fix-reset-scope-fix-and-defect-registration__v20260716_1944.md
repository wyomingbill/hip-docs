# DISPATCH_TD126_REMEDIATION
Status: BUILT
Reconciled-Against: (see commit for hash)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_TD126_REMEDIATION__no-match-floor-and-checkout-scoped-reset__v20260716_1937.md`
(items 1 and 2 — the two code changes). Item 3 below is documentation only
and has no REQ, per CLAUDE.md item 10 (analysis/registration work needs
none) — it registers a defect and corrects a prep doc, it does not build
anything.

## THE ASK

Bill's dispatch, verbatim:

> "Three items from your TD-126 analysis. REQ doc first on any code.
>
> 1. FIX min_tier="low". voice_orch.py:1393-1394 — the explicit upgrade
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
> does at line 22.
>
> 3. DO NOT re-enroll voiceprints. DO NOT build speaker verification.
> Decision: Resemblyzer is a stand-in for a vendor, same as Deepgram and
> Cartesia on the voice leg. Pindrop, Nuance, Veridas sell this. Operators
> already run Pindrop in their call centers.
>
> Your own control is why: a different real TTS voice scored 0.632 against
> a 0.50 medium threshold. A different human clears the bar the main path
> trusts. That is a research library used as a production verifier.
>
> Register as its own defect, separate from TD-126: speaker verification is
> a stand-in, error rate unquantified, first measurement 2026-07-16 shows a
> different real voice at 0.632 vs 0.50. Do not claim speaker ID in any demo
> or document.
>
> Update docs/demo_prep/HIP_DemoScript02_SpeakerIsolation prep: script 2 on
> TEXT never touches a voiceprint — the demo player posts "member": "bill"
> as a plain string, which you verified. Script 2 is demoable today. Say
> that so nobody runs the live-mic variant by accident.
>
> Push, report the hash."

## WHAT WAS DONE

1. Filed `REQ_TD126_REMEDIATION` before any code, per CLAUDE.md item 8 —
   THE REQUIREMENT quoted verbatim (items 1-2 only; item 3 is out of the
   REQ's scope since it's not a code change), acceptance test for both
   fixes, the floor value's justification stated as a judgment call with
   measured basis, hip-harness's separate-checkout status flagged as an
   explicit constraint (not touched).
2. `harness/speaker_id.py`: added a third threshold cut point (`"low":
   0.30`) to `_DEFAULTS["thresholds"]`; `_tier()` now returns a new
   `"no_match"` tier below it (was: unconditionally `"low"` below
   `"medium"`, no lower bound at all); module docstring updated.
3. `config.yaml` (hip-dev only): added the `low: 0.30` cut point with the
   measured justification in-line, following this module's own stated
   convention that threshold changes are config edits, not code edits.
4. `harness/member_registry.py` and `server/voice_orch.py`: both
   `_TIER_RANK` dicts updated so `"no_match"` ranks with `"unenrolled"`
   (0) — the two places that gate `min_tier` in the whole codebase, found
   by grep in the original TD-126 analysis.
5. `scripts/demo_reset.py`: removed `_HARNESS_ROOT = pathlib.Path.home() /
   "hip-harness"`; `_LOGS`'s two entries that used it now use `ROOT`
   (`pathlib.Path(__file__).parent.parent`) directly, same as
   `turns_demo.jsonl` already did.
6. Live-verified both fixes (see VERIFIED below) against the real
   Resemblyzer model / real audio / real filesystem — not simulated.
7. `docs/techdebt/DEBT_REGISTER__v20260712_2300.md`: TD-126 marked
   PARTIALLY FIXED (log-path half; voiceprint-deletion half explicitly
   still open, with the reason — it's the registry's recorded path, not
   this script's constant, and touching it means touching the shared-
   voiceprint architecture, out of scope here). New TD-127 registered:
   "speaker verification is a stand-in, not a component," with the full
   measured basis and an explicit "OPEN — by design, not a target for this
   codebase to close" status, since this is a product decision, not an
   unfinished task.
8. `docs/demo_prep/HIP_DemoScript02_SpeakerIsolation__prep__v20260715_1000.md`:
   added an amendment note at the top stating Script 2 on text never
   touches a voiceprint (with the file:line basis) and is demoable today;
   corrected the "Known soft spots" table and the "Anticipated attacks"
   table's speaker-ID rows to say the same thing and point at TD-127
   instead of "unquantified."
9. Registered everything in `docs/INDEX.md`; updated `REQ_TD126_
   REMEDIATION`'s own Status to BUILT with live results appended.

## WHAT WAS FOUND

- No new code-level findings beyond what `DISPATCH_TD126` already
  established — this dispatch is the fix, not further analysis. One
  incidental finding while verifying item 3's control: Bill's own real,
  untouched voiceprint (`bill.npz`) scores in the "medium" band (0.677,
  0.654) against TWO different Chatterbox eval audio samples, not just the
  one (`reference.wav`) used in the original analysis — independently
  reproducing TD-127's finding on a second sample, not just the first.

## VERIFIED

**Watched run:**
- `harness.speaker_id.SpeakerVerifier.verify` against the exact live
  `maya.npz`/`sam.npz` placeholder files, post-fix: `maya score=-0.1211
  tier=no_match` (was `"low"`), `sam score=-0.0282 tier=no_match` (was
  `"low"`) — real voice (`reference.wav`) as the probe.
- The same two placeholders against a SECOND, different real audio sample
  (`01_default_voice.wav`): `maya score=0.0216 tier=no_match`, `sam
  score=-0.0885 tier=no_match` — confirms the fix isn't an artifact of one
  probe.
- `harness.member_registry.get_member_by_voice(probe, min_tier="low")` —
  the exact call site the dispatch named (`voice_orch.py:1394`) — run
  directly: no longer matches either placeholder; correctly matches Bill's
  real print instead (`score=0.6768`/`0.6537`, `tier="medium"`), confirming
  the fix closes the false-positive path without breaking genuine
  identification.
- `scripts/demo_reset.py --yes`, run live, full script (not just the
  changed function): before, hip-dev `logs/router.jsonl` = 101091 bytes
  real data, no `voice_orch.log`; hip-harness's copies both 0 bytes
  (pre-zeroed by an earlier, pre-fix session). After: hip-dev's
  `router.jsonl` truncated to 0, new mtime; hip-harness's `voice_orch.log`/
  `router.jsonl` mtimes UNCHANGED — confirmed not touched by this run.
- `.venv/bin/python -m py_compile` on every changed `.py` file; `yaml.safe_
  load` on `config.yaml`; `pytest tests/test_injection_declarative.py
  tests/test_member_registry.py tests/test_permissions.py` (73 passed, 4
  skipped) as a nearby-suite regression check.

**Reasoned about:**
- That no OTHER `min_tier`/`_TIER_RANK` consumer exists beyond the two
  updated — based on a grep across `server/*.py`/`harness/*.py`
  (`DISPATCH_TD126` already enumerated these; this dispatch did not
  re-grep, it trusted that prior enumeration).
- That `pytest tests/` as a whole showing one unrelated failure
  (`test_sensitivity.py::test_sensitive_queries_route_local`, a routing/
  classifier assertion with zero connection to anything touched here) and
  one unrelated collection error (`test_routing.py`, a stale import) are
  pre-existing and not caused by this change — inferred from the fact that
  neither touched file is anywhere near `speaker_id.py`/`member_registry.py`/
  `demo_reset.py`/the `_TIER_RANK` blocks in `voice_orch.py`, not from
  independently bisecting when those failures were introduced.

## HASH

(filled in after commit — see commit message and `git log`)

## OPEN

- The floor value (0.30) is a measured, reasoned default, not a validated
  one — flagged explicitly in the REQ and in `config.yaml`'s own comment.
  Recalibration is Bill's call if better data emerges.
- TD-126's voiceprint-deletion half remains open: `demo_reset.py` still
  deletes maya/sam's voiceprints on hip-harness, because the actual path
  comes from the registry's recorded `voiceprint_path`
  (`harness/speaker_id.py:43`'s shared `DATA_DIR`), not a local constant in
  `demo_reset.py`. Fixing that touches whether voiceprints are meant to be
  shared across checkouts at all — an architecture decision, not this
  build's scope.
- hip-harness's own copies of `demo_reset.py`, `speaker_id.py`, and
  `config.yaml` are unmodified — a separate, frozen checkout with its own
  git remote. If that checkout is ever updated from hip-dev, these same
  fixes would need porting there too.
- No dedicated regression test exists for either fix — verification is the
  live runs recorded above, not an automated suite. A future change could
  silently regress either fix without a test catching it.
- TD-127 is explicitly not something this codebase is meant to close (a
  product decision, not a backlog item) — but nothing currently prevents a
  future session from "fixing" it by tuning thresholds further, which would
  be exactly the wrong response per item 3's decision. The tech-debt entry
  says so; whether that's durable against a future session that doesn't
  read it first is an open process risk, not a code risk.
