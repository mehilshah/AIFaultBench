# Reproduction Bundle

This bundle reproduces the Generalized Advantage Estimation documentation bug
reported in `bug_report.txt`.

The issue is in `codebase/labml_nn/rl/ppo/gae.py`:

- the infinite-horizon example repeats `r_{t+1}` where it should advance to `r_{t+2}`
- the weighting formula omits the `(1-\lambda)` factor

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

`setup_env.sh` creates a local `.venv` so it does not need system-wide Python
package installation privileges.

`run_repro.sh` intentionally fails with an `AssertionError` after printing the
relevant source excerpt and the incorrect formulas.
