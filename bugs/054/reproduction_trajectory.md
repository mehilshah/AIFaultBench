# Reproduction Trajectory — Bug 054: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1711](https://github.com/keras-team/keras-io/issues/1711)
- **Repository:** keras-team/keras-io @ `b124d091b3ee87b6ae6b10ed2707be18e647c81d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read examples/vision/pointnet.py from the local codebase.
2. Verify that test_dataset is created from test_points and test_labels.
3. Verify that model.fit passes validation_data=test_dataset.

## Observed behavior

- source_file=codebase/examples/vision/pointnet.py | fit_line=263 | test_dataset_line=148 | ast_validation_arg='test_dataset' | finding=validation_data is bound to test_dataset, which is constructed from the test split | ast_fit_lineno=263

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
