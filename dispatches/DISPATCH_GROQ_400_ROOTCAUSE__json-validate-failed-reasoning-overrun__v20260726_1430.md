# DISPATCH_GROQ_400_ROOTCAUSE: care_coordination T01/T02 — json_validate_failed, reasoning-token overrun
Status: BUILT (diagnosis complete, root cause proven live; NO code changed per instruction)
Reconciled-Against: cfd4290 (clean tree; repro scripts in session scratchpad only, never in the repo)
TYPE: MEASUREMENT / DIAGNOSIS
REQ: NONE (analysis dispatch; the fix, when authorized, belongs under its own REQ — file:line named below)
Predecessor: DISPATCH_MET_VERIFICATION__harness-discipline-blocked-by-groq-400__v20260726_1253.md (this dispatch executes that doc's handoff item 1 and corrects one of its inferences)

## Method (read-only)

Rebuilt the EXACT fact_change Groq request outside the harness — same
builder logic (`read_user_facts(owner, limit=None)` + `_fact_line` +
`_USER_TEMPLATE` + `_SYSTEM_PROMPT` + `_CHANGES_SCHEMA`, model
`openai/gpt-oss-20b`, temperature 0.0, max_tokens 2048,
response_format json_schema — harness/fact_change.py:436-452) — for the
failing turn (T01: owner=bill, "My mother Elena was switched from
metformin to Jardiance, ten milligrams, starting this week.",
demo_scripts/test/care_coordination.json) and the passing comparator
(R04: owner=maya, "Ray switched from metformin to Jardiance 10mg last
week."). Sent both repeatedly, captured HTTP status, full error body,
and token usage. No repo code touched; no graph writes (reads only).

## The diff (item 3)

The two request bodies are IDENTICAL in model, temperature, max_tokens,
response_format/schema, and headers. They differ ONLY in message
content: the owner's facts_block (bill's 5 facts vs maya's 8) and the
utterance. Nothing about the Elena payload is structurally invalid — no
field, encoding, length, or character problem. Groq accepts the request;
what fails is on the RESPONSE side.

## Proven root cause (items 1-4)

`400 {"error": {"code": "json_validate_failed", "message": "Failed to
validate JSON. Please adjust your prompt...", "failed_generation": ""}}`

- `openai/gpt-oss-20b` is a REASONING model; `max_tokens: 2048`
  (fact_change.py:450) caps reasoning + content TOGETHER. When the
  model's hidden reasoning overruns the cap, the content slot comes out
  EMPTY, Groq's server-side json_schema validation then fails on the
  empty string, and the API returns 400 json_validate_failed with
  failed_generation="".
- Mechanism proven: with max_tokens=64 (forcing overrun) the exact
  production signature reproduces 2/2. With the production 2048, the
  T01 payload fails 3/6 (same signature); its successful calls show
  completion_tokens 661 vs 1377 on IDENTICAL input at temperature 0.0 —
  reasoning length is high-variance and sometimes exceeds 2048.
- Payload-correlated, not payload-invalid: R04's simpler utterance ran
  6/6 clean (completion_tokens 364-1297, always under the cap). T01's
  shape (third-party subject "my mother Elena", spelled-out dosage "ten
  milligrams", relative date "starting this week") drives longer, more
  variable reasoning. ~50% per-call failure on T01 => (~0.5)^3 ~ 12%
  chance all three retries fail on a given turn — matching today's
  timeline (passed 09:00, failed in consecutive runs ~12:45-12:51,
  reproducible-looking in adjacent runs, 200s again by 13:05). The
  predecessor dispatch's "NOT a flake" inference is hereby corrected:
  it is a payload-biased coin, not a deterministic failure — and not a
  Groq-side change.
- The retry loop compounds it (fact_change.py:458-477): all three
  attempts resend the IDENTICAL payload at temperature 0.0, so failures
  are correlated instead of independent — the code's own zero-changes
  path already knows this trick and retries at temperature=0.2
  (fact_change.py:957-961); the 400 path never got the same treatment.
- Observability gap that made this expensive: the warning at
  fact_change.py:473-476 logs only `repr(exc)` — the response BODY
  (which names json_validate_failed outright) is discarded, so
  production logs showed a bare "400 Bad Request" and diagnosis
  required out-of-band reproduction.

## Verdict (item 4)

PAYLOAD-BIASED MODEL-SIDE failure, fixable in how fact_change builds
and retries the request — NOT a Groq outage, NOT a request-format bug,
NOT related to today's crypto/audit work. Fix candidates for Bill's
authorization (NOT implemented, per instruction; needs its own REQ):

1. harness/fact_change.py:450 — raise `max_tokens` (e.g. 8192) and/or
   add `"reasoning_effort": "low"` (supported for gpt-oss models on
   Groq's OpenAI-compatible API; this extraction task needs minimal
   reasoning — lower cost AND lower overrun probability).
2. harness/fact_change.py:458-477 — on `json_validate_failed`
   specifically, retry with temperature jitter (0.2, mirroring
   :957-961) so retries are decorrelated; keep identical-resend for
   genuine transport errors.
3. harness/fact_change.py:473-476 — include `resp.text` (truncated) in
   the retry warning so the Groq error code is visible in production
   logs the next time.

Impact restated: every failure of this call is a silently dropped fact
write surfaced only by the F3 gate's honest refusal — the D-01/fail-open
family's territory. The fix is small; the class (external structured-
output call with correlated retries and a shared reasoning/content
token budget) is worth a harness check of its own once fixed —
REQ_HARNESS_DISCIPLINE's standard applies to it like any other check.

## MET impact

REQ_HARNESS_DISCIPLINE remains blocked only by this: everything the REQ
itself governs is green (predecessor dispatch). Once the fix lands and
`--full` runs clean, the MET determination is ready with no further
condition.
