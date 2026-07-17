# Bug 418

Reproduction bundle for PyG issue `#10163`, pinned to commit `69193c895fe721fb45e63985bb79e8d130ee7782`.

## What fails

`TransformerConv(bias=False)` still creates biased `lin_key`, `lin_query`, and `lin_value` submodules, while `lin_skip` correctly respects `bias=False`.

## Files

- `bug_report.txt`: original issue report
- `codebase/torch_geometric/nn/conv/transformer_conv.py`: source snapshot of the affected module
- `repro.py`: runtime check for the bias mismatch
- `requirements.txt`: Python dependencies for the repro environment
- `setup_env.sh`: creates a virtualenv and installs dependencies
- `run_repro.sh`: runs the repro

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is expected to fail with an assertion showing that the three attention projections still have bias parameters when `bias=False`.
