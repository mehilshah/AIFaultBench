# Bug 375

This folder is a self-contained repro bundle for the JAX `gammaln` subnormal
regression described in `bug_report.txt`.

Included inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- issue URL: `https://github.com/jax-ml/jax/issues/38634`
- observed in: `jax==0.10.1`, `jaxlib==0.10.1`
- platform: CPU backend
- symptom: `jax.scipy.special.gammaln` returns `inf` for the smallest positive
  `float32` subnormal instead of a large finite value
