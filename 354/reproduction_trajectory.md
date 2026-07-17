# Reproduction Trajectory — Bug 354: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/2236](https://github.com/facebookresearch/detectron2/issues/2236)
- **Repository:** facebookresearch/detectron2 @ `137745de04797fa488a2bc86955795e91318b8ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny RGB test image.
2. Apply the same BGR channel reversal used by detectron2's image-loading path.
3. Convert the resulting NumPy view with torch.from_numpy(...).
4. Observe the negative-stride ValueError.

## Observed behavior

- run_repro.sh prints a NumPy image with strides (6, 3, -1), then torch.from_numpy(image).permute(2, 0, 1) raises ValueError: At least one stride in the given numpy array is negative.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
