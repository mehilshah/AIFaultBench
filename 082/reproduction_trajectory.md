# Reproduction Trajectory — Bug 082: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/269](https://github.com/lucidrains/vit-pytorch/issues/269)
- **Repository:** lucidrains/vit-pytorch @ `ce4bcd08fbab864e92167415552a722ff5ce2005`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a ViT with image_size=256, patch_size=32, dim=1024, depth=6, heads=8, and mlp_dim=2048.
2. Wrapped it in MPP with patch_size=32, dim=1024, mask_prob=0.15, random_patch_prob=0.30, and replace_prob=0.50.
3. Ran `bash run_repro.sh` in a fresh `.venv` and observed the LayerNorm shape mismatch when MPP applies `transformer.to_patch_embedding[-1]` to raw flattened patches.

## Observed behavior

- Running `bash run_repro.sh` reliably fails in `codebase/vit_pytorch/mpp.py:154` with `RuntimeError: Given normalized_shape=[1024], expected input with shape [*, 1024], but got input of size[20, 64, 3072]`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
