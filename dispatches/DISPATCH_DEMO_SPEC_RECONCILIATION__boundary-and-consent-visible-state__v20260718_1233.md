# DISPATCH_DEMO_SPEC_RECONCILIATION
Status: BUILT
Reconciled-Against: main 601ac25, 2026-07-18 (code read only, nothing changed)

**TYPE:** ANALYSIS

**REQ:** NONE. Explicitly a verification pass, not a build — "no new features,
verify what exists... change nothing."

## THE ASK

Bill's words, verbatim:

> "DEMO SPEC RECONCILIATION — no new features, verify what exists.
>
> The boundary_and_consent demo has accreted changes across many sessions.
> Bill can no longer tell by looking whether it meets its requirements.
> Before any more changes, produce a reconciliation.
>
> For REQ_VOICE_DEMO and the four governance-visibility objectives
> (DEMO_SCRIPT01_GOVERNANCE_VISIBILITY, 5eee5dc), make a table: each
> requirement, whether it is VISIBLE in the browser right now, and file:line
> for where it renders. Specifically:
>
> 1. Cascade visibility (frontier hop shown) — visible? where?
> 2. Honest NET flag (OFF·GROQ vs OFF·FRONTIER vs ON) — visible? where?
> 3. Decline path (nothing leaves, no fact) — is it in THIS script or a
>    separate variant Bill has to load? Which?
> 4. Code-built payload proof — Bill looked and sees NO hover functionality
>    and no proof pane. Is it actually wired and rendering, or was the prior
>    report wrong? If it doesn't render, say so plainly.
> 5. The new MASTER → HKDF(sam) → KEY → UNLOCK line in the speaker pane —
>    what is this, when did it land, and is it accurate to the CURRENT
>    (filter-based) architecture? It appears to visualize the single-master
>    model the crypto spec is about to replace.
> 6. Empty speaker panes on this script — correct behavior (script doesn't
>    touch personal records) or a bug? If correct, should the UI say why
>    instead of just 'waiting'?
>
> Report the table. Change nothing. I need to know what the demo actually
> shows before deciding what to fix."

## WHAT WAS DONE

1. Identified that `/demo` serves `server/static/demo.html` (read fresh from
   disk on every request, `server/demo_dashboard.py:828-834`) — a separate
   file from the dev-console UI (`demo_dashboard.py`'s own inline `_HTML`)
   touched by the prior `SECURE_DEV_ENDPOINTS` session. Confirmed this is
   the actual page Bill watches for `boundary_and_consent`, not the console
   at `/`.
2. Traced each of the six questions to source, both frontend
   (`server/static/demo.html`) and backend (`server/voice_orch.py`,
   `harness/disclosure.py`, `harness/epistemic_record.py`,
   `server/demo_dashboard.py`).
3. Read both `demo_scripts/boundary_and_consent__v20260717_1330.json` and
   `demo_scripts/boundary_and_consent_decline__v20260718_1008.json` in full.
4. **Checked process staleness** — compared the running dashboard's start
   time against the commit timestamps of the code each question is about,
   after noticing the routing/NET/payload machinery is very recently landed
   (`5eee5dc`, same day). This turned out to be the load-bearing finding —
   see WHAT WAS FOUND.
5. Diffed `harness/epistemic_record.py` and `server/voice_orch.py` across
   `5eee5dc^..5eee5dc` to confirm exactly what was old vs. new, rather than
   assuming the newest file on disk reflects what's running.
6. Found two new PLAN-status spec docs (committed by a separate agent
   session between this dispatch and the prior one) that bear directly on
   question 5 — read enough of the first to characterize it accurately.
7. Made zero code changes. Ran no reset/seed/live-turn cycle — this
   dispatch is a static trace plus one live process-metadata check
   (`ps`), not a functional re-verification.

## WHAT WAS FOUND

**The load-bearing finding, true for questions 1, 2, and 4 alike: the
dashboard process Bill has been testing against predates the code these
questions are about.**

- `server.demo_dashboard --port 7871` (PID 9295) has been running since
  **2026-07-18 10:08:49** (`ps -p 9295 -o lstart`).
- Commit `5eee5dc` (DEMO_SCRIPT01_GOVERNANCE_VISIBILITY — the cascade
  writer, the NET fix, the payload-hover wiring) landed at **10:42:58** —
  34 minutes later.
- Confirmed by diff, not inference: `_write_disclosure_routing_log`
  (`server/voice_orch.py:269-321`) has zero occurrences in the commit
  before `5eee5dc` and three in `5eee5dc` itself (`git show 5eee5dc^:... |
  grep -c`). Before this commit, the disclosure-gate code path
  (`server/voice_orch.py:2662-2758`) never wrote anything to
  `router.jsonl` for T04/T04b — not a mislabeled row, no row at all.
- Confirmed by diff: `harness/epistemic_record.py`'s `net` field was
  `("off" if tier=="escalate" else "on") if tier else None` before
  `5eee5dc` — **"on" for every Groq mid/core call and every frontier
  crossing** (exactly D-08). `_compute_net` (`:114-131`), which actually
  distinguishes Groq/frontier/local, is new in `5eee5dc`.
- Python does not hot-reload; `server/voice_orch.py`, `harness/disclosure.py`,
  and `harness/epistemic_record.py` are all imported once into the running
  process. **None of the governance-visibility code can execute on the
  live port-7871 server until it is restarted.** `server/static/demo.html`
  itself IS read fresh every request (`demo_dashboard.py:834`) — the
  frontend Bill's browser fetches is current; the backend data it renders
  is not.

**A second, more serious finding, found while tracing question 5, not
asked for but directly relevant to "what the demo actually shows":**
`server/static/demo.html` has its own `VaultPanel` component
(`:294-393`) — a near-duplicate of the dev-console's `VaultSection` that
the prior `SECURE_DEV_ENDPOINTS` session fixed, but never itself touched
or even knew existed. `VaultPanel`'s decrypt call
(`server/static/demo.html:322-324`) still POSTs the **old**
`{ciphertext, encrypted_dek, owner}` body shape. The current
`/api/decrypt` (`server/demo_dashboard.py`, post-`5d6bde3`) requires
`{fact_id}` and no longer authenticates `/demo` at all. **The moment
port-7871 is restarted to pick up the governance-visibility fixes, the
`/demo` Vault pane will silently stop decrypting anything** — `/api/facts`
will 401 (no session ever established from `/demo`), `/api/decrypt` will
400/401 on every call, both swallowed by an empty `catch(_){}`
(`:330`, `demo_dashboard.py`'s own facts poll `:654`) — the
MASTER→HKDF→KEY→UNLOCK animation will still play (it's a client-side
timer, decoupled from whether decrypt actually succeeds) and land on
"● VAULT OPEN" over rows that stay permanently "ENCRYPTED · Fernet." Not
fixed here per "change nothing" — flagged for the next session that
touches either file.

Per-question findings (full detail, file:line, and the table are in the
chat response, not duplicated here):

1. **Cascade visibility** — wired correctly (`GateChip`, `isGate` dispatch
   in `RoutingRow`), not visible on the live server for the staleness
   reason above.
2. **Honest NET flag** — wired correctly on both ends, not visible for the
   same reason; the pre-`5eee5dc` bug (`net` always "on" except literal
   `escalate`) is what's actually still running.
3. **Decline path** — a separate script file
   (`boundary_and_consent_decline__v20260718_1008.json`, T04b="No, keep it
   local."), not a branch of the main script. Confirmed structurally: the
   decline branch (`voice_orch.py:2675-2679`) returns before the `else`
   clause that calls `call_frontier` (`:2687`) is ever reached — same
   file, cannot fall through.
4. **Payload proof hover** — wired correctly (backend populates
   `payload_fact_ids`/`payload_attributes` only for `gate_pending`,
   frontend renders them as a native `title` attribute), not visible for
   the staleness reason. Even once restarted, it's a plain browser tooltip
   with no icon or visual cue — real but easy to miss. The prior BUILD
   dispatch's own acceptance test says browser automation was unavailable
   that session too — its "prove it live" was API-level, same method used
   here, never an actual rendered check. Not wrong; not a visual
   confirmation either.
5. **MASTER→HKDF→KEY→UNLOCK** — accurate to what's running today: one
   master key, HKDF-derived per-owner keys, unchanged by the auth fix
   (confirmed independently by the new PLAN-status spec,
   `docs/deliverables/HIP_MemberIsolation__crypto-partition-and-recovery-design__v20260718_1117.md`,
   which states this plainly: "the root cause the prior trace named — one
   master key derives all — is untouched"). One UI copy line overclaims:
   "vault opens in their scope only" (`demo.html:1370`, the static
   HowToReadOverlay glossary — a second, non-live copy of this same
   text) reads as a cryptographic guarantee; the actual mechanism is a
   policy check (`_vault_selected_member`) over a server that can derive
   any member's key. Two new PLAN-status specs already propose retiring
   this model — nothing built yet.
6. **Empty speaker panes** — correct, by design, for a reason more specific
   than "the script doesn't write anything": household-owned facts
   (D3/D7/D10/D11 — everything but D1) are excluded from the
   read-triggers-reveal rule by design (`demo_dashboard.py:208-215`,
   `_household_fact_ids`) — only a WRITE reveals them. Since T01-T04 are
   pure reads, the HOUSEHOLD MEMORY section can never populate no matter
   how long the script runs; only T04b's new frontier-fact write would
   ever land there. The empty-state copy ("waiting — records appear when
   dialogue touches them," `demo.html:382,388`) is the same string
   regardless of cause and reads as "give it time" — true for genuinely
   untouched facts, structurally false for these four, which will never
   populate under this script no matter how long it runs.

## VERIFIED

- **Watched (live, but metadata-only):** `ps -p 9295 -o lstart` — actual
  process start time, not inferred. `git show <rev>:<path> | grep -c` —
  actual presence/absence of the relevant code at each commit, not
  assumed from commit messages.
- **Reasoned about, from source, not executed:** every rendering path
  (GateChip, netInfo, VaultPanel, the empty-state copy) — read directly,
  cross-checked against its actual call sites, not run in a browser. No
  browser tooling was available this session (same limitation the prior
  BUILD dispatch noted). The process-staleness finding substitutes for
  much of what a browser check would have shown anyway — code that cannot
  execute in the running process cannot render, regardless of what the
  browser would otherwise do with it.
- **Not verified this dispatch:** whether restarting port-7871 actually
  produces the rendering Bill expects to see (the code trace says it
  should, for 1/2/4; the VaultPanel finding says restarting will also
  break something). Restarting the live server was out of scope for a
  "change nothing" dispatch.

## HASH

NONE. No code changed. This dispatch doc and its chat-response table are
the only artifacts.

## OPEN

- **The dashboard has not been restarted since 10:08:49 this morning,
  across at least four commits that matter to what it renders**
  (`5eee5dc`, `5d6bde3`, and the two PLAN spec commits which don't affect
  runtime but do affect question 5's context). Restarting is the single
  highest-leverage next action if the goal is "see what's actually been
  built" — but it will also surface the `VaultPanel` regression above the
  moment it happens. Whoever restarts it should expect that, not discover
  it live in front of an audience.
- **The `VaultPanel`/`/demo` decrypt-contract mismatch is unfixed and
  unowned.** No defect ID exists for it yet — flagged here, not
  registered in `docs/BACKLOG.md` (out of scope for "change nothing";
  registering it is itself a documentation change beyond a pure trace,
  left for whoever picks this up next).
- **Payload-hover discoverability** (native `title` tooltip, no visual
  affordance) is a real UX gap independent of the staleness issue — worth
  a design pass once the underlying wiring is confirmed live.
- **The empty-state copy issue (Q6)** — same string for "will populate
  once touched" and "will never populate under this script" — is a small,
  precise fix (distinguish the two cases) that was not made here per
  instruction.
