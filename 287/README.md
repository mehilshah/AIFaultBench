# FastFileWriter fd leak repro

This bundle reproduces the `FastFileWriter._fini()` file-descriptor leak from
`codebase/deepspeed/io/fast_file_writer.py`.

## What the repro does

- Loads the `deepspeed.io` writer modules directly from `codebase/`.
- Creates a `FastFileWriter`, closes it, then unlinks the file.
- Repeats the sequence and counts deleted file descriptors under `/proc/<pid>/fd`.

## Expected result

On the buggy code path, `deleted_fds` matches the iteration count.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
