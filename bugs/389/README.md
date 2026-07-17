# Bug 389

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

Reproduction status:
- `jax==0.10.1`
- `jaxlib==0.10.1`
- `numpy==2.4.6`
- `python==3.12.3`
- reproducible: yes

Run the repro:
1. `./run_repro.sh`
2. If you want to prepare the environment separately, run `./setup_env.sh` first and then rerun `./run_repro.sh`.

Direct command after environment setup:
`JAX_PLATFORMS=cpu ./.venv/bin/python repro.py`

Observed output:
`jax: [[nan, nan, nan], [0.35449573397636414, 0.04463260620832443, 1.1511584574463996e-07]]`
The third element is `nan`, but it should be `-inf`.
