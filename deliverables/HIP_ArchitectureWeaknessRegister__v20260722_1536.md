# HIP Architecture Weakness Register
Status: LIVE (running register, new entries appended with an ID — same
convention as `docs/techdebt/DEBT_REGISTER` and `docs/BACKLOG.md`. Resolved
entries are marked RESOLVED with the commit that closed them, never
deleted. When this file changes materially, cut a new timestamped version
and repoint `LATEST_HIP_ArchitectureWeaknessRegister.md`.)
Reconciled-Against: main 4390240

**PORTED TO ROADMAP, 2026-07-27 (DISPATCH 35, per Bill's ruling that
roadmap's numbering is authoritative):** this file did not previously
exist on `roadmap` — it was `main`-only. Content below (AW-01 through
AW-05, the column legend, the closing demo-relevance note) is ported
**unchanged** from `main` commit `4390240`'s version of this file; no
finding, wording, or verdict was altered. Only the cross-reference
paragraph immediately below was updated, because it named `TD-131` and
commit `4390240` by `main`'s numbering, and `main`'s `TD-131` collides
with an unrelated, pre-existing `TD-131` already on `roadmap` (a
git-worktree-checkout finding). See `HIP_RegisterReconciliation__cross-branch-id-collisions__v20260727_1930.md`
for the full audit and renumbering map this port executes against.

Cross-reference: **`TD-136`** (`docs/techdebt/LATEST_DEBT.md`) and the
run-of-show correction at `9e61641` are related but distinct. **`TD-136`
is main's `TD-131` (commit `4390240`), renumbered on port per the
reconciliation plan — `roadmap`'s own `TD-131` is a different, unrelated
finding (a git-worktree-checkout gap) and was not touched or renumbered.**
TD-136 is content this codebase deliberately sends to an external provider
today (household facts, in the MID/CORE payload, by design). This register's
entries concern an attacker inferring content that was never intended for
them, via shared inference infrastructure — a different mechanism, a
different register. **UPDATE 2026-07-27 (DISPATCH 36, phase 2): TD-136 is
now filed for real in `docs/techdebt/DEBT_REGISTER__v20260727_1935.md`
(`docs/techdebt/LATEST_DEBT.md` repointed there) — this cross-reference is
a real entry, not a forward reference, as of this dispatch. `D-28`
(`HIP_DefectRegister`) remains cross-referenced there as a related but
distinct finding in the same call path (`strip_context_for_tier`'s
section-coverage gap, not the MID/CORE tier-gating question TD-136
raises) — D-28 was fixed for its own specific shape under
`REQ_STRIP_CONTEXT_COMPLETENESS`; TD-136's broader MID/CORE question
remains OPEN, Bill's decision required, untouched by that fix.**

**UPDATE 2026-07-27 (DISPATCH 38): `AW-06` added — detection signatures
for KV-cache prompt extraction (the five usage signals, specified in
full, detailing AW-05's layer-three defense). Not a correction to any
prior entry; AW-01 through AW-05 are unchanged. This closes
`HIP_ArchitectureForDiligence`'s Open Question 1 (the AW-06
naming-discrepancy two other documents referenced but this register
never defined) — that document's own citations of `AW-06` now resolve to
a real entry.**

## Column legend

ID (`AW-nn`), Source, Mechanism, Applicability to HIP, Proposed Resolution,
Status, Demo-relevant or roadmap-only.

---

| ID | Source | Mechanism | Applicability to HIP | Proposed Resolution | Status | Demo-relevant or roadmap-only |
|---|---|---|---|---|---|---|
| AW-01 | Wu et al., "I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving," NDSS 2025 (PROMPTPEEK) | KV cache sharing plus Longest Prefix Match scheduling creates a return-order side channel. A local model with the same tokenizer generates candidate tokens; the side channel confirms matches, reconstructing another tenant's prompt token by token. | HIGH. The paper names colocation as the main real-world obstacle; an operator hub serving one neighborhood off one or two cards guarantees colocation. The paper measured the attack works better on an underloaded GPU, which an edge hub is by design. Amplifier: every household shares the same system-prompt template (`orch.local_system_prompt`, `voice_orch.py:2603`) — the paper's cloze-style input-extraction case, its cheapest and highest-success scenario at 99%. An adversary household knows the boilerplate and starts guessing at the first divergent token: the neighbor's address. | Per-household cache scoping — a tenant identifier in the cache key, block matching restricted to same-tenant blocks. Cost is small: the shared prefix is roughly 20-30 tokens of boilerplate before values diverge; intra-household reuse is unaffected. Not default in vLLM or SGLang. Residual: member-vs-member inside one household still shares a namespace. | OPEN | Roadmap-only. Specify before build. |
| AW-02 | Same threat class as AW-01 (shared multi-tenant inference infrastructure) — general shared-silicon risk surface, not one cited paper. | Attention masking defects in packed batches; shared logs and crash dumps; error paths echoing prompt content; timing and contention side channels; availability contention. | Household-crossing is a legal category above member-crossing for a cable operator, under 47 USC 551. | Not yet specified. Flagged as a risk surface, not yet scoped to a fix. | OPEN | Roadmap-only. |
| AW-03 | Internal gap analysis, following from AW-01/AW-02 — no external citation; this is HIP's own current detection posture. | There is no taint tracking. A cross-household fragment appearing in a reply has nothing watching for it, and unlike a refusal failure, it produces no visible symptom. | Direct. Any of AW-01/AW-02 succeeding today would be silent — nothing in the current harness or runtime would notice. | Cross-household contamination gets its own hard-zero invariant class in the crypto harness, with per-household canary facts, separate from member isolation. | OPEN | Roadmap-only. |
| AW-04 | General confidential-computing literature and vendor claims — not one cited paper. | Confidential Compute (CC) encrypts GPU memory against the host, giving operator-blind at inference. With one model instance serving many tenants, all tenants sit inside the same enclave — CC protects them collectively from the host, not from each other. Cryptographic tenant separation at inference requires per-tenant model instances (dedicated silicon), giving up the utilization that makes shared serving economic. | Direct. Bears on any claim that "confidential compute" alone solves tenant separation at a shared-serving operator hub. | None. State the limit plainly rather than propose a fix that doesn't exist at the current economics. | ACCEPTED LIMIT | Roadmap-only. |
| AW-05 | Wu et al., NDSS 2025 (same paper as AW-01) — this entry is its usage-signal detail. | Five signals: volume (the paper's user model is 40 requests per 3 hours; one extraction costs 1500-4800 requests); `max_tokens=1` on candidate and dummy requests; candidate fan-out (N requests sharing a prefix, differing only in the final token, sent together); dummy batches sized to exceed max batch size; the inverse cache-flush pattern (unique leading tokens, maximum output length, sent to force LRU eviction). | Layered defense order, three layers. Layer 1, structural: households do not hold raw inference API access — they speak to the assistant, and HIP's orchestrator builds the prompt and sets parameters, which breaks the paper's Condition 3 architecturally. This is a boundary, not a wall: anything reaching the orchestrator's inference client regains that control. Layer 2: per-household cache scoping (AW-01's proposed resolution). Layer 3: rate limiting plus the five signals above. | Implement layer-3 detection (the five signals) as defense-in-depth behind layers 1 and 2. | PROPOSED | Roadmap-only. |
| AW-06 | Wu et al., NDSS 2025 (same paper as AW-01/AW-05) — detection signatures for KV-cache prompt extraction, richer than volume alone, specifying AW-05's layer-three defense in full. | Five signatures. (1) VOLUME: the source paper's own user model is 40 requests per 3 hours per user; an extraction needs 1500 to 4800 requests per prompt, two to three orders of magnitude above household norms. (2) `max_tokens=1`: the attacker sets output length to one token on candidate and dummy requests to minimize memory strain — a household query always wants a full answer, so a stream of single-token-output requests is diagnostic. (3) CANDIDATE FAN-OUT: N requests sharing an identical prefix, differing only in the final token, submitted close together — the token-extraction primitive's fingerprint, nearly impossible to produce accidentally. (4) DUMMY BATCHES: repeated batches of identical prompts, sized to exceed max batch size, interleaved before and after the fan-out. (5) CACHE-FLUSH PATTERN: the inverse signature — requests with unique leading tokens and maximum output length, sent to saturate memory and force LRU eviction between extraction rounds. | Roadmap only, target multi-tenant architecture, consistent with AW-01 through AW-05. | The structural answer outranks rate limiting, in this order of precedence. The source paper's third attack condition is that clients hold extensive control over request parameters and unrestricted dispatch. In HIP's architecture, households do not hold raw inference API access; they speak to the assistant, and the orchestrator constructs the prompt and sets the parameters. That breaks the condition architecturally, not by monitoring. Caveat stated plainly: this is a boundary, not a wall — anything reaching the orchestrator's inference client, a compromised edge process or a scripted device, regains that control, which is why the five signatures above remain worth having as defense in depth. | SPECIFIED, NOT BUILT | Roadmap-only. |

---

No entry in this register is demo-relevant today. All six concern the
target multi-tenant operator-hub architecture; the current demo runs one
household on one box, so none of these mechanisms apply to what a live demo
shows. That is a statement about today's demo scope, not a statement that
these weaknesses are minor.
