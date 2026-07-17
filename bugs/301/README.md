# Bug 301 Repro

This folder captures the CPU FSDP repro for Lightning issue [#21778](https://github.com/Lightning-AI/pytorch-lightning/issues/21778).

## What I tried

The reported failure path is `lightning.pytorch.strategies.FSDPStrategy._setup_model()` on a CPU-only distributed setup. The local source still passes `device_id=self.root_device.index`, so the root cause from the issue is present in the code snapshot.

## Result in this environment

The bug is **not reproducible here**.

Reason: this checkout is running `torch 2.13.0+cu130`, and the CPU FSDP setup completes successfully with only a warning. The `RuntimeError: FSDP needs a non-CPU accelerator device` from the report does not trigger in this runtime.

The bundled requirements target the reported torch window (`2.5.x` / `2.6.x`) so a fresh environment can be driven toward the failure case more faithfully than the current runtime.

## Files

- `repro.py`: standalone reproducer that initializes a one-process `gloo` group and calls `FSDPStrategy._setup_model()` on a CPU model.
- `requirements.txt`: minimal package set for the repro harness.
- `setup_env.sh`: creates a local venv and installs the requirements.
- `run_repro.sh`: sets up the environment and captures stdout/stderr.

## Reproduction command

```bash
./run_repro.sh
```

## Observed output

The run completes without an exception and records the warning emitted by PyTorch FSDP when initializing on CPU.
