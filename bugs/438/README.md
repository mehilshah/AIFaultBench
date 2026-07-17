# DeepSpeed issue 7812 repro

This bundle reproduces the `DeepSpeedEngine.__del__` failure described in `bug_report.txt`.

What happens:
- `deepspeed.initialize()` fails early with `AssertionError: DeepSpeed lamb optimizer requires dynamic loss scaling`
- the partially constructed `DeepSpeedEngine` is later finalized
- `DeepSpeedEngine.destroy()` calls `is_deepcompile_active()`
- `_deepcompile_active` was never set, so `__del__` prints an `AttributeError`

Why the repro is CPU-only:
- the target bug is in the early constructor failure path, not in CUDA execution
- the harness uses `DS_ACCELERATOR=cpu` and a tiny `deepspeed.comm` shim so the run reaches the relevant failure instead of a separate CPU comm-op error

Files:
- `setup_env.sh` creates an isolated venv and installs the needed packages
- `run_repro.sh` runs the repro and writes `repro_stdout.log` and `repro_stderr.log`
- `repro.py` contains the minimal reproducer

Usage:
```bash
bash setup_env.sh
bash run_repro.sh
```
