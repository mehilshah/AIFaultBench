# Bug 551 Reproduction

This folder reproduces the NumPyro `MatrixNormal` documentation mismatch from
issue 2026.

What the repro checks:
- `codebase/numpyro/distributions/continuous.py` says `scale_tril_row` and
  `scale_tril_column` are lower Cholesky factors of *correlation* matrices.
- The class definition uses `constraints.lower_cholesky` and samples with matrix
  multiplication, which is consistent with covariance factors.

Run:

```bash
bash run_repro.sh
```

The script writes the final JSON verdict to `reproduction.json` and prints
the same payload to stdout.
