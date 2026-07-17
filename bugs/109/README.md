# Bug 109

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
- issue URL: `https://github.com/adapter-hub/adapters/issues/794`
- commit hash: `not found in Dataset.csv`
- inferred library: `adapters`
- inferred library version: `1.1.0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`

Repro summary:
- Trigger: `PrefixTuningConfig` with `BatchSplit("a", "b", batch_sizes=[2, 0])`
- Control: the reversed split `batch_sizes=[0, 2]` succeeds
- Failure site: `codebase/src/adapters/methods/prefix_tuning.py:529`
