# Reproduction Trajectory — Bug 640: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2392](https://github.com/huggingface/pytorch-image-models/issues/2392)
- **Repository:** huggingface/pytorch-image-models @ `131518c15cef20aa6cfe3c6831af3a1d0637e3d1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python virtual environment and installed the CPU torch/torchvision stack plus Pillow and NumPy.
2. Installed the local `codebase/` as an editable package so the repro uses the bundled timm sources.
3. Ran `bash run_repro.sh` to apply `create_transform(..., is_training=False, crop_pct=1.0)` to a synthetic non-square image with a left-edge "A" feature.
4. Compared the transform output with a direct resize and confirmed the feature disappeared in the timm transform output.

## Observed behavior

- Running `bash run_repro.sh` in a clean venv with `torch==2.5.1+cpu` and `torchvision==0.20.1+cpu` reproduced the issue. The synthetic wide image kept 1842 dark pixels in the left 60 columns after a plain resize, but `create_transform(input_size=224, is_training=False, crop_pct=1.0, normalize=False)` reduced that to 0 dark pixels, showing the edge feature was center-cropped away.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
