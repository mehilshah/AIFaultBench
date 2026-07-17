# Reproduction Trajectory — Bug 010: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11117](https://github.com/tensorflow/models/issues/11117)
- **Repository:** tensorflow/models @ `19ce8ecda0732e52d943ccdf540a5659d103c2fc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install dependencies with `bash setup_env.sh`.
2. Run the harness with `bash run_repro.sh`.
3. Observe that the task validation losses reported by the real Model Garden code are both `0.0`.

## Observed behavior

- Running `bash run_repro.sh` produced `{"maskrcnn_validation_loss": 0.0, "semantic_segmentation_validation_loss": 0.0}` in `repro_stdout.log`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
