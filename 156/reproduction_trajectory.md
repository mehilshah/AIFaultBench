# Reproduction Trajectory — Bug 156: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/43072](https://github.com/huggingface/transformers/issues/43072)
- **Repository:** huggingface/transformers @ `a7f2952`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a CUDA segmentation map tensor with `torch.randint_like`.
2. Pass it to `convert_segmentation_map_to_binary_masks` from the local EoMT image processor.
3. The helper calls `np.unique` on the CUDA tensor and raises the NumPy conversion TypeError.

## Observed behavior

- Running `bash run_repro.sh` prints `image_device=cuda:0` and `segmentation_map_device=cuda:0`, then fails in `codebase/src/transformers/models/eomt/image_processing_eomt.py:83` with `TypeError: can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
