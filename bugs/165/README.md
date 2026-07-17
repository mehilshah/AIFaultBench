# Kornia PadTo repro

This bundle reproduces the `PadTo` behavior described in `bug_report.txt`.

## What happens

`kornia.augmentation.PadTo((5, 5))` is applied to a `10x10` tensor. Instead of
raising an error or leaving the image unchanged, it returns the top-left `5x5`
crop because `torch.nn.functional.pad` accepts negative padding and crops.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

## Expected result

`repro.py` raises an `AssertionError` after printing the cropped output shape
and tensor contents to `repro_stdout.log`.
