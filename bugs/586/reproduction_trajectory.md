# Reproduction Trajectory — Bug 586: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7718](https://github.com/deepspeedai/DeepSpeed/issues/7718)
- **Repository:** microsoft/DeepSpeed @ `e0a6bb510bf77f5f5b3907da2a76786abe74eef1`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a CPU-only virtualenv with torch 2.7.1+cpu and install the local DeepSpeed source editable.
2. Run a two-rank `torchrun` probe that executes the same synthetic training step under DDP, ZeRO-2, and ZeRO-3.
3. Compare the final gradient norms from all three runs.

## Observed behavior

- CPU/gloo probe on DeepSpeed 0.18.3+unknown produced the same global grad norm for DDP, ZeRO-2, and ZeRO-3: 2.2715824653.
- The ZeRO-2 and ZeRO-3 runs matched the DDP baseline on the checked-out source, so the reported ZeRO-2-only regression was not observed here.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The issue did not reproduce in this CPU-only environment. The GPU/stream-overlap path described in the report was not exercised, and the local probe matched DDP and ZeRO-3.
