# Bug 221

This folder contains a self-contained reproduction bundle for TorchIO issue 1335.

Reproduction:
- `bash run_repro.sh`
- The script writes the outcome to `reproduction.json`
- Stdout and stderr are captured in `repro_stdout.log` and `repro_stderr.log`

Observed result:
- `tio.Pad(1, padding_mode='minimum')` pads with axis-wise minima from NumPy
- The padded border contains values like `10.0` and `13.0` even though the global minimum is `-2.0`

Inputs reused from the benchmark:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
