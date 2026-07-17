# Reproduction Trajectory — Bug 504: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3400](https://github.com/pytorch/rl/issues/3400)
- **Repository:** pytorch/rl @ `3fe392b63c849e22b9ce10860c0ae2c4de9b6fd1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a TransformedEnv from NestedCountingEnv(has_root_done=True, nest_done=True, max_steps=2) with StepCounter(max_steps=2).
2. Run a short rollout and inspect the produced keys.
3. Verify that root next/done, next/truncated, and next/step_count exist while nested next/data/step_count and next/data/truncated do not.
4. The repro exits with an AssertionError once the missing nested step_count key is checked.

## Observed behavior

- Running the local repro shows root-level StepCounter outputs, but nested next/data step_count and truncated keys are absent even though the env exposes nested data/done keys. The run ends with AssertionError: StepCounter did not create a nested step_count key when a root done key was present.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
