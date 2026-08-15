# DISPATCH_TD126
Status: BUILT
Reconciled-Against: no code changed (analysis only)

**TYPE:** ANALYSIS

**REQ:** NONE. This dispatch produced findings and measurements, not a code
change. No requirements doc governs it because none was needed to trace and
measure — see CLAUDE.md Requirements Discipline item 10.

**Timestamp note (sourced honestly, not reconstructed):** no independent log
of the exact minute this dispatch was received exists. The stamp above
(18:46) is the timestamp of `td126_measure.py`, the script that produced
this doc's core measurement — the clearest sourced anchor available. The
preceding commit (`3c0cb74`, the D-03/D-18 build) landed at 18:19 MT per
`git show -s --format=%ad 3c0cb74`; this dispatch followed it. The window
between is UNSOURCED beyond that bound.

## THE ASK

Bill's dispatch, verbatim:

> "Three items from your TD-126 analysis, in order. REQ doc first on any
> code.
>
> 1. FIX min_tier="low". voice_orch.py:1393-1394 — the explicit upgrade
>    trigger ("it's me", "verify me") calls _tier() with min_tier="low",
>    which has no floor. speaker_id.py:326-332 returns "low" for ANY score
>    under 0.50, negatives included, as long as a print file exists. A guest
>    says "it's me", gets scored against both placeholders, sam's -0.028
>    beats maya's -0.121, and HIP says "Got it, I recognize you now" and
>    binds them to Sam.
>
>    Confident wrong identification. This is our integration bug, not a
>    Resemblyzer limitation. Fix the floor."

(Items 2 and 3 of that same dispatch, and the antecedent dispatch that
requested the analysis itself, are the subject of separate dispatch docs —
see OPEN below. This doc backfills the ANALYSIS dispatch that PRODUCED the
TD-126 findings items 1-3 argue from — i.e., the "Answer these four
questions" dispatch that preceded it:)

> "TD-126. Analysis only, no fix. This is script 2's foundation and script 2
> is one of two working demo scripts.
>
> demo_reset.py hardcodes ~/hip-harness for log/voiceprint paths regardless
> of which checkout invokes it. Proving D-03 live deleted maya's and sam's
> voiceprint enrollment on the frozen demo checkout at :7860. demo_seed.py
> recreates SYNTHETIC PLACEHOLDERS on reseed, not real enrollment.
>
> Script 2's entire premise is that HIP knows who is speaking.
>
> ANSWER THESE:
>
> 1. What is on :7860 right now — real voiceprints or placeholders?
>
> 2. THE ONE THAT MATTERS: with a placeholder in place, what does speaker
>    verification actually do? Read the Resemblyzer comparison code and the
>    threshold. Two possibilities:
>      a. It fails visibly — no match, HIP says it does not recognize the
>         speaker. Obvious, fixable, fine.
>      b. It matches anyway — a synthetic placeholder scores above threshold
>         against a real voice, and HIP confidently identifies Sam as Maya.
>         The demo runs, the panes light, it proves nothing, and nobody
>         knows.
>    Do not guess. Trace the code and say which, with file:line. If you
>    cannot determine it from the code, say so and propose the measurement.
>
> 3. Does the TEXT path use voiceprints at all, or is it the member
>    dropdown? If text is a dropdown, script 2 on text is unaffected and
>    only the voice leg is exposed. Say which.
>
> 4. What other checkouts can demo_reset.py reach and damage?
>
> Report with file:line. Propose nothing until I see it."

## WHAT WAS DONE

1. Read `harness/speaker_id.py` in full (thresholds, `_tier`, `verify`,
   `SpeakerVerifier`, `SpeakerEnroller`).
2. Read `scripts/demo_seed.py`'s `_ensure_voiceprint` (the synthetic-print
   generator) and confirmed its exact algorithm.
3. Decrypted the LIVE on-disk files at `~/hip-harness/data/voiceprints/
   {maya,sam}.npz` via `harness.speaker_id._load_voiceprint` and diffed them
   numerically against the exact synthetic generator (same seeds) to
   confirm — not infer — what is actually on disk.
4. Located a real recorded human voice sample already on this machine
   (`~/chatterbox-eval/samples/reference.wav`, from an unrelated prior TTS
   eval session) and embedded it via the real `harness.speaker_id._embed`
   (actual Resemblyzer `VoiceEncoder`, not a stub).
5. Computed real cosine similarity (`harness.speaker_id._cosine`) between
   that real embedding and: (a) the two live placeholder embeddings, (b) 300
   more synthetic vectors at other seeds for a distribution, (c) two more
   real audio samples from the same directory, as a same-real-voice /
   different-real-voice control.
6. Traced every call site of `SpeakerVerifier.verify` and
   `get_member_by_voice` (`server/voice_orch.py`, `server/voice_https_orch.py`,
   `harness/member_registry.py`) to find every `min_tier` value actually used
   in the running system, not just the one path in the ASK.
7. Traced `/api/text-query` in both `server/voice_https_orch.py` and
   `server/demo_dashboard.py`, and `demo_scripts/speaker_isolation__v20260715_1158.json`,
   to determine whether the text path ever calls into `speaker_id`.
8. Searched this machine for other checkouts (`find [REDACTED-USER-PATH] -maxdepth 1
   -iname "hip*"`) to bound the blast radius of `demo_reset.py`'s hardcoded
   path.

## WHAT WAS FOUND

**Q1 — what's on :7860 right now.** Synthetic placeholders, confirmed
numerically:
```
maya.npz: n_samples=3, matches synth(seed=7)  exactly: True
sam.npz:  n_samples=3, matches synth(seed=13) exactly: True
```
Generator: `scripts/demo_seed.py:178-182` (`_ensure_voiceprint`) —
`np.random.default_rng(seed=7 or 13).standard_normal(256)`, L2-normalized.
Pure Gaussian noise, no relation to recorded audio. File mtimes:
`maya.npz`/`sam.npz` both `Jul 16 18:16` (this session's own reset+reseed
cycles from the D-03 live proof); `bill.npz` untouched at `Jul 3 13:51`
(`demo_reset.py:34`, `KEEP_MEMBER = "bill"`).

**Q2 — measured, not guessed.** Thresholds: `config.yaml:114-116` (both
checkouts, identical), `high: 0.75`, `medium: 0.50`, cosine similarity
(`speaker_id.py:139-141` `_cosine`, `speaker_id.py:326-332` `_tier`).

Full number table (real voice = `reference.wav`, embedded via the real
Resemblyzer `VoiceEncoder`):
| comparison | score |
|---|---|
| ref vs itself (sanity) | 1.000 |
| ref vs a real clone of ref (same target speaker) | 0.913 |
| ref vs a different real TTS voice | **0.632** |
| ref vs maya's live placeholder (seed=7) | -0.121 |
| ref vs sam's live placeholder (seed=13) | -0.028 |
| maya's placeholder vs sam's placeholder | -0.021 |
| ref vs 300 more random synthetic vectors | mean 0.0025, std 0.0637, min -0.226, max 0.1815; 0 of 300 reach 0.20 |

Main per-turn attribution loop (`server/voice_orch.py:1330-1369`) only
accepts a candidate `if _TIER_RANK.get(_r.tier, 0) >= 2` (line 1350 —
medium/high only). Placeholder scores never clear 0.50, so both are
filtered before becoming `best_result`; `current_turn_member = None`, logged
`"no enrolled member matched — guest mode"` (line 1369),
`sensitivity_override = "high"` (line 1389). Same floor at
`harness/member_registry.py:203-240` (`get_member_by_voice`, default
`min_tier="medium"`) and `server/voice_https_orch.py:308`, which on no
match returns the literal string `"I don't recognize your voice..."`
(lines 329-335). **This is (a): visible, safe failure**, for the default
path.

**The exception — a real (b)-shaped hole**: `server/voice_orch.py:1393-1394`,
the explicit self-ID trigger (`_UPGRADE_TRIGGER`, line 412 — "it's me",
"verify me", "i am <name>"), calls `get_member_by_voice(audio_bytes,
min_tier="low")`. `_tier()` (`speaker_id.py:326-332`) has no floor below
"low" — it returns "low" for any score under 0.50 including deeply negative
ones, as long as a print file exists at all (`tier="unenrolled"` fires only
when there is no file, `speaker_id.py:341-344`). At `min_tier="low"` the
acceptance filter is `tier_rank>=1` (`member_registry.py:217-218,237`),
which a placeholder's score always clears. Sam's placeholder (-0.028) beats
maya's (-0.121) on `score > best_score`; the system would say "Got it, I
recognize you now" (`voice_orch.py:1401`) and bind the speaker to Sam's
identity. This is what item 1 of Bill's follow-up dispatch orders fixed.

**Q3 — text path.** Dropdown-equivalent, confirmed by grep, zero hits:
`server/demo_dashboard.py` has no reference to `speaker_id`/
`SpeakerVerifier`/`voiceprint`/`get_member_by_voice` anywhere.
`server/voice_https_orch.py`'s only voiceprint code is the unrelated
`/api/enroll` and `/api/voice-query` endpoints — not what
`demo_scripts/*.json` calls. `demo_scripts/speaker_isolation__v20260715_1158.json`
turns carry an explicit `"member": "bill"`/`"sam"` string field, which is
what the demo player posts to `/api/text-query`. Script 2, as actually run
(scripted, via this JSON), never touches a voiceprint. The exposure is
scoped to a live-mic variant, which
`docs/demo_prep/HIP_DemoScript02_SpeakerIsolation__prep__v20260715_1000.md:117,191`
had already flagged as an unquantified soft spot before this dispatch,
independent of it.

**Q4 — blast radius.** `scripts/demo_reset.py:27`,
`_HARNESS_ROOT = pathlib.Path.home() / "hip-harness"` — a literal string,
not derived from `__file__`, resolves identically regardless of invoking
checkout. Damages (per-invocation): `logs/voice_orch.log`,
`logs/router.jsonl` (lines 29-30), and every non-Bill voiceprint under
`data/voiceprints/` (line 37 `_VOICEPRINTS_DIR`, deleted at line 88's loop
which excludes only `KEEP_MEMBER = "bill"`). `turns_demo.jsonl` (line 31) IS
correctly checkout-relative (`ROOT = pathlib.Path(__file__).parent.parent`,
line 22). Neo4j/registry deletion are correctly scoped via `NEO4J_URI`/
`HIP_REGISTRY_DB` env vars. Only one other checkout exists on this machine
(`find [REDACTED-USER-PATH] -maxdepth 1 -iname "hip*"` →`hip-harness`, `hip-dev`,
and an empty non-repo directory `[REDACTED-USER-PATH]/HIP`) — so the blast radius
today is exactly `hip-harness`, unconditionally, from any invoking checkout.

## VERIFIED

**Watched run** (not reasoned about):
- The exact byte-for-byte identity of the live `maya.npz`/`sam.npz` files
  against the synthetic generator (`np.allclose`, `atol=1e-6`, both `True`).
- All cosine-similarity numbers in the table above — every one is the
  output of an actual `harness.speaker_id._embed`/`_cosine` call against
  real audio and the real live placeholder files, not a simulated or
  assumed embedding space.
- The zero-hits grep confirming no voiceprint code path exists in
  `demo_dashboard.py`.
- The single other-checkout directory search (`find`).

**Reasoned about** (from code, not independently run):
- That `server/voice_orch.py:1330-1369`'s attribution loop would behave as
  described for the placeholders — this follows deterministically from the
  measured scores plus the threshold code, but was not separately exercised
  as a live end-to-end voice turn (no live mic session was run against
  :7860 during this dispatch).
- That the "it's me" upgrade path would actually bind to Sam in a live
  session — same basis: the score comparison is real and measured, the
  code path that CONSUMES it (`voice_orch.py:1393-1404`) was read and cited
  by line, but not exercised live end-to-end (no real guest audio was
  played through the actual running :7860 pipeline).

## HASH

NONE. No code changed in this dispatch — analysis and measurement only, per
Bill's explicit "Analysis only, no fix" framing. The two code fixes this
analysis fed are BUILD dispatches of their own (see OPEN).

## OPEN

- The floor fix (item 1: bound `min_tier="low"` with an actual lower cutoff)
  and the `demo_reset.py` checkout-scoping fix (item 2) are follow-on BUILD
  work, not covered by this ANALYSIS dispatch — each needs its own REQ doc
  per CLAUDE.md item 8 before any code lands.
- Item 3 of Bill's follow-up dispatch (register speaker verification as its
  own "stand-in, not a component" defect; update the Script 02 prep doc to
  say text-path is voiceprint-free) is documentation work, separate from
  this analysis and from the two code fixes.
- Whether a live end-to-end voice session against the ACTUAL :7860 process
  reproduces the reasoned-about behavior exactly as traced was not tested
  (would require a live mic session, out of scope for a text-path-focused
  analysis session).
- The 0.632-real-different-voice-vs-0.50-threshold finding (item 3 of the
  follow-up dispatch) raises a question this analysis did not resolve:
  whether the "medium" threshold itself is well-calibrated at all for
  distinguishing different real speakers, independent of the placeholder
  question. That is a separate, larger question about Resemblyzer's
  suitability as a verifier, not this dispatch's scope.
