# Bug 552

This folder reproduces the Pyro MCMC documentation failure reported in:
`https://github.com/pyro-ppl/pyro/issues/3018`

What is included:
- `bug_report.txt`: the recovered issue report
- `codebase/`: the local Pyro source snapshot
- `repro.py`: minimal reproduction script
- `requirements.txt`: pinned runtime dependencies for Python 3.10
- `setup_env.sh`: creates a clean virtual environment and installs deps
- `run_repro.sh`: runs the reproduction and writes logs
- `reproduction.json`: schema-constrained result
- `repro_stdout.log` and `repro_stderr.log`: captured output from the failing run

Reproduction command:
`./run_repro.sh`
