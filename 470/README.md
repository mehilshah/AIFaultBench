# Bug 470 Reproduction

This bundle reproduces the EVA rotary position embedding crash reported in:
`https://github.com/huggingface/pytorch-image-models/issues/2549`

Observed behavior in this checkout:
- `Eva(patch_drop_rate=0.75, use_rot_pos_emb=True)` with `batch_size=1` succeeds.
- The same model with `batch_size=8` fails with:
  `RuntimeError: The size of tensor a (12) must match the size of tensor b (8) at non-singleton dimension 1`

Files:
- `setup_env.sh`: creates a clean virtualenv and installs the pinned dependencies plus the local `timm` checkout
- `run_repro.sh`: runs the reproducer
- `repro.py`: minimal failing script
- `requirements.txt`: pinned Python dependencies used by the repro

To run:
```bash
bash setup_env.sh
bash run_repro.sh
```
