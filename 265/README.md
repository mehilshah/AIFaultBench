# Darts repro bundle

This bundle reproduces `KeyError: 'future'` in `darts.models.forecasting.regression_model.RegressionModel._generate_lags`
when `lags_past_covariates` is passed as a dict, `lags_future_covariates` is passed as a non-dict, and
`output_chunk_shift > 0`.

## Reproduction

```bash
bash run_repro.sh
```

The script writes the command output to:

* `repro_stdout.log`
* `repro_stderr.log`

## Notes

* The repro uses the bundled `codebase/datasets/AirPassengers.csv` file and does not require network access.
* The package itself is installed in editable mode from `codebase/` with dependency installation controlled by
  `requirements.txt`.
