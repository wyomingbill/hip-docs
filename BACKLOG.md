# BACKLOG — single source of order
Status: LIVE (working list — edit in place; this file is exempt from the
Naming Law's "never overwrite" rule, same exemption as INDEX.md and
LATEST_DEBT.md, because its whole job is to be the one current queue)
Reconciled-Against: main 33049a4, 2026-07-17

Sources reconciled into this one list:
- `docs/deliverables/HIP_DefectRegister__v20260715_1930.md` (D-*, I-*, H-*, X-*)
- `docs/deliverables/HIP_HarnessPlan__v20260715_1600.md` (Phases 0-7)
- `docs/deliverables/HIP_SIA_PhaseB__risk-memo__v20260716_1624.md` (§9 items 0/0b/1-6)
- `docs/techdebt/DEBT_REGISTER__v20260712_2300.md` (TD-*)

Dispatches for this reconciliation:
`docs/dispatches/DISPATCH_BACKLOG__reconcile-four-registers-into-single-order__v20260717_0658.md`
`docs/dispatches/DISPATCH_BACKLOG_GOVERNANCE__governed-defect-ungoverned-tagging__v20260717_0658.md`

Rule going forward: **work top-down.** If something jumps the queue, say so
and why, in a dispatch doc — not silently.

Fixed/closed items are not carried here. A short REMOVED appendix at the
bottom lists what was checked and dropped, for audit only.

---

## NAMED NEXT BUILD — the CLAIMS LEDGER STATUS GENERATOR (filed HA-21, 2026-08-09)

**UNGOVERNED — needs a REQ before any code.** Filed here as the named next build by Bill's
HA-21 instruction, which also says explicitly: **do NOT build it in that dispatch.**

**What it is:** a sibling of `scripts/ceiling_status.py`. It **derives** each claim's status
in `docs/deliverables/LATEST_HIP_ClaimsLedger.md` from the standing runs, and renders **two
outputs from ONE computation** — the private ledger and the public test-results subset.

**Why one computation and not two renderers, in the ledger's own words:** *"the public
test-results page renders from the same computation and may never exceed this ledger."* Two
computations could drift, and the direction that matters is the dangerous one — a public
page claiming more than the evidence supports. One computation makes that structurally
impossible rather than a review item.

**What it retires:** v1's statuses are **Claude's draft assessment**, marked as such in the
ledger's own header. They stop being asserted and start being computed the day this lands.
After that, **no session hand-rules a status, ever** — that is the ledger's governing rule.

**What it must NOT do:** let the `Timeline` column touch a status. The ledger is explicit
that the timeline is *"forecast only and can never influence a status or weaken an
acceptance."* A generator that reads it into a status has broken the instrument.

**Prerequisite that is Bill's, not the build's:** the claim WORDING is still v1 DRAFT
awaiting his ruling, and the claim-to-evidence map changes only by his ruling. The generator
can be specified against the current wording, but a REQ written before the wording is ruled
should say so.

---

## GOVERNANCE KEY — the point of this addendum, not a footnote

Every item below carries one of three tags:

- **GOVERNED** — a REQ doc in `docs/requirements/` already names and
  authorizes this exact work. The REQ doc is cited.
- **DEFECT** — has an ID in the defect or tech-debt register, root cause
  and fix location are pinned, blast radius is local. Per Bill: no REQ
  needed, fix it and close it.
- **UNGOVERNED** — needs a REQ doc before any code changes. Either no REQ
  exists, or an existing REQ explicitly does not cover this (REQ_HARNESS
  says "This task is Phase 1 only" in its own text — everything past
  Phase 1 is UNGOVERNED by REQ_HARNESS's own words, not by omission).

**The dividing line between DEFECT and UNGOVERNED is not severity, it's
blast radius and provenance.** A cosmetic `%d` bug is DEFECT. A change to
the classifier's default behavior that "collapses three other defects"
(D-01) is UNGOVERNED even though it has a defect ID and a pinned
file:line — because a wrong call there ripples everywhere, same as SIA's
did twice. TD-123 is UNGOVERNED for a documented reason: five prior fix
attempts each patched one layer and broke another. A sixth ad hoc patch
without a REQ and an acceptance test would repeat that exact pattern.

**The SIA track is marked UNGOVERNED in full, per Bill's explicit
instruction.** It originates from a chat session's theory doc, then a
Fable review, then a risk memo, then Bill "adopting" the result — an
adopted analysis, not a stated requirement. It shipped code twice
(`c86a414`, `3c0cb74`) and both carried regressions the ratchet caught
later, not before. Every item numbered 1-6 in the risk memo's §9 sequence
is UNGOVERNED below, no exceptions. This includes **G0/item 0b** — even
though `REQ_SIA_PHASEB` claims REQ_VOICE_DEMO is G0's "parent requirement,"
that same doc admits in its own text: *"REQ_VOICE_DEMO's text does not
name trust_ladder, D-03, D-18, or G0... The connection above is this doc's
inference, not a quote."* An inference by the same analysis lineage under
scrutiny is not governance. G0 needs its own REQ.

**The frontier tier is UNGOVERNED and it is the top demo item.** Nothing
in `docs/requirements/` authorizes building it. It needs a REQ before
anyone writes code, same as Bill said.

---

## NEEDS BILL — nothing below this line proceeds without him

| ID | Decision | Governance | Why it's stuck |
|---|---|---|---|
| BILL-1 | **Frontier tier: RESOLVED and the real round trip is now live-proven (2026-07-17).** Built (`DISPATCH_FRONTIER_TIER_BUILD__script1-t04-t05__v20260717_1330.md`) and the previously-blocked real Anthropic call completed with a working key (`DISPATCH_FRONTIER_TIER_LIVE__real-anthropic-roundtrip__v20260717_1530.md`): real setback answer for R-1-18 returned, landed ASSERTED (`write_state=augment`, `confidence=medium`) via the normal write path, coexisting with D11; boundary_and_consent T04/T05 landed 5/5 on fresh reset+seed. No blocker remains. | **GOVERNED — `REQ_FRONTIER_TIER`.** | None — resolved. |
| BILL-2 | **SIA Phase B cutover (Gate B).** 85.7% agreement against a 98% bar — but the memo argues the incumbent classifier is wrong on exactly the class SIA exists for, so an unknown share of the 14.3% gap is SIA being *right*, not SIA being worse. Cutover is explicitly "Bill's call only" (risk memo §8). | **UNGOVERNED** | Named explicitly Bill-only. The whole SIA track (items 1-6, backlog #39-44) sits behind this and is ungoverned regardless of how it resolves. |
| BILL-3 | **Spanish support — product goal or not?** Currently prompt-enforced English-only. No golden set, no oracle. `REQ_SIA_PHASEB` is explicit this is a product question, not a defect — filed so it doesn't resurface as a test gap. | **N/A** — no REQ is relevant until this becomes a stated product goal. | Needs a real product decision first. |
| BILL-4 | **G1 hard-zero gate: what do we do about the flake?** (I-10 / H-06, one design call.) ~91% failure rate on `--full`, one repeat-offender query. Three options: (a) keep hard-zero, fix detection reliability; (b) move G1 to the ratchet; (c) retry the detection step once. | **UNGOVERNED** | `REQ_HARNESS` itself says I-10 is "scoped OUTSIDE this REQ_HARNESS's own target... but it shares the same gate" — its own text excludes this. Option (b) would also directly contradict REQ_HARNESS's own written CONSTRAINT ("G1 and G4 must gate at HARD ZERO") — that's not a silent amendment, it needs Bill's explicit sign-off either as a new REQ or an amendment to the existing one. |
| BILL-5 | **TD-110: cross-member write authority.** Any member can supersede another member's health fact today with zero authority check. Two forks on file: (A) caregiver authority is intended, make it visible; (B) cross-subject writes land UNCONFIRMED, need a second signal. | **UNGOVERNED** | No REQ exists. "Decision required before fix" has stood unaddressed since 2026-07-08. |
| BILL-6 | **HarnessPlan Phases 2, 4, 6, 7 — deferred or abandoned?** `REQ_SIA_PHASEB`'s own reconciliation asserts "none are dead, just sequenced last" — but that assertion was written by an analysis session, not decided by Bill. Ask, don't assume it stands. | Gates items **UNGOVERNED** below (#34-38, #11, #33) regardless of the answer — even "still wanted" doesn't authorize code without a REQ per phase. | Untouched two days, no defect ID tracks the deferred/abandoned question itself (Phase 5/H-09 is the one exception — already confirmed "missing, not deferred," doesn't need this answer). |
| BILL-7 | **hip-vo has NO SANCTIONED GRAPH TARGET — which bolt port should it use?** The checkout has no repo `.env.dev`; `~/.env.dev` is forbidden by the preamble (it pins **7689, the frozen demo**); `.env.dev.example` says **7688**, which is the *roadmap* lane's graph; and `server/voice_https_orch.py` defaults to **7687** when `NEO4J_URI` is unset. **All four bolt ports (7687/7688/7689/7690) are listening**, so a wrong guess writes into another lane's graph rather than failing. **Consequence, already paid twice:** HA-50 and HA-51 could not run any graph-dependent suite or the memory harness on hip-vo — endpoint and source twins only. **A session must not resolve this by picking one**; that is the exact wrong-graph failure the lock/graph-separation rules exist to prevent. | **UNGOVERNED** — no REQ names hip-vo's graph. | Needs Bill: name the port (or say hip-vo is graph-less by design and the suites are permanently out of scope there). |

---

## HA-50 / HA-51 VERIFICATION GAP — recorded verbatim (HA-51 Part C, 2026-08-12)

Recorded so **nothing downstream reads HA-50 as full system verification**:

> **Graph/memory integration verification: NOT TESTED (hip-vo has no sanctioned graph
> configuration; endpoint + source twins only).**

**Applies to HA-50 and to HA-51 alike.** What WAS verified on hip-vo: endpoint auth twins
(401/200 both directions), source-level twins proving the four real endpoints carry a guard,
the `_build_requester` change exec'd from real source, and the master-key C1-C4 twins — **all
of which run without a graph.** What was NOT verified: anything requiring Neo4j, including the
memory harness, which has **no number against the 13-15/17 pin for either dispatch.**

**This is a coverage gap, not a failure** — but it is also not a pass, and it stays here until
**BILL-7** is answered and the suites can actually run.

**Surface choice, reported per the dispatch:** the HA-50 *dispatch doc* does not exist — HA-50
was reported terminal-only by its own routing rule — so the record went to **its dispatch-ledger
row in `docs/INDEX.md`** (the canonical home for a dispatch that produced no doc) and **here**.
**The claims ledger was deliberately NOT used:** its rows are claims about what the system does,
its statuses are computed from standing runs by the generator and **never hand-edited by a
session**, and a verification-coverage gap is not a claim status. Writing it there would have
been the wrong instrument.

---

## THE ORDERED BACKLOG

Ordered by what unblocks what. Each item: ID, one line, goal (1 = demo that
is true, 2 = product that works, 3 = harness that catches), governance tag,
blocked-by, whether Bill is needed.

| # | ID | One line | Goal | Gov | Blocked by | Bill? |
|---|---|---|---|---|---|---|
| 0 | **Frontier tier (Script 1 T04/T05) — BUILT and DONE, real round trip live-proven.** Disclosure gate, code-built payload builder, Anthropic frontier client, return-path write, T05 EDGE summary, and the T04/T04b/T05 script turns are all built and live-tested end to end, including the actual Anthropic round-trip (`DISPATCH_FRONTIER_TIER_LIVE__real-anthropic-roundtrip__v20260717_1530.md`, `~/.env.dev` key now valid): real setback answer for R-1-18 returned and captured (request + response), landed ASSERTED via the normal write path (`write_state=augment`, `confidence=medium`, coexisting with D11), T05 summary short + email-offer confirmed. boundary_and_consent T04/T05 landed 5/5 on fresh reset+seed each time. Gate/decline/write/summary all verified live. TD-128 registered (per-member key storage, explicit debt per Bill's own words) — still open, out of scope. | 1 | **GOVERNED — `REQ_FRONTIER_TIER`.** | Nothing — done. | No |
| 0b | **D-25** | **RESOLVED 2026-07-21 at 605bb79 — DK4 green, `--layer 7` 19/19, RATCHET PASS.** Root cause was suspect (b), sharper than filed: not worktree cross-counting but a registry/ledger provenance split — `.env.dev` pointed `HIP_REGISTRY_DB` at `~/hip-dev/data/registry.db` (shared with the hip-dev checkout) while custody.grant events land in the checkout-local `ledger/`, so DK4 counted hip-dev-seeded wraps (3) against roadmap-local grants (2). Suspect (a) cleared by code read: both INSERT sites in `dyad_registry.py` emit on the same path; f94fb11 epoch/care-team key classes are docs-only, no code writes wraps. Fix (605bb79): (1) `.env.dev` now pins `HIP_REGISTRY_DB` to `$HOME/hip-roadmap/data/registry.db` (per-checkout, file gitignored so the change lives on the mini); (2) harness guard beside the NEO4J_URI guard refuses Layer 7 when `HIP_REGISTRY_DB` is unset or resolves to the shared `~/hip-harness/registry.db` — both refusals negative-tested live; (3) `_emit_custody_grant` moved inside the SQLite transaction at both INSERT sites, closing the commit-then-emit crash window that could orphan a wrap. Mac-side evidence pull (2026-07-21, read-only) located the split via path resolution from three checkouts. | 2, 3 | **DEFECT — RESOLVED** | Nothing. | No |
| 0c | **D-26** | **Master-key split across checkouts — filed 2026-07-21 from STAGE1_RUN_SUMMARY.md (REQ_IDENTITY_BINDING Stage-1 unattended run, Jul 18), fix DELIBERATELY DEFERRED to Phase 3 planning.** The launchd dashboard plist (com.hip.demo.dashboard.plist) has had HIP_MASTER_KEY=~/hip-dev/data/encryption/.master_key baked into EnvironmentVariables since ~Jul 3, while harness/encryption.py's DEFAULT_MASTER_KEY_PATH resolves ~/hip-harness/data/encryption/.master_key for every process without the override (harness, demo_seed, manual runs). The two key files differ (distinct SHA-256; hip-dev key auto-created Jul 3, hip-harness key unchanged since Jun 20). Measured against the live graph: all 11 active :Fact nodes decrypt under the hip-dev key, ZERO under the hip-harness default — one population, 100% hip-dev-keyed; the hip-harness default file is orphaned, nothing in the graph belongs to it. Practical effect: any process reading with the default key gets InvalidToken (encryption.py:121 via extraction_queue.py:745) — this is what put the unexplained red into Stage 1's --full (INJ-3/INJ-6b baseline). Same disease family as D-25: home-anchored default plus per-process env override splitting one logical store across checkouts; D-25 closed the registry/ledger instance, this is the master-key instance. Fix direction already unambiguous from the data (align default or env on the hip-dev key — a design call reserved for Bill), DEFERRED to Phase 3 planning rather than fixed opportunistically. | 2, 3 | **DEFECT — DEFERRED by decision** | Phase 3 planning. | Yes — default-path vs env alignment is his call. |
| 1 | **D-06 / D-07** | Guard (INJ-6) fails to fire on `[bill] "What are my allergies?"` even though the patched predicate evaluates True — two records for the same query 2.3s apart give opposite outcomes. UNDER TRACE. | 2 | **DEFECT** — investigation task, no design decision to make yet. | Nothing — ready now. | No |
| 2 | **I-06 / G0 / risk-memo item 0b** | The runtime gate closing I-06's blind spot (reply names a registered member/care-recipient while nothing is admitted about them) is specced twice and built nowhere. Highest-leverage unbuilt item on this list. | 2, 3 | **UNGOVERNED** — see GOVERNANCE KEY above on why `REQ_SIA_PHASEB`'s "parent requirement" claim doesn't count. Needs REQ_G0 (see missing-REQ list). | REQ_G0 must be written first. | No — but a REQ is required before code |
| 3 | **D-01** | Fail-open routing: classifier defaults to `knowledge` (its most dangerous state) on both below-threshold and embedding failure. Fixing this collapses D-02/D-04 into smaller problems. | 2 | **UNGOVERNED** — high blast radius ("collapses three other defects"), and it's HarnessPlan Phase 3 territory, which REQ_HARNESS's own text scopes itself out of ("This task is Phase 1 only"). | REQ_D01 must be written first. Advisory: trace D-06/D-07 before trusting the fix's own verification. | No — but a REQ is required before code |
| 4 | **D-02** | Classifier has zero third-party exemplars — all ~30 `personal` entries are first-person; the eldercare beachhead is entirely third-party. | 1, 2 | **UNGOVERNED** — tied to BILL-2: patching the current classifier's exemplars could be throwaway work if SIA replaces it. | REQ_D02, and a steer from BILL-2 on whether to invest here at all. | Soft — see BILL-2 |
| 5 | **D-04** | Subject resolution matches "Ray Charles" to household member `ray`, root-causing D-09's accepted refusal on general-knowledge questions. | 2 | **DEFECT** — narrow, single heuristic fix, low blast radius. | Nothing | No |
| 6 | **REQ_VOICE_DEMO mic-control build** | Scripted demo completes (all 3 scripts, post D-03/D-18); the live-voice half of the acceptance test has never run end to end. No mic control exists on `/demo`. | 1 | **GOVERNED — `REQ_VOICE_DEMO`.** This gap is literally what that REQ's own KNOWN BROKEN section describes. | X-01 doc correction first, so the build starts from an accurate list. | No |
| 7 | **Voice-path exit-gate exposure** | D-03/D-18 and #2 above (once built) land in the text-query path only. `realtime_adapter.py` runs its own cascade, shares no checkpoint — voice keeps today's exact exposure. | 1 | **UNGOVERNED** — `REQ_atorvastatin` explicitly names this "out of scope here," no REQ covers it. Needs REQ_VOICE_CASCADE_CHECKPOINT. | REQ must be written first. | No |
| 8 | **X-01** | `REQ_VOICE_DEMO` says "there is NO mic control on /demo" — the mic has existed since `4cd9dc7`. Doc is stale. | 1 | **DEFECT** — doc-only correction, not a code change; no REQ applicable. | Nothing | No |
| 9 | **X-02** | Script 02 prep doc overclaims "nothing in the mechanism asks a model to behave" — false for anti-fabrication. Doc fix. | 1 | **DEFECT** — doc-only. | Nothing | No |
| 10 | **X-03** | Run-of-show Beat 3 says "56ms, model not called" — true on the guard path, false on the grounding-guard path (same string, two emitters). Doc fix. | 1 | **DEFECT** — doc-only. | Nothing | No |
| 11 | **X-05 / HarnessPlan 2.3** | `disclosure_oracle.FIXTURE` is hand-transcribed with a "verify before trusting" comment instead of code that verifies against `demo_seed.FIXTURES` at import. Same item as HarnessPlan Phase 2.3. | 3 | **UNGOVERNED** — bundled under Phase 2's own authorization question (BILL-6). | BILL-6, then REQ_HARNESS_PHASE2_ONWARD. | Yes — see BILL-6 |
| 12 | **D-16** | `EMPTY_SET_RE` can't distinguish a structural guard firing from a model hedge in the same words — same conflation family as D-06. | 2 | **DEFECT** — narrow instrumentation fix (assert `guard_kind` instead of string-matching). | Nothing, but shares root cause with D-06/D-07 — do after #1. | No |
| 13 | **I-08** | `harness_run.jsonl` is 0 bytes with an mtime after every other log — truncated post-run. UNDER TRACE. | 3 | **DEFECT** — investigation task. | Nothing | No |
| 14 | **I-09 (residual)** | `reply_source` field covers model and pending-park-gate paths; the F3 zero-write path still doesn't set it. | 3 | **DEFECT** — small field completion. | Nothing | No |
| 15 | **D-21** | **ROOT CAUSE FIXED 2026-07-17, triple-verified live — NOT fully closed, see row below.** `CANONICAL_ATTRIBUTES` widened to include `incident`/`medication_status` (REQ_D21_D23). The 100%-deterministic schema block is conclusively gone: isolated live turn + direct sync call + frozen-context re-measurement all show real detection/mutation (19/20 net after retry, vs 0/20 before). 24-utterance corpus still 0/24 — no regression. **But `--full` still fails `L2:three_zone_demo.T02`** — a residual ordinary stochastic miss (not the schema gap) trips the F3 zero-write gate into a false "nothing changed" reply on a turn where Neo4j shows the write landed. Hypothesized same family as I-10/H-06, not confirmed. See `DISPATCH_D21_D23__enum-widened-seed-validated-d10d11-blocked__v20260717_1240.md`. | 2 | **DEFECT** — root cause closed; scenario pass and the false-ack question still open, Bill's call. | Accept the residual ~5% stochastic rate, or invest in detection reliability; decide if the false-ack is I-10/H-06 or a new ID. | No |
| 16 | **TD-123** | Groq's fact detector still misfiles a fact's VALUE into the person-typed subject slot in some cases. Five stacked mitigations shipped; prompt hardening (the actual fix, subject-must-be-a-PERSON) still pending. **CORRECTED 2026-07-17: this is NOT D-21/D-23's fix track.** TD-123's own written scope is subject-slot person-typing, unrelated to missing/mismatched attribute categories — a citation error traced to two different documents both informally routing unrelated bugs through "TD-123." See the CITATION WARNING appended to TD-123's own tech-debt entry. | 2 | **UNGOVERNED** — five prior fix attempts each patched one layer and broke another. A sixth patch without a REQ and an acceptance test repeats that pattern. Needs REQ_TD123, scoped ONLY to subject-slot typing. | REQ must be written first. | No |
| 15b | **D-23** | **CLOSED 2026-07-17. Items 1/2/4 FIXED (enum widened, see D-21; `risk_pattern`/D8 deliberately excluded, DERIVED, on the record; seed path refuses loudly on an out-of-enum attribute, live-tested; companion INJ-2/INJ-6b keyword coverage added). Item 3 (D10/D11 disambiguation) RESOLVED by Bill's Q8 answer** (`DISPATCH_FRONTIER_TIER_BUILD__script1-t04-t05__v20260717_1330.md`): do NOT migrate to `household` — confirms the `verify_seed`/D7 collision found live was real, not a transient bug. `address` and `zone_district` added to `CANONICAL_ATTRIBUTES` as their own values instead (13 → 15). `_ENUM_EXEMPT_LABELS` no longer needs D10/D11 (now just `{"D8"}`). Re-verified live 2026-07-17 1500 (`DISPATCH_FRONTIER_TIER_VERIFY__post-session-loss__v20260717_1500.md`): fresh reset+seed, `verify_seed()` passes, no D7/D10/D11 collision, D11 prints `R-1-18`. See also `DISPATCH_D21_D23__enum-widened-seed-validated-d10d11-blocked__v20260717_1240.md` for the original collision trace. | 2 | **CLOSED.** | Nothing — all 4 items resolved. | No |
| 17 | **TD-125** | **MEASURED 2026-07-17, no longer "unmeasured": retry recovery rate on D-21's utterance is 0/20 (0%). Aggregate corpus miss rate at temp=0.0 is 0/24 (0%) — nothing else needed a retry to measure against.** Doubling latency on idempotent turns remains a real, separate cost (unmeasured recovery-rate concern is now closed; the latency-cost concern is not). See `DISPATCH_DETECTION_MISS_MEASUREMENT__d21-and-td125-numbers__v20260717_1117.md`. | 2, 3 | **DEFECT** — measurement done; if the latency-cost question needs action, that's a new, separate item. | Nothing further to measure for recovery rate. | No |
| 18 | **TD-122** | No fact in the demo/harness graph carries an embedding — "semantic retrieval" is a recency window (limit 8) today. Fix direction already proven safe elsewhere (`extraction_queue.write_facts`'s subject+predicate-only embedding pattern). | 2 | **DEFECT** — scoped, precedented fix. | Nothing | No |
| 19 | **TD-115** | Subject resolution maps "my mother Elena" to the wrong member/gender in some cases; ack wording sometimes misattributes a correctly-written fact. | 2 | **DEFECT** — pinned root cause, narrow fix. | Nothing | No |
| 20 | **TD-120 (D2 only)** | "What did I tell you about my mother's medication?" fails — the relational bridge fact is never stored from "My mother Elena..." utterances. D1/D3 of this TD already fixed. | 2 | **DEFECT** — narrow gap, clear fix target in Groq extraction. | Nothing | No |
| 21 | **D-14 / TD-127** | Speaker verification error rate is now measured (0.632-0.677 against a 0.50 threshold). Decision already made: disclosed stand-in for a real vendor, not a target for this codebase to close. | 1, 2 | **N/A** — closed by decision, not by build. Standing constraint: never claim speaker ID in a demo. | Nothing | No — already decided |
| 22 | **TD-126 (residual)** | Log-path fixed. Voiceprint deletion still reaches the frozen `hip-harness` checkout for maya/sam — fixing it touches the shared-voiceprint architecture, explicitly out of scope per TD-127's "don't build further" call. Accept as-is. | 3 | **N/A** — accepted residual, no action. | Nothing | No |
| 23 | **D-10 / TD-101b** | **FIXED 2026-07-18 (REQ_SECURE_DEV_ENDPOINTS).** Traced from "known gap" to a live, chainable plaintext bypass this session, then closed: `/api/decrypt` now takes only `fact_id`, looks up ciphertext/DEK/owner server-side, and only decrypts when the fact's owner matches the session's server-tracked selected member (or `'household'`); `/api/facts` gated behind the same session and stripped of `ciphertext`/`encrypted_dek`. Live-verified end to end (unauthenticated → 401 both endpoints; cross-member decrypt attempt → 403; correct-member decrypt → real plaintext; other panes unaffected). See `docs/dispatches/DISPATCH_SECURE_DEV_ENDPOINTS__api-facts-decrypt-auth__v20260718_1059.md`. | 2 | **DEFECT, was correctly classified — turned out NOT to need architectural scope beyond the two named endpoints.** | Nothing — closed. | No |
| 24 | **TD-101 (broader)** | Unauthenticated dashboard endpoints generally (`/api/reset`, `/api/demo/*`, `/api/text-query`'s client-supplied `member` field — this last one newly named by the isolation trace, distinct from D-10); embedding path may still touch a fact value pre-encryption; git-history scrub pending. Sits in a STALE audit doc. `/api/facts`+`/api/decrypt` no longer part of this item's scope (closed via #23). | 2 | **UNGOVERNED** — scope is fuzzy across several different sub-problems and one auth-model decision (session? bearer token? mTLS? — #23 set a session-cookie precedent this could extend). Needs REQ_TD101. | REQ must be written first. | No |
| 25 | **TD-108 (HEL Phase 2)** | Per-fact consent ledger, Phase 1 BUILT. Phase 2 (`fact.detect`/`value.decrypt`) has a detailed spec doc but no REQ. | 2 | **UNGOVERNED** — a spec under `docs/specs/` is not a REQ doc under `docs/requirements/`; CLAUDE.md's gate is specific about which folder. Needs REQ_HEL_PHASE2 (can mostly just cite the existing spec). | REQ must be written first. | No |
| 26 | **TD-109** | Biometric consent-and-retention control for speaker recognition. Real multi-part build (consent screens, retention schedule, audit log). | 2 | **UNGOVERNED** — substantial feature, needs its own REQ. | REQ must be written first. | No |
| 27 | **D-11 (residual)** | Two `demo_dashboard` processes bind :7871 — the launchd one shadows the working process. Key-sourcing fixed; shadow process still runs. | 2, 3 | **DEFECT** — disable/unload one launchd plist. | Nothing | No |
| 28 | **TD-103 / TD-104** | Ops flakiness: launchd bootstrap fails ~1-in-N; Neo4j password's shell-special char trips edits. Workarounds already on file. | 2 | **DEFECT** — known fixes, just apply them. | Nothing | No |
| 29 | **D-08** | `NET=ON` prints in green on external Groq calls — a false claim on screen. | 1, 2 | **DEFECT** — single display-logic fix. | Nothing | No |
| 30 | **D-12** | `parked=%d` prints a literal `%d` — cosmetic. | 2 | **DEFECT** | Nothing | No |
| 31 | **D-09** | Accepted, not a fix target — D-04's root cause surfacing. Carried for traceability. | 2 | **DEFECT** — tracking only. | D-04 | No |
| 32 | **TD-102** | `issue_INT-001_*.json` flagged 2026-07-05, never revisited, likely stale. | 3 | **DEFECT** — verify-and-close task. | Nothing | No |
| 33 | **HarnessPlan Phase 0 (residual)** | 0.3 done (I-03). 0.1 answered by D-04/D-09. 0.2/0.4 have no confirmed closure on file. | 3 | **UNGOVERNED** — bundled under Phase 2's authorization question; small. | BILL-6 | Yes — see BILL-6 |
| 34 | **Phase 2 — one oracle** (H-01..H-04) | Implementation-derived `expected` still stands beside a policy oracle whose docstring condemns exactly that; `no_leak` still passes on fabrication; `_valid()` still gives the implementation's blind spots amnesty. | 3 | **UNGOVERNED** | BILL-6, then REQ_HARNESS_PHASE2_ONWARD. | Yes |
| 35 | **Phase 4 — traffic that grows** (H-05) | All five `PHRASINGS` templates interpolate `{noun}` — the generator structurally cannot emit the idiom that breaks the classifier. Idiom bank / paraphrase pool / cosine-distance enforcement, unbuilt. | 3 | **UNGOVERNED** | BILL-6, then REQ_HARNESS_PHASE2_ONWARD. | Yes |
| 36 | **Phase 5 — metrics** (H-09) | Went missing, now tracked. Eight per-push metrics, none built. Doesn't need the deferred-vs-abandoned answer (already confirmed "not abandoned") but still needs its own REQ to authorize the build. | 3 | **UNGOVERNED** | REQ_HARNESS_PHASE2_ONWARD (or its own REQ). | No — governance question already resolved; still needs a REQ to build |
| 37 | **Phase 6 — record fidelity** (H-07) | `admitted[]` is a self-report; nothing verifies it matches what was actually serialized into the prompt. Partially closed; the hash-check itself is unbuilt. | 3 | **UNGOVERNED** | BILL-6, then REQ_HARNESS_PHASE2_ONWARD. | Yes |
| 37b | **Voice-path history disclosure ledger (residual of REQ_PROMPT_RECORD_FIDELITY)** | REQ_PROMPT_RECORD_FIDELITY's own EXPLICIT NON-GOAL, filed 2026-07-26: a fact disclosed in turn N reappears in turn N+5's prompt via `self._ctx._messages` (`voice_orch.py:1976-2011`) as plain assistant text with no `fact_id` attached — outside that later turn's own `admitted[]` entirely, invisible to any per-turn fact-id set comparison by construction, not by bug. A check built to REQ_PROMPT_RECORD_FIDELITY reports GREEN while history still carries facts. | 3 | **UNGOVERNED** — needs `REQ_VOICE_HISTORY_DISCLOSURE_LEDGER` (proposed, see MISSING REQ DOCS below); REQ_PROMPT_RECORD_FIDELITY's own text names this gap and points here. | REQ must be written first. | No — but a REQ is required before code |
| 38 | **Phase 7 — the gate, bifurcated** (H-08) | The ratchet is monotonic over a population where `value` is the only positive assertion — its fixed point is a system that refuses everything. | 3 | **UNGOVERNED** | BILL-6, then REQ_HARNESS_PHASE2_ONWARD. | Yes |
| 39 | **SIA item 1 — guards stop reading `intent`** | INJ-5's logic re-expressed from `speech_act`/`subject` axes instead of the 5-valued `intent` enum. | 2, 3 | **UNGOVERNED** — SIA track, no exceptions. | REQ_SIA_PHASEB_CUTOVER, and BILL-2. | Yes (via BILL-2) |
| 40 | **SIA item 2 — adjudicate the 14.3%** | Per-disagreement adjudication between SIA and the incumbent classifier, decided from policy. Gate B's real content. | 2 | **UNGOVERNED** | REQ_SIA_PHASEB_CUTOVER. Can produce findings without waiting on the cutover decision itself, but still needs a REQ to proceed as directed work. | No pending a REQ; cutover itself still needs BILL-2 |
| 41 | **SIA item 3 — re-key G1/G4 to SIO fields** | Shadow-only precision fix on invariants already running. Not a substitute for #2 (item 0b) above. | 3 | **UNGOVERNED** | REQ_SIA_PHASEB_CUTOVER. | Yes |
| 42 | **SIA item 4 — add `confirmation` to `VALID_TYPES`** | Closes the taxonomy gap that made trust_ladder T04 possible in the first place, now papered over by the D-03/D-18 gate fix rather than fixed at the type level. | 2, 3 | **UNGOVERNED** | REQ_SIA_PHASEB_CUTOVER. | Yes |
| 43 | **SIA item 5 — the decision table** | Guards become rows in one exhaustively-enumerated decision table instead of hand-written conjunctions. | 2, 3 | **UNGOVERNED** | REQ_SIA_PHASEB_CUTOVER, and items 1/4 above landing first as inputs. | Yes |
| 44 | **SIA item 6 — SIO fail-closed goes live** | The cutover itself. | 2, 3 | **UNGOVERNED** | REQ_SIA_PHASEB_CUTOVER, BILL-2, and everything above it in this sub-list. | Yes |
| 45 | **Gate integrity (risk-memo §7, residual)** | Mostly closed via D-17 (`--accept` now requires an ID/expiry). Worth a quick check that nothing else in this family is still open. | 3 | **DEFECT** — verify-only, no code change implied unless the check finds something new. | Nothing | No |
| 46 | **X-04** | D8 is seeded, not derived — "watch it infer" would be a false claim if said in a demo. No fix, just don't say it. | 1 | **N/A** — standing caution, not work. | N/A | No |
| 47 | **Frontier tier build** — SUPERSEDED, see row **#0** above. Kept as a pointer, not duplicated work. | 1 | **UNGOVERNED** | See row #0. | Yes |
| 48 | **TD-129** | Two `ollama serve` daemons on this box serve two DIFFERENT necessary ports (:11434 default, :11435 harness-classifier-pinned), not a stale/live duplicate pair — CORRECTED 2026-07-19 after stopping the presumed-stale one (:11434's daemon) took the port fully down and cascaded into 41 harness failures. Real issue: the two genuinely-necessary services contend for shared GPU/inference hardware under harness load, occasionally timing out a local call. | 3 | **UNGOVERNED** — no longer a narrow single-daemon fix; needs investigation into load-sharing or timeout tuning before any change. | Investigation, not a known fix. | No |
| 49 | **TD-137 — Two local clones of one remote keep separate docs/INDEX.md and MANIFEST.md** | `hip-roadmap` (branch `roadmap`) and `hip-vo` (branch `main`) are two independent local checkouts of the same GitHub remote (`wyomingbill/hip-dev`), and each registers its own deliverables into its own `docs/INDEX.md` and `docs/deliverables/MANIFEST.md` — the two registries have already diverged and will conflict on any merge between the checkouts. Same shape as the unresolved conflict already sitting in `hip-dev` on those same two files. Filed on discovery 2026-07-26 while registering diagram deliverables; not investigated further, not resolved. **RETARGETED 2026-07-27 (DISPATCH 35, `HIP_RegisterReconciliation__cross-branch-id-collisions__v20260727_1930.md`): this row originally reserved TD-135, but that number was never actually filed into `docs/techdebt/DEBT_REGISTER` — only reserved here. A later session filed a real, unrelated TD-135 (the corrupt `whitepaper/archive/HIP_White_Paper_Augmented.docx` finding) against the real register's own next-available number, creating a same-branch collision this row itself is an instance of the general problem it describes. Retargeted to TD-136 was also considered and rejected: TD-136 is reserved by this same dispatch for main's ported TD-131 (Groq MID/CORE payload finding, see the reconciliation doc's renumbering map). TD-137 is confirmed free on both branches as of this dispatch.** | 3 | **UNGOVERNED** — no reconciliation approach decided (per-checkout registries kept separate vs. one authoritative INDEX/MANIFEST vs. a merge/dedup step); the existing unresolved hip-dev conflict on the same two files should inform whatever the fix is. | Bill's decision on reconciliation approach. | Yes |
| 50 | **Prompt completeness (reverse of REQ_PROMPT_RECORD_FIDELITY's subset check)** | REQ_PROMPT_RECORD_FIDELITY's PSA1 check enforces `prompt_fact_ids ⊆ admitted_fact_ids` (a leak check) only — it does not, and per Bill's 2026-07-27 decision will not, catch an admitted fact_id that is silently dropped before render (under-disclosure, a different failure class from a leak). No real dropping path has been identified in current code: `voice_orch.py:2572-2573`'s declarative-turn rewrite (`dict(f, value=f"(about {subject}) {value}")`) preserves `fact_id` and overrides only `value`, so this is a plausible-gap named for the record, not a confirmed defect. | 3 | **UNGOVERNED** — needs `REQ_PROMPT_COMPLETENESS` (proposed, see MISSING REQ DOCS below), and not worth building until a real drop path is found. | A real drop path must be identified before this is worth building. | No — but a REQ is required before code |
| 54 | **Independent speaker verification ("belt and suspenders") — URGENT BEFORE THE VOICE 21 CONTRACT FREEZE** | **THE PROBLEM:** voice ASSERTS identity and HIP BELIEVES it. Today the member is resolved inside the voice component (`server/voice_orch.py:1441-1455`, argmax over enrolled prints at medium+) and handed to the core as fact. A compromised or spoofed voice component can therefore claim ANY identity, and every gate below it — INJ-1/3/7, care-team permits, owner-scoped retrieval, write authority — will enforce the wrong answer **correctly**. The gates are not bypassed; they are fed a lie. This is the single highest-leverage consequence of REQ_ARCHITECTURE_BOUNDARY §3 ("voice is untrusted by construction"): an untrusted component is currently the sole source of the principal every downstream decision keys on. **BILL'S RULING:** voice asserts, **HIP verifies independently with its own voiceprint**, neither trusted alone. **THE CONTRACT CONSEQUENCE — THIS IS THE URGENT PART:** independent verification requires voice to hand HIP **AUDIO**, not just a name. `turn(text, resolved_speaker)` becomes **`turn(text, asserted_speaker, audio)`**. The voice contract (turn/on_route/register_member/session_end) is being FROZEN IN THE OTHER LANE RIGHT NOW (Voice 21). **If it freezes without an audio channel, this becomes a contract BREAK later instead of a PARAMETER today.** Adding a field to an unfrozen contract is free; changing a frozen one is a renegotiation across two lanes. **CONTAINMENT NOTE:** audio crossing into HIP brings the memory-unsafe-parser problem with it — the exact hazard §3 exists to keep out. Therefore HIP runs **only the embedding model** on the sample, **in its own subprocess**, and **never a full STT stack**. HIP needs a voiceprint comparison, not a transcript; it already has the transcript from the assertion. Scope discipline here is what stops "verify independently" from re-importing the whole voice attack surface. **IMPLEMENTATION SKETCH (scoped, NOT designed — a starting plan, not a decision):** (1) *Where HIP-side voiceprints live* — NOT `~/hip-harness/data/voiceprints` (today's hardcoded absolute path at `harness/speaker_id.py:54`, shared by every process from every checkout, and inside the FROZEN tree). HIP's own prints belong under the core's own custody, ideally the same UID that will own writes, so a compromised voice component cannot read or replace the reference it is being checked against. If voice and HIP share one print store, the second opinion is not independent. (2) *Disagreement policy — FAIL CLOSED TO WHAT?* This is the open question and must be answered before build, not during. The candidate positions, none chosen: **(a) guest/unidentified** — the turn proceeds with NO member context (no personal facts admitted, INJ-7 not applicable); safest, and degrades a spoof into a useless turn rather than a wrong one. **(b) refuse the turn** — safest against a live attacker, worst under a false negative, and the measured separation says false negatives will be common. **(c) proceed as asserted but mark the record** — records the disagreement, enforces nothing; a downgrade of the ruling, listed only so it is explicitly rejected rather than silently adopted. The measurement that must inform this: D-14/TD-127 already has speaker verification at 0.632-0.677 against a 0.50 threshold (backlog #21), and D-82 measured every enrolled cross-speaker cosine ABOVE the 0.50 medium floor, with bill<->sam (0.679) exceeding bill<->bill_scripted (0.669). **A second opinion built on prints that cannot separate the speakers produces disagreements constantly** — so the disagreement policy and the enrollment quality are one decision, not two. (3) *Enrollment path* — HIP needs its own enrollment producing HIP-custodied prints. Open: whether it can re-use audio captured during voice enrollment (cheap, but a shared origin weakens independence) or requires its own capture (stronger, more presenter friction). Also unresolved and inherited: TD-109 (biometric consent-and-retention control) governs any new biometric store, and TD-126's residual — voiceprint deletion still reaches the frozen `hip-harness` checkout — applies to whatever store this creates. **GOVERNING DOC:** REQ_ARCHITECTURE_BOUNDARY §3 (voice untrusted by construction; the contract is a security boundary). That REQ records the ruling; it does NOT authorize this build. | 1, 2 | **UNGOVERNED** — REQ_ARCHITECTURE_BOUNDARY records the ruling and the threat model but authorizes no code (its own §7 says so). A build needs its own REQ, and the disagreement policy in (2) must be Bill's ruling before that REQ can state an acceptance test. | **The audio parameter must be added to the voice contract BEFORE Voice 21 freezes it** — that step is urgent and is NOT blocked on anything else here. The rest is blocked on the disagreement-policy ruling and on enrollment quality (#21 / D-14 / TD-127). | **YES — two rulings needed: the fail-closed target in (2), and whether the audio parameter goes into Voice 21 now.** |

---


**Numbering note (#54, not #51):** items **51, 52, 53 already exist on the `voice-port` branch** (frontier disclosure payload address-only; speaker_isolation rebuild; routing-pane CLASS -> inference_ms). This tree's BACKLOG.md tops out at #50 because the two clones keep separate copies — **TD-137 / item #49, the exact divergence this file is subject to.** #54 was chosen by reading `voice-port`'s BACKLOG.md from the shared object store (the hip-vo working tree was NOT touched — a parallel lane is writing it) so the two lists can merge without a collision. Filed D-85, 2026-08-01.

## MISSING REQ DOCS — proposed, not built

One line each: what's missing, and the one question only Bill can answer to
write it. These are not built. Writing any of them before Bill answers its
question would repeat exactly the mistake this addendum exists to stop.

| Proposed REQ | Question Bill has to answer |
|---|---|
| **REQ_D01** (fail-open classifier default) | Refuse/ask-for-clarification on low confidence — or hold this entirely for the SIA replacement to supersede, so it isn't fixed twice? |
| **REQ_D02** (third-party exemplars) | Patch the current classifier's exemplar set now, or wait on the SIA cutover decision since a replacement could make this throwaway work? |
| **REQ_G0** (runtime fabrication gate, I-06/item 0b) | A closed roster of known-safe reply shapes (cheap, per the risk memo's own framing), or full name/pronoun resolution against `resolved_subjects` (real NLP work) — and does day one need to cover voice, or text only? |
| **REQ_VOICE_CASCADE_CHECKPOINT** (voice-path exit-gate exposure) | Duplicate the D-03/D-18/G0 gates into `realtime_adapter.py` now, or accept voice stays exposed until a shared-checkpoint cascade redesign? |
| **REQ_TD123** (detector value-bleed, prompt hardening) | Five prior patches each broke something else — another prompt-only patch, or a harder rework (e.g. a structured extraction schema)? |
| **REQ_TD101** (dashboard/API auth model) | What's the target auth mechanism — session cookie, bearer token, mTLS — and does it have to hold before the next external demo? |
| **REQ_HEL_PHASE2** (TD-108, `fact.detect`/`value.decrypt`) | Build HEL Phase 2 next, or hold it behind the harness/SIA work currently ahead of it in the queue? |
| **REQ_TD109** (biometric consent build) | Pre-next-demo requirement, or can it wait until TD-127's stand-in is ever replaced by a real vendor? |
| **REQ_TD110** (cross-member write authority) | Fork A (caregiver authority, make it visible) or fork B (cross-subject writes need a second signal)? |
| **REQ_HARNESS_PHASE2_ONWARD** (HarnessPlan Phases 2/4/5/6/7, X-05, Phase-0 residual) | Confirmed still wanted, not abandoned — and if so, which phase gets a REQ written first once D-06/D-07, D-01, G0, and the I-10 decision clear the front of the queue? |
| **REQ_G1_GATE** (I-10/H-06 flake) | Keep hard-zero and fix detection reliability, move G1 to the ratchet, or retry once — and if the ratchet option, are you overriding REQ_HARNESS's own written "G1 must gate at HARD ZERO" constraint? |
| **REQ_SIA_PHASEB_CUTOVER** (risk-memo items 1-6) | Given the memo's own argument that 85.7% agreement-with-incumbent isn't the same as accuracy, what would you actually accept as proof the cutover is safe to ship? |
| **REQ_VOICE_HISTORY_DISCLOSURE_LEDGER** (row 37b, REQ_PROMPT_RECORD_FIDELITY's own explicit non-goal) | REQ_PROMPT_RECORD_FIDELITY's per-turn fact-id check cannot see a fact disclosed in an earlier turn resurfacing in `self._ctx._messages` — closing that needs a session-level ledger of which fact_ids have ever been rendered into history. Build this now alongside REQ_PROMPT_RECORD_FIDELITY, or accept the named gap and defer until the per-turn check ships and this becomes the next-highest-value item? |
| **REQ_PROMPT_COMPLETENESS** (row 50, reverse direction of REQ_PROMPT_RECORD_FIDELITY's subset check) | Narrowed out of REQ_PROMPT_RECORD_FIDELITY's acceptance test 2026-07-27 (Bill: a record-only fact_id is under-disclosure, not a leak, and a different failure class). No dropping path is known today — `voice_orch.py:2572-2573` preserves `fact_id` on its only rewrite. Worth investing in finding/inducing a real drop path now, or hold until a completeness regression is actually observed? |

---

## REMOVED (fixed/closed — checked, not carried)

D-03, D-05, D-13, D-15, D-17, D-18, D-19, D-20, D-22 (all FIXED or RESOLVED,
including D-19 as a side effect of D-22); I-01, I-02, I-03, I-04, I-05
(FIXED); TD-111, TD-112, TD-114, TD-116, TD-117, TD-119, TD-121 (RESOLVED).

I-07 ("G2 near-vacuous, zero forever, no trend signal") is explicitly "NOT
A DEFECT" on file — carried nowhere, no action implied.

One follow-up worth a line even though its parent is fixed: **D-05's
removed confirm/decline invitation** was pulled specifically because D-03
wasn't fixed yet. D-03 *is* fixed now (2026-07-16 1806, after D-05's own
fix landed earlier the same day). Nobody has revisited putting it back.
DEFECT-level (small, reversible UI-text change), no REQ needed, folded
into item #2's build rather than given its own line.

---

## STANDALONE LEDGER REQUIREMENT — consider with the next ledger-specific build
Added 2026-08-10 (HA-31 continuation 5, Bill's filing ruling). **NOT DESIGNED, NOT DECIDED.**

There is no ledger-specific REQ in `docs/requirements/` (144 files; none for HEL or the ledger).
HA-31 recorded Bill's **HEL 1.0 ISOLATION GATE** in `REQ_STRUCTURAL_CEILING` — confirmed as the
right home for now, since that REQ already governs the HEL 2.0 format and is the only one citing
`keyed_commitment` and D-R-163.

**The open question, for the next ledger-specific build to consider — not to be answered here:**
whether the HEL format, its isolation gate, and the R16 commitment contract deserve a requirement
of their own rather than living inside the ceiling REQ. **Do not design or decide it in advance.**
