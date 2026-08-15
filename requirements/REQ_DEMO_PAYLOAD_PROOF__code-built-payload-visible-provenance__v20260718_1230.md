# REQ_DEMO_PAYLOAD_PROOF
Status: BUILT
Reconciled-Against: (pending commit — see dispatch HASH)

Parent: REQ_DEMO_SCRIPT01_GOVERNANCE_VISIBILITY__cascade-offnet-decline-payload__v20260718_1002.md
(objective 4). That REQ's objective 4 was met to the letter — fact_ids +
`assembled_by` surfaced in router.jsonl, shown on GateChip hover — but not to
the intent. This REQ raises the bar objective 4 actually needed.

## THE REQUIREMENT

Bill's words, verbatim:

> Objective 4 (code-built payload proof) is not visible in the browser. The
> disclosure message states the fact_ids, and fact_ids show on hover, but neither
> PROVES the payload was assembled by code rather than composed by the model —
> which is the exact objection a technologist raises.
>
> Add an explicit, visible proof: a PROOF-tab view or pane that shows the
> outbound payload was built by the payload builder from Neo4j fact rows
> (address, zone_district by fact_id), with the model absent from the assembly
> path. Show the provenance, not just the ids. If the only current evidence is
> hover-a-fact_id, that is insufficient — make the "code built this, not the
> model" claim something visible on screen.
>
> Prove it live in the browser. Push, report the hash.

## THE ACCEPTANCE TEST

Against the live dashboard (port 7871), after a `boundary_and_consent`
disclosure-gate turn (T04) has fired, opening the PROOF overlay shows a
PAYLOAD PROVENANCE view that makes the "code built this, not the model" claim
inspectable — not merely asserted. Specifically, the view shows, all sourced
from a live endpoint that recomputes from the graph, not from cached text:

1. **The source fact rows, read from Neo4j by fact_id** — for each payload
   fact (address, zone_district): fact_id, attribute, trust rung, owner,
   sensitivity. These are the actual `:Fact` rows the builder matched, not a
   restatement of the consent message.
2. **The assembled artifacts, each line tracing to a fact_id** — the consent
   prompt HIP shows (attribute + rung + fact_id per line, one line per fact,
   nothing else), and the outbound fact block that actually leaves the network
   (values sealed in this view — length + sha256 — but structure intact, one
   `fact_id`-tagged line per fact).
3. **The assembler's own source code** — `inspect.getsource` of
   `build_payload` + `render_disclosure_prompt` + the frontier fact-block
   builder, shown on screen, so a viewer can read that assembly is fact-row
   iteration and string templating with no model/LLM/network call in it.
4. **A computed "model absent" verdict** — the endpoint scans the assembler
   source for outbound-call / model-client indicators and reports the count
   (0 → verdict green: "model not in the assembly path"). Not a hardcoded
   boolean; a scan of the actual source shipped in the same response.
5. **A determinism proof** — the endpoint recomputes the payload a second time
   from the same fact_ids and confirms the assembled output is byte-identical
   (matching sha256). Stated on screen as: a model-composed message is not
   reproducible byte-for-byte; this is, because it is code.

Verified live in the browser path: the endpoint returns the above for a real
gate turn, and the PROOF overlay renders it as a selectable view. (Browser
automation may be unavailable; if so, the endpoint's JSON is exercised
directly via the same URL the pane fetches, and the React source is confirmed
to render that exact shape — stated plainly as not pixel-verified, per the
parent REQ's constraint.)

## WHAT'S ALREADY DONE

- Objective 4's data plumbing (5eee5dc): `_write_disclosure_routing_log`
  writes `assembled_by`, `payload_fact_ids`, `payload_attributes` on the
  `gate_pending` router row; GateChip shows fact_ids on hover. This REQ builds
  the visible proof ON TOP of that data; it does not redo it.
- `harness/disclosure.py:build_payload` (`:98`) already reads `:Fact` rows by
  fact_id and returns `{fact_id, attribute, value, rung}`;
  `render_disclosure_prompt` (`:135`) already templates them with no model
  call. The claim is already TRUE in code — this REQ makes it VISIBLE.
- The PROOF overlay (`server/static/demo.html:1124`) and `/api/demo/proof`
  (`server/demo_dashboard.py:706`) already exist as the surface to extend.

## WHAT'S KNOWN BROKEN

- The only on-screen evidence today is the GateChip hover
  (`demo.html:199-217`) listing fact_ids, and the consent message text. Both
  restate the fact_ids; neither shows the *source rows* the builder read, the
  *assembler code*, or that the output is a deterministic function of the rows.
  A technologist's objection ("the model could have written that message
  citing those ids") is not answered by either.
- The frontier fact-block string is built inline inside `call_frontier`
  (`harness/frontier_client.py:56-59`), so a proof pane cannot show the EXACT
  outbound bytes without re-implementing that string (which could drift). The
  builder must be extracted to a named pure function both the caller and the
  proof endpoint use, or the proof is a re-implementation, not the real thing.

## CONSTRAINTS

- **No plaintext exposure regression.** The proof view must not ship decrypted
  fact values to the browser (address/zone_district plaintext). Values are
  shown sealed (length + sha256); the consent prompt is valueless by design.
  This keeps the new endpoint ungated (consistent with `/api/demo/proof` and
  `/api/routing`, which are not session-gated) without exposing household
  plaintext.
- **Do not fake the proof.** Every element must be computed live from the
  graph and the actual source (`inspect.getsource`), not hardcoded. The
  determinism check must actually recompute. The "model absent" verdict must
  be a real scan, not a literal `true`.
- **The frontier extraction is behavior-preserving.** Extracting the
  fact-block builder from `call_frontier` must produce byte-identical outbound
  requests — a pure refactor, verified by the frontier path still working.
- **Existing PROOF overlay behavior must not regress** — the four existing
  file sources (router, turns_demo, run_status, transcripts) still list and
  render; the new view is additive.
- Per CLAUDE.md item 12: `voice_orch.py` is not touched by this change
  (the gate already writes the router row); the change is
  `frontier_client.py` (pure extraction) + `demo_dashboard.py` (new endpoint)
  + `demo.html` (new view). `--full` is still run before done, and the actual
  RATCHET output read, because `frontier_client.py` is harness-adjacent.
