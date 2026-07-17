# Reproduction Trajectory — Bug 172: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/997](https://github.com/kornia/kornia/issues/997)
- **Repository:** kornia/kornia @ `bd49f1b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment with bash setup_env.sh.
2. Run bash run_repro.sh with PYTHONPATH pointed at codebase/.
3. Observe that projections_from_fundamental(torch.randn(1, 3, 3)) returns shape (1, 3, 4, 2) while the docstring advertises (*, 4, 4, 2).

## Observed behavior

- repro_stdout.log shows documented_shape=(*, 4, 4, 2) and actual_shape=(1, 3, 4, 2) with docstring_mentions_shape=True; repro_stderr.log is empty.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
