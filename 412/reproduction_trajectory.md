# Reproduction Trajectory — Bug 412: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2594](https://github.com/huggingface/pytorch-image-models/issues/2594)
- **Repository:** huggingface/pytorch-image-models @ `1ec391520aeebe580b0340fcb795cda30d08ef70`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Trace a minimal module that calls timm.layers.pos_embed_sincos.apply_rot_embed_cat(), which uses tensor_split().
2. Run coremltools.convert(..., convert_to='mlprogram') on the traced module.
3. Observe the conversion stop in coremltools with the tensor_split NotImplementedError.

## Observed behavior

- Core ML Tools 9.0 fails while converting the traced DINOv3 helper path with NotImplementedError: PyTorch convert function for op 'tensor_split' not implemented.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
