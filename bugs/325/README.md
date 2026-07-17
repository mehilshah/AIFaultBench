# Bug 325

This folder contains a self-contained reproduction bundle for the NumPyro warning regression described in `bug_report.txt`.

What reproduces:
- `numpyro.distributions.Dirichlet.sample` emits a `DeprecationWarning` from `ml_dtypes/_finfo.py`
- `numpyro.distributions.Beta.sample` hits the same path through its internal `Dirichlet` sampler

How to run locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source inputs:
- issue URL: `https://github.com/pyro-ppl/numpyro/issues/2146`
- bug report: `bug_report.txt`
- local codebase: `codebase/`
