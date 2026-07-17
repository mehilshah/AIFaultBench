# Reproduction Trajectory — Bug 525: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2485](https://github.com/huggingface/pytorch-image-models/issues/2485)
- **Repository:** huggingface/pytorch-image-models @ `d1140c1a0f21cab390f01b32768745f56ac0e87a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a temporary ImageNet-like root with `val/n00000000/0.jpg` and a compatible `meta.bin`.
2. Import `create_dataset` from `timm.data.dataset_factory`.
3. Call `create_dataset('torch/imagenet', root=<temp root>)` and observe the TypeError from `ImageFolder.__init__()`.

## Observed behavior

- With a minimal ImageNet-style root containing `val/` and `meta.bin`, `create_dataset('torch/imagenet', root=...)` fails in `torchvision/datasets/imagenet.py:56` with `TypeError: ImageFolder.__init__() got an unexpected keyword argument 'download'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
