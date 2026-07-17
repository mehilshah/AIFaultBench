# Reproduction Trajectory — Bug 441: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2577](https://github.com/huggingface/pytorch-image-models/issues/2577)
- **Repository:** huggingface/pytorch-image-models @ `818663b8b699d8a47026ac952a3adcbdd6350a67`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Materialize the referenced pytorch-image-models commit with `setup_codebase.sh`.
2. Load `codebase/timm/data/transforms.py` through local torch/torchvision stubs so the broken system torch install is bypassed.
3. Instantiate `ResizeKeepRatio` with `random_scale_range=(0.50, 1.20)` and `random_aspect_range=(0.90, 1.10)`.
4. Observe that `repr()` prints the wrong upper bound `1.100` for `random_scale_range`.
5. Assert that `random_scale_range=(0.500, 1.200)` should appear, which fails.

## Observed behavior

- Running `bash run_repro.sh` loads the local `codebase/timm/data/transforms.py` snapshot and prints `random_scale_range=(0.500, 1.100)` for `ResizeKeepRatio(size=224, random_scale_range=(0.50, 1.20), random_aspect_range=(0.90, 1.10))`. The script then fails an assertion because the expected fragment `random_scale_range=(0.500, 1.200)` is missing.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
