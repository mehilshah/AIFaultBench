# Reproduction Trajectory — Bug 240: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1753](https://github.com/pyro-ppl/numpyro/issues/1753)
- **Repository:** pyro-ppl/numpyro @ `f997da2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtualenv and install `jax==0.4.38`, `jaxlib==0.4.38`, and the editable `codebase/` checkout.
2. Run `bash run_repro.sh` from the standardized bug folder.
3. Confirm `baseline_init_ok` in stdout and an `UnexpectedTracerError` traceback in stderr.

## Observed behavior

- The baseline `SVI.init` path under `jax.vmap` completes, then the model with `numpyro.deterministic("test", a)` fails with `jax.errors.UnexpectedTracerError`. The traceback shows the tracer leak originates from `numpyro.handlers.seed.process_message` during `random.split(self.rng_key)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
