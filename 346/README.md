# Bug 346

Regression repro for the Transformers v5 pipeline generator regression described in `bug_report.txt`.

## What it checks

`repro.py` builds a tiny `transformers.Pipeline` subclass and passes a generator into `Pipeline.__call__()`.
The current code path converts the generator to a list immediately, so all `yield:*` events happen before the
first `preprocess:*` event.

## How to run

```bash
bash run_repro.sh
```

This script:

1. Creates a local `.venv`
2. Installs the minimal CPU-only Python dependencies from `requirements.txt`
3. Runs `repro.py`
4. Writes logs to `repro_stdout.log` and `repro_stderr.log`

## Expected outcome

The bug is reproducible in this folder. The stdout log should show:

`EVENTS ['yield:0', 'yield:1', 'yield:2', 'preprocess:item-0', ...]`

That ordering proves the generator was fully consumed before the pipeline started processing items.
