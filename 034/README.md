# Bug 034

This folder reproduces the `gelu` API mismatch reported in NVIDIA DeepLearningExamples issue 1187.

Observed bug:
- `codebase/PyTorch/LanguageModeling/BERT/modeling.py:122`
- `torch.nn.functional.gelu(x, approximate=True)` raises `TypeError` on the installed PyTorch build because `approximate` expects a string value.

Files in this bundle:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
1. `bash run_repro.sh`
2. Inspect `repro_stdout.log` and `repro_stderr.log`

Expected outcome:
- The repro exits non-zero and prints a `TypeError` mentioning `gelu(): argument 'approximate' must be str, not bool`.
