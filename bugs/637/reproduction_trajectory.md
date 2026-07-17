# Reproduction Trajectory — Bug 637: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/898](https://github.com/huggingface/accelerate/issues/898)
- **Repository:** huggingface/accelerate @ `5315290b55ea9babd95a281a27c51d87b89d7c85`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the virtualenv and install dependencies with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Inspect `repro_stderr.log` for the failing traceback.

## Observed behavior

- accelerate==0.14.0 in a Python 3.10 venv
- Running `accelerate test --config_file sagemaker_default_config.yaml` fails in `accelerate/commands/launch.py`
- Observed traceback: `AttributeError: 'Namespace' object has no attribute 'use_cpu'`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
