# Bug 167

This folder contains a minimal repro for the `kornia.geometry.depth.depth_to_3d_v2` batching bug.

## What fails

`depth_to_3d_v2` accepts batched camera intrinsics with shape `(*, 3, 3)`, but the internal
`unproject_meshgrid` helper still enforces an unbatched `(3, 3)` matrix. Passing a batched
`(B, 3, 3)` matrix triggers a runtime `TypeError`.

## Files

- `repro.py`: reproduces the failure.
- `requirements.txt`: minimal runtime dependencies.
- `setup_env.sh`: creates the isolated environment.
- `run_repro.sh`: installs deps and runs the repro.
- `manifest.json`: metadata for the standardized bundle.

## Repro command

```bash
bash run_repro.sh
```
