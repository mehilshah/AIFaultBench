# Bug 384

This folder reproduces the rotated-box IoU bug described in `bug_report.txt`.

## What fails

The reported box pair still produces a non-zero IoU:

```text
tensor([[0.2655]])
```

The expected value in the report is `tensor([[0.0]])`.

## Files

- `repro.py` prints the exact IoU mismatch as JSON.
- `requirements.txt` pins the runtime used for the repro.
- `setup_codebase.sh` restores the Detectron2 source tree as a symlinked external clone.
- `setup_env.sh` activates the preserved `.venv_repro` environment and builds the local `_C` extension in place if needed.
- `run_repro.sh` boots the environment and captures stdout/stderr in `repro_stdout.log` and `repro_stderr.log`.
- `manifest.json` records the bundle metadata.

## Run

```bash
bash run_repro.sh
```
