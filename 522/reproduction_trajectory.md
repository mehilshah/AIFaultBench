# Reproduction Trajectory — Bug 522: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21524](https://github.com/Lightning-AI/pytorch-lightning/issues/21524)
- **Repository:** Lightning-AI/pytorch-lightning @ `7d2de87084573e4f75aa83189d0fb43c463120e8`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a CPU-only virtualenv and installed the local source tree as editable `pytorch_lightning`.
2. Ran the import check from repro.py.
3. Verified that the reported `AttributeError` did not occur.

## Observed behavior

- Running ./run_repro.sh in the bundled CPU-only venv completed successfully.
- The repro output was: pytorch_lightning_import=ok version=2.6.1; lightning_fabric_import=ok; lightning_fabric_has_strategies=True.
- A direct check in the same venv also reported `2.6.1` and `True` for `hasattr(lightning.fabric, 'strategies')`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The local source tree does not reproduce the reported circular-import failure. In this folder, `import pytorch_lightning` and `import lightning.fabric` both succeed, and `lightning.fabric.strategies` is already present on the package object.
