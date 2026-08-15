# REQ_LOCK_ENFORCEMENT
Status: PLAN
Reconciled-Against: D-146, 2026-08-03 (survey only — no code, no shape chosen)

## THE REQUIREMENT

Bill's own words, verbatim:

> The .hip-lock is advisory and has failed three ways — written through (D-107),
> clobbered unread (D-118), and taken late twice (D-114, D-145). A lock that reports
> compliance it cannot enforce is worse than no lock. HIP's dev lanes SHALL NOT share
> one graph, and lock acquisition SHALL precede any write including the first read of
> a governed file.

**Expanded:** two distinct requirements, named separately because they fail differently and
may be fixed differently (see D-146's dispatch doc for the full survey and proposal this REQ
was filed alongside):

1. **Lock enforcement.** `.hip-lock` today is a convention — a session reads it, and is
   trusted to honor what it finds. That trust has failed three specific, named ways (below).
   The fix must make non-compliance IMPOSSIBLE or COSTLY-AND-LOUD, not merely re-document the
   convention more carefully. "Lock acquisition SHALL precede any write including the first
   read of a governed file" additionally scopes WHEN the lock must be held — not just before a
   commit, but before the FIRST READ of anything the lock is meant to protect, which is a
   stricter timing requirement than TD-148's original framing implied.
2. **Graph separation.** HIP's dev lanes currently do not each have their own Neo4j instance.
   Some collide by explicit, committed configuration; others collide by ambiguous, operator-
   dependent default; one lane deliberately shares the frozen demo's graph by design. "SHALL
   NOT share one graph" is stated with no carve-out for intentional or occasional sharing.

## THE ACCEPTANCE TEST

Cannot be written to a single implementation-specific pass/fail yet — item 2 of D-146
(propose the enforcement shape; do not pick) is upstream of this section, and the two
requirements above admit multiple genuinely different mechanisms with different costs (see the
dispatch doc's OPTIONS). Stated at the level of the requirement itself, testable once a shape
is chosen:

1. **Lock enforcement:** a fault twin exists where a second process attempts to write a
   governed resource while a first process holds `.hip-lock`, and the second process is
   BLOCKED OR REFUSED BY THE MECHANISM — not merely warned, not merely able to observe the
   lock and choose to proceed anyway. Reproduces D-107's write-through as a red case before the
   fix and a refused case after.
2. **Lock timing:** a fault twin exists where a process attempts to READ a governed file before
   acquiring the lock, and this is either structurally impossible (the read path requires the
   lock) or is detected and flagged.
3. **Graph separation:** for every currently-live lane (enumerated in D-146's survey), sourcing
   that lane's own environment resolves `NEO4J_URI` to a port no other currently-live lane's
   environment also resolves to. Reproduces the crypto-p2/stage1-wip/hip-roadmap 7688 collision
   and the hip-vo/hip-dev 7689 collision as red cases before the fix.

## WHAT'S ALREADY DONE

- **The read-first/noclobber CONVENTION** (CLAUDE.md's STANDARD PREAMBLE, D-137) — every
  dispatch this session has run has followed it. This is explicitly NOT the same claim as
  enforcement: it is discipline that a compliant session follows and a non-compliant or
  careless one does not, which is exactly Bill's stated reason this REQ exists.
- **Per-lane dedicated Neo4j instances, proven for two lanes already:** the frozen demo
  (`~/hip-dev`, port 7689, instance `~/neo4j-hipdev-demo`) and the demo-cutover lane
  (`~/hip-cutover-demo`, port 7690, instance `~/neo4j-cutover-demo`, stood up at D-106). The
  demo-cutover lane additionally has a working STARTUP GUARD precedent (D-108's "C2 guard" —
  `NEO4J_URI` checked at module import, `sys.exit(1)` before the app object exists if wrong)
  that refuses to run misconfigured rather than silently miswriting.
- **The demo-cutover lane's launcher-level isolation technique** (D-109): runs under `env -i`
  with a private, `.env.dev`-free `$HOME` so the home-level override hazard (below) cannot
  reach it at all, regardless of what any session sources.

## WHAT'S KNOWN BROKEN

**Lock, the three named failure modes, each with its own root cause (TD-148, HIP_HANDOFF.md
§2):**
- **Written through (D-107):** the demo-cutover lane wrote a REQ, a dispatch doc, and two
  INDEX rows into `~/hip-roadmap` WHILE the roadmap lane held the lock. The lock was read,
  understood, and overridden anyway — a compliance failure the lock's current shape cannot
  prevent, only report after the fact.
- **Clobbered unread (D-118):** a session took the lock with a bare `>` after only an
  existence check, destroying the prior holder's fields, never identified.
- **Taken late twice (D-114, D-145):** the `taken:` timestamp drifts from real mtime, which is
  the likely reason two sessions have each believed they held the lock.

**Graph separation — the full config-verified survey (D-146):**
- `~/hip-roadmap` (7688), `~/hip-roadmap-crypto-p2` (7688), `~/hip-roadmap-stage1-wip` (7688)
  all carry their OWN committed `.env.dev` pinning the identical port — an explicit,
  reproducible collision, not an accident of omission, for three separate working trees.
- `~/hip-roadmap-crypto-p1` and `~/hip-ungoverned` carry no env file of their own at all;
  their actual target graph depends entirely on what a session manually sources before running
  anything in them — ambiguous and unaudited, not deterministically wrong but not verifiably
  right either.
- `~/hip-vo`'s `.env.demo` explicitly runs `source ~/hip-dev/.env.dev`, deliberately targeting
  the FROZEN DEMO's own graph (port 7689) whenever demo mode is used — a real, live,
  by-design collision with the one lane CLAUDE.md already names as "the fallback, not a lane."
- Port 7687 has a live, running, unlabeled Neo4j instance (default Homebrew service, no
  dedicated `~/neo4j-*` home directory) that is ALSO the hardcoded silent fallback in
  `harness/extraction_queue.py`, `harness/zep_store.py`, and hip-vo's `server/demo_dashboard.py`
  when `NEO4J_URI` is unset — meaning any checkout run without careful env discipline writes
  into a graph with no clearly accountable owner at all.
- `~/.env.dev` (home-level, distinct from every repo's own `.env.dev`) pins port 7689 with
  `override=True` — already a named, documented hazard (CLAUDE.md's STANDARD PREAMBLE item 3)
  that can silently redirect ANY lane into the frozen demo's graph regardless of which
  checkout the session believes it is working in.

Full per-lane table and process/port cross-reference: D-146's dispatch doc.

## CONSTRAINTS

- **Must not break the two graph-separation cases that already work.** The frozen demo's 7689
  isolation and the demo-cutover lane's 7690 isolation (including its `env -i` launcher
  technique) are the model the fix should extend to, not risk regressing while fixing the
  other lanes.
- **Must not break the currently-working three-lane discipline** (build + governance both in
  `~/hip-roadmap`/7688, demo-cutover in `~/hip-cutover-demo`/7690, frozen demo as fallback) —
  whatever shape is chosen must fit around, not replace, workflows already functioning.
- **Memory is a real, previously-documented constraint on this machine, not a hypothetical
  one.** TD-129 recorded 0.07 GB free at one assessment point specifically when a SECOND Neo4j
  instance was considered and rejected as infeasible for that reason. Any shape that adds
  MORE running Neo4j instances (one per additional lane) must account for this, not assume
  headroom that was already once measured absent.
- **Neo4j Community's own limits are a real constraint, not a detail to discover mid-build.**
  Prior research in this project (banked D-63 review) already found Community edition is
  single-database — any shape relying on per-lane logical separation WITHIN one instance
  (rather than one instance per lane) needs this checked before it is proposed as free.
- **Do not touch the frozen demo** (`~/hip-dev`, Neo4j 7689). It is the fallback; it is not a
  lane, and no shape here should make it one.
