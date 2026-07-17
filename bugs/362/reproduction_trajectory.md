# Reproduction Trajectory — Bug 362: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14013](https://github.com/huggingface/diffusers/issues/14013)
- **Repository:** huggingface/diffusers @ `2d0110f8182d18834d5039b19232e5761023b5f6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean CPU Torch virtual environment and installed the minimal runtime dependencies from `requirements.txt`.
2. Ran `repro.py` against `codebase/src` using `FlowMatchEulerDiscreteScheduler(shift=3.0)`.
3. Observed that the manual custom-timestep path and the automatic path produce identical sigmas but different timestep values.

## Observed behavior

- With `shift=3.0`, `set_timesteps(num_inference_steps=2, timesteps=[1000.0, 2.99401209])` produced timesteps `[1000.0, 2.9940121173858643]` and sigmas `[1.0, 0.008928571827709675, 0.0]`.
- With the same scheduler config, `set_timesteps(num_inference_steps=2)` produced timesteps `[1000.0, 8.928571701049805]` and the same sigmas `[1.0, 0.008928571827709675, 0.0]`.
- The saved `repro_stdout.log` shows the mismatch directly: manual and automatic schedules share sigmas, but not timestep labels.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
