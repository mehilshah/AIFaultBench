# Reproduction Trajectory — Bug 251: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/2422](https://github.com/pytorch/rl/issues/2422)
- **Repository:** pytorch/rl @ `57f0580`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal benchmark in repro.py that matches the issue report's sampling pattern.
2. Added a compatibility shim for tensordict's renamed interaction_mode API so the repository snapshot can import cleanly.
3. Ran the benchmark against the local codebase and measured a ~27.9x slowdown with SliceSampler enabled.

## Observed behavior

- Running the benchmark in a clean venv reproduced the slowdown. Baseline ReplayBuffer sampling took 0.00018371284628907839 s, while the same benchmark with SliceSampler took 0.00512981618133684 s, for a 27.923012924555646x slowdown.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
PYTHONPATH=codebase /tmp/bug251-venv/bin/python repro.py
```
