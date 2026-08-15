# HIP Prior-Art — Candidate Set
Status: **BANKED**
Verification: **UNVERIFIED**
Reconciled-Against: 2026-08-15, HA-98. Nothing in this document has been checked against
the sources; it is banked as supplied so it stops living only in a chat window.

**Purpose:** the candidate prior-art and landscape set for patent counsel's review.

**Path ruling (Bill's, via FABLE, 2026-08-15):** this content is market research and lands in
`docs/research-market/`. `docs/research/` was NOT created — it is not in the LOCKED docs
structure, and adding a folder requires a ruling plus a CLAUDE.md update, not a session's
choice.

---

## SCOPE LIMIT — READ FIRST

Nothing in this document is a legal determination. Whether any reference legally qualifies as
prior art, and its effect under 35 USC 102 or 103, is for counsel. Publication dates here are
recorded facts, not conclusions.

## PRIMARY — element-map these five; claim-chart the patent claims where applicable

1. US20240412720A1 (application, pub 2024-12-12). Household / smart-home multi-user assistant.
   Separate conversation histories and privacy settings per user; one participant grants and
   revokes another's access to specific portions; purpose-and-scope notification;
   ownership/privacy metadata on conversation data. Closest to HIP's multi-principal household
   capability. No deterministic pre-model authorization identified.
2. US12517919B2 (granted 2026-01-06; priority 2022-11-22; pub US20250335458A1). Cryptographic
   memory capsules, embedded access rules, signed memory operations and agent decisions on an
   immutable ledger.
3. Collaborative Memory, Rezazadeh et al., arXiv 2505.18279 (2025-05-23). Multi-user
   private/shared memory, dynamic asymmetric access, immutable provenance, auditable memory
   operations. Write transforms use LLM prompts.
4. Harness-MU, arXiv 2606.21856 (2026-06-20). Deterministic Gatekeeper builds a
   non-probabilistic permission vector BEFORE model invocation; policy code outside the LLM;
   isolated per-principal context; fail-closed post-generation checker.
5. Purpose-Bound Memory Mediation / MaaS, arXiv 2506.22815v2. Item-level decisions over owner,
   requester, recipient, task, purpose and context, with structured withhold / abstract /
   reveal.

## SECONDARY — candidate references published before a 2026-08-15 filing. Legal prior-art effect NOT DETERMINED.

MemArchitect (Mar 2026), GAAP (Apr 2026), AFA (Apr 2026), GateMem (Jun 2026), MemClaw /
Governed Shared Memory (Jun 2026), PiSAs (Jul 2026).

## CONTEXTUAL INTEGRITY — foundation citations

Nissenbaum, Privacy as Contextual Integrity, 79 Wash. L. Rev. 119 (2004). Cited-by 4,489.
Nissenbaum, Privacy in Context, Stanford UP (2010). 6,504.
Barth, Datta, Mitchell & Nissenbaum, IEEE S&P (2006). 697.
Benthall, Gurses & Nissenbaum, FnT Privacy & Security 2(1):1-69 (2017),
  DOI 10.1561/3300000016. 92.
LIMIT: counts are a snapshot taken 2026-08-15 from the search index, NOT read from the Scholar
UI, which was rate-limiting. Provisional, not precise.

---

## PROPOSED CLAIMS-REGISTER ADDITIONS — AWAITING BILL

**THE REGISTER WAS NOT CHANGED BY THIS DISPATCH.** `docs/deliverables/HIP_ClaimsRegister__v20260727_1729.md`
declares a CLOSED status vocabulary, verbatim:

> **STATUS** is PROVEN, DESIGNED, ASPIRATIONAL, WRONG, or UNVERIFIED (one seeded claim keeps
> Bill's own word, DISPUTED, verbatim -- see CLAIM-04).

None of those six means either *"the capability is present in published work"* or *"still
differentiated in the current landscape"* — they grade whether HIP's own asserted claims are
true, not where HIP sits against the field. So the dispatch's second branch applies: **no status
was invented and no existing row was altered.** The rows below are proposals only.

### Proposed status A — capability present in published work

Definition to carry **verbatim**:

> This status means the broad architectural capability is present in published work. It is not a
> legal conclusion regarding patent novelty, anticipation, obviousness, or claim scope.

| proposed row | citing |
|---|---|
| multi-user private/shared AI memory | PRIMARY 1 (US20240412720A1), 3 (Collaborative Memory) |
| model-external deterministic authorization | PRIMARY 4 (Harness-MU) |
| provenance / audit of AI memory | PRIMARY 2 (US12517919B2), 3 (Collaborative Memory) |
| contextual-integrity formalization | CONTEXTUAL INTEGRITY foundation citations (Nissenbaum 2004, 2010; Barth et al. 2006; Benthall et al. 2017) |
| household voice identification | PRIMARY 1 (US20240412720A1) |

### Proposed status B — still differentiated in the current landscape

Definition to carry **verbatim**:

> This status means surviving current landscape differentiation. It is not a determination of
> patentability.

| proposed row | citing |
|---|---|
| a durable record of the exact context supplied to generation plus the reason for that answer or refusal | the SECONDARY set and PRIMARY 2-5, none of which was identified as recording the generation-input context together with the refusal reason |

### OPEN CONTRADICTION — filed as a finding, and VERIFIED against the code

The proposed row above is weakened by the implementation it would describe, and the
contradiction is recorded here rather than resolved by a session.

`harness/epistemic_ledger.py::append()` — docstring, verbatim:

> Append one event, durable before return. NEVER raises toward the caller; failures are
> counted, reported to stderr, and spooled.

**"Durable before return" and "never raises toward the caller" cannot both be load-bearing.**
The handler confirms which one gives way:

```python
except Exception as exc:   # noqa: BLE001 — never fail the turn (spec M-2)
    append_failures += 1
    print(f"HEL APPEND FAILURE #{append_failures} ...", file=sys.stderr)
    try:
        ... spool.failsafe ...
    except Exception:   # noqa: BLE001 — spool is best-effort
        pass
```

A ledger write can fail — and its failsafe spool can fail too — while the turn proceeds and the
governance outcome is **identical with or without the record**. That contradicts the
write-ahead property.

**Consequence, stated plainly:** if a ledger write can fail without changing the governance
outcome, then **"provable knowledge boundary" and "write-ahead evidence" are stronger than the
implementation supports.** Whether the fix is to make the write actually block the turn, or to
weaken the claim to match the code, is Bill's decision — this dispatch changed neither.

---

## PROVENANCE — WHAT THIS DOCUMENT IS AND IS NOT

- **The content above was supplied verbatim by the dispatch** and is banked unaltered. Nothing
  was researched, checked, added or reworded by this session.
- **`docs/research/HIP_LANDSCAPE__2026-08-15.md` DOES NOT EXIST and never did.** HA-98's
  inventory searched the roadmap tree (tracked and untracked) and `main`, `nc-b0`,
  `natural-conversation` and `demo-cutover-build`: zero files with "landscape" in the name, and
  no doc under `docs/` containing GateMem, PiSAs, MemArchitect or Purpose-Bound. **Bill's
  answer: the handoff's banked claim was wrong — the research existed only as chat text.**
- **THE FALSE CLAIM IS NOT IN ANY TRACKED DOCUMENT, so there was nothing in the repo to
  correct.** `docs/HIP_HANDOFF.md`, `docs/LANES.md`, `docs/BACKLOG.md`, `docs/INDEX.md` and
  `docs/deliverables/MANIFEST.md` contain no claim that a landscape doc was banked. The single
  "prior art" hit in `docs/HIP_CHAT_HANDOFF.md:124` is unrelated (progressive profiling in the
  onboarding critique). Recorded here so the next reader does not go looking for a correction
  that has no target.
