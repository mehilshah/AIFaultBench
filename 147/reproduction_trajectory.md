# Reproduction Trajectory — Bug 147: sentence-transformers

- **Bug report:** [https://github.com/huggingface/sentence-transformers/issues/3325](https://github.com/huggingface/sentence-transformers/issues/3325)
- **Repository:** huggingface/sentence-transformers @ `03dff58`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Prepare the environment with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Inspect `repro_stdout.log` for `BUG_REPRODUCED: encode(..., output_value=None) crashes on prompt_length`.
4. Inspect `repro_stderr.log` for the `TypeError` traceback from `SentenceTransformer.encode()`.

## Observed behavior

- Running `bash run_repro.sh` exits with code 0 after reproducing the bug marker in `repro_stdout.log`. `repro_stderr.log` shows `TypeError: 'int' object is not subscriptable` at `codebase/sentence_transformers/SentenceTransformer.py:704` in the `output_value=None` prompt branch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
