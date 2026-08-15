# DISPATCH_MEM_BASELINE_REPIN
Status: BUILT
Reconciled-Against: 2026-08-02 (D-109; parent 8ab4dec at dispatch time)

**TYPE:** PROCESS

**REQ:** **NONE** — register-only filing. No production or harness code
changed (D-109's own instruction: "Change no code beyond the register and
the TD"). The evidence base is D-108's read-only trace, itself printed to
the terminal per instruction rather than filed; this dispatch is where
those findings become durable.

## THE ASK

> 1. RE-PIN THE MEMORY-HARNESS BASELINE. It is currently pinned "13/17,
>    the same four." D-108 proved the four are environmental and that two
>    of them pass when the Groq model emits the supersede. Re-pin as:
>    "13-15/17, failures a subset of {MEM-115, 116, 117, 118}." Record
>    D-108's four grounds in one line each, so the next reader does not
>    re-derive them. A run outside that range is still a STOP.
> 2. FILE MEM-116's STALENESS AS A TD. Its verification code is stale
>    against the operator-blind work: REQ_CRYPTO_P3 decoupled roadmap's
>    key, and L7's OB6 asserts that no master key file exists on roadmap
>    as the CORRECT destroyed state. So MEM-116 can red for a structural
>    reason even when the path it tests succeeds. That is a false red
>    unrelated to its own subject — the same class as TD-142's
>    line-brittleness. Scope it, do NOT fix it: name what the
>    verification would have to check instead.
> 3. Change no code beyond the register and the TD.

## WHAT WAS DONE

1. Machine gate (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap /
   roadmap). Tree NOT clean at start — the demo-cutover lane's
   uncommitted work was present (two dispatch docs + two INDEX rows,
   timestamps 12:49 and 15:16 MT); committed AROUND it with explicit
   pathspecs and a surgical INDEX stage, per D-107's precedent.
   `.hip-lock` was free; taken, released after push.
2. Located every durable home of the old pin: grep found NO "13/17" pin
   in code (eval/, scripts/, harness/, memory_engine/) and none in the
   register — the pin lived only in dispatch docs' evidence sections
   (immutable history) and in the runbooks. The register is therefore
   the durable home; the re-pin landed there as a Notes entry.
3. Cut `DEBT_REGISTER__v20260802_1610.md` from v20260802_1222: TD-145
   filed (OPS), the baseline re-pin Note added, header note prepended;
   LATEST_DEBT repointed; INDEX debt row and this dispatch registered.
4. Verified TD-145's every file:line citation against the live source
   before filing (grep, not memory).

## WHAT WAS FOUND

**The re-pin (register Notes, verbatim intent):** memory-harness
baseline is now **"13-15/17, failures a strict subset of
{MEM-115, MEM-116, MEM-117, MEM-118}"** — any failure outside the four,
or a count below 13, is still a STOP. D-108's four grounds, one line
each, recorded with it:
1. MEM-117 flipped FAIL→PASS between two consecutive identical-code runs
   with no reset between — a code-caused delta is deterministic.
2. None of D-107's changed code is on the four's paths (encode's param
   defaults None with CEIL-CONV pinning byte-identical props; the memory
   harness runs neither demo_seed nor FixtureManager; test_lineage_block
   is pytest-only).
3. The movement matches the recorded mechanism — MEM-116/117/118 sit
   downstream of the live Groq detect_and_apply call, and their own
   pass/fail texts show the supersede landing or not.
4. The direction was pass-ward only — no new failure in any run, and
   MEM-111 (nearest D-107's change) passed all three.

**TD-145 (OPS, scoped not fixed):** MEM-116's value verification is the
single stale spot — `eval/memory_harness.py:1664`
`decrypt_fact_value(new_row["ct"], new_row["dek"], "maya")`, imported
from `harness.encryption` at `:1597`, the ONLY v1-helper use in the
memory harness. The live-written (maya→ray, medication) head is sealed
v2-by-class since REQ_CRYPTO_P2; the v1 helper reaches for
`~/hip-roadmap/data/encryption/.master_key`, which REQ_CRYPTO_P3
deliberately removed and OB6 (ABSOLUTE, passing) asserts absent as
CORRECT. So when the Groq-dependent detection SUCCEEDS, the scenario can
still die at `:1664` with `MasterKeyMissingError` — observed in D-107
run 2, versus run 1's genuinely-environmental mode (detection never
landed; assert at `:1644`). Two unrelated red modes means the verdict
alone is unreadable — TD-142's class. The structural assertions
(`:1637-1660`) are on-subject and fine. **What the verification would
have to check instead, two shapes named, none built:** (a) read through
the class-sealed path — fetch key_version/dyad_id/recipient_ref in the
Cypher at `:1655-1659` and call
`partition_crypto.decrypt_fact_value_for_caller(..., owner='maya',
caller_member_id='maya')`, the same self-read
`eval/harnesslib/fixture.py::decrypt_rows` uses, keeping the
'jardiance' content assertion; or (b) drop the decrypt and assert the
structural outcome only — MEM-116's subject is
supersession-under-withholding, not crypto.

## VERIFIED

- **Watched run:** grep confirmations this session — no "13/17" in
  eval//scripts//harness//memory_engine/; TD-145 free across docs/;
  `:1597`/`:1664` the only `harness.encryption.decrypt_fact_value` hits
  in eval/memory_harness.py; the cited assert/Cypher line numbers read
  back from the live file; `~/hip-roadmap/data/encryption/.master_key`
  confirmed absent (D-108, same session).
- **Reasoned about:** the run-1 vs run-2 failure-mode split relies on
  D-107's captured outputs (run 2's full log is on disk in the session
  scratchpad; runs 1 and 3 from the session transcript) — not re-run
  here, deliberately: the memory harness writes memtest rows and makes
  live model calls, and this dispatch is filing-only.

## HASH

Committed this session on `roadmap` (D-109); parent 8ab4dec.

## OPEN

- TD-145 itself — the harness fix (shape (a) or (b)) is deliberately
  not built; whichever is chosen should also assert the memory harness
  stays v1-helper-free.
- MEM-115's persistent red (denied_count=0, all three runs) is inside
  the re-pinned subset but is a consistent structural gap, not a flake —
  it has no TD of its own and may deserve one when next touched.
- The dispatch-doc evidence sections that say "13/17, the identical
  four" (D-96/D-97/D-99/D-105) are history and stay unedited; the
  register Note is the living pin.
