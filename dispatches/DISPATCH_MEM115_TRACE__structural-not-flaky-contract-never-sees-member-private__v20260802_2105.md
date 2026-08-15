# DISPATCH_MEM115_TRACE
Status: BUILT
Reconciled-Against: 2026-08-02 (D-110; parent a14d5da at dispatch time)

**TYPE:** ANALYSIS

**REQ:** **NONE** — trace-and-file dispatch; no production or harness code
changed (D-110's own instruction: "Change no code beyond the register and
docs"). Filed as TD-146 in `DEBT_REGISTER__v20260802_2105.md`.

## THE ASK

> 1. MEM-115 is the odd one in the pinned subset. D-109 found
>    denied_count=0 in ALL THREE runs — it does not flip with the
>    environment the way 116/117/118 do. That makes it a consistent
>    structural gap, not a flaky one, and it has no TD of its own.
> 2. TRACE IT. Report:
>    a. What MEM-115 asserts, and which assertion fails.
>    b. Why denied_count is 0 — is nothing being denied, or is the count
>       not being recorded? Those are different defects.
>    c. Whether the thing it tests still exists in the same shape, or
>       whether the scenario is stale against later work the way MEM-116
>       turned out to be.
>    d. Whether this is a real governance gap or a harness artifact. Say
>       which, with evidence.
> 3. FILE IT AS A TD either way, with the cause traced. If it is a real
>    governance gap, say what is not being denied that should be. Do NOT
>    fix it — scope it.
> 4. Change no code beyond the register and docs.

## WHAT WAS DONE

Read-only trace: `_run_mem_115` (eval/memory_harness.py:1402-1573),
`memory_engine/recall.py` in full (the cold Cypher, the caller-scoped
decrypt loop, the contract call, the audit writer), and
`harness/partition_crypto.py`'s member-private write path; then the
mechanism was confirmed against D-107 run 2's CAPTURED log (on disk in
the session scratchpad) rather than re-run — the memory harness writes
memtest facts and this dispatch changes nothing. TD-146 filed; the
D-109 baseline Note gained an addendum the trace makes necessary.

## WHAT WAS FOUND

**(a) What it asserts, and what fails.** Sub-case (a) — same-owner cold
recall allowed, audited, and excluded from candidate_facts — PASSES in
full. Sub-case (b) seeds a member-private cold fact for `memtest-115a-*`
and recalls it as `memtest-115b-*`. Its disclosure assertions PASS
(`:1542` the fact is absent from results; `:1555` allowed_fact_ids is
empty). **The single failing assertion is `:1551`:
`denied_count > 0`** — the audit records `denied_count=0`.

**(b) Why denied_count is 0 — a THIRD answer, not either offered one.**
Not "nothing fetched from the graph": the cold Cypher
(`recall.py:67-89`) is subject-scoped with no requester filter, and
D-107 run 2's captured log shows it returned BOTH cold rows — exactly
two `recall_from_cold: decrypt failed for <fid>
(FileNotFoundError(2, ...)) — skipping` warnings, and zero
"Neo4j query failed" lines. Not "count not recorded": the count is
recorded faithfully. The rows are dropped BETWEEN fetch and contract, at
Step 2's caller-scoped decrypt (`recall.py:228-236`,
`caller_member_id=requester` — REQ_CRYPTO_P2, named by the comment at
`:226-227`). With every row dropped, `facts` is empty, Step 3's
`apply_injection_contract` call (`:260-267`) never executes, and
`denied_count=0` (`:270-272`) is the honest record of a contract that
was never consulted. The requester cannot decrypt structurally:
member-private DEKs seal to the AUTHOR's keypair, auto-provisioned at
write (`partition_crypto.py:102-112`); `memtest-115b-*` never wrote
anything, so it has no key file at all (hence FileNotFoundError), and
even an enrolled requester's key could not unwrap another member's
member-private DEK — which is the design, asserted as PASSING product
behavior by L7's cross-member decrypt checks ("cross-member decrypt
count == 0").

**(c) Stale, same class as MEM-116.** The scenario predates
REQ_CRYPTO_P2_PARTITION_SEALED: written when a fetched fact decrypted
for any caller (v1 master-key era) and the injection contract (INJ-3)
was the layer that denied cross-member access — `denied_count > 0` was
then observable. P2 moved cross-member denial for member-private facts
DOWN into the crypto. With TD-145, this completes the pattern: **both
persistent memory-harness reds are crypto-era scenario staleness, not
product regressions.**

**(d) Verdict: HARNESS ARTIFACT — with one small, real,
audit-fidelity gap attached (named per the ask).** Not a disclosure
gap: nothing is disclosed, and the structural crypto denial is STRONGER
than the contract denial the scenario expected to observe. The contract
still governs this path for any fact class a requester CAN decrypt
(household-shared to a circle member, dyad-private to a co-custodian) —
§6 invariant 1 holds; MEM-115(b) just tests it with the one class the
contract can never see. **The real gap:** the recall audit cannot
distinguish "attempted, and structurally unreadable" from "no cold
facts exist" — both write `cold_fact_ids_fetched=[], allowed=[],
denied_count=0`; the decrypt-skip is a log.warning only, recorded in no
audit field (`:94-121`). On the one path built for deliberate,
member-initiated recall (pipeline-uncalled by design, `:181-183`),
that is an observability gap worth its TD line, not a disclosure.

**TD-146 (OPS) filed, scoped not fixed.** Two verification shapes
named: (a) exercise the contract with a decryptable class (both memtest
identities in a household circle + a household-shared cold fact, or a
shared-custody dyad) so INJ-3/INJ-7 actually fires and
`denied_count > 0` is real; (b) for the member-private case, add an
`undecryptable_count` (or skipped-ids list) to `_append_recall_audit`
and assert THAT — an audit schema change plus harness change together,
deliberately not done here.

**Consequence for D-109's pin, recorded as an addendum to its register
Note:** the 13-15/17 ceiling is STRUCTURAL — MEM-115(b) can never pass
under the current architecture, and MEM-116 is effectively
permanent-red too (TD-145's MasterKeyMissingError fires precisely when
its environmental mode does not). The live variation axis is only
{MEM-117, MEM-118}; 15/17 is the attainable maximum; a 16/17 run today
would correctly STOP, because it would mean a structural impossibility
passed. Either TD's fix must update the pin in the same dispatch.

## VERIFIED

- **Watched run:** none this dispatch (deliberately — read-only). The
  load-bearing observation is from D-107 run 2's captured log, on disk:
  two decrypt-skip warnings with FileNotFoundError, zero Neo4j-failure
  lines, and the audit line with `fetched=[], denied_count=0` from the
  same run. All file:line citations re-read from live source this
  session.
- **Reasoned about:** that an ENROLLED cross-member requester would
  fail the same way (LookupError instead of FileNotFoundError) — from
  the sealing design and L7's cross-member checks, not from a live
  probe with enrolled memtest identities.

## HASH

Committed this session on `roadmap` (D-110); parent a14d5da.

## OPEN

- TD-146's fix (shape a, b, or both) — its dispatch must update D-109's
  baseline pin the same day.
- Whether the audit's undecryptable-attempt blindness deserves
  escalation beyond OPS if `recall_from_cold` ever gains a real
  pipeline caller — today it has none, by design.
- MEM-117/118 remain the only genuinely environmental members of the
  pinned four; if either goes persistent, it gets this same treatment.
