# Bug 054

This folder contains a static repro for keras-io issue 1711.

Bug summary:
- `examples/vision/pointnet.py` trains with `validation_data=test_dataset`.
- `test_dataset` is built from the test split, so the example evaluates on the test set during training.

Files in this bundle:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`
