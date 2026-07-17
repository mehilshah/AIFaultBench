# Reproduction Trajectory — Bug 642: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1998](https://github.com/pyro-ppl/numpyro/issues/1998)
- **Repository:** pyro-ppl/numpyro @ `3b7d7f071c75c75080a910530bb39f0a4ab6479e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local Python 3.12 virtual environment.
2. Install the pinned JAX/funsor/scipy/tqdm dependencies and the local `codebase/` package in editable mode.
3. Run `bash run_repro.sh`, which executes `repro.py` with `JAX_CHECK_TRACER_LEAKS=1`.
4. Observe the tracer-leak exception from `numpyro.contrib.control_flow.scan`.

## Observed behavior

- Running `bash run_repro.sh` in the prepared Python 3.12 venv fails with `Exception: Leaked trace DynamicJaxprTrace` while tracing `body_fn` in `numpyro/contrib/control_flow/scan.py`.
- The leaked tracer is an `int32[10]` discrete `states` value retained through `AdjointTape._eager_to_lazy` during `infer_discrete(config_enumerate(hmm))`.
- The same failure is visible in the earlier targeted pytest run as `test_scan_hmm_smoke[0-2]` and `test_scan_hmm_smoke[1-2]` under `JAX_CHECK_TRACER_LEAKS=1`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
