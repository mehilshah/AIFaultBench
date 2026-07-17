# Bug 277

This folder is a self-contained reproduction bundle for NumPyro issue 2181.

## What fails

`Poisson(rate).log_prob(value)` depends on whether `rate` was passed as an integer or a float. For the same near-integer `value`, `Poisson(2)` and `Poisson(2.0)` produce different log probabilities.

## Repro

```bash
bash run_repro.sh
```

The script bootstraps a local virtual environment, installs the minimal runtime
dependencies, and runs [`repro.py`](./repro.py) against the local
[`codebase/`](./codebase) checkout.
