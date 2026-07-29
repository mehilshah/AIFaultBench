# Bug 750

This checks the claim that an `@task` executed before an interrupt runs again when a `StateGraph` compiled without a checkpointer is resumed with an API-style runtime-injected saver. The graph uses only an in-memory saver and a deterministic call counter; no model or network service is used. On this host the task runs once, so the reported fault is not reproduced.

The pinned Git checkout could not be obtained here: `setup_codebase.sh` created an empty Git repository despite the pinned SHA being reachable. The pinned source snapshot identifies itself as the released `langgraph==1.0.4`, so this entry uses that permitted package fallback with the issue-era LangGraph dependency versions.

Files:

- `repro.py` — deterministic interrupt/resume check.
- `requirements.txt` — exact package pins.
- `setup_env.sh` — virtual-environment bootstrap.
- `run_repro.sh` — reproduction entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — final captured output.
- `reproduction.json` and `reproduction_trajectory.md` — outcome and evidence.

Run:

```bash
bash run_repro.sh
```
