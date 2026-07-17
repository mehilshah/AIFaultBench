# Reproduction Trajectory — Bug 255: tutorials

- **Bug report:** [https://github.com/pytorch/tutorials/issues/3649](https://github.com/pytorch/tutorials/issues/3649)
- **Repository:** pytorch/tutorials @ `86b1c62`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Located the timing helper in the checked-in torch_compile tutorial source.
2. Compared it with the corrected helper in the related full example.
3. Ran `bash run_repro.sh` to capture the mismatch in the local logs.

## Observed behavior

- codebase/intermediate_source/torch_compile_tutorial.py:166 contains `return result, start.elapsed_time(end) / 1024`.
- codebase/intermediate_source/torch_compile_full_example.py:75 contains `return result, start.elapsed_time(end) / 1000`.
- repro_stdout.log shows a 1024.0 ms example being reported as 1.000 s by the tutorial helper, while the correct value is 1.024 s.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
