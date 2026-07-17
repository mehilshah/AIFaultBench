# Bug 632

This folder contains a self-contained reproduction bundle for the reported
`NeighborLoader` failure.

Inputs reused from the benchmark:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

The reproduced failure is:
`ImportError: 'NeighborSampler' requires either 'pyg-lib' or 'torch-sparse'`

The local bundle uses a minimal homogeneous graph and the current checkout of
`torch-geometric` to exercise the same sampling path as the issue report.
