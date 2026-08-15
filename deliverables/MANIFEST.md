# HIP Deliverables Manifest
Status: LIVE
Last updated: 2026-08-04 MT
Updated by: HA-83 (one design artifact registered in Section B, FIRST BANKING: the Moshi dual-model ARCHITECTURE DIAGRAM as adopted, four Mermaid views, cited by path relative to docs/ per the Section B convention. Renders verified by actually running mermaid-cli over all four blocks rather than inferring from syntax. **Section C CHECKED, NOT ASSUMED: no WP section maps to it** — it is an internal diagram of a research-lane direction that amends no plan of record, drawn entirely from two already-banked design docs plus the three already-banked research-mode findings; it introduces no new evidence and makes no product claim, the same reasoning HA-66 recorded for the documents it draws from. **No Section C row is marked NEEDS-UPDATE, and that is a check, not an omission.** Docs-only: no code, no lab run, no graph, no harness. Records a correction to its own dispatch's framing of M0's verdict.) Prior: FM 2 (two coordination documents registered in Section B, both FIRST BANKING: the HIP DEVELOPMENT OPERATING MODEL — the coordination model itself, authority Bill's FM 2 dispatch — and the FM COORDINATOR CHECKPOINT, a LIVE session-recovery state document. Both land in docs/ and are cited by path relative to docs/, the Section B convention. Written because FM 1 searched docs/ and found NO operating-model doc, NO coordinator checkpoint, NO worker board and NO review queue — these are the first. **Section C CHECKED, NOT ASSUMED: no WP section maps to either.** One is an internal coordination process, the other is internal coordinator state; neither is a research artifact any WP section cites, and neither makes a product claim — the same reasoning HA-66 recorded for the research-lane method. **No Section C row is marked NEEDS-UPDATE, and that is a check, not an omission.** Docs-only apart from `scripts/staging_guard.sh` and a scoped pre-commit hook: no product code, no graph, no harness run, no service touched.) Prior: Voice 42 (three Moshi lab documents registered in Section B, all FIRST BANKING: the M0 feasibility findings and the response-onset drift findings, both banked VERBATIM from ~/moshi-lab with bodies byte-verified by sha256 and only a Status/Verification header block prepended, plus a cover note over the pair. All three land in docs/reviews/ and are cited by path relative to docs/, the Section B convention. RESEARCH MODE artifacts: no REQ, no MET ruling, no harness run; UNVERIFIED per the reviews/ rule. Banked because ~/moshi-lab is not version controlled and the lane method §3 makes findings docs the only artifacts that cross into a HIP tree — no lab code crossed. Section C CHECKED, NOT ASSUMED: no WP section maps to these three. Part VI's P7 edge-latency mapping is topically adjacent and was examined; it is deliberately NOT marked NEEDS-UPDATE, because Section C cites the named voice-research P1-P8 corpus rather than these documents, and these are unverified research-mode findings about a third-party model in a lab. Docs-only dispatch: no code, no graph, no harness.) Prior: HA-66 (two Moshi research-lane documents registered in Section B, both FIRST BANKING, both banked VERBATIM from Bill's paste: the dual-model natural-conversation spec v2 and the research-lane development method. Both live in docs/design/ and are cited by path relative to docs/, the Section B convention. Section C checked, NOT assumed: NO WP section maps to either — one is an internal research-lane design direction that explicitly amends no plan of record, the other is an internal process method; neither is a research artifact any WP section cites, so no Section C row is marked NEEDS-UPDATE. Docs-only dispatch: no code, no graph, no harness.) Prior: HA-37 (HIP_FinishPlan registered as PLAN OF RECORD, banked verbatim from Bill's source; HIP_Roadmap__complete-sequence__v20260718_1600 marked SUPERSEDED and retained unaltered. Section C checked: NO WP section maps to a finish plan, so no row is marked NEEDS-UPDATE — checked, not assumed.) Prior: D-153 (HIP_DesignDigest Section B row updated -- new CURRENT version v20260804_0639 carrying "week of 2026-08-04": silent absorption as a failure mode distinct from unbuildable, a requirement enforced yet NOT MET on scope, what a lock must be to count as one, a status board that checks its own claim, and one root cause behind three memory-harness symptoms. Section C checked: NO WP section maps to the design digest, so no row is marked NEEDS-UPDATE -- checked, not assumed.) Prior: D-137 (HIP_DesignDigest Section B row updated -- new CURRENT version v20260803_1602 carrying "week of 2026-08-03": protection that scaled with visibility, the model-cooperation finding and the cost of establishing its width, classification-is-not-wiring, and the velocity instruments. Section C checked: NO WP section maps to the design digest, so no row is marked NEEDS-UPDATE -- checked, not assumed.) Prior: D-88 (HIP_DesignDigest Section B row updated -- new CURRENT version
v20260801_1214 carrying "week of 2026-08-01 (part 2)": the architecture boundary, the
reference-monitor/complete-mediation reframing, the ruled threat model, voice untrusted
by construction plus the belt-and-suspenders identity ruling, the audit being
tamper-evident against nobody, models-propose/core-commits, the acceptance-plan audit
[3 of 30 rows wired], and earned calibration. v20260731_2140 marked SUPERSEDED; the
digest is cumulative so no content is lost -- all three week sections are carried
forward, newest on top. Traceability table cites every artifact by path and landing
hash, verified with `git log --diff-filter=A` rather than recalled. Still NO Section C
row -- re-checked this dispatch, not assumed: the digest is an internal design note,
not a research artifact any WP section maps to. PRIOR PROVENANCE, retained: D-72
(HIP_DesignDigest Section B row updated -- new CURRENT version v20260731_2140 carrying
the week of 2026-08-01, consent/authorization/the dimensioned ceiling; prior week's
file marked SUPERSEDED). This deliverable IS in the Document Governance Rule's scope,
unlike the docs/requirements/ work earlier in the session, so the rule's same-commit
MANIFEST requirement applies and is met here); prior: D-55 (banked D-46 Fable critique listed in Section C's
diagnostic-artifacts table — FIRST docs/reviews/ row in this manifest, added on
explicit dispatch instruction; note docs/reviews/ is formally OUT of the
Document Governance Rule's MANIFEST-check scope per CLAUDE.md and no prior
banked review carries one, so back this row out rather than extend the pattern
if MANIFEST is to stay deliverables-only); prior: D-44 (HIP_BuildState Section B row brought current — scorer MET,
Bill's ruling; also flags that D-39/D-42/D-43 updated that deliverable in place
without the MANIFEST update this rule requires); prior: D-13
(HIP_GovernanceExplainer registered, Section B row); prior: D-08 (HIP_BuildState registered, Section B row -- new
deliverable, one-page built/integrated/planned summary, every status line
verified against INDEX/REQs/MANIFEST before landing); prior: DISPATCH 44
(REQ_COVERAGE_MEASUREMENT row marked MET -- both
previously-outstanding items closed, see Section B row); prior: DISPATCH 42
(Section 6 upgraded from interim to final, Case 3
split into 3A/3B, Case 1.5 added, interconnect wording corrected,
USENIX Security 2026 side-channel finding added, CC threat-model
exclusions attached to Case 2 by name, stale Open Question 1 numeric
cross-reference retired, changelog-vs-body gap DISPATCH 41 flagged
checked and found already resolved -- see below); prior: DISPATCH 41
(Section 10 rewritten from Bill's ratified positioning of vertical
depth/world modeling/multi-modal input, closing Open Question 2) and
DISPATCH 40 (Section 6 multi-tenancy posture interim ratification,
closing Open Question 1 again, plus a new edge-node concurrency/
utilization Open Question; Phase B citation verification reported
outside this repo) -- both same-day, same-file, concurrent with each
other and with DISPATCH 38a below; prior: DISPATCH
38a (Bill's refinement to DISPATCH 38, items 4/7/8 reframed as the gated
moat track, not resolved-by-rejection -- see below); prior: DISPATCH 38, HIP_ArchitectureForDiligence Open Questions
resolution (docs/deliverables/HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md,
docs/deliverables/HIP_ArchitectureWeaknessRegister__v20260722_1536.md):
AW-06 written into the roadmap AW register (five detection signatures for
KV-cache prompt extraction, specifying AW-05's layer-three defense in
full, status SPECIFIED NOT BUILT) -- closes Open Question 1 and the
register half of Open Question 2. Six further Open Questions ratified and
removed: learned ranker (retrieval stays rule-based indefinitely, a
position not a gate -- auditability over a learned ranker's opacity;
Section 4/Section 10 updated); proactive intelligence (not authorized;
three hard gates named for any future authorization -- opt-in categories,
an interruption floor, audience rules, drawn from the Context and
Interaction Architecture Reconciliation's own row 37/35); household phase
gates (numeric counts dropped; tens then hundreds, depth over raw count,
in the design note's own words); training-data record (moot -- no
learner, no record to classify; the operator-blind-at-rest collision is
removed by the same ruling, not resolved by a crypto-class decision);
federated learning (stubbed as a mechanism for training a learner that
does not exist, not left as an unplaced gap). Observation-and-perception
custody restated, not removed: positions now on record against
REQ_PARTITION_CUSTODY (system-observed facts about a caregiver seal to
caregiver+recipient only; non-members never stored without enrollment;
perception is process-and-discard) -- named plainly that none of this is
written into REQ_PARTITION_CUSTODY's own text yet, so this is ratification
awaited, not settled requirement text; two sub-questions stay open
(standing-policy disclosure-to-collection extension; whether observation
may raise a trust rung, corroborate yes/confirm never). Four Open
Questions remain, down from eleven: multi-tenancy platform posture
(REOPENED -- an external review split Case 3, adding a shared-base-plus-
adapter case vendor docs confirm is productized today, per the Phase A
verification that preceded this dispatch; waits on citation verification
before Section 6 itself is rewritten, not rewritten here), vertical/world-
model/multi-modal positioning (unchanged), observation-and-perception
custody's own ratification (restated above), and the four-tier deployment
hierarchy (unchanged). The multi-tenancy silicon-allocation document
itself remains main-only -- that half of the original branch-location
question was not reopened, only the AW-register half was closed.
Then: DISPATCH 38a, Bill's refinement to DISPATCH 38 (same file,
HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md,
Section 4 and Open Questions edited in place): items 4, 7, and 8 were
closed on the wrong framing above -- not resolved-by-rejection, but the
moat track, gated. Item 4's ruling is unchanged (retrieval stays
rule-based today, no learning process touches any household's data) but
is restated as the gate at the entrance to the differentiating half of
the roadmap -- learned ranker, household adaptation, federated learning,
proactive intelligence -- not a rejection of that half; the moat is the
governed learning substrate underneath retrieval, per-household training
signal held under the same partition as retrieval with the epistemic
record as provenance, gated on REQ_LEARNER_SIGNAL_ISOLATION, entered when
a measured retrieval failure justifies the cost, not on a schedule.
Deferred-and-absorb items (operator-blind at inference, ambient/full-duplex
voice) are named as the opposite category: commodity, adopted when
vendors mature them, not gated on anything HIP builds. Training-data
record (item 7) and federated learning (item 8) are un-closed: restored
to Open Questions as gated-moat items, training-data record's crypto
class/retention/identity form named as a live design question at
REQ_LEARNER_SIGNAL_ISOLATION's own Open Question 2, not moot; federated
learning named as the cross-household pooling mechanism for that same
gated track, not resolved by rejection. Six Open Questions now remain,
up from four (the four items already listed -- multi-tenancy platform
posture, vertical/world-model/multi-modal positioning,
observation-and-perception custody, the four-tier deployment hierarchy --
unchanged; items 7 and 8 restored alongside them).
Then: DISPATCH 41, write Section 10 (docs/deliverables/
HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md,
Section 10 and Open Questions edited in place): Section 10 (Long vision)
rewritten from Bill's ratified positioning -- the thesis that vertical
depth, world modeling, and multi-modal input are not separate bets, each
the same governed substrate extended; three positions ratified (multi-modal
input is perception, cross-referencing REQ_PARTITION_CUSTODY's
observation-custody positions; world model means the graph made predictive,
positioned as the destination Generation 6 points toward; verticality
lives in governed context, not domain-specific models); ordering stated
(perception enters when custody positions ratify, the predictive layer
enters after the learning substrate exists, vertical context packs can
start any time). Six-generation list left untouched. Open Question 2
closed and removed. New dispatch doc registered:
docs/dispatches/DISPATCH_41__write-section-10-close-open-question-2__v20260727_1954.md.
Then: DISPATCH 40, multi-tenancy posture interim ratification + citation
verification (docs/deliverables/
HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md,
Section 6 and Open Questions edited in place; concurrent with DISPATCH 41
above, both landed in the same shared working tree): Phase A -- Section 6
reframed on a two-axis spine (axis A, what is shared: weights, silicon,
GPU memory, serving process, VM, KV/prefix cache, scheduler, base model,
adapter; axis B, who must be unable to see it: other households, other
tenants, the operator, the model provider), cases kept as illustrations
under the axes; Case 1's isolation claim corrected from request-scoping-
only to software-isolated multi-tenancy over shared inference hardware,
citing AW-01 and AW-05 layer two (per-household cache scoping) as the
register's own named resolution -- the prior wording contradicted the
document's own weakness register; Case 2's unqualified superlative
softened to "the strongest practical infrastructure isolation and
confidentiality boundary for this deployment," naming six things
confidential computing does not cover (in-guest malicious code,
application-level logging, compromised attestation or key-release
administration, side channels, physical attack, denial of service);
platform posture ratified on an interim basis -- shared served model for
most tenants, dedicated accelerator for a tenant requiring operator
exclusion, fractional-GPU tenant models not offered because the fractional
options that exist do not exclude the operator and the option that does
is not fractional -- closing Open Question 1 again ("interim" because the
underlying MIG/vGPU/CC/vLLM/LoRA technical claims are verified separately
in Phase B, not because the posture itself is provisional). New
HIP-authored Open Question added: edge-node concurrency and utilization,
unmeasured, naming what the eventual measurement must cover. Five Open
Questions now remain (down from six, net of DISPATCH 41's closure and this
dispatch's close-one/add-one). Phase B (9-claim citation verification
against primary sources -- MIG/vGPU productization, MIG profile sizes,
NVIDIA CC docs on MIG/vGPU, P2P/NCCL/NVLink under MIG, vLLM cache_salt,
vLLM KV-cache transfer security, NIM/vLLM concurrent LoRA, a USENIX
Security 2026 MIG timing side-channel paper, NVIDIA's own CC threat-model
exclusions) is report-only per instruction; no further doc changes made
pending Bill's review; the 3A/3B refinement and a possible Case 1.5 are
explicitly deferred, not written here. New dispatch doc registered:
docs/dispatches/DISPATCH_40__multi-tenancy-posture-interim-ratification-and-verification__v20260727_1957.md.
Both DISPATCH 41 and DISPATCH 40's document edits landed bundled inside
DISPATCH 41's own commit (b9ed199) because the two sessions shared one
working tree and DISPATCH 41 committed first, capturing both sessions'
completed edits at that moment -- confirmed by direct comparison against
the committed file content, nothing lost or overwritten. This MANIFEST
and docs/INDEX.md update, plus the DISPATCH_40 dispatch doc itself, were
left for whichever session held these two files next, per DISPATCH 41's
own OPEN note; that turned out to be this same DISPATCH 40 session,
completing its own bookkeeping in a following commit.
Then: DISPATCH 42, reconcile Open Question 1 gap and upgrade Section 6 to
final (docs/deliverables/
HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md,
Section 6 and Open Questions edited in place, no concurrent session this
time): Task 1 checked the changelog-vs-body discrepancy DISPATCH 41's own
dispatch doc flagged (its OPEN note stated the Open Questions body still
showed multi-tenancy platform posture open after DISPATCH 40 closed it).
Read fresh against commit fdd9a42, the two already agreed: DISPATCH 40's
own closing edit had already landed in the body by the time everything
was committed, and DISPATCH 41 had read the file mid-edit, before that
edit finished, reporting what was true at that moment and not what
shipped. No content fix was needed; a clarifying note was added to the
Open Questions section recording the finding for any future reader. Task
2 upgraded Section 6's platform posture from interim to final now that
DISPATCH 40 Phase B verified all nine underlying technical claims against
primary sources: Case 3 split into 3A, fractional with the operator
trusted, MIG-backed vGPU confirmed productized on the RTX PRO 6000
Blackwell Server Edition (NVIDIA's AI Enterprise vGPU MIG-backed-vGPU
page, up to four MIG slices and 48 concurrent VMs; the Tesla MIG User
Guide's supported-profiles page, 24/48/96 gigabyte profiles, not four
fixed 24-gigabyte slices alone), and 3B, fractional with the operator
cryptographically excluded, not available because NVIDIA's confidential-
computing enterprise reference architecture states MIG and vGPU are not
supported in CC mode, a hard limitation with no roadmap language, across
both current GPU generations. Case 1.5 added: one shared base model with
per-tenant LoRA adapters, batched on one accelerator, productized in both
vLLM (its LoRA features page) and NVIDIA NIM (its PEFT customization
page), stated plainly as customization, not model custody, since the
operator's serving stack still loads and runs every tenant's adapter. The
old "disables the interconnect" line replaced with the MIG User Guide's
own deployment-considerations page: P2P works only between MIG instances
on the same GPU, not across GPUs; NCCL is not supported with MIG;
MIG-backed vGPUs are excluded from NVLink peer-to-peer transfer and
NVLink multicast. A new paragraph between 3A and 3B names the USENIX
Security 2026 paper "Behind Bars: A Side-Channel Attack on NVIDIA MIG
Cache Partitioning Using Memory Barriers" (artifact-evaluated, explicit
LLM-inference relevance in the authors' own words) and uses it to state
HIP's own three-way separation of resource isolation (MIG's hardware
split), tenant isolation (AW-05's cache scoping and Case 1's request-level
boundary), and cryptographic confidentiality (Case 2's CC guarantee
against the operator itself), cross-referenced against AW-04's own
accepted limit. Case 2's own entry now carries NVIDIA's confidential-
computing trust-and-threat-model exclusions by name: vulnerable inference
code inside the confidential guest, application-level payload logging, a
compromised attestation or key-release administrator, side channels,
physical attack, and that confidential computing is not a defense against
denial of service. The closing posture paragraph now states the posture
as a hardware fact, not a product-timing bet, that does not expire on a
driver release, and retires the stale numeric "Open Question 1"
cross-reference in favor of Section 6 stating its own reasoning directly.
Section 6's own header now reads "(allocation posture ratified final
2026-07-27, DISPATCH 42)," matching the convention DISPATCH 41 set for
Section 10. All prose newly added by this dispatch was checked by
isolated grep, separated from the surrounding text's own pre-existing
em dashes and the deliberate "Item 7 --"/"Item 8 --" historical-identifier
convention, and carries zero em dashes; the one retained three-part
construction (resource/tenant/cryptographic isolation) is the substantive
separation the ask itself named, not a decorative triad. Five Open
Questions remain, count unchanged by this dispatch. New dispatch doc
registered: docs/dispatches/DISPATCH_42__reconcile-oq1-and-upgrade-section6-to-final__v20260727_2056.md.
Prior: DISPATCH 36, register reconciliation phase 2 (docs/deliverables/
HIP_RegisterReconciliation__cross-branch-id-collisions__v20260727_1930.md,
Section 7/8/9 additions): main branch's four colliding entries filed for
real into roadmap's registers under their renumbered IDs, with lineage
(original ID, branch, commit) recorded in each -- TD-131 (commit 4390240)
as TD-136 (docs/techdebt/DEBT_REGISTER__v20260727_1935.md, new timestamped
cut per the Naming Law, LATEST_DEBT.md repointed); D-25/D-26/D-27
(commits 767517a/a6620d4/720c94c) as D-29/D-30/D-31 (HIP_DefectRegister,
edited in place, matching how D-24/27/28 were added). D-26/D-27's mutual
internal cross-references given minimal bracketed glosses pointing at
their new numbers, so porting them didn't recreate a dangling citation.
HIP_ArchitectureWeaknessRegister's TD-136 cross-reference (written as a
forward reference in phase 1) confirmed real. D-28 verified FIXED
independently in code this session (not assumed from
REQ_STRIP_CONTEXT_COMPLETENESS existing) -- reproduced the exact
triggering shape live against current harness/orchestrator.py, confirmed
no leak; regression-checked the two previously-working sections;
ran scripts/run_harness.sh --layer 7 live (L7:CTX-STRIP PASS, its
fault-injection twin PASS both directions, RATCHET PASS); confirmed
server/voice_orch.py untouched by the fix (TD-136's own broader MID/CORE
question genuinely untouched, not quietly resolved). Full verification
record in the reconciliation doc's new Section 9. Phase 3 (main-side
citation updates, main not touched) fully scoped in the doc's new
Section 8 -- every main-only file citing an old number, so the work is
scoped rather than forgotten.
Prior: DISPATCH 35, register reconciliation phase 1 (docs/deliverables/
HIP_RegisterReconciliation__cross-branch-id-collisions__v20260727_1930.md):
Bill's ruling adopted -- roadmap's numbering is authoritative, main's
colliding entries renumber on port. New AUDIT RECORD deliverable registered
in Section B below: full cross-branch collision audit (BACKLOG.md,
DEBT_REGISTER, HIP_DefectRegister, HIP_ArchitectureWeaknessRegister,
docs/INDEX.md, MANIFEST.md compared against main d4a8a90) -- collision set
(TD-131, D-25, D-26, D-27, each quoted both ways; D-24/TD-122 status-only
staleness, not topic collisions), per-register roadmap-only/main-only ID
counts, highest-ID-in-use table, the full citation-break list, and the
renumbering map (main's D-25/26/27 -> D-29/30/31, TD-131 -> TD-136 on
port; nothing ported yet, that's Phase 2). Phase 1 actions taken in the
same commit: (1) repaired REQ_PROMPT_SUBSET_ADMITTED's dangling
docs/BACKLOG.md:77/TD-131/BILL-7 citation (unresolvable on roadmap since
2026-07-26, predates this reconciliation work) with an inline correction
note, not a rewrite; (2) retargeted docs/BACKLOG.md row 49's TD-135
reservation to TD-137 (135 was already taken by an unrelated real entry,
136 is now reserved for the ported main-TD-131) -- no other BACKLOG row
touched; (3) ported HIP_ArchitectureWeaknessRegister (AW-01..AW-05)
verbatim from main 4390240, only its cross-reference header rewritten to
name TD-136 instead of main's TD-131, LATEST_ symlink created, registered
in Section B below in the same commit. No branch merge performed or
implied. Read-only audit that preceded this dispatch touched nothing;
this dispatch is the first write.
Prior: D-28 (docs/deliverables/HIP_DefectRegister__v20260715_1930.md):
new defect registered, NOT FIXED -- registered, not built, per instruction.
strip_context_for_tier's personal-section regex (harness/orchestrator.py:
655-658) covers 2 of the system prompt's 3 fact-bearing sections; the
third, "Confirmed facts about other people" (real cross-member household
facts, harness/orchestrator.py:429-444), passes an on-net Groq mid/core
call unstripped when it is the only section populated. Verified fresh by
direct code read this session (line citations in the entry itself,
spanning harness/orchestrator.py and server/voice_orch.py's live
assemble_governed_context -> Groq call-site trace, plus config.yaml:83).
Located while verifying HIP_ClaimsRegister CLAIM-04 (Bill's seeded
freshness-tier claim, kept DISPUTED). Cross-referenced: same class of
exposure as TD-131 on the main branch (commit 4390240, "household facts
reach MID/CORE Groq payload unfiltered," content HIP deliberately sends,
not an attacker-inferred side channel like the HIP_ArchitectureWeaknessRegister
AW-* entries -- that register's own header draws this exact distinction).
Named, not silently resolved: roadmap's own TD-131 slot in
docs/techdebt/LATEST_DEBT.md is a different, unrelated entry (git
worktree checkout gaps) -- the two branches' debt registers were cut
independently and collided on the same ID. No code changed.
Prior: HIP_ClaimsRegister (docs/deliverables/
HIP_ClaimsRegister__v20260727_1729.md): new AUDIT RECORD deliverable
registered in Section B below -- 18-claim register (5 seeded by Bill, 13
found independently) of every load-bearing claim the NDA package makes
about what HIP is or does, sourced from docs/rendered/ for the white
paper/Technical Annex/Prototype Evidence/Ecosystem Analysis (docx content
read from renderings, never parsed directly), read directly for NDA Open
Problems and the Governance Proof, and fetched live from the ten gated
site pages at hip.olindasolutions.com/d-7h4k2m9x/. No document corrected
-- register only. Confirms WRONG: voiceprint-as-identity (site +
Technical Annex; the reconstructed Confidential WP already states the
ratified device-keypair truth correctly), retrieval-time-not-storage-time
scoping (Technical Annex 6.3; real enforcement is write-time key-wrap/
class-sealing), Groq-hosted-inside-the-enclave (category error -- Groq is
a third-party hosted API), a fabricated "prototype benchmarks 8-15%"
confidential-computing figure (WP's own Part XIII says CC is "not
running fact, today"), a 10-vs-11+ canonical-attribute-count staleness,
and a 4-vs-5-tier internal inconsistency between the Technical Annex and
its own companion Prototype Evidence document. NEW FINDING beyond the
seeded claims: a real, located code gap in
harness/orchestrator.py's strip_context_for_tier -- the
"Confirmed facts about other people" system-prompt section (cross-member
household facts) is not covered by the section-stripping regex, so a
turn with that section populated but the speaker's own two sections empty
would not be stripped before an on-net Groq call; substantiates Bill's
seeded CLAIM-04 (kept as his own word, DISPUTED) with new evidence, not
previously named in any TD/REQ. Also corrects (names, does not silently
fix) how the HIP_PropagationWorkOrder cross-reference was asked for: that
exact string is not in build_nda.js -- it is in the tech-debt register
and business/financial/build_fin_chg5_risk_opex.py; build_nda.js instead
names a sibling never-filed document, HIP_FinalizationOrder -- both
already independently found by HIP_EcosystemAnalysis_Recovery
(2026-07-27), corroborated not duplicated here.
Prior: HIP_PackageDirectory (docs/deliverables/
HIP_PackageDirectory__v20260727_1716.md): new AUDIT RECORD deliverable
registered in Section B below -- read-only inventory, one row per document
in the Tier-1 NDA package and its supporting set plus the ten gated site
pages, cross-referenced against this file, docs/INDEX.md, docs/rendered/,
and `git log --all` on-disk/history reality. Changes no prose in any
surveyed document. FINDING surfaced (not corrected here, Bill's call):
beyond the already-flagged HIP_WhitePaper_Confidential v20260712_1852 gap,
the same claimed-CURRENT-but-not-found pattern recurs for 3 more
Confidential-WP chain versions, the Ecosystem Analysis NDA's own
claimed-CURRENT file, and the entire public White Paper chain from
v20260708_1604 onward (5 versions) -- none of these 9 exist on disk or in
`git log --all` on any local branch; Google Drive not checked for any of
them (only the original 2026-07-27 finding had that check done). Also
found: HIP_FinModel_ReviewMemo has a docs/INDEX.md row but no MANIFEST
Section B row (registration gap); three business/ecosystem Ecosystem
Analysis drafts and the real newest public WP file are on-disk and
git-tracked but registered nowhere.
Prior: REQ_DOC_RENDERING (docs/requirements/
REQ_DOC_RENDERING__docx-text-baseline-and-staleness-gate__v20260727_1649.md):
editorial addition to HIP_OperationsRunbook, two lines added under a new
"Reading document changes" heading pointing to scripts/docx_to_text.sh and
stating that git diff on docs/rendered/ (not the binaries) is how a document
change is read. No other content changed; same filename, same Section B row
(date already 2026-07-27, unchanged). No WP section affected, no Section C
change.
Prior: HIP_ArchitectureForDiligence (docs/deliverables/
HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md):
new Tier-1 deliverable registered in Section B below, DRAFT for Bill's
ratification, closing Gap 1 of the Tier-1 NDA Package Index (HIP_NDA_Package__
tier1-diligence__v20260714_1400.md, Stage 1 item 9, "Architecture Design-Level
Material" -- see that doc lines 164-174 and 401-403). Supersedes
HIP_TechnicalAnnex__v20260702_1155.docx (RETIRED 2026-07-28, row below); says
so in its own header. Assembled from the Context and Interaction Architecture Reconciliation,
the six named REQ docs (REQ_HARNESS_DISCIPLINE, REQ_COVERAGE_MEASUREMENT,
REQ_CRYPTO_P3_OPERATOR_BLIND, REQ_G0_OUTPUT_INVARIANT, REQ_PROMPT_RECORD_FIDELITY,
REQ_PARTITION_CUSTODY), the ecosystem analysis and market-research corpus, and
the NDA Open Problems / Debt Register NDA Appendix. Two cited sources --
HIP_ArchitectureWeaknessRegister (AW-01..AW-05; note AW-06 is referenced by
name in that doc and in docs/INDEX.md but no AW-06 entry exists anywhere) and
HIP_MultiTenancy__silicon-allocation-three-cases__v20260724_0801.md -- exist
only on the main branch, not on roadmap; read via git show against main for
this document, not merged. Both gaps (AW-06, branch location) are carried as
open items in the new document's own Open Questions section, not resolved
here. Docs only; no code touched; no other Section B row changed.
Prior: REQ_HARNESS_RUNNER (docs/requirements/REQ_HARNESS_RUNNER__local-run-harness-wrapper-with-guards__v20260727_1233.md):
Editorial addition to HIP_OperationsRunbook, two lines added under "Running
the gate" pointing to the new scripts/run_harness.sh wrapper (item 1 of a
five-item 2026-07-27 sprint). No other content changed; same filename, same
Section B row, date bumped below. No WP section affected, no Section C
change.
Prior: REQ_CRYPTO_P3_OPERATOR_BLIND pre-destruction audit for part (c)
(docs/requirements/REQ_CRYPTO_P3_OPERATOR_BLIND__stage4-phase3__v20260724_1129.md)
and new sibling REQ_DEMO_DASHBOARD_MIGRATION (docs/requirements/
REQ_DEMO_DASHBOARD_MIGRATION__retire-demo-master-key-migrate-to-partition-write-path__v20260724_1129.md):
two new Section B rows registered — this table previously carried no row for
REQ_CRYPTO_P3_OPERATOR_BLIND at all, an orphan gap now closed. Docs only; no
key file, code, or the demo touched. Prior: HIP_MemberIsolation_Dyads custody spec (docs/deliverables/
HIP_MemberIsolation_Dyads__custodial-crypto-entry-exit-overlapping__v20260718_1207.md):
new PLAN deliverable registered in Section B — extends the member-isolation
crypto design with the DYAD as the crypto unit (caregiver holds the key on the
keyless care-recipient's behalf, resolving the prior design's author-keyed
limit), a write-time dyad-private/household-shared/member-private partition,
atomic entry/exit with re-encryption under a new key, non-cooperative custodian
eviction via the same 2-of-3 recovery quorum, overlapping-dyad key rings, and
custody-transfer/dissolution flows. Grounded in the live data shape (demo_seed.py:3,126,352:
owner=custodian member, subject=care-recipient) at 47851d7. Section C Part II
stays NEEDS-UPDATE (unchanged; same trust-boundary claim). Spec only; no code,
no WP prose changed. Prior: HIP_MemberIsolation crypto design (docs/deliverables/
HIP_MemberIsolation__crypto-partition-and-recovery-design__v20260718_1117.md):
new PLAN deliverable registered in Section B — the cryptographic member-
isolation / operator-blind-at-rest / threshold-recovery design, grounded in a
re-read of encryption.py + extraction_queue.py + demo_dashboard.py at 5d6bde3.
Section C Part II ("The Moat") marked NEEDS-UPDATE: its "trust boundary
protects member data from the platform itself" claim is architectural intent,
not an implemented property, against the current filter-based isolation; the
design is the roadmap to make it literally true. Design only; no code, no WP
prose changed. Prior: DISPATCH_FRONTIER_TIER_BUILD (docs/dispatches/
DISPATCH_FRONTIER_TIER_BUILD__script1-t04-t05__v20260717_1330.md): new D-24
registered in HIP_DefectRegister — `medication_status` (added by the prior
REQ_D21_D23 commit `b36fa95`, not this dispatch) over-triggers on
medication-SWITCH statements ("switched from X to Y"), landing writes
under `medication_status` instead of `medication`; confirmed NOT caused by
this dispatch's own frontier-tier code (isolated by reproducing identically
on `b36fa95` alone). Found while verifying `--full` for this build's own
PROVE LIVE item (e); root cause confirmed via a direct Groq structured-
output call showing the actual misclassification. Not fixed here — out of
this dispatch's scope (REQ_D21_D23's territory). Prior: DISPATCH_ENUM_AUDIT (docs/dispatches/
DISPATCH_ENUM_AUDIT__seed-fixtures-outside-detector-schema__v20260717_1135.md):
D-21's root cause upgraded from "leading hypothesis" to CONFIRMED (direct
enum read: incident/medication_status absent from CANONICAL_ATTRIBUTES's
11 values). New D-23 registered — 5 of 11 seeded fixtures (45%) use
attributes outside the enum (D4=D-21, D5, D8, D10, D11); D10/D11 are a
distinct mismatch shape (matching category exists, seed uses a different
literal name). TD-123's tech-debt entry corrected: its actual scope is
subject-slot person-typing, a different bug than D-21/D-23 — two prior
documents had informally routed unrelated bugs through its ID. No code
changed, audit only, per instruction ("No fix"). Prior: DISPATCH_DETECTION_MISS_MEASUREMENT (docs/dispatches/
DISPATCH_DETECTION_MISS_MEASUREMENT__d21-and-td125-numbers__v20260717_1117.md):
D-21's HIP_DefectRegister entry corrected from "stochastic retry-recovery
gap" to "measured: 100% deterministic miss, 0% retry recovery" — a 24-
utterance aggregate corpus landed 24/24, ruling out a population-level
detection problem; leading (unconfirmed) hypothesis is a schema/enum
mismatch (the seed's "incident" attribute has no CANONICAL_ATTRIBUTES
equivalent), which would mean TD-123's prompt-hardening framing does not
fix this specific defect. No code changed — measurement only, per
instruction ("No fixes. No prompt changes."). Prior: REQ_D22_D20 (docs/requirements/
REQ_D22_D20__confirmation-gate-write-loss-and-imperative-openers__v20260716_2238.md):
D-22 fixed first (Bill's priority, "worst of the four") — confirmation
gate's "unclear" classification scoped to the exact <4-word floor where
Seam A/F3 structurally cannot reach a turn either way, instead of "any
declarative"; a genuinely new write no longer gets silently dropped. D-20
fixed — _QUESTION_OPENER_RE gains exactly "explain"/"trace" (grepped every
corpus first, nothing else added speculatively). D-19 resolved as an
honest, unplanned side effect of the D-22 fix. D-21 deliberately left
failing per Bill's instruction. Verified via `python -m eval.harness
--full` (not targeted turns, per Bill's new CLAUDE.md rule added this same
session) — exactly one RATCHET FAIL entry remains (D-21), no new
regression anywhere else. Prior: REQ_D17 (docs/requirements/
REQ_D17__reporter-masking-accept-amnesty-archive__v20260716_2158.md): D-17
registered FIXED — reporter.apply_baseline no longer masks regressions
behind brand-new failures (regression now checked first, both printed,
priority exit 1). CRITICAL: fixing D-17 and re-running --full on main
immediately surfaced 5 real, currently-masked regressions — D-19 (stale L1
unit-test assertion, not a security issue), D-20 (F3 gate misfires on
imperative reasoning queries like "Explain..."/"Trace..." — regression in
c86a414), D-21 (confirmed live instance of TD-125's detect-retry not
reaching 100% recovery), D-22 (D-03/D-18's confirmation gate silently drops
a genuinely new declarative's write when an unrelated older token is still
pending — regression in 3c0cb74). All four newly registered, NONE fixed in
this session (out of D-17's scope) — baseline deliberately left unchanged
so the ratchet keeps reporting them honestly. Prior: REQ_D03_D18 (docs/requirements/
REQ_D03_D18__confirmation-gate-no-fallthrough__v20260716_1806.md): D-03 and
D-18 registered FIXED in HIP_DefectRegister — confirmation_gate.py no
longer falls through to the model on an unmatched declarative confirmation
attempt (leading-word yes/no check + is_declarative_utterance discriminator,
same shape as the F3 write-path fix); 6/6 live acceptance turns watched,
Neo4j state verified, not reply text. TD-126 logged (demo_reset.py's
hardcoded hip-harness paths deleted that checkout's maya/sam voiceprints
during this session's live proof — flagged, not fixed). Prior: REQ_SIA_PHASEB reconciliation (docs/requirements/
REQ_SIA_PHASEB__reconcile-plans-and-file-requirement__v20260716_1736.md):
H-09 added to HIP_DefectRegister (Phase 5/metrics, dropped silently since
07-15, no owner until now — added to that register's ORDER section too);
HIP_HarnessPlan §3.3 amended in place (dated note: risk-memo item 0b, not
this plan's Phase-3 sequencing, governs runtime G0's build priority — the
two documents were disagreeing on the page). Neither edit is a new version;
both are in-place amendments to LIVE registers, consistent with how D-05/
I-10 were already corrected in place earlier the same day. Prior: HIP_SIA_PhaseB risk memo amended to v20260716_1624 (Bill adopted
ANALYSIS__postcondition-gap-review__v20260716_1512.md's split: two
outcome-state exit gates moved to the front of §9, §5.3 corrected — G0 does
not exist anywhere, re-keying G1/G4 is not a substitute — D-01 sequencing
rationale stated, voice-path-exposure + P2/i019-visibility costs added).
v0800 marked SUPERSEDED below, not overwritten. Prior: Orphan sweep of
docs/deliverables/ + docs/demo_prep/ (Findings was
not alone) — 2 more found on disk unregistered: HIP_SIA_PhaseB__risk-memo__
v20260716_0800.md (untracked in git besides) and
WP_PartII_TrustBoundary_DRAFT__v20260711_1730.md (tracked, prior draft of
the v1800 integrated version, never added to Section B). Both registered
below; SIA_PhaseB committed. Three named files (HIP_Theory__postcondition-
gap__v20260716_1500.md, HIP_Study__calibration__v20260716_1030.md,
HIP_Musings__calibration__v20260716_1100.md) checked and confirmed NOT on
disk anywhere in the repo or home directory — not orphans, don't exist;
the postcondition-gap one was already flagged missing by
ANALYSIS__postcondition-gap-review__v20260716_1512.md ("cited prior risk
memo NOT FOUND in repo"). Prior: D-05 follow-up — `PARKED_UPDATE_REPLY`
(T02 park ack) carried the same unreviewed "say yes / say no" invitation as
`_PENDING_PARK_REPLY_TPL`; removed, re-verified live; full-codebase sweep of
every reply template for user-directed invitations found no third instance.
Prior: D-18 registered (T04 instruction-leak — model confirms its own
system prompt back to the user on a D-03 gate miss); D-05 correction —
`_PENDING_PARK_REPLY_TPL` invitation removed as unreviewed scope creep,
re-verified live 5/5. Prior: I-10 rate correction (~1% → measured ~91% for
atorvastatin/seed=1); Findings registered (was orphaned). Prior: D-05 gate
two live-traced bugs fixed + D-17 (reporter regression-masking) added +
I-10 initially corrected.

This file is tracked in git. The binary files alongside it are not.
Every binary in docs/deliverables/ must appear in this manifest or it is orphaned.

---

## A. Naming Policy

All deliverables use `__v<YYYYMMDD_HHMM>` Mountain Time suffix.
Never overwrite a prior version. A new build = a new version file.
The canonical version of each deliverable is the one listed in Section B below.
Any file in docs/deliverables/ not listed in Section B is orphaned and must be named and registered or deleted.

---

## B. Canonical Deliverable Versions

| Deliverable | Canonical file | Format | Status | Last updated |
|---|---|---|---|---|
| **Prior-art candidate set — the landscape/prior-art material for patent counsel's review (HA-98, 2026-08-15).** Banked verbatim as supplied; **UNVERIFIED** and **not a legal determination** — whether any reference qualifies as prior art, and its effect under 35 USC 102/103, is for counsel. | research-market/HIP_PriorArt__candidate-set__v20260815_0949.md | md | BANKED (UNVERIFIED) | 2026-08-15 |
| **Claims Ledger (CANONICAL PROGRESS INSTRUMENT, banked verbatim from Bill's paste at HA-21, 2026-08-09).** 13 claims about what the system DOES, each with a status, its standing evidence, and a forecast timeline. **Governing rules are in the document itself and are Bill's ruling of 2026-08-07:** claims are append-only and reworded only by a superseding version with his recorded reason; only STANDING evidence counts; **status is COMPUTED, never declared, once the status generator lands**; the timeline column is forecast only and **can never influence a status or weaken an acceptance**; the public test-results page renders from the same computation and **may never exceed this ledger**; hard cap of 15 claims, so adding one retires or justifies; the claim-to-evidence map changes only by Bill's ruling and gets a periodic external sufficiency audit. **v1's statuses are CLAUDE'S DRAFT ASSESSMENT and are marked so in the document's own header** — they become computed at the generator build (filed as the named next build, NOT built at HA-21). **NOT the same instrument as `HIP_ClaimsRegister__v20260727_1729.md`**, which is a read-only AUDIT RECORD of claims the NDA package makes IN PROSE; this one is the progress instrument for what the system does. **Banked verbatim: first line `# HIP CLAIMS LEDGER`, last line `END OF LEDGER v1`, truncation-checked both ends, 13 claim rows, body sha256 `611838a9c2bbf676…`. Its `Status:` line reads `v1 DRAFT`, which is NOT one of the Naming Law's enumerated header values — flagged, not silently edited, because banked content is Bill's to reword** | HIP_ClaimsLedger__canonical-progress-instrument-13-claims__v20260809_1906.md | md | **SUPERSEDED by v2 (HA-23, 2026-08-10)** | 2026-08-09 |
| **Claims Ledger v2 — CANONICAL, the CURRENT version of the progress instrument (HA-23, 2026-08-10).** Supersedes v1 above. **Recorded reason: "Bill's status rulings, 2026-08-07 and 2026-08-09."** **Five status VALUES changed and nothing else in the claims: C-02, C-03 → PROVEN (Bill 2026-08-07); C-07, C-10 → PROVEN (Bill 2026-08-09); C-11 UNPROVEN → PARTIAL (Bill 2026-08-09).** **Claim wording is BYTE-IDENTICAL to v1** — verified column by column, which matters because the governing rules make a reword a superseding version with Bill's recorded reason, and none happened here. The eight unruled rows keep their v1 status value and gain an explicit `(draft)` marker, making per-row what v1's header said globally. Evidence and timeline cells for the five ruled rows are refreshed to the dispatches that earned the rulings (HA-19/HA-20/HA-22). **C-07 carries Bill's own separation of concerns: the CLAIM is covered, while `REQ_OFFER_MECHANISM` stays NOT MET until A1-A20 run.** **C-11's timeline is no longer a date but a condition — "after live-layer rule is set from collected run data"** — consistent with the item-12 amendment forbidding an invented threshold. **Statuses remain DECLARED, not computed: the status generator is still the named next build in `docs/BACKLOG.md` and was again not built here.** Governing rules unchanged and still carried in the document itself. Banked verbatim from Bill's paste; truncation-checked both ends (first line `# HIP CLAIMS LEDGER`, last `END OF LEDGER v2`, 13 claim rows) | HIP_ClaimsLedger__v2-bills-ruled-statuses__v20260810_0549.md | md | **SUPERSEDED by v3 (HA-26)** | 2026-08-10 |
| **Claims Ledger v3 — CANONICAL, the CURRENT progress instrument (HA-26, 2026-08-10).** Supersedes v2. **Recorded reason: "Add C-14 (Bill's wording, 2026-08-10) and restore the six dropped evidence citations."** **C-14 added at Bill's wording verbatim, status PARTIAL — Bill 2026-08-10:** *"Exact-scope offer acceptance. Once a response has been classified as an acceptance, HIP grants exactly the authority described by the offer, grants no additional authority, and only the intended member may accept it."* Evidence: HA-25's standing battery; **timeline is a CONDITION — "after the response classifier is built"** — recording the dependency HA-25 flagged. **Three dropped dispatch-ID citations restored** as the rider named them (`D-R-194`→C-08, `HA-04/HA-05`→C-05, `D-146`→C-13). **C-01..C-13 claim wording verified BYTE-IDENTICAL to v2**, column by column. **DISCREPANCY REPORTED, NOT RESOLVED SILENTLY: the rider says "six" citations and names THREE CELLS** — those three are restored; the other three cosmetic changes HA-23 counted (`REQ_STRUCTURAL_REFUSAL`→"Structural-refusal" in C-04, comma→semicolon in C-06, C-01's substantive refresh) were left untouched under the rider's own "No other wording changes." **Statuses remain DECLARED, not computed** — the generator is still the named next build. Cap 15, **14 used**. | HIP_ClaimsLedger__v3-c14-and-restored-citations__v20260810_0812.md | md | **SUPERSEDED by v4 (HA-27)** | 2026-08-10 |
| **Claims Ledger v4 — CANONICAL, the CURRENT progress instrument (HA-27, 2026-08-10).** Supersedes v3. **Recorded reason: "Add C-15 (Bill's wording, 2026-08-10)."** **C-15 added at Bill's wording verbatim, status PROVEN — Bill 2026-08-10:** *"A member's decline is control state only. It never enters the household record, embeddings, summaries, scoring, or model context, and no acceptance metrics exist."* Evidence: HA-26's 38-test standing battery. **This closes the gap HA-26 flagged** — Ruling 5's isolation had no claim covering it. **THE HEADER NOW RECORDS `CAP: 15/15 — FULL`:** the governing rules set a hard cap of fifteen and say "adding one retires or justifies", so **a sixteenth claim requires a retirement, and that is Bill's ruling, not a session's** — recorded in the ledger itself so it is unmissable at the point of adding one. **C-01..C-14 wording verified BYTE-IDENTICAL to v3**, column by column. Statuses remain DECLARED, not computed; the status generator is still the named next build. | HIP_ClaimsLedger__v4-c15-cap-full__v20260810_0848.md | md | **SUPERSEDED by v5 (HA-42)** | 2026-08-10 |
| **Claims Ledger v5 — CANONICAL, the CURRENT progress instrument (HA-42, 2026-08-11).** Supersedes v4. **Recorded reason, Bill's ruling of 2026-08-11 verbatim: "C-14: PROVEN. Its stated missing condition — the utterance-to-ResponseKind classifier — exists with the ratified v1 vocabulary, and the exact grant path is exercised end to end."** **C-14 PARTIAL → PROVEN — Bill 2026-08-11, and that status cell is the ONLY table edit in the entire document.** All fifteen claims' wording is BYTE-IDENTICAL to v4, verified by diffing the claim rows column by column; **no claim added, none retired, no other status touched.** **The cap is UNAFFECTED at 15/15 — a status change is not an addition**, so no retirement is required and none was made. **Bill's instruction was "wording unchanged, status citing this ruling; change nothing else", and it was followed literally**, which is why one thing is flagged rather than fixed: **C-14's TIMELINE cell still reads "after the response classifier is built"** — the very condition this ruling reports as satisfied. It is left VERBATIM. Per the ledger's own governing rules the timeline column is forecast only and can never influence a status, so the stale forecast changes nothing; **correcting it is Bill's call, not a session's**, and it is recorded in v5's header so it cannot be mistaken for an oversight. **Statuses remain DECLARED, not computed: the status generator is still the named next build** and `scripts/ceiling_status.py` does not read this instrument. | HIP_ClaimsLedger__v5-c14-proven__v20260811_1549.md | md | **CURRENT (v5)** | 2026-08-11 |
| Public white paper | HIP_White_Paper_Updated__v20260712_1852.docx | docx | CURRENT | 2026-07-12 |
| Public white paper (prior version) | HIP_White_Paper_Updated__v20260712_1602.docx | docx | SUPERSEDED | 2026-07-12 |
| Public white paper (prior version) | HIP_White_Paper_Updated__v20260711_2311.docx | docx | SUPERSEDED | 2026-07-11 |
| Public white paper (prior version) | HIP_White_Paper_Updated__v20260711_1830.docx | docx | SUPERSEDED | 2026-07-11 |
| Public white paper (prior version) | HIP_White_Paper_Updated__v20260708_1604.docx | docx | SUPERSEDED | 2026-07-08 |
| Confidential WP / NDA superset -- NEVER PRODUCED (2026-07-27 finding: this MANIFEST row and HIP_NDA_Package__tier1-diligence both recorded this version as CURRENT/HANDABLE on 2026-07-14, but no file of this name was ever found on disk, in this machine's git history on any branch of hip-roadmap/hip-dev, or on Google Drive under the account that produced it -- see the reconstruction row below) | HIP_WhitePaper_Confidential__v20260712_1852.docx | docx | NEVER PRODUCED | 2026-07-12 |
| Confidential WP (prior version) | HIP_WhitePaper_Confidential__v20260712_1602.docx | docx | SUPERSEDED | 2026-07-12 |
| Confidential WP (prior version) | HIP_WhitePaper_Confidential__v20260711_2311.docx | docx | SUPERSEDED | 2026-07-11 |
| Confidential WP (prior version) | HIP_WhitePaper_Confidential__v20260711_1830.docx | docx | SUPERSEDED | 2026-07-11 |
| Confidential WP (prior version) | HIP_WhitePaper_Confidential__v20260704_2142.docx | docx | SUPERSEDED | 2026-07-04 |
| Confidential WP / NDA superset -- RECONSTRUCTED (built 2026-07-27 via python-docx from the last surviving version, v20260704_2142, since the true v20260712_1852 was never produced; supersedes nothing in the chain above -- it is a NEW artifact standing in for the lost one, not a continuation of it. Applies, in order: ROUND 1 recovered verbatim from docs/deliverables/WP_PartII_TrustBoundary_DRAFT__v20260711_1800.md [Part II trust-boundary subsection, 10 paragraphs]; ROUND 2 items 1-4 recovered from commit 6f2f1d9 [item 5 excluded, superseded by Round 4a]; ROUND 3 P0/P1 recovered from commit 4b5f14d; ROUND 4 new corrections dated 2026-07-27, Bill's call -- (a) key custody rewritten to the built, proven at-rest property [per-member keys, per-fact class-sealed DEKs, four scopes as key-wrap rosters, master key destroyed, cited PS1/PS2/OB4] with the at-inference limit stated in the same breath [confidential computing not built], applied at 18 locations across the document found by full-text sweep, not just the one Part II passage; (b) Part II's MANIFEST:309 NEEDS-UPDATE distinction folded into every Round 4(a) location; (c) every voiceprint-as-identity or voiceprint-as-key-input claim corrected to device-keypair-possession, voiceprint demoted to hint/step-up signal only, 3 locations. One clearly marked placeholder inserted [Part II, after the speaker-verification paragraph] where the NDA-only speaker-verifier attack-surface paragraph belongs -- exact prose not recovered, not authored here by design, Bill to write. NOT YET PUSHED, NOT YET BILL-REVIEWED.) | HIP_WhitePaper_Confidential__v20260727_1104.docx | docx | CURRENT -- PENDING BILL REVIEW | 2026-07-27 |
| WP Part II trust-boundary draft | WP_PartII_TrustBoundary_DRAFT__v20260711_1800.md | md | INTEGRATED | 2026-07-11 |
| WP Part II trust-boundary draft (prior version) | WP_PartII_TrustBoundary_DRAFT__v20260711_1730.md | md | SUPERSEDED | 2026-07-11 |
| NDA Open Problems / Expansion Roadmap | NDA_OpenProblems__expansion-roadmap__v20260713_1100.md | md | CURRENT | 2026-07-13 |
| Debt Register NDA Appendix | HIP_DebtRegister_NDA_Appendix__v20260713_1100.md | md | CURRENT | 2026-07-13 |
| Debt Register NDA Appendix (prior version) | HIP_DebtRegister_NDA_Appendix__v20260711_2312.md | md | SUPERSEDED | 2026-07-11 |
| Ecosystem Analysis NDA | HIP_EcosystemAnalysis_NDA__v20260712_1602.docx | docx | CURRENT | 2026-07-12 |
| Ecosystem Analysis NDA (prior version) | HIP_EcosystemAnalysis_NDA__v20260707_0618.docx | docx | SUPERSEDED | 2026-07-07 |
| Ecosystem Analysis recovery record (2026-07-27 finding, docs only, no prose in HIP_EcosystemAnalysis_NDA changed: v20260712_1602 above is CURRENT/HANDABLE per this row and per HIP_NDA_Package but was never produced -- no file of that name exists on disk, in git history on any branch of hip-roadmap/hip-dev, or on Google Drive; the newest file that actually exists, business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx (commit 90a5a7d), is an unregistered orphan not listed anywhere in this table; the version this table's own chain treats as current, v20260707_0618 above, is missing the eldercare-BAA/PHI resolution and the operator-blind/consent-ledger/biometric resolution language entirely -- both blocks recovered and quoted verbatim in the recovery record, sourced from real git commits [8ca0704 propagation, 90a5a7d finalization], not reconstructed from fragments; also flags a second gap -- even v20260707_0814 lacks whatever INJ-1..7/OP-1..5 "Section 11" content the lost version apparently carried per HIP_NDA_Package's own consistency-check language; OPEN ITEM FOR BILL carried, not decided: Block 2's operator-blind paragraph needs the same at-rest-versus-at-inference scoping being applied to the Confidential WP rebuild; this row and the recovery record do NOT change the CURRENT/SUPERSEDED labels above -- that is Bill's call, per the checklist in the record itself) | HIP_EcosystemAnalysis_Recovery__version-divergence-and-missing-decisions__v20260727_1235.md | md | CURRENT | 2026-07-27 |
| Financial Annex (xlsx, live model) | HIP_FinancialAnnex__v20260713_2010.xlsx | xlsx | CURRENT | 2026-07-13 |
| Financial Annex (xlsx, prior v10) | HIP_FinancialAnnex__v20260713_1707.xlsx | xlsx | SUPERSEDED | 2026-07-13 |
| Financial Annex (xlsx, prior version) | HIP_FinancialAnnex__v20260705_2020.xlsx | xlsx | SUPERSEDED | 2026-07-05 |
| Financial Annex methodology/parameter-defense | HIP_FinMethodology__parameter-defense__v20260713_1708.md | md | CURRENT | 2026-07-13 |
| Financial Annex (docx, formatted) | HIP_FinancialAnnex__v20260702_1913.docx | docx | STALE | 2026-07-02 |
| Technical Annex (NDA) | HIP_TechnicalAnnex__v20260702_1155.docx | docx | RETIRED 2026-07-28 -- superseded-by HIP_ArchitectureForDiligence; no successor annex minted (a second live architecture doc would re-create the duplicate/phantom-document problem the Claims Register and Package Directory audits exist to kill); kept for historical record, not deleted; this docx itself untouched | 2026-07-02 |
| Architecture for Diligence (Tier-1, closes Gap 1; UPDATED 2026-07-27 DISPATCH 38 -- 8 of 11 Open Questions resolved [AW-06, learned ranker RATIFIED not pursued, proactive intelligence RATIFIED not authorized with 3 named hard gates, household phase gates RATIFIED dropped to tens-then-hundreds, training-data record moot, federated learning stubbed on the same ruling, observation-and-perception custody RESTATED as positions on record awaiting REQ_PARTITION_CUSTODY ratification]; 4 remain, incl. multi-tenancy platform posture REOPENED by an external review's shared-base-plus-adapter split of Case 3. FURTHER UPDATED 2026-07-27 DISPATCH 38a, Bill's refinement -- items 4/7/8 were closed on the wrong framing: item 4's ruling stands (retrieval rule-based, no learning on household data) but is restated as the gate at the entrance to the differentiating half of the roadmap [learned ranker, household adaptation, federated learning, proactive intelligence], not a rejection of it, gated on REQ_LEARNER_SIGNAL_ISOLATION and entered on a measured retrieval failure; training-data record [item 7] and federated learning [item 8] restored to Open Questions as gated-moat items, not resolved-by-rejection. 6 Open Questions now remain. FURTHER UPDATED 2026-07-27 DISPATCH 41 -- Section 10 rewritten from Bill's ratified vertical/world-model/multi-modal positioning (each the same governed substrate extended, not a separate bet); Open Question 2 closed. FURTHER UPDATED 2026-07-27 DISPATCH 40 (concurrent with DISPATCH 41, same working tree) -- Section 6 reframed on a two-axis spine (what is shared / who must be excluded); Case 1 corrected from request-scoping-only to software-isolated multi-tenancy over shared hardware, citing AW-01/AW-05 layer two; Case 2's superlative softened, six CC exclusions named; platform posture ratified on an interim basis (shared served model for most tenants; dedicated accelerator for operator-exclusion tenants; fractional-GPU tenant models not offered), reclosing Open Question 1; new edge-node concurrency/utilization Open Question added. Phase B (9-claim citation verification) reported outside this repo, no doc changes. 5 Open Questions now remain: observation-and-perception custody, the four-tier deployment hierarchy, training-data record, federated learning, edge-node concurrency/utilization. FURTHER UPDATED 2026-07-27 DISPATCH 42 -- Section 6 upgraded from interim to final: Case 3 split into 3A (fractional, operator trusted, MIG-backed vGPU on RTX PRO 6000 Blackwell Server Edition, productized) and 3B (fractional, operator excluded, not available, MIG/vGPU unsupported in CC mode); Case 1.5 added (shared base plus per-tenant LoRA adapters, NIM/vLLM, customization not custody); interconnect wording corrected to the specific P2P/NCCL/NVLink limits under MIG; USENIX Security 2026 "Behind Bars" MIG side-channel finding added, used to state HIP's own three-way separation of resource isolation, tenant isolation, and cryptographic confidentiality; NVIDIA's own CC threat-model exclusions attached to Case 2 by name; changelog-vs-body gap DISPATCH 41 flagged checked and found already resolved in the committed document, no content fix needed; stale numeric "Open Question 1" cross-reference retired. 5 Open Questions remain, count unchanged) | HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md | md | DRAFT -- for Bill's ratification | 2026-07-27 |
| Prototype Evidence (NDA) | HIP_PrototypeEvidence__v20260702_1615.docx | docx | STALE | 2026-07-02 |
| Tier-1 NDA Package Index | HIP_NDA_Package__tier1-diligence__v20260714_1400.md | md | CURRENT | 2026-07-14 |
| HIP build state: built, built-not-integrated, planned (UPDATED 2026-07-30 D-44: Curator Stage 2 shadow scorer MET, Bill's ruling, dated update-log block + scorer row revised; carries the honest limit that the trained regime is still CLOSED pending the deliberate operator registration act. NOTE, flagged not silently fixed: this row's date column sat at 2026-07-28 through the D-39/D-42/D-43 in-place updates to this deliverable, which did not update this MANIFEST row as the Document Governance Rule requires — D-44 is bringing it current, not claiming those updates were registered) | HIP_BuildState__built-integrated-planned__v20260729_2033.md | md | CURRENT | 2026-07-30 |
| HIP governance explainer: what it actually does | HIP_GovernanceExplainer__what-it-actually-does__v20260729_0709.md | md | CURRENT | 2026-07-29 |
| Tier-1 NDA Package Index (prior version) | HIP_NDA_Package__tier1-diligence__v20260713_1314.md | md | SUPERSEDED | 2026-07-13 |
| Governance proof (audited transcript + conformance summary) | HIP_GovernanceProof__audited-transcript__v20260714_1345.md | md | CURRENT | 2026-07-14 |
| Governance proof (prior version) | HIP_GovernanceProof__audited-transcript__v20260714_1330.md | md | SUPERSEDED | 2026-07-14 |
| Voice architecture decision memo | HIP_VoiceArchitecture__decision-memo__v20260714_2030.md | md | CURRENT | 2026-07-14 |
| Voice architecture decision memo (prior version) | HIP_VoiceArchitecture__decision-memo__v20260714_1500.md | md | SUPERSEDED | 2026-07-14 |
| Demo run-of-show (presenter script) | HIP_DemoRunOfShow__presenter-script__v20260714_2100.md | md | CURRENT | 2026-07-14 |
| Demo run-of-show (presenter script, prior version) | HIP_DemoRunOfShow__presenter-script__v20260714_1600.md | md | SUPERSEDED | 2026-07-14 |
| Harness build plan (Phase 1 — L6 record invariants; §3.3 amended 07-16, points to risk-memo item 0b for runtime G0 priority) | HIP_HarnessPlan__v20260715_1600.md | md | PENDING | 2026-07-16 |
| Defect register (D-01 through D-24 [D-03/D-18/D-17/D-19/D-20/D-22 FIXED or RESOLVED; D-21/D-23 PARTIALLY FIXED (root cause confirmed, --full residual open); D-24 NEW, NOT FIXED (medication_status over-triggering on switches, found 2026-07-17, not this dispatch's scope; main branch's own D-24 carries a later FIXED resolution roadmap's copy does not, named not ported, see HIP_RegisterReconciliation)] + D-27 [known_facts second render path bypasses the injection contract, NOT FIXED -- registered, not built] + D-28 [FIXED 2026-07-27, verified independently in code, not assumed from the REQ: strip_context_for_tier's personal-section regex now derives from FACT_BEARING_SECTION_HEADERS, all 3 fact-bearing sections covered; REQ_STRIP_CONTEXT_COMPLETENESS, commits f2deae1/95327c0/3472d1f; TD-136's broader MID/CORE question explicitly untouched, remains OPEN] + D-29/D-30/D-31 [PORTED 2026-07-27, DISPATCH 36 phase 2, from main branch D-25/D-26/D-27 (commits 767517a/a6620d4/720c94c) verbatim with lineage recorded per entry, per Bill's ruling that roadmap's numbering is authoritative; roadmap's own pre-existing D-25/D-26/D-27 [outside this file / this file] untouched] + I-06..I-10 + H-01..H-09, live) | HIP_DefectRegister__v20260715_1930.md | md | CURRENT | 2026-07-27 |
| Findings: disclosure pipeline (H-01..H-08, I-06) | HIP_Findings__disclosure-pipeline__v20260715_1900.md | md | CURRENT | 2026-07-15 |
| SIA Phase B risk memo (§9 revised: output-side exit gates first, §5.3 corrected, D-01 sequencing stated, voice-path + P2/i019 costs) | HIP_SIA_PhaseB__risk-memo__v20260716_1624.md | md | CURRENT | 2026-07-16 |
| SIA Phase B risk memo (prior version — input-side-only sequence) | HIP_SIA_PhaseB__risk-memo__v20260716_0800.md | md | SUPERSEDED | 2026-07-16 |
| Member isolation crypto design (partition, per-member keys, operator-blind-at-rest, threshold recovery, migration) | HIP_MemberIsolation__crypto-partition-and-recovery-design__v20260718_1117.md | md | PLAN (design only, nothing built) | 2026-07-18 |
| Member isolation dyad custody model (extends the crypto design: dyad as crypto unit, custodial keys for keyless care-recipients, atomic entry/exit + re-encryption, non-cooperative eviction via the recovery quorum, overlapping dyads, custody transfer/dissolution) | HIP_MemberIsolation_Dyads__custodial-crypto-entry-exit-overlapping__v20260718_1207.md | md | PLAN (spec only, nothing built) | 2026-07-18 |
| **HIP Finish Plan — PLAN OF RECORD for finishing the project (HA-37, 2026-08-11). Banked VERBATIM from Bill's source text: same wording, order and list structure, nothing added, removed, reordered, summarised or corrected; all 240 source prose lines verified present unchanged, and only the header is not Bill's.** Three finish lines in order — demo, core product, proof package — then a 14-step sequence, each step carrying its own finish condition. Supersedes `HIP_Roadmap__complete-sequence__v20260718_1600.md`, which is retained unaltered and marked SUPERSEDED with its prior status left visible. Its closing finiteness rule was landed in the same dispatch as STANDARD PREAMBLE item 12, so it binds every session rather than only readers of this file. Plans only: builds nothing and rules nothing MET. **AMENDED BY the HIP Trust Boundary Roadmap (HA-50, 2026-08-12), which INSERTS five egress/identity/authority phases rather than forking this plan; this plan is NOT superseded.** | HIP_FinishPlan__three-finish-lines-14-steps__v20260811.md | md | **PLAN OF RECORD (amended)** | 2026-08-11 |
| **HIP Trust Boundary Roadmap — five phases over egress, identity and authority (HA-50, 2026-08-12). AMENDS the Finish Plan; does NOT fork it — it INSERTS.** Banked VERBATIM from Bill's dispatch text under a governance header. Written from an external review (ChatGPT coordinator memo + Claude verification against source) that found **four egress/identity findings in the hip-vo checkout, all verified in source 2026-08-12**: (1) `/api/decrypt` and `/api/reset` on `voice_https_orch` have **NO auth**, decrypt returns member+household **plaintext**, the server binds **0.0.0.0**, `/api/text-query` trusts a caller-supplied member on both servers, and `_build_requester` **falls back adult/full on registry miss**; (2) the typed-query path sends mid/core messages to Groq **without the strip the live path applies**, while config says `groq_is_onnet: false`; (3) `fact_change` re-reads and decrypts the **full owner+household set** and sends it to Groq on declarative turns — *"encode is not disclosure"* is **wrong from an egress standpoint** — originally done for TD-121 (a partial block dropped writes 7/8), so the real fix needs a design ruling; (4) `build_payload` receives facts, not principal/authority, so **consent is evaluated and authority is not**. **PHASES 0-1 ARE DEMO-PHASE** (privacy-unsafe, inside the VD-40 freeze criteria); **PHASES 2-4 ARE CORE-PRODUCT-PHASE** and absorb work already sequenced on the roadmap branch (R2 permit, ceiling audience axis). Phase 0 stops the exposure; Phase 1 is egress correctness behind ONE gateway with an AST build check; Phase 2 is one authenticated principal established by the system and **never the request body**; Phase 3 separates authority from consent and **PORTS R2 permit + ceiling audience axis rather than rebuilding them on hip-dev**; Phase 4 proves it and trues up any ledger claim standing above its evidence. **Each phase carries its own DONE condition.** **No new REQ per phase** — each names its governing REQ before code (Phase 0 = `REQ_SECURE_DEV_ENDPOINTS`, already filed). **Builds nothing and rules nothing MET.** | HIP_TrustBoundaryRoadmap__five-phase-egress-identity-authority__v20260812.md | md | **PLAN** | 2026-08-12 |
| HIP Roadmap: complete sequence (plan of record for the confidentiality + truthfulness builds; identity binding as the shared root; Stage 0-5 sequence; decisions made/open; branch rules; 8-item honest-limits section) | HIP_Roadmap__complete-sequence__v20260718_1600.md | md | SUPERSEDED 2026-08-11 by the Finish Plan (HA-37); was PLAN OF RECORD (sequencing doc, builds nothing) | 2026-07-18 |
| Audit: master key findings (D-26 confirmed -- installed launchd job resolves to a different master-key file than the harness default; 2 distinct key files exist by truncated hash; plist's master-key variable is a path, not an embedded value; full inventory held locally at ~/hip-audit, not committed; no destroy target named or recommended) | AUDIT_MASTER_KEY_FINDINGS__d26-launchd-vs-harness-key-divergence__v20260722_1529.md | md | BUILT | 2026-07-22 |
| Crypto Stage 4 Phase 3: operator-blind at rest -- MET, all three parts (a: zero v1 facts; b: no write path can produce v1, OB4, MET 2026-07-22; c: master key destroyed Bill-authorized 2026-07-26, backed up first, N5/R7 proven directly against all 12 live facts twice [12/12 fail via master path -- no key exists at all; 12/12 open via real class keys with zero master key present]). PS1-fault-injection/PS2-fault-injection/PS3/PS4 RETIRED per Bill's decision (v1-simulation fixtures, now categorically impossible to construct); PS1/PS2's own v2-sealing checks kept; successor OB6 built (tier=ABSOLUTE: no master-key file exists + v1 construction raises); OB5's own second check reworked to be checkout-agnostic. --layer 7 verified clean (23/23, 13-row 13/13, OB4/OB5/OB6/G0 all PASS, no regression -- exit 2 not 1); the sole remaining new-failure (AUDIT:four-part-roster) belongs to REQ_HARNESS_DISCIPLINE's own registry, not touched. --full's two apparent regressions (L2:reveal_demo.R04, L4:PW012) traced via code (zero functional path from harness.encryption to the write/detect/generate pipeline) and confirmed flaky via isolated retry, not caused by this REQ. Demo confirmed untouched throughout | requirements/REQ_CRYPTO_P3_OPERATOR_BLIND__stage4-phase3__v20260724_1129.md | md | MET | 2026-07-26 |
| Demo dashboard migration: retire pre-partition write path (scope only -- moves ~/hip-dev's demo checkout off harness.encryption's unconditional master-key seal and onto roadmap's already-MET dyad/class-sealed model; filed as its own scheduled job, explicitly not a blocker on REQ_CRYPTO_P3_OPERATOR_BLIND; two paths named, undecided, no acceptance test yet pending Bill's choice) | requirements/REQ_DEMO_DASHBOARD_MIGRATION__retire-demo-master-key-migrate-to-partition-write-path__v20260724_1129.md | md | NOT MET | 2026-07-24 |
| Weekly design digest, CURRENT (Bill's running design note, newest week on top; "week of 2026-08-04" added D-153 -- SILENT ABSORPTION named as a failure mode distinct from unbuildable: four representation classes the classifier cannot produce are not refused but ABSORBED, three stamped HEALTH_CLAIM and the fourth SCATTERED across whichever class the attribute yields, so the system cannot say where its instances went; R2 enforced at the single materialization point yet ruled NOT MET on a scope gap, with R5 found to hold VACUOUSLY BY ABSENCE and unmonitored -- 'no code does X' is a finding with a shelf life; what a lock must be to count as one (kernel refusal, keyed on the RESOURCE not the checkout, acquisition a precondition of the tooling rather than a step, since both late-takes were committed by sessions that knew the rule); an unconfigured checkout made to FAIL rather than fall back to an unowned instance, and a port collision removed by SUBTRACTION; a status board whose empty parse must fail rather than render a clean page, with UNDETERMINED as a counted outcome, which then found three defects in the documents and was taught to check its own LIVE claim -- exposing a VISIBILITY gap distinct from a coverage gap; and one root cause behind three memory-harness symptoms, two correct mechanisms interacting) | HIP_DesignDigest__weekly__v20260804_0639.md | md | CURRENT | 2026-08-04 |
| Weekly design digest, week of 2026-08-03 (SUPERSEDED by v20260804_0639; content retained in the successor, which is cumulative -- newest week on top) (Bill's running design note, newest week on top; "week of 2026-08-03" added D-137 -- the structural-refusal guarantee that protected only subjects the requester could already see, so protection scaled with visibility, and the resolution-is-not-disclosure split that fixed it; the model-cooperation finding, its wrong first headline, and what four dispatches cost to establish its width, including a scenario that was zero of thirty-one rows; classification is not wiring -- an orphaned disclosure oracle referenced by no runner, and sixteen honestly UNWRITABLE acceptance rows; and the velocity instruments: ratchet plus accepted-red baseline, fault twins and anti-vacuity as convention, trace-before-build as a gate, corrections that land as records, and a count is a claim that ages while a pointer is not) | HIP_DesignDigest__weekly__v20260803_1602.md | md | SUPERSEDED | 2026-08-03 |
| Weekly design digest, week of 2026-08-01 part 2 (SUPERSEDED by v20260803_1602; content retained in the successor, which is cumulative -- newest week on top) (Bill's running design note, newest week on top; "week of 2026-08-01 part 2" added D-88 -- the architecture boundary. Records that the monolith ruling STANDS but that the boundary exists in no running process, so the core is named a REFERENCE MONITOR whose target property is COMPLETE MEDIATION and which does not have it today; the policy-chain-vs-privilege-separation distinction, with INJ-7 being disabled by default as the tell; the ruled threat model and its consequence that three of four in-scope adversaries defeat an in-process boundary in CPython, careless code being the only one it stops, with the operator DEFERRED not dismissed; voice untrusted by construction regardless of vendor, its two hard rules, and the belt-and-suspenders identity ruling whose contract consequence has a freeze deadline; the audit being tamper-evident against nobody with anchor-don't-split as the cheap fix and the anchor-vs-separate ruling NOT made; models propose and only the core commits, with the two ungated model-output-to-write paths; the acceptance-plan audit finding 3 of 30 rows wired and A11's rationale false; and earned calibration keyed on validated correctness rather than usage. Cumulative -- carries the week of 2026-08-01 part 1 and the week of 2026-07-25 unchanged. Traceability table verified with `git log --diff-filter=A`) | HIP_DesignDigest__weekly__v20260801_1214.md | md | SUPERSEDED | 2026-08-01 |
| Weekly design digest, week of 2026-08-01 part 1 (SUPERSEDED by v20260801_1214; content retained in the successor, which is cumulative -- newest week on top. Carried consent, authorization, and the dimensioned ceiling, with a traceability table citing every artifact filed that week by path and landing hash) | HIP_DesignDigest__weekly__v20260731_2140.md | md | SUPERSEDED | 2026-08-01 |
| Weekly design digest, week of 2026-07-25 (SUPERSEDED by v20260731_2140; content retained in the successor, which is cumulative -- newest week on top. Originally committed 2026-07-26 morning without registration, orphan fixed same day) | HIP_DesignDigest__weekly__v20260725_1400.md | md | SUPERSEDED | 2026-07-26 |
| G0 output-side fabrication backstop REQ (BUILT and MET -- runtime reply gate [risk-memo 0b, scoped to reply_source=="model"] + layer-7 ABSOLUTE-tier standing invariant [HarnessPlan 3.3, L7 25/25->26/26]; closes G1's subjects=[] blind spot; all 4 acceptance items evidenced live incl. a real monkeypatched-model fabrication caught and a grounded reply passing untouched; full --full RATCHET PASS; gates the truth track and the context-arch learning half per the ContextArch reconciliation STEP 4) | requirements/REQ_G0_OUTPUT_INVARIANT__output-side-fabrication-backstop__v20260726_0735.md | md | MET | 2026-07-26 |
| Context & interaction architecture reconciliation: master-plan diff (analysis only, ratifies nothing; 50 rows -- ALREADY RATIFIED 10 / CONSISTENT EXTENSION 31 / CONFLICTS 2 / NEW DECISION 7; 7 false/stale current-behavior assertions with file:line; STEP 4 governance verdict: learner-never-overrides-authorization is ratified law and current dataflow fact but not a machine-checked property -- G0 + prompt-subset-of-admitted invariant + training isolation required before any learned ranker; proposal itself filed verbatim at docs/design/HIP_ContextArch_Proposal__context-interaction-intelligence__v20260726_0710.md) | HIP_ContextArch_Reconciliation__master-plan-diff__v20260726_0710.md | md | BUILT | 2026-07-26 |
| HIP Level of Effort: build to done (estimate only, nothing built; near-term both tracks to provable under 1 week = 3-4 sessions [G0 output invariant, #5 part (c), two conflict amendments]; context-architecture new roadmap = 15-20 sessions past crypto close, gated on G0 built + prompt-subset-admitted invariant + 3 of 7 open decisions; 20-30% buffer added; bottom line: confidentiality + truth demonstrable within a week, full architecture is a quarter not a sprint) | HIP_LOE__build-to-done__v20260726_0801.md | md | PLAN | 2026-07-26 |
| Harness discipline REQ: four-part check standard + sprint gate (REQ only, no code; every harness check needs fault-injection twin + ground-truth fixture + coverage entry + metamorphic wrapper before it counts as MET; standing rule re-asserted at sprint start, twin-less merges are a FAIL of this REQ; 4-part acceptance incl. an audit script on --full that rosters every L7 check, rejects twin-less additions, and passes PS1/PS2/OB4/OB5/G0/G1/G4 as reference implementations; known gaps named, TD-132/TD-122 stay open -- zero hidden gaps, not zero gaps -- MET 2026-07-26: blocking care_coordination.T01/T02 Groq 400 cleared by REQ_GROQ_CALL_RESILIENCE at d83a111, --full re-run RATCHET PASS, AUDIT 3/3, T01/T02 PASS, one pre-existing unrelated flake (L1:P2 i019) not a regression) | requirements/REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827.md | md | MET | 2026-07-26 |
| Groq call resilience REQ: fact_change reasoning-overrun fix (fixes json_validate_failed via gpt-oss-20b reasoning-token overrun starving the content slot, root-caused in DISPATCH_GROQ_400_ROOTCAUSE; shipped at d83a111 -- max_tokens raised 2048->8192 [kept], jittered temperature-0.2 retry on json_validate_failed specifically, resp.text now logged in the retry warning; reasoning_effort:"low" tried and REVERTED same session -- broke park-path update->add semantics, regressed P10/HARNESS1.3/R04/PW012, produced one G1 HARD ZERO under --full, so that specific acceptance item does not hold, by design; --layer 7 then --full both RATCHET PASS with care_coordination.T01/T02 green -- this REQ's bar and REQ_HARNESS_DISCIPLINE's last blocker cleared in the same run) | requirements/REQ_GROQ_CALL_RESILIENCE__fact-change-reasoning-overrun-fix__v20260726_1438.md | md | MET | 2026-07-26 |
| Testing best-practices research (comparison memo: HIP harness vs published practice for LLM systems + privacy-critical/crypto code; per-technique ahead/behind/adopt verdicts -- ahead on discipline [red-on-command twins, mechanical hard-zero tier, four-part audit, destroyed-key negative test, runtime G0 gate, record invariants], behind on generation and scale [no property-based generation, hand-written variant sets, declared-not-measured coverage, no auto red-team, literal-substring canary per TD-132, no Wycheproof-style boundary vectors]; 7-item prioritized TD-133 adoption list [CheckList templates + Hypothesis, semantic canary, Wycheproof X25519/Fernet boundary vectors, mutation score, coverage measurement, trend rendering, opt-in auto red-team]; ~25 sources cited) | HIP_TestingBestPractices__research__v20260726_1005.md | md | BUILT | 2026-07-26 |
| Coverage measurement REQ: coverage metric + mutation score (scope only, no code; turns the four-part audit's coverage entry from declaration into measurement -- exercised-cells derived mechanically from fixtures over the role x scope x attribute x intent grid, invalid cells excluded from the denominator and listed, uncovered valid cells printed on --full, declared-vs-measured discrepancies flagged per check, fraction ratcheted; plus a mutation-score metric over the gate predicates [injection_contract, write_rule, g0_invariant, record_invariants] -- in-memory mutants, killed/survived per module, survivors file:line = untested gate logic feeding the TD-133-style burn-down; 8-item pass/fail acceptance incl. both metrics' own fault-twins and a no-silent-disappearance rule for survivors; closes the research memo's "audit verifies existence, not strength" + "coverage declared not measured" findings, adoption items 4+5. OPEN ITEM 2026-07-26 (later still, docs only): acceptance item 7's no-silent-disappearance rule cannot run -- no survivor output file exists anywhere in the repo; mutation_score.py prints survivors but does not persist them to a trend-comparable file) | requirements/REQ_COVERAGE_MEASUREMENT__coverage-metric-and-mutation-score__v20260726_1224.md | md | MET | 2026-07-28 (per DISPATCH_44 -- both previously-outstanding items closed: illustrative-example discrepancy resolved 24948b9, --full run verified at /tmp/hip_harness_20260728_0514.log, all 8 acceptance items evidenced; see REQ doc's own UPDATE) |
| HIP Operations Runbook (docs only, operational reality separate from the REQ docs and the plan of record; covers the two-machine setup [the mini runs all real work, battery-powered, can die mid-run; the laptop has no working stack and must SSH over], the mandatory whoami/hostname/branch check before running anything, the worktree list, the venv path, the two graphs [7688 roadmap / 7689 demo] and two Ollama daemons [never kill either, TD-129], the TD-129 memory-pressure --full killer, the lean-then-full gate sequence, and a standing secrets note on the dead OpenAI key in .env.dev history) | deliverables/HIP_OperationsRunbook__how-to-run__v20260726_1606.md | md | CURRENT | 2026-07-27 |
| Prompt/record fidelity REQ: layer-7 prompt is a subset of record.admitted[] — SUPERSEDED 2026-07-27 by REQ_PROMPT_RECORD_FIDELITY__factid-set-parity-prompt-vs-admitted__v20260726_1717.md, retained for history (scope only, no code; every harness assertion today -- G0/G1-G4, INJ-1..7 discrepancy checks -- asserts against the RECORD, and admitted[] is a self-report the assembled prompt is never checked against; a leak of an unadmitted fact into the actual model-facing prompt [stale cache, bad merge, Seam-A splitting error] is invisible to every existing check; acceptance: ABSOLUTE-tier hard-zero check wired unconditionally into layer7_crypto.py run() [G0's pattern], compares assembled prompt against record.admitted[] per generation turn, fault-injection twin, ground-truth fixture [alice/bob/mary], coverage entry, metamorphic wrapper, full RATCHET PASS before/after; precondition (ii) of three for the context-arch learned ranker per HIP_ContextArch_Reconciliation STEP 4 -- G0 is (i), MET; (iii) learner/training-signal isolation has no REQ yet) | requirements/REQ_PROMPT_SUBSET_ADMITTED__layer7-prompt-record-fidelity__v20260726_1617.md | md | SUPERSEDED | 2026-07-27 |
| Prompt/record fidelity REQ: fact-ID set parity between assembled prompt and record.admitted[] (operationalizes REQ_PROMPT_SUBSET_ADMITTED via a read-only code trace -- record.admitted[] traces to injection_result.allowed [epistemic_record.py:184, fact_id-bearing] but the prompt is built from a SEPARATELY REBUILT local admitted variable [voice_orch.py:2550, 2569-2578] filtering other_subject_facts and rewriting dicts on declarative turns -- two distinct objects by destination; acceptance: local_system_prompt [orchestrator.py:363-375, 408-420] returns the fact_ids it rendered instead of discarding them at format time [orchestrator.py:368, :412], new field record.prompt_fact_ids populated only from that return value never from prose, capture point voice_orch.py:3224 [text path], check compares fact_id SETS by ID/set membership asserting the SUBSET invariant, positive case must PASS + negative case (a prompt-only fact_id) must FAIL naming the id, full RATCHET green before/after; EXPLICIT NON-GOAL: voice-path conversation history [voice_orch.py:1976-2011] not covered -- needs its own REQ [REQ_VOICE_HISTORY_DISCLOSURE_LEDGER, proposed, BACKLOG entry filed]; also names the known_facts bypass [orchestrator.py:376-402, currently neutralized] as a second render path to cover if re-enabled -- UPDATED 2026-07-27: hot_context named as a fourth uninstrumented render site [orchestrator.py:344,374-375], verified inert on BOTH text and voice paths [server/voice_orch.py has exactly one `store =` assignment in the file, :2218, _NoopStore(); BUILD-1 routes voice through the same assemble_governed_context() the text path uses, :1722 vs :3054, which builds its own fresh _NoopStore() at :2500-2501], correcting REQ_PROMPT_SUBSET_ADMITTED's retained "live on the voice path" note -- UPDATED 2026-07-27 (MET): items 4-6 narrowed by Bill's decision from bidirectional set parity to the subset invariant actually built [harness/prompt_fidelity_invariant.check_psa1:35-45, prompt_fact_ids ⊆ admitted_fact_ids] -- a record-only fact_id is under-disclosure not a leak, and equality would false-positive on max_facts truncation; reverse direction filed separately [BACKLOG row 50 / REQ_PROMPT_COMPLETENESS, proposed]; all 7 items MET with evidence inline; discipline audit confirmed on L7:PSA1 by name [coverage/fixture/metamorphic/twin all ok]; fifth gap named: the fault-injection twin [layer7_crypto.py:1395-1427] is proven against a synthetic local_system_prompt call, not the real assemble_governed_context/declarative-turn rebuild end to end; L7 24/24, AUDIT 3/3, RATCHET PASS; the five named gaps are stated scope limits, not unmet acceptance items) | requirements/REQ_PROMPT_RECORD_FIDELITY__factid-set-parity-prompt-vs-admitted__v20260726_1717.md | md | MET | 2026-07-27 |
| Learner/training-signal isolation REQ: a learner must never train on, or read, anything the requesting identity is not authorized to see (scope only, no code; precondition (iii) of three for the context-arch learned ranker per HIP_ContextArch_Reconciliation STEP 4 -- G0 is (i) MET, REQ_PROMPT_RECORD_FIDELITY is (ii) MET 2026-07-27, this is (iii), which STEP 4 itself says "no REQ exists -- needs one"; Bill's words: training signal is subject to the same partition as retrieval, a ranker that learns across households or scopes is a leak with a delay; grounded in STEP 4 gap 3 [training-signal isolation exists nowhere -- nothing guarantees a learner's reward is computed only on post-gate outcomes, that gate decisions are excluded from its feature/gradient space, or that household personalization weights cannot reach gate inputs] and row 6(iii) [ranker placed so it can only NARROW the authorized candidate set, never source outside it]; acceptance drafted in the REQ_HARNESS_DISCIPLINE four-part shape -- ABSOLUTE-tier hard-zero layer-7 check wired into layer7_crypto.py run(), fault-injection twin [cross-household/cross-scope training-signal pooling], ground-truth fixture [alice/bob/mary extended with a second household], coverage entry over the four ratified scopes (RI1) x household-boundary crossings, metamorphic wrapper, full RATCHET PASS before/after; no learner/ranker/reward/gradient code exists anywhere in this codebase today -- this REQ's check is a standing refusal gate wired before any learner is proposed; does NOT authorize building a learned ranker [row 16's own NEW DECISION REQUIRED]; four OPEN QUESTIONS carried for Bill, not decided here: row 6(iii)'s retrieval-time scope-ownership, row 31's training-record crypto-class/retention/identity-form, row 16 itself, and whether intra-household cross-scope pooling is the same violation class as cross-household pooling) | requirements/REQ_LEARNER_SIGNAL_ISOLATION__training-signal-partition-parity-with-retrieval__v20260727_0828.md | md | NOT MET | 2026-07-27 |
| Turn pipeline diagram (one-page SVG, 9-stage text-path pipeline -- turn arrival, intent classification, subject resolution, injection contract, key-class fact opening, prompt assembly, model generation, output check, record write -- paired against what watches each stage: INJ-1..7 discrepancy checks, PS1/PS2/DK1-4/OB4/OB5, PSA1, G0; every file/check label verified against roadmap branch code [harness/orchestrator.py, injection_contract.py, g0_invariant.py, prompt_fidelity_invariant.py, partition_crypto.py, subject_resolution.py, intent_classifier.py, eval/harnesslib/check_registry.py] before commit; two drift corrections made during verification: PSA1 box read "Built, not yet run" -- corrected to "Built and wired in" [check_psa1 is a registered Scenario with fault-injection twin, ground-truth fixtures, and metamorphic wrapper, runs under --layer 7/--full today; only the specific known_facts bypass it backstops, D-27, has no live turn exercising it]; PS1/PS2/DK1-4/OB4 box was missing OB5 -- added [OB5 is the check that actually verifies the destroyed-master-key state; PS1/PS2's own fault-injection twins were retired 2026-07-26 per REQ_CRYPTO_P3_OPERATOR_BLIND {v1-simulation fixture now categorically impossible}, PS3/PS4 removed outright, OB6 built as their named successor]) | HIP_Diagram_TurnPipeline__what-happens-on-one-turn__v20260726_1940.svg | svg | BUILT | 2026-07-26 |
| Package directory (AUDIT RECORD, read-only, changes no prose: 49-row inventory of the Tier-1 NDA package + supporting set + the ten gated site pages, one row per document, cross-referenced against this file / docs/INDEX.md / docs/rendered/ / `git log --all`; docx content read from docs/rendered/ renderings, not parsed directly; FINDING beyond the already-known WP-Confidential gap -- the same claimed-CURRENT/SUPERSEDED-but-not-found pattern recurs for 3 more Confidential-WP chain versions, the Ecosystem Analysis NDA's own claimed-CURRENT file, and the ENTIRE public White Paper chain from v20260708_1604 onward [5 versions] -- 9 total MISSING rows, none checked against Drive; also found HIP_FinModel_ReviewMemo has an INDEX row but no MANIFEST row, and 4 real on-disk files [3 business/ecosystem Ecosystem Analysis drafts + the real newest public WP] registered nowhere) | HIP_PackageDirectory__v20260727_1716.md | md | AUDIT RECORD | 2026-07-27 |
| Claims register (AUDIT RECORD, read-only, changes no prose: 18-claim register of every load-bearing claim the NDA package makes about what HIP is or does -- 5 seeded by Bill, 13 found independently; docx content read from docs/rendered/ renderings, ten gated site pages fetched live from hip.olindasolutions.com/d-7h4k2m9x/; STATUS PROVEN/DESIGNED/ASPIRATIONAL/WRONG/UNVERIFIED per claim, ratified truth named where the package's own reconstructed Confidential WP already states it correctly; confirms WRONG voiceprint-as-identity, retrieval-not-storage scoping [real enforcement is write-time key-wrap/class-sealing], Groq-hosted-inside-the-enclave category error, a fabricated confidential-computing benchmark figure [WP's own Part XIII: "not running fact, today"], 10-vs-11+ canonical-attribute staleness, and a 4-vs-5-tier inconsistency between the Technical Annex and its own companion Prototype Evidence doc; NEW FINDING -- a located code gap in harness/orchestrator.py's strip_context_for_tier, the "Confirmed facts about other people" cross-member section is not covered by the personal-section-stripping regex, substantiating Bill's seeded CLAIM-04 [kept DISPUTED, his word]; also names, without silently fixing, that HIP_PropagationWorkOrder is not literally in build_nda.js [it's in the tech-debt register + build_fin_chg5_risk_opex.py; build_nda.js names a sibling never-filed HIP_FinalizationOrder instead] -- both already found by HIP_EcosystemAnalysis_Recovery, corroborated not duplicated) | HIP_ClaimsRegister__v20260727_1729.md | md | AUDIT RECORD | 2026-07-27 |
| Architecture Weakness Register (PORTED from main 4390240, 2026-07-27, DISPATCH 35 phase 1 -- did not exist on roadmap before this. AW-01..AW-05 content unchanged from main; cross-reference header rewritten, naming TD-136 [roadmap's renumbering of main's TD-131] instead of main's TD-131; LATEST_ symlink created matching main's convention. UPDATED 2026-07-27 DISPATCH 38: AW-06 added [detection signatures for KV-cache prompt extraction, specifying AW-05's layer-three defense in full, status SPECIFIED NOT BUILT], closing HIP_ArchitectureForDiligence's Open Question 1. See HIP_RegisterReconciliation for the full audit this port executes against) | HIP_ArchitectureWeaknessRegister__v20260722_1536.md | md | LIVE | 2026-07-27 |
| Register Reconciliation: cross-branch ID collisions (AUDIT RECORD + phase-1/phase-2 action log, DISPATCH 35+36 -- Bill's ruling adopted: roadmap's numbering is authoritative, ports renumber. Full audit of BACKLOG.md/DEBT_REGISTER/HIP_DefectRegister/HIP_ArchitectureWeaknessRegister/docs-INDEX/MANIFEST against main d4a8a90: collision set TD-131 + D-25/26/27 [quoted both versions] + D-24/TD-122 status-only staleness; per-register only-on-one-branch ID counts; highest-ID table; full citation-break list; renumbering map. Phase 1: REQ_PROMPT_SUBSET_ADMITTED's dangling BACKLOG:77/TD-131/BILL-7 citation repaired; BACKLOG row 49's TD-135 reservation retargeted to TD-137; AW register ported. Phase 2 (DONE, this update): main TD-131/D-25/D-26/D-27 filed for real as TD-136/D-29/D-30/D-31 with lineage recorded in each entry; AW register's TD-136 cross-reference confirmed real; D-28 independently verified fixed in code (not assumed from the REQ) and status updated with the verification record. Phase 3 (not done, main untouched): full list of main-side files still citing the old numbers, scoped in the doc's own Section 8. No branch merge performed or implied) | HIP_RegisterReconciliation__cross-branch-id-collisions__v20260727_1930.md | md | PLAN OF RECORD | 2026-07-27 |
| Pitch, full (v2) — the investor/technical narrative. FIRST BANKING on any ref, 2026-08-05: no prior version of this deliverable exists in this table, in docs/INDEX.md, or on any branch, so this row supersedes nothing and opens no chain. Twelve parts — the need-to-know / read-in master frame; the four governance pieces (briefing packet, nurse's licence, evidence room, pharmacist); the ten-step trace of one turn; the pattern layer and its metadata-only property; the learner that does not exist and the isolation check built ahead of it; storage (sealed envelope with a readable outside, the superintendent's master key and its self-regeneration blocker, the safe-deposit-box limit at inference, the keyless person and the two-person key structure); routing and what leaves the house; the five modes and why two are live; build-vs-rent-vs-deliberately-not-built; the two anchor stories (the mislabelled-sensitivity leak, the asking problem); the advantage argued with its own counter-argument; and a four-way PROVEN / BUILT-PROOF-NOT-ACCEPTED / DESIGNED-OR-RULED / OUT-OF-SCOPE recap plus a breaking-point appendix. STATUS LABELS RECONCILED TO REQ_STRUCTURAL_CEILING §16 AS OF 2026-08-05; THE NARRATIVE ITSELF IS UNVERIFIED and neither this row nor the document's header claims otherwise. The §16 check performed at banking: 30 requirements defined (R1–R30); 11 currently ruled MET (R1, R2, R8, R10, R11, R12, R16, R17, R18, R29, R30); none currently NOT MET, every NOT MET entry in §16 being marked historical; 19 with acceptance not run — which is what the document's Part Eleven asserts. Its "six items moved in the two days before this version" matches §16's six 2026-08-05 rulings (R2, R8, R10, R11, R16, R17). Its care-team "formally marked as not met" line resolves to REQ_CARE_TEAM_READ_AUTH, NOT MET per that REQ's own header and INDEX row — a separate REQ outside the ceiling's 30, so it does not contradict §16's none-currently-NOT-MET picture. Body byte-identical to the source apart from the five inserted house-header lines, verified by diff. Symlink LATEST_HIP_Pitch.md | HIP_Pitch__full-v2-claim-governance-storage-routing-and-advantage__v20260805_1528.md | md | BUILT | 2026-08-05 |
| Pitch, 15-minute timed script. FIRST BANKING on any ref, 2026-08-05; supersedes nothing and opens no chain. A timed script rather than a summary (~2,000 spoken words, blocks from 0:00 to 14:30 with a 30-second close): every topic from the full pitch appears with the detail stripped and the breaking points kept, each block carries its own status label, and a CUT LIST at the bottom names what was dropped and where to reach in the full pitch if the room asks — including the explicit instruction to verify the confirmation channel's current wiring before claiming it. STATUS LABELS RECONCILED TO REQ_STRUCTURAL_CEILING §16 AS OF 2026-08-05; NARRATIVE UNVERIFIED. Its headline number — thirty requirements, eleven proven, none failing, nineteen never run — matches §16 exactly at banking time (same check recorded on the row above). COMPANION to HIP_Pitch, not a successor: both are CURRENT/BUILT simultaneously and neither supersedes the other, which is why they carry two separate LATEST_ symlinks. Body byte-identical to the source apart from the five inserted house-header lines, verified by diff. Symlink LATEST_HIP_Pitch15Min.md | HIP_Pitch15Min__timed-script-with-cut-list__v20260805_1528.md | md | BUILT | 2026-08-05 |
| Offer mechanism REQ: governed initiation of new authority (FIRST BANKING on any ref, 2026-08-06, D-R-195 — no prior version of this REQ exists in this table, in docs/INDEX.md, or on any branch, so this row supersedes nothing and opens no chain). Bill's revised text FILED VERBATIM: body copied, not retyped and not summarised, every line from the first `---` onward byte-identical to the source (body SHA-256 `3bb8dc3a…`, `diff` clean); only the header block differs — Status replaced, `Reconciled-Against` added, prior header wording quoted inside the new one rather than discarded. Governs the ONE path by which HIP may initiate a request for authority it does not already hold: three initiation classes and no fourth (AUTHORIZED_OPERATION, AUTHORIZED_SAFETY_INTERRUPT, OFFER), the trigger registry as sole eligibility source importing its four material-change kinds UNCHANGED, one situation → one pre-approved minimal authority delta spent on first delivery, template and delta bound as one versioned immutable object with no generative or A/B surface, explicit response only, and a decline held as control state that may never become a fact about the member. 6 RULINGS, R1-R25, A1-A20 at ABSOLUTE tier, 6 NAMED LIMITS the REQ states against itself (incl. that it cannot prove the four imported change kinds are complete, and that fixed wording prevents adaptive persuasion but not bad policy). **DRAFT-RATIFIED-PENDING, and that is a real state, not a soft MET:** the text is Bill's, but FORMAL RATIFICATION IS THE FUTURE D-R THAT LANDS STEP 1 of the REQ's own LANDING ORDER (§12), not this filing. Nothing built, no code touched, **A1-A20 unattempted**. **`REQ_STRUCTURAL_CEILING`'s solicitation section was deliberately NOT touched** — the `Supersedes:` header states the intent, and the REQ's own §12 step 9 orders that swap only after A1-A20 run. | requirements/REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1320.md | md | DRAFT-RATIFIED-PENDING | 2026-08-06 |
| ChatGPT key-lifecycle review — custody, destruction, rotation (FIRST BANKING on any ref, 2026-08-06, HA-12; supersedes nothing, opens no chain). **One external model's opinion, NOT a ruling, and NOT ONE CLAIM VERIFIED against this codebase.** Banked from Bill's inline paste after HA-10 and HA-11 both stopped on a file that never existed; those failures are preserved on the record. Truncation check run twice — on the paste and on the written file — both boundaries PASS; body SHA-256 `b6a6fb82…`. Thesis: do not enable crypto-erasure against real household data under file-based key custody, because the erasure claim is only as strong as the ability to account for every recoverable copy of the target key (NIST SP 800-88r2); names seven gates before real-data erasure, and argues that derived artifacts readable without the owner key make key destruction PRIMARY-RECORD crypto-erasure only — independently corroborated by HA-10's own measurement on subject `dad`. NOT in scope of the Document Governance Rule's MANIFEST-check (that rule governs WP-to-research reconciliation, which review docs do not participate in); registered here per HA-12 item 3. | reviews/CHATGPT_KeyLifecycle__custody-destruction-rotation__v20260806.md | md | BANKED — UNVERIFIED | 2026-08-06 |
| **Bill's key-lifecycle RULING — three rulings** (FIRST BANKING on any ref, 2026-08-06, HA-13; supersedes nothing, opens no chain). **AUTHORITATIVE, not a review** — it shares `docs/reviews/` with the ChatGPT key-lifecycle opinion per its own Ruling 1, and the two carry opposite authority; both headers state which is which so a reader cannot mistake an opinion for a decision. Banked verbatim from Bill's inline paste; truncation check passed at both ends twice, body SHA-256 `c0e06de5…` unchanged across a mid-dispatch connection drop. Rules: (1) `docs/reviews/`, never invent `docs/research/`, and preserve the failed attempts; (2) exclude every key path from Time Machine before any destination exists, consolidate to one custody location, and do not restore availability by re-adding the key store to backup — prefer erasure integrity for this phase; (3) build the metadata-scrub cascade because current behaviour is only primary-record VALUE erasure, retain opaque operational proof, treat raw recall query text as a separate defect, and accept erasure only against a three-outcome definition where an unlisted store fails. **Carries the enablement gate: no real-data erasure until both key-custody cleanup and the semantic-metadata cascade land.** NOT in scope of the Document Governance Rule's MANIFEST-check; registered here per HA-13 item 2. | reviews/RULING_KeyLifecycle__three-rulings__v20260806_2000.md | md | BANKED — BILL'S RULING | 2026-08-06 |
| Moshi dual-model architecture DIAGRAM, as adopted (FIRST BANKING, 2026-08-14, HA-83; supersedes nothing). Four Mermaid views of the ADOPTED design — D1 runtime topology, D2 the semantic commit point with output classes C0-C5, D3 the interaction-vs-information latency split, D4 the stage ladder with the research/governed border. **Renders verified with mermaid-cli, all four blocks, not assumed from syntax.** Drawn from spec v2 where v1 and v2 differ, so v1's "Moshi may say harmless things itself", its phrase whitelist, and rejected Option 3 are deliberately NOT drawn. **Every element labelled LAB-MEASURED / ADOPTED DESIGN / OPEN QUESTION** — relabeled from PROVEN by HA-84's ruling, the label carrying the meaning rather than a footnote redefining it; the M0 evidence is RESEARCH MODE and UNVERIFIED. Records a correction to its own dispatch's framing: M0 was described as provisional-pass with Q2 pending, but the verdict was RESOLVED TO PASS on 2026-08-14 by Bill's live mic test. Docs-only: no code, no lab run, no graph. | design/HIP_DESIGN_DIAGRAM__moshi-dual-model-architecture-as-adopted__v20260814_1331.md | md | BUILT | 2026-08-14 |
| Natural conversation dual-model architecture, spec v2 (FIRST BANKING on any ref, 2026-08-13, HA-66; supersedes nothing, opens no chain). Research-lane DIRECTION, not a requirement and not a FinishPlan step — the document's own §8 says it does not amend the plan of record. Consolidates three inputs delivered via chat on 2026-08-13 (CGPT dual-model spec, Fable ACCEPT WITH CHANGES with 5 changes, CGPT second pass) into one durable record; §11 dispositions all five Fable changes. Banked VERBATIM from Bill's paste, unedited. | design/HIP_DESIGN__dual-model-natural-conversation-v2__v20260813_1500.md | md | ADOPTED DIRECTION | 2026-08-13 |
| Moshi research lane development method (FIRST BANKING on any ref, 2026-08-13, HA-66; supersedes nothing, opens no chain). PROCESS document, ADOPTED by Bill 2026-08-13: two modes split by what the work asserts; research mode runs in its own ~/moshi-lab checkout with fail-closed environment isolation and no process machinery; governed mode returns at M3. The border is absolute — lab code never merges into a HIP tree, and findings docs are the only artifacts that cross. Banked VERBATIM from Bill's paste, unedited. | design/HIP_PROCESS__moshi-research-lane-method__v20260813_1500.md | md | ADOPTED | 2026-08-13 |
| **Moshi lab — M0 + drift SUMMARY (cover note)** (FIRST BANKING on any ref, 2026-08-14, Voice 42; supersedes nothing, opens no chain). A READING AID over the two findings docs banked in the same commit; **claims nothing beyond them** and is not a ruling. Carries M0's verdict **PASS** (was PROVISIONAL-PASS PENDING Q2 MIC, resolved by Bill's live mic test 2026-08-14), compute **RTF 0.684 steady state on both stages**, the **5 min 28 s / 4096-frame codec ceiling in BOTH directions** (~0.61 s rotation cost, RULED ACCEPTED for research 2026-08-13 and expressly NOT discharged for the product), the drift verdict **STATE-ARTIFACT at frame 4096**, and the two constraints M1 inherits. RESEARCH MODE: no REQ, no MET, no harness run; UNVERIFIED per the `reviews/` rule | reviews/HIP_REVIEW__moshi-m0-summary__v20260814_0815.md | md | BANKED / UNVERIFIED | 2026-08-14 |
| **Moshi lab — M0 feasibility FINDINGS** (FIRST BANKING on any ref, 2026-08-14, Voice 42; supersedes nothing, opens no chain). Banked **VERBATIM** from `~/moshi-lab/FINDINGS__m0__v20260813.md` (ML-01 / Voice 38), body byte-verified sha256 `30c979aeab71f3e9`; a Status/Verification header block was prepended and nothing else changed, so the body's own first line remains the stage verdict **PASS**. Q1 compute MET with room, Q2 duplex CONFIRMED at the microphone, Q3 pre-emission text access YES with audio causally downstream of the text token, Q4 suppression YES with state advancing through the refusal. **BANKED BECAUSE `~/moshi-lab` IS NOT VERSION CONTROLLED** — the lane method §3 makes findings docs the only artifacts that cross into a HIP tree, and no lab code crossed. RESEARCH MODE, UNVERIFIED, marks nothing MET | reviews/HIP_REVIEW__moshi-m0-findings__v20260814_0815.md | md | BANKED / UNVERIFIED | 2026-08-14 |
| **Moshi lab — response-onset DRIFT FINDINGS** (FIRST BANKING on any ref, 2026-08-14, Voice 42; supersedes nothing, opens no chain). Banked **VERBATIM** from `~/moshi-lab/FINDINGS__drift__v20260814.md` (ML-02 / Voice 39), body byte-verified sha256 `1205f6bf8ed69969`; header block prepended only, first body line remains the verdict **STATE-ARTIFACT**. Settles M0's top open question: the onset drift is **NOT tunable and NOT co-tenancy** — with input held byte-identical across a cyclic stimulus the model's leaning toward speech steps up sharply **exactly at frame 4096**, where the KV cache fills and begins rotating. **Separates a confound M0 had recorded as inseparable** by running with no Mimi codec at all. Implication: not a calibration task; mitigation is architectural. RESEARCH MODE, UNVERIFIED, marks nothing MET | reviews/HIP_REVIEW__moshi-drift-findings__v20260814_0815.md | md | BANKED / UNVERIFIED | 2026-08-14 |
| **HIP DEVELOPMENT OPERATING MODEL** (FIRST BANKING on any ref, 2026-08-14, FM 2; supersedes nothing, opens no chain). PROCESS document, authority Bill's FM 2 dispatch: the coordination model itself — Bill → FABLE MASTER (single coordination point) → four CC workers → implementation evidence → FABLE reconciles → ChatGPT independent review at gates → findings → FABLE → **disagreement only** to Bill. Carries the command rule (old chats are reference only; direct Bill-to-worker scope changes reconcile into FABLE state before dependent work continues), chat-is-control-room/repo-is-truth with the session-recovery read order, capability dispatches with five and only five stop conditions, preflight excavation, the DESIGN/CODE/CLOSEOUT gates with `HIP_REVIEW_<capability>_<HEAD>.zip` primary-evidence packaging, five phone-alert classes, three testing tiers including **one heavy suite at a time on this machine**, thirteen settled natural-conversation principles, and the efficiency metrics. Also specifies the STAGING GUARD (§2b) with its six-case twin. **Describes coordination; rules nothing MET; where it restates a `CLAUDE.md` rule, `CLAUDE.md` governs.** | `design/HIP_PROCESS__development-operating-model__v20260814_1025.md` | BUILT |
| **FM COORDINATOR CHECKPOINT — FABLE MASTER state** (FIRST BANKING on any ref, 2026-08-14, FM 2; supersedes nothing, opens no chain). LIVE state document for **session recovery**: HEADs read, active worktrees + targets, worker seat assignments, active capabilities, the open decision queue for Bill, and the review queue. Read FIRST when the coordinator session is lost, before `LANES.md`, dispatch docs and git state — and never reconstruct coordination state from memory. **Versioned per the Naming Law with a `LATEST_` symlink; a sixth never-overwrite exemption is PROPOSED to Bill, NOT self-granted** (the list is CLOSED; Voice 2's `LANES.md` precedent is the shape). Carries an explicit CURRENCY WARNING: every HEAD FM 1 recorded had already changed by the time this checkpoint was written. | `general/FM_CHECKPOINT__coordinator-state__v20260814_1025.md` (current via `general/LATEST_FM_CHECKPOINT.md`) | LIVE |

Note on STALE items: the Financial Annex docx, Technical Annex, and Prototype Evidence were last updated before the SIA spec, harness Phase 2, and voice research corpus existed. They are listed here for completeness. Do not distribute the STALE items without reconciling against the current research corpus first.

---

## C. WP-to-Research Mapping

This table is the paper trail. For each WP section: what it claims, which research artifact backs it, which harness results validate it, and whether the section is current or needs updating.

Reading convention:
- CURRENT: the WP section accurately reflects the research artifacts listed; no update needed before distribution.
- NEEDS-UPDATE: a research artifact that postdates the WP section changes, adds precision to, or qualifies what the section says. The WP is not wrong, but it is incomplete.
- GAP: the WP makes a claim that no research artifact currently backs. The claim may be correct but is unvalidated.

Reference timestamp: public WP v20260712_1602 is the document being mapped. All research artifact statuses are per docs/INDEX.md as of 2026-07-12.

---

### Terms and Acronyms

**Claims:** defines terminology used throughout the WP.

**Research backing:** none required (definitional).

**Harness backing:** none required.

**Status: NEEDS-UPDATE**

New terms introduced since the WP was written that should appear in the glossary:

- SIA (Structured Intent Architecture): the unified classification layer spec'd in SIA_SPEC__structured-intent-architecture__v20260710_1614.md, replacing seven divergent regex classifiers with a single edge-model call producing a Structured Intent Object (SIO).
- SIO (Structured Intent Object): the output of the stateless classification call; the schema that every downstream governed path reads instead of raw utterance text.
- CandidateIntent: the pattern in which every model-produced classification is a proposal with no authority, evaluated by a deterministic policy envelope. Documented in ANALYSIS__candidate-intent-deep-review__v20260711_0501.md.
- Identity envelope: the immutable record of who is speaking, established by voiceprint or session authentication, never by the model. Per the deep review: immutable once bound, probabilistically bound.
- Policy envelope: the deterministic code (injection contract INJ-1 through INJ-7) that evaluates CandidateIntents against the identity envelope, household membership, attribute sensitivity, and capability grants.
- Layer 0 / 1 / 2 / 3: the four-layer HIP architecture from HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032.md. Layer 0 is the replaceable interaction surface; Layer 1 is the routing cascade; Layer 2 is the governed context; Layer 3 is the deterministic control plane.

---

### Executive Summary

**Claims:** HIP is a household AI platform with persistent, governed, private memory, running inference on the operator's edge, with a trust boundary that protects member data from the platform itself. Context compounds over time and creates switching cost the model layer cannot create.

**Research backing:**
- Architecture: HIP_Architecture_Spine__v20260704_1315.md (layer sort, routing cascade, injection contract, operator-blind boundary)
- System state: SYSTEM_UNIVERSE__v20260706_0900.md (pipeline map, 17 divergences as of Jul 6)
- Trust boundary architecture: HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032.md (Layer 3 deterministic control plane)
- Competitive claim: ANALYSIS__candidate-intent-deep-review__v20260711_0501.md (section 4: no commercial platform does multi-entity governed memory)

**Harness backing:**
- Injection contract: HARNESS_PHASE2__L3-mutation-P3P5-L4-pairwise__v20260709_1102.md (L1-L4 RATCHET PASS)
- Cross-member boundary: F4_FIX__access-control-refusal-inj7__v20260708_1140.md (existence-invariant cross-member denial)

**Status: NEEDS-UPDATE**

The ES describes the governed injection contract in one sentence ("The contract governs what the model may see" or equivalent). It does not describe the CandidateIntent pattern, the SIA architecture, or the specific attack the architecture was built against (A6-05: a 7B edge classifier obeyed embedded JSON in an adversarial utterance at 0.9 confidence). The ES can remain high-level, but "the model cannot establish identity, authorization, or permission" is a stronger and more specific claim than what the current ES says, and it is now fully backed by the deep review. Adding one paragraph on the CandidateIntent pattern to the ES would strengthen the trust-boundary claim materially.

---

### Part I: HIP

**Subsections:** What HIP is / How AI works today / The inference cascade / Why this architecture

**Claims:** HIP is a household AI system with private, persistent memory organized per member. The inference cascade routes requests across edge, mid, core, and frontier tiers by complexity and sensitivity. The architecture is justified by cost discipline and the compounding value of private context.

**Research backing:**
- Architecture spine: HIP_Architecture_Spine__v20260704_1315.md (routing cascade as new-art owned layer; injection contract as moat; layer sort)
- Live call graph: LIVE_CALLGRAPH__v20260706_1107.md (actual statement and question turn traces as of main 2213512)
- Epistemic process: EPISTEMIC_PROCESS__v20260706_1000.md (live path vs governed design, 10-row divergence map)
- Fact lifecycle: FACT_LIFECYCLE_DIAGRAM__v20260706_0800.md (state diagram for governed fact transitions)
- System universe: SYSTEM_UNIVERSE__v20260706_0900.md (7 subsystems, 17 divergences)
- Interaction layer: HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032.md (four-layer model, what changes vs what does not)
- Classifier placement: ANALYSIS__classifier-placement-sovereignty__v20260711_1333.md (decision-plane vs data-plane line; "classification carries no authority, placement is not an authorization decision" invariant; fold into the same Part I update)

**Harness backing:**
- Routing gate: HARNESS_PHASE1__fixture-reporter-L2-P1-P2__v20260709_0802.md (L2 25-case corpus, 22/25 pass, 3 accepted)
- Injection contract: HARNESS_PHASE2__L3-mutation-P3P5-L4-pairwise__v20260709_1102.md (L1-L4 RATCHET PASS)

**Status: NEEDS-UPDATE**

The "inference cascade" description in Part I describes the tier structure accurately at the macro level but does not reflect the SIA architecture (the stateless classification call at Layer 0 that now precedes retrieval and routing). The injection contract is referenced by name but the CandidateIntent pattern (every classification is a proposal, confidence carries no authority, the policy envelope is deterministic) is not described. The "why this architecture" subsection would benefit from the policy-envelope argument: the specific reason the architecture separates probabilistic inference from deterministic enforcement is the finding that prompt-level defenses against classifier injection do not hold (A6-05).

The four-layer model from HIP_Interaction_Layer_Architecture_and_Roadmap (Layer 0 replaceable interaction surface, Layer 1 routing, Layer 2 governed context, Layer 3 deterministic control plane) provides a cleaner organizing framework for Part I than what the current WP uses, and would reduce the risk that a reader conflates "the model" with "the system."

---

### Part II: The Moat

**Subsections:** The model is not the moat / Context compounds / The trust boundary is the second half of the moat / The feedback loop closes the moat / Cable holds all five structural advantages / The moat shapes every argument that follows

**Claims:** The model commoditizes; context compounds. The trust boundary, not the model, is the defensible position. The operator is the only entity that can hold the trust boundary because frontier labs cannot adopt the custody model without abandoning their business model.

**Research backing:**
- Layer sort: HIP_Architecture_Spine__v20260704_1315.md (rent commodity, own compounding layers; the sort is the strategic argument)
- Trust boundary precision: HIP_Interaction_Layer_Architecture_and_Roadmap__v20260710_1032.md (Layer 3: identity, consent, policy in deterministic code around the probabilistic core)
- Competitive mapping: ANALYSIS__candidate-intent-deep-review__v20260711_0501.md (section 4: no consumer platform does policy-mediated multi-entity memory; Apple/Amazon/Google voice ID is convenience-grade, not authorization-grade; personal-memory startups are single-principal; enterprise AI governance is org-vs-platform not principal-vs-principal)
- Novelty: ANALYSIS__candidate-intent-deep-review__v20260711_0501.md (section 3: what is actually novel in multi-entity household context)
- Market research: research-market/ECOSYSTEM_DEVELOPERS__40-company-demand-validation__v20260706_1200.md

**Harness backing:**
- Existence-invariant cross-member denial: F4_FIX__access-control-refusal-inj7__v20260708_1140.md
- Adversarial injection containment: SIA_SHADOW_DIFF__v20260710_2106.md + SIA_SHADOW_DIFF__v20260710_2204.md (A6-05 documented, classified as contained, not prevented)
- Two-gate conformance analysis: SIA_SHIP_BAR__two-gate-conformance__v20260711_0842.md (governance-critical gate 26/26 = 100%; enumerates the 26 governance-critical entries as the citable contract; distinguishes injection containment from classification quality)
- Authoritative harness architecture and invariant reference: TEST_HARNESS__architecture-and-invariants__v20260711_1900.md (five-layer corpus, conformance contracts, ratchet discipline, NIST AI RMF mapping; backs the WP's testing claims directly)
- Architecture diagram spec: DIAGRAM_SPEC__architecture-visuals__v20260711_1809.md (SVG content spec for all 7 WP/NDA architecture diagrams -- D1 CandidateIntent flow, D2 decision/data plane, D3 trust ladder + P8, D4 proof harness, D5 orthogonal contracts, D6 four-layer arch, D7 P10 confirmation gate; no WP prose changes; SVG build source)

**Status: CURRENT — NEEDS-UPDATE (trust-boundary claim, see 2026-07-18 note below)**

Canonical versions: v20260712_1852 (both public and confidential). Reconciled against main commit c5a8c1f (2026-07-12).

NEEDS-UPDATE (2026-07-18, HIP_MemberIsolation__crypto-partition-and-recovery-design__v20260718_1117.md): Part II claims "a trust boundary that protects member data from the platform itself" and that the operator holds a custody model. The member-isolation design filed today establishes, against code at 5d6bde3, that this protection is **not yet cryptographically true** — member separation is a retrieval filter (`extraction_queue.py:704-705`) over values the server can always decrypt via one master key (`encryption.py:79-123`); the operator is not blind at rest today. The design is the roadmap that would make Part II's claim literally true (per-member asymmetric keys, master-key retirement at end of migration), and until that migration reaches its Phase 3, Part II's "protects member data from the platform itself" is an architectural intent, not an implemented property. Reconcile Part II's wording to distinguish the built trust boundary (governed injection contract, member-to-member policy) from the not-yet-built operator-blind-at-rest property before any distribution that leans on the latter. Design doc is PLAN; no WP prose changed in this commit.

Additive artifact: HIP_GovernanceProof__audited-transcript__v20260714_1345.md (2026-07-14) provides a turn-by-turn audited transcript of a real reveal_demo run (7 turns, 14 engine records) and a conformance summary covering P1-P6 with harness evidence. Suitable for NDA package inclusion alongside Part II. No WP prose changes required; the governance proof is a companion artifact, not a correction.

Round 3 -- P0/P1 diligence fixes (v20260712_1852): Two corrections applied to both docx versions per WP_NDA_REVIEW__diligence-punch-list__v20260712_1742.md:
(P0) SIA two-gate correction: replaced single "90.2 percent" figure with two-gate presentation -- Gate A (26/26 governance-critical entries, 100% PASS) and Gate B (133 total, 85.7%, Phase B cutover deferred pending 90% threshold). The 90.2% figure was stale and below what any engineer would observe running the conformance suite.
(P1) Voice governance closure: removed stale sentence "Voice-path hardening to run that same enforcement chain end to end is open engineering work, tracked in the debt register as Code Review Finding 4." Replaced with: "Voice-path governance is now implemented: OrchestratorGate routes voice turns through the same injection contract and subject-resolution path as typed queries (BUILD-1, closed). The voice governance boundary is gated by the same conformance suite."

Round 2 -- NDA diligence fixes (v20260711_2311): Five targeted corrections applied to both docx versions:
(1) CI wording: "gated in CI" replaced with "gated by a ratcheted conformance suite that runs on every change through an auto-gate agent" -- no CI pipeline exists; gating is manual/auto-gate script.
(2) A6-05 narrative accuracy: prior text implied live-path containment; corrected to accurately describe shadow-mode evaluation, deny-safe default, and deterministic pre-classifier injection guard as the containment mechanism.
(3) Gate B quality honesty: added overall classification quality figure (90.2% across 133-entry corpus); residual failures enumerated as non-governance; governance-critical gate at 100%. NOTE: this figure was further corrected in Round 3 above.
(4) Harness scope: added "to the typed interaction path" narrowing the harness-proof claim to the typed path.
(5) Key custody: "encrypts under keys the household controls" (Part III privacy section) replaced with accurate custody language: operator-custodial master key, HKDF-SHA256 per-owner derivation, Fernet at rest; Shamir 2-of-2 recovery is a design specification, not yet built; platform makes no claim of household key control today.

Round 1 (v20260711_1830): "The trust boundary is the second half of the moat" subsection replaced in both public WP and NDA superset. 4 prior paragraphs replaced with 11 new paragraphs. Existing Charter/Latis competitive reference preserved. NDA version carries expanded speaker-verifier attack surface paragraph (three documented vectors: replay, voice cloning, household-insider mimicry; TD-109 referenced; possession-based escalation path described). CandidateIntent pattern stated precisely; honest speaker verifier qualification with Amazon/Apple competitive behavior cited; Gate A 26/26 quantitative grounding; injection claim is containment not prevention. No em-dashes or en-dashes anywhere in either document.

Round 2 -- NDA diligence fixes (v20260711_2311): Five targeted corrections applied to both docx versions:
(1) CI wording: "gated in CI" replaced with "gated by a ratcheted conformance suite that runs on every change through an auto-gate agent" -- no CI pipeline exists; gating is manual/auto-gate script.
(2) A6-05 narrative accuracy: prior text implied live-path containment; corrected to accurately describe shadow-mode evaluation, deny-safe default, and deterministic pre-classifier injection guard as the containment mechanism.
(3) Gate B quality honesty: added overall classification quality figure (90.2% across 133-entry corpus); residual failures enumerated as non-governance; governance-critical gate at 100%.
(4) Harness scope: added "to the typed interaction path" narrowing the harness-proof claim to the typed path. The companion WP sentence ("Voice-path hardening to run that same enforcement chain end to end is open engineering work, tracked in the debt register as Code Review Finding 4") was accurate when written but is now stale -- BUILD-1 (fbcd372) delivered voice-path governance by wiring voice_orch.py through the injection contract. Both WP v2311 docx files carry this residual stale sentence; remove it in the next WP revision.
(5) Key custody: "encrypts under keys the household controls" (Part III privacy section) replaced with accurate custody language: operator-custodial master key, HKDF-SHA256 per-owner derivation, Fernet at rest; Shamir 2-of-2 recovery is a design specification, not yet built; platform makes no claim of household key control today.

---

### Part III: The Forces Converging on the Household

**Subsections:** The care crisis / AI build-out backlash / Privacy reactivation / Institutional trust collapse / The five forces converge

**Claims:** Five independent forces create the market conditions HIP is positioned to meet: a care crisis with no scalable supply, AI backlash creating demand for local/private alternatives, privacy reactivation as a market force, and institutional trust collapse driving demand for a custodial platform.

**Research backing:**
- Eldercare demand: research-market/ELDERCARE_MARKET_TAM__us-tam-demographics-wtp__v20260706_2049.md
- AI backlash / privacy: research-market/AI_STACK_ECONOMICS__costs-moat-enterprise-roi__v20260706_1200.md (datacenter backlash, consumer sentiment)
- Ecosystem demand: research-market/ECOSYSTEM_DEVELOPERS__40-company-demand-validation__v20260706_1200.md

**Harness backing:** none required (market analysis).

**Status: CURRENT**

Updated in v20260712_1602. Four additive paragraphs inserted (P3_A after the group-text para, P3_B after the five-forces-converge para; P9_A after the "undefended" para, P9_B after the "model layer is cheap now" para). All insertions verified by automated check: present, ordered correctly, no em/en-dashes.

Prior NEEDS-UPDATE note (for record): The care crisis and forces-converge subsections were qualitatively current but carried no cited household-size or caregiver-count figures. The 2026-07-12 market research corpus (MARKET_RESEARCH__household-trust-circle-segment-sizing-verified__v20260712_1331.md, adversarially verified) supplies additive cited numbers that belong in the care-crisis subsection and the five-forces-converge closing:

- 63.7% / 84.2M of 132.2M US households are 1-2 person (2024 CPS ASEC HH-4) [CITED]
- 29.2M married-couple-only households (CPS 2023 Table H1) [CITED floor]
- 15.2M households with a 65+ adult living alone (ACS-derived) [CITED]
- 63M family caregivers (AARP/NAC 2025), 3 in 10 care recipients live alone [CITED]
- Remote monitoring use: 13% (2020) to 25% (2025) [CITED, AARP/NAC 2025]
- Trust-circle size: mean 2 confidants (McPherson et al. ASR 2006), kin-centered, supports dyad architecture
- Growth wave: boomers moving through ages 75-85 between 2025-2045 is the product-relevant demand surge

The modeled 45-55% addressable figure (external analysis, no direct Census source) may be referenced if labeled [MODELED] every time. The refuted ~80% older-adults-in-1-2-person-HH framing must not appear.

Update is ADDITIVE to current Part III prose; no subsection is replaced. The care-crisis paragraphs (paras 183-188 in v20260711_2311) receive the cited household-size and caregiver data. The five-forces-converge closing (paras 212-215) receives the trust-circle closure.

Research artifact: HIP_STRATEGY__positioning-and-market__v20260712_1541.md (Section 4 and cascade map Section 8.1) is the strategy source. HIP_STRATEGY cascade map Section 8.4 governs what must not appear unlabeled.

---

### Part IV: Intelligence Commoditizes

**Subsections:** Open intelligence has a track record / Licensing varies / Bias is mitigable / Specialists beat generalists / HIP as the operating system for an open model ecosystem

**Claims:** Open-weight models are approaching frontier capability on a closing schedule. The defensible position is not model access but the platform layer that hosts interchangeable models. HIP is the operating system for an open model ecosystem.

**Research backing:**
- Model commoditization thesis: HIP_Architecture_Spine__v20260704_1315.md (Layer 1: prior-art, rent; swappability is the feature, not the gap)
- Voice model taxonomy: voice-research/HIP_Voice_Architecture_Research_P1_Taxonomy__v20260709_2154.md (taxonomy of voice interaction models; confirms the same commoditization thesis extends to the interaction layer)
- Market research: research-market/AI_STACK_ECONOMICS__costs-moat-enterprise-roi__v20260706_1200.md

**Harness backing:** none required (market and architecture thesis).

**Status: NEEDS-UPDATE (final subsection)**

The "HIP as the operating system for an open model ecosystem" subsection is the thesis capstone for Part IV. The voice research corpus (P1-P8) extends the same argument explicitly to the interaction layer: three voice architectures have emerged in two years (cascade, turn-based audio-native, full-duplex), each displacing the last, and HIP's position is that it does not bet on which architecture wins. This is a concrete, documentable instance of the commoditization argument that would strengthen the final subsection: not just "models commoditize" but "interaction architectures commoditize too, and HIP is architectured to absorb that."

---

### Part V: The Expensive Input Is Memory, Not Compute

**Subsections:** Memory is the bottleneck / Shortage has reached the consumer / Micron's position / Cost curves diverge by workload / Operator edge avoids the facility cost spiral / The turn

**Claims:** Memory bandwidth and capacity, not raw compute, constrain AI workloads. The shortage is real and locked in. The operator edge avoids the facility cost spiral because the plant already exists.

**Research backing:**
- Cost analysis: research-market/AI_STACK_ECONOMICS__costs-moat-enterprise-roi__v20260706_1200.md
- Edge compute: HIP_Architecture_Spine__v20260704_1315.md (Layer 1: edge hardware cost and tier economics)

**Harness backing:** none required (market and infrastructure analysis).

**Status: CURRENT**

No technical research postdates or qualifies Part V's claims. The voice research (P7 latency/cost model) adds edge inference latency specifics but does not change the macro argument.

---

### Part VI: Where Compute Must Live

**Subsections:** Centralized compute is constrained / Inference distributes, training mostly does not / Physical security gates the location / The two limits converge

**Claims:** Centralized compute cannot scale fast enough. Inference distributes outward to wherever it can be secured and powered. Physical security requirements gate the location to a narrow set of facilities.

**Research backing:**
- Distributed inference: research-market/AI_STACK_ECONOMICS__costs-moat-enterprise-roi__v20260706_1200.md
- Security gate: HIP_Architecture_Spine__v20260704_1315.md (Layer 5: confidential computing; "what the TEE vendor does not close for you")
- Edge latency budget: voice-research/HIP_Voice_Architecture_Research_P7_Latency_Cost_Model__v20260710_1137.md (encode-decode-model budget analysis, edge inference latency constraints)
- Classifier placement: ANALYSIS__classifier-placement-sovereignty__v20260711_1333.md (decision-plane inference does not distribute; it anchors to the governance boundary)

**Harness backing:** none required.

**Status: NEEDS-UPDATE**

P7 adds specificity on edge latency budgets for voice workloads but does not change Part VI's macro argument. The classifier-placement analysis DOES qualify it: "inference distributes outward" needs one paragraph distinguishing data-plane inference (distributes freely; the Groq reasoning tier is the example) from decision-plane inference (anchors to the governance boundary; the SIO classifier is the counterexample). Scope: one qualifying paragraph, no structural change.

---

### Part VII: Cable Owns the Location

**Subsections:** The facilities exist at scale / Virtualization is freeing space / Powered, secured, connected / The honest limit / Hardware cost confirms it / NVIDIA and the operators are already building this

**Claims:** Cable headends and hubs are powered, secured, connected, and already staffed. Virtualization is freeing space. NVIDIA is actively co-deploying inference at these facilities. The honest limit (legacy facilities were not built for GPU-density liquid cooling) is stated and bounded.

**Research backing:**
- Platform economics: research-market/PLATFORM_TAKE_RATES__marketplace-benchmarks__v20260706_1200.md
- Smart home / robotics TAM: research-market/CONSUMER_ROBOTICS_MARKET__tam-platform-attach-smart-home__v20260706_2102.md
- Architecture spine NVIDIA note: HIP_Architecture_Spine__v20260704_1315.md (Layer 5: NVIDIA Confidential GPU; Layer 2: NVIDIA-vertical stack option)

**Harness backing:** none required.

**Status: CURRENT**

---

### Part VIII: The Economics

**Subsections:** Deployment cost is incremental / Hardware cheaper after tax / Why deploy compute before subscribers / The lease-back bridge / Success-based deployment / Risk case / How the model should be built / The turn

**Claims:** HIP deployment is incremental cost on existing operator infrastructure. Hardware qualifies for bonus depreciation. The lease-back bridge closes the chicken-and-egg problem. The model is conservative and the risk case is stated plainly.

**Research backing:**
- Financial model: business/financial/ (model scripts + current xlsx deliverable HIP_FinancialAnnex__v20260705_2020.xlsx)
- Infrastructure cost: research-market/AI_STACK_ECONOMICS__costs-moat-enterprise-roi__v20260706_1200.md
- Formatted annex: HIP_FinancialAnnex__v20260702_1913.docx (formatted version; STALE vs v20260705_2020.xlsx)

**Harness backing:** none required.

**Status: CURRENT (narrative); STALE (financial annex docx)**

The Part VIII narrative is current. The Financial Annex docx (formatted deliverable) has not been rebuilt since v20260702_1913; the xlsx model is v20260705_2020. If the Financial Annex docx is distributed to a partner, reconcile it against the current xlsx before sending.

---

### Part IX: Why Now

**Subsections:** The position is real and undefended / The contestants are arriving / The window is defined by the moat / The conditions are aligned now / What closes if cable waits

**Claims:** No one currently occupies the multi-entity household AI position. The window is defined by how long it takes a competitor to build switching cost. All favorable conditions (cheap models, edge economics, demand forces, NVIDIA co-deployment) are simultaneously active and will not stay aligned.

**Research backing:**
- Competitive positioning: ANALYSIS__candidate-intent-deep-review__v20260711_0501.md (section 4: full competitive landscape mapping; specific statements on Amazon, Apple, Google, personal-memory startups, enterprise AI governance -- none occupies multi-entity governed household memory)
- Market research: research-market/ECOSYSTEM_DEVELOPERS__40-company-demand-validation__v20260706_1200.md

**Harness backing:** none required.

**Status: CURRENT**

Updated in v20260712_1602. Two additive paragraphs inserted: P9_A (after "asset is held, undefended" para) names the Amazon PIN / Apple proximity / Google Voice Match concessions explicitly; P9_B (after "model layer is cheap now" para) adds the CMS GUIDE Model (July 2024) reimbursed path and the caregiver remote monitoring adoption doubling (2020-2025) as timing-specific evidence. Verified by automated check: present, ordered, no em/en-dashes.

Prior NEEDS-UPDATE note (for record): "the position is real, and it is undefended" subsection previously made the competitive gap claim in general terms. The Amazon/Apple/Google concession detail and the GUIDE Model are now inline in the section.

---

### Part X: The Builder

**Claims:** Bill Brewster's operator background (Comcast X1, Canoe Ventures) positions him to build and operate this platform.

**Research backing:** none required (biography).

**Status: CURRENT**

---

### References

**Status: NEEDS-UPDATE**

---

### Diagnostic artifacts (no WP section mapping required)

The following research-technical docs are diagnostic or engineering artifacts.
They do not map to any WP/NDA section claim and require no NEEDS-UPDATE action
on any WP section. Listed here for completeness per governance discipline.

| Artifact | What it covers | WP impact |
|---|---|---|
| DIAG__l3-mutation-window-emits-gated-records__v20260715_1930.md | Layer 3 INJ-6b disable window emits fabrication-class d1.1 records that Layer 6 gates; stale pre-c75655d INJ-6 predicate copied in inproc.py:122-125 clears the patched guard; four consequences incl. remaining green-half blocker and 0-byte harness_run.jsonl explanation. | None -- harness instrument diagnostic; no WP section claims mutation-layer internals. |
| docs/requirements/REQ_TEMPLATE__requirements-doc-template__v20260715_1601.md | Requirements discipline template: one doc per build, written first from Bill's verbatim words, with acceptance test, already-done, known-broken, and constraints sections. Enforced via CLAUDE.md Requirements Discipline. | None -- process artifact; no WP section claims a requirements process. |
| docs/requirements/REQ_VOICE_DEMO__one-screen-script-plus-live-voice__v20260715_1601.md | First requirements doc: /demo one-screen scripted-then-live-voice demo. 9-step acceptance test; GA session.update schema fix, tier=realtime d1.1 emit, and LIVE rendering recorded as done; missing mic control on /demo recorded as the gap. | None -- internal build requirement; demo capability claims in WP unaffected until built. |
| docs/requirements/REQ_UNRESOLVED_SUBJECT_GUARD__empty-set-guard-fires-when-no-subject-resolves__v20260804_0806.md | Requirement that the empty-set guard fire when no subject resolves and facts would otherwise enter the prompt ungoverned. INJ-6 and INJ-6b are both gated on has_personal_subject, so on the resolved_subjects==[] path neither guard runs while household-owned facts are still admitted (INJ-1/INJ-2/INJ-5 each pass household unconditionally). Measured scope: 188/199 baseline and 63/68 cutover turns ran on that unguarded path -- the norm in both systems, NOT a cutover regression. Consequence recorded: the seven guard-shaped-no-guard items are not structurally protected; the model refused voluntarily, and this build cannot distinguish that from a compelled refusal on that path. Status PLAN, nothing built, nothing ruled MET, C9 not ruled. | None -- internal build requirement for the injection contract's guard precondition; no WP/NDA section claims guard-precondition behavior or distinguishes structural from voluntary refusal. Listed for completeness per the two REQ rows above, which are this table's established precedent for requirements docs. |
| DIAG__p2-i019-detection-miss__v20260714_1500.md | P2 i019 is a detection false negative, not write latency. Groq returns changes:[] for sam/preference/vegetarian at i019 (i016 maya same value lands). TD-124 wrong fix; correct track is TD-123 prompt hardening (dietary vs preference disambiguation). AMENDED 2026-07-14: Scenario A confirmed (i009 landed, i000-i018 all landed); false negative estimate corrected from ~14-17 to likely 1-10 (detected_no_changes=29 < 40 expected idempotent; guard absorbs share of idempotent; precise FN count = landed=False poll records). | None -- WP does not claim write-path detection recall at this level; no section needs update. |
| EVAL__chatterbox-tts-apple-silicon__v20260714_2310.md (+ companion eval script) | Chatterbox TTS (MIT) measured on the Mini: runs on MPS; air-gap CONFIRMED (offline generation, zero outbound); PerTh watermark CONFIRMED (score 1.0, no API off-switch); NOT real-time on Mini (warm RTF ~1.27, non-streaming API). Viable TODAY for voice-preservation/legacy tier; operator-GPU candidate for live TTS; strengthens Deepgram/Cartesia negotiation position. | None -- WP makes no TTS-vendor claims. Voice memo (deliverable) gains a candidate for its OSS fallback stack; fold into next memo revision, no NEEDS-UPDATE mark required now. |
| docs/reviews/FABLE_D46_critique__household-seeding-parts1-3__v20260731_1258.md | Fable design critique (dispatch D-46), banked verbatim D-54/D-55. Scope: HIP_HouseholdSeeding_Roadmap v20260730_1936, Parts 1-3 ONLY (confirmation subroutine, seeding/onboarding, boundary manager); Parts 4-5 reviewed separately. Status BANKED, findings UNVERIFIED, proposes no REQ status. Blocking finding: the roadmap's CORROBORATED wiring contradicts D-50 Principle 3, REQ_ATTESTED, and REQ_TRUST_AXES. | None -- pre-spec design critique of an unbuilt subsystem; no WP/NDA section claims household-seeding onboarding, confirmation, or boundary-management behavior. Listed for completeness only. **Scope note:** docs/reviews/ is explicitly OUT of scope of the Document Governance Rule's MANIFEST-check per CLAUDE.md, and no prior banked review (D-35, D-49) carries a MANIFEST row -- this row is added on the D-55 dispatch's explicit instruction and is the first of its kind. If MANIFEST is to stay deliverables-only, back this row out rather than extending the pattern. |
| ../reviews/CHATGPT_EvalMethodology__evaluation-methodology-review__v20260803_1527.md | ChatGPT's evaluation-methodology review, answering ../research-technical/HIP_EvalMethodology_ReviewPrompt__v20260803_1527.md. Status BANKED, findings UNVERIFIED, proposes no REQ status. | None -- external methodology research; no WP/NDA section claims a specific test-suite architecture. Listed for completeness only. |
| ../reviews/FABLE_EvalMethodology__evaluation-methodology-review__v20260803_1527.md | Fable's evaluation-methodology review, answering the same prompt, independently. Status BANKED, findings UNVERIFIED, proposes no REQ status. | None -- external methodology research; no WP/NDA section claims a specific test-suite architecture. Listed for completeness only. |
| ../reviews/CHATGPT_ConversationMemory__conversation-memory-review__v20260803_1527.md | ChatGPT's conversation-memory review, source was a conversation not a file (flagged in the document's own header, not byte-comparable to any artifact). Status BANKED, findings UNVERIFIED, proposes no REQ status. **CANONICAL COPY (Index Demo 2, 2026-08-03).** An independent, older copy of this same review was found already banked on `hip-vo` branch `voice-port` (Voice 33, commit `547df44`, filename `docs/reviews/VOICE33_CONVERSATION_MEMORY_REVIEW__chatgpt-research-query-rewriting-critique__v20260801_1722.md`), predating this row and unknown to the dispatch that wrote it. THIS roadmap copy is now the canonical one for this tree; the voice-port copy is a known duplicate, not reconciled, to be DROPPED when voice-port merges into or retires against roadmap -- not before, and not by this filing (delete nothing). | None -- pre-spec design critique of an unbuilt subsystem; no WP/NDA section claims conversation-memory behavior. Listed for completeness only. |
| ../reviews/VOICE33_CONVERSATION_MEMORY_REVIEW__fable-query-rewriting-critique__v20260801_1722.md | Fable's conversation-memory review, RECONCILED INTO ROADMAP (Index Demo 2, 2026-08-03) -- ported byte-exact from `hip-vo` branch `voice-port` @ `547df44` (originally banked there 2026-08-01, Voice 33; `cmp` verified identical to the voice-port blob at copy time). Filename preserved from its origin rather than re-stamped with today's date, since this content was not first banked here -- it was absent from roadmap, not absent from the world. Source was a conversation, not a file (the document's own header states this explicitly and presents no diff/sha256 as verification, calling that circular against a reproduction of itself). Status BANKED / UNVERIFIED-BY-CONSTRUCTION (the document's own status line), proposes no REQ. Companion to the CHATGPT_ConversationMemory row above -- both reviewed the same brief, converged independently on the same central finding. | None -- pre-spec design critique of an unbuilt subsystem; no WP/NDA section claims conversation-memory behavior. Listed for completeness only. |
| ../reviews/CUTOVER_D110_Comparison__16-turn-roadmap-vs-hipvo__v20260803_1527.md | This session's own D-110 dispatch: 16 live turns compared against hip-vo's baseline. Status BANKED / VERIFIED-BY-EXECUTION (not an external review). | None -- internal demo-cutover verification; no WP/NDA section claims demo-script parity with hip-vo. Listed for completeness only. |
| ../reviews/CUTOVER_C5CaveatVerify__live-verification-trust-ladder-header-panel__v20260803_1527.md | This session's own live verification of the C5 panel + T05 provenance-caveat port. Status BANKED / VERIFIED-BY-EXECUTION. | None -- internal demo-cutover verification; no WP/NDA section claims this panel's behavior. Listed for completeness only. |
| ../reviews/CUTOVER_TrustMarkerReconcile__duplicate-port-analysis__v20260803_1527.md | This session's own read-only reconciliation of two duplicate trust-marker ports. Status BANKED / VERIFIED-BY-EXECUTION. | None -- internal code-provenance analysis; no WP/NDA section claims. Listed for completeness only. |
| ../reviews/CUTOVER_HeaderFixConfirm__section-other-people-rename-confirmation__v20260803_1527.md | This session's own confirmation of another lane's already-landed header-rename fix, plus an independent harness run. Status BANKED / VERIFIED-BY-EXECUTION. | None -- internal verification; no WP/NDA section claims this header text. Listed for completeness only. |
| ../design/HIP_ConversationMemory_ReviewBrief__v20260803_1527.md | The conversation-memory brief sent out for external review 2026-08-01. Status SUPERSEDED BY THE REVIEWS ABOVE -- its §5 proposed solution was rejected by both reviewers; not a design of record. | None -- pre-spec brief for an unbuilt subsystem; no WP/NDA section claims conversation-memory behavior. Listed for completeness only. |
| ../research-technical/HIP_EvalMethodology_ReviewPrompt__v20260803_1527.md | The prompt both eval-methodology reviews answered. Status BUILT (used as intended). | None -- process artifact; no WP section claims a review-prompt process. |
| ../research-technical/HIP_RepoBankingGaps__demo-lane__v20260803_1527.md | State snapshot (TYPE: STATE, no status field) of what the demo/cutover lane had not yet banked as of 2026-08-03 -- the document that motivated this dispatch. | None -- internal housekeeping record; no WP section claims repo-banking completeness. |

**CONVENTION NOTE, flagged not silently applied:** the ten rows above use Bill's explicitly-requested `../reviews/`, `../design/`, `../research-technical/` relative-path style (Index Bank 1, 2026-08-03). Checked against the file before writing: this exact literal convention is **not** what row 907 above established (`docs/reviews/...`, repo-root-relative, added D-55) -- and per REQ_RECORD_GRADED_REFUSAL's Voice 37 filing (2026-08-02, INDEX.md), a `../requirements/`-style convention **is** established, but in **hip-vo's** MANIFEST, not this tree's; that filing explicitly declined to import it here, citing CLAUDE.md's Document Governance Rule (scoped to docs/research-technical/ and docs/deliverables/ only) and TD-137 (the two trees' MANIFEST conventions already diverging). This dispatch follows Bill's literal current instruction rather than either prior precedent, on the reasoning that a direct, explicit dispatch from Bill is itself the deliberate convention decision Voice 37 said would be needed -- but the divergence from both this tree's own prior row (907) and its own prior considered refusal (Voice 37) is real and is flagged here rather than smoothed over. If this is not the convention Bill intended, these eleven rows (907 + these ten) are the ones to reconcile.

References should add: SIA_SPEC, ANALYSIS__candidate-intent-deep-review, HIP_Interaction_Layer_Architecture_and_Roadmap, and voice-research corpus (P1-P8) as internal research sources available under NDA on request. The current reference list covers external sources only; internal research artifacts are now substantive enough to cite.

---

## D. Update Policy (enforced discipline, not a suggestion)

### When a research artifact is created or updated
1. Read this MANIFEST.
2. Find every WP section that maps to the changed artifact.
3. Set that section's status to NEEDS-UPDATE in this file.
4. Commit the MANIFEST change in the same commit as the research artifact.
5. Commit message must reference the MANIFEST update: "MANIFEST: marks Part II / trust boundary as needs-update."

### When a deliverable is updated
1. Copy the new file to docs/deliverables/ with the new version suffix.
2. Update Section B (canonical version table) in this file.
3. Update the section mapping rows for every section that changed.
4. Commit the MANIFEST update in the same commit.
5. Commit message: "deliverable update: WP v<new>; MANIFEST updated; sections X, Y reconciled."
6. Never commit a deliverable update without a MANIFEST update.

### Orphan detection
Any file in docs/deliverables/ not listed in Section B is an orphaned artifact. Flag it in the next session and either register it or delete it.

### CLAUDE.md cross-reference
CLAUDE.md contains the enforcement reminder that reads docs/deliverables/MANIFEST.md before any commit touching docs/research-technical/ or docs/deliverables/.

---

## E. Deletion Candidates (awaiting user confirmation)

These files are redundant given the canonical versions now in docs/deliverables/. Do NOT delete without explicit user confirmation.

### Downloads/ -- older WP versions (superseded by whitepaper/HIP_White_Paper_Updated__v20260708_1604.docx)
- ~/Downloads/HIP_White_Paper.docx (Jun 2)
- ~/Downloads/HIP_White_Paper.pdf (Jun 2)
- ~/Downloads/HIP_White_Paper_v3.docx (Jun 5)
- ~/Downloads/HIP_White_Paper_v3 (1).docx (Jun 5)
- ~/Downloads/HIP_White_Paper_v3 (1).pdf (Jun 5)
- ~/Downloads/HIP_White_Paper (1).docx (Jun 30)
- ~/Downloads/HIP_White_Paper_Updated__v20260704_0755.docx
- ~/Downloads/HIP_White_Paper_Updated__v20260704_0813.docx
- ~/Downloads/HIP_White_Paper_Updated__v20260704_0837.docx
- ~/Downloads/HIP_White_Paper_Updated__v20260704_0856.docx
- ~/Downloads/HIP_White_Paper__v20260704_1644.docx
- ~/Downloads/HIP_White_Paper__v20260704_1644 (1).docx
- ~/Downloads/HIP_White_Paper_Updated__v20260704_1655.docx (superseded by v20260708_1604)
- ~/Downloads/HIP_WhitePaper_Confidential__v20260704_1414.docx (superseded by v20260704_2142)
- ~/Downloads/HIP_EcosystemAnalysis_NDA__v20260707_0618.docx (duplicate of whitepaper/nda/ version)

### Downloads/ -- older Financial Annex versions (superseded by v20260705_2020)
- ~/Downloads/HIP_FinancialAnnex__v20260703_0823.xlsx
- ~/Downloads/HIP_FinancialAnnex__v20260703_0954.xlsx
- ~/Downloads/HIP_FinancialAnnex__v20260704_0836.xlsx

### whitepaper/nda/ -- older Financial Annex versions (superseded by v20260705_2020 in deliverables/)
- whitepaper/nda/HIP_FinancialAnnex__v20260702_1529.xlsx
- whitepaper/nda/HIP_FinancialAnnex__v20260702_1530.docx
- whitepaper/nda/HIP_FinancialAnnex__v20260702_1913.xlsx
- whitepaper/nda/HIP_FinancialAnnex__v20260703_0823.xlsx

### Google Drive -- docx versions already in whitepaper/ or deliverables/
These are Google Drive sync duplicates. Safe to clear from Downloads once confirmed:
- "~/Google Drive/.../White Paper/HIP_White_Paper_Updated__v20260704_1655.docx" (same as whitepaper/ copy)
- All gdoc pointers (.gdoc files) are Google Docs stubs, not editable files -- not relevant to the deliverables governance

### Keep (do not delete)
- whitepaper/ directory and all its contents (history, sections, archive, diagrams)
- The latest NDA docx/xlsx copies in whitepaper/nda/ -- they are the source-of-record for the nda/ structure; deliverables/ holds copies
- Google Drive gdoc stubs (not managed here)
