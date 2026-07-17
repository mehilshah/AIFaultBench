# Reproduction Bundle

This bundle reproduces the Accelerate bug from issue 1116.

## What fails

When a multi-node config uses a single GPU id per node, for example `gpu_ids: "0"`, `accelerate.commands.launch.launch_command`
sets `args.multi_gpu = False` and falls back to `simple_launcher`. That ignores `num_machines > 1` and prevents the multi-node
launcher path from being used.

## How the repro works

`repro.py` creates two temporary configs:

1. `gpu_ids: "0"` should still use the multi-node launcher, but the buggy code selects `simple_launcher`.
2. `gpu_ids: "all"` takes the multi-GPU launcher path as expected.

The script monkeypatches the launcher functions so it records control flow without starting real distributed jobs.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
cat repro_stdout.log
cat repro_stderr.log
```
