# Reproduction Trajectory — Bug 161: lmdeploy

- **Bug report:** [https://github.com/InternLM/lmdeploy/issues/4116](https://github.com/InternLM/lmdeploy/issues/4116)
- **Repository:** InternLM/lmdeploy @ `0da627e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Verified `codebase/setup.py` resolves CUDA 13 to `nvidia-cublas-cu13`.
2. Created an isolated Python virtual environment.
3. Ran `pip install nvidia-cublas-cu13==0.0.1` inside that environment.
4. Captured the deprecation failure emitted by the package build backend.

## Observed behavior

- lmdeploy 0.10.2 hardcodes `nvidia-cublas-cu{CUDAVER}` in setup.py, and installing `nvidia-cublas-cu13==0.0.1` fails with the package's deprecation error.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
