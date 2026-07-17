# Reproduction Trajectory — Bug 554: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9959](https://github.com/pyg-team/pytorch_geometric/issues/9959)
- **Repository:** pyg-team/pytorch_geometric @ `5fb2a8eaae3047a9dd430fd58e735e333daed79d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local CPU-only virtualenv and installed `torch==2.5.1+cpu` plus `numpy==2.2.1`.
2. Bootstrapped `torch.distributed.rpc` with a single local worker so the RPC decorator gate is satisfied.
3. Patched `global_all_gather` to return a worker map containing one `None` value.
4. Called `rpc_partition_to_workers(...)` and observed the same unpacking TypeError from the issue report.

## Observed behavior

- Running `bash run_repro.sh` in the local venv exits with `TypeError: cannot unpack non-iterable NoneType object` at `codebase/torch_geometric/distributed/rpc.py:123` inside `rpc_partition_to_workers`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
