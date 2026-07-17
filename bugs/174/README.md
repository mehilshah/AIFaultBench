# Bug 174

Repro bundle for Lark issue 1355.

Files:
- `bug_report.txt`: original report
- `codebase/`: local source snapshot
- `repro.py`: minimal reproducer
- `requirements.txt`: environment dependencies
- `setup_env.sh`: virtualenv bootstrap
- `run_repro.sh`: repro entrypoint
- `manifest.json`: bundle metadata

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```

Expected result:
- `repro.py` raises `GrammarError` while loading the report grammar.
