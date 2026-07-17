# Reproduction Trajectory — Bug 070: DeepSpeedExamples

- **Bug report:** [https://github.com/deepspeedai/DeepSpeedExamples/issues/948](https://github.com/deepspeedai/DeepSpeedExamples/issues/948)
- **Repository:** deepspeedai/DeepSpeedExamples @ `476f600be931e77b1d819ff05cc78709608d5269`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` from the bug folder.
2. The script creates a venv, installs `torch==2.5.1` and `deepspeed==0.16.0`, initializes `torch.distributed`, and then calls `deepspeed.comm.all_reduce(...)`.
3. The call fails with the same `NoneType.all_reduce` traceback reported in the issue.

## Observed behavior

- repro_stdout.log shows torch.distributed initialized successfully while deepspeed.comm.cdb remained None.
- repro_stderr.log ends with AttributeError: 'NoneType' object has no attribute 'all_reduce' from deepspeed.comm.all_reduce.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
