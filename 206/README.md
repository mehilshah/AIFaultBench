# Bug 206

This folder is the reusable standardized benchmark input for POT issue 691.

Reused sources:
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

Reproduction summary:
- `POT==0.9.4` returns `[[0.51122814, 0.18807032], [0.18807032, 0.51122814]]`
- `POT==0.9.5` returns `[[0.32205361, 0.11847690], [0.11847690, 0.32205361]]`
- the local checkout matches the `0.9.5` result

Run:
`bash run_repro.sh`

Source metadata:
- issue URL: `https://github.com/PythonOT/POT/issues/691`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
