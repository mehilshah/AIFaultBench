# Bug 468

This folder contains a self-contained reproduction bundle for DeepSpeed issue 7807.

Inputs:
- `bug_report.txt`
- `codebase/` pinned to `15ad92b459c6c39b7c5527efe1e42080eb4ab99f`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
- `bash run_repro.sh`

What the repro checks:
- the fully reduced gradient path that should be safe before Muon orthogonalization
- the mixed reduced/local gradient state that occurs with `reduce_scatter=true`
- the resulting partition slices and reconstructed update
