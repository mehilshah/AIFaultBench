# Reproduction Trajectory — Bug 116: bayesflow

- **Bug report:** [https://github.com/bayesflow-org/bayesflow/issues/468](https://github.com/bayesflow-org/bayesflow/issues/468)
- **Repository:** bayesflow-org/bayesflow @ `a4d58c9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated venv and install the bundled requirements plus the local `codebase/` editable package.
2. Run `bash run_repro.sh` with `KERAS_BACKEND=numpy`.
3. Observe that `PointInferenceNetwork(...)["mvn"]["covariance"]` produces a non-finite inverse immediately after initialization.

## Observed behavior

- run_repro.sh exited with code 1.
- repro_stdout.log shows `inverse_finite=False`, `inverse_has_inf=True`, and `bug_reproduced=non_finite_inverse` for seed 0.
- repro_stderr.log contains `RuntimeWarning: overflow encountered in cast` from `numpy.linalg.inv` while inverting the covariance.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
