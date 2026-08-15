# REQ_DYAD_AUDIENCE_DERIVATION: The Dyad Audience Branch Reads Columns That Do Not Exist
Status: PLAN
Branch: roadmap
Reconciled-Against: f30ecd5 (2026-07-30);
DISPATCH_D36__verify-fable-curator-findings__v20260730_0851.md (finding (c),
CONFIRMED against the live `data/registry.db`, not merely against the DDL);
REQ_LEARNER_TARGET_AUTHENTICATION (D-37 — the security fix this is
DELIBERATELY NOT bundled with);
REQ_PARTITION_CUSTODY (the ratified custody/epoch model this branch is
supposed to honor).

**Filed as a SEPARATE REQ on purpose.** D-37's dispatch asked for this
explicitly and the reasoning is worth keeping: the 7th hole was a security
defect in the gate's *design* (one operand authenticated, one not), whereas
this is a plain *coding error* — a branch reading field names that were never
in the table — sitting in code no test exercises. Different root cause,
different acceptance test, different risk of fixing. Bundling a schema
correction into a security fix makes both harder to review and lets a green
run on one be read as evidence for the other.

## THE REQUIREMENT

From the D-37 dispatch:

> File a SEPARATE REQ (or DEBT_REGISTER entry) for the dyad-schema defect — the
> audience branch reads columns absent from the dyads DDL. Do NOT bundle it with the
> security fix; different root cause, different acceptance. If fixing it now is
> low-risk, fix + test under that REQ; if not, register it as a named defect and
> report.

## THE DEFECT, AS MEASURED

`harness/learner_isolation.py` `_audience_of`, dyad branch:

    d = get_dyad(dyad_id)
    members = {d.get("member_a"), d.get("member_b"),
               d.get("caregiver"), d.get("recipient")}
    return frozenset(m for m in members if m)

`get_dyad` is `SELECT * FROM dyads WHERE dyad_id = ?`. The live `dyads` table
(`PRAGMA table_info`, read from `data/registry.db`) has exactly:

    dyad_id | recipient_ref | household_id | dyad_pubkey | status | created_at

**Intersection with the four names read: empty.** Zero of four exist. The
near-miss is `recipient_ref`, which the code asks for as `recipient`. The
actual custodians live in a different table entirely — `dyad_members`
(`custodian_member_id`, `role`, `added_at`, `removed_at`) — which this branch
never reads.

Two consequences, both measured live in D-36:

1. **Every dyad-private fact derives `audience == frozenset()`.** Empty is not
   `None`, so `_audience_of` returns a value the caller reads as a real
   roster. Against a normal target this over-blocks, with a violation string
   asserting `live source audience []` — a fabricated roster, not a derived
   one, so the error actively misleads whoever debugs it.
2. **No currency filter.** `get_dyad` returns the row regardless of `status`,
   and a real `status='exited'` row exists in the table today. Its two
   siblings in the same module both filter for active
   (`get_active_dyad_for`, `get_dyad_for_recipient`), and the other two
   audience branches both bind to live tables with `removed_at IS NULL`. This
   branch filters on nothing — HOLE-6's exact failure mode, in the one branch
   nothing exercises.

**Severity is currently bounded, and D-37 narrowed it further.** Before D-37,
consequence 1 composed with the 7th hole: an empty derived source audience
against an empty target audience was ADMISSIBLE, so dyad-private data — the
most tightly partitioned class under REQ_PARTITION_CUSTODY — could train a
model. D-37 closed that composition from the other end (emptiness now fails
closed on both sides) and additionally REFUSED `dyad` as a registrable model
scope class rather than derive it wrongly. So the security exposure is
closed; what remains is a correctness defect that will produce wrong,
confidently-worded behavior the moment dyad-scoped training is wanted.

## THE ACCEPTANCE TEST

1. **The branch reads columns that exist.** The dyad audience is derived from
   `dyad_members` (`custodian_member_id` where `removed_at IS NULL`) plus the
   dyad's `recipient_ref` from `dyads`. Observable: for a seeded dyad with two
   custodians and a recipient, the derived audience is exactly those three ids.
2. **Currency.** A custodian whose `dyad_members.removed_at` is set is ABSENT
   from the derived audience on the next call, with no caller involvement —
   the same live-roster property `list_caregivers` and `list_circle_members`
   already have. A dyad whose `status` is `exited` resolves to no audience at
   all (fail closed), matching `get_active_dyad_for`'s filter.
3. **Fail closed, never empty-as-a-value.** An unresolvable dyad, a dyad with
   no active custodians, or a missing `recipient_ref` yields `None`, not
   `frozenset()`. Empty is never returned as if it were a derived roster.
4. **`dyad` becomes a supported model scope class** in
   `harness/model_registry.py` (D-37 refuses it today precisely because this
   derivation is defective), with its audience derived by the same corrected
   path.
5. **The Four.** A fault-injection twin that turns the derivation red on
   command (a removed custodian still appearing ⇒ red; removal honored ⇒
   green), a ground-truth fixture with hand-verified membership, a coverage
   entry that removes "dyad-private audience derivation" from L7:LI1's NAMED
   UNCOVERED list, and a metamorphic wrapper or an explicit `na` with a stated
   reason. Battery cases added for the dyad path under the now-wired battery.
6. **Layer 7 green, RATCHET PASS, `--full` before any MET.** No self-MET.

## WHAT'S ALREADY DONE (do not redo)

- The defect is **measured, not suspected** — D-36 confirmed it against the
  live database with a runtime proof, not by reading the DDL. Do not re-trace.
- **The security composition is already closed** by D-37 (emptiness fails
  closed both sides; `dyad` refused as a model scope class). This REQ is not
  carrying a live security exposure — do not treat it as urgent for that
  reason, and do not weaken D-37's fail-closed behavior while fixing it.
- `dyad_members` already carries `removed_at`, and `dyad_registry` already has
  the active-filtering precedents to copy. The primitives exist.

## WHAT'S KNOWN BROKEN

- The branch itself, as above.
- **Nothing exercises it.** The 27-case battery injects fixture resolvers and
  never runs `RegistryProvenanceResolver`; that is why a defect this total
  survived a MET, a `--full`, and two independent code reviews (only one of
  the two Fable reviewers found it). Any fix here that does not also add live
  coverage repeats the conditions that hid it.

## CONSTRAINTS

- **Do not bundle with the security fix.** Separate commit, separate
  assessment, separate MET ruling.
- Do not weaken D-37's empty-is-fail-closed rule to make dyad derivation
  "work"; the correct fix returns a real roster or `None`.
- The working path is sacred: RATCHET green before and after.
- Do not self-MET.

## RECOMMENDATION (this session's, for Bill)

**Register now, fix in its own dispatch — do not fix in D-37.** Reasons:

1. **The security exposure is already closed.** D-37's fail-closed-on-empty
   plus the refusal of `dyad` as a scope class removes the exploitable
   composition. What is left is correctness, which does not carry the same
   clock.
2. **A correct fix needs live coverage, and live coverage is a bigger job than
   the fix.** Deriving from `dyad_members` is perhaps ten lines. Proving it —
   a seeded dyad, a revocation, a fault twin, a coverage entry — is most of
   the work, and it needs the graph/registry rather than a fixture. Doing that
   inside a dispatch already carrying a gate rewrite and a harness-wiring
   change would put three unrelated failure modes in one commit.
3. **D-37 is already large.** It changes the gate's signature, adds a
   registry, rewrites four call sites, reverses a battery expectation, and
   wires a new suite into the harness runner. Adding a schema fix raises the
   chance that a problem in one obscures a problem in another — the precise
   risk Requirements Discipline item 5 exists to prevent.

If Bill would rather have it now, it is genuinely low-risk to write and the
main cost is coverage, not danger.
