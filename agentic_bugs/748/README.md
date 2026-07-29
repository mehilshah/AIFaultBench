# Bug 748

This reproduces langgraph issue #6578: a tool returns `Command(goto="__end__")`, but the
agent loop still invokes its model again. `repro.py` uses a deterministic local fake chat model,
so it makes no provider calls or requires no API key; it fails only when that second invocation
occurs. The fault reproduced on this host (the repro exits 1 with the deliberate observed-fault
exception).

The full repository clone was impractically delayed by concurrent clone/index operations on this
host, so this bundle uses the issue-report's pinned released-package environment instead:
LangChain 1.1.0, LangGraph 1.0.4, and matching pinned dependencies.

Files:

- `repro.py` — deterministic offline reproduction.
- `requirements.txt` — exact package pins.
- `setup_env.sh` — creates and installs `.venv`.
- `run_repro.sh` — bootstraps the environment and runs the repro.
- `repro_stdout.log` and `repro_stderr.log` — final captured evidence.
- `reproduction.json` and `reproduction_trajectory.md` — structured result and narrative.

Run:

```bash
bash run_repro.sh
```
