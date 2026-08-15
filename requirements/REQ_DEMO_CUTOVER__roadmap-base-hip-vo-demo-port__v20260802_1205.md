# REQ_DEMO_CUTOVER
Status: SUPERSEDED
Reconciled-Against: 2f69f2f (roadmap HEAD at filing)

> **SUPERSEDED 2026-08-04 (Index Demo 23) by
> `REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260804_1939.md`.**
> **One criterion changed: C9's gate.** This version gates C9 on leak count at or under 6
> (stated in the RULINGS section below, Bill 2026-08-02). Measurement against the reconciled
> 400-row dataset (Index Demo 22, `e2a2c0b`) established that the gate is insensitive to the
> property it exists to protect: the run fails at **10 leaks against 6**, and **would fail
> identically whether its 3 structural refusals existed or not** — the three (G087, G107,
> G187) intersect the leak set nowhere. A leak-count gate scores a voluntary refusal the same
> as a compelled one, so a build could clear it with **zero** structural refusals. The
> successor gates on STRUCTURAL-REFUSAL RATE, evidenced by telemetry
> (`guard_triggered` / `guard.kind` / `inference_ms`), never by prose shape, with the
> threshold left explicitly OPEN for Bill.
> **Nothing below is edited** — this document is retained intact as the record of what was
> gated before, including Bill's 2026-08-02 rulings in their original form. Read the
> successor for the operative criterion. **C9 was not ruled by that amendment, and is not
> ruled here.**

## THE REQUIREMENT

Bill's words, verbatim (2026-08-02):

> "I don't want to fix the demo tree. I want to roll the rest of the code into a new demo
> (not the frozen one), and I want to test against that."

And earlier the same day, on why:

> "does it actually work? Or are we just staging the entire thing and not really producing
> something that can engage in a two way conversation with an actual human?"

## THE DECISION OF RECORD

**Roadmap is the base. hip-vo's demo surface ports onto it.** Not the reverse, not a third
tree.

Roadmap is ahead on every governance mechanism examined and hip-vo is ahead on none. Roadmap
holds the harness — `eval.harness --full`, layers L1 through L6 — which has no equivalent on
hip-vo. hip-vo's advantage is entirely the demo surface: five newer script versions, the
Epistemic State panel, and the dashboard self-check system.

The frozen demo is untouched by this and remains the fallback. `~/hip-dev`, branch
`demo-presenter-package`. Note that `demo-frozen-known-good` is a **label for commit
`8cef82d`, not a branch** — no branch of that name exists, and `8cef82d` is now four commits
behind that branch's HEAD.

## THE ACCEPTANCE TEST

Each row passes or fails. No partial credit.

**C1 — THE NEW DEMO RUNS FROM ROADMAP**
A dashboard serves the new demo from a roadmap-based checkout. `/api/preflight` reports
`all_ok` and a `git_head` matching the cutover commit.

**C2 — GRAPH ISOLATION IS STRUCTURAL, NOT CONFIGURED**
The new demo uses its own dedicated Neo4j instance on a port that is neither 7688 (roadmap's
dev graph), 7689 (the frozen demo's), nor 7687 (the shared no-owner fallthrough).
The dashboard **refuses to start** — loudly, not silently degrading — if `NEO4J_URI` ever
resolves to 7689.
**Fault twin:** point it at 7689 and confirm it refuses; restore and confirm it starts.

Note: `~/.env.dev` is a home-directory file loaded with `override=True` unconditionally.
A new checkout's own `.env` or `config.yaml` cannot override it by precedence. The guard
must be a hard-coded refusal, following the pattern `demo_preflight.sh` already uses to pin
7688.

**C3 — ALL THREE SCRIPTS RUN END TO END ON THE NEW BASE**
boundary_and_consent (4 turns), speaker_isolation (7 turns), trust_ladder (5 turns) each
complete against roadmap's newer injection contract. Every turn's tier, guard outcome and
admitted fact set is recorded.
Any turn that behaves differently than it did on hip-vo is reported as a **FINDING**, not
silently accepted.

**C4 — THE TRUST_LADDER FILENAME COLLISION IS RESOLVED BY VERSION BUMP**
`trust_ladder__v20260716_1600.json` exists on both trees with the same filename and
different content — 5 turns on hip-vo, 4 on roadmap. hip-vo's T05 was added by `517dd7c`
without a version bump.
The 5-turn version lands under a **new versioned filename**. Roadmap's 4-turn file is marked
superseded and kept. Neither is silently overwritten.

**C5 — THE EPISTEMIC STATE PANEL IS ON THE NEW BASE**
The fixed five-rung ladder with plain-English labels renders and moves when trust_ladder
runs. Roadmap's own crypto and dyad UI additions still render.

**C6 — THE DASHBOARD SELF-CHECK SYSTEM IS PORTED**
`GET /api/preflight`, `_startup_self_check` and `_degraded_mode_guard` exist on the new base.
Roadmap has none of it today, and C2's guard needs somewhere to live.

**C7 — THE CONSENT-GATE ASSERTION IS RE-VERIFIED**
`demo_preflight.sh`'s `run_consent_check()` passes on the cutover commit.
It was proven MET at `cfd1f96`. Roadmap HEAD is 162 commits past that and it has not been
re-run since. This closes a live-verification gap, not a build gap.

**C8 — THE FULL HARNESS PASSES**
`eval.harness --full` runs on the cutover commit. The AUDIT is green. Any new red is a
FINDING and is reported with its cause, not baselined away.

**C9 — THE PROBE SETS RUN AGAINST THE NEW BASE**
Both 200-item probe sets run and their results are compared against the hip-vo baseline
(Voice 38, `/tmp/voice38_set1_results.csv`). Specifically report whether these three change:
the leak count of 6; the 11-of-33 unresolved-reference answer rate; the 7 items producing
guard-shaped prose with no guard fired.

**C10 — THE FROZEN DEMO IS UNTOUCHED**
`~/hip-dev` shows zero diff throughout. Its dashboard PID and its Neo4j on 7689 are
unchanged. Verified before and after by PID, not assumed.

## WHAT'S ALREADY DONE — DO NOT REDO

- `REQ_DEMO_PREFLIGHT_CONSENT_ASSERTION` is **MET**, built on branch `demo-cutover`
  (`5b7a5bb`), with fault-injection twins proven red-on-command. `run_consent_check()` is
  live at `demo_preflight.sh:110-256` and wired into the main sequence at 674-675.
- Roadmap's `demo_seed.py` (522 lines) already has the crypto and identity-binding seed
  infrastructure hip-vo lacks: `_ensure_identity_keypair`, `_ensure_seal_keypair`,
  `_ensure_dyad`, `_ensure_household_circle_member`, `_ensure_care_team_member`.
- `scripts/demo_run.py` is byte-identical on both trees (commit `cfaf057`). Nothing to port.
- Ports 7690, 7691 and 7692 were confirmed free on 2026-08-02.
- **(D-106, 2026-08-02)** `demo-cutover` branch (`5b7a5bb`) is fully merged into `roadmap` —
  0 commits ahead, 73 behind. It is stale/closed-out history, not a live base; the worktree
  below is cut fresh from current roadmap HEAD, not from that branch.

## WHAT'S KNOWN BROKEN

**On hip-vo, and therefore fixed for free by moving to roadmap:**
- `harness/hipconfig.py:30` — `SENSITIVITY_RANK` has no `"critical"` key. A critical-
  sensitivity fact ranks below the lowest category on the routing path. This is TD-137, live
  on hip-vo today. Voice 38's baseline ran on this code.
- No `_ATTRIBUTE_FAMILIES` concept, so a plain "what medication is X on?" misses a fact filed
  under a narrower attribute. hip-vo only narrowed the write-time trigger.
- No caregiver permit condition on INJ-3. A multi-caregiver scenario is not representable.
- No `AnswerMode` gating on the grounding guard.

**On roadmap, and therefore inherited:**
- No dashboard self-check system at all. See C6.
- Demo scripts are five versions behind and the declutter never landed — the newest
  boundary_and_consent is `v20260717_1330` (6 turns), still at `demo_scripts/` root.
- Only the older Epistemic Timeline in `demo.html`. See C5.
- No `pending_disclosures.json`-clearing fix in `demo_reset.py` — a stale-gate TTL hijack
  hip-vo closed on 07-29.

**Both trees:**
- 6 leaks, 11-of-33 unresolved references answered, and 7 guard-shaped-prose replies were
  measured on hip-vo. Whether any of these change on roadmap is **unknown**. C9 measures it.

## CONSTRAINTS — WHAT MUST NOT REGRESS

- The frozen demo is never modified. It stays the fallback until the new demo has passed
  C1 through C9.
- No silent overwrite of any script file that exists on both trees under the same name.
- The new demo never writes to 7689, and that is enforced by a refusal, not by configuration.
- Voice is **out of scope**. `voice-port` and `voice-latency` are deliberate phase 2, scoped
  separately. The demo work in scope here is entirely text-based and depends on none of it.
- Roadmap is the other lane's active tree. Lock discipline applies; this work coordinates
  with them rather than assuming the tree is free.
- No acceptance row is marked MET by a session. That is Bill's call.

## ESTIMATE

| Piece | Hours |
|---|---|
| Port and re-verify the three demo scripts against roadmap's newer injection contract, including the C4 version bump | 4-8 |
| Port the Epistemic State ladder, reconcile with roadmap's crypto/dyad UI | 4-6 |
| Port the self-check and degraded-mode system, add the C2 refusal guard | 3-5 |
| Port the `demo_reset.py` pending_disclosures fix | 0.5-1 |
| New dedicated Neo4j instance and config wiring | 2-4 |
| Full harness run, re-run `demo_preflight.sh`, live-fire every script end to end | 4-8 |
| **Total** | **18-32** |

Voice, if pulled into the same pass instead of phase 2: **+13-26 hours**.

## RULINGS (Bill, 2026-08-02)

Three rulings on this REQ's open items, given verbatim:

> "Three rulings on REQ_DEMO_CUTOVER's open items, Bill, 2026-08-02:
>
> 1. PORT: 7690. Confirmed free. New dedicated instance at ~/neo4j-cutover-demo,
>    its own data dir, own conf, own credentials.
>
> 2. TREE: a NEW WORKTREE of the roadmap repo, not a branch inside ~/hip-roadmap.
>    Reason: ~/hip-roadmap is the other lane's active tree and the lock caught two
>    live collisions there today. A separate worktree gives the demo its own checkout
>    of the same repo, which is the pattern already in use across hip-dev, hip-vo and
>    hip-roadmap. Two lanes writing one checkout is the thing to avoid.
>
> 3. C9 PROBE COMPARISON: MEASUREMENT, with ONE GATE.
>    The 6-leak baseline was measured on hip-vo, which ships the sensitivity bug
>    roadmap fixed. The numbers SHOULD move, and some movement is improvement.
>    So the comparison does not gate the cutover — EXCEPT that leaks must not
>    INCREASE. If the leak count goes above 6, that is a STOP and a finding, not a
>    number to baseline. Everything else in C9 is reported, not gated.
>
> Record these in the REQ and proceed."

**Effect on the open items below (D-106):**
1. RESOLVED — port is 7690, not 7691 or 7692. See infra dispatch DISPATCH_DEMO_CUTOVER_INFRA.
2. RESOLVED — new worktree, cut fresh from roadmap HEAD (not the stale `demo-cutover`
   branch — see WHAT'S ALREADY DONE). See infra dispatch for path/branch.
3. RESOLVED — C9's text above is unchanged (it already only *reports* the three numbers);
   this ruling adds a gate not previously stated in C9: **leak count increasing above 6 is
   a STOP**, treated as a blocking finding, not a baseline to accept. The other two C9
   measurements (unresolved-reference rate, guard-shaped-prose count) remain
   measurement-only, ungated.

## OPEN — BILL'S CALL, NOT MADE

~~1. Which port for the new Neo4j instance. 7690 recommended and confirmed free.~~
~~2. Whether the new demo tree is a new worktree or a branch in an existing one.~~
~~3. Whether C9's probe comparison gates the cutover, or is measurement only.~~

All three resolved by the RULINGS section above (2026-08-02). Nothing open at filing time.
