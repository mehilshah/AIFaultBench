# Reproduction Trajectory — Bug 464: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46899](https://github.com/huggingface/transformers/issues/46899)
- **Repository:** huggingface/transformers @ `c96378c4136f5882fee50d8ff8ee1e9588a17eb6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated venv with `bash setup_env.sh`.
2. Run the reduced Gemma4 multimodal repro with `bash run_repro.sh`.
3. Observe the byte-typed multimodal features and the `masked_scatter` dtype mismatch.

## Observed behavior

- Running `bash run_repro.sh` in a clean venv produced `feature_dtype=torch.uint8` from `Gemma4UnifiedMultimodalEmbedder.forward()` and then failed with `RuntimeError: masked_scatter: expected self and source to have same dtypes but gotBFloat16 and Byte`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
