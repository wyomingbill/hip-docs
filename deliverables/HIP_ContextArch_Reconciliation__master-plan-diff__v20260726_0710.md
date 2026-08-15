# HIP_ContextArch_Reconciliation — Master-Plan Diff
Status: BUILT (analysis complete; ratifies nothing)
Reconciled-Against: proposal docs/design/HIP_ContextArch_Proposal__context-interaction-intelligence__v20260726_0710.md (filed this dispatch); plan of record LATEST_HIP_Roadmap.md (v20260718_1600 + 07-21 variance notes); REQ_PARTITION_CUSTODY v20260721_0831; REQ_CRYPTO_P3_OPERATOR_BLIND v20260724_1129 (working copy incl. uncommitted OB5 update); REQ_CONFIDENCE_DISCIPLINE v20260721_0945; REQ_WRITE_TIME_CLASSIFIER v20260721_0839; crypto design 47851d7; dyad spec 601ac25; HIP_VoiceArchitecture decision memo v20260714_2030; HIP_Interaction_Layer_Architecture v20260710_1032; code read at working tree on fe1f021 (branch roadmap; tree carries uncommitted OB5 changes to encryption/identity/seal-key files, untouched by this dispatch)

## What this is

The Context & Interaction Intelligence Architecture proposal, reconciled against the ratified HIP design
and the code as it exists. Analysis only. Nothing here is ratified; the CONFLICTS and NEW DECISION rows
are input for Bill. Session: `bill-ai` on `[REDACTED-MACHINE-NAME]`, `[REDACTED-USER-PATH]/hip-roadmap`,
branch `roadmap`.

**Proposal provenance:** the proposal was NOT present on any disk path (repo, `~`, Downloads, Desktop,
Documents all searched); it arrived as pasted text and is filed verbatim this dispatch at
`docs/design/HIP_ContextArch_Proposal__context-interaction-intelligence__v20260726_0710.md` so this diff
can cite it. Section references (§) below are to that file.

**One material code-state note:** the write-time classifier that REQ_WRITE_TIME_CLASSIFIER's own
WHAT'S-KNOWN-BROKEN section describes as unbuilt has since been BUILT — `harness/write_rule.py` is fully
rewritten to the ratified four-scope/four-level model (its docstring says so, and the code matches),
`harness/role_resolution.py`, `harness/compound_split.py`, `harness/standing_policy.py`,
`harness/care_team_keys.py`, and `harness/answer_mode.py` all exist. Reconciliation below is against the
CODE, which is ahead of that REQ's snapshot text.

## Verified-true proposal premises (for confidence in the rest)

- "HIP already uses Bloom's hierarchy as a routing mechanism" (§12) — TRUE. `harness/complexity_features.py:7-10`
  (tier is a hard function of effective Bloom level), consumed by `harness/router.py:757-758`.
- "HIP already distinguishes valid time from record time" (§6.3) — TRUE. `memory_engine/store.py:186-192,221-223`
  (valid_from/valid_to AND recorded_at/record_closed_at; CORRECT inherits valid_from, `store.py:327-340`).
- "Privacy enforcement occurs before context reaches the reasoning model" (§2.4) — TRUE today.
  `harness/injection_contract.py:1-56` — INJ-3 "structural: the DENY happens before fact text reaches the model."
- SUPERSEDE / AUGMENT / CORRECT / UNRESOLVED (§11) — all four exist. `memory_engine/store.py:290-340`,
  `harness/fact_change.py:800-818`.

---

## STEP 2 — THE TABLE

Disposition legend (each row lands in exactly ONE): **AR** = ALREADY RATIFIED · **CE** = CONSISTENT
EXTENSION · **CF** = CONFLICTS · **ND** = NEW DECISION REQUIRED. Where one proposal spans two
dispositions it is split into lettered parts that each land cleanly.

| # | Proposal / subsystem (§) | Disp. | Basis — citation; what it adds; or both sides of the conflict |
|---|---|---|---|
| 1 | P1: Context Manager becomes a named subsystem (§4, §44) | CE | Today the orchestrator IS the context layer, composed inline (`harness/orchestrator.py:1-30`): owner-scoped read + top-5 cosine (`extraction_queue.py:804-879`) → injection contract → prompt. Naming it a subsystem with rank/pack/prune changes nothing built; it formalizes an existing seam. |
| 2 | P2: relevance is dynamic; no stored per-fact relevance score (§2.3, §44) | CE | No relevance/importance field exists on Fact nodes (grep: zero hits); nothing ratified stores one. Compatible as stated. |
| 3 | P2b: store an importance PRIOR and usage history with memory (§6.6, §11) | CE | New additive Fact metadata; nothing conflicts. Any new canonical field goes through the same seed-schema/enum discipline as `vitals`/`care_plan` did (REQ_D21_D23 pattern). |
| 4 | P3: context selection as constrained optimization (§7, §44) | CE | Replaces the flat `top_k=5` cosine cut + `ORDER BY timestamp` (`extraction_queue.py:756,804-879`) and INJ-2 keyword relevance with utility packing. Constraint carried forward: must preserve the ratified attribute-family surfacing rule (REQ_CONFIDENCE_DISCIPLINE, RETRIEVAL-RELEVANCE amendment) — a packer that re-introduces silent drops of authorized true facts re-opens T02. |
| 5 | P4a: governance is a hard gate outside ranking; the learner can never override access policy (§8, §44) | AR | Ratified twice, independently: REQ_CONFIDENCE_DISCIPLINE (Bill verbatim: "Confidence... may never create permission"; policy stages deterministic) and REQ_PARTITION_CUSTODY (level 4: "only deterministic facts... decide who reads it"). Enforced today structurally at `apply_injection_contract` (INJ-1..7 run before any fact text reaches the model). The proposal restates the ratified law. |
| 6 | P4b: the ENFORCEMENT that keeps a *learned* ranker under those gates | ND | The principle is ratified (#5); the machinery is not — see STEP 4. Decision in one line: ratify the three preconditions before any learned ranker ships — (i) G0 built (already ratified mandatory, unbuilt), (ii) a standing OB4-style harness invariant "model prompt facts ⊆ contract-admitted set," (iii) ranker placed so it can only NARROW the authorized candidate set, never source outside it. |
| 7 | P5a: CUV dimensions — task fit, temporal fit, authority, importance, urgency, actionability, dependency, continuity, volatility, redundancy, token cost (§6, §44) | CE | None exist as retrieval signals today (retrieval = cosine + recency + INJ-2 keywords). Two fences from ratified design: (a) redundancy pruning must never collapse rows that share (subject, attribute) but disagree on value — CONFLICT_PRESENTATION depends on both rows being admitted (`harness/answer_mode.py:89-99`); (b) the dependency example (caregiver authorization) is a registry lookup, not a rankable fact — see STEP 3 item S7. |
| 8 | P5b: EPISTEMIC FIT as an inclusion/exclusion ranking dimension (§6.4, §7) | CF | Proposal: "An ASSERTED fact might be entirely appropriate for [gossip] but insufficient for [caregiver medication]... a task-dependent epistemic requirement" — i.e., trust can rank an authorized fact OUT of context. Ratified: REQ_CONFIDENCE_DISCIPLINE — "Uncertain WHETHER-TRUE → hedge, for an already-authorized reader. This is presentation only — it never blocks access to a reader who is otherwise permitted," and the T02 amendment: "authorized + fact-known → surface, never silently refuse." An epistemic-fit ranker that drops the fact reproduces the exact `guard_empty_set`/`admitted: []` silent-refusal class the amendment closed. The ratified home for epistemic fit already exists and is BUILT: it selects the ANSWER MODE (`answer_mode.py:150-157`, ATTRIBUTED_HEDGE vs PLAIN_STATEMENT), not the inclusion set. Adopting §6.4 as written reverses a ratified decision. |
| 9 | P5c: privacy-exposure cost as a packing penalty (§6.12) | CE | Compatible as HANDLING: external-model eligibility is a ratified level-4 sensitivity consumer (REQ_PARTITION_CUSTODY level 4). Fence: it biases packing for an already-authorized reader; it must never become an audience decision — "sensitivity NEVER determines audience by itself." |
| 10 | P6a: routing already conditions on privacy and tool/capability need, not Bloom alone (§12) | AR | Built and ratified: sensitivity blocks off-net escalation (`router.py:699-742`); capability/freshness axes escalate (`router.py:767+`); intent gates (`route()` stage 1); tier = f(bloom) (`complexity_features.py:7-10`). "Bloom determines workload; risk and governance determine reliability" is a restatement of the existing axis structure. |
| 11 | P6b: add consequence-risk, latency budget, cost, model-performance history to routing (§12, §15) | CE | None are routing inputs today — `route()` is pure, stateless, no cost/latency/history signal. Additive. |
| 12 | P7: Interaction Manager as a layer distinct from the Context Manager (§23-24, §44) | CE | Aligns with the interaction-layer doctrine already on record: Layer 0 swappable surface; the "governed interaction operating system" named as standing whitespace (HIP_Interaction_Layer_Architecture §3 Alpha 3, §5); voice-research P3 interaction/thinking split. Nothing built maintains interaction state beyond per-turn voice session handling; no conflict. |
| 13 | P8: lightweight per-household personalization (weights/thresholds), no per-household fine-tunes (§16, §44) | CE | Nothing ratified on personalization. The §40 guards (bounded weights, rollback, versioning, baseline evaluation) match the repo's ratchet culture and should ship with it. |
| 14 | P9a: global learning consumes strategy/features, never household facts (§21, §36-37, §44) | CE | Matches the operator-blind posture (REQ_CRYPTO_P3; crypto design §7) in principle: "Export learning whenever possible, not household memory." Compatible; the concrete mechanism is #15. |
| 15 | P9b: WHAT telemetry actually leaves a household, in what identity form (§20, §37, §45) | ND | Decision: ratify the export unit (de-identified features? gradients? aggregates? federated?) and its identity handling. Existing constraint already on the books: HEL-ACTOR-1 makes registry-level opaque IDs a HARD precondition for the first external household (EPISTEMIC_LEDGER hel-oq2 spec). §20's record carries `household_id` + `speaker_role`; unresolvable without this decision. |
| 16 | P10: context selection becomes TRAINABLE (rules → teacher → learned ranker → household adaptation) (§17, §30, §44) | ND | This puts the system's first probabilistic component inside the retrieval path. Ratified architecture confines probabilistic signals to handling/presentation and keeps policy deterministic; a learned ranker below the gates is PERMITTED by that philosophy but nowhere authorized. Decision: adopt the learned-ranker track (with #6's preconditions), or hold retrieval rule-based (Generation 1-2 only). |
| 17 | P11: counterfactual context ablation; Context Lift; Dead Context Rate (§18, §44) | CE | New offline eval machinery; complements the ratified Phase F truth metrics; no conflict. |
| 18 | P12: voice development decoupled from context validation; text/push-to-talk pilots first (§28, §44) | AR | Plan of record already sequences exactly this: truth+crypto validated on the text harness; Stage 1 voice scope deliberately minimal ("single speaker... Do not build speaker arbitration"); and Bill's own design digest (HIP_DesignDigest__weekly__v20260725_1400, Sequencing): "Validate context and memory with text or push-to-talk first. Delay full-duplex voice until the brain proves itself." |
| 19 | P13a: fast conversational path + slower deliberative path as coordinated services (§26, §44) | CE | The interaction-plus-reasoning split is already HIP doctrine (Interaction_Layer §2 Layer 1: the routing cascade "already implements that split"; voice-research P3). Building it as two concurrent coordinated paths for voice is the extension. |
| 20 | P13b: fast path EMITTING spoken content ("conversational acknowledgments... short simple responses") outside the text checkpoint (§26) | CF | Proposal fast path "handles... backchannel... short simple responses" on its own. Ratified DECIDED (HIP_VoiceArchitecture memo §3, §6): "The cascade architecture (STT → text checkpoint → TTS) is DECIDED... a permanent requirement of the governance architecture"; "The voice path and the typed path share the same governance enforcement. There is no voice-specific disclosure logic." Any fast-path utterance that carries content must traverse the same checkpoint or it is precisely the ungoverned audio path the memo excludes. Resolvable constraint (Bill's to ratify): fast path limited to content-free turn management/backchannels; any content-bearing text passes the checkpoint. |
| 21 | Bitemporal fact graph as CUV substrate (§6.3 premise, §3 diagram) | AR | Built: `store.py:186-192,221-223` (valid/record time), CORRECT inherits valid_from (`:327-340`); P8 write-monotonicity on the trust ladder (`memory_engine/trust.py:27-34`). |
| 22 | As-of-time retrieval ("state valid in March") (§6.3) | CE | Unbuilt: every read path serves current heads only — `WHERE f.valid_to IS NULL` (`extraction_queue.py:750,833`; `store.py:253`). An as-of read API is a genuine addition the bitemporal store already supports structurally. |
| 23 | Memory domains: episodic / semantic / procedural / active-state (§5) | CE | Today: one bitemporal Fact graph + session memory. No procedural store, no active-state ("things underway") store exists. Additive taxonomy. |
| 24 | Context Pack structured object; "why did this fact enter the prompt" (§10) | CE | Substrate partially built: the epistemic record already answers admitted/withheld/deny-reason per turn (d1.1; injection contract deny reasons; `turn_metadata`). The pack object (budgets, uncertainties, prohibited_disclosures, required_citations) is new. |
| 25 | Memory write path flow (§11 flow diagram) | AR | The proposed flow IS the built pipeline: compound splitting (`harness/compound_split.py`) → role resolution (`role_resolution.py`) → four-level precedence (`write_rule.py:125-231`) → trust assignment (`trust.py:81-93`) → temporal + SUPERSEDE/AUGMENT/CORRECT/UNRESOLVED (`store.py:290-340`) → class-sealed commit (`store.py:418-490`). Restates REQ_PARTITION_CUSTODY + REQ_WRITE_TIME_CLASSIFIER, now built. |
| 26 | New write-time metadata: volatility class, source-authority class, retrieval/usefulness counters, correction history (§11) | CE | No such fields exist. Additive; same fence as #3. |
| 27 | Model roles, not model brands (§14) | CE | Role abstraction is new packaging; two constituents are already ratified law: the policy/classification model "does not have final authority over access control" (= level-4 sensitivity handling-only), and frontier use is permission-gated (escalation + disclosure contract + sensitivity block). "Verification model" slot overlaps ratified-but-unbuilt G0 — note G0 is specified as deterministic CODE, not a model; a model may assist it, never replace it. |
| 28 | Model router: deterministic-first ladder + selection over quality/cost/availability/history (§15) | CE | The ladder's spine exists: deterministic short-circuit before any model (`temporal.py:123-142` local clock answers), then edge/mid/core/escalate tiers. Selection over workload/history/quality metrics is new. |
| 29 | Feedback: silence is not positive reinforcement; corrections weigh most (§19) | AR | Already the built behavior: `harness/satisfaction.py:77-87` — positive ONLY on explicit cues; empty/ambiguous → neutral; corrections → negative. See STEP 3 item S6: the proposal "tightens" an assumption the code never held. |
| 30 | Feedback: the wider weak-signal taxonomy (abandonment, latency, repeated request, manual search) (§19) | CE | None of these are captured today (`satisfaction.py` is regex over the next utterance). Additive instrumentation. |
| 31 | Training data record retained per interaction (§20) | ND | As specified it retains `response`, `user_correction`, `context_scores` + `household_id` in a store outside member sealing — collides with operator-blind-at-rest unless the record is member-sealed the way HEL events are (HEL Phase 2: detect events encrypted under owner key; decrypt-event exposure metadata "never plaintext") and opaque-ID'd (HEL-ACTOR-1). Decision: ratify the training record's crypto class, retention, and identity form before any telemetry ships. |
| 32 | Deployment hierarchy: household / edge site (shared models + meta-policy) / operator core / frontier (§41) | CE | Fits the operator-edge sovereignty doctrine (Interaction_Layer §4). The edge-site shared-model tier and "one meta-policy, many sites" are new; nothing conflicts provided household keys/personalization stay household-resident as drawn. |
| 33 | Household testing scale: 10-20 → 50-100 → 200-500 → 1000+ as engineering gates (§22) | CE | No ratified counts exist; digest says "Tens, then hundreds. Depth over raw household count." The proposal's gates elaborate the same posture. |
| 34 | Interaction state object (active/identified/probable speakers, floor, privacy mode...) (§24) | CE | Nothing like it is built. HARD fence carried from ratified law: "identified/probable speakers" may drive turn-taking and modality ONLY. Identity for ACCESS is device-key possession; voiceprint is a hint (plan of record: "Identity is device binding... Voiceprint stays a hint (TD-127)"; REQ_CONFIDENCE_DISCIPLINE voice rules; built demotion at `voice_orch.py:1405-1471`). |
| 35 | Modes 3-5: audience determination from audio for shared-room disclosure ("whether the response can be public") (§24 privacy mode, §27) | ND | Nothing ratified defines what counts as reliable evidence of WHO IS PRESENT for a shared-surface disclosure. Ratified identity proves device possession — bystanders have no device to prove; ratified fallback for uncertain-WHO is withhold + step-up. Decision: ratify a presence/audience evidence standard and a default (e.g., shared surfaces emit household-circle-audience content only) before Mode 3+ work starts. |
| 36 | Interaction-mode ladder 0-5 (§27) | CE | Modes 0-1 are the current state (text query path; controlled-voice demo). The ladder as a maturity model is new and consistent with #18. |
| 37 | Proactive intelligence + proactive utility function (§31) | ND | HIP initiating turns is a NEW governance surface: disclosure without a query, interruption cost, never-proactive categories. Nothing ratified covers it; the proposal itself lists the thresholds as open (§45). Decision: authorize a proactive track at all, and if so its hard gates (opt-in categories, interruption floor, audience rules — composes with #35). |
| 38 | Learning interaction preferences (delivery mode per member) (§32) | CE | Lightweight policy learning over delivery preferences; no conflict; subject to #13's drift guards. |
| 39 | Eval: Authorization Violation Rate = 0, Disclosure Violation Rate = 0 (§33) | AR | This is the ratified hard-zero class: G0/G1/G4 never baselinable, `--accept` refused (REQ_CONFIDENCE_DISCIPLINE Phase G); layer-7 N-invariants + mandatory fault injection (REQ_CRYPTO_HARNESS discipline). Restatement. |
| 40 | Eval: context-quality metrics — precision/recall/lift/dead-token/stale-rate/temporal accuracy/correction retention/continuity (§33) | CE | New metric family alongside the ratified seven truth metrics (Phase F). Additive. |
| 41 | Context Regret (oracle-relative context quality) (§34) | CE | Adjacent to, NOT the same as, the ratified oracle-agreement-rate metric (Phase F #4, opposite-polarity ratchet). Adopting regret must not displace that metric or its ratchet direction. |
| 42 | Observability of every context decision (candidates/rejected/selected/scores) (§35) | CE | Substrate built: d1.1 epistemic record + HEL spec already log admitted/withheld/guard/deny-reason. Candidate counts and per-candidate utility scores exist nowhere — new. |
| 43 | Context poisoning: conversational input must never modify ranking rules, authority, or precedence (§39) | AR | Ratified and largely built: standing policy is deterministic policy objects, "NOT free-text the model may weigh" (REQ_PARTITION_CUSTODY level 1); authority/membership/custody changes are quorum-gated, ledger-recorded governed operations (#6 custody governance; built via `harness/quorum.py`/`custody_exit.py`, REQ_CRYPTO_P4 MET); injection contract + MT1 metamorphic-invariance decode (`injection_contract.py:56-77`). The proposal extends the same philosophy to a learner — the extension rides on #6/#16. |
| 44 | Personalization drift guards: bounded weights, decay, rollback, versioning, protected priors (§40) | CE | Required companion to #13/#16; matches ratchet/baseline culture; nothing conflicts. |
| 45 | OpenRouter / model gateways as dev convenience, not core architecture (§42) | CE | Consistent as stated — the proposal itself confines gateways to development, matching the digest ("OpenRouter is a good dev start... Direct contracts later"). Fence from ratified law: governed-core on-net inference runs in the operator enclave (`router.py` doctrine; trust-boundary DECIDED in the voice memo) — a gateway may only ever sit on the already-governed, consent-gated escalation path or in dev. |
| 46 | Development sequence Phases A-G (§43) | ND | A second sequencing authority alongside the plan of record, which is explicit: do not start new build ahead of the ratified sequence. Stage 4 P3 part (c) steps 2-5 are open (master key not destroyed); Stage 5 (REQ_CONFIDENCE_DISCIPLINE) is NOT MET. Decision: where Phase A ("instrument the brain") slots relative to those — after Stage 5, interleaved, or superseding. This diff does not propose an answer. |
| 47 | External context sources: calendar, portal, devices, weather, web (§5) | CE | Today only web-freshness escalation exists (SerpAPI path, consent-gated off-net). Calendar/portal/device integrations are new, each entering through the same authorized-escalation pattern. |
| 48 | Synthetic household simulation corpus before scale (§38) | CE | Harness fixture/probe-set culture extended to simulated longitudinal households; evaluation target (correct historical state) matches the bitemporal design. Additive. |
| 49 | Hard-gates list: authorization, custody state, scope, consent, revocation, audience policy, model locality, handling rules (§8) | AR | Every named gate is an existing deterministic mechanism: INJ-1..7; custody/quorum (P4 MET); four scopes as key-wrap rosters; tiered consent (#6); epoch rotation on removal; sensitivity→handling incl. external-model eligibility; in-boundary locality (voice memo DECIDED). Restatement of the ratified inventory. |
| 50 | Response/Policy Verification stage (§3 diagram; §2.4 "Disclosure Check") | AR | This box IS ratified G0 (REQ_CONFIDENCE_DISCIPLINE: mandatory output-side invariant, "hard-fail regardless of what any upstream stage believed") — ratified, NOT built (see STEP 3 item S4 and STEP 4). The proposal restates the ratified decision; it does not add to it. |

**Column counts: ALREADY RATIFIED 10 · CONSISTENT EXTENSION 31 · CONFLICTS 2 · NEW DECISION REQUIRED 7. (50 rows.)**

---

## STEP 3 — FALSE OR STALE ASSERTIONS ABOUT CURRENT HIP BEHAVIOR

The proposal describes the system wrong in seven places. Each with evidence from the code/docs read.

- **S1 — §9 names the scope "HOUSEHOLD-SHARED." STALE.** Renamed HOUSEHOLD-CIRCLE-SHARED, ratified
  2026-07-21 precisely so the name self-documents "roster, not label" (REQ_PARTITION_CUSTODY, partition
  section). Code: `harness/write_rule.py:74` — `CLASS_HOUSEHOLD = "household-circle-shared"`. Any adopted
  Context Manager doc must use the ratified name; the old one is retired vocabulary.
- **S2 — §9 names precedence level 1 "recipient standing policy." STALE.** Generalized to OWNER's
  standing policy 2026-07-21 (REQ_PARTITION_CUSTODY, "The write rule" level 1: "generalized... was
  'recipient's'"). Code: `harness/write_rule.py:150-151` (`resolve_owner` → `standing_policy`),
  `harness/role_resolution.py:81-91`.
- **S3 — §9 lists CUSTODIAN as a fifth per-fact role retrieval must preserve. MISCHARACTERIZED.** The
  ratified per-clause role set is four: AUTHOR / SUBJECT / OWNER / BENEFICIARY (REQ_PARTITION_CUSTODY
  role separation #3; `harness/role_resolution.py`). CUSTODIAN is a custody-governance role (who holds a
  dyad key on a recipient's behalf — dyad spec §1.2, custody policy #6), not a field the write or read
  path resolves per fact.
- **S4 — §3 diagram / §2.4 sequence shows a live "Response / Policy Verification" (Disclosure Check)
  stage after reasoning. FALSE as current behavior.** G0 does not exist in code: grep of `harness/`,
  `eval/harnesslib/`, `server/` for a G0 implementation returns nothing; REQ_CONFIDENCE_DISCIPLINE's
  WHAT'S-KNOWN-BROKEN ("G0 does not exist... the single highest-leverage gap") is still accurate against
  the tree. The only post-generation control today is the hand-built D-05/G4 park template
  (`server/voice_orch.py:2343-2364` per that REQ's own citation). All governance today is INPUT-side.
- **S5 — §6.3 "Context retrieval must understand that distinction" (valid vs record time), with the
  what-was-true-in-March example. STALE against the read path.** The store is bitemporal, but every
  retrieval path serves current heads only: `WHERE f.valid_to IS NULL` at `extraction_queue.py:750`
  (read_user_facts), `:833` (embedding search), `store.py:253`. No as-of-time read exists anywhere; the
  March query cannot be served today (table row 22 is the extension that would).
- **S6 — §19 "One earlier assumption should be tightened: silence should not automatically be treated as
  positive reinforcement." STALE as a correction.** The built classifier never held that assumption:
  `harness/satisfaction.py:77-87` — empty or no-signal input returns "neutral"; positive requires
  explicit cues. There is nothing to tighten; the code already implements the proposed rule.
- **S7 — §29 "It may retrieve the authorization fact solely for internal policy evaluation." 
  MISCHARACTERIZED.** Caregiver authorization is not a fact/memory retrieved into context; it is an
  enrollment-registry lookup the gates consult directly — read path: `injection_contract.py` INJ-3 via
  `care_team_keys.is_active_caregiver` (the one 2026-07-21 addition, per the module docstring); write
  path: `write_rule.py:174,200-217` (`care_team_keys` / `dyad_registry`). A Context Manager must NOT
  model enrollment as rankable context — a ranker that can down-rank an authorization input is exactly
  what proposal §8 itself forbids.

One integration imprecision worth naming here because it feeds STEP 4: §9 "The Context Manager should
receive already-authorized candidate facts." In today's dataflow, candidates are owner-scoped at the
Cypher layer, but FULL authorization (INJ-1..7) runs AFTER retrieval-and-ranking, immediately before the
model (`orchestrator.py:254-261` retrieve → `:517-524` resolve subjects + injection contract). The
"already-authorized candidates" the proposal assumes exist only after the contract runs. Placement of a
future ranker relative to that contract is therefore a design commitment, not a given.

---

## STEP 4 — GOVERNANCE: DOES THE LEARNER-NEVER-OVERRIDES-AUTHORIZATION SEPARATION ACTUALLY HOLD?

**The ratified law is unambiguous, twice over.** REQ_CONFIDENCE_DISCIPLINE (Bill verbatim: confidence
"may never create permission"; policy stages — identity, authorization, scope, retrieval enforcement,
key ops — deterministic, no confidence input) and REQ_PARTITION_CUSTODY (audience decided only by
deterministic facts; the one probabilistic signal, sensitivity, confined to handling). The proposal's
Proposal 4 and §8 restate this law; they do not change it.

**What the code enforces today — separation holds, BY DATAFLOW.** The two ranking-like components that
exist (top-5 cosine at `extraction_queue.py:804-879`; INJ-2 keyword relevance) cannot widen access, for
two structural reasons read from code: (1) the candidate pool is owner-scoped in Cypher before any
ranking sees it; (2) the deterministic contract (INJ-1..7) runs downstream of ranking on every
candidate, before any fact text reaches the model, and the orchestrator feeds the model exclusively from
`injection.allowed` (`orchestrator.py:517-524`; `injection_contract.py` header: INJ-3 "structural").
At rest, class-sealing makes wrong-party reads a crypto failure, not a filter failure (`store.py:418-490`
→ `seal_by_class`; PS1/PS2 + OB4 standing invariants green per REQ_CRYPTO_P2/P3 evidence). Answer-mode
is deterministic code before generation (`answer_mode.py`). So today: yes, governance is a hard gate
outside ranking, and no learner exists to test it.

**But the separation is a dataflow fact, not a machine-checked property — and adopting a learned ranker
requires enforcement that DOES NOT EXIST YET.** Three gaps, highest stakes first:

1. **G0 is ratified mandatory and unbuilt (S4).** It is the only check that would catch a
   ranker-induced (or any upstream) leak at the reply boundary, independent of every stage that
   misbehaved. The ratified text already says it exists precisely because upstream fixes are not
   individually guaranteed. A learned component upstream RAISES the value of the output backstop; today
   there is none. G0 should be a hard precondition to any Generation-3+ context manager.
2. **No standing invariant asserts "model prompt facts ⊆ contract-admitted set."** Today this is true by
   code shape, and nothing would go red if a refactor fed ranker output (or a new "context pack") to the
   prompt directly, bypassing the contract. The repo already invented the exact pattern needed:
   OB4/OB5 — a structural property wired into layer-7 so it re-proves itself on every `--full`, with
   fault injection. The read/prompt path has no equivalent invariant. Without it, the Context Manager
   build could silently move the model's input upstream of authorization and no harness would notice.
3. **Training-signal isolation exists nowhere.** The proposal's own rule — "The learning system must
   never be permitted to optimize authorization policy" (§8) — has no mechanism: nothing yet guarantees
   a learner's reward is computed only on post-gate outcomes, that gate decisions are excluded from its
   feature/gradient space, or that household personalization weights cannot reach gate inputs. Also
   unresolved on the same axis: the §20 training record (row 31) would persist decrypted content and
   `household_id` outside member sealing — colliding with operator-blind-at-rest and HEL-ACTOR-1 unless
   sealed and opaque-ID'd.

**One inherited weakness a learner would compound:** intent still fails open — below-threshold and
embed-failure both return `("knowledge", ...)` (`intent_classifier.py:197,210-211` — verified this
session, unchanged since the REQ's trace), and the `UNCERTAIN`/`AMBIGUOUS` typed states remain unbuilt
(`answer_mode.py` docstring discloses both). A learned ranker feeding a path that fails open inherits
its risk; REQ_CONFIDENCE_DISCIPLINE's acceptance tests 1-2 are prior work in any sequencing decision
(row 46).

**Bottom line for Bill:** the proposal's governance claims are ratified law and are true of today's
dataflow; they are NOT yet enforced as standing, fault-injected properties. Adopting the learned Context
Manager is safe only behind three builds: G0 (ratified, unbuilt), a prompt⊆admitted layer-7 invariant
(no REQ exists — needs one), and learner/training isolation (no REQ exists — needs one). That is the
substance of table rows 6, 16, and 31.

---

## What this diff does NOT do

It ratifies nothing, sequences nothing, and builds nothing. The 2 CONFLICTS and 7 NEW DECISION rows are
Bill's queue. Per Requirements Discipline, any build that follows starts from a REQ naming this doc and
the proposal, not from this doc alone.
