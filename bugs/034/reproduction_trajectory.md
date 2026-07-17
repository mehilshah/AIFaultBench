# Reproduction Trajectory — Bug 034: DeepLearningExamples

- **Bug report:** [https://github.com/NVIDIA/DeepLearningExamples/issues/1187](https://github.com/NVIDIA/DeepLearningExamples/issues/1187)
- **Repository:** NVIDIA/DeepLearningExamples @ `0e20ac8e84db2f879c4388b6bcaa11a93a0599a1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal repro script that imports modeling.gelu from codebase/PyTorch/LanguageModeling/BERT/modeling.py.
2. Installed the required runtime dependencies in a local venv via setup_env.sh.
3. Executed bash run_repro.sh and captured stdout/stderr in repro_stdout.log and repro_stderr.log.
4. Observed the expected TypeError complaining that approximate must be a string, not a bool.

## Observed behavior

- Running bash run_repro.sh reproduces a TypeError from codebase/PyTorch/LanguageModeling/BERT/modeling.py:122: 'gelu(): argument 'approximate' must be str, not bool'. The traceback shows the failure occurs when gelu(x) calls torch.nn.functional.gelu(x, approximate=True).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
