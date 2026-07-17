# Reproduction Trajectory — Bug 081: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/304](https://github.com/lucidrains/vit-pytorch/issues/304)
- **Repository:** lucidrains/vit-pytorch @ `5578ac472faf3903d4739ba783f3875b77177e57`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a `CrossViT` instance with the parameters from the issue report.
2. Pass a tensor with shape `1 x 1 x 256 x 256` to the model.
3. Observe the `LayerNorm` shape mismatch in `vit_pytorch/cross_vit.py` during the forward pass.

## Observed behavior

- Running `bash run_repro.sh` exits with code 1 and raises `RuntimeError: Given normalized_shape=[768], expected input with shape [*, 768], but got input of size[1, 256, 256]` when `CrossViT` processes a 1-channel image.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
