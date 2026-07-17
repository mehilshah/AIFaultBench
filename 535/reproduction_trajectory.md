# Reproduction Trajectory — Bug 535: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7741](https://github.com/deepspeedai/DeepSpeed/issues/7741)
- **Repository:** microsoft/DeepSpeed @ `20cfce004a79e026e7ba01d2f103b05e2637c6e0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Launch `DecoupledCheckpointEngine` with a local stub writer config.
2. Terminate the spawned checkpoint subprocess before calling `commit()`.
3. Start `commit()` on a daemon thread and wait 2 seconds.
4. Observe that the thread is still blocked on `save_event.wait()`.
5. Capture stdout/stderr in `repro_stdout.log` and `repro_stderr.log`.

## Observed behavior

- After terminating the checkpoint subprocess, `commit()` remained blocked for at least 2 seconds. The saved stdout log shows: `checkpoint child alive after terminate: False` followed by `commit() is still blocked after 2s` and `evidence: save_event.wait() does not time out and there is no process-health check`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
