# Reproduction Trajectory — Bug 066: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1160](https://github.com/keras-team/keras-io/issues/1160)
- **Repository:** keras-team/keras-io @ `b56f87af9e968003666e61f88185a93ff0f0eee8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` in the standardized bug folder.
2. Observe the script output showing the MIRNet source file and the relevant line numbers.
3. Confirm that level2_dau_2 is assigned once and that the final SKFF call uses level3_dau_2 twice.

## Observed behavior

- In codebase/examples/vision/mirnet.py, line 347 assigns level2_dau_2, but line 352 calls selective_kernel_feature_fusion(level1_dau_2, level3_dau_2, level3_dau_2). The final SKFF call repeats level3_dau_2 and does not consume level2_dau_2.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
