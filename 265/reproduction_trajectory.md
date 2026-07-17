# Reproduction Trajectory — Bug 265: darts

- **Bug report:** [https://github.com/unit8co/darts/issues/2652](https://github.com/unit8co/darts/issues/2652)
- **Repository:** unit8co/darts @ `c52ec83`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Installed the repro environment with `setup_env.sh`.
2. Loaded the bundled AirPassengers CSV and built the target and covariate TimeSeries objects.
3. Instantiated `LinearRegressionModel(lags_past_covariates={'month': [-6]}, lags_future_covariates=[0], output_chunk_shift=1)` and observed `KeyError: 'future'`.

## Observed behavior

- Running the bundle via `bash run_repro.sh` reproduced `KeyError: 'future'` while constructing `LinearRegressionModel` with `lags_past_covariates` as a dict, `lags_future_covariates` as a list, and `output_chunk_shift=1`. The traceback points to `codebase/darts/models/forecasting/regression_model.py:399`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
