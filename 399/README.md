# Bug 399

Repro for TorchRL issue #3599.

Observed failure:

`CSVLogger(..., video_format="mp4").log_video(...)` on the pre-fix TorchRL checkout
hits `AttributeError: module 'torchvision.io' has no attribute 'write_video'`
with torchvision 0.26+.

What this bundle contains:

- `repro.py`: minimal driver that exercises the logger path
- `requirements.txt`: isolated wheel set used by the repro
- `setup_env.sh`: installs the deps into `deps/` and pins the buggy checkout
- `run_repro.sh`: runs the driver with the local source tree on `PYTHONPATH`

Run:

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro uses codebase commit `61e05b3d9a967c0cbbda2e355859287ce7221f52`,
which is the pre-fix revision with the direct `torchvision.io.write_video` call.
