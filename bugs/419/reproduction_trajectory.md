# Reproduction Trajectory — Bug 419: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38620](https://github.com/jax-ml/jax/issues/38620)
- **Repository:** jax-ml/jax @ `4250605d1e353e8f3e5f943abc485d5bbe1fb250`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- bash run_repro.sh exits with status 1. repro_stdout.log shows jax.scipy.stats.chi2.logpdf returning nan for x=0.0, df=2.0 and x=inf, df=2.0 while scipy returns -0.6931471805599453 and -inf, respectively.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
