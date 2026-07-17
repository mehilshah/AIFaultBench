# Reproduction Trajectory — Bug 303: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7971](https://github.com/deepspeedai/DeepSpeed/issues/7971)
- **Repository:** microsoft/DeepSpeed @ `0ba235294fcbe35f5c42681bd85666dff5c48a93`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Compiled fp_quantizer_warning_repro.cu with nvcc -std=c++17 -arch=sm_80 -c.
2. Observed CUDA compiler warnings matching the bug report: warning #68-D and warning #62-D.

## Observed behavior

- fp_quantizer_warning_repro.cu(12): warning #68-D: integer conversion resulted in a change of sign
- fp_quantizer_warning_repro.cu(25): warning #62-D: shift count is negative

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
