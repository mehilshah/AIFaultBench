# Bug 529 Reproduction Bundle

This folder contains a self-contained reproduction attempt for
https://github.com/pyg-team/pytorch_geometric/issues/9974.

What is included:
- `repro.py`: a minimal distributed graph-classification harness based on the
  model from the issue report.
- `setup_env.sh`: creates a local virtual environment and installs the runtime
  dependencies.
- `run_repro.sh`: runs the repro and captures stdout/stderr.
- `requirements.txt`: Python dependencies for the repro environment.
- `manifest.json`: machine-readable metadata for the bundle.
- `reproduction.json`: final result describing whether the bug reproduced
  here.
- `repro_stdout.log` and `repro_stderr.log`: command output from the last run.

Notes:
- The reported failure was a GPU/distributed segfault on PyG 2.5.3 + PyTorch
  2.3.1.
- This workspace does not expose the reported CUDA/NCCL environment, so the
  repro script falls back to CPU/gloo when GPUs are unavailable.
- The script still exercises the same layer stack and distributed training
  pattern from the report.
- In this workspace, the CPU fallback completed successfully and did not
  trigger a segfault.
