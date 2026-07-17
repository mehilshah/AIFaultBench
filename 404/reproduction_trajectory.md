# Reproduction Trajectory — Bug 404: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38622](https://github.com/jax-ml/jax/issues/38622)
- **Repository:** jax-ml/jax @ `4250605d1e353e8f3e5f943abc485d5bbe1fb250`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create a venv and install the local JAX checkout plus dependencies.
2. Run `bash run_repro.sh` to execute the boundary-case reproducer.
3. Confirm that the `k=+inf, mu>0` case prints `scipy: 1.0` and `jax/jit: nan`.

## Observed behavior

- On the local JAX checkout, `jax.scipy.stats.poisson.cdf(np.float32(np.inf), np.float32(1.0), np.float32(0.0))` returns `nan` both eagerly and under `jax.jit`, while `scipy.stats.poisson.cdf(...)` returns `1.0`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
