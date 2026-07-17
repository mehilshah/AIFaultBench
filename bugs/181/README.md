# Bug 181 Reproduction

This folder contains a minimal reproduction for the Lightning bug reported in
`bug_report.txt`.

## What it shows

Lightning 2.5.1rc2 rejects `accelerator="xpu"` during `Trainer` initialization
with:

`ValueError: You selected an invalid accelerator name: accelerator='xpu'`

## Files

- `repro.py`: minimal Python repro
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: optional environment bootstrap
- `run_repro.sh`: runs the repro
- `manifest.json`: metadata for the standardized bundle
- `reproduction.json`: machine-readable result
- `repro_stdout.log` / `repro_stderr.log`: captured run output

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro uses the local `codebase/src` tree through `PYTHONPATH`, so it does
not need the package installed globally.
