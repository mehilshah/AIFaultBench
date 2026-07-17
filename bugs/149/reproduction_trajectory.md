# Reproduction Trajectory — Bug 149: sentence-transformers

- **Bug report:** [https://github.com/huggingface/sentence-transformers/issues/3617](https://github.com/huggingface/sentence-transformers/issues/3617)
- **Repository:** huggingface/sentence-transformers @ `f5f6249`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtual environment with setup_env.sh.
2. Run run_repro.sh to execute repro.py.
3. Observe the import failure in repro_stderr.log.

## Observed behavior

- A clean virtual environment installed only huggingface_hub and tqdm, with requests absent.
- Running repro.py against codebase/sentence_transformers/util/file_io.py failed at the top-level `import requests`.
- The captured stderr contains `ModuleNotFoundError: No module named 'requests'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
