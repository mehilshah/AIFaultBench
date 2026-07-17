# Flair TextRegressor repro

This bundle reproduces the `TextRegressor._labels_to_tensor` bug described in `bug_report.txt`.

The failure is triggered by a sentence that has both:

- the regression label named by `label_name`
- an unrelated string label

`TextRegressor.forward_loss()` still iterates over `sentence.labels` instead of filtering to `self.label_name`, so it tries to convert `"bar"` to `float`.

## Run locally

```bash
bash setup_env.sh
bash run_repro.sh
```

## Expected result

The run fails with:

```text
ValueError: could not convert string to float: 'bar'
```
