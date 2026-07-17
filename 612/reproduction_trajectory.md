# Reproduction Trajectory — Bug 612: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7710](https://github.com/deepspeedai/DeepSpeed/issues/7710)
- **Repository:** microsoft/DeepSpeed @ `7f2f423257592725259a0950094dc9fe9d276a27`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read bug_report.txt and located the failing ZeRO-2 gradient reduction path in codebase/deepspeed/runtime/zero/stage_1_and_2.py.
2. Created a minimal source-level harness in repro.py that reproduces the empty-bucket access.
3. Ran ./run_repro.sh and captured stdout/stderr in repro_stdout.log and repro_stderr.log.

## Observed behavior

- repro_stdout.log shows the offending DeepSpeed source line: self.average_tensor(bucket.buffer[bucket.index].narrow(0, 0, bucket.elements), comm_dtype)
- repro_stderr.log ends with IndexError: list index out of range from Harness().reduce_ipg_grads()
- codebase/deepspeed/runtime/zero/stage_1_and_2.py:1499 contains the same direct bucket.buffer[bucket.index] access

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
