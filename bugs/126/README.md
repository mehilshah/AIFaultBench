# Bug 126

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- issue URL: `https://github.com/exaloop/codon/issues/506`
- observed locally with `codon 0.19.6`
- minimal trigger: `arr = [1, 2]; print(*arr)`
- failure: `error: argument after * must be a tuple, not 'List[int]'`

Reproduction command:
`bash run_repro.sh`
