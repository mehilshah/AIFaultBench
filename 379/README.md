# Bug 379

This folder contains a self-contained reproduction of Hugging Face Accelerate issue 1598.

What reproduces the bug:
- `dispatch_model(model, {"": "cpu"})` on a tiny `nn.Module`
- `multiprocessing` with the `spawn` start method
- process start fails with `PicklingError: Can't pickle <function Embedding.forward ...>`

What does not fail:
- the same model without `dispatch_model`

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
