# Bug 168

This folder contains a standalone reproduction bundle for Kornia issue 3194.

Inputs reused from the benchmark source:
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

How to run:
- `bash setup_env.sh`
- `bash run_repro.sh`

Observed behavior in this snapshot:
- `RandomCrop` does not keep frames identical within each video.
- `RandomHorizontalFlip` keeps frames identical within each video, but still applies the same transform across the batch.
- The combined pipeline reproduces the same batch-level failure.
