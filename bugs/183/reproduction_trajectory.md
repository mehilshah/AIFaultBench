# Reproduction Trajectory — Bug 183: liger_kernel

- **Bug report:** [https://github.com/linkedin/Liger-Kernel/issues/488](https://github.com/linkedin/Liger-Kernel/issues/488)
- **Repository:** linkedin/Liger-Kernel @ `ac56674`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean Python 3.12 virtualenv and installed CPU PyTorch, Triton, and packaging.
2. Loaded the local fused linear cross entropy implementation directly from codebase/src.
3. Monkeypatched the Triton kernel with a CPU stub that writes a distinct value per token into the loss buffer.
4. Called LigerFusedLinearCrossEntropyLoss(reduction='none') on a small CPU tensor input.
5. Observed that the returned loss was scalar instead of a 1D tensor of unreduced losses.

## Observed behavior

- With a dummy Triton kernel that writes per-token losses into the loss buffer, LigerFusedLinearCrossEntropyLoss(reduction='none') still returns a scalar tensor with shape torch.Size([]).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
