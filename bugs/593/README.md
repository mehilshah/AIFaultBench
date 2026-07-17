# Bug 593

This folder contains a self-contained repro bundle for
https://github.com/pyg-team/pytorch_geometric/issues/9897.

What was checked:
- `bug_report.txt`
- local `codebase/`
- a clean virtualenv with `torch-geometric==2.6.1`

Outcome:
- `from torch_geometric.data.data import BaseData` succeeds in a clean environment here.
- The reported `ImportError` is not reproducible on this Linux/Python 3.12 host.
- The issue appears environment-specific, likely tied to the reported Windows/Anaconda setup or a transient import-cache state.

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Notes:
- The local codebase snapshot is `2.7.0`, while the bug report references `2.6.1`.
- The compatibility pin in `requirements.txt` uses a Python 3.12-compatible PyTorch build so the import probe can run in this environment.
