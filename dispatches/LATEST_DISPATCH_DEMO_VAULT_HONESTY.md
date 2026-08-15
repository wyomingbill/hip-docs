# DISPATCH_DEMO_VAULT_HONESTY
Status: BUILT
Reconciled-Against: commit — see HASH below

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_VAULT_HONESTY__vaultpanel-rewire-and-overclaim-fixes__v20260718_1331.md`
— filed BEFORE code per CLAUDE.md gate item 8.

## THE ASK

See the REQ doc's own THE REQUIREMENT section for Bill's full verbatim
text. Summary: (1) rewire `server/static/demo.html`'s `VaultPanel` off the
pre-D-10 `/api/decrypt` contract before the dashboard is restarted, and
make its "VAULT OPEN" indicator reflect a real decrypt outcome, not a
timer; (2) reword two prose locations that overclaim cryptographic
member isolation; (3) fix the household-section empty-state copy, which
falsely implies "just wait" for facts that structurally never populate
under a read-only script; (4) then restart `:7871` and confirm all of
`DISPATCH_DEMO_SPEC_RECONCILIATION`'s six items live.

## WHAT WAS DONE

1. Set up a local, offline-independent JSX syntax check
   (`@babel/standalone` installed to a `/tmp` scratch dir, transpiled the
   file's `<script type="text/babel">` block directly) — confirmed the
   *pre-edit* file transpiled cleanly first, to have a real baseline, not
   an assumption.
2. Rewired `VaultPanel` (`server/static/demo.html:326-463`):
   - Added a `checkAuth`/`authed` state and a `VaultLogin` component
     (`:294-324`), mirroring the dev-console's existing pattern
     (`server/demo_dashboard.py`'s `VaultSection`/`VaultLogin`) — same
     shape, second file, so the two don't drift again.
   - `doDecrypt` now calls `POST /api/session/select-member` first, then
     `POST /api/decrypt {fact_id}` only — no `ciphertext`/`encrypted_dek`/
     `owner` in any request body.
   - Replaced the timer-driven `kdStep>=kdSteps.length-1` → "VAULT OPEN"
     with a `vaultOutcome` state (`"open"|"empty"|"failed"`) set only from
     real `fetch` results: `"open"` requires at least one `200` with
     plaintext; `"empty"` means zero facts were even eligible (nothing
     attempted, not a failure); `"failed"` means facts existed but no
     decrypt succeeded. Each path now also `console.error`s the actual
     failure reason, since the UI's own failed-state label says "see
     console" — that claim had to be made true, not just added.
3. Reworded the "MEMBER SPEAKS" glossary line and added an explicit
   honest-limits paragraph to the `HowToReadOverlay`'s "MEMBER VIEWS" card
   (`:1541-1583` at time of edit) — see WHAT WAS FOUND for the exact
   before/after.
4. Reworded the household-section empty-state copy
   (`server/static/demo.html:465`) only — left the personal-section copy
   (`:459`) unchanged, since it remains true (a personal-fact read does
   register as "touched").
5. Re-ran the babel transpile check after every edit round (three times
   total) — clean each time.
6. Restarted `:7871` via `launchctl kickstart -k gui/501/com.hip.demo.dashboard`
   — chosen over `scripts/restart-dashboard.sh`'s manual
   `pkill`+`nohup` because that job runs under launchd with
   `KeepAlive=true`: a plain `pkill` would race launchd's own respawn for
   the port. Confirmed the plist's baked-in `EnvironmentVariables` are
   current (`NEO4J_URI=bolt://localhost:7688`, `DASH_PORT=7871`, and the
   real API keys) before relying on it — the `OPENAI_API_KEY`-missing
   problem `D-11` recorded against this exact plist is fixed on-disk now,
   not still open.
7. Reset + reseeded the real Neo4j instance (`bolt://localhost:7688` —
   Bill's actual dashboard data, not a throwaway sandbox this time) via
   `scripts/demo_reset.py --yes` + `scripts/demo_seed.py`, since preparing
   a clean state for the verification run is the same thing Bill's own
   click-through will need next.
8. Drove all 6 turns of `boundary_and_consent__v20260717_1330.json`
   through the live dashboard's own `/api/demo/load` + `/api/demo/next` —
   the exact calls the browser buttons make, same method the prior BUILD
   dispatches in this area used.
9. Verified each of the six `DISPATCH_DEMO_SPEC_RECONCILIATION` items
   against the resulting live state — see VERIFIED.

## WHAT WAS FOUND

- **The "MEMBER VIEWS" reword** (`server/static/demo.html`, inside
  `HowToReadOverlay`): "HKDF key derived for that member; vault opens in
  their scope only" → "HKDF derives that member's key; a server-side
  policy check (which member this session selected) decides what gets
  decrypted" — plus a new standalone paragraph directly under the
  MASTER→HKDF→KEY→UNLOCK mini-diagram: *"What this actually is:
  owner-scoped retrieval + at-rest encryption. The server holds one master
  key and can derive any member's key on request — decryption is gated by
  the policy check above (which member this session selected), not by a
  cryptographic guarantee unique to each member."* Left the "OPERATOR" row
  and the three-line MASTER/KEY/UNLOCK mechanism list alone — both are
  accurate on their own; the overclaim was specifically in the "vault
  opens in their scope only" framing, not in describing HKDF/Fernet
  mechanically.
- **Household empty-state copy**: "waiting — records appear when dialogue
  touches them" → "household facts surface only when WRITTEN — being read
  or cited in conversation does not reveal them here." Generic (true for
  any script, not hardcoded to this one), matching CLAUDE.md's "don't
  over-fit a fix to one instance" instinct.
- **A real routing anomaly, unrelated to this fix, worth flagging:** on
  this run, T02 ("Can I schedule the plumber...") answered at `tier=edge`
  with `tier_target=qwen2.5:7b` (local) instead of the script's own
  expected `tier=mid`; T03 ("What's the best morning...") answered at
  `tier=mid` with `tier_target=llama-3.1-8b-instant` instead of expected
  `tier=core`. Both scripts' own `note` fields call this out explicitly
  ("If router answers at EDGE, the routing demo premise is broken — flag
  and report"). NET still reported honestly for whatever tier actually
  ran (confirmed correct in both cases) — this is a **routing-escalation**
  behavior, not a NET-honesty defect, and is out of scope for the three
  items this dispatch was asked to fix. Not chased further; flagged so
  Bill isn't surprised if T02/T03 look shallower than the script narrates
  when he clicks through.
- **D1 (Maya's personal appointment fact) was not in the touched set this
  run** — consistent with T03 landing at `mid` rather than `core` (the
  synthesis question that would pull D1 in apparently didn't need it at
  the shallower tier this time). This meant the live verification proved
  the `"open"` (real decrypt success) and cross-tab household-visibility
  paths directly, but not the `"empty"` vault-outcome path specifically —
  that path's logic (`toDecrypt.length===0`) is simple enough that code
  review + the babel transpile check stand in for it; flagged as the one
  code path not independently exercised live.

## VERIFIED

**Watched run**, live, against Bill's real dashboard and real Neo4j
instance (`bolt://localhost:7688`), not a sandbox:

1. `launchctl kickstart -k gui/501/com.hip.demo.dashboard` → new process
   confirmed listening on `:7871` within 4 seconds; `GET /`, `/demo`,
   `/api/members`, `/api/status` all `200`.
2. Served `/demo` HTML directly inspected — contains the new
   `household facts surface only when WRITTEN`, `What this actually is`,
   `VaultLogin`, `vaultOutcome` strings (9 matches) — confirms the edited
   file is what's actually being served, not a stale copy.
3. `demo_reset.py --yes` + `demo_seed.py` against the real instance —
   23 stale nodes deleted, 11 fresh seeded.
4. `POST /api/demo/load {"script": "boundary_and_consent__v20260717_1330.json"}`
   → `{"status":"loaded",...,"turn_total":6}`, then six sequential
   `POST /api/demo/next` calls, each blocking until its turn completed,
   ending `{"state":"done"}`.
5. **Item 1 (cascade visibility) — CONFIRMED LIVE.** `GET /api/routing`
   shows a real row for T04 (`disclosure_kind:"gate_pending"`,
   `payload_fact_ids` present) and T04b (`tier:"frontier"`,
   `tier_target:"openai:gpt-4.1"`, `disclosure_kind:"frontier_crossed"`) —
   both were entirely absent before `5eee5dc`; now present and correctly
   shaped for `GateChip` to render.
6. **Item 2 (honest NET) — CONFIRMED LIVE.** T03's row
   (`tier_target:"llama-3.1-8b-instant"`) matches `netInfo()`'s
   `GROQ_MODEL_TARGETS` → renders `OFF · GROQ`. T04b's row
   (`tier_target:"openai:gpt-4.1"`) matches the `openai:` prefix check →
   renders `OFF · FRONTIER`. T01's row (`tier_target:"qwen2.5:7b"`) is
   genuinely local → renders `ON`, correctly.
7. **Payload-provenance PROOF view (`f1afc56`, confirmed post-restart, not
   rebuilt here) — CONFIRMED LIVE.** `GET /api/demo/payload-proof` → `200`,
   `model_in_assembly_path: false`, `deterministic: true`.
8. **Item 4 (Vault pane actually decrypts) — CONFIRMED LIVE, the
   highest-risk item in this dispatch.** Logged in with the real operator
   token (`~/hip-harness/data/dashboard/.operator_token`), called
   `POST /api/session/select-member {"member":"maya"}` → `200`, then
   `POST /api/decrypt {"fact_id":"<the touched household zone_district
   fact>"}` → `200` with the **real, full OpenAI frontier answer**
   (the actual R-1-18 setback numbers, cited to lakewood.org) as
   plaintext — this is the genuine T04b write, round-tripped through
   encryption and back, through the exact code path `VaultPanel` now
   calls. A fresh, cookie-less `POST /api/decrypt` to the same `fact_id`
   immediately after → `401`, confirming the session gate still holds
   post-restart.
9. **Item 5 (overclaim strings gone) — CONFIRMED** by direct string
   search on the served HTML (see point 2) and by re-reading the edited
   source in place.
10. **Item 6 (empty-pane copy truthful) — CONFIRMED** by direct string
    search; not independently re-derived live beyond that (the underlying
    `_touched_fact_ids`/`_household_fact_ids` mechanism was already
    verified in `DISPATCH_DEMO_SPEC_RECONCILIATION` and is unchanged by
    this dispatch).

**Reasoned about, not independently executed live:** the `"empty"`
vault-outcome branch (no browser session ever selected a member with zero
touched facts this run, per the D1/tier finding above); actual pixel
rendering in a browser (no browser tooling available this session, same
limitation every prior dispatch in this area has stated plainly).

## HASH

See commit — staged: `server/static/demo.html`,
`docs/requirements/REQ_DEMO_VAULT_HONESTY__vaultpanel-rewire-and-overclaim-fixes__v20260718_1331.md`,
this dispatch doc, `docs/INDEX.md`, plus the still-uncommitted
`DISPATCH_DEMO_SPEC_RECONCILIATION` doc and its symlink from the prior
turn (same session, filed but not yet committed).

## OPEN

- **T02/T03 routing-escalation anomaly** (found in WHAT WAS FOUND) is
  unfixed and unowned — no defect ID yet. Not this dispatch's scope; worth
  a session of its own if it reproduces.
- **The `"empty"` vault-outcome path was not exercised live** this run —
  code-reviewed and babel-checked, not watched running. Worth confirming
  directly the next time a script leaves a member's tab with zero touched
  facts (e.g., `bill`'s tab on this same script, if a run ever completes
  with no household fact touched at all).
- **No browser was available to confirm actual pixel rendering** — every
  claim above is API-level, same limitation as every prior dispatch in
  this area. Bill's own planned click-through is the first real browser
  confirmation.
- **`docs/BACKLOG.md` was not updated** — this fix closes an
  unregistered bug (the `VaultPanel`/`/demo` decrypt-contract mismatch
  flagged in `DISPATCH_DEMO_SPEC_RECONCILIATION`'s OPEN section had no
  defect ID). Nothing to remove from the backlog; also nothing was added
  when it was found. Left as-is rather than retroactively inventing an ID
  for a bug that's now fixed before it was ever registered.
