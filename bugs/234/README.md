# Bug 234

This folder contains a standalone reproduction bundle for the Equinox `error_if`
call-order bug described in `bug_report.txt`.

Observed behavior in this checkout:
- first call with a non-error input succeeds
- second call with an error input raises `ValueError`
- expected type is `EquinoxRuntimeError`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Suggested local workflow:
1. `./setup_env.sh`
2. `./run_repro.sh`

Source summary:
- issue URL: `https://github.com/patrick-kidger/equinox/issues/1156`
- inferred library: `equinox`
- inferred library version: `0.13.2`
- runtime used for reproduction: `jax==0.8.2`
