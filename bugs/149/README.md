# Reproduction Bundle

This bundle reproduces the missing `requests` dependency reported for `sentence-transformers` 5.2.1.

## What it does

`repro.py` loads `codebase/sentence_transformers/util/file_io.py` directly from the local checkout.
That module imports `requests` at top level, but the package metadata only installs `huggingface_hub`.

## Expected result

The repro fails with:

```text
ModuleNotFoundError: No module named 'requests'
```

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
cat repro_stdout.log
cat repro_stderr.log
```
