# Reproduction Trajectory — Bug 558: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21477](https://github.com/Lightning-AI/pytorch-lightning/issues/21477)
- **Repository:** Lightning-AI/pytorch-lightning @ `affee2885b1913ca12e4c5dd5c0da82038918c40`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a CPU-only venv and installed the local Lightning source snapshot in editable mode.
2. Ran LightningCLI with a subclass datamodule, trained for one epoch, and saved a checkpoint.
3. Loaded the checkpoint through LightningDataModule.load_from_checkpoint and observed the base class instead of the subclass.

## Observed behavior

- LightningDataModule.load_from_checkpoint returned lightning.pytorch.core.datamodule.LightningDataModule instead of the concrete TestDataSaveHparams subclass. The saved checkpoint contained datamodule_hyper_parameters with _class_path, _instantiator, batch_size, and num_workers.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
