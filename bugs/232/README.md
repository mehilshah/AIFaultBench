# NeuralProphet future-regressor null forecast repro

This bundle reproduces the issue reported in https://github.com/ourownstory/neural_prophet/issues/1567.

The failing case is:

- `n_lags = 15`
- `n_forecasts = 15`
- training dataframe length is exactly `30`
- a future regressor is configured

Observed result:

- `predict()` returns a dataframe where every `yhat*` column is `NaN`
- the same data without the future regressor produces a populated forecast

Run:

```bash
./run_repro.sh
```

The script prints a JSON summary of both forecasts.
