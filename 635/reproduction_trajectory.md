# Reproduction Trajectory — Bug 635: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13462](https://github.com/huggingface/diffusers/issues/13462)
- **Repository:** huggingface/diffusers @ `5063aa5566f068b68bba799b6604e9ac14eaf37c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Imported the real `annotate_pipeline()` helper from `codebase/examples/profiling/profiling_utils.py`.
2. Annotated a dummy scheduler method exactly as the profiling code does.
3. Deep-copied the scheduler to simulate the LTX2 audio scheduler duplication path.
4. Called `audio_scheduler.step('audio')` and observed that it mutated the original scheduler instance instead of the copy.

## Observed behavior

- Running `bash run_repro.sh` showed that the copied scheduler's wrapper captured the original scheduler id, `audio_scheduler.step('audio')` incremented `original_step_index` to 1 while `copied_step_index` stayed 0, and the wrapper reported `self_id` equal to the original scheduler.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
