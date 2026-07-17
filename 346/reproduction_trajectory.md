# Reproduction Trajectory — Bug 346: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47116](https://github.com/huggingface/transformers/issues/47116)
- **Repository:** huggingface/transformers @ `eee480d59810135f45280f8db99f14d0136bed82`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local .venv and install the CPU torch wheel plus the minimal runtime dependencies from requirements.txt.
2. Run repro.py against codebase/src via PYTHONPATH.
3. Observe that the generator yields all items before the first preprocess call, proving eager list materialization.

## Observed behavior

- repro_stdout.log shows the generator was exhausted up front: EVENTS ['yield:0', 'yield:1', 'yield:2', 'preprocess:item-0', 'forward:item-0', 'postprocess:item-0', ...]. That ordering matches the regression described in the bug report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
