# Reproduction Trajectory — Bug 031: DeepLearningExamples

- **Bug report:** [https://github.com/NVIDIA/DeepLearningExamples/issues/1268](https://github.com/NVIDIA/DeepLearningExamples/issues/1268)
- **Repository:** NVIDIA/DeepLearningExamples @ `acecffe16f0358cc7247893cca00707d63e527e1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv and installed `torch==2.5.1` from the PyTorch CPU wheel index.
2. Generated a synthetic checkpoint by renaming the current model's `layers.*` keys to the legacy `layer1.*` layout.
3. Called `resnet50(pretrained_from_file=...)` through the real loader in `codebase/PyTorch/Classification/ConvNets`.

## Observed behavior

- Running `bash run_repro.sh` after environment setup exits with code 1 and prints `EXPECTED_RUNTIME_ERROR` plus `Error(s) in loading state_dict for ResNet` with missing `layers.0.0.conv1.weight` and unexpected `layer1.0.conv1.weight` keys.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
