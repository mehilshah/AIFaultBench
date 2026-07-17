# FSDP2 DTensor safetensors repro

This folder reproduces the Accelerate FSDP2 unwrap issue from `bug_report.txt`.

## What fails

`Accelerator.unwrap_model()` returns an FSDP2-wrapped GPT-2 model whose `state_dict()` still contains `DTensor`
weights. Serializing that state dict with `safetensors.torch.save_file()` raises:

`RuntimeError: Attempted to access the data pointer on an invalid python storage.`

## Files

- `repro.py`: minimal Python reproducer
- `run_repro.sh`: runs the repro and captures `repro_stdout.log` and `repro_stderr.log`
- `setup_env.sh`: installs the Python dependencies and the local `codebase/`
- `requirements.txt`: external Python dependencies for the repro

## Run

```bash
bash run_repro.sh
```

The command is expected to fail with the safetensors DTensor storage error.
