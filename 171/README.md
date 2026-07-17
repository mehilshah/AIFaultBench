# Bug 171

This folder contains a self-contained repro for Kornia issue 996.

Observed behavior in this snapshot:
- `projections_from_fundamental(torch.randn(1, 3, 3))` succeeds
- `projections_from_fundamental(torch.randn(1, 1, 3, 3))` fails with `AssertionError: torch.Size([1, 1, 3])`
- `projections_from_fundamental(torch.randn(3, 3))` fails with `AssertionError: torch.Size([3])`

Relevant files:
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

Run:
`bash run_repro.sh`

If you need a clean environment:
`bash setup_env.sh`

The setup script creates `.venv/` in this folder and installs the editable local `codebase/`
copy there so `run_repro.sh` can reuse it.

Source summary:
- issue URL: `https://github.com/kornia/kornia/issues/996`
- inferred library: `kornia`
- inferred library version: `0.5.2rc1`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
