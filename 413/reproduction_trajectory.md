# Reproduction Trajectory — Bug 413: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/1064](https://github.com/facebookresearch/detectron2/issues/1064)
- **Repository:** facebookresearch/detectron2 @ `2612e4a90e77ce3ea650546ac99a91e8c6ac9aad`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- Running `bash run_repro.sh` in the isolated venv reproduces `TypeError: len() of a 0-d tensor` from `codebase/detectron2/structures/instances.py:71` when `Instances.__getitem__` calls `ret.set(k, v[item])` with integer indexing.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
