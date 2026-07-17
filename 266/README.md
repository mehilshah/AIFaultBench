# Bug 266 Repro Bundle

This folder contains a self-contained reproduction bundle for JAX issue
`https://github.com/jax-ml/jax/issues/39167`.

The reported failure requires a multi-GPU CUDA environment. The repro script
checks for that precondition and then runs the exact TensorFlow-import-first
JAX collective described in the bug report.

Files:
- `bug_report.txt`: source issue report
- `codebase/`: local JAX source checkout used for the repro
- `requirements.txt`: Python dependencies for the bundle
- `setup_env.sh`: creates a virtualenv and installs dependencies
- `run_repro.sh`: runs the repro and writes logs
- `repro.py`: actual reproduction logic
- `manifest.json`: bundle metadata
- `reproduction.json`: structured outcome from this environment
- `repro_stdout.log`, `repro_stderr.log`: captured command output

How to run locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Expected behavior on the original affected setup:
- `import tensorflow` before the JAX collective should trigger
  `XlaRuntimeError` with NCCL `invalid argument`.

Observed behavior in this environment:
- The repro is blocked because there are not two local GPU devices
  available here.
