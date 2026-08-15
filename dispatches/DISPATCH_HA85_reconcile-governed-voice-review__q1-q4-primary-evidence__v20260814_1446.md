# DISPATCH_HA85 — reconcile the independent governed-voice review
Status: IN_PROGRESS — **Q1–Q4 answered; cross-check VERIFIED; F2/F3a now owned (TD-R-191/192); F5 and F7 still await Bill's paste**
Reconciled-Against: `hip-vo` @ `65c263e` (the reviewed package HEAD), `hip-cutover-demo` @ `6c56512`

**TYPE:** MEASUREMENT / ANALYSIS — **evidence only. No fixes, no ruling application.**
No code changed. All cross-tree work read-only; the only live probes were
**read-only GETs** against `:7872` and one non-mutating route test.

**REQ: NONE** — a reconciliation, not a build.

> **STATE OF THIS DOCUMENT.** The dispatch says the review's full text (verdict
> NOT CLOSED, findings F1–F7) is pasted **after** this dispatch. It is not yet in
> session. So this records **primary evidence for the four priority questions**,
> which are specified precisely enough to answer now, plus a preliminary
> classification for the findings those questions identify (F1, F2, F3, F4, F6).
> **F5 and F7, and the verbatim wording of all seven, are not classified here** —
> classifying a finding I have not read would be exactly the failure this
> dispatch exists to prevent.

---

## THE SENTENCE I WOULD PUT IN FRONT OF BILL ABOUT THE FREEZE

> **The demo at `:7872` is bound to `127.0.0.1` and is NOT reachable from the
> LAN — I probed `[REDACTED-LAN-ADDRESS]:7872` and got connection refused, with loopback
> returning 200 as a control. So none of these findings is remotely exploitable
> as the demo is currently running. What IS true on loopback is that
> `/api/routing` returns 200 with no authentication and exposes verbatim
> household queries — "What medication is Ray on now?", "Ray's on Jardiance 10mg
> now." — including a medication name. That is a real exposure to anything
> running on the Mini, and it is not a freeze-stopper only because of the bind
> address, which is a deployment accident rather than a control.**

## Q1 — FREEZE-CRITICAL, PER SURFACE

Server on `:7872` is `python -m server.demo_dashboard --host 127.0.0.1 --port 7872`
(pid 95051, cwd `[REDACTED-USER-PATH]/hip-cutover-demo`). Kernel socket: `127.0.0.1:7872`.

| surface | verdict | evidence |
|---|---|---|
| **F1 — realtime WebSocket `/ws/voice`** | **REGISTERED-AND-ROUTED, loopback only** | `server/demo_dashboard.py:3208` `@app.websocket("/ws/voice")`; `:3210` `await websocket.accept()` with **no caller authentication**; `:3204` `_REALTIME_MEMBER = "bill"` — a **hardcoded identity**, not derived from the caller; `:3205` `_REALTIME_WSS_URL = wss://api.openai.com/v1/realtime?model=…`. Live process provenance: started 13:55:55, file mtime 13:53:21, worktree clean at `6c56512`, so the running process loaded this route. |
| **F4 — unauthenticated `/api` reads** | **MIXED — partially REACHABLE, loopback only** | Live GETs: `/api/facts` → **401** `"dashboard session required"` (gated at `:180`); `/api/routing` → **200, 6737 bytes**; `/api/last_speaker` → **200**; `/api/metrics` → **200**. |
| **LAN reachability, both** | **NOT REACHABLE** | `GET http://[REDACTED-LAN-ADDRESS]:7872/api/routing` → **HTTP 000, refused**; `GET …:7872/` → refused. Loopback control → **200**. |

**What `/api/routing` actually exposes, read live:** 16 rows, each with a `query`
field — `'What medication is Ray on now?'`, `"Ray's on Jardiance 10mg now."`,
`'What medication is Maya on?'`, `'What medication is Sam taking?'` — plus member
names `ray/maya/sam` and the medication `jardiance`.

> **A correction to my own first reading, recorded because it matters
> methodologically.** A source grep found **zero** `require_operator` and zero
> `Depends(` in this tree's dashboard, which would have supported "no `/api` read
> is gated". **The live probe contradicted that**: `/api/facts` returns 401 via an
> in-handler session check at `:180`. Source-only would have over-claimed F4.
> The probe is why F4 is PARTIAL rather than confirmed outright.

**Not done deliberately:** I did **not** open `/ws/voice`. The handler calls
`accept()` and then assembles governed context and emits records — that is state
mutation, which this dispatch forbids. A plain `GET` cannot distinguish a
registered WebSocket route from an absent one (both return 404 in Starlette), so
registration is established from **source plus process provenance**, and I have
labelled it REGISTERED-AND-ROUTED rather than claiming a probed REACHABLE.

## Q2 — F3's core claim

**F3a — `frontier_client` sends `body`, not the permitted payload. CONFIRMED.**

`harness/frontier_client.py`:
* `:84` `body = {"model": …, "input": user_content, "tools": …}` — built **before** the permit;
* `:99` `_gw = permit(destination=Destination.FRONTIER, purpose=Purpose.ANSWER, payload=[{"role":"system","content":context_lines},{"role":"user","content":question}], …)`;
* `:104` `resp = requests.post(OPENAI_API_URL, json=body, headers=headers, …)`.

**`_gw` occurs exactly once in the file — the assignment. It is never read.** The
permit is computed and discarded; what goes on the wire is `body`, a different
object from the payload the gateway was asked to approve.

**The same repository contains the correct pattern**, which is what makes this a
defect rather than a design choice: `server/voice_orch.py:3594`
`_egress_messages = _permit.payload` and `:3601` `messages=_egress_messages`.

**F3b — `fact_change` POSTs to a configurable URL after self-declaring LOCAL.
PARTIALLY CONFIRMED, and the halves differ.**

* **Confirmed:** `:429` `LOCAL_CHAT_URL = os.environ.get("HIP_LOCAL_CHAT_URL", "http://localhost:11434/v1/chat/completions")` — env-overridable; and `:450` `permit(destination=Destination.LOCAL, …)` **hardcodes the destination**. The classification is a self-declaration decoupled from the transport target, so setting that env var sends the full decrypted household set off-device **under a LOCAL permit**. The module's own comment at `:425-428` states that this payload is the full decrypted owner+household set.
* **Not confirmed:** unlike `frontier_client`, this path **does** use the permit — `:461` `json={… "messages": gw.payload …}` — and honours `EgressRefused` by deferring with nothing disclosed.

**`eval/test_egress_gateway.py` — 39 tests: 37 passed, 2 FAILED.**

```
FAILED test_C1_no_NEW_direct_offdevice_host_outside_the_gateway
FAILED test_C8_zero_offdevice_hosts_outside_the_gateway
  server/demo_dashboard.py:2765 -> 'wss://api.openai.com/v1/realtime?model='
```

**The project's own egress suite already fails, naming F1's surface.** Its message:
*"Add the call to the gateway, or — if it is genuinely a new transport shape —
extend KNOWN_UNROUTED with a reason, never silently."*

**And the exception list is EMPTY:** `eval/test_egress_gateway.py:153`
`KNOWN_UNROUTED: tuple[str, ...] = ()`. So the realtime endpoint is **not an
accepted exception with a recorded reason** — it is an un-excepted violation, and
the suite is red on it right now. The debt is open, not absorbed.

## Q3 — F6. CONFIRMED, both halves.

1. **`test_egress_gateway.py` appears ZERO times in `scripts/run_governance_suite.py`'s
   `SUITES`.** The governance gate does not run the suite that is currently failing.
2. **The recorded 11/11 gate covers an EARLIER commit.** Latest gate run
   `logs/gate-runs/df205a94ab07.json`, written **Aug 14 09:07**, all 11 steps pass.
   The reviewed HEAD `65c263e` was committed **Aug 14 10:24** — **77 minutes later**.

So an 11/11 "governance suite PASS" is recorded against a tree that (a) predates
the reviewed package and (b) never exercised the egress gateway suite.

## Q4 — F2's fail-open. CONFIRMED.

`server/voice_orch.py:1328-1337`:

```python
try:
    escalated = await self._on_user_text(query, audio, transcription_ms)
except Exception as e:  # noqa: BLE001 — never wedge the audio loop
    logger.warning(f"[orch] turn handling failed, answering locally: {e}")
    escalated = False
if escalated:
    return  # placeholder already spoken; don't feed the LLM
await self.push_frame(
    TranscriptionFrame(query, "client", time_now_iso8601(), finalized=True), direction,
)
```

`_on_user_text` is the governed turn path. **Any exception it raises — including a
governance exception — is caught, logged as a warning, and `escalated` is forced
to `False`**, which skips the `return` whose own comment reads
`don't feed the LLM`, and the transcript is then pushed downstream to the model.

**The handler's own log line names the behaviour: "turn handling failed,
answering locally."** The rationale comment (`never wedge the audio loop`) shows
the trade was deliberate for liveness — liveness bought with the governance
guarantee.

**Not proven by injection.** I did not force a governance exception on the live
path; the dispatch permits it "if provable with a targeted injection", and the
control flow above is unambiguous from source without mutating a running demo
mid-freeze. Named as read-not-executed rather than presented as a live proof.

## PRELIMINARY RECONCILIATION — only the findings Q1–Q4 identify

| finding | classification | already owned by | freeze-relevant |
|---|---|---|---|
| **F1** `/ws/voice` off-gateway to `api.openai.com` | **CONFIRMED-KNOWN** | **TD-V-022** (SEC) — *"`/ws/voice` reaches `api.openai.com` from PYTHON, outside the egress gateway"*, found by Voice 40, **confirmed by Voice 41 executing Bill's ruling R-6**; **TD-V-023** (SEC) covers the refusal-delivery half | **YES** — but loopback-only |
| **F2** governance fail-open in `_flush_utterance` | **CONFIRMED-NEW** | **NOW OWNED: `TD-R-191`** (filed by this continuation, 2026-08-14, SEC, FILED-NOT-FIXED). Was unowned — the register's only `_on_user_text` mention sits under TD-V-007, which is the UnboundLocalError finding, not this | **YES** |
| **F3a** frontier permit discarded | **CONFIRMED-NEW** | **NOW OWNED: `TD-R-192`** (filed by this continuation, 2026-08-14, SEC, FILED-NOT-FIXED). Was unowned — `_gw` / "permit is discarded" appear nowhere in the register; `frontier_client` appears under TD-128 for an unrelated reason | **YES** |
| **F3b** LOCAL self-declaration vs configurable URL | **PARTIALLY CONFIRMED** | **unowned** — `HIP_LOCAL_CHAT_URL` and `Destination.LOCAL` appear nowhere in the register | YES (config-dependent) |
| **F4** unauthenticated `/api` reads | **PARTIALLY CONFIRMED** | unowned for `/api/routing` | **YES** — loopback-only |
| **F6** gate does not cover the egress suite / stale commit | **CONFIRMED** | adjacent to **TD-V-029** (`--full` never baselined on this lane), which does not own this | **NO** (process, not exposure) |
| **F5** caller-supplied transcript given SPOKEN provenance | **CONFIRMED — PARTIAL on the required change** | **unowned** | **YES** |
| **F7** Layer 1 asserts the parked row is active alongside the head | **CONFIRMED-KNOWN** | **TD-V-029** (GATE) — names `layer1`, "parked row active", STALE, TD-V-018/HA-73, with `L1:P8` in its regression list | **NO** — stale test expectation, not an exposure |

> **F5 AND F7 ARE NOW CLASSIFIED.** The verbatim text arrived in a later message and both were read
> before verdict. The preceding note — which recorded that this row was deliberately left unfilled
> while the text was unavailable — is superseded and kept in git history rather than restated here.

### F5 — caller-supplied transcript given SPOKEN provenance. CONFIRMED, PARTIAL on the fix.

**What the review says, and what the code says.** `server/voice_https_orch.py:382-388` states the
asymmetry in its own comment: a caller transcript *"is still ACCEPTED (transcribe absent/false),
because the demo player and the existing tests use it… it is recorded as `transcript_origin="caller"`
and carries NO confidence… confirmations are the one place that distinction changes an outcome."*

**The construction is real.** `:450` calls `spoken_request(query, principal=_principal,
verification=_verification, transcript_confidence=(stt_evidence.get("confidence") if transcribe
else None), source_detail={"transcript_origin": "server_stt" if transcribe else "caller", …})`.
So when `transcribe` is false, a **SPOKEN** `TurnRequest` is built from **caller-supplied text**,
bound to a **voiceprint-derived principal**, with confidence `None`.

`harness/turn_request.py:210` documents `spoken_request` as *"A turn that arrived as audio and was
transcribed BY THE SERVER"* — which is not what this path does.

**Why PARTIAL, and it cuts both ways:**

* The review's required change asks that caller text *"be given a distinct provenance type"*. **That
  half already exists** — `transcript_origin="caller"` — so this part of the finding is
  **CHALLENGED**: it asks for something already built.
* The other half — *"prohibit it from producing member-attributed memory writes, consent,
  confirmation or disclosure records"* — is **NOT built, and the distinction is the whole point.**
  `transcript_origin` occurs at `:384` (comment), `:458`, `:483`, `:513` — **every one a RECORDING
  site. Nothing in product code ever reads it as a gate.** The marker is written down and never
  enforced.
* **Confirmations are already protected, but by a different mechanism than the marker** — caller
  transcripts carry no confidence, so they cannot satisfy R-3's spoken-confirmation floor. That is
  the "one place" the comment names. **Memory writes and disclosure records have no equivalent
  block.**

**Freeze-relevant: YES — and HA-85's close-out measured exactly how, read-only.**

### F5 LIVE DURING DEMO — YES, and not because the demo starts it

| question | answer | evidence |
|---|---|---|
| `:7860` | **`TCP *:7860 (LISTEN)` — ALL INTERFACES** | pid 72415, `python -m server.voice_https_orch --host 0.0.0.0 --port 7860`, cwd `[REDACTED-USER-PATH]/hip-vo` |
| `:7862` | **nothing listening** | `lsof` empty |
| does the cutover launcher start it? | **NO** | `voice_https_orch` appears **0 times** in `scripts/cutover_demo_start.sh` |
| then what does? | **launchd**, permanently | parent pid 1; `~/Library/LaunchAgents/com.hip.voice.orch.plist` → `voice_https_orch --host 0.0.0.0 --port 7860`. `dev.sh:114` uses the same flags but is not this process's parent |
| is the endpoint in the running code? | **YES** | `server/voice_https_orch.py:308` `@runner.app.post("/api/voice-query")`; process started 09:27:36, file mtime 09:27:13, worktree clean at the reviewed HEAD |

**VERDICT: F5 IS LIVE DURING THE DEMO** — and the wording matters: it is live
*whenever the machine is up*, because a launchd agent keeps it running on all
interfaces regardless of whether anyone runs a demo. That is broader than "the
demo starts it", not narrower.

**BUT THE EXPOSURE IS BOUNDED, and this is the half that decides freeze-vs-post-freeze.**
`:353` `require_operator(request)  # R-5: runs a full governed turn — operator only`.
**`/api/voice-query` is operator-gated.** So F5 is **not** an unauthenticated path:
it is a **record-integrity** defect — the durable record asserts that a verified
speaker said words they may not have said — reachable by someone who already
holds the operator credential.

**Read against F4, the contrast is the point:** F4 is an *unauthenticated* read on
a loopback-bound demo; F5 is an *authenticated* write-with-false-provenance on an
all-interfaces service. Different exposure, different urgency, and neither is
described correctly by "caller-supplied".

### F7 — Layer 1 encodes superseded park behaviour. CONFIRMED-KNOWN.

`eval/harnesslib/layer1.py:885` asserts `s.check(bool(parked_row), "A: parked row active alongside
head", …)` where `parked_row = [r for r in after if r["fid"] == res.new_fact_id]` and `after =
_heads(...)` — i.e. the **active** rows. It requires the parked row to be active.

HA-73's implementation ruled the opposite (`memory_engine/store.py`, `_tx_unresolved`): **"WHEN A
HEAD ALREADY EXISTS, THE PARKED ROW IS NOT OPENED ACTIVE"**, and the governance test
`eval/test_supersede_no_contradictory_state.py:191-193` asserts `len(active) == 1` with the head
retained. **The reviewer's §5 answer — siding with the governance test and calling `layer1.py:885`
stale — is correct**, and matches the ruling that produced the behaviour.

**Already owned: `TD-V-029`**, which records that `--full` *"has NEVER been baselined on this lane,
and three of its invariant probes are STALE against TD-V-018/HA-73"*, listing `L1:P8` among the
regressions. F7 is a more precise statement of a defect the register already carries.

**Freeze-relevant: NO.** A stale test expectation is a gate-accuracy problem, not an exposure.

## CROSS-CHECK — the scrubbed-package claims, VERIFIED AGAINST THE LIVE TREE

**Source of the claim:** a reading of the **scrubbed demo-cutover package `7904c36`**, offered by
Bill explicitly *"as a claim to verify, not as truth"*. **Verified here against the LIVE tree,
`~/hip-cutover-demo` @ `3b3d7b2`** — read-only, nothing executed, nothing changed.

### VERDICT: every claim's SUBSTANCE holds. Every LINE NUMBER is wrong by a constant.

| claim | package line | **LIVE line** | substance |
|---|---|---|---|
| `@app.websocket("/ws/voice")` registered unconditionally at module scope | 3164 | **3208** | **CONFIRMED** |
| `_REALTIME_MEMBER = "bill"` | 3160 | **3204** | **CONFIRMED** |
| direct OpenAI `wss://` URL | 3161 | **3205** | **CONFIRMED** |
| `--host` defaults to `0.0.0.0` | 3492 | **3536** | **CONFIRMED** |

**THE DRIFT IS EXACTLY +44 ON ALL FOUR.** 3208−3164 = 3204−3160 = 3205−3161 = 3536−3492 = **44**.

> ### ⚠ THE +44 IS A PROPERTY OF THE SCRUBBED REVIEW PACKAGE — **NOT OF THIS REPOSITORY**
>
> **Stated plainly so no later reader mistakes a package line number for a repo line number.**
>
> The offset exists because the **scrubbed package `7904c36` is 44 lines shorter** than the live
> tree above this point — the address-scrubbing rebuild (FM 5) removed those lines from the
> *copy that was sent out for review*. **Nothing was removed from the repository.** No file in
> `~/hip-cutover-demo` shifted; the live tree has always had the numbers in the right-hand column.
>
> **A constant offset across four unrelated call sites is the signature of a REDACTION, not of a
> code difference.** Had the four drifted by different amounts, that would have meant the two trees
> genuinely diverged and each finding needed separate reconciliation.
>
> **THIS DOCUMENT CITES LIVE-TREE LINE NUMBERS ONLY.** Every `demo_dashboard.py:NNNN` in HA-85 —
> including Q1's `:3208` — is a line in `~/hip-cutover-demo`, read there. **A package line number
> appears nowhere in this document except in the left-hand "package line" column of the table
> above, where it is labelled as such.** If a future reader finds a bare `:3164` attributed to this
> repository, it came from the review package and is wrong by 44.

**This matters beyond bookkeeping.** HA-85's own Q1 table already cites `demo_dashboard.py:3208`
from the live tree. Had the package numbers been carried into the record unchecked, the dispatch
would have contained **two different line numbers for the same finding**, and a later reader would
have had no way to tell which tree either referred to.

### The substance, verified line by line

- **`:3208` `@app.websocket("/ws/voice")` — column 1, module scope, unconditional.** The nearest
  preceding column-1 statement is `:3205` `_REALTIME_WSS_URL = …`; there is **no `if`, no feature
  flag, and no enclosing block.** Registration happens on import.
- **No auth.** `await websocket.accept()` is the **first statement** of the handler — the socket is
  accepted before anything is checked. A grep for `require_operator|operator_token|_check_session|auth`
  across the handler body (`:3208-3300`) returns **0 matches**. The only gate present is
  `if not api_key:` — an **`OPENAI_API_KEY` presence check, which is configuration, not
  authentication.**
- **`:3204` `_REALTIME_MEMBER = "bill"`**, consumed at `:3218` `member = _REALTIME_MEMBER`. The
  member is hardcoded, not derived from a principal.
- **`:3536` `parser.add_argument("--host", default="0.0.0.0")`** — the module's own default is
  all-interfaces.

### Launcher bindings — one half of the claim is CHALLENGED

| script | live line | binds | claim |
|---|---|---|---|
| `scripts/cutover_demo_start.sh` | **250** (claim said 231) | `--host 127.0.0.1` | **CONFIRMED** (line number wrong) |
| `scripts/restart.sh` | 43 | `--host 0.0.0.0` (dash, :7870) | **CONFIRMED** |
| `scripts/restart-dashboard.sh` | 18 | `--host 0.0.0.0` (:7871) | **CONFIRMED** |
| `scripts/start_dashboard.sh` | 61, 64 | `--host "$BIND_HOST"` | **⚠ CHALLENGED** |

### ⚠ `start_dashboard.sh` — ITS OWN FINDING: NOT `0.0.0.0`, BUT **NOT LOOPBACK EITHER**

**`start_dashboard.sh` does NOT bind `0.0.0.0`.** It resolves `BIND_HOST` at `:34-42`: **Tailscale
IP first** (`tailscale ip -4`), then an `ifconfig` scan of the Tailscale CGNAT range
`100.64.0.0/10`, then **`127.0.0.1`** as the final fallback — and at `:44` it prints *"Binding to
Tailscale interface … (tailnet-only access)."* **The string `0.0.0.0` never appears in the file.**
So the claim that all three launchers bind `0.0.0.0` is right for two and **wrong for this one.**

**BUT "not 0.0.0.0" IS NOT "loopback", AND THAT IS THE FINDING.** When the Tailscale IP resolves —
the script's FIRST and PREFERRED branch, and the one that runs on any machine with Tailscale up —
**the dashboard is bound to a tailnet-routable address and is reachable from every other device on
the tailnet.**

**The script says so itself**, which is why this needs no probe to establish:

- `:33` describes the loopback branch as *"safe but **unreachable from other tailnet devices**"* —
  the contrast is the script's own statement that the **Tailscale branch IS reachable from them**;
- `:4` states the intent: *"Binds to the Tailscale interface IP so only Tailscale-authenticated
  peers can"* reach it;
- `:74` advertises the result for use: `echo "OK: http://$BIND_HOST:$PORT"`.

**There is no token, password or operator gate anywhere in this launcher** — a case-insensitive
search for `token|auth|operator|password` matches **only the line-4 comment**. Containment rests
**entirely** on tailnet membership.

**WHY THIS CHANGES THE CONTAINMENT STORY IF THIS SCRIPT EVER STARTS THE DEMO.** F1's disposition is
*registered-and-routed, **loopback only***. That holds for `cutover_demo_start.sh`, which pins
`127.0.0.1`. It does **not** hold under `start_dashboard.sh`: the unauthenticated `/ws/voice` at
`:3208` — no auth, `websocket.accept()` first, member hardcoded to `"bill"`, direct OpenAI `wss://`
— would be reachable from **any tailnet peer**, not just this host. **Which launcher starts the
demo is therefore a freeze-relevant fact, not an operational detail.**

**Not probed, per the dispatch — read from the script.** No connection was attempted from another
device, and the live posture at check time was `127.0.0.1:7872` (`cutover_demo_start.sh`'s pin).
**What is established is reachability BY CONFIGURATION, not an observed remote connection.**

**Live posture at the time of this check:** the only dashboard listener is
**`127.0.0.1:7872`** (PID 95051) — loopback. **The `0.0.0.0` default is reachable but not currently
taken**, which is exactly the shape Q1 recorded for F1: *registered-and-routed, loopback only.*

### What this does NOT change

**No F-classification moves.** F1 was already **CONFIRMED-KNOWN** (TD-V-022) and freeze-relevant
**YES — loopback-only**; this cross-check re-verifies that on the live tree and adds the auth
detail, but the verdict and the owner are unchanged. **No remediation-order row changes.**

---

## PROPOSED REMEDIATION ORDER — proposals only, Bill rules

1. **F3a** — one line, highest ratio: send `_gw.payload`, matching
   `voice_orch:3594`'s existing correct pattern. Removes an unpermitted body from
   a frontier call.
2. **F2** — narrow the `except Exception` so governance exceptions do **not**
   reach the "answering locally" path. Liveness for transport faults is
   defensible; liveness for a refused turn is not.
3. **F4** — gate `/api/routing` the way `/api/facts` already is at `:180`; the
   mechanism exists in the same file.
4. **F6** — add `test_egress_gateway.py` to the governance `SUITES` and re-run the
   gate at the actual package HEAD. Cheap, and it is what would have surfaced
   F1/F3 without an external review.
5. **F5** — **inserted here by the F5/F7 pass, and it is the one that moves.**
   The marker `transcript_origin="caller"` already exists and is already recorded
   at three sites; what is missing is that **nothing reads it**. Making it
   load-bearing — refuse member-attributed memory writes, consent and disclosure
   records when it is `"caller"` — is a guard at sites that already carry the
   field, not new plumbing. Ranked below F4 only because F4 is a live open read on
   a running demo, whereas F5 needs a caller who can already reach the endpoint.
6. **F3b** — derive the egress destination from the URL actually being posted to,
   rather than hardcoding `Destination.LOCAL`.
7. **F1** — already owned by TD-V-022/023 and awaiting Bill's ruling there; not
   re-opened here.
8. **F7** — **last, and deliberately.** It is a stale test expectation, not an
   exposure: `layer1.py:885` still asserts the pre-HA-73 park behaviour. It is
   already owned by **TD-V-029**, and correcting it is part of baselining `--full`
   on this lane rather than a freeze action. Fixing it changes no product
   behaviour and closes no exposure — but leaving it means the gate keeps
   asserting something the implementation deliberately stopped doing.

## VERIFIED

**Watched run:** the `:7872` process command line and kernel socket; four live
read-only GETs plus the `/api/routing` payload; LAN-vs-loopback probes from
`[REDACTED-LAN-ADDRESS]`; `eval/test_egress_gateway.py` (37/2 of 39) and the two failure
messages; the gate-run JSON and its timestamp against `git log` for `65c263e`;
`grep -c` for `test_egress_gateway` in the governance runner.

**Read, not executed:** the `_flush_utterance` control flow; `frontier_client`'s
permit/POST lines; `fact_change`'s destination constant; the `/ws/voice` handler.
No governance exception was injected and no WebSocket session was opened.

## OPEN — NEEDS BILL

1. ~~The review's full text~~ **— RECEIVED. All seven findings are now
   classified against primary evidence; nothing in F1–F7 remains unread.**
2. **The freeze call**, on the sentence at the top of this document. **F5 sharpens
   it**: caller-supplied text can be recorded with spoken provenance for every
   outcome except confirmation, and that is reachable by anyone who can reach the
   endpoint — which, per FM 8, is loopback only *because one launcher flag says
   so*, over a module default of `0.0.0.0`.
3. ~~F3a and F2 are unowned~~ **— NOW OWNED: `TD-R-191` (F2) and `TD-R-192` (F3a),
   filed by CC-1 in this same continuation.**
4. ~~F5 is unowned~~ **— FILED as `TD-V-030` in `~/hip-vo`'s register, per Bill's
   close-out ruling. F5 IS LIVE DURING THE DEMO** (launchd keeps
   `voice_https_orch` on `0.0.0.0:7860` independent of any demo launcher) **but is
   OPERATOR-GATED** (`:353`), so it is a record-integrity defect rather than an
   open path — which is what makes it arguably a post-freeze item.
5. ~~Which register owns a hip-vo finding~~ **— RULED by Bill, 2026-08-14: THE
   REGISTER FOLLOWS THE CODE, NOT THE DISPATCH LANE.** The test is *"where will the
   person who has to fix this go looking"*. Applied: `TD-R-191`/`TD-R-192` **stay
   exactly where they are** — published ids are not renumbered, deleted or
   rewritten — and now carry the rule plus a pointer forward; hip-vo's register
   gains pointer rows `TD-V-P191`/`TD-V-P192` naming them and the files, so a
   hip-vo session sees its own debt. **The earlier revert was the rule working,
   not a lapse** (Bill's words).

6. **A duplicate filing was avoided and is recorded rather than hidden.** This
   session was instructed to file TDs for F2 and F3a and had written
   `TD-V-030`/`TD-V-031` into `~/hip-vo`'s register before pulling and finding
   CC-1's `TD-R-191`/`TD-R-192` already committed for the same two findings. The
   `TD-V` pair was reverted **uncommitted and never pushed**. Two ids for one
   finding across two registers is the collision class this project has already
   paid for twice (TD-146, D-136), and two sessions acting on one instruction is
   how it happens. **Which register should own a finding in `~/hip-vo` code
   raised by a `roadmap`-lane dispatch is a real ambiguity in item 10's
   lane-prefix rule, and it is Bill's to settle.**
