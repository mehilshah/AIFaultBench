# Bug 666

This bundle reproduces issue #2073: running a user script named `smolagents.py`
causes Python to import that partially initialized local file instead of the
installed `smolagents` package. The offline repro asserts the resulting
`ImportError`; no model client, API key, or network service is used at runtime.

Current result on this host: reproduced.

Files:

- `repro.py` — deterministic shadowing reproduction
- `requirements.txt` — pinned runtime dependencies
- `setup_env.sh` / `run_repro.sh` — environment setup and single reproduction entrypoint
- `repro_stdout.log` / `repro_stderr.log` — final captured execution output
- `reproduction.json` / `reproduction_trajectory.md` — structured evidence and narrative

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
