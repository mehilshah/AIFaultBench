# Reproduction Trajectory — Bug 029: pytorch/examples

- **Bug report:** [https://github.com/pytorch/examples/issues/1134](https://github.com/pytorch/examples/issues/1134)
- **Repository:** pytorch/examples @ `54f4572509891883a947411fd7239237dd2a39c3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python environment and installed `torch==2.5.1` and `torchvision==0.20.1`.
2. Ran `python repro.py` via `bash run_repro.sh` with `--dummy` against `codebase/imagenet/main.py`.
3. Removed `torch.backends.mps` at runtime to emulate the unsupported backend path described in the bug report, then observed the same AttributeError.

## Observed behavior

- Running `bash run_repro.sh` printed `=> creating model 'resnet18'` and then failed with `AttributeError: module 'torch.backends' has no attribute 'mps'`.
- The traceback points to `codebase/imagenet/main.py:171` at `elif torch.backends.mps.is_available():`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
