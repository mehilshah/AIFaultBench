# Reproduction Trajectory — Bug 050: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1898](https://github.com/keras-team/keras-io/issues/1898)
- **Repository:** keras-team/keras-io @ `3e3467de2b61a5af6291dcf860089885614d58ad`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a venv and install `keras==3.4.1`, `torch==2.3.1`, and `numpy==1.26.4` with `bash setup_env.sh`.
2. Run `bash run_repro.sh` to execute the GAN sample against a `torch.utils.data.DataLoader`.
3. Observe that `train_step()` receives a `list` batch and crashes when it accesses `real_images.shape`.

## Observed behavior

- `bash run_repro.sh` prints `batch type: list` and then fails at `batch_size = real_images.shape[0]` with `AttributeError: 'list' object has no attribute 'shape'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
