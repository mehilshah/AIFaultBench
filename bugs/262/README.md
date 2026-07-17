# Bug 262

This folder contains a standalone repro bundle for the TensorLy complex-valued
Tensor Train regression described in `bug_report.txt`.

What to use:
- `bug_report.txt` for the original report
- `codebase/` for the local TensorLy source snapshot
- `run_repro.sh` to build the environment and run the repro
- `repro.py` for the exact failing workload

Observed result in this folder:
- TensorLy `0.9.0`
- NumPy `2.3.1`
- complex Tensor Train reconstruction error increases with rank instead of
  decreasing monotonically
- the bundled repro uses a fixed random seed so the failure is deterministic

Run:
```bash
bash run_repro.sh
```

The command writes its output to `repro_stdout.log` and `repro_stderr.log`, and
the summary decision is stored in `reproduction.json`.

Generated artifacts:
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
