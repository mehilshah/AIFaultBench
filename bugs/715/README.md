# Bug 715

Langflow's `litellm` optional dependency omitted LiteLLM's required `proxy` extra. The offline repro checks the pinned metadata and imports LiteLLM's proxy module with Langflow's normal supporting dependencies installed; on this host it deterministically reports the missing `apscheduler` package and exits 1. No LLM client, API key, or provider call is used.

Current result: reproduced on this host.

Files: `repro.py` is the assertion script; `requirements.txt` and `setup_env.sh` create its isolated environment; `run_repro.sh` is the entrypoint; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
