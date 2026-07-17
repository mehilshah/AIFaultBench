# Reproduction Trajectory — Bug 167: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/2970](https://github.com/kornia/kornia/issues/2970)
- **Repository:** kornia/kornia @ `4bd1bd1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated environment with setup_env.sh and installed the minimal runtime dependencies.
2. Ran repro.py with depth shape (4, 512, 512) and batched intrinsics shape (4, 3, 3).
3. Observed the runtime TypeError raised from KORNIA_CHECK_SHAPE in unproject_meshgrid.

## Observed behavior

- Running bash run_repro.sh reaches TypeError in codebase/kornia/geometry/depth.py:55 because unproject_meshgrid enforces camera_matrix shape ['3', '3'] while depth_to_3d_v2 passes a batched tensor with shape torch.Size([4, 3, 3]).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
