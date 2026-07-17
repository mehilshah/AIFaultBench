# Reproduction Trajectory — Bug 562: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2463](https://github.com/huggingface/pytorch-image-models/issues/2463)
- **Repository:** huggingface/pytorch-image-models @ `e44f14d7d2f557b9f3add82ee4f1ed2beefbb30d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Instantiate vit_small_patch16_224.augreg_in21k_ft_in1k from the local timm codebase and save a deterministic checkpoint.
2. Find a synthetic RGB image whose top-1 prediction changes between the model-aware preprocessing and the default preprocessing used by onnx_validate.py.
3. Export ONNX from the same checkpoint, verify torch and ONNX agree on the same preprocessed tensor, and run validate.py plus onnx_validate.py to capture the divergent data-config paths.

## Observed behavior

- validate.py resolves the model-aware preprocessing for vit_small_patch16_224.augreg_in21k_ft_in1k from its pretrained_cfg, while onnx_validate.py falls back to generic defaults because it calls resolve_data_config(vars(args)) without model metadata. On the same checkpoint and the same synthetic image, the correct preprocessing predicted class 686 and the default ONNX validation preprocessing predicted class 752; ONNX export matched PyTorch with max abs diff 0.000002.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
