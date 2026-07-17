# Reproduction Trajectory — Bug 641: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3238](https://github.com/pytorch/rl/issues/3238)
- **Repository:** pytorch/rl @ `8570c25a745da54ca647b8a70231112f063d1421`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a two-worker MultiSyncDataCollector on GymEnv(Pendulum-v1) with frames_per_batch=200, max_frames_per_traj=50, cat_results=0, and split_trajs=True.
2. Call collector.set_seed(42) before iterating.
3. Iterate the collector until the first batch is split into trajectories.
4. Observe the failure in torchrl.collectors.utils.split_trajectories when torch.Tensor.split receives mismatched split sizes.

## Observed behavior

- Running MultiSyncDataCollector with split_trajs=True and collector.set_seed(42) raises RuntimeError: split_with_sizes expects split_sizes to sum exactly to 200 but got split_sizes=[100, 50, 100, 50].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
