# Bug 276 Reproduction Bundle

This folder contains a self-contained reproduction for the TorchRL Minari cache bug described in `bug_report.txt`.

The repro mirrors the failing sequence in `codebase/torchrl/data/datasets/minari_data.py`:
the dataset is downloaded into a temporary Minari cache, the environment is restored,
and `minari.load_dataset(...)` is called after the restore, so it looks in the wrong cache path.

## Files

- `repro.py`: minimal Python reproduction
- `run_repro.sh`: wrapper that writes `repro_stdout.log` and `repro_stderr.log`
- `setup_env.sh`: no-op environment setup for this stdlib-only repro
- `requirements.txt`: intentionally empty, because the repro uses only the standard library
- `manifest.json`: metadata for the standardized bundle

## Run

```bash
bash run_repro.sh
```

Expected result: a `FileNotFoundError` that matches the issue report pattern, proving the bug is reproducible in this checkout.
