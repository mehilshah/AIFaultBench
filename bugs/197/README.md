# Reproduction Bundle

This bundle reproduces the DiceMetric reduction bug described in `bug_report.txt`.

## What it checks

The repro constructs three batches of `BCHW` tensors, feeds them into `monai.metrics.DiceMetric`,
and verifies the output shapes for:

- `reduction="mean_batch"`: expected shape `(3,)`
- `reduction="mean_channel"`: expected shape `(5,)`

In this codebase snapshot the observed shapes are swapped:

- `mean_batch` returns `(5,)`
- `mean_channel` returns `(12,)`

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The run writes stdout to `repro_stdout.log` and stderr to `repro_stderr.log`.
