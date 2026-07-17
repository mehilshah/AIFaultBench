# Reproduction Trajectory — Bug 287: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/8003](https://github.com/deepspeedai/DeepSpeed/issues/8003)
- **Repository:** microsoft/DeepSpeed @ `a7811998498f9d1a8f869af7dab04a46e4ba2c65`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the DeepSpeed `io` modules directly from `codebase/deepspeed/io/` with small stubs for `deepspeed.accelerator` and `deepspeed.ops.op_builder`.
2. Create a `FastFileWriter`, call `close()`, unlink the file, and repeat for 20 iterations.
3. Count deleted file descriptors under `/proc/<pid>/fd` and observe that the count matches the number of iterations.

## Observed behavior

- Running `bash run_repro.sh 20` produced `iterations=20`, `deleted_fds=20`, and 20 leaked `/proc/<pid>/fd` entries pointing at deleted checkpoint files.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh 20
```
