# Reproduction Trajectory — Bug 470: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2549](https://github.com/huggingface/pytorch-image-models/issues/2549)
- **Repository:** huggingface/pytorch-image-models @ `b2034bb6c57fa6b41fda7398140bf21405361df7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- On this checkout, `Eva(patch_drop_rate=0.75, use_rot_pos_emb=True)` in training mode succeeds for batch size 1 and fails for batch size 8 with `RuntimeError: The size of tensor a (12) must match the size of tensor b (8) at non-singleton dimension 1` from `timm/models/eva.py:180`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
