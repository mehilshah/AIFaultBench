# Reproduction Trajectory — Bug 253: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3122](https://github.com/pytorch/rl/issues/3122)
- **Repository:** pytorch/rl @ `0592fdc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment and installed torch==2.7.1, tensordict==0.10.0, numpy, and packaging.
2. Ran the local codebase via PYTHONPATH=codebase against the issue script.
3. Observed IQLLoss fail when the categorical action spec uses shape torch.Size((1,)).
4. Verified that the same setup succeeds when the categorical action spec uses shape torch.Size(()).

## Observed behavior

- Running the local TorchRL source with torch==2.7.1 and tensordict==0.10.0 reproduces the bug for Categorical actions shaped as (batch, 1). The failing case prints: RuntimeError: Losses shape mismatch: torch.Size([2, 2]) and torch.Size([2]). The workaround case with action shape (batch,) completes successfully.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
