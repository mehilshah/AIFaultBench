# Bug 092

Recovered issue: https://github.com/lucidrains/x-transformers/issues/263

## Verdict

This checkout does not reproduce the reported NaN on the all-false `context_mask` path.

## What the repro checks

- Builds a `TransformerWrapper` with `Decoder(cross_attend=True, attn_flash=True)`
- Passes a context tensor with `context_mask = torch.zeros(..., dtype=torch.bool)`
- Prints whether the decoder output contains any NaNs

## Files

- `repro.py`: minimal trigger script
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: runs the repro script
- `reproduction.json`: schema-constrained result payload

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The current output is finite, so the bug is not reproducible in this folder with the local `codebase/` snapshot and installed runtime.
