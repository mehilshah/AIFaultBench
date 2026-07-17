# Reproduction Trajectory — Bug 242: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1991](https://github.com/pyro-ppl/numpyro/issues/1991)
- **Repository:** pyro-ppl/numpyro @ `627d19a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtual environment and install the pinned dependencies from `requirements.txt`.
2. Install the local `codebase/` tree into that environment.
3. Run `python repro.py` and observe the `ValueError` during `log_likelihood`.

## Observed behavior

- With jax==0.5.1, jaxlib==0.5.1, flax==0.10.4, and the in-tree numpyro 0.17.0 codebase, `numpyro.infer.util.log_likelihood(model, mcmc.get_samples(), x=x, y=y)` raises `ValueError: First argument passed to an init function should be a jax.PRNGKey or a dictionary mapping strings to jax.PRNGKey` when the model re-enters `random_flax_module`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
