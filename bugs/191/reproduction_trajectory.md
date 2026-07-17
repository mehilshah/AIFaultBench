# Reproduction Trajectory — Bug 191: distributed_adam_cuda

- **Bug report:** [https://github.com/NVIDIA/apex/issues/1823](https://github.com/NVIDIA/apex/issues/1823)
- **Repository:** NVIDIA/apex @ `59b80ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` from the standardized bug folder.
2. The script runs `pip install -v --disable-pip-version-check --no-cache-dir --global-option=--cpp_ext --global-option=--cuda_ext .` in `codebase/`.
3. The build backend imports `setup.py` in an isolated environment that does not contain `torch`.

## Observed behavior

- pip install failed during build-isolation with ModuleNotFoundError: No module named 'torch'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
