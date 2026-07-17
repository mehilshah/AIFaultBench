# Reproduction Trajectory — Bug 151: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/42762](https://github.com/huggingface/transformers/issues/42762)
- **Repository:** huggingface/transformers @ `471d7ce`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtualenv and install the missing Python packages with `bash setup_env.sh`.
2. Run `bash run_repro.sh` with `PYTHONPATH` pointing at `codebase/src`.
3. Observe that `_prepare_generation_config()` rewrites explicit `temperature=1.0` to the model default `1e-06`.

## Observed behavior

- The repro script prints `custom_config.temperature=1.0` and then `prepared_config.temperature=1e-06`, and stderr includes the warning that generation_config defaults were modified to model-specific defaults.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
