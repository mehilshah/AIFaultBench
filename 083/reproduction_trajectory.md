# Reproduction Trajectory — Bug 083: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/279](https://github.com/lucidrains/vit-pytorch/issues/279)
- **Repository:** lucidrains/vit-pytorch @ `8208c859a5474b2d93b429202833fcd9f395ec30`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local virtualenv with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Observe the `NameError` in `repro_stderr.log`.

## Observed behavior

- Running `bash run_repro.sh` exits with code 1 and `repro_stderr.log` shows `NameError: name 'ttention' is not defined. Did you mean: 'Attention'?` from `codebase/vit_pytorch/cross_vit.py:118` while instantiating `CrossViT`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
