# Reproduction Trajectory — Bug 112: albumentations

- **Bug report:** [https://github.com/albumentations-team/albumentations/issues/2527](https://github.com/albumentations-team/albumentations/issues/2527)
- **Repository:** albumentations-team/albumentations @ `218d663`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtual environment and installed the repo-era dependency set from requirements.txt.
2. Imported albumentations from the local codebase with the standardized bug folder on sys.path.
3. Ran the exact MotionBlur reproduction from the bug report with blur_limit=(5, 5), allow_shifted=False, angle_range=(0, 0), and direction_range fixed to -1, 0, and 1.
4. Observed identical kernels for all three direction_range values and confirmed the equality check printed `kernels_all_equal: True`.

## Observed behavior

- Running the report's MotionBlur snippet against the local albumentations code produces the same 5x5 kernel for direction_range values -1, 0, and 1. The saved stdout shows `kernels_all_equal: True` after printing the three identical kernels.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
