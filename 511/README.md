# Bug 511 Reproduction Bundle

This folder reproduces the temporal neighbor-sampling failure reported in
`bug_report.txt`.

## What is reproduced

`NeighborSampler` raises:

`RuntimeError: Found invalid non-sorted temporal neighborhood`

when temporal sampling is run on a destination-sorted graph whose source
timestamps are not sorted within a local neighborhood.

## Files

- `repro.py`: standalone repro script
- `requirements.txt`: runtime dependencies used by the repro environment
- `setup_env.sh`: creates `.venv` and installs the dependencies
- `run_repro.sh`: runs the repro and captures logs
- `manifest.json`: bundle metadata
- `reproduction.json`: structured reproduction result written by the repro
- `repro_stdout.log`, `repro_stderr.log`: captured run output

## Run

```bash
bash setup_env.sh
./run_repro.sh
cat reproduction.json
```

The repro is expected to succeed in triggering the backend error and write
`reproducible: true` to `reproduction.json`.
