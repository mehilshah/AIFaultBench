# Bug 534

Reproduction bundle for the Accelerate checkpoint pruning bug described in `bug_report.txt`.

What this checks:
- `ProjectConfiguration(total_limit=3, automatic_checkpoint_naming=True)`
- 20 consecutive `Accelerator.save_state()` calls
- final checkpoint retention under `codebase/src/accelerate/accelerator.py`

Expected result if the bug is present:
- the retained folders are not the latest three numeric checkpoints
- on the reported code path this typically leaves `checkpoint_8`, `checkpoint_9`, and `checkpoint_19`

Run:
```bash
bash run_repro.sh
```

Files in this folder:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
