# Reproduction Trajectory — Bug 072: DeepSpeedExamples

- **Bug report:** [https://github.com/deepspeedai/DeepSpeedExamples/issues/924](https://github.com/deepspeedai/DeepSpeedExamples/issues/924)
- **Repository:** deepspeedai/DeepSpeedExamples @ `957ae3141946daf9a6bc5731e261032a13a82f05`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspected `bug_report.txt` and confirmed the reported traceback points to `main.py:367`.
2. Verified the codebase still contains `print_throughput(model.model, args, end - start, args.global_rank)` at `codebase/applications/DeepSpeed-Chat/training/step1_supervised_finetuning/main.py:367`.
3. Ran `bash run_repro.sh > repro_stdout.log 2> repro_stderr.log`.
4. Observed the expected `AttributeError` in `repro_stderr.log` and exit status 1.

## Observed behavior

- Running `bash run_repro.sh` exits with status 1 and raises `AttributeError: 'DeepSpeedEngine' object has no attribute 'model'`. The failing repository line is `codebase/applications/DeepSpeed-Chat/training/step1_supervised_finetuning/main.py:367`, which calls `print_throughput(model.model, ...)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
