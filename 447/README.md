# Bug 447

This folder is a self-contained reproduction bundle for
`https://github.com/pyg-team/pytorch_geometric/issues/10159`.

Reused source inputs:
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

Run the repro locally with:
`bash run_repro.sh`

Outcome in this environment:
- the reported mismatch did not reproduce on CPU
- `first_max_diff=0.0`
- `rest_max_diff=0.0`
