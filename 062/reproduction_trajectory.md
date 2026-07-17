# Reproduction Trajectory — Bug 062: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1518](https://github.com/keras-team/keras-io/issues/1518)
- **Repository:** keras-team/keras-io @ `12795962e429e758d5b97b4755b7c635bff51b9a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create two small pandas DataFrames.
2. Call `train_df.append(test_df)` to mirror the masked_language_modeling example.
3. Observe the pandas 2.x AttributeError because `append` no longer exists.

## Observed behavior

- With pandas 2.2.3 in the local venv, running `bash run_repro.sh` prints `About to call train_df.append(test_df)` and then fails with `AttributeError: 'DataFrame' object has no attribute 'append'. Did you mean: '_append'?` at `repro.py:23`, matching `codebase/examples/nlp/masked_language_modeling.py:114`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
