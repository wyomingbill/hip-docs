# HIP Testing Best Practices: Research Comparison
Status: BUILT (research memo, analysis only; changes no code, ratifies nothing)
Reconciled-Against: 048a21f (harness state: REQ_HARNESS_DISCIPLINE audit at 003fd9c/7730044, 52 checks, TD-133's 54 flagged gaps; G0 MET at edb0791; master key destroyed at b3e2368, PS1-PS4 fixture retirement in flight in the crypto session)

## What this is

Bill's standing instruction: compare HIP's harness approach — standing invariants with fault
injection, metamorphic testing, canary/taint tracking, hard-zero gates, the four-part
discipline standard — against published best practice for testing LLM systems and
privacy-critical/crypto code. For each: where HIP is ahead of common practice, where it is
behind, and what specific technique is worth adopting into the TD-133 burn-down. Concrete
and honest, not a puff piece. Sources cited at the end; claims about HIP are grounded in
the code and registers at the commit above, not in aspiration.

The one-line summary: HIP's harness is ahead of common LLM-application practice on
discipline (deterministic invariants, fault-proven checks, non-negotiable gates, honest
gap registers) and behind on generation and scale (no property-based generation, no
automated adversarial campaigns, hand-authored variant sets, declared-not-measured
coverage). Most of TD-133's 54 flagged gaps are exactly the places where a published
generative technique would close dozens of hand-built gaps at once.

---

## 1. Standing invariants with fault injection

**What HIP does.** Every layer-7 crypto check runs automatically on every `--layer 7`/
`--full` (PS1/PS2/OB4/OB5/G0 and the rest); the load-bearing ones carry a deliberately
constructed violation that turns them red on command (misseal to the wrong D_pub → N2/P2
red; a mislabeled master-sealed fact → PS1/PS2 red; a missing key file → OB5's refusal
path exercised; a monkeypatched fabricating model → G0 blocks it). The 2026-07-21 OB4
incident is the pattern's live proof: fault injection found consolidate.py writing v1
facts in production code before the fix, not after.

**Published practice.** This is the core insight of chaos engineering (Basiri et al.,
"Chaos Engineering," IEEE Software 2016; Netflix's Chaos Monkey): a control you have never
watched fail is unproven. Jepsen's distributed-systems work (Kingsbury, jepsen.io) is the
canonical demonstration that invariant checking plus actively injected faults finds bugs
that clean-path testing never will. In safety engineering the same idea is older still —
you test the alarm by setting a fire in a can. Mutation testing (DeMillo, Lipton & Sayward,
"Hints on Test Data Selection," IEEE Computer 1978; industrialized at Google per Petrović
& Ivanković, "State of Mutation Testing at Google," ICSE-SEIP 2018) generalizes it: seed
artificial defects, measure whether the suite notices.

**Verdict: ahead of common practice, behind the systematic version.** Most production LLM
applications have nothing like red-on-command proof for their guardrails; HIP requiring it
per check (and now auditing for it) is genuinely unusual. But HIP's fault injections are
hand-picked, one or two per check. Mutation testing is the systematic version — mutate the
GUARD code itself and measure the kill rate. HIP's Layer 3 is a narrow, targeted form of
this (guard mutations on an in-process server); no mutation SCORE exists, so nobody knows
what fraction of guard mutants the suite would actually catch.

**Adopt into TD-133:** run an off-the-shelf mutation tool (mutmut or cosmic-ray) over
`harness/injection_contract.py`, `harness/write_rule.py`, and `harness/g0_invariant.py`,
record the mutation score, and turn surviving mutants into the missing fault-twins. This
closes twin gaps by measurement instead of one hand-built violation at a time, and it
covers the twin-less checks TD-133 lists (P4, PS3, FF1-FF4, SC1) with a single mechanism.

## 2. Metamorphic testing

**What HIP does.** MT1 (12 hand-written wording variants of one query; the admit/refuse
decision must not change), MT2 (single-auth-condition mutations must FLIP the decision —
a directional test, in the literature's terms), and since 003fd9c the audit's executable
rewording probes for G0, G1-G4, the PS1/OB4 scan pattern, and the PS2 wrap verdict.

**Published practice.** Metamorphic testing is a mature field: Chen, Cheung & Yiu coined
it (HKUST technical report, 1998); Segura et al.'s survey (IEEE TSE 42(9), 2016) is the
standard reference. For NLP specifically, CheckList (Ribeiro et al., ACL 2020,
aclanthology.org/2020.acl-main.442) is the landmark: Invariance tests (INV — label-
preserving perturbations must not change the prediction) and Directional Expectation
tests (DIR — controlled changes must move it a known way), generated at scale from
templates and lexicons rather than written one at a time. MT1 is an INV test; MT2 is a
DIR test — HIP independently converged on both categories. Recent LLM work extends this
to hallucination detection via metamorphic prompt mutation (MetaQA, 2025) and multi-turn
dialogue robustness (arXiv:2401.12483).

**Verdict: ahead on placement, behind on generation.** Placing metamorphic checks on the
AUTHORIZATION decision (who may read what) rather than on task quality is the right,
uncommon choice — CheckList tests capabilities; HIP tests a security boundary. But 12
hand-written variants is a fixed corpus, and TD-133 says it plainly: metamorphic runs on
the demo script only, not all checks. TD-119's history (a guard that answered "What
medication is Elena on now?" but refused "What medication does Elena take?") shows exactly
what a phrasing-generated suite catches and a hand-picked one misses.

**Adopt into TD-133:** CheckList-style template generation — a small template+lexicon
expander ({ask-verb} {subject}'s {attribute}, per member, per attribute family) generating
hundreds of INV variants per decision surface, run against the injection contract the way
MT1 already runs. Deterministic, offline, no model in the oracle. This closes most of the
"no rewording wrapper" flags for the decision-testing checks in one build. Property-based
testing (Claessen & Hughes, "QuickCheck," ICFP 2000; Hypothesis for Python) is the same
move for structured inputs: generate records for G1-G4 and classification rows for P4 with
random content and asserted-invariant properties, with shrinking on failure. The audit's
`_g_record` fixtures are hand-built instances of what Hypothesis would generate thousands
of.

## 3. Canary / taint tracking

**What HIP does.** CT plants a literal canary on every forbidden surface (prompt,
retrieval, vector index, logs) and scans for it; CT-VECTOR-INDEX covers the embedding
index; CT-OUTPUT-GAP (opt-in) scans a real model reply. The register is honest about the
limit: TD-132 records that literal-substring matching catches a verbatim leak, not a
paraphrase — observed live when the local model restated an authorized fact's substance
while dropping the bracketed marker.

**Published practice.** Honeytokens go back to Spitzner ("Honeytokens: The Other
Honeypot," SecurityFocus 2003); Thinkst's Canarytokens is the industrialized version.
Dynamic taint tracking through a system is TaintDroid (Enck et al., OSDI 2010). For the
failure mode TD-132 names, the relevant literature is memorization/extraction: Carlini et
al., "Extracting Training Data from Large Language Models" (USENIX Security 2021) — and
the modern practice of semantic leakage detection: embedding-similarity or NLI-entailment
between the secret and each downstream surface, not substring match. LLM privacy
evaluations (e.g. DecodingTrust, NeurIPS 2023) test exactly this restated-secret channel.

**Verdict: parity on mechanism, behind on semantics — and HIP already knows it.** Planting
canaries on every surface including the vector index is more thorough than most
deployments (log/prompt scanning is common; index taint is not). The paraphrase hole is
real, registered (TD-132), and named in this memo's own audit as the missing semantic-
metamorphic wrapper for the CT family.

**Adopt into TD-133/TD-132:** a semantic canary: for each forbidden fact, compute
embedding similarity (the stack already embeds facts) between the fact VALUE and each
scanned surface, flag above-threshold hits; where a hit needs adjudication, an NLI
entailment check ("surface text entails the secret") — with the teacher-model-not-sole-
oracle rule satisfied by human-verified fixture pairs calibrating the threshold. This is
one probe, closes the CT-family metamorphic flags, and upgrades the leak guarantee from
"the marker didn't appear" to "the substance didn't appear," which is what the trust claim
actually needs.

## 4. Hard-zero gates and the ratchet

**What HIP does.** Three tiers (ABSOLUTE/SERIOUS/QUALITY); ABSOLUTE tolerates zero
failures and zero flakes and mechanically refuses `--accept` regardless of justification
(G0/G1/G4, the RE suite, FF1/FF4, CT). Every other acceptance requires a defect ID or an
explicit expiry — a bare excuse string is rejected by regex. FLAKE is a first-class
quarantined state that never turns a run green silently. D-17's history (a brand-new
failure masking a real regression) is the reason both are always printed.

**Published practice.** Regression ratchets and quarantine lanes are standard CI
(Google's flaky-test literature: Luo et al., "An Empirical Analysis of Flaky Tests," FSE
2014; Micco/Memon's Google testing talks). What is NOT standard is a tier that cannot be
baselined by anyone for any reason: in most CI systems every failure is quarantinable
with enough seniority, which is exactly how privacy regressions ship. The closest
published analogues are "merge gates" on mutation score and the safety-case framing from
safety-critical software (DO-178C's non-negotiable objectives), plus NIST AI RMF's
"non-acceptable risk" categories — but a mechanical, code-enforced never-acceptable tier
in a test harness is ahead of common practice.

**Verdict: ahead.** The `--accept`-refusal mechanism plus expiry-or-debt-ID discipline on
everything else is better than the industry norm. One behind-item: the trend files
(`harness_trend.jsonl`, `invariants_trend.jsonl`) exist but nothing renders or alerts on
them — published practice treats eval trend dashboards as the operational half of gating
(every major eval framework — HELM's public leaderboards, promptfoo/DeepEval CI reports —
ships one). A gate you only see when it fires is half a gate.

**Adopt:** small; render the two trend JSONLs (fail/flake counts per layer over time, the
G-counts, the TD-133 flag count as a burn-down line) into the existing demo dashboard.
The TD-133 count specifically should be a visible monotone-down metric.

## 5. The four-part discipline standard (the audit itself)

**What HIP does.** REQ_HARNESS_DISCIPLINE: no check counts without (a) a fault-injection
twin, (b) a human-verified ground-truth fixture (a teacher model may assist ranking, never
be the sole oracle), (c) a coverage entry naming the authorization-state-space slice, (d)
a metamorphic wrapper where the check tests a decision. Enforced mechanically: a standing
audit enumerates every check by AST, verifies declarations against source/roster/
executable probes, rejects a twin-less check (proven red-on-command every run by synthetic
injection), and prints all 54 registered gaps on every run (TD-133).

**Published practice.** There is no direct published equivalent of a mechanical
four-artifact merge gate for checks-about-checks. The nearest relatives: Google's Test
Certified ladder (test-quality maturity as a gate, described in "Software Engineering at
Google," Winters et al., O'Reilly 2020), mutation-score merge thresholds, and CheckList as
a methodology (a taxonomy of what a test suite must cover, but human-enforced). The
human-verified-oracle rule anticipates the now-documented weaknesses of LLM-as-judge:
position/verbosity/self-preference biases (Zheng et al., "Judging LLM-as-a-Judge with
MT-Bench and Chatbot Arena," NeurIPS 2023) — current best practice is judge + human
agreement calibration, never judge alone, which is exactly standard (b).

**Verdict: ahead — with two honest caveats.** First, the audit verifies that artifacts
EXIST and run green; it cannot verify they are GOOD (a weak twin passes the same as a
strong one). The mutation-score adoption in §1 is the published answer to that: measure
artifact strength, don't declare it. Second, HIP's coverage entries are declarations, not
measurements. Published practice for state-space coverage is combinatorial testing with
measured coverage (Kuhn et al., NIST SP 800-142 / the ACTS covering-array tooling); HIP's
Layer 4 pairwise matrix already does the generation half for retrieval, but nothing
measures which (role x scope x attribute-family x intent) cells the whole suite actually
exercises versus the registry's claims.

**Adopt into TD-133:** a coverage MEASUREMENT pass: derive the exercised cells from the
scenarios' own fixtures (they are enumerable — owners, subjects, attributes, classes are
literals in the registry and code), diff against the declared coverage entries, and print
uncovered cells in the audit report. That converts standard (c) from honor-system to
measured, the same upgrade the ratchet made to "we test before shipping."

## 6. The crypto layer specifically

**What HIP does.** Uses vetted primitives (X25519, Fernet from pyca/cryptography), tests
the COMPOSITION (wrap chains, class sealing, quorum shares, revocation re-key) with live
invariants (N*/P*/DK*/RE*), Shamir 2-of-3 with an information-theoretic single-share
claim, and — as of b3e2368 — the strongest possible negative test: the master key
actually destroyed, N5/R7 proven against live facts with no key in existence. The
PS1-PS4 fixture-builder retirement in flight is the honest cost of that: a fixture that
can no longer be constructed because the system made the state unrepresentable.

**Published practice.** For primitive USAGE, the standard is adversarial known-answer
vectors: Google's Project Wycheproof (github.com/C2SP/wycheproof — curated edge-case
vectors that have found 40+ real library bugs), NIST CAVP/ACVP validation vectors, and
pyca/cryptography's own vector policy (official-source vectors only, cryptography.io's
test-vectors documentation). For side channels, constant-time verification (dudect,
ctgrind). For the highest tier, formally verified implementations (HACL*/Project Everest,
Fiat-Crypto). Fault injection against crypto in the literature usually means glitching
hardware — HIP's logical-layer fault injection is the right analogue for a software
system.

**Verdict: composition testing ahead, primitive-boundary testing absent, side channels
out of scope but should stay NAMED.** Nobody at HIP is re-implementing primitives (good),
but nothing runs adversarial vectors against the USAGE boundary either — e.g. malformed
or low-order X25519 public keys fed to the wrap path, tampered Fernet tokens fed to
unwrap, truncated/bit-flipped ciphertexts asserted to fail CLOSED with the right error
and no partial plaintext. Wycheproof's X25519 vector file covers exactly the first class.
The destroyed-key negative test, on the other hand, is beyond what most published
practice achieves — most systems' "we can't decrypt it" claim is never tested against a
world where the key is truly gone; HIP's is.

**Adopt into TD-133:** a WV1 check: run Wycheproof's X25519 vectors (and a small
tampered-token suite for Fernet) through `dyad_crypto`'s wrap/unwrap boundary, asserting
fail-closed on every invalid vector. Offline, deterministic, a few hundred vectors, and
it gives DK1/DK2 the missing red-on-command twins from published vectors instead of
hand-built ones. Side-channel testing: do NOT adopt now; add one line to the honest-limits
list ("timing side channels untested") so the gap is registered rather than silent —
consistent with how limits 1-8 in the plan of record already work.

## 7. The LLM layer specifically

**What HIP does.** Deterministic oracles wherever possible (routing, injection contract,
answer-mode selection are code, not model judgment); live-model checks quarantined behind
flake handling or opt-in gates (CT-OUTPUT-GAP); G0 as a runtime output gate independent of
every upstream stage; L5's A1-A5 adversarial fixture set; record-level invariants (G1-G4)
over every logged turn, so every production turn retroactively becomes a test.

**Published practice.** Industry LLM testing (HELM, Liang et al. 2022; OWASP Top 10 for
LLM Applications; NIST AI RMF; MITRE ATLAS) combines offline evals on golden datasets,
runtime guardrails, tracing/observability, and adversarial red-teaming — with 2026
practice emphasizing automated, agent-orchestrated red-team campaigns against the FULL
application (system prompt, retrieval, tools), not the bare model, using tools like
Microsoft PyRIT, garak, and promptfoo. Manual red-teaming methodology: Perez et al., "Red
Teaming Language Models with Language Models" (EMNLP 2022); Ganguli et al. (Anthropic,
2022).

**Verdict: ahead on runtime gating and record invariants, behind on adversarial scale.**
G1-G4 over every logged turn is the "every production trace is an eval" pattern that
observability vendors sell, built in-house and gated. G0 as a deterministic, code-level
output gate is stronger than the prompt-based "guardrail" most deployments use (a prompt
instruction is not a gate — HIP's G0 REQ says this explicitly and the risk memo forbids
refusal-by-prompt-instruction). But L5's adversarial set is a fixed, hand-authored fixture
list; published practice generates attacks continuously. The threat model most relevant
to HIP — a household member socially engineering the assistant into revealing another
member's facts, via paraphrase, role-play, or multi-turn setup — is exactly what
automated red-teaming tools generate at scale and what a static A1-A5 set cannot keep up
with.

**Adopt into TD-133:** an opt-in RT layer (same gating pattern as CT-OUTPUT-GAP: off the
deterministic path, explicit env flag) running a garak/PyRIT-style campaign against the
text-query path with the ABM fixture loaded, asserting zero cross-member disclosures;
survivors become new L5 fixtures (the same finder→fixture ratchet the defect registers
already implement for bugs). Second, cheaper item: multi-turn versions of the A1-A5
fixtures — every current adversarial scenario is single-turn, and multi-turn context
manipulation is the documented weak spot of single-turn testing (arXiv:2401.12483).

---

## Summary table

| Technique | vs published practice | TD-133 adoption |
|---|---|---|
| Fault-injection twins | Ahead (per-check red-on-command is rare); behind mutation testing's systematic version | Mutation score over guard code; survivors become twins |
| Metamorphic (MT1/MT2 + audit probes) | Ahead on placement (auth boundary); behind on generation (hand-written variants) | CheckList-style template expansion; Hypothesis for records/classifier rows |
| Canary/taint | Parity on mechanism, index-taint unusual; behind on semantics (TD-132) | Semantic canary: embedding-similarity + calibrated NLI, human-verified fixture pairs |
| Hard-zero gates + ratchet | Ahead (mechanically un-acceptable tier); trend data unrendered | Trend dashboard incl. TD-133 burn-down line |
| Four-part standard + audit | Ahead (no published mechanical equivalent); verifies existence, not strength; coverage declared not measured | Coverage measurement pass (covering-array style diff of exercised vs declared cells) |
| Crypto composition | Ahead (destroyed-key negative test); primitive-boundary vectors absent; side channels unnamed | Wycheproof X25519 vectors + tampered-Fernet suite at the wrap boundary; name timing as a limit |
| LLM adversarial | Ahead on runtime gates (G0) + record invariants; behind on attack generation | Opt-in auto red-team layer; multi-turn A1-A5 variants |

Priority order for the TD-133 burn-down, by gap-closure per unit work: (1) CheckList
template expansion + Hypothesis generation — closes the largest number of flagged
twin/metamorphic gaps with two mechanisms; (2) semantic canary — closes TD-132 and the CT
family; (3) Wycheproof boundary vectors — closes DK-family twins from published vectors;
(4) mutation score — converts twin quality from declared to measured; (5) coverage
measurement; (6) trend rendering; (7) opt-in auto red-team.

## Sources

- Chen, Cheung & Yiu, "Metamorphic Testing: A New Approach for Generating Next Test
  Cases," HKUST-CS98-01, 1998.
- Segura, Fraser, Sanchez & Ruiz-Cortés, "A Survey on Metamorphic Testing," IEEE TSE
  42(9), 2016.
- Ribeiro, Wu, Guestrin & Singh, "Beyond Accuracy: Behavioral Testing of NLP Models with
  CheckList," ACL 2020 — https://aclanthology.org/2020.acl-main.442/
- MetaQA: metamorphic prompt mutation for hallucination detection, ACM 2025; multi-turn
  metamorphic relations — https://arxiv.org/pdf/2401.12483
- DeMillo, Lipton & Sayward, "Hints on Test Data Selection: Help for the Practicing
  Programmer," IEEE Computer, 1978.
- Petrović & Ivanković, "State of Mutation Testing at Google," ICSE-SEIP 2018.
- Claessen & Hughes, "QuickCheck: A Lightweight Tool for Random Testing of Haskell
  Programs," ICFP 2000; Hypothesis (hypothesis.readthedocs.io).
- Basiri et al., "Chaos Engineering," IEEE Software 33(3), 2016; Jepsen — https://jepsen.io
- Luo, Hariri, Eloussi & Marinov, "An Empirical Analysis of Flaky Tests," FSE 2014.
- Winters, Manshreck & Wright, "Software Engineering at Google," O'Reilly 2020.
- Kuhn, Kacker & Lei, "Practical Combinatorial Testing," NIST SP 800-142, 2010.
- Google Project Wycheproof — https://github.com/C2SP/wycheproof
- NIST ACVP; "Point Intervention: Improving ACVP Test Vector Generation Through Human
  Assisted Fuzzing," ICICS 2024 — https://link.springer.com/chapter/10.1007/978-981-97-8801-9_3
- pyca/cryptography test-vector policy — https://cryptography.io/en/latest/development/test-vectors/
- Spitzner, "Honeytokens: The Other Honeypot," SecurityFocus, 2003; Thinkst Canarytokens.
- Enck et al., "TaintDroid," OSDI 2010.
- Carlini et al., "Extracting Training Data from Large Language Models," USENIX Security
  2021.
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2023.
- Perez et al., "Red Teaming Language Models with Language Models," EMNLP 2022; Ganguli
  et al. (Anthropic), "Red Teaming Language Models to Reduce Harms," 2022.
- Liang et al., "Holistic Evaluation of Language Models (HELM)," 2022.
- OWASP Top 10 for LLM Applications; NIST AI RMF; MITRE ATLAS.
- 2026 LLM red-teaming practice surveys — https://kili-technology.com/blog/llm-red-teaming-in-2026 ;
  https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies ;
  https://www.vervali.com/blog/ai-and-llm-application-testing-in-2026-the-definitive-guide/
- Microsoft PyRIT — https://github.com/Azure/PyRIT ; garak — https://github.com/NVIDIA/garak
