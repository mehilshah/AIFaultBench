# Bug 298

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:
- issue URL: `https://github.com/jax-ml/jax/issues/39109`
- commit hash: `5279767b48b562d0a26428b4b43b5383dfa895f3`
- library: `jax`
- source tree version observed locally: `0.11.0.dev20260717`
- bug report source: `bug_report.txt`

Observed result in this checkout:
- `jax.numpy.heaviside([nan, 0.0, -1.0], [1.0, 1.0, 1.0])` prints `['nan', '1.0', '0.0']`
- that matches NumPy, so the reported bug is not reproducible in this tree.
