# Bug 088 Reproduction

This bundle reproduces the `align_right` pad-value bug from `x-transformers`.

Bug summary:
- `x_transformers.autoregressive_wrapper.align_right()` accepts `pad_id`
- the implementation currently calls `F.pad(..., value=0)` instead of using `pad_id`
- when `pad_id != 0`, generated left padding is incorrect

Files:
- `repro.py`: minimal assertion-based repro
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: installs Python dependencies
- `run_repro.sh`: runs the repro end to end

Usage:
```bash
bash run_repro.sh
```

Expected result:
- the script fails with an assertion showing that left padding used `0` instead of the requested `pad_id`
