# Reproduction Trajectory — Bug 165: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/2121](https://github.com/kornia/kornia/issues/2121)
- **Repository:** kornia/kornia @ `58a6a47`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Python 3.12 virtual environment with system site packages and installed the local kornia checkout in editable mode from codebase/.
2. Applied kornia.augmentation.PadTo((5, 5), pad_value=0) to a 10x10 tensor with values 0..99.
3. Observed that the output was the top-left 5x5 crop rather than the original image or an exception.

## Observed behavior

- Running PadTo((5, 5), pad_value=0) on a 1x1x10x10 tensor produced output_shape=(1, 1, 5, 5), and the output matched the top-left 5x5 crop of the input. The repro script then raised AssertionError because the transform cropped instead of acting as a no-op or erroring.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
