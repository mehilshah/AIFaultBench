# Reproduction Trajectory — Bug 481: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2041](https://github.com/pyro-ppl/numpyro/issues/2041)
- **Repository:** pyro-ppl/numpyro @ `7a3c24ff4b072f3f3df6c0ef9494d1635753c53d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Clone or use the provided `codebase/` at commit `7a3c24ff4b072f3f3df6c0ef9494d1635753c53d`.
2. Run `bash setup_env.sh` to create `.venv` and install `jax[cpu]==0.4.25`, `numpy<2`, `typing_extensions`, and the local NumPyro checkout.
3. Run `bash run_repro.sh` to execute `repro.py`.
4. Observe the expected `TypeError` from `WishartCholesky.infer_shapes`.

## Observed behavior

- Running `bash setup_env.sh && bash run_repro.sh` in the pinned NumPyro checkout prints `EXPECTED_EXCEPTION`, `TypeError`, and `Shapes must be 1D sequences of concrete values of integer type, got [4. 5.].` from `WishartCholesky.infer_shapes(concentration, scale_matrix=scale_matrix)` with `concentration = jnp.array([4.0, 5.0])` and `scale_matrix = jnp.array([[[1.0, 0.5], [0.5, 1.0]]])`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
