# Reproduction Trajectory — Bug 120: stable_baselines3

- **Bug report:** [https://github.com/DLR-RM/stable-baselines3/issues/1634](https://github.com/DLR-RM/stable-baselines3/issues/1634)
- **Repository:** DLR-RM/stable-baselines3 @ `ba77dd7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the runtime dependencies from `requirements.txt`.
2. Loaded `codebase/stable_baselines3/common/logger.py` directly with `importlib` so the repro stays focused on the logger implementation.
3. Logged both a `np.ndarray` and a `torch.Tensor` through `TensorBoardOutputFormat`, then read the generated TensorBoard event files with `EventAccumulator`.

## Observed behavior

- Running `bash run_repro.sh` produced TensorBoard histogram keys for `torch` only. `repro_stdout.log` shows `histograms=['torch']`, `compressed_histograms=['torch']`, and `observed_histograms=['torch']`. `repro_stderr.log` ends with `AssertionError: np.ndarray was not logged as a histogram`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
