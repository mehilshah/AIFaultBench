# Reproduction Trajectory — Bug 388: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10356](https://github.com/pyg-team/pytorch_geometric/issues/10356)
- **Repository:** pyg-team/pytorch_geometric @ `85cf9fc12b1138c1f2adbed8a761356c3f4197e7`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a clean venv with torch 2.7.1+cpu, torch_geometric 2.6.1, psutil, and numpy.
2. Ran `bash run_repro.sh --epochs 30` against the reported on-disk graph loading pattern.
3. Checked `repro_stdout.log`; RSS rose during warmup but then oscillated in a bounded range instead of monotonically increasing each epoch.

## Observed behavior

- In the isolated venv (Python 3.12.3, torch 2.7.1+cpu, torch_geometric 2.6.1), the repro started at 298.22 MB RSS and then fluctuated between 346.07 MB and 426.02 MB over 30 epochs. The curve was noisy and bounded, not the steady per-epoch climb described in the report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh --epochs 30
```

## Why it does not reproduce on the reference machine

The bug was not reproducible in this container under the reported package versions; the observed RSS pattern did not match the runaway memory growth from the issue report.
