# Reproduction Trajectory — Bug 624: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/903](https://github.com/huggingface/accelerate/issues/903)
- **Repository:** huggingface/accelerate @ `e9d15e59732fab5a123f61ec7ccb6dd41e207542`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Loaded codebase/src/accelerate/commands/launch.py through a stubbed accelerate runtime so the broken system torch install would not interfere.
2. Parsed the reported command line: --multi_gpu --gpu_ids 0,1,2,3 --mixed_precision no --num_machines 1 --num_processes 1 --num_cpu_threads_per_process=1.
3. Called launch_command(args) and observed multi_gpu_launcher invoked with no validation error.

## Observed behavior

- launch_command accepted --multi_gpu with --num_processes 1 and invoked multi_gpu_launcher instead of rejecting the combination.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
