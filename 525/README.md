# Bug 525

This folder contains a self-contained reproduction of the `torch/imagenet` dataset
construction bug reported in [pytorch-image-models issue 2485](https://github.com/huggingface/pytorch-image-models/issues/2485).

## What fails

`timm.data.dataset_factory.create_dataset('torch/imagenet', root=...)` forwards a
`download` keyword to `torchvision.datasets.ImageNet`, which then forwards it to
`ImageFolder.__init__()`. In the reproduced environment this raises:

`TypeError: ImageFolder.__init__() got an unexpected keyword argument 'download'`

## Files

- `repro.py`: creates a minimal ImageNet-style directory and triggers the failure
- `requirements.txt`: CPU-only dependency pins for the repro
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro script
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log` / `repro_stderr.log`: command output from the latest repro run

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
