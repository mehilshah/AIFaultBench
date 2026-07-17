# Reproduction Trajectory — Bug 616: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2000](https://github.com/pyro-ppl/numpyro/issues/2000)
- **Repository:** pyro-ppl/numpyro @ `3b7d7f071c75c75080a910530bb39f0a4ab6479e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment in .venv
2. Installed pinned JAX CPU, SciPy, pytest, and the local NumPyro codebase
3. Ran the leak-checking MCMC test target from codebase/test/infer/test_mcmc.py
4. Observed a tracer leak while executing `test_chain_inside_jit`

## Observed behavior

- With JAX 0.4.38 / jaxlib 0.4.38 and the local NumPyro 0.17.0 checkout, `JAX_CHECK_TRACER_LEAKS=1 python repro.py` fails in `test_chain_inside_jit` with `Exception: Leaked trace DynamicJaxprTrace`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
