# HIP Trust Boundary Roadmap

Version: v20260812
Status: **PLAN**
Branch: roadmap
Banked by: HA-50, 2026-08-12, on Bill's instruction
Reconciled-Against: roadmap `f2f17ca` (HA-49A, 2026-08-12)
Amends: `HIP_FinishPlan__three-finish-lines-14-steps__v20260811.md` — that document gains a
pointer here; this one names it in its own first line below.

> **Body banked VERBATIM from Bill's dispatch text.** The six lines above are the governance
> header the Naming Law requires on every doc; everything from the rule below is Bill's wording,
> unedited. **Nothing in this roadmap is ruled MET, and it builds nothing.**

---

Amends: HIP_FinishPlan (three-finish-lines-14-steps, v20260811).
Phases 0-1 are DEMO-phase work (privacy-unsafe findings inside the
VD-40 freeze criteria). Phases 2-4 are CORE-PRODUCT-phase and absorb
work already sequenced on the roadmap branch (R2 permit, ceiling
audience axis). This roadmap does not fork the plan; it inserts.

Source findings (all verified in hip-vo source 2026-08-12):
1. GET /api/decrypt and POST /api/reset on voice_https_orch have NO
   auth; decrypt returns member+household plaintext; server binds
   0.0.0.0. /api/text-query trusts caller-supplied member on both
   servers. _build_requester falls back adult/full on registry miss.
2. Typed-query path sends mid/core messages to Groq WITHOUT the
   strip the live path applies; config says groq_is_onnet: false.
3. fact_change re-reads + decrypts the full owner+household set and
   sends it to Groq on declarative turns ("encode is not disclosure"
   — wrong from an egress standpoint). Reason was TD-121 (partial
   block dropped writes 7/8); real fix needs a design ruling.
4. build_payload receives facts, not principal/authority. Consent
   is evaluated; authority is not.

PHASE 0 — Stop the exposure (today).
  Funnel off 7860. Operator token on /api/decrypt, /api/reset,
  /api/text-query (both servers). _build_requester registry-miss ->
  guest, not adult/full. Master key loads fail-closed: ciphertext
  present + key file absent -> refuse to start.
  DONE: second-machine curl fails on all four endpoints; server
  refuses boot with key removed.

PHASE 1 — Egress correctness (days).
  Port the on-net/strip branch to the typed path. Bill rules the
  fact-change egress question (local detection / narrowed candidate
  set / declare Groq on-net + change config+claims). Build ONE egress
  gateway; AST test fails build on any direct external-model call
  outside it (same pattern as the spend machine's import guard).
  DONE: AST check proves zero direct external calls; a twin adding
  one goes red.

PHASE 2 — One authenticated principal (~week).
  System establishes principal, never the request body. Voice: speaker
  verification. Text: session bound to a member. Demo scripts run as a
  declared, recorded principal. Every sensitive endpoint + the
  confirmation and disclosure gates consume it.
  DONE: no endpoint reads identity from the body; impersonation test
  fails closed.

PHASE 3 — Authority separated from consent.
  Disclosure decisions take principal+subject+facts+destination+
  purpose; authority checked before consent. PORT R2 permit + ceiling
  audience axis from roadmap — do not rebuild on hip-dev.
  DONE: one site evaluates the full tuple; a twin with consent-but-no-
  authority refuses.

PHASE 4 — Prove it + true up claims.
  Reconcile 39/39 vs 9/11 suites. Standing adversarial battery
  attempts every bypass in this review, asserts fail-closed. Re-check
  every ledger claim citing the strip/off-device guarantee; anything
  above its evidence reverts until Phase 1 lands.
  DONE: bypass battery standing; public page states nothing above the
  private ledger.

This roadmap does not require a new REQ per phase; each phase names
its governing REQ before code (Phase 0 = REQ_SECURE_DEV_ENDPOINTS,
already filed; later phases file their own).
