# Bug 101

This folder is a self-contained repro bundle for:
`https://github.com/lucidrains/rotary-embedding-torch/issues/8`

Observed failure:
`rotate_queries_and_keys()` with `use_xpos=True` produces non-finite values in `k` for moderate sequence lengths. In this folder, `seq_len=96` is enough to reproduce the issue deterministically with tensors of ones.

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

Usage:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro script exits successfully only when the bug is observed.
