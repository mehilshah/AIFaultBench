# Reproduction Trajectory — Bug 551: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2026](https://github.com/pyro-ppl/numpyro/issues/2026)
- **Repository:** pyro-ppl/numpyro @ `b49b8f8d389d6357ab04003a003ef9fa16ee2e43`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Open codebase/numpyro/distributions/continuous.py.
2. Inspect the MatrixNormal docstring at lines 1444-1452.
3. Inspect arg_constraints and sample() at lines 1459-1500.
4. Confirm the docstring says 'lower cholesky of rows/columns correlation matrix' while the implementation uses lower_cholesky factors and covariance-style sampling.

## Observed behavior

- See the captured logs below for the observed output.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
