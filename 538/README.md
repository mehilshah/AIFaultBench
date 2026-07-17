# Bug 538

This folder is the reusable standardized reproduction bundle for TorchRL issue 3291.

What is included:
- `bug_report.txt` from the benchmark input
- `codebase/` from `pytorch/rl@ab35c364cbebea9267bbe50b6e6cafab0768b249`
- Reproduction artifacts:
  - `repro.py`
  - `requirements.txt`
  - `setup_env.sh`
  - `run_repro.sh`
  - `reproduction.json`
  - `repro_stdout.log`
  - `repro_stderr.log`

Observed result:
- `SACLoss(target_entropy="auto")` returns `-1.0` for a 2D `BoundedContinuous` action spec.
- The expected entropy target is `-2.0`, matching `-dim(A)`.

Reproduction command:
- `bash run_repro.sh`

Notes:
- The repro uses only the local `codebase/` snapshot plus the dependencies listed in `requirements.txt`.
- The bug is reproducible in this snapshot; no application code was modified.
