# Reproduction Trajectory — Bug 221: torchio

- **Bug report:** [https://github.com/TorchIO-project/torchio/issues/1335](https://github.com/TorchIO-project/torchio/issues/1335)
- **Repository:** TorchIO-project/torchio
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a synthetic 3D ScalarImage with a known global minimum.
2. Apply tio.Pad(1, padding_mode='minimum').
3. Inspect border voxels and compare them with the global minimum.

## Observed behavior

- global_min=-2.0, padded_shape=(4, 4, 5), z0_face=[[-2.0, -2.0, 1.0, 3.0, -2.0], [-2.0, -2.0, 1.0, 3.0, -2.0], [4.0, 4.0, 5.0, 6.0, 4.0], [-2.0, -2.0, 1.0, 3.0, -2.0]], y0_face=[[-2.0, -2.0, 1.0, 3.0, -2.0], [10.0, 10.0, 11.0, 12.0, 10.0], [-2.0, -2.0, 1.0, 3.0, -2.0], [-2.0, -2.0, 1.0, 3.0, -2.0]], x0_face=[[-2.0, -2.0, 4.0, -2.0], [10.0, 10.0, 13.0, 10.0], [-2.0, -2.0, 4.0, -2.0], [-2.0, -2.0, 4.0, -2.0]]

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
