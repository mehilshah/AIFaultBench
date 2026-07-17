# Reproduction Trajectory — Bug 073: DeepSpeedExamples

- **Bug report:** [https://github.com/deepspeedai/DeepSpeedExamples/issues/940](https://github.com/deepspeedai/DeepSpeedExamples/issues/940)
- **Repository:** deepspeedai/DeepSpeedExamples @ `be0a0e189714f7e4cb523cb8d40ced1da964153a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` from the standardized folder root.
2. Inspect `repro_stderr.log` for the traceback showing `cdb` is still None when `all_reduce()` is called.

## Observed behavior

- Running `python3 repro.py` raises `AttributeError: 'NoneType' object has no attribute 'all_reduce'` at the unguarded `cdb.all_reduce(...)` call in `repro.py:19`, matching the DeepSpeed Domino report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
