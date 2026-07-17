# Bug 030 Reproduction

This bundle reproduces the Lightning scheduler failure reported for nnUNet in
NVIDIA/DeepLearningExamples issue 1407.

Observed failure:

```text
MisconfigurationException: The provided lr scheduler `CosineAnnealingWarmRestarts`
doesn't follow PyTorch's LRScheduler API.
```

Root cause in the codebase:

- `codebase/PyTorch/Segmentation/nnUNet/nnunet/nn_unet.py`
- `configure_optimizers()` returns `{"optimizer": ..., "monitor": "val_loss", "lr_scheduler": scheduler}`
- The scheduler is `torch.optim.lr_scheduler.CosineAnnealingWarmRestarts`

Files in this bundle:

- `repro.py`
- `pkg_resources.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`

Reproduction:

```bash
bash setup_env.sh
bash run_repro.sh
```

The reproducible command used for validation was:

```bash
./run_repro.sh > repro_stdout.log 2> repro_stderr.log
```

Result:

- reproducible: yes
- failure occurs before training begins, during Lightning optimizer/scheduler validation
