# Bug 308 Reproduction

This folder reproduces the `torchrl.data.ReplayBuffer` prefetch off-by-one bug described in `bug_report.txt`.

Observed behavior:
- `prefetch=1` leaves `len(rb._prefetch_queue) == 0` after the first `sample()`
- the report expects the queue to retain one in-flight batch

Files:
- `repro.py`: minimal Python reproducer
- `requirements.txt`: runtime deps for the repro venv
- `setup_env.sh`: creates a local venv and installs deps
- `run_repro.sh`: runs the repro and captures logs
- `manifest.json`: bundle metadata

Run locally:
```bash
bash run_repro.sh
```

Expected result:
- the script fails with `AssertionError: Bug present: Expected prefetch queue to have 1 item, but got 0.`

