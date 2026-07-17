# Reproduction Trajectory — Bug 550: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/3288](https://github.com/pytorch/rl/issues/3288)
- **Repository:** pytorch/rl @ `9b0492906d312550c1fa88eb0d507781dcd4bca2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- repro.py printed `reproduced=True`.
- Both tested configurations failed with `ValueError: Multi-agent network expected output with shape[-2]=3 but got torch.Size([4, 3, 6, 4])`.
- The saved stderr only contains the expected TorchRL extension warning.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
