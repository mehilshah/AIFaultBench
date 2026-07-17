# Bug 001

This folder contains a minimal reproduction bundle for:

`https://github.com/tensorflow/models/issues/166`

The bug report points at the `transformer/` MNIST example. The unstable line is
the legacy cross-entropy computation in `codebase/transformer/cluttered_mnist.py`:

`cross_entropy = -tf.reduce_sum(y * tf.log(y_pred))`

The reproduction script demonstrates that this formulation can become `NaN`
when `y_pred` contains exact zeros, which is the same numerical failure mode
reported in the issue.

Files:
- `bug_report.txt`: original issue summary
- `codebase/`: local source snapshot used for the repro
- `repro.py`: minimal TensorFlow reproduction
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: creates the isolated environment
- `run_repro.sh`: convenience entrypoint
- `reproduction.json`: machine-readable result
- `repro_stdout.log` / `repro_stderr.log`: captured run output

Run:

`bash run_repro.sh`
