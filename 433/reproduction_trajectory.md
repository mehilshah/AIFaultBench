# Reproduction Trajectory — Bug 433: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38529](https://github.com/jax-ml/jax/issues/38529)
- **Repository:** jax-ml/jax @ `e2f2e9e21d6723efc4c4e16e5e070dbc7e76a676`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtual environment and installed jax==0.9.0.1 with its dependencies.
2. Saved jax.ShapeDtypeStruct((10, 10), jnp.float16) with numpy.save.
3. Loaded the file with jnp.load(..., allow_pickle=True) and observed a 0-d object ndarray wrapper.
4. Confirmed that ndarray.item() returns the underlying ShapeDtypeStruct.

## Observed behavior

- On jax 0.9.0.1, saving a ShapeDtypeStruct with numpy.save and loading it with jnp.load(..., allow_pickle=True) returns a 0-d numpy.ndarray of dtype object instead of a direct ShapeDtypeStruct. The repro output shows loaded_type=ndarray, loaded_shape=(), loaded_dtype=dtype('O'), loaded_repr=array(ShapeDtypeStruct(shape=(10, 10), dtype=float16), dtype=object), and y.item() is the original ShapeDtypeStruct.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
