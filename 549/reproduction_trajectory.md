# Reproduction Trajectory — Bug 549: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2472](https://github.com/huggingface/pytorch-image-models/issues/2472)
- **Repository:** huggingface/pytorch-image-models @ `ea728f67fa26779f65e1cb9738ece458dbc86a42`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv and installed the pinned repro dependencies from requirements.txt.
2. Ran `bash run_repro.sh` with `PYTHONPATH` pointing at the checked-in `codebase/`.
3. Observed the AttributeError raised from `timm.utils.onnx.onnx_export` when it calls `torch.onnx._export`.

## Observed behavior

- Running `bash run_repro.sh` in a Python 3.12 virtualenv with torch==2.6.0, torchvision==0.21.0, and onnx==1.17.0 printed `has_torch_onnx__export=False` and failed inside `codebase/timm/utils/onnx.py` at `torch.onnx._export` with `AttributeError: module 'torch.onnx' has no attribute '_export'. Did you mean: 'export'?`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
