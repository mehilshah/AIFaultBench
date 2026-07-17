# Bug 123

This folder contains a self-contained repro for Stable-Baselines3 issue 2119.

Reused inputs:
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

Observed result:
- `make_vec_env(..., wrapper_class=gym.wrappers.ClipAction)` returns `Box(-inf, inf, (2,), float32)` instead of preserving the bounded action space.

Primary reproduction command:
`bash run_repro.sh`
