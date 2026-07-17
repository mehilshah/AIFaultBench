# Reproduction Trajectory — Bug 286: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/3502](https://github.com/huggingface/accelerate/issues/3502)
- **Repository:** huggingface/accelerate @ `67adb473a4d96652fb1b38fb2617f01eacf9481f`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Ran `./setup_env.sh` to create an isolated venv and install the runtime dependencies.
2. Ran `./run_repro.sh`, which detected only one CUDA device and fell back to the smoke test.
3. Verified that `Accelerator.prepare(model, optimizer, dataloader, scheduler)` returns normally in the local smoke test.

## Observed behavior

- The local smoke test completed successfully: `after prepare(): Linear AcceleratedOptimizer DataLoaderShard AcceleratedScheduler`.
- The wrapper reported the environment blocker on stderr: `BLOCKED: requested 4 GPUs, but only 1 CUDA device(s) are available.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

This machine only exposes 1 CUDA device, but the reported failure requires a 4-process multi-GPU launch. The exact 4-GPU prepare path cannot be exercised here.
