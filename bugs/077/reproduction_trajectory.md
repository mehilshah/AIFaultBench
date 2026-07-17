# Reproduction Trajectory — Bug 077: Mask_RCNN

- **Bug report:** [https://github.com/matterport/Mask_RCNN/issues/2979](https://github.com/matterport/Mask_RCNN/issues/2979)
- **Repository:** matterport/Mask_RCNN @ `3deaec5d902d16e1daf56b62d5971d428dc920bc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv with `./setup_env.sh` and installed `tensorflow-cpu==2.17.1`.
2. Executed `./run_repro.sh` against one real JPEG from `codebase/images/` and one deliberately missing path.
3. Observed the TensorFlow input pipeline abort with a `NotFoundError` when `tf.io.read_file()` reached the missing image path.

## Observed behavior

- Running `./run_repro.sh` in a fresh virtualenv consistently fails during `model.fit()` with `tensorflow.python.framework.errors_impl.NotFoundError: Graph execution error` and `codebase/images/definitely_missing.jpg; No such file or directory` at `ReadFile`/`IteratorGetNext`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```
