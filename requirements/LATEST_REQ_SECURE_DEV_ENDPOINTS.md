# REQ_SECURE_DEV_ENDPOINTS
Status: IN_PROGRESS
Reconciled-Against: main, pre-fix (post 33049a4 + same-session frontier-tier build)

## THE REQUIREMENT

Bill's words, verbatim:

> "DISPATCH: SECURE_DEV_ENDPOINTS__api-facts-decrypt-auth__v20260718
> TYPE: BUILD
> GOAL: security — live plaintext bypass
> DEFECT: D-10 / TD-101b
>
> /api/facts (demo_dashboard.py:212) returns every member's ciphertext +
> wrapped DEK with no owner filter and no auth. /api/decrypt (:254) takes a
> caller-supplied owner and returns plaintext, also unauthenticated. Chain
> them and any network client reads any member's private facts. CC traced
> this from "known gap" to complete bypass this session.
>
> Fix, minimum:
>   - /api/decrypt: remove the caller-supplied `owner`. Derive the member
>     from an authenticated session, not the request body. No session ->
>     reject.
>   - /api/facts: scope to the authenticated member (own + household), same
>     WHERE clause the real retrieval path uses. Never return all members'
>     ciphertext in one response.
>   - If these endpoints exist only for the demo dashboard and nothing in
>     production needs them, say so and propose removing them entirely
>     instead.
>
> Confirm the demo still works after — the dashboard's own panes may call
> these. If they do, that call must carry the session too.
>
> REQ doc first. Prove: an unauthenticated curl to both endpoints is
> rejected; the demo still runs.
>
> Push, report the hash."

## THE ACCEPTANCE TEST

1. `curl -X POST /api/decrypt` with no session cookie, any body → 401,
   regardless of what `owner`/`ciphertext`/`encrypted_dek` are supplied.
2. `curl /api/facts` with no session cookie → 401, no fact data of any
   kind (not even ciphertext) in the response body.
3. With a valid dashboard session (logged in via the real operator token):
   the Vault pane's existing "OPERATOR VIEW" / "`<MEMBER>` SPEAKS" tabs
   still work end to end — selecting a member's tab still reveals that
   member's own + household plaintext facts, and nothing else decrypts.
4. No response from either endpoint, at any point, contains a decryptable
   `{ciphertext, encrypted_dek}` pair the client could replay against
   `/api/decrypt` for a member other than the one currently selected in
   that session.
5. Every other dashboard pane (routing, metrics, transcript, demo
   script runner) is unaffected — unauthenticated, exactly as before this
   fix (explicitly out of scope, see CONSTRAINTS).

## WHAT'S ALREADY DONE

- The bypass itself was traced end to end this session (not newly found —
  D-10/TD-101b already existed) —
  `docs/dispatches/DISPATCH_ISOLATION_TRACE__per-member-enforcement-mechanism__v20260718_1002.md`.
  That dispatch is read-only analysis; this REQ is the first code change
  against the finding.
- The real retrieval path's owner-scoping (`harness/extraction_queue.py:700-767`,
  `WHERE (f.owner = $owner OR f.owner = 'household')`) is unaffected by
  this REQ — it was never the vulnerable part. This REQ only touches the
  two dashboard debug endpoints named above.

## WHAT'S KNOWN BROKEN (before this build)

- `server/demo_dashboard.py:212-251` (`/api/facts`): no owner filter, no
  auth. Returns `ciphertext` + `encrypted_dek` for every `:Fact` node in
  one response.
- `server/demo_dashboard.py:254-266` (`/api/decrypt`): takes
  `{ciphertext, encrypted_dek, owner}` straight from the request body, no
  auth, no check that `owner` matches anything. `harness/encryption.py`'s
  `_derive_key(owner)` (`:79-92`) will derive any owner's key on request —
  see the isolation-trace dispatch for the full mechanism.
- **No session/auth concept exists anywhere in this codebase.** Confirmed
  by grep before starting (`session`/`cookie`/`Depends`/`Request` all
  absent from `demo_dashboard.py` except unrelated Neo4j driver
  `.session()` calls). Every other dashboard endpoint — `/api/reset`,
  `/api/demo/start`, `/api/text-query`'s `member` field — is equally
  unauthenticated and out of this REQ's scope (see CONSTRAINTS). This is
  the first auth mechanism built in this codebase; it did not exist to
  extend.

## WHAT WAS BUILT (see CONSTRAINTS for one explicit deviation)

1. **A single-operator dashboard session**, not a per-member login system
   — there is no per-household-member account model anywhere in this
   codebase to authenticate against, and building one was out of scope for
   a fix to two debug endpoints. A shared operator token (auto-generated
   0600 on first run at `~/hip-harness/data/dashboard/.operator_token`,
   overridable via `$HIP_DASHBOARD_TOKEN` — same pattern as
   `harness/encryption.py`'s master key) gates a session cookie
   (`hip_dashboard_session`, httponly, samesite=strict), set via
   `POST /api/session/login {token}` and checked by a `require_dashboard_session`
   FastAPI dependency.
2. **`/api/decrypt` redesigned around `fact_id`, not client-supplied
   ciphertext.** The endpoint now takes `{fact_id}` only, looks up the
   real `ciphertext`/`encrypted_dek`/`owner` itself from Neo4j, and only
   decrypts if that fact's `owner` matches the session's server-tracked
   *currently selected member* (see next point) or is `'household'`. The
   client can no longer supply `owner`, `ciphertext`, or `encrypted_dek` at
   all — closing the bypass more completely than scoping `owner` alone
   would have, since the old endpoint's real defect was trusting
   client-supplied ciphertext/DEK/owner as a triple, not just the `owner`
   field in isolation.
3. **Server-tracked "currently selected vault member"**
   (`POST /api/session/select-member {member}`, session-gated) — the Vault
   pane's existing "OPERATOR VIEW" vs "`<MEMBER>` SPEAKS" tabs already
   modeled exactly this state client-side; it now also exists server-side,
   authoritatively, and `/api/decrypt` reads it instead of trusting the
   request body. Selecting "operator" (or nothing) clears it, and
   `/api/decrypt` refuses (403) with nothing selected — matching the
   pane's own "OPERATOR VIEW sees ciphertext only" rule, now enforced
   server-side instead of only in the UI's copy.
4. **`/api/facts` gated behind the same session** and stripped of
   `ciphertext`/`encrypted_dek` from its response entirely — the client no
   longer needs them (decrypt is now `fact_id`-keyed), so they're not
   sent. `ciphertext_preview` (a already-truncated, non-actionable slice)
   is kept for the vault's cosmetic "this is actually encrypted" visual.
   See CONSTRAINTS for why this is a deliberate divergence from "scope to
   own + household," not an oversight.
5. Front end (`_HTML` in `demo_dashboard.py`): a `LoginGate` component
   wraps the dashboard root render — checks `/api/session/status` on
   mount, shows a minimal token-entry form if unauthenticated, renders
   `<HIPDashboard/>` once a session exists. `VaultSection`'s tab-change
   effect now calls `select-member` before decrypting, and `/api/decrypt`
   calls pass `fact_id` instead of `{ciphertext, encrypted_dek, owner}`.

## CONSTRAINTS

- **Deliberate deviation from the literal instruction, flagged, not
  silent:** Bill's fix spec says `/api/facts` should "scope to the
  authenticated member (own + household)... never return all members'
  ciphertext in one response." Implemented instead: `/api/facts` still
  returns metadata (fact_id, attribute, owner, sensitivity, confidence,
  timestamp) for **every** household member in one response, gated behind
  the session — but with `ciphertext`/`encrypted_dek` removed entirely,
  because the Vault pane's "OPERATOR VIEW" tab is a real, load-bearing
  demo feature (`server/demo_dashboard.py:1150`, `tabs=[{id:"operator",...}]`)
  that shows the whole household's encrypted vault at once, by design —
  narrowing `/api/facts` to one member would delete that feature outright,
  not just fix a bug. Since `/api/decrypt` no longer accepts client-supplied
  ciphertext at all (point 2 above), the actual exploit chain ("chain them
  and any network client reads any member's private facts") is closed
  regardless of `/api/facts`'s scope — decryptable material never leaves
  the server to an unauthenticated caller, and an authenticated caller
  still can't turn ANY fact_id into plaintext without also holding a
  session where that member is selected. **If this reasoning is wrong and
  the operator-overview tab should be cut instead, say so — this is the
  one call in this build a technologist reviewer should double-check.**
- Out of scope: every other unauthenticated dashboard endpoint
  (`/api/reset`, `/api/demo/*`, `/api/text-query`'s client-supplied
  `member` field — see the isolation-trace dispatch's OPEN section). This
  REQ fixes the two endpoints named in the dispatch and nothing else. The
  broader "should the whole dashboard require a session" question is
  `docs/BACKLOG.md`'s `REQ_TD101` line, not this REQ.
- Do not touch the real retrieval path (`harness/extraction_queue.py`,
  `harness/injection_contract.py`) — verified clean by the isolation trace,
  not the subject of this fix.
- Removal (the dispatch's third option) was considered and rejected: both
  endpoints power load-bearing Vault-pane demo functionality (confirmed by
  reading the client-side call sites,
  `server/demo_dashboard.py:1176`/`:1364`), not leftover dev debris.
