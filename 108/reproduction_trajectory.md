# Reproduction Trajectory — Bug 108: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/42502](https://github.com/huggingface/transformers/issues/42502)
- **Repository:** huggingface/transformers @ `cac0a28c83cf87b7a05495de3177099c635ba852`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python venv and installed the minimal runtime dependencies listed in requirements.txt.
2. Executed repro.py with PYTHONPATH pointed at codebase/src.
3. Observed the tensor-label failure and the successful list-label case in the same run.

## Observed behavior

- Running DataCollatorWithFlattening on features whose labels are torch.Tensor objects raises TypeError('can only concatenate list (not "Tensor") to list').
- The same collator succeeds when labels are provided as Python lists, producing flattened input_ids, labels, and position_ids.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
