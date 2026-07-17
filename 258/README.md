# Bug 258

This folder is the self-contained repro bundle for SDV issue 2297.

What is included:
- `bug_report.txt`: the original report
- `codebase/`: the local source tree used for reproduction
- `repro.py`: minimal failing script
- `requirements.txt`: lean runtime dependency set for the repro
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: runs the repro script against the local `codebase/`
- `reproduction.json`: machine-readable reproduction result
- `repro_stdout.log` and `repro_stderr.log`: captured command output

Reproduction command:
`bash run_repro.sh`

Observed behavior:
- `GaussianCopulaSynthesizer.fit()` completes with an empty learned model.
- `get_learned_distributions()` then crashes with `AttributeError: 'NoneType' object has no attribute 'to_dict'`.

The repro uses import stubs for `ctgan`, `deepecho`, and `sdmetrics` because those packages are imported by SDV’s package-level `__init__` but are not needed for this bug path.
