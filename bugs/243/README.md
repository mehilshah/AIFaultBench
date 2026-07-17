# Bug 243

Reproduction bundle for NumPyro issue `#2029`.

What is included:
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

Repro summary:
- model: one-parameter Poisson likelihood with a uniform prior on `lam`
- samplers: `NUTS`, `AIES`, `ESS`
- comparison metric: lag-1 autocorrelation of flattened posterior draws
- observed pattern: `ESS` autocorrelation is near zero while `NUTS` and `AIES` are much higher

Run:
`bash run_repro.sh`
