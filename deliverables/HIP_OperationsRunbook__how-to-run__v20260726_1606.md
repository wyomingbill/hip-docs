# HIP Operations Runbook
How to run the system. Separate from the REQ docs (what it does) and the plan of record (what's next). This is how to operate the machine it runs on.

## The machines
- The mini: [REDACTED-USER]@[REDACTED-MACHINE-NAME], Tailscale [REDACTED-TAILNET-ADDRESS], alias "mini" in SSH config. ALL real work runs here. It is a MacBook Pro used as a server; it runs on battery and CAN die mid-run, which kills every running session. Keep it plugged in.
- The laptop: billbrewster@Bills-MacBook-Pro, Tailscale 100.75.242.86. NO working stack. Has no ~/hip-roadmap, no bill-ai user. Sessions here cannot run the harness and must SSH to the mini. Do not run builds from the laptop reaching over SSH; open a session ON the mini.

## Getting onto the mini
ssh [REDACTED-USER]@[REDACTED-TAILNET-ADDRESS] (or `ssh mini`). If Tailscale shows the mini offline, it is asleep, off, or battery dead; wake it physically. Give it a minute to rejoin the tailnet after power on.

## Confirm before running ANYTHING
whoami && hostname && git -C ~/hip-roadmap branch --show-current && git -C ~/hip-roadmap log --oneline -3
Expect bill-ai, the mini hostname, branch roadmap, recent commits. If branch or box is wrong, STOP. This check has caught a wrong-worktree write twice.

## The worktrees (git worktree list)
- ~/hip-roadmap (roadmap) = all active build. This is home.
- ~/hip-dev (main) = frozen demo, runs on its own graph.
- ~/hip-frontier-label, ~/hip-roadmap-crypto-p1/-p2, ~/hip-roadmap-stage1-wip = older parallel worktrees. Easy to land in by accident. Always confirm branch=roadmap before running.

## The venv and env
The harness python is ~/hip-dev/.venv/bin/python, sourced from .env.dev. Run the harness with that interpreter, not bare `python`.

## Graphs
- bolt://localhost:7688 = roadmap graph (11-12 facts, all v2, operator-blind).
- bolt://localhost:7689 = demo graph (hip-dev). Separated 2026-07-21 after the demo wiped a migration on the shared graph. Do not let anything but the demo write to 7689 or anything but roadmap work write to 7688.
- Two Ollama daemons: :11434 default, :11435 harness-pinned. Do NOT kill either (TD-129: a kill caused 41 failures).

## Memory pressure (TD-129) - the --full killer
--full needs RAM. At low free memory (~100MB) with five concurrent Ollama processes, the OS SIGKILLs the run mid-flight. Before --full: vm_stat | head -3, confirm free memory is healthy (a fresh boot gives ~3GB). If --full OOMs, it is not a code failure; re-run on a clean memory window. Real fix (unbuilt): load-sharing/timeout work on the Ollama daemons.

## Running the gate
Lean first: <venv> -m eval.harness --layer 7. Then full: <venv> -m eval.harness --full. --full takes several minutes; run it foreground with nothing else competing for RAM. Care_coordination T01/T02 only appear in --full, not lean L7.

Preferred entry point: scripts/run_harness.sh [args] from ~/hip-roadmap, not the venv command above directly. It refuses from the wrong directory or with empty NEO4J_PASSWORD/GROQ_API_KEY, starts neo4j-dev on 7688 if needed, refuses --full under 2GB free (TD-129), and tees to /tmp/hip_harness_<timestamp>.log.

## Standing secrets note
The OpenAI key in .env.dev is dead (revoked, confirmed) but still sits in pushed git history; replace the dead value so the harness stops needing overrides. Check the plist secrets (Groq, SerpAPI, Neo4j) against history and rotate if live.

## Reading document changes
Regenerate text renderings of every whitepaper/business/NDA `.docx` with `scripts/docx_to_text.sh`. `git diff` on `docs/rendered/` — not the binaries — is how you read what changed in a document.
