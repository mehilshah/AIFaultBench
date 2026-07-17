# Reproduction Trajectory — Bug 318: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/3486](https://github.com/huggingface/accelerate/issues/3486)
- **Repository:** huggingface/accelerate @ `63168b151fa15987064a22c77b8b8ec72946f54e`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local venv, installed a CUDA-enabled PyTorch build compatible with the available GPU, and installed the local Accelerate checkout plus the TRL/Transformers/Datasets stack.
2. Ran the issue-shaped 2-rank GPU reproduction path and observed a NCCL duplicate-GPU failure before the original bug could be reached.
3. Ran the CPU FSDP2 probe and confirmed `fsdp2_prepare_model` completes successfully there.

## Observed behavior

- The issue-shaped GPU launch (`accelerate launch --config_file fsdp2.yaml repro.py`) fails earlier with NCCL duplicate-GPU errors because this machine exposes only one physical GPU, so the reported FSDP2 DeviceMesh assertion is not reached.
- The CPU fallback probe (`CUDA_VISIBLE_DEVICES= CPU_FSDP_PROBE=1 torchrun --standalone --nproc_per_node=2 repro.py`) completes successfully, which also does not reproduce the reported failure.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
source .venv/bin/activate && NCCL_P2P_LEVEL=LOC accelerate launch --config_file fsdp2.yaml repro.py
```

## Why it does not reproduce on the reference machine

Only one physical GPU is visible in this environment, so the multi-rank FSDP2 launch needed to reach the reported bug fails first with NCCL duplicate-GPU errors. The CPU probe path also succeeds, so the original DeviceMesh assertion is not reproducible here.
