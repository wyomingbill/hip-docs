# Curator research reconciliation: memo A vs memo B

Status: DRAFT. Ratifies nothing. Five decisions below are Bill's.
Sources: HIP_CuratorResearch__learned-retrieval-training-federation__v20260728_1045.md (A)
and HIP_CuratorResearch_B__hybrid-ranker-and-federation__v20260728_1733.md (B, ChatGPT-sourced).

## Settled: where both memos agree

These points are consensus across two independent research passes and are
treated as the working baseline, not open questions.

1. The Curator is a small tree-based ranker (GBDT/LambdaMART), not a neural
   retriever. Trained-retriever literature operates at millions of passages;
   nothing is published at household scale.
2. It runs after the injection contract and can only narrow the admitted
   set, never add to it. Authorization is not learnable.
3. Rules remain the permanent fallback: shadow deployment first, kill switch
   always, rollback is one flag.
4. Federated learning cannot deliver literal zero cross-household influence.
   Secure aggregation plus differential privacy gives a bounded guarantee,
   not isolation. B sets ~1,000 completed households as the target; A's
   cited evidence (6,500-12,000/round) doesn't disagree but never commits
   to a number that low.
5. Everything required for the initial Curator trains and serves on in-home
   CPE hardware.
6. Corrections and overrides are deliberate judgments and clean training
   labels.

## Disagreement 1: semantic feature

B: metadata-only ranking cannot distinguish "takes metformin," "stopped
metformin," and "allergic to metformin," so a frozen MiniLM similarity
score should be one ranking feature from the start.
A (§7.2): at household scale the admitted set is small and mostly
disambiguated by attribute-family, recency, trust, and supersession;
measure before adding text-awareness.

Resolution: B's examples are already distinguished structurally in HIP.
Supersession separates takes from stopped; the attribute enum separates
medication from allergy; subject separates Dad from Susan. B's concern is
real only where normalization is imperfect. Stage 0's
candidates-per-attribute-family measurement decides this with data: the
semantic feature is added only if families are measurably crowded (more
than 3 live candidates within one family for one subject at meaningful
frequency). Adopted from B regardless of that outcome: an embedding is
derived private data and inherits its fact's key class, audience,
revocation, and deletion lifecycle. No plaintext embeddings in any shared
store.

## Disagreement 2: cold start and per-household architecture

A: per-household-only training, no pooling; accept the slow cold start.
B: a shared base ranker trained only on public, synthetic, and centrally
authored data, plus a local household head that never leaves the home
(FedRep pattern).

Resolution: B's architecture is strictly better and is the recommended
design. The isolation claim survives intact: no household data ever enters
the shared component, so isolation stays provable by training-example
provenance, exactly what REQ_LEARNER_SIGNAL_ISOLATION's acceptance test
checks. The cold-start penalty A accepted is removed: a new household
starts from the synthetic-trained base instead of from nothing. The local
head is sealed under household keys and is destroyed or re-keyed on
revocation.

## Disagreement 3: is an accepted answer a clean label?

A (Part 2): groups accepted answers with corrections and overrides as
deliberate judgments landing as clean pairwise labels.
B (§2.2): acceptance may reflect generator quality, patience, low
stakes, or an unnoticed omission; "HIP therefore cannot treat 'answer
accepted' as a clean relevance label."

Resolution: B's position is adopted. Passive acceptance is at most a
weak positive, never weighted equal to a correction; explicit
confirmation ("yes, that fact was right to use") remains a clean label.
Stage 0's logged fields are unchanged; Stage 2's training objective
weights corrections and overrides above acceptances.

## Consequence for federation, if ever

Both memos gate federation behind fleet scale and a separate ruling. B
sets ~1,000 completed households as the target; A's cited evidence
(6,500-12,000/round) doesn't disagree but never commits to a number that
low. B adds one engineering fact A did not: FedAvg does not train
decision trees, so a federated Curator means swapping the tree for a
small neural or linear scorer over the same features.

## The five decisions, consolidated (Bill's)

1. Isolation definition. Strict (zero cross-household influence, shared
   base trained on non-household data only) versus bounded (household
   updates enter a shared model under clipping, secure aggregation, and a
   stated privacy budget). Recommendation: strict, via the B architecture.
   The sellable claim survives and the cold-start cost is gone.
2. Intra-household scope crossing. Whether member-private signal training
   a household-shared model is the same violation class as cross-household
   pooling. Recommendation: same class; keep the REQ's current wording.
3. Entry trigger. The measured retrieval-failure rate and window that opens
   Gate A. Recommendation: set the number after Stage 0's first baseline
   report; do not pick it blind.
4. Loss priority. Which failure the ranker is punished hardest for.
   Recommendation: omission of a decisive authorized fact, the D-24/T02
   class; it is the one failure with deterministic ground truth.
5. Decrypted-value processing boundary. In-home CPE only, operator
   confidential-computing enclave, or operator service. Recommendation:
   in-home CPE only until confidential computing is integrated into the
   inference path; this also keeps the cross-encoder shelved.

## After the rulings

The rulings amend REQ_LEARNER_SIGNAL_ISOLATION (decisions 1 and 2), set
the Gate A instrument thresholds (3), define the Stage 2 training
objective (4), and constrain the Stage 1 training-record design (5). One
dispatch carries all five into the REQ and the scope doc once ruled.
