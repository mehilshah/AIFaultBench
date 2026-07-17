# Reproduction Trajectory — Bug 567: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9933](https://github.com/pyg-team/pytorch_geometric/issues/9933)
- **Repository:** pyg-team/pytorch_geometric @ `ef028547ff4459f6e98fe429d1564bd1d513fc31`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a local virtualenv and install torch 2.5.1+cu121 plus the PyG extension wheels.
2. Install the local `codebase/` snapshot in editable mode.
3. Run `bash run_repro.sh` to exercise the `cuda:1` PNAConv path.
4. Observe that the run is blocked before the target path because only one CUDA device is visible.

## Observed behavior

- Running `bash run_repro.sh` exits with code 2 and writes a JSON summary showing `cuda_available: true` but `cuda_device_count: 1`.
- The repro script stops before the PNAConv forward pass with: `Need at least two visible CUDA devices to probe cuda:1, but only 1 device(s) are visible.`
- The reported failure requires a `cuda:1`-style environment, which is not available in this workspace.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

Only one CUDA device is visible in this workspace, so the `cuda:1` reproduction path cannot run here.
