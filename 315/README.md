# Reproduction Bundle

This bundle reproduces the continuous batching warning text from the bug report.

## Setup

```bash
bash setup_env.sh
```

## Run

```bash
bash run_repro.sh
```

## Expected result

The run prints the warning:

```text
synced_gpus is not ignored for continuous batching. Got synced_gpus = True
```

The run also records the exact warning output in `repro_stdout.log` and `repro_stderr.log`.
