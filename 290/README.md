# Bug 290 Repro

This folder reproduces timm issue 2691: `param_groups_layer_decay()` assigns `lr_scale` values as if frozen EMA parameters still consumed a layer depth.

## What is included

- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies for the reproducer
- `setup_env.sh`: installs the runtime dependencies
- `run_repro.sh`: runs the reproducer and captures logs
- `torchvision/`: tiny local shim for `FrozenBatchNorm2d`

## Reproduction

```bash
bash run_repro.sh
```

The expected failure is an assertion showing that the observed `lr_scale` sequence is:

```text
0.7290000000000001, 0.7290000000000001, 0.81, 0.81, 0.9, 0.9
```

instead of the expected:

```text
0.81, 0.81, 0.9, 0.9, 1.0, 1.0
```
