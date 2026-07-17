# Bug 618

This folder is a standalone repro bundle for SDV issue 2702.

What is reproduced:
- `DayZSynthesizer.create_parameters` crashes instead of falling back to defaults when it sees an empty table or an all-null numerical/datetime column.

Relevant inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
```bash
bash setup_env.sh
bash run_repro.sh
```

Observed failures in this checkout:
- empty table with detected metadata: `AttributeError: 'float' object has no attribute 'item'`
- all-null numerical column with explicit metadata: `AttributeError: 'float' object has no attribute 'item'`
- all-null datetime column with explicit metadata: `ValueError: NaTType does not support strftime`
