# Reproduction Trajectory — Bug 542: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38099](https://github.com/jax-ml/jax/issues/38099)
- **Repository:** jax-ml/jax @ `eb93eda9fbe95cf21c1501db8b064f66b040bf33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtual environment and installed the runtime dependencies from requirements.txt.
2. Ran bash run_repro.sh with JAX_PLATFORMS=cpu and PYTHONPATH pointing at codebase/.
3. Observed the mismatch: jit(log(exp(89))) = 89.0 and eager log(exp(89)) = inf.
4. Confirmed the bundled assertion failed with an AssertionError describing the overflow rewrite discrepancy.

## Observed behavior

- On the local checkout with jax 0.10.2.dev20260717 and jaxlib 0.10.1, `jit(log(exp(89)))` printed 89.0 while eager `log(exp(89))` printed inf, and the bundled assertion failed with an inf location mismatch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
