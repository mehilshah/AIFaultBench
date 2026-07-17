# Bug 066

This folder contains a self-contained repro bundle for the MIRNet typo reported in keras-io issue #1160.

Inputs reused from the benchmark snapshot:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Summary:
- The final SKFF call in `codebase/examples/vision/mirnet.py` uses `level3_dau_2` twice.
- `level2_dau_2` is assigned but never consumed by that call.
