# Bug 204

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction flow:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro script uses the Equinox-based model from `bug_report.txt` and checks the `render_model` path in `numpyro.infer.inspect`.

Source summary:
- issue URL: `https://github.com/pyro-ppl/numpyro/issues/2077`
- commit hash: `not found in Dataset.csv`
- inferred library: `numpyro`
- inferred library version: `0.19.0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
