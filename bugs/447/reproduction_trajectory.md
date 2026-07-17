# Reproduction Trajectory — Bug 447: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10159](https://github.com/pyg-team/pytorch_geometric/issues/10159)
- **Repository:** pyg-team/pytorch_geometric @ `69193c895fe721fb45e63985bb79e8d130ee7782`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a fresh virtual environment and installed torch 2.4.1+cpu plus the editable local pytorch_geometric snapshot.
2. Ran the reported 10,000-iteration Linear loop through repro.py.
3. Observed identical outputs across all iterations; no first-element divergence appeared.

## Observed behavior

- On a clean CPU-only environment, the reproduced loop printed first_max_diff=0.0 and rest_max_diff=0.0 with device=cpu and cuda_available=False.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The issue did not reproduce in this environment. The available runtime is CPU-only, while the report likely depends on a different GPU/CUDA setup.
