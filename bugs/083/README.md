# Bug 083 Repro

This folder reproduces the `CrossViT` constructor failure from the pinned `vit-pytorch` codebase.

Observed defect:
- `codebase/vit_pytorch/cross_vit.py` references `ttention(...)` instead of `Attention(...)` while building `CrossTransformer`.
- Instantiating `CrossViT` raises `NameError` during `CrossTransformer.__init__`.

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro script writes the traceback to `repro_stderr.log` and any stdout to `repro_stdout.log`.
