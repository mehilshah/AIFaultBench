# Reproduction Trajectory — Bug 204: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2077](https://github.com/pyro-ppl/numpyro/issues/2077)
- **Repository:** pyro-ppl/numpyro @ `fb14da7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment with the minimal runtime dependencies: editable `codebase/`, `equinox`, `graphviz`, `jax==0.4.38`, and `jaxlib==0.4.38`.
2. Executed the exact Equinox-based model from the bug report in `repro.py`.
3. Observed `numpyro.render_model(..., render_distributions=True, render_params=True)` raise the same JAX TypeError reported in the issue.

## Observed behavior

- Running `bash setup_env.sh && bash run_repro.sh` in this folder reproduces the reported failure. The stderr log shows `numpyro.render_model(...)` failing inside `jax.eval_shape(get_trace)` with `TypeError: Value <function eqx_module.<locals>.<lambda> ...> with type <class 'function'> is not a valid JAX type`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
