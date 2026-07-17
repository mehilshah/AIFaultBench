# Reproduction Notes

This bundle checks the MAE example from `codebase/README.md` against the checked-out source.

The current snapshot already contains the valid slice expression in `codebase/vit_pytorch/mae.py`:

`tokens = tokens + self.encoder.pos_embedding[:, 1:(num_patches + 1)]`

The repro loads `vit.py` and `mae.py` directly so the package-level `torchvision` import does not interfere with the MAE path under test.

## Setup

```bash
bash setup_env.sh
```

## Run

```bash
bash run_repro.sh
```

## Observation

In this snapshot, the MAE example fails at `codebase/vit_pytorch/mae.py:49` with a shape mismatch between the patch tokens and the encoder positional embedding.
