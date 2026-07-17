# Reproduction Trajectory — Bug 614: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2410](https://github.com/huggingface/pytorch-image-models/issues/2410)
- **Repository:** huggingface/pytorch-image-models @ `c96e9e7ce03e34aa8812e4aa50463e46131793e5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh virtualenv with the CPU PyTorch wheels and the local editable `codebase/` install.
2. Run `bash run_repro.sh`.
3. Observe that the 224x224 forward pass succeeds and the 512x512 forward pass fails with the input-height assertion.

## Observed behavior

- In a clean CPU-only virtualenv, `timm.create_model('swinv2_cr_tiny_224', pretrained=False, features_only=True)` successfully runs on a 224x224 tensor, then raises `AssertionError: Input image height (512) doesn't match model (224).` on a 512x512 tensor.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
