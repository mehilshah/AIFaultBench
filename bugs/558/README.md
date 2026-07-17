# Bug 558

This folder is a self-contained reproduction bundle for the Lightning bug described in `bug_report.txt`.

Contents:
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

Reproduction summary:
- issue URL: `https://github.com/Lightning-AI/pytorch-lightning/issues/21477`
- observed behavior: `LightningDataModule.load_from_checkpoint` returns the base `LightningDataModule` instead of the concrete datamodule subclass stored in the checkpoint
- local verification: reproducible in this folder with the bundled source snapshot and a CPU-only torch environment

Run:
`bash run_repro.sh`
