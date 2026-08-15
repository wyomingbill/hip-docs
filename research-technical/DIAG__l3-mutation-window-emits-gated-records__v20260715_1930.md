# DIAG: L3 mutation window emits records that L6 gates; stale INJ-6 mirror in the mutation wrapper
Status: BUILT
Reconciled-Against: d76be9e (analysis of run at 7b71d6c, 2026-07-16T01:12Z)

REQ: docs/requirements/REQ_HARNESS__orthogonal-e2e-regression-per-push__v20260715_1700.md
Analysis only. No fix applied. Dispatch: explain the post-clear G1 record
([bill] 'What are my allergies?', path=generation, guard=None, admitted =
5 household facts, none about bill) that patched INJ-6 should have guarded.

## THE ANSWER

The record was produced inside Layer 3's INJ-6b disable-mutation window.
It is not contamination, not a stale process, and not a contract defect.
The mutation wrapper contains a hardcoded copy of the PRE-c75655d INJ-6
predicate, and that stale mirror silently un-fires the patched INJ-6.

## THE CHAIN, file:line

1. eval/harnesslib/layer3.py:91 fires 'What are my allergies?' as bill,
   unmutated. Patched INJ-6 (injection_contract.py:467) fires: resolved
   ['bill'], no admitted fact about bill. That is the GUARD record 2.3s
   earlier (admitted=[], denied=None: the guard emit at voice_orch.py:2771
   does not pass injection_result, so those fields default).

2. layer3.py:101 re-fires the SAME query under mutate_guard("INJ-6b",
   "disable"). The wrapper (inproc.py:96-131) calls the REAL contract;
   patched INJ-6 fires again, guard_triggered=True.

3. inproc.py:117-126, the stale mirror: to decide whether the trigger was
   INJ-6 (keep) or INJ-6b (clear), the wrapper recomputes "would plain
   INJ-6 fire" as `not result.allowed and intent in _PERSONAL_INTENTS` --
   the PRE-c75655d condition. allowed holds 5 household facts (INJ-4), so
   it concludes INJ-6 would not fire, attributes the trigger to 6b, and
   CLEARS guard_triggered.

4. voice_orch sees guard_triggered False, no DisclosureBlocked, proceeds to
   generation. The grounding rule (orchestrator.py:80-94, appended at
   orchestrator.py:406) makes the model emit the canned string. Record:
   path=generation, guard=None, inference_ms non-null. Every field matches
   the observed record. G1 fires on it -- correctly: it IS a fabrication-
   class turn, deliberately induced by the mutation engine.

Answers to the dispatch's candidates: apply_injection_contract IS reached
(via the wrapper bound at server.voice_orch, inproc.py:157-162); there is
no early return (INJ-7's return at injection_contract.py:392 requires a
non-requester member subject; resolved=['bill']=requester); result.allowed
is delivered unmodified to the record (the wrapper mutates only
guard_triggered/access_denied fields, never allowed); the 2.3s-earlier
guard record is the same probe's unmutated baseline; no stale process --
the stale thing is a predicate COPY inside inproc.py.

## FOUR CONSEQUENCES

C1. inproc.py:122-125 must mirror the patched INJ-6 or, better, stop
    mirroring: the contract should report WHICH guard fired (guard_kind
    already distinguishes empty_set/attr_empty_set) so the wrapper reads
    result.guard_kind == "attr_empty_set" instead of recomputing.

C2. layer3.py:88-90's isolation premise ("household facts admitted, so
    plain INJ-6 cannot fire -- isolates 6b") died with c75655d. On this
    probe the baseline refusal now comes from patched INJ-6, not 6b. L3's
    INJ-6b PASS is currently proven by the wrapper bug: disabling "6b"
    actually disables patched INJ-6. Fixing C1 alone will turn L3 INJ-6b
    RED (disable will no longer change the outcome). The probe needs a
    fixture where 6b fires and patched INJ-6 does not: an admitted fact
    ABOUT the subject with a different attribute (e.g. seed a bill
    preference fact, then ask bill's allergies).

C3. L3 runs BEFORE L6 (harness.py:276 vs 283) and its mutated turns land
    in the L6 flush. Even with C1/C2 fixed, every disable window
    deliberately produces guard-off records; G1 hard-zero then fails main
    on every run BY DESIGN. This is the remaining green-half blocker.
    Options (decision needed, none built): (a) inproc.mutate_guard writes
    mutation windows [t0,t1,guard,mode] to a sidecar
    (logs/mutation_windows.jsonl) and L6 excludes records inside windows,
    counting exclusions loudly; (b) L3 moves after L6; (c) L3 snapshots
    and restores turns_demo.jsonl around mutation probes. (a) preserves
    both instruments unchanged and keeps spec section 4 amendment 1 (no
    test-only branches in app code); recommended.

C4. G1 run-to-run variance (3 then 1) decomposes as: >=1 deterministic
    L3-induced record (this finding) + 0..N PW012-class setup-landed
    flakes (layer4.py:96-107, Groq detection false negatives).

## THE 0-BYTE harness_run.jsonl (mtime 19:13, post-run)

Exactly one line of code truncates that file: harness.py:226, at STARTUP.
Nothing on any exit path writes or truncates it. Therefore a SECOND
harness invocation started ~19:13, passed _guards() (harness.py:175) and
get_driver() (harness.py:217), truncated at 226, and died or was
interrupted before the first flush append (the window spans HarnessServer
startup, up to 60s ready-wait, through Layer 2's first fixture.reset()).
Whether it was a ctrl-C, a port-still-bound startup failure, or a wrapper
script's second call is not determinable from this machine.

Bill's named defect stands regardless: the next invocation's startup
truncation destroys the previous run's Layer 6 input, so the gate's
evidence is unreproducible after the fact. Design note (not built):
archive per run -- logs/harness_runs/harness_run.<ts>_<commit>.jsonl,
written at the same point the truncation happens today, before it.
