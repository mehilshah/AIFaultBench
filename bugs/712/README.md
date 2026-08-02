# Bug 712

Langflow's custom-component sandbox drops `from __future__ import annotations` when it recompiles definitions. The offline reproduction executes the pinned sandbox code with a `TYPE_CHECKING`-only annotation and checks that it raises the reported `NameError`. On this host the fault reproduced: the script prints the exact `NameError` and deliberately exits 1.

Files: `repro.py`, `requirements.txt`, `setup_env.sh`, `run_repro.sh`, `repro_stdout.log`, `repro_stderr.log`, `reproduction.json`, and `reproduction_trajectory.md`.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
