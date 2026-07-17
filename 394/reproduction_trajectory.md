# Reproduction Trajectory — Bug 394: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7837](https://github.com/deepspeedai/DeepSpeed/issues/7837)
- **Repository:** microsoft/DeepSpeed @ `a44fb58f134afc5399b29c154a5502e14272774c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Installed the pinned DeepSpeed checkout from `codebase/` into a local virtualenv with ops disabled.
2. Ran `bash run_repro.sh`, which executes the bf16 ZeRO-0 and ZeRO-1 paths in separate fresh subprocesses.
3. Observed that ZeRO-0 retained gradients after `engine.step()` and the norm tripled over three iterations, while ZeRO-1 cleared gradients.

## Observed behavior

- In stage 0, the gradient norm grew monotonically across three identical steps: 1.326786 -> 2.653573 -> 3.980515, with `post_step_non_none_grads=2` after every `engine.step()`.
- In stage 1, the same script cleared gradients after each step and reported `post_step_non_none_grads=0` with stable zero gradient norms.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
