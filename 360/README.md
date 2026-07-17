# Bug 360

This folder is a self-contained repro bundle for:
`https://github.com/jax-ml/jax/issues/38813`

What is included:
- `bug_report.txt`
- `codebase/`
- Reproduction artifacts:
  - `repro.py`
  - `requirements.txt`
  - `setup_env.sh`
  - `run_repro.sh`
  - `reproduction.json`
  - `repro_stdout.log`
  - `repro_stderr.log`

Observed result:
- On CPU, `jax.nn.scaled_matmul(...)` raises `NotImplementedError: MLIR translation rule for primitive 'scaled_matmul' not found for platform cpu`.

Usage:
- `bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/jax-ml/jax/issues/38813`
- commit hash: `6a19c8b5ae8986e3aba44cb78b4bb024cd1997b2`
- library: `jax`
- library version reported by the checkout: `0.11.0.dev20260717`
