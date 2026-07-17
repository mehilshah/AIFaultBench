# Repro Bundle

This folder reproduces the `FlowMatchEulerDiscreteScheduler.set_timesteps` mismatch described in `bug_report.txt`.

## What it shows

With `shift=3.0`:

- `set_timesteps(num_inference_steps=2, timesteps=[1000.0, 2.99401209])` keeps the manual timestep values.
- `set_timesteps(num_inference_steps=2)` generates a different timestep list.
- Both calls produce the same sigma schedule.

That means the model can receive different timestep labels for the same noise schedule.

## Run

```bash
bash run_repro.sh
```

The script writes stdout to `repro_stdout.log` and stderr to `repro_stderr.log`.
