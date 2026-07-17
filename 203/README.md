# Bug 203

This folder is a self-contained repro bundle for NumPyro issue 1911.

Observed failure:
- `MCMC.get_samples()` returns `{}` when the model contains only `numpyro.deterministic` sites.
- `MCMC.print_summary()` then crashes with `ValueError: max() iterable argument is empty`.

Files:
- `bug_report.txt`: source report from the benchmark.
- `codebase/`: local NumPyro checkout used for reproduction.
- `repro.py`: minimal failing script.
- `requirements.txt`: runtime dependencies for the repro environment.
- `setup_env.sh`: creates a local virtualenv and installs dependencies.
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`.
- `manifest.json`: metadata for the standardized folder.

Usage:
```bash
bash setup_env.sh
bash run_repro.sh
```
