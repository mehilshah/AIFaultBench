# Reproduction Trajectory — Bug 290: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2691](https://github.com/huggingface/pytorch-image-models/issues/2691)
- **Repository:** huggingface/pytorch-image-models @ `af354f6a671083624482df637c0252f0504e5e87`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the local timm sources from codebase/ without importing the full timm package init.
2. Create the reporter's model with three trainable Linear blocks and three frozen EMA blocks.
3. Call create_optimizer_v2(..., layer_decay=0.9) and inspect optimizer.param_groups["lr_scale"].

## Observed behavior

- run_repro.sh exits 1 after reproducing the layer-decay mismatch. repro_stdout.log shows actual_lr_scales [0.7290000000000001, 0.7290000000000001, 0.81, 0.81, 0.9, 0.9] versus expected_lr_scales [0.81, 0.81, 0.9, 0.9, 1.0, 1.0].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
