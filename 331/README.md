# Bug 331

Repro bundle for https://github.com/huggingface/transformers/issues/47228.

What it does:
- builds a tiny `Sam3Model` in `torch.bfloat16`
- runs one eager forward successfully
- runs the same model through `torch.compile`
- reproduces the `RuntimeError: mat1 and mat2 must have the same dtype, but got Float and BFloat16`

Files:
- `bug_report.txt`: original issue description
- `codebase/`: local transformers source snapshot used for the repro
- `repro.py`: minimal reproduction script
- `requirements.txt`: runtime dependencies for the repro environment
- `setup_env.sh`: creates `.venv` and installs dependencies with `uv`
- `run_repro.sh`: executes the repro inside `.venv`
- `reproduction.json`: schema-constrained result
- `repro_stdout.log` / `repro_stderr.log`: captured run output
