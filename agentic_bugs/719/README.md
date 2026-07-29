# Bug 719

This bundle reproduces browser-use issue [#4676](https://github.com/browser-use/browser-use/issues/4676): `TokenCost` wraps a raw LangChain `ChatOpenAI` using Browser Use's incompatible `ainvoke` signature, so a Pydantic output model becomes LangChain's `config` and causes `AttributeError: items`. The fault reproduced on this host without an LLM key or provider request.

The full checkout did not complete here, so this released-package issue uses the pinned `browser-use==0.12.6` wheel instead.

Files:

- `repro.py` — deterministic offline reproducer.
- `requirements.txt` and `setup_env.sh` — isolated environment setup.
- `run_repro.sh` — reproduction entry point.
- `repro_stdout.log` and `repro_stderr.log` — final captured run.
- `reproduction.json` and `reproduction_trajectory.md` — result metadata and narrative.

Run:

```bash
bash run_repro.sh
```
