# DISPATCH_DEMO_PAYLOAD_PROOF
Status: BUILT
Reconciled-Against: (pending commit — see HASH)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_PAYLOAD_PROOF__code-built-payload-visible-provenance__v20260718_1230.md`
(child of REQ_DEMO_SCRIPT01_GOVERNANCE_VISIBILITY objective 4).

## THE ASK

Verbatim:

> Objective 4 (code-built payload proof) is not visible in the browser. The
> disclosure message states the fact_ids, and fact_ids show on hover, but neither
> PROVES the payload was assembled by code rather than composed by the model —
> which is the exact objection a technologist raises.
>
> Add an explicit, visible proof: a PROOF-tab view or pane that shows the
> outbound payload was built by the payload builder from Neo4j fact rows
> (address, zone_district by fact_id), with the model absent from the assembly
> path. Show the provenance, not just the ids. [...] Prove it live in the
> browser. Push, report the hash.

## WHAT WAS DONE

1. Re-read the current surfaces: `demo.html`'s `ProofOverlay` (1124),
   `GateChip` hover (199-217), `/api/demo/proof` (837),
   `harness/disclosure.py:build_payload`/`render_disclosure_prompt` (98/135),
   and the inline frontier fact-block string in `frontier_client.py:56-59`.
   Confirmed the objection: the only on-screen evidence was fact_ids restated
   in the consent message and the hover — neither shows the source rows, the
   assembler code, or determinism.
2. Wrote REQ_DEMO_PAYLOAD_PROOF first (before code, per CLAUDE.md gate item 8),
   with an acceptance test whose bar is "inspectable, not asserted."
3. **Behavior-preserving refactor:** extracted `build_frontier_fact_block(
   payload_rows)` from `call_frontier` (`harness/frontier_client.py`) so the
   proof surface shows the EXACT outbound bytes, not a re-implementation that
   could drift. `call_frontier` now calls it; verified the real frontier call
   still fires identically (see VERIFIED).
4. **New endpoint** `GET /api/demo/payload-proof`
   (`server/demo_dashboard.py`), ungated like `/api/demo/proof` because it
   ships NO decrypted value (sealed: length + sha256 only). It recomputes live
   from the graph + source and returns: the fact_ids the gate used (from the
   last `gate_pending` router row, else re-derived from the graph, labeled);
   the source `:Fact` rows (fact_id, attribute, rung, owner, sensitivity,
   value_len, value_sha256); the consent prompt + per-line fact_id provenance;
   the outbound block with values sealed; `inspect.getsource` of the three
   assembler functions; a **scanned** model-absent verdict
   (`model_call_indicators_in_assembler` — a scan of the shipped source for
   call signatures, not a constant); and a determinism proof (recompute →
   byte-identical consent/outbound sha256).
5. **New PROOF view** `PayloadProvenance` (`server/static/demo.html`), added as
   the **first** entry in the PROOF overlay ("⚙ PAYLOAD PROVENANCE — code
   built it, not the model"), default-selected. Renders the verdict banner,
   the source-rows table, the two assembled artifacts with line-level fact_id
   tracing, the determinism line, and a collapsible view of the assembler's
   actual source. The four existing file sources still list and render
   (additive, no regression).
6. Restarted the dashboard (launchd respawn), verified the endpoint and the
   full flow live, compiled the entire `demo.html` JSX through babel, and ran
   `--full`.

## WHAT WAS FOUND

- The frontier fact block was built inline in `call_frontier`
  (`frontier_client.py:56-59` pre-change) — a proof pane could not show the
  real outbound bytes without duplicating that string. Extraction to
  `build_frontier_fact_block` fixed this; it is the honest source of the
  "what leaves" artifact.
- The assembler source, scanned for the call signatures `requests.`,
  `openai`, `call_frontier(`, `https://`, `.post(`, `chatcompletion`,
  `responses.create`, `ollama`, `.generate(`, `completion(`, `anthropic`,
  yields **zero hits** — so `model_in_assembly_path` is a computed `false`,
  not a hardcoded boolean. The scan indicators are deliberately specific call
  signatures, not bare words: `render_disclosure_prompt`'s own text contains
  the string "outside model", which must not (and does not) trip the scan.

## VERIFIED

- **Watched run — the endpoint, live, on a real gate turn.** Loaded
  `boundary_and_consent__v20260717_1330.json`, fired T01-T04, then
  `GET /api/demo/payload-proof` returned `available:true`,
  `fact_id_source:"last disclosure-gate turn (router.jsonl)"`,
  `fact_ids:[9e4b4005…, 77f78f61…]`, `model_call_indicators_in_assembler:[]`,
  `model_in_assembly_path:false`, `deterministic:true`, and the two fact rows
  (address: household/medium/30b/sha 9be91e95; zone_district:
  household/low/6b/sha df5fd421) with **no plaintext**. The `assembler_source`
  field contained the actual `build_payload`/`render_disclosure_prompt`/
  `build_frontier_fact_block` source. consent_sha256 137971ad…, outbound_sha256
  31000c84….
- **Watched run — frontier refactor is behavior-preserving.** Fired T04b
  (approve); `logs/dashboard.log` shows
  `harness.frontier_client:call_frontier … call ok — model=gpt-4.1
  payload_facts=[9e4b4005…, 77f78f61…] answer_chars=1867` — the real outbound
  call still happens, same fact_ids, through the extracted function. Pure
  refactor confirmed.
- **Watched run — the page compiles.** Extracted the full 96,328-char
  `text/babel` block from `demo.html` and transformed it with
  `@babel/standalone` + `preset-react`: **"BABEL OK — full demo.html JSX
  compiles."** This rules out the blank-page risk that browser-less UI edits
  otherwise carry. `/demo` serves HTTP 200.
- **Watched run — `--full`, twice.** Run 1: `EXIT_CODE=1`, `RATCHET FAIL —
  regressed vs baseline: ['L2:care_coordination.T01', 'L2:care_coordination.T02']`
  — the exact documented signature of **D-24** (a medication-switch statement,
  "Elena was switched from metformin to Jardiance," lands under
  `medication_status` not `medication`, so the `(bill,elena,medication)`
  graph-state check finds 0 rows and T02's query returns empty_set). D-24 is
  registered (MANIFEST header, HIP_DefectRegister line 66) and confirmed
  reproducible on `b36fa95` before any of this code existed. In the same run,
  `care_coordination.T03` (D-16) and `three_zone_demo.T02` (D-21) both PASSED
  — the flake set rotates. Run 2 (no code changed between): **`EXIT_CODE=0`,
  fully green — `care_coordination.T01/T02` PASS, zero RATCHET/NEW-FAILURE
  lines.** The green second run is decisive: run 1's failures were the
  rotating D-24 detection flake, not a regression. This diff touches
  `frontier_client.py` (pure extraction, behavior-preserving),
  `demo_dashboard.py` (new endpoint, not in any harness layer), and
  `demo.html` (UI) — none reach the extraction/`medication_status`
  classification path the failures live in.
- **Reasoned about, not pixel-verified:** browser automation was unavailable
  this session (declined earlier by the user). The PROOF pane's rendering was
  verified by (a) the endpoint returning the exact JSON shape the React
  reads, field-for-field, and (b) the full JSX compiling under babel — but
  not by a human watching the overlay paint. Stated plainly per the parent
  REQ's constraint; this is not equivalent to pixel confirmation. The
  `fact_id_source:"recomputed from current graph"` fallback branch (no gate
  turn on record) was reasoned from the code, not exercised live (the test
  run had a gate turn on record).

## HASH

Pending — see the commit that carries this dispatch.

## OPEN

- No pixel-level browser confirmation (see VERIFIED). If Bill wants it,
  reconnect Chrome or check the PROOF overlay visually — the endpoint + babel
  compile are strong but not a substitute for watching it render.
- The endpoint ships value length + sha256, never plaintext. If a future need
  arises to show the real outbound values in the pane ("exactly these bytes
  left"), that requires gating the endpoint behind `require_dashboard_session`
  like `/api/facts` — deliberately not done here to keep the pane ungated and
  plaintext-free.
- The determinism proof shows byte-identity across two recomputes in one
  request. It does not, and cannot, prove the frontier MODEL didn't later
  paraphrase the payload — that is a different claim (the model receives the
  code-built payload; what it does with it is the frontier's output, governed
  separately). This pane proves the ASSEMBLY is code, which is the stated
  objective.
