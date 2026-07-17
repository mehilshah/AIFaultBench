# Bug 628

This folder contains a self-contained repro for the TorchRL collector bug from
https://github.com/pytorch/rl/issues/3240.

What the repro does:
- validates that a `ParallelEnv` rollout can be extended into a replay buffer
  outside the collector
- starts a `MultiSyncDataCollector` with the same `ParallelEnv` factory and a
  replay buffer
- times out before the first collector batch is yielded

Files:
- `repro.py`: the actual repro
- `requirements.txt`: Python dependencies for the isolated venv
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `reproduction.json`: machine-readable result

Observed status in this snapshot:
- `MultiSyncDataCollector` reproducibly hangs during the first collection when
  `replay_buffer` is provided
- the simpler `aSyncDataCollector` CPU-only variant did not reproduce in this
  environment
