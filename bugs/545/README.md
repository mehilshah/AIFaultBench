# Bug 545

This folder is a self-contained repro bundle for Lightning issue 21488.

Inputs preserved from the benchmark:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
- `bash run_repro.sh`

Observed result:
- `save_hyperparameters(ignore="arg2")` in the child class does not remove `arg2` from `model.hparams` when the base class already saved hyperparameters.
- The minimal repro fails with `AssertionError: arg2 unexpectedly persisted in hparams`.
