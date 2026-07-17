# Bug 404

Reproduction bundle for `jax.scipy.stats.poisson.cdf(k=inf, mu>0)` returning
`nan` instead of `1.0`.

Source inputs:
- `bug_report.txt`
- `codebase/` at commit `4250605d1e353e8f3e5f943abc485d5bbe1fb250`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
`bash run_repro.sh`

Observed result:
- `k = +inf`, `mu > 0` reproduces the mismatch
- SciPy returns `1.0`
- JAX returns `nan`
