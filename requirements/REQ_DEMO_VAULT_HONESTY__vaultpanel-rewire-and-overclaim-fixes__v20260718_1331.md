# REQ_DEMO_VAULT_HONESTY
Status: IN_PROGRESS
Reconciled-Against: main f1afc56

## THE REQUIREMENT

Bill's words, verbatim:

> "Do NOT restart the :7871 dashboard yet. Two things must land first or the
> restart breaks the Vault pane.
>
> 1. FIX demo.html's VaultPanel (:294-393). It still POSTs {ciphertext,
>    encrypted_dek, owner} to /api/decrypt (:322-324). The D-10 fix rejects
>    that. On restart it will 401/reject silently while the MASTER→HKDF→UNLOCK
>    animation keeps playing on a client-side timer and lands on "VAULT OPEN"
>    over rows that never decrypted — a fake success. Rewire it to the new
>    session-based /api/decrypt (fact_id only, server-tracked member), and
>    make the animation reflect ACTUAL decrypt success, not a timer.
>
> 2. FIX the two overclaim strings (#5): demo.html:1370 "vault opens in their
>    scope only" and the HowToReadOverlay glossary copy at :1367-1388. Both
>    read as cryptographic guarantees. The real mechanism is a policy check
>    over a server that can derive any member's key. Reword to state what's
>    actually true today: owner-scoped retrieval + at-rest encryption, NOT
>    cryptographic member isolation. This is the honest-limits reframe — the
>    demo must stop implying crypto it doesn't have.
>
> 3. FIX the empty-pane copy (#6): demo.html:382,388 "waiting — records appear
>    when dialogue touches them" is false for this script — these facts are
>    household-owned and excluded by design, they will NEVER appear. Say
>    that: "household facts — not shown in personal memory" or similar.
>    Don't imply they're coming.
>
> THEN restart the dashboard (source ~/.env.dev first). Confirm in the
> browser: cascade shows, NET flag shows OFF·GROQ/OFF·FRONTIER, payload proof
> renders, Vault pane actually decrypts (or honestly shows it can't),
> overclaim strings gone, empty-pane copy truthful.
>
> Bill clicks through all 6 turns at the screen after. Push, report the
> hash."

## THE ACCEPTANCE TEST

1. `VaultPanel` no longer sends `ciphertext`/`encrypted_dek`/`owner` in any
   `/api/decrypt` request body — only `fact_id`.
2. `VaultPanel` establishes a dashboard session (login form, matching the
   dev-console's existing pattern) before attempting any decrypt; without a
   session, it says so rather than silently failing.
3. The "VAULT OPEN" indicator only shows after at least one real decrypt
   call has returned `200` with plaintext. A tab with facts but zero
   successful decrypts shows a distinct, honest failure state. A tab with
   no touched facts shows a distinct, honest empty state (not "open" and
   not "failed" — nothing was attempted).
4. `demo.html:1370` and the surrounding `HowToReadOverlay` "MEMBER VIEWS"
   copy no longer claims the vault "opens in their scope only" as if that
   were a cryptographic guarantee. Reworded to name the actual mechanism:
   owner-scoped retrieval + at-rest encryption, with an explicit statement
   that the server can derive any member's key and gates access via a
   policy check, not independent per-member cryptography.
5. `demo.html:388` (household-section empty copy) no longer implies
   "wait, it's coming" — states plainly that household facts reveal only
   on a write, not a read, so a read-only script's citations will never
   surface them here.
6. `demo.html:382` (personal-section empty copy) is unchanged — it remains
   true (a personal-fact read does register as "touched").
7. `server/static/demo.html`'s JSX transpiles cleanly under
   `@babel/standalone` (checked locally, not just "no blank page").
8. Dashboard restarted (`~/.env.dev` sourced first). Live in the browser
   against a fresh `boundary_and_consent` run: cascade rows visible, NET
   flag correct (OFF·GROQ / OFF·FRONTIER / ON), payload-provenance PROOF
   view renders (objective 4, already shipped in `f1afc56` — confirmed
   working post-restart, not re-built here), Vault pane actually decrypts
   (or shows an honest failure), overclaim strings gone, empty-pane copy
   truthful.
9. Bill clicks through all 6 turns live and confirms.

## WHAT'S ALREADY DONE

- `/api/decrypt` (`fact_id`-only, session + selected-member gated) and
  `/api/facts` (session-gated, no ciphertext/DEK in response) —
  `REQ_SECURE_DEV_ENDPOINTS`, commit `5d6bde3`. This REQ does not touch the
  backend contract, only the one frontend consumer that was never migrated
  to it.
- The dev-console's own `VaultSection`/`VaultLogin` (`server/demo_dashboard.py`)
  already implement the session-login pattern this REQ ports into
  `server/static/demo.html`'s `VaultPanel` — same shape, second file.
- Cascade visibility, honest NET, and payload-provenance PROOF view
  (`5eee5dc`, `f1afc56`) — live once the dashboard restarts; this REQ
  does not modify them, only confirms them post-restart per item 8.

## WHAT'S KNOWN BROKEN (before this build)

- `VaultPanel` (`server/static/demo.html:294-393`) POSTs the pre-D-10 body
  shape to `/api/decrypt`; every call would now fail, silently, while the
  UI still reports success — see `DISPATCH_DEMO_SPEC_RECONCILIATION`.
- Two prose locations overclaim a cryptographic guarantee the system does
  not have (`:1370` and the surrounding glossary block).
- The household-section empty-state copy is misleading for any read-only
  script (this one specifically, but the underlying claim is generically
  wrong wherever a household fact is only ever read, not written).

## CONSTRAINTS

- Do not touch the backend `/api/decrypt`/`/api/facts` contract — already
  correct, built and proven in `REQ_SECURE_DEV_ENDPOINTS`.
- Do not touch `f1afc56`'s new `PayloadProvenance` view or
  `/api/demo/payload-proof` — out of scope, already shipped, confirm only.
- Do not re-litigate objective 4 (payload proof) — that REQ
  (`REQ_DEMO_PAYLOAD_PROOF`) is a separate, already-landed track.
- Restart only after 1-3 are verified to transpile and the code is
  reviewed — Bill's own ordering, stated explicitly ("must land first or
  the restart breaks the Vault pane").
- Verify with a real babel transpile (network-fetched `@babel/standalone`
  in an isolated `/tmp` scratch install), not just "no blank page in my
  head" — this file has no build step and no test harness of its own.
