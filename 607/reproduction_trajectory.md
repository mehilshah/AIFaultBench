# Reproduction Trajectory — Bug 607: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/37993](https://github.com/jax-ml/jax/issues/37993)
- **Repository:** jax-ml/jax @ `535ed7ad76113cc2fedaf4b230aabedbb348108f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate a local virtualenv with the packages in requirements.txt.
2. Run `PYTHONPATH=codebase .venv/bin/python repro.py` via run_repro.sh.
3. Compare NumPy and JAX on the float32 near-overflow array from bug_report.txt.
4. Observe that NumPy returns nan while JAX returns inf.

## Observed behavior

- With PYTHONPATH=codebase and the local .venv, the repro prints `numpy.std(x) = np.float32(nan)` and `jax.std(x) = inf`. The saved logs in repro_stdout.log and repro_stderr.log show the same result.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
