# Bug 522 Repro Bundle

This folder contains a clean repro attempt for:

`https://github.com/Lightning-AI/pytorch-lightning/issues/21524`

What the bundle does:
- creates a CPU-only virtualenv
- installs the local Lightning source tree as `pytorch_lightning`
- checks the import path that the report points at

Result in this folder:
- the reported `AttributeError: partially initialized module 'lightning_fabric' has no attribute 'strategies'` did not reproduce
- `import pytorch_lightning` and `import lightning.fabric` both succeed in the local CPU-only venv

Run order:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro script is intentionally small and reads only from the bundled `codebase/` source tree.
