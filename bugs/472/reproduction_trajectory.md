# Reproduction Trajectory — Bug 472: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/3463](https://github.com/pytorch/rl/issues/3463)
- **Repository:** pytorch/rl @ `ab49b59dd37a4210f1d0102b89b7b00340217cf1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtual environment and installed torch 2.8.0 plus tensordict 0.11.0.
2. Ran the bundled repro against codebase/ab49b59dd37a4210f1d0102b89b7b00340217cf1 with PYTHONPATH pointing at the local source tree.
3. Observed a corrupted sample from TensorDictReplayBuffer during concurrent extend() and sample() on LazyTensorStorage(device='cuda:0').

## Observed behavior

- On CUDA hardware, the bundled repro reported CORRUPTION at step=375: the sampled value at storage_coord (13, 2) was expected=1475 but got_obs=1450.0 and got_traj=1450.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
