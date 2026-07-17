# Bug 049

This folder contains a self-contained repro bundle for fairseq issue 4622.

Observed outcome in this snapshot:
- `RelPositionMultiHeadedAttention` is already patched.
- `pos_bias_u` and `pos_bias_v` are initialized with Xavier, so the uninitialized-bias failure from the issue report does not reproduce here.

Files:
- `bug_report.txt`: recovered issue description
- `codebase/`: local fairseq snapshot used for verification
- `repro.py`: minimal runtime check
- `requirements.txt`: minimal Python dependencies
- `setup_env.sh`: optional virtualenv bootstrap
- `run_repro.sh`: executes the repro and captures logs
- `reproduction.json`: schema-constrained result
- `repro_stdout.log`: captured stdout from the repro
- `repro_stderr.log`: captured stderr from the repro

Run locally:
```bash
bash run_repro.sh
```

The repro script writes `reproduction.json` after checking the module initialization.
