# Reproduction Trajectory — Bug 266: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/39167](https://github.com/jax-ml/jax/issues/39167)
- **Repository:** jax-ml/jax @ `4e85fb88cdac6818d820d8f36b99427b01ec6d58`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a repro bundle around the local JAX source checkout and TensorFlow import sequence from the bug report.
2. Added a runtime preflight that checks for two GPU devices before attempting the collective.
3. Prepared the baseline and TensorFlow-import-first runs to mirror the report when the hardware precondition is met.
4. Captured the local outcome in repro_stdout.log and repro_stderr.log.

## Observed behavior

- After installing the editable local JAX source tree and TensorFlow 2.21.0, both runs printed `jax.devices(): [CpuDevice(id=0)]`, `gpu devices: []`, and exited with code 2 after the explicit `BLOCKED` message. The TensorFlow-import-first path never reached NCCL.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

No multi-GPU CUDA runtime is available in this environment, so the NCCL communicator path from the report cannot be exercised.
