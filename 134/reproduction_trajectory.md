# Reproduction Trajectory — Bug 134: flair

- **Bug report:** [https://github.com/flairNLP/flair/issues/3684](https://github.com/flairNLP/flair/issues/3684)
- **Repository:** flairNLP/flair @ `d4ea377`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install the repro requirements.
2. Run `bash run_repro.sh` from the standardized bug folder.
3. Observe the expected ImportError for `flair.datasets.WIKINER_FRENCH` in the captured logs.

## Observed behavior

- Running `from flair.datasets import WIKINER_FRENCH` against the local `codebase/` raises `ImportError: cannot import name 'WIKINER_FRENCH' from 'flair.datasets'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
