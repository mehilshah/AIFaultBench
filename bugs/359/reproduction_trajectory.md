# Reproduction Trajectory — Bug 359: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10399](https://github.com/pyg-team/pytorch_geometric/issues/10399)
- **Repository:** pyg-team/pytorch_geometric @ `a0f9e8fe469ef50760ae0c9a2702bf8443017b0c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a fresh `.venv` and installed the CPU torch wheel plus the minimal runtime dependencies from `requirements.txt`.
2. Ran `bash run_repro.sh` from the standardized bug folder.
3. Observed the expected TorchScript failures for `HypergraphConv` with and without attention.

## Observed behavior

- In a clean CPU-only Python 3.12 venv with torch 2.8.0+cpu and the local codebase on PYTHONPATH, `torch.jit.script(HypergraphConv(...))` fails for both modes: `use_attention=False` raises `Module 'HypergraphConv' has no attribute 'att'`, and `use_attention=True` raises `Variable 'alpha' previously had type NoneType but is now being assigned to a value of type Tensor`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
