# Bug 195

This folder contains a standalone repro for the jaxtyping issue described in `bug_report.txt`.

Files of interest:
- `repro.py`: minimal script that triggers the bug
- `requirements.txt`: dependencies needed to run the repro
- `setup_env.sh`: creates a local venv and installs dependencies
- `run_repro.sh`: runs the repro and captures logs
- `reproduction.json`: schema-constrained result for this folder
- `repro_stdout.log` and `repro_stderr.log`: captured run output

Reproduction:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

Expected behavior here:
- direct `@beartype` usage on the function with a symbolic return axis raises `jaxtyping.AnnotationError`
- the message points at the symbolic axis expression `dim+1`

Source summary:
- issue URL: `https://github.com/patrick-kidger/jaxtyping/issues/231`
- inferred library: `jaxtyping`
- inferred library version: `0.2.33`
