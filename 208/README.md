# Bug 208

This folder contains a standalone reproduction for POT issue 738.

Bug summary:
- `ot.wasserstein_circle` with the default `p=1` is not rotationally invariant for the sample from the issue report.
- Translating both input samples by the same `delta` changes the returned distance from `0.095` to `0.09`.

Files in this bundle:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
1. Install dependencies with `bash setup_env.sh`.
2. Reproduce the bug with `bash run_repro.sh`.
3. Inspect `repro_stdout.log` and `repro_stderr.log` for the observed mismatch.

Source metadata:
- issue URL: `https://github.com/PythonOT/POT/issues/738`
- inferred library: `POT`
- inferred library version: local source tree
