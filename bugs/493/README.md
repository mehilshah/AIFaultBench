# Bug 493 Reproduction Bundle

This folder reproduces the Pyro infinite-loop bug reported in
`https://github.com/pyro-ppl/pyro/issues/3156`.

What is included:
- `bug_report.txt`: upstream issue description.
- `codebase/`: local Pyro snapshot used for the repro.
- `repro.py`: minimal trigger script.
- `requirements.txt`: isolated runtime dependencies.
- `setup_env.sh`: creates a local virtualenv and installs dependencies.
- `run_repro.sh`: runs the repro under a timeout and captures logs.
- `manifest.json`: metadata for the standardized bundle.
- `reproduction.json`: machine-readable result after running the repro.
- `repro_stdout.log` / `repro_stderr.log`: captured command output.

Repro summary:
- `repro.py` patches `torch.__version__` to satisfy the older Pyro snapshot.
- It constructs an `HMC` instance whose potential returns `NaN`.
- `HMC._find_reasonable_step_size()` then never exits because the loop keeps
  taking the same branch even after the step size collapses to zero.

Usage:
```bash
bash setup_env.sh
bash run_repro.sh
```
