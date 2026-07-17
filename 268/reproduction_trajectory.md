# Reproduction Trajectory — Bug 268: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14195](https://github.com/huggingface/diffusers/issues/14195)
- **Repository:** huggingface/diffusers @ `bc529a5f677db9c4b3fc72c76962c4e2f61567e1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the local reproduction environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh`, which executes `repro.py` twice in separate fresh processes: once with `HF_HUB_OFFLINE=1` and once with `local_files_only=True`.
3. Observe that both runs create a temporary `adapter.safetensors` file and then fail with the offline-mode `weight_name` ValueError.

## Observed behavior

- Both fresh-process reproductions fail on the local temporary LoRA directory. The `HF_HUB_OFFLINE=1` case and the `local_files_only=True` case both raise `ValueError: When using the offline mode, you must specify a weight_name.` from `codebase/src/diffusers/loaders/lora_base.py:_best_guess_weight_name()`. The saved logs show the failure occurs before any successful LoRA loading.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
