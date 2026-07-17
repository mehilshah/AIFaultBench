# Reproduction Trajectory — Bug 033: DeepLearningExamples

- **Bug report:** [https://github.com/NVIDIA/DeepLearningExamples/issues/1250](https://github.com/NVIDIA/DeepLearningExamples/issues/1250)
- **Repository:** NVIDIA/DeepLearningExamples @ `35d8759cb8cf52f8c7d33900ef27fd0f16d6cff3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed CPU-only PyTorch from the official wheel index.
2. Built a minimal harness that mirrors the `ConvSE3` self-interaction matmul in `se3_transformer/model/layers/convolution.py`.
3. Executed the harness with a degree-1 feature tensor shaped like the reported failing path, which triggers the exact RuntimeError.

## Observed behavior

- Running `bash run_repro.sh` reproduces the reported PyTorch failure and exits non-zero with `RuntimeError: Expected size for first two dimensions of batch2 tensor to be: [8910, 1] but got: [8910, 3].`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
