# Reproduction Trajectory — Bug 503: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2525](https://github.com/huggingface/pytorch-image-models/issues/2525)
- **Repository:** huggingface/pytorch-image-models @ `3bacf433889b345c75f8f0271bc3066bb15402d7`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a clean CPU-only virtualenv
2. Install torch, torchvision, and the project dependencies
3. Run repro.py against the local codebase

## Observed behavior

- timm.list_models('*faster*') returned ['fasternet_l', 'fasternet_m', 'fasternet_s', 'fasternet_t0', 'fasternet_t1', 'fasternet_t2']
- timm.create_model('fasternet_l.in1k', pretrained=False) returned FasterNet

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported bug does not occur in this codebase snapshot.
