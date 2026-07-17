# Bug 343

This folder is a self-contained reproduction bundle for SDV issue 2852.

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

Reproduction command:
`./setup_env.sh && ./run_repro.sh`

Summary:
- issue URL: `https://github.com/sdv-dev/SDV/issues/2852`
- commit hash: `db5bcb22a86ca2a1f790f531f0df4a7bd6cc737d`
- library: `SDV`
- library version: `1.35.1.dev0`
- result: reproducible here by chaining `FixedCombinations` with a row-dropping programmable constraint that leaves the index sparse, which triggers `pandas.errors.IndexingError` inside `reverse_transform_constraints`
