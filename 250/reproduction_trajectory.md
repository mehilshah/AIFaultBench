# Reproduction Trajectory — Bug 250: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/2404](https://github.com/pytorch/rl/issues/2404)
- **Repository:** pytorch/rl @ `e82a69f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a TensorDictReplayBuffer with pin_memory=True and a custom transform that returns a new TensorDict without an explicit device.
2. Added 100 observation batches to a LazyMemmapStorage-backed replay buffer.
3. Sampled from the buffer and observed that the returned observation tensor was on CPU but not pinned.

## Observed behavior

- Running `./run_repro.sh` with torch=2.4.0+cpu and tensordict=0.5.0 printed `sample.device=None`, `observation.device=cpu`, and `observation.is_pinned=False`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
