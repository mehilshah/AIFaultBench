# Reproduction Trajectory — Bug 628: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3240](https://github.com/pytorch/rl/issues/3240)
- **Repository:** pytorch/rl @ `8570c25a745da54ca647b8a70231112f063d1421`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create `.venv` and install the pinned dependencies.
2. Run `bash run_repro.sh` from the bug folder.
3. Confirm that the manual `ParallelEnv` replay-buffer extend succeeds and that the `MultiSyncDataCollector` never yields its first batch.

## Observed behavior

- In a CPU-only venv with torch 2.7.1, tensordict 0.10.0, gymnasium 1.1.1, and the local torchrl codebase, `repro.py` prints `manual_extend_ok len=8 write_count=8`, then prints `collector_created`, then stops at `Returning final rollout with NO buffer (maybe_dense_stack).` without ever emitting `iter=0` before `run_repro.sh` times out.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
