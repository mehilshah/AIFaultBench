# Reproduction Trajectory — Bug 385: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3702](https://github.com/pytorch/rl/issues/3702)
- **Repository:** pytorch/rl @ `80381880145591e3546c9bbe850bcbe277d8bfa3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a custom PettingZoo ParallelEnv with two agents and per-agent action masks.
2. Wrap it with torchrl.envs.libs.pettingzoo.PettingZooWrapper using use_mask=True and done_on_any=False.
3. Reset the wrapper, then step once after the environment drops agent_1 from the active observation dict.

## Observed behavior

- KeyError raised from PettingZooWrapper._update_action_mask when accessing a missing agent key: KeyError('agent_1').

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
