# Reproduction Trajectory — Bug 305: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/2381](https://github.com/huggingface/peft/issues/2381)
- **Repository:** huggingface/peft @ `1e2d6b5832401e07e917604dfb080ec474818f2b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv and installed the PEFT runtime dependencies.
2. Instantiated a small `BertForSequenceClassification` model and wrapped it with `LoraConfig(task_type=TaskType.SEQ_CLS)`.
3. Added the `delete_me` adapter, verified it appeared in `classifier.modules_to_save`, then called `delete_adapter('delete_me')`.
4. Observed that `delete_me` was still present in `classifier.modules_to_save`, causing the assertion to fail.

## Observed behavior

- Running the repro leaves the deleted adapter in `model.base_model.classifier.modules_to_save`: stdout shows `before_delete=['default', 'delete_me']` and `after_delete=['default', 'delete_me']`, and stderr ends with `AssertionError` from the post-delete check.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
