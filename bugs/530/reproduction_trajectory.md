# Reproduction Trajectory — Bug 530: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38100](https://github.com/jax-ml/jax/issues/38100)
- **Repository:** jax-ml/jax @ `eb93eda9fbe95cf21c1501db8b064f66b040bf33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python 3.12 virtual environment and installed the pinned requirements.
2. Ran the minimal `jax.jit(lambda x: jnp.log2(jnp.exp2(x)))` reproducer on `float32` inputs 128.0 and 13.0.
3. Observed the JIT path return the input value while eager evaluation returned `inf` for 128.0 and the rounded float32 value for 13.0.

## Observed behavior

- In a fresh venv with jax 0.10.2 and jaxlib 0.10.1, `x=128.0` printed `jit=128.0 eager=inf`, and `x=13.0` printed `jit=13.0 eager=13.000000953674316`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
