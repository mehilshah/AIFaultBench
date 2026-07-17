# Reproduction Trajectory — Bug 557: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13703](https://github.com/huggingface/diffusers/issues/13703)
- **Repository:** huggingface/diffusers @ `d773308ca726766d6d2867f1fb8732df3d1dc5a3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python 3.12 virtualenv and installed the minimal runtime dependencies for the local diffusers checkout.
2. Ran the default UNet1DModel configuration from the report and compared the same input at two different timesteps.
3. Ran the no-skip configuration from the report and confirmed the output changes with timestep.

## Observed behavior

- In the scripted repro, the default UNet1DModel config produced identical outputs for timestep 0 vs 10 (max abs diff 0.0), while the no-skip/time-aware config from the report produced different outputs (max abs diff 0.45627978444099426).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
