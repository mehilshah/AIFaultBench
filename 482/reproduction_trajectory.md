# Reproduction Trajectory — Bug 482: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38125](https://github.com/jax-ml/jax/issues/38125)
- **Repository:** jax-ml/jax @ `cd5f656651c3ef2c9f05fcf3345e147577d81fd8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Python 3.12 virtual environment and installed the runtime dependencies from `requirements.txt`.
2. Pointed `PYTHONPATH` at the local `codebase/` checkout and executed `repro.py`.
3. Observed the `AttributeError: 'TupTy' object has no attribute 'ndim'` traceback from the `jit` batching path.

## Observed behavior

- Running `bash run_repro.sh` in a Python 3.12 venv with the local JAX checkout reproduces the bug. The repro prints `typeof(tup) = Tup{float32[3],float32[3]}` and then fails with `AttributeError: 'TupTy' object has no attribute 'ndim'` from `jax/_src/pjit.py` while evaluating `jax.vmap(jax.jit(lambda x: x), in_axes=TupSpec((0, 0)), out_axes=TupSpec((0, 0)), axis_size=3)(tup)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
