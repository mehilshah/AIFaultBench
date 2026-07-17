# Bug 450

This folder contains a self-contained reproduction of
https://github.com/huggingface/diffusers/issues/13920.

What is being reproduced:
- `Ideogram4MRoPE.forward` runs `inv_freq @ pos.unsqueeze(2)` under autocast.
- With `torch.autocast(..., dtype=torch.bfloat16)`, the image-grid positions collapse and rotary embeddings become identical.
- The bundled repro uses CPU autocast on this host because the local GPU architecture is not supported by the installed torch wheel.

Local artifacts:
- `bug_report.txt`
- `codebase/` with the bug-relevant diffusers module needed by the repro
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Expected result:
- Reference path: distinct positions stay distinct.
- Autocast path: positions collapse and the script prints a large max difference.

The scripts create their isolated Python environment at `/tmp/repro_bug450_venv` by default.
