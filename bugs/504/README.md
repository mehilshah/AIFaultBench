# Bug 504 Reproduction

This folder reproduces the `StepCounter` MARL key-propagation issue from torchrl issue `#3400`.

What the repro shows:
- `NestedCountingEnv(has_root_done=True, nest_done=True)` exposes both a root `done` key and nested `data/done` keys.
- `StepCounter(max_steps=2)` only creates `step_count` and `truncated` at the root level.
- Nested `next/data/step_count` and `next/data/truncated` are missing even though the nested `done` entries exist.

How to run:
- `bash setup_env.sh`
- `bash run_repro.sh`

Evidence:
- `repro_stdout.log` contains the printed key sets.
- The repro ends with `AssertionError: StepCounter did not create a nested step_count key`.
