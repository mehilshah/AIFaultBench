# Bug 318

## Summary

This folder captures the issue report for Accelerate FSDP2 + `SFTTrainer` and a local repro bundle built from the bundled `codebase/`.

The reported failure is:

- `torch.distributed.fsdp._fully_shard` asserts on a missing named `DeviceMesh` during FSDP2 setup.

## Files

- `bug_report.txt`: original issue description.
- `codebase/`: local Accelerate source used for the repro bundle.
- `repro.py`: combined repro script.
- `fsdp2.yaml`: Accelerate launch config for the GPU path.
- `setup_env.sh`: creates a venv and installs the required packages.
- `run_repro.sh`: launches the issue-shaped repro command.
- `requirements.txt`: Python dependencies outside the local Accelerate checkout.
- `reproduction.json`: final reproducibility result.
- `repro_stdout.log`, `repro_stderr.log`: useful command output from the reproduction attempts.

## Repro command

```bash
bash run_repro.sh
```

## Local result

On this machine the GPU path does not reach the reported assertion. It fails earlier with NCCL duplicate-GPU errors because only one physical GPU is visible while the repro uses a 2-rank launch.

I also ran a CPU FSDP2 probe from `repro.py`:

```bash
CUDA_VISIBLE_DEVICES= CPU_FSDP_PROBE=1 torchrun --standalone --nproc_per_node=2 repro.py
```

That probe completes successfully, which is consistent with the reported issue being tied to the multi-GPU launch path.
