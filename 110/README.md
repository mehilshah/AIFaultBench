# Bug 110

This folder contains a standalone reproduction bundle for the safetensors
DataLoader pickling bug described in `bug_report.txt`.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Observed result in this environment:
- `timeout 20s .venv/bin/python repro.py` exits with code `124`
- stderr contains `_pickle.PicklingError: Can't pickle <class 'safetensors_rust.SafetensorError'>: import of module 'safetensors_rust' failed`
- the main process does not terminate with the underlying tensor lookup error

Source summary:
- issue URL: `https://github.com/huggingface/safetensors/issues/492`
- inferred library: `safetensors`
- tested library version: `0.4.4`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
