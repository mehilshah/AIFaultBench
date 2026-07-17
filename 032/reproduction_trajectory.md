# Reproduction Trajectory — Bug 032: DeepLearningExamples

- **Bug report:** [https://github.com/NVIDIA/DeepLearningExamples/issues/1272](https://github.com/NVIDIA/DeepLearningExamples/issues/1272)
- **Repository:** NVIDIA/DeepLearningExamples @ `f613b7c0a8ff252dcbc8cc7747995334198844b3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment and install the bundled Python dependency list.
2. Run `bash run_repro.sh` from the bug folder.
3. Observe the TypeError emitted from `codebase/PyTorch/LanguageModeling/BERT/modeling.py:122`.

## Observed behavior

- Running `bash run_repro.sh` loads `codebase/PyTorch/LanguageModeling/BERT/modeling.py` and fails at `return torch.nn.functional.gelu(x, approximate=True)` with `TypeError: gelu(): argument 'approximate' must be str, not bool`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
