# Reproduction Trajectory — Bug 532: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13722](https://github.com/huggingface/diffusers/issues/13722)
- **Repository:** huggingface/diffusers @ `6382a3db4dd1e129ce8be68649db6fcbae015e8c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment and installed CPU-only torch plus the minimal diffusers runtime dependencies.
2. Ran `bash run_repro.sh` from the standardized bug folder.
3. Observed that `ErnieImageTransformer2DModel.from_single_file(...)` raises AttributeError immediately.

## Observed behavior

- repro_stdout.log contains: has_from_single_file: False
- repro_stderr.log contains: AttributeError: type object 'ErnieImageTransformer2DModel' has no attribute 'from_single_file'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
