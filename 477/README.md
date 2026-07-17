# Bug 477

This folder contains a standalone reproduction bundle for the JAX type-stub bug in issue `#38188`.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Observed result:
- `pyrefly` reports `missing-attribute` for `jnp.zeros(3).platform()`
- the local checkout matches the bug report because `jax/_src/basearray.pyi` declares `devices()` but not `platform()`
- the harness uses `pyrefly snippet` because file-based checking was permissive in this environment
