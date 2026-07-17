# Bug 601 Reproduction Bundle

This folder reproduces the `KeyError: 'architecture'` reported for:

```python
from timm import create_model
create_model("hf-hub:google/mobilenet_v2_1.0_224", pretrained=True)
```

The failure occurs in `codebase/timm/models/_hub.py` when `load_model_config_from_hf()`
tries to read `architecture` from the Hugging Face config JSON for the original
MobileNetV2 model repo.

## Files

- `bug_report.txt`: source issue description
- `codebase/`: local checkout of `huggingface/pytorch-image-models`
- `repro.py`: minimal reproducer
- `requirements.txt`: Python dependencies for the repro environment
- `setup_env.sh`: creates a virtualenv and installs dependencies
- `run_repro.sh`: runs the reproducer and captures logs
- `manifest.json`: standardized metadata for this bug folder
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured command output

## Run

```bash
./setup_env.sh
./run_repro.sh
```

The repro is expected to fail with:

```text
KeyError: 'architecture'
```
