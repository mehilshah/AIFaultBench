# Reproduction Trajectory — Bug 030: DeepLearningExamples

- **Bug report:** [https://github.com/NVIDIA/DeepLearningExamples/issues/1407](https://github.com/NVIDIA/DeepLearningExamples/issues/1407)
- **Repository:** NVIDIA/DeepLearningExamples @ `729963dd47e7c8bd462ad10bfac7a7b0b604e6dd`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- Running ./run_repro.sh with the local venv (torch 2.13.0+cu130, pytorch_lightning 1.7.7, torchmetrics 0.9.3) raises pytorch_lightning.utilities.exceptions.MisconfigurationException in _validate_scheduler_api for CosineAnnealingWarmRestarts.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh > repro_stdout.log 2> repro_stderr.log
```
