# Bug 624

This folder reproduces the CLI validation gap reported in:
`https://github.com/huggingface/accelerate/issues/903`

What the repro checks:
- `accelerate launch --multi_gpu ... --num_processes 1 --num_machines 1` is accepted.
- The launch path dispatches to `multi_gpu_launcher` instead of rejecting the invalid combination up front.

Files in this folder:
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

Reproduction command:
`bash run_repro.sh`

Notes:
- The harness stubs `torch` and `psutil` so the repro stays isolated from the broken system torch install in this environment.
- The actual `accelerate` launch code is loaded from `codebase/src/accelerate/commands/launch.py`.
