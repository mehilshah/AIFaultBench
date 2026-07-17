# Reproduction Trajectory — Bug 438: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7812](https://github.com/deepspeedai/DeepSpeed/issues/7812)
- **Repository:** microsoft/DeepSpeed @ `5b2ccad96a2e8f0567f08714a07aa0baca11c7ef`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- Running the repro in a CPU-only venv with torch 2.6.0+cpu and the checked-out DeepSpeed commit 5b2ccad96a2e8f0567f08714a07aa0baca11c7ef prints the expected AssertionError: DeepSpeed lamb optimizer requires dynamic loss scaling.
- After that caught init failure, stderr shows Exception ignored in: <function DeepSpeedEngine.__del__ ...> and AttributeError: 'DeepSpeedEngine' object has no attribute '_deepcompile_active'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
