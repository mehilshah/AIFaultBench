# Bug 233

This folder is the reusable standardized benchmark input for Equinox issue 1089.

Observed behavior:
- `Problematic.__hash__` hashes the raw field values.
- A `dict` field makes the module unhashable.
- `jax.jit(..., static_argnames="static")` fails with `Non-hashable static arguments are not supported`.

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/patrick-kidger/equinox/issues/1089`
- library: `equinox`
- version: `0.13.0`
- report source: `bug_report.txt`
- codebase source: `codebase`
