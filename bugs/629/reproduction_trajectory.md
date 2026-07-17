# Reproduction Trajectory — Bug 629: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1999](https://github.com/pyro-ppl/numpyro/issues/1999)
- **Repository:** pyro-ppl/numpyro @ `3b7d7f071c75c75080a910530bb39f0a4ab6479e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and populate the isolated environment with ./setup_env.sh.
2. Run the minimal reproduction with JAX_CHECK_TRACER_LEAKS=1 ./run_repro.sh.
3. Observe the JAX leaked-trace exception during the first SVI update.

## Observed behavior

- JAX_CHECK_TRACER_LEAKS=1 ./run_repro.sh exits with status 1 and raises Exception: Leaked trace MainTrace(3,JVPTrace) from SVI.run(...), with the leaked tracer retained through mutable_state["loc1p"]["value"].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
JAX_CHECK_TRACER_LEAKS=1 ./run_repro.sh
```
