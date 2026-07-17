# Bug 569

This folder contains a minimal reproduction for the Minimax M3 attention block-selection bug.

## What the repro checks

The issue report points to this logic in the local Transformers source:

`scores.amax(dim=-1).amax(dim=1)`

The second `amax(dim=1)` collapses the head axis and produces one shared block ranking for all heads.
The reference behavior keeps per-head block rankings separate.

## Files

- `bug_report.txt`: original issue report
- `codebase/`: local Transformers source snapshot
- `repro.py`: synthetic tensor repro
- `requirements.txt`: minimal runtime dependencies
- `setup_env.sh`: installs the repro dependencies
- `run_repro.sh`: runs the repro script
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured command output

## Run

```bash
bash run_repro.sh
```

The script prints a JSON blob showing that head 0 and head 1 select different blocks in the reference
calculation, while the current implementation collapses them into one shared choice.
