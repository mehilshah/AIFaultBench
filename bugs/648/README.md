# Bug 648

`RemoteGraph` at the pinned LangGraph commit sends a request containing both runtime `context` and `config["configurable"]`.  The server rejects that documented combination with HTTP 400, preventing simultaneous middleware context and checkpoint thread configuration.  The local, deterministic repro uses a standard-library HTTP stub—there are no LLM, API-key, or third-party service calls—and currently reproduces the rejection on this host.

Files: `repro.py` is the failing reproduction; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run the isolated environment; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
