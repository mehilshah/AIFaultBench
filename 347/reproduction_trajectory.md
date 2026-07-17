# Reproduction Trajectory — Bug 347: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14063](https://github.com/huggingface/diffusers/issues/14063)
- **Repository:** huggingface/diffusers @ `21ba39457d0b9b72dc59ef8aec7981c947c59f6b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtual environment with bash setup_env.sh.
2. Run bash run_repro.sh to execute the deterministic device-mismatch harness.
3. Inspect repro_stdout.log and repro_stderr.log for the source-line confirmation and RuntimeError traceback.

## Observed behavior

- The repro script hit the same device-mismatch failure mode at the Kandinsky5 I2I concat site in codebase/src/diffusers/pipelines/kandinsky5/pipeline_kandinsky_i2i.py:547. Captured stderr shows: RuntimeError: Tensor on device meta is not on the expected device cpu!

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
