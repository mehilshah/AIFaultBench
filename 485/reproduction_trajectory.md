# Reproduction Trajectory — Bug 485: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21567](https://github.com/Lightning-AI/pytorch-lightning/issues/21567)
- **Repository:** Lightning-AI/pytorch-lightning @ `8e805f9268043c9aa8f0d70800be537b56a93c19`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created and activated a clean venv with the bundle dependencies and editable local codebase install.
2. Upgraded PyTorch to a CUDA build that supports the host GPU (`torch==2.13.0+cu129`, `sm_120`).
3. Ran `bash run_repro.sh`; the script printed `step=0` and then failed with the AccumulateGrad stream-mismatch warning in stderr.

## Observed behavior

- With torch 2.13.0+cu129 on the local Blackwell GPU, `bash run_repro.sh` reaches `fabric.backward(loss)` and raises the reported `UserWarning: The AccumulateGrad node's stream does not match...` from `torch.autograd`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
