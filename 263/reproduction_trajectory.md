# Reproduction Trajectory — Bug 263: tianshou

- **Bug report:** [https://github.com/thu-ml/tianshou/issues/1272](https://github.com/thu-ml/tianshou/issues/1272)
- **Repository:** thu-ml/tianshou @ `be657fa`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a DummyEnv with a 1D int32 observation and wrap it in gymnasium.wrappers.FrameStack(3).
2. Run the wrapped envs through tianshou.env.DummyVectorEnv and tianshou.env.ShmemVectorEnv with the same actions.
3. Compare the first post-step observation: DummyVectorEnv updates the frame stack, while ShmemVectorEnv remains frozen at the reset value.

## Observed behavior

- The repro prints that DummyVectorEnv advances the stacked frames, but ShmemVectorEnv stays at [[[0], [0], [0]]] for step_0 through step_2. The script finishes with: BUG_REPRODUCED: ShmemVectorEnv keeps returning the reset frame stack after step().

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
