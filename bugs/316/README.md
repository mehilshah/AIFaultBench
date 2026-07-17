# Bug 316

Reproduction bundle for https://github.com/huggingface/diffusers/issues/14114.

## What this reproduces

The `_flash_3_varlen_hub` attention backend in Diffusers infers per-sample valid
lengths from `encoder_hidden_states_mask` and then slices key/value tensors by
prefix. That works for contiguous masks, but it is wrong when valid tokens are
non-contiguous.

This bundle uses a CPU-safe stub for the hub kernel so the bug can be exercised
without FlashAttention or CUDA. The repro shows:

- contiguous masks match the reference path
- non-contiguous masks diverge from the reference path
- gradients diverge as well

## Files

- `repro.py` - standalone reproduction
- `requirements.txt` - minimal Python dependencies
- `setup_env.sh` - creates a local virtualenv and installs dependencies
- `run_repro.sh` - runs the repro and captures logs
- `manifest.json` - machine-readable metadata

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
