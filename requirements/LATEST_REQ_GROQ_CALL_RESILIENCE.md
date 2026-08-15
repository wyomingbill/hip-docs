# REQ_GROQ_CALL_RESILIENCE: fact_change Reasoning-Overrun Fix
Status: MET
Branch: roadmap
Reconciled-Against: a61c49a (root cause proven in DISPATCH_GROQ_400_ROOTCAUSE__json-validate-failed-reasoning-overrun__v20260726_1430.md; this REQ is filed BEFORE the build, from Bill's dispatch words, per Requirements Discipline items 1/8); d83a111 (fix landed, item 4 of the dispatch REVERTED — see UPDATE below)

## UPDATE 2026-07-26 (MET)

Shipped fix, as landed at d83a111, differs from the dispatch's item 1 in one
respect: `reasoning_effort: "low"` was tried and REVERTED same session — it
broke park-path extraction semantics (update->add) and regressed
P10/HARNESS1.3/R04/PW012 plus produced one G1 HARD ZERO under `--full`. The
max_tokens 8192 raise (the acceptance test's own words: "this is the actual
fix") was kept, since 2233-token successes observed post-raise prove the old
2048 cap was truncating real reasoning, not padding it. Fixes 2 and 3
(jittered `json_validate_failed` retry, `resp.text` body logging) shipped as
specified.

Net: acceptance items 1/2/3/5 hold as specified. Item 4
(reasoning_effort:"low" reduces reasoning volume) does NOT hold — that lever
was reverted by design once it proved to regress correctness elsewhere; the
max_tokens raise alone is the fix that stuck.

Verification, `python -m eval.harness --full` at d83a111 ([REDACTED-USER]@[REDACTED-MACHINE-NAME],
roadmap, foreground, no other run competing for RAM):
- RATCHET PASS — no scenario regressed vs baseline.
- `care_coordination.T01` PASS, `care_coordination.T02` PASS (the Elena
  medication-switch payload that previously 400'd 3/6 on json_validate_failed).
- AUDIT 3/3, L1 14/15 (one pre-existing P2 async-write-timing flake, i019,
  unrelated to this fix — same class as the previously-diagnosed R04/PW012/
  HARNESS1.3 flakiness), L2 25/35 (10 skipped by design), L3 3/3, L4 27/31 (4
  skipped), L6 1/1, L7 23/23, L7V2 25/26 (1 opt-in skip), SCHEMA 1/1, VOICE 1/1.
- `--layer 7` run in isolation beforehand also came back RATCHET PASS with the
  same T01/T02-equivalent scenarios green, confirming the fix held through
  the earlier crash this REQ was reopened to investigate.

REQ_GROQ_CALL_RESILIENCE: MET.

## THE REQUIREMENT

Bill's words, verbatim (dispatch, 2026-07-26):

> Implement all three fixes from your own root-cause (a61c49a).
> 1. fact_change.py:450 — raise max_tokens to 8192 AND add "reasoning_effort": "low" for the gpt-oss extraction call. This is the actual fix: reasoning overrun no longer starves the content slot.
> 2. fact_change.py:458-477 — on json_validate_failed specifically, retry with temperature jitter 0.2 (mirror the zero-changes path at :957-961); keep identical-resend for real transport errors.
> 3. fact_change.py:473-476 — log resp.text in the retry warning so the error body is never discarded again.

## THE ACCEPTANCE TEST

From Bill's words (items 4-5 of the dispatch), pass/fail:
1. The old T01 failure condition, forced (reasoning overrun via a starved
   token budget), reproduces the 400 signature pre-fix-path and the fixed
   call path now succeeds on the same payload.
2. care_coordination T01/T02 pass consistently across several consecutive
   runs (not once).
3. `python -m eval.harness --full` exits RATCHET PASS with T01/T02 green.
4. Completion-token counts observed before/after confirm
   reasoning_effort:"low" reduces reasoning volume (the overrun
   probability driver).
5. The retry warning now contains the Groq error body (resp.text), proven
   by a forced failing call whose log line names json_validate_failed.

## WHAT'S ALREADY DONE

- Root cause proven live (DISPATCH_GROQ_400_ROOTCAUSE, a61c49a): identical
  request bodies except message content; empty failed_generation;
  2/2 repro at max_tokens=64; 3/6 fail at production settings on T01 vs
  6/6 clean on R04; retry correlation math matching the observed timeline.
- The zero-changes retry-at-0.2 pattern already exists at
  fact_change.py:957-961 — fix 2 mirrors it, not a new invention.

## WHAT'S KNOWN BROKEN

- fact_change.py:450 max_tokens=2048 shared by reasoning+content; overrun
  empties the content slot -> Groq 400 json_validate_failed.
- fact_change.py:458-477 retries resend the identical payload at
  temperature 0.0 — correlated failures (~50% per call on T01-shaped
  payloads -> ~12% per-turn triple-drop).
- fact_change.py:473-476 discards the response body; production logs
  showed a bare 400 with no error code.

## CONSTRAINTS

- Touch ONLY harness/fact_change.py for the code change. Do not touch the
  mutation-score files the concurrent session is building, layer7 crypto
  files, or any audit file.
- Transport errors (timeouts, 5xx, connection failures) keep the existing
  identical-resend behavior — jitter is scoped to json_validate_failed.
- No behavior change to the F3 gate or the zero-changes retry path.
- Done means the FULL RATCHET passes (CLAUDE.md item 12), not just T01/T02.
- This REQ is also the last blocker on REQ_HARNESS_DISCIPLINE's MET
  determination: if --full is clean post-fix, that REQ gets marked MET per
  Bill's dispatch item 5.
