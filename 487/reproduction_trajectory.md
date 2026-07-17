# Reproduction Trajectory — Bug 487: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7804](https://github.com/deepspeedai/DeepSpeed/issues/7804)
- **Repository:** microsoft/DeepSpeed @ `5aa2d17dd71ab71d129719ba25e261a92f677d80`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Checked out microsoft/DeepSpeed at 5aa2d17dd71ab71d129719ba25e261a92f677d80 into codebase/.
2. Ran the source-level reproducer against codebase/deepspeed/runtime/zero/stage_1_and_2.py.
3. Observed that IPGBucket.clear() resets index to 0 and the simulated ping-pong buffer never alternates.
4. Attempted to assess the full runtime path, but the local PyTorch/DeepSpeed CUDA stack is not usable in this container.

## Observed behavior

- The pinned DeepSpeed source contains the IPG bucket index reset in `IPGBucket.clear()`, and the source-level reproducer shows the post-reduction buffer index sequence stays [1, 1, 1, 1] instead of alternating. The full CUDA multi-GPU overlap trace described in the bug report could not be executed here because the local PyTorch install is broken and the environment does not provide a usable DeepSpeed/CUDA runtime.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The bug needs a working multi-GPU CUDA DeepSpeed runtime to validate the actual communication/computation overlap. In this container, torch import is broken (`libtorch_cuda.so: undefined symbol: ncclCommResume`), and the required multi-GPU setup is unavailable.
