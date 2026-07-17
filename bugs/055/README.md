# Bug 055 Reproduction Bundle

This folder contains a self-contained repro attempt for the reported
`neural_machine_translation_with_keras_nlp` `GreedySampler` crash.

## Contents

- `bug_report.txt`: original report text
- `codebase/`: local source snapshot from `keras-team/keras-io`
- `repro.py`: minimal sampler callback reproducer
- `requirements.txt`: pinned runtime dependencies
- `setup_env.sh`: creates an isolated virtualenv and installs dependencies
- `run_repro.sh`: executes the repro script
- `manifest.json`: metadata for the standardized bug folder
- `reproduction.json`: machine-readable reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured command output

## Result

In this environment, the exact GPU segfault from the report is not reachable.
TensorFlow 2.15.0 installs and the `GreedySampler` callback runs successfully on
CPU, but TensorFlow cannot register GPU devices here because the required CUDA
libraries are unavailable.

## Run

```bash
./run_repro.sh
```

The script prints the environment details and the sampler output.
