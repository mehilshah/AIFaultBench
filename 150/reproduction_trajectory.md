# Reproduction Trajectory — Bug 150: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/42502](https://github.com/huggingface/transformers/issues/42502)
- **Repository:** huggingface/transformers @ `cac0a28`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install runtime dependencies from requirements.txt via setup_env.sh
2. Run repro.py against the local transformers source tree
3. Observe the tensor-label failure and the list-label success path

## Observed behavior

- With local codebase/src on PYTHONPATH, DataCollatorWithFlattening(return_tensors="pt") raised TypeError('can only concatenate list (not "Tensor") to list') when features contained tensor labels.
- The list-label control case succeeded and produced flattened input_ids, labels, and position_ids.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
