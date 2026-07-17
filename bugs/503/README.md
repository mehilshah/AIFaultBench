# Bug 503

This folder is a reusable reproduction bundle for the FasterNet registry issue reported in
https://github.com/huggingface/pytorch-image-models/issues/2525.

## What was tested

- `timm.list_models("*faster*")`
- `timm.create_model("fasternet_l.in1k", pretrained=False)`

## Result

The issue is not reproducible in this snapshot.

Observed behavior:

- `fasternet_l` is present in `timm.list_models("*faster*")`
- `timm.create_model("fasternet_l.in1k", pretrained=False)` returns `FasterNet`

## Files

- `repro.py`: minimal runtime check
- `setup_env.sh`: creates a clean CPU-only Python environment
- `run_repro.sh`: runs the repro and captures logs
- `requirements.txt`: dependency set used by the repro
- `repro_stdout.log`, `repro_stderr.log`: captured output from the verified run
