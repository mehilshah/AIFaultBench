# Reproduction Trajectory — Bug 194: equinox

- **Bug report:** [https://github.com/patrick-kidger/equinox/issues/900](https://github.com/patrick-kidger/equinox/issues/900)
- **Repository:** patrick-kidger/equinox @ `15a800d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local virtualenv via `setup_env.sh`.
2. Install the pinned repro dependencies and the local `codebase/` editable package.
3. Run `repro.py` through `run_repro.sh` and observe the output shape mismatch.

## Observed behavior

- `bash run_repro.sh` prints `jax: (3, 4, 2) eqx: (4, 3, 2)` and then raises `AssertionError: wrong out_axes arrangement: expected (3, 4, 2), got (4, 3, 2)`.
- The captured logs in `repro_stdout.log` and `repro_stderr.log` show the same mismatch under the standardized setup.
- The local checkout reports `equinox version: 0.11.8` and reproduces the issue with `jax version: 0.4.28`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
