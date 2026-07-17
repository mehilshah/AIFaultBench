# Bug 523

This folder contains a self-contained repro bundle for:
`https://github.com/huggingface/accelerate/issues/1174`

Observed behavior in this snapshot:
`Accelerator(cpu=True).prepare(optimizer)` raises the reported `AssertionError`.

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run locally:
1. `./setup_env.sh`
2. `./run_repro.sh`

The repro uses the local `codebase/` source tree and pins a CPU-only torch build plus a setuptools version that still provides `pkg_resources`.
