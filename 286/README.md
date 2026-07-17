# Bug 286

This folder contains a minimal reproduction bundle for Accelerate issue
`https://github.com/huggingface/accelerate/issues/3502`.

What is included:
- `bug_report.txt`: recovered issue report
- `codebase/`: local Accelerate source snapshot
- `repro.py`: minimal `Accelerator.prepare()` reproducer
- `requirements.txt`: runtime Python dependencies
- `setup_env.sh`: creates an isolated venv and installs deps
- `run_repro.sh`: runs the 4-GPU attempt when hardware is available, otherwise runs a smoke test
- `reproduction.json`: machine-readable result
- `repro_stdout.log` / `repro_stderr.log`: captured command output

Current outcome in this environment:
- The local single-process smoke test completes.
- The reported 4-GPU hang is not reproducible here because only one CUDA device is available.

To rerun locally:
`bash setup_env.sh && bash run_repro.sh`
