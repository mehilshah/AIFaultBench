# Reproduction Trajectory — Bug 182: lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21036](https://github.com/Lightning-AI/pytorch-lightning/issues/21036)
- **Repository:** Lightning-AI/pytorch-lightning @ `791753b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated `.venv` and installed the bug-specific runtime dependencies plus `torch==2.6.0+cpu`.
2. Executed the minimal dataclass repro in `repro.py` against the local Lightning source tree.
3. Observed the expected crash in `save_hyperparameters()` when `not_a_param` is accessed before initialization.

## Observed behavior

- Running `bash run_repro.sh` in a fresh venv with CPU Torch and `codebase/src` on `PYTHONPATH` raises `AttributeError: 'Module' object has no attribute 'not_a_param'`. The traceback points to `codebase/src/lightning/pytorch/utilities/parsing.py:170`, where `fields(obj)` is iterated without filtering `init=False` dataclass fields.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
