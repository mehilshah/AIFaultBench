# Reproduction Trajectory — Bug 309: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2161](https://github.com/pyro-ppl/numpyro/issues/2161)
- **Repository:** pyro-ppl/numpyro @ `0fcf1218c27e7f562cc1f1bae8d9d3c1f9c7d52e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the pinned CPU JAX and Flax dependencies together with the local editable NumPyro checkout.
2. Run the control MCMC case with NNX parameters but no mutable state.
3. Run the mutable-state MCMC case with `numpyro.deterministic`, which raises `Leaked trace DynamicJaxprTrace`.

## Observed behavior

- Control case without mutable state completed successfully; the mutable-state case with deterministic output failed with a JAX tracer leak during NUTS sampling.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
