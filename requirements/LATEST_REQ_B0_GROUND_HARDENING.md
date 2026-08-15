# REQ_B0_GROUND_HARDENING
Status: PLAN
Reconciled-Against: 2026-08-14. Build worktree `~/hip-nc2` @ `nc-b0`, cut from `origin/main`
at `5c71e42`. Filed by NC 8 **before the first code edit**.

Findings lifted from
`docs/design/HIP_EXECUTION_MAP__natural-conversation-demo-v1-preflight-excavation__v20260814_1720.md`
(NC 7), §9 and §§1.3, 3.2, 8.

---

## THE REQUIREMENT

Bill's words, 2026-08-14, verbatim:

> **OBJECTIVE: close the B0 gaps NC 7's execution map pinned, so a voice path can later become
> governance-bearing.**
>
> **1. intent_classifier.py:190-212 — the three indistinguishable failure modes (no embedding /
> below threshold / uninit) stop returning "knowledge". Each returns a DISTINCT typed failure;
> callers fail closed on all three. Twins per mode.**
>
> **2. server/app.py POST /chat — the ungoverned ingress: remove it or gate it so it cannot
> execute (404/refused), prove it.**
>
> **3. escalation_backends.py:400 SerpAPI — route through the egress gateway with a real
> permit; temporal.py:98's config endpoint gets destination classification. Twins both.**
>
> **4. CONSUMER-PATH TESTS: at least one executing test per kernel entry (process_text_query /
> assemble_governed_context / _governed_turn) that CALLS the function through the real path —
> anti-vacuity: valid principal -> real result, plus the refusal case. Source-text assertions
> don't count.**

**Expanded.** These are ground conditions, not features. Each is a measured defect from NC 7,
each is on the path a governance-bearing voice turn must later traverse, and each currently
fails *open* — which is the property that makes the later capability unprovable rather than
merely unbuilt.

---

## THE ACCEPTANCE TEST

**Eleven observations. Every gate is exercised in the red as well as the green.**

### 1. Typed intent failure

- **1a** `embed_text` returns `None` → a result whose outcome is **distinguishably**
  "embedding unavailable", **not** `knowledge`.
- **1b** every route scores below `CONFIDENCE_THRESHOLD` → outcome **"below threshold"**,
  carrying the best score.
- **1c** the classifier was never initialised (no route vectors) → outcome
  **"uninitialised"** — today this is indistinguishable from 1b because `best_route` is
  seeded to `"knowledge"`.
- **1d** the three outcomes are **mutually distinguishable by value**, not by confidence alone.
- **1e** **the caller fails closed on all three**: `harness/router.py` must not take an
  intent-driven branch and must not permit an off-net escalation on any of them.
- **1f** a healthy classification still returns its intent (no regression on the green path).

### 2. The ungoverned ingress

- **2a** `POST /chat` **cannot execute**: a request reaching it is refused or 404s.
- **2b** proven by **calling it**, not by reading the source.
- **2c** `server/app.py` no longer reaches a model on that path.

### 3. SerpAPI egress

- **3a** the SerpAPI call at `escalation_backends.py:400` passes `permit()` with a truthful
  `Destination`; **a refusal stops the call** rather than being logged past.
- **3b** the config-supplied endpoint (`SearchBackend.search`, `:98`) is **classified** — its
  destination is derived and asserted, not assumed.
- **3c** twins for both: permitted → call proceeds; refused → `EgressRefused`, no network call.

### 4. Consumer-path tests

- **4a** one **executing** test per kernel entry — `process_text_query`,
  `assemble_governed_context`, `_governed_turn` — that **calls** it.
- **4b** anti-vacuity: a valid principal yields a **real result**, asserted on content, not on
  "did not raise".
- **4c** the refusal case for each is also exercised.
- **Source-text assertions do not count toward 4a–4c.** They may exist alongside.

---

## WHAT'S ALREADY DONE — DO NOT REBUILD

| piece | evidence |
|---|---|
| `harness/egress_gateway.py` — `permit()` `:175`, `permit_stream()` `:235`, `Destination` `:51`, `_assert_destination_is_truthful()` `:116` | six off-device calls already route through it (NC 7 §3.1) |
| `_build_requester` fails closed — registry miss is a **guest** | `voice_orch.py:680-706`, HA-50 Phase 0. **Settled; not reopened.** |
| noise detection | `intent_classifier.py:154` `_is_noise` — a real, distinct outcome already |
| the temporal short-circuit | `voice_orch.py:1596` — removes local-now queries from escalation. **It does not gate the path** and is not a substitute for item 3. |

---

## WHAT'S KNOWN BROKEN

1. **`intent_classifier.classify()` `:190-212`** — three failure modes converge on
   `("knowledge", …)`: `:197` (no embedding), `:211` (below threshold), and `:201`'s seeded
   `best_route = "knowledge"` (uninitialised). The caller cannot tell them apart, and
   `knowledge` is a permissive route.
2. **`server/app.py` `POST /chat`** — imports `json time pathlib datetime requests yaml
   FastAPI BaseModel` and nothing else. No governance of any kind; `user_id` is caller-supplied;
   the model is called at `:36`.
3. **`harness/escalation_backends.py:400`** — `requests.get("https://serpapi.com/search")` with
   no `permit()`; the module never imports `egress_gateway`. Reachable: `voice_orch.py:104`
   imports the backends, `voice_orch.py:1591` and `temporal.py:98` both describe escalation
   reaching it *unconditionally*, `config.yaml:121-123` configures it. `:98` posts to a
   config-supplied endpoint whose destination is unknowable from the code.
4. **No executing consumer-path test.** Five files name a kernel entry; **zero call one**. 22 of
   37 test files assert over source text.

---

## CONSTRAINTS — WHAT MUST NOT REGRESS

- **`~/hip-vo` is not touched.** All work is in `~/hip-nc2` @ `nc-b0`.
- **No graph writes.** This dispatch stands up no Neo4j; `~/hip-nc2` declares 7693, which no
  lane owns and where nothing listens.
- **Out of scope, explicitly:** the kernel extraction itself, conversation state, voice changes,
  `/api/text-query` dedup, the frozen tree, anything in the demo lane.
- **The green path must still work.** A healthy classification, a permitted egress and a valid
  principal must behave as they do today; failing closed is for the failure modes only.
- **Exit codes are not answers** (Requirements Discipline item 13) — verification steps run
  unchained.
- **STOP FOR BILL** only on: security-policy questions, architecture outside this list, or
  destructive ambiguity.

---

## OPEN — NOT DECIDED BY THIS REQ

**What "fail closed" means for item 1e at `router.py:710` is a routing decision with a
behavioural cost, and the implementing dispatch must state which it took.** Dropping the turn
(as the noise path does at `:705`) is maximally closed and would silence every query whenever
the embedder is down. Pinning to on-box handling with no intent branch and no escalation is
closed on the privacy axis while keeping the assistant answering. **The implementation must not
choose silently.**
