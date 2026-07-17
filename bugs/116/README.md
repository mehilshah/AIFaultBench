# Bug 116

This folder contains a reproducible setup for BayesFlow issue 468.

Observed behavior:
- `MultivariateNormalScore` can produce a covariance whose inverse is non-finite immediately after building a `PointInferenceNetwork`.
- The deterministic repro here uses `seed=0` with the NumPy backend.

Run locally:
```bash
bash run_repro.sh
```

Files in this folder:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:
- issue URL: `https://github.com/bayesflow-org/bayesflow/issues/468`
- library: `bayesflow`
- version: `2.0.3`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
