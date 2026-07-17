# Bug 385

Reproduction bundle for TorchRL issue https://github.com/pytorch/rl/issues/3702.

## What this shows

`torchrl.envs.libs.pettingzoo.PettingZooWrapper._update_action_mask` raises a `KeyError` when a `ParallelEnv` removes an agent from the observation dict while `done_on_any=False` and action masks are enabled.

The bundled repro uses a minimal custom PettingZoo `ParallelEnv` that:

- starts with two agents,
- exposes an `action_mask` in each observation,
- drops `agent_1` after the first step,
- keeps `done_on_any=False` so the wrapper continues instead of resetting.

## Expected result

Running `./run_repro.sh` should produce `reproduction.json` with `reproducible: true` and a `KeyError` evidence string.

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: local venv setup
- `run_repro.sh`: executes the repro
- `manifest.json`: standardized metadata
- `reproduction.json`: structured result written by the repro
- `repro_stdout.log`, `repro_stderr.log`: captured run output
