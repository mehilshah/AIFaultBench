# Bug 651

On the pinned smolagents commit, `agent.replay(detailed=True)` passes `ChatMessage` dataclass objects to a logger that calls `dict(message)`.  Since `ChatMessage` is not iterable, this raises `TypeError`.  The repro builds an agent with a local fake model, injects the same kind of recorded action step that an agent run produces, and verifies the exact failure without any provider or network call.

Current result on this host: reproduced.

Files:

- `repro.py` — deterministic failing reproduction.
- `requirements.txt` — pinned runtime dependencies.
- `setup_env.sh` — creates the isolated environment.
- `run_repro.sh` — reproducible entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — output from the final run.
- `reproduction.json` and `reproduction_trajectory.md` — evidence and narrative.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
