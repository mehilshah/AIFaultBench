# Bug 305

This folder reproduces https://github.com/huggingface/peft/issues/2381.

Observed behavior:
- adding a second adapter that uses `modules_to_save`
- deleting that adapter leaves its entry behind in `modules_to_save`

Files:
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

Run:
- `bash setup_env.sh`
- `bash run_repro.sh`

The repro uses a locally instantiated `BertForSequenceClassification` model to avoid external model downloads.
