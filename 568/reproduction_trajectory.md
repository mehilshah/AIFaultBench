# Reproduction Trajectory — Bug 568: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38097](https://github.com/jax-ml/jax/issues/38097)
- **Repository:** jax-ml/jax @ `eb93eda9fbe95cf21c1501db8b064f66b040bf33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv and installed the runtime dependencies from requirements.txt.
2. Ran repro.py against the local codebase snapshot with JAX constrained to CPU execution.
3. Observed the reported mismatch between jitted and eager gradients for log(exp(x)) at x=89.0 and x=88.0.

## Observed behavior

- Running the bundled JAX repro on this snapshot prints x=89 jit: [1.] eager: [nan] and x=88 jit: [1.] eager: [0.], matching the bug report's gradient mismatch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
