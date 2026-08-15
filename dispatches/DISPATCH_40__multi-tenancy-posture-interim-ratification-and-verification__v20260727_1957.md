# DISPATCH_40
Status: BUILT (Phase A only; Phase B is verification, reported outside this repo per instruction)
Reconciled-Against: commit — see HASH below (Phase A ships with this doc)

**TYPE:** BUILD (Phase A: docs only, ratifies stated posture into the
diligence deliverable; no code, no REQ acceptance test) + MEASUREMENT
(Phase B: citation verification against primary sources, report only)

**REQ:** none named. Phase A writes ratified content into
`docs/deliverables/HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md`,
a diligence deliverable, not a REQ doc — no build starts against it, so
Requirements Discipline item 8's gate does not apply the way it does to a
code-changing dispatch. Phase B is a MEASUREMENT dispatch component per
CLAUDE.md item 10 and carries REQ: NONE by design — it verifies claims,
it does not build anything.

## THE ASK

> PHASE A — write the ratified interim posture into HIP_ArchitectureForDiligence
> section 6 and close Open Question 1: replace "a request-scoping problem,
> not a hardware problem" with software-isolated multi-tenancy over shared
> inference hardware, citing AW-01 and per-household cache scoping as the
> named resolution; adopt a two-axis framing as the spine (axis A, what is
> shared; axis B, who must be unable to see it), cases as illustrations;
> state the posture — shared served model for most tenants, dedicated
> accelerator for operator-exclusion tenants, fractional-GPU tenant models
> not offered; soften Case 2's superlative and name what confidential
> computing does not cover; add the edge-concurrency measurement to Open
> Questions as HIP's own item. Commit and push Phase A on its own.
>
> PHASE B — verification, report only, no doc changes. Fetch primary
> sources and report CONFIRMED/CONTRADICTED/UNVERIFIABLE for 9 named
> technical claims (MIG/vGPU productization on RTX PRO 6000 Blackwell
> Server Edition, MIG profile sizes, NVIDIA CC docs on MIG/vGPU support,
> P2P/NCCL/NVLink limits under MIG, vLLM cache_salt, vLLM KV-cache
> transfer security docs, NIM/vLLM concurrent LoRA support, a USENIX
> Security 2026 MIG timing side-channel paper, NVIDIA's own CC threat
> model exclusions). Report and stop; further doc integration (3A/3B,
> Case 1.5) waits on Bill's review.

## WHAT WAS DONE

1. Verified environment before touching anything: `bill-ai` /
   `[REDACTED-MACHINE-NAME]`, toplevel `[REDACTED-USER-PATH]/hip-roadmap`,
   branch `roadmap`. `git status --short` was DIRTY on first check — a
   completed but uncommitted Dispatch 39 addition to
   `REQ_PARTITION_CUSTODY` (70 lines, self-labeled NOT RATIFIED). Per the
   dispatch's own STOP-on-dirty instruction, paused and asked Bill how to
   proceed rather than committing or discarding unilaterally; Bill chose
   to commit Dispatch 39's work first. By the time that commit ran, it
   turned out already committed and pushed by a concurrent session
   (`9047487`) — `git commit` correctly reported nothing to commit.
2. Read `docs/INDEX.md`, `docs/deliverables/MANIFEST.md` (Section B row
   362 and the top-of-file changelog), and `docs/dispatches/` before
   editing, per CLAUDE.md's mandatory-read-first and Document Governance
   Rule. Confirmed no prior dispatch had already traced the MIG/vGPU/LoRA
   citation-verification question Open Question 1 names as outstanding.
3. Edited Section 6 ("Multi-tenancy in edge AI") of the architecture
   deliverable: added the two-axis framing (axis A/B) as the section's
   spine ahead of the three cases; rewrote Case 1 to name the isolation
   posture as software-isolated multi-tenancy over shared inference
   hardware rather than a pure request-scoping claim, citing AW-01 (the
   KV-cache prefix side channel) and AW-05 layer two (per-household cache
   scoping) as the register's own named resolution — the prior framing
   contradicted the document's own weakness register, named as such;
   softened Case 2's unqualified superlative to "the strongest practical
   infrastructure isolation and confidentiality boundary for this
   deployment" and named six things confidential computing does not
   cover (in-guest malicious code, application-level logging, compromised
   attestation or key-release administration, side channels, physical
   attack, denial of service); replaced the undecided-posture paragraph
   with the ratified posture itself (shared served model for most
   tenants; dedicated accelerator for operator-exclusion tenants;
   fractional-GPU tenant models not offered, because the fractional
   options that exist do not exclude the operator and the option that
   does is not fractional), stated as interim pending Phase B's citation
   verification.
4. Edited "Open questions for Bill": closed item 1 (multi-tenancy
   platform posture) on the reasoning above, added a new HIP-authored item
   on edge-node concurrency and utilization (unmeasured; named what the
   eventual measurement must cover — request rates, arrival distribution,
   prompt/output lengths, prefill/decode mix, latency ceilings, model mix,
   cache policy, HA replicas), and renumbered the remaining carried-forward
   items.
5. The file was edited concurrently, live, by other sessions throughout
   this work — DISPATCH 38a (Section 4 / Open Questions reframing) landed
   between my first and second edits, and DISPATCH 41 (Section 10
   rewrite, closing Open Question 2) landed between my second and third.
   Each time the edit tool flagged the file as modified on disk, re-read
   the current live state fresh before proceeding rather than trusting a
   stale read — same discipline DISPATCH 41's own doc records. My final
   edit to "Open questions for Bill" applied cleanly with no further
   concurrent change landing mid-edit.
6. DISPATCH 41 committed first (`b9ed199`), and because all sessions
   share one working tree, that commit bundled my completed Section 6 and
   Open Questions edits along with DISPATCH 41's own Section 10 work —
   confirmed by grep against the committed file content post-commit. Phase
   A's actual document content is therefore already committed and pushed,
   just not isolated in its own commit as instructed; see OPEN below.
7. Updated `docs/INDEX.md` (deliverable row + this dispatch's own row)
   and `docs/deliverables/MANIFEST.md` (top-of-file changelog + Section B
   row) to describe the full cumulative state — DISPATCH 38a, 40, and 41
   together — since those two files had been explicitly left untouched by
   the concurrent sessions ("held by that session," per DISPATCH 41's own
   note) and an accurate MANIFEST/INDEX entry needs to describe what the
   file actually contains now, not just this dispatch's own delta.

## WHAT WAS FOUND

Same discrepancy DISPATCH 41 already logged, now closed: the top-of-file
changelog line had claimed (ahead of the body edit landing) that this
dispatch reclosed Open Question 1, while the list body still showed it
open — an artifact of writing the changelog note before the body edit was
confirmed applied under concurrent editing. The final committed content,
verified post-commit, shows item 1 correctly absent from the Open
Questions list body, consistent with the changelog. No content was lost
or duplicated across the three concurrent sessions' edits to this file
today (38a, 40, 41) — each touched disjoint sections (4, 6/Open-Questions,
10 respectively) and the shared-tree commit captured all three cleanly.

## VERIFIED

- **Watched, direct read:** full current state of Section 6 and "Open
  questions for Bill," re-read fresh after each concurrent-edit
  interruption.
- **Watched:** `git diff` / `grep` against the committed file after
  DISPATCH 41's commit, confirming this dispatch's own Section 6 and
  Open-Questions changes are present in `b9ed199` byte-for-byte as
  written, not reverted or partially overwritten by the concurrent
  commit.
- **Reasoned about, not independently re-derived:** the posture ratified
  in Section 6 (operator-exclusion argument for why fractional-GPU tenant
  models are not offered) is Bill's own reasoning, taken as given; this
  dispatch's own contribution was placement, the AW-01/AW-05 citation
  correction, the CC-exclusions list, and the axis framing.
- `git status` before this doc's own commit: `docs/INDEX.md` and
  `docs/deliverables/MANIFEST.md` are the only files this dispatch itself
  changes going into its commit; the architecture deliverable's content
  is already committed in `b9ed199`.

## HASH

See commit — this dispatch doc, the `docs/INDEX.md` update, and the
`docs/deliverables/MANIFEST.md` update ship together. The architecture
deliverable's own Section 6 / Open Questions content shipped earlier in
`b9ed199` (DISPATCH 41's commit), bundled by the shared working tree.

## OPEN

- Phase A was not committed and pushed "on its own" as instructed — it
  landed bundled inside DISPATCH 41's commit (`b9ed199`) because both
  sessions shared one working tree and DISPATCH 41 committed first,
  capturing whatever was staged at that moment, including this dispatch's
  already-completed edits. Flagged to Bill in the chat report rather than
  attempting a history rewrite on a branch already pushed to `origin`.
- Phase B (citation verification of the nine named technical claims) is
  reported directly to Bill, not filed as a document, per the explicit
  "report only, no doc changes" instruction — no Phase B write-up exists
  in this repo. The 3A/3B refinement and Case 1.5 named in the original
  ask are explicitly deferred pending Bill's review of Phase B's results.
