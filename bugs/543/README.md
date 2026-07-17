# Bug 543

This folder contains a self-contained reproduction bundle for the transformers
issue described in `bug_report.txt`.

What the repro does:
- installs a clean CPU-only PyTorch environment in `.venv`
- loads the local `codebase/src` checkout through `PYTHONPATH`
- runs `VideoPrismForVideoClassification` with `num_frames=2`
- asserts that `outputs.hidden_states` should be `None` or a tuple

Observed behavior in this checkout:
- `outputs.hidden_states` is a raw `torch.Tensor`
- the assertion fails, matching the bug report

Primary commands:
- `bash setup_env.sh`
- `bash run_repro.sh`

The machine-readable outcome is written to `reproduction.json`.
