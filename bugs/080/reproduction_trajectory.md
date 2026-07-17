# Reproduction Trajectory — Bug 080: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/311](https://github.com/lucidrains/vit-pytorch/issues/311)
- **Repository:** lucidrains/vit-pytorch @ `90be7233a3f55c29692a72da6ee4dcb5aab267d4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Built synthetic left/right classification images and applied the same train/val transform split as the notebook.
2. Trained the local vit_for_small_dataset ViT for three epochs with the notebook-style metric accounting.
3. Observed validation accuracy higher than the averaged training accuracy, while a clean train evaluation confirmed the model learned the task.

## Observed behavior

- The notebook-style training metric lags the end-of-epoch validation metric. On the synthetic reproduction, validation stayed above training while a clean train-set pass reached 1.0, showing the gap comes from the measurement setup rather than a failure in the ViT forward pass.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
