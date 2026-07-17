# Bug 253

This folder is the reusable standardized benchmark input for TorchRL issue 3122.

What the repro does:
- installs a clean Python environment with `torch==2.7.1` and `tensordict==0.10.0`
- loads the local `codebase/` via `PYTHONPATH`
- runs `IQLLoss` with a categorical action spec shaped as `(batch, 1)`
- confirms the bug by reproducing `RuntimeError: Losses shape mismatch: torch.Size([2, 2]) and torch.Size([2])`
- runs the scalar action-shape workaround `(batch,)` to show the failure is shape-specific

Files generated for reproduction:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
`bash run_repro.sh`
