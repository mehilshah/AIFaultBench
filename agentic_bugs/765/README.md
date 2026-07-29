# Bug 765

Separate `add_edge` calls into one LangGraph node do not make a dependency join.
This reproduction constructs the reported shape and checks that node `f` runs before
the `b -> c -> d` path can set its required state. On this host and the pinned
checkout, it raises the expected early-execution `RuntimeError`.

Files:

- `repro.py` — deterministic offline reproduction.
- `requirements.txt` — exact Python dependency pins.
- `setup_env.sh` / `run_repro.sh` — setup and single-command runner.
- `repro_stdout.log` / `repro_stderr.log` — output captured from the final run.
- `reproduction.json` / `reproduction_trajectory.md` — reproduction evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
