# Reproduction Trajectory — Bug 079: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/330](https://github.com/lucidrains/vit-pytorch/issues/330)
- **Repository:** lucidrains/vit-pytorch @ `fcb9501cdd9e056dd040915deb3e0a6378821843`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtual environment and installed the repro dependencies from requirements.txt.
2. Ran repro.py through the standard entry point, run_repro.sh.
3. Observed the LayerNorm shape mismatch when RegionViT was instantiated with tokenize_local_3_conv=True.

## Observed behavior

- Running `bash run_repro.sh` in the standardized folder printed `input_shape=(1, 3, 224, 224)` and then failed with `RuntimeError: Given normalized_shape=[64], expected input with shape [*, 64], but got input of size[1, 64, 112, 112]`. The traceback corresponds to `nn.LayerNorm(init_dim)` in `codebase/vit_pytorch/regionvit.py:215`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
