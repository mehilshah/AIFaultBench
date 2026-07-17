# Bug 164

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:
- issue URL: `https://github.com/kornia/kornia/issues/1396`
- commit hash: `not found in Dataset.csv`
- inferred library: `kornia`
- inferred library version: `0.5.11`
- bug report source: `bug_report.txt`
- codebase source: `codebase`

Repro notes:
- The checked-in snapshot does not include `bbox_v2`, so the reproducer uses the exact amin/amax gradcheck pattern from the report with the local `kornia.testing.tensor_to_gradcheck_var` helper.
- Expected result: 2D gradcheck passes, 3D gradcheck fails with a Jacobian mismatch.
- Run: `bash run_repro.sh`
