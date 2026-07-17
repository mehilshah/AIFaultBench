# Reproduction Trajectory — Bug 598: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/993](https://github.com/huggingface/accelerate/issues/993)
- **Repository:** huggingface/accelerate @ `b22f088ff662de748cf3f97c7ad8bf5a6dd6a7b9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Set up a Python 3.11 venv with the local accelerate source installed editable.
2. Run bash run_repro.sh.
3. Confirm that dispatch_model breaks the tied embed/head relationship when the embedding is offloaded to disk.

## Observed behavior

- The repro script shows the alias is broken after dispatch: pre_dispatch_shared=True, post_dispatch_shared=False, and post_dispatch_named_parameters=['embed_tokens.weight', 'lm_head.weight']. The script then restores the alias with tie_weights(), matching the reported failure mode.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
