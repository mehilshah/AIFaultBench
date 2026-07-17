# Reproduction Trajectory — Bug 232: neuralprophet

- **Bug report:** [https://github.com/ourownstory/neural_prophet/issues/1567](https://github.com/ourownstory/neural_prophet/issues/1567)
- **Repository:** ourownstory/neural_prophet @ `2354356`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a 30-row daily dataframe with ds, y, and reg columns.
2. Fit NeuralProphet with n_lags=15, n_forecasts=15, and a future regressor named reg.
3. Call predict on the same dataframe and observe that all yhat columns are NaN.
4. Fit the same model without the future regressor and confirm predict returns populated yhat values.

## Observed behavior

- With a future regressor enabled, the forecast summary reports 0 non-null values for every yhat column across 15 rows.
- The control model without the future regressor reports one non-null value in each yhat column across 30 rows.
- stderr shows NeuralProphet dropping 15 trailing rows because future regressor values are NaN: 'Dropped 15 rows at the end with NaNs in future regressors.'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
