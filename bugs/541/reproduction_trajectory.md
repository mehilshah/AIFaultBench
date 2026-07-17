# Reproduction Trajectory — Bug 541: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9965](https://github.com/pyg-team/pytorch_geometric/issues/9965)
- **Repository:** pyg-team/pytorch_geometric @ `47ac8186010bcd14ce14493f02075962d6b359d5`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a clean Python 3.11 virtual environment in .venv.
2. Installed torch==2.5.1+cpu and the local torch-geometric package from codebase/.
3. Ran repro.py through run_repro.sh and observed all checks pass.

## Observed behavior

- Inspector(SAGEConv).type_repr(Final[Optional[Tensor]]) returned 'typing.Final[Optional[Tensor]]', matching the expected value from the issue report.
- File-backed TorchScript wrappers for coalesce and sort_edge_index compiled and ran successfully with Optional[Tensor] and List[Tensor] inputs.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
