# Reproduction Trajectory — Bug 199: torch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/8711](https://github.com/pyg-team/pytorch_geometric/issues/8711)
- **Repository:** pyg-team/pytorch_geometric @ `e167d2b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtualenv with setup_env.sh.
2. Installed torch and the PyG Python runtime dependencies from requirements.txt.
3. Ran repro.py through run_repro.sh against the local codebase checkout.
4. Observed the hop-count mismatch: get_num_hops returned 1 while the output activated 2 hops away.

## Observed behavior

- Running ./run_repro.sh prints get_num_hops: 1 and actual hops: 2 for a deterministic ChebConv(K=3) example on the line graph from the bug report.
- The repro exits with a bug marker after showing that get_num_hops reports one MessagePassing layer while the model's receptive field reaches two hops.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
