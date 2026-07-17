# Bug 236

This folder contains a self-contained reproduction bundle for Equinox issue 898.

What is included:
- `bug_report.txt`: the original issue description
- `codebase/`: the checked-out Equinox snapshot
- `repro.py`: the minimal reproducer
- `requirements.txt`: pinned runtime dependencies
- `setup_env.sh`: creates the local virtualenv and installs dependencies
- `run_repro.sh`: executes the repro and writes logs
- `reproduction.json`: machine-readable reproduction result
- `repro_stdout.log` and `repro_stderr.log`: command output from the repro run

Observed result:
- The bug is reproducible in this snapshot with `jax==0.4.38`.
- `jnp.asarray(MyArray(...))` succeeds.
- `jnp.asarray(MyEqxArray(...))` raises `TypeError: Unexpected input type for array: <class '__main__.MyEqxArray'>`.

Reproduction command:
```bash
bash run_repro.sh
```
