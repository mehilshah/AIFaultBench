# Bug 314

This folder contains a self-contained repro bundle for:

`jax.scipy.special.gammaincc` returning `NaN` for `a = inf`.

## What was checked

- `repro.py` runs the minimal example from `bug_report.txt`.
- `setup_env.sh` creates an isolated venv and installs the local source tree plus the runtime deps.
- `run_repro.sh` runs the repro under CPU-only JAX.

## Result in this folder

The bug is not reproducible in the checked-in codebase + supported runtime set.

- `jaxlib 0.10.1` is rejected by the local source tree with a version check.
- `jaxlib 0.10.2` runs successfully and returns `[1.]` for `gammaincc(inf, 2.0)`.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro script exits with:

- `0` when the bug is reproduced
- `1` when the expected value is returned
- `2` when dependencies are missing
