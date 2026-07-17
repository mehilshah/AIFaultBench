# Bug 616

Reproduction bundle for NumPyro issue 2000, "Running mcmc within jit might cause tracer leak".

## What this reproduces

`test_chain_inside_jit` from `codebase/test/infer/test_mcmc.py` fails under `JAX_CHECK_TRACER_LEAKS=1` with:

`Exception: Leaked trace DynamicJaxprTrace`

## Environment

- NumPyro: `0.17.0` from the local `codebase/`
- JAX: `0.4.38`
- jaxlib: `0.4.38`

## How to run

```bash
./run_repro.sh
```

The run writes stdout to `repro_stdout.log` and stderr to `repro_stderr.log`.

