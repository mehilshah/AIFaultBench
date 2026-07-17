# Reproduction Trajectory — Bug 085: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/253](https://github.com/lucidrains/vit-pytorch/issues/253)
- **Repository:** lucidrains/vit-pytorch @ `46dcaf23d8a044a41e1909ab8cfcf815c0589d65`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local venv with `bash setup_env.sh`.
2. Run `bash run_repro.sh` from the standardized folder.
3. Observe the MAE forward pass fail at the positional-embedding addition in `MAE.forward`.

## Observed behavior

- Running `bash run_repro.sh` prints `torch=2.13.0+cpu` and confirms the MAE source slice line is present.
- The run fails in `codebase/vit_pytorch/mae.py:49` with `RuntimeError: The size of tensor a (3072) must match the size of tensor b (1024) at non-singleton dimension 2`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
