# Bug 373 Reproduction Bundle

This folder contains a minimal reproduction for SDV issue 2839.

Bug summary:
- `Metadata.visualize()` uses the table primary key in relationship labels.
- It should use the relationship's `parent_primary_key` value instead.

Expected failure mode:
- The rendered graph source shows `fk → pk` for the relationship below.
- The correct label would be `fk → other`.

Files:
- `repro.py`: standalone repro script
- `requirements.txt`: Python dependencies for the repro
- `setup_env.sh`: installs the repro dependencies
- `run_repro.sh`: runs the repro and records logs
- `manifest.json`: metadata for this benchmark folder
- `reproduction.json`: structured result written after running the repro
- `repro_stdout.log`, `repro_stderr.log`: command output logs
