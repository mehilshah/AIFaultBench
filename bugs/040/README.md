# Bug 040 Reproduction

This bundle reproduces the attention normalization bug reported for DDPM U-Net.

The defect is in [`codebase/labml_nn/diffusion/ddpm/unet.py`](codebase/labml_nn/diffusion/ddpm/unet.py):

- `AttentionBlock.forward()` computes attention logits with `einsum('bihd,bjhd->bijh', ...)`
- the logits are then normalized with `softmax(dim=1)`
- for this layout, `dim=1` is the query axis, while the key axis is `dim=2`

The repro script checks the normalization invariant directly on a deterministic tensor:

- buggy attention sums to 1 across the query axis
- corrected attention sums to 1 across the key axis

## Files

- `repro.py`: deterministic tensor-level repro
- `run_repro.sh`: executes the repro
- `setup_env.sh`: installs runtime dependencies
- `requirements.txt`: minimal Python dependencies
- `manifest.json`: metadata for this bug folder

## Run

```bash
bash run_repro.sh
```

The script writes the schema result to `reproduction.json` and prints the evidence used by the logs.
