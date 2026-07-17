# Bug 386

This folder is the reusable standardized benchmark input for the CVAE example bug described in `bug_report.txt`.

The bug is in `codebase/examples/cvae/baseline.py`: `MaskedBCELoss` forwards masked targets containing `-1` into `torch.nn.functional.binary_cross_entropy`, which newer PyTorch releases reject.

## Files

- `repro.py` triggers the invalid BCE target path directly.
- `requirements.txt` lists the minimal runtime dependencies for the repro.
- `setup_env.sh` creates a local virtualenv and installs those dependencies.
- `run_repro.sh` bootstraps the environment, runs the repro, and saves stdout/stderr.
- `manifest.json` records the metadata for this bundle.

## Run

```bash
bash run_repro.sh
```

Expected output includes a JSON object with `reproducible: true` and the BCE validation exception message.
