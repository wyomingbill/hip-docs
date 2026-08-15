# HIP ROADMAP — CHAT HANDOFF / STATE OF PLAY
Status: SUPERSEDED (D-141, 2026-08-03)
Superseded-By: `docs/HIP_HANDOFF.md` — the LIVE handoff, created D-137, maintained by the
lane that lands each dispatch (CLAUDE.md, "The live handoff document").
Reconciled-Against: roadmap `c5c9202`

> **DO NOT FOLLOW THE CONVENTIONS BELOW — READ `docs/HIP_HANDOFF.md` INSTEAD.**
>
> This document is retained UNCHANGED below this header for provenance: it is a real record
> of how the lane worked as of 2026-07-31, and parts of it are still true. But it is a
> SNAPSHOT, not a maintained document, and at least one of its instructions is now WRONG:
>
> - **Line ~11, "OUTPUT: dispatches PRINT full report to terminal"** — superseded by
>   CLAUDE.md's route-by-size rule (D-136): SHORT reports print to the terminal; LONG
>   reports (any build, any harness run, any per-row evidence) go to the dispatch doc, and
>   the terminal gets only the status first-line, the file path, and the commit hash. Its
>   parenthetical remains correct and is now recorded in CLAUDE.md with its reason:
>   terminal-copy and file-open both arrive blank, which is why `open -e` is forbidden and
>   dragging the file is the working route.
> - Its dispatch numbering ("currently at D-54"), its two-sessions-by-screen-position
>   convention, and its lock inventory are all snapshots of 2026-07-31 and have moved.
>
> D-136 identified this contradiction and correctly declined to edit another lane's
> artifact. D-141 marks it superseded IN PLACE, on Bill's instruction: not deleted — its
> provenance is real — and its body is not rewritten.

_As of 2026-07-31. Paste this into a new chat's first message to continue seamlessly._

## HOW TO WORK (conventions — also in memory, restated for safety)
- Two CC sessions by screen position: **UPPER = Sonnet, LOWER = Fable.** Do not reverse.
- Dispatch numbering: this ROADMAP thread uses **D-NN** (currently at D-54). The DEMO lane
  (separate chat) uses "Index Demo N" — different count, don't mix.
- Every dispatch: machine gate first (whoami/hostname/pwd/git toplevel/branch, STOP on mismatch),
  take the right lock (graph+harness for code; INDEX/MANIFEST for docs), read-before-write,
  requirements-first, assess-don't-self-MET (MET is Bill's call alone).
- OUTPUT: dispatches PRINT full report to terminal; Bill SCREENSHOTS (terminal-copy and
  file-open both arrive blank for Bill). Claude CAN read Bill's uploaded files directly off
  /mnt/user-data/uploads/ via bash even when chat preview shows blank.
- Repo: ~/hip-roadmap, branch roadmap, on the Mac mini.
- Known recurring bug: lock files' "taken:" timestamp drifts hours from mtime — likely why
  concurrent sessions both think they hold the lock. Cheap fix pending, not yet done.

## WHAT'S DONE (closed, not in question)
- **Curator learning track: CLOSED.** All three REQs MET, externally Fable-reviewed:
  REQ_LEARNER_SIGNAL_ISOLATION (isolation gate, 7 holes found+fixed, battery wired+proven),
  REQ_LEARNER_TARGET_AUTHENTICATION, REQ_CURATOR_SHADOW_SCORER (dead-substrate bug fixed,
  --full green, ruled MET at commit 9a266cf). Next Curator step = Gate A, needs REAL USAGE
  to fill Stage-0 data — NOT a dispatch. Parked, not blocked.
- **Part 1 of the household-seeding design: DONE and banked** as
  docs/design/HIP_ConfirmationModel_PortraitRethink__v20260731_0730.md (commit 4f8f472, D-50).
  See "PART 1 MODEL" below.
- **Trust-axis ruling: DONE.** REQ_TRUST_AXES + REQ_ATTESTED filed (D-52), then revised to
  "record both, rank neither" (D-53) after external evaluation. See "TRUST AXES" below.
- **External reviews banked** in docs/reviews/: Fable D-46 critique, ChatGPT pass1, pass2,
  and pass3 (pass3 = the trust-axis evaluation; being banked via D-54 — CONFIRM it committed).

## PART 1 MODEL (the portrait rethink — the core design win)
- CORE ANALOGY (preserve for engineering): the system stores **PORTRAITS, not PHOTOGRAPHS.**
  Every claim is an attributed rendering — "X asserts Y, based on Z, at time T" — signed by its
  author, never mistaken for truth about the subject. Two disagreeing portraits both kept
  (Cubist: hold the contradiction). Confirmation = the artist signing the canvas, NOT the
  museum declaring the portrait is reality.
- SIX PRINCIPLES: (1) atomic unit = attributed claim; (2) confirmation signs an attribution
  not a truth, only the authorized subject confirms their own; (3) corroboration = independent
  agreement, a SEPARATE AXIS not a rung; (4) terminal states — never dead-ends SILENTLY
  (DECLINED/UNREACHABLE/NO_AUTHORITY/CONTESTED/AUTHOR_ONLY/UNSAFE_TO_CONFIRM; DECLINED must be
  STORED, can't be derived); (5) never proactively route a third-party claim to its subject,
  confirmation emerges only on volunteering; (6) CONTENT-BLIND custody — hold a claim's judgment
  without adopting it, never normalize/merge/adjudicate/derive from framing.
- FIVE STRESS-TEST CASES (they ARE the spec): drinking (judgment held neutrally); music
  (structural twin, proves content-blindness); "a drink once in a while" (subject's framing
  recorded as his, does NOT confirm the claimant's verdict); "beat me up" (DISCLOSURE — Part 1
  neutrality STOPS, Part 4 safety takes over); false witness (HIP renders no verdicts, so it
  can't bear false witness).
- THE SEAM: Part 1 neutral custody has a HARD boundary at Part 4 (harm response); the
  claim-vs-disclosure recognizer must fail TOWARD safety. Single most important component;
  needs psychologist + attorney review.
- ACTIVE-TRUTH-SEEKING FORK, RESOLVED: a FLOOR (non-configurable: never adjudicate, never
  register accusations as facts, never aggregate into a profile, harm routes to safety) PLUS a
  configurable SWITCH above the floor (how much truth-seeking scaffolding offered to the USER),
  governed by meta-governance so a false accuser can't weaponize it.
- META-GOVERNANCE = a SIXTH foundational area, flagged NOT designed: rules for changing the
  rules (who can change a permission/role, what triggers it, amendment process, authority
  disputes, custodian succession, minor→18, cognitive decline, dissolution). A COMPOSITION
  problem (borrow OS/DB/IAM/healthcare-consent/legal/version-control/constitutional-amendment),
  not invention. Needs its own pass + attorney review.

## TRUST AXES (D-52/D-53, the "record both rank neither" resolution)
- Three contradictory trust orderings existed in tree. Ruling: don't declare one ordering,
  declare one PER AXIS.
- Keep TRUST_RANK unchanged = WRITE-AUTHORITY axis (DERIVED=0 is correct, don't "fix" it).
- The epistemic-strength "axis" is NOT a ranking — it's a RECORD: store two separate,
  co-existing signals — (subject_asserted: bool) and (independent attestations: set WITH
  provenance) — and NEVER collapse them into a single trust verdict. Consumer weighs them.
- NO motive-to-misreport attribute table (external eval killed it: content-blindness violation).
- Return shape = (subject_asserted, attestations-with-provenance) record, not a score/comparator.
- Build ahead of consumer (no caller this pass) — it's now storage, fully self-testable.
- Keep CORROBORATED = reconciliation-hardening (ratified, don't rename). Social attestation gets
  a NEW rung name: ATTESTED (schema change — confirmed_by scalar → set + provenance). REQ_ATTESTED
  is DESIGN-DRAFT, depends on the attributed-claim model.
- ECHO CASE (load-bearing): HIP is a transmission channel — if the system tells B a fact and B
  affirms it, that's an echo not evidence. Attestations MUST carry provenance to detect this.

## OPEN DECISIONS (Bill's calls, none urgent)
1. **trust_rung feature for the shadow scorer** — honoring "rank neither" for the LEARNER means
   giving it the two signals as TWO features + dropping the collapsed scalar. But that moves
   DECLARED_FEATURE_KEYS from 10 to 11, breaking the D-33 ten-key lock (an ABSOLUTE check).
   Decision: two features + break the lock, OR keep the lock and don't feed the scorer the trust
   record yet. Fable named 3 options, picked none — Bill's call.
2. Whether D-54 (bank pass3) committed — CONFIRM.

## THE D-46 CRITIQUE STUDY — WHERE WE ARE
Fable's D-46 critique of the seeding roadmap has 3 sections (Parts 1-3), banked at
docs/reviews/FABLE_D46_seeding-critique.md. Also ChatGPT pass1 critiques all 5 parts.
- **Section 1 (confirmation subroutine): COMPLETE** — resolved into the Part 1 model above.
- **Section 2 (seeding/onboarding): SUMMARIZED, NOT WORKED.** Five findings, open:
  2.1 narrator collects facts about others without consent (portrait model helps but doesn't
      fully solve COLLECTION consent — the big one); also a contextual-integrity violation at
      the WRITE point; collides with Part 4 "disclosure about another adult member" (unresolved).
  2.2 custodian per-fact confirmation causes rubber-stamping (fix: risk-tiered review); a
      declined dependent-fact has no other confirmer (dead-ends).
  2.3 minimum-seed metric unmeasurable (no denominator; every household degraded day-one).
  2.4 zone ordering uses persuasion techniques unnamed: Zone-1 = foot-in-the-door;
      "reflect don't interrogate" misappropriates motivational interviewing; prior art is
      progressive profiling (completion-rate incentive). The design uses persuasion while
      claiming "never force" — that gap must be named/defended.
- **Section 3 (boundary manager): NOT TOUCHED.** (withdrawal detection underspecified;
  sensitivity encoding mis-ranks 'critical' in code; "detail must serve family" was self-
  certifying — already fixed via evaluation portfolio in an earlier revision; Part1/Part3
  circular dependency.)
- **Parts 4 (safety) & 5 (cross-cutting): reviewed, deep findings, not studied.** Safety:
  "recognize+route never adjudicate" is too passive — must become "never determine guilt but
  ALWAYS assess immediate risk," 3 tiers; "store nothing" impossible+harmful, needs ephemeral
  safety path; account-holder-is-abuser has no safe storage. Cross-cutting: policy isolation
  NOT cryptographic isolation until per-member keys exist — the "strict isolation" CLAIM must be
  downgraded; legal exposure (subpoena, mandatory-reporting varies by jurisdiction).

## ENGINEERING DEBTS (clean, decision-light, ready to build)
- The trust-axis code (D-53 REQ) — build REQ_TRUST_AXES to "record both."
- Dyad-schema fix: dyads table has no member_a/member_b/caregiver/recipient columns but
  learner_isolation._audience_of reads them (D-36 finding c).
- Populate members.household_id — NULL for all 5 rows (bill/maya/sam/p4smoke_x/p4smoke_y),
  the D-31b limit; causes member-owned-fact confirmer lookups to dead-end.
- Lock-timestamp drift fix (see conventions).

## RECOMMENDED NEXT MOVES (for the new chat)
1. Confirm D-54 banked pass3 (screenshot the terminal).
2. Then either: (a) rule the trust_rung ten-key decision → build REQ_TRUST_AXES, or
   (b) study Section 2 of the critique one finding at a time (start 2.1, the collection-consent
   problem), or (c) knock out an engineering debt (dyad-schema is the easiest clean win).
None are urgent. The design is mapped and banked; nothing is at risk.
