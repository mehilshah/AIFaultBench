# Bug 629

This folder is the reusable standardized benchmark input for the NumPyro tracer-leak bug reported in issue 1999.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

What reproduces:
- `JAX_CHECK_TRACER_LEAKS=1 ./run_repro.sh`
- The run fails in `SVI.run(...)` with a JAX `Leaked trace MainTrace(3,JVPTrace)` error.

Environment used for verification:
- Python 3.12.3
- JAX 0.4.25
- jaxlib 0.4.25
- NumPyro 0.17.0 from `codebase/`
