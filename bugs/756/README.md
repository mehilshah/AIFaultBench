# Bug 756

At the pinned smolagents commit, the local restricted Python executor does not
provide the built-in `bytes` type. The offline repro executes the issue's
`type(bytes)` expression directly through `LocalPythonExecutor` and verifies
that it raises the reported `InterpreterError`.

The bug reproduces on this host.

Files: `repro.py` is the minimal check; `requirements.txt` pins its runtime
dependencies; `setup_env.sh` creates the environment; `run_repro.sh` runs it;
the `repro_*.log` files contain final-run evidence; and `reproduction.json` and
`reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
