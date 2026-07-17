# Bug 103 Reproduction

This bundle reproduces the `ResidualLFQ` commitment-loss masking warning described in `bug_report.txt`.

## Repro command

```bash
bash run_repro.sh
```

## What it does

- Instantiates `ResidualLFQ` from the checked-in `codebase/`
- Passes a boolean token mask with two masked-out positions
- Enables `commitment_loss_weight=1.0`
- Triggers the `torch.nn.functional.mse_loss` broadcasting warning in `LFQ.forward`

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: optional environment bootstrap
- `run_repro.sh`: reproduction entry point
- `manifest.json`: bundle metadata
