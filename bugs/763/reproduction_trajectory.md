# Reproduction Trajectory — Bug 763: dspy

- **Bug report:** [https://github.com/stanfordnlp/dspy/issues/8917](https://github.com/stanfordnlp/dspy/issues/8917)
- **Repository:** stanfordnlp/dspy @ `eacbcdd8501527e3b9898c46f7b9758e461a9f95`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the pinned source SHA. The initial clone had transferred no commit objects, so I explicitly fetched and checked out that same SHA.
2. Created `.venv` and installed the pinned dependencies and the local checkout.
3. Ran `bash run_repro.sh`, which imports DSPy and looks up the reported `dspy.AzureOpenAI` API without configuring a model or sending any provider request.

## Observed behavior

- The lookup raises `AttributeError: module 'dspy' has no attribute 'AzureOpenAI'` and the script exits with status 1.
- The pinned `dspy/__init__.py` imports `dspy.clients` but has no `AzureOpenAI` export.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
