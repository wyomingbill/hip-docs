# REQ_STRIP_CONTEXT_COMPLETENESS
Status: SUPERSEDED — by REQ_STRIP_CONTEXT_COMPLETENESS__header-rename-facts-about-other-people__v20260803_0731.md (D-117: Bill's 2026-08-02 header-rename ruling; acceptance re-based on the new literal and re-run there). The MET ruling below stands as the record for the OLD header literal's acceptance; it is not revoked, it is superseded.
Status-at-supersession: MET
MET-Ruling: Bill, 2026-07-29 (D-20 dispatch) -- item 4's intent (no
regression in the strip) is satisfied by the recorded prior-session
baseline plus every green run since, including the 2026-07-28 --full run
(DISPATCH_44, where L7:CTX-STRIP passed with both fault-injection
directions in the log). Items 1/2/3/5 were confirmed against that same
run by DISPATCH_44; item 4's literal same-session before/after pairing is
ruled unnecessary to its purpose. Further ruled: this REQ's own
CONSTRAINTS line forbidding --full for its verification is SUPERSEDED by
CLAUDE.md Requirements Discipline item 12 (--full is the house bar for
done), resolved in practice by Dispatch 44's full run
Reconciled-Against: harness/orchestrator.py at HEAD (D-28, roadmap defect
register), no prior commit touches this bug

## UPDATE 2026-07-27 (later, same day)

All five acceptance items built and verified at Layer 7 scope, in three
checkpointed commits (REQ doc `f2deae1`, the fix `95327c0`, the check —
this commit, hash in that commit's own message). `L7:CTX-STRIP` (ABSOLUTE
tier) PASSES 5/5 of its own checks: the real-prompt positive case (all
three sections), D-28's own exact triggering shape (other-people section
only — the one that reproduced the bug pre-fix), the fault-injection twin
RED (a synthetic fourth section survives when unregistered) and GREEN (the
identical prompt strips clean once `FACT_BEARING_SECTION_HEADERS` covers
it), and a restoration proof (the monkeypatch is fully undone). Registered
in `check_registry.py` with real (non-debt) twin/fixture/coverage/
metamorphic(na) artifacts — verified directly against source, not assumed.
`python -m eval.harness --layer 7`: `L7: 25/25` (up from 24/24),
`four-part-roster PASS` (57 checks, 35 flagged gaps — unchanged, CTX-STRIP
added zero new flags), `RATCHET PASS`. `git diff` confirms zero changes to
`server/` this entire session — the MID/CORE constraint holds by
construction, nothing there was touched.

**Not marked MET**, for two honest reasons, not a formality: (1) this
session was scoped to `--layer 7` only, never `--full` — CLAUDE.md item 12
makes the full ratchet the actual bar for "done," and that has not run
against this change; (2) acceptance item 4 asks for RATCHET PASS both
BEFORE and AFTER this build, and only the AFTER run happened inside this
session's own scope (the immediately-prior state was last confirmed green
in an earlier, separate session's work, not re-verified as a same-session
baseline here). Reports readiness; Bill decides. `docs/INDEX.md` was
deliberately not touched or updated to reflect this REQ, per this
session's own explicit instruction (another session holds it) — the
registration is outstanding, not forgotten.

## THE REQUIREMENT

Bill's words, verbatim:

> Fix D-28. This is the narrow bug, not TD-131's open decision.
>
> _PERSONAL_SECTION_RE at harness/orchestrator.py:655-658 matches only two of
> the three fact-bearing system-prompt section headers. The third, "Confirmed
> facts about other people", carries cross-member household facts and passes
> through strip_context_for_tier unmodified because the truncation logic at
> :683-687 leaves the prompt untouched on no match. The three sections at
> :388-392, :414-420 and :429-444 are independently conditional, so a turn
> where only the third is populated is stripped of nothing.
>
> The requirement: strip_context_for_tier must strip every fact-bearing
> section, not a subset. The regex must be derived from the same source that
> defines the section headers, so adding a fourth section cannot silently
> escape stripping again.
>
> Acceptance: a layer-7 check, hard zero, that a frontier-bound prompt
> contains no fact-bearing section. Fault-injection twin both directions: a
> fourth synthetic section escapes stripping and the check goes red, then
> goes green when the derivation covers it. Plus the harness-discipline
> four. RATCHET green before and after.
>
> Do NOT extend stripping to MID or CORE. That is TD-131 and it is Bill's
> open decision. State that boundary in the REQ.

Expanded: this REQ closes exactly one gap — the THIRD section header
("Confirmed facts about other people") missing from `_PERSONAL_SECTION_RE`'s
alternation at `harness/orchestrator.py:656` — for the frontier tier's
EXISTING call sites (`server/voice_orch.py:1825`, `:1902`, `:3239`, all
`tier="frontier"`). It does not add any NEW call to `strip_context_for_tier`
for MID or CORE tiers, and does not touch whether or where those tiers call
it. That is TD-131 — the standing debt entry that the text-query path
(`process_text_query`) never calls `strip_context_for_tier` at all for
mid/core — and it stays explicitly OUT OF SCOPE here, pending Bill's own
open decision on it. See CONSTRAINTS below; this boundary is load-bearing,
not a footnote.

## THE ACCEPTANCE TEST

1. A new hard-zero, ABSOLUTE-tier Layer 7 scenario (`L7:CTX-STRIP`) asserts:
   given a REAL system prompt built by `TurnOrchestrator.local_system_prompt()`
   with all three fact-bearing sections populated (mem/"Recent context",
   known/"Things you know", other_subject_facts/"Confirmed facts about other
   people"), `strip_context_for_tier(messages, "frontier", query)`'s output
   contains NONE of the three section headers. Count of surviving
   fact-bearing sections in the stripped output: must be 0.
2. Fault-injection twin, both directions, on the SAME scenario:
   - RED: a synthetic fourth section header, not present in the code's
     derivation source, is appended to a system prompt; the SAME stripping
     call leaves it un-stripped (the check fires, naming the surviving
     section).
   - GREEN: the derivation source itself (the shared header list, not the
     regex directly) is extended to include the synthetic header; the
     IDENTICAL stripping call now removes it. This proves the mechanism —
     not just today's three hardcoded strings — is what closes the gap.
3. `eval/harnesslib/check_registry.py` carries a real (non-debt) entry for
   `L7:CTX-STRIP` with all four REQ_HARNESS_DISCIPLINE artifacts:
   fault-injection twin (item 2 above), ground-truth fixture (a
   human-verified expected section-header list, not model-graded),
   coverage entry (which section/tier slice this covers, and which it
   explicitly does not — mid/core), metamorphic wrapper or an honest `na`
   if a rewording wrapper does not apply to a fixed-vocabulary
   section-header check (stated, not assumed away).
4. `python -m eval.harness --layer 7` (never `--full` for this REQ's own
   build/verification): RATCHET PASS, both before this build (baseline) and
   after (the new check joins the roster clean — `four-part-roster PASS`
   recognizes `L7:CTX-STRIP` by name, 0 missing artifacts).
5. No call site in `server/voice_orch.py` or elsewhere gains a NEW call to
   `strip_context_for_tier` for `tier in ("mid", "core")`. Grepped and
   confirmed unchanged from this REQ's own baseline commit.

## WHAT'S ALREADY DONE

- `strip_context_for_tier` exists and is called for `tier="frontier"` at
  four sites in `server/voice_orch.py` (`:1825`, `:1902`, `:1986` — this one
  is the mid/core `groq_messages` call, unaffected by this REQ, see WHAT'S
  KNOWN BROKEN — and `:3239`). The frontier-tier truncation mechanism
  itself (cut the system prompt at the first matched personal-section
  boundary, drop all conversation history, send only system+query) is
  correct in shape; only the MATCH SET is incomplete.
- The three fact-bearing sections it must strip are independently
  conditional and already well understood: `harness/orchestrator.py:388-392`
  (mem/"Recent context about this person"), `:414-420` (known/"Things you
  know about this person"), `:429-444` (other_subject_facts/"Confirmed
  facts about other people", TD-119's own third-party section).
- Sensitive prior-turn filtering (`strip_context_for_tier`'s step 3,
  `:707-720`, via `_is_query_sensitive`) is a SEPARATE mechanism from the
  system-prompt section strip and is not touched by this REQ.

## WHAT'S KNOWN BROKEN

- `_PERSONAL_SECTION_RE` (`harness/orchestrator.py:655-658`) is a
  hand-written regex alternation naming only two of the three section
  headers. When a turn's system prompt contains the third section
  ("Confirmed facts about other people") but NEITHER of the other two,
  `_PERSONAL_SECTION_RE.search()` returns `None`, and the truncation logic
  (`:683-687`) falls back to `clean_sys = sys_content` — the ENTIRE system
  prompt, cross-member facts included, is sent unmodified to the
  frontier-tier off-device call. This is D-28 exactly, not a hypothetical.
- The header text is duplicated by hand in two places today — the f-string
  literals that BUILD each section (`:390`, `:417`, `:442`) and the regex
  that MATCHES them (`:656`) — with nothing enforcing they stay in sync.
  This is the root cause, not just the immediate two-of-three miss: a
  future fourth section (or a rename of an existing one) has no structural
  reason to also update the regex, and would silently repeat D-28.
- TD-131 (a SEPARATE, pre-existing debt entry — on `main`'s register, and
  echoed by roadmap's own `D-28` filing): the MID/CORE tiers do not call
  `strip_context_for_tier` at all on the text-query path
  (`process_text_query`). This is a real gap but a DIFFERENT one — whether
  MID/CORE should be stripped at all is an open product decision (does the
  off-net boundary start at frontier only, or at mid/core too?), not a
  regex-completeness bug. Not touched here.

## CONSTRAINTS

- Do NOT extend `strip_context_for_tier` calls to MID or CORE tiers. That
  decision belongs to TD-131 and is Bill's to make, not this REQ's to
  preempt by shipping the capability quietly alongside a bug fix.
- Do NOT change `strip_context_for_tier`'s existing behavior for any
  currently-passing case — only the previously-unmatched third section
  newly gets stripped; the frontier truncation shape (drop history,
  system+query only) and the sensitive-history filter (step 3) are
  unchanged.
- Layer 7 only for this REQ's own verification — no `--full`. No graph
  reset, no reseed. The new check must not require either (THE ACCEPTANCE
  TEST item 1 builds its system prompt from hand-supplied fact dicts via
  `TurnOrchestrator.local_system_prompt()` — no live graph read/write is
  needed for the section-header text itself).
- RATCHET must stay green throughout — a hard-zero ABSOLUTE-tier check
  joining the roster is additive; it must never cause an existing scenario
  to regress.
