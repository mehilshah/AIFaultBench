# Reproduction Trajectory — Bug 315: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47276](https://github.com/huggingface/transformers/issues/47276)
- **Repository:** huggingface/transformers @ `63f32a8782cb70da3365acab16f2b67947737985`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated environment with `bash setup_env.sh`.
2. Run the reproduction with `bash run_repro.sh`.
3. Observe the warning line `synced_gpus is not ignored for continuous batching. Got synced_gpus = True` in the captured logs.

## Observed behavior

- Running `model.generate(input_ids, synced_gpus=True, cache_implementation='paged')` on a tiny GPT-2 config emits `synced_gpus is not ignored for continuous batching. Got synced_gpus = True`, matching the bug report's misleading wording.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
