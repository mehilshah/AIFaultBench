# Reproduction Trajectory — Bug 520: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38101](https://github.com/jax-ml/jax/issues/38101)
- **Repository:** jax-ml/jax @ `eb93eda9fbe95cf21c1501db8b064f66b040bf33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run bash setup_env.sh to create .venv and install numpy, scipy, ml_dtypes, opt_einsum, jaxlib, and the local codebase in editable mode.
2. Run bash run_repro.sh.
3. Observe that the JIT-compiled vmapped path returns 3.4028235e+38 while the eager vmapped path returns inf, causing AssertionError.

## Observed behavior

- With the local codebase and a CPU runtime using jaxlib 0.10.1, the reproducer prints jit(vmap(f))(x): [3.4028235e+38] and vmap(f)(x): [inf], then fails the allclose assertion.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh > repro_stdout.log 2> repro_stderr.log || true
```
