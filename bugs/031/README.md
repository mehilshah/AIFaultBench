# Bug 031 Reproduction

This folder reproduces the ResNet50 pretrained-weight loading failure reported in NVIDIA DeepLearningExamples issue 1268.

## What fails

`codebase/PyTorch/Classification/ConvNets/image_classification/models/model.py` loads `--pretrained-from-file` checkpoints with raw `torch.load(...)` contents and calls `model.load_state_dict(...)` without applying the legacy `layer1.* -> layers.0.*` key remap that is only used for `pretrained=True`.

The repro script creates a synthetic checkpoint whose keys follow the older `layer1.*` naming and then invokes the real `resnet50(pretrained_from_file=...)` loader. The run fails with the same `RuntimeError` pattern from the report:

- missing keys such as `layers.0.0.conv1.weight`
- unexpected keys such as `layer1.0.conv1.weight`

## Files

- `repro.py` - minimal reproducer
- `requirements.txt` - runtime dependency set
- `setup_env.sh` - installs the Python dependency
- `run_repro.sh` - executes the repro

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

Or, if using Docker:

```bash
```

## Expected result

The command exits non-zero after printing `EXPECTED_RUNTIME_ERROR` and the `load_state_dict` key mismatch.
