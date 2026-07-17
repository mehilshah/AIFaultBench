# Bug 393

This folder contains a self-contained reproduction bundle for the Accelerate issue in `bug_report.txt`.

What is reproduced:
- `accelerate.test_utils.scripts.test_script.test_split_between_processes_nested_dict`
- The failure is an assertion mismatch in the 4-process case for nested dictionaries

Local environment notes:
- The report mentions `accelerate 0.20.3` with DeepSpeed on 4x A100 GPUs.
- The bundled repro uses the pinned local `accelerate` snapshot and a 4-process CPU `gloo` setup to hit the same failing code path without requiring GPUs.

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Inputs preserved from the benchmark:
- `bug_report.txt`
- `codebase/`
