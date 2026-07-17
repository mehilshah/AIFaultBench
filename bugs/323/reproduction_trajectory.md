# Reproduction Trajectory — Bug 323: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/3405](https://github.com/facebookresearch/detectron2/issues/3405)
- **Repository:** facebookresearch/detectron2 @ `05bc8439ca10e11300d9d34e4fe0dd1d3f42773a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment and installed the minimal runtime dependencies from `requirements.txt`.
2. Loaded `detectron2.data.common.MapDataset` from the local `codebase/` while bypassing `detectron2.__init__`.
3. Constructed `MapDataset` with a list-backed dataset and an identity map function.
4. Observed the `object.__new__()` `TypeError` from `MapDataset.__new__`.

## Observed behavior

- Running `bash run_repro.sh` creates a clean venv, installs `torch==2.13.0+cpu`, `numpy`, and `cloudpickle`, then fails when constructing `MapDataset([{"x": 1}], lambda x: x)`. The traceback points to `codebase/detectron2/data/common.py:77` and ends with `TypeError: object.__new__() takes exactly one argument (the type to instantiate)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
