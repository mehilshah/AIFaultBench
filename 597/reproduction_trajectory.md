# Reproduction Trajectory — Bug 597: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21450](https://github.com/Lightning-AI/pytorch-lightning/issues/21450)
- **Repository:** Lightning-AI/pytorch-lightning @ `027455bcd9433f201b1136f68d54b1a07588abe3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the virtual environment and install the pinned dependencies with bash setup_env.sh.
2. Run bash run_repro.sh to execute the Lightning training loop and capture the warnings.

## Observed behavior

- A 2-step Trainer.fit run with ThroughputMonitor and no flops_per_batch attribute emitted the same warning 2 times.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
