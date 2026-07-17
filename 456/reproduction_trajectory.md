# Reproduction Trajectory — Bug 456: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2555](https://github.com/huggingface/pytorch-image-models/issues/2555)
- **Repository:** huggingface/pytorch-image-models @ `e6ab6bc3c6f40b5a9600051309eb5b1933845501`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Cloned `huggingface/pytorch-image-models` at `e6ab6bc3c6f40b5a9600051309eb5b1933845501` into `codebase/`.
2. Created a Python 3.9 virtual environment with `uv venv --python 3.9 .venv` via `setup_env.sh`.
3. Ran `bash run_repro.sh`, which executes `repro.py` and triggers the import-time `TypeVar | None` `TypeError`.
4. Confirmed the same `TypeError` with a direct Python 3.9 snippet using `TypeVar` and `F | None`.

## Observed behavior

- Running `bash setup_env.sh && bash run_repro.sh` in the generated Python 3.9.25 environment raises `TypeError: unsupported operand type(s) for |: 'TypeVar' and 'NoneType'` at the `def nullwrap(fn: F | None = None)` line. `repro_stdout.log` shows the matched source line from `codebase/timm/layers/typing.py`, and `repro_stderr.log` contains the traceback.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
