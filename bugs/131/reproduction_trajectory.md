# Reproduction Trajectory — Bug 131: flair

- **Bug report:** [https://github.com/flairNLP/flair/issues/3489](https://github.com/flairNLP/flair/issues/3489)
- **Repository:** flairNLP/flair @ `9f403b9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a sentence with both `regression_label` and an unrelated string label.
2. Instantiate `TextRegressor` with `label_name='regression_label'` and a tiny local `DocumentEmbeddings` implementation.
3. Call `forward_loss([sentence])` through `bash run_repro.sh`.
4. Observe that the model still iterates over all labels and crashes on the unrelated string label.

## Observed behavior

- Running `bash run_repro.sh` prints `sentence labels: [(4.5, 1.0), ('bar', 1.0)]` and then fails in `TextRegressor._labels_to_tensor` with `ValueError: could not convert string to float: 'bar'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
