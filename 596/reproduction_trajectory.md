# Reproduction Trajectory — Bug 596: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13488](https://github.com/huggingface/diffusers/issues/13488)
- **Repository:** huggingface/diffusers @ `71a6fd9f0df04d3764dfa999268a05d87903a85a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a fresh Python 3.12 virtual environment and installed the local diffusers source in editable mode.
2. Ran repro.py through run_repro.sh with a CUDA-capable PyTorch build.
3. Observed the failure on the second scheduler step when UniPCMultistepScheduler.multistep_uni_p_bh_update stacks mixed-device rks tensors.

## Observed behavior

- On CUDA, the minimal 3-step UniPCMultistepScheduler run fails on the second scheduler step with RuntimeError: Expected all tensors to be on the same device, but got tensors is on cuda:0, different from other tensors on cpu, raised from torch.stack(rks) in scheduling_unipc_multistep.py:907.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
