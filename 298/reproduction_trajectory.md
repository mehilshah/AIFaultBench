# Reproduction Trajectory — Bug 298: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/39109](https://github.com/jax-ml/jax/issues/39109)
- **Repository:** jax-ml/jax @ `5279767b48b562d0a26428b4b43b5383dfa895f3`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a virtual environment and installed the local checkout with `./setup_env.sh`.
2. Ran the standardized repro entrypoint with `./run_repro.sh`.
3. Confirmed the observed JAX output matched NumPy for the reported NaN input.

## Observed behavior

- Running ./run_repro.sh in a fresh venv from this checkout printed `jax: [nan, 1.0, 0.0]` and `expected: [nan, 1.0, 0.0]`, then exited with code 1. The current source tree already matches NumPy for the NaN case.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The checked-out JAX source already contains the NaN-handling behavior fix for `jax.numpy.heaviside`, so the reported bug does not reproduce in this folder.
