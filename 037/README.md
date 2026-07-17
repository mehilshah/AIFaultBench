# Bug 037 Reproduction Bundle

This folder reproduces the value-rotation bug reported against
`labml_nn/transformers/rope/value_pe/__init__.py`.

Observed issue:
- the value tensor is rotated once before attention and then rotated again inside the
  `einsum` call
- with identity attention, the intended behavior is to reconstruct the original values
- the current implementation returns a rotated tensor instead

Files:
- `bug_report.txt`: original issue summary
- `codebase/`: local source snapshot used for analysis
- `repro.py`: self-contained reproduction
- `run_repro.sh`: convenience runner
- `setup_env.sh`: no-op environment setup for this self-contained repro
- `requirements.txt`: empty because the repro uses only the Python standard library
- `manifest.json`: metadata for the standardized bundle
- `reproduction.json`: machine-readable reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured command output

Run:
```bash
bash run_repro.sh
```
