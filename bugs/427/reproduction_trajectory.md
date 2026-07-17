# Reproduction Trajectory — Bug 427: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2593](https://github.com/huggingface/pytorch-image-models/issues/2593)
- **Repository:** huggingface/pytorch-image-models @ `0645384b3a68d0ddf4657400125bb2c68c42bc60`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtual environment and install CPU torch/torchvision plus the repro dependencies.
2. Install the local `codebase/` checkout in editable mode.
3. Create `vit_base_patch16_dinov3.lvd1689m` with `pretrained=False`.
4. Call `set_input_size(512)` and observe the AttributeError from `RotaryEmbeddingDinoV3`.

## Observed behavior

- Using a CPU-only venv with the local timm checkout, `timm.create_model("vit_base_patch16_dinov3.lvd1689m", pretrained=False)` constructs `RotaryEmbeddingDinoV3`, and `model.set_input_size(512)` raises `AttributeError: 'RotaryEmbeddingDinoV3' object has no attribute 'update_feat_shape'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
