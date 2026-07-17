# Bug 497 Reproduction Bundle

Issue: https://github.com/huggingface/transformers/issues/46858

This folder contains a self-contained repro attempt for the reported static-cache + `torch.compile` generation regression.

Current result in this checkout:
- `reproducible`: `false`
- The exact GPT-2 reproduction completed two `generate()` calls successfully on CPU with `torch.compile(backend="inductor")` and `generation_config.cache_implementation = "static"`.

Artifacts:
- `repro.py`: standalone repro attempt
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local virtualenv and installs the requirements
- `run_repro.sh`: runs the repro
- `reproduction.json`: schema-constrained result payload
- `repro_stdout.log`, `repro_stderr.log`: captured command output

Notes:
- The local `codebase/` tree is installed in editable mode.
- The repro uses a CPU torch wheel because the issue report is CPU-specific.
