# Reproduction Trajectory — Bug 529: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9974](https://github.com/pyg-team/pytorch_geometric/issues/9974)
- **Repository:** pyg-team/pytorch_geometric @ `9b794b600d41802edaad26aac18bff958fc8f642`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a minimal distributed graph-classification repro based on the reported GraphConv + global pooling architecture.
2. Installed a clean local PyTorch 2.3.1 environment and used the checked-in PyG source tree via PYTHONPATH.
3. Ran the repro in CPU/gloo mode and confirmed the model forward/backward path completes without a segfault.

## Observed behavior

- FORCE_CPU=1 WORLD_SIZE=1 bash run_repro.sh completed successfully.
- Captured stdout ended with 'completed without segfault'.
- A prior GPU-path attempt on this machine exposed a PyTorch CUDA compatibility warning for an RTX PRO 6000 Blackwell Max-Q (sm_120), so the reported CUDA/NCCL environment is not available here.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
FORCE_CPU=1 WORLD_SIZE=1 bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The local machine does not match the reported GPU/runtime stack; the available GPU is incompatible with the installed PyTorch wheel (sm_120 vs supported up to sm_90), so the reported CUDA/NCCL segfault could not be exercised here.
