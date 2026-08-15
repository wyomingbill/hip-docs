# Moshi Research Lane — Development Method
Status: ADOPTED (Bill, 2026-08-13)
Reconciled-Against: f1c687f (roadmap HEAD at write time; tree clean apart from four untracked demo-cutover dispatch docs belonging to another lane, left as found). Banked at 4a7b82f, HA-66, 2026-08-13. Docs-only: banked VERBATIM from Bill's paste, reconciled against no code, no graph and no harness run.
Purpose: run the dual-model research WITHOUT the full HIP dispatch process. Bill's constraint: no second turn-heavy process while the current demo is being finished.

## 1. Two modes, split by what the work asserts
RESEARCH MODE — work that claims nothing and touches no HIP data: all of M0; M1's and M4's experiments.
GOVERNED MODE — work HIP must stand behind: M2's gate design and rulings, M3, M5, and ANY code that lands in a HIP tree. Full standard process: REQ before code, executed evidence, Bill rules MET, locks, MANIFEST/INDEX law.

## 2. Research mode rules
- OWN CHECKOUT: ~/moshi-lab. Never a worktree of any HIP repo; no HIP repo is ever a dependency.
- ENVIRONMENT ISOLATION, FAIL-CLOSED: the lab shell exports no NEO4J_* variables, holds no HIP credentials, and never reads ~/hip-keys, any hip-* checkout, data/voiceprints, or any HIP graph port (7687-7690). FIRST ACT of every lab session: assert those absences; refuse to proceed if any are present.
- NO PROCESS MACHINERY: no locks, no lanes, no dispatch numbers, no REQ docs, no MET rulings, no MANIFEST law inside the lab.
- AUTONOMOUS SESSIONS: each stage runs as one fire-and-finish session with written stop conditions — not segmented check-ins. A session stops only on: a stop condition, a hardware limit, or a result that changes the plan.
- ONE FINDINGS DOC PER STAGE: FINDINGS__m0__vYYYYMMDD.md (etc.), kept in the lab. First line is the verdict, one of the stage's named outcomes. Evidence after.
- BILL'S TOUCHES PER STAGE: fire it; read the verdict. M1 adds exactly one up-front ruling: the approved act -> utterance table.

## 3. The border (absolute)
- Nothing from the lab is ever merged, copied, or symlinked into a HIP tree.
- Graduation = re-implementation through the governed process in the proper HIP tree, with its own REQ and evidence. Lab code is reference material only.
- The ONLY artifacts that cross are findings docs, banked into hip-roadmap docs/reviews/ by a normal short docs dispatch. That dispatch follows the full standard process.
- No lab process ever holds a HIP graph credential or writes a HIP-owned path. This prevents the two failure modes already paid for: the frozen orch holding write authority (D-84) and cross-checkout DATA_DIR coupling.

## 4. Reporting
Research-mode sessions still end with a terminal recap Bill screenshots: exception-reporting first line (COMPLETE / STOPPED AT / COMPLETE WITH FINDINGS); STAGE; VERDICT (a named outcome); findings doc path; NEEDS BILL (usually nothing, or one decision).

## 5. Bill's total management load
One go/no-go per stage. One act-table ruling before M1. Governed mode returns at M3 — by which point the demo is done per the spec's §8.

## 6. Stop-the-lane conditions
Any PARK or FAIL outcome at M0. Any evidence the act gate cannot be enforced without destroying the duplex value. Any research-mode step found to need HIP data to proceed — that need itself means the step belongs in governed mode: stop and reclassify.
END OF DOCUMENT
