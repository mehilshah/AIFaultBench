# NumPyro scan tracer-leak repro

This bundle reproduces the tracer leak reported in `bug_report.txt` when `scan` is used over discrete latent variables.

The minimal trigger is:

1. Build the local environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh`.
3. `JAX_CHECK_TRACER_LEAKS=1` causes the `infer_discrete(config_enumerate(...))` path to fail inside `numpyro.contrib.control_flow.scan`.

Files:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

