# Reproduction Trajectory — Bug 409: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7835](https://github.com/deepspeedai/DeepSpeed/issues/7835)
- **Repository:** microsoft/DeepSpeed @ `a44fb58f134afc5399b29c154a5502e14272774c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Use the local codebase/ snapshot that reproduces the DeepSpeed import chain leading to sharded_moe.py.
2. Run bash setup_env.sh to create a local .deps directory and install torch==2.10.0.
3. Run bash run_repro.sh to execute repro.py with DeprecationWarning promoted to an error.
4. Inspect repro_stdout.log and repro_stderr.log for the import-time warning traceback.

## Observed behavior

- With torch==2.10.0 installed in a clean local dependency directory, importing DeepSpeedEngine from the local codebase snapshot raises DeprecationWarning as an exception. The failure occurs while importing src_codebase/deepspeed/moe/sharded_moe.py at the @torch.jit.script decorator on line 4.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
