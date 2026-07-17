# Bug 161 Repro Bundle

This directory contains a standalone reproduction harness for the lmdeploy dependency bug reported in issue `#4116`.

## What fails

`codebase/setup.py` derives CUDA runtime dependencies from `nvcc --version`. For CUDA 13, it adds:

- `nvidia-nccl-cu13`
- `nvidia-cuda-runtime-cu13`
- `nvidia-cublas-cu13`
- `nvidia-curand-cu13`

The deprecated package is `nvidia-cublas-cu13`. Installing it fails with:

`⚠️ THIS PROJECT 'nvidia-cublas-cu13' IS DEPRECATED. Please use 'nvidia-cublas' instead.`

## Repro

Run:

```bash
bash run_repro.sh
```

The script writes:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

## Source references

- `codebase/setup.py`
- `codebase/lmdeploy/version.py`
- `bug_report.txt`
