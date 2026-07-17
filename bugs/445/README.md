# Bug 445

This folder is the reusable standardized benchmark input for this bug.

Reused inputs:
- `bug_report.txt`
- `codebase/` from `pyro-ppl/pyro@dd4e0f81b4ddceb82ebd663b20333e175ce27c2a`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Outcome:
- The reported `AttributeError` is not reproducible in this snapshot.
- `pyro.optim.ExponentialLR` exists and resolves to a wrapper function.

Reproduction command:
`bash run_repro.sh`
