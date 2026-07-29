# Bug 737

This reproduction shows that a streamable HTTP transport shutdown closes the session write stream before `ServerSession.send_log_message()` finishes. A subsequent log notification raises `anyio.ClosedResourceError`, matching the fault reported during server shutdown. The bug reproduces on this host without an HTTP listener, model provider, API key, or third-party runtime call.

Files: `repro.py` contains the deterministic reproduction; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` prepare and execute it; `repro_stdout.log` and `repro_stderr.log` contain final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
