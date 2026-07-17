# Bug 537

This folder is the reusable standardized benchmark input for issue
`https://github.com/huggingface/pytorch-image-models/issues/2481`.

What I checked:
- `timm.create_model("resnet34", pretrained=False, num_classes=100)`
- The ResNet-34 stem documented in `codebase/timm/models/resnet.py`
- A random forward pass on 32x32 inputs

Outcome:
- `reproducible = false`
- The local smoke test shows model construction and execution work.
- The accuracy gap in the report is not reproducible as a deterministic library defect here.

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
