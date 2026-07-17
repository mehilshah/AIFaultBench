# Bug 213 Reproduction Bundle

This folder reproduces SDV issue [#2366](https://github.com/sdv-dev/SDV/issues/2366):
conditional sampling on an unfitted single-table synthesizer returns a misleading sampling error
instead of a proactive `SamplingError` about fitting first.

Files:
- `repro.py`: executes the reporter's snippet and prints the exception chain.
- `requirements.txt`: installs the local `codebase/` in editable mode.
- `setup_env.sh`: installs the reproduction environment.
- `run_repro.sh`: runs the repro script.
- `reproduction.json`: structured result written after verification.
- `repro_stdout.log`, `repro_stderr.log`: captured command output.

Usage:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The local source snapshot is in `codebase/` and is not mutated by the repro bundle.
