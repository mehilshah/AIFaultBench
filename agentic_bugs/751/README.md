# Bug 751

This bug report claimed that dynamically scheduled `Send` objects could not be JSON-serialized by `PostgresSaver`. The offline repro executes the report's map-reduce graph through the pinned PostgresSaver implementation, using a local cursor that validates every JSONB value without connecting to PostgreSQL. On this host the graph completes, so the reported failure is not reproduced at the pinned checkout.

Files:

- `repro.py` — deterministic offline reproduction attempt.
- `requirements.txt` — pinned runtime dependencies.
- `setup_env.sh` — creates the virtual environment and installs the editable checkout packages.
- `run_repro.sh` — single reproduction entrypoint.
- `repro_stdout.log` / `repro_stderr.log` — output from the final run.
- `reproduction.json` / `reproduction_trajectory.md` — verdict and evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
