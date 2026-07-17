# Bug 016

This folder is a self-contained reproduction bundle for TensorFlow Models issue #11042.

What is in here:
- `bug_report.txt`: original issue report
- `codebase/`: standardized source snapshot
- `repro.py`: static reproduction harness for the reported multi-worker setup
- `requirements.txt`: environment dependencies inferred from the report and codebase
- `setup_env.sh`: optional local environment bootstrap
- `run_repro.sh`: wrapper that captures stdout and stderr
- `manifest.json`: metadata for the bundle

Observed result:
- The report describes a multi-node GPU throughput problem.
- The checked-in `codebase/official/legacy/image_classification/configs/examples/resnet/imagenet/gpu.yaml` still uses `distribution_strategy: mirrored`.
- `classifier_trainer.py` does call `configure_cluster()` and `distribute_utils.get_distribution_strategy()` for `multi_worker_mirrored`, but this workspace does not provide the required 2-node GPU cluster to measure scaling.
- Reproduction status in this folder: not reproducible.
