# Bug 535

This folder contains the reusable standardized reproduction bundle for the DeepSpeed decoupled checkpoint hang.

Inputs preserved from the benchmark:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
```bash
bash run_repro.sh
```

The repro intentionally starts `DecoupledCheckpointEngine`, kills the checkpoint subprocess, and verifies that `commit()` remains blocked because the implementation waits on `save_event` without a timeout or process-health check.
