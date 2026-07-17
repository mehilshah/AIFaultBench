# Reproduction Trajectory — Bug 537: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2481](https://github.com/huggingface/pytorch-image-models/issues/2481)
- **Repository:** huggingface/pytorch-image-models @ `91e6e1737efd8788c3199a93ca95016cf69918b0`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Install the local CPU-only PyTorch/torchvision environment.
2. Import the local `codebase/` copy of timm and instantiate `resnet34` with `num_classes=100`.
3. Run a random 32x32 forward pass to confirm the model path works.

## Observed behavior

- timm version: 1.0.15 | model type: ResNet | conv1 kernel/stride/padding: (7, 7)/(2, 2)/(3, 3) | maxpool present: MaxPool2d | classifier out_features: 100 | forward output shape: (2, 100)

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported symptom is an end-to-end CIFAR-100 accuracy gap after 200 epochs, which is not deterministically reproducible from the repository alone here. The local smoke test shows `timm.create_model('resnet34')` builds and runs, and the source documents `resnet34` as the standard torchvision-style 7x7-stem ResNet, not a CIFAR-specific variant.
