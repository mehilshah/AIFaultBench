# NeMo Canary timestamp repro

This bundle reproduces the issue reported in NVIDIA NeMo issue `#15305`.

Observed behavior:

- `EncDecMultiTaskModel.from_pretrained("nvidia/canary-1b-v2")`
- `model.transcribe(..., timestamps=True, batch_size=1, return_hypotheses=True)`
- The returned hypothesis has:
  - `timestamp["word"] == []`
  - `timestamp["segment"] == []`

## Files

- `repro.py` runs the testcase and asserts the failure mode.
- `timestamp.zip` contains the reporter-provided audio clip.
- `setup_env.sh` creates a local virtualenv and installs the required runtime stack.
- `run_repro.sh` executes the repro.

## Run locally

```bash
bash setup_env.sh
bash run_repro.sh
```

## Notes

- The model download is handled by `EncDecMultiTaskModel.from_pretrained(...)`.
- The repro was verified with CPU-only PyTorch in a local virtual environment.
