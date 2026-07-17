# Reproduction Trajectory — Bug 084: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/257](https://github.com/lucidrains/vit-pytorch/issues/257)
- **Repository:** lucidrains/vit-pytorch @ `5699ed7d139062020d1394f0e85a07f706c87c09`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv and installed the CPU PyTorch stack plus einops.
2. Generated synthetic cats/dogs archives that match the notebook's train.zip/test.zip flow.
3. Ran the example's ViT + Linformer training loop against the generated data.
4. Observed 100% accuracy on the first epoch and on validation across the run.

## Observed behavior

- Epoch 1 logged acc=1.0000 and val_acc=1.0000; subsequent epochs stayed at val_acc=1.0000.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
