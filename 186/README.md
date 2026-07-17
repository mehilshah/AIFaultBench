# Bug 186

This folder is a self-contained reproduction bundle for the Marimo `--base-url` LSP websocket bug.

What reproduces:
- `GET`/upgrade-style requests to `/my/custom/path/lsp/pylsp` are rejected.
- Requests to `/lsp/pylsp` succeed.
- That shows the LSP websocket is mounted at the root path instead of under the configured base URL.

How to run:
- `bash setup_env.sh`
- `bash run_repro.sh`

Captured output:
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`

Source inputs:
- `bug_report.txt`
- `codebase/`
