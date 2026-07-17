# Bug 023

This folder contains a standalone reproduction bundle for TensorFlow Models issue
10972.

Observed result in this environment:
- The notebook import cell in `codebase/docs/vision/object_detection.ipynb`
  completed successfully after installing the package set used by the notebook.
- I did not observe the reported import failure here.

Files in this folder:
- `bug_report.txt`: original issue report
- `codebase/`: local source snapshot used for inspection
- `repro.py`: script that mirrors the notebook import cell
- `requirements.txt`: direct runtime dependencies for the repro
- `setup_env.sh`: installs dependencies into `.deps`
- `run_repro.sh`: runs the repro script with `.deps` on `PYTHONPATH`
- `reproduction.json`: schema-constrained summary of the outcome
- `repro_stdout.log` / `repro_stderr.log`: captured run output

To rerun locally:
`bash setup_env.sh && bash run_repro.sh`
