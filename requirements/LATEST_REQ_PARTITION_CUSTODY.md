# REQ_PARTITION_CUSTODY: Stage 2 Ratification
Version: v20260721_0831
Status: NOT MET — 12/13 verified; row 3 deferred pending clinical-ethics review (Bill's D-21 ruling, 2026-07-29 — a known parked decision, not an unfinished build; see the OPEN DEFERRED DECISION block below)
Branch: roadmap
Reconciled against: crypto design 47851d7 (partition, s3); dyad spec 601ac25 (custody, s4-s6); plan of record 3532f90; fail-private decision (Bill, 2026-07-18); household-circle ratification (Bill, 2026-07-21); role-separation and custody-governance ratifications (Bill, 2026-07-21)

UPDATED 2026-07-20: D1/D2/D3 ratified by Bill in-session, ahead of the
REQ_CRYPTO_P1_DYAD_KEYS build (asked directly because that phase's own REQ
names this one as a hard prerequisite and nothing had recorded a decision
yet — checked git log, confirmed). D1: ratify as written (three-class
partition + five-rule order including rule 3) — ACCEPTED. D2: quorum
composition (operator escrow / household admin / second-principal-or-PoA,
2-of-3, operator alone insufficient) — ACCEPTED as proposed. D3: directive
vocabulary (exactly "just between us" / "share with the family" for this
demo) — ACCEPTED as proposed. Status stays NOT MET: this REQ's own
acceptance test additionally requires "the write-rule acceptance table
passes against a fixture" (the 9-row table), which is NOT built — Phase 1
implemented only rule 3's deterministic dyad-membership lookup
(harness.dyad_registry.get_active_dyad_for), used opt-in for its own demo
write and harness proof, not the full 5-rule write-time classifier (member
directive detection, sensitivity-based routing, the fixture-table run
itself). That remains Stage 4 phase 2's job (REQ_CRYPTO_P2_PARTITION_SEALED).
See DISPATCH_CRYPTO_P1_DYAD_KEYS__stage4-phase1-build__v20260720_0910.md.

UPDATED 2026-07-20 (second update, dyad access model): Bill ratified the
dyad-private access model, confirmed by two independent external reviews
(two-review reconciled). This resolves BLOCKING-OPEN ambiguity 1 of
REQ_CRYPTO_HARNESS_V2 (dyad-private conflated pair-private with
care-team-private) and amends D1's three-class partition IN PLACE: the
single "dyad-private" class is split into CARE-TEAM-PRIVATE and
PAIR-PRIVATE, the five-rule write order is replaced by the four-level
precedence order below, compound statements are split rather than
single-classified, and sensitivity no longer determines audience (handling
only). The sections below are edited to the ratified model; the pre-split
text survives in git history. Docs only — nothing here is built; the
write-time classifier remains Stage 4 phase 2's job and this REQ's status
stays NOT MET until the acceptance table passes against a fixture.

UPDATED 2026-07-21 (decision #2, household-circle ratified): Bill ratified
the household-shared audience — it was a scope name, not a defined
audience, until now. HOUSEHOLD-SHARED is renamed HOUSEHOLD-CIRCLE-SHARED
throughout this doc, gets its own enrolled roster, its own key class, and
an explicit enrollment/removal procedure, mirroring how CARE-TEAM-PRIVATE
was made a real roster rather than an inferred one. This is additive to
the 2026-07-20 dyad access model ratification — it does not reopen or
change any already-ratified dyad/precedence content. Status stays NOT MET:
the acceptance table still has not been run against a fixture, but rows 1
and 7 (the household rows) are now writable against a defined rule instead
of an undefined one.

UPDATED 2026-07-21 (decisions #3 and #6 ratified): Bill ratified role
separation (#3 — AUTHOR/SUBJECT/OWNER/BENEFICIARY resolved per clause,
subject-visibility wrap omission, the mandatory subject-exclusion rule
generalized) and custody consent/revocation/abuse resistance (#6 —
tiered consent, the peer-cannot-revoke-alone asymmetry, custody as
read-and-attestation agency only, one governance fabric across circle
enrollment/care-team enrollment/custody). This closes the six-ambiguity
backlog from REQ_CRYPTO_HARNESS_V2 (#1 dyad access model and #2
household-circle already closed above; #4, the CONFIRMED definition, is
ratified in REQ_CONFIDENCE_DISCIPLINE, a separate doc — not this one's
scope). Additive to everything already ratified in this doc, with one
named exception: the mandatory subject-is-caregiver rule (originally part
of the 2026-07-20 dyad access model) is WIDENED, not left intact — see
"Role separation" below for why a parallel rule was rejected in favor of
generalizing the existing trigger. Status stays NOT MET: nothing here is
built, and the acceptance table — still the 13-row table from #1/#2, not
extended with new rows for #3/#6 — still has not run against a fixture.

UPDATED 2026-07-29 (D-18, first real run of the 13-row acceptance table):
`python3 -m eval.harness --layer 7` run against the dev graph
(bolt://localhost:7688), sourced .env.dev, DEV_MARKER.txt present /
DEMO_MARKER.txt absent. 12 of 13 rows are clean; row 3 surfaces a real,
previously-unreconciled discrepancy between this doc's own text and the
ratified coordination/observation enum — flagged below, not papered over.
Full log: /tmp/l7_full_run.log.

- Rows 1-9 (scenario `P4`, eval/harnesslib/layer7_crypto.py) — the
  harness reports "all 9 rows classify to the expected class/dyad"
  against ITS OWN hardcoded per-row expectations (row1 household-circle
  via 3a; row2 care-team via 3b, correctly including maya per the
  ratified role-separation model, not just sam; row3 pair-private via
  3c; row4/5/8/9 member-private; row6 member-private via the private
  directive; row7 household-circle via the share-household directive).
  P4's own fault-injection (row4 checked against a deliberately wrong
  expected class) correctly reports MISMATCH, proving the comparison can
  fail, not just pass by construction. Live sealing round-trip also
  green: row1 household-circle reads for maya, row2 the active caregiver
  (sam) reads but a non-caregiver (bill) doesn't, row6 the author (bill)
  reads but another member (maya) doesn't.

  **ROW 3 FLAGGED, not a clean pass.** This doc's own acceptance-table
  text (below) says row 3 ("Ray is on metformin", maya, same care team)
  expects care-team-private. The harness's own p4_rows fixture instead
  hardcodes CLASS_DYAD (pair-private, sealed to the maya-ray dyad) as
  row 3's expected value — unchanged since the fixture was first written,
  confirmed via `git log -p` on layer7_crypto.py, unlike row 2's sibling
  tuple, which carries an explicit 2026-07-21 comment recording its
  expected value flipping from CLASS_DYAD to CLASS_CARE_TEAM under the
  ratified role-separation model. Row 3 got no equivalent update or
  comment. Root cause traced to harness/extraction_queue.py's
  CANONICAL_ATTRIBUTES: "medication" (a standing fact — "Prescription or
  OTC medications the person takes") and "medication_status" (a change —
  "started, stopped, switched") are two distinct canonical attributes;
  only "medication_status" is in write_rule.COORDINATION_ATTRIBUTES.
  "Ray is on metformin" is a standing fact, canonical attribute
  "medication", so it never reaches level 3b's care-team default — it
  falls to level 3c's mandatory subject-exclusion and lands pair-private
  (maya-ray only), NOT care-team (maya+sam), because the code's
  classify() call in the P4 fixture is passed attribute="medication".
  This is a real behavioral question, not a typo: under the current
  code, Sam (Ray's other enrolled caregiver) does NOT learn what
  medication Ray is on unless Maya's utterance is independently
  reclassified as a status CHANGE or Maya uses the "share with the care
  team" directive. This sits in tension with this doc's own STATED COST
  section, which names "pair-private-as-default hides falls and
  medication events from the other caregiver" as exactly the silent
  safety failure the care-team default was chosen to avoid — though
  that section's own wording ("medication events") could be read as
  scoped to status CHANGES specifically, not standing medication facts,
  making this a genuinely open policy question rather than a clear bug
  either way. NOT resolved by this session — flagged for Bill's ruling:
  either (a) ratify that standing medication/clinical facts about the
  recipient are correctly mandatory-exclusion by design, and correct
  this doc's row 3 text to match what row 2's sibling comment already
  models, or (b) rule this a gap, and widen COORDINATION_ATTRIBUTES (or
  the level-3b test) so standing medication facts about an enrolled
  care recipient default to care-team-private like row 2's incident
  does. This is a policy call, not something this session should decide
  unilaterally.
- Rows 10-11 (scenario `P4-EXT`, layer7_crypto_v2.py) PASS — row10 lands
  pair-private on the real sam-ray dyad (via level 3c, not the level-2
  directive path the table's own annotation names — the table's DECISION
  is matched, the firing rule differs, flagged in-line in the harness
  output, not hidden); row11 lands member-private via
  `3c-mandatory-exclusion-narrowed`, proving the subject-is-a-caregiver
  exclusion is mandatory, not author-optional.
- Row 12 (scenario `P4-EXT-row12`) PASSES against a REAL splitter
  (harness.compound_split), not pre-split clauses: "Ray fell and Susan
  can't cover Tuesday" decomposes into exactly 2 clauses, clause 1
  (the fall) lands care-team-private, clause 2 (Susan's availability)
  lands member-private. Honest scope boundary disclosed in-code: this
  splitter handles the clean and/semicolon case only, not pronoun
  back-reference — the REQ's own three-clause worked example ("she"
  resolving to "Maya") is a harder case not exercised by this scenario.
- Row 13 (scenario `P4-EXT-row13`) PASSES — ray's standing-policy
  restriction on sam is honored; the row's own premise (excluding sam
  from a care-team-private default) doesn't literally arise for a
  non-coordination attribute like "financial" (it routes narrower, via
  3c, before any care-team default is reached), so the restriction is
  satisfied a fortiori by the narrower scope rather than by an explicit
  `excluded_member_ids` entry — flagged in-line, not hidden.

Full run: `== L7: 25/25 (0 flaked, 0 skipped)`, `== L7V2: 27/28 (0 flaked,
1 skipped — CT-OUTPUT-GAP, opt-in-only, unrelated to this table)`,
`RATCHET PASS — no scenario regressed vs baseline`.

Status stays NOT MET: 12/13 rows clean, row 3 is a genuine open
discrepancy between this doc's text and the ratified/implemented
enum, not a mechanical failure — this session does not rule on it and
does not stage a MET flip while it's open, per standing instruction
never to self-mark MET. Once Bill rules on row 3 (and, if needed, this
doc's row 3 text or the code is corrected to match), re-run the table
before any MET flip is considered.

UPDATED 2026-07-29 (D-21, Bill's ruling — row 3 PARKED as an OPEN DEFERRED
DECISION): 12 of 13 acceptance rows pass (D-18's first real run of the
table, recorded in the update above). Row 3 — care-team access to a
STANDING medication fact — is NOT an engineering defect but an unresolved
clinical-ethics policy question requiring review by a medical expert and an
ethicist before ratification. The current built behavior stands as the
conservative default: the care team receives medication_status CHANGE
events (care-team-private via the coordination enum), not the standing
medication list, which seals pair-private under the level-3c mandatory
exclusion; widening the standing list to care-team-private requires the
owner to explicitly share, OR a future ratified policy adding `medication`
to the coordination enum. This default was chosen to err toward less
sharing pending expert review, not as a final answer.

The two candidate resolutions the reviewers will choose between:
- OPTION A: add `medication` to the coordination/observation enum, so
  standing medication facts about an enrolled care recipient default to
  care-team-private (row 3's original expected value; D-18's branch (b)).
- OPTION B: keep changes-only — the code's current behavior; ratify it and
  correct this doc's row 3 text to pair-private (D-18's branch (a)).

Until that review lands, this REQ stays NOT MET by design; no MET flip is
staged or implied.

## What this is

The partition and custody policy, ratified. The specs designed it; this REQ makes it the buildable law. Stage 3's invariants and every Stage 4 phase build against this doc. Nothing in Stage 4 starts until this is MET.

MET for this REQ means: Bill has confirmed each numbered decision below, and the write-rule acceptance table passes against a fixture. There is no code in this REQ; the code is Stage 4.

## The partition: four scopes (ratified 2026-07-20, two-review reconciled)

Every fact is in exactly one scope at write time. The scope decides which keys can unwrap its DEK. Scopes name the audience always — the bare word "private" must never appear in a classification, a UI, or a log line; a scope without a named audience is not a scope.

1. HOUSEHOLD-CIRCLE-SHARED (renamed 2026-07-21, was HOUSEHOLD-SHARED — the rename self-documents "roster, not label"): the explicitly enrolled household circle can read — never inferred from cohabitation, adulthood, surname, network presence, or authentication. Its own key class: a household-circle X25519 key per home, epoch-versioned, wrapped per enrolled member's device, rotated on removal (mirrors the care-team key extension). Default is EXCLUSION — an unenrolled device or person authors as member-private and has zero household-circle read, full stop. The audience is an enumerated roster even when the default enumeration is "all adults" — a classification label is not an ACL.
2. CARE-TEAM-PRIVATE: the care recipient plus ALL explicitly enrolled caregivers of that recipient. The care team is an enumerated list per recipient, never inferred from household membership. Its own key class: a care-team key wrapped to each enrolled caregiver (see the design docs' care-team key extension). This is the coordination class: "Ray fell last night" written by Sam is readable by Maya too, because both are Ray's enrolled caregivers.
3. PAIR-PRIVATE: the care recipient plus ONE named caregiver. DEK sealed to that single dyad's keypair. This is the confidence class: what Ray told Sam alone stays with Sam.
4. MEMBER-PRIVATE: the authoring member only. DEK sealed to that member's keypair alone.

There is no fifth scope. A fact that fits nothing above is member-private. That is what fail-private means.

The old single "dyad-private" class conflated scopes 2 and 3 ("each dyad is isolated" vs "readable by their caregivers, plural" are different policies); it is retired and must not appear in new code or docs.

**Roster invariant (added 2026-07-21):** all four scopes are explicit key-wrap rosters, without exception. A scope label never grants access by itself — every fact records the exact pubkey IDs authorized to decrypt it. "Household-circle-shared" is a roster the same way "care-team-private" and "pair-private" are; none of the four scope names are self-enforcing.

## The write rule: four-level precedence, highest first

At write time, in strict precedence order (a higher level always overrides a lower one):

1. OWNER'S STANDING POLICY (generalized 2026-07-21, was "recipient's" — see Role separation below for how OWNER is derived; substance unchanged for the recipient case). OWNER's explicit grants and restrictions ("do not share my financial info with Sam"; "only Maya may discuss my behavioral health"). These are standing policy objects evaluated deterministically at write and read time — NOT free-text the model may weigh or ignore. Where OWNER lacks capacity, an explicitly recognized legal or delegated authority sets this policy — never whichever caregiver happened to enroll first.
2. EXPLICIT PER-FACT AUTHOR DIRECTIVE. "Share with the care team" / "keep this between us" / "private note for me." The system visibly confirms the resulting audience at write time ("visible to Maya and Sam"), so the effect of the directive — or its absence — is never invisible. Household-circle widening restriction (added 2026-07-21): an author may use a level-2 directive to widen to household-circle-shared only for facts about the author themself or generic household facts; widening a fact whose subject is another person requires that person's standing policy (level 1), not merely the author's say-so — this closes the same hole that made subject-is-a-caregiver mandatory at level 3, one level up. Narrow-versus-widen rule, stated explicitly (added 2026-07-27, RULING on a discrepancy REQ_COVERAGE_MEASUREMENT's coverage-grid work found): a level-2 directive that NARROWS scope — e.g. "share with the care team" directing a household-attribute fact to CARE-TEAM-PRIVATE, narrower than its level-3 household-circle-shared default — is safe and permitted; nothing above restricts narrowing, and the constraint this doc states is on WIDENING only, per the household-circle widening restriction one sentence up. The two prior sentences already say this in full (widening to household-circle-shared is restricted to author/generic-household facts; widening beyond a fact's level-3 default for another person requires that person's own standing policy) — this sentence exists only to make the NARROW/WIDE asymmetry unmissable, since its absence was read as a blanket restriction on any level-2 redirection of a household attribute, which it was never meant to be. The mandatory subject-exclusion rule below stays a hard, non-overridable constraint regardless of narrow-or-widen framing — narrowing never overrides it either. Safety-concern directive (added 2026-07-21, role separation #3): a distinct level-2 directive, "flag as safety concern," separate from "share with the care team" — the only lever that can escalate a characterization about another person to CARE-TEAM-PRIVATE-MINUS-SUBJECT (see SUBJECT_VISIBILITY below); an ordinary "share with the care team" directive cannot do this on its own when the fact characterizes someone other than the author.
3. ATTRIBUTE + SUBJECT CLASSIFICATION (the deterministic default). Care/health/safety/coordination facts about the recipient default to CARE-TEAM-PRIVATE. Household logistics (attribute == household) remain household-circle-shared (renamed 2026-07-21) as a LEVEL-3 default — level 1 can restrict that default in either direction but can never grant household-circle access to a person who is not enrolled in the household circle. Mandatory subject-exclusion rule, GENERALIZED 2026-07-21 (role separation #3; was "any fact whose SUBJECT is another enrolled caregiver seals PAIR-PRIVATE MANDATORILY" — that trigger is widened in place, not replaced by a parallel rule): any fact where SUBJECT != AUTHOR and the ATTRIBUTE is NOT in the coordination/observation enum (incident, medication_status, appointment, vitals, care_plan) seals PAIR-PRIVATE-OR-NARROWER MANDATORILY — this now covers SUBJECT being the recipient as well as SUBJECT being another enrolled caregiver. This is a HARD, non-overridable constraint: it is not author-optional and cannot be released downward by level 2 except through the safety-concern directive above; Sam's note about Maya, and Susan's characterization of Dad, must never default into their readable set.
4. SENSITIVITY affects HANDLING ONLY — encryption strength, logging suppression, authentication requirements, external-model eligibility. Sensitivity NEVER determines audience by itself. The old rule that routed high/critical-sensitivity facts to a privacy class is retired: a probabilistic classifier output may harden how a fact is handled, but only deterministic facts (policy, directive, attribute, subject, enrollment) decide who reads it.

Uncertainty rule (decided, Bill 2026-07-18, unchanged): if classification cannot be determined, or extraction fails, the fact is member-private. Fail-private. The author directive is the release valve. Cost accepted: over-walling, released by the owner re-sharing.

## Compound statements are split, never single-classified

A statement with mixed audiences is SPLIT into separate facts, each classified independently — it is never assigned one class covering the whole utterance. "Ray fell because Maya keeps leaving him alone, and she's irresponsible" splits into: the fall event (care-team-private — coordination fact about the recipient), the concern about Maya (pair-private or member-private — subject is another enrolled caregiver, level-3 mandatory), and the opinion of Maya (member-private). One utterance, three facts, three audiences. A classifier that cannot split falls back to fail-private for the whole statement.

## Role separation (#3, ratified 2026-07-21)

Four roles, resolved per clause — after compound splitting, so each clause carries its own role set — deterministically, no model call:

- AUTHOR: the authenticated identity whose device key signed the write. Always exactly one; never inferred.
- SUBJECT: the person the clause asserts ABOUT, from the existing subject-resolution mechanism run against the enrollment roster. Merely being mentioned is not being the subject. Unresolvable (no enrolled subject can be determined) -> MEMBER-PRIVATE, the same fail-private landing as every other unresolvable case in this doc.
- OWNER (derived, not author-filled): SUBJECT when SUBJECT is an enrolled member with standing-policy rights (the recipient, or symmetrically any member with a first-person policy over facts naming them); otherwise AUTHOR. OWNER names whose level-1 policy applies — level 1 above is generalized from "recipient's" to "OWNER's" for exactly this reason.
- BENEFICIARY: not an input. It is the computed key-wrap target set — the output of the audience-from-roles rule below, never a field an author fills in. Letting an author self-declare a beneficiary would let them route around the mandatory rule.

Audience-from-roles, in order: resolve the four roles for the clause -> levels 1-3 above pick the scope -> build the key-wrap set from OWNER's applicable groups (member/dyad/care-team/household-circle key material as the scope dictates) -> apply mandatory subject exclusions (below) -> if any role cannot be resolved, MEMBER-PRIVATE. Two deterministic axes decide the mandatory-exclusion question: is SUBJECT == AUTHOR, and is the ATTRIBUTE in the coordination/observation enum (incident, medication_status, appointment, vitals, care_plan) — never a subjective "is this an allegation" judgment.

SUBJECT_VISIBILITY (NEW per-fact field, ratified 2026-07-21): INCLUDE or EXCLUDE, applied at key-wrap construction, not at decryption time — the subject's device key is simply not among the keys a care-team-class DEK is wrapped to for this value_version. This is wrap omission, the same mechanism the rest of this doc already uses ("scope decides which keys seal the DEK"); it is NOT a fifth scope, and NOT a policy filter layered on top of a key the subject could otherwise use to decrypt. Default EXCLUDE when AUTHOR != SUBJECT and the attribute is a characterization, allegation, opinion, or undiscussed clinical note (not in the coordination/observation enum). Default INCLUDE when SUBJECT == AUTHOR, when the attribute is coordination/observation-class (an observed care event is never hidden from the recipient — that is the "silent safety failure" the STATED COST section below already rejected, and this rule does not reopen it), or when an explicit directive (level 2) widens it.

Composition with precedence: role resolution runs BEFORE the four levels — the levels above are edited in place to consume AUTHOR/SUBJECT/OWNER as named inputs rather than hardcoding "recipient" or "caregiver." This is a refinement of level 3, not a fifth precedence level: it conditions only on enumerable inputs (attribute-class membership, identity equality), preserving deterministic-over-probabilistic. The prior mandatory rule ("subject is another enrolled caregiver") is WIDENED in place to the general form above rather than left standing beside a new parallel rule for "subject is the recipient" — two overlapping mandatory rules for adjacent cases would drift out of sync; one generalized trigger does not.

Honest limit, stated here rather than left implicit: the EXCLUDE default can under-flag a real risk framed as a private characterization (a drinking concern that is actually a dangerous medication interaction, told to only one caregiver who never reaches for the safety-concern directive) — a narrow, deliberate reintroduction of the same forgot-to-mark cost the STATED COST section below already accepted for the care-team default, not a new failure class. Every objectively observable safety/care event stays care-team-private, unchanged, so that earlier trade does not regress. And a limit no rule here closes: HIP cannot verify that an authorized author's assertion is true — role separation governs WHO reads a claim, never whether the claim is honest.

## Why deterministic-over-probabilistic still holds

The precedence order keeps the ratified principle: levels 1-3 are all deterministic (policy objects, explicit directives, attribute strings, subject identity, enrollment registry lookups). The one probabilistic signal, sensitivity, is confined to level 4 where it can only harden handling, never widen or narrow an audience. Care-team membership is a fact of the enrollment registry (deterministic), exactly as dyad membership was under the old rule 3.

## STATED COST (a limit of the ratified model, not hidden)

The care-team default leaks forgotten confidences: if a caregiver does not mark a confidence pair-private at write time, the other enrolled caregivers see it, irreversibly. A keyless recipient's confidences are only as safe as the caregiver they confide in remembering to mark them — partly mitigated by the recipient's standing policy at precedence level 1, which holds regardless of any one caregiver's diligence. This cost is ACCEPTED deliberately, to avoid the alternative's silent safety failure: pair-private-as-default hides falls and medication events from the other caregiver, and that failure surfaces in the physical world with no warning. Honest limit on caregiver removal: rotation blocks future reads; it cannot make someone forget or delete plaintext already downloaded.

Two further honest limits, stated plainly rather than left implicit (added 2026-07-21):

1. The system enforces exactly the roster and policy it is given. It cannot adjudicate legitimacy if every sponsor or quorum-holder for a circle, care team, or dyad is simultaneously compromised — no cryptographic scheme in this design can. What it guarantees instead: every membership change is attributable, quorum-gated, and ledger-recorded, so a compromise is discoverable and reversible-going-forward, not silent.
2. Revocation — of a household-circle member, a care-team member, or a dyad custodian — is "no new access," not "unremembers." It stops future reads; it cannot make a former member forget or delete plaintext already downloaded before removal. This limit applies identically across all three roster types and is not unique to the household circle.

## Custody policy (from the dyad spec, ratified as-is)

- The custodian holds the dyad key on the care recipient's behalf. The recipient needs no device.
- Entry: consent event + key grant (D_priv sealed to the new custodian's member pubkey). HEL event: custody.grant.
- Exit: atomic revocation + dyad re-key + DEK re-seal, so the old key is dead forward. HEL event: custody.exit. Honest limit, stated everywhere it matters: exit is "no new access," not "unremembers."
- Non-cooperative eviction uses the SAME 2-of-3 quorum primitive as key recovery. HEL event: custody.evict.
- Overlapping dyads: a member holds one key per dyad (a keyring). A pair-private fact belongs to exactly one dyad; care-team-private facts seal to the recipient's care-team key, wrapped to each enrolled caregiver.
- Care-team key epochs (ratified 2026-07-20): a newly added caregiver receives the CURRENT epoch by default — future care-team facts plus current active facts (medications, allergies, care plans). Historical events require an explicit backfill grant; historical access is never inferred from current membership. On removal: rotate the care-team key (new epoch), block future reads, revoke sessions and cache. Removal cannot make someone forget or delete plaintext already downloaded.

## Household circle enrollment (ratified 2026-07-21, option A)

- Routine add: any existing circle member sponsors the new enrollment. Keypair ceremony wraps the current household-circle key epoch to the new member's device key. The add is announced and logged as a HEL `custody.grant` event, same event family as dyad/care-team custody. Any circle member may contest a routine add.
- A contested add, or any removal, escalates to the same 2-of-3 recovery/eviction quorum used for dyad custody — no unilateral household-circle membership change survives a contest.
- Removal: rotates to a new household-circle key epoch, re-wraps the corpus under the new epoch, destroys the old wraps, invalidates the removed member's sessions and cache, and takes effect without the removed person's consent.
- New members receive the CURRENT epoch only by default, mirroring the care-team epoch rule above; historical household-circle facts require an explicit backfill grant, never inferred from current membership.
- Paid home-health workers are enrolled in the relevant care recipient's CARE-TEAM, never in the HOUSEHOLD-CIRCLE — a paid worker's access is scoped to the recipient they serve, not to the household's general roster.

## Custody consent, revocation, and abuse resistance (#6, ratified 2026-07-21)

**Consent.** A caregiver may never self-appoint as custodian. Entry always requires a signed HEL custody-grant event from a source OTHER than the incoming custodian — the candidate's own attestation is never sufficient on its own. Three tiers by the recipient's capacity, which HIP never determines itself:
- Tier A (capacity): the recipient affirms the grant via a witnessed channel, attested by a non-candidate.
- Tier B (no capacity, a legal or delegated authority exists): that authority executes the grant; the instrument's hash is recorded as the event's source_class; self-appointment by the authority is announced and contestable, escalating to the same 2-of-3 quorum as recovery/eviction if contested.
- Tier C (no capacity, no authority exists): provisional custody only — time-boxed, reduced powers, auto-escalates to quorum review before it can become ordinary custody. Capacity itself is never HIP's own determination; the system records who asserted it and on what instrument, never adjudicates it.

**Revocation.** A capacitated recipient may revoke custody unilaterally — no quorum required, their own standing policy at level 1 is sufficient. A recognized authority may revoke if its instrument is valid and uncontested. A PEER CAREGIVER ACTING ALONE CANNOT REVOKE another custodian — peer-initiated revocation always requires the same 2-of-3 quorum as recovery/eviction, a deliberate asymmetry against the cheaper household-circle removal path above: evicting the honest custodian is itself the shape of an isolation attack, and a single peer's say-so must never be sufficient to accomplish it. A contested PoA or an estrangement dispute freezes custody at last-known-good, with elevated logging; the quorum may impose an interim custodian, but never adjudicates the legal instruments on their content — that determination stays outside HIP. Custodian resignation triggers a continuity event: no path in this design leaves the recipient custodian-less silently.

**Abuse resistance.** Custody grants read-and-attestation agency and nothing more. It does not grant: unilateral removal of a caregiver, a silent rewrite of the recipient's standing policy (a capacity-era policy always outranks any custodian's directive at level 1, permanently), or a cryptographically indispensable key (every custody key participates in the same 2-of-3 recovery-share scheme as everything else — no custodian holds a key nothing else can reconstruct). The custody key itself is non-exportable, usable only through the policy path, never extracted raw. Detection is logging that informs humans, never an automatic block: every custodian act is signed AS-CUSTODIAN, and anomaly detection surfaces patterns (bulk reads or exports, financial-record concentration, unusual policy-change frequency, scope-skew relative to the custodian's normal activity) for a human to review. What this cannot do, stated plainly: it cannot stop a custodian from reading within their legitimately granted scope, cannot detect exploitation that happens outside the system entirely, and cannot judge intent from the shape of the data alone.

**Composition.** One governance fabric, not three separate ones: the same 2-of-3 quorum, the same HEL ledger, the same option-A sponsor-plus-contest pattern already ratified for household-circle enrollment above, reused unchanged for care-team enrollment, custody grant/revocation, and audit. Three distinct objects, never conflated: standing policy (what OWNER has decided), authority (who may act on OWNER's behalf when OWNER cannot), and custodian (who holds operational key access). Every quorum action names, explicitly, which of the three it is changing. A new custodian receives the current epoch plus future events by default; historical access requires an explicit backfill grant, exactly the epoch rule already ratified for care-team and household-circle keys.

Honest limit, stated here rather than left implicit: the quorum fires once someone notices and contests — it cannot fire on its own. The singleton family, where one caregiver is the sole custodian and effectively the only human anywhere near the quorum, is faithfully served by this design and unprotected by it: there is no fourth party to notice. HIP is built to be a witness — a signed, court-readable record of who did what and on what authority — not a guardian that intervenes on its own judgment. That is a deliberate design boundary, not an oversight, and it is stated here so it is never mistaken for a guarantee this system does not make.

## Observation-and-perception custody — RATIFIED, WITH NAMED EXCEPTIONS (dated 2026-07-27, DISPATCH 43; positions landed 2026-07-27, DISPATCH 39)

**RATIFIED**, except where noted below. Position 1 carries a stated
caveat — settled provisionally, not final. Position 2 is ratified in
amended form and is itself named as a position pending legal and
care-model review, the same posture as position 1's caveat. Positions 3
and 4 are ratified without caveat. The two sub-questions below remain
genuinely open, not ratified by this update. Nothing below is part of
this REQ's MET criteria (the DECISIONS FOR BILL section below is
unchanged by this ratification) or its acceptance table — these
positions would need their own acceptance items, written when this REQ's
Stage 3 fixture work reaches them.

Cross-reference: `docs/deliverables/HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md`
Section 10 ("Long vision") and its Open Questions list, the item named
"Observation-and-perception custody" — cited here by subject, not by
number, per that document's own DISPATCH 42 naming-fix precedent: its
Open Questions list has already been renumbered twice in one day, and a
bare numeric cross-reference goes stale exactly the way DISPATCH 42 found
and fixed for Section 6's own cross-reference into that same list. That
document's own words when these positions were first landed (DISPATCH
39): "The observation-and-perception custody question is named here as
open, awaiting ratification of stated positions, not as undefined...
Ratifying these positions means writing them in." This section is that
ratification.

These positions extend the write rule above (level 3's "ATTRIBUTE +
SUBJECT CLASSIFICATION") to a fact SOURCE none of the four precedence
levels currently name: a system observation — a sensor, a camera, a
continuous-listening device — rather than a member's own utterance.

**The positions:**

1. A system-observed fact whose subject is a caregiver seals to that
   caregiver and the recipient only. RATIFIED 2026-07-27, WITH A STATED
   CAVEAT, Bill's own words: ratified for now; the care model is not yet
   understood well enough to know what is legally and ethically
   required, so this is settled provisionally and revisits when the
   care-model and legal review land.
2. Presence versus naming, not presence versus nothing. RATIFIED
   2026-07-27 IN AMENDED FORM — the original flat rule here, "non-members
   captured by sensors are never stored without enrollment," is replaced
   by a three-way split:
   - BARE PRESENCE without identity resolution — a person was present,
     unidentified — may be stored as a household-scoped event. This is
     the perception version of an unresolved subject, and belongs to the
     household.
   - IDENTITY RESOLUTION against a non-enrolled person is REFUSED.
     Minting a fact about a named individual who never enrolled fails
     closed: no key, no scope, no standing policy, and a distinct legal
     exposure for an operator storing identified facts about
     non-subscribers.
   - An enrolled member or an existing subject is handled by the
     existing scopes, unchanged.

   FLAGGED, not settled: the presence-versus-naming line itself is a
   position pending legal and care-model review, the same posture as
   position 1's caveat above. Ratified as the working rule, not as
   final.
3. Perception is process-and-discard: frames are never retained, only
   the derived sealed fact. RATIFIED 2026-07-27. The limit stated in the
   same breath: at inference, the model sees the frame in memory to
   derive the fact, so the at-inference gap applies to perception
   exactly as it does to text — the same shape REQ_CRYPTO_P2_PARTITION_
   SEALED's own CONSTRAINT already states for a fact value ("the model
   seeing plaintext is not the same as the server being able to derive
   it," `REQ_CRYPTO_P2_PARTITION_SEALED__stage4-phase2__v20260719_0840.md:82`).
   Operator-blind-at-rest survives this ratification. Operator-blind-
   at-inference does not, and is named here rather than left implicit.
4. Observation may CORROBORATE a fact but may never CONFIRM one.
   RATIFIED 2026-07-27. The same principle as speaker ID and
   repetition-never-raises-status: a mechanism with an error rate cannot
   mint CONFIRMED. Precedent already ratified elsewhere in this
   codebase, not invented for this position:
   `REQ_CONFIDENCE_DISCIPLINE__truth-track__v20260721_0945.md` demotes
   voiceprint match from gate to hint ("never sufficient alone to admit a
   turn as a given member," citing `server/voice_orch.py:1405-1471`) and
   states that repetition alone never raises trust level (the
   `CONFIRMED > CORROBORATED > ASSERTED > UNCONFIRMED/DERIVED` ordinal
   ladder, `memory_engine/trust.py:27-34`, is provenance-of-corroboration-
   event, not a repeat-count). Position 4 is the same rule applied to a
   third class of imperfect signal.

**Still genuinely open — sub-questions, not positions, not ratified by
this update:**

- Whether the recipient's standing policy (this REQ's own precedence
  level 1) extends from disclosure — what is later shared — to
  COLLECTION — what is sensed at all. No observation in my bedroom, in
  Bill's own framing, is the concrete shape of this question. Meaning
  whether a recipient can restrict what the system senses, not only what
  it later tells someone; and whether that extension, if ratified,
  survives the recipient's own incapacity via the recognized authority
  (this REQ's Custody consent section above, Tier B/C).
- How a system-observed fact classifies when no AUTHOR exists for the
  mandatory subject-exclusion rule (this REQ's level 3c, keyed on
  `SUBJECT != AUTHOR`) to fire on — every write-time rule in this REQ,
  levels 1 through 3c, assumes an authenticated human author; a sensor
  observation has none, and nothing above says what stands in for AUTHOR
  when deciding whether the mandatory exclusion applies.

## DECISIONS FOR BILL (the REQ is MET when these are answered)

D1. Ratify the three classes and the five-rule write order above, including rule 3. [yes / amend] — RATIFIED 2026-07-20 as originally written, then AMENDED same day by the dyad access model ratification (two-review reconciled): four scopes and the four-level precedence order above supersede the three-class/five-rule text D1 originally named. The amendment is Bill's own decision, not a build session's interpretation.

D2. Quorum composition, the open Stage 4 governance call, decided now so Stage 4 does not stall. Proposed, per the spec's example: share A operator escrow; share B the household admin (Bill in the demo); share C a second family principal OR a verified legal instrument (PoA credential). Any 2 of 3 recover a key or evict a custodian; the operator's single share is cryptographically insufficient alone. [accept / name different holders]

D3. Directive vocabulary. The demo recognizes exactly two directives: "just between us" (member-private or pair-private per subject) and "share with the family" (household-circle-shared, renamed 2026-07-21). Everything subtler is post-demo. [accept / expand] — ACCEPTED 2026-07-20; the dyad-access-model ratification adds "share with the care team" (care-team-private) as a third recognized directive at precedence level 2.

## THE ACCEPTANCE TEST (pass/fail, runs against a fixture at Stage 3)

Write each row's utterance; assert the class:

| # | Utterance (speaker) | Expected scope |
|---|---|---|
| 1 | "Trash day moved to Thursday" (bill) | household-circle-shared (level 3, attribute) |
| 2 | "Ray fell last night" (sam, sam and maya both enrolled caregivers of ray) | care-team-private: ray's care team [maya, sam] (level 3, coordination fact about recipient) |
| 3 | "Ray is on metformin" (maya, same care team) | care-team-private: ray's care team [maya, sam] (level 3) |
| 4 | "I've been feeling depressed" (bill, high sensitivity, no care relationship) | member-private (fail-private default; sensitivity hardens handling only, level 4) |
| 5 | "I like black coffee" (bill) | member-private, member-shareable (default) |
| 6 | "Just between us: I'm worried about money" (bill) | member-private (level 2, directive) |
| 7 | "Share with the family: I'll be traveling in May" (bill) | household-circle-shared (level 2, directive) |
| 8 | Extraction failure / sensitivity unknown (any) | member-private (fail-private) |
| 9 | "Ray fell" (sam) when sam is NO LONGER an enrolled caregiver of ray | member-private to sam (level 3 requires ACTIVE enrollment) |
| 10 | "Keep this between us: Ray told me he's scared of falling again" (sam) | pair-private: [sam, ray] (level 2, directive names the pair) |
| 11 | "Maya keeps leaving Ray alone all day" (sam, maya is an enrolled caregiver) | pair-private/member-private to sam — MANDATORY, subject is another enrolled caregiver (level 3); a level-2 "share with the care team" directive must NOT release it into maya's readable set |
| 12 | "Ray fell because Maya keeps leaving him alone, and she's irresponsible" (sam) | SPLIT into three facts: fall event → care-team-private; concern about maya → pair/member-private (mandatory); opinion of maya → member-private. One scope for the whole utterance is a FAIL |
| 13 | "Ray's bank balance is low" (sam), ray's standing policy: "do not share my financial info with Sam's siblings" | audience excludes the restricted caregivers regardless of level-3 default (level 1 overrides) |

Row 9 is load-bearing: it proves exit changes future writes, not just future reads. Row 11 is load-bearing the other way: it proves the subject-is-a-caregiver rule is mandatory, not author-optional. Row 12 proves splitting; row 13 proves the recipient's standing policy sits above everything.

Rows 1 and 7 are now writable against a defined household-circle roster and key class (2026-07-21) — previously "household-shared" named an audience without a defined enrollment or key, so those two rows could not have been meaningfully asserted against a fixture even if the table existed. The table itself, all 13 rows, still has not been run — status stays NOT MET.

## CONSTRAINTS

- This REQ defines policy; it changes no code. Stage 4 phase 2 implements the write rule; Stage 3 mechanizes this table.
- Nothing here weakens the operator-blind target: class decides WHICH member keys seal the DEK; no class seals to an operator key.
- The write rule must be implementable from fields that exist at write time (speaker, subject, attribute, sensitivity, dyad registry, directive). No new model calls on the write path.

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, as a co-equal objective to the policy itself. We do not rig the build for it.

SHOW: The write-rule table (rows 1-13) run live. Speak each utterance, show the scope it lands in with its named audience. "Ray fell last night" -> care-team-private [maya, sam]. "Trash day moved to Thursday" -> household-circle-shared. The compound row 12 splitting into three facts with three audiences, visibly. Extraction failure -> member-private. The rule firing, visibly, not narrated.

LET THEM RUN: Hand the engineer the fixture. Let them compose their own utterance, predict the class, and run it. Especially: let them try to make a private fact go shared by accident, and watch fail-private catch it. Let them exit a dyad and re-run row 9, proving exit changes future writes.

THE CLAIM IT PROVES: "Where a fact lands is a deterministic rule you can read and test, not a model's guess. When we are unsure, we wall it, and I can show you the exact rule that does it."

THE HARDEST QUESTION + HONEST ANSWER: "Your care-team default means a forgotten directive leaks a confidence to the whole care team, irreversibly. You chose that on purpose?" Answer: yes, and here is the trade stated plainly — the alternative default (pair-private) silently hides falls and medication events from the other caregiver, a safety failure that surfaces in the physical world with no warning, while the chosen default's failure is a social harm with a warning built in (the write path shows the audience at write time). The recipient's standing policy at level 1 and the mandatory subject-is-a-caregiver rule at level 3 cap the worst cases. And note what sensitivity can no longer do: it never picks an audience — a wrong 7B-model sensitivity call can harden handling but can never widen who reads a fact. The model can only ever over-share within the audience the deterministic rules already chose. It can never breach the wall. State the limit before they find it.
