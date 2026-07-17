# Reproduction Trajectory — Bug 399: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/3599](https://github.com/pytorch/rl/issues/3599)
- **Repository:** pytorch/rl @ `f54a7c70c6ddc342867ac113bf12b908404df79c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Checked out TorchRL commit 61e05b3d9a967c0cbbda2e355859287ce7221f52, which still calls torchvision.io.write_video in CSVExperiment.add_video.
2. Installed an isolated CPU wheel set for torch 2.13.0, torchvision 0.28.0, tensordict 0.11.0, and pyvers into deps/.
3. Ran repro.py with PYTHONPATH=deps:codebase and triggered CSVLogger.log_video(..., video_format='mp4').

## Observed behavior

- Running the pre-fix TorchRL checkout with torchvision 0.28.0+cpu prints `torchvision.io.write_video exists= False` and then fails in `torchrl/record/loggers/csv.py:102` with `AttributeError: module 'torchvision.io' has no attribute 'write_video'. Did you mean: 'write_file'?`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
