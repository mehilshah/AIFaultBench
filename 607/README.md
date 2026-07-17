# Bug 607

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

Reproduction summary:
- issue URL: `https://github.com/jax-ml/jax/issues/37993`
- library: `jax`
- observed result: `np.std(x) -> nan`, `jnp.std(jnp.array(x)) -> inf`
- status: reproducible in this checkout

Run:
`bash run_repro.sh`
